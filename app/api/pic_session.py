# -*- coding: utf-8 -*-
"""
API router for the Pic Studio per-project tile management.

Endpoints
─────────
GET    /api/pic/session/{run_id}/tiles                               → list tiles
POST   /api/pic/session/{run_id}/tiles                               → create tile
PUT    /api/pic/session/{run_id}/tiles/{tile_id}                     → update tile
DELETE /api/pic/session/{run_id}/tiles/{tile_id}                     → delete tile
POST   /api/pic/session/{run_id}/tiles/{tile_id}/copy                → copy tile
GET    /api/pic/session/{run_id}/tiles/{tile_id}/status              → generation status

POST   /api/pic/session/{run_id}/tiles/{tile_id}/prompts/new         → create + add to slot
POST   /api/pic/session/{run_id}/tiles/{tile_id}/run                 → start generation
GET    /api/pic/session/{run_id}/tiles/{tile_id}/job                 → poll job state
POST   /api/pic/session/{run_id}/tiles/{tile_id}/archive/{prompt_id} → archive result
       ?slot_index=0
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services import pic_session_service, pic_generation_service, i2i_prompts_service

router = APIRouter(prefix="/api/pic", tags=["pic"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class PromptItem(BaseModel):
    id:        str
    output_id: str  = ""   # 18-char random ID; assigned server-side if empty
    enabled:   bool = True
    name:      str
    positive:  str
    negative:  str  = ""
    note:      str  = ""
    params:    dict = Field(default_factory=lambda: {"steps": 30, "cfg": 8, "denoise": 1.0})


class ImageSlot(BaseModel):
    image:   str              = ""
    prompts: list[PromptItem] = Field(default_factory=list)


class TilePayload(BaseModel):
    type:          str             = "one_image_many_prompts"
    name:          str             = ""
    source_dir:    str             = ""
    output_dir:    str             = ""
    global_suffix: str             = ""
    image_slots:   list[ImageSlot] = Field(default_factory=list)


# ── Tile CRUD ─────────────────────────────────────────────────────────────────

@router.get("/session/{run_id}/tiles")
async def get_tiles(run_id: str):
    try:
        return {"tiles": pic_session_service.get_tiles(run_id)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/session/{run_id}/tiles")
async def create_tile(run_id: str, body: TilePayload):
    try:
        d = body.model_dump()
        d["image_slots"] = [
            {"image": s.image, "prompts": [p.model_dump() for p in s.prompts]}
            for s in body.image_slots
        ]
        tile = pic_session_service.create_tile(run_id, d)
        return {"ok": True, "tile": tile}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("/session/{run_id}/tiles/{tile_id}")
async def update_tile(run_id: str, tile_id: str, body: TilePayload):
    try:
        d = body.model_dump()
        d["image_slots"] = [
            {"image": s.image, "prompts": [p.model_dump() for p in s.prompts]}
            for s in body.image_slots
        ]
        tile = pic_session_service.update_tile(run_id, tile_id, d)
        return {"ok": True, "tile": tile}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/session/{run_id}/tiles/{tile_id}")
async def delete_tile(run_id: str, tile_id: str):
    try:
        pic_session_service.delete_tile(run_id, tile_id)
        return {"ok": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/session/{run_id}/tiles/{tile_id}/copy")
async def copy_tile(run_id: str, tile_id: str):
    try:
        tile = pic_session_service.copy_tile(run_id, tile_id)
        return {"ok": True, "tile": tile}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/session/{run_id}/tiles/{tile_id}/status")
async def tile_status(run_id: str, tile_id: str):
    try:
        return pic_session_service.get_tile_status(run_id, tile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Prompt creation ───────────────────────────────────────────────────────────

class NewTilePromptRequest(BaseModel):
    """Create a prompt in the global library and add it to a tile slot."""
    slot_index: int  = 0
    add_to_all: bool = False   # True → add to every image slot
    category:   str  = ""
    name:       str
    positive:   str
    negative:   str  = ""
    note:       str  = ""
    params:     dict = Field(default_factory=lambda: {"steps": 30, "cfg": 8, "denoise": 1.0})


@router.post("/session/{run_id}/tiles/{tile_id}/prompts/new")
async def create_tile_prompt(run_id: str, tile_id: str, body: NewTilePromptRequest):
    """
    Create a prompt in the global library (sequential p000xxxx ID),
    then add it to the specified slot (or all slots if add_to_all=True).
    """
    try:
        if not body.name.strip():
            raise HTTPException(status_code=422, detail="Podaj nazwę promptu")
        if not body.positive.strip():
            raise HTTPException(status_code=422, detail="Positive prompt jest wymagany")

        prompt = i2i_prompts_service.create_prompt(
            category=body.category,
            name=body.name,
            positive=body.positive,
            negative=body.negative,
            note=body.note,
            params=body.params,
        )

        if body.add_to_all:
            pic_session_service.add_prompt_to_all_slots(run_id, tile_id, prompt)
        else:
            pic_session_service.add_prompt_to_slot(run_id, tile_id, body.slot_index, prompt)

        return {"ok": True, "prompt": prompt}
    except HTTPException:
        raise
    except (KeyError, IndexError) as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Generation ────────────────────────────────────────────────────────────────

class RunRequest(BaseModel):
    force_all:  bool          = False
    slot_index: Optional[int] = None   # None = all slots


@router.post("/session/{run_id}/tiles/{tile_id}/run")
async def run_tile(run_id: str, tile_id: str, body: RunRequest):
    """Start generation for a tile (all slots or a single slot)."""
    result = pic_generation_service.start_tile_run(
        run_id, tile_id, body.force_all, body.slot_index
    )
    if result == "already_running":
        raise HTTPException(status_code=409, detail="Generowanie już trwa dla tego kafelka")
    return {"ok": True, "status": "queued"}


@router.get("/session/{run_id}/tiles/{tile_id}/job")
async def get_tile_job(run_id: str, tile_id: str):
    """Return current generation job state (poll every ~3 s)."""
    return pic_generation_service.get_job(run_id, tile_id)


@router.post("/session/{run_id}/tiles/{tile_id}/archive/{prompt_id}")
async def archive_tile_result(
    run_id:     str,
    tile_id:    str,
    prompt_id:  str,
    slot_index: int = Query(default=0),
):
    """Move a generated result to the archive/ subfolder."""
    try:
        dest = pic_generation_service.archive_result(
            run_id, tile_id, prompt_id, slot_index
        )
        return {"ok": True, "archived_to": str(dest)}
    except (FileNotFoundError, KeyError, IndexError) as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
