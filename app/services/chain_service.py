# -*- coding: utf-8 -*-
"""
Chain service — generates chain clip steps using the configured backend.

Analogous to talk_service.py but for chain tiles.

Flow:
  1. start_chain() validates inputs, reads flow, resolves frames, creates async task.
  2. _run_chain() iterates steps, calls backend.generate_transition() in executor.
  3. UI polls /api/chain/status (same pattern as /api/talk/status).
"""

import asyncio
import sys
import time
from pathlib import Path

from app.services.media_service import _project_folder
from app.services.run_file_service import get_run_flow


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":       "idle",   # idle | queued | running | done | error
    "run_filename": None,
    "chain_prefix": None,
    "step":         None,     # current step number (1-indexed)
    "total_steps":  None,
    "from_step":    None,     # first step being generated (1-indexed)
    "error":        None,
    "started_at":   None,
    "elapsed_s":    None,
}

_task: asyncio.Task | None = None


def get_chain_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("queued", "running"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":       "idle",
        "run_filename": None,
        "chain_prefix": None,
        "step":         None,
        "total_steps":  None,
        "from_step":    None,
        "error":        None,
        "started_at":   None,
        "elapsed_s":    None,
    })


def cancel_chain() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


# ── Public entry point ────────────────────────────────────────────────────────

def start_chain(run_filename: str, chain_prefix: str, from_step_0: int) -> dict:
    """
    Queue a chain generation job.

    Parameters
    ----------
    run_filename : str   RUN_*.yaml filename
    chain_prefix : str   chain_prefix field from YAML
    from_step_0  : int   0-indexed step to start from (UI's si value)
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Chain generacja jest już w toku"}

    # Guard: don't run alongside the main batch process
    try:
        from app.services.process_service import process_service
        if process_service.get_status()["status"] == "running":
            return {"ok": False, "error": "Generacja batch jest w toku — poczekaj lub anuluj"}
    except Exception:
        pass

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono project_folder: {run_filename}"}

    flow_data = get_run_flow(run_filename)
    if not flow_data:
        return {"ok": False, "error": "Nie można wczytać flow"}

    flow = flow_data["flow"]

    chain_idx, chain_item = _find_chain(flow, chain_prefix)
    if chain_item is None:
        return {"ok": False, "error": f"Nie znaleziono chain '{chain_prefix}'"}

    steps = chain_item.get("chain", [])
    if not steps:
        return {"ok": False, "error": "Chain nie ma żadnych stepów"}

    total_steps = len(steps)
    from_step = from_step_0 + 1  # convert to 1-indexed

    if not 1 <= from_step <= total_steps:
        return {"ok": False, "error": f"Nieprawidłowy krok: {from_step} (total: {total_steps})"}

    # When regenerating from step > 1, the previous step must still exist
    if from_step > 1:
        chains_dir = pf / "transitions" / "chains"
        prev_name = f"{chain_prefix}_{from_step - 1:03d}.mp4"
        if not (chains_dir / prev_name).exists():
            return {"ok": False,
                    "error": f"Poprzedni krok {prev_name} nie istnieje — zacznij od step 1"}

    preceding_file = _find_preceding_file(flow, chain_idx)
    end_target     = _find_end_target(flow, chain_idx)

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "chain_prefix": chain_prefix,
        "step":         from_step,
        "total_steps":  total_steps,
        "from_step":    from_step,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_chain(
                run_filename=run_filename,
                chain_prefix=chain_prefix,
                from_step=from_step,
                chain_item=chain_item,
                preceding_file=preceding_file,
                end_target=end_target,
                pf=pf,
            )
        )
    except RuntimeError as exc:
        _state.update({"status": "error", "error": str(exc)})
        return {"ok": False, "error": str(exc)}

    return {"ok": True}


# ── Internal helpers ──────────────────────────────────────────────────────────

def _find_chain(flow: list, chain_prefix: str) -> tuple[int, dict | None]:
    for i, item in enumerate(flow):
        if isinstance(item, dict) and item.get("chain_prefix") == chain_prefix and "chain" in item:
            return i, item
    return -1, None


def _find_preceding_file(flow: list, chain_idx: int) -> str | None:
    """Return the filename of the item that immediately precedes the chain."""
    for i in range(chain_idx - 1, -1, -1):
        item = flow[i]
        if not isinstance(item, dict):
            continue
        if item.get("break") or item.get("type") == "scene_break":
            return None
        if item.get("file"):
            return item["file"]
    return None


def _find_end_target(flow: list, chain_idx: int) -> str | None:
    """Return the first static-image filename after the chain (for last-step I2V2I)."""
    for i in range(chain_idx + 1, len(flow)):
        item = flow[i]
        if not isinstance(item, dict):
            if isinstance(item, str):
                return item
            continue
        if item.get("break") or item.get("type") == "scene_break":
            return None
        if "chain" in item or item.get("type") == "talk":
            return None
        if item.get("file"):
            return item["file"]
    return None


def _build_backend_config(chain_item: dict) -> dict:
    from app.services import app_config_service

    backend_name = chain_item.get("backend") or "linux"
    cfg = dict(app_config_service.get_backend(backend_name))

    # video_gen model provides config_path / workflows_path
    video_gen = app_config_service.get_model(backend_name, "video_gen")
    cfg.update(video_gen)

    if backend_name == "atlascloud":
        if chain_item.get("atlascloud_resolution"):
            cfg["atlascloud_resolution"] = chain_item["atlascloud_resolution"]
        if chain_item.get("atlascloud_prompt_extend") is not None:
            cfg["atlascloud_prompt_extend"] = chain_item["atlascloud_prompt_extend"]

    return cfg


def _init_backend(chain_item: dict):
    backend_name = chain_item.get("backend") or "linux"
    cfg = _build_backend_config(chain_item)

    if backend_name == "linux":
        from backends.linux_backend import LinuxBackend
        return LinuxBackend(cfg)
    elif backend_name == "local":
        from backends.local_backend import LocalBackend
        return LocalBackend(cfg)
    elif backend_name == "atlascloud":
        from backends.atlascloud_video_backend import AtlasCloudVideoBackend
        return AtlasCloudVideoBackend(cfg)
    else:
        from backends.linux_backend import LinuxBackend
        return LinuxBackend(cfg)


def _detect_resolution(pf: Path, flow: list) -> tuple[int, int]:
    try:
        from utils.frame_extractor import FrameExtractor

        non_virtual = [
            item["file"] for item in flow
            if isinstance(item, dict) and item.get("file")
        ]
        if not non_virtual:
            return 1024, 1024

        extractor = FrameExtractor(project_folder=pf)
        w, h = extractor.auto_detect_resolution(non_virtual)
        return (w // 16) * 16 or 1024, (h // 16) * 16 or 1024
    except Exception:
        return 1024, 1024


def _get_start_frame(
    pf: Path,
    chain_prefix: str,
    step: int,
    preceding_file: str | None,
    frame_cache: dict,
    target_w: int,
    target_h: int,
) -> Path | None:
    from helpers.chain_handler import ChainHandler

    chain_handler = ChainHandler(pf)

    if step == 1:
        if not preceding_file:
            return None
        stem = Path(preceding_file).stem
        # Prefer _real.png (actual last frame of preceding transition)
        real_p = pf / "frames" / f"{stem}_real.png"
        if real_p.exists():
            return real_p
        for ext in ("png", "jpg"):
            end_p = pf / "frames" / f"{stem}_end.{ext}"
            if end_p.exists():
                return end_p
        src = pf / preceding_file
        if src.exists():
            try:
                from utils.frame_extractor import FrameExtractor
                return FrameExtractor(project_folder=pf).extract_end_frame(
                    preceding_file, target_w, target_h
                )
            except Exception:
                pass
        return None
    else:
        prev_name = f"{chain_prefix}_{step - 1:03d}.mp4"
        cached = frame_cache.get(prev_name)
        if cached and Path(cached).exists():
            return Path(cached)
        prev_path = chain_handler.get_chain_output_path(prev_name)
        if prev_path.exists():
            return chain_handler.extract_last_frame(prev_path, target_w, target_h)
        return None


def _get_end_frame(pf: Path, end_target: str, target_w: int, target_h: int) -> Path | None:
    stem = Path(end_target).stem
    for ext in ("png", "jpg"):
        p = pf / "frames" / f"{stem}_start.{ext}"
        if p.exists():
            return p
    src = pf / end_target
    if src.exists():
        try:
            from utils.frame_extractor import FrameExtractor
            return FrameExtractor(project_folder=pf).extract_start_frame(
                end_target, target_w, target_h
            )
        except Exception:
            pass
    return None


# ── Background task ───────────────────────────────────────────────────────────

async def _run_chain(
    run_filename:   str,
    chain_prefix:   str,
    from_step:      int,
    chain_item:     dict,
    preceding_file: str | None,
    end_target:     str | None,
    pf:             Path,
) -> None:
    from helpers.chain_handler import ChainHandler
    from app.services import app_config_service

    loop = asyncio.get_running_loop()

    try:
        flow_data  = get_run_flow(run_filename)
        flow       = flow_data["flow"] if flow_data else []
        target_w, target_h = _detect_resolution(pf, flow)

        # Validate backend (blocking)
        backend = _init_backend(chain_item)
        await loop.run_in_executor(None, backend.validate_requirements)

        chain_handler = ChainHandler(pf)
        steps    = chain_item["chain"]
        total    = len(steps)
        defaults = app_config_service.get_defaults()
        frame_cache: dict[str, Path] = {}

        # Chain-level config (shared across all steps)
        chain_base = {
            k: v for k, v in chain_item.items()
            if k not in ("chain", "chain_prefix", "transition_to_next")
        }

        _state["status"] = "running"

        for step_idx in range(from_step, total + 1):
            _state["step"] = step_idx

            print(f"  ⛓  Chain '{chain_prefix}' — step {step_idx}/{total}")

            # Merge per-step overrides on top of chain defaults
            step_cfg = {**chain_base, **steps[step_idx - 1]}

            # Resolve frames
            start_frame = _get_start_frame(
                pf, chain_prefix, step_idx,
                preceding_file, frame_cache,
                target_w, target_h,
            )
            if start_frame is None or not Path(start_frame).exists():
                raise RuntimeError(
                    f"Brak klatki startowej dla step {step_idx} "
                    f"(szukano: {start_frame})"
                )

            end_frame: Path | None = None
            if step_idx == total and end_target:
                end_frame = _get_end_frame(pf, end_target, target_w, target_h)

            # Output
            out_name = f"{chain_prefix}_{step_idx:03d}.mp4"
            out_path = chain_handler.get_chain_output_path(out_name)
            out_path.parent.mkdir(parents=True, exist_ok=True)

            # Per-step AtlasCloud overrides
            if chain_item.get("backend") == "atlascloud":
                if step_cfg.get("atlascloud_resolution"):
                    backend.config["atlascloud_resolution"] = step_cfg["atlascloud_resolution"]
                if step_cfg.get("atlascloud_prompt_extend") is not None:
                    backend.config["atlascloud_prompt_extend"] = step_cfg["atlascloud_prompt_extend"]

            # Run generation in thread pool (blocking call)
            sf, ef, op, sc = start_frame, end_frame, out_path, step_cfg
            success = await loop.run_in_executor(
                None,
                lambda sf=sf, ef=ef, op=op, sc=sc: backend.generate_transition(
                    start_frame=sf,
                    end_frame=ef,
                    output_path=op,
                    duration=sc.get("duration", defaults.get("duration", 5)),
                    fps=sc.get("fps", defaults.get("fps", 16)),
                    steps=sc.get("steps", defaults.get("steps", 6)),
                    cfg=sc.get("cfg", defaults.get("cfg", 2.0)),
                    seed=sc.get("seed", -1),
                    positive_prompt=sc.get("pos", "") or "",
                    negative_prompt=sc.get("neg", "") or "",
                    width=target_w,
                    height=target_h,
                    blocks_to_swap=sc.get("blocks_to_swap", defaults.get("blocks_to_swap")),
                    frame_interpolation=sc.get(
                        "frame_interpolation",
                        defaults.get("frame_interpolation", True),
                    ),
                ),
            )

            if not success:
                raise RuntimeError(f"Backend zwrócił błąd dla step {step_idx}/{total}")

            print(f"  ✓ {out_name}")

            # Extract last frame for the next step's start
            last_frame = await loop.run_in_executor(
                None,
                lambda op=out_path: chain_handler.extract_last_frame(op, target_w, target_h),
            )
            if last_frame:
                frame_cache[out_name] = last_frame

            # Last step + end_target: write _real.png so the next item starts cleanly
            if step_idx == total and end_target and last_frame:
                real_p = pf / "frames" / f"{Path(end_target).stem}_real.png"
                if not real_p.exists():
                    try:
                        from utils.frame_extractor import FrameExtractor
                        FrameExtractor(project_folder=pf).extract_last_frame_to(
                            out_path, target_w, target_h, real_p
                        )
                    except Exception:
                        pass

        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
        print(f"  ✅ Chain '{chain_prefix}' gotowy ({elapsed}s)")

    except asyncio.CancelledError:
        _state.update({"status": "idle", "error": "Anulowano"})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})
        print(f"  ✗ Chain error: {exc}", file=sys.stderr)
