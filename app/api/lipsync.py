# -*- coding: utf-8 -*-
"""
API router for V2V dialogue lipsync (LatentSync 1.5, Linux/WSL2 ComfyUI).

Endpoints:
    POST /api/lipsync/start   — queue a manual lipsync job for a clip
    GET  /api/lipsync/status  — current job status
    POST /api/lipsync/cancel  — cancel running job
"""

import base64

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from app.services.lipsync_service import (
    start_lipsync, start_lipsync_multi, get_lipsync_status, cancel_lipsync,
    preview_face_positions,
)
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


@router.post("/start_multi")
async def lipsync_start_multi(request: Request):
    """
    Start a multi-talk lipsync job: 2+ characters in the SAME clip, each with
    their own dialogue audio and time window (see app/services/lipsync_service.py
    module docstring "Multi-talk" section for the full design).
    Body JSON: {"run": "RUN_xxx.yaml", "name": "clip.mp4",
                "assignments": [{"audio": "a.mp3", "sync_lips"?: true,
                                  "position_index"?: 0}, ...]}
    List order = time-window order only (assignments[0] covers the clip's
    start, its own window length derived from its own audio's duration, then
    assignments[1] picks up from there, etc. - the last assignment always
    runs to the clip's real end). "position_index" (0 = leftmost face in the
    frame, defaults to the list index if omitted) is independent per entry
    and MAY REPEAT - the same person can speak multiple non-contiguous turns
    (e.g. position_index sequence 1, 0, 1). Uses the same "audio relative to
    project_folder root" convention as /start.
    """
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        name = str(body.get("name", ""))
        assignments = body.get("assignments") or []
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")
    if not isinstance(assignments, list) or not assignments:
        raise HTTPException(status_code=422, detail="assignments must be a non-empty list")

    result = start_lipsync_multi(run, name, assignments)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/face_preview")
async def lipsync_face_preview(request: Request):
    """
    Diagnostic-only: preview which physical face position_index=N will pick
    for one dialog turn, BEFORE queuing the real (multi-minute) multi-talk
    job. Draws numbered boxes (1,2,3... left-to-right) on a representative
    frame sampled from that turn's own computed time window (same
    cumulative-duration math as /start_multi - see lipsync_service.py's
    _compute_windows). No side effects on the clip itself.
    Body JSON: {"run": "RUN_xxx.yaml", "name": "clip.mp4",
                "assignments": [{"audio": "a.mp3"}, ...], "target_index": 0}
    For "Prosty" mode, pass a 1-item assignments list and target_index=0.
    Returns: {"ok": true, "image_base64": "<PNG bytes, base64>"}.
    """
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        name = str(body.get("name", ""))
        assignments = body.get("assignments") or []
        target_index = int(body.get("target_index", 0))
        threshold = float(body.get("threshold", 0.5))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")
    if not isinstance(assignments, list) or not assignments:
        raise HTTPException(status_code=422, detail="assignments must be a non-empty list")

    try:
        png_bytes = await preview_face_positions(run, name, assignments, target_index, threshold)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"ok": True, "image_base64": base64.b64encode(png_bytes).decode("ascii")}


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
