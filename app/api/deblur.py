# -*- coding: utf-8 -*-
"""
API router for the LTX 2.3 deblur post-process (IC-LoRA, Linux/WSL2 ComfyUI).

Endpoints:
    POST /api/deblur/start   — queue a deblur job for a clip
    GET  /api/deblur/status  — current job status
    POST /api/deblur/cancel  — cancel running job
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.deblur_service import start_deblur, get_deblur_status, cancel_deblur

router = APIRouter(prefix="/api/deblur", tags=["deblur"])


@router.post("/start")
async def deblur_start(request: Request):
    """
    Start a deblur job for a clip. Works on any clip regardless of what
    generated it (WAN, LTX, or an external source video).
    Body JSON: {"run": "RUN_xxx.yaml", "name": "clip.mp4", "type": "generated"}
    """
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        name = str(body.get("name", ""))
        clip_type = str(body.get("type", "generated"))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run or not name:
        raise HTTPException(status_code=422, detail="run and name are required")

    if clip_type not in ("generated", "external"):
        clip_type = "generated"

    result = start_deblur(run, name, clip_type)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/status")
async def deblur_status():
    """Return the current deblur job status."""
    return get_deblur_status()


@router.post("/cancel")
async def deblur_cancel():
    """Cancel the running deblur job."""
    return cancel_deblur()
