# -*- coding: utf-8 -*-
"""
Per-project Pic Studio session service.

Manages the `pic_flow` key inside each project's RUN_*.yaml file.

Unified tile schema (image_slots, supports 1×N and N×N):

  pic_flow:
    - id: "modelka_2"
      type: one_image_many_prompts   # kept for backwards compat
      name: "Modelka 2"
      source_dir:    "C:/projekty/kasia/model_source"
      output_dir:    "C:/projekty/kasia/i2i_studio/kasiaX_modele"
      global_suffix: ""
      image_slots:
        - image: "kasia_01.jpg"
          prompts:
            - id:       p0000001
              enabled:  true
              name:     "Ręce pod boki"
              positive: "..."
              negative: "..."
              note:     ""
              params:   { steps: 30, cfg: 8, denoise: 1.0 }
        - image: "kasia_02.jpg"
          prompts:
            - id: p0000001
              ...   # independent copy — can differ from other slots

Output file naming: {output_dir}/{output_id}.png
  where output_id is an 18-char random ID stored in each prompt instance in image_slots.

Old format migration (source_image + top-level prompts):
  Tiles with `source_image` key are auto-migrated to image_slots on load.
"""

from __future__ import annotations

import json
import random
import re
import string
import time
from pathlib import Path
from typing import Any

import yaml

from app.services.run_file_service import RUNS_FOLDER
from app.services import i2i_prompts_service

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}
_OUTPUT_ID_CHARS = string.ascii_letters + string.digits  # 62 chars → 62^18 ≈ 1.6×10³²


# ── Helpers ────────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9_\-]", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "tile"


def _make_output_id() -> str:
    """Generate an 18-character random output file ID."""
    return "".join(random.choices(_OUTPUT_ID_CHARS, k=18))


def _get_source_dirs(tile: dict) -> list[str]:
    """Return list of source directories; handles both source_dirs (list) and legacy source_dir (str)."""
    dirs = tile.get("source_dirs")
    if isinstance(dirs, list):
        return [d for d in dirs if d]
    single = tile.get("source_dir", "")
    return [single] if single else []


def _get_dirs_field(tile: dict, multi_key: str, single_key: str) -> list[str]:
    """Generic multi-dir helper: reads `multi_key` list, falls back to `single_key` string."""
    dirs = tile.get(multi_key)
    if isinstance(dirs, list):
        return [d for d in dirs if d]
    single = tile.get(single_key, "")
    return [single] if single else []


def _archive_slot_outputs(output_dir: Path, output_ids: list[str]) -> int:
    """Move generated files for *output_ids* into output_dir/archive/. Returns count moved."""
    if not output_dir.is_dir() or not output_ids:
        return 0
    archive_dir = output_dir / "archive"
    archive_dir.mkdir(exist_ok=True)
    count = 0
    for oid in output_ids:
        for ext in _IMAGE_EXTS:
            src = output_dir / f"{oid}{ext}"
            if src.exists():
                dest = archive_dir / src.name
                if dest.exists():
                    stem, n = src.stem, 1
                    while dest.exists():
                        dest = archive_dir / f"{stem}_{n}{ext}"
                        n += 1
                src.rename(dest)
                count += 1
    return count


def _archive_changed_outputs(old_tile: dict, updates: dict) -> None:
    """
    Compare old tile image references with incoming updates.
    For every slot whose source image changed, archive existing output files.
    output_ids are preserved (not reassigned) so new generation overwrites correctly.
    """
    output_dir = Path(old_tile.get("output_dir") or updates.get("output_dir") or "")
    if not output_dir.is_dir():
        return

    tile_type = old_tile.get("type", "one_image_many_prompts")

    if tile_type == "one_image_many_prompts":
        new_slots = updates.get("image_slots", [])
        for i, old_slot in enumerate(old_tile.get("image_slots", [])):
            if i >= len(new_slots):
                break
            if old_slot.get("image") != new_slots[i].get("image"):
                oids = [p["output_id"] for p in old_slot.get("prompts", []) if p.get("output_id")]
                _archive_slot_outputs(output_dir, oids)

    elif tile_type == "character_insert":
        new_slots = updates.get("scene_slots", [])
        for i, old_slot in enumerate(old_tile.get("scene_slots", [])):
            if i >= len(new_slots):
                break
            if old_slot.get("scene_image") != new_slots[i].get("scene_image"):
                oids = [p["output_id"] for p in old_slot.get("prompts", []) if p.get("output_id")]
                _archive_slot_outputs(output_dir, oids)

    elif tile_type == "paste_character":
        new_slots = updates.get("paste_slots", [])
        for i, old_slot in enumerate(old_tile.get("paste_slots", [])):
            if i >= len(new_slots):
                break
            new_slot    = new_slots[i]
            scene_diff  = old_slot.get("scene_image") != new_slot.get("scene_image")
            old_chars   = old_slot.get("characters", [])
            new_chars   = new_slot.get("characters", [])
            chars_diff  = len(old_chars) != len(new_chars) or any(
                oc.get("model_image") != nc.get("model_image")
                for oc, nc in zip(old_chars, new_chars)
            )
            if scene_diff or chars_diff:
                oid = old_slot.get("output_id") or old_slot.get("id")
                if oid:
                    _archive_slot_outputs(output_dir, [oid])


def _ensure_output_ids(tile: dict) -> bool:
    """
    Assign output_id to every prompt that is missing one, and fix duplicates.
    Duplicate output_ids across slots would cause two slots to write to the same
    output file — one overwriting the other.  We detect and fix them here.

    Handles:
      - one_image_many_prompts  → image_slots[].prompts[]
      - character_insert        → scene_slots[].prompts[]
                                  (legacy: top-level prompts[] migrated by _migrate_tile)
    Returns True if any IDs were newly assigned (caller should persist).
    """
    changed = False
    seen_output_ids: set[str] = set()

    if tile.get("type") == "character_insert":
        for slot in tile.get("scene_slots", []):
            for p in slot.get("prompts", []):
                oid = p.get("output_id")
                if not oid or oid in seen_output_ids:
                    p["output_id"] = _make_output_id()
                    changed = True
                else:
                    seen_output_ids.add(oid)
    else:
        for slot in tile.get("image_slots", []):
            for p in slot.get("prompts", []):
                oid = p.get("output_id")
                if not oid or oid in seen_output_ids:
                    p["output_id"] = _make_output_id()
                    changed = True
                else:
                    seen_output_ids.add(oid)
    return changed


def _last_active_stage(tile: dict) -> int:
    """Return highest stage index that is configured and enabled (0=paste, 1=edge, 2=scene)."""
    if tile.get("scene_blend_enabled") and any(
        p.get("enabled", True) for p in tile.get("scene_blend_prompts", [])
    ):
        return 2
    if tile.get("edge_blend_enabled") and any(
        p.get("enabled", True) for p in tile.get("edge_blend_prompts", [])
    ):
        return 1
    return 0


def _get_tile_type(run_id: str, tile_id: str) -> str:
    """Return the type string of a tile ('one_image_many_prompts' by default)."""
    data = _load(run_id)
    tile = next((t for t in data.get("pic_flow", []) if t["id"] == tile_id), None)
    return tile.get("type", "one_image_many_prompts") if tile else "one_image_many_prompts"


def _unique_id(base: str, existing: list[str]) -> str:
    slug = _slugify(base)
    if slug not in existing:
        return slug
    for i in range(2, 999):
        candidate = f"{slug}_{i}"
        if candidate not in existing:
            return candidate
    return f"{slug}_{int(time.time())}"


# ── Migration ──────────────────────────────────────────────────────────────────

def _migrate_tile(tile: dict) -> dict:
    """
    Migrate tile to current format. Mutates tile in-place and returns it.

    OI migrations:
      source_image + top-level prompts  →  image_slots

    CI migrations:
      scene_dir       →  scene_dirs  (list)
      characters_dir  →  characters_dirs  (list)
      scene_image + character_images + top-level prompts  →  scene_slots[0]
    """
    tile_type = tile.get("type", "one_image_many_prompts")

    if tile_type == "paste_character":
        tile.setdefault("paste_slots", [])

        # ── paste_slots: migrate old single model_image → characters list ─────
        for slot in tile["paste_slots"]:
            if "characters" not in slot:
                char = {}
                for k in ("model_image", "top_pct", "bottom_pct",
                          "x_center_pct", "erode_px", "blur_px"):
                    if k in slot:
                        char[k] = slot.pop(k)
                slot["characters"] = [char] if char.get("model_image") else []

        # ── edge blend: consolidate all legacy shapes → edge_blend_prompts ────
        tile.setdefault("edge_blend_enabled", False)
        tile.setdefault("edge_blend_px", 15)
        if not tile.get("edge_blend_prompts"):
            # gather from oldest → newest legacy keys
            if "blend_enabled" in tile:
                tile["edge_blend_enabled"] = tile.pop("blend_enabled", False)
            pos = tile.pop("blend_positive",        None) \
               or tile.pop("edge_blend_positive",   None) or ""
            neg = tile.pop("blend_negative",        None) \
               or tile.pop("edge_blend_negative",   None) or ""
            par = tile.pop("blend_params",          None) \
               or tile.pop("edge_blend_params",     None) \
               or {"steps": 30, "cfg": 8, "denoise": 0.6}
            if pos:
                tile["edge_blend_prompts"] = [{
                    "id": "local_eb_0", "name": "Edge Blend",
                    "positive": pos, "negative": neg, "params": par,
                    "enabled": True, "_notInLibrary": True,
                }]
            elif tile.get("edge_blend_enabled"):
                # Pass enabled but no prompt — auto-load system default p0000021
                sys_p = i2i_prompts_service.get_prompt("p0000021")
                tile["edge_blend_prompts"] = ([dict(sys_p)] if sys_p else [])
            else:
                tile["edge_blend_prompts"] = []
        else:
            # clean up stale keys if prompts already present
            for k in ("blend_positive", "blend_negative", "blend_params",
                      "edge_blend_positive", "edge_blend_negative", "edge_blend_params"):
                tile.pop(k, None)

        # ── scene blend: same consolidation ───────────────────────────────────
        tile.setdefault("scene_blend_enabled", False)
        if not tile.get("scene_blend_prompts"):
            pos = tile.pop("scene_blend_positive", None) or ""
            neg = tile.pop("scene_blend_negative", None) or ""
            par = tile.pop("scene_blend_params",   None) \
               or {"steps": 30, "cfg": 8, "denoise": 0.4}
            if pos:
                tile["scene_blend_prompts"] = [{
                    "id": "local_sb_0", "name": "Scene Blend",
                    "positive": pos, "negative": neg, "params": par,
                    "enabled": True, "_notInLibrary": True,
                }]
            elif tile.get("scene_blend_enabled"):
                # Pass enabled but no prompt — auto-load system default p0000022
                sys_p = i2i_prompts_service.get_prompt("p0000022")
                tile["scene_blend_prompts"] = ([dict(sys_p)] if sys_p else [])
            else:
                tile["scene_blend_prompts"] = []
        else:
            for k in ("scene_blend_positive", "scene_blend_negative", "scene_blend_params"):
                tile.pop(k, None)

        return tile

    if tile_type == "character_insert":
        # 1. Migrate single-dir → multi-dir
        if "scene_dir" in tile and "scene_dirs" not in tile:
            tile["scene_dirs"] = [tile.pop("scene_dir")] if tile["scene_dir"] else []
        elif "scene_dir" in tile:
            tile.pop("scene_dir", None)

        if "characters_dir" in tile and "characters_dirs" not in tile:
            tile["characters_dirs"] = [tile.pop("characters_dir")] if tile["characters_dir"] else []
        elif "characters_dir" in tile:
            tile.pop("characters_dir", None)

        tile.setdefault("scene_dirs", [])
        tile.setdefault("characters_dirs", [])

        # 2. Migrate flat scene_image / character_images / prompts → scene_slots
        if "scene_slots" not in tile:
            old_scene  = tile.pop("scene_image",      "")
            old_chars  = tile.pop("character_images", [])
            old_prompts = tile.pop("prompts",         [])
            tile["scene_slots"] = (
                [{"scene_image": old_scene, "character_images": old_chars,
                  "prompts": old_prompts}]
                if old_scene else []
            )
        else:
            # Clean up any leftover legacy top-level keys
            tile.pop("scene_image",      None)
            tile.pop("character_images", None)
            tile.pop("prompts",          None)

        return tile

    # ── OI migration: source_image + top-level prompts → image_slots ─────────
    if "image_slots" in tile:
        return tile
    old_image   = tile.pop("source_image", "")
    old_prompts = tile.pop("prompts",      [])
    tile["image_slots"] = (
        [{"image": old_image, "prompts": old_prompts}] if old_image else []
    )
    return tile


# ── I/O ────────────────────────────────────────────────────────────────────────

def _load(run_id: str) -> dict:
    path = RUNS_FOLDER / run_id
    if not path.exists():
        raise FileNotFoundError(f"Session file not found: {run_id}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def _save(run_id: str, data: dict) -> None:
    path = RUNS_FOLDER / run_id
    path.write_text(
        yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=10_000,
        ),
        encoding="utf-8",
    )


# ── CRUD ───────────────────────────────────────────────────────────────────────

def get_tiles(run_id: str) -> list[dict]:
    data  = _load(run_id)
    tiles = data.get("pic_flow", [])
    # Migrate old-format tiles transparently; persist only if something changed
    changed = False
    for tile in tiles:
        before = "image_slots" in tile
        _migrate_tile(tile)
        if not before:
            changed = True
        if _ensure_output_ids(tile):
            changed = True
    if changed:
        data["pic_flow"] = tiles
        _save(run_id, data)
    return tiles


def create_tile(run_id: str, tile_data: dict) -> dict:
    data = _load(run_id)
    tiles: list[dict] = data.get("pic_flow", [])
    existing_ids = [t["id"] for t in tiles]
    tile = dict(tile_data)
    _migrate_tile(tile)          # normalise in case caller sends old format
    _ensure_output_ids(tile)     # assign output_id to any new prompts
    tile["id"] = _unique_id(tile.get("name", "tile"), existing_ids)
    tiles.append(tile)
    data["pic_flow"] = tiles
    _save(run_id, data)
    return tile


def update_tile(run_id: str, tile_id: str, updates: dict) -> dict:
    data = _load(run_id)
    for tile in data.get("pic_flow", []):
        if tile["id"] == tile_id:
            _migrate_tile(tile)
            for k, v in updates.items():
                if k != "id":
                    tile[k] = v
            # Clean up legacy source_dir when new source_dirs key is present
            if "source_dirs" in updates:
                tile.pop("source_dir", None)
            _migrate_tile(tile)      # in case updates brought old keys
            _ensure_output_ids(tile) # assign output_id to any new/missing prompts
            _save(run_id, data)
            return tile
    raise KeyError(f"Tile not found: {tile_id}")


def delete_tile(run_id: str, tile_id: str) -> None:
    data = _load(run_id)
    data["pic_flow"] = [t for t in data.get("pic_flow", []) if t["id"] != tile_id]
    _save(run_id, data)


def reorder_tiles(run_id: str, ids: list[str]) -> list[dict]:
    """Reorder pic_flow tiles to match the given id order.
    Tiles not present in *ids* are appended at the end unchanged."""
    data  = _load(run_id)
    tiles = data.get("pic_flow", [])
    by_id = {t["id"]: t for t in tiles}
    ordered   = [by_id[i] for i in ids if i in by_id]
    leftover  = [t for t in tiles if t["id"] not in set(ids)]
    data["pic_flow"] = ordered + leftover
    _save(run_id, data)
    return data["pic_flow"]


def add_prompt_to_slot(
    run_id: str,
    tile_id: str,
    slot_index: int,
    prompt: dict,
) -> dict:
    """
    Add a prompt (from global library) to a specific image slot.
    No-op if a prompt with the same id already exists in that slot.
    Returns the updated tile dict.
    """
    data = _load(run_id)
    for tile in data.get("pic_flow", []):
        if tile["id"] == tile_id:
            _migrate_tile(tile)
            slots: list[dict] = tile.get("image_slots", [])
            if slot_index < 0 or slot_index >= len(slots):
                raise IndexError(
                    f"Slot index {slot_index} out of range "
                    f"(tile has {len(slots)} slot(s))"
                )
            slot    = slots[slot_index]
            prompts = slot.setdefault("prompts", [])
            if not any(p["id"] == prompt["id"] for p in prompts):
                p = dict(prompt)
                if not p.get("output_id"):
                    p["output_id"] = _make_output_id()
                prompts.append(p)
                _save(run_id, data)
            return tile
    raise KeyError(f"Tile not found: {tile_id}")


def add_prompt_to_all_slots(run_id: str, tile_id: str, prompt: dict) -> dict:
    """
    Add a prompt to every image slot that doesn't already have it.
    Returns the updated tile dict.
    """
    data = _load(run_id)
    for tile in data.get("pic_flow", []):
        if tile["id"] == tile_id:
            _migrate_tile(tile)
            for slot in tile.get("image_slots", []):
                prompts = slot.setdefault("prompts", [])
                if not any(p["id"] == prompt["id"] for p in prompts):
                    p = dict(prompt)
                    if not p.get("output_id"):
                        p["output_id"] = _make_output_id()
                    prompts.append(p)
            _save(run_id, data)
            return tile
    raise KeyError(f"Tile not found: {tile_id}")


def add_prompt_to_all_scene_slots(run_id: str, tile_id: str, prompt: dict) -> dict:
    """
    Add a prompt copy (with a fresh output_id) to every scene_slot of a
    character_insert tile that doesn't already have a prompt with the same id.
    Returns the updated tile dict.
    """
    data = _load(run_id)
    for tile in data.get("pic_flow", []):
        if tile["id"] == tile_id:
            _migrate_tile(tile)
            changed = False
            for slot in tile.get("scene_slots", []):
                prompts = slot.setdefault("prompts", [])
                if not any(p["id"] == prompt["id"] for p in prompts):
                    p = dict(prompt)
                    p["output_id"] = _make_output_id()   # always fresh per slot
                    prompts.append(p)
                    changed = True
            if changed:
                _save(run_id, data)
            return tile
    raise KeyError(f"Tile not found: {tile_id}")


def copy_tile(run_id: str, tile_id: str) -> dict:
    data = _load(run_id)
    tiles: list[dict] = data.get("pic_flow", [])
    original = next((t for t in tiles if t["id"] == tile_id), None)
    if not original:
        raise KeyError(f"Tile not found: {tile_id}")
    _migrate_tile(original)
    new_tile = json.loads(json.dumps(original))
    existing_ids = [t["id"] for t in tiles]
    new_tile["id"]   = _unique_id(new_tile.get("name", "tile") + "_kopia", existing_ids)
    new_tile["name"] = new_tile.get("name", "") + " (kopia)"

    # Reset all output_ids so the copy doesn't share file names with the original.
    # paste_character: each paste_slot has its own output_id (used for file naming)
    for slot in new_tile.get("paste_slots", []):
        slot["output_id"] = _make_output_id()
        # also regenerate the slot id to avoid API collisions
        slot["id"] = str(__import__("uuid").uuid4())
    # one_image_many_prompts / character_insert: prompts carry output_id
    for slot in new_tile.get("image_slots", []):
        for p in slot.get("prompts", []):
            p["output_id"] = _make_output_id()
    for slot in new_tile.get("scene_slots", []):
        for p in slot.get("prompts", []):
            p["output_id"] = _make_output_id()

    tiles.append(new_tile)
    data["pic_flow"] = tiles
    _save(run_id, data)
    return new_tile


# ── Status ─────────────────────────────────────────────────────────────────────

def get_tile_status(run_id: str, tile_id: str) -> dict:
    """
    Compute generation status by scanning output_dir for files matching
    {output_id}.<ext>  (output_id is stored per prompt instance in image_slots).

    Returns:
        overall:  'all' | 'partial' | 'none' | 'empty'
        done:     int   (# enabled prompt×image combos with output file)
        total:    int   (# enabled prompt×image combos)
        slots:    [{ image, done, total, prompts: {pid: {done, output_path, output_id}} }]
    """
    data = _load(run_id)
    tile = next(
        (t for t in data.get("pic_flow", []) if t["id"] == tile_id), None
    )
    if not tile:
        raise KeyError(f"Tile not found: {tile_id}")

    _migrate_tile(tile)

    output_dir = Path(tile.get("output_dir", ""))

    # ── paste_character: paste_slots ──────────────────────────────────────────
    if tile.get("type") == "paste_character":
        paste_slots  = tile.get("paste_slots", [])
        total_done   = 0
        total_count  = len(paste_slots)
        slot_statuses: list[dict[str, Any]] = []

        work_dir = output_dir / "robocze"

        for slot in paste_slots:
            oid        = slot.get("output_id", slot.get("id", ""))
            n_chars    = len(slot.get("characters", []))
            slot_sb      = bool(slot.get("scene_blend_enabled", True))
            global_eb    = bool(tile.get("edge_blend_enabled", False))
            global_sb    = bool(tile.get("scene_blend_enabled", False))
            chars_cfg    = slot.get("characters", [])
            last_char_eb = bool(chars_cfg[-1].get("edge_blend_enabled", True)) if chars_cfg else True

            def _find_file(stem: str) -> str | None:
                """Check working_dir first, then output_dir root (legacy/finalized)."""
                if not oid or not output_dir.is_dir():
                    return None
                for search_dir in (work_dir, output_dir):
                    for ext in _IMAGE_EXTS:
                        p = search_dir / f"{stem}{ext}"
                        if p.exists():
                            return str(p)
                return None

            def _is_final(stem: str) -> bool:
                """True if file exists in output_dir root (finalized, not just in robocze/)."""
                for ext in _IMAGE_EXTS:
                    if (output_dir / f"{stem}{ext}").exists():
                        return True
                return False

            # Per-character pil + edge paths
            chars_status: list[dict] = []
            for ci in range(n_chars):
                chars_status.append({
                    "pil":       _find_file(f"{oid}_c{ci}_pil"),
                    "pil_final": _is_final(f"{oid}_c{ci}_pil"),
                    "edge":      _find_file(f"{oid}_c{ci}_edge"),
                    "edge_final":_is_final(f"{oid}_c{ci}_edge"),
                })

            scene_file  = _find_file(f"{oid}_scene")
            scene_final = _is_final(f"{oid}_scene")

            # Custom passes
            cp_statuses: list[dict] = []
            for ci, cp in enumerate(slot.get("custom_passes", [])):
                cp_file  = _find_file(f"{oid}_cp{ci}")
                cp_final = _is_final(f"{oid}_cp{ci}")
                cp_statuses.append({
                    "path":    cp_file,
                    "final":   cp_final,
                    "enabled": cp.get("enabled", True),
                    "name":    cp.get("name") or f"Pass {ci+1}",
                })

            # Legacy fallback: old _s0/_s1/_s2 files → map to single char entry
            if not any(c["pil"] for c in chars_status):
                s0 = _find_file(f"{oid}_s0")
                s1 = _find_file(f"{oid}_s1")
                s2 = _find_file(f"{oid}_s2")
                if s0:
                    chars_status = [{"pil": s0, "pil_final": False,
                                     "edge": s1, "edge_final": False}]
                    if not scene_file:
                        scene_file = s2
                # Very old format: bare {oid}.png
                elif _find_file(oid):
                    chars_status = [{"pil": _find_file(oid), "pil_final": False,
                                     "edge": None, "edge_final": False}]

            # "done" = last stage that generation can actually produce.
            # Mirrors the skip-check in _run_paste_character_async: a pass only
            # counts as "expected" if it is enabled AND has a configured prompt.
            def _has_prompt(prompts_list: list) -> bool:
                return any(
                    (p.get("positive") or "").strip()
                    for p in prompts_list
                    if p.get("enabled", True)
                )
            sb_has_prompt = _has_prompt(tile.get("scene_blend_prompts", []))
            eb_has_prompt = _has_prompt(tile.get("edge_blend_prompts", []))

            # Last enabled custom pass with a positive prompt is the true done_file
            _active_cp = [cp for cp in cp_statuses if cp["enabled"]]
            if _active_cp:
                done_file  = _active_cp[-1]["path"]
                final_file = _active_cp[-1]["final"]
            elif global_sb and slot_sb and sb_has_prompt:
                done_file  = scene_file
                final_file = scene_final
            elif global_eb and last_char_eb and n_chars and eb_has_prompt:
                done_file  = chars_status[-1]["edge"] if chars_status else None
                final_file = chars_status[-1]["edge_final"] if chars_status else False
            else:
                done_file  = chars_status[-1]["pil"] if chars_status else None
                final_file = chars_status[-1]["pil_final"] if chars_status else False

            found = bool(done_file)
            if found:
                total_done += 1

            slot_final = final_file

            # output_path = most advanced file (for thumbnail / compat)
            output_path = (
                next((cp["path"] for cp in reversed(_active_cp) if cp["path"]), None)
                or scene_file
                or next((c["edge"] for c in reversed(chars_status) if c["edge"]), None)
                or next((c["pil"]  for c in reversed(chars_status) if c["pil"]),  None)
            )

            slot_statuses.append({
                "scene_image":    slot.get("scene_image", ""),
                "done":           1 if found else 0,
                "total":          1,
                "output_path":    output_path,
                "output_id":      oid,
                "chars":          chars_status,
                "scene":          scene_file,
                "scene_final":    scene_final,
                "slot_final":     slot_final,
                "custom_passes":  cp_statuses,
            })

        overall = (
            "empty"   if total_count == 0 else
            "none"    if total_done  == 0 else
            "all"     if total_done  >= total_count else
            "partial"
        )
        return {
            "tile_id": tile_id,
            "overall": overall,
            "done":    total_done,
            "total":   total_count,
            "slots":   slot_statuses,
        }

    # ── character_insert: scene_slots ─────────────────────────────────────────
    if tile.get("type") == "character_insert":
        scene_slots = tile.get("scene_slots", [])
        slot_statuses: list[dict[str, Any]] = []
        total_done  = 0
        total_count = 0

        for slot in scene_slots:
            scene_image     = slot.get("scene_image", "")
            character_images = slot.get("character_images", [])
            prompts          = slot.get("prompts", [])
            enabled          = [p for p in prompts if p.get("enabled", True)]

            prompt_status: dict[str, Any] = {}
            for p in enabled:
                oid   = p.get("output_id", "")
                found = False
                out_p = None
                if oid and output_dir.is_dir():
                    for ext in _IMAGE_EXTS:
                        candidate = output_dir / f"{oid}{ext}"
                        if candidate.exists():
                            found = True
                            out_p = str(candidate)
                            break
                prompt_status[p["id"]] = {"done": found, "output_path": out_p, "output_id": oid}

            slot_done  = sum(1 for s in prompt_status.values() if s["done"])
            slot_total = len(enabled)
            total_done  += slot_done
            total_count += slot_total

            slot_statuses.append({
                "scene_image":      scene_image,
                "character_images": character_images,
                "done":    slot_done,
                "total":   slot_total,
                "prompts": prompt_status,
            })

        overall = (
            "empty"   if total_count == 0 else
            "none"    if total_done  == 0 else
            "all"     if total_done  >= total_count else
            "partial"
        )
        return {
            "tile_id": tile_id,
            "overall": overall,
            "done":    total_done,
            "total":   total_count,
            "slots":   slot_statuses,
        }

    # ── one_image_many_prompts: slot-based ────────────────────────────────────
    image_slots = tile.get("image_slots", [])
    slot_statuses: list[dict[str, Any]] = []
    total_done  = 0
    total_count = 0

    for slot in image_slots:
        image_name  = slot.get("image", "")
        prompts     = slot.get("prompts", [])
        enabled     = [p for p in prompts if p.get("enabled", True)]

        prompt_status: dict[str, Any] = {}
        for p in enabled:
            pid   = p["id"]
            oid   = p.get("output_id", "")
            found = False
            out_p = None
            if oid and output_dir.is_dir():
                for ext in _IMAGE_EXTS:
                    candidate = output_dir / f"{oid}{ext}"
                    if candidate.exists():
                        found = True
                        out_p = str(candidate)
                        break
            prompt_status[pid] = {"done": found, "output_path": out_p, "output_id": oid}

        slot_done  = sum(1 for s in prompt_status.values() if s["done"])
        slot_total = len(enabled)
        total_done  += slot_done
        total_count += slot_total

        slot_statuses.append({
            "image":   image_name,
            "done":    slot_done,
            "total":   slot_total,
            "prompts": prompt_status,
        })

    if total_count == 0:
        overall = "empty"
    elif total_done == 0:
        overall = "none"
    elif total_done >= total_count:
        overall = "all"
    else:
        overall = "partial"

    return {
        "tile_id": tile_id,
        "overall": overall,
        "done":    total_done,
        "total":   total_count,
        "slots":   slot_statuses,
    }
