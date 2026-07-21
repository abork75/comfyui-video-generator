# -*- coding: utf-8 -*-
"""
API router for RUN file operations.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request  # noqa: F401 (Request used in put_flow)
from app.services.run_file_service import (
    RUNS_FOLDER,
    scan_runs_folder, get_run_details, get_run_content, get_run_flow,
    invalidate_run_info_cache,
)
from app.services.media_service import get_transition_status, get_post_clips, invalidate_run_cache, create_numbered_flow
from app.services.yaml_service import save_yaml_flow, get_yaml_globals, save_yaml_globals, create_run_from_globals
from pydantic import BaseModel

router = APIRouter(prefix="/api/runs", tags=["runs"])


class CloneRunRequest(BaseModel):
    new_name: str
    source_filename: str | None = None   # YAML run to copy globals from (None = blank defaults)


@router.post("/clone")
async def clone_run(body: CloneRunRequest):
    """
    Create a new RUN_*.yaml by copying globals (project_folder, defaults,
    linux_backend) from RUNS/TEMPLATE.yaml and leaving flow empty.
    Also generates a companion .py file.
    Returns: {"ok": true, "filename": "RUN_XXX.yaml"}
    """
    # Always use TEMPLATE.yaml as the source of defaults
    template_yaml = RUNS_FOLDER / "TEMPLATE.yaml"
    source_yaml = template_yaml if template_yaml.exists() else None

    try:
        out_path = create_run_from_globals(
            new_name=body.new_name,
            out_dir=RUNS_FOLDER,
            source_yaml=source_yaml,
        )
    except FileExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Generate companion .py
    py_error = None
    try:
        from app.services.yaml_service import generate_py_from_yaml
        generate_py_from_yaml(out_path)
    except Exception as exc:
        py_error = str(exc)

    invalidate_run_info_cache()
    return {"ok": True, "filename": out_path.name, "py_error": py_error}


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


@router.get("/{filename}/status")
async def get_run_status(filename: str):
    """Get transition file existence status for every FLOW item."""
    data = get_transition_status(filename)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Cannot resolve status for: {filename}")
    return data


@router.get("/{filename}/postclips")
async def get_run_postclips(filename: str):
    """Ordered list of all playable mp4 clips for the post-processing view."""
    data = get_post_clips(filename)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Cannot resolve post clips for: {filename}")
    return data


@router.get("/{filename}/source")
async def get_run_source(filename: str):
    """Get raw source code of a RUN file."""
    content = get_run_content(filename)
    if content is None:
        raise HTTPException(status_code=404, detail=f"RUN file not found: {filename}")
    return {"filename": filename, "content": content}


@router.post("/{filename}/migrate-to-yaml")
async def migrate_to_yaml(filename: str):
    """
    Migrate a RUN_*.py file to a RUN_*.yaml file.
    Writes RUN_*.yaml next to the .py (does NOT delete the original .py).
    Returns the name of the created .yaml file.
    """
    if not filename.endswith(".py"):
        raise HTTPException(status_code=422, detail="Source file must be a .py file")
    py_path = RUNS_FOLDER / filename
    if not py_path.exists() or not py_path.name.startswith("RUN_"):
        raise HTTPException(status_code=404, detail=f"RUN file not found: {filename}")

    from app.services.yaml_service import migrate_py_to_yaml
    try:
        out = migrate_py_to_yaml(py_path)
        # Invalidate caches: the new .yaml must be picked up on next scan
        invalidate_run_info_cache()
        return {"ok": True, "yaml_filename": out.name}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/{filename}/reformat-yaml")
async def reformat_yaml_file(filename: str):
    """
    Re-parse and re-write a RUN_*.yaml with the current pretty formatter.
    Useful after formatter improvements — same data, nicer output.
    """
    if not filename.endswith(".yaml"):
        raise HTTPException(status_code=422, detail="Source file must be a .yaml file")
    yaml_path = RUNS_FOLDER / filename
    if not yaml_path.exists() or not yaml_path.name.startswith("RUN_"):
        raise HTTPException(status_code=404, detail=f"RUN YAML file not found: {filename}")

    from app.services.yaml_service import reformat_yaml
    try:
        reformat_yaml(yaml_path)
        # Invalidate caches so the fresh content is picked up
        invalidate_run_info_cache(filename)
        return {"ok": True, "filename": filename}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/{filename}/generate-py")
async def generate_py(filename: str):
    """
    (Re-)generate a RUN_*.py from a RUN_*.yaml file.
    Overwrites the .py if it already exists.
    Returns the name of the written .py file.
    """
    if not filename.endswith(".yaml"):
        raise HTTPException(status_code=422, detail="Source file must be a .yaml file")
    yaml_path = RUNS_FOLDER / filename
    if not yaml_path.exists() or not yaml_path.name.startswith("RUN_"):
        raise HTTPException(status_code=404, detail=f"RUN YAML file not found: {filename}")

    from app.services.yaml_service import generate_py_from_yaml
    try:
        out = generate_py_from_yaml(yaml_path)
        # Invalidate caches: the (re-)generated .py might have changed
        invalidate_run_info_cache(out.name)
        invalidate_run_cache(out.name)
        return {"ok": True, "py_filename": out.name}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{filename}/project-files")
async def get_project_files(filename: str):
    """
    List image/video files in the project_folder of this RUN.
    Returns: {"files": [...], "folder": "..."}
    """
    info = get_run_details(filename)
    if info is None:
        raise HTTPException(status_code=404, detail=f"RUN file not found: {filename}")

    folder = info.get("project_folder")
    if not folder:
        raise HTTPException(status_code=422, detail="project_folder not configured in this RUN")

    from pathlib import Path as _Path
    project_path = _Path(folder)
    if not project_path.exists():
        raise HTTPException(status_code=404, detail=f"Project folder does not exist: {folder}")

    _IMG_VIDEO = {
        ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif",
        ".mp4", ".avi", ".mov", ".mkv", ".webm",
        ".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a",
    }
    files = sorted(
        f.name for f in project_path.iterdir()
        if f.is_file() and f.suffix.lower() in _IMG_VIDEO
    )
    return {"files": files, "folder": str(project_path)}


@router.get("/{filename}/globals")
async def get_globals(filename: str):
    """
    Get non-flow sections of a YAML RUN file for the settings editor.
    Returns: project_folder, use_test_flow, defaults{}, linux_backend{}
    """
    if not filename.endswith(".yaml"):
        raise HTTPException(status_code=422, detail="Only YAML files have editable globals")
    yaml_path = RUNS_FOLDER / filename
    if not yaml_path.exists() or not yaml_path.name.startswith("RUN_"):
        raise HTTPException(status_code=404, detail=f"YAML file not found: {filename}")
    data = get_yaml_globals(yaml_path)
    if data is None:
        raise HTTPException(status_code=400, detail="Failed to parse YAML file")
    return data


@router.put("/{filename}/globals")
async def put_globals(filename: str, request: Request):
    """
    Update non-flow sections of a YAML RUN file.
    Body JSON: {"project_folder": "...", "defaults": {...}, "linux_backend": {...}, "use_test_flow": bool}
    Also auto-regenerates the companion .py file.
    """
    if not filename.endswith(".yaml"):
        raise HTTPException(status_code=422, detail="Only YAML files can be edited via the GUI")
    yaml_path = RUNS_FOLDER / filename
    if not yaml_path.exists() or not yaml_path.name.startswith("RUN_"):
        raise HTTPException(status_code=404, detail=f"YAML file not found: {filename}")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    try:
        save_yaml_globals(yaml_path, body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    py_error = None
    try:
        from app.services.yaml_service import generate_py_from_yaml
        out = generate_py_from_yaml(yaml_path)
        invalidate_run_info_cache(out.name)
        invalidate_run_cache(out.name)
    except Exception as exc:
        py_error = str(exc)

    invalidate_run_info_cache(filename)
    invalidate_run_cache(filename)   # bust project_folder path cache after globals change
    return {"ok": True, "py_error": py_error}


@router.patch("/{filename}/globals/pre-target")
async def patch_pre_target(filename: str, request: Request):
    """
    Persist pre-processing target resolution (pre_target_w, pre_target_h) to YAML defaults.
    Body: { "pre_target_w": 1920, "pre_target_h": 1080 }
    """
    import yaml as _yaml
    if not filename.endswith(".yaml"):
        raise HTTPException(status_code=422, detail="Only YAML files supported")
    yaml_path = RUNS_FOLDER / filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Not found: {filename}")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    w = body.get("pre_target_w")
    h = body.get("pre_target_h")
    if not isinstance(w, int) or not isinstance(h, int):
        raise HTTPException(status_code=400, detail="pre_target_w and pre_target_h must be integers")
    data = get_yaml_globals(yaml_path)
    if data is None:
        raise HTTPException(status_code=400, detail="Cannot parse YAML")
    data["defaults"]["pre_target_w"] = w
    data["defaults"]["pre_target_h"] = h
    save_yaml_globals(yaml_path, data)
    return {"ok": True}


@router.put("/{filename}/flow")
async def put_flow(filename: str, request: Request):
    """
    Save an updated FLOW list back to a RUN_*.yaml file.
    Body JSON: {"flow": [...internal items...], "flow_key": "flow"|"flow_test"}
    The flow is converted back to YAML format and the file is rewritten.
    Also auto-regenerates the companion .py file.
    """
    if not filename.endswith(".yaml"):
        raise HTTPException(status_code=422, detail="Only YAML files can be edited via the GUI")
    yaml_path = RUNS_FOLDER / filename
    if not yaml_path.exists() or not yaml_path.name.startswith("RUN_"):
        raise HTTPException(status_code=404, detail=f"YAML file not found: {filename}")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON body")

    new_flow = body.get("flow")
    flow_key = body.get("flow_key", "flow")
    if not isinstance(new_flow, list):
        raise HTTPException(status_code=422, detail="'flow' must be a list")
    if flow_key not in ("flow", "flow_test"):
        raise HTTPException(status_code=422, detail="flow_key must be 'flow' or 'flow_test'")

    try:
        save_yaml_flow(yaml_path, new_flow, flow_key)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Auto-regenerate .py so it stays in sync
    py_error = None
    try:
        from app.services.yaml_service import generate_py_from_yaml
        out = generate_py_from_yaml(yaml_path)
        invalidate_run_info_cache(out.name)
        invalidate_run_cache(out.name)
    except Exception as exc:
        py_error = str(exc)

    invalidate_run_info_cache(filename)
    invalidate_run_cache(filename)
    return {"ok": True, "flow_key": flow_key, "py_error": py_error}


@router.post("/{filename}/create-flow")
async def create_flow_folder(filename: str):
    """
    Create a numbered FLOW folder in final_outputs/.
    Copies all clips in flow order: 0001_clip.mp4, 0002_transition.mp4, ...
    Returns: {ok, folder, path, copied, missing, error}
    """
    import asyncio
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, create_numbered_flow, filename)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
