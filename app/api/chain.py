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
    Rename chain output files when chain_prefix changes.

    Body JSON:
    {
        "run_filename": "RUN_001.yaml",
        "old_prefix":   "ewelina_stands",
        "new_prefix":   "ewelina_sits"
    }

    Returns:
    {
        "renamed": ["ewelina_stands_001.mp4", ...],
        "skipped": [],
        "errors":  []
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
        return {"renamed": [], "skipped": [], "errors": []}

    pf = _project_folder(run_filename)
    if pf is None:
        raise HTTPException(status_code=404, detail=f"Project folder not found for: {run_filename}")

    chains_dir = pf / "transitions" / "chains"
    dry_run = bool(body.get("dry_run", False))
    renamed, skipped, errors = [], [], []

    if chains_dir.exists():
        for src in sorted(chains_dir.iterdir()):
            if not src.is_file():
                continue
            name = src.name
            if name.startswith(old_prefix + "_") and name.endswith(".mp4"):
                suffix = name[len(old_prefix):]   # e.g. "_001.mp4"
                dst = chains_dir / (new_prefix + suffix)
                if dst.exists():
                    skipped.append(name)
                    continue
                if dry_run:
                    renamed.append(name)
                else:
                    try:
                        src.rename(dst)
                        renamed.append(name)
                    except Exception as e:
                        errors.append(f"{name}: {e}")

    return {"renamed": renamed, "skipped": skipped, "errors": errors, "dry_run": dry_run}


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
