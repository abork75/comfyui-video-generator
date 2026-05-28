# -*- coding: utf-8 -*-
"""
API router for global application configuration (app_config.yaml).

GET  /api/app-config   → return full config
PUT  /api/app-config   → save full config
"""

from fastapi import APIRouter, HTTPException, Request

from app.services import app_config_service

router = APIRouter(prefix="/api/app-config", tags=["app-config"])


@router.get("")
async def get_app_config():
    """Return current global application configuration."""
    return app_config_service.get_all()


@router.put("")
async def put_app_config(request: Request):
    """
    Save global application configuration.
    Body JSON: full config dict (linux_backend, models, defaults).
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not isinstance(body, dict):
        raise HTTPException(status_code=422, detail="Body must be a JSON object")

    # Basic validation — ensure expected top-level keys are dicts
    for key in ("backends", "defaults"):
        if key in body and not isinstance(body[key], dict):
            raise HTTPException(status_code=422, detail=f"'{key}' must be an object")

    try:
        app_config_service.save(body)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"ok": True}
