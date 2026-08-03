# -*- coding: utf-8 -*-
"""
Scene Configurator API

GET  /api/scene-conf/templates            — list templates from RUN_000
POST /api/scene-conf/analyze              — analyze image via Qwen (multipart)
POST /api/scene-conf/generate             — generate RUN yaml from template
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import scene_conf_service as svc
from app.services.run_file_service import invalidate_run_info_cache

router = APIRouter(prefix="/api/scene-conf", tags=["scene-conf"])


@router.get("/templates")
async def get_templates():
    return {"templates": svc.list_templates()}


@router.get("/template-slots")
async def get_template_slots(index: int = 0):
    try:
        slots = svc.get_template_slots(index)
    except Exception as e:
        raise HTTPException(500, str(e))
    return {"slots": slots}


class AnalyzeRequest(BaseModel):
    image_path: str


@router.post("/analyze")
async def analyze_image(req: AnalyzeRequest):
    p = Path(req.image_path)
    if not p.exists():
        raise HTTPException(404, f"Plik nie istnieje: {req.image_path}")
    try:
        image_bytes = p.read_bytes()
        descriptor = await svc.analyze_image(image_bytes, p.name)
    except TimeoutError as e:
        raise HTTPException(504, str(e))
    except Exception as e:
        raise HTTPException(500, f"Błąd analizy: {e}")
    return {"descriptor": descriptor}


class GenerateRequest(BaseModel):
    target_filename: str
    template_index: int
    descriptor: dict
    image_map: dict = {}
    scene_name: str = ""


@router.post("/generate")
async def generate_run(req: GenerateRequest):
    try:
        svc.append_scene(
            target_filename=req.target_filename,
            template_index=req.template_index,
            descriptor=req.descriptor,
            image_map=req.image_map,
            scene_name=req.scene_name,
        )
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(409, str(e))
    except Exception as e:
        raise HTTPException(500, f"Błąd generacji: {e}")
    invalidate_run_info_cache()
    return {"ok": True}
