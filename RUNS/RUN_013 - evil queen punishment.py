# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_013 - evil queen punishment.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_013 - evil queen punishment.yaml"))
# Generated: 2026-07-29 00:33:48
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\dungeon_team\\film'

FORCE_RESOLUTION = (
    512,
    512,
)
DEFAULT_RESOLUTION = (
    512,
    512,
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
        'type': 'scene_break',
        'name': 'NARADA',
    },
    {
        'file': 'Narada_1.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'scene_break',
        'name': 'NOC W LOCHU',
    },
    {
        'file': 'Wizyta_0.mp4',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Woman approaches another woman',
        'neg': 'NONE',
        'width': 1024,
        'height': 1024,
    },
    {
        'file': 'Wizyta_1.png',
        'backend': 'linux',
        'duration': 4,
        'pos': "Woman on left rises hand and touches chained woman's breast",
        'neg': 'NONE',
        'width': 1024,
        'height': 1024,
    },
    {
        'file': 'Wizyta_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'Woman on left is leaving the dungeon, screen slowly fades to black after her leaving',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'opuszcza loch',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'width': 1024,
        'height': 1024,
    },

    {"break": True},

    {
        'file': 'Crossed_3.png',
        'backend': 'linux',
        'duration': 5,
        'pos': 'cinematic 5-second video sequence, woman chained to stone wall with arms and legs spread wide in X position, heavy metal chains, dynamically and decisively struggling and yanking against restraints with forceful body movements, intense determined expression, start frame full body view, end frame extreme close-up on lower body and legs with camera zoom-in, dramatic lighting, high detail, anatomical correctness',
        'neg': 'static pose, no movement, blurry, low quality, deformed hands, extra limbs, bad anatomy, text, watermark, cartoon, overexposed, underexposed, unnatural clothing movement, jittery fabric, erratic cloth shaking',
    },
    {
        'file': 'Crossed_1.png',
        'backend': 'linux',
        'duration': 5,
        'pos': 'cinematic 5-second video sequence, woman chained to stone wall with arms and legs spread wide in X position, heavy metal chains, dynamically and decisively struggling and yanking against restraints with forceful body movements, intense determined expression, start frame close-up from mid-breasts downward showing lower torso hips and spread legs, end frame showing full breasts and face with smooth upward camera movement from lower body to upper body, dramatic lighting, high detail, anatomical correctness',
        'neg': 'fabric movement, rippling cloth, moving wrinkles, animated texture, oscillating patterns, clothing movement, texture flickering, static camera, no camera movement, frozen pose',
        'use_lightning': False,
    },
    {
        'file': 'Crossed_2.png',
        'backend': 'linux',
        'duration': 5,
        'pos': '',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'Punishment_all_night_long.mp3',
            'pos': 'A close-up of a woman speaking with intense pain on her face, mouth moving as she talks, furrowed brows, squinted eyes, tense jaw, subtle grimacing, emotional distress, realistic facial expressions and lip movements, cinematic lighting, high detail, 5-second video clip',
            'neg': 'static image, no movement, smiling, relaxed face, blurry, deformed, low quality',
        },
        'width': 768,
        'height': 768,
        'backend': 'linux',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman is bowing her head',
                'neg': '',
            },
        ],
        "chain_prefix": 'Bowing head',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': 'PODRÓŻ PRZEZ MIASTO',
    },
    {"break": True},

    {
        'file': 'prezentacja_krolowej_na_dziedzincu.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'prezentacja_krolowej_wyjazd_z_dziedzinca.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'prezentacja_krolowej_pod_katedra.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'prezentacja_krolowej_jazda_przez_miasto.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'prezentacja_krolowej_jazda_przez_miasto2.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'CHŁOSTA',
    },
    {
        'file': 'She Came at last.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'chlosta_start.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Rip apart.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'rozprucie_start_v3.png',
        'backend': 'linux',
        'duration': 3,
        'pos': "Queen's elegant green dress made of luxurious expensive fabric with intricate golden embroidery patterns, high-quality material in perfect condition at start and end frames, lower part of the dress magically tearing and ripping open to reveal buttocks and legs as sorceress on left wave her hand and magic light is visible, woman standing under pillory, magical tearing effect with bright flash, detailed fabric texture, realistic cloth dynamics",
        'neg': 'deformed, bad anatomy, blurry, low quality, extra limbs, mutated hands, poorly drawn face, text, watermark, overexposed, underexposed, torn dress at start, damaged fabric, cheap material',
        'frame_interpolation': False,
    },
    {
        'file': 'wiezy_znikaja.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Pleas have mercy.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'showed_no_mercy.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'lora_strength': None,
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p2.png',
        'backend': 'linux',
        'duration': 5,
        'pos': """Dynamic 5-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 5 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'generate_count': 3,
    },
    {"break": True},

    {
        'file': 'whip1_p3.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """Dynamic 5-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 5 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': '',
        'neg': '',
    },
    {"break": True},

    {
        'file': 'whip1_p5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 5-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 5 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p6.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p7.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p8.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p9.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p10.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p11.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p12.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p13.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p14.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p15.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p16.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p17.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p18.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p19.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p20.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': 'Woman bound to the cross is moving her butt, shaking head',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 5,
                'pos': 'The woman beneath the cross lets go of the ropes she is holding, kneeling at the cross - face to cross, and putting hands behind her back',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'Cierpienie krolowej0',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'TenStrokesNotEnough.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'PeoplesWill.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p21.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p22.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p23.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p24.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p25.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'sharp whip crack impact, loud leather whip strike, crisp snap sound, woman sharp gasp cry of pain, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p26.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p27.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p28.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p29.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'generate_count': 3,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p30.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p31.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p32.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p33.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'generate_count': 3,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p34.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p35.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'generate_count': 3,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p36.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p37.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'generate_count': 3,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p38.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'whip1_p39.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 3-second video: A sorceress on the left aggressively and repeatedly whipping a naked woman tied to a wooden pole in the center. Multiple fast, powerful whip strikes hitting her directly at legs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.

In the background: animated medieval crowd with subtle natural movement - people shifting weight, turning heads, slightly raising hands, murmuring, small movements, cheering crowd with gentle motion, not too many people.

Realistic whip motion with motion blur, dynamic action, cinematic side view, dramatic lighting, dark fantasy atmosphere, highly detailed main subjects, subtle background animation, 3 seconds video""",
        'neg': 'static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
        'frame_interpolation': False,
        'generate_count': 3,
        'audio_prompt': 'whip crack slap sound, woman yelp cry out pain, sharp impact flesh, gasp moan distress, high quality sound effects',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': 'whip1_p40.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': 'Woman bound to the cross is moving her butt, shaking head',
                'neg': '',
            },
            {
                'duration': 5,
                'pos': 'The woman beneath the cross lets go of the ropes she is holding, turns toward the camera, and grabs them again. , woman with whip throws away whip out of scene to the left side',
                'neg': '',
            },
        ],
        "chain_prefix": 'Cierpienie krolowej',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'whip1_p41FIN.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'GNIEW TŁUMU',
    },
    {
        'file': 'Gniew_tlumu_01.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Gniew_tlumu_02.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Gniew_tlumu_03.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Gniew_tlumu_04.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Gniew_tlumu_05.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Gniew_tlumu_06.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'ZDZIERANIE UBRANIA',
    },
    {
        'file': 'Nothing is yours.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '01_removing_clothes.png',
        'backend': 'linux',
        'duration': 4,
        'pos': "A powerful sorceress on the right side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's right breast with her hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
        'frame_interpolation': True,
    },
    {
        'file': '02_removing_clothes.png',
        'backend': 'linux',
        'duration': 4,
        'pos': "A powerful sorceress on the right side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's hand with her hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '02a_removing_clothes.png',
        'backend': 'linux',
        'duration': 4,
        'pos': "A powerful sorceress on the right side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's right breast with her hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '02b_removing_clothes.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """A powerful sorceress on the right side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's - bottom part of torn robes with her right empty hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k
""",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '03_removing_clothes.png',
        'backend': 'linux',
        'duration': 5,
        'pos': "A powerful sorceress on the right side of the frame, leaning forward over a queen bound to a wooden pole with arms raised and tied above her head, using her right empty hand to reach up and tear rags from the bound queen's wrists — first tearing the fabric from one wrist, then the other — actively pulling and throwing the pieces away, intense focused gaze directed exactly at the wrists, body angled toward the action, wand held in her left hand, dramatic motion, precise hand contact with fabric at the wrists, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing from wrists, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'reaching low, hands at breast level or below, reaching down, arms lowered, hands near torso or hips, static pose, standing still, frozen motion, not reaching up, hands not at wrists, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '04_removing_clothes.png',
        'backend': 'linux',
        'duration': 4.5,
        'pos': 'Static camera, same framing as start and end frames. A sorceress walks with smooth, dignified movement, passing behind a queen who is tightly bound to a wooden pole with ropes. The queen looks around anxiously with worried expression. The sorceress moves from one side of the pole to the other in a fluid, elegant motion. Detailed anatomy, realistic fabric movement, cinematic lighting, high quality',
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '05b_removing_clothes.png',
        'backend': 'linux',
        'duration': 4,
        'pos': "A powerful sorceress on the left side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's belly with her hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '06_removing_clothes.png',
        'backend': 'linux',
        'duration': 4.5,
        'pos': "A powerful sorceress on the left side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's hips with her hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {
        'file': '07_removing_clothes.png',
        'backend': 'linux',
        'duration': 4.5,
        'pos': "A powerful sorceress on the right side of the frame, leaning forward over a woman bound to a wooden pole, dynamically tearing individual pieces of clothing from the bound woman's hand with her hand, actively pulling and throwing the fabric away, intense focused gaze directed exactly at the tearing point, body angled toward the action, wand in her other hand, dramatic motion, precise hand contact with fabric, weight shifted forward, anatomically correct hands and fingers gripping cloth, highly detailed fabric tearing, dynamic pose, cinematic lighting, photorealistic, sharp details, 8k",
        'neg': 'static pose, standing still, frozen motion, no action, hands not touching fabric, not tearing clothes, blurry hands, deformed fingers, bad anatomy, extra limbs, wrong hand position, fabric intact, motionless sorceress, low quality, blurry',
    },
    {"break": True},

    {
        'file': 'ItIsSoHumilating.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'ItIsSoHumilating.MP3',
            'pos': 'Person is talking hands up in still position',
        },
        'width': 768,
        'height': 768,
        'backend': 'linux',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'NOCNE CZUWANIE',
    },
    {
        'file': 'AllNightLong.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Warriors_3.png',
        'backend': 'linux',
        'duration': 6,
        'pos': 'Night scene in a medieval town square, several fierce female warriors in armor standing guard around a naked woman tied to a wooden stake, dramatic moonlight, time-lapse effect with very fast accelerated movements, crowd of people rapidly disappearing from the square, moon moving across the sky from right side of frame to left side, dynamic motion blur, fast time passage, cinematic, highly detailed, photorealistic',
        'neg': 'slow motion, gradual movements, slow actions, static poses, slow time lapse, relaxed pacing, no slow movements',
    },
    {
        'file': 'Warriors_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Warriors_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'At dawn in a medieval town square, a naked woman is tightly bound by her wrists high above her head to a tall wooden pole in the center. Two fierce female warriors stand on either side of her, dynamically swinging whips to flog her already marked body. The bound woman thrashes violently and screams in pain, her body twisting helplessly while her arms remain firmly secured. A large crowd of onlookers surrounds the scene watching the public spectacle. Dramatic early morning light, misty atmosphere, realistic anatomy, dynamic motion, detailed skin textures, cinematic composition',
                'neg': 'blurry, deformed hands, extra limbs, poor anatomy, text, watermark, cartoon, low quality',
            },
            {
                'duration': 5,
                'pos': 'At dawn in a medieval town square, a naked woman is tightly bound by her wrists high above her head to a tall wooden pole in the center. Two fierce female warriors stand on either side of her, dynamically swinging whips to flog her already marked body. The bound woman thrashes violently and screams in pain, her body twisting helplessly while her arms remain firmly secured. A large crowd of onlookers surrounds the scene watching the public spectacle. Dramatic early morning light, misty atmosphere, realistic anatomy, dynamic motion, detailed skin textures, cinematic composition',
                'neg': 'blurry, deformed hands, extra limbs, poor anatomy, text, watermark, cartoon, low quality',
            },
        ],
        "chain_prefix": 'poranna chłosta',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'Warriors_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Warrior_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Naked woman exhausted is falling on the ground',
        'neg': 'NONE',
    },
    {
        'file': 'Warrior_6.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'koniec_kary.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'Warrior_7.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """Two female warriors stand beside a naked, extremely exhausted queen, firmly grabbing her arms and dragging her out of the frame, her body slumping limply with exhaustion, head hanging forward, feet barely touching the ground, dragged motion, cinematic movement, highly detailed anatomy, realistic skin texture, dynamic action
""",
                'neg': """clothed, clothing, dress, text, watermark, deformed, bad anatomy, extra limbs, blurry, low quality, cartoon, anime, overexposed, underexposed, motion blur, artifacts"
""",
            },
            {
                'duration': 1,
                'pos': 'Women moving forward leaving the scene',
                'neg': 'anybody on scene',
            },
        ],
        "chain_prefix": 'Wyprowadzenie złej królowej',
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
