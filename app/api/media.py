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
