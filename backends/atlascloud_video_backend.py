# -*- coding: utf-8 -*-
"""
AtlasCloud Video Backend — WAN 2.7 image-to-video via AtlasCloud API.

Supports:
  I2V    (start frame only — chain steps, no end_frame)
  I2V2I  (start + end frame — transitions between two images/clips)

Resolution is set per-run in config['atlascloud_resolution'] (720P/1080P/1080P-SR/1440P-SR).
The API preserves input aspect ratio regardless of the resolution label.
"""

import os
import time
import base64
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

        fps / steps / blocks_to_swap / frame_interpolation are ignored
        (not supported by the cloud API).
        resolution / prompt_extend are taken from self.config.
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
            return result is not None and Path(output_path).exists()
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

    def _run_sync(
        self,
        start_frame, end_frame, output_path,
        positive_prompt, negative_prompt,
        duration, resolution, prompt_extend, seed,
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
