# -*- coding: utf-8 -*-
"""
Single-transition service — regenerates one file-to-file transition clip.

Analogous to chain_service.py but for regular (non-chain) transitions.

Flow:
  1. start_single_transition() validates inputs, finds the TransitionPair,
     resolves frames, creates an async task.
  2. _run() calls backend.generate_transition() in an executor thread.
  3. UI polls /api/single_transition/status.
"""

import asyncio
import sys
import time
from pathlib import Path

from app.services.media_service import _project_folder
from app.services.run_file_service import get_run_flow


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":          "idle",   # idle | queued | running | done | error
    "run_filename":    None,
    "transition_name": None,
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


# ── Public entry point ────────────────────────────────────────────────────────

def start_single_transition(run_filename: str, transition_name: str, mmaudio: bool = False) -> dict:
    """
    Queue a single-transition generation job.

    Parameters
    ----------
    run_filename     : str  RUN_*.yaml filename
    transition_name  : str  e.g. "18.53. Igraszki_2_19.41 happy_end sitting_transition.mp4"
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Single-transition generacja jest już w toku"}

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

    # Find the TransitionPair that matches transition_name
    from flow_parser import parse_flow
    parser = parse_flow(flow)
    pair = None
    for p in parser.get_transition_pairs():
        if p.get_transition_name() == transition_name:
            pair = p
            break

    if pair is None:
        return {"ok": False, "error": f"Nie znaleziono pary dla: {transition_name}"}

    _reset_state()
    _state.update({
        "status":          "queued",
        "run_filename":    run_filename,
        "transition_name": transition_name,
        "started_at":      time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run(run_filename=run_filename, pair=pair, pf=pf, mmaudio=mmaudio)
        )
    except RuntimeError as exc:
        _state.update({"status": "error", "error": str(exc)})
        return {"ok": False, "error": str(exc)}

    return {"ok": True}


# ── Param logging ────────────────────────────────────────────────────────────

def _log_gen_params(label, width, height, duration, fps, steps, cfg, seed,
                    bts, bts_src, fi, lora_high=None, lora_low=None,
                    audio_prompt=None, pos=None, use_lightning=None):
    from app.services.process_service import process_service
    bts_str = f"{bts} ({bts_src})" if bts is not None else f"workflow ({bts_src})"
    fi_str  = "✓" if fi else "✗"
    mode_str = " | ⚡ light" if use_lightning else " | 🎨 HQ"
    lora_str = ""
    if lora_high or lora_low:
        lh = Path(lora_high).stem if lora_high else "—"
        ll = Path(lora_low).stem  if lora_low  else "—"
        lora_str = f"\n   🎭 LoRA H: {lh} | L: {ll}"
    audio_str = f"\n   🔊 {audio_prompt[:70]}..." if audio_prompt and len(audio_prompt) > 70 \
                else (f"\n   🔊 {audio_prompt}" if audio_prompt else "")
    pos_str = f"\n   📝 pos: {pos}..." if pos else ""
    process_service.log_sys(
        f"{label}\n"
        f"   📐 {width}×{height} | ⏱ {duration}s | 🎞 {fps}fps | "
        f"🪜 {steps} steps | cfg={cfg} | seed={seed}\n"
        f"   🔲 bts={bts_str} | RIFE={fi_str}{mode_str}"
        f"{lora_str}{audio_str}{pos_str}"
    )


# ── Backend helpers (mirrors chain_service) ───────────────────────────────────

def _build_backend_config(backend_name: str, atlascloud_resolution=None, atlascloud_prompt_extend=None) -> dict:
    from app.services import app_config_service

    cfg = dict(app_config_service.get_backend(backend_name))
    video_gen = app_config_service.get_model(backend_name, "video_gen")
    cfg.update(video_gen)

    if backend_name == "atlascloud":
        if atlascloud_resolution is not None:
            cfg["atlascloud_resolution"] = atlascloud_resolution
        if atlascloud_prompt_extend is not None:
            cfg["atlascloud_prompt_extend"] = atlascloud_prompt_extend

    return cfg


def _init_backend(backend_name: str, atlascloud_resolution=None, atlascloud_prompt_extend=None):
    cfg = _build_backend_config(backend_name, atlascloud_resolution, atlascloud_prompt_extend)

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


def _get_start_frame(pf: Path, from_file: str, target_w: int, target_h: int) -> Path | None:
    stem = Path(from_file).stem
    real_p = pf / "frames" / f"{stem}_real.png"
    if real_p.exists():
        return real_p
    for ext in ("png", "jpg"):
        end_p = pf / "frames" / f"{stem}_end.{ext}"
        if end_p.exists():
            return end_p
    src = pf / from_file
    if src.exists():
        try:
            from utils.frame_extractor import FrameExtractor
            return FrameExtractor(project_folder=pf).extract_end_frame(
                from_file, target_w, target_h
            )
        except Exception:
            pass
    return None


def _get_end_frame(pf: Path, to_file: str, target_w: int, target_h: int) -> Path | None:
    stem = Path(to_file).stem
    for ext in ("png", "jpg"):
        p = pf / "frames" / f"{stem}_start.{ext}"
        if p.exists():
            return p
    src = pf / to_file
    if src.exists():
        try:
            from utils.frame_extractor import FrameExtractor
            return FrameExtractor(project_folder=pf).extract_start_frame(
                to_file, target_w, target_h
            )
        except Exception:
            pass
    return None


# ── Background task ───────────────────────────────────────────────────────────

async def _run(run_filename: str, pair, pf: Path, mmaudio: bool = False) -> None:
    from app.services import app_config_service
    from app.services.run_file_service import get_run_details

    loop = asyncio.get_running_loop()

    try:
        flow_data = get_run_flow(run_filename)
        flow = flow_data["flow"] if flow_data else []

        run_details = get_run_details(run_filename) or {}

        # Mirror batch_transitions.py priority: FROM config > TO config > defaults
        sc_from = pair.from_config or {}
        sc_to   = pair.to_config or {}

        def _pick(key, default=None):
            v = sc_from.get(key)
            if v is not None:
                return v
            v = sc_to.get(key)
            if v is not None:
                return v
            return default

        # Resolution: from_config only > project > auto-detect
        # TO config intentionally excluded — end frame is a visual target, not a param source
        _tile_w = sc_from.get("width")
        _tile_h = sc_from.get("height")
        if _tile_w and _tile_h:
            target_w = (int(_tile_w) // 16) * 16 or 1024
            target_h = (int(_tile_h) // 16) * 16 or 1024
        else:
            configured_res = run_details.get("force_resolution") or run_details.get("default_resolution")
            if configured_res:
                target_w = (int(configured_res[0]) // 16) * 16 or 1024
                target_h = (int(configured_res[1]) // 16) * 16 or 1024
            else:
                target_w, target_h = _detect_resolution(pf, flow)

        import os
        if mmaudio:
            os.environ["MMAUDIO_ENABLED"] = "1"
        elif "MMAUDIO_ENABLED" in os.environ:
            del os.environ["MMAUDIO_ENABLED"]

        defaults = app_config_service.get_defaults()
        # Merge project-level defaults on top (project overrides app globals)
        proj_defs = run_details.get("defaults") or {}
        if proj_defs:
            defaults = {**defaults, **{k: v for k, v in proj_defs.items() if v is not None}}

        _backend_name = _pick("backend") or "linux"
        _ac_res = _pick("atlascloud_resolution")
        _ac_pe  = _pick("atlascloud_prompt_extend")

        backend = _init_backend(_backend_name, _ac_res, _ac_pe)
        await loop.run_in_executor(None, backend.validate_requirements)

        # Resolve frames
        start_frame = await loop.run_in_executor(
            None,
            lambda: _get_start_frame(pf, pair.from_file, target_w, target_h),
        )
        if not start_frame or not Path(start_frame).exists():
            raise RuntimeError(
                f"Brak klatki startowej dla {pair.from_file} "
                f"(szukano: {start_frame})"
            )

        end_frame = await loop.run_in_executor(
            None,
            lambda: _get_end_frame(pf, pair.to_file, target_w, target_h),
        )

        out_path = pf / "transitions" / pair.get_transition_name()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        _state["status"] = "running"

        _dur        = _pick("duration",            defaults.get("duration", 5))
        _fps        = _pick("fps",                 defaults.get("fps", 16))
        _cfg        = _pick("cfg",                 defaults.get("cfg", 2.0))
        _seed       = _pick("seed",                -1)
        _fi         = _pick("frame_interpolation", defaults.get("frame_interpolation", True))
        _lh         = _pick("lora_high")    or None
        _ll         = _pick("lora_low")     or None
        _ln         = _pick("lora_name")    or None
        _ls         = _pick("lora_strength") or None
        _ul         = _pick("use_lightning")
        _ul         = _ul if _ul is not None else defaults.get("use_lightning", True)
        if _ul:
            # Lightning: don't override steps — workflow JSON has correct baked-in count
            _steps = None
            _steps_hq = None
        else:
            # HQ: steps_hq from file item → project → global → 15
            _steps_hq = _pick("steps_hq") or defaults.get("steps_hq", 15)
            _steps = None
        # Workflow override: project defaults → backend uses global (no per-step field for file tiles)
        _proj_defs_raw = run_details.get("defaults") or {}
        _proj_wf_key = 'lightning_workflow' if _ul else 'hq_workflow'
        _wf_override = (_proj_defs_raw.get(_proj_wf_key) or "").strip() or None
        _ap         = _pick("audio_prompt") or None
        _an         = _pick("audio_negative_prompt") or None
        _pos_full   = _pick("pos") or ""
        _neg        = _pick("neg") or ""
        _gen_count  = max(1, int(_pick("generate_count") or 1))
        _pos        = _pos_full[:80]

        _tile_bts = _pick("blocks_to_swap")
        if _tile_bts is not None:
            _bts, _bts_src = _tile_bts, "manual"
        else:
            _proj_auto = (run_details.get("defaults") or {}).get("auto_blocks_to_swap")
            _is_auto   = _proj_auto if _proj_auto is not None else defaults.get("auto_blocks_to_swap", True)
            if _is_auto:
                from backends.base_backend import _auto_blocks_to_swap as _calc_bts
                _bts, _bts_src = _calc_bts(target_w, target_h), "auto"
            else:
                _bts, _bts_src = defaults.get("blocks_to_swap"), "global"

        _log_gen_params(
            label=f"🎬 {pair.get_transition_name()}",
            width=target_w, height=target_h,
            duration=_dur, fps=_fps, steps=_steps_hq if not _ul else None, cfg=_cfg, seed=_seed,
            bts=_bts, bts_src=_bts_src, fi=_fi,
            lora_high=_lh, lora_low=_ll,
            audio_prompt=_ap, pos=_pos,
            use_lightning=_ul,
        )

        _gt_kwargs = dict(
            start_frame=start_frame,
            end_frame=end_frame,
            output_path=out_path,
            duration=_dur,
            fps=_fps,
            steps=_steps,
            steps_hq=_steps_hq,
            cfg=_cfg,
            seed=_seed,
            positive_prompt=_pos_full,
            negative_prompt=_neg,
            width=target_w,
            height=target_h,
            blocks_to_swap=_bts,
            frame_interpolation=_fi,
            lora_name=_ln,
            lora_strength=_ls,
            lora_high=_lh,
            lora_low=_ll,
            audio_prompt=_ap or "",
            audio_negative_prompt=_an or "",
            use_lightning=_ul,
            workflow_override=_wf_override,
        )

        import shutil
        from datetime import datetime

        success = False
        for _gen_i in range(_gen_count):
            if _gen_count > 1:
                from app.services.process_service import process_service
                process_service.log_sys(f"  🎲 Generacja {_gen_i + 1}/{_gen_count}")
            if _gen_i > 0 and out_path.exists():
                _ts   = datetime.now().strftime('%y%m%d%H%M%S')
                _arch = out_path.with_name(f"{out_path.stem}_ver{_ts}{out_path.suffix}")
                shutil.move(str(out_path), str(_arch))
            success = await loop.run_in_executor(None, lambda: backend.generate_transition(**_gt_kwargs))
            if not success:
                break

        if not success:
            raise RuntimeError("Backend zwrócił błąd")

        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
        print(f"  ✅ {pair.get_transition_name()} gotowy ({elapsed}s)")

    except asyncio.CancelledError:
        _state.update({"status": "idle", "error": "Anulowano"})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})
        print(f"  ✗ Single transition error: {exc}", file=sys.stderr)
