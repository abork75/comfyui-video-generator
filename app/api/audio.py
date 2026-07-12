# -*- coding: utf-8 -*-
"""
API router for MMAudio — add/regenerate audio for an existing transition video.

POST /api/audio/{run_filename}
  body: { "name": "transition.mp4", "audio_prompt"?: "...", "audio_negative_prompt"?: "..." }
  Runs MMAudio in background; progress appears in log panel via WebSocket.
"""

import asyncio
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request

from app.services.app_config_service import get_backend as cfg_get_backend
from app.services.process_service import process_service
from app.services.yaml_service import get_yaml_globals

PROJECT_ROOT = Path(__file__).parent.parent.parent
RUNS_FOLDER  = PROJECT_ROOT / "RUNS"

_FALLBACK_AUDIO_PROMPT    = "foley sound effects, physical environment sounds, footsteps, cloth movement, objects, wind bursts, creaking, synchronized with video, crisp, realistic, high quality"
_FALLBACK_AUDIO_NEG_PROMPT = "music, melody, instruments, singing, ambient drone, sustained atmosphere, continuous background noise, reverb heavy, low quality, distortion"

router = APIRouter(prefix="/api/audio", tags=["audio"])


class _LogBridge:
    """Forward logger calls to the WebSocket log panel."""
    def info(self, msg):    process_service.log_sys(f"ℹ️  {msg}")
    def success(self, msg): process_service.log_sys(f"✅ {msg}")
    def warning(self, msg): process_service.log_sys(f"⚠️  {msg}")
    def error(self, msg):   process_service.log_sys(f"❌ {msg}")


async def _run_audio_bg(
    video_path: Path,
    prompt: str,
    negative_prompt: str,
    api_url: str,
    duration: float,
) -> None:
    from utils.mmaudio_utils import add_audio as _add_audio
    logger = _LogBridge()
    logger.info(f"MMAudio re-generacja: {video_path.name}")
    loop = asyncio.get_running_loop()
    ok = await loop.run_in_executor(None, lambda: _add_audio(
        video_path=video_path,
        prompt=prompt,
        negative_prompt=negative_prompt,
        api_url=api_url,
        duration=duration,
        steps=25,
        cfg=4.5,
        seed=-1,
        logger=logger,
    ))
    if not ok:
        process_service.log_sys(f"⚠️  MMAudio: nie dodano audio do {video_path.name}")
    else:
        process_service.log_sys(f"[AUDIO_READY] {video_path.name}")


@router.post("/{run_filename}")
async def add_audio_to_clip(run_filename: str, request: Request):
    """
    Regenerate audio for an already-generated transition video using MMAudio.
    Runs in background — progress streamed to log panel via WebSocket.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    name: str = (body.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Brak parametru 'name'")

    yaml_path = RUNS_FOLDER / run_filename
    if not yaml_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik nie istnieje: {run_filename}")

    globals_data = get_yaml_globals(yaml_path)
    if not globals_data:
        raise HTTPException(status_code=400, detail="Nie można odczytać YAML")

    project_folder = Path(globals_data.get("project_folder") or "")
    if not project_folder or not project_folder.exists():
        raise HTTPException(status_code=400, detail=f"Folder projektu nie istnieje: {project_folder}")

    video_path = project_folder / "transitions" / name
    if not video_path.exists():
        video_path = project_folder / "transitions" / "chains" / name
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Plik wideo nie istnieje: {name}")

    # Audio prompts: request body → YAML defaults → system fallback
    defs = globals_data.get("defaults") or {}
    audio_prompt = (
        body.get("audio_prompt")
        or defs.get("default_audio_prompt")
        or _FALLBACK_AUDIO_PROMPT
    )
    audio_negative_prompt = (
        body.get("audio_negative_prompt")
        or defs.get("default_audio_negative_prompt")
        or _FALLBACK_AUDIO_NEG_PROMPT
    )

    # api_url: YAML linux_backend → app_config
    lb = globals_data.get("linux_backend") or {}
    api_url = lb.get("api_url") or cfg_get_backend("linux").get("api_url", "http://127.0.0.1:8189")

    # Video duration via ffprobe/OpenCV
    try:
        from utils.video_utils import get_video_info
        info = get_video_info(video_path)
        duration = float(info["duration"]) if info.get("duration") and info["duration"] > 0 else 10.0
    except Exception:
        duration = 10.0

    asyncio.create_task(_run_audio_bg(video_path, audio_prompt, audio_negative_prompt, api_url, duration))
    return {"ok": True}
