# -*- coding: utf-8 -*-
"""
API router for the continuity audit (LF-poprzednika vs plik diff report —
see project_continuity_golden_rule memory).

Endpoints:
    POST /api/continuity-audit/start   — queue an audit job for a RUN's flow
    GET  /api/continuity-audit/status  — current job status + results
    POST /api/continuity-audit/cancel  — cancel running job

Image results are served via the existing generic /api/fs/image?path=
endpoint (lf_path / file_path in each result are already absolute paths).
"""

from fastapi import APIRouter, HTTPException, Request

from app.services.continuity_audit_service import (
    start_audit, get_audit_status, cancel_audit, recompute_entry, set_accepted,
)

router = APIRouter(prefix="/api/continuity-audit", tags=["continuity-audit"])


@router.post("/start")
async def continuity_audit_start(request: Request):
    """Body JSON: {"run": "RUN_xxx.yaml", "force": false}
    force=True bypasses the per-seam results cache (see
    continuity_audit_service._try_cache_hit) and recomputes every candidate
    from scratch — the "🔁 Przelicz ręcznie" button. Default False is the
    fast path used both by the auto-refresh-on-open and the normal "▶
    Uruchom audyt" button: skips any seam whose source clips' mtimes match
    the last computed pass."""
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        force = bool(body.get("force", False))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    if not run:
        raise HTTPException(status_code=422, detail="run is required")

    result = start_audit(run, force)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/status")
async def continuity_audit_status():
    """Return the current audit job status (progress while running, results when done)."""
    return get_audit_status()


@router.post("/cancel")
async def continuity_audit_cancel():
    """Cancel the running audit job."""
    return cancel_audit()


@router.post("/recompute")
async def continuity_audit_recompute(request: Request):
    """Re-check a single row after the underlying clip was fixed (trim/color-
    grade) — re-extracts LF/FF and re-diffs, without re-running the whole
    audit. Body JSON: {"run": "RUN_xxx.yaml", "chain_idx": 78, "row_id": "golenie_3a::ext"}
    row_id picks which row when a chain has several (one external + one per
    internal step seam, see project_continuity_audit_tool 2026-09-09)."""
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        chain_idx = int(body.get("chain_idx"))
        row_id = str(body.get("row_id", ""))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body (need run, chain_idx, row_id)")

    if not run or not row_id:
        raise HTTPException(status_code=422, detail="run and row_id are required")

    result = await recompute_entry(run, chain_idx, row_id)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/accept")
async def continuity_audit_accept(request: Request):
    """Manually mark a row accepted/un-accepted (persisted, survives re-runs
    of the audit). Body JSON: {"run": "RUN_xxx.yaml", "row_id": "golenie_3a::ext", "accepted": true}"""
    try:
        body = await request.json()
        run = str(body.get("run", ""))
        row_id = str(body.get("row_id", ""))
        accepted = bool(body.get("accepted", True))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body (need run, row_id, accepted)")

    if not run or not row_id:
        raise HTTPException(status_code=422, detail="run and row_id are required")

    result = set_accepted(run, row_id, accepted)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
