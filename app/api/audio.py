# -*- coding: utf-8 -*-
"""
API router for MMAudio — add/regenerate audio for an existing transition video.

POST /api/audio/{run_filename}
  body: { "name": "transition.mp4", "audio_prompt"?: "...", "audio_negative_prompt"?: "..." }
  Runs MMAudio in background; progress appears in log panel via WebSocket.
"""

import asyncio
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request

from app.services.app_config_service import get_backend as cfg_get_backend
from app.services.process_service import process_service
from app.services.yaml_service import get_yaml_globals

PROJECT_ROOT = Path(__file__).parent.parent.parent
RUNS_FOLDER  = PROJECT_ROOT / "RUNS"

_FALLBACK_AUDIO_PROMPT         = "foley sound effects, physical interactions, footsteps, cloth movement, object handling, impacts, synchronized with video, crisp, realistic"
_FALLBACK_AUDIO_NEG_PROMPT     = "music, melody, ambient drone, continuous atmosphere, background noise, reverb, sustained tones, low quality, distortion"
_FALLBACK_AMBIENT_PROMPT       = "natural environment ambience, continuous atmospheric sound, wind, room tone, immersive background, seamless"
_FALLBACK_AMBIENT_NEG_PROMPT   = "music, melody, instruments, sudden impacts, foley, footsteps, cloth, synchronized effects, stingers, low quality, distortion"

router = APIRouter(prefix="/api/audio", tags=["audio"])


class _LogBridge:
    """Forward logger calls to the WebSocket log panel."""
    def info(self, msg):    process_service.log_sys(f"ℹ️  {msg}")
    def success(self, msg): process_service.log_sys(f"✅ {msg}")
    def warning(self, msg): process_service.log_sys(f"⚠️  {msg}")
    def error(self, msg):   process_service.log_sys(f"❌ {msg}")


async def _run_audio_bg(
    video_path: Path,
    prompt: str,
    negative_prompt: str,
    api_url: str,
    duration: float,
) -> None:
    from utils.mmaudio_utils import add_audio as _add_audio
    logger = _LogBridge()
    logger.info(f"MMAudio re-generacja: {video_path.name}")
    loop = asyncio.get_running_loop()
    ok = await loop.run_in_executor(None, lambda: _add_audio(
        video_path=video_path,
        prompt=prompt,
        negative_prompt=negative_prompt,
        api_url=api_url,
        duration=duration,
        steps=25,
        cfg=4.5,
        seed=-1,
        logger=logger,
    ))
    if not ok:
        process_service.log_sys(f"⚠️  MMAudio: nie dodano audio do {video_path.name}")
    else:
        process_service.log_sys(f"[AUDIO_READY] {video_path.name}")


@router.post("/{run_filename}")
async def add_audio_to_clip(run_filename: str, request: Request):
    """
    Regenerate audio for an already-generated transition video using MMAudio.
    Runs in background — progress streamed to log panel via WebSocket.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    name: str = (body.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Brak parametru 'name'")

    yaml_path = RUNS_FOLDER / run_filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik nie istnieje: {run_filename}")

    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")

    project_folder = Path(globals_data.get("project_folder") or "")
    if not project_folder or not project_folder.exists():
        raise HTTPException(status_code=400, detail=f"Folder projektu nie istnieje: {project_folder}")

    video_path = project_folder / "transitions" / name
    if not video_path.exists():
        video_path = project_folder / "transitions" / "chains" / name
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik wideo nie istnieje: {name}")

    # Audio prompts: request body → YAML defaults → system fallback
    defs = globals_data.get("defaults") or {}
    audio_prompt = (
        body.get("audio_prompt")
        or defs.get("default_audio_prompt")
        or _FALLBACK_AUDIO_PROMPT
    )
    audio_negative_prompt = (
        body.get("audio_negative_prompt")
        or defs.get("default_audio_negative_prompt")
        or _FALLBACK_AUDIO_NEG_PROMPT
    )

    # api_url: YAML linux_backend → app_config
    lb = globals_data.get("linux_backend") or {}
    api_url = lb.get("api_url") or cfg_get_backend("linux").get("api_url", "http://127.0.0.1:8189")

    # Video duration via ffprobe/OpenCV
    try:
        from utils.video_utils import get_video_info
        info = get_video_info(video_path)
        duration = float(info["duration"]) if info.get("duration") and info["duration"] > 0 else 10.0
    except Exception:
        duration = 10.0

    asyncio.create_task(_run_audio_bg(video_path, audio_prompt, audio_negative_prompt, api_url, duration))
    return {"ok": True}


# ── Sequence ambient audio ───────────────────────────────────────────────────

async def _run_sequence_audio_bg(
    clips: list[Path],
    output_mp3: Path,
    prompt: str,
    negative_prompt: str,
    api_url: str,
    clip_names: list[str],
    clip_durations: list[float],
    *,
    prompt_used: str = "",
    negative_prompt_used: str = "",
) -> None:
    import json, subprocess, tempfile
    from utils.mmaudio_utils import add_audio as _add_audio
    logger = _LogBridge()

    # Build ffmpeg concat list
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        for p in clips:
            f.write(f"file '{str(p).replace(chr(39), chr(39)+chr(92)+chr(39)+chr(39))}'\n")
        concat_list = Path(f.name)

    concat_video = output_mp3.parent / (output_mp3.stem + '_concat_tmp.mp4')
    try:
        logger.info(f"Concat {len(clips)} klipów...")
        r = subprocess.run(
            ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_list),
             '-c', 'copy', str(concat_video)],
            capture_output=True, timeout=300,
        )
        if r.returncode != 0:
            logger.error(f"ffmpeg concat failed: {r.stderr.decode()[:200]}")
            return

        from utils.video_utils import get_video_info
        info = get_video_info(concat_video)
        duration = float(info.get("duration") or 10.0)

        logger.info(f"MMAudio na {duration:.1f}s sekwencji...")
        ok = await asyncio.get_running_loop().run_in_executor(None, lambda: _add_audio(
            video_path=concat_video,
            prompt=prompt,
            negative_prompt=negative_prompt,
            api_url=api_url,
            duration=duration,
            steps=25,
            cfg=4.5,
            seed=-1,
            logger=logger,
        ))
        if not ok:
            logger.error("MMAudio nie wygenerował audio")
            return

        # Extract audio → mp3
        r2 = subprocess.run(
            ['ffmpeg', '-y', '-i', str(concat_video), '-vn', '-q:a', '2', str(output_mp3)],
            capture_output=True, timeout=120,
        )
        if r2.returncode != 0:
            logger.error(f"ffmpeg audio extract failed: {r2.stderr.decode()[:200]}")
            return

        # Save sidecar JSON with clip metadata for sync
        offsets = []
        acc = 0.0
        for d in clip_durations:
            offsets.append(round(acc, 4))
            acc += d
        sidecar = output_mp3.with_suffix('.json')
        sidecar.write_text(json.dumps({
            "clips": clip_names,
            "clip_durations": [round(d, 4) for d in clip_durations],
            "offsets": offsets,
            "prompt_used": prompt_used or prompt,
            "negative_prompt_used": negative_prompt_used or negative_prompt,
        }, ensure_ascii=False, indent=2), encoding='utf-8')

        logger.success(f"Ambient audio zapisane: {output_mp3.name}")
        process_service.log_sys(f"[AMBIENT_READY] {output_mp3.name}")

    finally:
        concat_list.unlink(missing_ok=True)
        concat_video.unlink(missing_ok=True)


def _podklad_dir(project_folder: Path) -> Path:
    d = project_folder / "transitions" / "podklad"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ambient_path(project_folder: Path, filename: str) -> Path | None:
    """Resolve ambient mp3: check transitions/podklad/ then project root (legacy)."""
    p = project_folder / "transitions" / "podklad" / filename
    if p.exists():
        return p
    p2 = project_folder / filename
    if p2.exists():
        return p2
    return None


@router.get("/ambient/{run_filename}")
async def list_ambient_files(run_filename: str):
    """List sequence_ambient_*.mp3 files (from transitions/podklad/ and project root legacy)."""
    import json
    yaml_path = RUNS_FOLDER / run_filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik nie istnieje: {run_filename}")
    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")
    project_folder = Path(globals_data.get("project_folder") or "")
    if not project_folder or not project_folder.exists():
        return {"files": []}

    # Collect from both locations; podklad/ takes priority (exclude archiwum subdir)
    seen: set[str] = set()
    all_files: list[Path] = []
    podklad = project_folder / "transitions" / "podklad"
    archivum = podklad / "archiwum"
    if podklad.exists():
        for p in podklad.glob("*.mp3"):
            if archivum in p.parents:
                continue  # skip archived files
            all_files.append(p)
            seen.add(p.name)
    for p in project_folder.glob("sequence_ambient_*.mp3"):
        if p.name not in seen:
            all_files.append(p)

    all_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    result = []
    for p in all_files:
        sidecar = p.with_suffix('.json')
        clips, offsets = [], []
        if sidecar.exists():
            try:
                data = json.loads(sidecar.read_text(encoding='utf-8'))
                clips = data.get("clips", [])
                offsets = data.get("offsets", [])
            except Exception:
                pass
        result.append({
            "name": p.name,
            "size_mb": round(p.stat().st_size / 1_048_576, 2),
            "clips": clips,
            "offsets": offsets,
        })
    return {"files": result}


@router.get("/ambient/{run_filename}/{filename}")
async def serve_ambient_file(run_filename: str, filename: str):
    """Serve a sequence_ambient_*.mp3 file."""
    from fastapi.responses import FileResponse
    yaml_path = RUNS_FOLDER / run_filename
    globals_data = get_yaml_globals(yaml_path) if yaml_path.exists() else None
    if not globals_data:
        raise HTTPException(status_code=404)
    if not filename.endswith(".mp3"):
        raise HTTPException(status_code=404)
    project_folder = Path(globals_data.get("project_folder") or "")
    p = _ambient_path(project_folder, filename)
    if not p:
        raise HTTPException(status_code=404)
    return FileResponse(str(p), media_type="audio/mpeg")


@router.delete("/ambient/{run_filename}/{filename}")
async def delete_ambient_file(run_filename: str, filename: str):
    """Delete a sequence_ambient_*.mp3 file and its sidecar JSON."""
    yaml_path = RUNS_FOLDER / run_filename
    globals_data = get_yaml_globals(yaml_path) if yaml_path.exists() else None
    if not globals_data:
        raise HTTPException(status_code=404)
    if not filename.endswith(".mp3"):
        raise HTTPException(status_code=404)
    project_folder = Path(globals_data.get("project_folder") or "")
    p = _ambient_path(project_folder, filename)
    if not p:
        raise HTTPException(status_code=404)
    p.unlink()
    p.with_suffix('.json').unlink(missing_ok=True)
    return {"ok": True}


@router.post("/ambient/{run_filename}/archive/{filename}")
async def archive_ambient_file(run_filename: str, filename: str):
    """Move ambient mp3+json to /podklad/archiwum/ instead of deleting."""
    yaml_path = RUNS_FOLDER / run_filename
    globals_data = get_yaml_globals(yaml_path) if yaml_path.exists() else None
    if not globals_data:
        raise HTTPException(status_code=404)
    if not filename.endswith(".mp3"):
        raise HTTPException(status_code=404)
    project_folder = Path(globals_data.get("project_folder") or "")
    p = _ambient_path(project_folder, filename)
    if not p:
        raise HTTPException(status_code=404)
    archivum = project_folder / "transitions" / "podklad" / "archiwum"
    archivum.mkdir(parents=True, exist_ok=True)
    dst = archivum / filename
    # Avoid overwrite in archive
    if dst.exists():
        stem, suffix = filename.rsplit('.', 1)
        import time
        dst = archivum / f"{stem}_{int(time.time())}.{suffix}"
    p.rename(dst)
    sidecar = p.with_suffix('.json')
    if sidecar.exists():
        sidecar.rename(dst.with_suffix('.json'))
    return {"ok": True}


@router.post("/sequence/{run_filename}")
async def generate_sequence_audio(run_filename: str, request: Request):
    """
    Generate continuous ambient audio for a sequence of clips.
    Concatenates clips, runs MMAudio, extracts audio → sequence_ambient_XXXXXX.mp3
    Body: { "clips": ["a_b_transition.mp4", ...], "audio_prompt"?: "...", "audio_negative_prompt"?: "..." }
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    clip_names: list[str] = body.get("clips") or []
    if not clip_names:
        raise HTTPException(status_code=400, detail="Brak listy klipów")

    yaml_path = RUNS_FOLDER / run_filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik nie istnieje: {run_filename}")

    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")

    project_folder = Path(globals_data.get("project_folder") or "")
    if not project_folder or not project_folder.exists():
        raise HTTPException(status_code=400, detail=f"Folder projektu nie istnieje")

    from app.services.media_service import resolve_video
    clips: list[Path] = []
    for name in clip_names:
        p = resolve_video(run_filename, name)
        if p and p.exists():
            clips.append(p)
        else:
            raise HTTPException(status_code=404, detail=f"Klip nie znaleziony: {name}")

    defs = globals_data.get("defaults") or {}
    # Ambient prompt hierarchy: request body → YAML ambient default → YAML FX default → system ambient fallback
    audio_prompt = (
        body.get("audio_prompt")
        or defs.get("default_ambient_audio_prompt")
        or defs.get("default_audio_prompt")
        or _FALLBACK_AMBIENT_PROMPT
    )
    audio_negative_prompt = (
        body.get("audio_negative_prompt")
        or defs.get("default_ambient_audio_negative_prompt")
        or defs.get("default_audio_negative_prompt")
        or _FALLBACK_AMBIENT_NEG_PROMPT
    )

    lb = globals_data.get("linux_backend") or {}
    api_url = lb.get("api_url") or cfg_get_backend("linux").get("api_url", "http://127.0.0.1:8189")

    # Get clip durations for sidecar JSON (used for sync in frontend)
    from utils.video_utils import get_video_info
    clip_durations: list[float] = []
    for cp in clips:
        try:
            info = get_video_info(cp)
            clip_durations.append(float(info.get("duration") or 0.0))
        except Exception:
            clip_durations.append(0.0)

    podklad = _podklad_dir(project_folder)
    output_name: str = (body.get("output_name") or "").strip()
    if not output_name or not output_name.endswith(".mp3"):
        from datetime import datetime
        ts = datetime.now().strftime("%y%m%d%H%M%S")
        output_name = f"sequence_ambient_{ts}.mp3"
    output_mp3 = podklad / output_name

    asyncio.create_task(_run_sequence_audio_bg(
        clips, output_mp3, audio_prompt, audio_negative_prompt, api_url,
        clip_names=clip_names, clip_durations=clip_durations,
    ))
    return {"ok": True, "output": output_mp3.name}


# ── Batch missing audio ───────────────────────────────────────────────────────

_batch_state: dict = {"status": "idle", "done": 0, "total": 0, "error": None}


@router.get("/batch_missing_status")
async def batch_missing_status():
    return dict(_batch_state)


@router.post("/batch_missing/{run_filename}")
async def batch_missing_audio(run_filename: str, request: Request):
    """
    Generate audio for all clips that have audio_prompt but no audio track.
    Runs sequentially in background.
    Body: { "clips": [{"name": "x.mp4", "audio_prompt": "...", "audio_negative_prompt": "..."}] }
    """
    global _batch_state
    if _batch_state["status"] == "running":
        raise HTTPException(status_code=400, detail="Batch audio już trwa")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON")

    clips = body.get("clips", [])
    if not clips:
        raise HTTPException(status_code=400, detail="Brak klipów do przetworzenia")

    yaml_path = RUNS_FOLDER / run_filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik nie istnieje: {run_filename}")

    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")

    project_folder = Path(globals_data.get("project_folder") or "")
    if not project_folder or not project_folder.exists():
        raise HTTPException(status_code=400, detail=f"Folder projektu nie istnieje: {project_folder}")

    lb = globals_data.get("linux_backend") or {}
    api_url = lb.get("api_url") or cfg_get_backend("linux").get("api_url", "http://127.0.0.1:8189")

    _batch_state.update({"status": "running", "done": 0, "total": len(clips), "error": None})
    asyncio.create_task(_run_batch_audio(clips, project_folder, api_url))
    return {"ok": True, "total": len(clips)}


async def _run_batch_audio(clips: list, project_folder: Path, api_url: str) -> None:
    global _batch_state
    from utils.mmaudio_utils import add_audio as _add_audio
    from utils.video_utils import get_video_info

    logger = _LogBridge()
    loop = asyncio.get_running_loop()

    try:
        for i, clip in enumerate(clips):
            name    = clip.get("name", "")
            prompt  = clip.get("audio_prompt", "")
            neg     = clip.get("audio_negative_prompt", "") or _FALLBACK_AUDIO_NEG_PROMPT

            video_path = project_folder / "transitions" / name
            if not video_path.exists():
                video_path = project_folder / "transitions" / "chains" / name
            if not video_path.exists():
                logger.warning(f"Pomijam (brak pliku): {name}")
                _batch_state["done"] = i + 1
                continue

            try:
                info = get_video_info(video_path)
                duration = float(info["duration"]) if info.get("duration") and info["duration"] > 0 else 10.0
            except Exception:
                duration = 10.0

            logger.info(f"MMAudio [{i+1}/{len(clips)}]: {name}")
            await loop.run_in_executor(None, lambda vp=video_path, p=prompt, n=neg, d=duration: _add_audio(
                video_path=vp, prompt=p, negative_prompt=n,
                api_url=api_url, duration=d, steps=25, cfg=4.5, seed=-1, logger=logger,
            ))
            process_service.log_sys(f"[AUDIO_READY] {name}")
            _batch_state["done"] = i + 1

        _batch_state["status"] = "done"
        logger.success(f"Batch audio zakończone ({len(clips)} klipów)")

    except Exception as exc:
        _batch_state.update({"status": "error", "error": str(exc)})
        print(f"  ✗ Batch audio error: {exc}", file=sys.stderr)
