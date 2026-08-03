# -*- coding: utf-8 -*-
"""
Talk-transition service — generates I2V2I bridge clips for a talk tile:
  • prev_clip → talk_01  (only if a previous clip exists in the same scene)
  • talk_01  → talk_02   (between every adjacent segment pair)
  • talk_02  → talk_03   …

One ⇌ button generates all junctions sequentially.
Output: transitions/talks/{stem}_transition.mp4, {stem}_01_02_transition.mp4 …
"""

import asyncio
import sys
import time
from pathlib import Path

from app.services.media_service import _project_folder, talk_path
from app.services.run_file_service import get_run_flow, get_run_details


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":          "idle",   # idle | queued | running | done | error
    "run_filename":    None,
    "transition_name": None,     # currently generating
    "progress":        None,     # e.g. "1/3"
    "error":           None,
    "started_at":      None,
    "elapsed_s":       None,
}

_task: asyncio.Task | None = None


def get_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("queued", "running"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":          "idle",
        "run_filename":    None,
        "transition_name": None,
        "progress":        None,
        "error":           None,
        "started_at":      None,
        "elapsed_s":       None,
    })


def cancel() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_prev_clip(flow: list, talk_index: int) -> str | None:
    """Scan backwards within the same scene (stops at break) for preceding video."""
    for i in range(talk_index - 1, -1, -1):
        item = flow[i]
        if not isinstance(item, dict):
            continue
        if item.get("break") or item.get("type") == "scene_break":
            break
        if item.get("chain") and item.get("chain_prefix") and item.get("chain"):
            n = str(len(item["chain"])).zfill(3)
            return f"transitions/chains/{item['chain_prefix']}_{n}.mp4"
        if item.get("type") == "multitalk":
            name = (item.get("name") or "").strip()
            if name:
                return f"transitions/multitalk/{name if name.endswith('.mp4') else name + '.mp4'}"
        if item.get("file"):
            return item["file"]
    return None


def _find_segments(pf: Path, talk_item: dict) -> list[Path]:
    """Return existing segment files for this talk tile (in order)."""
    base = talk_path(pf, talk_item)
    # Multi-segment: look for _01, _02 …
    segs = []
    i = 1
    while True:
        s = base.parent / f"{base.stem}_{i:02d}.mp4"
        if s.exists():
            segs.append(s)
            i += 1
        else:
            break
    if segs:
        return segs
    # Single-segment fallback
    if base.exists():
        return [base]
    return []


def _get_last_frame(pf: Path, clip_file: str, w: int, h: int) -> Path | None:
    stem = Path(clip_file).stem
    for candidate in (
        pf / "frames" / f"{stem}_real.png",
        pf / "frames" / f"{stem}_end.png",
        pf / "frames" / f"{stem}_end.jpg",
    ):
        if candidate.exists():
            return candidate
    src = pf / clip_file
    if src.exists():
        try:
            from utils.frame_extractor import FrameExtractor
            return FrameExtractor(project_folder=pf).extract_end_frame(clip_file, w, h)
        except Exception:
            pass
    return None


def _get_last_frame_of_video(pf: Path, video: Path, w: int, h: int) -> Path | None:
    stem = video.stem
    for candidate in (
        pf / "frames" / f"{stem}_real.png",
        pf / "frames" / f"{stem}_end.png",
        pf / "frames" / f"{stem}_end.jpg",
    ):
        if candidate.exists():
            return candidate
    if video.exists():
        try:
            rel = str(video.relative_to(pf))
            from utils.frame_extractor import FrameExtractor
            return FrameExtractor(project_folder=pf).extract_end_frame(rel, w, h)
        except Exception:
            pass
    return None


def _get_first_frame_of_video(pf: Path, video: Path, w: int, h: int) -> Path | None:
    stem = video.stem
    for candidate in (
        pf / "frames" / f"{stem}_start.png",
        pf / "frames" / f"{stem}_start.jpg",
    ):
        if candidate.exists():
            return candidate
    if video.exists():
        try:
            rel = str(video.relative_to(pf))
            from utils.frame_extractor import FrameExtractor
            return FrameExtractor(project_folder=pf).extract_start_frame(rel, w, h)
        except Exception:
            pass
    return None


def _init_backend():
    from app.services import app_config_service
    cfg = dict(app_config_service.get_backend("linux"))
    cfg.update(app_config_service.get_model("linux", "video_gen"))
    from backends.linux_backend import LinuxBackend
    return LinuxBackend(cfg)


def _logsys(msg: str) -> None:
    try:
        from app.services.process_service import process_service
        process_service.log_sys(msg)
    except Exception:
        print(msg)


# ── Public entry point ────────────────────────────────────────────────────────

def start_talk_transition(run_filename: str, talk_item: dict, flow_index: int) -> dict:
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Tranzycja jest już generowana"}

    try:
        from app.services.process_service import process_service
        if process_service.get_status()["status"] == "running":
            return {"ok": False, "error": "Generacja batch w toku — poczekaj"}
    except Exception:
        pass

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono project_folder: {run_filename}"}

    flow_data = get_run_flow(run_filename)
    if not flow_data:
        return {"ok": False, "error": "Nie można wczytać flow"}
    flow = flow_data["flow"]

    segments = _find_segments(pf, talk_item)
    if not segments:
        return {"ok": False, "error": "Talk nie wygenerowany — brak plików segmentów"}

    prev_clip = _get_prev_clip(flow, flow_index)

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run(
                run_filename=run_filename,
                pf=pf,
                flow=flow,
                segments=segments,
                prev_clip=prev_clip,
                talk_item=talk_item,
            )
        )
    except RuntimeError as exc:
        _state.update({"status": "error", "error": str(exc)})
        return {"ok": False, "error": str(exc)}

    n_transitions = len(segments) - 1 + (1 if prev_clip else 0)
    return {"ok": True, "count": n_transitions}


# ── Background task ───────────────────────────────────────────────────────────

async def _run(
    run_filename: str,
    pf: Path,
    flow: list,
    segments: list[Path],
    prev_clip: str | None,
    talk_item: dict,
) -> None:
    from app.services import app_config_service

    loop = asyncio.get_running_loop()

    try:
        run_details = get_run_details(run_filename) or {}
        defaults    = app_config_service.get_defaults()
        proj_defs   = run_details.get("defaults") or {}
        if proj_defs:
            defaults = {**defaults, **{k: v for k, v in proj_defs.items() if v is not None}}

        # Resolution from talk tile > project > fallback
        _tile_w = talk_item.get("width")
        _tile_h = talk_item.get("height")
        if _tile_w and _tile_h:
            target_w = (int(_tile_w) // 16) * 16 or 480
            target_h = (int(_tile_h) // 16) * 16 or 832
        else:
            proj_res = run_details.get("force_resolution") or run_details.get("default_resolution")
            if proj_res:
                target_w = (int(proj_res[0]) // 16) * 16 or 480
                target_h = (int(proj_res[1]) // 16) * 16 or 832
            else:
                target_w, target_h = 480, 832

        _steps = None  # talk uses Lightning-equivalent workflow; step count from workflow JSON
        _proj_auto = proj_defs.get("auto_blocks_to_swap")
        _is_auto   = _proj_auto if _proj_auto is not None else defaults.get("auto_blocks_to_swap", True)
        if _is_auto:
            from backends.base_backend import _auto_blocks_to_swap as _calc_bts
            _bts = _calc_bts(target_w, target_h)
        else:
            _bts = defaults.get("blocks_to_swap")

        base_stem = talk_path(pf, talk_item).stem

        # Build list of (start_video_or_clip, end_video, out_name)
        jobs: list[tuple] = []

        # prev_clip → seg[0]  (only within same scene)
        if prev_clip:
            jobs.append(("prev", prev_clip, segments[0], f"{base_stem}_transition.mp4"))

        # seg[i] → seg[i+1]
        for i in range(len(segments) - 1):
            jobs.append(("seg", segments[i], segments[i + 1],
                         f"{base_stem}_{i+1:02d}_{i+2:02d}_transition.mp4"))

        if not jobs:
            raise RuntimeError("Brak złączy do wygenerowania")

        _state["status"] = "running"
        backend = _init_backend()
        await loop.run_in_executor(None, backend.validate_requirements)

        for job_i, (kind, src, dst_video, out_name) in enumerate(jobs, 1):
            _state["progress"]        = f"{job_i}/{len(jobs)}"
            _state["transition_name"] = out_name
            out_path = pf / "transitions" / "talks" / out_name
            out_path.parent.mkdir(parents=True, exist_ok=True)

            # Resolve start frame
            if kind == "prev":
                start_frame = await loop.run_in_executor(
                    None, lambda s=src: _get_last_frame(pf, s, target_w, target_h)
                )
            else:
                start_frame = await loop.run_in_executor(
                    None, lambda s=src: _get_last_frame_of_video(pf, s, target_w, target_h)
                )

            # Resolve end frame (first frame of destination video)
            end_frame = await loop.run_in_executor(
                None, lambda d=dst_video: _get_first_frame_of_video(pf, d, target_w, target_h)
            )

            if not start_frame or not start_frame.exists():
                _logsys(f"  ⚠ Pominięto {out_name}: brak klatki startowej")
                continue
            if not end_frame or not end_frame.exists():
                _logsys(f"  ⚠ Pominięto {out_name}: brak klatki końcowej")
                continue

            _logsys(
                f"🔗 Tranzycja {job_i}/{len(jobs)}: {out_name}\n"
                f"   ▶ {start_frame.name} → {end_frame.name}"
            )

            success = await loop.run_in_executor(
                None,
                lambda sf=start_frame, ef=end_frame, op=out_path: backend.generate_transition(
                    start_frame=sf,
                    end_frame=ef,
                    output_path=op,
                    duration=1.0,
                    fps=16,
                    steps=_steps,
                    cfg=float(defaults.get("cfg", 2.0)),
                    seed=-1,
                    positive_prompt="Smooth cinematic transition, high quality, natural motion",
                    negative_prompt="",
                    width=target_w,
                    height=target_h,
                    blocks_to_swap=_bts,
                    frame_interpolation=False,
                    lora_name=None,
                    lora_strength=None,
                    lora_high=None,
                    lora_low=None,
                    audio_prompt="",
                    audio_negative_prompt="",
                ),
            )

            if success:
                _logsys(f"  ✅ {out_name}")
            else:
                _logsys(f"  ❌ Błąd generacji: {out_name}")

        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
        _logsys(f"✅ Wszystkie tranzycje talk gotowe ({elapsed}s)")

    except asyncio.CancelledError:
        _state.update({"status": "idle", "error": "Anulowano"})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})
        print(f"  ✗ Talk transition error: {exc}", file=sys.stderr)
