# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_006 - zamtuz_przyklad.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_006 - zamtuz_przyklad.yaml"))
# Generated: 2026-08-17 19:36:25
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_006 - zamtuz przyklad_kary'

FORCE_RESOLUTION = (
    464,
    688,
)
DEFAULT_RESOLUTION = (
    464,
    688,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 20
DEFAULT_CFG            = 5
DEFAULT_DURATION       = 4
DEFAULT_BLOCKS_TO_SWAP      = 35
DEFAULT_FRAME_INTERPOLATION = True
DEFAULT_POSITIVE_PROMPT = 'smooth motion, high quality, cinematic'
DEFAULT_NEGATIVE_PROMPT = 'blurry, distorted, artifacts, watermark, text'
DEFAULT_AUDIO_PROMPT   = 'ambient sound, environmental audio, natural soundscape, high quality'
DEFAULT_AUDIO_NEGATIVE_PROMPT = 'music, melody, instruments, singing, low quality, distortion'
DEFAULT_SEED           = None
SKIP_MISSING           = True
SKIP_EXISTED           = True
IMAGE_QUALITY          = 95
ASPECT_RATIO_TOLERANCE = 0.13
ASPECT_RATIO_STRATEGY  = 'most_common'
DEBUG_LOG              = True

POSTPROCESSING = {'enabled': False}

# ── Linux backend paths ─────────────────────────────────────────
CONFIG_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflow_configs\\wan_i2v_config.yaml'
WORKFLOWS_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflows'
COMFYUI_OUTPUT_FOLDER = 'D:\\ComfyUI\\output\\video'
API_URL = 'http://127.0.0.1:8189'

USE_TEST_FLOW = False

# ============================================================
# FLOW
# ============================================================

FLOW_FULL = [
    {
        'file': 'Start1_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition totaly naked woman approachesy',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': 'Start2_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '01_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '05_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '06_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '07_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '04_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '08_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '09_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '10_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '11_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '13_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '12_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '14_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '15_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '16_przyklad.mp4',
        'backend': 'local',
        'duration': 0.5,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '17_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': 'END_przyklad.mp4',
        'backend': 'local',
        'duration': 0,
        'pos': 'NOT GENERATAD BEFORE CHAIN',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': 'Woman sits still in that position',
            },
        ],
        "chain_prefix": 'koniec',
        'backend': 'local',
        'fps': 16,
        'steps': 20,
        'cfg': 5.0,
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
    },

    {
        'file': 'END2_przyklad.mp4',
    },
]

FLOW_TEST = [
    {
        'file': 'Start1_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': 'Start2_przyklad.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
]

FLOW = FLOW_TEST if USE_TEST_FLOW else FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
