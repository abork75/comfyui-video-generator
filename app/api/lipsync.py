# -*- coding: utf-8 -*-
"""
API router for V2V dialogue lipsync (LatentSync 1.5, Linux/WSL2 ComfyUI).

Endpoints:
    POST /api/lipsync/start   — queue a manual lipsync job for a clip
    GET  /api/lipsync/status  — current job status
    POST /api/lipsync/cancel  — cancel running job
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from app.services.lipsync_service import start_lipsync, get_lipsync_status, cancel_lipsync
from app.services.media_service import _project_folder

router = APIRouter(prefix="/api/lipsync", tags=["lipsync"])


@router.post("/start")
async def lipsync_start(request: Request):
    """
    Start a manual lipsync job for a clip.
    Body JSON: {"run": "RUN_xxx.yaml", "name": "clip.mp4", "audio": "dialogue.mp3",
                "trim_to_audio"?: false, "sync_lips"?: true}
    "audio" is a filename relative to the run's project_folder root (same
    convention as the talk/multitalk audio picker). "trim_to_audio" defaults to
    False - the clip's own duration stays untouched (audio is padded/truncated
    to match); pass true to reshape the video to match the dialogue instead.
    "sync_lips" defaults to True (runs LatentSync); pass false for dialogue
    that doesn't need mouth sync (voice from off-screen) - a much faster
    ffmpeg-only mux with no GPU step.
    """
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        name = str(body.get("name", ""))
        audio = str(body.get("audio", ""))
        trim_to_audio = bool(body.get("trim_to_audio", False))
        sync_lips = bool(body.get("sync_lips", True))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name or not audio:
        raise HTTPException(status_code=422, detail="run, name and audio are required")

    result = start_lipsync(run, name, audio, trim_to_audio, sync_lips)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/status")
async def lipsync_status():
    """Return the current lipsync job status."""
    return get_lipsync_status()


@router.post("/cancel")
async def lipsync_cancel():
    """Cancel the running lipsync job."""
    return cancel_lipsync()


@router.get("/audio/{run_filename}/{filename}")
async def lipsync_audio(run_filename: str, filename: str):
    """Serve the dialogue mp3/wav attached to a step (step.lipsync_audio) so
    the Flow lipsync badge can play it on click. Filename is relative to the
    run's project_folder root — same convention as start_lipsync's `audio`."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Nieprawidłowa nazwa pliku")
    if not filename.lower().endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Oczekiwano pliku .mp3/.wav")
    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(status_code=404, detail=f"Nie znaleziono projektu: {run_filename}")
    p = pf / filename
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Nie znaleziono pliku audio: {filename}")
    media = "audio/wav" if filename.lower().endswith(".wav") else "audio/mpeg"
    return FileResponse(str(p), media_type=media)
