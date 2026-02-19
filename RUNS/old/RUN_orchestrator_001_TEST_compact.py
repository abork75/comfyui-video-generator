# -*- coding: utf-8 -*-
"""
ORCHESTRATOR TEST 001: Mixed cloud + local backends
First transition: CLOUD (01→02)
Second transition: LOCAL (03→04)

Total cost: ~$0.10 (only first transition)
Total time: ~1 min cloud + ~4 min local = ~5 min
"""

# ============================================================
# IMPORTANT: Add parent directory to path (RUNS/ subfolder)
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# Configs and validator
# ============================================================

from config_validator import validate_config_or_exit

# ============================================================
# Import orchestrator
# ============================================================
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\mixed_story"

# ============================================================
# FLOW - Mixed backends!
# ============================================================

FLOW = [
    # === Transition 1: Image→Video (CLOUD) ===
    {
        "file": "01_ewelina_sit.jpg",
        "backend": "cloud",  # ← CLOUD (fast, paid) "cloud"
        "duration": 2,
        "pos": "[image_to_video]",
        "neg": "[image_to_video]",
    },
    
    # === File B ===
    {"file": "02_ewelina_braOFF.mp4"},
    
    {"break": True},  # Hard cut
    
    # === Transition 2: Video→Image (LOCAL) ===
    {
        "file": "03._ewlina_panties_off.mp4",
        "backend": "local",  # ← LOCAL (slow, FREE)
        "duration": 4,
        "pos": "[video_to_image]",
        "neg": "[video_to_image]",
    },
    
    # === File D ===
    {"file": "04_ewlina_out.png"},
]

# ============================================================
# GENERIC PROMPTS
# ============================================================

GENERIC_PROMPTS = {
    "image_to_video": {
        "pos": "photograph springs to life, motion begins smoothly, gradual acceleration",
        "neg": "static photo, no motion, stays frozen, sudden jump",
    },
    
    "video_to_image": {
        "pos": "motion gradually slows down, freeze into photograph, cinematic stop",
        "neg": "sudden stop, abrupt freeze, jerky motion",
    },
}

# ============================================================
# RESOLUTION
# ============================================================

MIN_WIDTH = 336
MIN_HEIGHT = 448
MAX_WIDTH = 336
MAX_HEIGHT = 448
DEFAULT_RESOLUTION = (336, 448)
FORCE_RESOLUTION = None

# ============================================================
# GENERATION SETTINGS
# ============================================================

DEFAULT_DURATION = 4
DEFAULT_FPS = 16
DEFAULT_STEPS = 15
DEFAULT_CFG = 4.0
DEFAULT_SEED = None

DEFAULT_POSITIVE_PROMPT = "smooth motion, high quality"
DEFAULT_NEGATIVE_PROMPT = "blurry, distorted, artifacts"

SKIP_MISSING = True
SKIP_EXISTED = True  # Always regenerate for test
IMAGE_QUALITY = 95
ASPECT_RATIO_TOLERANCE = 0.10
ASPECT_RATIO_STRATEGY = "most_common"

# ============================================================
# BACKEND-SPECIFIC SETTINGS
# ============================================================

# Cloud (Comfy.icu)
COMFY_ICU_WORKFLOW_ID = "fv9kYUtmjLzC5I8tRR49y"
WORKFLOW_TEMPLATE_PATH = r"D:\streamlit_project\comfyui_integration\workflows\workflow-api-fv9kYUtmjLzC5I8tRR49y.json"

# Local (ComfyUI)
CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"D:\ComfyUI\output\video"

# ============================================================
# POSTPROCESSING CONFIG (opcjonalne)
# ============================================================

POSTPROCESSING = {
    'enabled': True,  # ← Master switch - Zmień na True aby uruchomić postprocessing
    
    # === Individual processors (można włączyć kilka naraz) ===
    
    'full_concat': True,  # Tworzy FULL_MOVIE_[project]_[timestamp].mp4
    
    'numbered_flow': True,  # Kopiuje pliki do FLOW_[project]_[timestamp]/
    
    # (Rozwojowo - na później)
    # 'upscale': False,
    # 'color_grade': False,
    # 'audio_overlay': False,
    # 'watermark': False,
    
    # === Settings per processor ===
    
    'full_concat_settings': {
        'output_name': None,  # None = auto: FULL_MOVIE_[project]_[timestamp].mp4
        'check_missing': True,  # Sprawdź kompletność FLOW
        'confirm_if_missing': True,  # Pytaj jeśli brakuje plików
        'video_codec': 'libx264',
        'crf': 18,
        'preset': 'medium',
    },
    
    'numbered_flow_settings': {
        'output_folder': None,  # None = auto: FLOW_[project]_[timestamp]
        'number_format': 'f{:04d}',  # f0001, f0002, ... (max 9999)
        'copy_only_from_flow': True,  # Tylko pliki z FLOW (ignore stare wersje)
    },
}

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    # Auto-build config from global variables + validate
    config = validate_config_or_exit(globals())
    
    # Run!
    run_batch_generation(config)