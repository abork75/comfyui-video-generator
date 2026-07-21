# -*- coding: utf-8 -*-
"""
Multitalk API — single-speaker clips with N-person silence masking.

POST /api/multitalk/setup      — create N person-image copies for mask painting
GET  /api/multitalk/status     — job state
POST /api/multitalk/start      — generate one clip
POST /api/multitalk/cancel     — cancel running job
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.multitalk_service import (
    get_multitalk_status,
    start_multitalk,
    cancel_multitalk,
    setup_person_images,
    suggest_resolution,
    person_image_path,
)
from app.services.media_service import _project_folder
from pathlib import Path

router = APIRouter(prefix="/api/multitalk", tags=["multitalk"])


@router.post("/setup")
async def multitalk_setup(request: Request):
    """
    Create N copies of the base image for per-person mask painting.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "image": "scene.jpg",
        "num_persons": 3
    }

    Returns list of absolute paths to person image copies.
    Existing copies are NOT overwritten (masks are preserved).
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(422, "Invalid JSON")

    run_filename = body.get("run_filename")
    image        = body.get("image", "")
    num_persons  = int(body.get("num_persons", 2))

    if not run_filename or not image:
        raise HTTPException(422, "Required: run_filename, image")
    if num_persons < 2 or num_persons > 8:
        raise HTTPException(422, "num_persons must be 2–8")

    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(404, f"project_folder not found: {run_filename}")

    try:
        paths = setup_person_images(pf, image, num_persons)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))

    return {
        "ok": True,
        "num_persons": num_persons,
        "person_images": [str(p) for p in paths],
    }


@router.get("/status")
async def multitalk_status():
    return get_multitalk_status()


@router.post("/start")
async def multitalk_start(request: Request):
    """
    Start a multitalk clip generation.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "image": "scene.jpg",
        "item": {
            "audio":       "voice.mp3",
            "speaker_idx": 0,
            "num_persons": 3,
            "width":       480,    // optional — auto if omitted
            "height":      720,    // optional
            "pos":         "people talking naturally",
            "name":        "dialog_01.mp4"
        }
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(422, "Invalid JSON")

    run_filename = body.get("run_filename")
    image        = body.get("image", "")
    item         = body.get("item", {})

    if not run_filename or not image or not item:
        raise HTTPException(422, "Required: run_filename, image, item")

    result = start_multitalk(run_filename, item, image)
    if not result["ok"]:
        raise HTTPException(400, result["error"])
    return result


@router.post("/cancel")
async def multitalk_cancel():
    return cancel_multitalk()


@router.post("/suggest-resolution")
async def multitalk_suggest_resolution(request: Request):
    """
    Suggest width×height for the image (proportional, max ~307k px).

    Body JSON: { "run_filename": "RUN_001.yaml", "image": "scene.jpg" }
    Returns: { "width": 480, "height": 720 }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(422, "Invalid JSON")

    run_filename = body.get("run_filename")
    image        = body.get("image", "")
    if not run_filename:
        raise HTTPException(422, "run_filename required")

    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(404, "project_folder not found")

    image_path = pf / image if image else None
    if image_path and image_path.exists():
        w, h = suggest_resolution(image_path)
    else:
        w, h = 480, 832

    return {"width": w, "height": h}
