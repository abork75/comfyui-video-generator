# -*- coding: utf-8 -*-
"""
API router for RUN file operations.
"""

from fastapi import APIRouter, HTTPException
from app.services.run_file_service import scan_runs_folder, get_run_details, get_run_content, get_run_flow

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.get("")
async def list_runs():
    """List all RUN_*.py files in RUNS/ (top level only)."""
    return scan_runs_folder()


@router.get("/{filename}")
async def get_run(filename: str):
    """Get parsed details of a single RUN file."""
    info = get_run_details(filename)
    if info is None:
        raise HTTPException(status_code=404, detail=f"RUN file not found: {filename}")
    return info


@router.get("/{filename}/flow")
async def get_flow(filename: str):
    """Get parsed FLOW list from a RUN file."""
    data = get_run_flow(filename)
    if data is None:
        raise HTTPException(status_code=404, detail=f"FLOW not found in: {filename}")
    return data


@router.get("/{filename}/source")
async def get_run_source(filename: str):
    """Get raw source code of a RUN file."""
    content = get_run_content(filename)
    if content is None:
        raise HTTPException(status_code=404, detail=f"RUN file not found: {filename}")
    return {"filename": filename, "content": content}
