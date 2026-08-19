# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_001 - Ewelina_strips_in_office.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_001 - Ewelina_strips_in_office.yaml"))
# Generated: 2026-08-17 20:59:24
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_001 - Ewelina_strips_in_office'

FORCE_RESOLUTION = (
    512,
    672,
)
DEFAULT_RESOLUTION = (
    512,
    672,
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
        'file': '00.03. Ewelina spokojnie stoi w marynarce.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'woman standing naturally, subtle breathing, soft lighting',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '00.05. Ewelina zdejmuje marynarke.mp4',
        'backend': 'local',
        'duration': 2,
        'pos': 'woman standing naturally, subtle breathing, soft lighting',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '00.08. Ewelina wyjmuje koszule z marynarki.mp4',
        'backend': 'local',
        'duration': 4,
        'pos': 'elegant woman standing confidently, soft ambient lighting, subtle natural movements',
        'neg': 'blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '01.03_ewelina_stands_in_skirt.jpg',
        'pos': 'shy woman slowly reaches for blouse buttons, hesitant fingers begin unbuttoning from top, gentle nervous movements, gradually opening blouse button by button, natural breathing motion, soft uncertain expression, warm lighting',
        'neg': 'fast motion, rushed, aggressive movement, ripping clothes, sudden actions, blurry, distorted',
        'duration': 8,
    },
    {
        'file': '01.04_ewelina_stands_in_unbuttoned_skirt.png',
        'pos': 'woman gently grabs open blouse edges, slowly slides fabric off shoulders, arms gradually pulling out of sleeves one by one, blouse falling softly, smooth continuous motion, shy facial expression, natural movement flow',
        'neg': 'jerky motion, sudden pull, throwing clothes, fast undressing, abrupt movements, teleporting, blurry',
        'duration': 5,
    },
    {
        'file': '01.06. Ewelina stands in skirt and bra.png',
        'pos': 'standing woman slowly bends knees, hips gradually lowering toward chair, arms reaching back for support, body smoothly descending into sitting position, shy blushing expression, gentle controlled motion, natural sitting transition',
        'neg': 'falling, dropping down, sudden sit, jerky movement, losing balance, abrupt motion, distorted',
        'duration': 2,
    },
    {
        'file': '01.08._ewelina_sit_in_skirt_bra.jpg',
        'pos': 'seated woman places hands on armrests, slowly pushes body upward, legs gradually straightening, hips rising from chair, smooth controlled ascent, reluctant hesitant movement, natural standing transition, uncertain expression',
        'neg': 'jumping up, fast motion, sudden stand, jerky ascent, losing balance, abrupt movement, blurry',
        'duration': 4,
    },
    {
        'file': '01.10. Ewelina stands in skirt and bra.png',
        'pos': 'simple transition',
        'neg': 'frozen statue, completely static, no movement, sudden actions, blurry, low quality moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
        'duration': 3,
    },
    {
        'file': '01.20. Ewelina undress skirt.mp4',
        'backend': 'local',
    },
    {"break": True},

    {
        'file': '02_ewelina_braOFF.mp4',
        'backend': 'local',
    },
    {"break": True},

    {
        'file': '03._ewelina_panties_off.mp4',
        'backend': 'local',
        'duration': 4,
        'pos': 'motion gradually slows down, movement smoothly decelerating, freeze into photograph, cinematic slow-motion stop, graceful halt, natural deceleration into stillness',
        'neg': 'sudden stop, abrupt freeze, jerky motion, choppy slowdown, stuttering, unnatural halt',
    },
    {
        'file': '04_ewelina_out.png',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'woman starts walking down the corridor, hesitant first steps, foot lifting and placing carefully, moving away from camera, body gradually getting smaller in frame, uncertain slow pace',
            },
            {
                'duration': 2,
                'pos': 'woman continues walking deeper into corridor, steady hesitant steps, arms swaying gently, body receding further, getting noticeably smaller in distant view, maintained slow uncertain pace',
            },
            {
                'duration': 2,
                'pos': 'woman walks further down corridor toward far end, very small figure in distance, continued hesitant walking motion, diminishing into corridor depth, distant perspective',
            },
        ],
        "chain_prefix": 'ewelina_walks',
        'backend': 'local',
        'fps': 16,
        'steps': 20,
        'cfg': 5.0,
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
    },

]

FLOW_TEST = [
    {
        'file': '01.03_ewelina_stands_in_skirt.jpg',
        'pos': 'shy woman slowly reaches for blouse buttons, hesitant fingers begin unbuttoning from top, gentle nervous movements, gradually opening blouse button by button, natural breathing motion, soft uncertain expression, warm lighting',
        'neg': 'fast motion, rushed, aggressive movement, ripping clothes, sudden actions, blurry, distorted',
        'duration': 8,
    },
    {
        'file': '01.04_ewelina_stands_in_unbuttoned_skirt.png',
        'pos': 'woman gently grabs open blouse edges, slowly slides fabric off shoulders, arms gradually pulling out of sleeves one by one, blouse falling softly, smooth continuous motion, shy facial expression, natural movement flow',
        'neg': 'jerky motion, sudden pull, throwing clothes, fast undressing, abrupt movements, teleporting, blurry',
        'duration': 5,
    },
]

FLOW = FLOW_TEST if USE_TEST_FLOW else FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
