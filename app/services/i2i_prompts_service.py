# -*- coding: utf-8 -*-
"""
Global I2I prompt library service.

Reads / writes  i2i_prompts.yaml  (repo root).

Structure
─────────
  categories:
    - id, name, icon, order
  defaults:
    steps, cfg, denoise
  prompts:
    - id, category, name, note, positive, negative, params

All operations are synchronous (file I/O only — no heavy work).
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT    = Path(__file__).parent.parent.parent
PROMPTS_PATH  = _REPO_ROOT / "i2i_prompts.yaml"

_DEFAULT_DOC: dict[str, Any] = {
    "categories": [],
    "defaults":   {"steps": 30, "cfg": 8, "denoise": 1.0},
    "prompts":    [],
    "last_id":    0,
}


# ── I/O ──────────────────────────────────────────────────────────────────────

def _load_raw() -> dict:
    try:
        text = PROMPTS_PATH.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def _save(data: dict) -> None:
    header = (
        "# i2i_prompts.yaml — Globalna biblioteka promptów Image-to-Image (Qwen Inpaint)\n"
        "# Edytuj z poziomu zakładki Pic w aplikacji lub bezpośrednio w tym pliku.\n\n"
    )
    body = yaml.dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=10_000,
    )
    PROMPTS_PATH.write_text(header + body, encoding="utf-8")


def load() -> dict:
    """Return full library dict with guaranteed keys."""
    raw = _load_raw()
    return {
        "categories": raw.get("categories") or [],
        "defaults":   raw.get("defaults")   or _DEFAULT_DOC["defaults"],
        "prompts":    raw.get("prompts")     or [],
        "last_id":    raw.get("last_id", 0),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    """Convert display text to a safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9_\-]", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "item"


def _unique_id(base: str, existing: list[str]) -> str:
    slug = _slugify(base)
    if slug not in existing:
        return slug
    for i in range(2, 999):
        candidate = f"{slug}_{i}"
        if candidate not in existing:
            return candidate
    return f"{slug}_{int(time.time())}"


# ── Categories ────────────────────────────────────────────────────────────────

def get_categories() -> list[dict]:
    return sorted(load()["categories"], key=lambda c: c.get("order", 999))


def create_category(name: str, icon: str = "🗂") -> dict:
    data = load()
    cats = data["categories"]
    existing_ids = [c["id"] for c in cats]
    max_order = max((c.get("order", 0) for c in cats), default=0)
    cat = {
        "id":    _unique_id(name, existing_ids),
        "name":  name,
        "icon":  icon,
        "order": max_order + 1,
    }
    cats.append(cat)
    data["categories"] = cats
    _save(data)
    return cat


def update_category(cat_id: str, name: str, icon: str) -> dict:
    data = load()
    for cat in data["categories"]:
        if cat["id"] == cat_id:
            cat["name"] = name
            cat["icon"] = icon
            _save(data)
            return cat
    raise KeyError(f"Category not found: {cat_id}")


def delete_category(cat_id: str) -> None:
    data = load()
    data["categories"] = [c for c in data["categories"] if c["id"] != cat_id]
    # also remove prompts in this category
    data["prompts"] = [p for p in data["prompts"] if p.get("category") != cat_id]
    _save(data)


def reorder_categories(ordered_ids: list[str]) -> None:
    data = load()
    idx = {cid: i for i, cid in enumerate(ordered_ids)}
    for cat in data["categories"]:
        cat["order"] = idx.get(cat["id"], 999)
    _save(data)


# ── Prompts ───────────────────────────────────────────────────────────────────

def get_prompts(category_id: str | None = None) -> list[dict]:
    prompts = load()["prompts"]
    if category_id:
        prompts = [p for p in prompts if p.get("category") == category_id]
    return prompts


def get_prompt(prompt_id: str) -> dict | None:
    for p in load()["prompts"]:
        if p["id"] == prompt_id:
            return p
    return None


def create_prompt(
    category: str,
    name: str,
    positive: str,
    negative: str = "",
    note: str = "",
    params: dict | None = None,
) -> dict:
    data = load()
    last_id = int(data.get("last_id") or 0) + 1
    prompt = {
        "id":       f"p{last_id:07d}",
        "category": category or "",
        "name":     name,
        "note":     note,
        "positive": positive,
        "negative": negative,
        "params":   params or {"steps": 30, "cfg": 8, "denoise": 1.0},
    }
    data["prompts"].append(prompt)
    data["last_id"] = last_id
    _save(data)
    return prompt


def update_prompt(prompt_id: str, updates: dict) -> dict:
    data = load()
    for p in data["prompts"]:
        if p["id"] == prompt_id:
            allowed = {"category", "name", "note", "positive", "negative", "params"}
            for k, v in updates.items():
                if k in allowed:
                    p[k] = v
            _save(data)
            return p
    raise KeyError(f"Prompt not found: {prompt_id}")


def delete_prompt(prompt_id: str) -> None:
    data = load()
    before = len(data["prompts"])
    data["prompts"] = [p for p in data["prompts"] if p["id"] != prompt_id]
    if len(data["prompts"]) == before:
        raise KeyError(f"Prompt not found: {prompt_id}")
    _save(data)


def get_defaults() -> dict:
    return load().get("defaults", _DEFAULT_DOC["defaults"])


def update_defaults(steps: int, cfg: float, denoise: float) -> dict:
    data = load()
    data["defaults"] = {"steps": steps, "cfg": cfg, "denoise": denoise}
    _save(data)
    return data["defaults"]


def get_all() -> dict:
    """Return full library (categories + defaults + prompts)."""
    return load()
