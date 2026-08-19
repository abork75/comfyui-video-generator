# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_007 - MKK_taniec.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_007 - MKK_taniec.yaml"))
# Generated: 2026-08-17 19:06:47
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_007 - taniec'

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
        'file': '01.05. Sala_glowna01.png',
        'backend': 'local',
        'duration': 4,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '01.06. Sala_glowna01.png',
        'backend': 'local',
        'duration': 4,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '01.07. Sala_glowna01.png',
        'backend': 'local',
        'duration': 4,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '02.01_kotki_pieski.mp4',
        'backend': 'local',
        'duration': 1,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.02_kotki_pieski.mp4',
        'backend': 'local',
        'duration': 1,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.03_kotki_pieski.mp4',
        'backend': 'local',
        'duration': 0,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '02.15 taniec.png',
        'backend': 'local',
        'duration': 5,
        'pos': """Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.""",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.16 taniec.png',
        'backend': 'local',
        'duration': 5,
        'pos': """Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged.""",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.17 taniec.png',
        'backend': 'local',
        'duration': 5,
        'pos': """Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

Action sequence (5 seconds total, fluid and provocative movements):

0-1 second (Introduction):
- She stands center-frame facing camera at medium shot, hips swaying seductively side-to-side.
- Slowly tosses her long hair back dramatically with both hands, arching her back slightly, lips parted in invitation.

1-3 seconds (Build-up):
- Raises both arms gracefully, interlacing fingers behind her head, elbows out - thrusting her chest forward prominently.
- Body undulates in slow waves: shoulders roll, torso twists erotically, hips circle teasingly while maintaining arched posture.

3-4 seconds (Intensification):
- Hands glide down sensually from behind head, tracing neck, over shoulders, down sides of body.
- Fingers trail provocatively over breasts, then lower to caress inner thighs and intimate areas through sheer fabric - lingering touches with slight hip thrusts.

4-5 seconds (Climax):
- Both hands cup and squeeze her full breasts firmly from below, lifting and presenting them to camera.
- Ends with a sultry gaze directly into lens, biting lower lip, body frozen in this pose as subtle hip sway fades out.""",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.18 taniec.png',
        'backend': 'local',
        'duration': 10,
        'pos': """A sensual female dancer performs an intimate, slow-motion erotic dance in a luxurious dimly lit bedroom, 10-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 3-6s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 6-10s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold""",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.19 taniec.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '03.05. applause.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Men is clapping hands',
        'cfg': 5.0,
        'steps': 30,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, wind, ripples, dynamic scene, any movement, third leg',
    },
    {
        'file': '03.07. applause.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '05.05_podobalosie.mp4',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman is waving hand and leaving the scene',
            },
        ],
        "chain_prefix": 'koniec',
        'backend': 'local',
        'fps': 16,
        'steps': 20,
        'cfg': 5.0,
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
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
