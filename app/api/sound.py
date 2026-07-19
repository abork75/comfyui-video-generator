# -*- coding: utf-8 -*-
"""
Sound API — audio loop builder.

GET  /api/sound/files          — list MP3s from source folder
POST /api/sound/loop           — build looped audio to target duration
GET  /api/sound/results        — list files in output folder
DELETE /api/sound/results/{filename} — delete a result file
"""

import json
import math
import subprocess
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/sound", tags=["sound"])

SRC_DIR = Path(r"D:\audio\podklady")
OUT_DIR = Path(r"D:\audio\podklady\robocze")

CROSSFADE_CURVES = ["tri", "exp", "nofade", "log", "ipar", "qsin"]


def _ensure_dirs():
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def _get_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, timeout=15,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {r.stderr.decode()}")
    return float(json.loads(r.stdout)["format"]["duration"])


@router.get("/files")
async def list_files():
    _ensure_dirs()
    exts = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
    files = sorted(
        ({"name": p.name, "size_kb": round(p.stat().st_size / 1024)}
         for p in SRC_DIR.iterdir()
         if p.suffix.lower() in exts and p.parent == SRC_DIR),
        key=lambda x: x["name"])
    return {"files": files}


@router.get("/results")
async def list_results():
    _ensure_dirs()
    exts = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
    files = sorted(
        ({"name": p.name, "size_kb": round(p.stat().st_size / 1024)}
         for p in OUT_DIR.iterdir()
         if p.suffix.lower() in exts),
        key=lambda x: x["name"])
    return {"files": files}


@router.get("/play/{filename}")
async def play_result(filename: str):
    p = OUT_DIR / filename
    if not p.exists():
        # also check source dir
        p = SRC_DIR / filename
    if not p.exists():
        raise HTTPException(404, "Plik nie znaleziony")
    return FileResponse(str(p), media_type="audio/mpeg")


@router.delete("/results/{filename}")
async def delete_result(filename: str):
    p = OUT_DIR / filename
    if not p.exists():
        raise HTTPException(404, "Plik nie istnieje")
    p.unlink()
    return {"ok": True}


class LoopRequest(BaseModel):
    filename: str
    duration: float       # target duration in seconds
    crossfade: float = 0.3
    curve: str = "tri"


@router.post("/loop")
async def build_loop(req: LoopRequest):
    _ensure_dirs()

    if req.curve not in CROSSFADE_CURVES:
        raise HTTPException(400, f"Nieznana krzywa: {req.curve}")
    if req.duration < 1 or req.duration > 3600:
        raise HTTPException(400, "Długość musi być między 1 a 3600s")

    src = SRC_DIR / req.filename
    if not src.exists():
        raise HTTPException(404, f"Plik nie znaleziony: {req.filename}")

    try:
        src_dur = _get_duration(src)
    except Exception as e:
        raise HTTPException(500, f"Błąd odczytu pliku: {e}")

    if req.crossfade >= src_dur:
        raise HTTPException(400, f"Crossfade ({req.crossfade}s) >= długość pliku ({src_dur:.2f}s)")

    # How many copies needed:
    # total = n * src_dur - (n-1) * crossfade = n*(src_dur - crossfade) + crossfade
    # n = ceil((target - crossfade) / (src_dur - crossfade))
    step = src_dur - req.crossfade
    n = max(2, math.ceil((req.duration - req.crossfade) / step))

    # Build output filename
    stem = src.stem
    ts   = datetime.now().strftime("%H%M%S")
    cf_s = str(req.crossfade).replace(".", "_")
    out_name = f"{stem}_{int(req.duration)}s_cf{cf_s}_{req.curve}_{ts}.mp3"
    out_path = OUT_DIR / out_name

    # Build ffmpeg filter_complex dynamically
    inputs = []
    for _ in range(n):
        inputs += ["-i", str(src)]

    if n == 1:
        # Edge case: single copy, just trim
        filter_str = f"[0]atrim=end={req.duration},asetpts=PTS-STARTPTS[out]"
    else:
        parts = []
        for i in range(n - 1):
            a = f"[s{i}]" if i > 0 else f"[{i}]"
            b = f"[{i + 1}]"
            out_label = f"[s{i + 1}]"
            parts.append(f"{a}{b}acrossfade=d={req.crossfade}:c1={req.curve}:c2={req.curve}{out_label}")
        last = f"[s{n - 1}]"
        parts.append(f"{last}atrim=end={req.duration},asetpts=PTS-STARTPTS[out]")
        filter_str = ";".join(parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-q:a", "2",
        str(out_path),
    ]

    try:
        r = subprocess.run(cmd, capture_output=True, timeout=300)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.decode())
    except Exception as e:
        if out_path.exists():
            out_path.unlink()
        raise HTTPException(500, f"ffmpeg error: {e}")

    return {
        "ok": True,
        "filename": out_name,
        "copies": n,
        "actual_duration": req.duration,
    }
