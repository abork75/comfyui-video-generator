# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_021 - EM nowa praca.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_021 - EM nowa praca.yaml"))
# Generated: 2026-07-20 08:07:44
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\muszelka_pliki\\EM\\nowa_praca'

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
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'MODEL EM',
    },
    {
        'file': '99.006 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': 'A woman kneeling before man. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
        ],
        "chain_prefix": 'blow job_natural 1_kopia',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {"break": True},

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'MODELKAEM_1MIN',
    },
    {
        'file': '99.007 Natural.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': "The video then jumpcuts to the same woman Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'sexspoon doggy_MODELKAEM_1MIN',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.007 Natural.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggy_MODELKAEM_1MIN',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.008 Natural.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 6,
                'pos': """The video then jumpcuts to the same Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair  now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
        ],
        "chain_prefix": 'doggyback_MODELKAEM_1MIN',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.007 Natural.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

she looks at the camera throughout the video.

The video is shot from above looking down on the scene. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': 'static, frozen, thigh highs, socks, hosiery, legwear',
                'lora_high': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Blink_Squatting_Cowgirl_Position_I2V_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_MODELKAEM_1MIN',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'file': '99.007 Natural.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair small eyes. The video then jumpcuts to the same woman now lying down in same background as the first frame, stone tile floor, building wall with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
            },
            {
                'duration': 3,
                'pos': """Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

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
                'pos': """Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through various facial expressions throughout the video from happy to gasping she looks like she is talking.

She looks at the camera throughout the video
 same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 5,
                'pos': 'Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference same background as the first frame, wooden floor, white walls, red accent wall, potted plant.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 5,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman. The video then jumpcuts to the same woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 3,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_MODELKAEM_1MIN',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
