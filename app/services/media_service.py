# -*- coding: utf-8 -*-
"""
Media service — resolves paths for frames, transitions and chain files.

All paths are derived from PROJECT_FOLDER read from the RUN file —
no arbitrary filesystem access.

Directory structure under PROJECT_FOLDER:
    frames/
        {stem}_start.jpg
        {stem}_end.jpg
    transitions/
        {from_stem}_{to_stem}_transition.mp4
        chains/
            {chain_prefix}_NNN.mp4
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any

from app.services.run_file_service import get_run_details, get_run_flow

# ── Path resolution helpers ───────────────────────────────────────────

def _project_folder(run_filename: str) -> Path | None:
    info = get_run_details(run_filename)
    if not info or not info.get("project_folder"):
        return None
    return Path(info["project_folder"])


def frame_path(project_folder: Path, item_file: str, kind: str) -> Path:
    """Return path to _start.jpg or _end.jpg for a given source file."""
    stem = Path(item_file).stem
    return project_folder / "frames" / f"{stem}_{kind}.jpg"


def transition_path(project_folder: Path, from_file: str, to_file: str) -> Path:
    """Normal transition: transitions/{from_stem}_{to_stem}_transition.mp4"""
    from_stem = Path(from_file).stem
    to_stem   = Path(to_file).stem
    return project_folder / "transitions" / f"{from_stem}_{to_stem}_transition.mp4"


def chain_path(project_folder: Path, chain_filename: str) -> Path:
    """Chain file: transitions/chains/{chain_filename}"""
    return project_folder / "transitions" / "chains" / chain_filename


# ── Status check ─────────────────────────────────────────────────────

def get_transition_status(run_filename: str) -> dict | None:
    """
    For each FLOW item determine whether its output file exists.

    Returns a list of dicts:
        {
            "index":    int,
            "type":     "file" | "chain" | "break",
            "name":     str,              # transition/chain filename
            "exists":   bool,
            "size_mb":  float | None,
            "path":     str | None,       # absolute path (for serving)
        }
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None

    flow_data = get_run_flow(run_filename)
    if not flow_data:
        return None

    flow: list[dict[str, Any]] = flow_data["flow"]
    results = []

    # We need to iterate pairs like batch_transitions does
    # to derive the correct transition filenames.
    # Collect all non-break items in order.
    items = [item for item in flow if not item.get("break")]

    # Walk pairs
    for idx, item in enumerate(flow):
        if item.get("break"):
            results.append({"index": idx, "type": "break",
                             "name": None, "exists": None,
                             "size_mb": None, "path": None})
            continue

        if item.get("chain"):
            # Each step in the chain has its own output file
            chain_prefix = item.get("chain_prefix") or "chain"
            step_results = []
            for si, step in enumerate(item["chain"]):
                fname = f"{chain_prefix}_{si+1:03d}.mp4"
                p = chain_path(pf, fname)
                exists = p.exists()
                step_results.append({
                    "filename": fname,
                    "exists":   exists,
                    "size_mb":  round(p.stat().st_size / 1_048_576, 1) if exists else None,
                    "path":     str(p) if exists else None,
                })
            all_exist = all(s["exists"] for s in step_results)
            results.append({
                "index":    idx,
                "type":     "chain",
                "name":     chain_prefix,
                "steps":    step_results,
                "exists":   all_exist,
                "size_mb":  None,
                "path":     None,
            })
            continue

        # FILE item — need the NEXT non-break item to build the transition name
        # Find next file/chain in the flow
        next_item = None
        for j in range(flow.index(item) + 1, len(flow)):
            if not flow[j].get("break"):
                next_item = flow[j]
                break

        if next_item is None:
            # Last item — no transition generated
            results.append({"index": idx, "type": "file",
                             "name": item.get("file"), "exists": None,
                             "size_mb": None, "path": None})
            continue

        from_file = item.get("file", "")
        to_file   = (next_item.get("file") or
                     (next_item.get("chain_prefix", "chain") + "_001.mp4"))

        if next_item.get("chain"):
            # Transition into a chain → output is the chain's first file
            chain_prefix = next_item.get("chain_prefix") or "chain"
            p = chain_path(pf, f"{chain_prefix}_001.mp4")
        else:
            p = transition_path(pf, from_file, to_file)

        exists = p.exists()
        results.append({
            "index":   idx,
            "type":    "file",
            "name":    p.name,
            "exists":  exists,
            "size_mb": round(p.stat().st_size / 1_048_576, 1) if exists else None,
            "path":    str(p) if exists else None,
        })

    return {
        "project_folder": str(pf),
        "items":          results,
        "total":          sum(1 for r in results if r["exists"] is not None),
        "existing":       sum(1 for r in results if r["exists"] is True),
        "missing":        sum(1 for r in results if r["exists"] is False),
    }


# ── Frame serving ─────────────────────────────────────────────────────

def resolve_frame(run_filename: str, item_file: str, kind: str) -> Path | None:
    """Return Path to a frame file, or None if not found."""
    if kind not in ("start", "end"):
        return None
    pf = _project_folder(run_filename)
    if pf is None:
        return None
    p = frame_path(pf, item_file, kind)
    return p if p.exists() else None


# ── Video serving ─────────────────────────────────────────────────────

def resolve_video(run_filename: str, video_name: str) -> Path | None:
    """
    Resolve a transition or chain .mp4 by name.
    Looks in transitions/ then transitions/chains/.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None

    for candidate in [
        pf / "transitions" / video_name,
        pf / "transitions" / "chains" / video_name,
    ]:
        if candidate.exists():
            return candidate
    return None


# ── Archive (rename with timestamp suffix) ────────────────────────────

def archive_video(run_filename: str, video_name: str) -> dict:
    """
    Rename  transitions/{name}.mp4
    →       transitions/{name}_ver{YYMMDDHHmmss}.mp4
    (or same in chains/ subdirectory).
    Returns {ok, new_name, error}.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono PROJECT_FOLDER"}

    original = resolve_video(run_filename, video_name)
    if original is None:
        return {"ok": False, "error": f"Plik nie istnieje: {video_name}"}

    ts       = datetime.now().strftime("%y%m%d%H%M%S")
    stem     = original.stem
    new_name = f"{stem}_ver{ts}.mp4"
    new_path = original.parent / new_name

    try:
        original.rename(new_path)
    except OSError as exc:
        return {"ok": False, "error": str(exc)}

    return {"ok": True, "new_name": new_name, "old_name": video_name}
