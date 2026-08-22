# -*- coding: utf-8 -*-
"""
Multichain migration service — converts old flow patterns to the new `multichain` tile.

Two conversion kinds, always manual/opt-in (analyze returns proposals, apply only
touches items the user explicitly selected):

1. file -> file (single_transition_service style, config lives inline on the FROM
   file tile) -> file -> multichain(1 step) -> file. Every adjacent file/file pair
   in the flow is a candidate (per-pair, never merged across a longer run — merging
   would lose per-pair I2V2I end-frame precision, which is why chains of file->file
   exist in the first place: hitting every intermediate keyframe exactly).

2. Old `chain:` block -> `multichain` (model_class from `backend`: atlascloud ->
   atlascloud, everything else -> wan). Same chain_prefix kept (file naming
   convention is identical), so this is a pure YAML rewrite with zero file moves.

Effective per-pair config is resolved the same way single_transition_service._pick()
does: FROM file's value wins, TO file's value is the fallback — so a migrated
multichain step generates identically to what the old file->file transition would.

blocks_to_swap is intentionally NEVER carried over — multichain always sources BTS
from the global auto_bts_table, by design (no manual BTS field in the UI at all).
"""

import re
from pathlib import Path
from typing import Any

from app.services.media_service import _project_folder
from app.services.run_file_service import RUNS_FOLDER, get_run_flow

_PICK_KEYS = (
    "pos", "neg", "duration", "fps", "cfg", "seed", "frame_interpolation",
    "lora_high", "lora_low", "lora_name", "lora_strength", "use_lightning",
    "workflow", "backend", "atlascloud_resolution", "atlascloud_prompt_extend",
    "width", "height", "audio_prompt", "audio_negative_prompt",
)

_VER_RE = re.compile(r"_ver(\d{12})$")


def _is_plain_file_item(item: Any) -> bool:
    """True for a plain `file:` loader tile (not chain/multichain/talk/multitalk/dubit/header/break)."""
    return isinstance(item, dict) and "file" in item and item.get("type") is None


def _pick(from_cfg: dict, to_cfg: dict, key: str):
    v = from_cfg.get(key)
    if v is not None:
        return v
    v = to_cfg.get(key)
    if v is not None:
        return v
    return None


def _model_class_for_backend(backend: str | None) -> str:
    return "atlascloud" if backend == "atlascloud" else "wan"


def _build_multichain_step(from_cfg: dict, to_cfg: dict) -> dict:
    step: dict[str, Any] = {
        "duration": _pick(from_cfg, to_cfg, "duration") or 3,
        "pos": _pick(from_cfg, to_cfg, "pos") or "NONE",
        "neg": "",
        # Always explicit — multichain steps default RIFE to off, and old file->file
        # tiles never carried this field, so it must never be left unset here
        # (an unset key silently falls back to True in chain_service._run_chain()).
        "frame_interpolation": _pick(from_cfg, to_cfg, "frame_interpolation") or False,
    }
    for k in ("lora_high", "lora_low", "lora_name",
              "lora_strength", "use_lightning", "workflow",
              "audio_prompt", "audio_negative_prompt"):
        v = _pick(from_cfg, to_cfg, k)
        if v is not None:
            step[k] = v
    return step


def _dedupe_prefix(base: str, used: set[str]) -> str:
    prefix = base
    n = 2
    while prefix in used:
        prefix = f"{base}_{n}"
        n += 1
    used.add(prefix)
    return prefix


def _existing_prefixes(flow: list) -> set[str]:
    return {
        item["chain_prefix"]
        for item in flow
        if isinstance(item, dict) and item.get("chain_prefix")
    }


def analyze_migration(run_filename: str) -> dict:
    """Dry-run: scan the flow, return proposed conversions. Touches nothing."""
    flow_data = get_run_flow(run_filename)
    if not flow_data:
        raise ValueError(f"Nie można wczytać flow: {run_filename}")
    flow = flow_data["flow"]

    pf = _project_folder(run_filename)
    used_prefixes = _existing_prefixes(flow)

    pairs = []
    for i in range(len(flow) - 1):
        a, b = flow[i], flow[i + 1]
        if not (_is_plain_file_item(a) and _is_plain_file_item(b)):
            continue
        stem_a = Path(a["file"]).stem
        stem_b = Path(b["file"]).stem
        base_prefix = f"{stem_a}_{stem_b}"
        prefix = _dedupe_prefix(base_prefix, used_prefixes)

        backend = _pick(a, b, "backend") or "linux"
        model_class = _model_class_for_backend(backend)

        old_name = f"{stem_a}_{stem_b}_transition.mp4"
        file_exists = False
        archived_count = 0
        if pf:
            transitions_dir = pf / "transitions"
            if (transitions_dir / old_name).exists():
                file_exists = True
            if transitions_dir.exists():
                archived_count = sum(
                    1 for _ in transitions_dir.glob(f"{stem_a}_{stem_b}_transition_ver????????????.mp4")
                )

        pairs.append({
            "key": f"pair_{i}",
            "from_idx": i,
            "to_idx": i + 1,
            "from_file": a["file"],
            "to_file": b["file"],
            "chain_prefix": prefix,
            "model_class": model_class,
            "old_transition_name": old_name,
            "file_exists": file_exists,
            "archived_versions": archived_count,
        })

    chains = []
    for i, item in enumerate(flow):
        if isinstance(item, dict) and "chain" in item and item.get("type") != "multichain":
            backend = item.get("backend") or "linux"
            chains.append({
                "key": f"chain_{i}",
                "idx": i,
                "chain_prefix": item.get("chain_prefix", "chain"),
                "model_class": _model_class_for_backend(backend),
                "steps": len(item.get("chain") or []),
            })

    return {"pairs": pairs, "chains": chains}


def _rename_with_archives(transitions_dir: Path, chains_dir: Path,
                           old_name: str, new_name: str) -> list[str]:
    """Rename the main transition file plus any archived (_verTIMESTAMP) versions.
    Returns a list of human-readable 'old -> new' descriptions of what happened."""
    chains_dir.mkdir(parents=True, exist_ok=True)
    done = []

    src = transitions_dir / old_name
    dst = chains_dir / new_name
    if src.exists() and not dst.exists():
        src.rename(dst)
        done.append(f"{src.name} -> {dst}")

    old_stem = old_name.rsplit(".", 1)[0]
    new_stem = new_name.rsplit(".", 1)[0]
    if transitions_dir.exists():
        for verfile in transitions_dir.glob(f"{old_stem}_ver????????????.mp4"):
            m = _VER_RE.search(verfile.stem)
            if not m:
                continue
            ts = m.group(1)
            ver_dst = chains_dir / f"{new_stem}_ver{ts}.mp4"
            if not ver_dst.exists():
                verfile.rename(ver_dst)
                done.append(f"{verfile.name} -> {ver_dst}")

    return done


def apply_migration(run_filename: str, pair_keys: list[str], chain_keys: list[str]) -> dict:
    """Apply the selected proposals: rename files on disk + rewrite the flow YAML."""
    flow_data = get_run_flow(run_filename)
    if not flow_data:
        raise ValueError(f"Nie można wczytać flow: {run_filename}")
    flow = list(flow_data["flow"])

    pf = _project_folder(run_filename)
    if pf is None:
        raise ValueError(f"Nie znaleziono project_folder: {run_filename}")
    transitions_dir = pf / "transitions"
    chains_dir = transitions_dir / "chains"

    proposal = analyze_migration(run_filename)
    pair_by_key = {p["key"]: p for p in proposal["pairs"]}
    chain_by_key = {c["key"]: c for c in proposal["chains"]}

    file_ops: list[str] = []
    errors: list[str] = []
    chains_converted = 0
    pairs_converted = 0

    # Old chain -> multichain: pure structural rewrite, same chain_prefix, no file moves.
    for key in chain_keys:
        c = chain_by_key.get(key)
        if not c:
            errors.append(f"{key}: nie znaleziono w bieżącej analizie (flow się zmienił?)")
            continue
        old_item = flow[c["idx"]]
        if not isinstance(old_item, dict) or "chain" not in old_item:
            errors.append(f"{key}: element pod indeksem {c['idx']} już nie jest chainem")
            continue
        new_item: dict[str, Any] = {
            "type": "multichain",
            "chain_prefix": old_item.get("chain_prefix", "chain"),
            "model_class": c["model_class"],
        }
        for k in ("neg", "width", "height", "atlascloud_resolution", "atlascloud_prompt_extend",
                  "ambient_audio_prompt", "ambient_audio_negative_prompt"):
            if k in old_item:
                new_item[k] = old_item[k]
        new_item["chain"] = [
            {k: v for k, v in step.items() if k != "blocks_to_swap"}
            for step in (old_item.get("chain") or [])
        ]
        flow[c["idx"]] = new_item
        chains_converted += 1

    # file -> file pairs: build multichain, rename files, replace FROM file with a pure loader.
    # Process from the end so earlier indices stay valid while we mutate the list in place
    # (we replace in place, we never insert/remove entries, so order doesn't strictly
    # matter here, but iterating a stable snapshot avoids any doubt).
    for key in pair_keys:
        p = pair_by_key.get(key)
        if not p:
            errors.append(f"{key}: nie znaleziono w bieżącej analizie (flow się zmienił?)")
            continue
        i = p["from_idx"]
        a = flow[i]
        b = flow[i + 1]
        if not (_is_plain_file_item(a) and _is_plain_file_item(b)):
            errors.append(f"{key}: element pod indeksem {i}/{i+1} już nie jest parą file->file")
            continue

        prefix = p["chain_prefix"]
        new_name = f"{prefix}_001.mp4"
        try:
            ops = _rename_with_archives(transitions_dir, chains_dir, p["old_transition_name"], new_name)
            file_ops.extend(ops)
        except Exception as exc:
            errors.append(f"{key}: błąd rename plików: {exc}")
            continue

        step = _build_multichain_step(a, b)
        multichain_item: dict[str, Any] = {
            "type": "multichain",
            "chain_prefix": prefix,
            "model_class": p["model_class"],
            "neg": _pick(a, b, "neg") or "",
            "chain": [step],
        }
        w = _pick(a, b, "width")
        h = _pick(a, b, "height")
        if w and h:
            multichain_item["width"] = w
            multichain_item["height"] = h
        for k in ("ambient_audio_prompt", "ambient_audio_negative_prompt"):
            v = _pick(a, b, k)
            if v is not None:
                multichain_item[k] = v
        if p["model_class"] == "atlascloud":
            for k in ("atlascloud_resolution", "atlascloud_prompt_extend"):
                v = _pick(a, b, k)
                if v is not None:
                    multichain_item[k] = v

        # FROM file becomes a pure loader (new-tile convention).
        flow[i] = {"file": a["file"], "backend": "linux", "duration": 2, "pos": "NONE", "neg": "NONE"}
        # Insert the multichain right after the (now-loader) FROM file, before TO file.
        # We can't just overwrite index i+1 (that's the TO file, still needed) -
        # so we insert instead. Do this via a marker-based rebuild below.
        flow[i] = {"__migrated_file__": flow[i], "__insert_after__": multichain_item}
        pairs_converted += 1

    # Strip the terminal file of a converted run too (its fields were only ever a
    # fallback for the pair before it, never a primary source - but they're dead now).
    # Only the true end of a selected run: a to_idx that is never itself a selected
    # from_idx (if it is, it gets stripped anyway when its own pair is processed).
    selected = [pair_by_key[k] for k in pair_keys if k in pair_by_key]
    selected_from_idxs = {p["from_idx"] for p in selected}
    selected_to_idxs = {p["to_idx"] for p in selected}
    for idx in selected_to_idxs - selected_from_idxs:
        item = flow[idx]
        if isinstance(item, dict) and "file" in item and "__migrated_file__" not in item:
            flow[idx] = {"file": item["file"], "backend": "linux", "duration": 2, "pos": "NONE", "neg": "NONE"}

    # Rebuild flow, expanding the insert markers (single pass, preserves order).
    new_flow = []
    for item in flow:
        if isinstance(item, dict) and "__migrated_file__" in item:
            new_flow.append(item["__migrated_file__"])
            new_flow.append(item["__insert_after__"])
        else:
            new_flow.append(item)

    if chains_converted > 0 or pairs_converted > 0:
        flow_key = "flow_test" if flow_data.get("flow_type") == "test" else "flow"
        yaml_path = RUNS_FOLDER / run_filename
        from app.services.yaml_service import save_yaml_flow, generate_py_from_yaml
        save_yaml_flow(yaml_path, new_flow, flow_key)
        try:
            generate_py_from_yaml(yaml_path)
        except Exception:
            pass

    return {
        "ok": True,
        "converted_pairs": pairs_converted,
        "converted_chains": chains_converted,
        "file_ops": file_ops,
        "errors": errors,
    }
