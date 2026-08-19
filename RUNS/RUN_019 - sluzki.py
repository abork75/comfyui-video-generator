# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_019 - sluzki.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_019 - sluzki.yaml"))
# Generated: 2026-08-17 17:08:39
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_019 - sluzki'

FORCE_RESOLUTION = (
    560,
    560,
)
DEFAULT_RESOLUTION = (
    560,
    560,
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
        'file': '05. Start_sluzki_sie_zastanawiaja.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '06. Sluzka czerwona nie zdradzi krolowej.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '07. Sluzka zielona nie zdradzi krolowej.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '08. no mercy.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '11 w strojach nocnych.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '21. start przejażdzki.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '22. Wsiadanie na woz.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '24.01. start tranzycji do zwiazania.jpg',
        'backend': 'linux',
        'duration': 5,
        'pos': """two women sitting, hands become bound behind back, ropes appear around wrists,
cloth gag tied around mouth, women restrained and silenced, subtle struggle,
medieval setting, dramatic lighting, same position throughout""",
        'neg': """standing up, falling, camera movement, extra people, clothes changing,
background changing, smooth morph, dissolve effect, blurry transition""",
    },
    {
        'file': '24.02. koniec tranzycji do zwiazania.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '25.01.  woz_odjezdza_start.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """side view of horse-drawn cart slowly moving out of frame to the right, wooden cart boards visible in foreground,
women seated on cart moving away with it women on cart fidgeting nervously, shifting uneasily, anxious movements, cart wheels rolling, castle courtyard,
cart gradually disappearing off the edge of frame, courtyard becoming empty,
crowd or guards in background, medieval atmosphere""",
        'neg': 'side view of horse-drawn cart slowly moving out of frame to the right,',
        'width': 1040,
        'height': 1040,
    },
    {
        'file': '25.02.  woz_odjezdza_end.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '31. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '32. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '33. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '34. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '35. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '36. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '37. Jazda przez miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '41.51. wjazd na plac_start.jpg',
        'backend': 'linux',
        'duration': 3,
        'pos': """horse-drawn cart slowly entering the square from the side, wheels rolling on cobblestones,
executioner standing at the pillory shifts weight slightly, turns head to look at arriving cart,
crowd standing in silence watching, subtle movement through the crowd, heads turning,
medieval town square, tense atmosphere, overcast light""",
        'neg': """frozen figures, static people, no movement, teleportation, cart disappearing,
extra people on cart, crowd cheering, sudden motion, camera shake""",
        'width': 1040,
        'height': 1040,
    },
    {
        'file': '41.53. wjazd na plac_end.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '41.55 woz podjezdza blizej.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '42.51start.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '42.61. whipping.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '42.81. finish.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '51.51. whipped servant on cart.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """horse-drawn cart positioned sideways in foreground slowly begins to move,
wheels start turning, cart gradually pulls out of frame to the side,
women seated on cart sway and bounce gently with the motion,
crowd of people in background shifts slightly, ambient movement,
medieval town square, dust rising under wheels, slow steady departure, only coachman and two women on cart
cinematic wide shot, natural lighting""",
                'neg': """teleportation, cart disappearing, sudden jump cut, static frozen scene,
camera movement, zoom, blur extra people, additional figures, crowd on cart, more than three people on cart, spectators on cart""",
            },
            {
                'duration': 3,
                'pos': """horse-drawn cart positioned sideways in foreground slowly begins to move,
wheels start turning, cart gradually pulls out of frame to the side, only coachman and two women on cart
women seated on cart sway and bounce gently with the motion,
crowd of people in background shifts slightly, ambient movement,
medieval town square, dust rising under wheels, slow steady departure,
cinematic wide shot, natural lighting""",
                'neg': """teleportation, cart disappearing, sudden jump cut, static frozen scene,
camera movement, zoom, blur extra people, additional figures, crowd on cart, more than three people on cart, spectators on cart""",
            },
        ],
        "chain_prefix": 'wyjazd',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'width': 1040,
        'height': 1040,
    },

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
