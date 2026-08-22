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
noise/music the source never had. By default that's discarded (_fix_audio_track
re-muxes the source's own audio back in, or strips audio if the source had
none). But if the clip's originating flow step already carries an audio_prompt
(the same field used for MMAudio on chain/multichain/talk/multitalk tiles),
_find_flow_audio_prompt reuses it to steer the hallucination into deliberate
FX/ambience instead of wasting it — appended onto the joint text conditioning,
since the workflow has no separate audio-only prompt node. For chain/multichain
clips (no source audio) the generated FX becomes the whole track; for
talk/multitalk clips (source has dialogue) it's mixed in quietly underneath
rather than replacing the speech.
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
from app.services.media_service import resolve_video, resolve_source_video, _extract_video_frame
from app.services.multitalk_service import _concatenate_clips
from utils.video_utils import get_video_info

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

_FX_MIX_VOLUME = 0.178  # ~-15dB: generated FX ducked under existing dialogue

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


def _fix_audio_track(video_path: Path, source_path: Path, dest: Path, fx_used: bool) -> bool:
    """Reconcile dest's audio against what the source actually had, per the
    four cases in the module docstring:
      - dialogue source + fx_used:    mix generated FX quietly under the speech
      - dialogue source + no fx:      replace hallucination with the original dialogue
      - silent source + fx_used:      keep the generated FX as the whole track
      - silent source + no fx:        strip audio entirely (deblur touches sharpness only)
    """
    try:
        source_has_audio = _has_audio(source_path)
        if source_has_audio and fx_used:
            cmd = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(source_path),
                   "-filter_complex",
                   f"[1:a]volume=1.0[dlg];[0:a]volume={_FX_MIX_VOLUME}[fx];"
                   "[dlg][fx]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                   "-map", "0:v:0", "-map", "[aout]",
                   "-c:v", "copy", "-c:a", "aac", "-shortest", str(dest)]
        elif source_has_audio and not fx_used:
            cmd = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(source_path),
                   "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
                   "-shortest", str(dest)]
        elif not source_has_audio and fx_used:
            cmd = ["ffmpeg", "-y", "-i", str(video_path),
                   "-map", "0:v:0", "-map", "0:a:0", "-c", "copy", str(dest)]
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
    fx_prompt: str | None = None,
    fx_negative_prompt: str | None = None,
    on_progress: Callable[..., None] | None = None,
) -> Path:
    """
    Run one clip through the deblur ComfyUI workflow end-to-end (copy in,
    extract first frame, submit, poll, wait-stable). Returns the ComfyUI
    output path. Cleans up its own temp input+frame files; the caller owns
    cleanup of the returned output path.
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

        # 4. Submit to ComfyUI
        def _submit():
            try:
                return _http_post(f"{deblur_url}/prompt", {"prompt": workflow})
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        f"Linux ComfyUI niedostępny ({deblur_url}). "
                        f"Uruchom WSL2 ComfyUI i spróbuj ponownie."
                    ) from e
                raise

        resp = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return prompt_id: {resp}")

        if on_progress:
            on_progress(prompt_id=prompt_id)

        # 5. Poll for completion (history API + directory fallback)
        max_polls = 800  # 800 x 3s = 40 min max
        out_video_path: Path | None = None

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

            for p in output_dir.rglob("*.mp4"):
                if expected_prefix in p.name and p.stat().st_size > 0:
                    out_video_path = p
                    break
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

        fx_prompt, fx_negative_prompt = _find_flow_audio_prompt(run_filename, source_path, clip_name)
        fx_used = bool(fx_prompt)

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
                loop, deblur_url, input_dir, output_dir, clip_source, ts_label,
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

        # 7b. Reconcile dest's audio against the source (mix/replace/keep/strip -
        # see _fix_audio_track). chunk_outputs already carry per-chunk generated
        # audio when fx_used; _concatenate_clips (built for multitalk) preserves it.
        audio_fixed = output_dir / f"_deblur_audiofix_{ts}.mp4"
        if await loop.run_in_executor(None, _fix_audio_track, final_video, source_path, audio_fixed, fx_used):
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

        if dest_path.exists():
            dest_path.unlink()
        tmp_dest.rename(dest_path)

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
