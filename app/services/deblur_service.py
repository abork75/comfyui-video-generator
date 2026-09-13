# -*- coding: utf-8 -*-
"""
Deblur service — sharpens a single generated (or external) video clip using an
LTX 2.3 IC-LoRA "deblur" pass, running on the Linux/WSL2 ComfyUI instance
(same backend as LtxBackend, port 8189).

Always applicable — the tool sharpens whatever clip it's given, regardless of
which model originally generated it (WAN, LTX, or an external source video).

The deblur workflow only has a full (non-GGUF) fp8 LTX 2.3 22B UNET — on a
16GB card ComfyUI has to stream ~24GB of weights, which is slow but works for
short clips and stalls (VRAM exhausted by activations on top of the streamed
weights) past roughly 10-15s. To route around that without reworking the
workflow's sampler for a quantized model, clips longer than ~8s are split into
near-equal chunks (none over _MAX_CHUNK_S), deblurred one at a time, then re-joined.

Flow (mirrors upscale_service.py, adapted for the linux/WSL2 backend and the
deblur workflow):
  0. If duration > _MAX_CHUNK_S: split source into N near-equal chunks (frame-accurate,
     video-only) via ffmpeg, each processed as its own job below.
  1. Copy (chunk) clip -> ComfyUI input dir (unique temp name)
  2. Extract its first frame -> feeds the workflow's LoadImage node (needed
     even though that node is labeled unused — ComfyUI still validates it)
  3. Build workflow from template (swap file, prompts, seed, lora strength)
  4. POST to ComfyUI /prompt
  5. Poll /history/{prompt_id} until done (every 3 s, max 40 min), with a
     directory-scan fallback keyed on a unique filename_prefix
  6. Wait for the output file size to stabilize (long clips keep encoding
     after ComfyUI reports the job done)
  7. If multiple chunks: concatenate the per-chunk outputs (stream copy)
  8. Archive original (_ver{timestamp}_beforedeblur) -> replace with corrected clip
  9. Clean up all temp chunk/input/frame files

LTX 2.3 is a joint audio/video model — fed a silent clip it still generates an
audio track from an empty latent (LTXVEmptyLatentAudio), i.e. hallucinated
noise/music the source never had.

2026-09-09 audio architecture (see _classify_source_audio, _fix_main_track):
a clip's own mp4 audio track is either SILENCE or real lipsync DIALOGUE —
tertium non datur. FX/ambience never lives in the main track; it's always a
standalone side file at utils.mmaudio_utils.fx_sidecar_path, exactly like a
real MMAudio generation now also always uses (see app/api/audio.py). Deblur
gets this for free from the hallucination it already produces:
  - Clip has no audio at all + no FX sidecar yet: the hallucination IS
    steered (appended onto the joint text conditioning via
    _find_flow_audio_prompt — the workflow has no separate audio-only prompt
    node — falling back to the run's default_audio_prompt or a hardcoded
    fallback, resolved in-flight and never written back to the step's YAML)
    and saved as the sidecar. This is a real MMAudio generation avoided for
    free — no extra model load, no extra pass.
  - Clip already has real dialogue (talk/multitalk tile, or a chain clip
    with has_lipsync_applied): main track keeps that dialogue untouched, and
    the hallucination isn't even steered (fx_prompt stays unset) since it'll
    just be discarded.
  - Clip has SOME audio but no lipsync marker ("legacy_fx" — chain clips
    from before this convention existed): assumed to be old audio baked
    straight into the main track. Migrated (not regenerated — the SOURCE's
    own existing audio is what gets moved) into the sidecar on first touch,
    main track goes silent. This classification is only safe because every
    clip that could be real dialogue despite lacking the marker (made via a
    manual LTX-lipsync workflow before lipsync_service existed — e.g.
    RUN_022) has been retroactively marked with the same _beforelipsync
    convention. Never re-narrow this without redoing that retro-mark pass.
  - An FX sidecar already exists: never touched, never overwritten — a real
    manually-triggered MMAudio run always wins over deblur's free byproduct.
"""

import asyncio
import copy
import json
import math
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Callable

from app.services import app_config_service
from app.services.media_service import resolve_video, resolve_source_video, _extract_video_frame, _project_folder
from app.services.multitalk_service import _concatenate_clips
from utils.video_utils import get_video_info
from utils.video_metadata import update_metadata
from utils.mmaudio_utils import fx_sidecar_path, FALLBACK_AUDIO_PROMPT, FALLBACK_AUDIO_NEG_PROMPT

_WORKFLOW_PATH = Path(__file__).parent.parent.parent / "workflows" / "_LTX23_Deblur.json"

_DEFAULT_POS_PROMPT = (
    "The same shot as the reference video. Same person, same face, same clothes, "
    "same body, same background. Restore sharp focus and fine surface detail. "
    "Do not change identity, wardrobe, hair, or scene layout."
)
_DEFAULT_NEG_PROMPT = (
    "pc game, console game, video game, cartoon, childish, ugly, different clothes, "
    "different person, extra head, extra person, warped face, new background"
)

_MAX_CHUNK_S = 8.2  # clips longer than this get split; +0.2s (~4-5 frames at 24-25fps)
                     # so an 8s clip with a few extra encoder-rounding frames doesn't
                     # spuriously split

# Identifies which base checkpoint the Deblur workflow was wired to when this
# job ran - bump this string whenever _LTX23_Deblur.json's node 3940/2199
# checkpoint choice changes, so has_deblur_applied(checkpoint=...) can tell a
# deblur done on an since-superseded checkpoint from a current one.
_DEBLUR_CHECKPOINT_ID = "dev-UD-Q5_K_M+distilled-1.1-lora-0.61"

# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":        "idle",   # idle | queued | running | done | error
    "prompt_id":     None,
    "run_filename":  None,
    "clip_name":     None,
    "error":         None,
    "started_at":    None,
    "elapsed_s":     None,
    "chunk_current": None,     # 1-based index of the chunk being processed
    "chunk_total":   None,     # total number of chunks (None/1 = not chunked)
}

_task: asyncio.Task | None = None


def get_deblur_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("running", "queued"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":        "idle",
        "prompt_id":     None,
        "run_filename":  None,
        "clip_name":     None,
        "error":         None,
        "started_at":    None,
        "elapsed_s":     None,
        "chunk_current": None,
        "chunk_total":   None,
    })


def cancel_deblur() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


# ── HTTP helpers (sync, called via run_in_executor) ──────────────────────────

def _http_post(url: str, payload: dict, timeout: int = 15) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _http_get(url: str, timeout: int = 10) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


# ── Chunk planning & extraction ───────────────────────────────────────────────

def _plan_chunks(frame_count: int, fps: float, max_chunk_s: float = _MAX_CHUNK_S) -> list[tuple[int, int]]:
    """
    Split [0, frame_count) into the fewest near-equal chunks such that none
    exceeds max_chunk_s. E.g. at max_chunk_s=6: 10s -> 2x5s, 11s -> 2x5.5s,
    15s -> 3x5s. Returns [(start_frame, num_frames), ...].
    """
    duration = frame_count / fps if fps > 0 else 0.0
    n = 1 if duration <= max_chunk_s else math.ceil(duration / max_chunk_s)
    boundaries = [round(i * frame_count / n) for i in range(n + 1)]
    boundaries[-1] = frame_count  # guard against rounding drift on the last chunk
    return [(boundaries[i], boundaries[i + 1] - boundaries[i]) for i in range(n)]


def _extract_chunk(source: Path, dest: Path, start_frame: int, num_frames: int, fps: float) -> bool:
    """Cut [start_frame, start_frame+num_frames) from source into dest (video-only,
    re-encoded for frame accuracy — the deblur workflow only reads frames, not audio)."""
    start_s = start_frame / fps
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{start_s:.6f}", "-i", str(source),
             "-vframes", str(num_frames), "-an",
             "-c:v", "libx264", "-crf", "15", "-preset", "fast",
             str(dest)],
            capture_output=True, timeout=120,
        )
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def _snap_length_up(num_frames: int) -> int:
    """Round num_frames UP to the nearest 8k+1 - the latent length LTX's
    EmptyLTXVLatentVideo actually honors (it silently floors any other value
    via ((length-1)//8)+1 latent frames, see nodes_lt.py). Rounding down would
    permanently drop real source frames from the deblurred output; rounding up
    means the workflow generates a few extra frames that _trim_video_frames
    then cuts back off after generation, so the corrected clip ends up with
    exactly num_frames again."""
    return ((num_frames + 6) // 8) * 8 + 1


def _trim_video_frames(source: Path, dest: Path, num_frames: int) -> bool:
    """Re-encode source down to exactly num_frames video frames (from the
    start), keeping the audio track in sync via -shortest. Used to correct
    for LTX's length-snapping (see _snap_length_up) so the final deblurred
    clip matches the source's frame count/duration exactly."""
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", str(source),
             "-vframes", str(num_frames),
             "-c:v", "libx264", "-crf", "15", "-preset", "fast",
             "-c:a", "copy", "-shortest",
             str(dest)],
            capture_output=True, timeout=120,
        )
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def _has_audio(path: Path) -> bool:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
            capture_output=True, timeout=10,
        )
        return r.returncode == 0 and b"audio" in r.stdout
    except Exception:
        return False


def _classify_source_audio(source_path: Path) -> str:
    """Classify what source_path's existing audio track actually IS, so
    deblur's audio reconciliation can honor the 2026-09-09 invariant: a
    clip's own mp4 audio track is EITHER silence OR real lipsync dialogue,
    tertium non datur — FX always lives in a side file (utils.mmaudio_utils.
    fx_sidecar_path), never baked into the main track. See module docstring.

    Returns:
      "none"      — no audio at all.
      "dialogue"  — real speech: talk/multitalk tiles are dialogue by
                    construction, or a chain clip with has_lipsync_applied.
      "legacy_fx" — a chain clip that HAS audio but no lipsync marker — from
                    before this invariant existed, safe to assume it's old
                    baked-in FX and migrate it to a sidecar. This is ONLY
                    safe because every clip that could be real dialogue
                    despite lacking the marker (made via a manual LTX-lipsync
                    workflow, before the real lipsync_service tool existed —
                    e.g. RUN_022) has been retroactively marked with the same
                    _beforelipsync convention — see the 2026-09-09 retro-mark
                    note. Do not weaken this classification without redoing
                    that retroactive pass first.
    """
    if not _has_audio(source_path):
        return "none"
    parent = source_path.parent.name  # "chains" | "talks" | "multitalk"
    if parent in ("talks", "multitalk"):
        return "dialogue"
    try:
        from app.services.lipsync_service import has_lipsync_applied  # lazy: circular import
        if has_lipsync_applied(source_path):
            return "dialogue"
    except Exception:
        pass
    return "legacy_fx"


def _extract_audio_to_mp3(video_path: Path, dest_mp3: Path) -> bool:
    """Pull video_path's own audio track out as a standalone mp3 - used to
    save the deblur workflow's hallucinated audio (steered by the step's
    audio_prompt into deliberate FX - see _find_flow_audio_prompt) as a real
    MMAudio-equivalent side file, reusing the exact same location convention
    as utils.mmaudio_utils.fx_sidecar_path so it's indistinguishable from a
    genuine MMAudio-after-lipsync run (see 2026-09-09 note in module docstring)."""
    try:
        dest_mp3.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest_mp3.with_suffix(".tmp_fx.mp3")
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path), "-vn", "-q:a", "2", str(tmp)],
            capture_output=True, timeout=60,
        )
        if r.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
            tmp.unlink(missing_ok=True)
            return False
        tmp.replace(dest_mp3)
        return True
    except Exception:
        return False


def _fix_main_track(video_path: Path, source_path: Path, dest: Path, keep_dialogue: bool) -> bool:
    """Decide the deblurred clip's own MAIN-TRACK audio. FX never lives here
    any more (always a sidecar, see module docstring) — this only ever
    restores real dialogue or strips to silence:
      - keep_dialogue=True:  replace the hallucination with the source's own
                              real dialogue (dest video + source audio).
      - keep_dialogue=False: strip audio entirely — silence, whether the
                              source was already silent or had legacy FX
                              (which gets migrated to a sidecar separately,
                              see _classify_source_audio / _deblur_clip_core).
    """
    try:
        if keep_dialogue:
            cmd = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(source_path),
                   "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
                   "-shortest", str(dest)]
        else:
            cmd = ["ffmpeg", "-y", "-i", str(video_path),
                   "-map", "0:v:0", "-c:v", "copy", "-an", str(dest)]
        r = subprocess.run(cmd, capture_output=True, timeout=60)
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def _find_flow_audio_prompt(run_filename: str, source_path: Path, clip_name: str) -> tuple[str | None, str | None]:
    """Reverse-map a deblur clip back to its originating flow item, to reuse
    whatever audio_prompt/audio_negative_prompt was already entered there for
    MMAudio (chain/multichain steps, talk/multitalk tiles) instead of asking
    the user to type it again. Returns (None, None) if no match is found —
    the caller then falls back to stripping/restoring audio as before."""
    from app.services.run_file_service import get_run_flow

    flow_data = get_run_flow(run_filename)
    flow = (flow_data or {}).get("flow") or []
    parent = source_path.parent.name  # "chains" | "talks" | "multitalk"

    try:
        if parent == "chains":
            stem = source_path.stem
            prefix, sep, idx_s = stem.rpartition("_")
            if not sep or not idx_s.isdigit():
                return None, None
            idx = int(idx_s)
            for item in flow:
                if isinstance(item, dict) and item.get("chain_prefix") == prefix and "chain" in item:
                    steps = item["chain"]
                    if 1 <= idx <= len(steps) and isinstance(steps[idx - 1], dict):
                        step = steps[idx - 1]
                        return step.get("audio_prompt") or None, step.get("audio_negative_prompt") or None
            return None, None

        if parent == "multitalk":
            for item in flow:
                if isinstance(item, dict) and item.get("type") == "multitalk":
                    name = (item.get("name") or "").strip()
                    if name and not name.endswith(".mp4"):
                        name += ".mp4"
                    if name == clip_name:
                        return item.get("audio_prompt") or None, item.get("audio_negative_prompt") or None
            return None, None

        if parent == "talks":
            from app.services.chain_service import _talk_video_relpath
            for item in flow:
                if isinstance(item, dict) and item.get("type") == "talk":
                    if _talk_video_relpath(item).endswith(f"/{clip_name}"):
                        return item.get("audio_prompt") or None, item.get("audio_negative_prompt") or None
            return None, None
    except Exception:
        return None, None

    return None, None


# ── Background task ──────────────────────────────────────────────────────────

def _archive_before_deblur(source_path: Path, clip_type: str) -> None:
    """Back up the original file before deblurring - same pattern as upscale's
    _archive_before_upscale, labeled _beforedeblur so its origin is obvious."""
    ts = datetime.now().strftime("%y%m%d%H%M%S")
    backup_name = f"{source_path.stem}_ver{ts}_beforedeblur{source_path.suffix}"

    if clip_type == "external":
        backup_dir = source_path.parent / "source_backup"
        backup_dir.mkdir(exist_ok=True)
        shutil.copy2(str(source_path), str(backup_dir / backup_name))
    else:
        shutil.copy2(str(source_path), str(source_path.parent / backup_name))


def _find_video_in_outputs(outputs: dict) -> dict | None:
    """Scan ALL output nodes for any that contain a 'videos' list with mp4 files."""
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
    """Poll `path` until its size stops changing for `stable_rounds` consecutive
    readings. Catches ComfyUI reporting "done" while still encoding."""
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


async def _run_single_clip(
    loop: asyncio.AbstractEventLoop,
    deblur_url: str,
    input_dir: Path,
    output_dir: Path,
    clip_source: Path,
    ts_label: str,
    num_frames: int,
    fx_prompt: str | None = None,
    fx_negative_prompt: str | None = None,
    on_progress: Callable[..., None] | None = None,
) -> Path:
    """
    Run one clip through the deblur ComfyUI workflow end-to-end (copy in,
    extract first frame, submit, poll, wait-stable). Returns the ComfyUI
    output path (already trimmed back to num_frames, see _snap_length_up).
    Cleans up its own temp input+frame files; the caller owns cleanup of the
    returned output path.
    """
    tmp_name = f"deblur_{ts_label}_{clip_source.name}"
    tmp_in = input_dir / tmp_name
    frame_name = f"deblur_{ts_label}_{clip_source.stem}_frame0.jpg"
    tmp_frame = input_dir / frame_name

    try:
        expected_prefix = f"deblur_{ts_label}"

        # 1. Copy source -> ComfyUI input dir
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(clip_source), str(tmp_in))

        # 2. Extract first frame -> feeds the workflow's LoadImage node (2004).
        # That node is labeled "UNUSED (Deblur nie I2V)" but ComfyUI still
        # validates it as part of the graph, so it needs a real image file.
        if not await loop.run_in_executor(None, _extract_video_frame, tmp_in, tmp_frame):
            raise RuntimeError(f"Nie udało się wyciągnąć pierwszej klatki z {clip_source.name}")

        # 3. Build workflow from template
        workflow = json.loads(_WORKFLOW_PATH.read_text(encoding="utf-8"))
        workflow["5001"]["inputs"]["file"] = tmp_name
        workflow["2004"]["inputs"]["image"] = frame_name
        pos_prompt = _DEFAULT_POS_PROMPT + (f" Audio: {fx_prompt}." if fx_prompt else "")
        neg_prompt = _DEFAULT_NEG_PROMPT + (f", {fx_negative_prompt}" if fx_negative_prompt else "")
        workflow["2483"]["inputs"]["text"] = pos_prompt
        workflow["2612"]["inputs"]["text"] = neg_prompt
        workflow["4852"]["inputs"]["filename_prefix"] = f"video/{expected_prefix}"
        # Override the dynamic GetImageSize->length wiring (node 5029->3059):
        # EmptyLTXVLatentVideo silently floors "length" to the nearest 8k+1
        # latent-compatible value (nodes_lt.py: ((length-1)//8)+1), which -
        # left on the raw source frame count - was quietly truncating a few
        # frames off the end of every deblurred clip whose length wasn't
        # already of that form. Snap up instead (never lose real frames) and
        # trim the extra generated frames back off below once the job is done.
        snapped_length = _snap_length_up(num_frames)
        workflow["3059"]["inputs"]["length"] = snapped_length

        # 4. Submit to ComfyUI. The files just copied above can briefly look
        # missing/invalid to ComfyUI (running in WSL2) even though shutil.copy2
        # already finished writing them on the Windows side - WSL2's DrvFs view
        # of a Windows-mounted directory can lag a moment behind external
        # writes, which shows up as either a slow response (client-side
        # timeout here) or a "Invalid video/image file" validation error on
        # ComfyUI's side. A short settle delay plus a couple of retries clears
        # it reliably (confirmed: manually re-queuing the same job right after
        # a failure like this always works).
        def _submit():
            try:
                return _http_post(f"{deblur_url}/prompt", {"prompt": workflow}, timeout=30)
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        f"Linux ComfyUI niedostępny ({deblur_url}). "
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

        # 5. Poll for completion (history API + directory fallback). VHS_VideoCombine
        # writes the silent draft video first, then muxes audio (the LTX joint
        # audio/video hallucination) into a SEPARATE "*-audio.mp4" file a moment
        # later. History correctly reports the audio one once it exists, but if
        # the fallback dir-scan below fires before it exists yet, grabbing the
        # first same-prefix match can silently return the audio-less draft -
        # the FX-sidecar/_fix_main_track step then has no audio stream to
        # extract (degrades to its own WARN fallback further down). Prefer a "-audio" match whenever
        # one exists; hold off on a plain match for a grace period first.
        max_polls = 800  # 800 x 3s = 40 min max
        _AUDIO_GRACE_POLLS = 10  # ~30s to wait for the "-audio" file once a silent draft is seen
        out_video_path: Path | None = None
        _plain_fallback: Path | None = None
        _plain_fallback_polls = 0

        for _ in range(max_polls):
            await asyncio.sleep(3)

            try:
                def _check_history():
                    return _http_get(f"{deblur_url}/history/{prompt_id}")

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
            raise RuntimeError("Timeout: deblur job did not complete within 40 minutes")

        if out_video_path is None or not out_video_path.exists():
            raise RuntimeError(f"Output file not found: {out_video_path}")

        # 6. Wait until ComfyUI finishes writing the file
        stable = await _wait_for_stable_file(out_video_path, poll_interval=2.0, stable_rounds=3, max_wait=120.0)
        file_size = out_video_path.stat().st_size if out_video_path.exists() else 0
        if not stable or file_size < 1024:
            raise RuntimeError(
                f"Output file incomplete after wait: {out_video_path.name} ({file_size} bytes)"
            )

        # 6b. Trim back to num_frames if we asked the workflow to generate a
        # few extra frames to satisfy the 8k+1 latent-length snap above.
        if snapped_length != num_frames:
            trimmed_path = out_video_path.parent / f"{out_video_path.stem}_trimmed.mp4"
            ok = await loop.run_in_executor(
                None, _trim_video_frames, out_video_path, trimmed_path, num_frames
            )
            if ok:
                try:
                    out_video_path.unlink()
                except Exception:
                    pass
                out_video_path = trimmed_path
            else:
                print(
                    f"  WARN: Nie udalo sie przyciac nadmiarowych klatek "
                    f"({snapped_length} -> {num_frames}) na {out_video_path.name}; "
                    f"wynik moze byc o kilka klatek dluzszy niz zrodlo"
                )

        return out_video_path

    finally:
        for p in (tmp_in, tmp_frame):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


async def _deblur_clip_core(
    source_path:  Path,
    dest_path:    Path,
    run_filename: str,
    clip_name:    str,
    clip_type:    str,
    on_progress:  Callable[..., None] | None = None,
) -> None:
    """State-free deblur pipeline (chunk/generate/rejoin/fix-audio/archive/replace).
    Raises on failure. Reports progress via on_progress(**kwargs) instead of
    touching the module-level _state, so it's safe to call concurrently with
    (or independently of) the standalone UI deblur job - see _run_deblur for
    the UI-facing wrapper that does own _state, and the chain_service call
    site for the auto-deblur-per-step integration."""
    loop = asyncio.get_running_loop()
    _linux = app_config_service.get_backend("linux")
    deblur_url = _linux.get("api_url")
    input_dir = Path(_linux["comfyui_input_dir"])
    # comfyui_output_folder points at the Wan22_I2V subfolder - the deblur
    # workflow writes to its own "video/" subfolder under the ComfyUI base output dir.
    output_dir = Path(_linux["comfyui_output_folder"]).parent

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    chunk_sources: list[Path] = []   # cut fragments fed into ComfyUI (only when n>1)
    chunk_outputs: list[Path] = []   # ComfyUI outputs, one per chunk
    extra_temp_files: list[Path] = []  # concat/audio-fix intermediates

    try:
        info = await loop.run_in_executor(None, get_video_info, source_path)
        fps, frame_count = info["fps"], info["frame_count"]
        if fps <= 0 or frame_count <= 0:
            raise RuntimeError(f"Nie udało się odczytać metadanych wideo: {source_path.name}")

        chunks = _plan_chunks(frame_count, fps)
        n = len(chunks)

        # Free MMAudio-equivalent FX (2026-09-09, see module docstring and
        # _classify_source_audio): decide UP FRONT whether we'll actually
        # want to keep the hallucination as real FX, before generation even
        # starts - only then is it worth steering the joint LTX prompt with
        # an audio hint at all. Never overwrites an existing sidecar; never
        # touches a dialogue clip's audio.
        audio_class = _classify_source_audio(source_path)
        pf_for_audio = _project_folder(run_filename)
        fx_sidecar = fx_sidecar_path(pf_for_audio, source_path.name) if pf_for_audio is not None else None
        fx_action = None  # None | 'generate' | 'migrate'
        if fx_sidecar is not None and not fx_sidecar.exists():
            if audio_class == "none":
                fx_action = "generate"
            elif audio_class == "legacy_fx":
                fx_action = "migrate"

        fx_prompt, fx_negative_prompt = (None, None)
        if fx_action == "generate":
            fx_prompt, fx_negative_prompt = _find_flow_audio_prompt(run_filename, source_path, clip_name)
            if not fx_prompt:
                # In-flight fallback only - never written back to the step's
                # own audio_prompt field in the YAML (rule: "w locie, nigdzie
                # nie zapisywać"). Same 3-tier resolution as app/api/audio.py.
                from app.services.run_file_service import get_run_details
                run_defaults = (get_run_details(run_filename) or {}).get("defaults") or {}
                fx_prompt = run_defaults.get("default_audio_prompt") or FALLBACK_AUDIO_PROMPT
                fx_negative_prompt = fx_negative_prompt or run_defaults.get("default_audio_negative_prompt") or FALLBACK_AUDIO_NEG_PROMPT
        # fx_prompt stays None unless fx_action == "generate" - _run_single_clip
        # only appends the "Audio: ..." hint to the joint prompt when it's set,
        # so the hallucination is only steered when we're actually keeping it.

        if on_progress:
            on_progress(status="running", chunk_total=n if n > 1 else None)

        for i, (start_frame, num_frames) in enumerate(chunks):
            if n > 1:
                if on_progress:
                    on_progress(chunk_current=i + 1)
                clip_source = input_dir / f"deblur_{ts}_c{i+1}_{source_path.stem}.mp4"
                ok = False
                for _cut_attempt in range(3):
                    ok = await loop.run_in_executor(
                        None, _extract_chunk, source_path, clip_source, start_frame, num_frames, fps
                    )
                    if ok:
                        break
                    await asyncio.sleep(1.5)  # transient Windows file-lock (e.g. AV scan) - retry
                if not ok:
                    raise RuntimeError(f"Nie udało się wyciąć fragmentu {i+1}/{n} z {source_path.name}")
                chunk_sources.append(clip_source)
            else:
                clip_source = source_path

            ts_label = ts if n == 1 else f"{ts}_c{i+1}"
            out_path = await _run_single_clip(
                loop, deblur_url, input_dir, output_dir, clip_source, ts_label, num_frames,
                fx_prompt, fx_negative_prompt, on_progress,
            )
            chunk_outputs.append(out_path)

        # 7. Join chunk outputs (or pass the single one through untouched)
        if len(chunk_outputs) == 1:
            final_video = chunk_outputs[0]
        else:
            if on_progress:
                on_progress(chunk_current=None)
            concat_target = output_dir / f"_deblur_concat_{ts}.mp4"
            await _concatenate_clips(chunk_outputs, concat_target, loop)
            extra_temp_files.append(concat_target)
            final_video = concat_target

        # 7a. FX sidecar (2026-09-09, see module docstring / _classify_source_audio):
        # generate (fresh hallucination, steered above) or migrate (existing
        # legacy baked-in audio) into the FX side file — decided up front,
        # fx_action is None for dialogue clips or when MMAudio already exists.
        if fx_action == "generate":
            ok = await loop.run_in_executor(None, _extract_audio_to_mp3, final_video, fx_sidecar)
            if ok:
                print(f"  INFO: Halucynowany FX z deblura zapisany jako {fx_sidecar.name} (MMAudio nie bylo jeszcze wygenerowane)")
            else:
                print(f"  WARN: Nie udalo sie zapisac FX-sidecar z deblura dla {source_path.name}")
        elif fx_action == "migrate":
            ok = await loop.run_in_executor(None, _extract_audio_to_mp3, source_path, fx_sidecar)
            if ok:
                print(f"  INFO: Stary FX (sprzed konwencji sidecar) przeniesiony do {fx_sidecar.name}")
            else:
                print(f"  WARN: Nie udalo sie zmigrowac starego FX do sidecara dla {source_path.name}")

        # 7b. Main track (see _fix_main_track): real dialogue clips keep their
        # own audio, everything else is silent now — FX never lives here.
        audio_fixed = output_dir / f"_deblur_audiofix_{ts}.mp4"
        keep_dialogue = audio_class == "dialogue"
        if await loop.run_in_executor(None, _fix_main_track, final_video, source_path, audio_fixed, keep_dialogue):
            extra_temp_files.append(audio_fixed)
            final_video = audio_fixed
        else:
            print("  WARN: Naprawa audio nie powiodla sie; wynik moze zawierac halucynowany dzwiek z ComfyUI")

        # 8. Archive original before overwriting
        try:
            _archive_before_deblur(source_path, clip_type)
        except Exception as _arch_err:
            print(f"  WARN: Archiwizacja pominieta ({_arch_err}); kontynuuje deblur bez kopii zapasowej")

        # 9. Copy corrected file to original path (temp + atomic rename)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_dest = dest_path.parent / f"_tmp_deblur_{dest_path.name}"

        copied = False
        last_err: Exception | None = None
        for _attempt in range(8):
            try:
                shutil.copy2(str(final_video), str(tmp_dest))
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
            raise RuntimeError(f"Nie mozna odczytac pliku wyjsciowego ComfyUI: {last_err}")

        copied_size = tmp_dest.stat().st_size if tmp_dest.exists() else 0
        if copied_size < 1024:
            tmp_dest.unlink(missing_ok=True)
            raise RuntimeError(f"Skopiowany plik jest pusty lub uszkodzony ({copied_size} bytes)")

        # Swap into place — retried the same way as the ComfyUI-output copy
        # above, because dest_path can legitimately be open right now: the
        # user is allowed to keep watching/opening the pre-deblur clip via
        # the ▶ button the whole time deblur runs (2026-09-09 — the tile
        # spinner deliberately does NOT disable it). On Windows an unlink()
        # of a file another handle (FastAPI's FileResponse serving it, or a
        # local player) has open can raise PermissionError; on POSIX it
        # would just succeed underneath the reader. Retry-with-backoff covers
        # the Windows case without ever needing to block viewing up front.
        swapped = False
        last_swap_err: Exception | None = None
        for _attempt in range(8):
            try:
                if dest_path.exists():
                    dest_path.unlink()
                tmp_dest.rename(dest_path)
                swapped = True
                break
            except PermissionError as e:
                last_swap_err = e
                await asyncio.sleep(2)
        if not swapped:
            try:
                tmp_dest.unlink(missing_ok=True)
            except Exception:
                pass
            raise RuntimeError(
                f"Nie mozna zapisac zdeblurowanego pliku — {dest_path.name} jest wciaz otwarty "
                f"(odtwarzacz/podglad?). Zamknij podglad i uruchom deblur ponownie. ({last_swap_err})"
            )

        if not update_metadata(
            dest_path, deblurred=True, deblur_checkpoint=_DEBLUR_CHECKPOINT_ID,
            deblur_ts=ts,
        ):
            print(f"  WARN: Nie udalo sie zapisac metadanych deblura na {dest_path.name}")

        _invalidate_thumb(dest_path)

    finally:
        for p in chunk_sources + chunk_outputs + extra_temp_files:
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


async def _run_deblur(
    source_path:  Path,
    dest_path:    Path,
    run_filename: str,
    clip_name:    str,
    clip_type:    str,
) -> None:
    """UI-facing wrapper around _deblur_clip_core - reports progress into the
    module-level _state dict that the standalone deblur panel polls."""
    def _on_progress(**kwargs) -> None:
        _state.update(kwargs)

    try:
        await _deblur_clip_core(source_path, dest_path, run_filename, clip_name, clip_type, _on_progress)
        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({"status": "done", "elapsed_s": elapsed})
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})


def _invalidate_thumb(video_path: Path) -> None:
    thumb = video_path.parent.parent / "frames" / f"{video_path.stem}_thumb.jpg"
    try:
        if thumb.exists():
            thumb.unlink()
    except Exception:
        pass


# ── Public API ───────────────────────────────────────────────────────────────

def start_deblur(run_filename: str, clip_name: str, clip_type: str = "generated") -> dict:
    """Queue a deblur job. Returns immediately. clip_type: 'generated' or 'external'."""
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Deblur jest już w toku"}

    if clip_type == "external":
        source_path = resolve_source_video(run_filename, clip_name)
        if source_path is None:
            return {"ok": False, "error": f"Nie znaleziono pliku zewnętrznego: {clip_name}"}
    else:
        source_path = resolve_video(run_filename, clip_name)
        if source_path is None:
            return {"ok": False, "error": f"Nie znaleziono klipu: {clip_name}"}

    dest_path = source_path  # deblurred replaces original (after archiving)

    _reset_state()
    _state.update({
        "status": "queued",
        "run_filename": run_filename,
        "clip_name": clip_name,
        "started_at": time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_deblur(source_path, dest_path, run_filename, clip_name, clip_type)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}
