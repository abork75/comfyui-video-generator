# -*- coding: utf-8 -*-
"""
Upscale service — upscales a single generated video clip using RealESRGAN
running on the Windows ComfyUI instance (port 8100).

Flow:
  1. Copy source clip → ComfyUI input dir (unique temp name)
  2. Build workflow from template (swap file + dimensions)
  3. POST to ComfyUI /prompt
  4. Poll /history/{prompt_id} until done (every 3 s, max 15 min)
  5. On success: archive original → move upscaled file to original path
  6. Clean up temp input file
"""

import asyncio
import copy
import json
import shutil
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.services import app_config_service
from app.services.media_service import (
    resolve_video,
    resolve_source_video,
    _project_folder,
)

# ── Workflow template (based on UPSCALER VIDEO utility-gan_upscaler.json) ────
_WORKFLOW_TEMPLATE: dict = {
    "1": {
        "inputs": {"model_name": "RealESRGAN_x4plus.pth"},
        "class_type": "UpscaleModelLoader",
        "_meta": {"title": "Load Upscale Model"},
    },
    "2": {
        "inputs": {
            "upscale_model": ["1", 0],
            "image":         ["10", 0],
        },
        "class_type": "ImageUpscaleWithModel",
        "_meta": {"title": "Upscale Image (using Model)"},
    },
    "9": {
        "inputs": {"file": "PLACEHOLDER.mp4"},
        "class_type": "LoadVideo",
        "_meta": {"title": "Load Video"},
    },
    "10": {
        "inputs": {"video": ["9", 0]},
        "class_type": "GetVideoComponents",
        "_meta": {"title": "Get Video Components"},
    },
    "11": {
        "inputs": {
            "fps":    ["10", 2],
            "images": ["13", 0],
            "audio":  ["10", 1],
        },
        "class_type": "CreateVideo",
        "_meta": {"title": "Create Video"},
    },
    "12": {
        "inputs": {
            "filename_prefix": "video/ComfyUI",
            "format":          "auto",
            "codec":           "auto",
            "video":           ["11", 0],
        },
        "class_type": "SaveVideo",
        "_meta": {"title": "Save Video"},
    },
    "13": {
        "inputs": {
            "width":         1024,
            "height":        1024,
            "interpolation": "lanczos",
            "method":        "stretch",
            "condition":     "always",
            "multiple_of":   0,
            "image":         ["2", 0],
        },
        "class_type": "ImageResize+",
        "_meta": {"title": "🔧 Image Resize"},
    },
}


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":       "idle",   # idle | queued | running | done | error
    "prompt_id":    None,
    "run_filename": None,
    "clip_name":    None,
    "width":        None,
    "height":       None,
    "output_name":  None,
    "error":        None,
    "started_at":   None,
    "elapsed_s":    None,
}

_task: asyncio.Task | None = None


def get_upscale_status() -> dict:
    """Return a copy of the current upscale job state."""
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("running", "queued"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":       "idle",
        "prompt_id":    None,
        "run_filename": None,
        "clip_name":    None,
        "width":        None,
        "height":       None,
        "output_name":  None,
        "error":        None,
        "started_at":   None,
        "elapsed_s":    None,
    })


# ── HTTP helpers (sync, called via run_in_executor) ──────────────────────────

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


# ── Background task ──────────────────────────────────────────────────────────

def _archive_before_upscale(source_path: Path, clip_type: str) -> None:
    """
    Back up the original file before upscaling, adding _beforeupscale to the name
    so the origin of the backup is immediately obvious.

    External:  project_folder/source_backup/{stem}_ver{ts}_beforeupscale.mp4
    Generated: same directory as the original / {stem}_ver{ts}_beforeupscale.mp4
    """
    ts = datetime.now().strftime("%y%m%d%H%M%S")
    backup_name = f"{source_path.stem}_ver{ts}_beforeupscale{source_path.suffix}"

    if clip_type == "external":
        backup_dir = source_path.parent / "source_backup"
        backup_dir.mkdir(exist_ok=True)
        shutil.copy2(str(source_path), str(backup_dir / backup_name))
    else:
        # transitions/ or transitions/chains/ — keep backup next to the original
        shutil.copy2(str(source_path), str(source_path.parent / backup_name))


def _find_video_in_outputs(outputs: dict) -> dict | None:
    """
    Scan ALL output nodes for any that contain a 'videos' list with mp4 files.
    Returns the first video entry found, or None.
    This is robust against ComfyUI renumbering nodes or using non-standard IDs.
    """
    for node_id, node_out in outputs.items():
        if not isinstance(node_out, dict):
            continue
        videos = node_out.get("videos") or node_out.get("gifs") or []
        for v in videos:
            if isinstance(v, dict) and v.get("filename", "").endswith(".mp4"):
                return v
    return None




async def _wait_for_stable_file(
    path: Path,
    poll_interval: float = 2.0,
    stable_rounds: int = 3,
    max_wait: float = 120.0,
) -> bool:
    """
    Poll `path` until its size stops changing for `stable_rounds` consecutive
    readings.  Returns True when stable, False if max_wait exceeded.
    This catches the case where ComfyUI reports a job as done but is still
    encoding/writing the output file (common for long videos).
    """
    prev_size = -1
    stable_count = 0
    deadline = time.time() + max_wait

    while time.time() < deadline:
        await asyncio.sleep(poll_interval)
        try:
            cur_size = path.stat().st_size
        except OSError:
            stable_count = 0
            prev_size = -1
            continue

        if cur_size > 0 and cur_size == prev_size:
            stable_count += 1
            if stable_count >= stable_rounds:
                return True
        else:
            stable_count = 0
            prev_size = cur_size

    return False


async def _run_upscale(
    source_path:  Path,
    dest_path:    Path,
    run_filename: str,
    clip_name:    str,
    clip_type:    str,
    width:        int,
    height:       int,
) -> None:
    """
    Full upscale pipeline:
      copy → submit → poll → archive original → place output → cleanup

    Detection strategy (in order):
      1. ComfyUI /history/{prompt_id} — scan ALL output nodes for mp4
      2. Directory fallback — any new mp4 in output/video since job start
    """
    loop         = asyncio.get_running_loop()
    _win         = app_config_service.get_backend("windows")
    upscale_url  = _win.get("api_url")  or settings.comfyui_upscale_url
    input_dir    = Path(_win.get("input_dir")  or settings.comfyui_upscale_input_dir)
    output_dir   = Path(_win.get("output_dir") or settings.comfyui_upscale_output_dir)
    video_dir   = output_dir / "video"

    ts       = datetime.now().strftime("%Y%m%d%H%M%S")
    tmp_name = f"upscale_{ts}_{source_path.name}"
    tmp_in   = input_dir / tmp_name

    try:
        # 1. expected_prefix used by fallback to find the exact output file
        expected_prefix: str = f"upscale_{ts}"

        # 2. Copy source → ComfyUI input dir
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source_path), str(tmp_in))

        # 3. Build workflow — prefer file from config, fallback to hardcoded template
        _wf_path_str = app_config_service.get_backend("windows").get("models", {}).get("upscale_video", {}).get("workflow_json", "")
        if _wf_path_str:
            _wf_path = Path(_wf_path_str)
            if _wf_path.exists():
                workflow = json.loads(_wf_path.read_text(encoding="utf-8"))
            else:
                workflow = copy.deepcopy(_WORKFLOW_TEMPLATE)
        else:
            workflow = copy.deepcopy(_WORKFLOW_TEMPLATE)
        workflow["9"]["inputs"]["file"]    = tmp_name
        workflow["13"]["inputs"]["width"]  = width
        workflow["13"]["inputs"]["height"] = height
        # Unique prefix per job → output: video/upscale_{ts}_00001_.mp4
        # Lets us detect the exact output file without mtime tricks or name collisions.
        upscale_prefix = f"video/upscale_{ts}"
        if "12" in workflow and "filename_prefix" in workflow["12"].get("inputs", {}):
            workflow["12"]["inputs"]["filename_prefix"] = upscale_prefix

        # 4. Submit to ComfyUI
        def _submit():
            try:
                return _http_post(f"{upscale_url}/prompt", {"prompt": workflow})
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):  # Windows / Linux "connection refused"
                    raise RuntimeError(
                        f"Windows ComfyUI niedostępny ({upscale_url}). "
                        f"Uruchom środowisko Windows i spróbuj ponownie."
                    ) from e
                raise

        resp = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return prompt_id: {resp}")

        _state["prompt_id"] = prompt_id
        _state["status"]    = "running"

        # 5. Poll for completion (history API + directory fallback)
        max_polls = 800          # 800 × 3 s = 40 min max (RealESRGAN ~17 min observed)
        out_video_path: Path | None = None
        _prompt_id = prompt_id   # local copy for closures

        for _ in range(max_polls):
            await asyncio.sleep(3)

            # ── Primary: ComfyUI history API ──────────────────────────
            try:
                def _check_history():
                    return _http_get(f"{upscale_url}/history/{_prompt_id}")

                history = await loop.run_in_executor(None, _check_history)

                if _prompt_id in history:
                    job     = history[_prompt_id]
                    outputs = job.get("outputs", {})

                    # Scan ALL nodes — don't hardcode node ID "12"
                    video_entry = _find_video_in_outputs(outputs)
                    if video_entry:
                        subfolder      = video_entry.get("subfolder", "")
                        filename       = video_entry["filename"]
                        candidate      = output_dir / subfolder / filename
                        print(f"  [upscale] history API → subfolder={subfolder!r} file={filename!r} candidate={candidate}")
                        if candidate.exists():
                            out_video_path = candidate
                            break
                        print(f"  [upscale] candidate not on disk yet, waiting...")
                    else:
                        print(f"  [upscale] history API: job done but no video entry in outputs={list(outputs.keys())}")

                    # Detect ComfyUI-reported error
                    status_info = job.get("status", {})
                    if status_info.get("status_str") == "error":
                        msgs = status_info.get("messages", [])
                        err  = next(
                            (m[1].get("exception_message", str(m))
                             for m in msgs if m[0] == "execution_error"),
                            "ComfyUI reported an error",
                        )
                        raise RuntimeError(err)

            except RuntimeError:
                raise   # re-raise ComfyUI errors
            except Exception as _e:
                print(f"  [upscale] history API hiccup: {_e}")  # transient — try fallback

            # ── Fallback: scan output_dir for file matching our unique prefix ──
            for p in output_dir.rglob("*.mp4"):
                if expected_prefix in p.name and p.stat().st_size > 0:
                    print(f"  [upscale] fallback found: {p}")
                    out_video_path = p
                    break
            if out_video_path:
                break

        else:
            raise RuntimeError("Timeout: upscale job did not complete within 40 minutes")

        if out_video_path is None or not out_video_path.exists():
            raise RuntimeError(
                f"Output file not found: {out_video_path}. "
                f"Checked ComfyUI output: {video_dir}"
            )

        # 6. Wait until ComfyUI finishes writing the file (size must stabilize).
        #    For long videos (26s+) ComfyUI keeps encoding after reporting job done.
        #    Poll every 2s; require 3 stable consecutive readings; max wait 120s.
        stable = await _wait_for_stable_file(out_video_path, poll_interval=2.0, stable_rounds=3, max_wait=120.0)
        file_size = out_video_path.stat().st_size if out_video_path.exists() else 0
        if not stable or file_size < 1024:
            raise RuntimeError(
                f"Output file incomplete after wait: {out_video_path.name} "
                f"({file_size} bytes) — ComfyUI może mieć OOM lub plik urwany"
            )

        # 7. Archive original (with _beforeupscale label)
        #    Done AFTER the wait so the original is still intact if step 8 fails.
        #    Non-fatal: some paths (e.g. CapCut junction-backed folders) reject mkdir.
        #    Log the warning but proceed — user loses the backup, not the upscale.
        try:
            _archive_before_upscale(source_path, clip_type)
        except Exception as _arch_err:
            print(f"  ⚠ Archiwizacja pominięta ({_arch_err}); kontynuuję upscale bez kopii zapasowej")

        # 8. Copy upscaled file to original path, then delete source.
        #    Strategy: copy2 to a temp file in dest dir → atomic rename → delete source.
        #    This avoids leaving an empty file if ComfyUI still holds a partial lock.
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_dest = dest_path.parent / f"_tmp_upscale_{dest_path.name}"

        copied = False
        last_err: Exception | None = None
        for attempt in range(8):          # up to 8 × 2 s = 16 s of retries
            try:
                shutil.copy2(str(out_video_path), str(tmp_dest))
                copied = True
                break
            except PermissionError as e:
                last_err = e
                if tmp_dest.exists():
                    try:
                        tmp_dest.unlink()
                    except Exception:
                        pass
                await asyncio.sleep(2)

        if not copied:
            raise RuntimeError(
                f"Nie można odczytać pliku wyjściowego ComfyUI "
                f"(zablokowany przez Windows po {8 * 2}s): {last_err}"
            )

        # Sanity check — verify the copy is not empty
        copied_size = tmp_dest.stat().st_size if tmp_dest.exists() else 0
        if copied_size < 1024:
            tmp_dest.unlink(missing_ok=True)
            raise RuntimeError(
                f"Skopiowany plik jest pusty lub uszkodzony ({copied_size} bytes): {tmp_dest.name}"
            )

        # Atomically replace dest (same drive → rename is instant, no empty-file risk)
        if dest_path.exists():
            dest_path.unlink()
        tmp_dest.rename(dest_path)

        # Delete source from ComfyUI output dir
        try:
            out_video_path.unlink()
        except Exception:
            pass   # not critical

        # 9. Invalidate thumbnail cache
        _invalidate_thumb(dest_path)

        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({
            "status":      "done",
            "output_name": clip_name,
            "elapsed_s":   elapsed,
        })

    except Exception as exc:
        _state.update({
            "status": "error",
            "error":  str(exc),
        })

    finally:
        try:
            if tmp_in.exists():
                tmp_in.unlink()
        except Exception:
            pass


def _invalidate_thumb(video_path: Path) -> None:
    """Delete cached thumbnail so it gets re-extracted on next request."""
    thumb = video_path.parent.parent / "frames" / f"{video_path.stem}_thumb.jpg"
    try:
        if thumb.exists():
            thumb.unlink()
    except Exception:
        pass


# ── Public API ───────────────────────────────────────────────────────────────

def start_upscale(
    run_filename: str,
    clip_name:    str,
    clip_type:    str,
    width:        int,
    height:       int,
) -> dict:
    """
    Queue an upscale job.  Returns immediately.

    clip_type: "generated" (transition/chain) or "external" (source video in project_folder)
    Returns {"ok": True} or {"ok": False, "error": "..."}.
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Upscale jest już w toku"}

    if width < 64 or width > 8192 or height < 64 or height > 8192:
        return {"ok": False, "error": "Wymiary muszą być między 64 a 8192"}

    # Resolve source path based on clip type
    if clip_type == "external":
        source_path = resolve_source_video(run_filename, clip_name)
        if source_path is None:
            return {"ok": False, "error": f"Nie znaleziono pliku zewnętrznego: {clip_name}"}
    else:
        source_path = resolve_video(run_filename, clip_name)
        if source_path is None:
            return {"ok": False, "error": f"Nie znaleziono klipu: {clip_name}"}

    dest_path = source_path   # upscaled replaces original (after archiving)

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "clip_name":    clip_name,
        "width":        width,
        "height":       height,
        "started_at":   time.time(),
    })

    # Schedule async task (must be called from within a running event loop — FastAPI guarantees this)
    try:
        _task = asyncio.create_task(
            _run_upscale(source_path, dest_path, run_filename, clip_name, clip_type, width, height)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}


def cancel_upscale() -> dict:
    """Cancel the running upscale job (best-effort)."""
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


# ── Lanczos (ffmpeg) upscale ─────────────────────────────────────────────────

async def _run_lanczos_upscale(
    source_path:  Path,
    dest_path:    Path,
    run_filename: str,
    clip_name:    str,
    clip_type:    str,
    width:        int,
    height:       int,
) -> None:
    """
    Fast Lanczos resize using ffmpeg (no ComfyUI required).
    Resizes `source_path` to WxH and replaces it in-place (with archive backup).
    """
    import subprocess as _sp

    loop = asyncio.get_running_loop()
    ts   = datetime.now().strftime("%Y%m%d%H%M%S")
    tmp_out = source_path.parent / f"_tmp_lanczos_{ts}_{source_path.name}"

    try:
        _state["status"] = "running"

        def _ffmpeg():
            cmd = [
                "ffmpeg",
                "-i", str(source_path),
                "-vf", f"scale={width}:{height}:flags=lanczos",
                "-c:v", "libx264",
                "-crf", "18",
                "-preset", "slow",
                "-c:a", "copy",
                "-movflags", "+faststart",
                "-y",
                str(tmp_out),
            ]
            result = _sp.run(cmd, capture_output=True)
            if result.returncode != 0:
                err = result.stderr.decode("utf-8", errors="replace")[-500:]
                raise RuntimeError(f"ffmpeg exited {result.returncode}: {err}")

        await loop.run_in_executor(None, _ffmpeg)

        if not tmp_out.exists() or tmp_out.stat().st_size < 1024:
            raise RuntimeError(f"ffmpeg produced no output: {tmp_out}")

        # Archive original
        _archive_before_upscale(source_path, clip_type)

        # Replace original with resized file
        if dest_path.exists():
            dest_path.unlink()
        tmp_out.rename(dest_path)

        # Invalidate thumbnail
        _invalidate_thumb(dest_path)

        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({
            "status":      "done",
            "output_name": clip_name,
            "elapsed_s":   elapsed,
        })

    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})
    finally:
        try:
            if tmp_out.exists():
                tmp_out.unlink()
        except Exception:
            pass


def start_lanczos_upscale(
    run_filename: str,
    clip_name:    str,
    clip_type:    str,
    width:        int,
    height:       int,
) -> dict:
    """
    Queue a Lanczos (ffmpeg) resize job.  Returns immediately.

    clip_type: "generated" (transition/chain) or "external" (source video in project_folder)
    Returns {"ok": True} or {"ok": False, "error": "..."}.
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Upscale jest już w toku"}

    if width < 64 or width > 8192 or height < 64 or height > 8192:
        return {"ok": False, "error": "Wymiary muszą być między 64 a 8192"}

    # Resolve source path based on clip type
    if clip_type == "external":
        source_path = resolve_source_video(run_filename, clip_name)
        if source_path is None:
            return {"ok": False, "error": f"Nie znaleziono pliku zewnętrznego: {clip_name}"}
    else:
        source_path = resolve_video(run_filename, clip_name)
        if source_path is None:
            return {"ok": False, "error": f"Nie znaleziono klipu: {clip_name}"}

    dest_path = source_path  # resized replaces original (after archiving)

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "clip_name":    clip_name,
        "width":        width,
        "height":       height,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_lanczos_upscale(source_path, dest_path, run_filename, clip_name, clip_type, width, height)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}
