# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_008 - MKK_kara.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_008 - MKK_kara.yaml"))
# Generated: 2026-08-17 19:05:21
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_008 - MK kara'

FORCE_RESOLUTION = (
    960,
    720,
)
DEFAULT_RESOLUTION = (
    960,
    720,
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
        'file': '03.03 START.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.05. RozbierajSieDoNaga.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.07. PospieszSie.mp4',
        'backend': 'local',
        'duration': 4,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '03.09. grzecznie_wstaniesz.mp4',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'naked woman stands up and turning back to the camera, head bowed. Woman in black dress looking at her. Camera stands still same angle, same position of camera',
            },
            {
                'duration': 4,
                'pos': 'naked woman stands up and turning back to the camera, head bowed. Woman in black dress looking at her. Camera stands still same angle, same position of camera',
            },
            {
                'duration': 2,
                'pos': 'naked woman slowly walks towards left wall of room. hands along her body. Woman in black dress is waiting still and looking at naked woman. Camera stands still same angle, same position of camera',
            },
        ],
        "chain_prefix": 'go_to_wall',
        'backend': 'local',
        'fps': 16,
        'steps': 20,
        'cfg': 5.0,
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
    },

    {"break": True},

    {
        'file': '03.11. IdzWGlabSali.mp4',
        'backend': 'local',
        'duration': 5,
        'pos': 'A naked woman with empty hands walks deeper into the dimly lit room, moving away toward the far wall, while the woman in a tight black latex dress watches her intently from behind.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.13. IdzWGlabSali.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '04.05 wstep.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '04.07 wstep.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '04.09 wstep.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '04.11 wstep.mp4',
        'backend': 'local',
        'duration': 2,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.05_chlosta_1raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.07_chlosta_2raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'cfg': 5.0,
        'steps': 30,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg',
    },
    {
        'file': '05.08_12razow_p1.mp4',
        'backend': 'local',
        'duration': 1,
        'pos': 'Smooth transition',
        'cfg': 5.0,
        'steps': 30,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg',
    },
    {
        'file': '05.08_12razow_p2.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'cfg': 5.0,
        'steps': 30,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg',
    },
    {
        'file': '05.09_chlosta_3raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.11_chlosta_4raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.13_chlosta_5raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.15_chlosta_6raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.17_chlosta_7raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.19_chlosta_8raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.21_chlosta_9raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.23_chlosta_10raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.25_chlosta_11raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.27_chlosta_12raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.29_chlosta_13raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.31_chlosta_14raz.mp4',
        'backend': 'local',
        'duration': 5,
        'pos': 'camera smoothly zoom in',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.31_dodatkowe_razy.mp4',
        'backend': 'local',
        'duration': 3,
        'pos': 'Smooth transition, camera zoom out',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.33_chlosta_15raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.35_chlosta_16raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.37_chlosta_17raz.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.39_chlosta_18raz.mp4',
        'backend': 'local',
        'duration': 5,
        'pos': 'Camera smoothly zoom in.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.40 koniec_chlosty.mp4',
        'backend': 'local',
        'duration': 5,
        'pos': """Cinematic 5-second shot in dark BDSM dungeon, black brick walls, red neon ceiling light, green LED floor strips, hanging metal chains, leather padding.

0-4 seconds: exactly one naked athletic blonde woman with long hair slowly kneels facing the wall, places both hands high flat on the rough brick wall, knees slightly apart, back arched, head slightly bowed in total submission, remains perfectly still afterward. Visible red whip welts and stripes across her buttocks and upper thighs. Strong rim lighting from behind, dramatic red spotlight shadows emphasizing bare skin curves and vulnerability.

From 3.5 seconds: tall dominant woman in tight glossy black latex mini dress with deep cleavage, long flared sleeves, waist belt, extremely high black stilettos enters frame from right, stands proudly behind the kneeling girl. She looks down with cold contempt, superior sneer, aristocratic expression. Holds thin black riding crop loosely in right hand.

Photorealistic, ultra-detailed skin textures, cinematic moody color grading, deep blacks, strong red-green contrast, volumetric neon lighting, slow-motion from 3.5s onward, fluid natural human motion, no text, no watermark, 16:9""",
        'neg': 'blurry, low quality, deformed, extra limbs, mutated hands, bad anatomy, poorly drawn face, extra fingers, fused fingers, watermark, text, logo, cartoon, anime, 3d render, plastic skin, oversaturated, underexposed, overexposed, artifacts, jpeg noise, compression, multiple people interacting, sudden jumps, fast cuts, shaky camera, unrealistic proportions',
    },
    {
        'file': '05.41 koniec.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'dominant woman slowly turns 180 degrees with perfect elegant posture, chin high, dignified walk away from camera into dark shadows, slow confident swaying steps, glossy latex reflecting red and green lights. Static camera, shallow depth of field, focus stays on empty space where she stood and the motionless submissive woman facing wall.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.41 koniec_2.png',
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
