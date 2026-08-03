# -*- coding: utf-8 -*-
"""
API router for generation control.

Endpoints:
    GET    /api/generate/status      — current process status
    POST   /api/generate/{filename}  — start generation
    DELETE /api/generate             — stop generation
    POST   /api/generate/stdin       — answer interactive input() prompt
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.process_service import process_service

router = APIRouter(prefix="/api/generate", tags=["generation"])


@router.get("/status")
async def get_status():
    """Return current generation status."""
    return process_service.get_status()


@router.post("/stdin")
async def send_stdin(request: Request):
    """
    Send user's answer to an interactive input() prompt in the subprocess.
    Body JSON: {"text": "y"} or {"text": "n"}
    """
    try:
        body = await request.json()
        text = str(body.get("text", "n"))
    except Exception:
        text = "n"

    result = await process_service.provide_input(text)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{filename}")
async def start_generation(filename: str, request: Request):
    """
    Start generation for the given RUN file.

    Optional JSON body:
      {"only": ["transition_name.mp4", ...]}   — re-generate only listed files
      {"force_all": true}                       — regenerate ALL (skip_existed=False)
    """
    only: list[str] | None = None
    force_all: bool = False
    mmaudio: bool = False
    lightning_override = None
    try:
        body = await request.json()
        raw = body.get("only")
        if isinstance(raw, list) and raw:
            only = [str(x) for x in raw if x]
        if body.get("force_all"):
            force_all = True
        if body.get("mmaudio"):
            mmaudio = True
        if "lightning_override" in body:
            val = body.get("lightning_override")
            if isinstance(val, bool):
                lightning_override = val
    except Exception:
        pass

    result = await process_service.start(filename, only=only, force_all=force_all, mmaudio=mmaudio, lightning_override=lightning_override)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("")
async def stop_generation():
    """Stop the currently running generation process."""
    result = await process_service.stop()
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
