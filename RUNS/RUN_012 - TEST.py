# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_012 TEST.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_012 TEST.yaml"))
# Generated: 2026-06-04 10:55:09
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\muszelka_pliki\\obce\\oponka\\film'

FORCE_RESOLUTION = (
    440,
    592,
)
DEFAULT_RESOLUTION = (
    440,
    592,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 6
DEFAULT_CFG            = 2.0
DEFAULT_DURATION       = 2
DEFAULT_BLOCKS_TO_SWAP      = 35
DEFAULT_FRAME_INTERPOLATION = True
DEFAULT_SEED           = None
SKIP_MISSING           = True
SKIP_EXISTED           = True
IMAGE_QUALITY          = 95
ASPECT_RATIO_TOLERANCE = 0.13
ASPECT_RATIO_STRATEGY  = 'most_common'
DEBUG_LOG              = True

POSTPROCESSING = {'enabled': False}

# ── Linux backend paths ─────────────────────────────────────────
CONFIG_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflow_configs\\wan_i2v.yaml'
WORKFLOWS_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflows'
COMFYUI_OUTPUT_FOLDER = 'D:\\ComfyUI\\output\\Wan22_I2V'
API_URL = 'http://127.0.0.1:8189'

USE_TEST_FLOW = False

# ============================================================
# FLOW
# ============================================================

FLOW_FULL = [
    {
        'file': '10.51. prawy przod.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Woman appears',
        'neg': 'NONE',
    },
    {
        'file': '10.53. on scene.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Move',
                'neg': '',
            },
        ],
        "chain_prefix": 'chain source of talk',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'talk',
        'audio': '13.79. ktos przyjechal.mp3',
        'width': 448,
        'height': 592,
        'transition': {
            'duration': 2,
            'pos': 'Women is running out of garrage',
        },
    },

    {
        'file': '10.51. prawy przod TEST1.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '11.53. on scene.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': '11.57. Gdzie ten lewarek.mp3',
        'width': 448,
        'height': 592,
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'wave hand',
                'neg': '',
            },
            {
                'duration': 3,
                'pos': 'move and kneel at the table',
                'neg': '',
            },
        ],
        "chain_prefix": 'talk is source of chain',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '11.55 gdzie ten lewarek.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
