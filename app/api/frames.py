# -*- coding: utf-8 -*-
"""
Frames API — extract / cache real end-frames from generated clips.

POST /api/frames/extract-real
    Body: { run, clip, name }
    Extracts the last frame of `clip` and saves it as
    {project_folder}/frames/{name}_real.jpg.
    Skips silently if the file already exists.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.media_service import resolve_video, _project_folder
from app.api.trim import _get_video_info, _extract_frame

router = APIRouter(prefix="/api/frames", tags=["frames"])


class ExtractRealRequest(BaseModel):
    run: str
    clip: str
    name: str   # output stem — frame saved as frames/{name}_real.jpg


@router.post("/extract-real")
async def extract_real_frame(req: ExtractRealRequest):
    pf = _project_folder(req.run)
    if pf is None:
        raise HTTPException(404, "Nie znaleziono PROJECT_FOLDER")

    video_path = resolve_video(req.run, req.clip)
    if video_path is None:
        raise HTTPException(404, f"Klip nie istnieje: {req.clip}")

    frames_dir = pf / "frames"
    out_path = frames_dir / f"{req.name}_real.jpg"

    if out_path.exists():
        return {"ok": True, "skipped": True, "file": out_path.name}

    try:
        info = _get_video_info(video_path)
    except Exception as e:
        raise HTTPException(500, f"ffprobe: {e}")

    last_frame = max(0, info["total_frames"] - 1)

    try:
        jpg_bytes = _extract_frame(video_path, last_frame)
    except Exception as e:
        raise HTTPException(500, f"ffmpeg: {e}")

    frames_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(jpg_bytes)

    return {"ok": True, "skipped": False, "file": out_path.name}
