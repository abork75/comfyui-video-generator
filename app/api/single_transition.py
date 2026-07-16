# -*- coding: utf-8 -*-
"""
API router for single-transition regeneration.
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.single_transition_service import (
    get_status,
    start_single_transition,
    cancel,
)

router = APIRouter(prefix="/api/single_transition", tags=["single_transition"])


@router.get("/status")
async def single_transition_status():
    """Current single-transition job state."""
    return get_status()


@router.post("/start")
async def single_transition_start(request: Request):
    """
    Start a single-transition generation job.

    Body JSON:
    {
        "run_filename":    "RUN_018_naked_warrior.yaml",
        "transition_name": "18.53. Igraszki_2_19.41 happy_end sitting_transition.mp4"
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename    = body.get("run_filename")
    transition_name = body.get("transition_name")
    mmaudio         = bool(body.get("mmaudio", False))

    if not run_filename or not transition_name:
        raise HTTPException(
            status_code=422,
            detail="Required fields: run_filename, transition_name",
        )

    result = start_single_transition(run_filename, transition_name, mmaudio=mmaudio)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/cancel")
async def single_transition_cancel():
    """Cancel the running single-transition job."""
    return cancel()
