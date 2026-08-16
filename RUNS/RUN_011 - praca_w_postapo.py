# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_011_praca_w_postapo.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_011_praca_w_postapo.yaml"))
# Generated: 2026-05-28 17:43:58
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\muszelka_pliki\\MKK\\praca w postapo\\film'

FORCE_RESOLUTION = (
    1024,
    1024,
)
DEFAULT_RESOLUTION = (
    1024,
    1024,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 6
DEFAULT_CFG            = 2
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
        'file': '09.51. full street.png',
        'backend': 'linux',
        'duration': 5,
        'pos': 'Smooth, cinematic camera zoom-in on the women standing on the street, starting from a medium shot and slowly pushing in naturally over 4-5 seconds. The camera movement feels organic and handheld-like, with subtle parallax. The women move naturally and realistically — slight weight shifts, natural breathing, small head turns, blinking, subtle hair movement, gentle body sways and micro-expressions. They remain in approximately the same positions but feel alive and dynamic. Very natural motion, realistic physics, no sudden jumps, smooth continuous zoom combined with lifelike character animation, high detail, photorealistic, cinematic lighting',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '09.53. full street_zoom.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE tu prompt jest niepotrzebny',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '09.55. full street_zoom.p.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'Woman is touching the collar with right hand',
                'neg': '',
            },
            {
                'duration': 3,
                'pos': 'Woman is leaving the scene going to the right edge of screen',
                'neg': '',
            },
        ],
        "chain_prefix": 'dotyka_obrozy',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': '',
    },

    {"break": True},

    {
        'file': '10.01. presentation.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """2-second cinematic I2V2I time-lapse:

Start with empty post-apocalyptic street in bright daylight (Image 1).

In a very fast, dramatic transition the scene rapidly changes to deep night (dark blue/purple sky, strong shadows, moonlight), and at that exact moment the character instantly appears standing still in the center of the street. Then the lighting quickly transitions back to bright daylight (Image 2).

The character does not move or walk in — they simply appear during the night phase. Focus on strong, cinematic day-night-day cycle in just 2 seconds. Moody atmosphere, realistic lighting changes, photorealistic, ultra detailed.""",
        'neg': 'slow transition, static lighting, no lighting change, character walking in, gradual appearance, fade in, low quality motion, jerky lighting, unrealistic sky, deformed character, bad composition, extra movement, long animation',
    },
    {
        'file': '10.03. presentation.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """2-second cinematic I2V2I:

Start with Image 1 — character standing in pose A on a destroyed post-apocalyptic street in bright daylight.

In a rapid time-lapse: the scene dramatically darkens to night, during which the first character fades out completely. At the peak of darkness the second character (Image 2) instantly appears in a different pose in the same spot. Then the lighting rapidly returns to daylight.

Focus on the strong day-night-day cycle to show passage of time. Character switch is abrupt and sudden (no smooth morphing or walking). Cinematic, moody atmosphere, photorealistic.""",
        'neg': 'smooth character transition, morphing, character walking, slow fade, gradual change, fluid animation, static lighting, no day-night change, low quality lighting transition, deformed character, extra movement, long animation, character moving between poses',
    },
    {
        'file': '10.05. presentation.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """2-second cinematic I2V2I:

Start with Image 1 — character standing in pose A on a destroyed post-apocalyptic street in bright daylight.

In a rapid time-lapse: the scene dramatically darkens to night, during which the first character fades out completely. At the peak of darkness the second character (Image 2) instantly appears in a different pose in the same spot. Then the lighting rapidly returns to daylight.

Focus on the strong day-night-day cycle to show passage of time. Character switch is abrupt and sudden (no smooth morphing or walking). Cinematic, moody atmosphere, photorealistic.""",
        'neg': 'smooth character transition, morphing, character walking, slow fade, gradual change, fluid animation, static lighting, no day-night change, low quality lighting transition, deformed character, extra movement, long animation, character moving between poses',
    },
    {
        'file': '10.07. presentation.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """2-second cinematic I2V2I:

Start with Image 1 — character standing in pose A on a destroyed post-apocalyptic street in bright daylight.

In a rapid time-lapse: the scene dramatically darkens to night, during which the first character fades out completely. At the peak of darkness the second character (Image 2) instantly appears in a different pose in the same spot. Then the lighting rapidly returns to daylight.

Focus on the strong day-night-day cycle to show passage of time. Character switch is abrupt and sudden (no smooth morphing or walking). Cinematic, moody atmosphere, photorealistic.""",
        'neg': 'smooth character transition, morphing, character walking, slow fade, gradual change, fluid animation, static lighting, no day-night change, low quality lighting transition, deformed character, extra movement, long animation, character moving between poses',
    },
    {
        'file': '10.09. presentation.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'Women smoothly standing up',
        'neg': 'NONE',
    },
    {
        'file': '10.11. presentation.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Woman rapidly runs into ruined building door and disappears in it',
        'neg': 'NONE',
    },
    {
        'file': '10.13. presentation.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'Woman runs into building door nearby and disappears in interior of it ',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '10.47. Empty_street.png',
        'backend': 'linux',
        'duration': 5,
        'pos': """Smooth cinematic 6-second transition from the starting image (empty street) to the end frame. A group of four post-apocalyptic men slowly and naturally walk into the frame from the left side, moving with realistic gait and weight shifts. They form a loose queue in front of the ruined building entrance, stopping in their final positions.
Simultaneously, a beautiful woman smoothly appears in the upper floor window on the right — she leans out seductively over the windowsill, looking down at the men with a provocative smile. Her movement is graceful and natural, as if she was just stepping to the window.
Natural character animation, realistic walking motion, subtle body sways, breathing, and micro-movements. Smooth continuous camera movement with slight parallax. High detail, photorealistic motion, cinematic atmosphere, fluid 24fps transition, no sudden jumps or teleporting.""",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '10.49. near_building_Queue_2.png',
        'backend': 'linux',
        'duration': 5,
        'pos': 'Smooth, cinematic camera zoom-in on the women in the window, starting from a medium shot and slowly pushing in naturally over 4-5 seconds. The camera movement feels organic and handheld-like, with subtle parallax. The women move naturally and realistically — slight weight shifts, natural breathing, small head turns, blinking, subtle hair movement, gentle body sways and micro-expressions. They remain in approximately the same positions but feel alive and dynamic. Very natural motion, realistic physics, no sudden jumps, smooth continuous zoom combined with lifelike character animation, high detail, photorealistic, cinematic lighting',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '10.51. Panienka z okienka.mp4',
        'backend': 'linux',
        'duration': 3,
        'pos': 'A cinematic 3-second video: A young woman with long dark hair is leaning far out of an old apartment window, looking down with a worried expression. She slowly and smoothly pulls her upper body back into the dark interior of the room. Her movement is cautious and continuous. She gradually disappears completely from the window frame until only the empty, slightly moving curtain remains. Realistic lighting, moody atmosphere, slight camera shake, photorealistic, cinematic color grading, 4K.',
        'neg': """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement,
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement,
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions,
low quality, blurry motion, motion blur, artifact, glitch, flickering,
text, watermark, logo, overlay,
overexposed, underexposed, wrong lighting, warm colors,
multiple angles, split screen, changing camera angle too fast,
unnatural camera movement, orbiting too quickly, spinning camera""",
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'A cinematic 3-second video: A young woman with long dark hair is leaning far out of an old apartment window, looking down with a worried expression. She slowly and smoothly pulls her upper body back into the dark interior of the room. Her movement is cautious and continuous. She gradually disappears completely from the window frame until only the empty, slightly moving curtain remains. Realistic lighting, moody atmosphere, slight camera shake, photorealistic, cinematic color grading, 4K.',
                'neg': """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement,
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement,
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions,
low quality, blurry motion, motion blur, artifact, glitch, flickering,
text, watermark, logo, overlay,
overexposed, underexposed, wrong lighting, warm colors,
multiple angles, split screen, changing camera angle too fast,
unnatural camera movement, orbiting too quickly, spinning camera""",
            },
        ],
        "chain_prefix": 'dissapearing_woman',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
    },

    {"break": True},

    {
        'file': '15.41_klient1.png',
        'backend': 'linux',
        'duration': 5,
        'pos': 'Cinematic 4-second I2V video: The man is already standing next to the sofa at the beginning of the clip. He then walks with confident, purposeful steps from beside the sofa toward the left door frame in the foreground. When he reaches the door frame, he leans casually but firmly against it with his shoulder and back, turning his body slightly toward the camera. Keep his exact clothing, appearance, and the entire background (ruined room, sofa, debris, lighting) completely unchanged. Smooth, natural walking motion, realistic stride, confident posture, photorealistic, highly detailed, 4K.',
        'neg': """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement,
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement,
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions,
low quality, blurry motion, motion blur, artifact, glitch, flickering,
text, watermark, logo, overlay,
overexposed, underexposed, wrong lighting, warm colors,
multiple angles, split screen, changing camera angle too fast,
unnatural camera movement, orbiting too quickly, spinning camera""",
    },
    {
        'file': '15.43_klient1.png',
        'backend': 'linux',
        'duration': None,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '15.45_klient2.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '15.51. bedroom_2.png',
        'backend': 'linux',
        'duration': 5,
        'pos': "Camera slowly and smoothly zooms in from a medium shot to a close-up on the woman's face an breasts while she is sitting seductively on the bed. The final framing clearly shows her breasts at the top, belly in the center, and upper thighs at the bottom. Slow continuous zoom-in, elegant and sensual movement, cinematic lighting, intimate atmosphere, 5 seconds, high detail, photorealistic, woman slighlty moves her head smiles a little, move her hand and finger.",
        'neg': """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement,
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement,
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions,
low quality, blurry motion, motion blur, artifact, glitch, flickering,
text, watermark, logo, overlay,
overexposed, underexposed, wrong lighting, warm colors,
multiple angles, split screen, changing camera angle too fast,
unnatural camera movement, orbiting too quickly, spinning camera""",
    },
    {
        'file': '15.53. bedroom_2zoom.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'bra disappearing, clothes morphing, teleporting bra, blurry hands, unnatural motion, blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '15.55_a na czym polega.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '15.71. bede_cie_bral.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Man is going towards camera',
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain0',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '15.81. ale ta gra wymagajaca.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'jeki_2_3 krotkie.mp3',
            'pos': """cinematic video of a beautiful young woman lying flat on her back on a bed, arms spread wide above her head. She is being rhythmically and intensely thrust into, causing her entire body to slide back and forth on the sheets in a smooth, continuous motion without lifting her head or torso off the mattress. Her hips and lower body move naturally with the rhythm while her upper back and head stay pressed against the bed.
Her eyes slowly open and close, fluttering with pleasure, and her mouth gently parts and closes with soft moaning breaths in sync with the thrusts. Natural breast movement, realistic fabric sliding and wrinkles under her body, detailed skin and muscle micro-movements. Passionate yet grounded sexual motion, highly realistic physics, sensual atmosphere, soft cinematic lighting, 24fps smooth motion, photorealistic""",
        },
        'width': 512,
        'height': 512,
        'prefix': 'Pani_jeczy_1',
    },

    {"break": True},

    {
        'file': '16.41_klient2.png',
        'backend': 'linux',
        'duration': 4,
        'pos': '4-second cinematic video from static image: The bearded man sitting on the sofa in the destroyed living room pushes himself up and stands confidently. He walks with steady, self-assured steps across the room directly toward the left door frame. Upon reaching the frame, he leans back against it in a relaxed yet strong pose, one shoulder and arm resting on the frame, looking forward. Smooth transition from sitting to standing to walking to leaning. Keep the exact same clothing, facial features, room details, lighting, and debris. Natural physics, realistic motion, filmic atmosphere, photorealistic, 4K.',
        'neg': """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement,
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement,
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions,
low quality, blurry motion, motion blur, artifact, glitch, flickering,
text, watermark, logo, overlay,
overexposed, underexposed, wrong lighting, warm colors,
multiple angles, split screen, changing camera angle too fast,
unnatural camera movement, orbiting too quickly, spinning camera""",
    },
    {
        'file': '16.43_klient2.jpg',
        'backend': 'linux',
        'duration': None,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '16.45 ornitolog.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'Cinematic 3-second I2V video: The man standing in the frame slowly lowers his head and gaze downward, looking directly at his own crotch area. At the same time, he raises his right hand and points clearly with his index finger at his intimate area (groin). The movement is slow, deliberate and smooth. He holds the pointing gesture and keeps looking down until the end of the clip. Keep his exact body posture, standing position, clothing, background, lighting, and camera angle completely unchanged. Realistic, natural motion, slight motion blur on the moving hand, photorealistic, high detail, 4K.',
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain1',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '16.47 a co robi ornilolog.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Edit the woman\'s facial expression and hand position: Change her face to a surprised and shocked expression — wide open eyes, raised eyebrows, slightly open mouth in an "O" shape. She looks directly at the camera with a shocked gaze. Simultaneously, she raises both hands to her head and grabs her head/temples in a classic surprised gesture (fingers in her hair or on the sides of her head). Keep her exact body pose, torso position, legs, clothing, hair (except where hands touch it), background, lighting, and camera angle completely unchanged. Only modify the face and arms/hands. Perfect anatomy, natural hand placement, photorealistic, highly detailed, seamless edit.',
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain2',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '16.49. szuka ptaszka.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '16.51_klient2.png',
        'backend': 'linux',
        'duration': 5,
        'pos': "Smooth cinematic video: The camera slowly zooms in from medium shot to a tight close-up on the woman's face. She slightly leans her body and head forward toward the camera in an intimate way. While maintaining eye contact with the viewer, she slowly and naturally looks around — turning her head gently left and right, scanning the environment with curious eyes. Simultaneously, she waves her right hand softly and elegantly. Graceful, subtle movements, sensual atmosphere, beautiful lighting, shallow depth of field in the final close-up, photorealistic, 4K.",
        'neg': 'NONE',
    },
    {
        'file': '16.53_klient2.png',
        'backend': 'linux',
        'duration': None,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '16.53 juz znalazlam.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'Cinematic slow-motion video: The woman starts kneeling on the bed, then sensually slides her body down, lying on her side along the mattress facing the camera. While lying on her side and looking provocatively at the viewer, she smoothly raises her right arm and points her index finger downward toward the camera at a slight angle (as if beckoning or teasing). Her finger points clearly in the direction of the camera, not straight down. Strong seductive eye contact, confident and inviting expression. Smooth, graceful movement, luxurious bed, soft lighting, photorealistic, 4K, sensual mood.',
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain3',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '16.55. podobna do bierek.mp4',
        'backend': 'linux',
        'duration': 1,
        'pos': 'Smooth transition',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'jeki_1_dwa_dlugie.mp3',
            'pos': """cinematic video of a beautiful young woman lying flat on her back on a bed, arms spread wide above her head. She is being rhythmically and intensely thrust into, causing her entire body to slide back and forth on the sheets in a smooth, continuous motion without lifting her head or torso off the mattress. Her hips and lower body move naturally with the rhythm while her upper back and head stay pressed against the bed.
Her eyes slowly open and close, fluttering with pleasure, and her mouth gently parts and closes with soft moaning breaths in sync with the thrusts. Natural breast movement, realistic fabric sliding and wrinkles under her body, detailed skin and muscle micro-movements. Passionate yet grounded sexual motion, highly realistic physics, sensual atmosphere, soft cinematic lighting, 24fps smooth motion, photorealistic""",
        },
        'width': 512,
        'height': 512,
        'prefix': 'Pani_jeczy_2',
    },

    {"break": True},

    {
        'file': '17.41_klient3.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Cinematic 5-second I2V video: At the beginning of the clip the man is standing behind the sofa. He walks around the sofa in a natural arc (from the back side to the front), moving with confident, steady steps. After circling the sofa, he continues walking directly toward the left door frame in the foreground. Upon reaching it, he leans back against the frame in a relaxed yet strong pose — shoulder and arm resting on the frame. Keep the exact same clothing, facial features, ruined room details, sofa, debris, and lighting as in the original image. Fluid, realistic movement, natural physics, photorealistic, 4K.',
        'neg': 'NONE',
    },
    {
        'file': '17.43_klient3.png',
        'backend': 'linux',
        'duration': None,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '17.45. jaka zabawa.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'Cinematic 4-second I2V video: The woman starts in a kneeling position on the bed, facing slightly towards the camera. She sensually lowers herself, arching her back slightly, sliding her body down onto the bed in a fluid, provocative motion. She lies on her side along the bed, one leg slightly bent, supporting her head with one hand. Throughout the entire movement she maintains strong, direct eye contact with the camera, giving a bold, challenging, and seductive look. Slow motion, smooth transitions, soft dramatic lighting, luxurious bedroom setting, elegant lingerie or silk sheets, very sensual and alluring atmosphere, photorealistic, 8K quality.',
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain5',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '17.47. zabawa w palka zapalka.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 2,
                'pos': 'The man standing in the ruined room holds a heavy spiked club in his right hand. He first makes a short, powerful swing with the bat, then extends his arm forward and points the spiked end straight at the camera in a menacing, provocative way — as if threatening the viewer. His posture is strong and aggressive, muscles tense, cold intense stare directly into the lens. Slow-motion cinematic movement at the beginning turning into more dynamic motion, realistic physics on the bat, subtle camera shake, dark moody lighting, photorealistic, 4K, ultra-detailed.',
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain6',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '17.47. to maczuga.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': {
            'file': 'jeki_3_dwa dlugie_joy.mp3',
            'pos': """3-second cinematic video of a beautiful young woman lying flat on her back on a bed, arms spread wide above her head. She is being rhythmically and intensely thrust into, causing her entire body to slide back and forth on the sheets in a smooth, continuous motion without lifting her head or torso off the mattress. Her hips and lower body move naturally with the rhythm while her upper back and head stay pressed against the bed.
Her eyes slowly open and close, fluttering with pleasure, and her mouth gently parts and closes with soft moaning breaths in sync with the thrusts. Natural breast movement, realistic fabric sliding and wrinkles under her body, detailed skin and muscle micro-movements. Passionate yet grounded sexual motion, highly realistic physics, sensual atmosphere, soft cinematic lighting, 24fps smooth motion, photorealistic""",
        },
        'width': 512,
        'height': 512,
        'prefix': 'Pani_jeczy_3',
    },

    {"break": True},

    {
        'file': '18.41_klient4.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': '4-second cinematic video from static image: The bearded man sitting on the sofa in the destroyed living room pushes himself up and stands confidently. He walks with steady, self-assured steps across the room directly toward the left door frame. Upon reaching the frame, he leans back against it in a relaxed yet strong pose, one shoulder and arm resting on the frame, looking forward. Smooth transition from sitting to standing to walking to leaning. Keep the exact same clothing, facial features, room details, lighting, and debris. Natural physics, realistic motion, filmic atmosphere, photorealistic, 4K.',
        'neg': 'NONE',
    },
    {
        'file': '18.43_klient4.jpg',
        'backend': 'linux',
        'duration': None,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.43_kląskanie.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.45. co to za gra.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.47_na_kolana.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.49. klient4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """5 second film:

Start with the woman kneeling on the bed (from first reference image). She smoothly and sensually gets off the bed, moving downwards, and kneels on the floor in front of the bed, ending in the exact same kneeling position as in the second reference image.

At the same time, a man enters the scene from the left side of the frame, walking confidently into the shot. He stops on the left side next to the woman, standing and facing forward toward the camera with a dominant posture.

The woman’s movement from kneeling on the bed to kneeling on the floor should be fluid and continuous. The man’s entrance and stopping should be natural and strong. Keep both characters' exact appearances, clothing, and style from their respective reference images. Maintain consistent lighting, bedroom environment, and camera angle.

Smooth camera movement if needed, realistic physics, natural motion blending between both reference images, photorealistic, highly detailed, 4K.""",
        'neg': 'static pose, no movement, woman staying on bed, man appearing suddenly, teleporting, bad transition, deformed motion, extra limbs, distorted body, wrong pose, low quality motion, jerky movement, floating, bad anatomy, different clothing, lighting inconsistency, blurry motion',
    },
    {
        'file': '18.51. klient4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.53. klient4.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.55. klient4.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '18.57. klient4.mp4',
        'backend': 'linux',
        'duration': 5,
        'pos': 'Man is turning towards camera while woman is still in position but shaking his buttock which slowly turns red.',
        'neg': 'NONE',
    },
    {
        'file': '18.59. klient4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': """Cinematic 5 second I2V video:

A woman who is kneeling on the floor in front of the bed slowly and gracefully stands up. She then turns and smoothly lies down on her back on the luxurious bed, placing her head comfortably on the pillows. Her movement is sensual and fluid.

At the same time, a man standing in the foreground facing the camera slowly turns his head and upper body toward the woman as she moves onto the bed, watching her with focus.

Both movements happen naturally and are well synchronized. Keep the exact appearance, clothing, and style of both characters. Maintain consistent lighting, bedroom environment, and realistic physics. Smooth, elegant motion, photorealistic, highly detailed, cinematic atmosphere, 4K.""",
                'neg': 'static pose, no movement, woman staying on bed, man appearing suddenly, teleporting, bad transition, deformed motion, extra limbs, distorted body, wrong pose, low quality motion, jerky movement, floating, bad anatomy, different clothing, lighting inconsistency, blurry motionstatic pose, no movement, woman staying on bed, man appearing suddenly, teleporting, bad transition, deformed motion, extra limbs, distorted body, wrong pose, low quality motion, jerky movement, floating, bad anatomy, different clothing, lighting inconsistency, blurry motion',
            },
        ],
        "chain_prefix": 'nowy_chain8',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '18.61. klient4.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': [
            {
                'file': 'jeki_2_3 krotkie.mp3',
                'pos': 'beautiful young woman lying on her back on a bed, arms spread wide above her head. She is being rhythmically and intensely moved back and forth on the sheets by strong, fast thrusts. Her body slides up and down the bed with each powerful motion, hips slightly lifting, breasts bouncing naturally. Her head tilts back, mouth opens wide in pleasure with each forward push, eyes half-closed or rolling back. Passionate and intense sexual motion, realistic physics, natural body movement, detailed fabric wrinkles on the sheets, soft cinematic lighting, highly realistic, sensual atmosphere, 24fps smooth motion',
            },
            {
                'file': 'jeki_3_dwa dlugie_joy.mp3',
                'pos': """beautiful young woman lying flat on her back on a bed, arms spread wide above her head. She is being rhythmically and intensely thrust into, causing her entire body to slide back and forth on the sheets in a smooth, continuous motion without lifting her head or torso off the mattress. Her hips and lower body move naturally with the rhythm while her upper back and head stay pressed against the bed.
Her eyes slowly open and close, fluttering with pleasure, and her mouth gently parts and closes with soft moaning breaths in sync with the thrusts. Natural breast movement, realistic fabric sliding and wrinkles under her body, detailed skin and muscle micro-movements. Passionate yet grounded sexual motion, highly realistic physics, sensual atmosphere, soft cinematic lighting, 24fps smooth motion, photorealistic""",
            },
        ],
        'width': 512,
        'height': 512,
        'prefix': 'Pani_jeczy_4',
    },

    {"break": True},

    {
        'file': '19.53. Empty_street END.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '19.55. Empty_street END.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '19.57. Empty_street END.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '19.59. Empty_street END.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '20.49. old_one_END.png',
        'backend': 'linux',
        'duration': 5,
        'pos': """Cinematic 5-second I2V2I video transition:

Start with the first reference image: the woman standing in the distance with her back fully turned to the camera.

During the 5 seconds the camera slowly and smoothly zooms in toward the woman. At the same time, she slowly and sensually turns her upper body and head toward the camera. The turn should be graceful and continuous, ending with her facing the camera directly.

End frame (second reference image): tight close-up from waist up, woman looking at the camera.

Perfect synchronization between the camera zoom and her turning motion. Smooth, elegant movement, realistic physics, natural turning speed. Maintain her exact clothing, hair, body proportions and style from both reference images. Consistent lighting and environment. Photorealistic, highly detailed, cinematic atmosphere, 4K.""",
        'neg': 'static camera, no zoom, sudden turn, fast rotation, jerky movement, bad transition, deformed body during turn, extra limbs, distorted face, changed clothing, different hair, blurry motion, low quality, static pose, no turning, wrong framing at the end, teleporting, unnatural rotation',
    },
    {
        'file': '20.51. old_one_END.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'smooth transition',
        'neg': 'NONE',
    },
    {
        'file': '20.53. old_one_END.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': '20.55. old_one_END.mp4',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 3-second I2V video: In a post-apocalyptic ruined street with destroyed buildings, crumbling facades, and cracked asphalt, a beautiful woman gracefully leaves the scene.

She is wearing only a tight black corset that exposes her breasts, long black leather boots, and a black leather collar with metal spikes. Otherwise she is completely nude.

She turns slightly and walks away from the camera with sensual, confident movement — slow seductive steps, beautiful posture, gentle sway of her hips and long hair. She moves from the foreground toward the background and elegantly exits the frame.

Graceful yet raw and seductive exit in a desolate environment. Smooth cinematic motion, dramatic filmic lighting, photorealistic, highly detailed, 4K.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'nowy_chain9',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

]

FLOW_TEST = [
    {
        'file': '05.05. ZOOM_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.09. ZOOM_2.png',
        'backend': 'linux',
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
