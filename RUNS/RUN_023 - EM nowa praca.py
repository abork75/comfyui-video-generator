# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_023 - EM nowa praca.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_023 - EM nowa praca.yaml"))
# Generated: 2026-07-21 14:20:50
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
    {
        'type': 'scene_break',
        'name': 'WYJSCIE Z DOMU',
    },
    {
        'file': '98.001 start.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': [
            {
                'file': '001. ide do klubu.mp3',
                'pos': 'The person is little ashamed',
            },
            {
                'file': '002. duzo placa.mp3',
                'pos': 'The person is little ashamed',
            },
        ],
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'NIGHT CLUB',
    },
    {
        'file': '98.002 night club.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'The video begins with the woman and man in spoon position. Then video jumpcuts to scene in night-club. Both dressed in elegant nightclub attire — she in a form-fitting short dress, he in a dark shirt and trousers. The video begins with the couple dancing close together on a crowded nightclub dance floor. Flashing colored lights, bass-heavy atmosphere, other dancers around them. Then video jumpcuts to the same couple — she is pressed against him from behind, his hands on her hips, both moving sensually to the music. Then video jumpcuts to a frontal view of the couple face to face, swaying together, foreheads almost touching, lost in the moment. Dark club interior, strobe lights, shallow depth of field, realistic, cinematic lighting.',
                'neg': '',
            },
            {
                'duration': 4,
                'pos': 'Scene in night-club. Both dressed in elegant nightclub attire — she in a form-fitting short dress, he in a dark shirt and trousers. The video begins with the couple dancing close together on a crowded nightclub dance floor. Flashing colored lights, bass-heavy atmosphere, other dancers around them. Then video jumpcuts to the same couple — she is pressed against him from behind, his hands on her hips, both moving sensually to the music. Then video jumpcuts to a frontal view of the couple face to face, swaying together, foreheads almost touching, lost in the moment. Dark club interior, strobe lights, shallow depth of field, realistic, cinematic lighting.',
                'neg': '',
            },
        ],
        "chain_prefix": 'night club',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'TAKSÓWKA',
    },
    {
        'file': '98.003 night club.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'Scene with the same woman and man — frontal view of a couple sitting in the back seat of a taxi, kissing passionately. The interior is dimly lit by passing streetlights. ',
                'neg': '',
                'lora_high': '',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'The woman is now straddling the man, facing him, moving slowly. Her hands on his shoulders, his hands on her waist. The taxi windows are slightly fogged. Intimate atmosphere, shallow depth of field, realistic, cinematic lighting.',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'taksówka',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'TEASER W DOMU',
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
                'duration': 5,
                'pos': 'A woman kneeling before man. The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 5,
                'pos': 'Woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
            },
            {
                'duration': 5,
                'pos': 'Woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference',
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

    {
        'file': '99.010 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'Man has penis erected',
        'neg': 'NONE',
        'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
        'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
    },
    {
        'file': '99.011 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
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
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 4,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_MODELKAEM_1MIN',
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
                'pos': "The video then jumpcuts to the same woman Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman - Than video jumpcut to scene with same woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 4,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. Woman is lying on her side, legs slightly bent. A man lying behind her in spooning position, vigorously fucking her from behind. Strong, deep, rhythmic penetration, man's hips thrusting forward against her ass. Clear side view showing the woman's face in profile, breasts exposed and bouncing with each thrust, open mouth, eyes rolling back, intense pleasure and overwhelm expression, heavy breathing. Man's hand gripping her hip and waist tightly, holding her against his body, dynamic and powerful sex motion, detailed anatomy, realistic penetration, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_high_noise.safetensors',
                'lora_low': 'WAN2.2_LoraSet/mql_casting_sex_spoon_wan22_i2v_v1_low_noise.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'sexspoon doggy_MODELKAEM_1MIN_2',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.011 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Man is kneeling down head bowed',
                'neg': '',
                'audio_prompt': 'subtle body movement, soft weight shift, quiet fabric rustle, gentle shuffling feet on floor, light position change, soft clothing sounds, natural movement foley, realistic, high quality',
                'audio_negative_prompt': 'music, melody, ambient drone, loud impact, hard footsteps, slap, sustained atmosphere, low quality, distortion',
            },
        ],
        "chain_prefix": 'man is kneeling down',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.023 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1184,
        'height': 1776,
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 6,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. Woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
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
        'file': '99.022 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1184,
        'height': 1776,
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
            {
                'duration': 6,
                'pos': """From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

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
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
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
            {
                'duration': 5,
                'pos': "Woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_MODELKAEM_1MIN',
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

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'HUSBAND AND WIFE',
    },
    {
        'file': '99.012 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 5,
                'pos': """A man is furiously licking the nose and philtrum of a woman. His tongue flicks in and out of her nostrils, and he purses his lips to suck on her nose. He brings his face so close to hers that they almost touch. The camera slowly zooms in on the woman's face.

St0p_l1ck, a man licks furiously from the chin to the forehead of a frozen woman. His right hand grips the nape of her neck and chin, forcing her head back. His tongue leaves a wide, wet trail from her chin to the corner of her mouth.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/SleepingKissLick_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/SleepingKissLick_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 5,
                'pos': """A man is furiously licking the nose and philtrum of a woman. His tongue flicks in and out of her nostrils, and he purses his lips to suck on her nose. He brings his face so close to hers that they almost touch. The camera slowly zooms in on the woman's face.

St0p_l1ck, a man licks furiously from the chin to the forehead of a frozen woman. His right hand grips the nape of her neck and chin, forcing her head back. His tongue leaves a wide, wet trail from her chin to the corner of her mouth.""",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/SleepingKissLick_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/SleepingKissLick_LOW.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'licking cum',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.013 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': 'The video begins with a close-up of a fully nude woman and the fully nude man. Man is showing his erected penis and testicles.',
                'neg': 'no penis deformed penis',
                'lora_high': 'WAN2.2_LoraSet/PENISLORA_22_i2v_HIGH_e320.safetensors',
                'lora_low': 'WAN2.2_LoraSet/PENISLORA_22_i2v_LOW_e496.safetensors',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'penis lora',
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
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman and man. Jumpcut to a same woman kneeling on all fours on the ground, back arched. A naked man from start image standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 6,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. Woman kneeling on all fours on the ground, back arched. A naked man standing behind her and vigorously fucking her in doggystyle position. Strong, deep, rhythmic penetration, man's hips slamming against her ass. Clear front view showing the woman's face, breasts hanging and bouncing with each thrust, open mouth, wide eyes, intense pleasure and overwhelm expression, heavy breathing. Man's hands gripping her waist tightly, dynamic and powerful sex motion, detailed anatomy, realistic penetration, forest setting, dramatic lighting, high detail, erotic atmosphere same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': 'side view, back view, wrong camera angle, no penetration, bad anatomy, deformed body, extra limbs, blurry, low quality, censored, clothes on, monster not behind her, weak motion, static pose, cartoon, floating, unrealistic scale, poor connection between bodies',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Front_Doggystyle_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'doggy_MODELKAEM_Husband',
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
                'pos': """The video begins with a close-up of a fully nude woman and the man The video then jumpcuts to the same woman and man now having sex with a same man in squatting cowgirl position her face fills the screen she is leaning over forwards as she bounces up and down aggressively. Man erect penis is in her vagina.

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
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 5,
                'pos': "Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair. The video begins with a close-up of a woman and man. The video then immiedately jumpcuts to the same woman now having sex in missionary position with the man from image. She is lying on her back on the ground with her legs spread with her knees to her chest hands on the floor. A man's penis is visible entering her vagina from below. The man is positioned kneeling between her legs infront of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'SquatCowgirl missionary_MODELKAEM_HUSBAND',
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
                'pos': "The video begins with a close-up of a fully nude woman (Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair small eyes) and the man. The video then jumpcuts to the same woman and man now lying down in same background as the first frame, with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
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
        "chain_prefix": 'titjob_hndjob_blwhnd_blow_finale_MODELKAEM_HUSBAND',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
        'frame_interpolation': False,
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'WYCZERPANA PRACOWNICA',
    },
    {
        'file': '99.014 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Woman is touching her breast and vagina sligtly moves',
                'neg': '',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'lezy wyczerpana',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'talk',
        'audio': [
            {
                'file': '01. Jestem dziwka.mp3',
                'pos': 'Woman is touching her breast and vagina sligtly moves',
            },
            {
                'file': '02. Najpierw klient.mp3',
                'pos': 'Woman is touching her breast and vagina sligtly moves',
            },
            {
                'file': '03 trzej klienci.mp3',
                'pos': 'Woman is touching her breast and vagina sligtly moves',
            },
            {
                'file': '04.Chwile odpoczac.mp3',
                'pos': 'Woman is touching her breast and vagina sligtly moves',
            },
        ],
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {
        "chain": [
            {
                'duration': 3,
                'pos': 'A woman lying on the floor curls up into a ball.',
                'neg': '',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        "chain_prefix": 'zwija w klebek',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.015 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'talk',
        'audio': [
            {
                'file': '05. Koniec przerwy koledzy.mp3',
                'pos': 'Man is looking at camera',
            },
            {
                'file': '06. we trzech na raz.mp3',
                'pos': 'Man is looking at camera',
            },
            {
                'file': '07. a mąż popatrzy.mp3',
                'pos': 'Man is looking at camera',
            },
        ],
        'width': 448,
        'height': 672,
        'backend': 'linux',
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
        'type': 'talk',
        'audio': '08. na wasze uslugi.mp3',
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.017 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'scene_break',
        'name': 'NEXT CUSTOMERS',
    },
    {
        'file': '99.018 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1584,
        'height': 2368,
    },
    {
        'type': 'talk',
        'audio': {
            'file': '10_zaproszenie_ nastepny_1.mp3',
            'pos': 'smiling eagerly, shaking her buttocks',
        },
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.021 next customers.png',
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
                'duration': 6,
                'pos': """The video then jumpcuts to the same Caucasian woman, light skin, slightly wrinkled face, medium brown shoulder-length straight hair  now having sex in doggystyle position with the man. From an overhead perspective, she is laying on the table with legs spread facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner.
Her legs are planted apart on the floor.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
            {
                'duration': 6,
                'pos': """From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

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
        "chain_prefix": 'doggyback_MODELKAEM_NEXT1_kopia',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.018 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1584,
        'height': 2368,
    },
    {
        'type': 'talk',
        'audio': {
            'file': '11. wyliz dokladnie 1.mp3',
            'pos': 'Woman is shaking her buttocks',
        },
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.020 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1184,
        'height': 1776,
    },
    {
        "chain": [
            {
                'duration': 6,
                'pos': """Woman now having sex in doggystyle position with the man. From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

she is looking directly at the camera fully facing it.

she looks back at the camera.

she looks at the camera throughout the video. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.""",
                'neg': 'side view only, back view, no eye contact, woman not looking at camera, static pose, weak thrusting, bad anatomy, deformed body, extra limbs, blurry motion, low quality, censored, clothes on, poor penetration, unrealistic scale, cartoon',
                'audio_prompt': 'rhythmic skin-on-skin slapping, flesh impact sounds, body weight shifting, wet contact sounds, rhythmic thrusting foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Back_Doggystyle_LOW.safetensors',
            },
            {
                'duration': 6,
                'pos': """From an overhead perspective, she is on all fours with her back facing the camera. A man is positioned behind her. his hand gripping her hips as he penetrates her from behind. The woman's expression changes throughout the scene, showing moments of pleasure and engagement with her partner. Her legs are spread apart with the man in-between her legs.

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
        "chain_prefix": 'doggyback_MODELKAEM_NEXT1',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': '99.017 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1120,
        'height': 1680,
    },
    {
        'type': 'talk',
        'audio': {
            'file': '11. wyliz dokladnie 2.mp3',
            'pos': 'Woman is laying on the table legs spread wide open',
        },
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.019 next customers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1264,
        'height': 1680,
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': "Woman now having sex in missionary position. She is lying on her back on the table with her legs spread with her knees to her chest hands on the table. A man's penis is visible entering her vagina from below. The man is positioned standing between her legs in front of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
            {
                'duration': 5,
                'pos': "Woman now having sex in missionary position. She is lying on her back on the table with her legs spread with her knees to her chest hands on the table. A man's penis is visible entering her vagina from below. The man is positioned standing between her legs in front of her thrusting his penis into her vagina. Throughout the scene, she appears to be experiencing pleasure, often with her mouth open or eyes closed as she lies back. Her hands hold onto her thighs spreading her legs. same background as the first frame, wooden floor, white walls, red accent wall, potted plant.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Missionary_I2V_LOW.safetensors',
                'audio_prompt': 'female moaning loud pleasure, rhythmic thrusting sounds, skin slapping wet impact, gasping breath, increasing intensity, climax vocal',
                'audio_negative_prompt': 'music, melody, speech, words, lyrics, reverb, echo, distortion, cartoon, low quality',
            },
        ],
        "chain_prefix": 'Missionary_MODELKAEM_3rd customer',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'TANIEC',
    },
    {
        'file': '99.024 next activities.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1328,
        'height': 3152,
    },
    {
        'type': 'talk',
        'audio': [
            '13. Należycie zaspokoilam.mp3',
            '14. umilic czas.mp3',
        ],
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.015 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 448,
        'height': 672,
    },
    {
        'type': 'talk',
        'audio': {
            'file': '15. zatanczysz.mp3',
            'pos': 'Man is looking at camera and is calm and steady',
        },
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.025 next activities.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1680,
        'height': 2512,
    },
    {
        'type': 'talk',
        'audio': {
            'file': '16 czy taki ubior odpowiada.mp3',
            'pos': 'Sensual woman, 28 years old, beautiful face, slowly spreading her arms outwards in a seductive gesture, gracefully circling and swaying her hips, talking directly to camera with soft seductive voice, natural lip sync, expressive face and body language, smooth elegant movements, dynamic pose, cinematic, photorealistic, 5 seconds video',
            'neg': 'static pose, stiff movement, deformed hands, bad anatomy, blurry, low quality, deformed hips, unnatural motion, extra limbs, text, watermark',
        },
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.015 Natural.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 448,
        'height': 672,
    },
    {
        'type': 'talk',
        'audio': '17. Jak tania dziwka.mp3',
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

    {"break": True},

    {
        'file': '99.027 dance.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'width': 1680,
        'height': 2512,
    },
    {
        'type': 'talk',
        'audio': [
            {
                'file': '18_a tak moze byc.mp3',
                'pos': 'Sensual woman, 28 years old, beautiful face, slowly spreading her arms outwards in a seductive gesture, gracefully circling and swaying her hips, talking directly to camera with soft seductive voice, natural lip sync, expressive face and body language, smooth elegant movements, dynamic pose, cinematic, photorealistic, 5 seconds video',
                'neg': 'static pose, stiff movement, deformed hands, bad anatomy, blurry, low quality, deformed hips, unnatural motion, extra limbs, text, watermark',
            },
            {
                'file': '19_od razu zatanczyc.mp3',
                'pos': 'Sensual woman, 28 years old, beautiful face, slowly spreading her arms outwards in a seductive gesture, gracefully circling and swaying her hips, talking directly to camera with soft seductive voice, natural lip sync, expressive face and body language, smooth elegant movements, dynamic pose, cinematic, photorealistic, 5 seconds video',
                'neg': 'static pose, stiff movement, deformed hands, bad anatomy, blurry, low quality, deformed hips, unnatural motion, extra limbs, text, watermark',
            },
        ],
        'width': 448,
        'height': 672,
        'backend': 'linux',
    },

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
