# -*- coding: utf-8 -*-
"""
API router for Talk (InfiniteTalk) generation.
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.talk_service import (
    get_talk_status,
    start_talk,
    cancel_talk,
    suggest_resolution,
)
from app.services.media_service import _project_folder
from pathlib import Path

router = APIRouter(prefix="/api/talk", tags=["talk"])


@router.get("/status")
async def talk_status():
    """Current talk job state."""
    return get_talk_status()


@router.post("/start")
async def talk_start(request: Request):
    """
    Start a talk generation job.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "talk_item": {
            "type": "talk",
            "audio": "voice.mp3",       // or ["p1.mp3", "p2.mp3"]
            "width": 480,
            "height": 832,
            "pos": "a man is talking"   // optional
        },
        "start_image": "face.jpg"       // relative to project_folder
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename = body.get("run_filename")
    talk_item    = body.get("talk_item")
    start_image  = body.get("start_image")

    if not run_filename or not talk_item or not start_image:
        raise HTTPException(
            status_code=422,
            detail="Required fields: run_filename, talk_item, start_image",
        )

    result = start_talk(run_filename, talk_item, start_image)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/cancel")
async def talk_cancel():
    """Cancel the running talk job."""
    return cancel_talk()


@router.post("/suggest-resolution")
async def talk_suggest_resolution(request: Request):
    """
    Suggest optimal width×height for a talk clip.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "image": "face.jpg",
        "audio": ["voice.mp3"]          // list of audio filenames
    }

    Returns {"width": 480, "height": 832}
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename = body.get("run_filename")
    image_name   = body.get("image", "")
    audio_names  = body.get("audio", [])
    if isinstance(audio_names, str):
        audio_names = [audio_names]
    # audio items may be step dicts {audio: "...", pos: "...", neg: "..."} — extract filename
    audio_names = [
        (a["audio"] if isinstance(a, dict) else a)
        for a in audio_names
        if a and (isinstance(a, str) or (isinstance(a, dict) and a.get("audio")))
    ]

    if not run_filename:
        raise HTTPException(status_code=422, detail="run_filename required")

    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(status_code=404, detail="project_folder not found")

    try:
        # If image is a video, use the extracted end-frame (PNG preferred, JPEG fallback)
        _vid_exts = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
        if image_name and Path(image_name).suffix.lower() in _vid_exts:
            stem = Path(image_name).stem
            frame_path = pf / "frames" / f"{stem}_end.png"
            if not frame_path.exists():
                frame_path = pf / "frames" / f"{stem}_end.jpg"
            image_path = frame_path if frame_path.exists() else (pf / image_name if image_name else None)
        else:
            image_path = pf / image_name if image_name else None
        audio_paths = [pf / a for a in audio_names if a]

        if image_path and image_path.exists():
            w, h = suggest_resolution(image_path, audio_paths)
        else:
            # Image not found in project_folder — fall back to safe default
            w, h = 480, 832
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"suggest_resolution failed: {exc}")

    return {"width": w, "height": h}
