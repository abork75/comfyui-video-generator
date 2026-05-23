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

    Optional JSON body: {"only": ["transition_name.mp4", ...]}
    When 'only' is provided, only those specific transitions are (re-)generated,
    bypassing skip_existed — useful for targeted single-file regeneration.
    """
    only: list[str] | None = None
    try:
        body = await request.json()
        raw = body.get("only")
        if isinstance(raw, list) and raw:
            only = [str(x) for x in raw if x]
    except Exception:
        pass

    result = await process_service.start(filename, only=only)
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
