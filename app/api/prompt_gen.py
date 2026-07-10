# -*- coding: utf-8 -*-
"""
Prompt Generator API

POST   /api/prompt-gen/{run_id}/tiles                                → create tile
GET    /api/prompt-gen/{run_id}/tiles/{tile_id}                      → tile info
GET    /api/prompt-gen/{run_id}/tiles/{tile_id}/sessions             → list sessions
POST   /api/prompt-gen/{run_id}/tiles/{tile_id}/sessions             → create session
GET    /api/prompt-gen/{run_id}/tiles/{tile_id}/sessions/{sid}       → load session
PUT    /api/prompt-gen/{run_id}/tiles/{tile_id}/sessions/{sid}       → save session
DELETE /api/prompt-gen/{run_id}/tiles/{tile_id}/sessions/{sid}       → delete session
POST   /api/prompt-gen/{run_id}/tiles/{tile_id}/sessions/{sid}/chat  → send message
GET    /api/prompt-gen/{run_id}/tiles/{tile_id}/cost                 → cost summary
GET    /api/prompt-gen/formats                                        → list formats
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import prompt_gen_service
from app.services.pic_session_service import _load, _save, _slugify

router = APIRouter(prefix="/api/prompt-gen", tags=["prompt-gen"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class CreateTileRequest(BaseModel):
    name:          str = "Prompt Generator"
    output_format: str = "flux"
    n_images:      int = 6
    steps:         int = 28
    resolution:    int = 1024


class CreateSessionRequest(BaseModel):
    name: str = "Nowa rozmowa"


class UpdateSessionRequest(BaseModel):
    conversation:  list[dict] | None = None
    prompt_fields: dict[str, str] | None = None
    name:          str | None = None


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = Field(default_factory=list)


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/intents")
def list_intents():
    return {
        key: {
            "label":     val["label"],
            "icon":      val["icon"],
            "keywords":  val["keywords"],
            "questions": val["questions"],
            "prompt_tips": val["prompt_tips"],
        }
        for key, val in prompt_gen_service.INTENTS.items()
    }


@router.get("/formats")
def list_formats():
    return {
        key: {"label": val["label"], "fields": val["fields"], "has_negative": val["has_negative"]}
        for key, val in prompt_gen_service.OUTPUT_FORMATS.items()
    }


@router.post("/{run_id}/tiles", status_code=201)
def create_tile(run_id: str, body: CreateTileRequest):
    if body.output_format not in prompt_gen_service.OUTPUT_FORMATS:
        raise HTTPException(400, f"Unknown output_format '{body.output_format}'")
    fmt = prompt_gen_service.OUTPUT_FORMATS[body.output_format]
    tile = {
        "id":            _slugify(body.name) + "_pg",
        "type":          "prompt_generator",
        "name":          body.name,
        "output_format": body.output_format,
        "n_images":      body.n_images,
        "steps":         body.steps,
        "resolution":    body.resolution,
        "sessions":      [],
    }
    data = _load(run_id)
    tiles = data.get("pic_flow") or []
    existing_ids = {t["id"] for t in tiles}
    base_id, n = tile["id"], 1
    while tile["id"] in existing_ids:
        tile["id"] = f"{base_id}_{n}"; n += 1
    tiles.append(tile)
    data["pic_flow"] = tiles
    _save(run_id, data)
    return tile


@router.get("/{run_id}/tiles/{tile_id}")
def get_tile(run_id: str, tile_id: str):
    try:
        return prompt_gen_service.get_tile_info(run_id, tile_id)
    except KeyError as e:
        raise HTTPException(404, str(e))


class UpdateTileRequest(BaseModel):
    output_format: str | None = None
    n_images:      int | None = None
    steps:         int | None = None
    resolution:    int | None = None


@router.patch("/{run_id}/tiles/{tile_id}")
def update_tile(run_id: str, tile_id: str, body: UpdateTileRequest):
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if "output_format" in updates and updates["output_format"] not in prompt_gen_service.OUTPUT_FORMATS:
        raise HTTPException(400, f"Unknown output_format '{updates['output_format']}'")
    try:
        prompt_gen_service._patch_tile(run_id, tile_id, updates)
        return prompt_gen_service.get_tile_info(run_id, tile_id)
    except KeyError as e:
        raise HTTPException(404, str(e))


# ── Sessions ──────────────────────────────────────────────────────────────────

@router.get("/{run_id}/tiles/{tile_id}/sessions")
def list_sessions(run_id: str, tile_id: str):
    try:
        return prompt_gen_service.list_sessions(run_id, tile_id)
    except KeyError as e:
        raise HTTPException(404, str(e))


@router.post("/{run_id}/tiles/{tile_id}/sessions", status_code=201)
def create_session(run_id: str, tile_id: str, body: CreateSessionRequest):
    try:
        return prompt_gen_service.create_session(run_id, tile_id, body.name)
    except KeyError as e:
        raise HTTPException(404, str(e))


@router.get("/{run_id}/tiles/{tile_id}/sessions/{session_id}")
def get_session(run_id: str, tile_id: str, session_id: str):
    try:
        return prompt_gen_service.get_session(run_id, tile_id, session_id)
    except KeyError as e:
        raise HTTPException(404, str(e))


@router.put("/{run_id}/tiles/{tile_id}/sessions/{session_id}")
def update_session(run_id: str, tile_id: str, session_id: str, body: UpdateSessionRequest):
    try:
        return prompt_gen_service.update_session(
            run_id, tile_id, session_id,
            conversation=body.conversation,
            prompt_fields=body.prompt_fields,
            name=body.name,
        )
    except KeyError as e:
        raise HTTPException(404, str(e))


@router.delete("/{run_id}/tiles/{tile_id}/sessions/{session_id}")
def delete_session(run_id: str, tile_id: str, session_id: str):
    try:
        prompt_gen_service.delete_session(run_id, tile_id, session_id)
        return {"ok": True}
    except KeyError as e:
        raise HTTPException(404, str(e))


@router.post("/{run_id}/tiles/{tile_id}/sessions/{session_id}/chat")
def chat(run_id: str, tile_id: str, session_id: str, body: ChatRequest):
    try:
        return prompt_gen_service.chat_in_session(
            run_id, tile_id, session_id, body.message, body.history,
        )
    except KeyError as e:
        raise HTTPException(404, str(e))
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Cost ──────────────────────────────────────────────────────────────────────

@router.get("/{run_id}/tiles/{tile_id}/cost")
def get_cost(run_id: str, tile_id: str):
    try:
        return prompt_gen_service.get_tile_cost(run_id, tile_id)
    except KeyError as e:
        raise HTTPException(404, str(e))
