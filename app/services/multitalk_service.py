# -*- coding: utf-8 -*-
"""
Multitalk service — single-speaker talk clips with N-person silence masking.

One API call = one clip: one person speaks, all others are masked to silence.
Designed to feed Video Generator for dialog composition.

Workflow: multitalk_wanvideo_test_api.json (WanVideoWrapper + block swap)

Mask storage (reuses existing pic mask mechanism):
  {project_folder}/multitalk/{image_stem}/person_0.png   ← copy of base image
  {project_folder}/multitalk/{image_stem}/masks/person_0.png  ← painted face mask
"""

import asyncio
import copy
import io
import json
import shutil
import struct
import subprocess
import time
import wave
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image as _PILImage

from app.core.config import settings
from app.services.media_service import _project_folder
from app.services import app_config_service


# ── Workflow config key ──────────────────────────────────────────────────────

_MULTITALK_WORKFLOW_KEY = "multitalk"

def _load_multitalk_workflow() -> dict:
    _wf = (
        app_config_service.get_model("linux", _MULTITALK_WORKFLOW_KEY).get("workflow_json")
        or getattr(settings, "multitalk_workflow_json",
                   str(Path(__file__).parent.parent.parent /
                       "workflow_configs" / "multitalk_wanvideo_test_api.json"))
    )
    path = Path(_wf)
    if not path.exists():
        raise FileNotFoundError(f"Multitalk workflow JSON not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not any(
        isinstance(v, dict) and "class_type" in v for v in data.values()
    ):
        raise ValueError(f"Invalid API-format workflow: {path}")
    return data


# ── Node lookup ──────────────────────────────────────────────────────────────

def _find_node_by_title(workflow: dict, title: str) -> dict | None:
    for node in workflow.values():
        if isinstance(node, dict) and node.get("_meta", {}).get("title") == title:
            return node
    return None


# ── Workflow patching ────────────────────────────────────────────────────────

def _patch_multitalk_workflow(
    workflow: dict,
    speaker_image_filename: str,
    silence_image_filename: str,
    audio_filename: str,
    silence_filename: str,
    width: int,
    height: int,
    positive_prompt: str = "",
    filename_prefix: str = "multitalk",
) -> dict:
    wf = copy.deepcopy(workflow)

    node = _find_node_by_title(wf, "[PATCH] Image + Maska Osoba 1 (namalowana)")
    if node:
        node["inputs"]["image"] = speaker_image_filename

    node = _find_node_by_title(wf, "[PATCH] Ten sam obraz + Maska Osoba 2 (namalowana)")
    if node:
        node["inputs"]["image"] = silence_image_filename

    node = _find_node_by_title(wf, "[PATCH] Audio - Osoba 1 (mowi)")
    if node:
        node["inputs"]["audio"] = audio_filename

    node = _find_node_by_title(wf, "[PATCH] Audio - Osoba 2 (cisza lub mowi)")
    if node:
        node["inputs"]["audio"] = silence_filename

    node = _find_node_by_title(wf, "[PATCH] Resize obrazu (width/height podmieniane przez backend)")
    if node:
        node["inputs"]["width"]  = width
        node["inputs"]["height"] = height

    node = _find_node_by_title(wf, "Save Video")
    if node:
        node["inputs"]["filename_prefix"] = filename_prefix

    if positive_prompt:
        node = _find_node_by_title(wf, "Text Encode")
        if node:
            node["inputs"]["positive_prompt"] = positive_prompt

    return wf


# ── Mask helpers ─────────────────────────────────────────────────────────────

def _mask_path(person_image_path: Path) -> Path:
    """Return masks/{filename} next to the person image (mirrors pic_session convention)."""
    return person_image_path.parent / "masks" / person_image_path.name


def _load_mask_array(mask_path: Path) -> np.ndarray | None:
    """Load a grayscale mask PNG as float32 array [0..1]. Returns None if missing."""
    if not mask_path.exists():
        return None
    try:
        with _PILImage.open(str(mask_path)) as img:
            return np.array(img.convert("L"), dtype=np.float32) / 255.0
    except Exception:
        return None


def _merge_masks(mask_arrays: list[np.ndarray | None]) -> np.ndarray | None:
    """Merge multiple masks with element-wise MAX. Returns None if all missing."""
    result: np.ndarray | None = None
    for arr in mask_arrays:
        if arr is None:
            continue
        result = arr if result is None else np.maximum(result, arr)
    return result


def _make_rgba_png_bytes(image_path: Path, mask_array: np.ndarray | None) -> bytes:
    """
    Combine image RGB + mask alpha into a RGBA PNG.
    ComfyUI LoadImage returns image[0]=RGB, mask[1]=alpha channel.
    """
    with _PILImage.open(str(image_path)) as img:
        rgb = img.convert("RGB")

    if mask_array is None:
        alpha = _PILImage.new("L", rgb.size, 0)
    else:
        mask_uint8 = (np.clip(mask_array, 0, 1) * 255).astype(np.uint8)
        alpha_img = _PILImage.fromarray(mask_uint8, "L")
        if alpha_img.size != rgb.size:
            alpha_img = alpha_img.resize(rgb.size, _PILImage.LANCZOS)
        alpha = alpha_img

    rgba = _PILImage.merge("RGBA", (*rgb.split(), alpha))
    buf = io.BytesIO()
    rgba.save(buf, "PNG")
    return buf.getvalue()


# ── Silence generator ────────────────────────────────────────────────────────

def _generate_silence_wav(path: Path, duration_s: float = 0.5, sample_rate: int = 16000) -> None:
    n_samples = max(1, int(duration_s * sample_rate))
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{n_samples}h", *([0] * n_samples)))


# ── Resolution ───────────────────────────────────────────────────────────────

def _round16(n: int) -> int:
    return max(16, (n // 16) * 16)


def suggest_resolution(image_path: Path) -> tuple[int, int]:
    """
    Scale the image to fit within ~307k pixels while preserving aspect ratio.
    Returns (width, height) both divisible by 16.
    """
    MAX_PIXELS = 307_200
    try:
        with _PILImage.open(str(image_path)) as img:
            w, h = img.size
    except Exception:
        return 480, 832

    if w == 0 or h == 0:
        return 480, 832

    scale = min(1.0, (MAX_PIXELS / (w * h)) ** 0.5)
    return _round16(int(w * scale)), _round16(int(h * scale))


# ── Person image copies ──────────────────────────────────────────────────────

def _persons_dir(project_folder: Path, image_path: Path) -> Path:
    stem = image_path.stem
    return project_folder / "multitalk" / stem


def person_image_path(project_folder: Path, image_path: Path, idx: int) -> Path:
    return _persons_dir(project_folder, image_path) / f"person_{idx}{image_path.suffix}"


def setup_person_images(
    project_folder: Path,
    image_filename: str,
    num_persons: int,
) -> list[Path]:
    """
    Create N copies of the base image in multitalk/{stem}/ for mask painting.
    Existing copies are not overwritten (masks would be lost).
    Returns list of absolute paths to person image copies.
    """
    src = project_folder / image_filename
    if not src.exists():
        raise FileNotFoundError(f"Base image not found: {src}")

    persons_dir = _persons_dir(project_folder, src)
    persons_dir.mkdir(parents=True, exist_ok=True)
    (persons_dir / "masks").mkdir(exist_ok=True)

    paths = []
    for i in range(num_persons):
        dst = person_image_path(project_folder, src, i)
        if not dst.exists():
            shutil.copy2(str(src), str(dst))
        paths.append(dst)

    return paths


# ── HTTP helpers ─────────────────────────────────────────────────────────────

import urllib.request
import urllib.error


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


# ── Output helpers ───────────────────────────────────────────────────────────

def _find_video_in_outputs(outputs: dict) -> dict | None:
    for node_out in outputs.values():
        if not isinstance(node_out, dict):
            continue
        for key in ("videos", "gifs"):
            for v in node_out.get(key) or []:
                if isinstance(v, dict) and v.get("filename", "").endswith(".mp4"):
                    return v
    return None


def _newest_mp4_added_after(directory: Path, known: set[str]) -> Path | None:
    if not directory.exists():
        return None
    candidates = [p for p in directory.glob("*.mp4") if p.name not in known]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


# ── Global job state ─────────────────────────────────────────────────────────

_state: dict = {
    "status":       "idle",
    "prompt_id":    None,
    "run_filename": None,
    "clip_name":    None,
    "error":        None,
    "started_at":   None,
    "elapsed_s":    None,
}

_task: asyncio.Task | None = None


def get_multitalk_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("queued", "running"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def _reset_state() -> None:
    _state.update({
        "status":    "idle",
        "prompt_id": None,
        "run_filename": None,
        "clip_name": None,
        "error":     None,
        "started_at": None,
        "elapsed_s": None,
    })


# ── Core generator ───────────────────────────────────────────────────────────

async def _generate_clip(
    loop:           asyncio.AbstractEventLoop,
    comfyui_url:    str,
    input_dir:      Path,
    output_dir:     Path,
    base_image:     Path,
    speaker_mask:   np.ndarray | None,
    silence_mask:   np.ndarray | None,
    audio_path:     Path,
    width:          int,
    height:         int,
    positive_prompt: str,
    prefix:         str,
) -> Path:
    """
    Submit one multitalk clip to ComfyUI and return the output mp4 path.
    """
    import os as _os
    _os.makedirs(str(input_dir), exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")

    # Build speaker RGBA PNG (image + speaker face mask as alpha)
    speaker_png_bytes = _make_rgba_png_bytes(base_image, speaker_mask)
    tmp_speaker = input_dir / f"mt_speaker_{ts}.png"
    tmp_speaker.write_bytes(speaker_png_bytes)

    # Build silence RGBA PNG (image + merged silent-faces mask as alpha)
    silence_png_bytes = _make_rgba_png_bytes(base_image, silence_mask)
    tmp_silence = input_dir / f"mt_silence_{ts}.png"
    tmp_silence.write_bytes(silence_png_bytes)

    # Copy audio
    tmp_audio = input_dir / f"mt_audio_{ts}{audio_path.suffix}"
    shutil.copy2(str(audio_path), str(tmp_audio))

    # Generate silence WAV
    audio_dur = _audio_duration(audio_path)
    silence_dur = max(0.5, audio_dur * 0.1)
    tmp_silence_wav = input_dir / f"mt_sil_{ts}.wav"
    _generate_silence_wav(tmp_silence_wav, silence_dur)

    existing_mp4s: set[str] = (
        {p.name for p in output_dir.glob("*.mp4")} if output_dir.exists() else set()
    )

    try:
        workflow = _load_multitalk_workflow()
        workflow = _patch_multitalk_workflow(
            workflow,
            speaker_image_filename=tmp_speaker.name,
            silence_image_filename=tmp_silence.name,
            audio_filename=tmp_audio.name,
            silence_filename=tmp_silence_wav.name,
            width=width,
            height=height,
            positive_prompt=positive_prompt,
            filename_prefix=prefix,
        )

        def _submit():
            try:
                return _http_post(f"{comfyui_url}/prompt", {"prompt": workflow})
            except urllib.error.HTTPError as e:
                try:
                    body = e.read().decode("utf-8", errors="replace")
                except Exception:
                    body = str(e)
                raise RuntimeError(f"ComfyUI rejected prompt (HTTP {e.code}): {body}") from e
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError("ComfyUI niedostępny (port 8189).") from e
                raise

        resp = await loop.run_in_executor(None, _submit)
        prompt_id = resp.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"No prompt_id in response: {resp}")

        _state["prompt_id"] = prompt_id

        out_video_path: Path | None = None
        unreachable_streak = 0
        for _ in range(1800):   # 90 min max
            await asyncio.sleep(3)
            history_ok = False
            try:
                history = await loop.run_in_executor(
                    None, lambda: _http_get(f"{comfyui_url}/history/{prompt_id}")
                )
                history_ok = True
                unreachable_streak = 0

                if prompt_id in history:
                    job     = history[prompt_id]
                    outputs = job.get("outputs", {})
                    video   = _find_video_in_outputs(outputs)
                    if video:
                        candidate = output_dir / video.get("subfolder", "") / video["filename"]
                        if candidate.exists():
                            out_video_path = candidate
                            break
                    status = job.get("status", {})
                    if status.get("status_str") == "error":
                        msgs = status.get("messages", [])
                        err  = next(
                            (m[1].get("exception_message", str(m))
                             for m in msgs if m[0] == "execution_error"),
                            "ComfyUI error",
                        )
                        raise RuntimeError(err)
            except RuntimeError:
                raise
            except Exception:
                unreachable_streak += 1

            if not history_ok and unreachable_streak >= 5:
                new_file = _newest_mp4_added_after(output_dir, existing_mp4s)
                if new_file:
                    out_video_path = new_file
                    break
        else:
            raise RuntimeError("Timeout: multitalk did not complete within 90 minutes")

        if not out_video_path or not out_video_path.exists():
            raise RuntimeError(f"Output file not found: {out_video_path}")

        # Wait for file to stabilise
        await asyncio.sleep(3)
        prev_size = -1
        for _ in range(30):
            cur = out_video_path.stat().st_size
            if cur == prev_size and cur > 0:
                break
            prev_size = cur
            await asyncio.sleep(3)

        # Re-mux with original audio
        muxed = out_video_path.with_name(f"_mux_{out_video_path.name}")
        try:
            mx = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    [
                        "ffmpeg", "-y",
                        "-i", str(out_video_path),
                        "-i", str(tmp_audio),
                        "-c:v", "copy",
                        "-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "192k",
                        "-movflags", "+faststart",
                        "-shortest",
                        str(muxed),
                    ],
                    capture_output=True,
                ),
            )
            if mx.returncode == 0 and muxed.exists():
                out_video_path.unlink(missing_ok=True)
                muxed.rename(out_video_path)
        except Exception as exc:
            raise RuntimeError(f"Audio mux failed: {exc}") from exc

        return out_video_path

    finally:
        for p in (tmp_speaker, tmp_silence, tmp_audio, tmp_silence_wav):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass


def _audio_duration(path: Path) -> float:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        return float(r.stdout.strip())
    except Exception:
        return 1.0


# ── Background task ──────────────────────────────────────────────────────────

async def _run_multitalk(
    project_folder: Path,
    base_image:     Path,
    speaker_idx:    int,
    num_persons:    int,
    audio_path:     Path,
    dest_path:      Path,
    run_filename:   str,
    clip_name:      str,
    width:          int,
    height:         int,
    positive_prompt: str,
) -> None:
    loop       = asyncio.get_running_loop()
    url        = settings.comfyui_url
    input_dir  = Path(settings.comfyui_linux_input_dir)
    output_dir = Path(settings.comfyui_linux_output_dir)

    _state["status"] = "running"

    try:
        # Load per-person masks
        person_masks: list[np.ndarray | None] = []
        for i in range(num_persons):
            pimg = person_image_path(project_folder, base_image, i)
            mp   = _mask_path(pimg)
            person_masks.append(_load_mask_array(mp))

        speaker_mask  = person_masks[speaker_idx]
        silence_masks = [m for i, m in enumerate(person_masks) if i != speaker_idx]
        silence_mask  = _merge_masks(silence_masks)

        prefix = f"multitalk_{Path(dest_path).stem}"
        out = await _generate_clip(
            loop=loop,
            comfyui_url=url,
            input_dir=input_dir,
            output_dir=output_dir,
            base_image=base_image,
            speaker_mask=speaker_mask,
            silence_mask=silence_mask,
            audio_path=audio_path,
            width=width,
            height=height,
            positive_prompt=positive_prompt,
            prefix=prefix,
        )

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_dest = dest_path.parent / f"_tmp_{dest_path.name}"
        shutil.copy2(str(out), str(tmp_dest))
        if dest_path.exists():
            dest_path.unlink()
        tmp_dest.rename(dest_path)
        try:
            out.unlink()
        except Exception:
            pass

        _state.update({
            "status":    "done",
            "clip_name": clip_name,
            "elapsed_s": round(time.time() - _state["started_at"], 1),
        })

    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})


# ── Public API ───────────────────────────────────────────────────────────────

def start_multitalk(run_filename: str, item: dict, image_filename: str) -> dict:
    """
    Start a multitalk clip generation.

    item fields:
        audio       : str    audio filename (relative to project_folder)
        speaker_idx : int    0-based index of the speaking person
        num_persons : int    total number of people in the scene
        width       : int    (optional, auto-detected from image if missing)
        height      : int    (optional)
        pos         : str    (optional) positive prompt
        name        : str    (optional) output clip name
    """
    global _task

    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Multitalk jest już w toku"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono project_folder: {run_filename}"}

    base_image = pf / image_filename
    if not base_image.exists():
        return {"ok": False, "error": f"Nie znaleziono obrazu: {image_filename}"}

    audio_name = item.get("audio", "")
    if not audio_name:
        return {"ok": False, "error": "Brak pola audio"}
    audio_path = pf / audio_name
    if not audio_path.exists():
        return {"ok": False, "error": f"Nie znaleziono audio: {audio_name}"}

    speaker_idx = int(item.get("speaker_idx", 0))
    num_persons = int(item.get("num_persons", 2))
    if speaker_idx >= num_persons:
        return {"ok": False, "error": f"speaker_idx={speaker_idx} >= num_persons={num_persons}"}

    # Verify person images exist
    for i in range(num_persons):
        p = person_image_path(pf, base_image, i)
        if not p.exists():
            return {"ok": False, "error": f"Brak kopii osoby {i}: {p.name} — wywołaj /setup najpierw"}

    # Resolution
    if item.get("width") and item.get("height"):
        width  = _round16(int(item["width"]))
        height = _round16(int(item["height"]))
    else:
        width, height = suggest_resolution(base_image)

    positive_prompt = str(item.get("pos", "") or "")
    clip_name = str(item.get("name", "") or f"multitalk_{datetime.now().strftime('%H%M%S')}.mp4")
    if not clip_name.endswith(".mp4"):
        clip_name += ".mp4"

    dest_path = pf / "transitions" / clip_name

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "clip_name":    clip_name,
        "started_at":   time.time(),
    })

    try:
        _task = asyncio.create_task(
            _run_multitalk(
                project_folder=pf,
                base_image=base_image,
                speaker_idx=speaker_idx,
                num_persons=num_persons,
                audio_path=audio_path,
                dest_path=dest_path,
                run_filename=run_filename,
                clip_name=clip_name,
                width=width,
                height=height,
                positive_prompt=positive_prompt,
            )
        )
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}

    return {"ok": True, "clip_name": clip_name, "width": width, "height": height}


def cancel_multitalk() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}
