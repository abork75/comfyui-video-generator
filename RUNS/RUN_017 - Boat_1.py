# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_017 - Boat_1.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_017 - Boat_1.yaml"))
# Generated: 2026-08-17 17:17:37
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_017 - Boat_1'

FORCE_RESOLUTION = (
    480,
    624,
)
DEFAULT_RESOLUTION = (
    480,
    624,
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
        'file': 'FIN028_p1.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_p2.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_spank01.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank02.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank03.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank04.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_spank1.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a tall dominant woman in black latex standing over a submissive woman who is bent over, ass up, completely naked and vulnerable. The domina is whipping the slave's ass hard with a thick leather belt.

Two powerful strikes: first strong swing and impact at 1.2s, second even harder strike at 2.8s. Focus on the dynamic motion of the belt, realistic impact, jiggle and red marks on skin after each hit, belt movement with motion blur, strong swing dynamics, cinematic camera angle from slightly below, dramatic lighting, high detail, realistic physics, sensual and intense atmosphere""",
        'neg': 'static pose, slow motion, no movement, weak hits, no impact, blurry motion, deformed bodies, extra limbs, bad anatomy, low quality, cartoon, anime, text, watermark, deformed belt, floating belt, poor physics',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank2.png',
        'backend': 'linux',
        'duration': 4,
        'pos': 'NONE',
        'neg': 'NONE',
        'frame_interpolation': False,
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'FIN028_spank3.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a tall dominant woman in black latex standing over a submissive woman who is bent over, ass up, completely naked and vulnerable. The domina is whipping the slave's ass hard with a thick leather belt.

Two powerful strikes: first strong swing and impact at 1.2s, second even harder strike at 2.8s. Focus on the dynamic motion of the belt, realistic impact, jiggle and red marks on skin after each hit, belt movement with motion blur, strong swing dynamics, cinematic camera angle from slightly below, dramatic lighting, high detail, realistic physics, sensual and intense atmosphere""",
        'neg': 'static pose, slow motion, no movement, weak hits, no impact, blurry motion, deformed bodies, extra limbs, bad anatomy, low quality, cartoon, anime, text, watermark, deformed belt, floating belt, poor physics',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_spankingface1.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_spank4.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a tall dominant woman in black latex standing over a submissive woman who is bent over, ass up, completely naked and vulnerable. The domina is whipping the slave's ass hard with a thick leather belt.

Two powerful strikes: first strong swing and impact at 1.2s, second even harder strike at 2.8s. Focus on the dynamic motion of the belt, realistic impact, jiggle and red marks on skin after each hit, belt movement with motion blur, strong swing dynamics, cinematic camera angle from slightly below, dramatic lighting, high detail, realistic physics, sensual and intense atmosphere""",
        'neg': 'static pose, slow motion, no movement, weak hits, no impact, blurry motion, deformed bodies, extra limbs, bad anatomy, low quality, cartoon, anime, text, watermark, deformed belt, floating belt, poor physics',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank5.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a tall dominant woman in black latex standing over a submissive woman who is bent over, ass up, completely naked and vulnerable. The domina is whipping the slave's ass hard with a thick leather belt.

Two powerful strikes: first strong swing and impact at 1.2s, second even harder strike at 2.8s. Focus on the dynamic motion of the belt, realistic impact, jiggle and red marks on skin after each hit, belt movement with motion blur, strong swing dynamics, cinematic camera angle from slightly below, dramatic lighting, high detail, realistic physics, sensual and intense atmosphere""",
        'neg': 'static pose, slow motion, no movement, weak hits, no impact, blurry motion, deformed bodies, extra limbs, bad anatomy, low quality, cartoon, anime, text, watermark, deformed belt, floating belt, poor physics',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank6.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank7.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
    },
    {"break": True},

    {
        'file': 'FIN028_spankingface2.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_spank7.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank8.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Dynamic 4-second video, intense BDSM scene: a dominant woman in black latex standing over a submissive naked woman bent over on all fours, ass up. The domina is whipping the slave hard with a thick leather belt, focusing on powerful strikes to the left buttock.

Two strong hits: first powerful strike landing precisely on the left ass cheek at 1.2 seconds, second even harder strike on the same left buttock at 2.8 seconds. Clear motion of the belt swing, realistic impact physics, skin jiggle and red whip marks appearing on the left buttock after each hit, dynamic belt movement with natural motion blur, cinematic side angle, dramatic lighting, high detail, realistic pain reaction, sensual and intense atmosphere""",
        'neg': 'hitting right buttock, hitting both buttocks equally, weak hits, no impact, static pose, slow motion, deformed bodies, bad anatomy, blurry motion, floating belt, poor physics, low quality, cartoon',
        'frame_interpolation': False,
        'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley',
        'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
    },
    {
        'file': 'FIN028_spank9.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Dynamic 4-second video, intense BDSM scene: a tall dominant woman in black latex standing over a submissive woman who is bent over, ass up, completely naked and vulnerable. The domina is whipping the slave's ass hard with a thick leather belt.

Two powerful strikes: first strong swing and impact at 1.2s, second even harder strike at 2.8s. Focus on the dynamic motion of the belt, realistic impact, jiggle and red marks on skin after each hit, belt movement with motion blur, strong swing dynamics, cinematic camera angle from slightly below, dramatic lighting, high detail, realistic physics, sensual and intense atmosphere""",
        'neg': 'static pose, slow motion, no movement, weak hits, no impact, blurry motion, deformed bodies, extra limbs, bad anatomy, low quality, cartoon, anime, text, watermark, deformed belt, floating belt, poor physics',
    },
    {"break": True},

    {
        'file': 'FIN028_spankingface3.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_koniecchlosty.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'Dominatrix is leaving the room, woman on bed is laying still without movement',
                'neg': '',
                'audio_prompt': 'foley sound effects, physical environment sounds, footsteps, cloth movement, objects, wind bursts, creaking, synchronized with video, crisp, realistic, high quality',
                'audio_negative_prompt': 'music, melody, instruments, singing, ambient drone, sustained atmosphere, continuous background noise, reverb heavy, low quality, distortion',
            },
            {
                'duration': 2,
                'pos': 'Woman on bed is still laying practially without any move just brathing, face down to bed',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'domina wychodzi',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'FIN028_corridorwalk.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_waiting.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'Woman on bed is still laying practially without any move just brathing, face down to bed',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'oczekiwanie',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'FIN028_nomoreresting.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'FIN028_waiting.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """A woman lying face down on a large bed at the beginning, camera starts from a medium full shot. She slowly and with visible effort begins to get up. She slides her legs off the edge of the bed, carefully places her feet on the floor, then pushes herself up with her hands firmly planted on the bed. She rises unsteadily, supporting her weight on her arms.

Camera movement: starts distant, smoothly dollies in and transitions into a close-up shot as she stands up, ending in a medium close-up of her upper body and arms as she leans on the bed. Slow, realistic, struggling movement, tired and heavy motion, natural body physics, detailed skin and muscle tension, cinematic lighting, high detail, smooth 4-second video""",
        'neg': 'fast movement, sudden jump, easy rising, standing up too quickly, no effort, static camera, no camera movement, deformed body, bad anatomy, extra limbs, blurry motion, low quality, cartoon, unrealistic physics',
        'frame_interpolation': True,
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'FIN028_standingup.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman is leaving the scene going front to camera',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'opuszcza kajute',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'FIN028_to the wall.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Domintarix is passing away, woman ad wall is standing still',
                'neg': '',
                'audio_prompt': 'foley sound effects, physical environment sounds, footsteps, cloth movement, objects, wind bursts, creaking, synchronized with video, crisp, realistic, high quality',
                'audio_negative_prompt': 'music, melody, instruments, singing, ambient drone, sustained atmosphere, continuous background noise, reverb heavy, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': 'We woman on right is continuing leaving the scene. Woman at the wall standing still',
                'neg': '',
                'audio_prompt': 'foley sound effects, physical environment sounds, footsteps, cloth movement, objects, wind bursts, creaking, synchronized with video, crisp, realistic, high quality',
                'audio_negative_prompt': 'music, melody, instruments, singing, ambient drone, sustained atmosphere, continuous background noise, reverb heavy, low quality, distortion',
            },
        ],
        "chain_prefix": 'passing away',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'FIN028_final_humilation_expose.mp4',
        'backend': 'linux',
        'duration': 3,
        'pos': "Smooth zoom on woman's face",
        'neg': 'NONE',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'FIN028_finalhumilation_zoom.mp4',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Camera slowly zoom out',
        'neg': 'NONE',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'FIN028_finalhumilation_zoomout.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Women is kneeling down before her dominatrix',
        'neg': 'NONE',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'FIN028_kleczy.jpg',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Women is bowing and kissing boots of her dominatrix',
        'neg': 'NONE',
        'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
        'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
    },
    {
        'file': 'FIN028_calujestopy.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
