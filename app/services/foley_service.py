# -*- coding: utf-8 -*-
"""
Foley FX service — LTX 2.3 Foley LoRA + sliding-window V2A (video-to-audio),
running on the Linux/WSL2 ComfyUI instance (same backend as lipsync/deblur,
port 8189). Manual, opt-in alternative to MMAudio for single clips where
MMAudio's result is unacceptable (e.g. MMAudio's unremovable spurious
whispering) - see memory project_ltx_foley_sliding_window.md for the full
investigation and node-substitution recipe this workflow template embodies.

Much slower than MMAudio (minutes vs seconds) - this is why it's a manual
per-clip choice, not a default. FX only, not ambient: the sliding-window
mechanism has no cross-window continuity (validated separately), which is
fine for a single clip's one-shot FX event but was ruled out for multi-clip
ambient sequences on speed alone even where quality held up.

Fire-and-log, no status-polling state - mirrors app/api/audio.py's own
_run_audio_bg (MMAudio's FX path): progress goes to the WebSocket log panel,
there is no dedicated spinner widget for FX regen today (unlike lipsync/deblur).

Flow (mirrors deblur_service.py/lipsync_service.py for the ComfyUI plumbing):
  1. Copy clip -> ComfyUI input dir (unique temp name)
  2. ffprobe frame count -> round up to the nearest valid window/frame size
     (LTXFoleyWindowPlan/VideoToAudioLatent require frames % 8 == 1)
  3. Build workflow from template (swap video filename, prompts, frame count)
  4. POST to ComfyUI /prompt
  5. Poll /history/{prompt_id} + directory-scan fallback until the rendered
     video appears, then wait for it to stop growing
  6. Extract its audio track as the clip's FX sidecar mp3 (utils.mmaudio_utils
     fx_sidecar_path) - same convention as MMAudio's own FX, no archiving of
     a previous FX (matches add_audio_to_clip's own behavior: the UI confirm()
     dialog is the warning, not a kept backup)
"""

import asyncio
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from app.services import app_config_service
from app.services.deblur_service import (
    _http_post,
    _http_get,
    _find_video_in_outputs,
    _wait_for_stable_file,
)
from app.services.media_service import resolve_video, _project_folder
from app.services.process_service import process_service
from utils.mmaudio_utils import fx_sidecar_path, FALLBACK_AUDIO_PROMPT, FALLBACK_AUDIO_NEG_PROMPT

_WORKFLOW_PATH = Path(__file__).parent.parent.parent / "workflows" / "_LTX23_Foley.json"

# LTX Foley's own trained/demonstrated bucket is 89 frames; going well past it
# measurably softens timing precision on distinct events (see memory) - cap
# any single window there. Longer clips still work, just via more windows
# (LTXFoleyWindowPlan's own sliding-window logic), accepting the documented
# cross-window-consistency risk as a rare edge case for FX (unlike ambient,
# where that risk was the reason it got ruled out).
_MAX_WINDOW_FRAMES = 169
_MIN_WINDOW_FRAMES = 9


def _round_up_valid_frames(n: int) -> int:
    """Smallest m >= n with m % 8 == 1 (LTXFoleyWindowPlan's own requirement),
    clamped to [_MIN_WINDOW_FRAMES, _MAX_WINDOW_FRAMES]."""
    if n <= _MIN_WINDOW_FRAMES:
        return _MIN_WINDOW_FRAMES
    m = n + ((1 - n) % 8)
    return min(m, _MAX_WINDOW_FRAMES)


def _get_frame_count(path: Path) -> int:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-count_frames", "-show_entries", "stream=nb_read_frames",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, timeout=30, text=True,
        )
        val = r.stdout.strip()
        return int(val) if r.returncode == 0 and val.isdigit() else 0
    except Exception:
        return 0


async def _run_foley_bg(video_path: Path, sidecar_path: Path, prompt: str, negative_prompt: str) -> None:
    loop = asyncio.get_running_loop()
    _linux = app_config_service.get_backend("linux")
    foley_url = _linux.get("api_url")
    input_dir = Path(_linux["comfyui_input_dir"])
    output_dir = Path(_linux["comfyui_output_folder"]).parent

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    tmp_video_name = f"foley_{ts}_{video_path.name}"
    tmp_video = input_dir / tmp_video_name
    expected_prefix = f"ltx_foley_loop_{ts}"

    process_service.log_sys(f"🦊 LTX Foley: {video_path.name} → FX jako osobny plik ({sidecar_path.name})")

    try:
        # 1. Copy source clip -> ComfyUI input dir
        input_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(video_path), str(tmp_video))

        # 2. Frame count -> valid window size (see module docstring)
        frames = await loop.run_in_executor(None, _get_frame_count, tmp_video)
        window_frames = _round_up_valid_frames(frames if frames > 0 else _MIN_WINDOW_FRAMES)

        # 3. Build workflow from template
        workflow = json.loads(_WORKFLOW_PATH.read_text(encoding="utf-8"))
        workflow["1"]["inputs"]["file"] = tmp_video_name
        workflow["6"]["inputs"]["text"] = prompt
        workflow["7"]["inputs"]["text"] = negative_prompt
        workflow["9"]["inputs"]["window_frames"] = window_frames
        workflow["13"]["inputs"]["frames"] = window_frames
        workflow["28"]["inputs"]["filename_prefix"] = expected_prefix

        # 4. Submit to ComfyUI. Same WSL2/DrvFs settle-delay-and-retry pattern
        # as lipsync/deblur - a just-copied file can briefly look missing to
        # ComfyUI even though the Windows-side write already finished.
        def _submit():
            try:
                return _http_post(f"{foley_url}/prompt", {"prompt": workflow}, timeout=30)
            except OSError as e:
                if getattr(e, "errno", None) in (10061, 111):
                    raise RuntimeError(
                        f"Linux ComfyUI niedostępny ({foley_url}). Uruchom WSL2 ComfyUI i spróbuj ponownie."
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
                raise  # ComfyUI isn't even up - retrying won't help
            except Exception as e:
                _submit_err = e
            if _attempt < 2:
                await asyncio.sleep(1.5)
        if not resp or not resp.get("prompt_id"):
            raise _submit_err or RuntimeError(f"ComfyUI did not return prompt_id: {resp}")
        prompt_id = resp["prompt_id"]
        process_service.log_sys(f"🦊 LTX Foley: kolejka ComfyUI ({window_frames} klatek/okno)...")

        # 5. Poll for completion. CreateVideo+SaveVideo write ONE finished file
        # (audio already embedded via CreateVideo's own audio input) - unlike
        # VHS_VideoCombine there's no silent-draft-then-audio-remux race, so
        # no "-audio" suffix grace period needed here.
        max_polls = 800  # 800 x 3s ~= 40 min max - sliding-window over many windows is slow
        out_video_path: Path | None = None

        for _ in range(max_polls):
            await asyncio.sleep(3)

            try:
                def _check_history():
                    return _http_get(f"{foley_url}/history/{prompt_id}")

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
            if matches:
                out_video_path = matches[0]
                break
        else:
            raise RuntimeError("Timeout: Foley job did not complete within 40 minutes")

        if out_video_path is None or not out_video_path.exists():
            raise RuntimeError(f"Output file not found: {out_video_path}")

        # 6. Wait until ComfyUI finishes writing the file
        stable = await _wait_for_stable_file(out_video_path, poll_interval=2.0, stable_rounds=3, max_wait=120.0)
        file_size = out_video_path.stat().st_size if out_video_path.exists() else 0
        if not stable or file_size < 1024:
            raise RuntimeError(f"Output file incomplete after wait: {out_video_path.name} ({file_size} bytes)")

        # 7. Extract its audio track as the clip's FX sidecar mp3. No archiving
        # of a previous FX here - matches add_audio_to_clip's own MMAudio
        # path (the UI's confirm() dialog is the overwrite warning).
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_mp3 = sidecar_path.parent / f"_tmp_foley_{ts}.mp3"

        def _extract_audio() -> bool:
            r = subprocess.run(
                ["ffmpeg", "-y", "-i", str(out_video_path), "-vn", "-q:a", "2", str(tmp_mp3)],
                capture_output=True, timeout=60,
            )
            return r.returncode == 0 and tmp_mp3.exists() and tmp_mp3.stat().st_size > 0

        if not await loop.run_in_executor(None, _extract_audio):
            raise RuntimeError("ffmpeg: nie udało się wyodrębnić audio z wyniku Foley")

        if sidecar_path.exists():
            sidecar_path.unlink()
        tmp_mp3.rename(sidecar_path)

        try:
            out_video_path.unlink()
        except Exception:
            pass

        process_service.log_sys(f"[FX_READY] {video_path.name}")

    except Exception as exc:
        process_service.log_sys(f"❌ LTX Foley: {exc}")
    finally:
        try:
            if tmp_video.exists():
                tmp_video.unlink()
        except Exception:
            pass


# ── Public API ───────────────────────────────────────────────────────────────

def start_foley(
    run_filename: str, clip_name: str,
    audio_prompt: str = "", audio_negative_prompt: str = "",
) -> dict:
    """Queue a manual Foley FX job for a clip. Returns immediately, progress
    streamed to the log panel via WebSocket (same UX as MMAudio's own FX -
    see add_audio_to_clip/_run_audio_bg). Empty prompts fall back to
    FALLBACK_AUDIO_PROMPT/FALLBACK_AUDIO_NEG_PROMPT (same constants MMAudio's
    own FX path uses) - callers should already have resolved the
    request -> YAML-default -> fallback chain themselves before calling this."""
    video_path = resolve_video(run_filename, clip_name)
    if video_path is None:
        return {"ok": False, "error": f"Nie znaleziono klipu: {clip_name}"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono project_folder dla tego RUN"}

    sidecar_path = fx_sidecar_path(pf, clip_name)
    prompt = audio_prompt or FALLBACK_AUDIO_PROMPT
    negative_prompt = audio_negative_prompt or FALLBACK_AUDIO_NEG_PROMPT

    asyncio.create_task(_run_foley_bg(video_path, sidecar_path, prompt, negative_prompt))
    return {"ok": True}
