# -*- coding: utf-8 -*-
"""
RUN_005: Samantha Fox - Nothing Gonna Stop Me Now
WITH BATCH UPSCALING POSTPROCESSING

Complete workflow:
1. Video generation (batch_transitions)
2. Numbered flow (copy to FLOW_* folder)
3. Full concat (merge all clips)
4. Batch upscale (GAN upscaling with interactive source selection)

Author: abork75
Date: 2026-02-19
"""

# ============================================================
# IMPORTANT: Add parent directory to path (RUNS/ subfolder)
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# Core imports: Config validation and orchestrator
# ============================================================
from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\muszelka_pliki\EM\zamtuz\przyklad_kary"

# ============================================================
# FLOW - Select test or full production
# ============================================================

USE_TEST_FLOW = False  # ← Change to False for full production run

FLOW_TEST = [
    # ============================================================
    # SEQUENCE 1: PRZED USC
    # ============================================================
    
     {
        "file": "Start1_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
  
    {
        "file": "Start2_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "NONE",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    
]

FLOW_FULL = [  

    # ============================================================
    # SEQUENCE 1: Scena na jachcie
    # ============================================================
     {
        "file": "Start1_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition totaly naked woman approachesy",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
  
    {
        "file": "Start2_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "NONE",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "01_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "03_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "02_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {"break": True},

    {
        "file": "05_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "06_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "07_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {"break": True},

    {
        "file": "04_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },


    {
        "file": "08_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "09_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "10_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "11_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "13_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "12_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {"break": True},

    {
        "file": "14_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "15_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "16_przyklad.mp4",
        "backend": "local",
        "duration": 0.5,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "17_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "END_przyklad.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {    
        "chain": [
            {
                "duration": 5, 
                "pos": "Woman sits still in that position"
            },
        ],
        "chain_prefix": "koniec",
        "backend": "local",
        "fps": 16,
        "steps": 20,  # ← Zwiększone z 15 (hi-res quality!)
        "cfg": 5.0,   # ← Zwiększone z 4.0 (stronger guidance)
        "neg": "static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality",        

        # "transition_to_next": {
            # "duration": 4,
            # "steps": 20,
            # "pos": "Woman is slowly standing up"
        # }
    
    },
    # {"file": "END2_przyklad.mp4"}
    

]

FLOW = FLOW_TEST if USE_TEST_FLOW else FLOW_FULL

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
# RESOLUTION SETTINGS
# ============================================================

MIN_WIDTH = 336
MIN_HEIGHT = 448
MAX_WIDTH = 336
MAX_HEIGHT = 448
DEFAULT_RESOLUTION = (336, 448)
FORCE_RESOLUTION = (464, 688)  # None for auto

# ============================================================
# GENERATION SETTINGS
# ============================================================

DEFAULT_DURATION = 4
DEFAULT_FPS = 16
DEFAULT_STEPS = 20
DEFAULT_CFG = 5.0
DEFAULT_SEED = None

DEFAULT_POSITIVE_PROMPT = "smooth motion, high quality"
DEFAULT_NEGATIVE_PROMPT = "blurry, distorted, artifacts"

SKIP_MISSING = True
SKIP_EXISTED = True
IMAGE_QUALITY = 95
ASPECT_RATIO_TOLERANCE = 0.13
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
# POSTPROCESSING CONFIG
# Sequential execution: numbered_flow → full_concat → upscale
# ============================================================

POSTPROCESSING = {
    # Master switch
    'enabled': False,  # ← Set to True to enable postprocessing
    
    # === Individual processors (executed in order) ===
    
    # Step 1: Copy to numbered FLOW folder
    'numbered_flow': True,  # Creates FLOW_[project]_[timestamp]/ with f0001, f0002, ...
    
    # Step 2: Concatenate all clips into single movie
    'full_concat': False,  # Creates FULL_MOVIE_[project]_[timestamp].mp4
    
    # Step 3: Upscale (NEW!)
    'upscale': False,  # Batch GAN upscaling with interactive source selection
    
    # Future processors (disabled for now)
    # 'color_grade': False,
    # 'audio_overlay': False,
    # 'watermark': False,
    
    # === Settings per processor ===
    
    'numbered_flow_settings': {
        'output_folder': None,  # None = auto: FLOW_[project]_[timestamp]
        'number_format': 'f{:04d}',  # f0001, f0002, ... (max 9999)
        'copy_only_from_flow': True,  # Only files from FLOW (ignore old versions)
    },
    
    'full_concat_settings': {
        'output_name': None,  # None = auto: FULL_MOVIE_[project]_[timestamp].mp4
        'check_missing': True,  # Check FLOW completeness
        'confirm_if_missing': True,  # Ask if files missing
        'video_codec': 'libx264',
        'crf': 18,
        'preset': 'medium',
        'fps': 16,
    },
    
    'upscale_settings': {
        # Source selection mode:
        # 'interactive' - Ask user to choose (project source / FLOW folder / full movie)
        # 'source' - Upscale from project dirs (main, chain, transitions)
        # 'numbered_flow' - Upscale latest FLOW folder
        # 'full_movie' - Upscale full concat movie
        'source_mode': 'interactive',
        
        # Upscale parameters
        'target_resolution': (1920, 1440),
        'upscale_model': 'RealESRGAN_x4plus.pth',
        'interpolation': 'lanczos',  # lanczos (best), bicubic, bilinear, nearest
        'method': 'stretch',  # stretch, crop, fit
        
        # ComfyUI connection
        'comfyui_server': 'http://127.0.0.1:8100',
        'comfyui_output_folder': 'D:/ComfyUI/output',
    },
}

# ============================================================
# DEBUG SETTINGS
# ============================================================

DEBUG_LOG = True  # True = verbose, False = clean production logs

# ============================================================
# RUN - Minimal execution code (logic in orchestrators)
# ============================================================

if __name__ == "__main__":
    # Auto-build config from global variables + validate
    config = validate_config_or_exit(globals())
    
    # Run batch generation (includes postprocessing if enabled)
    run_batch_generation(config)