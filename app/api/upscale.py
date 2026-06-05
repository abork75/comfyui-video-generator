# -*- coding: utf-8 -*-
"""
API router for video upscaling via Windows ComfyUI (RealESRGAN).

Endpoints:
    POST /api/upscale/start   — queue an upscale job
    GET  /api/upscale/status  — current job status
    POST /api/upscale/cancel  — cancel running job
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.upscale_service import (
    start_upscale,
    start_lanczos_upscale,
    get_upscale_status,
    cancel_upscale,
)

router = APIRouter(prefix="/api/upscale", tags=["upscale"])


@router.post("/start")
async def upscale_start(request: Request):
    """
    Start an upscale job for a generated clip.
    Body JSON: {"run": "RUN_xxx.yaml", "name": "clip.mp4", "width": 1024, "height": 1024}
    """
    try:
        body      = await request.json()
        run       = str(body.get("run",       ""))
        name      = str(body.get("name",      ""))
        clip_type = str(body.get("type",      "generated"))
        width     = int(body.get("width",     1024))
        height    = int(body.get("height",    1024))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")

    if clip_type not in ("generated", "external"):
        clip_type = "generated"

    result = start_upscale(run, name, clip_type, width, height)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/status")
async def upscale_status():
    """Return the current upscale job status."""
    return get_upscale_status()


@router.post("/start_lanczos")
async def upscale_start_lanczos(request: Request):
    """
    Start a fast Lanczos (ffmpeg) resize job for a generated clip.
    No Windows ComfyUI required — runs ffmpeg locally.
    Body JSON: {"run": "RUN_xxx.yaml", "name": "clip.mp4", "type": "generated", "width": 1024, "height": 1024}
    """
    try:
        body      = await request.json()
        run       = str(body.get("run",       ""))
        name      = str(body.get("name",      ""))
        clip_type = str(body.get("type",      "generated"))
        width     = int(body.get("width",     1024))
        height    = int(body.get("height",    1024))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")

    if clip_type not in ("generated", "external"):
        clip_type = "generated"

    result = start_lanczos_upscale(run, name, clip_type, width, height)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/cancel")
async def upscale_cancel():
    """Cancel the running upscale job."""
    return cancel_upscale()


@router.get("/debug")
async def upscale_debug():
    """
    Diagnostic endpoint — returns raw ComfyUI history for the current prompt_id.
    Use when a job completes in ComfyUI but the modal stays stuck.
    """
    import urllib.request, json as _json
    from app.core.config import settings as _s
    from app.services.upscale_service import _state

    prompt_id = _state.get("prompt_id")
    if not prompt_id:
        return {"error": "No active prompt_id", "state": _state}

    try:
        url = f"{_s.comfyui_upscale_url}/history/{prompt_id}"
        with urllib.request.urlopen(url, timeout=10) as r:
            raw = _json.loads(r.read())
        return {"prompt_id": prompt_id, "state": _state, "history": raw}
    except Exception as e:
        return {"prompt_id": prompt_id, "state": _state, "error": str(e)}
