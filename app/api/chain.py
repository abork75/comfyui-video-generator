# -*- coding: utf-8 -*-
"""
API router for Chain generation.
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.chain_service import get_chain_status, start_chain, cancel_chain
from app.services.media_service import _project_folder

router = APIRouter(prefix="/api/chain", tags=["chain"])


@router.get("/status")
async def chain_status():
    """Current chain job state."""
    return get_chain_status()


@router.post("/start")
async def chain_start(request: Request):
    """
    Start a chain generation job.

    Body JSON:
    {
        "run_filename":  "RUN_001.yaml",
        "chain_prefix":  "ewelina_stands",
        "from_step":     0              // 0-indexed step to start from
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename = body.get("run_filename")
    chain_prefix = body.get("chain_prefix")
    from_step    = int(body.get("from_step", 0))
    to_step_raw  = body.get("to_step")
    to_step      = int(to_step_raw) if to_step_raw is not None else None

    if not run_filename or not chain_prefix:
        raise HTTPException(
            status_code=422,
            detail="Required fields: run_filename, chain_prefix",
        )

    result = start_chain(run_filename, chain_prefix, from_step, to_step)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/cancel")
async def chain_cancel():
    """Cancel the running chain job."""
    return cancel_chain()


@router.post("/rename-files")
async def chain_rename_files(request: Request):
    """
    Rename chain output files when chain_prefix changes — video (transitions/
    chains/*.mp4, including archive/marker variants like _ver..._beforedeblur)
    AND its FX side file (transitions/fx/*.mp3, see utils.mmaudio_utils.
    fx_sidecar_path). Renaming only the video used to leave the FX sidecar
    orphaned under the old name (2026-09-09 incident — confirmed real data
    loss reported by the user, root cause not fully pinned down, but this was
    a definite, independently-confirmed gap worth closing regardless).

    Two-pass / all-or-nothing per file: EVERY planned (src, dst) pair is
    validated up front — dst must not already exist, and no two sources may
    collide on the same dst — before any actual rename happens. A file is
    only ever renamed if its destination was free at validation time; a
    partial failure elsewhere can't leave one directory renamed and the
    other not (video and fx move together or neither does, per name).

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "old_prefix":   "ewelina_stands",
        "new_prefix":   "ewelina_sits",
        "dry_run":      false
    }

    Returns:
    {
        "renamed": ["ewelina_stands_001.mp4", "ewelina_stands_001.mp3", ...],
        "skipped": [...],   # destination already existed, or collided with another planned rename
        "errors":  [...],   # rename() itself failed (e.g. transient file lock)
        "dry_run": false
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename = body.get("run_filename")
    old_prefix   = body.get("old_prefix", "").strip()
    new_prefix   = body.get("new_prefix", "").strip()

    if not run_filename or not old_prefix or not new_prefix:
        raise HTTPException(status_code=422, detail="Required fields: run_filename, old_prefix, new_prefix")
    if old_prefix == new_prefix:
        return {"renamed": [], "skipped": [], "errors": [], "dry_run": bool(body.get("dry_run", False))}

    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(status_code=404, detail=f"Project folder not found for: {run_filename}")

    chains_dir = pf / "transitions" / "chains"
    fx_dir     = pf / "transitions" / "fx"
    dry_run = bool(body.get("dry_run", False))

    # Pass 1: collect every candidate (src, dst) across both directories —
    # nothing is touched yet.
    def _candidates(directory, ext):
        out = []
        if not directory.exists():
            return out
        for src in sorted(directory.iterdir()):
            if not src.is_file():
                continue
            name = src.name
            if name.startswith(old_prefix + "_") and name.endswith(ext):
                suffix = name[len(old_prefix):]   # e.g. "_001.mp4" / "_001.mp3"
                dst = directory / (new_prefix + suffix)
                out.append((src, dst))
        return out

    planned = _candidates(chains_dir, ".mp4") + _candidates(fx_dir, ".mp3")

    # Pass 2: validate ALL destinations up front — free, and no collision
    # between two planned renames landing on the same dst.
    seen_dst = set()
    valid, skipped = [], []
    for src, dst in planned:
        dst_key = str(dst)
        if dst.exists() or dst_key in seen_dst:
            skipped.append(src.name)
            continue
        seen_dst.add(dst_key)
        valid.append((src, dst))

    if dry_run:
        return {"renamed": [s.name for s, d in valid], "skipped": skipped, "errors": [], "dry_run": True}

    # Pass 3: only now actually rename — every pair here was already
    # confirmed collision-free.
    renamed, errors = [], []
    for src, dst in valid:
        try:
            src.rename(dst)
            renamed.append(src.name)
        except Exception as e:
            errors.append(f"{src.name}: {e}")

    return {"renamed": renamed, "skipped": skipped, "errors": errors, "dry_run": False}


@router.post("/split")
async def chain_split_files(request: Request):
    """
    Rename chain files with renumbering — used for split and merge operations.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "old_prefix":   "foo",      // source prefix
        "new_prefix":   "foo_b",    // destination prefix
        "from_step":    3,          // 1-based: first step to rename
        "to_step":      5,          // 1-based: last step to rename
        "new_start":    1           // 1-based: new numbering starts here
    }

    Split example: foo_003→foo_b_001, foo_004→foo_b_002, foo_005→foo_b_003
    Merge example: bar_001→foo_004, bar_002→foo_005  (new_start = prev_chain_len + 1)
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    run_filename = body.get("run_filename")
    old_prefix   = body.get("old_prefix", "").strip()
    new_prefix   = body.get("new_prefix", "").strip()
    from_step    = int(body.get("from_step", 1))
    to_step      = int(body.get("to_step", 1))
    new_start    = int(body.get("new_start", 1))
    dry_run      = bool(body.get("dry_run", False))

    if not run_filename or not old_prefix or not new_prefix:
        raise HTTPException(status_code=422, detail="Required: run_filename, old_prefix, new_prefix")

    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(status_code=404, detail=f"Project folder not found: {run_filename}")

    chains_dir = pf / "transitions" / "chains"
    frames_dir = pf / "frames"
    renamed, skipped, errors = [], [], []

    # offset: old_step + offset = new_step
    offset = new_start - from_step

    for old_step in range(from_step, to_step + 1):
        new_step = old_step + offset
        old_stem = f"{old_prefix}_{old_step:03d}"
        new_stem = f"{new_prefix}_{new_step:03d}"

        # Main video file
        if chains_dir.exists():
            src = chains_dir / f"{old_stem}.mp4"
            dst = chains_dir / f"{new_stem}.mp4"
            if src.exists():
                if dst.exists() and src != dst:
                    skipped.append(src.name)
                elif src != dst:
                    if dry_run:
                        renamed.append(f"{src.name} → {dst.name}")
                    else:
                        try:
                            src.rename(dst)
                            renamed.append(f"{src.name} → {dst.name}")
                        except Exception as e:
                            errors.append(f"{src.name}: {e}")

        # Frame cache files (_last / _first thumbnails)
        if frames_dir.exists():
            for suffix in ("_last.jpg", "_first.jpg", "_last.png", "_first.png"):
                fsrc = frames_dir / f"{old_stem}{suffix}"
                fdst = frames_dir / f"{new_stem}{suffix}"
                if fsrc.exists() and fsrc != fdst:
                    if fdst.exists():
                        skipped.append(fsrc.name)
                    elif dry_run:
                        renamed.append(f"{fsrc.name} → {fdst.name}")
                    else:
                        try:
                            fsrc.rename(fdst)
                            renamed.append(f"{fsrc.name} → {fdst.name}")
                        except Exception as e:
                            errors.append(f"{fsrc.name}: {e}")

    return {"renamed": renamed, "skipped": skipped, "errors": errors, "dry_run": dry_run}
