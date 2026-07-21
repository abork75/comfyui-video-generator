# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_000 - templates.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_000 - templates.yaml"))
# Generated: 2026-07-21 10:08:24
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\generacja_filmow\\NSFW'

FORCE_RESOLUTION = (
    448,
    672,
)
DEFAULT_RESOLUTION = (
    448,
    672,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 6
DEFAULT_CFG            = 2
DEFAULT_DURATION       = 2
DEFAULT_BLOCKS_TO_SWAP      = 20
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
        'name': 'ONE MINUTE NTSW',
    },
    {
        'file': '99.004 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
            },
        ],
        "chain_prefix": 'sexspoon doggy',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': """The same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression. ",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 5,
                'pos': 'The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 5,
                'pos': "The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': 'LONG DOGGY',
    },
    {
        'file': '99.001 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """The same woman - now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': """The same woman - ow having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback 2',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'EROTIC DANCE 1',
    },
    {
        'file': '99.001 Natural.png',
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
                'duration': 5,
                'pos': """Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged.""",
                'neg': '',
            },
            {
                'duration': 5,
                'pos': """Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged.""",
                'neg': '',
            },
            {
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
- Ends with a sultry gaze directly into lens, biting lower lip, body frozen in this pose as subtle hip sway fades out.

Camera work:
- Starts with smooth tracking shot circling from front at eye level.
- Transitions to slight low-angle tilt-up emphasizing curves and movements.
- Static hold in final second for intimate close-up on face and bust.
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background.""",
                'neg': '',
            },
            {
                'duration': 3,
                'pos': """Create a 10-second hyper-detailed cinematic erotic dance video, 8K realistic animation, 60fps smooth motion.

Scene setup:

Precise 10-second sequence focusing purely on body movements:
0-2s: Places both hands behind head, elbows wide, hips sway seductively side-to-side, chest thrust forward.
2-4s: Slowly pivots 180 degrees turning back to camera, arches back, pushes buttocks out prominently.
4-7s: Maintains rear pose, circles hips/ass in wide deliberate rolls, adds short teasing up-down bounces making buttocks jiggle enticingly.
7-10s: Swings back to face camera, intense eye contact, hands glide provocatively over breasts, down stomach to caress inner thighs and intimate areas through fabric.
Camera: Static medium shot eye-level, subtle zoom to hips during rear section, full body visible. Fluid natural motions only, high detail.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.001 Natural.png',
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
                'duration': 5,
                'pos': """A sensual female dancer performs an intimate, slow-motion erotic dance in a luxurious dimly lit bedroom, 10-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 3-6s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 6-10s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold""",
                'neg': '',
            },
            {
                'duration': 5,
                'pos': """A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 5-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
• 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
• 2-4s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
• 4-5s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

Camera and movement:
• STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
• Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

Technical rendering:
Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2',
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
