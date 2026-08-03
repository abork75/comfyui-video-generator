# -*- coding: utf-8 -*-
"""
API router for global application configuration (app_config.yaml).

GET  /api/app-config   → return full config
PUT  /api/app-config   → save full config
"""

import fnmatch
from pathlib import Path

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


@router.get("/workflow-variants")
async def get_workflow_variants():
    """Return available workflow files per type, scanned from disk."""
    cfg = app_config_service.get_all()
    workflows_path = Path(cfg["backends"]["linux"].get("workflows_path", ""))
    wc_path = Path(__file__).parent.parent.parent / "workflow_configs"

    def scan(directory: Path, pattern: str) -> list[str]:
        if not directory.exists():
            return []
        return sorted(
            p.name if directory == workflows_path else str(p)
            for p in directory.iterdir()
            if p.is_file() and fnmatch.fnmatch(p.name.lower(), pattern.lower())
        )

    i2v_all = scan(workflows_path, "_I2V_*.json")
    i2v_lightning = [f for f in i2v_all if "_hq" not in f.lower()]
    i2v_hq        = [f for f in i2v_all if "_hq" in f.lower()]
    talk_files = [
        str(p) for p in sorted(wc_path.iterdir())
        if p.is_file() and "talk" in p.name.lower() and "multitalk" not in p.name.lower() and p.suffix == ".json"
    ] if wc_path.exists() else []

    return {
        "lightning":    i2v_lightning,
        "hq":           i2v_hq,
        "talk":         talk_files,
        "multitalk":    scan(wc_path, "*multitalk*.json"),
        "upscale_video": scan(wc_path, "*upscal*video*.json") or scan(wc_path, "*upscaler*video*.json"),
        "upscale_image": scan(wc_path, "*upscal*image*.json") or scan(wc_path, "*upscaler*image*.json"),
        "i2i":          scan(wc_path, "*i2i*.json"),
        "ci_1ref":      scan(wc_path, "*ci*1ref*.json"),
        "ci_2ref":      scan(wc_path, "*ci*2ref*.json"),
    }
