# -*- coding: utf-8 -*-
"""
DubIt service — generates lipsync clips using LTX-Video 2.3 DubIt IC-LoRA.

Two-pass architecture:
  Pass 1: P1_W × P1_H (= P2/2), 8 euler steps
  Pass 2: P2_W × P2_H, spatial upscale x2, 3 refinement steps

Requirements:
  - ComfyUI running on Linux/WSL2 with --highvram flag
  - ltx-2.3-22b-dev-UD-Q3_K_S.gguf in ComfyUI models/unet/
  - ltx-2.3-22b-ic-lora-dubit-0.9.safetensors in models/loras/
  - Workflow configured in app_config.yaml → backends.linux.models.dubit.workflow_json
"""

import asyncio
import copy
import json
import math
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.services.media_service import dubit_path, _project_folder
from app.services import app_config_service


# ── Resolution helpers ────────────────────────────────────────────────────────

def round64(n: int) -> int:
    """Round to nearest multiple of 64 (DubIt 2-pass requirement)."""
    return max(64, round(n / 64) * 64)


# ── Audio helpers ─────────────────────────────────────────────────────────────

def _audio_duration(path: Path) -> float:
    """Return audio duration in seconds via ffprobe, or 0 on failure."""
    _args = ["-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1"]
    # Try Windows ffprobe first
    try:
        result = subprocess.run(
            ["ffprobe"] + _args + [str(path)],
            capture_output=True, text=True, timeout=10,
        )
        val = float(result.stdout.strip())
        if val > 0:
            return val
    except Exception:
        pass
    # WSL fallback
    try:
        result = subprocess.run(
            ["wsl", "ffprobe"] + _args + [_win_to_wsl(path)],
            capture_output=True, text=True, timeout=10,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def _frames_from_duration(duration_s: float, fps: int = 24) -> int:
    """Calculate frame count (8n+1 form), rounded UP — video covers full audio duration."""
    import math
    raw = duration_s * fps
    return max(9, math.ceil(raw / 8) * 8 + 1)


def _pad_audio(audio_path: Path, target_duration: float, tmp_dir: Path) -> Path:
    """
    Return a path to audio padded to target_duration with silence.
    If audio is already >= target_duration, returns original path.
    Uses ffmpeg apad filter — no extra Python deps required.
    """
    actual = _audio_duration(audio_path)
    if actual <= 0 or actual >= target_duration - 0.05:
        return audio_path

    out = tmp_dir / f"_dubit_pad_{audio_path.stem}.wav"
    pad_sec = target_duration - actual
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(audio_path),
            "-af", f"apad=pad_dur={pad_sec:.3f}",
            "-t", f"{target_duration:.3f}",
            "-ar", "44100",
            "-ac", "2",
            str(out),
        ],
        capture_output=True,
        timeout=60,
    )
    if out.exists() and out.stat().st_size > 0:
        return out
    return audio_path  # fallback: use original if padding failed


# ── Workflow helpers ──────────────────────────────────────────────────────────

_workflow_cache: dict | None = None


def _load_workflow() -> dict:
    global _workflow_cache
    if _workflow_cache is not None:
        return _workflow_cache
    wf_path = app_config_service.get_model("linux", "dubit").get("workflow_json", "")
    if not wf_path or not Path(wf_path).exists():
        raise RuntimeError(
            f"DubIt workflow JSON not found: {wf_path!r}. "
            "Check app_config.yaml → backends.linux.models.dubit.workflow_json"
        )
    with open(wf_path, encoding="utf-8") as f:
        _workflow_cache = json.load(f)
    return _workflow_cache


def _patch_workflow(
    workflow: dict,
    image_filename: str,
    audio_filename: str,
    p1_w: int,
    p1_h: int,
    p2_w: int,
    p2_h: int,
    frames: int,
    audio_duration: float,
    prompt: str,
    negative_prompt: str,
    filename_prefix: str,
) -> dict:
    """Patch a deep copy of the DubIt workflow with per-job parameters."""
    wf = copy.deepcopy(workflow)

    # Prompts
    if "10" in wf:
        wf["10"]["inputs"]["text"] = prompt or "A person is speaking, lip movements synchronized with audio"
    if "11" in wf and negative_prompt:
        wf["11"]["inputs"]["text"] = negative_prompt

    # Image and audio inputs
    if "20" in wf:
        wf["20"]["inputs"]["image"] = image_filename
    if "21" in wf:
        wf["21"]["inputs"]["audio"] = audio_filename

    # Pass 1 resize (P2/2)
    if "35" in wf:
        wf["35"]["inputs"]["resize_type.width"]  = p1_w
        wf["35"]["inputs"]["resize_type.height"] = p1_h

    # Pass 2 resize
    if "36" in wf:
        wf["36"]["inputs"]["resize_type.width"]  = p2_w
        wf["36"]["inputs"]["resize_type.height"] = p2_h

    # Pass 1 empty latents
    if "40" in wf:
        wf["40"]["inputs"]["width"]  = p1_w
        wf["40"]["inputs"]["height"] = p1_h
        wf["40"]["inputs"]["length"] = frames
    if "41" in wf:
        wf["41"]["inputs"]["frames_number"] = frames

    # Output prefix
    if "83" in wf:
        wf["83"]["inputs"]["filename_prefix"] = filename_prefix

    # Audio trim: set to actual padded duration
    if "84" in wf:
        wf["84"]["inputs"]["duration"] = round(audio_duration, 3)

    return wf


def _ascii_safe(name: str, max_len: int = 40) -> str:
    safe = re.sub(r'[^\x20-\x7E]', '', name)
    safe = re.sub(r'[^\w\-.]', '_', safe)
    return safe[:max_len].strip('_') or "x"


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":        "idle",
    "prompt_id":     None,
    "run_filename":  None,
    "dubit_name":    None,
    "output_name":   None,
    "error":         None,
    "started_at":    None,
    "elapsed_s":     None,
    "flow_idx":      None,
    "step_current":  None,
    "step_total":    None,
}

_task: asyncio.Task | None = None


def get_dubit_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("running", "queued"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":        "idle",
        "prompt_id":     None,
        "run_filename":  None,
        "dubit_name":    None,
        "output_name":   None,
        "error":         None,
        "started_at":    None,
        "elapsed_s":     None,
        "flow_idx":      None,
        "step_current":  None,
        "step_total":    None,
    })


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _http_post(url: str, payload: dict, timeout: int = 15) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _http_get(url: str, timeout: int = 10) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


# ── Output detection ──────────────────────────────────────────────────────────

def _find_video_in_outputs(outputs: dict) -> dict | None:
    for node_id, node_out in outputs.items():
        if not isinstance(node_out, dict):
            continue
        for key in ("videos", "gifs", "images"):
            for v in (node_out.get(key) or []):
                if isinstance(v, dict) and v.get("filename", "").endswith(".mp4"):
                    return v
    return None


def _newest_mp4_added_after(directory: Path, known: set[str]) -> Path | None:
    if not directory.exists():
        return None
    candidates = [p for p in directory.rglob("*.mp4") if p.name not in known]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def _win_to_wsl(p: Path) -> str:
    """Convert Windows path (D:\\foo\\bar) to WSL path (/mnt/d/foo/bar)."""
    s = str(p)
    if len(s) >= 2 and s[1] == ':':
        return '/mnt/' + s[0].lower() + '/' + s[2:].replace('\\', '/')
    return s.replace('\\', '/')


def _extract_last_frame(mp4_path: Path, out_path: Path) -> bool:
    """Extract last frame of mp4 to out_path (PNG)."""
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(mp4_path), "-update", "1", str(out_path)],
            capture_output=True, timeout=60,
        )
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


def _logsys(msg: str) -> None:
    try:
        from app.services.process_service import process_service as _ps
        _ps.log_sys(msg)
    except Exception:
        print(msg)


# ── Core generation task ──────────────────────────────────────────────────────

async def _run_dubit(
    source_image: Path,
    audio_path:   Path,
    dest_path:    Path,
    run_filename: str,
    dubit_name:   str,
    p2_w:         int,
    p2_h:         int,
    prompt:       str,
    negative_prompt: str,
    prefix:       str,
    _final:       bool = True,
) -> None:
    loop       = asyncio.get_running_loop()
    url        = settings.comfyui_url
    input_dir  = Path(settings.comfyui_linux_input_dir)
    output_dir = Path(settings.comfyui_linux_output_dir)

    p1_w = p2_w // 2
    p1_h = p2_h // 2

    import os as _os
    _os.makedirs(str(input_dir), exist_ok=True)

    ts          = datetime.now().strftime("%Y%m%d%H%M%S%f")
    _safe_stem  = _ascii_safe(source_image.stem)
    _safe_audio = _ascii_safe(audio_path.stem)
    _img_ext    = ".png" if source_image.suffix.lower() in {".jpg", ".jpeg"} else source_image.suffix
    tmp_img     = input_dir / f"dubit_img_{ts}_{_safe_stem}{_img_ext}"
    tmp_audio   = input_dir / f"dubit_aud_{ts}_{_safe_audio}{audio_path.suffix}"

    # Convert JPEG → PNG
    if source_image.suffix.lower() in {".jpg", ".jpeg"}:
        from PIL import Image as _PILImage
        with _PILImage.open(str(source_image)) as _img:
            if _img.mode != "RGB":
                _img = _img.convert("RGB")
            _img.save(str(tmp_img), "PNG")
    else:
        shutil.copy2(str(source_image), str(tmp_img))

    # Pad audio if shorter than video duration
    audio_dur = _audio_duration(audio_path)
    if audio_dur <= 0:
        audio_dur = 3.0
    # Add 0.5s tail silence so the last syllable has future audio context for the model
    audio_dur_for_frames = audio_dur + 0.5
    frames    = _frames_from_duration(audio_dur_for_frames)
    video_dur = frames / 24.0

    padded_audio = _pad_audio(audio_path, video_dur, input_dir)
    shutil.copy2(str(padded_audio), str(tmp_audio))
    # clean up temp padded file if we created one
    _padded_is_tmp = (padded_audio != audio_path)

    existing_mp4s: set[str] = (
        {p.name for p in output_dir.rglob("*.mp4")} if output_dir.exists() else set()
    )

    _img_size = tmp_img.stat().st_size if tmp_img.exists() else -1
    _logsys(f"[DubIt] tmp_img → {tmp_img.name} ({_img_size}B) {'✓' if _img_size > 0 else '❌ BRAK/PUSTY'}")

    try:
        _logsys(f"[DubIt] {dubit_name}: {p2_w}×{p2_h}, {frames}f ({video_dur:.1f}s), audio={audio_path.name}")
        _logsys(f"[DubIt] prompt: {prompt[:120] if prompt else '(default)'}")

        workflow = _load_workflow()
        workflow = _patch_workflow(
            workflow,
            image_filename=tmp_img.name,
            audio_filename=tmp_audio.name,
            p1_w=p1_w, p1_h=p1_h,
            p2_w=p2_w, p2_h=p2_h,
            frames=frames,
            audio_duration=audio_dur_for_frames,
            prompt=prompt,
            negative_prompt=negative_prompt,
            filename_prefix=prefix,
        )

        def _submit():
            try:
                return _http_post(f"{url}/prompt", {"prompt": workflow})
            except urllib.error.HTTPError as e:
                try:
                    body = e.read().decode("utf-8", errors="replace")
                except Exception:
                    body = str(e)
                raise RuntimeError(f"ComfyUI rejected prompt (HTTP {e.code}): {body}") from e
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        "Linux ComfyUI niedostępny (port 8189). Uruchom środowisko Linux."
                    ) from e
                raise

        resp      = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return prompt_id: {resp}")

        _state["prompt_id"] = prompt_id
        _state["status"]    = "running"

        out_video_path: Path | None = None
        streak = 0
        # DubIt at 896×1152 takes ~10–15 min → poll up to 90 min (1800 × 3s)
        for _ in range(1800):
            await asyncio.sleep(3)
            ok = False
            try:
                def _check():
                    return _http_get(f"{url}/history/{prompt_id}")
                history = await loop.run_in_executor(None, _check)
                ok = True
                streak = 0

                if prompt_id in history:
                    job     = history[prompt_id]
                    outputs = job.get("outputs", {})
                    entry   = _find_video_in_outputs(outputs)
                    if entry:
                        subfolder = entry.get("subfolder", "")
                        filename  = entry["filename"]
                        candidate = output_dir / subfolder / filename
                        if candidate.exists():
                            out_video_path = candidate
                            break

                    if job.get("status", {}).get("status_str") == "error":
                        msgs = job["status"].get("messages", [])
                        err  = next(
                            (m[1].get("exception_message", str(m))
                             for m in msgs if m[0] == "execution_error"),
                            "ComfyUI reported an error",
                        )
                        raise RuntimeError(err)

            except RuntimeError:
                raise
            except Exception:
                streak += 1

            if not ok and streak >= 5:
                new_file = _newest_mp4_added_after(output_dir, existing_mp4s)
                if new_file is not None:
                    out_video_path = new_file
                    break
        else:
            raise RuntimeError("Timeout: DubIt did not complete within 90 minutes")

        if out_video_path is None or not out_video_path.exists():
            raise RuntimeError(f"DubIt output file not found: {out_video_path}")

        # Wait for file write to stabilise
        await asyncio.sleep(3)
        prev_size = -1
        for _ in range(30):
            cur_size = out_video_path.stat().st_size
            if cur_size == prev_size and cur_size > 0:
                break
            prev_size = cur_size
            await asyncio.sleep(3)

        # Extract end frame before moving (WSL filesystem is accessible here)
        _end_frame_tmp = input_dir / f"dubit_endframe_{dest_path.stem}.png"
        _extract_last_frame(out_video_path, _end_frame_tmp)

        # Move to destination
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_dest = dest_path.parent / f"_tmp_dubit_{dest_path.name}"
        shutil.copy2(str(out_video_path), str(tmp_dest))
        if dest_path.exists():
            dest_path.unlink()
        tmp_dest.rename(dest_path)
        try:
            out_video_path.unlink()
        except Exception:
            pass

        # Save end frame for continuity (next tile can use this as start frame)
        pf         = dest_path.parent.parent.parent
        frames_dir = pf / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        end_dst = frames_dir / f"{dest_path.stem}_end.png"
        if _end_frame_tmp.exists():
            shutil.copy2(str(_end_frame_tmp), str(end_dst))
            try:
                _end_frame_tmp.unlink()
            except Exception:
                pass
        else:
            _extract_last_frame(dest_path, end_dst)

        # Write _real.png for the next static-image tile — only for final segment
        # (intermediate segments must not overwrite _real.png of preceding file tiles)
        if _final:
            try:
                from app.services.run_file_service import get_run_flow
                _flow_data = get_run_flow(run_filename)
                _flow      = (_flow_data.get("flow") or []) if _flow_data else []
                _next_file = None
                for _fi in _flow:
                    if not isinstance(_fi, dict):
                        continue
                    if _fi.get("break") or _fi.get("type") == "scene_break":
                        break
                    if _fi.get("type") == "dubit" and (_fi.get("prefix") or "") == (dubit_name.replace("dubit_", "").replace(".mp4", "")):
                        _next_file = None
                        continue
                    if _fi.get("file"):
                        _next_file = _fi["file"]
                        break
                if _next_file:
                    _real_path = pf / "frames" / f"{Path(_next_file).stem}_real.png"
                    if end_dst.exists():
                        shutil.copy2(str(end_dst), str(_real_path))
            except Exception:
                pass

        elapsed = round(time.time() - _state["started_at"], 1)
        _logsys(f"[DubIt] {'Done' if _final else 'Step done'}: {dest_path.name} ({elapsed}s)")
        if _final:
            _state.update({
                "status":      "done",
                "output_name": dest_path.name,
                "elapsed_s":   elapsed,
            })

    except Exception as exc:
        _logsys(f"[DubIt] Error: {exc}")
        _state.update({"status": "error", "error": str(exc)})

    finally:
        for p in (tmp_img, tmp_audio):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass
        if _padded_is_tmp:
            try:
                padded_audio.unlink()
            except Exception:
                pass


# ── Multi-step runner ────────────────────────────────────────────────────────

def _seg_path(dest_path: Path, i: int) -> Path:
    """Permanent segment path for multi-step DubIt: dubit_{stem}_01.mp4 (1-indexed, like talk)."""
    return dest_path.parent / f"{dest_path.stem}_{i+1:02d}.mp4"


def _seg_end_frame(frames_dir: Path, dest_path: Path, i: int) -> Path:
    """End-frame path for segment i (1-indexed filename)."""
    return frames_dir / f"{dest_path.stem}_{i+1:02d}_end.png"


async def _run_dubit_multi(
    steps_data:      list[dict],
    source_image:    Path,
    dest_path:       Path,
    pf:              Path,
    run_filename:    str,
    dubit_name:      str,
    p2_w:            int,
    p2_h:            int,
    prefix:          str,
    start_from_step: int = 0,
    end_at_step:     int | None = None,
    dry_run:         bool = False,
) -> None:
    if dry_run:
        _logsys("[DubIt][dry-run] tryb suchy — generacja ComfyUI pominięta")
    input_dir  = Path(settings.comfyui_linux_input_dir)
    frames_dir = pf / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    n    = len(steps_data)
    _end = n - 1 if end_at_step is None else min(end_at_step, n - 1)
    stem = dest_path.stem

    # When re-generating from an intermediate step, use last frame of preceding segment.
    # Follows Talk pattern: lastframes stored in input_dir as dubit_lastframe_{stem}_{N:02d}.png
    current_image = source_image
    if start_from_step > 0:
        prev_frame = input_dir / f"dubit_lastframe_{stem}_{start_from_step:02d}.png"
        if not prev_frame.exists():
            prev_seg = _seg_path(dest_path, start_from_step - 1)
            if prev_seg.exists():
                _extract_last_frame(prev_seg, prev_frame)
                _logsys(f"[DubIt] start_from_step={start_from_step}: wyciągam z {prev_seg.name} → {prev_frame.name}")
        if prev_frame.exists():
            current_image = prev_frame
            _logsys(f"[DubIt] start_from_step={start_from_step}: cur_img={prev_frame.name} ✓")
        else:
            _logsys(f"[DubIt] start_from_step={start_from_step}: brak segmentu {stem}_{start_from_step:02d}.mp4, cur_img=source_image")

    for i, step in enumerate(steps_data):
        seg_dest = _seg_path(dest_path, i)
        abs_step = i + 1  # 1-indexed, matches Talk convention

        if i < start_from_step or i > _end:
            if i < start_from_step and not seg_dest.exists():
                raise RuntimeError(
                    f"DubIt krok {i+1}: segment {seg_dest.name} nie istnieje — uruchom od początku"
                )
            continue

        _state["step_current"] = i + 1
        _state["step_total"]   = n
        _state["status"]       = "running"

        audio_file = (step.get("file") or "").strip()
        audio_path = pf / audio_file
        if not audio_path.exists():
            raise RuntimeError(f"DubIt krok {i+1}: nie znaleziono audio: {audio_file}")

        seg_prefix = f"{prefix}_s{i:03d}"
        _logsys(f"[DubIt] krok {abs_step}/{n}: source_image={current_image.name}, audio={audio_path.name}, dest={seg_dest.name}")

        if dry_run and seg_dest.exists():
            _logsys(f"[DubIt][dry-run] krok {abs_step}: {seg_dest.name} istnieje, pomijam ComfyUI")
        elif dry_run:
            _logsys(f"[DubIt][dry-run] krok {abs_step}: {seg_dest.name} NIE ISTNIEJE — nie można dry-run")
            continue
        else:
            await _run_dubit(
                source_image=current_image,
                audio_path=audio_path,
                dest_path=seg_dest,
                run_filename=run_filename,
                dubit_name=seg_dest.name,
                p2_w=p2_w,
                p2_h=p2_h,
                prompt=step.get("pos", "") or "",
                negative_prompt=step.get("neg", "") or "",
                prefix=seg_prefix,
                _final=False,
            )

        if _state["status"] == "error":
            return

        # Each subsequent segment anchors on last frame of the previous one.
        # Follows Talk pattern exactly: extract to input_dir, log ok=
        if i < _end:
            frame_path = input_dir / f"dubit_lastframe_{stem}_{abs_step:02d}.png"
            ok = _extract_last_frame(seg_dest, frame_path)
            _logsys(f"  [seg{abs_step}→{abs_step+1}] extract_last_frame: ok={ok} frame={frame_path.name} exists={frame_path.exists()}")
            if ok:
                current_image = frame_path

    # Verify all segments up to _end exist (skip in dry-run — some segments intentionally missing)
    if not dry_run:
        for i in range(_end + 1):
            sp = _seg_path(dest_path, i)
            if not sp.exists():
                raise RuntimeError(f"DubIt: brakuje segmentu {sp.name}")

    # Save tile-level end frame for continuity with next tile in flow
    last_seg    = _seg_path(dest_path, _end)
    end_dst     = frames_dir / f"{stem}_end.png"
    last_lf     = input_dir / f"dubit_lastframe_{stem}_{_end + 1:02d}.png"
    # Try lastframe file first (extracted before move), then extract from final segment
    if last_lf.exists():
        shutil.copy2(str(last_lf), str(end_dst))
    else:
        _extract_last_frame(last_seg, end_dst)

    # Write _real.png for next static tile in flow
    try:
        from app.services.run_file_service import get_run_flow
        _flow_data = get_run_flow(run_filename)
        _flow      = (_flow_data.get("flow") or []) if _flow_data else []
        _next_file = None
        for _fi in _flow:
            if not isinstance(_fi, dict):
                continue
            if _fi.get("break") or _fi.get("type") == "scene_break":
                break
            if _fi.get("type") == "dubit" and (_fi.get("prefix") or "") == (dubit_name.replace("dubit_", "").replace(".mp4", "")):
                _next_file = None
                continue
            if _fi.get("file"):
                _next_file = _fi["file"]
                break
        if _next_file:
            _real_path = pf / "frames" / f"{Path(_next_file).stem}_real.png"
            if end_dst.exists():
                shutil.copy2(str(end_dst), str(_real_path))
    except Exception:
        pass

    first_seg = _seg_path(dest_path, 0)
    elapsed   = round(time.time() - _state["started_at"], 1)
    generated = _end - start_from_step + 1
    _logsys(f"[DubIt] Multi-step done: {generated}/{n} kroków → {first_seg.name} … ({elapsed}s)")
    _state.update({
        "status":      "done",
        "output_name": first_seg.name,
        "elapsed_s":   elapsed,
    })


# ── Public API ────────────────────────────────────────────────────────────────

def start_dubit(
    run_filename:    str,
    dubit_item:      dict,
    start_image:     str,
    flow_idx:        int | None = None,
    start_from_step: int = 0,
    end_at_step:     int | None = None,
    dry_run:         bool = False,
) -> dict:
    """
    Queue a DubIt lipsync generation job.

    Parameters
    ----------
    run_filename : RUN_*.yaml filename
    dubit_item   : YAML tile dict (type, audio, pos, neg, prefix, width, height)
    start_image  : filename of start frame (relative to project_folder)
    flow_idx     : flow index for status tracking
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "DubIt jest już w toku"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono project_folder dla: {run_filename}"}

    # Resolution: tile > project > fallback (896×1152), always rounded to nearest 64
    _tile_w = dubit_item.get("width")
    _tile_h = dubit_item.get("height")
    if _tile_w and _tile_h:
        p2_w = round64(int(_tile_w))
        p2_h = round64(int(_tile_h))
    else:
        from app.services.run_file_service import get_run_details
        _run_details = get_run_details(run_filename) or {}
        _proj_res    = _run_details.get("force_resolution") or _run_details.get("default_resolution")
        if _proj_res:
            p2_w = round64(int(_proj_res[0]))
            p2_h = round64(int(_proj_res[1]))
        else:
            p2_w, p2_h = 896, 1152

    # Resolve start image (mirrors talk_service logic)
    _vid_exts = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    if Path(start_image).suffix.lower() in _vid_exts:
        stem       = Path(start_image).stem
        frame_path = pf / "frames" / f"{stem}_end.png"
        if not frame_path.exists():
            frame_path = pf / "frames" / f"{stem}_end.jpg"
        if frame_path.exists():
            img_path = frame_path
        else:
            video_src = pf / start_image
            if not video_src.exists():
                video_src = pf / "transitions" / "chains" / start_image
            if video_src.exists():
                try:
                    rel = str(video_src.relative_to(pf))
                except ValueError:
                    rel = video_src.name
                from utils.frame_extractor import FrameExtractor
                extractor = FrameExtractor(project_folder=pf, image_quality=95)
                extracted = extractor.extract_end_frame(rel, p2_w, p2_h)
                if extracted and extracted.exists():
                    img_path = extracted
                else:
                    return {"ok": False, "error": f"Nie udało się wyciągnąć klatki z: {start_image}"}
            else:
                return {"ok": False, "error": f"Nie znaleziono pliku źródłowego: {start_image}"}
    else:
        _stem      = Path(start_image).stem
        _real_path = pf / "frames" / f"{_stem}_real.png"
        img_path   = _real_path if _real_path.exists() else pf / start_image

    if not img_path.exists():
        return {"ok": False, "error": f"Nie znaleziono klatki startowej: {start_image}"}

    # Resolve audio steps (supports both legacy single-string and new [{file,pos,neg}] format)
    root_pos = str(dubit_item.get("pos", "") or "")
    root_neg = str(dubit_item.get("neg", "") or "")
    raw_audio = dubit_item.get("audio", "")

    if isinstance(raw_audio, list):
        steps_data = []
        for a in raw_audio:
            if isinstance(a, dict):
                steps_data.append({
                    "file": (a.get("file") or "").strip(),
                    "pos":  a.get("pos", "") or root_pos,
                    "neg":  a.get("neg", "") or root_neg,
                })
            else:
                steps_data.append({"file": str(a).strip(), "pos": root_pos, "neg": root_neg})
    elif isinstance(raw_audio, dict):
        steps_data = [{"file": (raw_audio.get("file") or "").strip(), "pos": root_pos, "neg": root_neg}]
    else:
        steps_data = [{"file": str(raw_audio).strip(), "pos": root_pos, "neg": root_neg}]

    steps_data = [s for s in steps_data if s["file"]]
    if not steps_data:
        return {"ok": False, "error": "DubIt: brak pliku audio w konfiguracji"}

    # Validate all audio files exist
    for s in steps_data:
        ap = pf / s["file"]
        if not ap.exists():
            return {"ok": False, "error": f"Nie znaleziono pliku audio: {s['file']}"}

    # Destination
    dest_path  = dubit_path(pf, dubit_item)
    dubit_name = dest_path.name

    # Prefix for ComfyUI output naming (based on first audio stem or explicit prefix)
    explicit_prefix = (dubit_item.get("prefix") or "").strip()
    first_audio_stem = Path(steps_data[0]["file"]).stem
    if explicit_prefix:
        prefix = f"DubIt_{_ascii_safe(explicit_prefix)}"
    else:
        prefix = f"DubIt_{_ascii_safe(first_audio_stem)}"

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "dubit_name":   dubit_name,
        "started_at":   time.time(),
        "flow_idx":     flow_idx,
        "step_total":   len(steps_data) if len(steps_data) > 1 else None,
    })

    if len(steps_data) == 1:
        audio_path = pf / steps_data[0]["file"]

        async def _launch():
            await _run_dubit(
                source_image=img_path,
                audio_path=audio_path,
                dest_path=dest_path,
                run_filename=run_filename,
                dubit_name=dubit_name,
                p2_w=p2_w,
                p2_h=p2_h,
                prompt=steps_data[0]["pos"],
                negative_prompt=steps_data[0]["neg"],
                prefix=prefix,
            )
    else:
        _sfs = max(0, min(start_from_step, len(steps_data) - 1))

        _eat = (
            min(end_at_step, len(steps_data) - 1)
            if end_at_step is not None else None
        )

        async def _launch():
            await _run_dubit_multi(
                steps_data=steps_data,
                source_image=img_path,
                dest_path=dest_path,
                pf=pf,
                run_filename=run_filename,
                dubit_name=dubit_name,
                p2_w=p2_w,
                p2_h=p2_h,
                prefix=prefix,
                start_from_step=_sfs,
                end_at_step=_eat,
                dry_run=dry_run,
            )

    import asyncio as _asyncio
    loop = None
    try:
        loop = _asyncio.get_event_loop()
    except RuntimeError:
        pass

    global _task
    if loop and loop.is_running():
        _task = loop.create_task(_launch())
    else:
        _asyncio.run(_launch())

    return {"ok": True, "dubit_name": dubit_name, "resolution": f"{p2_w}×{p2_h}"}


def cancel_dubit() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano"})
    return {"ok": True}
