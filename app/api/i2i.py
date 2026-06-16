# -*- coding: utf-8 -*-
"""
API router for the I2I (Image-to-Image) Pic studio.

Phase 1: Global prompt library CRUD only.
Phase 2 (future): per-project sessions, job runner, results browser.

Endpoints
─────────
GET  /api/i2i/prompts              → full library (categories + defaults + prompts)
POST /api/i2i/prompts              → create prompt
PUT  /api/i2i/prompts/{id}         → update prompt
DEL  /api/i2i/prompts/{id}         → delete prompt

GET  /api/i2i/categories           → list categories
POST /api/i2i/categories           → create category
PUT  /api/i2i/categories/{id}      → update category
DEL  /api/i2i/categories/{id}      → delete category
POST /api/i2i/categories/reorder   → reorder categories

GET  /api/i2i/defaults             → global generation defaults
PUT  /api/i2i/defaults             → update global defaults
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import i2i_prompts_service

router = APIRouter(prefix="/api/i2i", tags=["i2i"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class PromptParams(BaseModel):
    steps:   int   = 30
    cfg:     float = 8.0
    denoise: float = 1.0


class PromptCreate(BaseModel):
    category: str
    name:     str
    positive: str
    negative: str  = ""
    note:     str  = ""
    params:   PromptParams = Field(default_factory=PromptParams)


class PromptUpdate(BaseModel):
    category: str  | None = None
    name:     str  | None = None
    positive: str  | None = None
    negative: str  | None = None
    note:     str  | None = None
    params:   PromptParams | None = None


class CategoryCreate(BaseModel):
    name: str
    icon: str = "🗂"


class CategoryUpdate(BaseModel):
    name: str
    icon: str = "🗂"


class ReorderRequest(BaseModel):
    ordered_ids: list[str]


class DefaultsUpdate(BaseModel):
    steps:   int   = 30
    cfg:     float = 8.0
    denoise: float = 1.0


# ── Library ───────────────────────────────────────────────────────────────────

@router.get("/prompts")
async def get_library():
    """Return full prompt library: categories + defaults + prompts."""
    return i2i_prompts_service.get_all()


# ── Prompts ───────────────────────────────────────────────────────────────────

@router.post("/prompts")
async def create_prompt(body: PromptCreate):
    try:
        p = i2i_prompts_service.create_prompt(
            category=body.category,
            name=body.name,
            positive=body.positive,
            negative=body.negative,
            note=body.note,
            params=body.params.model_dump(),
        )
        return {"ok": True, "prompt": p}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("/prompts/{prompt_id}")
async def update_prompt(prompt_id: str, body: PromptUpdate):
    updates = body.model_dump(exclude_none=True)
    if "params" in updates:
        updates["params"] = body.params.model_dump()
    try:
        p = i2i_prompts_service.update_prompt(prompt_id, updates)
        return {"ok": True, "prompt": p}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/prompts/{prompt_id}")
async def delete_prompt(prompt_id: str):
    try:
        i2i_prompts_service.delete_prompt(prompt_id)
        return {"ok": True}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Categories ────────────────────────────────────────────────────────────────

@router.get("/categories")
async def get_categories():
    return {"categories": i2i_prompts_service.get_categories()}


@router.post("/categories")
async def create_category(body: CategoryCreate):
    try:
        cat = i2i_prompts_service.create_category(body.name, body.icon)
        return {"ok": True, "category": cat}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("/categories/{cat_id}")
async def update_category(cat_id: str, body: CategoryUpdate):
    try:
        cat = i2i_prompts_service.update_category(cat_id, body.name, body.icon)
        return {"ok": True, "category": cat}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/categories/{cat_id}")
async def delete_category(cat_id: str):
    try:
        i2i_prompts_service.delete_category(cat_id)
        return {"ok": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/categories/reorder")
async def reorder_categories(body: ReorderRequest):
    try:
        i2i_prompts_service.reorder_categories(body.ordered_ids)
        return {"ok": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Defaults ──────────────────────────────────────────────────────────────────

@router.get("/defaults")
async def get_defaults():
    return i2i_prompts_service.get_defaults()


@router.put("/defaults")
async def update_defaults(body: DefaultsUpdate):
    try:
        d = i2i_prompts_service.update_defaults(body.steps, body.cfg, body.denoise)
        return {"ok": True, "defaults": d}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
