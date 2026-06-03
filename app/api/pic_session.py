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
from app.services.pic_session_service import _get_tile_type, add_prompt_to_all_scene_slots

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


class SceneSlot(BaseModel):
    scene_image:      str              = ""
    character_images: list[str]        = Field(default_factory=list)
    prompts:          list[PromptItem] = Field(default_factory=list)


class CharacterEntry(BaseModel):
    model_image:  str   = ""
    top_pct:      float = 10.0
    bottom_pct:   float = 85.0
    x_center_pct: float = 50.0
    erode_px:     int   = 3
    blur_px:      int   = 2


class PasteSlot(BaseModel):
    id:           str                     = ""
    output_id:    str                     = ""
    scene_image:  str                     = ""
    characters:   list[CharacterEntry]    = Field(default_factory=list)


class TilePayload(BaseModel):
    type:             str              = "one_image_many_prompts"
    name:             str              = ""
    # one_image_many_prompts
    source_dirs:      list[str]        = Field(default_factory=list)
    image_slots:      list[ImageSlot]  = Field(default_factory=list)
    # character_insert
    scene_dirs:       list[str]        = Field(default_factory=list)
    characters_dirs:  list[str]        = Field(default_factory=list)
    scene_slots:      list[SceneSlot]  = Field(default_factory=list)
    # paste_character
    paste_slots:          list[PasteSlot] = Field(default_factory=list)
    edge_blend_enabled:   bool            = False
    edge_blend_px:        int             = 15
    edge_blend_cfg:       Optional[float] = None
    edge_blend_denoise:   Optional[float] = None
    edge_blend_prompts:   list[dict]      = Field(default_factory=list)
    scene_blend_enabled:  bool            = False
    scene_blend_cfg:      Optional[float] = None
    scene_blend_denoise:  Optional[float] = None
    scene_blend_prompts:  list[dict]      = Field(default_factory=list)
    # common
    output_dir:         str              = ""
    global_suffix:      str              = ""
    crop_to_subject:    bool             = False
    pad_input_to_ratio: bool             = False


# ── Tile CRUD ─────────────────────────────────────────────────────────────────

@router.get("/session/{run_id}/tiles")
async def get_tiles(run_id: str):
    try:
        return {"tiles": pic_session_service.get_tiles(run_id)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


def _serialize_payload(body: TilePayload) -> dict:
    d = body.model_dump()
    d["image_slots"] = [
        {"image": s.image, "prompts": [p.model_dump() for p in s.prompts]}
        for s in body.image_slots
    ]
    d["scene_slots"] = [
        {
            "scene_image":      s.scene_image,
            "character_images": s.character_images,
            "prompts":          [p.model_dump() for p in s.prompts],
        }
        for s in body.scene_slots
    ]
    d["paste_slots"] = [
        {
            "id":          s.id,
            "output_id":   s.output_id,
            "scene_image": s.scene_image,
            "characters":  [c.model_dump() for c in s.characters],
        }
        for s in body.paste_slots
    ]
    return d


@router.post("/session/{run_id}/tiles")
async def create_tile(run_id: str, body: TilePayload):
    try:
        tile = pic_session_service.create_tile(run_id, _serialize_payload(body))
        return {"ok": True, "tile": tile}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("/session/{run_id}/tiles/{tile_id}")
async def update_tile(run_id: str, tile_id: str, body: TilePayload):
    try:
        tile = pic_session_service.update_tile(run_id, tile_id, _serialize_payload(body))
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


class ReorderRequest(BaseModel):
    ids: list[str]


@router.post("/session/{run_id}/tiles/reorder")
async def reorder_tiles(run_id: str, body: ReorderRequest):
    try:
        tiles = pic_session_service.reorder_tiles(run_id, body.ids)
        return {"ok": True, "tiles": tiles}
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

        tile_type = _get_tile_type(run_id, tile_id)
        if tile_type == "character_insert":
            add_prompt_to_all_scene_slots(run_id, tile_id, prompt)
        elif body.add_to_all:
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
    prompt_id:  Optional[str] = None   # None = all prompts in slot; str = single prompt


@router.post("/session/{run_id}/tiles/{tile_id}/run")
async def run_tile(run_id: str, tile_id: str, body: RunRequest):
    """Start generation for a tile (all slots, single slot, or single prompt)."""
    result = pic_generation_service.start_tile_run(
        run_id, tile_id, body.force_all, body.slot_index, body.prompt_id
    )
    if result == "already_running":
        raise HTTPException(status_code=409, detail="Generowanie już trwa dla tego kafelka")
    return {"ok": True, "status": "queued"}


@router.get("/session/{run_id}/tiles/{tile_id}/job")
async def get_tile_job(run_id: str, tile_id: str):
    """Return current generation job state (poll every ~3 s)."""
    return pic_generation_service.get_job(run_id, tile_id)


@router.delete("/session/{run_id}/tiles/{tile_id}/result/{prompt_id}")
async def delete_tile_result(
    run_id:     str,
    tile_id:    str,
    prompt_id:  str,
    slot_index: int = Query(default=0),
):
    """Delete the generated output file for a prompt (keeps prompt in tile config)."""
    try:
        deleted = pic_generation_service.delete_result(
            run_id, tile_id, prompt_id, slot_index
        )
        return {"ok": True, "deleted": deleted}
    except (KeyError, IndexError) as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


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
