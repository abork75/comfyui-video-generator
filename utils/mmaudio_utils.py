# -*- coding: utf-8 -*-
"""
MMAudio utility — generates audio for a silent video via WSL ComfyUI.

Flow:
  1. Upload video to ComfyUI input via /upload/image
  2. Queue MMAudio workflow (constructed in-memory, no JSON file needed)
  3. Poll /history/{prompt_id} until done
  4. Download audio via /view API
  5. Merge audio into video with ffmpeg (in-place)
  6. Clean up temp audio file
"""

import io
import json
import random
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

_MODEL_MAIN    = "mmaudio_large_44k_v2_fp16.safetensors"
_MODEL_VAE     = "mmaudio_vae_44k_fp16.safetensors"
_MODEL_SYNCH   = "mmaudio_synchformer_fp16.safetensors"
_MODEL_CLIP    = "apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors"

_POLL_INTERVAL = 4.0
_TIMEOUT_S     = 300


def _build_workflow(video_filename: str, prompt: str, duration: float, steps: int, cfg: float, seed: int) -> dict:
    """Build MMAudio ComfyUI API workflow dict."""
    return {
        "1": {
            "inputs": {
                "video": video_filename,
                "force_rate": 25,
                "force_size": "Disabled",
                "custom_width": 512,
                "custom_height": 512,
                "frame_load_cap": 0,
                "skip_first_frames": 0,
                "select_every_nth": 1,
            },
            "class_type": "VHS_LoadVideo",
        },
        "2": {
            "inputs": {
                "mmaudio_model": _MODEL_MAIN,
                "base_precision": "fp16",
            },
            "class_type": "MMAudioModelLoader",
        },
        "3": {
            "inputs": {
                "vae_model":           _MODEL_VAE,
                "synchformer_model":   _MODEL_SYNCH,
                "clip_model":          _MODEL_CLIP,
                "mode":                "44k",
                "precision":           "fp16",
            },
            "class_type": "MMAudioFeatureUtilsLoader",
        },
        "4": {
            "inputs": {
                "mmaudio_model":    ["2", 0],
                "feature_utils":    ["3", 0],
                "images":           ["1", 0],
                "duration":         round(duration, 2),
                "steps":            steps,
                "cfg":              cfg,
                "seed":             seed,
                "prompt":           prompt,
                "negative_prompt":  "",
                "mask_away_clip":   False,
                "force_offload":    True,
            },
            "class_type": "MMAudioSampler",
        },
        "5": {
            "inputs": {
                "filename_prefix": "mmaudio/audio",
                "audio": ["4", 0],
            },
            "class_type": "SaveAudio",
        },
    }


def _http_post_json(url: str, payload: dict, timeout: int = 15) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                  headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _http_get(url: str, timeout: int = 15):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.read()


def _upload_video(video_path: Path, api_url: str) -> str:
    """Upload video to ComfyUI input folder. Returns filename."""
    import urllib.parse, uuid
    unique_name = f"mmaudio_{uuid.uuid4().hex[:8]}_{video_path.name}"

    boundary = "----FormBoundary" + uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{unique_name}"\r\n'
        f"Content-Type: video/mp4\r\n"
        f"\r\n"
    ).encode() + video_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()

    url = f"{api_url}/upload/image"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
    return result.get("name") or unique_name


def _queue_workflow(workflow: dict, api_url: str) -> str:
    """Queue workflow and return prompt_id."""
    result = _http_post_json(f"{api_url}/prompt", {"prompt": workflow})
    return result["prompt_id"]


def _poll_history(prompt_id: str, api_url: str) -> dict | None:
    """Poll until job done. Returns outputs dict or None on timeout."""
    deadline = time.time() + _TIMEOUT_S
    while time.time() < deadline:
        try:
            raw = _http_get(f"{api_url}/history/{prompt_id}")
            data = json.loads(raw)
            if prompt_id in data:
                return data[prompt_id].get("outputs", {})
        except Exception:
            pass
        time.sleep(_POLL_INTERVAL)
    return None


def _find_audio_in_outputs(outputs: dict) -> tuple[str, str] | None:
    """Return (filename, subfolder) of first audio file in outputs, or None."""
    for node_out in outputs.values():
        if not isinstance(node_out, dict):
            continue
        for entry in node_out.get("audio", []):
            if isinstance(entry, dict) and entry.get("filename"):
                return entry["filename"], entry.get("subfolder", "")
    return None


def _download_audio(filename: str, subfolder: str, api_url: str) -> bytes:
    """Download audio file via ComfyUI /view API."""
    import urllib.parse
    params = urllib.parse.urlencode({
        "filename": filename,
        "subfolder": subfolder,
        "type": "output",
    })
    return _http_get(f"{api_url}/view?{params}", timeout=30)


def _merge_audio_into_video(video_path: Path, audio_bytes: bytes, audio_ext: str, logger=None) -> bool:
    """
    Merge audio into video in-place using ffmpeg.
    Audio is trimmed to video duration (-shortest).
    Returns True on success.
    """
    suffix = audio_ext if audio_ext.startswith(".") else f".{audio_ext}"
    tmp_audio = video_path.with_suffix(f".tmp_audio{suffix}")
    tmp_video = video_path.with_suffix(".tmp_mmaudio.mp4")

    try:
        tmp_audio.write_bytes(audio_bytes)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(tmp_audio),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(tmp_video),
        ]
        r = subprocess.run(cmd, capture_output=True, timeout=120)
        if r.returncode != 0:
            if logger:
                logger.warning(f"  ffmpeg merge exit {r.returncode}: {r.stderr.decode(errors='replace')[:200]}")
            return False
        tmp_video.replace(video_path)
        return True
    except Exception as e:
        if logger:
            logger.warning(f"  Błąd merge audio: {e}")
        return False
    finally:
        tmp_audio.unlink(missing_ok=True)
        if tmp_video.exists():
            tmp_video.unlink(missing_ok=True)


def add_audio(
    video_path: Path,
    prompt: str,
    api_url: str = "http://127.0.0.1:8189",
    duration: float = 10.0,
    steps: int = 25,
    cfg: float = 4.5,
    seed: int = -1,
    logger=None,
) -> bool:
    """
    Generate and add audio to video_path using MMAudio via WSL ComfyUI.
    Modifies video_path in-place.
    Returns True on success, False on any error (original video unchanged).
    """
    if seed == -1:
        seed = random.randint(0, 2**32 - 1)

    if logger:
        logger.info(f"  MMAudio: generowanie audio ({duration:.1f}s)...")
        logger.info(f"  Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    try:
        # 1. Upload video
        if logger:
            logger.info(f"  MMAudio: upload wideo...")
        video_filename = _upload_video(video_path, api_url)

        # 2. Build and queue workflow
        workflow = _build_workflow(video_filename, prompt, duration, steps, cfg, seed)
        prompt_id = _queue_workflow(workflow, api_url)
        if logger:
            logger.info(f"  MMAudio: kolejka ({prompt_id[:8]}...) czekam...")

        # 3. Poll until done
        outputs = _poll_history(prompt_id, api_url)
        if outputs is None:
            if logger:
                logger.warning(f"  MMAudio: timeout po {_TIMEOUT_S}s")
            return False

        # 4. Find and download audio
        audio_info = _find_audio_in_outputs(outputs)
        if not audio_info:
            if logger:
                logger.warning("  MMAudio: brak pliku audio w outputs")
            return False

        audio_filename, audio_subfolder = audio_info
        audio_ext = Path(audio_filename).suffix or ".flac"
        audio_bytes = _download_audio(audio_filename, audio_subfolder, api_url)

        # 5. Merge into video
        if logger:
            logger.info(f"  MMAudio: merge audio ({audio_filename}) → {video_path.name}")
        ok = _merge_audio_into_video(video_path, audio_bytes, audio_ext, logger)

        if ok and logger:
            logger.success(f"  MMAudio: audio OK")
        elif not ok and logger:
            logger.warning(f"  MMAudio: merge nieudany, wideo bez audio")

        return ok

    except Exception as e:
        if logger:
            logger.warning(f"  MMAudio: błąd {e}")
        return False
