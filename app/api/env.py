# -*- coding: utf-8 -*-
"""
API router for environment status (health-check only).

Endpoints:
    GET /api/env/status  — returns {linux, windows} = "ready" | "stopped"
"""

from fastapi import APIRouter
from app.services.env_service import env_service

router = APIRouter(prefix="/api/env", tags=["env"])


@router.get("/status")
async def env_status():
    return await env_service.get_status()
