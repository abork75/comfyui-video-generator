# -*- coding: utf-8 -*-
"""
API router for media operations:
    GET  /api/media/frame   — serve a frame JPEG
    GET  /api/media/video   — serve a transition/chain MP4
    POST /api/media/archive — rename a generated file (add _ver timestamp)
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from app.services.media_service import (
    resolve_frame,
    resolve_video,
    archive_video,
    get_transition_status,
)

router = APIRouter(prefix="/api/media", tags=["media"])


@router.get("/frame")
async def get_frame(run: str, file: str, kind: str = "start"):
    """
    Serve a frame JPEG.
    ?run=RUN_xxx.py&file=09.51. full street.png&kind=start|end
    """
    path = resolve_frame(run, file, kind)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Frame not found: {file} ({kind})")
    return FileResponse(str(path), media_type="image/jpeg")


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
