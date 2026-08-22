# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_026 - warrior and sorceress.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_026 - warrior and sorceress.yaml"))
# Generated: 2026-08-22 02:11:58
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_026 - warrior_and_sorceress'

FORCE_RESOLUTION = (
    1104,
    816,
)
DEFAULT_RESOLUTION = (
    1104,
    816,
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
        'file': '40.51. ida na walke.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.53. zblizaja sie do obozu.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.55. walka o skarb.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.59. skrzynia_skarbow.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.61. ida przez las.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.63. ida przez las.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.65. wejscie_do_miasta.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.69. wejscie_do_karczmy.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '40.69. wejscie_do_karczmy_40.71. wejscie_do_karczmy',
        'model_class': 'ltx',
        'neg': 'exaggerated motion, frantic movement, large gestures, waving arms, walking, talking, jumping, sudden movement, jump cut, twitching, rubber body, distorted faces, blurry, low quality',
        'chain': [
            {
                'duration': 10,
                'pos': 'The camera slowly pans left at a constant speed. The characters stay seated and standing in their original poses. Only tiny idle motion: slow breathing and a barely visible weight shift. No head turns, no talking, no walking, no gesturing.',
                'neg': '',
                'use_lightning': False,
                'workflow': '_I2V_classic_hq_nog4gg.json',
                'ltx_variant': '8step',
                'frame_interpolation': False,
            },
        ],
        'width': 1280,
        'height': 960,
    },

    {
        'file': '40.71. wejscie_do_karczmy.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '40.71. wejscie_do_karczmy_40.73. wejscie_do_karczmy',
        'model_class': 'ltx',
        'neg': 'freeze frame, completely static image, no movement, frozen characters, still photo, motionless, jump cut, sudden movement, walking, talking, distorted faces, blurry, low quality',
        'chain': [
            {
                'duration': 8,
                'pos': 'The camera slowly pans to the left. All characters remain standing in place with only natural subtle movements — gentle breathing, slight shifts in posture, and small head turns as they look around. No big actions, no walking. Smooth continuous camera pan, realistic micro-movements, cinematic lighting.',
                'neg': '',
                'frame_interpolation': False,
                'ltx_variant': '8step',
            },
        ],
        'width': 1280,
        'height': 960,
    },

    {
        'file': '40.73. wejscie_do_karczmy.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.74. wejscie_do_karczmy.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.75. wejscie_do_karczmy.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.51. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.53. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.55. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.57. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.59. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.61. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.63. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.65. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.67. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.69. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.71. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.73. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.75. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.77. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.79. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.81. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.83. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.85. party.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wyczerpane',
        'model_class': 'wan',
        'neg': 'static, frozen, no movement',
        'chain': [
            {
                'duration': 4,
                'pos': 'Two almost naked women hang nearly limp from the ceiling, their wrists bound and tied above their heads. Their bodies hang heavily with little movement, only slight natural swaying. Heads tilted down, exhausted and passive posture. Dim dramatic lighting, 4 seconds.',
                'neg': 'standing, strong movement, struggling, smiling, extra people, fully clothed, hands free, blurry, deformed limbs, bad anatomy, low quality',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '50.87. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.89. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.91. party.mp4',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': 'Soft magical spell sounds, gentle glowing energy whooshes, subtle crystalline chimes, light mystical humming, quiet sparkling particles',
        'ambient_audio_negative_prompt': 'ambient sounds, background noise, room tone, wind, footsteps, continuous atmosphere, music, heavy bass, explosions, screaming, talking in normal language, silence, distorted audio, talking at all, magical formula spoken, ',
    },
    {"break": True},

    {
        'file': '51.51. Healing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '51.51. Healing_51.53. Healing',
        'model_class': 'ltx',
        'neg': 'no healing, wounds increasing, extra people, clothing changes, strong magic remaining at the end, blurry, deformed bodies, artifacts',
        'chain': [
            {
                'duration': 4,
                'pos': 'Soft magical healing light appears and flows over the two wounded women. Their wounds begin to slowly close. Gentle glowing particles and light mist surround them during the motion. Toward the end the magical effect starts to fade slightly.',
                'neg': '',
                'frame_interpolation': False,
                'audio_prompt': 'Soft magical spell sounds, gentle glowing energy whooshes, subtle crystalline chimes, light mystical humming, quiet sparkling particles, soft female voice whispering an arcane formula in a strange fictional language',
                'audio_negative_prompt': 'ambient sounds, background noise, room tone, wind, footsteps, continuous atmosphere, music, heavy bass, explosions, screaming, talking in normal language, silence, distorted audio',
                'ltx_variant': '8step',
            },
        ],
    },

    {
        'file': '51.53. Healing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '51.53. Healing_51.55. Healing',
        'model_class': 'ltx',
        'neg': 'Magical healing light continues over the two women. Wounds keep closing and skin regenerates. Soft glowing particles and light mist are visible during the movement. Toward the end the magical effect gently fades.',
        'chain': [
            {
                'duration': 4,
                'pos': 'Magical healing light continues over the two women. Wounds keep closing and skin regenerates. Soft glowing particles and light mist are visible during the movement. Toward the end the magical effect gently fades.',
                'neg': '',
                'frame_interpolation': False,
                'audio_prompt': 'Soft magical spell sounds, gentle glowing energy whooshes, subtle crystalline chimes, light mystical humming, quiet sparkling particles, soft female voice whispering an arcane formula in a strange fictional language',
                'audio_negative_prompt': 'ambient sounds, background noise, room tone, wind, footsteps, continuous atmosphere, music, heavy bass, explosions, screaming, talking in normal language, silence, distorted audio',
                'ltx_variant': '8step',
            },
        ],
    },

    {
        'file': '51.55. Healing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '51.55. Healing_51.57. Healing',
        'model_class': 'ltx',
        'neg': 'no healing, wounds remaining heavily, extra people, clothing changes, strong magic remaining at the end, blurry, deformed bodies, artifacts',
        'chain': [
            {
                'duration': 4,
                'pos': 'Magical healing light works on both women. Most wounds disappear and skin becomes smoother. Soft glowing particles and light mist visible during the clip. Toward the end the effect starts fading.',
                'neg': '',
                'frame_interpolation': False,
                'audio_prompt': 'Soft magical spell sounds, gentle glowing energy whooshes, subtle crystalline chimes, light mystical humming, quiet sparkling particles, soft female voice whispering an arcane formula in a strange fictional language',
                'audio_negative_prompt': 'ambient sounds, background noise, room tone, wind, footsteps, continuous atmosphere, music, heavy bass, explosions, screaming, talking in normal language, silence, distorted audio',
            },
        ],
    },

    {
        'file': '51.57. Healing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '51.57. Healing_51.59. Healing',
        'model_class': 'ltx',
        'neg': 'wounds remaining, no healing, extra people, clothing changes, strong magic remaining at the end, blurry, deformed bodies, artifacts',
        'chain': [
            {
                'duration': 4,
                'pos': 'Final wounds close and vanish under soft magical light. The women’s skin becomes clean. Gentle glowing particles are visible during the motion and fade toward the end.',
                'neg': '',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '51.59. Healing.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': '51.59. Healing_51.61. Healing',
        'model_class': 'ltx',
        'neg': 'still wounded, naked, strong magic, extra people, deformed bodies, blurry, artifacts, incomplete clothing',
        'chain': [
            {
                'duration': 4,
                'pos': 'Soft magical light and glowing particles gently fade away completely. The two fully healed women become dressed again while magic sparkling dust falls upon their from the ceilling. Clean and calm final moment.',
                'neg': '',
                'frame_interpolation': False,
                'audio_prompt': 'Soft magical spell sounds, gentle glowing energy whooshes, subtle crystalline chimes, light mystical humming, quiet sparkling particles, soft female voice whispering an arcane formula in a strange fictional language',
                'audio_negative_prompt': 'ambient sounds, background noise, room tone, wind, footsteps, continuous atmosphere, music, heavy bass, explosions, screaming, talking in normal language, silence, distorted audio',
            },
        ],
    },

    {
        'file': '51.61. Healing.png',
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
