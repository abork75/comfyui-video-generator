# -*- coding: utf-8 -*-
"""
API router for media operations:
    GET  /api/media/frame    — serve a frame JPEG
    GET  /api/media/video    — serve a transition/chain MP4
    POST /api/media/archive  — rename a generated file (add _ver timestamp)
    GET  /api/media/versions — list all versions (current + archived)
    POST /api/media/trash    — move a file to the Windows Recycle Bin
"""

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.services.media_service import (
    resolve_frame,
    resolve_video,
    resolve_video_thumb,
    resolve_source_video,
    archive_video,
    batch_archive_videos,
    clear_frame_cache,
    get_transition_status,
    list_file_versions,
    restore_video,
    trash_video,
    upload_source_file,
    MAX_UPLOAD_BYTES,
)

router = APIRouter(prefix="/api/media", tags=["media"])


_FRAME_MEDIA_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png",  ".webp": "image/webp",
    ".gif": "image/gif",  ".bmp": "image/bmp",
    ".tiff": "image/tiff", ".tif": "image/tiff",
}


@router.get("/frame")
async def get_frame(run: str, file: str, kind: str = "start"):
    """
    Serve a frame image.
    Returns extracted thumbnail if it exists, otherwise falls back to
    the original source image (e.g. after source file replacement).
    ?run=RUN_xxx.py&file=09.51. full street.png&kind=start|end
    """
    from pathlib import Path as _Path
    path = resolve_frame(run, file, kind)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Frame not found: {file} ({kind})")
    media_type = _FRAME_MEDIA_TYPES.get(_Path(path).suffix.lower(), "image/jpeg")
    return FileResponse(str(path), media_type=media_type)


@router.get("/video")
async def get_video(run: str, name: str):
    """
    Serve a transition or chain MP4.
    ?run=RUN_xxx.py&name=09.51._09.53._transition.mp4
    """
    path = resolve_video(run, name)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Video not found: {name}")
    return FileResponse(str(path), media_type="video/mp4")


@router.post("/archive")
async def archive(request: Request):
    """
    Archive (rename with _verYYMMDDHHmmss) a generated transition/chain file.
    Body JSON: {"run": "RUN_xxx.py", "name": "film_transition.mp4"}
    """
    try:
        body = await request.json()
        run  = str(body.get("run",  ""))
        name = str(body.get("name", ""))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")

    result = archive_video(run, name)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/batch-archive")
async def batch_archive(request: Request):
    """
    Archive multiple files using a single shared timestamp (batch consistency).
    Body JSON: {"run": "RUN_xxx.yaml", "names": ["a.mp4", "b.mp4", ...]}
    Returns: {"ts": "...", "results": [{"name": ..., "ok": ..., "new_name": ...}, ...]}
    """
    try:
        body  = await request.json()
        run   = str(body.get("run",  ""))
        names = body.get("names", [])
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not isinstance(names, list) or not names:
        raise HTTPException(status_code=422, detail="run and names[] are required")

    return batch_archive_videos(run, [str(n) for n in names if n])


@router.get("/versions")
async def get_versions(run: str, name: str):
    """
    List all versions of a video: the canonical current file + archived _verXXX files.
    ?run=RUN_xxx.py&name=A_B_transition.mp4
    """
    data = list_file_versions(run, name)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Project not found for run: {run}")
    return data


@router.post("/restore")
async def restore(request: Request):
    """
    Restore an archived _verXXX file as the current canonical file.
    Body JSON: {"run": "RUN_xxx.py", "name": "film_transition_ver240101120000.mp4"}
    """
    try:
        body = await request.json()
        run  = str(body.get("run",  ""))
        name = str(body.get("name", ""))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")

    result = restore_video(run, name)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/trash")
async def trash(request: Request):
    """
    Move a video file to the Windows Recycle Bin.
    Body JSON: {"run": "RUN_xxx.py", "name": "film_transition_ver240101120000.mp4"}
    """
    try:
        body = await request.json()
        run  = str(body.get("run",  ""))
        name = str(body.get("name", ""))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")

    result = trash_video(run, name)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/dimensions")
async def get_dimensions(run: str, file: str):
    """
    Return actual pixel dimensions of a source image or video file.
    GET /api/media/dimensions?run=RUN_xxx.yaml&file=09.51.+full+street.png
    Response: {"width": 1920, "height": 1080, "ratio": 0.5625}
    """
    from pathlib import Path as _Path
    path = resolve_frame(run, file, kind="start")
    if path is None:
        raise HTTPException(status_code=404, detail=f"File not found: {file}")
    p = _Path(path)
    suffix = p.suffix.lower()
    try:
        if suffix in (".mp4", ".avi", ".mov", ".mkv", ".webm"):
            import cv2
            cap = cv2.VideoCapture(str(p))
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
        else:
            from PIL import Image
            with Image.open(str(p)) as img:
                w, h = img.size
        ratio = round(h / w, 3) if w else 0
        return {"width": w, "height": h, "ratio": ratio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/loras")
async def list_loras(dir: str = "WAN2.2_LoraSet"):
    """
    Return list of .safetensors filenames from D:\\ComfyUI\\models\\loras\\{dir}
    GET /api/media/loras?dir=WAN2.2_LoraSet
    Response: {"files": ["lora_a.safetensors", ...]}
    """
    import os as _os
    base = _os.path.join(r"D:\ComfyUI\models\loras", dir)
    if not _os.path.isdir(base):
        raise HTTPException(status_code=404, detail=f"Directory not found: {base}")
    files = sorted(
        dir + "/" + f   # ComfyUI expects subdir/filename relative to models/loras/
        for f in _os.listdir(base)
        if f.lower().endswith(".safetensors")
    )
    return {"files": files}


@router.post("/crop-to-ratio")
async def crop_to_ratio(request: Request):
    """
    Crop or resize a source image to the target aspect ratio + dimensions.
    Archives original as _beforecrop before modifying.
    Body: {run, file, width, height, mode: "resize"|"crop"}
    """
    from pathlib import Path as _Path
    from PIL import Image as _Image
    import shutil as _shutil
    from datetime import datetime as _dt

    body = await request.json()
    run    = body.get('run')
    file   = body.get('file')
    width  = int(body.get('width', 0))
    height = int(body.get('height', 0))
    mode   = body.get('mode', 'crop')

    if not run or not file:
        raise HTTPException(status_code=400, detail="Brak run lub file")
    if width < 64 or height < 64:
        raise HTTPException(status_code=400, detail="Wymiary za małe (min 64px)")

    path = resolve_frame(run, file, kind="start")
    if path is None:
        raise HTTPException(status_code=404, detail=f"Plik nie znaleziony: {file}")

    # For MP4 files resolve_frame returned the cached thumbnail; we need the actual source file
    from app.services.media_service import _project_folder as _get_pf
    pf = _get_pf(run)
    if pf is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono project folder")

    ext = _Path(file).suffix.lower()
    p   = pf / file   # actual source file (image or video)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Plik nie znaleziony: {file}")

    ts     = _dt.now().strftime("%y%m%d%H%M%S")
    backup = p.parent / f"{p.stem}_ver{ts}_beforecrop{p.suffix}"

    if ext == '.mp4':
        # ── Video crop via ffmpeg ──────────────────────────────────────
        import subprocess as _sp, json as _json
        # Get source dimensions via ffprobe
        probe = _sp.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=width,height', '-of', 'json', str(p)],
            capture_output=True, timeout=15,
        )
        if probe.returncode != 0:
            raise HTTPException(status_code=500, detail='ffprobe failed: ' + probe.stderr.decode())
        dims = _json.loads(probe.stdout)['streams'][0]
        src_w, src_h = dims['width'], dims['height']

        if mode == 'resize':
            vf = f'scale={width}:{height}'
        else:
            # center crop (same logic as PIL path below)
            target_ratio = width / height
            src_ratio    = src_w / src_h
            if src_ratio > target_ratio:
                new_w = int(src_h * target_ratio)
                x     = (src_w - new_w) // 2
                vf    = f'crop={new_w}:{src_h}:{x}:0,scale={width}:{height}'
            elif src_ratio < target_ratio:
                new_h = int(src_w / target_ratio)
                y     = (src_h - new_h) // 2
                vf    = f'crop={src_w}:{new_h}:0:{y},scale={width}:{height}'
            else:
                vf = f'scale={width}:{height}'

        _shutil.copy2(str(p), str(backup))
        tmp = p.parent / f"_tmp_crop_{p.name}"
        try:
            cmd = [
                'ffmpeg', '-y', '-i', str(p),
                '-vf', vf,
                '-c:v', 'libx264', '-crf', '18', '-c:a', 'copy',
                str(tmp),
            ]
            r = _sp.run(cmd, capture_output=True, timeout=300)
            if r.returncode != 0:
                raise RuntimeError(r.stderr.decode())
            p.unlink()
            tmp.rename(p)
            # Invalidate cached thumbnail so it's re-extracted on next view
            from app.services.media_service import frame_path as _frame_path
            cached_thumb = _frame_path(pf, file, 'start')
            if cached_thumb.exists():
                cached_thumb.unlink()
        except Exception as e:
            if tmp.exists():
                tmp.unlink()
            raise HTTPException(status_code=500, detail=str(e))
        return {"ok": True}

    # ── Image crop via PIL ────────────────────────────────────────────
    if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'):
        raise HTTPException(status_code=400, detail="Crop działa tylko na obrazkach lub MP4")

    try:
        with _Image.open(str(p)) as img:
            img = img.convert('RGB') if img.mode not in ('RGB', 'RGBA', 'L') else img.copy()
            src_w, src_h = img.size

            if mode == 'resize':
                result = img.resize((width, height), _Image.LANCZOS)
            else:
                # center crop to target ratio, then resize to exact dimensions
                target_ratio = width / height
                src_ratio    = src_w / src_h
                if src_ratio > target_ratio:
                    # too wide — crop left/right equally
                    new_w = int(src_h * target_ratio)
                    left  = (src_w - new_w) // 2
                    img   = img.crop((left, 0, left + new_w, src_h))
                elif src_ratio < target_ratio:
                    # too tall — crop top/bottom equally
                    new_h = int(src_w / target_ratio)
                    top   = (src_h - new_h) // 2
                    img   = img.crop((0, top, src_w, top + new_h))
                result = img.resize((width, height), _Image.LANCZOS)

        _shutil.copy2(str(p), str(backup))

        # Save via temp → rename (no partial-write risk)
        tmp = p.parent / f"_tmp_crop_{p.name}"
        save_kwargs = {'quality': 95} if ext in ('.jpg', '.jpeg') else {}
        result.save(str(tmp), **save_kwargs)
        p.unlink()
        tmp.rename(p)

        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear-frame-cache")
async def clear_frame_cache_endpoint(request: Request):
    """
    Delete the frames/ thumbnail cache for a run so all thumbnails
    are re-extracted from source on next request.
    Body JSON: {"run": "RUN_xxx.yaml"}
    """
    try:
        body = await request.json()
        run = str(body.get("run", ""))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")
    if not run:
        raise HTTPException(status_code=422, detail="run is required")
    result = clear_frame_cache(run)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Błąd czyszczenia cache"))
    return result


@router.get("/source-video")
async def get_source_video(run: str, name: str):
    """
    Serve a source video file (external mp4) from PROJECT_FOLDER.
    Used for playback of imported video clips in the FLOW view.
    ?run=RUN_xxx.yaml&name=my_clip.mp4
    """
    path = resolve_source_video(run, name)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Source video not found: {name}")
    return FileResponse(str(path), media_type="video/mp4")


@router.get("/video-thumb")
async def get_video_thumb(run: str, name: str):
    """
    Serve a thumbnail (first frame) for a generated transition/chain mp4.
    Extracts and caches via ffmpeg on first call.
    ?run=RUN_xxx.yaml&name=A_B_transition.mp4
    """
    path = resolve_video_thumb(run, name)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Thumbnail not found: {name}")
    return FileResponse(str(path), media_type="image/jpeg")


@router.post("/upload-source")
async def upload_source(
    run:  str        = Form(...),
    name: str        = Form(...),
    file: UploadFile = File(...),
):
    """
    Replace a source file (image/video) in PROJECT_FOLDER.
    Old file is moved to PROJECT_FOLDER/source_backup/.
    Cached frame thumbnails for this file are deleted.
    """
    content = await file.read()
    result = upload_source_file(run, name, content)
    if not result["ok"]:
        status = 413 if "za duży" in result["error"] else 400
        raise HTTPException(status_code=status, detail=result["error"])
    return result


@router.post("/audio-smooth")
async def audio_smooth(request: Request):
    """
    Apply fade-in/out + loudnorm to audio tracks of selected clips in-place.
    Body: { "run": "RUN_xxx.yaml", "names": ["a.mp4", "b.mp4", ...],
            "fade_pct": 0.15, "loudnorm": true }
    First clip: fade-out only. Last clip: fade-in only. Middle: both.
    """
    import asyncio
    from pathlib import Path as _Path
    from app.services.process_service import process_service
    from app.services.yaml_service import get_yaml_globals
    from utils.video_utils import smooth_audio_clip, get_video_info

    RUNS_FOLDER_local = _Path(__file__).parent.parent.parent / "RUNS"

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Nieprawidłowy JSON")

    run: str = (body.get("run") or "").strip()
    names: list = body.get("names") or []
    fade_pct: float = float(body.get("fade_pct") or 0.15)
    do_loudnorm: bool = bool(body.get("loudnorm", True))

    if not run or not names:
        raise HTTPException(status_code=400, detail="Brak parametrów run/names")

    yaml_path = RUNS_FOLDER_local / run
    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")

    project_folder = _Path(globals_data.get("project_folder") or "")
    transitions_dir = project_folder / "transitions"

    class _Log:
        def info(self, m):    process_service.log_sys(f"ℹ️  {m}")
        def success(self, m): process_service.log_sys(f"✅ {m}")
        def warning(self, m): process_service.log_sys(f"⚠️  {m}")
        def error(self, m):   process_service.log_sys(f"❌ {m}")

    def _resolve(name: str) -> Path | None:
        for p in [transitions_dir / name, transitions_dir / "chains" / name]:
            if p.exists():
                return p
        return None

    async def _run_smooth():
        logger = _Log()
        valid = [(n, _resolve(n)) for n in names]
        valid = [(n, p) for n, p in valid if p is not None]
        if not valid:
            logger.warning("Brak plików do przetworzenia")
            return
        logger.info(f"🔊 Uspójnianie audio: {len(valid)} plików...")
        n_total = len(valid)
        done = 0
        loop = asyncio.get_running_loop()
        for i, (name, path) in enumerate(valid):
            info = get_video_info(path)
            dur = info.get("duration") or 0.0
            fade_s = min(dur * fade_pct, 0.5) if dur > 0 else 0.0
            fade_in  = fade_s if i > 0           else 0.0
            fade_out = fade_s if i < n_total - 1 else 0.0
            logger.info(f"  [{i+1}/{n_total}] {name} (fi={fade_in:.2f}s fo={fade_out:.2f}s)")
            ok = await loop.run_in_executor(
                None,
                lambda p=path, fi=fade_in, fo=fade_out: smooth_audio_clip(
                    p, fade_in_s=fi, fade_out_s=fo, loudnorm=do_loudnorm, logger=logger
                ),
            )
            if ok:
                done += 1
        logger.success(f"🔊 Uspójnianie zakończone ({done}/{n_total} plików)")

    asyncio.create_task(_run_smooth())
    return {"ok": True, "count": len(names)}


@router.post("/batch-ensure-fps")
async def batch_ensure_fps(request: Request):
    """
    Convert selected transition videos to 24fps in-place using ffmpeg.
    Runs in background; progress logged to the WebSocket log panel.
    Body: { "run": "run.yaml", "names": ["a.mp4", "b.mp4", ...] }
    """
    import asyncio
    from pathlib import Path
    from app.services.process_service import process_service
    from app.services.yaml_service import get_yaml_globals
    from utils.video_utils import ensure_24fps

    RUNS_FOLDER = Path(__file__).parent.parent.parent / "RUNS"

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Nieprawidłowy JSON")

    run: str = (body.get("run") or "").strip()
    names: list = body.get("names") or []
    if not run or not names:
        raise HTTPException(status_code=400, detail="Brak parametrów run/names")

    yaml_path = RUNS_FOLDER / run
    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")

    project_folder = Path(globals_data.get("project_folder") or "")
    if not project_folder.exists():
        raise HTTPException(status_code=400, detail=f"Folder projektu nie istnieje: {project_folder}")

    transitions_dir = project_folder / "transitions"

    class _Log:
        def info(self, m):    process_service.log_sys(f"ℹ️  {m}")
        def success(self, m): process_service.log_sys(f"✅ {m}")
        def warning(self, m): process_service.log_sys(f"⚠️  {m}")
        def error(self, m):   process_service.log_sys(f"❌ {m}")

    def _resolve(name: str) -> Path | None:
        # Regular transition
        p = transitions_dir / name
        if p.exists():
            return p
        # Chain clip (stored in transitions/chains/)
        p2 = transitions_dir / "chains" / name
        if p2.exists():
            return p2
        return None

    async def _run_batch():
        logger = _Log()
        logger.info(f"Konwersja FPS: {len(names)} plików...")
        done = 0
        for name in names:
            path = _resolve(name)
            if path is None:
                logger.warning(f"Pominięto (brak pliku): {name}")
                continue
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda p=path: ensure_24fps(p, logger))
            done += 1
        logger.success(f"Konwersja FPS zakończona ({done}/{len(names)} plików)")

    asyncio.create_task(_run_batch())
    return {"ok": True, "count": len(names)}
