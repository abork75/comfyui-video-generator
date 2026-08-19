# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_003 - walentynki.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_003 - walentynki.yaml"))
# Generated: 2026-08-17 20:11:32
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_003 - walentynki'

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
        'file': '03.05 przed USC.jpeg',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple standing in front of a building, evening light. They make eye contact, then move into a close, affectionate hug. Warm, romantic mood, slow motion, close-up on embrace, cinematic, 5 sec.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.08 przed USC.jpg',
        'backend': 'local',
        'duration': 5,
        'pos': "Couple hugging closely. They pull back slightly, gaze into each other's eyes, then start a slow, intense, passionate kiss. Close-up on faces, warm romantic lighting, cinematic, 5 sec.",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.10 przed USC.jpg',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple ends deep kiss, smiles softly, holds hands, turns and walks straight toward camera. Warm romantic lighting, slow walk, cinematic, close-up to medium shot, 5 sec.',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.14 przed USC.mp4',
        'backend': 'local',
        'duration': 5,
        'pos': 'PROMPT',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '05.05 taniec.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': "Couple is dancing do not show woman's face",
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.07 taniec.mp4',
        'backend': 'local',
        'duration': 5,
        'pos': 'PROMPT',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '07.05 sypialnia.jpg',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple sitting together on bed in normal clothes. Pink hearts appear and float, quick white flash. Same pose — now they’re in underwear only. Magical romantic vibe, seamless transition, close-up, 5 sec.',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '07.07 sypialnia.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple sitting on bed edge. They turn to face each other, intense eye contact, then start a slow, deep, passionate kiss. Sensual close-up on faces, warm light, cinematic, 5 sec.',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '07.09 sypialnia.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple sitting on bed edge. They stand, face each other, sit deeper on bed pulling into a deep, passionate hug. Sensual, close embrace, warm light, cinematic close-up, 5 sec.',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '07.11 sypialnia.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple sitting on bed. They lie back deeper together, passionately touching and caressing each other. Sensual close embrace, warm light, intimate mood, cinematic close-up, 5 sec.',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '07.13 sypialnia.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Couple lying on bed. They turn to each other, embrace tightly, caress gently, then start a slow passionate kiss. Sensual close-up, warm light, intimate mood, cinematic, 5 sec.',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': 'Woman and man lying on back next to each other on bed. She slowly gets on top of him, lies fully on his body, intense eye contact, then deep passionate kissing. Intimate, sensual, close-up on faces, cinematic, warm evening light, 5 sec.',
            },
            {
                'duration': 5,
                'pos': 'Woman and man lying on back next to each other on bed. She slowly gets on top of him, lies fully on his body, intense eye contact, then deep passionate kissing. Intimate, sensual, close-up on faces, cinematic, warm evening light, 5 sec.',
            },
        ],
        "chain_prefix": 'girl_leaves',
        'backend': 'local',
        'fps': 16,
        'steps': 20,
        'cfg': 5.0,
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
    },

]

FLOW_TEST = [
    {
        'file': '03.05 przed USC.jpeg',
        'backend': 'local',
        'duration': 2,
        'pos': 'PROMPT',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.08 przed USC.jpeg',
        'backend': 'local',
        'duration': 2,
        'pos': 'PROMPT',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.10 przed USC.jpeg',
        'backend': 'local',
        'duration': 4,
        'pos': 'PROMPT',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
]

FLOW = FLOW_TEST if USE_TEST_FLOW else FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
