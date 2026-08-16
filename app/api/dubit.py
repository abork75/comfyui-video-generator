# -*- coding: utf-8 -*-
"""API router for DubIt lipsync generation."""

from fastapi import APIRouter, HTTPException, Request

from app.services.dubit_service import get_dubit_status, start_dubit, cancel_dubit

router = APIRouter(prefix="/api/dubit", tags=["dubit"])


@router.get("/status")
async def dubit_status():
    return get_dubit_status()


@router.post("/start")
async def dubit_start(request: Request):
    """
    Start a DubIt lipsync generation job.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "dubit_item": {
            "type": "dubit",
            "audio": "voice.mp3",
            "pos": "A woman is speaking Polish, saying: \\"Chodź na plażę!\\"",
            "neg": "blurry, distorted face",
            "prefix": "scene01_talk",   // optional
            "width": 896,               // optional, overrides project resolution
            "height": 1152
        },
        "start_image": "face.jpg",      // relative to project_folder
        "flow_idx": 3                   // optional, for status tracking
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename     = body.get("run_filename")
    dubit_item       = body.get("dubit_item")
    start_image      = body.get("start_image")
    flow_idx         = body.get("flow_idx")
    start_from_step  = int(body.get("start_from_step") or 0)
    _eat             = body.get("end_at_step")
    end_at_step      = int(_eat) if _eat is not None else None
    dry_run          = bool(body.get("dry_run", False))

    if not run_filename or not dubit_item or not start_image:
        raise HTTPException(
            status_code=422,
            detail="Required fields: run_filename, dubit_item, start_image",
        )

    result = start_dubit(run_filename, dubit_item, start_image, flow_idx=flow_idx,
                         start_from_step=start_from_step, end_at_step=end_at_step,
                         dry_run=dry_run)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/cancel")
async def dubit_cancel():
    return cancel_dubit()
