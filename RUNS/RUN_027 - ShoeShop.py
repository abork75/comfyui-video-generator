# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_027 - ShoeShop.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_027 - ShoeShop.yaml"))
# Generated: 2026-08-21 09:02:43
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_027 - ShoeShop'

FORCE_RESOLUTION = (
    896,
    1152,
)
DEFAULT_RESOLUTION = (
    896,
    1152,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 8
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
        'file': '50.51. pose.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'sexy_dance, They do a sexy dance. They thrusts and sways her hips in a sexual manner. Next they kneeling down.',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'Quiet exclusive shoe store ambience, soft footsteps on wooden floor, gentle rustling of tissue paper, quiet voices in the distance, soft door chime, subtle clothing and shoe movement sounds, calm refined atmosphere, low-level ambient room tone',
                'audio_negative_prompt': 'supermarket, hypermarket, loud announcements, shopping carts, beeping scanners, crowded noise, loud music, heavy bass, traffic, street noise, strong reverb, distorted audio',
            },
            {
                'duration': 3,
                'pos': 'sexy_dance, They do a sexy dance. They thrusts and sways her hips in a sexual manner while kneeling.',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'Sex Dance',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '50.53. pose.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'We are shop assistant.MP3',
            'pos': 'Kneeling, the women clasp their hands behind their backs, keeping their arms along their sides.',
        },
        'width': 896,
        'height': 1152,
        'backend': 'linux',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'The women slowly rise and stand at attention.',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'wstawanie',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '50.51. pose.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'spanking.MP3',
            'pos': 'Women look into the camera, hiding their hands behind their backs.',
        },
        'width': 624,
        'height': 800,
        'backend': 'linux',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Women slowly and sensually turns back',
                'neg': '',
            },
        ],
        "chain_prefix": 'turns back',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '50.55. pose.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Camera slowly zoom in women on foreground shakes their buttocks',
        'neg': 'static women no movement',
    },
    {
        'file': '50.57. pose.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.59. single talk.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': [
            {
                'file': 'Please take me.mp3',
                'pos': 'Kneeling, the women clasp their hands behind their backs, keeping their arms along their sides.',
            },
            {
                'file': 'I am yours.MP3',
                'pos': 'The woman extends her hands invitingly in front of her.',
            },
        ],
        'width': 624,
        'height': 800,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '50.59. single talk.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'dubit',
        'audio': [
            {
                'file': 'Please take me.MP3',
                'pos': 'A person is speaking English, saying: "Please take me!"',
                'neg': 'blurry, distorted face',
            },
            {
                'file': 'I am yours.MP3',
                'pos': 'A person is speaking English, saying: "I am yours"',
                'neg': '',
            },
            {
                'file': 'Here and now.mp3',
                'pos': 'A person is speaking English, saying: "Here and now"',
                'neg': 'blurry, distorted face',
            },
        ],
        'width': 896,
        'height': 1152,
    },
    {"break": True},

    {
        'file': 'resize.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'dubit',
        'audio': 'chodz na plaze.mp3',
        'pos': 'A woman is speaking Polish, saying: " Chodź na plażę! Nie ma co w hotelu siedzieć!"',
        'neg': 'blurry, distorted face',
        'width': 896,
        'height': 1152,
    },
    {"break": True},

    {
        'file': '50.53. pose.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'test nowego multi chain 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Women is waving hands',
                'neg': '',
                'ltx_variant': '8step',
                'frame_interpolation': False,
            },
            {
                'duration': 3,
                'pos': 'Womane is standing up',
                'neg': '',
                'frame_interpolation': True,
            },
        ],
        'width': 448,
        'height': 576,
    },

    {
        'file': '50.51. pose.png',
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
