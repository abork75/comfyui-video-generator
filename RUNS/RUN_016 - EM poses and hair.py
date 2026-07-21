# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_016 - EM poses and hair.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_016 - EM poses and hair.yaml"))
# Generated: 2026-07-20 10:34:40
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\muszelka_pliki\\EM\\Poses and hair\\film'

FORCE_RESOLUTION = (
    880,
    1184,
)
DEFAULT_RESOLUTION = (
    880,
    1184,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 6
DEFAULT_CFG            = 2
DEFAULT_DURATION       = 2
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
        'file': '50.51. zaproszenie.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '50.51. zaproszenie.m4a',
            'pos': 'Man is waving his hips pennis is waving',
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '50.53. stan na bacznosc.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': '50.53. stan na bacznosc ale to juz.mp3',
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '50.55. tak jest prosze pani.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': '50.55. tak jest prosze pani.m4a',
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '50.57. to ma byc bacznosc.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': '50.57. to ma byc na bacznosc.mp3',
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '50.59. czy teraz dobrze.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': '50.59. czy teraz dobrze prosze pani.m4a',
        'width': 608,
        'height': 816,
    },

    {
        "chain": [
            {
                'duration': 1.5,
                'pos': "Camera makes smooth zoom on man's belly",
                'neg': '',
            },
        ],
        "chain_prefix": 'zoom in',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '50.61. idz na gore.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '50.61. moze byc marsz na gore.mp3',
            'pos': """A beautiful woman looks directly at the camera with a dominant, seductive expression. She holds a realistic whip in her left hand and points the tip of the whip straight toward the camera in a commanding gesture.

While speaking, she keeps the whip steadily pointed at the viewer, maintaining natural whip length without any stretching or deformation. The whip stays realistic, stiff and at correct proportions. Her right hand can rest on her hip or make a small emphasizing gesture. Strong eye contact, confident posture, slight head tilt.

Natural lip sync, realistic whip physics, no rubbery stretching, high detail, photorealistic animation.""",
            'neg': 'stretched whip, elongated whip, rubbery whip, deformed whip, unnaturally long whip, elastic whip, bad physics, warped object, whip stretching, two hands holding whip, blurry whip, low detail whip, floating whip, bad hand grip, unnatural bending, jerky motion, weak gesture, looking away from camera, shy expression',
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '50.63. biegiem na gore.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'Man turns back and rapidly runs upstairs',
                'neg': '',
            },
        ],
        "chain_prefix": 'bieg na gore',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '50.65. idzie w kierunku drzwi.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '50.65. bardzo posluszny.mp3',
            'pos': 'Woman is going slowly toward camera',
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '50.67 szpicruta.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """4-second I2V video: A detailed spiked whip floats in the air and spins dynamically. It rotates smoothly around its axis, performing several elegant full turns with natural flexibility and slight whipping motion.

The leather braid bends and springs realistically during the rotation. Beautiful play of light and shadows on the surface as it turns. Clean background, sharp focus, realistic physics, cinematic slow-motion feel, photorealistic, ultra detailed.""",
                'neg': 'static whip, no rotation, minimal movement, deformed whip, rubbery motion, stiff whip, bad physics, blurry rotation, low detail, floating without spinning, jerky movement, unnatural bending, artifacts, plastic texture, changed shape',
            },
        ],
        "chain_prefix": 'obroc szpicrute',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
