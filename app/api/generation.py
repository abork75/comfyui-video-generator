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
async def start_generation(filename: str):
    """Start generation for the given RUN file."""
    result = await process_service.start(filename)
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
