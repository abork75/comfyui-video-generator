# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_012 - dmuchinj w oponke.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_012 - dmuchinj w oponke.yaml"))
# Generated: 2026-06-04 07:24:36
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
        'duration': 5,
        'pos': """Cinematic 5-second I2V2I video with magical effect:

Start frame (Image 1): Empty room with a large poster of a beautiful woman/model hanging on the wall.

During the 5 seconds a magical transformation happens: The woman on the poster begins to glow with bright, ethereal light. Suddenly there is a strong flash of light, sparkling particles and magical energy burst from the poster. The woman magically materializes and steps out of the poster into reality.

She appears on the floor in the room below the poster in a natural, slightly surprised pose. The transition is smooth and spectacular — glowing particles, light trails, and bright flash emphasize the magical transfer from 2D poster to real 3D person.
End frame (Image 2): The same empty room, but now the real woman is sitting/lying on the floor beneath the now empty poster.

Magical, fantastical atmosphere, dramatic lighting, sparkling particles, beautiful cinematic effect, photorealistic, highly detailed, 4K.""",
        'neg': 'deformed body, bad anatomy, extra limbs, missing limbs, mutated hands, blurry motion, low quality, artifacts, watermark, text, logo, poster tearing, broken poster, woman walking out of poster, smooth morphing, slow transition, no magical effect, no glow, no particles, no flash, dull lighting, realistic transfer without magic, static scene, no materialization, bad composition, distorted proportions, cartoonish, plastic skin, low detail, overexposed flash, underexposed, jerky movement, floating body, wrong pose, different clothing, face deformation, extra people, empty room without woman',
    },
    {
        'file': '10.53. on scene.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '10.55 Dmuchne w oponke.mp3',
            'pos': 'Woman is waving a hand',
        },
        'width': 608,
        'height': 832,
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman is standing up, turning back to camera and leaves garrage',
                'neg': '',
            },
        ],
        "chain_prefix": 'wychodzi na zewnątrz',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '11.51. maszyny_wywazarka.jpeg',
        'backend': 'linux',
        'duration': 5,
        'pos': """5-second magical I2V2I: In an empty room, a large poster of a woman hangs on the wall (Image 1). Suddenly the poster starts glowing intensely. A bright flash of light and swirling magical particles erupt from the poster. The woman dramatically materializes out of the poster, emerging into the real world and landing gracefully on the floor.

Strong emphasis on magical transfer, glowing effects, sparkles, and light burst. End frame shows the real woman on the floor and the now blank poster (Image 2). Cinematic, enchanting, photorealistic, ultra detailed.""",
        'neg': 'deformed body, bad anatomy, extra limbs, missing limbs, mutated hands, blurry motion, low quality, artifacts, watermark, text, logo, poster tearing, broken poster, woman walking out of poster, smooth morphing, slow transition, no magical effect, no glow, no particles, no flash, dull lighting, realistic transfer without magic, static scene, no materialization, bad composition, distorted proportions, cartoonish, plastic skin, low detail, overexposed flash, underexposed, jerky movement, floating body, wrong pose, different clothing, face deformation, extra people, empty room without woman',
    },
    {
        'file': '11.53. on scene.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '11.55. przykrecac kolka.mp3',
            'pos': 'Woman is rising both hands and waving them',
        },
        'width': 608,
        'height': 832,
    },

    {"break": True},

    {
        'file': '11.55 gdzie ten lewarek.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'Woman is chaotically looking for something on table',
                'neg': '',
            },
        ],
        "chain_prefix": 'gdzie lewarek',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': '',
    },

    {
        'type': 'talk',
        'audio': {
            'file': '11.57. Gdzie ten lewarek.mp3',
            'pos': 'Woman is chaotically looking for something on table',
        },
        'width': 608,
        'height': 832,
    },

    {"break": True},

    {
        'file': '13.51. taniec.png',
        'backend': 'linux',
        'duration': 5,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': """5-second cinematic video: A woman sitting on a sofa with another woman standing and leaning over her seductively. The seated woman slowly rises to her feet, moving very close to the standing woman. They immediately begin dancing together in a slow, extremely sensual and passionate style — hips moving, bodies sliding against each other, soft caresses, intense eye contact and elegant, erotic dance moves.

Smooth transitions, seductive atmosphere, cinematic lighting, photorealistic, high detail.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain_1',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '13.71. taniec.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Two women dancing seductively. They turn to face each other, slowly and gracefully embrace — arms wrapped around each other, bodies close together. They continue dancing as a couple: slow, intimate movements, hips swaying in unison, gentle caresses, foreheads almost touching, intense eye contact. Passionate, erotic and elegant partner dance. Smooth cinematic motion, soft dramatic lighting, photorealistic.',
        'neg': 'NONE',
    },
    {
        'file': '13.75. taniec.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 5-second I2V video: Two beautiful women dancing sensually together. They slowly move closer to each other while dancing, bodies swaying in rhythm. They gently embrace, lean in and give each other a soft, passionate kiss on the lips. After the kiss they pull back slightly, smiling, and continue dancing closely together in a very intimate and seductive way — hips moving, gentle touching, deep eye contact.

Smooth, fluid and erotic choreography, slow-motion elements during the kiss, sensual atmosphere, soft cinematic lighting, graceful movements, photorealistic, highly detailed, 4K.""",
        'neg': 'NONE',
    },
    {
        'file': '13.77. taniec.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Zoom on woman in black black lace bodysuit with blonde hair other woman is not visible',
                'neg': '',
            },
        ],
        "chain_prefix": 'zoom on blonde',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'talk',
        'audio': {
            'file': '13.79. ktos przyjechal.mp3',
            'pos': 'Face is little frighetned and courious',
        },
        'width': 608,
        'height': 832,
    },

    {"break": True},

    {
        'file': '15.51. powitanie.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Women are smiling and waving her right hands in greetings',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '15.51. Lauren_witamy.mp3',
            'pos': 'Women is waving hand with greetings',
        },
        'width': 608,
        'height': 832,
    },

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
