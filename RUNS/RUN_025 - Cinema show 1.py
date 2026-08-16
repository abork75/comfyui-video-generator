# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_RUN025 - Cinema show 1.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_RUN025 - Cinema show 1.yaml"))
# Generated: 2026-08-11 22:15:51
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1'

FORCE_RESOLUTION = (
    736,
    944,
)
DEFAULT_RESOLUTION = (
    736,
    944,
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
        'type': 'scene_break',
        'name': 'START',
    },
    {
        'file': '10.51 start.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '10.61. Undress start.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'The three women slowly begin undressing. The red-haired woman starts pulling her dress up and over her head. She has panties underneath. The blonde woman unbuttons and starts unzipping her jeans. The black-haired woman begins lifting her top up. They only start the process of undressing, clothing is not fully removed yet. Natural slow movements, 4 seconds.',
                'neg': 'fully naked, clothes completely removed, fast movement, sudden undressing, standing still, no action, deformed hands, bad anatomy, blurry, low quality',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'The three women slowly begin undressing. The red-haired woman remove her dress over her head. She has panties underneath. The blonde woman pulling down her jeans. The black-haired woman begins lifting her top up. Natural slow movements, 4 seconds.',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'undress start',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': 'EROTIC DANCE',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.51 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 448,
        'height': 672,
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged.""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': """Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged.""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 5,
                'pos': """Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic
Woman has bare buttocks, has no panties at all she is naked from belly to bottom

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
- Ends with a sultry gaze directly into lens, biting lower lip, body frozen in this pose as subtle hip sway fades out.

Camera work:
- Starts with smooth tracking shot circling from front at eye level.
- Transitions to slight low-angle tilt-up emphasizing curves and movements.
- Static hold in final second for intimate close-up on face and bust.
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background.""",
                'neg': 'Panties, hidden vagina',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1_EROTIC_DANCE',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '40.53 start dancing.png',
        'backend': 'linux',
        'duration': 5,
        'pos': '5-second video. A woman stands with her back to the camera, facing the audience deeper in the frame. From 0 to 3 seconds she pulls her shirt up and over her head, removing it completely while still facing the audience. Underneath she is completely naked. Between 3 and 4 seconds she throws the shirt outside the scene. From 4 to 5 seconds she remains standing with her back to the camera. Natural fluid motion of removing and throwing the shirt.',
        'neg': 'facing the camera while removing shirt, shirt not removed, shirt stays in hand, slow motion, static, deformed hands, bad anatomy, extra limbs, blurry, low quality, incomplete action, spinning too fast',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '40.55 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'A woman stands with her back to the camera in a straight posture. In 2 seconds she turns toward the camera with a smooth dance-like motion, keeping both hands behind her head the entire time. She ends facing the camera with hands still behind her head. Natural fluid body movement.',
        'neg': 'hands moving away from head, fast spin, abrupt turn, static, no movement, deformed arms, bad anatomy, blurry, low quality',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 448,
        'height': 672,
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """A sensual female dancer performs an intimate, slow-motion erotic dancem, 4-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 1-2s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 3-4s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': """A provocative erotic dancer finishes her routine and sits down on the floor with her back to the camera. 5-second cinematic video with strictly static camera.

Action sequence:
• 0-2s: Stands center-frame facing the camera at a slight angle, exhales from the performance, arms dropping naturally.
• 2-5s: Slowly and gracefully sits down on the floor over 3 seconds, turning her back to the camera as she lowers herself. At the end she is sitting still on the floor with her back fully facing the camera.

Camera: Strictly static locked-off camera, fixed medium-wide angle, eye-level, no panning, tilting, zooming or tracking.
Cinematic hyper-realistic 8K, photorealistic skin and fabric details, natural fluid motion.""",
                'neg': 'walking out of frame, exiting the scene, standing up, facing the camera at the end, fast movement, camera movement, panning, zooming, deformed limbs, blurry, low quality',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2_EROTIC_DANCE',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '50.51 start.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'scene_break',
        'name': 'SHOW BIG SCREEN',
    },
    {
        'file': '50.51 start.png',
        'backend': 'linux',
        'duration': 4,
        'pos': 'The woman sitting on the floor with her back to the camera slowly and naturally turns her body to face the camera over 4 seconds. She uses her hands and legs to help the movement: she places one hand on the floor for support, shifts her weight, pivots on her hips, and moves her legs to rotate her body around. The turn is gradual and realistic, not spinning. At the end she sits fully facing the camera.',
        'neg': 'spinning like on a chair, rotating in place without using hands or legs, unnatural rotation, sliding turn, fast spin, floating movement, deformed limbs, blurry, low quality',
        'use_lightning': True,
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '50.61 turned back.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Zoom on woman's face",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'Zoom on face',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '51.51. Waiting.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'On the large cinema screen a film frame suddenly appears and is projected. The movie image lights up and becomes clearly visible on the screen within 2 seconds. Smooth, realistic projection effect, the screen transitions from empty/dark to showing a clear film frame.',
        'neg': 'static screen, no image on screen, black screen, blurry projection, slow fade, artifacts, distorted image',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '51.55. Waiting.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'A woman slowly enters the scene from the left side of the frame and walks a few steps into the shot. After entering she stops and stands completely still for the remaining time. Smooth, natural walking motion lasting about 3 seconds, realistic body movement, then full stillness.',
        'neg': 'fast movement, running, sudden appearance, continuous walking, no stopping, blurry, deformed limbs, extra legs, low quality, jittery motion',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '51.61. Waiting.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'A woman slowly enters the scene from the right side of the frame and walks a few steps into the shot. After entering she stops and stands completely still for the remaining time. Smooth, natural walking motion lasting about 3 seconds, realistic body movement, then full stillness.',
        'neg': 'fast movement, running, sudden appearance, continuous walking, no stopping, blurry, deformed limbs, extra legs, low quality, jittery motion',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '51.71. Waiting.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'The women in the background slowly kneel down on the floor and bow their heads downward. Smooth, natural kneeling motion followed by lowering their heads, lasting about 3 seconds. Realistic body movement and final still pose with heads bowed.',
                'neg': 'standing, no kneeling, head remaining upright, fast movement, sudden drop, blurry, deformed limbs, extra legs, low quality, jittery motion',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'modelki klekają',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': 'MST V1',
    },
    {
        'file': '61.51 start MST.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'A woman seductively transitions from a kneeling to a sitting position, supporting herself with one hand while holding the other between her legs—looking into the camera.',
        'neg': 'Unnatural movement, hovering, and spinning without the use of hands or legs; static scene, no movement.',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\61.53 start MST.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': """Technical specifications:
cinematic depth of field with subtle rack focus, high dynamic range lighting, realistic skin subsurface scattering, gentle motion blur on slow movements.

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': """- Hands glide slowly upward from thighs to caress full breasts – fingers trace underboob, circle nipples gently pinching.
- Slides down to flat stomach, palms pressing sensually in circles, hips shift forward slightly.
- With a sultry wink, grips inner thighs and spreads legs languidly wide – knees part outward to 90 degrees, feet flat on sheets exposing intimate area teasingly.

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'MST 1_kopia_MST_V1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '50.61 turned back.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """- One hand lingers on breast, kneading softly while maintaining eye contact and soft humming moan.
- Other hand trails down abdomen, fingers hovering teasingly over mound before parting labia delicately with index and middle finger.
- Hips tilt upward invitingly, legs hold spread pose with subtle inner thigh quiver.

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 2,
                'pos': """- Begins slow masturbation: fingers circle clitoris in deliberate lazy spirals, building wetness visible in glistening light.
- Expression deepens to aroused bliss – eyes half-lidded but locked on camera, smile fades to parted-lip gasp, soft audible sighs escape.
- Body undulates gently, breasts rise with deepening breaths,

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'MST 2_kopia_MST_V1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '50.61 turned back.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """- Begins slow masturbation: fingers circle clitoris in deliberate lazy spirals, building wetness visible in glistening light.
- Expression deepens to aroused bliss – eyes half-lidded but locked on camera, smile fades to parted-lip gasp, soft audible sighs escape.
- Body undulates gently, breasts rise with deepening breaths,

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_g4gg.json',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """- Begins slow masturbation: fingers circle clitoris in deliberate lazy spirals, building wetness visible in glistening light.
- Expression deepens to aroused bliss – eyes half-lidded but locked on camera, smile fades to parted-lip gasp, soft audible sighs escape.
- Body undulates gently, breasts rise with deepening breaths,

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_g4gg.json',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'MST 3_kopia_MST_V1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '50.61 turned back.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """She slowly rotates her upper body and hips toward the camera in a smooth 90-degree turn until she is facing forward directly into the lens. As her face enters the frame, apply the exact face from the top-left corner of the original photo as her consistent face – perfectly matched to lighting, skin tone, hair, and expressions. The top-left corner must now be empty / clean / showing only the background.
Once facing the camera, she locks eyes with the lens: slow, heavy-lidded, inviting gaze, slight parted-lips smile conveying strong sexual invitation and arousal.
She immediately slides / sinks deeper into the chair, reclining her back fully against the backrest, pelvis tilted forward. At the same time she spreads her legs very wide apart – knees moving outward as far as possible, feet flat on the floor or hooked over the edges of the seat if the chair allows – fully exposing her intimate area to the camera.
Both hands move directly between her widely spread thighs. She begins openly masturbating: fingers of both hands working rhythmically on her clitoris and vulva – slow circular motions at first, then gradually faster and more intense stroking / rubbing. Her movements are deliberate, visible, and unapologetic – clear self-pleasure with fingers sliding over wet skin, occasional parting of labia, focused clit stimulation.
She continues masturbating visibly and intensely until the very end of the video – never stopping, never closing her legs, never removing her hands from between her thighs. Her breathing becomes heavier, hips subtly rock forward into her own touch, expression shifts from inviting to deeply aroused (eyes half-closed, lips parted, soft moans implied).
""",
                'neg': '',
                'lora_high': '',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 4,
                'pos': """She slowly rotates her upper body and hips toward the camera in a smooth 90-degree turn until she is facing forward directly into the lens. As her face enters the frame, apply the exact face from the top-left corner of the original photo as her consistent face – perfectly matched to lighting, skin tone, hair, and expressions. The top-left corner must now be empty / clean / showing only the background.
Once facing the camera, she locks eyes with the lens: slow, heavy-lidded, inviting gaze, slight parted-lips smile conveying strong sexual invitation and arousal.
She immediately slides / sinks deeper into the chair, reclining her back fully against the backrest, pelvis tilted forward. At the same time she spreads her legs very wide apart – knees moving outward as far as possible, feet flat on the floor or hooked over the edges of the seat if the chair allows – fully exposing her intimate area to the camera.
Both hands move directly between her widely spread thighs. She begins openly masturbating: fingers of both hands working rhythmically on her clitoris and vulva – slow circular motions at first, then gradually faster and more intense stroking / rubbing. Her movements are deliberate, visible, and unapologetic – clear self-pleasure with fingers sliding over wet skin, occasional parting of labia, focused clit stimulation.
She continues masturbating visibly and intensely until the very end of the video – never stopping, never closing her legs, never removing her hands from between her thighs. Her breathing becomes heavier, hips subtly rock forward into her own touch, expression shifts from inviting to deeply aroused (eyes half-closed, lips parted, soft moans implied).
""",
                'neg': '',
                'lora_high': '',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'MST 4_kopia_MST_V1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\61.53 start MST.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': """The naked woman sits on the floor facing the camera. She locks intense, heavy-lidded eye contact with the lens, slow aroused half-smile, parted lips. She spreads her legs very wide, fully exposing her vulva.

Both hands move between her thighs and she begins masturbating openly – fingers circling and rubbing her clitoris in deliberate motions that gradually become faster and harder. One hand works her clit while the other parts her labia or slides fingers inside. Movements are clear, wet and visible.

She continues without pause, legs staying maximally spread. Her breathing quickens, hips start to grind forward into her hand, thighs tremble, expression becomes lost in pleasure – eyes fluttering, mouth open in gasps.

She builds to a powerful orgasm: movements turn frantic, body arches, legs tremble violently while remaining wide open, visible contractions around her vulva, loud moan implied. After the peak she collapses limp and exhausted on the floor – body slumped, arms fallen loosely, legs still spread wide, eyes half-closed in post-orgasmic haze, breathing slowly calming. She remains still and spent.""",
                'neg': '',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 2,
                'pos': """The naked woman sits on the floor facing the camera. She locks intense, heavy-lidded eye contact with the lens, slow aroused half-smile, parted lips. She spreads her legs very wide, fully exposing her vulva.

Both hands move between her thighs and she begins masturbating openly – fingers circling and rubbing her clitoris in deliberate motions that gradually become faster and harder. One hand works her clit while the other parts her labia or slides fingers inside. Movements are clear, wet and visible.

She continues without pause, legs staying maximally spread. Her breathing quickens, hips start to grind forward into her hand, thighs tremble, expression becomes lost in pleasure – eyes fluttering, mouth open in gasps.

She builds to a powerful orgasm: movements turn frantic, body arches, legs tremble violently while remaining wide open, visible contractions around her vulva, loud moan implied. After the peak she collapses limp and exhausted on the floor – body slumped, arms fallen loosely, legs still spread wide, eyes half-closed in post-orgasmic haze, breathing slowly calming. She remains still and spent.""",
                'neg': '',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 2,
                'pos': 'Woman is laying still and breath heavily',
                'neg': 'move whole body standing up',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'MST 5_kopia_MST_V1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': 'SENSUAL BI DANCE',
    },
    {
        'file': '71.51. kissing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Movie on screen slowly dissapear and fade away',
        'neg': 'NONE',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '71.53. kissing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': '',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman slowly rises to sitting position back to the camera',
                'neg': '',
            },
            {
                'duration': 3,
                'pos': 'Woman slowly turns toward camera to kneeling  position',
                'neg': '',
            },
        ],
        "chain_prefix": 'rises',
        'backend': 'linux',
        'fps': 16,
        'cfg': 3,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '71.55. kissing.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'The completely naked woman in the foreground rises from a kneeling position and walks out of the scene. Smooth natural motion of standing up and exiting the frame.',
        'neg': 'other women moving, additional women appearing, extra people, clothing on the woman, dressed, top, bottom, underwear, blurry, deformed limbs, bad anatomy, low quality, incomplete exit',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '71.57. kissing.png',
        'backend': 'linux',
        'duration': 4,
        'pos': 'Woman in foreground finishes leaving the scene completely to the righ edge of scene. Then two women in background slowly turn towards camera and approach with fluid, sensual steps.',
        'neg': 'NONE',
    },
    {
        'file': '71.59. kissing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'lora_high': '',
        'lora_low': '',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'sexy_dance, They do a sexy dance. They thrusts and sways her hips in a sexual manner.',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'sexy_dance, They do a sexy dance. They thrusts and sways her hips in a sexual manner. Next they turns to each other',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'sexy dance',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '71.61. kissing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'sexy_dance, Two women embrace each other and begin a sensual dance, slowly grinding and circling their hips while pressing their breasts tightly together. Intimate body contact, soft sensual movements, erotic tension, realistic skin and body details.',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': 'sexy_dance, While continuing their sensual dance and grinding their hips together with breasts pressed against each other, the two women lean in and begin passionately kissing. Soft open-mouth kisses, tongues meeting, intimate and erotic, continuous slow body movement.',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': 'sexy_dance, While continuing their sensual dance and grinding their hips together with breasts pressed against each other, the two women lean in and begin passionately kissing. Soft open-mouth kisses, tongues meeting, intimate and erotic, continuous slow body movement.',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'dancing together',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '71.62. kissing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': '',
        'neg': 'NONE',
        'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
        'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'sexy_dance, While continuing their sensual dance and grinding their hips together with breasts pressed against each other, the two women lean in and begin passionately kissing. Soft open-mouth kisses, tongues meeting, intimate and erotic, continuous slow body movement.',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': 'sexy_dance, Women stop kissing and sexy dancing turns back to camera',
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20HIGH%2014B.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Wan2.2%20-%20T2V%20-%20Sexy%20Dance%20-%20LOW%2014B%20.safetensors',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'kissing',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '71.63. kissing END.png',
        'backend': 'linux',
        'duration': 4,
        'pos': 'Women slowly moving away towards the cinema screen with a fluid, sensual step ',
        'neg': 'NONE',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': '71.57. kissing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'scene_break',
        'name': 'MODEL 1 ONE MINUTE NSFW V2',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame.",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': "Woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        "chain_prefix": 'Missionary FK2_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_MODEL_1_ONE_MINUTE_NSFW_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame.",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'Sexspoon FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_MODEL_1_ONE_MINUTE_NSFW_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2.5,
                'pos': "The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
            },
        ],
        "chain_prefix": 'Doggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_MODEL_1_ONE_MINUTE_NSFW_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'use_lightning': True,
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """Woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'Backdoggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_MODEL_1_ONE_MINUTE_NSFW_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """Woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_MODEL_1_ONE_MINUTE_NSFW_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\FILMY\\Cinema_1\\40.57 start dancing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now kneeling down in same background as the first frame, with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame.",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame.""",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video same background as the first frame.""",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame.",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_MODEL_1_ONE_MINUTE_NSFW_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'ZAKOŃCZENIE',
    },
    {
        'file': '81.51 Final.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Women kneels down face to camera',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Women smiling and waving hands',
                'neg': '',
                'audio_prompt': 'Excited joyful crowd cheers and shouts at an MMA event, energetic happy yelling, celebratory crowd reactions, people cheering loudly with enthusiasm',
                'audio_negative_prompt': 'ambient sound, background noise, music, commentary, announcer, fighting sounds, punches, kicks, low rumble, room tone, silence, distant noise',
            },
            {
                'duration': 4,
                'pos': 'Women leaving the scene',
                'neg': '',
                'audio_prompt': 'Excited joyful crowd cheers and shouts at an MMA event, energetic happy yelling, celebratory crowd reactions, people cheering loudly with enthusiasm',
                'audio_negative_prompt': 'ambient sound, background noise, music, commentary, announcer, fighting sounds, punches, kicks, low rumble, room tone, silence, distant noise',
            },
            {
                'duration': 2,
                'pos': 'Women leaving the scene turning to left edge of scene. Other woman do not appear on screen',
                'neg': 'Other woman on scene',
                'audio_prompt': 'Excited joyful crowd cheers and shouts at an MMA event, energetic happy yelling, celebratory crowd reactions, people cheering loudly with enthusiasm',
                'audio_negative_prompt': 'ambient sound, background noise, music, commentary, announcer, fighting sounds, punches, kicks, low rumble, room tone, silence, distant noise',
            },
        ],
        "chain_prefix": 'goodbye',
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
