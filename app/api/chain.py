# -*- coding: utf-8 -*-
"""
API router for Chain generation.
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.chain_service import get_chain_status, start_chain, cancel_chain

router = APIRouter(prefix="/api/chain", tags=["chain"])


@router.get("/status")
async def chain_status():
    """Current chain job state."""
    return get_chain_status()


@router.post("/start")
async def chain_start(request: Request):
    """
    Start a chain generation job.

    Body JSON:
    {
        "run_filename":  "RUN_001.yaml",
        "chain_prefix":  "ewelina_stands",
        "from_step":     0              // 0-indexed step to start from
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename = body.get("run_filename")
    chain_prefix = body.get("chain_prefix")
    from_step    = int(body.get("from_step", 0))
    to_step_raw  = body.get("to_step")
    to_step      = int(to_step_raw) if to_step_raw is not None else None

    if not run_filename or not chain_prefix:
        raise HTTPException(
            status_code=422,
            detail="Required fields: run_filename, chain_prefix",
        )

    result = start_chain(run_filename, chain_prefix, from_step, to_step)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/cancel")
async def chain_cancel():
    """Cancel the running chain job."""
    return cancel_chain()
