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

        for p in prompts:
            oid = p.get("output_id")
            if not oid:
                _log(f"  ⚠ Slot {slot_idx} / Prompt {p['id']} nie ma output_id — pomijam")
                continue
            dest = output_dir / f"{oid}.png"
            if force_all or not dest.exists():
                to_run.append((scene_path, char_paths, p, dest, slot_idx,
                               f"{scene_image} × {p.get('name', p['id'])}"))

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

    # Select workflow based on max number of character reference images across slots.
    # 0-1 refs → ci_1ref (scene + 1 LoadImage ref slot)
    # 2+  refs → ci     (scene + 2 LoadImage ref slots)
    max_refs = max(
        (len(s.get("character_images", [])) for s in scene_slots),
        default=0,
    )
    if max_refs >= 2:
        wf_path_str = (models.get("ci",      {}).get("workflow_json", "")
                       or models.get("ci_1ref", {}).get("workflow_json", ""))
    else:
        wf_path_str = (models.get("ci_1ref", {}).get("workflow_json", "")
                       or models.get("ci",      {}).get("workflow_json", "")
                       or models.get("i2i",     {}).get("workflow_json", ""))

    if not wf_path_str:
        raise ValueError("Brak ścieżki do workflow JSON (app_config.yaml → backends.windows.models.ci / ci_1ref)")
    wf_path = Path(wf_path_str)
    if not wf_path.exists():
        raise ValueError(f"Workflow JSON nie istnieje: {wf_path}")
    workflow_template = json.loads(wf_path.read_text(encoding="utf-8"))
    _log(f"  📋 Workflow: {wf_path.name} (max {max_refs} ref{'s' if max_refs != 1 else ''})")

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

    for idx, (scene_path, char_paths, p, dest, slot_idx, label) in enumerate(to_run, 1):
        pname = p.get("name", p["id"])
        _update_job(run_id, tile_id, current_prompt=label)
        _log(f"  ⚙ [{idx}/{len(to_run)}] {label} …")
        _archive_existing(dest)   # archive previous result before overwriting

        pos = p.get("positive", "")
        if global_suffix:
            pos = f"{pos}, {global_suffix}" if pos else global_suffix
        params  = p.get("params", {})
        steps   = int(params.get("steps",   30))
        cfg     = float(params.get("cfg",    8.0))
        denoise = float(params.get("denoise", 1.0))
        _log(f"  📝 Prompt pozytywny: {pos[:120]}{'…' if len(pos) > 120 else ''}")

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
            _migrate_tile,
            _slugify,
            _get_source_dirs,
        )

        data = _load_sess(run_id)
        tile = next(
            (t for t in data.get("pic_flow", []) if t["id"] == tile_id), None
        )
        if not tile:
            raise ValueError(f"Tile not found: {tile_id}")

        _migrate_tile(tile)

        tile_type     = tile.get("type", "one_image_many_prompts")
        output_dir    = Path(tile.get("output_dir", ""))
        global_suffix = tile.get("global_suffix", "")

        # ── Route to character_insert pipeline ────────────────────────────────
        if tile_type == "character_insert":
            await _run_character_insert_async(
                run_id, tile_id, tile, output_dir, global_suffix, force_all, prompt_id, slot_index,
            )
            return

        source_dirs   = [Path(d) for d in _get_source_dirs(tile)]
        image_slots   = tile.get("image_slots", [])

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

        # Build work queue: list of (source_path, prompt, dest_path, label)
        # Naming: {output_id}.png  (output_id stored per prompt instance in YAML)
        to_run: list[tuple[Path, dict, Path, str]] = []
        total_prompts = 0
        for slot in slots_to_run:
            image_name = slot.get("image", "")
            if not image_name:
                continue
            source_path = next(
                (sd / image_name for sd in source_dirs if (sd / image_name).exists()),
                None,
            )
            if source_path is None:
                _log(f"  ⚠ Obrazek nie istnieje w żadnym katalogu źródłowym, pomijam: {image_name}")
                continue
            for p in slot.get("prompts", []):
                if not p.get("enabled", True):
                    continue
                if prompt_id is not None and p["id"] != prompt_id:
                    continue
                oid = p.get("output_id")
                if not oid:
                    _log(f"  ⚠ Prompt {p['id']} nie ma output_id — pomijam (odśwież kafelek)")
                    continue
                total_prompts += 1
                dest = output_dir / f"{oid}.png"
                if force_all or not dest.exists():
                    to_run.append((source_path, p, dest, image_name))

        skipped = total_prompts - len(to_run)
        if not to_run:
            _set_job(run_id, tile_id, {
                "status":         "done",
                "tile_id":        tile_id,
                "total":          0,
                "done":           0,
                "skipped":        skipped,
                "current_prompt": None,
                "errors":         [],
            })
            _log(f"🖼 Pic Studio: [{tile.get('name', tile_id)}] "
                 f"wszystko już wygenerowane ({skipped} pominiętych)")
            return

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
        tile_name = tile.get("name", tile_id)

        _set_job(run_id, tile_id, {
            "status":         "running",
            "tile_id":        tile_id,
            "tile_name":      tile_name,
            "total":          len(to_run),
            "done":           0,
            "skipped":        skipped,
            "current_prompt": None,
            "errors":         [],
            "started_at":     time.time(),
        })

        slot_label = f" (slot {slot_index})" if slot_index is not None else ""
        _log(f"🖼 Pic Studio: [{tile_name}]{slot_label} start — {len(to_run)} "
             f"kombinacji" + (f" ({skipped} pominiętych)" if skipped else ""))

        loop   = asyncio.get_running_loop()
        errors: list[dict] = []
        done   = 0

        for idx, (source_path, p, dest, image_name) in enumerate(to_run, 1):
            pname = p.get("name", p["id"])
            label = f"{image_name} × {pname}"
            _update_job(run_id, tile_id, current_prompt=label)
            _log(f"  ⚙ [{idx}/{len(to_run)}] {label} …")
            _archive_existing(dest)   # archive previous result before overwriting

            pos = p.get("positive", "")
            if global_suffix:
                pos = f"{pos}, {global_suffix}" if pos else global_suffix
            neg     = p.get("negative", "")
            params  = p.get("params", {})
            steps   = int(params.get("steps",   30))
            cfg     = float(params.get("cfg",    8.0))
            denoise = float(params.get("denoise", 1.0))
            _log(f"  📝 Prompt pozytywny: {pos[:120]}{'…' if len(pos) > 120 else ''}")

            try:
                await _generate_one(
                    loop, comfyui_url, input_dir, comfyui_out,
                    workflow_template, source_path,
                    pos, neg, steps, cfg, denoise, dest, label=label,
                )
                done += 1
                _update_job(run_id, tile_id, done=done)
                _log(f"  ✅ [{idx}/{len(to_run)}] {label} → {dest.name}")
            except Exception as exc:
                errors.append({
                    "prompt_id":   p["id"],
                    "prompt_name": pname,
                    "image":       image_name,
                    "error":       str(exc),
                })
                _update_job(run_id, tile_id, errors=list(errors))
                _log(f"  ❌ [{idx}/{len(to_run)}] {label}: {exc}")

        final_status = "error" if (errors and done == 0) else "done"
        _update_job(
            run_id, tile_id,
            status=final_status,
            done=done,
            current_prompt=None,
            errors=errors,
        )
        summary = (f"✅ Pic Studio: [{tile_name}]{slot_label} "
                   f"zakończono {done}/{len(to_run)}")
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
