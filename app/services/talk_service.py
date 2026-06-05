# -*- coding: utf-8 -*-
"""
Talk service — generates InfiniteTalk clips using Linux ComfyUI (port 8189).

Flow (per audio segment):
  1. Copy start-frame image → ComfyUI input dir (unique temp name)
  2. Copy .mp3 → ComfyUI input dir (unique temp name)
  3. Load API-format workflow JSON, patch: image, audio, width, height
  4. POST to ComfyUI /prompt
  5. Poll /history/{prompt_id} until done (every 3 s, max 20 min)
  6. Move output → project transitions/ folder
  7. Clean up temp inputs

Multi-audio: segments are processed sequentially and concatenated with ffmpeg.

SETUP REQUIRED:
  Export the API-format workflow from ComfyUI:
    Settings → Enable Dev Mode → click "Save (API Format)"
  Place the JSON at the path configured in app_config.yaml → models.talk.workflow_json.

  The service will look for nodes by class_type and patch:
    LoadImage      → inputs.image
    LoadAudio      → inputs.audio
    ImageScale     → inputs.width / inputs.height
    VHS_VideoCombine → inputs.filename_prefix  (keeps outputs distinguishable)
"""

import asyncio
import copy
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.services.media_service import talk_path, _project_folder
from app.services import app_config_service


# ── Resolution presets & auto-detection ─────────────────────────────────────

# (width, height, pixels, ratio_name)
_PRESETS: list[tuple[int, int, int, str]] = [
    # 9:16
    (480,  832,  399_360, "9:16"),
    (576, 1024,  589_824, "9:16"),
    (720, 1280,  921_600, "9:16"),
    # 16:9
    (832,  480,  399_360, "16:9"),
    (1024,  576, 589_824, "16:9"),
    (1280,  720, 921_600, "16:9"),
    # 1:1
    (512,  512,  262_144, "1:1"),
    (640,  640,  409_600, "1:1"),
    (768,  768,  589_824, "1:1"),
]

# Pixel-count tiers based on max audio duration
_TIER_HIGH    = 600_000   # < 5s  → up to ~590k px
_TIER_SAFE    = 420_000   # 5–15s → up to ~400k px
_TIER_MINIMAL =       0   # > 15s → lowest available

_RATIO_TOLERANCE = 0.06   # ±6 % aspect-ratio match


def _detect_ratio(width: int, height: int) -> str | None:
    """Return the standard ratio name if the image fits within tolerance."""
    if height == 0:
        return None
    r = width / height
    for _, _, _, rname in _PRESETS:
        pw, ph = (4, 3) if rname == "4:3" else map(int, rname.split(":"))
        ref = pw / ph
        if abs(r - ref) / ref < _RATIO_TOLERANCE:
            return rname
    return None


def _audio_duration(path: Path) -> float:
    """Return audio duration in seconds via ffprobe, or 0 on failure."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True, text=True, timeout=10,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def _round32(n: int) -> int:
    """Round down to nearest multiple of 32 (diffusion model requirement)."""
    return max(32, (n // 32) * 32)


def suggest_resolution(image_path: Path, audio_paths: list[Path]) -> tuple[int, int]:
    """
    Auto-suggest (width, height) for a talk clip.

    Logic:
      1. Read image dimensions via ffprobe.
      2. Detect aspect ratio group.
      3. Compute tier from max(audio durations).
      4. Pick highest preset below the tier pixel limit in that group.
         If no standard ratio matched: scale proportionally so longer side ≤ 832,
         round to multiple of 32.
    """
    # Read image dims
    img_w, img_h = 0, 0
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "default=noprint_wrappers=1",
                str(image_path),
            ],
            capture_output=True, text=True, timeout=10,
        )
        for line in result.stdout.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                if k == "width":
                    img_w = int(v)
                elif k == "height":
                    img_h = int(v)
    except Exception:
        pass

    if img_w == 0 or img_h == 0:
        return 480, 832  # safe default

    # Tier from max audio duration
    max_dur = max((_audio_duration(p) for p in audio_paths), default=0.0)
    if max_dur < 5.0:
        tier_px = _TIER_HIGH
    elif max_dur < 15.0:
        tier_px = _TIER_SAFE
    else:
        tier_px = _TIER_MINIMAL

    # Detect standard ratio
    ratio = _detect_ratio(img_w, img_h)

    if ratio:
        # Find best preset in the same ratio group, within tier
        candidates = [(w, h, px) for w, h, px, rn in _PRESETS
                      if rn == ratio and px <= tier_px]
        if not candidates:
            # Below minimum → use lowest in group
            candidates = [(w, h, px) for w, h, px, rn in _PRESETS if rn == ratio]
        # Highest px that fits within tier
        best = max(candidates, key=lambda t: t[2])
        # Keep original orientation
        if img_w < img_h:
            return min(best[0], best[1]), max(best[0], best[1])
        return max(best[0], best[1]), min(best[0], best[1])

    # Non-standard ratio → scale proportionally, longer side ≤ 832
    max_side = 832
    if img_w >= img_h:
        new_w = min(img_w, max_side)
        new_h = int(img_h * new_w / img_w)
    else:
        new_h = min(img_h, max_side)
        new_w = int(img_w * new_h / img_h)

    return _round32(new_w), _round32(new_h)


# ── Workflow helpers ─────────────────────────────────────────────────────────

def _load_workflow() -> dict:
    """Load the API-format workflow JSON from disk."""
    # Priority: app_config.yaml backends.linux.models.talk → settings fallback
    _wf = app_config_service.get_model("linux", "talk").get("workflow_json") or settings.talk_workflow_json
    path = Path(_wf)
    if not path.exists():
        raise FileNotFoundError(
            f"Talk workflow JSON not found: {path}\n"
            "Export it from ComfyUI: Settings → Enable Dev Mode → Save (API Format).\n"
            f"Place the file at: {path}"
        )
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    # Guard: API-format is {node_id: {class_type, inputs, ...}, ...}
    # Regular (node-graph) format has top-level keys like "nodes", "links",
    # "version", "extra" whose values are lists/primitives, NOT node dicts.
    # Sending the wrong format causes ComfyUI to crash with AttributeError.
    if not isinstance(data, dict):
        raise ValueError(
            f"Workflow file is not a JSON object: {path}"
        )
    if "nodes" in data and isinstance(data.get("nodes"), list):
        raise ValueError(
            f"Workflow file is in regular ComfyUI format, NOT API format: {path}\n"
            "To export the correct format:\n"
            "  1. Open the workflow in ComfyUI\n"
            "  2. Settings → Enable Dev Mode (toggle)\n"
            "  3. Click  'Save (API Format)'  (NOT the regular Save button)\n"
            f"  4. Replace the file at: {path}"
        )
    # Check that at least one value looks like a node dict
    has_node = any(
        isinstance(v, dict) and "class_type" in v
        for v in data.values()
    )
    if not has_node:
        raise ValueError(
            f"Workflow file has no recognisable ComfyUI nodes (class_type missing): {path}\n"
            "Make sure you exported with 'Save (API Format)' in Dev Mode."
        )

    return data


def _find_node(workflow: dict, class_type: str) -> dict | None:
    """Return the first node dict whose class_type matches."""
    for node in workflow.values():
        if isinstance(node, dict) and node.get("class_type") == class_type:
            return node
    return None


def _patch_workflow(
    workflow: dict,
    image_filename: str,
    audio_filename: str,
    width: int,
    height: int,
    prompt: str = "",
    negative_prompt: str = "",
    filename_prefix: str = "Talk",
) -> dict:
    """
    Patch a deep copy of the workflow with job-specific parameters.
    Searches by class_type — robust against node ID changes.
    """
    wf = copy.deepcopy(workflow)

    node = _find_node(wf, "LoadImage")
    if node:
        node["inputs"]["image"] = image_filename

    node = _find_node(wf, "LoadAudio")
    if node:
        node["inputs"]["audio"] = audio_filename

    node = _find_node(wf, "ImageScale")
    if node:
        node["inputs"]["width"]  = width
        node["inputs"]["height"] = height

    node = _find_node(wf, "WanVideoTextEncodeCached")
    if node:
        if prompt:
            node["inputs"]["positive_prompt"] = prompt
        if negative_prompt:
            node["inputs"]["negative_prompt"] = negative_prompt

    node = _find_node(wf, "VHS_VideoCombine")
    if node:
        node["inputs"]["filename_prefix"] = filename_prefix

    return wf


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":       "idle",   # idle | queued | running | done | error
    "prompt_id":    None,
    "run_filename": None,
    "talk_name":    None,
    "segment":      None,     # current audio segment label
    "total_segs":   None,
    "output_name":  None,
    "error":        None,
    "started_at":   None,
    "elapsed_s":    None,
}

_task: asyncio.Task | None = None


def get_talk_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("running", "queued"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":       "idle",
        "prompt_id":    None,
        "run_filename": None,
        "talk_name":    None,
        "segment":      None,
        "total_segs":   None,
        "output_name":  None,
        "error":        None,
        "started_at":   None,
        "elapsed_s":    None,
    })


# ── HTTP helpers ─────────────────────────────────────────────────────────────

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


# ── Output detection helpers ─────────────────────────────────────────────────

def _find_video_in_outputs(outputs: dict) -> dict | None:
    for node_id, node_out in outputs.items():
        if not isinstance(node_out, dict):
            continue
        videos = node_out.get("videos") or node_out.get("gifs") or []
        for v in videos:
            if isinstance(v, dict) and v.get("filename", "").endswith(".mp4"):
                return v
    return None


def _newest_mp4_added_after(directory: Path, known: set[str]) -> Path | None:
    if not directory.exists():
        return None
    candidates = [p for p in directory.glob("*.mp4") if p.name not in known]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


# ── Single-segment generator ─────────────────────────────────────────────────

async def _generate_segment(
    loop:            asyncio.AbstractEventLoop,
    comfyui_url:     str,
    input_dir:       Path,
    output_dir:      Path,
    image_path:      Path,
    audio_path:      Path,
    width:           int,
    height:          int,
    prompt:          str,
    negative_prompt: str,
    prefix:          str,
) -> Path:
    """
    Submit one audio segment to ComfyUI and return the path to the output mp4.
    Raises RuntimeError on any failure.
    """
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    tmp_img   = input_dir / f"talk_img_{ts}_{image_path.name}"
    tmp_audio = input_dir / f"talk_aud_{ts}_{audio_path.name}"

    # os.makedirs is more reliable than Path.mkdir for UNC and network paths
    import os as _os
    _os.makedirs(str(input_dir), exist_ok=True)
    shutil.copy2(str(image_path), str(tmp_img))
    shutil.copy2(str(audio_path), str(tmp_audio))

    # Snapshot existing outputs (for fallback detection)
    existing_mp4s: set[str] = (
        {p.name for p in output_dir.glob("*.mp4")} if output_dir.exists() else set()
    )

    try:
        # Load and patch workflow
        workflow = _load_workflow()
        workflow = _patch_workflow(
            workflow,
            image_filename=tmp_img.name,
            audio_filename=tmp_audio.name,
            width=width,
            height=height,
            prompt=prompt,
            negative_prompt=negative_prompt,
            filename_prefix=prefix,
        )

        # Submit
        import urllib.error as _ue

        def _submit():
            try:
                return _http_post(f"{comfyui_url}/prompt", {"prompt": workflow})
            except _ue.HTTPError as e:
                # ComfyUI returns 400/500 when the prompt is invalid.
                # Read the body so we surface the real error message.
                try:
                    body = e.read().decode("utf-8", errors="replace")
                except Exception:
                    body = str(e)
                raise RuntimeError(
                    f"ComfyUI rejected the prompt (HTTP {e.code}): {body}"
                ) from e
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        "Linux ComfyUI niedostępny (port 8189). "
                        "Uruchom środowisko Linux i spróbuj ponownie."
                    ) from e
                raise

        resp = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"ComfyUI did not return prompt_id: {resp}")

        _state["prompt_id"] = prompt_id

        # Poll (max 20 min = 400 × 3 s)
        out_video_path: Path | None = None
        for _ in range(400):
            await asyncio.sleep(3)

            try:
                def _check():
                    return _http_get(f"{comfyui_url}/history/{prompt_id}")
                history = await loop.run_in_executor(None, _check)

                if prompt_id in history:
                    job     = history[prompt_id]
                    outputs = job.get("outputs", {})

                    video_entry = _find_video_in_outputs(outputs)
                    if video_entry:
                        subfolder = video_entry.get("subfolder", "")
                        filename  = video_entry["filename"]
                        candidate = output_dir / subfolder / filename
                        if candidate.exists():
                            out_video_path = candidate
                            break

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
                raise
            except Exception:
                pass

            # Directory fallback
            new_file = _newest_mp4_added_after(output_dir, existing_mp4s)
            if new_file is not None:
                out_video_path = new_file
                break

        else:
            raise RuntimeError("Timeout: segment did not complete within 20 minutes")

        if out_video_path is None or not out_video_path.exists():
            raise RuntimeError(f"Output file not found: {out_video_path}")

        # Wait for ComfyUI to release the file handle (Linux NFS/CIFS delay)
        await asyncio.sleep(3)

        # Re-mux with the original audio to guarantee an audio track.
        # VHS_VideoCombine may not embed audio correctly when it receives audio
        # from MultiTalkWav2VecEmbeds output [1] — so we always mux explicitly.
        muxed = out_video_path.with_name(f"_mux_{out_video_path.name}")
        try:
            mx = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    [
                        "ffmpeg", "-y",
                        "-i", str(out_video_path),
                        "-i", str(audio_path),
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-ar", "44100",   # standard sample rate
                        "-ac", "2",       # force stereo (browsers choke on mono AAC)
                        "-b:a", "192k",
                        "-movflags", "+faststart",  # moov atom at front for browser streaming
                        "-shortest",
                        str(muxed),
                    ],
                    capture_output=True,
                ),
            )
            if mx.returncode == 0 and muxed.exists():
                try:
                    out_video_path.unlink()
                except Exception:
                    pass
                muxed.rename(out_video_path)
            else:
                # Mux failed — keep the original (video-only) and log warning
                stderr_txt = mx.stderr.decode("utf-8", errors="replace").strip()
                try:
                    muxed.unlink()
                except Exception:
                    pass
                raise RuntimeError(f"ffmpeg audio mux failed: {stderr_txt}")
        except RuntimeError:
            raise
        except Exception as exc:
            # Non-fatal: keep original file, log the problem
            raise RuntimeError(f"Audio mux error: {exc}") from exc

        return out_video_path

    finally:
        for p in (tmp_img, tmp_audio):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


# ── Background task ──────────────────────────────────────────────────────────

async def _run_talk(
    source_image:   Path,
    audio_entries:  list[dict],   # each: {"path": Path, "pos": str, "neg": str}
    dest_path:      Path,
    run_filename:   str,
    talk_name:      str,
    width:          int,
    height:         int,
    *,
    # Optional overrides — used by generate_talk_clip_sync() for batch scripts.
    # When None the values are read from app settings (default web-app path).
    _comfyui_url:  str | None  = None,
    _input_dir:    Path | None = None,
    _output_dir:   Path | None = None,
) -> None:
    loop       = asyncio.get_running_loop()
    url        = _comfyui_url or settings.comfyui_url
    input_dir  = _input_dir   or Path(settings.comfyui_linux_input_dir)
    output_dir = _output_dir  or Path(settings.comfyui_linux_output_dir)

    try:
        segment_paths: list[Path] = []
        total = len(audio_entries)
        _state["total_segs"] = total

        for idx, entry in enumerate(audio_entries, 1):
            audio_path = entry["path"]
            seg_pos    = entry.get("pos", "")
            seg_neg    = entry.get("neg", "")

            _state["segment"] = f"{idx}/{total} ({audio_path.name})"
            _state["status"]  = "running"

            prefix  = f"Talk_{Path(dest_path).stem}_{idx:02d}"
            seg_out = await _generate_segment(
                loop=loop,
                comfyui_url=url,
                input_dir=input_dir,
                output_dir=output_dir,
                image_path=source_image,
                audio_path=audio_path,
                width=width,
                height=height,
                prompt=seg_pos,
                negative_prompt=seg_neg,
                prefix=prefix,
            )
            segment_paths.append(seg_out)

        # Merge segments (or just move if only one)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if len(segment_paths) == 1:
            tmp_dest = dest_path.parent / f"_tmp_talk_{dest_path.name}"
            shutil.copy2(str(segment_paths[0]), str(tmp_dest))
            if dest_path.exists():
                dest_path.unlink()
            tmp_dest.rename(dest_path)
            try:
                segment_paths[0].unlink()
            except Exception:
                pass
        else:
            # Concatenate with ffmpeg
            concat_list = dest_path.parent / f"_concat_{dest_path.stem}.txt"
            try:
                lines = [f"file '{p}'\n" for p in segment_paths]
                concat_list.write_text("".join(lines), encoding="utf-8")
                subprocess.run(
                    [
                        "ffmpeg", "-y",
                        "-f", "concat", "-safe", "0",
                        "-i", str(concat_list),
                        "-c", "copy",
                        str(dest_path),
                    ],
                    check=True,
                    capture_output=True,
                )
            finally:
                try:
                    concat_list.unlink()
                except Exception:
                    pass
                for p in segment_paths:
                    try:
                        p.unlink()
                    except Exception:
                        pass

        elapsed = round(time.time() - _state["started_at"], 1)
        _state.update({
            "status":      "done",
            "output_name": talk_name,
            "elapsed_s":   elapsed,
        })

    except Exception as exc:
        _state.update({
            "status": "error",
            "error":  str(exc),
        })


# ── Public API ───────────────────────────────────────────────────────────────

def start_talk(
    run_filename: str,
    talk_item:    dict,
    start_image:  str,
) -> dict:
    """
    Queue a talk generation job.

    Parameters
    ----------
    run_filename : str   RUN_*.yaml filename
    talk_item    : dict  YAML internal talk item (has: type, audio, width, height, pos)
    start_image  : str   filename of the start frame (relative to project_folder)

    Returns {"ok": True} or {"ok": False, "error": "..."}
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Talk jest już w toku"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono project_folder dla: {run_filename}"}

    # Width/height needed early for on-the-fly frame extraction
    width  = int(talk_item.get("width", 480))
    height = int(talk_item.get("height", 832))

    # Resolve start image.
    # If the caller passed a video filename, use the extracted end-frame JPEG
    # from the frames/ sub-folder so that ComfyUI's LoadImage node can load it.
    # Chain-step videos live in transitions/chains/ and their frames may not
    # yet exist — extract on-the-fly with FrameExtractor (same approach as chain).
    _vid_exts = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    if Path(start_image).suffix.lower() in _vid_exts:
        stem = Path(start_image).stem
        frame_path = pf / "frames" / f"{stem}_end.png"
        if not frame_path.exists():
            frame_path = pf / "frames" / f"{stem}_end.jpg"
        if frame_path.exists():
            img_path = frame_path
        else:
            # Frame missing — find the source video and extract the end frame.
            # Source can be in project_folder directly or in transitions/chains/.
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
                extracted = extractor.extract_end_frame(rel, width, height)
                if extracted and extracted.exists():
                    img_path = extracted
                else:
                    return {"ok": False, "error": f"Nie udało się wyciągnąć klatki z: {start_image}"}
            else:
                return {"ok": False, "error": f"Nie znaleziono pliku źródłowego: {start_image}"}
    else:
        img_path = pf / start_image
    if not img_path.exists():
        return {"ok": False, "error": f"Nie znaleziono klatki startowej: {start_image}"}

    # Item-level defaults for pos/neg (used when segment doesn't override)
    default_pos = str(talk_item.get("pos", "") or "")
    default_neg = str(talk_item.get("neg", "") or "")

    # Resolve audio files — each entry may be a plain filename string or a dict
    # with {file, pos, neg} for per-segment prompt overrides (chain-style).
    raw_audio = talk_item.get("audio", "")
    audio_list = raw_audio if isinstance(raw_audio, list) else [raw_audio]
    audio_entries: list[dict] = []
    for a in audio_list:
        if isinstance(a, dict):
            fname   = a.get("file", "")
            seg_pos = a.get("pos", default_pos) or default_pos
            seg_neg = a.get("neg", default_neg) or default_neg
        else:
            fname   = str(a)
            seg_pos = default_pos
            seg_neg = default_neg
        if not fname:
            return {"ok": False, "error": "Pusty wpis audio"}
        ap = pf / fname
        if not ap.exists():
            return {"ok": False, "error": f"Nie znaleziono pliku audio: {fname}"}
        audio_entries.append({"path": ap, "pos": seg_pos, "neg": seg_neg})

    if not audio_entries:
        return {"ok": False, "error": "Brak pliku audio"}

    dest_path = talk_path(pf, talk_item)
    talk_name = dest_path.name

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "talk_name":    talk_name,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_talk(img_path, audio_entries, dest_path,
                      run_filename, talk_name, width, height)
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True}


def cancel_talk() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


# ── Batch-script helper ──────────────────────────────────────────────────────

def _snap_to_multiple(value: int, multiple: int = 16) -> int:
    """Round value UP to the nearest multiple of `multiple`."""
    return ((value + multiple - 1) // multiple) * multiple


def generate_talk_clip_sync(
    comfyui_url:     str,
    linux_input_dir: Path,
    linux_output_dir: Path,
    source_image:    Path,
    audio_entries:   list[dict],
    dest_path:       Path,
    width:           int,
    height:          int,
    log_fn=None,
) -> bool:
    """
    Synchronous, self-contained talk clip generation for batch scripts.
    Does not require a running FastAPI app or existing asyncio event loop.

    Parameters
    ----------
    comfyui_url      : Linux ComfyUI base URL, e.g. "http://127.0.0.1:8189"
    linux_input_dir  : UNC/Windows path to ComfyUI input folder
    linux_output_dir : UNC/Windows path to ComfyUI output folder
    source_image     : absolute Path to start-frame image
    audio_entries    : list of {path: Path, pos: str, neg: str}
    dest_path        : absolute Path where the final mp4 should land
    width / height   : generation resolution (will be snapped to multiple of 16)
    log_fn           : optional callable(msg) for progress messages

    Returns True on success, False on failure.
    """
    # MultiTalk requires dimensions divisible by 16 (spatial token alignment)
    width  = _snap_to_multiple(width,  16)
    height = _snap_to_multiple(height, 16)
    if log_fn:
        log_fn(f"Talk resolution: {width}×{height}")

    _reset_state()
    _state.update({
        "status":    "queued",
        "talk_name": dest_path.name,
        "started_at": time.time(),
    })

    async def _coro():
        await _run_talk(
            source_image=source_image,
            audio_entries=audio_entries,
            dest_path=dest_path,
            run_filename="batch",
            talk_name=dest_path.name,
            width=width,
            height=height,
            _comfyui_url=comfyui_url,
            _input_dir=linux_input_dir,
            _output_dir=linux_output_dir,
        )

    try:
        asyncio.run(_coro())
    except Exception as exc:
        if log_fn:
            log_fn(f"Talk generation error: {exc}")
        _state.update({"status": "error", "error": str(exc)})

    if log_fn and _state.get("error") and _state["status"] == "error":
        log_fn(f"Error: {_state['error']}")

    return _state["status"] == "done" and dest_path.exists()
