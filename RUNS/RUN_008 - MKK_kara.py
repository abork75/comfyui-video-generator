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

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\muszelka_pliki\MKK\kara"

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
        "file": "03.03 START.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
    
    {
        "file": "03.05. RozbierajSieDoNaga.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "03.07. PospieszSie.mp4",
        "backend": "local",
        "duration": 4,
        "pos": "NONE",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {"break": True},

    {"file": "03.09. grzecznie_wstaniesz.mp4"},
    
    {
        "chain": [
            {
                "duration": 2, 
                "pos": "naked woman stands up and turning back to the camera, head bowed. Woman in black dress looking at her. Camera stands still same angle, same position of camera"
            },
            {
                "duration": 4, 
                "pos": "naked woman stands up and turning back to the camera, head bowed. Woman in black dress looking at her. Camera stands still same angle, same position of camera"
            },
            {
                "duration": 2, 
                "pos": "naked woman slowly walks towards left wall of room. hands along her body. Woman in black dress is waiting still and looking at naked woman. Camera stands still same angle, same position of camera"
            },
        ],
        "chain_prefix": "go_to_wall",
        "backend": "local",
        "fps": 16,
        "steps": 20,  # ← Zwiększone z 15 (hi-res quality!)
        "cfg": 5.0,   # ← Zwiększone z 4.0 (stronger guidance)
        "neg": "static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality",
        
        # ============================================================
        # Optional: Transition to next (jeśli dodasz następny plik)
        # ============================================================
        # "transition_to_next": {
        #     "duration": 4,
        #     "steps": 20,
        #     "pos": "woman gradually slows walking pace, steps decelerating smoothly, comes to gentle stop, feet settling into standing position, smooth continuous deceleration, natural halt"
        # }
    },

    {"break": True},

    {
        "file": "03.11. IdzWGlabSali.mp4",
        "backend": "local",
        "duration": 5,
        "pos": "A naked woman with empty hands walks deeper into the dimly lit room, moving away toward the far wall, while the woman in a tight black latex dress watches her intently from behind.",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "03.13. IdzWGlabSali.png",
        "backend": "local",
        "duration": 0,
        "pos": "NONE",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },


    {"break": True},

    {
        "file": "04.05 wstep.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },


    {
        "file": "04.07 wstep.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "04.09 wstep.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "04.11 wstep.mp4",
        "backend": "local",
        "duration": 2,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.05_chlosta_1raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.07_chlosta_2raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "cfg": 5.0,
        "steps": 30,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg",
    },

    {    
        "file": "05.08_12razow_p1.mp4",
        "backend": "local",
        "duration": 1,
        "pos": "Smooth transition",
        "cfg": 5.0,
        "steps": 30,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg",
    },    

    {
        "file": "05.08_12razow_p2.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "cfg": 5.0,
        "steps": 30,
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg",
    },

    {
        "file": "05.09_chlosta_3raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.11_chlosta_4raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.13_chlosta_5raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.15_chlosta_6raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.17_chlosta_7raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.19_chlosta_8raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.21_chlosta_9raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.23_chlosta_10raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.25_chlosta_11raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.27_chlosta_12raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.29_chlosta_13raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.31_chlosta_14raz.mp4",
        "backend": "local",
        "duration": 5,
        "pos": "camera smoothly zoom in",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.31_dodatkowe_razy.mp4",
        "backend": "local",
        "duration": 3,
        "pos": "Smooth transition, camera zoom out",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.33_chlosta_15raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.35_chlosta_16raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.37_chlosta_17raz.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.39_chlosta_18raz.mp4",
        "backend": "local",
        "duration": 5,
        "pos": "Camera smoothly zoom in.",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {
        "file": "05.40 koniec_chlosty.mp4",
        "backend": "local",
        "duration": 5,
        "pos": """Cinematic 5-second shot in dark BDSM dungeon, black brick walls, red neon ceiling light, green LED floor strips, hanging metal chains, leather padding. 

0-4 seconds: exactly one naked athletic blonde woman with long hair slowly kneels facing the wall, places both hands high flat on the rough brick wall, knees slightly apart, back arched, head slightly bowed in total submission, remains perfectly still afterward. Visible red whip welts and stripes across her buttocks and upper thighs. Strong rim lighting from behind, dramatic red spotlight shadows emphasizing bare skin curves and vulnerability.

From 3.5 seconds: tall dominant woman in tight glossy black latex mini dress with deep cleavage, long flared sleeves, waist belt, extremely high black stilettos enters frame from right, stands proudly behind the kneeling girl. She looks down with cold contempt, superior sneer, aristocratic expression. Holds thin black riding crop loosely in right hand.

Photorealistic, ultra-detailed skin textures, cinematic moody color grading, deep blacks, strong red-green contrast, volumetric neon lighting, slow-motion from 3.5s onward, fluid natural human motion, no text, no watermark, 16:9""",
        "neg": "blurry, low quality, deformed, extra limbs, mutated hands, bad anatomy, poorly drawn face, extra fingers, fused fingers, watermark, text, logo, cartoon, anime, 3d render, plastic skin, oversaturated, underexposed, overexposed, artifacts, jpeg noise, compression, multiple people interacting, sudden jumps, fast cuts, shaky camera, unrealistic proportions",
    },

    {
        "file": "05.41 koniec.png",
        "backend": "local",
        "duration": 3,
        "pos": "dominant woman slowly turns 180 degrees with perfect elegant posture, chin high, dignified walk away from camera into dark shadows, slow confident swaying steps, glossy latex reflecting red and green lights. Static camera, shallow depth of field, focus stays on empty space where she stood and the motionless submissive woman facing wall.",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {"file": "05.41 koniec_2.png"},
  

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
FORCE_RESOLUTION = (960, 720)  # None for auto

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