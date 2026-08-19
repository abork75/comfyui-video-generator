# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_014 - skakanie_na _pilce.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_014 - skakanie_na _pilce.yaml"))
# Generated: 2026-08-17 17:35:22
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_014 - EM cat walk pilka'

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
        'file': '10.51. siedzi.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'Coby tu zrobic_Ewa Maj.mp3',
            'pos': 'Woman is scratching her head with hand looks at camera',
        },
        'width': 608,
        'height': 816,
        'transition': {
            'pos': 'Woman is slowly standing up an moving towards camera',
        },
    },

    {
        'file': '10.53. wstala.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'Kupilam_nowa_pilka_Ewa Maj.mp3',
            'pos': 'Woman is smiling seductively ',
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '11.51. stoi.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'najpierw troche gimnastyki_Ewa Maj.mp3',
            'pos': 'Woman is looking at camera',
        },
        'width': 608,
        'height': 816,
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """4-second video: Woman standing frontally to the camera performs two full torso bends. She bends forward at the hips with straight legs, lowering her torso and arms down towards the floor, then rises back up to standing position. She does this movement clearly and rhythmically two times (down-up, down-up).

Smooth but visible motion, natural body mechanics, slight hair movement, realistic muscle engagement. Front view, full body visible, photorealistic, cinematic, high detail.""",
                'neg': 'static pose, no bending, only one repetition, three or more bends, wrong movement count, minimal movement, lazy bending, bent legs, bad posture, deformed spine, unnatural flexibility, motion artifacts, blurry motion, low quality, deformed hands, extra fingers, face deformation, looking at side, turning head, side view, back view, twisting body, squatting instead of bending, overly smooth animation, rubbery limbs, floating feet, changed clothing, different lighting',
            },
            {
                'duration': 5,
                'pos': """Cinematic video of a beautiful woman sensually sitting down on a large exercise ball. She approaches the ball slowly, then lowers her body in a very seductive and controlled way — hips swaying gently, back slightly arched, chest forward. She places her hands on the ball for balance and slowly sits on it, letting her hips sink into the ball.

Movement is elegant, smooth and highly sensual, with emphasis on her curves, slow hip motion and graceful posture. Soft, seductive eye contact with the camera. Dramatic cinematic lighting, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, sudden sitting, fast movement, jerky motion, bad anatomy, deformed body, extra limbs, distorted proportions, bent awkwardly, falling, unbalanced pose, stiff posture, no hip movement, flat back, hunched shoulders, looking away from camera, ugly face, deformed hands, blurry, low quality, artifacts, rubbery motion, unnatural physics, ball deformation, ball moving too much, floating, bad lighting, overexposed, underexposed, cartoonish, plastic skin, low detail, different clothing, modest pose, unsexy movement, boring pose, legs closed, knees together',
            },
        ],
        "chain_prefix": 'gimnasytka',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '11.53. siedzi na pilce.png',
        'backend': 'linux',
        'duration': 5,
        'pos': '',
        'neg': '',
    },
    {
        'type': 'talk',
        'audio': 'Teraz_skakac_Ewa Maj.mp3',
        'width': 608,
        'height': 816,
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 4-second I2V video: A beautiful woman sitting on a large exercise ball performs a dynamic, rhythmic bouncing exercise. She pushes her hips upward forcefully, lifting her body off the ball with each bounce, creating visible separation between her body and the ball. The ball compresses and rebounds naturally on the floor with each bounce.

She does several clear, energetic up-and-down bounces. Her body moves naturally with the rhythm — breasts and hair bouncing freely. Hands resting on the sides of the ball or thighs for balance. Realistic physics: the ball bounces independently, compresses on impact, and the woman lifts and lands with slight separation.

Front view, visible realistic bouncing motion, natural ball deformation and rebound, sensual and athletic movement, photorealistic, highly detailed, cinematic lighting, 4K.""",
                'neg': 'glued to ball, stuck to ball, ball attached to body, woman and ball moving as one rigid object, no separation between woman and ball, floating together, unnatural ball physics, ball not compressing, ball not rebounding, ball deformed unnaturally, static ball, minimal bouncing, bad physics, rubbery motion, jerky movement, stiff body, bad anatomy, deformed ball, exaggerated floating, woman not lifting off ball, ball stuck to buttocks, low quality motion, artifacts, blurry',
            },
            {
                'duration': 3,
                'pos': """Cinematic 4-second I2V video: A beautiful woman sitting on a large exercise ball performs a dynamic, rhythmic bouncing exercise. She pushes her hips upward forcefully, lifting her body off the ball with each bounce, creating visible separation between her body and the ball. The ball compresses and rebounds naturally on the floor with each bounce.

She does several clear, energetic up-and-down bounces. Her body moves naturally with the rhythm — breasts and hair bouncing freely. Hands resting on the sides of the ball or thighs for balance. Realistic physics: the ball bounces independently, compresses on impact, and the woman lifts and lands with slight separation.

Front view, visible realistic bouncing motion, natural ball deformation and rebound, sensual and athletic movement, photorealistic, highly detailed, cinematic lighting, 4K.""",
                'neg': 'glued to ball, stuck to ball, ball attached to body, woman and ball moving as one rigid object, no separation between woman and ball, floating together, unnatural ball physics, ball not compressing, ball not rebounding, ball deformed unnaturally, static ball, minimal bouncing, bad physics, rubbery motion, jerky movement, stiff body, bad anatomy, deformed ball, exaggerated floating, woman not lifting off ball, ball stuck to buttocks, low quality motion, artifacts, blurry',
            },
        ],
        "chain_prefix": 'Skacze na pilce',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '11.55. siedzi na pilce 2.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Smooth transition woman is moving with ball',
        'neg': 'NONE',
    },
    {
        'file': '12.51. siedzi na pilce 2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'Woman is standing up and going towards corridor',
                'neg': '',
            },
        ],
        "chain_prefix": 'idzie do przedpokoju',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '12.53. przedpokoj.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': 'Ide_na_gorke_Ewa Maj.mp3',
        'width': 608,
        'height': 816,
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman is turning towards staris an climbing upstairs',
                'neg': '',
            },
            {
                'duration': 3,
                'pos': 'Woman dissapearing from scen climbing upstairs, empty scene seen at last 2 seconds',
                'neg': '',
            },
        ],
        "chain_prefix": 'idzie na gorke',
        'backend': 'linux',
        'fps': 16,
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
