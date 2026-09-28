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
from utils.video_metadata import read_metadata, update_metadata

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
    """True if THIS FILE has lipsync baked into its current (frame-locked)
    audio track. Callers (MMAudio FX generation, deblur's audio classification)
    use this to redirect FX into a side file instead of muxing into the mp4
    and clobbering the dialogue - see app/api/audio.py, deblur_service.py.

    Primary signal: the lipsync_applied metadata tag written by
    _replace_original on every successful run (utils/video_metadata.py,
    embedded in the mp4 itself - travels with the file, survives renames,
    and crucially does NOT survive a delete+regenerate under the same
    filename, unlike a sibling archive file would).

    Falls back to the old sibling-archive glob ONLY when the tag is absent
    (a clip lipsynced before this metadata tag existed) - this fallback is
    known to be imprecise (2026-09-15: a stale _beforelipsync archive left
    over from a deleted-and-regenerated clip falsely reported "already
    lipsynced" and made "Generuj zaznaczone" silently skip it) but removing
    it outright would regress every already-lipsynced clip predating this
    fix to "not lipsynced". Every fresh lipsync run from now on stamps the
    tag, so the false-positive window closes clip-by-clip as each one gets
    touched again."""
    meta = read_metadata(video_path)
    if "lipsync_applied" in meta:
        return meta.get("lipsync_applied") is True
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


async def _replace_original(source_result: Path, video_path: Path, dest_path: Path, sync_lips: bool = True) -> None:
    """Archive the original, then atomically replace dest_path with
    source_result (temp copy + rename, retrying on Windows file locks).
    Shared by both the LatentSync path and the voice-over-mux fast path.

    Stamps lipsync_applied=True (+ lipsync_sync_lips, lipsync_ts) into the
    NEW file's own metadata (utils/video_metadata.py) once the swap lands -
    see has_lipsync_applied for why this replaced the old sibling-archive-glob
    heuristic as the primary signal (2026-09-15 fix)."""
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

    try:
        update_metadata(
            dest_path,
            lipsync_applied=True,
            lipsync_sync_lips=bool(sync_lips),
            lipsync_ts=datetime.now().strftime("%Y%m%d%H%M%S"),
        )
    except Exception as _meta_err:
        print(f"  WARN: Zapis metadanych lipsync pominiety ({_meta_err})")

    _invalidate_thumb(dest_path)


async def _mux_voiceover(
    video_path:    Path,
    audio_path:    Path,
    trim_to_audio: bool = False,
    on_progress:   Callable[..., None] | None = None,
) -> Path:
    """Fast path for dialogue that doesn't need lip-sync (voice from off-screen)
    - no LatentSync/GPU inference, just mux the audio directly into the clip
    via ffmpeg (-c:v copy - lossless, seconds instead of ~90-150s on GPU).
    Returns the muxed temp file's path - no archiving, caller owns the result
    (extracted out of _voiceover_mux_core 2026-09-15, same reasoning as
    _submit_latentsync: multi-talk needs this per-segment without each
    segment archiving anything).
    trim_to_audio=False (default) keeps the clip's own duration, padding/
    truncating the voice track instead (see _normalize_audio_length);
    trim_to_audio=True lets -shortest reshape to whichever is shorter."""
    loop = asyncio.get_running_loop()
    if on_progress:
        on_progress(status="running")

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    tmp_audio = video_path.parent / f"_tmp_voice_audio_{ts}{audio_path.suffix}"
    tmp_mux = video_path.parent / f"_tmp_voice_mux_{ts}{video_path.suffix}"

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

        return tmp_mux

    finally:
        try:
            if tmp_audio.exists():
                tmp_audio.unlink()
        except Exception:
            pass


async def _voiceover_mux_core(
    video_path:    Path,
    audio_path:    Path,
    dest_path:     Path,
    trim_to_audio: bool = False,
    on_progress:   Callable[..., None] | None = None,
) -> None:
    """Single-clip wrapper: mux + archive + replace in place. Same Model A
    protection as the synced path - the resulting file gets lipsync_applied
    stamped too (_replace_original doesn't distinguish synced vs off-screen
    dialogue, both are equally "frame-locked, don't let FX touch this track")."""
    tmp_mux = await _mux_voiceover(video_path, audio_path, trim_to_audio, on_progress)
    try:
        await _replace_original(tmp_mux, video_path, dest_path, sync_lips=False)
    finally:
        try:
            if tmp_mux.exists():
                tmp_mux.unlink()
        except Exception:
            pass


async def _submit_latentsync(
    video_path:      Path,
    audio_path:      Path,
    trim_to_audio:   bool = False,
    position_index:  int | None = None,
    on_progress:     Callable[..., None] | None = None,
) -> Path:
    """Submit one video+audio pair to the LatentSync ComfyUI graph and return
    the path to its stable, finished output file - no archiving, no touching
    dest_path, caller owns what happens to the result. Extracted out of
    _lipsync_clip_core (2026-09-15) so multi-talk orchestration can run this
    once per character/time-segment against temp sub-clips, without each
    segment going through its own archive-and-replace (that happens exactly
    once, on the final concatenated result - see start_lipsync_multi).

    position_index: None (default) = largest face. 0,1,2,... = Nth face
    left-to-right (see LatentSyncNode's position_index widget, WSL2 vendor
    patch in ComfyUI-LatentSyncWrapper, 2026-09-15)."""
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
        workflow["40"]["inputs"]["position_index"] = -1 if position_index is None else int(position_index)

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

        return out_video_path

    finally:
        for p in (tmp_video, tmp_audio):
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
    position_index:  int | None = None,
) -> None:
    """State-free single-clip lipsync pipeline (submit/archive/replace).
    Raises on failure. Reports progress via on_progress(**kwargs) instead of
    touching the module-level _state, so it's safe to call from chain_service's
    auto-lipsync-per-step integration as well as the standalone UI job (see
    _run_lipsync for the UI-facing wrapper that owns _state).

    sync_lips=False skips LatentSync entirely and takes the fast ffmpeg-mux
    path (_voiceover_mux_core) - for dialogue that doesn't need mouth sync
    (voice from off-screen).

    position_index: see _submit_latentsync. For multi-talk (2+ characters in
    one clip, each with their own time window), see start_lipsync_multi
    instead - this function always does the whole clip in one pass."""
    if not sync_lips:
        await _voiceover_mux_core(video_path, audio_path, dest_path, trim_to_audio, on_progress)
        return

    out_video_path = await _submit_latentsync(video_path, audio_path, trim_to_audio, position_index, on_progress)
    try:
        await _replace_original(out_video_path, video_path, dest_path, sync_lips=True)
    finally:
        try:
            out_video_path.unlink()
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
    position_index: int | None = None,
) -> None:
    """UI-facing wrapper around _lipsync_clip_core - reports progress into the
    module-level _state dict that the standalone lipsync panel/button polls."""
    def _on_progress(**kwargs) -> None:
        _state.update(kwargs)

    try:
        await _lipsync_clip_core(
            video_path, audio_path, dest_path, run_filename, clip_name,
            _on_progress, trim_to_audio, sync_lips, position_index,
        )
        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})


# ── Public API ───────────────────────────────────────────────────────────────

def start_lipsync(
    run_filename: str, clip_name: str, audio_name: str,
    trim_to_audio: bool = False, sync_lips: bool = True,
    position_index: int | None = None,
) -> dict:
    """Queue a manual lipsync job. Returns immediately.
    audio_name: filename relative to the run's project_folder root (same
    convention as talk's audio picker - see editModal.audioFiles).
    trim_to_audio: False (default) keeps the clip's own duration untouched -
    the dialogue track is padded/truncated to match instead. True reshapes
    the video to match the dialogue's length (old behavior).
    sync_lips: True (default) runs LatentSync. False takes the fast ffmpeg-mux
    path for voice from off-screen - no mouth sync, no GPU.
    position_index: None (default) = largest face. 0,1,2,... = Nth face
    left-to-right - multi-talk building block, see _lipsync_clip_core."""
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
            _run_lipsync(video_path, audio_path, dest_path, run_filename, clip_name, trim_to_audio, sync_lips, position_index)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}


# ── Multi-talk (2+ characters, each with their own time window) ─────────────
#
# Design (2026-09-15, updated 2026-09-16 - see memory
# project_multitalk_face_selection.md): the clip is split into as many time
# windows as there are assignments (= "dialog turns"), boundaries computed by
# summing each assignment's OWN audio duration in order (turn #1 covers
# [0, dur1], #2 covers [dur1, dur1+dur2], ... last one always runs to the
# clip's real end, never truncating video). List order is ONLY the time
# order - it is NOT the position order. Each assignment carries its own
# explicit position_index (Nth face left-to-right, chosen independently per
# turn in the UI), so the same person/position can speak multiple
# non-contiguous turns (e.g. position_index sequence 1,0,1 - osoba2 mowi,
# potem osoba1, potem znowu osoba2). Each window gets its own LatentSync pass
# against a temp trimmed sub-clip using that turn's position_index. Results
# are ffmpeg-concatenated back into one file, which THEN goes through the
# normal single archive-and-replace (one lipsync_applied stamp for the whole
# clip, not per segment). A hard cut at each splice boundary, deliberately no
# crossfade - LatentSync only touches a small masked mouth region, so two
# independent passes differ only there; crossfading pixels in that region
# risks a blurry double-mouth artifact worse than a one-frame hard cut.

def _compute_windows(durs: list[float], total_dur: float) -> list[tuple[float, float]]:
    """Turn a list of per-turn audio durations (in time order) into
    [(start,end), ...] windows - turn #1 covers [0, dur1], #2 covers
    [dur1, dur1+dur2], etc. The LAST window always extends to total_dur
    (never truncate the clip just because audio durations under/overshoot
    it). Single source of truth for both _multi_lipsync_core (the real job)
    and preview_face_positions (the face-preview tool) - see module note
    above; keeping this in one place means preview and reality can never
    silently compute different windows."""
    starts = []
    acc = 0.0
    for d in durs:
        starts.append(acc)
        acc += d
    ends = starts[1:] + [total_dur]
    return list(zip(starts, ends))


async def _multi_lipsync_core(
    video_path:      Path,
    dest_path:       Path,
    assignments:     list[dict],
    on_progress:     Callable[..., None] | None = None,
) -> None:
    """assignments: ordered list of {"audio_path": Path, "sync_lips": bool,
    "position_index": int}. List order = time order only (see module-level
    note above - position_index is independent per turn and can repeat).
    Raises on failure. State-free like _lipsync_clip_core - see
    _run_lipsync_multi for the UI-facing wrapper owning _state."""
    loop = asyncio.get_running_loop()
    if on_progress:
        on_progress(status="running")

    total_dur = await loop.run_in_executor(None, _get_duration_s, video_path)
    if total_dur <= 0:
        raise RuntimeError("Nie mozna odczytac dlugosci klipu")

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    work_dir = video_path.parent
    cleanup: list[Path] = []

    try:
        # 1. Time windows from each assignment's own audio duration, in order
        durs = []
        for a in assignments:
            d = await loop.run_in_executor(None, _get_duration_s, a["audio_path"])
            durs.append(d if d > 0 else 0.0)
        windows = _compute_windows(durs, total_dur)
        starts = [w[0] for w in windows]
        ends = [w[1] for w in windows]

        seg_results: list[Path] = []
        for i, (a, start_s, end_s) in enumerate(zip(assignments, starts, ends)):
            if on_progress:
                on_progress(status="running", current_segment=i + 1, total_segments=len(assignments))

            seg_len = max(0.05, end_s - start_s)
            seg_src = work_dir / f"_mt_{ts}_seg{i}{video_path.suffix}"
            cleanup.append(seg_src)

            def _trim(src=seg_src, start=start_s, length=seg_len) -> bool:
                cmd = ["ffmpeg", "-y", "-ss", f"{start:.3f}", "-i", str(video_path),
                       "-t", f"{length:.3f}", "-an",
                       "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(src)]
                r = subprocess.run(cmd, capture_output=True, timeout=120)
                return r.returncode == 0 and src.exists() and src.stat().st_size > 0

            if not await loop.run_in_executor(None, _trim):
                raise RuntimeError(f"Nie udalo sie przyciac segmentu {i + 1}/{len(assignments)}")

            if a.get("sync_lips", True) is not False:
                seg_result = await _submit_latentsync(
                    seg_src, a["audio_path"], trim_to_audio=False,
                    position_index=a.get("position_index", i),
                )
            else:
                seg_result = await _mux_voiceover(seg_src, a["audio_path"], trim_to_audio=False)
            cleanup.append(seg_result)
            seg_results.append(seg_result)

        # 2. Concat the per-segment results back into one continuous clip -
        # hard cut at each boundary, see module-level note above.
        # seg_results live in ComfyUI's own output tree (see _submit_latentsync),
        # NOT in work_dir - the concat list must reference them by absolute
        # path, not just filename, or ffmpeg's concat demuxer (running with
        # cwd=work_dir) silently can't find them.
        concat_list = work_dir / f"_mt_{ts}_concat.txt"
        cleanup.append(concat_list)
        concat_list.write_text(
            "\n".join(f"file '{p.resolve().as_posix()}'" for p in seg_results), encoding="utf-8",
        )
        concat_out = work_dir / f"_mt_{ts}_final{video_path.suffix}"
        cleanup.append(concat_out)

        def _concat() -> tuple[bool, str]:
            cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list.name,
                   "-c", "copy", concat_out.name]
            r = subprocess.run(cmd, capture_output=True, timeout=120, cwd=str(work_dir))
            # ffmpeg's version/config banner is always the first ~500+ chars of
            # stderr - the actual error is near the end, so take the tail, not
            # the head (a head-slice here previously hid every real error).
            return r.returncode == 0 and concat_out.exists() and concat_out.stat().st_size > 0, \
                r.stderr.decode(errors="ignore")[-500:]

        ok, err = await loop.run_in_executor(None, _concat)
        if not ok:
            raise RuntimeError(f"Nie udalo sie skleic segmentow: {err}")

        # 3. One archive-and-replace for the whole clip (one lipsync_applied
        # stamp, not per segment)
        await _replace_original(concat_out, video_path, dest_path, sync_lips=True)

    finally:
        for p in cleanup:
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


async def _run_lipsync_multi(
    video_path:   Path,
    dest_path:    Path,
    assignments:  list[dict],
    run_filename: str,
    clip_name:    str,
) -> None:
    """UI-facing wrapper around _multi_lipsync_core - reports progress into
    the module-level _state dict, same as _run_lipsync."""
    def _on_progress(**kwargs) -> None:
        _state.update(kwargs)

    try:
        await _multi_lipsync_core(video_path, dest_path, assignments, _on_progress)
        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})


def start_lipsync_multi(run_filename: str, clip_name: str, assignments: list[dict]) -> dict:
    """Queue a multi-talk lipsync job. Returns immediately.
    assignments: ordered list of {"audio": "<filename relative to project_folder>",
    "sync_lips"?: true, "position_index"?: int}. List order = time-window
    order only (assignment 0 covers the clip's start, derived from each
    assignment's own audio duration). position_index (0 = leftmost face,
    default = list index if omitted) is independent per turn and can repeat -
    see _multi_lipsync_core module note."""
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Lipsync jest już w toku"}

    if not assignments:
        return {"ok": False, "error": "Brak przypisań (audio + pozycja) dla multi-talk"}

    video_path = resolve_video(run_filename, clip_name)
    if video_path is None:
        return {"ok": False, "error": f"Nie znaleziono klipu: {clip_name}"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono project_folder dla tego RUN"}

    resolved: list[dict] = []
    for i, a in enumerate(assignments):
        audio_name = (a.get("audio") or "").strip()
        if not audio_name:
            return {"ok": False, "error": f"Przypisanie #{i + 1}: brak pliku audio"}
        audio_path = pf / audio_name
        if not audio_path.exists():
            return {"ok": False, "error": f"Nie znaleziono pliku audio: {audio_name}"}
        resolved.append({
            "audio_path":     audio_path,
            "sync_lips":      a.get("sync_lips", True) is not False,
            "position_index": a.get("position_index", i),
        })

    dest_path = video_path

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "clip_name":    clip_name,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_lipsync_multi(video_path, dest_path, resolved, run_filename, clip_name)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}


# ── Face-detect preview (2026-09-15) ──────────────────────────────────────────
# Diagnostic tool, no side effects on any clip: before queuing a multi-minute
# multi-talk job, let the user confirm which physical face position_index=N
# will actually pick. Runs the SAME FaceDetector.get_valid_faces_sorted used
# by the real LatentSync pass (WSL2 vendor patch, 2026-09-15) via a small
# dedicated ComfyUI node/workflow (_FaceDetectPreview.json), so the preview
# can never disagree with reality. Per dialog-turn windows are computed with
# the exact same _compute_windows helper the real multi-talk job uses.

_FACE_PREVIEW_WORKFLOW_PATH = Path(__file__).parent.parent.parent / "workflows" / "_FaceDetectPreview.json"


def _extract_frame_jpg(video_path: Path, timestamp_s: float) -> bytes:
    """Grab a single frame at timestamp_s as JPEG bytes - used to sample a
    representative frame from within a computed multi-talk time window
    (see _compute_windows), not just always frame 1 of the whole clip."""
    cmd = ["ffmpeg", "-y", "-ss", f"{max(0.0, timestamp_s):.3f}", "-i", str(video_path),
           "-vframes", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-q:v", "3", "pipe:1"]
    r = subprocess.run(cmd, capture_output=True, timeout=15)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f"Nie udalo sie wyciac klatki: {r.stderr.decode(errors='ignore')[-300:]}")
    return r.stdout


def _find_image_in_outputs(outputs: dict) -> dict | None:
    """Scan all output nodes for a SaveImage-style 'images' list (mirrors
    _find_video_in_outputs, but for the single-frame preview workflow)."""
    for node_out in outputs.values():
        if not isinstance(node_out, dict):
            continue
        for im in (node_out.get("images") or []):
            if isinstance(im, dict) and im.get("filename"):
                return im
    return None


async def _submit_face_preview(image_path: Path, threshold: float = 0.5) -> Path:
    """Submit a single frame to the FaceDetectPreviewNode workflow and
    return the path to the resulting annotated PNG. Same submit/poll
    pattern as _submit_latentsync, much lighter (single image, no audio,
    no video mux) - should complete in a few seconds once the model is
    warm in VRAM."""
    loop = asyncio.get_running_loop()
    _linux = app_config_service.get_backend("linux")
    lipsync_url = _linux.get("api_url")
    input_dir = Path(_linux["comfyui_input_dir"])
    output_dir = Path(_linux["comfyui_output_folder"]).parent

    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    tmp_name = f"facepreview_{ts}{image_path.suffix}"
    tmp_path = input_dir / tmp_name
    expected_prefix = f"facepreview_{ts}"

    try:
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(image_path), str(tmp_path))

        workflow = json.loads(_FACE_PREVIEW_WORKFLOW_PATH.read_text(encoding="utf-8"))
        workflow["10"]["inputs"]["image"] = tmp_name
        workflow["20"]["inputs"]["threshold"] = float(threshold)
        workflow["30"]["inputs"]["filename_prefix"] = f"facepreview/{expected_prefix}"

        def _submit():
            try:
                return _http_post(f"{lipsync_url}/prompt", {"prompt": workflow}, timeout=30)
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        f"Linux ComfyUI niedostepny ({lipsync_url}). "
                        f"Uruchom WSL2 ComfyUI i sprobuj ponownie."
                    ) from e
                raise

        await asyncio.sleep(0.5)
        resp: dict | None = None
        _submit_err: Exception | None = None
        for _attempt in range(3):
            try:
                resp = await loop.run_in_executor(None, _submit)
                if resp.get("prompt_id"):
                    break
                _submit_err = RuntimeError(f"ComfyUI did not return prompt_id: {resp}")
            except RuntimeError:
                raise
            except Exception as e:
                _submit_err = e
            if _attempt < 2:
                await asyncio.sleep(1.5)
        if not resp or not resp.get("prompt_id"):
            raise _submit_err or RuntimeError(f"ComfyUI did not return prompt_id: {resp}")
        prompt_id = resp["prompt_id"]

        out_image_path: Path | None = None
        max_polls = 60  # 60 x 2s = 2 min max - single-frame job, should take seconds
        for _ in range(max_polls):
            await asyncio.sleep(2)
            try:
                def _check_history():
                    return _http_get(f"{lipsync_url}/history/{prompt_id}")

                history = await loop.run_in_executor(None, _check_history)
                if prompt_id in history:
                    job = history[prompt_id]
                    outputs = job.get("outputs", {})
                    image_entry = _find_image_in_outputs(outputs)
                    if image_entry:
                        subfolder = image_entry.get("subfolder", "")
                        filename = image_entry["filename"]
                        candidate = output_dir / subfolder / filename
                        if candidate.exists():
                            out_image_path = candidate
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

            matches = [p for p in output_dir.rglob("*.png")
                       if expected_prefix in p.name and p.stat().st_size > 0]
            if matches:
                out_image_path = matches[0]
                break
        else:
            raise RuntimeError("Timeout: podglad twarzy nie zakonczyl sie w 2 minuty")

        if out_image_path is None or not out_image_path.exists():
            raise RuntimeError("Nie znaleziono wynikowego obrazka podgladu")

        stable = await _wait_for_stable_file(out_image_path, poll_interval=1.0, stable_rounds=2, max_wait=30.0)
        if not stable or out_image_path.stat().st_size < 256:
            raise RuntimeError(f"Plik podgladu niekompletny: {out_image_path.name}")

        return out_image_path

    finally:
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except Exception:
            pass


async def preview_face_positions(
    run_filename:  str,
    clip_name:     str,
    assignments:   list[dict],
    target_index:  int,
    threshold:     float = 0.5,
) -> bytes:
    """For assignments[target_index] (one multi-talk dialog turn), compute
    that turn's own time window EXACTLY the way _multi_lipsync_core will
    (via _compute_windows - same durations, same cumulative-sum math), grab
    the frame at that window's START (the moment position_index actually
    switches to this turn - turn #1 starts at frame 0, turn #N starts where
    turn #N-1 just ended - NOT the window's middle, which can be far from
    the switch and already drifted), run it through FaceDetectPreviewNode,
    and return the annotated PNG bytes.

    assignments: ordered list of {"audio": "<filename relative to
    project_folder>"} - only entries up to and including target_index
    matter (later ones don't affect this turn's own window start/end), but
    the caller may just pass the full step.lipsync_multi list as-is.
    For "Prosty" (single-audio) mode, pass a 1-item list and
    target_index=0 - the window's start is frame 0, same as the real
    single-clip lipsync path (LatentSync sees the whole clip)."""
    if target_index < 0 or target_index >= len(assignments):
        raise RuntimeError("Nieprawidlowy target_index dla podgladu twarzy")

    video_path = resolve_video(run_filename, clip_name)
    if video_path is None:
        raise RuntimeError(f"Nie znaleziono klipu: {clip_name}")
    pf = _project_folder(run_filename)
    if pf is None:
        raise RuntimeError("Nie znaleziono project_folder dla tego RUN")

    loop = asyncio.get_running_loop()
    total_dur = await loop.run_in_executor(None, _get_duration_s, video_path)
    if total_dur <= 0:
        raise RuntimeError("Nie mozna odczytac dlugosci klipu")

    durs: list[float] = []
    for a in assignments[:target_index + 1]:
        audio_name = (a.get("audio") or "").strip()
        audio_path = pf / audio_name if audio_name else None
        if audio_path is None or not audio_path.exists():
            durs.append(0.0)
            continue
        d = await loop.run_in_executor(None, _get_duration_s, audio_path)
        durs.append(d if d > 0 else 0.0)

    # Durations after target_index don't affect ITS window at all - pad so
    # _compute_windows' index math lines up with the full assignments list.
    all_durs = durs + [0.0] * (len(assignments) - len(durs))
    windows = _compute_windows(all_durs, total_dur)
    start_s, _end_s = windows[target_index]
    # Sample from the WINDOW'S START, not its middle: that's the actual
    # moment LatentSync switches to this turn's position_index (turn #1's
    # start = frame 0; turn #N's start = where turn #N-1 just ended) - the
    # frame we most need to see is the one right at that switch, not
    # sometime later into the turn where framing may already have drifted.
    sample_s = start_s

    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    tmp_frame = video_path.parent / f"_fp_{ts}.jpg"
    try:
        jpg_bytes = await loop.run_in_executor(None, _extract_frame_jpg, video_path, sample_s)
        tmp_frame.write_bytes(jpg_bytes)

        out_path = await _submit_face_preview(tmp_frame, threshold)
        return out_path.read_bytes()
    finally:
        try:
            if tmp_frame.exists():
                tmp_frame.unlink()
        except Exception:
            pass
