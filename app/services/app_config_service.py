# -*- coding: utf-8 -*-
"""
Global application configuration service.

Reads / writes  app_config.yaml  (repo root).

Structure
─────────
  backends:
    linux:                  # WSL2 / Linux ComfyUI
      api_url, workflows_path, comfyui_output_folder
      models:
        video_gen:  { config_path }
        talk:       { workflow_json }
    windows:                # Windows ComfyUI (upscaler)
      api_url, input_dir, output_dir
      models:
        upscale:    { workflow_json }
    # external: ...
  defaults:
    resolution, fps, steps, cfg, duration, blocks_to_swap, frame_interpolation

Priority chain (highest → lowest):
  1. Per-project YAML  defaults:  section  (optional override)
  2. app_config.yaml              (this file)
  3. Hard-coded fallbacks below
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT      = Path(__file__).parent.parent.parent
APP_CONFIG_PATH = _REPO_ROOT / "app_config.yaml"

_DEFAULTS: dict[str, Any] = {
    "backends": {
        "linux": {
            "api_url":               "http://127.0.0.1:8189",
            "workflows_path":        "",
            "comfyui_output_folder": "",
            "models": {
                "video_gen": {"config_path":   ""},
                "talk":      {"workflow_json": ""},
            },
        },
        "windows": {
            "api_url":    "http://127.0.0.1:8100",
            "input_dir":  "",
            "output_dir": "",
            "models": {
                "upscale": {"workflow_json": ""},
                "i2i":     {"workflow_json": ""},
            },
        },
    },
    "defaults": {
        "resolution":          [1024, 1024],
        "fps":                 16,
        "steps":               6,
        "cfg":                 2.0,
        "duration":            2,
        "blocks_to_swap":      35,
        "frame_interpolation": True,
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _load_raw() -> dict:
    try:
        text = APP_CONFIG_PATH.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load() -> dict:
    """Return merged config: hard-coded defaults ← app_config.yaml."""
    return _deep_merge(_DEFAULTS, _load_raw())


def save(data: dict) -> None:
    """Persist *data* to app_config.yaml."""
    header = (
        "# app_config.yaml — Globalne ustawienia aplikacji\n"
        "# Edytuj ten plik aby zmienić modele i domyślne parametry.\n"
        "# Ustawienia per-projekt (defaults w RUN_*.yaml) nadpisują wartości "
        "z sekcji defaults.\n#\n"
    )
    body = yaml.dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=10_000,
    )
    APP_CONFIG_PATH.write_text(header + body, encoding="utf-8")


# ── Convenience accessors ────────────────────────────────────────────────────

def get_backend(name: str) -> dict:
    """
    Return the config dict for a backend, e.g. get_backend('linux').
    Keys depend on backend type (api_url always present).
    """
    return load().get("backends", {}).get(name, {})


def get_model(backend: str, model: str) -> dict:
    """
    Return a model config dict, e.g. get_model('linux', 'video_gen').
    Returns {} if backend or model not found.
    """
    return get_backend(backend).get("models", {}).get(model, {})


def get_defaults() -> dict:
    """Return defaults section."""
    return load().get("defaults", {})


def get_all() -> dict:
    """Return full config (for the API / UI)."""
    return load()
