# -*- coding: utf-8 -*-
"""
Filesystem browser API — used by the Pic Studio for directory/image picking.

Endpoints
─────────
GET /api/fs/browse?path=…   → {path, parent, dirs, images}
GET /api/fs/image?path=…    → serve any local image file (authenticated)
"""

from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, Response

router = APIRouter(prefix="/api/fs", tags=["fs"])

_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}


@router.get("/browse")
async def browse(path: str = Query(..., description="Absolute local path to browse")):
    """
    Return directory contents split into sub-directories and image files.
    Entries are sorted: dirs first (alphabetical), then images (alphabetical).
    """
    p = Path(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Ścieżka nie istnieje: {path}")
    if not p.is_dir():
        raise HTTPException(status_code=400, detail=f"Ścieżka nie jest katalogiem: {path}")

    try:
        entries = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        dirs = [
            {"name": e.name, "path": str(e)}
            for e in entries
            if e.is_dir() and not e.name.startswith(".")
        ]
        images = [
            {"name": e.name, "path": str(e)}
            for e in entries
            if e.is_file() and e.suffix.lower() in _IMAGE_EXTS
        ]
        parent = str(p.parent) if p.parent != p else None
        return {"path": str(p), "parent": parent, "dirs": dirs, "images": images}
    except PermissionError:
        raise HTTPException(status_code=403, detail="Brak uprawnień do odczytu katalogu")


@router.post("/mkdir")
async def mkdir(path: str = Query(..., description="Parent directory path"),
                name: str = Query(..., description="New folder name")):
    """Create a new subdirectory inside `path`."""
    parent = Path(path)
    if not parent.exists() or not parent.is_dir():
        raise HTTPException(status_code=404, detail=f"Katalog nadrzędny nie istnieje: {path}")
    # Sanitize name — no path separators, no dots leading
    safe_name = name.strip().replace("/", "").replace("\\", "").lstrip(".")
    if not safe_name:
        raise HTTPException(status_code=400, detail="Nieprawidłowa nazwa katalogu")
    new_dir = parent / safe_name
    if new_dir.exists():
        raise HTTPException(status_code=409, detail=f"Katalog już istnieje: {safe_name}")
    try:
        new_dir.mkdir(parents=False, exist_ok=False)
        return {"ok": True, "path": str(new_dir)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/image")
async def serve_image(path: str = Query(..., description="Absolute local path to image")):
    """Serve any local image file. Protected by the global auth middleware."""
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise HTTPException(status_code=404, detail="Plik nie istnieje")
    if p.suffix.lower() not in _IMAGE_EXTS:
        raise HTTPException(status_code=400, detail="Nieobsługiwany format pliku")
    return FileResponse(str(p), headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@router.get("/image_in_dirs")
async def serve_image_in_dirs(
    name: str = Query(..., description="Image filename"),
    dirs: List[str] = Query(..., description="Directories to search in order"),
):
    """Find image by filename across multiple directories and serve the first match."""
    for d in dirs:
        if not d:
            continue
        p = Path(d) / name
        if p.exists() and p.is_file() and p.suffix.lower() in _IMAGE_EXTS:
            return FileResponse(str(p), headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    raise HTTPException(status_code=404, detail=f"Plik '{name}' nie znaleziony w podanych katalogach")
