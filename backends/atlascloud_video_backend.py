# -*- coding: utf-8 -*-
"""
AtlasCloud Video Backend — WAN 2.7 image-to-video via AtlasCloud API.

Supports:
  I2V    (start frame only — chain steps, no end_frame)
  I2V2I  (start + end frame — transitions between two images/clips)

Resolution is set per-run in config['atlascloud_resolution'] (720P/1080P/1080P-SR/1440P-SR).
The API preserves input aspect ratio regardless of the resolution label.
After download, RIFE 2x frame interpolation is applied by default via local ComfyUI.
Pass frame_interpolation=False to skip.
"""

import json
import os
import shutil
import time
import base64
import uuid
from pathlib import Path

from .base_backend import BaseBackend
from workflow_base import Logger


_BASE_URL = "https://api.atlascloud.ai/api/v1/model"


class AtlasCloudVideoBackend(BaseBackend):
    """AtlasCloud WAN 2.7 image-to-video cloud backend."""

    def __init__(self, config):
        super().__init__(config)
        self.logger = Logger()
        self.api_key = os.getenv("ATLAS_CLOUD_API_KEY", "")

    # ── ABC stubs (logic lives in generate_transition override) ──────────────

    def validate_requirements(self):
        if not self.api_key:
            raise Exception(
                "ATLAS_CLOUD_API_KEY nie ustawiony — "
                "dodaj do zmiennych środowiskowych"
            )
        self.logger.success("AtlasCloud video backend gotowy (WAN 2.7)")
        return True

    def prepare_inputs(self, pair, workflow):
        return pair

    def execute(self, inputs, params, workflow):
        return self._run_sync(
            start_frame=inputs["start_frame"],
            end_frame=inputs.get("end_frame"),
            output_path=params["output_path"],
            positive_prompt=params.get("pos_prompt", ""),
            negative_prompt=params.get("neg_prompt", ""),
            duration=int(params.get("duration", 5)),
            resolution=params.get("atlascloud_resolution", "1080P"),
            prompt_extend=params.get("atlascloud_prompt_extend", True),
            seed=params.get("seed", -1),
        )

    def cleanup(self, inputs):
        pass

    def estimate_cost(self, params):
        duration = params.get("duration", 5)
        usd = round(duration * 0.15, 3)   # ~$0.75 / 5 s
        return {"credits": 0, "usd": usd, "time_min": 3.0}

    # ── Main entry point ─────────────────────────────────────────────────────

    def generate_transition(
        self,
        start_frame, end_frame, output_path,
        duration, fps, steps, cfg, seed,
        positive_prompt, negative_prompt,
        width, height,
        blocks_to_swap=None, frame_interpolation=None,
    ):
        """
        Override BaseBackend — maps I2V/I2V2I to AtlasCloud /generateVideo.

        steps / cfg / blocks_to_swap are ignored (not supported by the cloud API).
        resolution / prompt_extend are taken from self.config.
        frame_interpolation=False skips RIFE post-processing; default is True.
        """
        resolution    = self.config.get("atlascloud_resolution",    "1080P")
        prompt_extend = self.config.get("atlascloud_prompt_extend", True)

        mode = "I2V" if (end_frame is None) else "I2V2I"
        self.logger.info(
            f"  ☁ AtlasCloud WAN 2.7 — {mode} · {duration}s · {resolution}"
        )

        try:
            result = self._run_sync(
                start_frame=start_frame,
                end_frame=end_frame,
                output_path=Path(output_path),
                positive_prompt=positive_prompt or "",
                negative_prompt=negative_prompt or "",
                duration=int(max(2, min(15, duration))),
                resolution=resolution,
                prompt_extend=prompt_extend,
                seed=seed if seed is not None else -1,
            )
            if result is None or not Path(output_path).exists():
                return False

            # RIFE 2x frame interpolation (disable with frame_interpolation=False)
            if frame_interpolation is not False:
                self._rife_interpolate(Path(output_path), fps=fps or 16)

            return True
        except Exception as exc:
            self.logger.error(f"  ✗ AtlasCloud błąd: {exc}")
            return False

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _b64(path):
        path = Path(path)
        suffix = path.suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode()
        return f"data:{mime};base64,{data}"

    @staticmethod
    def _b64_audio(path: Path) -> str:
        path = Path(path)
        mime = "audio/mpeg" if path.suffix.lower() == ".mp3" else "audio/wav"
        data = base64.b64encode(path.read_bytes()).decode()
        return f"data:{mime};base64,{data}"

    @staticmethod
    def _audio_duration(path: Path) -> float:
        """Return audio duration in seconds via ffprobe, or 5.0 on failure."""
        import subprocess
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "quiet", "-print_format", "json",
                 "-show_streams", "-select_streams", "a:0", str(path)],
                capture_output=True, text=True, timeout=10,
            )
            streams = json.loads(result.stdout).get("streams", [])
            if streams:
                dur = float(streams[0].get("duration") or 0)
                if dur:
                    return dur
        except Exception:
            pass
        return 5.0

    # known ComfyUI ports to probe when the configured api_url is unavailable
    _RIFE_PROBE_PORTS = [8000, 8188, 8189]

    def _find_comfyui_url(self) -> str | None:
        """Return the first reachable ComfyUI base URL, or None."""
        import requests

        candidates = [self.config.get("api_url", "")]
        for port in self._RIFE_PROBE_PORTS:
            url = f"http://127.0.0.1:{port}"
            if url not in candidates:
                candidates.append(url)

        for url in candidates:
            if not url:
                continue
            try:
                requests.get(f"{url}/system_stats", timeout=2).raise_for_status()
                return url
            except Exception:
                continue
        return None

    @staticmethod
    def _probe_video_info(video_path: Path) -> tuple[int, int, int]:
        """Return (fps, width, height) via ffprobe, or (16, 0, 0) on failure."""
        import subprocess
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "quiet",
                    "-print_format", "json",
                    "-show_streams", "-select_streams", "v:0",
                    str(video_path),
                ],
                capture_output=True, text=True, timeout=10,
            )
            streams = json.loads(result.stdout).get("streams", [])
            if streams:
                s = streams[0]
                w = int(s.get("width", 0))
                h = int(s.get("height", 0))
                # nb_frames/duration is the most accurate display fps —
                # r_frame_rate and avg_frame_rate can be wrong for H.264/VFR
                nb = int(s.get("nb_frames") or 0)
                dur = float(s.get("duration") or 0)
                if nb and dur:
                    fps = max(1, round(nb / dur))
                else:
                    fps_str = s.get("avg_frame_rate") or s.get("r_frame_rate", "16/1")
                    num, den = map(int, fps_str.split("/"))
                    fps = max(1, round(num / den))
                return fps, w, h
        except Exception:
            pass
        return 16, 0, 0

    def _rife_interpolate(self, video_path: Path, fps: int = 16) -> bool:
        """Upload video to local ComfyUI, run RIFE 2x, replace file in-place."""
        import requests

        actual_fps, w, h = self._probe_video_info(video_path)
        self.logger.info(f"  [RIFE] wykryto {actual_fps}fps {w}x{h}")

        api_url = self._find_comfyui_url()
        if api_url is None:
            self.logger.error(
                "  RIFE: brak działającego ComfyUI "
                f"(próbowano porty {self._RIFE_PROBE_PORTS}) — pomijam"
            )
            return False

        out_base = Path(self.config.get("comfyui_output_folder", ""))
        # comfyui_output_folder is e.g. D:\ComfyUI\output\Wan22_I2V
        # parent → D:\ComfyUI\output
        comfy_out = out_base.parent if out_base.name else out_base

        wf_path = Path(__file__).parent.parent / "workflows" / "rife_interpolate.json"
        if not wf_path.exists():
            self.logger.error("  RIFE: brak rife_interpolate.json — pomijam")
            return False

        # 1. Upload video to ComfyUI input
        self.logger.info(f"  [RIFE] przesyłanie wideo ({api_url})…")
        try:
            with open(video_path, "rb") as f:
                up = requests.post(
                    f"{api_url}/upload/image",
                    files={"image": (video_path.name, f, "video/mp4")},
                    data={"type": "input", "subfolder": ""},
                    timeout=60,
                )
            up.raise_for_status()
            uploaded_name = up.json()["name"]
        except Exception as exc:
            self.logger.error(f"  RIFE upload błąd: {exc} — pomijam")
            return False

        # 2. Patch workflow: input filename, real dimensions, output fps = input fps (slow-motion 2×)
        workflow = json.loads(wf_path.read_text(encoding="utf-8"))
        workflow["1"]["inputs"]["video"]      = uploaded_name
        if w and h:
            workflow["1"]["inputs"]["custom_width"]  = w
            workflow["1"]["inputs"]["custom_height"] = h
        workflow["3"]["inputs"]["frame_rate"] = actual_fps

        # 3. Submit to ComfyUI queue
        client_id = str(uuid.uuid4())
        try:
            qr = requests.post(
                f"{api_url}/prompt",
                json={"prompt": workflow, "client_id": client_id},
                timeout=30,
            )
            qr.raise_for_status()
            prompt_id = qr.json()["prompt_id"]
        except Exception as exc:
            self.logger.error(f"  RIFE submit błąd: {exc} — pomijam")
            return False

        self.logger.info(
            f"  [RIFE] {prompt_id[:8]}… interpolacja 2x → {actual_fps}fps slow-motion…"
        )

        # 4. Poll /history until done, then locate output file
        t0 = time.monotonic()
        rife_file = None
        while time.monotonic() - t0 < 300:
            time.sleep(3)
            try:
                hist = requests.get(
                    f"{api_url}/history/{prompt_id}", timeout=10
                ).json()
            except Exception:
                continue
            if prompt_id not in hist:
                continue
            if hist[prompt_id].get("status", {}).get("status_str") == "error":
                self.logger.error("  RIFE: błąd ComfyUI — pomijam")
                return False
            for node_out in hist[prompt_id].get("outputs", {}).values():
                for vid in node_out.get("gifs", []):
                    # prefer fullpath from history (avoids D:/C: drive mismatch)
                    fp = vid.get("fullpath")
                    if fp:
                        candidate = Path(fp)
                    else:
                        sub  = vid.get("subfolder", "")
                        name = vid["filename"]
                        candidate = comfy_out / sub / name if sub else comfy_out / name
                    if candidate.exists():
                        rife_file = candidate
                        break
                if rife_file:
                    break
            if rife_file:
                break
            self.logger.info(
                f"  [RIFE] czekam… ({int(time.monotonic() - t0)}s)"
            )

        if not rife_file:
            self.logger.error("  RIFE: timeout lub brak pliku — pomijam")
            return False

        # 5. Replace original with RIFE output
        shutil.move(str(rife_file), str(video_path))
        size_mb = video_path.stat().st_size / 1_048_576
        self.logger.success(
            f"  ✓ RIFE 2x → {video_path.name} ({size_mb:.1f} MB, {actual_fps}fps slow-mo ×2)"
        )
        return True

    def generate_talk_clip(
        self,
        source_image: Path,
        audio_entries: list,
        dest_path: Path,
        width: int = 480,
        height: int = 832,
        frame_interpolation=None,
        atlascloud_resolution: str | None = None,
        atlascloud_prompt_extend=None,
    ) -> bool:
        """
        AtlasCloud talk clip (lip-sync) via /generateVideo with 'audio' field.

        Each audio_entry = {'path': Path, 'pos': str, 'neg': str}.
        Multi-segment clips are concatenated with ffmpeg.
        """
        import subprocess

        resolution    = atlascloud_resolution    or self.config.get("atlascloud_resolution",    "1080P")
        prompt_extend = atlascloud_prompt_extend if atlascloud_prompt_extend is not None \
                        else self.config.get("atlascloud_prompt_extend", True)

        segments: list[Path] = []
        try:
            for idx, entry in enumerate(audio_entries):
                audio_path = Path(entry["path"])
                pos = str(entry.get("pos", "") or "")
                neg = str(entry.get("neg", "") or "")

                raw_dur = self._audio_duration(audio_path)
                dur = max(2, min(15, round(raw_dur)))
                audio_b64 = self._b64_audio(audio_path)

                self.logger.info(
                    f"  ☁ AtlasCloud Talk — segment {idx + 1}/{len(audio_entries)} "
                    f"· {dur}s · {resolution}"
                )

                seg_path = dest_path.parent / f"_talkac_{idx}_{dest_path.name}"
                result = self._run_sync(
                    start_frame=source_image,
                    end_frame=None,
                    output_path=seg_path,
                    positive_prompt=pos,
                    negative_prompt=neg,
                    duration=dur,
                    resolution=resolution,
                    prompt_extend=prompt_extend,
                    seed=-1,
                    audio=audio_b64,
                )
                if result is None or not seg_path.exists():
                    self.logger.error(
                        f"  ✗ Talk segment {idx + 1} nieudany"
                    )
                    return False
                segments.append(seg_path)

        except Exception as exc:
            self.logger.error(f"  ✗ AtlasCloud talk błąd: {exc}")
            return False

        # Concatenate segments or move single result to dest
        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if len(segments) == 1:
                shutil.move(str(segments[0]), str(dest_path))
            else:
                list_file = dest_path.parent / f"_talkac_list_{dest_path.stem}.txt"
                list_file.write_text(
                    "\n".join(f"file '{s}'" for s in segments),
                    encoding="utf-8",
                )
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                     "-i", str(list_file), "-c", "copy", str(dest_path)],
                    check=True, capture_output=True, timeout=120,
                )
                list_file.unlink(missing_ok=True)
                for s in segments:
                    if s.exists():
                        s.unlink()
        except Exception as exc:
            self.logger.error(f"  ✗ Talk concat błąd: {exc}")
            return False

        # RIFE — same default as video transitions; disable with frame_interpolation=False
        fi_cfg = self.config.get("frame_interpolation", True)
        should_rife = (frame_interpolation is not False) and (fi_cfg is not False)
        if should_rife:
            self._rife_interpolate(dest_path)

        return dest_path.exists()

    def _run_sync(
        self,
        start_frame, end_frame, output_path,
        positive_prompt, negative_prompt,
        duration, resolution, prompt_extend, seed,
        audio: str | None = None,
    ):
        import requests

        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "model":           "alibaba/wan-2.7/image-to-video",
            "image":           self._b64(start_frame),
            "prompt":          positive_prompt,
            "negative_prompt": negative_prompt,
            "resolution":      resolution,
            "duration":        duration,
            "prompt_extend":   prompt_extend,
            "seed":            seed,
        }

        if audio:
            payload["audio"] = audio
        if end_frame and Path(end_frame).exists():
            payload["last_image"] = self._b64(end_frame)

        # ── submit (retry on rate limit) ──────────────────────────────────
        _retry_delays = [15, 30, 60]
        resp = None
        for attempt, delay in enumerate([0] + _retry_delays, start=1):
            if delay:
                self.logger.info(
                    f"  [AtlasCloud] rate limit — czekam {delay}s "
                    f"(próba {attempt}/4)…"
                )
                time.sleep(delay)
            resp = requests.post(
                f"{_BASE_URL}/generateVideo",
                headers=headers, json=payload, timeout=30,
            )
            if resp.status_code == 200:
                break
            if resp.status_code == 429 and attempt <= len(_retry_delays):
                continue
            raise RuntimeError(
                f"AtlasCloud submit HTTP {resp.status_code}: {resp.text[:300]}"
            )

        prediction_id = resp.json().get("data", {}).get("id")
        if not prediction_id:
            raise RuntimeError(
                f"AtlasCloud: brak prediction_id w odpowiedzi: {resp.text[:300]}"
            )

        self.logger.info(
            f"  [AtlasCloud] prediction {prediction_id} — generowanie…"
        )

        # ── poll ──────────────────────────────────────────────────────────
        poll_url     = f"{_BASE_URL}/prediction/{prediction_id}"
        poll_headers = {"Authorization": f"Bearer {self.api_key}"}
        timeout_s    = 600   # 10 min — generous for long/SR videos
        t0 = time.monotonic()

        video_url = None
        while time.monotonic() - t0 < timeout_s:
            time.sleep(4)
            pr     = requests.get(poll_url, headers=poll_headers, timeout=15)
            data   = pr.json().get("data", {})
            status = data.get("status", "")
            elapsed = int(time.monotonic() - t0)
            self.logger.info(f"  [AtlasCloud] {status} ({elapsed}s)…")

            if status in ("completed", "succeeded"):
                outputs = data.get("outputs", [])
                if not outputs:
                    raise RuntimeError(
                        "AtlasCloud: status completed ale brak outputs"
                    )
                video_url = outputs[0]
                break
            if status == "failed":
                raise RuntimeError(
                    f"AtlasCloud: generowanie nie powiodło się — "
                    f"{data.get('error', '?')}"
                )
        else:
            raise RuntimeError(
                f"AtlasCloud: timeout po {timeout_s}s "
                f"(prediction_id={prediction_id})"
            )

        # ── download MP4 ──────────────────────────────────────────────────
        self.logger.info(f"  [AtlasCloud] pobieranie wideo…")
        vr = requests.get(video_url, timeout=120)
        vr.raise_for_status()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(vr.content)

        size_mb = Path(output_path).stat().st_size / 1_048_576
        self.logger.success(
            f"  ✓ {Path(output_path).name} ({size_mb:.1f} MB) — "
            f"{int(time.monotonic() - t0)}s"
        )
        return Path(output_path)
