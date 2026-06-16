# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_014_2_cat walk.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_014_2_cat walk.yaml"))
# Generated: 2026-06-09 12:00:14
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\muszelka_pliki\\EM\\skakanie_na_pilce\\film'

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
        'file': '13.49. Start scene.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '13.49. Witaj to ja.mp3',
            'pos': 'Woman is waving hand with greetings and smiles',
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '13.51. Catwalk_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '13.53. Catwalk_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '13.55. Catwalk_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '17.49. Start scene.png.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '17.49 niewinna.mp3',
            'pos': """A beautiful young woman looking at the camera with a shy, innocent expression. She speaks softly and playfully: "Patrz jaka jestem niewinna..."

While saying this, she slowly and bashfully raises both hands to cover her face in a cute, embarrassed way. She first covers her mouth and cheeks, then gently covers more of her face with her palms, peeking shyly through her fingers. Very delicate, timid and adorable movement, slight head tilt, blushing cheeks, sweet and innocent vibe.

Natural lip sync with the spoken words, soft feminine voice, slow and graceful hand movement, expressive eyes, high detail, realistic animation.""",
        },
        'width': 608,
        'height': 816,
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'NONE',
                'neg': '',
            },
        ],
        "chain_prefix": 'shy woman',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 1.5,
        'neg': """slowly and bashfully raises both hands to cover her face in a cute, embarrassed way. She first covers her mouth and cheeks, then gently covers more of her face with her palms, peeking shyly through her fingers. Very delicate, timid and adorable movement, slight head tilt, blushing cheeks, sweet and innocent vibe.

Natural lip sync with the spoken words, soft feminine voice, slow and graceful hand movement, expressive eyes, high detail, realistic animation.""",
    },

    {"break": True},

    {
        'file': '17.51. Catwalk_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '17.53. Catwalk_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '17.55. Catwalk_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '14.49. Start scene.png.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '14.49. fajna jestem.mp3',
            'pos': """A beautiful woman looking directly at the camera with a confident and provocative expression. She speaks in a playful, seductive tone: "Fajna jestem prawda..."

While saying this, she smoothly places both hands on her hips in a classic "hands on hips" pose, elbows pointing outwards. She slightly tilts her head, pushes her chest forward and gives a bold, teasing, challenging look straight into the camera. Very sassy and self-assured attitude.

Natural lip sync with the spoken words, slow and confident hand movement, seductive body language, strong eye contact, high detail, realistic animation.""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '14.51. Catwalk_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '14.53. Catwalk_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '14.55. Catwalk_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '16.49. Start scene.png.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '16.49. co powiesz na to.mp3',
            'pos': """A beautiful woman looking at the camera with a seductive and playful expression. She speaks in a teasing, inviting tone: "A co powiesz na to?"

While saying this, she smoothly and encouragingly spreads both of her arms outwards in an open, inviting gesture — palms facing up, arms slightly bent, as if saying "what do you think?" or "come here". The movement is slow, sensual and confident. She tilts her head slightly, smiles provocatively and maintains strong, flirtatious eye contact with the camera.

Natural lip sync, expressive facial expression, seductive body language, smooth and graceful arm movement, high detail, realistic animation.""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '16.51. Catwalk_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '16.53. Catwalk_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '16.55. Catwalk_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '15.49 Start scene.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': '15.49. masz sie sluchac.mp3',
            'pos': """Modelka patrzy w kamerę władczym, rozkazującym wzrokiem. Mówi stanowczo i dominująco: "A teraz masz się mnie słuchać..."

W trakcie mówienia unosi prawą rękę i wskazuje palcem prosto w kierunku kamery w zdecydowanym, rozkazującym geście. Intensywne, kontrolujące spojrzenie, lekko uniesione brwi, pewna siebie postawa. Bardzo dominująca i władcza mimika.

Naturalny lip sync, wyraźny gest wskazywania palcem, mocna prezencja, wysoka jakość animacji.""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '15.51. Catwalk_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '15.53. Catwalk_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '15.55. Catwalk_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
