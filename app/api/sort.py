# -*- coding: utf-8 -*-
"""
API router for Sort view — flow reordering and scene_break management.

Endpoints:
    GET  /api/sort/{filename}          → flow items enriched with thumbnail URLs
    PUT  /api/sort/{filename}          → save reordered flow (full replacement)
    POST /api/sort/{filename}/scene-break → insert scene_break at given index
"""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.run_file_service import get_run_flow, RUNS_FOLDER
from app.services.yaml_service import save_yaml_flow, yaml_flow_to_internal
from app.services import media_service

router = APIRouter(prefix="/api/sort", tags=["sort"])

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
_VIDEO_EXTS = {".mp4", ".webm", ".mov"}


def _item_type(item: dict) -> str:
    if item.get("break"):
        return "break"
    if item.get("type") == "scene_break":
        return "scene_break"
    if item.get("type") == "talk":
        return "talk"
    if "chain" in item:
        return "chain"
    if item.get("file"):
        ext = Path(item["file"]).suffix.lower()
        return "video" if ext in _VIDEO_EXTS else "file"
    return "unknown"


def _thumbnail_url(filename: str, item: dict) -> str | None:
    """Return a /api/media/frame URL for items that have a source file."""
    src = item.get("file")
    if not src:
        return None
    return f"/api/media/frame?run={filename}&file={src}&kind=start"


def _enrich(filename: str, flow: list[dict]) -> list[dict]:
    results = []
    for idx, item in enumerate(flow):
        itype = _item_type(item)
        entry: dict[str, Any] = {
            "_sort_idx":   idx,
            "_type":       itype,
            "_thumb_url":  _thumbnail_url(filename, item) if itype in ("file", "video") else None,
        }
        entry.update(item)
        results.append(entry)
    return results


# ── GET ───────────────────────────────────────────────────────────────────────

@router.get("/{filename}")
async def get_sort_flow(filename: str):
    flow_data = get_run_flow(filename)
    if not flow_data:
        raise HTTPException(status_code=404, detail=f"Run not found or has no flow: {filename}")
    enriched = _enrich(filename, flow_data["flow"])
    return {"flow": enriched, "flow_type": flow_data.get("flow_type", "default")}


# ── PUT (reorder + scene_break edits) ────────────────────────────────────────

class SortSaveBody(BaseModel):
    flow: list[dict]
    flow_key: str = "flow"


@router.put("/{filename}")
async def save_sort_flow(filename: str, body: SortSaveBody):
    path = RUNS_FOLDER / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Run file not found: {filename}")
    if path.suffix.lower() != ".yaml":
        raise HTTPException(status_code=400, detail="Only YAML run files can be reordered via Sort")

    # Strip display-only _sort_* keys before saving
    clean = []
    for item in body.flow:
        clean.append({k: v for k, v in item.items() if not k.startswith("_")})

    try:
        save_yaml_flow(path, clean, flow_key=body.flow_key)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"ok": True, "saved": len(clean)}


# ── POST scene-break ──────────────────────────────────────────────────────────

class SceneBreakBody(BaseModel):
    name: str = ""
    after_index: int  # insert after this _sort_idx (-1 = at start)


@router.post("/{filename}/scene-break")
async def insert_scene_break(filename: str, body: SceneBreakBody):
    path = RUNS_FOLDER / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Run file not found: {filename}")
    if path.suffix.lower() != ".yaml":
        raise HTTPException(status_code=400, detail="Only YAML run files support scene breaks")

    flow_data = get_run_flow(filename)
    if not flow_data:
        raise HTTPException(status_code=404, detail="No flow found")

    flow = list(flow_data["flow"])
    insert_at = max(0, body.after_index + 1)
    flow.insert(insert_at, {"type": "scene_break", "name": body.name})

    try:
        save_yaml_flow(path, flow, flow_key=flow_data.get("flow_type_key", "flow"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"ok": True, "inserted_at": insert_at}
