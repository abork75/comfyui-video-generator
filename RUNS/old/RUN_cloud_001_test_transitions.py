# -*- coding: utf-8 -*-
"""
CLOUD TEST 001: First transition only (01→02)
Test Comfy.icu API integration

COST: ~$0.10 (1 transition @ 336x448, 2s)
TIME: ~0.8 min
"""

# ============================================================
# IMPORTANT: Add parent directory to path (RUNS/ subfolder)
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# Now imports work!
# ============================================================
from batch_transitions_cloud import run_batch_generation_cloud

# ============================================================
# COMFY.ICU WORKFLOW ID
# ============================================================

COMFY_ICU_WORKFLOW_ID = "fv9kYUtmjLzC5I8tRR49y"

# API keys read from environment variables:
# - COMFY_ICU_API_KEY (required)
# - IMGBB_API_KEY (required)

# ============================================================
# WORKFLOW TEMPLATE
# ============================================================

WORKFLOW_TEMPLATE_PATH = r"D:\streamlit_project\comfyui_integration\workflows\workflow-api-fv9kYUtmjLzC5I8tRR49y.json"

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\mixed_story"

FLOW = [
    {
        "file": "01_ewelina_sit.jpg",
        "duration": 2,
        "pos": "photograph springs to life, motion begins smoothly",
        "neg": "static photo, no motion, sudden jump",
    },
    {"file": "02_ewelina_braOFF.mp4"},
]

# ============================================================
# RESOLUTION - LOW (cheap tests)
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

DEFAULT_DURATION = 2
DEFAULT_FPS = 16
DEFAULT_STEPS = 15
DEFAULT_CFG = 4.0
DEFAULT_SEED = None

DEFAULT_POSITIVE_PROMPT = "smooth motion, high quality"
DEFAULT_NEGATIVE_PROMPT = "blurry, distorted, artifacts"

SKIP_MISSING = True
SKIP_EXISTED = False
IMAGE_QUALITY = 95
ASPECT_RATIO_TOLERANCE = 0.11
ASPECT_RATIO_STRATEGY = "most_common"

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    import os
    
    # Validate environment variables
    if not os.getenv('COMFY_ICU_API_KEY'):
        print("❌ ERROR: COMFY_ICU_API_KEY not set!")
        print("   Set: $env:COMFY_ICU_API_KEY = 'your_key'")
        exit(1)
    
    if not os.getenv('IMGBB_API_KEY'):
        print("❌ ERROR: IMGBB_API_KEY not set!")
        exit(1)
    
    print("\n" + "="*70)
    print("☁️  CLOUD TEST - Transition 1 (01→02)")
    print("="*70)
    print(f"Resolution: {MIN_WIDTH}x{MIN_HEIGHT}")
    print(f"Duration: {DEFAULT_DURATION}s, Steps: {DEFAULT_STEPS}")
    print(f"Estimated cost: ~$0.10")
    print("="*70 + "\n")
    
    config = {
        'project_folder': PROJECT_FOLDER,
        'flow': FLOW,
        'generic_prompts': {},
        'default_duration': DEFAULT_DURATION,
        'default_fps': DEFAULT_FPS,
        'default_steps': DEFAULT_STEPS,
        'default_cfg': DEFAULT_CFG,
        'default_seed': DEFAULT_SEED,
        'default_positive_prompt': DEFAULT_POSITIVE_PROMPT,
        'default_negative_prompt': DEFAULT_NEGATIVE_PROMPT,
        'min_width': MIN_WIDTH,
        'min_height': MIN_HEIGHT,
        'max_width': MAX_WIDTH,
        'max_height': MAX_HEIGHT,
        'default_resolution': DEFAULT_RESOLUTION,
        'force_resolution': FORCE_RESOLUTION,
        'skip_missing': SKIP_MISSING,
        'skip_existed': SKIP_EXISTED,
        'image_quality': IMAGE_QUALITY,
        'aspect_ratio_tolerance': ASPECT_RATIO_TOLERANCE,
        'aspect_ratio_strategy': ASPECT_RATIO_STRATEGY,
        'comfy_icu_api_key': '',  # Uses env COMFY_ICU_API_KEY
        'comfy_icu_workflow_id': COMFY_ICU_WORKFLOW_ID,
        'workflow_template_path': WORKFLOW_TEMPLATE_PATH,  # ← DODANE!
    }
    
    run_batch_generation_cloud(config)