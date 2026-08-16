# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_022_MODELKI_NSFW.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_022_MODELKI_NSFW.yaml"))
# Generated: 2026-08-09 22:45:53
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki'

FORCE_RESOLUTION = (
    704,
    1056,
)
DEFAULT_RESOLUTION = (
    704,
    1056,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 8
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
        'name': '99.001 ONE MINUTE NSFW',
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
                'duration': 2,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor with white walls and people in background.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 4,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor with white walls and people in background.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_001',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. Woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor with white walls and people in background.",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_99_001',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, wooden floor with white walls and people in background.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor with white walls and people in background.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_001',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden floor with white walls and people in background.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, wooden floor with white walls and people in background.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, wooden floor with white walls and people in background.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, wooden floor with white walls and people in background.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, wooden floor with white walls and people in background.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Latin American woman with dark features, tan skin with natural texture, long dark brown wavy hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, wooden floor with white walls and people in background.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_001',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.002 ONE MINUTE NSFW',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.002 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, tile floor, beige walls, restaurant setting with patrons.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, tile floor, beige walls, restaurant setting with patrons.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_002_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': """Latin American woman, light brown skin, smooth texture, long dark brown wavy hair.  The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, tile floor, beige walls, restaurant setting with patrons.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_99_002_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, tile floor, beige walls, restaurant setting with patrons.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, tile floor, beige walls, restaurant setting with patrons.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_002_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, tile floor, beige walls, restaurant setting with patrons.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, tile floor, beige walls, restaurant setting with patrons.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, tile floor, beige walls, restaurant setting with patrons.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, tile floor, beige walls, restaurant setting with patrons.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, tile floor, beige walls, restaurant setting with patrons.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Latin American woman, light brown skin, smooth texture, long dark brown wavy hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, tile floor, beige walls, restaurant setting with patrons.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_002_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.003. EROTIC DANCE 1',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.003 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """European woman with light skin and dark hair, light skin with natural tone and smooth texture, dark brown short wavy hair with slight highlights. Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged. same background as the first frame, marina with boats and green hills behind wooden bench.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """European woman with light skin and dark hair, light skin with natural tone and smooth texture, dark brown short wavy hair with slight highlights. Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged. same background as the first frame, marina with boats and green hills behind wooden bench.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """European woman with light skin and dark hair, light skin with natural tone and smooth texture, dark brown short wavy hair with slight highlights. Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

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
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background. same background as the first frame, marina with boats and green hills behind wooden bench.""",
                'neg': '',
            },
            {
                'duration': 3,
                'pos': """European woman with light skin and dark hair, light skin with natural tone and smooth texture, dark brown short wavy hair with slight highlights. Create a 10-second hyper-detailed cinematic erotic dance video, 8K realistic animation, 60fps smooth motion.

Scene setup:

Precise 10-second sequence focusing purely on body movements:
0-2s: Places both hands behind head, elbows wide, hips sway seductively side-to-side, chest thrust forward.
2-4s: Slowly pivots 180 degrees turning back to camera, arches back, pushes buttocks out prominently.
4-7s: Maintains rear pose, circles hips/ass in wide deliberate rolls, adds short teasing up-down bounces making buttocks jiggle enticingly.
7-10s: Swings back to face camera, intense eye contact, hands glide provocatively over breasts, down stomach to caress inner thighs and intimate areas through fabric.
Camera: Static medium shot eye-level, subtle zoom to hips during rear section, full body visible. Fluid natural motions only, high detail. same background as the first frame, marina with boats and green hills behind wooden bench.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1_99_003__EROTIC_DANCE_1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.003 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """European woman with light skin and dark hair, light skin with natural tone and smooth texture, dark brown short wavy hair with slight highlights. A sensual female dancer performs an intimate, slow-motion erotic dance in a luxurious dimly lit bedroom, 10-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 3-6s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 6-10s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold same background as the first frame, marina with boats and green hills behind wooden bench.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """European woman with light skin and dark hair, light skin with natural tone and smooth texture, dark brown short wavy hair with slight highlights. A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 5-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
• 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
• 2-4s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
• 4-5s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

Camera and movement:
• STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
• Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

Technical rendering:
Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze. same background as the first frame, marina with boats and green hills behind wooden bench.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2_99_003__EROTIC_DANCE_1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': '99.004 ONE MINUTE NSFW',
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
                'pos': "Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': """Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, wooden floor, white walls, red accent wall, potted plant.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Middle Eastern woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
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
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.005 TEST MODELU WANNSFW',
    },
    {
        'file': '99.005 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_005__KNEELING_ON_THE_STREET TEST WAN NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'width': 448,
        'height': 672,
    },

    {
        'type': 'scene_break',
        'name': '99.005.ONE MINUTE NSFW',
    },
    {
        'file': '99.005 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_005__KNEELING_ON_THE_STREET',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': """European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, urban street with pedestrians and storefronts.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_99_005__KNEELING_ON_THE_STREET',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, urban street with pedestrians and storefronts.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_005__KNEELING_ON_THE_STREET',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, urban street with pedestrians and storefronts.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, urban street with pedestrians and storefronts.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, urban street with pedestrians and storefronts.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair and light skin, light skin tone with natural texture, dark brown shoulder-length straight hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, urban street with pedestrians and storefronts.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_005__KNEELING_ON_THE_STREET',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.006 ONE MINUTE NTSW',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.006 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "White European woman, fair skin, smooth complexion, long blonde wavy hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, outdoor patio with stone floor and black wicker chairs.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, long blonde wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, outdoor patio with stone floor and black wicker chairs.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_006_ONE_MINUTE_NTSW_patio',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, long blonde wavy hair. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, outdoor patio with stone floor and black wicker chairs.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_99_006_ONE_MINUTE_NTSW_patio',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, long blonde wavy hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, outdoor patio with stone floor and black wicker chairs.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, long blonde wavy hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, outdoor patio with stone floor and black wicker chairs.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_006_ONE_MINUTE_NTSW_patio',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, long blonde wavy hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, outdoor patio with stone floor and black wicker chairs.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, long blonde wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, outdoor patio with stone floor and black wicker chairs.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, long blonde wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, outdoor patio with stone floor and black wicker chairs.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'White European woman, fair skin, smooth complexion, long blonde wavy hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, outdoor patio with stone floor and black wicker chairs.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "White European woman, fair skin, smooth complexion, long blonde wavy hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, outdoor patio with stone floor and black wicker chairs.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, long blonde wavy hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, outdoor patio with stone floor and black wicker chairs.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_006_ONE_MINUTE_NTSW_patio',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.007 EROTIC DANCE 1',
    },
    {
        'file': '99.007 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, long blonde straight hair. Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged. same background as the first frame, boat interior with glass windows and coastal view.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, long blonde straight hair. Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged. same background as the first frame, boat interior with glass windows and coastal view.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, long blonde straight hair. Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

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
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background. same background as the first frame, boat interior with glass windows and coastal view.""",
                'neg': '',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, long blonde straight hair. Create a 10-second hyper-detailed cinematic erotic dance video, 8K realistic animation, 60fps smooth motion.

Scene setup:

Precise 10-second sequence focusing purely on body movements:
0-2s: Places both hands behind head, elbows wide, hips sway seductively side-to-side, chest thrust forward.
2-4s: Slowly pivots 180 degrees turning back to camera, arches back, pushes buttocks out prominently.
4-7s: Maintains rear pose, circles hips/ass in wide deliberate rolls, adds short teasing up-down bounces making buttocks jiggle enticingly.
7-10s: Swings back to face camera, intense eye contact, hands glide provocatively over breasts, down stomach to caress inner thighs and intimate areas through fabric.
Camera: Static medium shot eye-level, subtle zoom to hips during rear section, full body visible. Fluid natural motions only, high detail. same background as the first frame, boat interior with glass windows and coastal view.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1_99_007_SLAVE_DANCE',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.007 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, long blonde straight hair. A sensual female dancer performs an intimate, slow-motion erotic dance in a luxurious dimly lit bedroom, 10-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 3-6s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 6-10s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold same background as the first frame, boat interior with glass windows and coastal view.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, long blonde straight hair. A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 5-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
• 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
• 2-4s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
• 4-5s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

Camera and movement:
• STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
• Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

Technical rendering:
Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze. same background as the first frame, boat interior with glass windows and coastal view.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2_99_007_SLAVE_DANCE',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': '99.009 ONE MINUTE NSFW',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.009 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, subway train interior with seated and standing passengers.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_99_009_ONE_MINUTE_NTSW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.009 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, subway train interior with seated and standing passengers.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, subway train interior with seated and standing passengers.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_009_ONE_MINUTE_NTSW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.009 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, subway train interior with seated and standing passengers.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, subway train interior with seated and standing passengers.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, subway train interior with seated and standing passengers.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, subway train interior with seated and standing passengers.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, subway train interior with seated and standing passengers.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Caucasian woman with light skin tone, smooth, light-toned skin, light brown hair tied up in a bun. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, subway train interior with seated and standing passengers.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_009_ONE_MINUTE_NTSW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.010 ONE MINUTE NSFW',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.010 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_010_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.010 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, light green walls with white framed mirror and soft bedding.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, light green walls with white framed mirror and soft bedding.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_99_010_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.010 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, light green walls with white framed mirror and soft bedding.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_010_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.010 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, light green walls with white framed mirror and soft bedding.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, light green walls with white framed mirror and soft bedding.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, light green walls with white framed mirror and soft bedding.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "East Asian woman with soft facial features, light beige, smooth and unblemished, dark brown shoulder-length wavy hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, light green walls with white framed mirror and soft bedding.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_010_ONE_MINUTE_NSFW',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '90.011 ONE MINUTE NSFW FK',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.011 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden platform with dirt ground and rustic stone buildings.",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden platform with dirt ground and rustic stone buildings.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, tile floor, beige walls, restaurant setting with patrons. same background as the first frame, wooden platform with dirt ground and rustic stone buildings.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy FK_90_011_ONE_MINUTE_NSFW_FK',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.011 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, wooden platform with dirt ground and rustic stone buildings.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden platform with dirt ground and rustic stone buildings.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary FK_90_011_ONE_MINUTE_NSFW_FK',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.011 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden platform with dirt ground and rustic stone buildings.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, wooden platform with dirt ground and rustic stone buildings.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, wooden platform with dirt ground and rustic stone buildings.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, wooden platform with dirt ground and rustic stone buildings.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, wooden platform with dirt ground and rustic stone buildings.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "European woman with dark hair, pale skin with visible scars and bruises, wet dark brown shoulder-length wavy hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, wooden platform with dirt ground and rustic stone buildings.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_90_011_ONE_MINUTE_NSFW_FK',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.012 EROTIC DANCE 1 - 600mb g4gg',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.012 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

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
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 3,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a 10-second hyper-detailed cinematic erotic dance video, 8K realistic animation, 60fps smooth motion.

Scene setup:

Precise 10-second sequence focusing purely on body movements:
0-2s: Places both hands behind head, elbows wide, hips sway seductively side-to-side, chest thrust forward.
2-4s: Slowly pivots 180 degrees turning back to camera, arches back, pushes buttocks out prominently.
4-7s: Maintains rear pose, circles hips/ass in wide deliberate rolls, adds short teasing up-down bounces making buttocks jiggle enticingly.
7-10s: Swings back to face camera, intense eye contact, hands glide provocatively over breasts, down stomach to caress inner thighs and intimate areas through fabric.
Camera: Static medium shot eye-level, subtle zoom to hips during rear section, full body visible. Fluid natural motions only, high detail. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1_99_012_EROTIC_DANCE_1_-_600mb_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.012 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. A sensual female dancer performs an intimate, slow-motion erotic dance in a luxurious dimly lit bedroom, 10-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 3-6s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 6-10s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 5-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
• 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
• 2-4s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
• 4-5s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

Camera and movement:
• STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
• Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

Technical rendering:
Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2_99_012_EROTIC_DANCE_1_-_600mb_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': '99.012 EROTIC DANCE 1 - 1200mb g4gg',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.012 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

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
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 3,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a 10-second hyper-detailed cinematic erotic dance video, 8K realistic animation, 60fps smooth motion.

Scene setup:

Precise 10-second sequence focusing purely on body movements:
0-2s: Places both hands behind head, elbows wide, hips sway seductively side-to-side, chest thrust forward.
2-4s: Slowly pivots 180 degrees turning back to camera, arches back, pushes buttocks out prominently.
4-7s: Maintains rear pose, circles hips/ass in wide deliberate rolls, adds short teasing up-down bounces making buttocks jiggle enticingly.
7-10s: Swings back to face camera, intense eye contact, hands glide provocatively over breasts, down stomach to caress inner thighs and intimate areas through fabric.
Camera: Static medium shot eye-level, subtle zoom to hips during rear section, full body visible. Fluid natural motions only, high detail. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1_99_012_EROTIC_DANCE_1_-_1200mb_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.012 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. A sensual female dancer performs an intimate, slow-motion erotic dance in a luxurious dimly lit bedroom, 10-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 3-6s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 6-10s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 5-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
• 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
• 2-4s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
• 4-5s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

Camera and movement:
• STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
• Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

Technical rendering:
Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2_99_012_EROTIC_DANCE_1_-_1200mb_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': '99.012 EROTIC DANCE 1 - 3steps g4gg',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.012 Natural.png',
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
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a short, seductive video from this image:

She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a short, erotic video from this image:

She slowly turns her back to the camera, facing away completely.

Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

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
- Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 3,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. Create a 10-second hyper-detailed cinematic erotic dance video, 8K realistic animation, 60fps smooth motion.

Scene setup:

Precise 10-second sequence focusing purely on body movements:
0-2s: Places both hands behind head, elbows wide, hips sway seductively side-to-side, chest thrust forward.
2-4s: Slowly pivots 180 degrees turning back to camera, arches back, pushes buttocks out prominently.
4-7s: Maintains rear pose, circles hips/ass in wide deliberate rolls, adds short teasing up-down bounces making buttocks jiggle enticingly.
7-10s: Swings back to face camera, intense eye contact, hands glide provocatively over breasts, down stomach to caress inner thighs and intimate areas through fabric.
Camera: Static medium shot eye-level, subtle zoom to hips during rear section, full body visible. Fluid natural motions only, high detail. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 1_99_012_EROTIC_DANCE_1_-_3steps_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.012 Natural.png',
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
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. A sensual female dancer performs an intimate, slow-motion erotic dancem, 4-second cinematic video with fluid progression.

Action sequence (smooth 10-second progression at 24fps, slow-motion 0.25x speed):
• 0-3s: Starts in a standing pose facing camera at 45-degree angle, hands slowly rising from hips, tracing up her sides with fingertips grazing ribs, then cupping and caressing her full breasts sensually, arching back slightly as camera orbits clockwise from low angle to emphasize cleavage and curve of torso
• 1-2s: Hands glide downward in fluid waves over her toned abdomen, fingers splaying and pressing into soft skin, body undulating in hypnotic hip sways, camera pulls back to medium shot tracking her movements, side lighting casting erotic highlights on muscles flexing
• 3-4s: Hands descend teasingly between her thighs, one palm pressing inward while the other traces inner legs, knees bending into a deep sensual squat with legs parting slowly, head tilting back in pleasure; camera dolly zooms in from front low angle to intimate close-up on hands and face, ending with a lingering hold same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
            {
                'duration': 4,
                'pos': """White European woman, light skin, smooth texture, medium brown shoulder-length straight hair. A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 4-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
• 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
• 1-2s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
• 3-4s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

Camera and movement:
• STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
• Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

Technical rendering:
Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze. same background as the first frame, green grass, tree trunk, leafy plants, paved path behind.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Erotic dance 1 part 2_99_012_EROTIC_DANCE_1_-_3steps_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': '99.004 ONE MINUTE NSFW,  desiva 600 no g4gg',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.013 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, tile floor, beige walls, restaurant setting with patrons. same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_004_ONE_MINUTE_NSFW___desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'width': 448,
        'height': 672,
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_004_ONE_MINUTE_NSFW___desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'width': 448,
        'height': 672,
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde shoulder-length wavy hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, wooden barrels, dark wooden walls, dimly lit cellar.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_004_ONE_MINUTE_NSFW___desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'width': 448,
        'height': 672,
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.014 ONE MINUTE NSFW, desiva 600 no g4gg',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.014 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, tile floor, beige walls, restaurant setting with patrons. same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_99_014_ONE_MINUTE_NSFW__desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 4,
                'pos': """blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_99_014_ONE_MINUTE_NSFW__desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "blonde woman with fair skin, fair skin with smooth texture, long straight blonde hair with dark roots. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, wooden bench against stone wall with green door and yellow mailbox.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_99_014_ONE_MINUTE_NSFW__desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.015 ONE MINUTE NSFW FACE KEEP, desiva 600 no g4gg',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.015 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, paved walkway surrounded by green bushes and trees.",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'rhythmic body slapping, heavy breathing, soft female moaning pleasure, bed creaking rhythmic, skin contact foley, intimate ambience',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, echo chamber, reverb, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, paved walkway surrounded by green bushes and trees.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, tile floor, beige walls, restaurant setting with patrons. same background as the first frame, paved walkway surrounded by green bushes and trees.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy FK_99_015_ONE_MINUTE_NSFW_FACE_KEEP__desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.015 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Her hands are placed on the ground. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, paved walkway surrounded by green bushes and trees.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. Woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Her hands are placed on the ground. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, paved walkway surrounded by green bushes and trees.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary FK_99_015_ONE_MINUTE_NSFW_FACE_KEEP__desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.015 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, paved walkway surrounded by green bushes and trees.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame, paved walkway surrounded by green bushes and trees.""",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, paved walkway surrounded by green bushes and trees.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, paved walkway surrounded by green bushes and trees.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 4,
                'pos': "White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, paved walkway surrounded by green bushes and trees.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "White European woman, fair skin, smooth complexion, blonde hair tied back in a ponytail. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, paved walkway surrounded by green bushes and trees.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_99_015_ONE_MINUTE_NSFW_FACE_KEEP__desiva_600_no_g4gg',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.016 ONE MINUTE NSFW FACE KEEP, V2',
    },
    {
        'file': '99.016 Natural.png',
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
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
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
        "chain_prefix": 'Sexspoon FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.016 Natural.png',
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
        "chain_prefix": 'Doggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'use_lightning': True,
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.016 Natural.png',
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
        "chain_prefix": 'Backdoggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.016 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, dark hair, shoulder-length, straight. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

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
                'pos': """White European woman, fair skin, smooth complexion, blonde hair, shoulder-length, straight. Woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.016 Natural.png',
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
                'pos': "White European woman, fair skin, smooth complexion, blonde hair, shoulder-length, straight. Woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        "chain_prefix": 'Missionary FK2_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.016 Natural.png',
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
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': '99.017 ONE MINUTE NSFW FACE KEEP CARTOON',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.017 Anime.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "Animated cartoon style, cel-shaded, stylized illustration. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, realistic penetration, dramatic lighting, erotic atmosphere, soft cartoon lighting, expressive stylized faces, high detail cartoon rendering",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, photorealistic, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': "Woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere",
                'neg': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'Sexspoon FK_99_017_ONE_MINUTE_NSFW_FACE_KEEP',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': "The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': "Woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
        ],
        "chain_prefix": 'Doggy FK_99_017_ONE_MINUTE_NSFW_FACE_KEEP',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.017 Anime.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic,. The video begins with a close-up of a woman. Than video jumpcut to scene with same woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, photorealistic, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 3,
                'pos': """animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic,. Woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, photorealistic, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'Back doggy FK_99_017_ONE_MINUTE_NSFW_FACE_KEEP',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.017 Anime.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic,. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear, photorealistic, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': """Woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
        ],
        "chain_prefix": 'SquatCowgirl _99_017_ONE_MINUTE_NSFW_FACE_KEEP',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.017 Anime.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs.",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear, photorealistic, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': "Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. Woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality,  photorealistic, hyperrealistic, 3D render, live action, real person, photography, cinematic realismrealistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'Missionary FK2_99_017_ONE_MINUTE_NSFW_FACE_KEEP',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.017 Anime.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression. ",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, poor connection, weak motion, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': """Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic.The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video

Man's feet are seen in the background""",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, poor connection, weak motion, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': """Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
""",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, poor connection, weak motion, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
            {
                'duration': 4,
                'pos': 'Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, poor connection, weak motion, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
            {
                'duration': 4,
                'pos': "Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video.",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, poor connection, weak motion, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': "Animated cartoon style, 2D animation, cel-shaded, stylized illustration, anime aesthetic. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body.",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, poor connection, weak motion, hyperrealistic, 3D render, live action, real person, photography, cinematic realism',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_99_017_ONE_MINUTE_NSFW_FACE_KEEP',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {
        'type': 'scene_break',
        'name': '99.018 ONE MINUTE NSFW FACE KEEP V2',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.018 Natural.png',
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
        "chain_prefix": 'Sexspoon FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_018_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.018 Natural.png',
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
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': "Woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        "chain_prefix": 'Doggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_018_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'use_lightning': True,
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.018 Natural.png',
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
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
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
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        "chain_prefix": 'Backdoggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_018_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.018 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, dark hair, shoulder-length, straight. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

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
                'pos': """White European woman, fair skin, smooth complexion, blonde hair, shoulder-length, straight. Woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_018_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.018 Natural.png',
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
                'pos': "White European woman, fair skin, smooth complexion, blonde hair, shoulder-length, straight. Woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        "chain_prefix": 'Missionary FK2_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_018_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.018 Natural.png',
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
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_018_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': '99.019 ONE MINUTE NSFW FACE KEEP V2',
    },
    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.019 Natural.png',
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
        "chain_prefix": 'Sexspoon FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_019_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.019 Natural.png',
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
        "chain_prefix": 'Doggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_019_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'use_lightning': True,
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.019 Natural.png',
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
        "chain_prefix": 'Backdoggy FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_019_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.019 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """White European woman, fair skin, smooth complexion, dark hair, shoulder-length, straight. The video begins with a close-up of a fully nude woman. The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

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
                'pos': """White European woman, fair skin, smooth complexion, blonde hair, shoulder-length, straight. Woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_019_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.019 Natural.png',
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
                'pos': "White European woman, fair skin, smooth complexion, blonde hair, shoulder-length, straight. Woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        "chain_prefix": 'Missionary FK2_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_019_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\__DEVIANT ART\\Modelki_igraszki\\99.019 Natural.png',
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
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale FK_99_016_ONE_MINUTE_NSFW_FACE_KEEP V2_kopia_99_019_ONE_MINUTE_NSFW_FACE_KEEP_V2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'MST full movie',
    },
    {
        'file': '99.019 Natural.png',
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
            },
            {
                'duration': 3,
                'pos': """- Hands glide slowly upward from thighs to caress full breasts – fingers trace underboob, circle nipples gently pinching.
- Slides down to flat stomach, palms pressing sensually in circles, hips shift forward slightly.
- With a sultry wink, grips inner thighs and spreads legs languidly wide – knees part outward to 90 degrees, feet flat on sheets exposing intimate area teasingly.

Legs remain widely spread from the moment she turns forward until the very last frame.
Hands stay between her legs masturbating continuously – no pauses, no covering, no change of position.
Face is visible only after the turn and matches the provided top-left face perfectly.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'MST 1',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.019 Natural.png',
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
            },
        ],
        "chain_prefix": 'MST 2',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.019 Natural.png',
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
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
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
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
        ],
        "chain_prefix": 'MST 3',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.019 Natural.png',
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
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
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
                'use_lightning': True,
                'workflow': '_I2V_dasiwa_3step_nog4gg.json',
            },
        ],
        "chain_prefix": 'MST 4',
        'backend': 'linux',
        'fps': 16,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.019 Natural.png',
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
            },
            {
                'duration': 2,
                'pos': """The naked woman sits on the floor facing the camera. She locks intense, heavy-lidded eye contact with the lens, slow aroused half-smile, parted lips. She spreads her legs very wide, fully exposing her vulva.

Both hands move between her thighs and she begins masturbating openly – fingers circling and rubbing her clitoris in deliberate motions that gradually become faster and harder. One hand works her clit while the other parts her labia or slides fingers inside. Movements are clear, wet and visible.

She continues without pause, legs staying maximally spread. Her breathing quickens, hips start to grind forward into her hand, thighs tremble, expression becomes lost in pleasure – eyes fluttering, mouth open in gasps.

She builds to a powerful orgasm: movements turn frantic, body arches, legs tremble violently while remaining wide open, visible contractions around her vulva, loud moan implied. After the peak she collapses limp and exhausted on the floor – body slumped, arms fallen loosely, legs still spread wide, eyes half-closed in post-orgasmic haze, breathing slowly calming. She remains still and spent.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'MST 5',
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
