# -*- coding: utf-8 -*-
"""
Lipsync service — V2V dialogue lipsync using LatentSync 1.5
(ComfyUI-LatentSyncWrapper), running on the Linux/WSL2 ComfyUI instance
(same backend as LtxBackend/deblur, port 8189).

Takes an already-generated clip plus a separate dialogue .mp3/.wav, and
replaces only the mouth region to match the audio. Background, body, and
camera motion are untouched by the node itself.

Unlike deblur, the result's audio track is NOT reconciled against the
source's prior audio (see deblur_service._fix_audio_track) — the whole
point of lipsync is that the dialogue track becomes the clip's permanent,
frame-locked audio ("Model A": lipsync bakes in, FX/ambient stay as side
files that can be freely regenerated without ever risking desync of the
lips). VHS_VideoCombine mixes in exactly the audio LatentSync just used to
drive the sync (workflow node 40 -> 50), discarding whatever the clip's
audio track held before.

Flow (mirrors deblur_service.py, single-clip - no chunking; LatentSync
1.5 is fast enough on an 8s clip that VRAM headroom hasn't required it):
  1. Copy clip + audio -> ComfyUI input dir (unique temp names)
  2. Build workflow from template (swap video/audio filenames)
  3. POST to ComfyUI /prompt
  4. Poll /history/{prompt_id} until done, with directory-scan fallback
  5. Wait for the output file size to stabilize
  6. Archive original (_ver{timestamp}_beforelipsync) -> replace with result
"""

import asyncio
import json
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

from app.services import app_config_service
from app.services.deblur_service import (
    _http_post,
    _http_get,
    _find_video_in_outputs,
    _wait_for_stable_file,
    _invalidate_thumb,
)
from app.services.media_service import resolve_video, _project_folder

_WORKFLOW_PATH = Path(__file__).parent.parent.parent / "workflows" / "_LatentSync_V2V.json"

# ── Global job state (standalone UI panel / manual 🗣 trigger) ───────────────

_state: dict = {
    "status":       "idle",   # idle | queued | running | done | error
    "prompt_id":    None,
    "run_filename": None,
    "clip_name":    None,
    "error":        None,
    "started_at":   None,
    "elapsed_s":    None,
}

_task: asyncio.Task | None = None


def get_lipsync_status() -> dict:
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
        "error":        None,
        "started_at":   None,
        "elapsed_s":    None,
    })


def cancel_lipsync() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


def _get_duration_s(path: Path) -> float:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, timeout=15, text=True,
        )
        return float(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else 0.0
    except Exception:
        return 0.0


def _normalize_audio_length(audio_path: Path, target_dur_s: float, dest: Path) -> bool:
    """Pad with trailing silence (if shorter) or truncate (if longer) so the
    dialogue track matches the CLIP's own duration exactly - used whenever
    trim_to_audio=False (the default) so lipsync never changes the clip's
    length. Continuity matters here: later chain steps and exports assume
    this clip's original duration/last frame, and dialogue is often added
    after the whole film is already generated - a mismatched take should
    never be allowed to reshape the video."""
    try:
        cmd = ["ffmpeg", "-y", "-i", str(audio_path), "-af", "apad",
               "-t", f"{target_dur_s:.3f}", str(dest)]
        r = subprocess.run(cmd, capture_output=True, timeout=60)
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def has_lipsync_applied(video_path: Path) -> bool:
    """True if this clip has a _beforelipsync archive sitting next to it -
    i.e. lipsync has already been baked into its current (frame-locked)
    audio track. Callers (MMAudio FX generation) use this to redirect FX
    into a side file instead of muxing into the mp4 and clobbering the
    dialogue - see app/api/audio.py."""
    return any(video_path.parent.glob(
        f"{video_path.stem}_ver????????????_beforelipsync{video_path.suffix}"
    ))


def _archive_before_lipsync(source_path: Path) -> None:
    """Back up the original file before lipsync overwrites it - same pattern
    as deblur_service._archive_before_deblur, labeled _beforelipsync. Also
    used by the voice-over fast path (_voiceover_mux_core) - the marker
    doesn't distinguish synced vs off-screen dialogue, both are equally
    "frame-locked, don't let FX touch this track" for has_lipsync_applied."""
    ts = datetime.now().strftime("%y%m%d%H%M%S")
    backup_name = f"{source_path.stem}_ver{ts}_beforelipsync{source_path.suffix}"
    shutil.copy2(str(source_path), str(source_path.parent / backup_name))


async def _replace_original(source_result: Path, video_path: Path, dest_path: Path) -> None:
    """Archive the original, then atomically replace dest_path with
    source_result (temp copy + rename, retrying on Windows file locks).
    Shared by both the LatentSync path and the voice-over-mux fast path."""
    try:
        _archive_before_lipsync(video_path)
    except Exception as _arch_err:
        print(f"  WARN: Archiwizacja pominieta ({_arch_err}); kontynuuje bez kopii zapasowej")

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_dest = dest_path.parent / f"_tmp_lipsync_{dest_path.name}"

    copied = False
    last_err: Exception | None = None
    for _attempt in range(8):
        try:
            shutil.copy2(str(source_result), str(tmp_dest))
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
        raise RuntimeError(f"Nie mozna odczytac pliku wynikowego: {last_err}")

    copied_size = tmp_dest.stat().st_size if tmp_dest.exists() else 0
    if copied_size < 1024:
        tmp_dest.unlink(missing_ok=True)
        raise RuntimeError(f"Skopiowany plik jest pusty lub uszkodzony ({copied_size} bytes)")

    if dest_path.exists():
        dest_path.unlink()
    tmp_dest.rename(dest_path)

    _invalidate_thumb(dest_path)


async def _voiceover_mux_core(
    video_path:    Path,
    audio_path:    Path,
    dest_path:     Path,
    trim_to_audio: bool = False,
    on_progress:   Callable[..., None] | None = None,
) -> None:
    """Fast path for dialogue that doesn't need lip-sync (voice from off-screen)
    - no LatentSync/GPU inference, just mux the audio directly into the clip
    via ffmpeg (-c:v copy - lossless, seconds instead of ~90-150s on GPU).
    Same continuity guarantee as the synced path: trim_to_audio=False (default)
    keeps the clip's own duration, padding/truncating the voice track instead
    (see _normalize_audio_length); trim_to_audio=True lets -shortest reshape
    to whichever is shorter. Same Model A protection too - _archive_before_lipsync
    covers this file so has_lipsync_applied() redirects future FX to a side file."""
    loop = asyncio.get_running_loop()
    if on_progress:
        on_progress(status="running")

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    tmp_audio = dest_path.parent / f"_tmp_voice_audio_{ts}{audio_path.suffix}"
    tmp_mux = dest_path.parent / f"_tmp_voice_mux_{ts}.mp4"

    try:
        if trim_to_audio:
            audio_for_mux = audio_path
        else:
            video_dur = await loop.run_in_executor(None, _get_duration_s, video_path)
            normalized = video_dur > 0 and await loop.run_in_executor(
                None, _normalize_audio_length, audio_path, video_dur, tmp_audio
            )
            audio_for_mux = tmp_audio if normalized else audio_path

        def _mux() -> bool:
            cmd = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_for_mux),
                   "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
                   "-shortest", str(tmp_mux)]
            r = subprocess.run(cmd, capture_output=True, timeout=120)
            return r.returncode == 0 and tmp_mux.exists() and tmp_mux.stat().st_size > 0

        if not await loop.run_in_executor(None, _mux):
            raise RuntimeError("ffmpeg mux nieudany (voice-over)")

        await _replace_original(tmp_mux, video_path, dest_path)

    finally:
        for p in (tmp_audio, tmp_mux):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


async def _lipsync_clip_core(
    video_path:      Path,
    audio_path:      Path,
    dest_path:       Path,
    run_filename:    str,
    clip_name:       str,
    on_progress:     Callable[..., None] | None = None,
    trim_to_audio:   bool = False,
    sync_lips:       bool = True,
) -> None:
    """State-free lipsync pipeline (submit/poll/wait-stable/archive/replace).
    Raises on failure. Reports progress via on_progress(**kwargs) instead of
    touching the module-level _state, so it's safe to call from chain_service's
    auto-lipsync-per-step integration as well as the standalone UI job (see
    _run_lipsync for the UI-facing wrapper that owns _state).

    sync_lips=False skips LatentSync entirely and takes the fast ffmpeg-mux
    path (_voiceover_mux_core) - for dialogue that doesn't need mouth sync
    (voice from off-screen)."""
    if not sync_lips:
        await _voiceover_mux_core(video_path, audio_path, dest_path, trim_to_audio, on_progress)
        return

    loop = asyncio.get_running_loop()
    _linux = app_config_service.get_backend("linux")
    lipsync_url = _linux.get("api_url")
    input_dir = Path(_linux["comfyui_input_dir"])
    output_dir = Path(_linux["comfyui_output_folder"]).parent

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    tmp_video_name = f"lipsync_{ts}_{video_path.name}"
    tmp_audio_name = f"lipsync_{ts}_{audio_path.name}"
    tmp_video = input_dir / tmp_video_name
    tmp_audio = input_dir / tmp_audio_name
    expected_prefix = f"lipsync_{ts}"

    try:
        if on_progress:
            on_progress(status="running")

        # 1. Copy source clip -> ComfyUI input dir
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(video_path), str(tmp_video))

        # 1b. Dialogue audio -> ComfyUI input dir. Default (trim_to_audio=False):
        # the clip's own duration must never change, so pad/truncate the audio
        # to match the video instead of letting VideoLengthAdjuster/VHS_VideoCombine
        # shorten (or otherwise reshape) the video to fit a mismatched take - see
        # _normalize_audio_length. trim_to_audio=True keeps the old behavior
        # (video reshaped to match audio) as an explicit opt-in.
        if trim_to_audio:
            shutil.copy2(str(audio_path), str(tmp_audio))
        else:
            video_dur = await loop.run_in_executor(None, _get_duration_s, tmp_video)
            normalized = video_dur > 0 and await loop.run_in_executor(
                None, _normalize_audio_length, audio_path, video_dur, tmp_audio
            )
            if not normalized:
                shutil.copy2(str(audio_path), str(tmp_audio))  # fallback: use as-is

        # 2. Build workflow from template
        workflow = json.loads(_WORKFLOW_PATH.read_text(encoding="utf-8"))
        workflow["10"]["inputs"]["video"] = tmp_video_name
        workflow["20"]["inputs"]["audio"] = tmp_audio_name
        workflow["50"]["inputs"]["filename_prefix"] = f"video/{expected_prefix}"
        workflow["50"]["inputs"]["trim_to_audio"] = bool(trim_to_audio)

        # 3. Submit to ComfyUI. The files just copied above can briefly look
        # missing/invalid to ComfyUI (running in WSL2) even though shutil.copy2
        # already finished writing them on the Windows side - WSL2's DrvFs view
        # of a Windows-mounted directory can lag a moment behind external
        # writes (same race hit deblur_service - see the comment there). A
        # short settle delay plus a couple of retries clears it reliably.
        def _submit():
            try:
                return _http_post(f"{lipsync_url}/prompt", {"prompt": workflow}, timeout=30)
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        f"Linux ComfyUI niedostępny ({lipsync_url}). "
                        f"Uruchom WSL2 ComfyUI i spróbuj ponownie."
                    ) from e
                raise

        await asyncio.sleep(0.5)
        resp: dict | None = None
        _submit_err: Exception | None = None
        for _submit_attempt in range(3):
            try:
                resp = await loop.run_in_executor(None, _submit)
                if resp.get("prompt_id"):
                    break
                _submit_err = RuntimeError(f"ComfyUI did not return prompt_id: {resp}")
            except RuntimeError:
                raise  # ComfyUI isn't even up - retrying won't help
            except Exception as e:
                _submit_err = e
            if _submit_attempt < 2:
                await asyncio.sleep(1.5)
        if not resp or not resp.get("prompt_id"):
            raise _submit_err or RuntimeError(f"ComfyUI did not return prompt_id: {resp}")
        prompt_id = resp["prompt_id"]

        if on_progress:
            on_progress(prompt_id=prompt_id)

        # 4. Poll for completion (history API + directory fallback). VHS_VideoCombine
        # writes the silent draft video first, then muxes audio into a SEPARATE
        # "*-audio.mp4" file a moment later (history correctly reports the audio
        # one once it exists, but if the fallback dir-scan below fires before it
        # exists yet, grabbing the first same-prefix match silently returns the
        # audio-less draft - lipsync has no downstream audio reconciliation like
        # deblur's _fix_audio_track, so that draft would ship as the final result
        # with no audio at all, despite the sync itself having worked). Prefer a
        # "-audio" match whenever one exists; hold off on a plain match for a
        # grace period in case the audio-muxed version is still on its way.
        max_polls = 400  # 400 x 3s = 20 min max - LatentSync 1.5 is fast
        _AUDIO_GRACE_POLLS = 10  # ~30s to wait for the "-audio" file once a silent draft is seen
        out_video_path: Path | None = None
        _plain_fallback: Path | None = None
        _plain_fallback_polls = 0

        for _ in range(max_polls):
            await asyncio.sleep(3)

            try:
                def _check_history():
                    return _http_get(f"{lipsync_url}/history/{prompt_id}")

                history = await loop.run_in_executor(None, _check_history)

                if prompt_id in history:
                    job = history[prompt_id]
                    outputs = job.get("outputs", {})

                    video_entry = _find_video_in_outputs(outputs)
                    if video_entry:
                        subfolder = video_entry.get("subfolder", "")
                        filename = video_entry["filename"]
                        candidate = output_dir / subfolder / filename
                        if candidate.exists():
                            out_video_path = candidate
                            break

                    status_info = job.get("status", {})
                    if status_info.get("status_str") == "error":
                        msgs = status_info.get("messages", [])
                        err = next(
                            (m[1].get("exception_message", str(m))
                             for m in msgs if m[0] == "execution_error"),
                            "ComfyUI reported an error",
                        )
                        raise RuntimeError(err)

            except RuntimeError:
                raise
            except Exception:
                pass  # transient - try fallback

            matches = [p for p in output_dir.rglob("*.mp4")
                       if expected_prefix in p.name and p.stat().st_size > 0]
            audio_match = next((p for p in matches if "-audio" in p.name), None)
            if audio_match:
                out_video_path = audio_match
            elif matches:
                if _plain_fallback is None:
                    _plain_fallback = matches[0]
                _plain_fallback_polls += 1
                if _plain_fallback_polls >= _AUDIO_GRACE_POLLS:
                    out_video_path = _plain_fallback  # audio never showed up - use the draft rather than fail
            if out_video_path:
                break
        else:
            raise RuntimeError("Timeout: lipsync job did not complete within 20 minutes")

        if out_video_path is None or not out_video_path.exists():
            raise RuntimeError(f"Output file not found: {out_video_path}")

        # 5. Wait until ComfyUI finishes writing the file
        stable = await _wait_for_stable_file(out_video_path, poll_interval=2.0, stable_rounds=3, max_wait=120.0)
        file_size = out_video_path.stat().st_size if out_video_path.exists() else 0
        if not stable or file_size < 1024:
            raise RuntimeError(
                f"Output file incomplete after wait: {out_video_path.name} ({file_size} bytes)"
            )

        # 6-7. Archive original, then replace it with the ComfyUI result
        await _replace_original(out_video_path, video_path, dest_path)

        try:
            out_video_path.unlink()
        except Exception:
            pass

    finally:
        for p in (tmp_video, tmp_audio):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


async def _run_lipsync(
    video_path:    Path,
    audio_path:    Path,
    dest_path:     Path,
    run_filename:  str,
    clip_name:     str,
    trim_to_audio: bool = False,
    sync_lips:     bool = True,
) -> None:
    """UI-facing wrapper around _lipsync_clip_core - reports progress into the
    module-level _state dict that the standalone lipsync panel/button polls."""
    def _on_progress(**kwargs) -> None:
        _state.update(kwargs)

    try:
        await _lipsync_clip_core(
            video_path, audio_path, dest_path, run_filename, clip_name,
            _on_progress, trim_to_audio, sync_lips,
        )
        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})


# ── Public API ───────────────────────────────────────────────────────────────

def start_lipsync(
    run_filename: str, clip_name: str, audio_name: str,
    trim_to_audio: bool = False, sync_lips: bool = True,
) -> dict:
    """Queue a manual lipsync job. Returns immediately.
    audio_name: filename relative to the run's project_folder root (same
    convention as talk's audio picker - see editModal.audioFiles).
    trim_to_audio: False (default) keeps the clip's own duration untouched -
    the dialogue track is padded/truncated to match instead. True reshapes
    the video to match the dialogue's length (old behavior).
    sync_lips: True (default) runs LatentSync. False takes the fast ffmpeg-mux
    path for voice from off-screen - no mouth sync, no GPU."""
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Lipsync jest już w toku"}

    video_path = resolve_video(run_filename, clip_name)
    if video_path is None:
        return {"ok": False, "error": f"Nie znaleziono klipu: {clip_name}"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono project_folder dla tego RUN"}
    audio_path = pf / audio_name
    if not audio_path.exists():
        return {"ok": False, "error": f"Nie znaleziono pliku audio: {audio_name}"}

    dest_path = video_path  # lipsync result replaces original (after archiving)

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "clip_name":    clip_name,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_lipsync(video_path, audio_path, dest_path, run_filename, clip_name, trim_to_audio, sync_lips)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}
