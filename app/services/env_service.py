# -*- coding: utf-8 -*-
"""
Environment service — health-check only.

Polls both ComfyUI instances and exposes their status to the UI.
Environments are started/stopped manually by the user.
"""

import asyncio
import urllib.request
from app.core.config import settings
from app.services import app_config_service


class EnvService:

    def _check_health_sync(self, url: str) -> bool:
        try:
            with urllib.request.urlopen(f"{url}/system_stats", timeout=3) as r:
                return r.status == 200
        except Exception:
            return False

    async def get_status(self) -> dict:
        linux_url   = app_config_service.get_backend("linux").get("api_url")   or settings.comfyui_url
        windows_url = app_config_service.get_backend("windows").get("api_url") or settings.comfyui_upscale_url
        loop = asyncio.get_running_loop()
        linux_ok, windows_ok = await asyncio.gather(
            loop.run_in_executor(None, self._check_health_sync, linux_url),
            loop.run_in_executor(None, self._check_health_sync, windows_url),
        )
        return {
            "linux":   "ready" if linux_ok   else "stopped",
            "windows": "ready" if windows_ok else "stopped",
        }


env_service = EnvService()
