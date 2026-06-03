# -*- coding: utf-8 -*-
"""
Pic Studio generation service.

Generates images for a single tile (type: one_image_many_prompts) by:
  1. Loading the Qwen Image Edit API-format workflow JSON
  2. For each enabled prompt (skipping done ones unless force_all=True):
     a. Copy source image  →  ComfyUI input dir  (unique temp name)
     b. Patch workflow (image, positive, negative, seed, steps, cfg, denoise,
        filename_prefix)
     c. POST  ComfyUI /prompt
     d. Poll  /history/{prompt_id}  until done (every 3 s, max 20 min)
     e. Copy  ComfyUI output image  →  {output_dir}/{source_stem}__{prompt_id}.png
     f. Delete temp input file

Workflow node mapping (by class_type + ControlNet reference traversal):
  LoadImage                         → inputs.image
  KSampler                          → inputs.seed / steps / cfg / denoise
  SaveImage                         → inputs.filename_prefix
  ControlNetInpaintingAliMamaApply  → reveals positive/negative node IDs
    → positive TextEncodeQwenImageEditPlus → inputs.prompt
    → negative TextEncodeQwenImageEditPlus → inputs.prompt

Job state is stored in module-level _jobs dict and polled via get_job().
"""

from __future__ import annotations

import asyncio
import copy
import json
import random
import shutil
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.services import app_config_service

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}

# Late import to avoid circular dependency at module load time
def _log(text: str) -> None:
    """Write to the WebSocket generation log (visible in main log panel)."""
    try:
        from app.services.process_service import process_service
        process_service.log_sys(text)
    except Exception:
        pass  # never break generation over a logging failure

# ── Job registry ──────────────────────────────────────────────────────────────
# key: "{run_id}::{tile_id}"
_jobs: dict[str, dict] = {}


def get_job(run_id: str, tile_id: str) -> dict:
    """Return a copy of the current job state (or {status: idle})."""
    return dict(_jobs.get(f"{run_id}::{tile_id}", {"status": "idle"}))


def _set_job(run_id: str, tile_id: str, data: dict) -> None:
    _jobs[f"{run_id}::{tile_id}"] = data


def _update_job(run_id: str, tile_id: str, **kwargs) -> None:
    key = f"{run_id}::{tile_id}"
    _jobs.setdefault(key, {}).update(kwargs)


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _http_post(url: str, payload: dict, timeout: int = 15) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _http_get(url: str, timeout: int = 10) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


# ── Workflow patching ─────────────────────────────────────────────────────────

def _find_node(workflow: dict, class_type: str) -> tuple[str | None, dict | None]:
    """Return (node_id, node) for the first node with the given class_type."""
    for nid, node in workflow.items():
        if isinstance(node, dict) and node.get("class_type") == class_type:
            return nid, node
    return None, None


def _patch_workflow(
    workflow:         dict,
    source_filename:  str,
    positive:         str,
    negative:         str,
    steps:            int,
    cfg:              float,
    denoise:          float,
    filename_prefix:  str,
) -> dict:
    wf = copy.deepcopy(workflow)

    # ── LoadImage → source filename ───────────────────────────────────────────
    # Use mask-wiring detection to find the main image node (same logic as CI).
    # This handles workflows with 1 or 2 LoadImage nodes correctly regardless
    # of dict ordering — the scene/main node is the one whose mask output [id,1]
    # is referenced elsewhere in the graph.
    scene_pair, _ = _split_ci_load_image_nodes(wf)
    if scene_pair:
        scene_pair[1]["inputs"]["image"] = source_filename
    else:
        # Fallback for simple workflows with no mask wiring
        nid, node = _find_node(wf, "LoadImage")
        if nid:
            node["inputs"]["image"] = source_filename

    # ── KSampler → generation params ─────────────────────────────────────────
    nid, node = _find_node(wf, "KSampler")
    if nid:
        node["inputs"]["seed"]    = random.randint(0, 2 ** 32 - 1)
        node["inputs"]["steps"]   = steps
        node["inputs"]["cfg"]     = cfg
        node["inputs"]["denoise"] = denoise

    # ── SaveImage → unique output prefix ─────────────────────────────────────
    nid, node = _find_node(wf, "SaveImage")
    if nid:
        node["inputs"]["filename_prefix"] = filename_prefix

    # ── Positive / Negative text encode ──────────────────────────────────────
    # Resolve via ControlNetInpaintingAliMamaApply's positive/negative references.
    _, cn_node = _find_node(wf, "ControlNetInpaintingAliMamaApply")
    if cn_node:
        pos_id = cn_node["inputs"].get("positive", [None])[0]  # e.g. "15"
        neg_id = cn_node["inputs"].get("negative", [None])[0]  # e.g. "11"
        if pos_id and pos_id in wf:
            wf[pos_id]["inputs"]["prompt"] = positive
        if neg_id and neg_id in wf:
            wf[neg_id]["inputs"]["prompt"] = negative or ""
    else:
        # Fallback: patch ALL TextEncodeQwenImageEditPlus nodes
        for node in wf.values():
            if (isinstance(node, dict) and
                    node.get("class_type") == "TextEncodeQwenImageEditPlus"):
                node["inputs"]["prompt"] = positive

    return wf


def _find_image_in_outputs(outputs: dict) -> dict | None:
    """Scan ALL output nodes for an images list; return first image entry found."""
    for node_out in outputs.values():
        if not isinstance(node_out, dict):
            continue
        for img in node_out.get("images", []):
            if isinstance(img, dict) and img.get("filename"):
                return img
    return None


# ── Per-prompt generation coroutine ──────────────────────────────────────────

async def _generate_one(
    loop:              asyncio.AbstractEventLoop,
    comfyui_url:       str,
    input_dir:         Path,
    comfyui_output:    Path,
    workflow_template: dict,
    source_path:       Path,
    positive:          str,
    negative:          str,
    steps:             int,
    cfg:               float,
    denoise:           float,
    dest_path:         Path,
    label:             str = "",   # for log messages, e.g. "Ręce pod boki"
) -> None:
    """Generate a single image and save it to dest_path. Raises on failure."""

    ts       = datetime.now().strftime("%Y%m%d%H%M%S%f")
    tmp_name = f"pic_{ts}_{source_path.name}"
    tmp_in   = input_dir / tmp_name
    prefix   = f"pic_out/pic_{ts}"

    # Snapshot existing PNG files in comfyui_output/pic_out (fallback detection)
    pic_out_dir = comfyui_output / "pic_out"
    existing_pngs: set[str] = (
        {p.name for p in pic_out_dir.glob("*.png")} if pic_out_dir.exists() else set()
    )

    try:
        # 1. Copy source → ComfyUI input
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source_path), str(tmp_in))

        # 2. Patch workflow
        wf = _patch_workflow(
            workflow_template, tmp_name,
            positive, negative,
            steps, cfg, denoise, prefix,
        )

        # 3. Submit
        def _submit():
            try:
                return _http_post(f"{comfyui_url}/prompt", {"prompt": wf})
            except OSError as exc:
                if getattr(exc, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        "Windows ComfyUI niedostępny (port 8100). "
                        "Uruchom ComfyUI i spróbuj ponownie."
                    ) from exc
                raise

        resp      = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return prompt_id: {resp}")

        # 4. Poll history (3 s × 400 = 20 min max)
        out_path: Path | None = None

        for _ in range(400):
            await asyncio.sleep(3)

            # ── Primary: history API ───────────────────────────────────
            try:
                def _check(pid=prompt_id):
                    return _http_get(f"{comfyui_url}/history/{pid}")

                history = await loop.run_in_executor(None, _check)
                if prompt_id in history:
                    job     = history[prompt_id]
                    outputs = job.get("outputs", {})
                    img     = _find_image_in_outputs(outputs)
                    if img:
                        subfolder = img.get("subfolder", "")
                        candidate = comfyui_output / subfolder / img["filename"]
                        if candidate.exists():
                            out_path = candidate
                            break
                        # File not yet flushed — try directory fallback immediately

                    status_info = job.get("status", {})
                    if status_info.get("status_str") == "error":
                        msgs = status_info.get("messages", [])
                        err  = next(
                            (m[1].get("exception_message", str(m))
                             for m in msgs if m[0] == "execution_error"),
                            "ComfyUI reported an error",
                        )
                        raise RuntimeError(err)

            except RuntimeError:
                raise
            except Exception:
                pass  # transient network hiccup — try fallback

            # ── Fallback: newest new PNG in pic_out dir ────────────────
            if pic_out_dir.exists():
                new_pngs = [
                    p for p in pic_out_dir.glob("*.png")
                    if p.name not in existing_pngs
                ]
                if new_pngs:
                    out_path = max(new_pngs, key=lambda p: p.stat().st_mtime)
                    break

        if out_path is None:
            raise RuntimeError("Timeout: generowanie nie zakończyło się w ciągu 20 minut")

        # 5. Move output to destination (no temp file left in pic_out)
        # Retry on WinError 32: ComfyUI may still have the file open for writing
        # when the fallback detector picks it up. Wait up to 10 s for it to close.
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        for _attempt in range(10):
            try:
                shutil.move(str(out_path), str(dest_path))
                break
            except OSError as _e:
                if getattr(_e, "winerror", None) == 32 and _attempt < 9:
                    await asyncio.sleep(1)
                else:
                    raise

    finally:
        try:
            if tmp_in.exists():
                tmp_in.unlink()
        except Exception:
            pass


# ── Archive helper ────────────────────────────────────────────────────────────

def archive_result(
    run_id: str, tile_id: str, prompt_id: str, slot_index: int = 0
) -> Path:
    """
    Move the generated file for (slot_index, prompt_id) to the archive/ subfolder.
    Searches for any extension.  Returns the archive path.
    """
    from app.services.pic_session_service import (
        _load as _load_sess,
        _migrate_tile,
        _IMAGE_EXTS as _IE,
    )

    data = _load_sess(run_id)
    tile = next((t for t in data.get("pic_flow", []) if t["id"] == tile_id), None)
    if not tile:
        raise KeyError(f"Tile not found: {tile_id}")

    _migrate_tile(tile)

    output_dir  = Path(tile.get("output_dir", ""))
    image_slots = tile.get("image_slots", [])

    # For character_insert: prompts live in scene_slots[slot_index].prompts
    if tile.get("type") == "character_insert":
        scene_slots = tile.get("scene_slots", [])
        if slot_index < 0 or slot_index >= len(scene_slots):
            raise IndexError(f"Scene slot index {slot_index} out of range")
        all_prompts = scene_slots[slot_index].get("prompts", [])
        prompt_obj  = next((p for p in all_prompts if p["id"] == prompt_id), None)
    else:
        if slot_index < 0 or slot_index >= len(image_slots):
            raise IndexError(f"Slot index {slot_index} out of range")
        slot_prompts = image_slots[slot_index].get("prompts", [])
        prompt_obj   = next((p for p in slot_prompts if p["id"] == prompt_id), None)

    if not prompt_obj:
        raise KeyError(f"Prompt '{prompt_id}' not found in tile '{tile_id}'")

    oid = prompt_obj.get("output_id")
    if not oid:
        raise ValueError(f"Prompt '{prompt_id}' has no output_id")

    src: Path | None = None
    for ext in _IE:
        candidate = output_dir / f"{oid}{ext}"
        if candidate.exists():
            src = candidate
            break

    if src is None:
        raise FileNotFoundError(
            f"Output file not found for prompt '{prompt_id}' in {output_dir}"
        )

    archive_dir = output_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    ts   = datetime.now().strftime("%y%m%d%H%M%S")
    dest = archive_dir / f"{src.stem}_{ts}{src.suffix}"
    shutil.move(str(src), str(dest))
    return dest


def delete_result(
    run_id: str, tile_id: str, prompt_id: str, slot_index: int = 0
) -> bool:
    """
    Delete the generated output file for (slot_index, prompt_id).
    Does NOT remove the prompt from the tile config — only clears the file.
    Returns True if a file was deleted, False if no file existed.
    """
    from app.services.pic_session_service import (
        _load as _load_sess,
        _migrate_tile,
        _IMAGE_EXTS as _IE,
    )

    data = _load_sess(run_id)
    tile = next((t for t in data.get("pic_flow", []) if t["id"] == tile_id), None)
    if not tile:
        raise KeyError(f"Tile not found: {tile_id}")

    _migrate_tile(tile)

    output_dir = Path(tile.get("output_dir", ""))

    if tile.get("type") == "character_insert":
        scene_slots = tile.get("scene_slots", [])
        if slot_index < 0 or slot_index >= len(scene_slots):
            raise IndexError(f"Scene slot index {slot_index} out of range")
        all_prompts = scene_slots[slot_index].get("prompts", [])
    else:
        image_slots = tile.get("image_slots", [])
        if slot_index < 0 or slot_index >= len(image_slots):
            raise IndexError(f"Slot index {slot_index} out of range")
        all_prompts = image_slots[slot_index].get("prompts", [])

    prompt_obj = next((p for p in all_prompts if p["id"] == prompt_id), None)
    if not prompt_obj:
        raise KeyError(f"Prompt '{prompt_id}' not found in tile '{tile_id}'")

    oid = prompt_obj.get("output_id")
    if not oid:
        return False

    deleted = False
    for ext in _IE:
        candidate = output_dir / f"{oid}{ext}"
        if candidate.exists():
            candidate.unlink()
            deleted = True

    return deleted


# ── Archive helper (inline) ───────────────────────────────────────────────────

def _archive_existing(dest: Path) -> None:
    """If dest exists, move it to dest.parent/archive/ before overwriting."""
    if not dest.exists():
        return
    archive_dir = dest.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    ts       = datetime.now().strftime("%y%m%d%H%M%S")
    dst_name = f"{dest.stem}_{ts}{dest.suffix}"
    shutil.move(str(dest), str(archive_dir / dst_name))


# ── Character-insert generation ───────────────────────────────────────────────

def _find_all_load_image_nodes(workflow: dict) -> list[tuple[str, dict]]:
    """Return all LoadImage nodes sorted by node ID."""
    nodes = [
        (nid, node) for nid, node in workflow.items()
        if isinstance(node, dict) and node.get("class_type") == "LoadImage"
    ]
    nodes.sort(key=lambda x: x[0])
    return nodes


def _split_ci_load_image_nodes(
    workflow: dict,
) -> tuple[tuple[str, dict] | None, list[tuple[str, dict]]]:
    """
    For character_insert workflows: split LoadImage nodes into:
      scene_node  — the one whose output[1] (mask) is referenced anywhere in the workflow
      ref_nodes   — all remaining LoadImage nodes, sorted by ID (char ref 1, char ref 2, …)

    If no mask-output reference is found (e.g. simple workflow), falls back to
    treating the first node (by ID) as the scene node.
    """
    # Collect node IDs whose second output [id, 1] is used as a mask input
    mask_source_ids: set[str] = set()
    for node in workflow.values():
        if not isinstance(node, dict):
            continue
        for val in node.get("inputs", {}).values():
            if isinstance(val, list) and len(val) == 2 and val[1] == 1:
                mask_source_ids.add(str(val[0]))

    all_load = _find_all_load_image_nodes(workflow)
    scene_candidates = [(nid, n) for nid, n in all_load if nid in mask_source_ids]
    ref_nodes        = [(nid, n) for nid, n in all_load if nid not in mask_source_ids]

    if scene_candidates:
        return scene_candidates[0], ref_nodes
    # Fallback: no mask wiring — treat first LoadImage as scene
    if all_load:
        return all_load[0], all_load[1:]
    return None, []


def _patch_ci_workflow(
    workflow:         dict,
    scene_filename:   str,
    char_filenames:   list[str],
    positive:         str,
    negative:         str,
    steps:            int,
    cfg:              float,
    denoise:          float,
    filename_prefix:  str,
) -> dict:
    """
    Patch a character_insert workflow:
      • scene_filename  → the LoadImage node whose mask output is wired into the graph
      • char_filenames  → the remaining LoadImage nodes in ID order (char ref 1, 2, …)
      • prompt / params → same as _patch_workflow
    """
    wf = copy.deepcopy(workflow)

    scene_pair, ref_pairs = _split_ci_load_image_nodes(wf)

    if scene_pair:
        scene_pair[1]["inputs"]["image"] = scene_filename

    for i, (nid, node) in enumerate(ref_pairs):
        if i < len(char_filenames):
            node["inputs"]["image"] = char_filenames[i]
            node.pop("mode", None)          # ensure node is active
        elif char_filenames:
            # Safety fallback: more ref slots in JSON than images provided.
            # Repeat the last image rather than leaving a stale hardcoded default.
            node["inputs"]["image"] = char_filenames[-1]
            node.pop("mode", None)

    # KSampler params
    nid, node = _find_node(wf, "KSampler")
    if nid:
        node["inputs"]["seed"]    = random.randint(0, 2 ** 32 - 1)
        node["inputs"]["steps"]   = steps
        node["inputs"]["cfg"]     = cfg
        node["inputs"]["denoise"] = denoise

    # SaveImage prefix
    nid, node = _find_node(wf, "SaveImage")
    if nid:
        node["inputs"]["filename_prefix"] = filename_prefix

    # Positive / Negative via ControlNet references
    _, cn_node = _find_node(wf, "ControlNetInpaintingAliMamaApply")
    if cn_node:
        pos_id = cn_node["inputs"].get("positive", [None])[0]
        neg_id = cn_node["inputs"].get("negative", [None])[0]
        if pos_id and pos_id in wf:
            wf[pos_id]["inputs"]["prompt"] = positive
        if neg_id and neg_id in wf:
            wf[neg_id]["inputs"]["prompt"] = negative or ""
    else:
        for node in wf.values():
            if (isinstance(node, dict) and
                    node.get("class_type") == "TextEncodeQwenImageEditPlus"):
                node["inputs"]["prompt"] = positive

    return wf


# ── Paste Character helpers ───────────────────────────────────────────────────

def _archive_step(source: Path, archive_dir: Path, stem: str) -> None:
    """Copy source to archive_dir/{stem}.png for intermediate step inspection."""
    if not source.exists():
        return
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source), str(archive_dir / f"{stem}.png"))
    except Exception:
        pass  # never break generation over archiving


def _pad_to_ratio(src: "Path", target_w: int, target_h: int) -> "Path | None":
    """
    Pad src image with white margins so its aspect ratio matches target_w:target_h.
    Never crops or scales content — only adds white space.
    Returns a new temp Path if padding was applied, or None if already correct.
    """
    from PIL import Image
    img = Image.open(src).convert("RGB")
    iw, ih = img.size
    target_ratio  = target_w / target_h
    current_ratio = iw / ih

    if abs(current_ratio - target_ratio) < 0.005:
        return None   # already close enough

    if current_ratio < target_ratio:
        # too narrow → pad width
        new_w = max(iw, int(ih * target_ratio))
        new_h = ih
    else:
        # too wide → pad height
        new_w = iw
        new_h = max(ih, int(iw / target_ratio))

    canvas = Image.new("RGB", (new_w, new_h), (255, 255, 255))
    paste_x = (new_w - iw) // 2
    paste_y = (new_h - ih) // 2
    canvas.paste(img, (paste_x, paste_y))

    tmp = src.parent / f"_padded_{src.name}"
    canvas.save(tmp, "PNG")
    _log(f"  ⬜ pad_to_ratio: {iw}×{ih} → {new_w}×{new_h} (target ratio {target_w}:{target_h})")
    return tmp


def _crop_to_subject(path: "Path") -> None:
    """
    After background removal: detect subject via white→alpha + density_bbox,
    crop tightly and save back to the same file.
    Preserves original dimensions if no subject found.
    """
    from PIL import Image, ImageChops  # type: ignore
    img  = Image.open(path)
    orig_mode = img.mode
    rgba = img.convert("RGBA")
    rgba = _white_to_alpha(rgba)
    bbox = _density_bbox(rgba.split()[3])
    if not bbox:
        return
    left, top, right, bottom = bbox
    w, h = rgba.size
    # Skip if bbox is nearly the full image (already tight — nothing to do)
    if left <= 2 and top <= 2 and right >= w - 2 and bottom >= h - 2:
        return
    # Percentage-based safety padding so extreme poses never get clipped.
    # Horizontal: 10% (wide arm/elbow poses), vertical: 2% (hair/feet).
    pad_x = max(15, int(w * 0.10))
    pad_y = max(15, int(h * 0.02))
    left   = max(0, left   - pad_x)
    top    = max(0, top    - pad_y)
    right  = min(w, right  + pad_x)
    bottom = min(h, bottom + pad_y)
    cropped = img.crop((left, top, right, bottom))
    cropped.save(path, "PNG")
    _log(f"  ✂️ crop_to_subject: {w}×{h} → {right-left}×{bottom-top}px (pad {pad_x}×{pad_y}px / 2%)")


def _density_bbox(
    alpha: "Image.Image",
    alpha_threshold: int = 30,
    min_px_ratio: float = 0.03,
) -> tuple | None:
    """
    Bounding box that handles artifact pixels at image edges via gap detection.

    Algorithm for top (same logic mirrored for bottom):
    - Scan rows from top.
    - Track the first row meeting density threshold (candidate top).
    - If a completely-zero row appears AFTER the candidate, those first rows
      were edge artifacts — reset the candidate and keep scanning.
    - The candidate survives only if it is never followed by a zero-row gap,
      meaning it is part of a continuous figure (fingers, hair, etc.).

    This distinguishes:
      artifacts : [24, 26, 23, 16, 12,  0,  0,  0] → gap → skip artifacts
      real top  : [ 0,  0, 13, 23, 30, 36, 41, 57] → no gap → keep from row 4
      fingertips: [ 0,  5, 15, 30, 80, 90, 70, 50] → continuous → keep from row 3
    """
    W, H = alpha.size
    data  = list(alpha.getdata())          # flat list, length W*H

    min_row = max(1, int(W * min_px_ratio))  # e.g. ≥3% of width
    min_col = max(1, int(H * min_px_ratio))  # e.g. ≥3% of height

    def row_count(y: int) -> int:
        base = y * W
        return sum(1 for v in data[base:base + W] if v > alpha_threshold)

    def col_count(x: int, y0: int, y1: int) -> int:
        return sum(1 for y in range(y0, y1) if data[y * W + x] > alpha_threshold)

    # ── top (two-stage) ───────────────────────────────────────────────────────
    # Stage 1 — gap-aware dense top: finds the first DENSE row (>= min_row px)
    # after any leading artifact block (artifacts → zero-gap → figure).
    # This correctly skips stray artifact pixels at the image top edge.
    top_candidate  = None
    gap_after_cand = False
    dense_top = None
    for y in range(H):
        cnt = row_count(y)
        if cnt >= min_row:
            if gap_after_cand:
                dense_top = y
                break
            if top_candidate is None:
                top_candidate = y
        elif cnt == 0 and top_candidate is not None:
            gap_after_cand = True
    if dense_top is None:
        dense_top = top_candidate
    if dense_top is None:
        return None

    # Stage 2 — extend upward through sparse pixels (hair tips, fingertips):
    # Scan upward from dense_top and include any row that has at least one pixel,
    # stopping at the first completely-zero row. This captures sparse hair/finger
    # tips above the dense region without crossing the artifact-separating gap.
    top = dense_top
    for y in range(dense_top - 1, -1, -1):
        if row_count(y) > 0:
            top = y
        else:
            break  # zero row = artifact gap boundary — stop here

    # ── bottom (simple — no gap detection) ───────────────────────────────────
    # Gap detection is intentionally NOT used for the bottom edge.
    # Feet and toes have natural white gaps between them (floor between feet,
    # gaps between toes) which would fool gap detection into cutting them off.
    # Bottom artefacts are rare and less harmful than clipping toes.
    # Strategy: last row that has ANY pixel above alpha_threshold (no min_row
    # requirement — even a single toe-tip pixel counts).
    bottom = None
    for y in range(H - 1, top - 1, -1):
        if row_count(y) > 0:
            bottom = y + 1
            break

    if bottom is None:
        bottom = top + 1

    # ── left / right ──────────────────────────────────────────────────────────
    left = None
    for x in range(W):
        if col_count(x, top, bottom) >= min_col:
            left = x
            break
    if left is None:
        return None

    right = left + 1
    for x in range(W - 1, left, -1):
        if col_count(x, top, bottom) >= min_col:
            right = x + 1
            break

    return (left, top, right, bottom)


def _make_edge_mask(
    model_path: "Path",
    scene_w: int, scene_h: int,
    paste_x: int, paste_y: int, paste_w: int, paste_h: int,
    edge_px: int,
) -> "Image.Image":
    """
    Create an inpainting mask covering the pasted character's footprint + edge_px border.
    Uses the original (pre-feather) model image so white areas inside the character
    are not accidentally excluded from the mask.
    Returns an "L" image (scene size): white = inpaint, black = keep.
    """
    from PIL import Image, ImageFilter  # type: ignore
    model = Image.open(model_path).convert("RGBA")
    model = _white_to_alpha(model)
    bbox  = model.getbbox()
    if bbox:
        model = model.crop(bbox)
    model_s   = model.resize((paste_w, paste_h), Image.LANCZOS)
    _, _, _, a = model_s.split()
    a = a.point(lambda v: 255 if v > 30 else 0)      # binarize
    for _ in range(edge_px):                          # dilate
        a = a.filter(ImageFilter.MaxFilter(3))
    scene_mask = Image.new("L", (scene_w, scene_h), 0)
    scene_mask.paste(a, (paste_x, paste_y))
    return scene_mask


async def _generate_ci_one(
    loop:              "asyncio.AbstractEventLoop",
    comfyui_url:       str,
    input_dir:         "Path",
    comfyui_output:    "Path",
    workflow_template: dict,
    scene_path:        "Path",   # RGBA PNG: alpha = inpainting mask
    char_path:         "Path",   # character reference image
    positive:          str,
    negative:          str,
    steps:             int,
    cfg:               float,
    denoise:           float,
    dest_path:         "Path",
    label:             str = "",
) -> None:
    """
    Generate using a ci_1ref workflow: scene (RGBA with mask) + 1 character reference.
    Mirrors _generate_one() but copies 2 inputs and uses _patch_ci_workflow().
    """
    ts             = datetime.now().strftime("%Y%m%d%H%M%S%f")
    scene_tmp_name = f"pic_{ts}_0_{scene_path.name}"
    char_tmp_name  = f"pic_{ts}_1_{char_path.name}"
    scene_tmp_in   = input_dir / scene_tmp_name
    char_tmp_in    = input_dir / char_tmp_name
    prefix         = f"pic_out/pic_{ts}"

    pic_out_dir = comfyui_output / "pic_out"
    existing_pngs: set[str] = (
        {p.name for p in pic_out_dir.glob("*.png")} if pic_out_dir.exists() else set()
    )

    try:
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(scene_path), str(scene_tmp_in))
        shutil.copy2(str(char_path),  str(char_tmp_in))

        wf = _patch_ci_workflow(
            workflow_template,
            scene_filename=scene_tmp_name,
            char_filenames=[char_tmp_name],
            positive=positive,
            negative=negative,
            steps=steps, cfg=cfg, denoise=denoise,
            filename_prefix=prefix,
        )

        def _submit():
            try:
                return _http_post(f"{comfyui_url}/prompt", {"prompt": wf})
            except OSError as exc:
                if getattr(exc, "errno", None) in (10061, 111):
                    raise RuntimeError("ComfyUI niedostępny") from exc
                raise

        resp      = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return prompt_id: {resp}")

        out_path: Path | None = None
        for _ in range(400):
            await asyncio.sleep(3)
            try:
                def _check(pid=prompt_id):
                    return _http_get(f"{comfyui_url}/history/{pid}")
                history  = await loop.run_in_executor(None, _check)
                if prompt_id in history:
                    job     = history[prompt_id]
                    outputs = job.get("outputs", {})
                    img     = _find_image_in_outputs(outputs)
                    if img:
                        subfolder = img.get("subfolder", "")
                        candidate = comfyui_output / subfolder / img["filename"]
                        if candidate.exists():
                            out_path = candidate
                            break
                    if job.get("status", {}).get("status_str") == "error":
                        msgs = job["status"].get("messages", [])
                        err  = next(
                            (m[1].get("exception_message", str(m))
                             for m in msgs if m[0] == "execution_error"),
                            "ComfyUI error",
                        )
                        raise RuntimeError(err)
            except RuntimeError:
                raise
            except Exception:
                pass
            if pic_out_dir.exists():
                new_pngs = [p for p in pic_out_dir.glob("*.png") if p.name not in existing_pngs]
                if new_pngs:
                    out_path = max(new_pngs, key=lambda p: p.stat().st_mtime)
                    break

        if out_path is None:
            raise RuntimeError("Timeout: generowanie nie zakończyło się w 20 min")

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        for _attempt in range(10):
            try:
                shutil.move(str(out_path), str(dest_path))
                break
            except OSError as _e:
                if getattr(_e, "winerror", None) == 32 and _attempt < 9:
                    await asyncio.sleep(1)
                else:
                    raise

    finally:
        for tmp in (scene_tmp_in, char_tmp_in):
            try:
                if tmp.exists():
                    tmp.unlink()
            except Exception:
                pass


# ── Paste Character — PIL composite + optional two-pass ComfyUI blend ─────────

def _white_to_alpha(img: "Image.Image", threshold: int = 220) -> "Image.Image":
    """Convert near-white / light-gray pixels to transparent.

    Uses min(R, G, B) >= threshold so ALL three channels must be bright.
    Default threshold=220 catches JPEG-artifact whites (compression shifts values
    to ~220-254) while keeping warm skin tones opaque (blue channel < 220).
    The old threshold=240 missed JPEG-compressed backgrounds.
    """
    from PIL import Image, ImageChops  # type: ignore
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    # min(R,G,B) per pixel — correctly requires ALL channels to be bright
    min_rg  = ImageChops.darker(r, g)
    min_rgb = ImageChops.darker(min_rg, b)
    # pixel is background if min >= threshold → set alpha to 0 (transparent)
    bg_alpha = min_rgb.point(lambda v: 0 if v >= threshold else 255)
    # combine: keep the more transparent of existing alpha vs background mask
    new_alpha = ImageChops.darker(a, bg_alpha)
    return Image.merge("RGBA", (r, g, b, new_alpha))


def _feather_alpha(img: "Image.Image", erode_px: int = 3, blur_px: int = 2) -> "Image.Image":
    """
    Erode + feather the alpha channel to remove white fringing on composited characters.
    - erode_px: shrinks the opaque area by N pixels (removes fringe)
    - blur_px:  Gaussian blur radius for soft edges
    """
    from PIL import Image, ImageFilter  # type: ignore
    r, g, b, a = img.split()
    # Erode: MinFilter shrinks bright (opaque) regions — removes white-fringe pixels
    for _ in range(erode_px):
        a = a.filter(ImageFilter.MinFilter(3))
    # Feather: blur the alpha for smooth, natural-looking edges
    if blur_px > 0:
        a = a.filter(ImageFilter.GaussianBlur(radius=blur_px))
    return Image.merge("RGBA", (r, g, b, a))


async def _run_paste_character_async(
    run_id:     str,
    tile_id:    str,
    tile:       dict,
    output_dir: "Path",
    force_all:  bool,
    slot_index: int | None = None,
) -> None:
    """
    Deterministic character paste using PIL — zero ComfyUI required.
    For each paste_slot:
      1. Load scene + model images
      2. Convert white background → transparent
      3. Scale model to fit [top_pct% … bottom_pct%] of scene height
      4. Paste at x_center_pct% horizontal position
      5. Save result to output_dir/{output_id}.png
    """
    from PIL import Image, ImageFilter  # type: ignore

    tile_name = tile.get("name", tile_id)
    _log(f"📌 Paste Character: [{tile_name}] start")

    paste_slots = tile.get("paste_slots", [])
    if not paste_slots:
        _set_job(run_id, tile_id, {
            "status": "done", "tile_id": tile_id, "tile_name": tile_name,
            "total": 0, "done": 0, "skipped": 0, "current_prompt": None, "errors": [],
        })
        _log(f"⚠ Paste Character: [{tile_name}] brak slotów")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Two-pass blend config ─────────────────────────────────────────────────
    # Pass 1 — Edge Blend: inpainting within dilated character mask (ci_1ref wf)
    eb_enabled  = bool(tile.get("edge_blend_enabled", False))
    eb_px       = int(tile.get("edge_blend_px", 15))
    _eb_prm     = next((p for p in tile.get("edge_blend_prompts", []) if p.get("enabled", True)), None)
    eb_positive = (_eb_prm.get("positive", "") if _eb_prm else "").strip()
    eb_negative = (_eb_prm.get("negative", "") if _eb_prm else "")
    _eb_p       = (_eb_prm.get("params", {}) if _eb_prm else {})
    eb_steps    = int(_eb_p.get("steps", 30))
    eb_cfg      = float(tile["edge_blend_cfg"])    if tile.get("edge_blend_cfg")    is not None else float(_eb_p.get("cfg",    8.0))
    eb_denoise  = float(tile["edge_blend_denoise"]) if tile.get("edge_blend_denoise") is not None else float(_eb_p.get("denoise", 0.6))
    eb_wf       = None; eb_url = None; eb_in_dir = None; eb_out_dir = None

    # Pass 2 — Scene Blend: full-image i2i for shadows / scene coherence
    sb_enabled  = bool(tile.get("scene_blend_enabled", False))
    _sb_prm     = next((p for p in tile.get("scene_blend_prompts", []) if p.get("enabled", True)), None)
    sb_positive = (_sb_prm.get("positive", "") if _sb_prm else "").strip()
    sb_negative = (_sb_prm.get("negative", "") if _sb_prm else "")
    _sb_p       = (_sb_prm.get("params", {}) if _sb_prm else {})
    sb_steps    = int(_sb_p.get("steps", 30))
    sb_cfg      = float(tile["scene_blend_cfg"])    if tile.get("scene_blend_cfg")    is not None else float(_sb_p.get("cfg",    8.0))
    sb_denoise  = float(tile["scene_blend_denoise"]) if tile.get("scene_blend_denoise") is not None else float(_sb_p.get("denoise", 0.4))
    sb_wf       = None; sb_url = None; sb_in_dir = None; sb_out_dir = None

    if eb_enabled and eb_positive:
        win        = app_config_service.get_backend("windows")
        eb_url     = win.get("api_url")    or settings.comfyui_upscale_url
        eb_in_dir  = Path(win.get("input_dir")  or settings.comfyui_upscale_input_dir)
        eb_out_dir = Path(win.get("output_dir") or settings.comfyui_upscale_output_dir)
        wf_str = win.get("models", {}).get("ci_1ref", {}).get("workflow_json", "")
        if wf_str:
            wf_p = Path(wf_str)
            if wf_p.exists():
                eb_wf = json.loads(wf_p.read_text(encoding="utf-8"))
                _log(f"  📋 Edge Blend workflow: {wf_p.name}")
            else:
                _log(f"  ⚠ Edge Blend workflow nie istnieje: {wf_p} — pass 1 wyłączony")
        else:
            _log("  ⚠ Edge Blend: brak ścieżki ci_1ref w app_config — pass 1 wyłączony")

    if sb_enabled and sb_positive:
        win        = app_config_service.get_backend("windows")
        sb_url     = win.get("api_url")    or settings.comfyui_upscale_url
        sb_in_dir  = Path(win.get("input_dir")  or settings.comfyui_upscale_input_dir)
        sb_out_dir = Path(win.get("output_dir") or settings.comfyui_upscale_output_dir)
        wf_str = win.get("models", {}).get("i2i", {}).get("workflow_json", "")
        if wf_str:
            wf_p = Path(wf_str)
            if wf_p.exists():
                sb_wf = json.loads(wf_p.read_text(encoding="utf-8"))
                _log(f"  📋 Scene Blend workflow: {wf_p.name}")
            else:
                _log(f"  ⚠ Scene Blend workflow nie istnieje: {wf_p} — pass 2 wyłączony")
        else:
            _log("  ⚠ Scene Blend: brak ścieżki i2i w app_config — pass 2 wyłączony")

    # Select slots
    if slot_index is not None:
        slots_to_run = [(slot_index, paste_slots[slot_index])] if 0 <= slot_index < len(paste_slots) else []
    else:
        slots_to_run = list(enumerate(paste_slots))

    skipped = len(paste_slots) - len(slots_to_run)
    _set_job(run_id, tile_id, {
        "status": "running", "tile_id": tile_id, "tile_name": tile_name,
        "total": len(slots_to_run), "done": 0, "skipped": skipped,
        "current_prompt": None, "errors": [], "started_at": time.time(),
    })

    done   = 0
    errors: list[dict] = []

    for idx, (si, slot) in enumerate(slots_to_run, 1):
        output_id = slot.get("output_id", slot.get("id", f"slot_{si}"))
        label     = f"Slot {si + 1}"
        _update_job(run_id, tile_id, current_prompt=label)

        out_path = output_dir / f"{output_id}.png"
        if not force_all and out_path.exists():
            _log(f"  ⏭ [{idx}/{len(slots_to_run)}] {label} — już istnieje, pomijam")
            done += 1
            _update_job(run_id, tile_id, done=done)
            continue

        scene_path  = Path(slot.get("scene_image", ""))
        characters  = slot.get("characters", [])

        if not scene_path.exists():
            err = f"Scena nie istnieje: {scene_path}"
            _log(f"  ❌ [{idx}] {err}")
            errors.append({"slot": si, "error": err})
            continue
        if not characters:
            err = "Slot nie ma żadnych postaci"
            _log(f"  ❌ [{idx}] {err}")
            errors.append({"slot": si, "error": err})
            continue

        try:
            archive_dir = output_dir / "archive"
            loop        = asyncio.get_running_loop()
            oid         = output_id

            # Start with the original scene; composite each character in sequence
            scene = Image.open(scene_path).convert("RGBA")
            W, H  = scene.size

            # Save initial scene so out_path is always a valid file from the start
            scene.convert("RGB").save(out_path, "PNG")

            for ci, char in enumerate(characters):
                model_path   = Path(char.get("model_image", ""))
                top_pct      = float(char.get("top_pct",      10)) / 100.0
                bottom_pct   = float(char.get("bottom_pct",   85)) / 100.0
                x_center_pct = float(char.get("x_center_pct", 50)) / 100.0
                erode_px     = int(char.get("erode_px", 3))
                blur_px      = int(char.get("blur_px",  2))
                char_label   = f"{label} char{ci+1}/{len(characters)}"

                if not model_path.exists():
                    _log(f"  ⚠ [{idx}] {char_label}: model nie istnieje: {model_path} — pomijam")
                    continue
                if bottom_pct <= top_pct:
                    _log(f"  ⚠ [{idx}] {char_label}: bottom_pct <= top_pct — pomijam")
                    continue

                # ── PIL composite ─────────────────────────────────────────
                # Re-open current state (may have been updated by edge blend)
                scene = Image.open(out_path).convert("RGBA")

                # Normalize: edge blend (ComfyUI) may output a different resolution
                if scene.size != (W, H):
                    _log(f"  ℹ [{idx}] {char_label}: normalizacja sceny {scene.size} → ({W}×{H})")
                    scene = scene.resize((W, H), Image.LANCZOS)

                _raw   = Image.open(model_path)
                _has_alpha = _raw.mode in ("RGBA", "LA", "PA")
                model  = _raw.convert("RGBA")
                _orig_size = model.size
                if not _has_alpha:
                    # no built-in alpha → white background → convert white→transparent
                    model = _white_to_alpha(model)
                # else: trust the existing alpha channel (BG-removal PNG)

                # Smart bbox: ignore rows/columns that have fewer than min_px
                # non-transparent pixels — filters out sparse artifact pixels at
                # image edges without eroding the figure itself.
                # Percentage-based safety padding (2% of each dimension) so hair
                # tips and toe pixels are never clipped before scaling.
                bbox  = _density_bbox(model.split()[3])
                if bbox:
                    _mw, _mh = model.size
                    _pad_x = max(15, int(_mw * 0.10))
                    _pad_y = max(15, int(_mh * 0.02))
                    _bl, _bt, _br, _bb = bbox
                    _bl = max(0,   _bl - _pad_x)
                    _bt = max(0,   _bt - _pad_y)
                    _br = min(_mw, _br + _pad_x)
                    _bb = min(_mh, _bb + _pad_y)
                    model = model.crop((_bl, _bt, _br, _bb))
                _log(f"  🔍 [{idx}] {char_label}: model {'RGBA' if _has_alpha else 'RGB→α'} "
                     f"{_orig_size[0]}×{_orig_size[1]} → bbox+pad {model.width}×{model.height}")
                if erode_px > 0 or blur_px > 0:
                    model = _feather_alpha(model, erode_px=erode_px, blur_px=blur_px)

                target_h = max(1, int((bottom_pct - top_pct) * H))
                target_w = max(1, int(model.width * (target_h / model.height)))
                model_s  = model.resize((target_w, target_h), Image.LANCZOS)

                x = int(x_center_pct * W) - target_w // 2
                y = int(top_pct * H)
                x = max(0, min(x, W - target_w))
                y = max(0, min(y, H - target_h))

                _log(f"  📐 [{idx}] {char_label}: top={top_pct*100:.0f}% bot={bottom_pct*100:.0f}% x={x_center_pct*100:.0f}%"
                     f" → model {target_w}×{target_h}px at ({x},{y}) na {W}×{H}")

                scene.paste(model_s, (x, y), model_s)
                scene.convert("RGB").save(out_path, "PNG")
                _archive_step(out_path, archive_dir, f"{oid}_char{ci}_step0_pil")
                _log(f"  🖼 [{idx}] {char_label}: PIL composite → {out_path.name}")

                # ── Edge Blend per character ──────────────────────────────
                if eb_enabled and eb_positive and eb_wf:
                    _log(f"  ✂️ [{idx}] {char_label} — edge blend "
                         f"(maska {eb_px}px  steps={eb_steps}  cfg={eb_cfg}  denoise={eb_denoise}) …")
                    edge_mask  = _make_edge_mask(
                        model_path, W, H, x, y, target_w, target_h, eb_px,
                    )
                    scene_rgba = Image.open(out_path).convert("RGBA")
                    scene_rgba.putalpha(edge_mask)

                    ts       = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    rgba_tmp = output_dir / f"_tmp_rgba_{ts}.png"
                    scene_rgba.save(rgba_tmp, "PNG")
                    try:
                        await _generate_ci_one(
                            loop, eb_url, eb_in_dir, eb_out_dir,
                            eb_wf, rgba_tmp, model_path,
                            eb_positive, eb_negative,
                            eb_steps, eb_cfg, eb_denoise,
                            out_path,
                            label=f"edge_blend {char_label}",
                        )
                    finally:
                        try:
                            rgba_tmp.unlink(missing_ok=True)
                        except Exception:
                            pass
                    _archive_step(out_path, archive_dir, f"{oid}_char{ci}_step1_edge")

            # ── Scene Blend once — after ALL characters composited ────────
            if sb_enabled and sb_positive and sb_wf:
                _log(f"  🎨 [{idx}/{len(slots_to_run)}] {label} — scene blend "
                     f"(steps={sb_steps}  cfg={sb_cfg}  denoise={sb_denoise}) …")
                await _generate_one(
                    loop, sb_url, sb_in_dir, sb_out_dir,
                    sb_wf, out_path,
                    sb_positive, sb_negative,
                    sb_steps, sb_cfg, sb_denoise,
                    out_path,
                    label=f"scene_blend {label}",
                )
                _archive_step(out_path, archive_dir, f"{oid}_step_scene")

            _log(f"  ✅ [{idx}/{len(slots_to_run)}] {label} → {out_path}")
            done += 1
            _update_job(run_id, tile_id, done=done)

        except Exception as exc:
            err = str(exc)
            _log(f"  ❌ [{idx}] {label}: {err}")
            errors.append({"slot": si, "error": err})

    final = "error" if (errors and done == 0) else "done"
    _update_job(run_id, tile_id, status=final, done=done, current_prompt=None, errors=errors)
    summary = f"✅ Paste Character: [{tile_name}] zakończono {done}/{len(slots_to_run)}"
    if errors:
        summary += f" ({len(errors)} błędów)"
    _log(summary)


async def _run_character_insert_async(
    run_id:       str,
    tile_id:      str,
    tile:         dict,
    output_dir:   "Path",
    global_suffix: str,
    force_all:    bool,
    prompt_id:    str | None = None,
    slot_index:   int | None = None,
    loop:         "asyncio.AbstractEventLoop | None" = None,
) -> None:
    """
    Generation pipeline for character_insert tiles.
    Scene + character references → one output image per prompt.
    LoadImage node order in workflow: [0]=scene, [1]=char1, [2]=char2 (optional).
    """
    from app.services.pic_session_service import _get_dirs_field

    tile_name    = tile.get("name", tile_id)
    scene_dirs   = [Path(d) for d in _get_dirs_field(tile, "scene_dirs",      "scene_dir")      if d]
    chars_dirs   = [Path(d) for d in _get_dirs_field(tile, "characters_dirs", "characters_dir") if d]
    scene_slots  = tile.get("scene_slots", [])

    def _find_in_dirs(name: str, dirs: list[Path]) -> Path | None:
        for d in dirs:
            p = d / name
            if p.exists():
                return p
        return None

    # Build full work queue: (scene_path, char_paths, prompt, dest, slot_idx, label)
    to_run: list[tuple] = []
    total_prompts = 0
    for slot_idx, slot in enumerate(scene_slots):
        if slot_index is not None and slot_idx != slot_index:
            continue
        scene_image = slot.get("scene_image", "")
        char_images = slot.get("character_images", [])
        prompts     = [p for p in slot.get("prompts", [])
                       if p.get("enabled", True) and (prompt_id is None or p["id"] == prompt_id)]
        total_prompts += len(prompts)

        if not scene_image:
            _log(f"  ⚠ Slot {slot_idx}: brak wybranej sceny — pomijam slot")
            continue

        scene_path = _find_in_dirs(scene_image, scene_dirs)
        if not scene_path:
            _log(f"  ⚠ Slot {slot_idx}: scena nie istnieje w żadnym katalogu: {scene_image}")
            continue

        char_paths = []
        for cname in char_images:
            cp = _find_in_dirs(cname, chars_dirs)
            if cp:
                char_paths.append(cp)
            else:
                _log(f"  ⚠ Slot {slot_idx}: postać nie znaleziona, pomijam: {cname}")

        # Per-slot workflow key based on how many character refs this slot has.
        n_chars = len(char_paths)
        wf_key  = "ci_2ref" if n_chars >= 2 else ("ci_1ref" if n_chars == 1 else "i2i")

        for p in prompts:
            oid = p.get("output_id")
            if not oid:
                _log(f"  ⚠ Slot {slot_idx} / Prompt {p['id']} nie ma output_id — pomijam")
                continue
            dest = output_dir / f"{oid}.png"
            if force_all or not dest.exists():
                to_run.append((scene_path, char_paths, p, dest, slot_idx,
                               f"{scene_image} × {p.get('name', p['id'])}", wf_key))

    skipped = total_prompts - len(to_run)
    if not to_run:
        _set_job(run_id, tile_id, {
            "status": "done", "tile_id": tile_id,
            "total": 0, "done": 0, "skipped": skipped,
            "current_prompt": None, "errors": [],
        })
        _log(f"🖼 Pic Studio CI: [{tile_name}] wszystko gotowe ({skipped} pom.)")
        return

    win         = app_config_service.get_backend("windows")
    comfyui_url = win.get("api_url")    or settings.comfyui_upscale_url
    input_dir   = Path(win.get("input_dir")  or settings.comfyui_upscale_input_dir)
    comfyui_out = Path(win.get("output_dir") or settings.comfyui_upscale_output_dir)
    models      = win.get("models", {})

    # Workflow templates loaded lazily per-slot (ci / ci_1ref / i2i).
    # Each item in to_run carries its own wf_key; templates are cached so the
    # same JSON is never read from disk more than once per tile run.
    wf_cache: dict[str, dict] = {}

    def _load_wf(key: str) -> dict | None:
        if key in wf_cache:
            return wf_cache[key]
        wf_str = models.get(key, {}).get("workflow_json", "")
        if not wf_str:
            return None
        wf_p = Path(wf_str)
        if not wf_p.exists():
            _log(f"  ⚠ Workflow '{key}' nie istnieje: {wf_p}")
            return None
        tmpl = json.loads(wf_p.read_text(encoding="utf-8"))
        wf_cache[key] = tmpl
        _log(f"  📋 Workflow załadowany: {wf_p.name} (key={key})")
        return tmpl

    _set_job(run_id, tile_id, {
        "status": "running", "tile_id": tile_id, "tile_name": tile_name,
        "total": len(to_run), "done": 0, "skipped": skipped,
        "current_prompt": None, "errors": [], "started_at": time.time(),
    })
    _log(f"🖼 Pic Studio CI: [{tile_name}] start — {len(to_run)} promptów"
         + (f" ({skipped} pom.)" if skipped else ""))

    loop   = loop or asyncio.get_running_loop()
    errors: list[dict] = []
    done   = 0

    for idx, (scene_path, char_paths, p, dest, slot_idx, label, wf_key) in enumerate(to_run, 1):
        pname = p.get("name", p["id"])
        _update_job(run_id, tile_id, current_prompt=label)
        _log(f"  ⚙ [{idx}/{len(to_run)}] {label} …")
        _archive_existing(dest)   # archive previous result before overwriting

        # Select workflow template for this slot (with fallback chain)
        _wf_fallbacks = {
            "ci_2ref": ["ci_2ref", "ci_1ref", "i2i"],
            "ci_1ref": ["ci_1ref", "i2i"],
            "i2i":     ["i2i"],
        }
        workflow_template = None
        resolved_key      = None
        for fb_key in _wf_fallbacks.get(wf_key, [wf_key]):
            workflow_template = _load_wf(fb_key)
            if workflow_template is not None:
                resolved_key = fb_key
                break
        if workflow_template is None or resolved_key is None:
            raise RuntimeError(
                f"Brak workflow dla klucza '{wf_key}'. "
                "Sprawdź app_config.yaml → backends.windows.models."
            )
        if resolved_key != wf_key:
            _log(f"  ⚠ [{idx}] Workflow '{wf_key}' niedostępny — fallback → '{resolved_key}'")
        _wf_json_path = models.get(resolved_key, {}).get("workflow_json", "?")
        _log(f"  🔧 [{idx}] Model: {resolved_key}  |  {Path(_wf_json_path).name}")

        pos = p.get("positive", "")
        if global_suffix:
            pos = f"{pos}, {global_suffix}" if pos else global_suffix
        params  = p.get("params", {})
        steps   = int(params.get("steps",   30))
        cfg     = float(params.get("cfg",    8.0))
        denoise = float(params.get("denoise", 1.0))
        _log(f"  📝 [{idx}] steps={steps}  cfg={cfg}  denoise={denoise}  "
             f"prompt: {pos[:100]}{'…' if len(pos) > 100 else ''}")

        try:
            # Copy all images into ComfyUI input dir with unique temp names
            ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
            all_sources = [scene_path] + char_paths
            tmp_names   = []
            tmp_ins     = []
            for i, src in enumerate(all_sources):
                tname = f"pic_{ts}_{i}_{src.name}"
                tin   = input_dir / tname
                input_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(tin))
                tmp_names.append(tname)
                tmp_ins.append(tin)

            prefix = f"pic_out/pic_{ts}"

            # Snapshot existing pic_out PNGs for fallback detection
            pic_out_dir = comfyui_out / "pic_out"
            existing_pngs: set[str] = (
                {p.name for p in pic_out_dir.glob("*.png")} if pic_out_dir.exists() else set()
            )

            # Patch workflow: scene → mask-wired LoadImage node,
            # char refs → remaining LoadImage nodes in ID order
            wf = _patch_ci_workflow(
                workflow_template,
                scene_filename=tmp_names[0],
                char_filenames=tmp_names[1:],
                positive=pos,
                negative=p.get("negative", ""),
                steps=steps, cfg=cfg, denoise=denoise,
                filename_prefix=prefix,
            )

            # Submit to ComfyUI
            def _submit(wf=wf):
                try:
                    return _http_post(f"{comfyui_url}/prompt", {"prompt": wf})
                except OSError as exc:
                    if getattr(exc, "errno", None) in (10061, 111):
                        raise RuntimeError("ComfyUI niedostepny") from exc
                    raise

            resp      = await loop.run_in_executor(None, _submit)
            prompt_id = resp.get("prompt_id")
            if not prompt_id:
                raise RuntimeError(f"Brak prompt_id: {resp}")

            # Poll history
            out_path: Path | None = None
            for _ in range(400):
                await asyncio.sleep(3)
                try:
                    def _check(pid=prompt_id):
                        return _http_get(f"{comfyui_url}/history/{pid}")
                    history = await loop.run_in_executor(None, _check)
                    if prompt_id in history:
                        job     = history[prompt_id]
                        outputs = job.get("outputs", {})
                        img     = _find_image_in_outputs(outputs)
                        if img:
                            subfolder = img.get("subfolder", "")
                            candidate = comfyui_out / subfolder / img["filename"]
                            if candidate.exists():
                                out_path = candidate
                                break
                        if job.get("status", {}).get("status_str") == "error":
                            msgs = job["status"].get("messages", [])
                            err  = next(
                                (m[1].get("exception_message", str(m)) for m in msgs if m[0] == "execution_error"),
                                "ComfyUI error",
                            )
                            raise RuntimeError(err)
                except RuntimeError:
                    raise
                except Exception:
                    pass
                if pic_out_dir.exists():
                    new_pngs = [p for p in pic_out_dir.glob("*.png") if p.name not in existing_pngs]
                    if new_pngs:
                        out_path = max(new_pngs, key=lambda p: p.stat().st_mtime)
                        break

            if out_path is None:
                raise RuntimeError("Timeout: generowanie nie zakończyło się w 20 min")

            dest.parent.mkdir(parents=True, exist_ok=True)
            for _attempt in range(10):
                try:
                    shutil.move(str(out_path), str(dest))
                    break
                except OSError as _e:
                    if getattr(_e, "winerror", None) == 32 and _attempt < 9:
                        await asyncio.sleep(1)
                    else:
                        raise

            done += 1
            _update_job(run_id, tile_id, done=done)
            _log(f"  ✅ [{idx}/{len(to_run)}] {pname} → {dest.name}")

        except Exception as exc:
            errors.append({"prompt_id": p["id"], "prompt_name": label, "slot_idx": slot_idx, "error": str(exc)})
            _update_job(run_id, tile_id, errors=list(errors))
            _log(f"  ❌ [{idx}/{len(to_run)}] {label}: {exc}")
        finally:
            for tin in tmp_ins:
                try:
                    if tin.exists(): tin.unlink()
                except Exception:
                    pass

    final = "error" if (errors and done == 0) else "done"
    _update_job(run_id, tile_id, status=final, done=done, current_prompt=None, errors=errors)
    summary = f"✅ Pic Studio CI: [{tile_name}] zakończono {done}/{len(to_run)}"
    if errors: summary += f" ({len(errors)} błędów)"
    _log(summary)


# ── Main generation runner ────────────────────────────────────────────────────

async def _run_tile_async(
    run_id:     str,
    tile_id:    str,
    force_all:  bool,
    slot_index: int | None = None,   # None = all slots
    prompt_id:  str | None = None,   # None = all prompts; str = single prompt
) -> None:
    """
    Full generation pipeline for one tile.
    Iterates image_slots (or a single slot if slot_index is given).
    File naming: {tile_slug}__{image_stem}__{prompt_id}.png
    Updates _jobs throughout.
    """
    try:
        from app.services.pic_session_service import (
            _load as _load_sess,
            _save as _save_sess,
            _migrate_tile,
            _slugify,
            _get_source_dirs,
            _ensure_output_ids,
        )

        data = _load_sess(run_id)
        tile = next(
            (t for t in data.get("pic_flow", []) if t["id"] == tile_id), None
        )
        if not tile:
            raise ValueError(f"Tile not found: {tile_id}")

        _migrate_tile(tile)

        # Guard: fix duplicate/missing output_ids before building the work queue.
        # This catches tiles that were saved before the dedup fix was deployed so that
        # generation never writes two different source images to the same output file.
        if _ensure_output_ids(tile):
            data["pic_flow"] = [
                tile if t["id"] == tile_id else t
                for t in data.get("pic_flow", [])
            ]
            _save_sess(run_id, data)
            _log(f"  ℹ [{tile.get('name', tile_id)}] naprawiono zduplikowane output_id przed generowaniem")

        tile_type     = tile.get("type", "one_image_many_prompts")
        output_dir    = Path(tile.get("output_dir", ""))
        global_suffix = tile.get("global_suffix", "")

        # ── Route to paste_character pipeline (PIL, no ComfyUI) ──────────────
        if tile_type == "paste_character":
            await _run_paste_character_async(
                run_id, tile_id, tile, output_dir, force_all, slot_index,
            )
            return

        # ── Route to character_insert pipeline ────────────────────────────────
        if tile_type == "character_insert":
            await _run_character_insert_async(
                run_id, tile_id, tile, output_dir, global_suffix, force_all, prompt_id, slot_index,
            )
            return

        source_dirs        = [Path(d) for d in _get_source_dirs(tile)]
        image_slots        = tile.get("image_slots", [])
        pad_input_to_ratio = tile.get("pad_input_to_ratio", False)
        _res               = data.get("resolution", [1024, 1024])
        target_w, target_h = int(_res[0]), int(_res[1])

        if not source_dirs:
            raise ValueError("Kafelek nie ma skonfigurowanego katalogu źródłowego.")
        if not image_slots:
            raise ValueError("Kafelek nie ma żadnych obrazków źródłowych.")

        # Select which slots to process
        if slot_index is not None:
            if slot_index < 0 or slot_index >= len(image_slots):
                raise ValueError(f"Slot index {slot_index} out of range")
            slots_to_run = [image_slots[slot_index]]
        else:
            slots_to_run = image_slots

        # ── Count total eligible prompts (for progress bar) ──────────────────
        # Source availability is re-checked lazily per-slot during generation,
        # so we count all enabled prompts with a valid output_id regardless of
        # whether their source image currently exists.
        total_prompts = 0
        for slot in slots_to_run:
            for p in slot.get("prompts", []):
                if not p.get("enabled", True):
                    continue
                if prompt_id is not None and p["id"] != prompt_id:
                    continue
                if p.get("output_id"):
                    total_prompts += 1

        # Load backend config
        win         = app_config_service.get_backend("windows")
        comfyui_url = win.get("api_url")    or settings.comfyui_upscale_url
        input_dir   = Path(win.get("input_dir")  or settings.comfyui_upscale_input_dir)
        comfyui_out = Path(win.get("output_dir") or settings.comfyui_upscale_output_dir)
        wf_path_str = win.get("models", {}).get("i2i", {}).get("workflow_json", "")

        if not wf_path_str:
            raise ValueError(
                "Brak ścieżki do workflow JSON (app_config.yaml → "
                "backends.windows.models.i2i.workflow_json)"
            )
        wf_path = Path(wf_path_str)
        if not wf_path.exists():
            raise ValueError(f"Workflow JSON nie istnieje: {wf_path}")

        workflow_template = json.loads(wf_path.read_text(encoding="utf-8"))
        _log(f"  📋 Workflow: i2i  |  {wf_path.name}")
        tile_name = tile.get("name", tile_id)

        _set_job(run_id, tile_id, {
            "status":         "running",
            "tile_id":        tile_id,
            "tile_name":      tile_name,
            "total":          total_prompts,
            "done":           0,
            "skipped":        0,
            "current_prompt": None,
            "errors":         [],
            "started_at":     time.time(),
        })

        slot_label = f" (slot {slot_index})" if slot_index is not None else ""
        _log(f"🖼 Pic Studio: [{tile_name}]{slot_label} start — {total_prompts} "
             f"kombinacji (źródła resolwowane per-slot)")

        loop    = asyncio.get_running_loop()
        errors: list[dict] = []
        done    = 0
        skipped = 0
        idx     = 0   # global counter across all slots

        for slot in slots_to_run:
            image_name = slot.get("image", "")
            if not image_name:
                continue

            # Resolve source NOW — after previous slots may have generated files
            source_path = next(
                (sd / image_name for sd in source_dirs if (sd / image_name).exists()),
                None,
            )
            if source_path is None:
                slot_prompts = [
                    p for p in slot.get("prompts", [])
                    if p.get("enabled", True)
                    and (prompt_id is None or p["id"] == prompt_id)
                    and p.get("output_id")
                ]
                skipped += len(slot_prompts)
                _update_job(run_id, tile_id, skipped=skipped)
                _log(f"  ⚠ Źródło nie istnieje jeszcze (lub nie ma go w żadnym katalogu), "
                     f"pomijam slot: {image_name}")
                continue

            for p in slot.get("prompts", []):
                if not p.get("enabled", True):
                    continue
                if prompt_id is not None and p["id"] != prompt_id:
                    continue
                oid = p.get("output_id")
                if not oid:
                    _log(f"  ⚠ Prompt {p['id']} nie ma output_id — pomijam (odśwież kafelek)")
                    skipped += 1
                    _update_job(run_id, tile_id, skipped=skipped)
                    continue
                dest = output_dir / f"{oid}.png"
                if not force_all and dest.exists():
                    skipped += 1
                    _update_job(run_id, tile_id, skipped=skipped)
                    continue

                idx += 1
                pname = p.get("name", p["id"])
                label = f"{image_name} × {pname}"
                _update_job(run_id, tile_id, current_prompt=label)
                _log(f"  ⚙ [{idx}/{total_prompts}] {label} …")
                _archive_existing(dest)   # archive previous result before overwriting

                pos = p.get("positive", "")
                if global_suffix:
                    pos = f"{pos}, {global_suffix}" if pos else global_suffix
                neg     = p.get("negative", "")
                params  = p.get("params", {})
                steps   = int(params.get("steps",   30))
                cfg     = float(params.get("cfg",    8.0))
                denoise = float(params.get("denoise", 1.0))
                _log(f"  📝 [{idx}] steps={steps}  cfg={cfg}  denoise={denoise}  "
                     f"prompt: {pos[:100]}{'…' if len(pos) > 100 else ''}")

                # Pad source to project ratio if requested
                padded_path: "Path | None" = None
                if pad_input_to_ratio:
                    padded_path = _pad_to_ratio(source_path, target_w, target_h)
                effective_source = padded_path if padded_path else source_path

                try:
                    await _generate_one(
                        loop, comfyui_url, input_dir, comfyui_out,
                        workflow_template, effective_source,
                        pos, neg, steps, cfg, denoise, dest, label=label,
                    )
                    if tile.get("crop_to_subject") and dest.exists():
                        _crop_to_subject(dest)
                    done += 1
                    _update_job(run_id, tile_id, done=done)
                    _log(f"  ✅ [{idx}/{total_prompts}] {label} → {dest.name}")
                except Exception as exc:
                    errors.append({
                        "prompt_id":   p["id"],
                        "prompt_name": pname,
                        "image":       image_name,
                        "error":       str(exc),
                    })
                    _update_job(run_id, tile_id, errors=list(errors))
                    _log(f"  ❌ [{idx}/{total_prompts}] {label}: {exc}")
                finally:
                    # Clean up padded temp file
                    if padded_path and padded_path.exists():
                        try:
                            padded_path.unlink()
                        except Exception:
                            pass

        final_status = "error" if (errors and done == 0) else "done"
        _update_job(
            run_id, tile_id,
            status=final_status,
            done=done,
            current_prompt=None,
            errors=errors,
        )
        summary = (f"✅ Pic Studio: [{tile_name}]{slot_label} "
                   f"zakończono {done}/{total_prompts}")
        if skipped:
            summary += f" ({skipped} pominiętych)"
        if errors:
            summary += f" ({len(errors)} błędów)"
        _log(summary)

    except Exception as exc:
        _log(f"❌ Pic Studio [{tile_id}]: {exc}")
        _set_job(run_id, tile_id, {
            "status":         "error",
            "tile_id":        tile_id,
            "tile_name":      tile_id,
            "total":          0,
            "done":           0,
            "skipped":        0,
            "current_prompt": None,
            "errors":         [{"error": str(exc)}],
        })


def start_tile_run(
    run_id: str,
    tile_id: str,
    force_all: bool,
    slot_index: int | None = None,
    prompt_id:  str | None = None,
) -> str:
    """
    Launch tile generation as a background asyncio task.
    slot_index=None runs all slots; pass an int to run a single image slot.
    Returns 'ok' or 'already_running'.
    """
    existing = _jobs.get(f"{run_id}::{tile_id}", {})
    if existing.get("status") == "running":
        return "already_running"

    _set_job(run_id, tile_id, {
        "status":         "queued",
        "tile_id":        tile_id,
        "total":          0,
        "done":           0,
        "current_prompt": None,
        "errors":         [],
    })

    asyncio.create_task(_run_tile_async(run_id, tile_id, force_all, slot_index, prompt_id))
    return "ok"
