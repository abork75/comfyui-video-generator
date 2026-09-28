# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_030 Slave wife training.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_030 Slave wife training.yaml"))
# Generated: 2026-09-28 08:36:34
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_030 - Slave wife training'

FORCE_RESOLUTION = (
    1472,
    832,
)
DEFAULT_RESOLUTION = (
    1472,
    832,
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
        'file': '50.51 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '50.53 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking_2',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '50.55 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking_3',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '50.57 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking_4',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman lying face-down on spakning woman knees with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '50.59 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking_5',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman kneeling face-down  with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman kneeling face-down  with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '50.61 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking_6',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman kneeling face-down  with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman kneeling face-down  with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '50.63 Spanking.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'spanking_7',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman kneeling face-down  with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
            {
                'duration': 4,
                'pos': 'spanked, A black clothed woman vigorously spanking a woman kneeling face-down  with her ass fully sticking out and raised high. The black clothed  woman delivers fast, hard, sharp spanking strikes with his open hand on her bare buttocks. Clear motion dynamics: quick powerful hits, exactly two strong spankings every 2 seconds, realistic impact, skin jiggle and bounce with each strike, hand moving rapidly up and down. Dynamic camera, natural motion blur on the fast hand movements, realistic physics, detailed skin deformation on impact,  high quality, smooth motion, cinematic lighting',
                'neg': 'slow motion, slow hits, soft spanking, weak strikes, blurry, deformed hands, extra fingers, bad anatomy, static image, no movement, frozen frame, low quality, artifacts, distorted body, unnatural physics, cartoon, anime, overexposed, underexposed',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lora_high': 'WAN2.2_LoraSet/Spanking_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/Spanking_LOW.safetensors',
                'audio_prompt': 'sharp slap impact, flesh impact sound, skin contact, crisp smack, physical strike, body percussion, high quality, realistic foley,woman cries loud',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, wet sound, low quality, distortion',
            },
        ],
    },

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
