# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_014_3_cat walk.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_014_3_cat walk.yaml"))
# Generated: 2026-08-17 17:35:01
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
        'file': '21.49. Stroje_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'cloth1_casual.mp3',
            'pos': 'Woman is waving hand with greetings and smiles',
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '21.51. Stroje_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '21.53. Stroje_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '21.55. Stroje_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '22.49. Stroje_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'cloth2_smart_casual.mp3',
            'pos': """The woman smoothly and naturally crosses her arms in front of her chest. She slowly raises her arms and places one arm over the other in a confident, relaxed pose. The movement is graceful, deliberate and feminine.

She keeps her body mostly still, only her arms are moving. She maintains eye contact with the camera and has a calm, slightly seductive expression.

Natural, smooth arm movement, realistic physics, elegant motion, photorealistic, high detail, cinematic lighting.
""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '22.51. Stroje_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '22.53. Stroje_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '22.55. Stroje_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '23.49. Stroje_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'cloth3_little_black_dress.mp3',
            'pos': """Cinematic video of a beautiful woman in a sexy little black dress. She stands elegantly, then slowly shifts into a seductive pose while speaking.

She says playfully and teasingly: "No i klasyka! Mała czarna sukienka, która zawsze działa. Co myślicie?"

While speaking, she gently places one hand on her hip, slightly tilts her body, pushes her chest forward and looks directly at the camera with a flirtatious, confident smile. She makes a slow, graceful turn of her hips and lightly runs her other hand down her side, showing off the dress.

Very feminine, elegant and seductive body language, slow seductive movements, strong eye contact, natural lip sync, photorealistic, high detail, cinematic lighting.""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '23.51. Stroje_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '23.53. Stroje_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '23.55. Stroje_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '24.49. Stroje_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'cloth4_Elegant Evening Gown.mp3',
            'pos': """A beautiful woman looking at the camera with a seductive and playful expression. She speaks in a teasing, inviting tone: "A co powiesz na to?"

While saying this, she smoothly and encouragingly spreads both of her arms outwards in an open, inviting gesture — palms facing up, arms slightly bent, as if saying "what do you think?" or "come here". The movement is slow, sensual and confident. She tilts her head slightly, smiles provocatively and maintains strong, flirtatious eye contact with the camera.

Natural lip sync, expressive facial expression, seductive body language, smooth and graceful arm movement, high detail, realistic animation.""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '24.51. Stroje_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '24.53. Stroje_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '24.55. Stroje_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '25.49. Stroje_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'cloth5_Glamorous Red Carpet.mp3',
            'pos': """Cinematic video of a stunning woman in a luxurious, deep red glamorous evening gown with plunging neckline and high leg slit. She stands elegantly and speaks with a sophisticated, confident tone:

„A na koniec coś naprawdę efektownego — głęboka czerwona suknia z rozcięciem. Idealna na wielką galę!”

While speaking, she moves gracefully and regally: slowly runs one hand down her hip and along the slit of the dress, gently shifts her weight to emphasize the leg slit, slightly turns her body to show the dress from different angles, and holds her head high with a proud, alluring smile. She maintains strong, captivating eye contact with the camera.

Very elegant, luxurious and seductive movements, slow and graceful body language, cinematic lighting, photorealistic, ultra detailed.""",
        },
        'width': 608,
        'height': 816,
    },

    {"break": True},

    {
        'file': '25.51. Stroje_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '25.53. Stroje_5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I video: A beautiful model walks confidently and seductively straight toward the camera in a sensual catwalk style.

She moves with strong, exaggerated hip sway, one leg crossing slightly in front of the other, elegant and powerful strides. Her body is dynamic and erotic — pronounced hip movement, arched back, chest forward, shoulders back, head held high. Arms swing naturally but stylishly by her sides.

The walk is very feminine, teasing and provocative. She maintains intense, seductive eye contact with the camera the entire time. Smooth, fluid and confident motion from start to end frame.

Photorealistic, highly detailed, cinematic lighting, sensual atmosphere, elegant catwalk gait, 4K.""",
        'neg': 'static pose, standing still, no hip sway, stiff walk, straight legs, legs too close together, minimal movement, awkward gait, hunched shoulders, looking away from camera, shy expression, bad walking animation, jerky motion, rubbery movement, unnatural stride, flat feet, pigeon toes, deformed legs, extra limbs, bad anatomy, low energy, boring walk, modest pose, no sensuality, stiff arms, arms glued to body, changed clothing, different hair, altered lighting, blurry motion, low quality, artifacts, cartoonish, plastic skin, side view, turning away, slow motion, floating feet',
    },
    {
        'file': '25.55. Stroje_5.png',
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
