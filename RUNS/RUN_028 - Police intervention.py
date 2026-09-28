# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_028 - Police intervention.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_028 - Police intervention.yaml"))
# Generated: 2026-09-14 23:54:58
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_028 - Police intervention'

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
        'type': 'scene_break',
        'name': 'INTRO',
    },
    {
        'file': '10.51 intro.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'intro',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 8,
                'pos': 'Camera slowly turns around the house',
                'neg': '',
                'ltx_variant': '8step',
                'frame_interpolation': False,
                'lipsync_audio': 'Clara narrator intro.mp3',
                'lipsync_sync_lips': False,
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'WEZWANIE POLICJI',
    },
    {
        'file': '20.51. Start_1.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wezwanie policji',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Woman looks bored, slowly moving her hand up and down',
                'neg': '',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger_not fulfill duties.mp3',
                'lipsync_sync_lips': False,
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
            },
            {
                'duration': 4,
                'pos': 'The woman waves her hand dismissively.',
                'neg': '',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia slave wife not in the mood.mp3',
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
                'ltx_variant': '20step',
                'lipsync_sync_lips': True,
            },
            {
                'duration': 4,
                'pos': 'Man is rising cell phone to his ear',
                'neg': '',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger calling slave police.mp3',
                'lipsync_sync_lips': False,
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
                'ltx_variant': '20step',
            },
        ],
    },

    {
        'file': '20.53. Start_2.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'PRZYJAZD POLICJI',
    },
    {
        'file': '30.51. Przyjazd_1.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': """Quiet suburban residential neighborhood ambience.
Soft distant traffic from a nearby street, occasional cars passing far away,
light wind moving through trees and gardens, faint birdsong,
and a very distant dog barking once in a while.

Natural outdoor daytime ambience. No speech is present. No music is present.""",
        'ambient_audio_negative_prompt': '',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wejscie do domu',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Policewomen turning back to the door',
                'neg': '',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '30.53. Przyjazd_2.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'pukanie do drzwi',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Policewoman approaching door. Blond policewoman is knocking to the door several times looking directly into house thgrough glass door. ',
                'neg': 'turning back, moving away from door, look at camera show face',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
            },
        ],
    },

    {
        'file': '30.54. przyjazd 4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'otwieranie drzwi',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Blond women is opening the door. She grabs a handle and gently push the door ',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
            },
        ],
    },

    {"break": True},

    {
        'file': '30.55. wchodzenie po schodach.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wchodza po schodach',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': "Smooth tracking shot, camera follows the subject steadily, keeping consistent framing and distance as they move. Camera motion is fluid and matches the subject's pace exactly. Only persons visible on screen, no other persons. Policewomen walk up the stairs with a determined stride.",
                'neg': 'camera lag, subject leaving frame, jerky camera movement, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica police woman lets go.mp3',
                'lipsync_sync_lips': False,
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
                'audio_prompt': """Women in thin high-heeled stiletto shoes walks up a staircase.
Each step makes a consistent sharp, hard heel click on stone stairs.
The footsteps have a natural spacious reverberation in a large empty mansion hall.
Quiet indoor room ambience. No speech is present. No music is present.""",
                'audio_negative_prompt': 'music, melody, song, singing, vocals, score, soundtrack, beat, rhythm bed, instrumental backing, tinny, thin, harsh, clipped, distorted, low bitrate, crackle, static noise, vinyl crackle, white noise, hiss, popping sounds',
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'INTERWENCJA W SYPIALNI',
    },
    {
        'file': '40.01 oczekiwanie.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'pojawienie sie meza',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Man is appearing on scene',
                'neg': '',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger husband dont want to listen.mp3',
                'lipsync_sync_lips': False,
            },
        ],
    },

    {
        'file': '40.03 mężczyzna wchodzi.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'pojawienie sie policjantek',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Policewomen walking steadily into room',
                'neg': '',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger husband listen to slave police.mp3',
                'lipsync_sync_lips': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {
        'file': '40.05 policjantki wchodza.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zona spoglada na policjantki',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Redhead woman has scared face ane is loooking striaght at camera',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger husband they came to you.mp3',
                'lipsync_sync_lips': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {
        'file': '40.07 strach w oczach.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zona spoglada na policjantki_kopia',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Redhead woman turns head towards right edge of screen with smooth move. Static painting on wall',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving, moving paintings',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {
        'file': '40.09 kobieta spoglada na policjantki.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'policjantki ida w strone meza',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Policewomen turns towards man and start moving towards him',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '40.11 Lets go.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Zbieraj sie',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Redhead woman on bed is hiding face in hand, Policewomen sligthly move toward bed',
                'neg': 'moving background, Vibrating walls, unsteady enviroment',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica police woman you come with us.mp3',
                'lipsync_sync_lips': False,
            },
            {
                'duration': 5,
                'pos': """Camera slowly zooms in on one redhead woman in the scene, smoothly pushing closer while keeping them centered and in focus. The subject's face and identity remain fully consistent throughout the motion.
Redhead woman on bed is hiding face in hand, Policewomen stands still, A red-haired woman on the bed slowly pushes herself up with her hands.""",
                'neg': 'camera shake, jerky zoom, subject leaving frame, changing facial features, identity drift, morphing face, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman dragged across the floor.mp3',
                'lipsync_sync_lips': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {
        'file': '40.12. wstawaj.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '40.13. mezu nie.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'mezu nie',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'A woman extends her hand in front of her in a defensive gesture.',
                'neg': '',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife dont take me away.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '40.15 unfortunaely not.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nieuzasadnione wezwanie',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 7,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Policewoman standing still, redhead woman in background slowly moving from bed, she is in black satin nightgown',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policwoman nieuzasadnione wezwanie.mp3',
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'WYPROWADZENIE',
    },
    {
        'file': '40.51. z sypialni.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wyprowadzenie z sypialni',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Women is slowly goes to the camera, camera is still',
                'neg': '',
                'ltx_variant': '8step',
                'frame_interpolation': False,
                'audio_prompt': 'slow tired footsteps on carpet floor, heavy labored walking, weight settling sounds, wood creak as sitting on log, body weight on wood, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, running, fast footsteps, bird sounds, wind loop, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
    },

    {"break": True},

    {
        'file': '40.53. woman in police car.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'podroz',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Cars drives away',
                'neg': '',
                'ltx_variant': '8step',
                'frame_interpolation': False,
                'audio_prompt': """Quiet suburban residential neighborhood ambience.
Soft distant traffic from a nearby street, occasional cars passing far away,
light wind moving through trees and gardens, faint birdsong,
and a very distant dog barking once in a while.

Natural outdoor daytime ambience. No speech is present. No music is present.""",
                'audio_negative_prompt': """music, song, melody, score, soundtrack, singing, vocals,
speech, voices, conversation, shouting, crowd,
close traffic, loud engines, sirens, construction,
close dog barking, footsteps, distorted, clipped, low bitrate""",
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'KOMISARIAT',
    },
    {
        'file': '49.51. wskazanie winy.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': """Soft, quiet mechanical office room tone.
Low air-conditioning hum, faint computer fan noise,
occasional page turns, paper handling, light keyboard taps,
gentle chair movement, and sparse distant footsteps.

Only non-vocal environmental sounds.""",
        'ambient_audio_negative_prompt': 'human voices, music, singing, radio, television',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wskazanie winy',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Camera slowly zoom in on policewoman face on right part of scene. Police women is looking at right part of screen, there is no person in backgrounc woman is in the same uniform. Only persons visivle on screen no other persons',
                'neg': 'Policewoman moving away turning back tu camera',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Camera is still and the policewoman is looking at the down left side of screen only breathing',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman you will be punished.mp3',
                'ltx_variant': '20step',
            },
        ],
    },

    {"break": True},

    {
        'file': '49.61. nie unikniesz.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'odpowiedz skazanej',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Camera slowly zoom in on redhead woman face on left part of scene. Redhead woman is looking at right upper part of screen.',
                'neg': 'Policewoman moving away turning back tu camera',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. The Redhead woman is looking at right up part of sreen with scared face.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife not my fault.mp3',
                'ltx_variant': '20step',
            },
        ],
    },

    {"break": True},

    {
        'file': '49.71 idziemy na dol.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'na miejsce kary',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Only persons visible on screen, no other persons. Redhead woman and touching her poicewoman on foreground slowly approach the camera. Redhead woman has hand tied behind her back. A female police officer is leading a red-haired woman the whole time, holding her by the hand. Policewomen on background standing still',
                'neg': 'camera lag, subject leaving frame, jerky camera movement, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'audio_prompt': """Redhead woman and touching her poicewoman walks on wooden floor.
Each step makes a consistent sharp, hard heel click on stone stairs.
The footsteps have a natural spacious reverberation in a large empty mansion hall.
Quiet indoor room ambience. No speech is present. No music is present. No run. Only footstep, no other sounds no ambient.""",
                'audio_negative_prompt': 'music, melody, song, singing, vocals, score, soundtrack, beat, rhythm bed, instrumental backing, tinny, thin, harsh, clipped, distorted, low bitrate, crackle, static noise, vinyl crackle, white noise, hiss, popping sounds',
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'PODZIEMIA I KARA',
    },
    {
        'file': '50.41. turning back.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': """Quiet dark dungeon cell ambience.
Cold damp stone walls, distant water drips echoing through the corridor,
a low draft of wind, occasional faint chain rattles,
and subtle iron bars creaking in the distance.

Deep, natural stone reverberation in an old underground prison.
No voices, no speech, no whispers, no music.""",
        'ambient_audio_negative_prompt': """music, soundtrack, score, melody, singing, vocals,
speech, voices, conversation, whispering, screaming, laughing,
modern machinery, vehicles, city traffic, electronic beeps,
loud impacts, distorted audio, clipped audio, low bitrate""",
    },
    {
        'type': 'multichain',
        'chain_prefix': 'turning back',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': "The woman standing against the wall looks at the policewoman in terror. She doesn't move only breath heavily. Policewoman looks at papersheet she is holding in left hand",
                'neg': 'hands down untie woman at wall',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica_policewoman 30strokes.mp3',
            },
            {
                'duration': 6,
                'pos': '1-2s. Woman at wall is standing still. 3-6s Woman at wall is slowly turning back. As the woman turns around, she does not break the bonds on her wrists. An iron ring attached to the wall rotates.',
                'neg': 'light changes, different colorgrade',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica police woman turn back.mp3',
            },
        ],
    },

    {
        'file': '50.43. tylem 1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'start kary',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons.
Cinematic 6-second shot, realistic live-action, one continuous take.

A policewoman in uniform stands in the foreground, holding a sheet of paper in her right hand and a thin cane in the same right hand. A second adult woman stands motionless against the wall in the background, breathing heavily, chest rising and falling, not moving her feet.

Action timeline:
0-2s: the policewoman looks down at the paper, then lets the sheet fall from her right hand to the floor.
2-4s: with her now empty right hand she takes the cane and transfers it into her left hand.
4-6s: she holds the cane in her left hand and stands still. The woman against the wall stays frozen in place, only breathing.

Locked camera, medium shot, stable framing, no cut, no extra people, no extra objects appearing, natural indoor lighting.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '50.43. tylem 2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'start kary 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Policewoman raises head and looks at camera.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '50.51. tylem 3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'dress is falling down',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman dress is smoothly falling down on the ground and dissaperaing from the scene',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman you will be naked.mp3',
            },
        ],
    },

    {
        'file': '50.53. tylem 4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '50.55. tylem 5.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Whipping 1',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Dynamic 5-second video: A police woman on the right aggressively and repeatedly whipping with thin cane using one hand a naked woman buttocks tied to a wall in the center. Multiple fast, powerful whip strikes hitting her buttocks and thighs, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.',
                'neg': 'hitting with pad, static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'audio_prompt': 'leather whip whoosh and crack, sharp impact sound, female vocal reaction pain cry, body impact foley',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
            },
            {
                'duration': 5,
                'pos': "Dynamic 5-second video: A police woman on the right aggressively and repeatedly whipping with thin cane using one hand a naked woman buttocks tied to a wall in the center. Multiple fast, powerful strikes hitting directly red haired woman's buttocks, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.",
                'neg': 'hitting with pad, static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'audio_prompt': 'leather whip whoosh and crack, sharp impact sound, female vocal reaction pain cry, body impact foley',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        'width': 2112,
        'height': 1152,
    },

    {
        'file': '50.57. tylem 6.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Whipping 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': "Dynamic 5-second video: A police woman on the right aggressively and repeatedly whipping with thin cane using right hand a naked woman buttocks tied to a wall in the center. Multiple fast, powerful strikes hitting directly red haired woman's buttocks, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact.",
                'neg': 'hitting with pad, hitting with right hand, static scene, slow motion, few strikes, single whip hit, blurry motion, deformed body, bad anatomy, low quality, artifacts, text, watermark, censored, calm scene, no movement, smiling, peaceful, static camera, weak hits',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'audio_prompt': 'leather whip whoosh and crack, sharp impact sound, female vocal reaction pain cry, body impact foley',
                'audio_negative_prompt': 'music, melody, ambient drone, echo, reverb, sustained atmosphere, continuous background noise, low quality, distortion',
            },
        ],
        'width': 1472,
        'height': 832,
    },

    {
        'file': '50.59. tylem 7.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Standing still',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. The red-haired woman is racked with shivers and do not turns back her head, the policewoman stands calmly and looks at the man with a blank expression, and the man barely moves.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving, redhead woman turns back',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica_policewoman should I whip her more.mp3',
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
            {
                'duration': 3,
                'pos': 'The red-haired woman is racked with shivers facing the wall, the policewoman stands calmly and looks at the man, and the man barely moves.',
                'neg': 'red woman turning towards camera, moving walls',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger_husband she deserves more.mp3',
                'lipsync_sync_lips': False,
            },
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons.
3-second video: A police woman on the right hits with thin cane in right hand a naked woman buttocks tied to a wall in the center. One fast, stroke hitting directly red haired woman's buttocks, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact. Police woman while hitting is standing still only right arm and right hand dynamically moves.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'frame_interpolation': False,
                'ltx_variant': '20step',
            },
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons.
3-second video: A police woman on the right hits with thin cane in right hand a naked woman buttocks tied to a wall in the center. One fast, stroke hitting directly red haired woman's buttocks, visible red welts, the bound woman flinching, jerking and writhing in pain with each impact. Police woman while hitting is standing still only right arm and right hand dynamically moves.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'frame_interpolation': False,
                'ltx_variant': '20step',
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {
        'file': '50.61. tylem 8.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Na gorę',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': '6-second video: 1–3s: A female police officer slowly approaches a man while looking at him. 4–6s: She stops in front of him and gestures for him to come over by raising hands and pointing up, extending her right hand in an inviting manner.',
                'neg': 'Shake hands, going backwards',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman go upstairs.mp3',
            },
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visible on screen, no other persons.  Man and woman are leaving the scene trhough left edge of scene.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'frame_interpolation': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {
        'file': '50.63. tylem 9.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'samotna',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. The red-haired woman is racked with shivers, ',
                'neg': """Waving walls, another person on scene, turning back, look at camera, moving wooden structure, lowering hands
camera pan, camera tilt, zoom, dolly movement, handheld camera shake,
rack focus, focus pull, depth of field shift,
new characters, additional people, someone entering or exiting the scene,
moving background, shifting walls, furniture moving""",
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'ltx_model': 'ltx-2.3-22b-dev-UD-Q5_K_M.gguf',
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'NAUKA DLA ŻONY',
    },
    {
        'file': '60.01  zoom slave wife.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': """Soft, quiet mechanical office room tone.
Low air-conditioning hum, faint computer fan noise,
occasional page turns, paper handling, light keyboard taps,
gentle chair movement, and sparse distant footsteps.

Only non-vocal environmental sounds.""",
        'ambient_audio_negative_prompt': 'human voices, music, singing, radio, television',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zoom na zone',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': "Camera slowly zooms in on naked woman's face sitting on chair in the scene leaving her on left side of frame, smoothly pushing closer while keeping them in focus. The subject's face and identity remain fully consistent throughout the motion. Policewoman and man standing still.",
                'neg': 'camera shake, jerky zoom, subject leaving frame, changing facial features, identity drift, morphing face, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger maz are you comfortable.mp3',
            },
        ],
    },

    {
        'file': '60.02 zoom slave wife.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'żona mówi 1',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 7,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons.

Only the seated redhead on the chair moves.
The policewoman stays frozen in place.

0-2s: the seated redhead turns her face toward the upper corner near the policewoman and looks at that corner of the frame.
2-5s: she breathes heavily, chest rising and falling, face stays in that direction.
5-7s: she reaches back and touches her own buttocks. Face stays in the same direction.

No other people. No extra motion.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving, look at left side of the frame',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia slave wife please let mi stand up.mp3',
                'lipsync_sync_lips': True,
            },
        ],
    },

    {"break": True},

    {
        'file': '60.03  zoom police woman.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'policjantka mowi 1',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman sit like that.mp3',
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {"break": True},

    {
        'file': '60.04 zoom slave wife 2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'żona mówi 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Red head woman bows her head with pain',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia żona oczywiście.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '60.05  zoom police woman.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'policjantka mowi 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman show what to do.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '60.11 na gorze.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'podchodzi i kleka',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. The policewoman walks across the room toward the seated woman and kneels in front of her. The woman on the chair stays seated, breathing, looking at the policewoman with a shy ashamed expression. No one else moves.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '60.13. blow_start.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '60.53.zoom_ubrane.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': """Soft, quiet mechanical office room tone.
Low air-conditioning hum, faint computer fan noise,
occasional page turns, paper handling, light keyboard taps,
gentle chair movement, and sparse distant footsteps.

Only non-vocal environmental sounds.""",
        'ambient_audio_negative_prompt': 'human voices, music, singing, radio, television',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'blow job',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'static locked-off camera shot, camera mounted on a tripod, completely still frame, close-up shot, dark dimly lit police interrogation room, single harsh light source casting sharp shadows, man wearing black suit and white buttoned shirt, penis fully exposed, his hips and lower torso remain stationary and grounded, blond policewoman with fair skin lowers and tilts her head down to reach him, then slides her mouth steadily over the length of the shaft, smooth controlled motion forwards and backwards, sucking sounds, wet squelches, muffled moaning and breathing. Red head woman in background is sitting still and looks embarrassed at man and policewoman with a pained, unsmiling expression',
                'neg': 'camera movement, panning, zooming, camera drift, tracking shot, handheld shake, dolly movement, detached anatomy, floating, disconnected from body, misplaced position, morphing, anatomy shifting position, distorted anatomy, red head woman smiling',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'cfg_pass1': 3,
                'cfg_pass2': 2,
                'loras': [
                    {
                        'name': 'LTX/ltxdeepthroat_v01.safetensors',
                        'strength': 0.5,
                    },
                ],
                'lora_strength': 1,
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 4,
                'pos': 'LTXdeepthroat, static locked-off camera shot, camera mounted on a tripod, completely still frame, close-up shot, dark dimly lit police interrogation room, single harsh light source casting sharp shadows, man wearing black suit and white buttoned shirt, penis fully exposed, his hips and lower torso remain stationary and grounded, blond policewoman with fair skin lowers and tilts her head down to reach him, then slides her mouth steadily over the length of the shaft, smooth controlled motion forwards and backwards, sucking sounds, wet squelches, muffled moaning and breathing. Red head woman in background is sitting still and looks embarrassed at man and policewoman with a pained, unsmiling expression',
                'neg': 'camera movement, panning, zooming, camera drift, tracking shot, handheld shake, dolly movement, detached anatomy, floating, disconnected from body, misplaced position, morphing, anatomy shifting position, distorted anatomy, red head woman smiling',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'cfg_pass1': 3,
                'cfg_pass2': 2,
                'loras': [
                    {
                        'name': 'LTX/ltxdeepthroat_v01.safetensors',
                        'strength': 0.5,
                    },
                ],
                'lora_strength': 1,
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
    },

    {
        'file': '60.55  zoom police woman.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'teraz twoja kolej',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking at penis, barely not move.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman show what you can do.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '60.61.zoom_ubrane.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zona mezowi 1',
        'model_class': 'wan',
        'neg': 'static, frozen, no movement',
        'chain': [
            {
                'duration': 4,
                'pos': "Woman now kneeling down in same background as the first frame, with her breasts positioned around the man's erect penis as he thrusts his penis up and down in a titjob motion sliding it between her breasts. she makes various facial expressions during the video she looks like she is talking and has her eyes wide open with a crazy expression.  same background as the first frame.",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon_Blink_Titjob_I2V_LOW.safetensors',
                'use_lightning': False,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
                'lipsync_audio': 'Natalia slave wife is it good.mp3',
            },
            {
                'duration': 3,
                'pos': """Woman now kneeling between a man's legs and feet with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's penis and moves it up and down its shaft in a steady rhythm, performing the handjob. She goes through facial expressions throughout the video from embarassment to shy to gasping she looks like she is talking. She is not smiling

She looks at the camera throughout the video

Man's feet are seen in the background same background as the first frame.""",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion, smiling woman',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%20-%20Blink_Handjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
    },

    {"break": True},

    {
        'file': '60.63.zoom_ubraneFIX.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zona mezowi 2',
        'model_class': 'wan',
        'neg': 'static, frozen, no movement',
        'chain': [
            {
                'duration': 3,
                'pos': """The video then jumpcuts to the same woman now kneeling between a man's legs with her upper body is bent forward over him, and her face is close to his lap. With one hand, she grasps the man's erect penis and moves it up and down its shaft in a steady rhythm, performing the handjob.  She goes through facial expressions throughout the video from embarassment to shy to gasping.

She looks at the camera throughout the video same background as the first frame.""",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'lora_high': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-HIGH-v1.safetensors',
                'lora_low': 'WAN2.2_LoraSet/WAN-2.2-I2V-HandjobBlowjobCombo-LOW-v1.safetensors',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 4,
                'pos': 'The video then jumpcuts to the same woman giving a blowjob to the same man standing in the same location. Only penis of man is visible. She is kneeling in front of him, looking up as she performs the blowjob. She is holding the man penis with both hands. She looks at the camera the entire time. She shoves the man penis deep in her mouth, sucking intensely with visible effort, saliva dripping, cheeks hollowed. Dynamic oral sex, high detail, explicit, realistic anatomy and size difference. same background as the first frame.',
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'audio_prompt': 'wet mouth sounds, oral suction, saliva dripping, lips sliding, rhythmic sucking and slurping, oral motion foley, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'lora_high': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGOON_Blink_Blowjob_I2V_LOW.safetensors',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 4,
                'pos': "Person in backround on left part of scene is leaving the scene. Woman now receiving a facial from a man's penis she has in mouth. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand standing before her holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. An explosion of thick white cum blasts her face. she looks directly at the camera throughout the video with embarassed face. same background as the first frame.",
                'neg': 'bad anatomy, deformed penis, extra limbs, blurry, low quality, censored, small penis, no saliva, closed mouth, no eye contact, bad hand position, teeth visible, static pose, cartoon, plastic skin, poor connection, weak motion',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
            {
                'duration': 3,
                'pos': "Woman now receiving a facial from a man's penis. She is kneeling on the floor looking up with a open mouth. The cum shoots all over her face. The man's hand holds his erect penis masturbating his penis and shooting the thick white cum directly onto her face, forehead, eyes, cheek and mouth. The thick white cum slowly drips down her face onto her body. same background as the first frame.  She looks with embarassed face.",
                'neg': '',
                'lora_high': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_HIGH.safetensors',
                'lora_low': 'WAN2.2_LoraSet/iGoon%2520-%2520Blink_Facial_I2V_LOW.safetensors',
                'audio_prompt': 'wet splashing sounds, thick liquid impact, fluid spray, viscous liquid dripping and hitting skin, wet surface contact, synchronized with video, crisp, high quality, realistic',
                'audio_negative_prompt': 'music, melody, ambient drone, moaning, voice, sustained atmosphere, continuous background noise, low quality, distortion',
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        'width': 960,
        'height': 512,
    },

    {"break": True},

    {
        'file': '60.71  zoom police woman.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'siadaj na miejscu',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman sit back on the chair.mp3',
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'NOWA KARA',
    },
    {
        'file': '70.51. humilation at police station 1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'rozchyl nogi',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. The woman sitting on the chair slowly and reluctantly spreads her legs. Small hesitant movement only. She stays seated. No other motion.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman show us.mp3',
                'lipsync_sync_lips': False,
            },
        ],
    },

    {
        'file': '70.53. humilation at police station 2_stretched.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zaslania sie',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'LTXNUDES, Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. 0-4s the redhead woman sits with her legs spread and covers her crotch and vagina with both hands. She looks embarassed at policewoman. No panties on redhead woman.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving, panties on redhead woman',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger maz simply didnt shave.mp3',
                'lipsync_sync_lips': False,
                'loras': [
                    {
                        'name': 'LTX/SexGod_Nudity_LTX23_v2_0.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {"break": True},

    {
        'file': '70.55  zoom police woman.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nie zaslaniaj',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman serious vilation.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '70.61. public punishment.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wszystko jasne',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman on chair looks at the man on left side of the screen frightened.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Roger husband wife should be punished.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '70.65  zoom police woman.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nie zaslaniaj_kopia',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move. Eyes of policewoman open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman broke contract part1.MP3',
            },
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move. Eyes of policewoman open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman broke contract part2.MP3',
            },
            {
                'duration': 5,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking down, barely not move. Eyes of policewoman open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman broke contract part3.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '70.71. prepare to leave.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wstaje do wyjscia',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman on chair is standing up. No panties on redhead woman',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving. Panties on redhead woman',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'DOPROWADZENIE',
    },
    {
        'file': '80.51. walk 1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': 'Realistic large city street ambience, continuous traffic noise, cars and buses passing, distant sirens far away, pedestrian footsteps, scattered voices, bicycle bells, air brakes, city rumble, natural outdoor urban soundscape, no music, no narration',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'walk 1',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': """5 second continuous tracking shot, front view. Camera dollies backward at a matching walking pace, keeping both women in frame at all times.

Two women walk toward the camera side by side, shoulder to shoulder, exactly matching pace and stride throughout — never single file, neither one ahead of the other.

The policewoman is on the left, holding a leash connected to the nude redhead on the right. The leash stays taut and visibly connected the entire time.

The redhead's hands are cuffed behind her back; her arms remain still behind her, she does not swing them forward. While walking she looks around, then lowers her head.

Pedestrians pass in the background going the opposite direction. Photorealistic daylight street scene.""",
                'neg': 'single file, one woman ahead of the other, staggered positions, walking in a line, changing distance between them, camera lag, subject leaving frame, jerky camera movement, new characters, additional people, moving background',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia I am humililiated_part1.MP3',
                'lipsync_sync_lips': False,
            },
            {
                'duration': 3,
                'pos': """5 second continuous tracking shot, front view. Camera dollies backward at a matching walking pace, keeping both women in frame at all times.

Two women walk toward the camera side by side, shoulder to shoulder, exactly matching pace and stride throughout — never single file, neither one ahead of the other.

The policewoman is on the left, holding a leash connected to the nude redhead on the right. The leash stays taut and visibly connected the entire time.

The redhead's hands are cuffed behind her back; her arms remain still behind her, she does not swing them forward. While walking she looks around, then lowers her head.

Pedestrians pass in the background going the opposite direction. Photorealistic daylight street scene.""",
                'neg': 'single file, one woman ahead of the other, staggered positions, walking in a line, changing distance between them, camera lag, subject leaving frame, jerky camera movement, new characters, additional people, moving background',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia I am humililiated_part2.MP3',
                'lipsync_sync_lips': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '80.53. walk 2.jpeg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'walk 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': '5 second continuous tracking shot, rear view. Camera follows behind the subjects at a matching walking pace, keeping all subjects in frame at all times. The subjects walk away from the camera side by side, shoulder to shoulder, exactly matching pace and stride throughout - never single file, neither one ahead of the other. Natural walking motion, photorealistic environment, daylight. Leash firmly attached to readhaad woman neck.',
                'neg': 'single file, one woman ahead of the other, staggered positions, walking in a line, changing distance between them, camera lag, subject leaving frame, jerky camera movement, new characters, additional people, moving background',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife How much longer.mp3',
                'lipsync_sync_lips': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '80.61 under the cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'under the cross',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons.
6 seconds, same empty street with a wooden cross. No camera move.

The policewoman and the nude redhead enter from the right edge of the frame and slowly walk across the roadway toward their final positions on the right side of the cross. Slow footsteps only. They stop beside the cross.

No other people appear. No extra motion.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife anything but that.mp3',
                'lipsync_sync_lips': False,
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {
        'file': '80.63 under the cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '80.65 Zoom on cross.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zoom on cross',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': """Smooth tracking shot, camera follows the subject steadily, keeping consistent framing and distance as they move. Camera motion is fluid and matches the subject's pace exactly. Only persons visible on screen, no other persons
5 seconds, empty scene, only the wooden cross. Slow zoom in on the inscription at the top of the cross. No people. No other motion.""",
                'neg': 'camera lag, subject leaving frame, jerky camera movement, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '80.67. krzyż druga strona_zoomx2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'komenda cross',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman spend some time.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '80.69. krzyż druga strona_zoom.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'komenda',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons
4 seconds, slow zoom in on the faces of both women. The redhead covers her face with both hands. The policewoman looks at her with contempt. No other motion.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife umre ze wstydu.mp3',
                'lipsync_sync_lips': False,
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'PRZYTWIERDZANIE',
    },
    {
        'file': '81.51. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
        'ambient_audio_prompt': 'Realistic large city street ambience, continuous traffic noise, cars and buses passing, distant sirens far away, pedestrian footsteps, scattered voices, bicycle bells, air brakes, city rumble, natural outdoor urban soundscape, no music, no narration, no talks',
        'ambient_audio_negative_prompt': 'talks, whispers',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wejscie na pudlo',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. A naked woman slowly and hesitantly steps onto a wooden crate—the base of the cross.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {
        'file': '81.53. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '81.54. Zoom on cross.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'rozloz rece i nogi',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman spread lesg rise arms.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '81.55. Zoom on cross.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'czy to konieczne',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': "Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman frightened look at right part of scene. She doesn't move, heavily breathing.",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife is it necessary.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '81.56. Zoom on cross.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Hurry up',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead to the left side of scene, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman hurry up.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '81.57. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'raising hands',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': """Static locked-off camera. Only two adult women visible.

A naked adult woman beneath a cross opens her arms and widens her stance.
She slowly slides both feet apart along the floor, with both feet flat on
the ground at all times. No lifting, stepping, floating, or hovering.

A policewoman slowly approaches.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving. Lifting, stepping, floating, or hovering.',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'use_lightning': False,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
    },

    {
        'file': '81.59. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '81.61. Zoom on cross .jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wait for tie',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman wait for tie.mp3',
            },
            {
                'duration': 7,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman obedient slave wife.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '81.63. Zoom on cross .png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'must be obedient',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 8,
                'pos': "Woman frightened look straight towards camera. Focus on redhead woman. Redhead woman doesn't move, heavily breathes. Persons in background walking.",
                'neg': 'shifting cross',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife obedient slave wife part1.mp3',
            },
            {
                'duration': 9,
                'pos': "Woman frightened look straight towards camera. Focus on redhead woman. Redhead woman doesn't move, heavily breathes. Persons in background walking.",
                'neg': 'shifting cross',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia wife obedient slave wife part2.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '81.65. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wchodzą robotnicy',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': '5 second continuous shot, static camera. A woman stands beneath a large cross, remaining still in her position throughout. Two male workers enter the frame from the right side and walk into the scene. The first worker, closer to the camera, carries hammer. The second worker, behind him, has both hands completely empty — no tools, nothing held. Both men wear plain work clothes. Photorealistic, natural daylight, cinematic.',
                'neg': 'three or more new people, extra background characters, both workers carrying a toolbox, neither worker carrying a toolbox, toolbox switching hands, camera pan, camera tilt, zoom, dolly movement, handheld camera shake, moving background, shifting walls, furniture moving, blurry, low quality, deformed hands',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '81.67. Zoom on cross.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Tie her to cross',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman carry on.mp3',
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'PUBLICZNA PREZENTACJA',
    },
    {
        'file': '82.51. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'prezentacja na krzyżu',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'A single continuous static wide shot of a woman standing completely motionless in the center of a city street. Pedestrians calmly walk around her in both directions. On the right side of the frame, a small group of three pedestrians notice her, turn their heads toward her, gesture in her direction and quietly exchange surprised looks while they continue walking. Other pedestrians briefly glance at the woman and keep moving. The central woman remains perfectly still and unchanged. Static tripod camera, stable street, buildings, lighting, perspective and background.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, moving background, shifting walls, pavement',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
            {
                'duration': 6,
                'pos': 'A single continuous static wide shot of a woman standing completely motionless in the center of a city street. Pedestrians calmly walk around her in both directions. On the right side of the frame, a small group of three pedestrians notice her, turn their heads toward her, gesture in her direction and quietly exchange surprised looks while they continue walking. Other pedestrians briefly glance at the woman and keep moving. The central woman remains perfectly still and unchanged. Static tripod camera, stable street, buildings, lighting, perspective and background.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, moving background, shifting walls, pavement',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
            {
                'duration': 6,
                'pos': 'A single continuous static wide shot of a woman standing completely motionless in the center of a city street. Pedestrians calmly walk around her in both directions. On the right side of the frame, a small group of three pedestrians notice her, turn their heads toward her, gesture in her direction and quietly exchange surprised looks while they continue walking. Other pedestrians briefly glance at the woman and keep moving. The central woman remains perfectly still and unchanged. Static tripod camera, stable street, buildings, lighting, perspective and background.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, moving background, shifting walls, pavement',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'file': '82.53. Zoom on cross.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'uplyw czasu',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout.
Locked-off wide shot of a woman standing exactly in the center of a city street. She remains perfectly still, maintaining the same pose, identity, clothing, facial expression, body position, scale and location in every shot. A discontinuous time-lapse sequence made of rapid jump cuts: crowds of pedestrians flow around her, then abruptly change between cuts. In one moment the street is crowded, in the next it is nearly empty, then a different dense crowd passes around her. Pedestrians may change completely from cut to cut. The woman in the center never moves and is never replaced. Static tripod camera, identical framing, unchanged street, buildings, perspective and lighting.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, moving background, shifting walls, pavement',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
            {
                'duration': 6,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout.
Locked-off wide shot of a woman bound to a cross standing exactly in the center of a city street. She remains perfectly still, maintaining the same pose, identity, clothing, facial expression, body position, scale and location in every shot. A discontinuous time-lapse sequence made of rapid jump cuts: crowds of pedestrians flow around her, then abruptly change between cuts. In one moment the street is crowded, in the next it is nearly empty, then a different dense crowd passes around her. Pedestrians may change completely from cut to cut. The woman in the center never moves and is never replaced. Static tripod camera, identical framing, unchanged street, buildings, perspective and lighting.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, moving background, shifting walls, pavement',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
            {
                'duration': 6,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout.
Locked-off wide shot of a woman bound to a cross standing exactly in the center of a city street. She remains perfectly still, maintaining the same pose, identity, clothing, facial expression, body position, scale and location in every shot. A discontinuous time-lapse sequence made of rapid jump cuts: crowds of pedestrians flow around her, then abruptly change between cuts. In one moment the street is crowded, in the next it is nearly empty, then a different dense crowd passes around her. Pedestrians may change completely from cut to cut. The woman in the center never moves and is never replaced. Static tripod camera, identical framing, unchanged street, buildings, perspective and lighting.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, moving background, shifting walls, pavement',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'GOLENIE',
    },
    {
        'file': '83.61. Zoom na zone.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Where am i',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': "Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman exhausted look at right part of scene. She doesn't move, heavily breathing, naked breasts.",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving, wooden cross moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '01N. Natalia slave wife Holy crap. Where am I.mp3',
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {"break": True},

    {
        'file': '83.63. zoom na policjantke.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Untied',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking at left side of scene, barely not move. Eyes open. Police stands in place',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '02J Jessica policewoman we untied you.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '83.65. Zoom na zone.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'Take me home',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 5,
                'pos': "Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman exhausted look at right part of scene. She doesn't move, heavily breathing.",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '03N. Natalia slave wife take me home.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '83.67. zoom na policjantke.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'shave with audience',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking at left side of scene, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '04J Jessica policewoman not so fast.mp3',
            },
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only policewoman visible on screen, no other persons. Police woman is steadily looking at left side of scene, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '05J Jessica policewoman nice shave here.mp3',
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {"break": True},

    {
        'file': '83.69. Zoom na zone.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'dont want not here',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': "Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman exhausted look at right part of scene. She doesn't move, heavily breathing.",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '06N. Natalia slave wife dont want to.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '83.71. zoom na policjantke.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'sit down',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 7,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking at left side of scene, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': '07J Jessica policewoman sit down.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '83. 81. shaving_bez_widzow_czeka_na_golenie.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'man apporaching',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons.man apporaching scene',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '83. 83. shaving_men_na_scenie_czeka_na_golenie.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'woman apporaching',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Woman apporaching scene.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '83. 85. shaving_men_women_na_scenie_czeka_na_golenie.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '83.51. Shaving process_part0.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nakladanie 1',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons
A static continuous medium shot. An adult woman slowly begins applying shaving foam
from the spray can in her hand onto her crotch. A small amount of soft white
foam emerges from the nozzle and settles naturally on the skin. Her hand moves slowly
and carefully. Preserve the same person, pose, camera, lighting, background and composition.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '83.53. Shaving process_part1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nakladanie 2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

A static continuous medium shot. An adult woman slowly begins applying shaving foam
from the spray can in her hand onto her crotch. A small amount of soft white
foam emerges from the nozzle and settles naturally on the skin. Her hand moves slowly
and carefully. Preserve the same person, pose, camera, lighting, background and composition.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '83.55. Shaving process_part2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nakladanie 3',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

A static continuous medium shot. An adult woman slowly begins applying shaving foam
from the spray can in her hand onto her crotch. A small amount of soft white
foam emerges from the nozzle and settles naturally on the skin. Her hand moves slowly
and carefully. Preserve the same person, pose, camera, lighting, background and composition.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '83.57. Shaving process_part3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'nakladanie 4',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

A static continuous medium shot. An adult woman slowly begins applying shaving foam
from the spray can in her hand onto her crotch. A small amount of soft white
foam emerges from the nozzle and settles naturally on the skin. Her hand moves slowly
and carefully. Preserve the same person, pose, camera, lighting, background and composition.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '83.59. Shaving process_part4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'upuszczenie pianki',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only the woman is visible on screen, no other persons.

Immediately, right at the very start of the shot with no delay: a red-haired woman opens her left hand and releases a spray foam bottle. She does not reach toward the camera, does not push or extend the bottle forward first — she simply lets go of it from where her hand already is. She does not throw it either. The bottle falls straight down under gravity, drops to the ground and disappears below the bottom edge of the frame. The bottle is pale blue with no labels or markings, and its color, shape and appearance stay exactly the same as it falls.

For the next 2 seconds, after the bottle is gone: she looks around, dazed and disoriented. Nothing else in the scene moves besides her head and eyes. No additional items appear on the wooden box where she is sitting. The towel does not move. The foam on her crotch does not move.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        'width': 960,
        'height': 512,
    },

    {"break": True},

    {
        'file': '83.61. zoom na policjantke.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'start shaving',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman start shaving.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '84.51. golenie_1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'golenie 1',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons
Static, locked-off camera. Focus remains fixed on the main subject throughout.
Only one adult woman is visible in the frame. No other people enter the shot.

The woman slowly moves the same razor from her left to her right across one narrow horizontal strip of shaving foam on the crotch directly below the razor.
The razor stays in gentle, continuous contact with the skin and removes only that one strip of foam in a single controlled shaving stroke. Behind the razor, the selected horizontal strip becomes cleaner, smooth, slightly wet visible skin, while almost all shaving foam above and below
the selected strip remains unchanged. Her hand moves slowly and steadily from left to right.
Preserve the same person, pose, anatomy, hands, camera, lighting, background and composition.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
    },

    {
        'file': '84.53. golenie_2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'golenie_2',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

The woman slowly moves the same razor from right to left, returning it to the left side
of the foam-covered skin area. During this returning movement, the razor is held slightly
above the skin and does not touch the shaving foam. The razor is not shaving.

No shaving foam is removed, displaced, smeared, reduced or changed during the return movement.
All foam coverage, all remaining foam strips and all previously shaved areas remain exactly unchanged.

Only her hand, wrist and razor move. Her body, face, pose, camera, lighting,
background and composition remain completely still.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lf_strength': 1,
            },
        ],
    },

    {
        'file': '84.54. Shaving process_part1a.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'golenie_2a',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

The woman slowly moves the same razor from left to right across the selected horizontal strip
of shaving foam directly beneath the razor. The razor glides gently over the surface of the skin
and removes only the shaving foam from that strip in one controlled shaving stroke.

The skin remains intact, continuous, smooth and unchanged. The razor does not cut, peel, lift,
pull, tear, remove or deform any skin. Only the white shaving foam is cleared away from the
surface, leaving small natural uneven traces of foam on the same unbroken skin surface.

The previously shaved strips remain unchanged. All shaving foam above and below the selected
strip remains unchanged. Only her hand, wrist and razor move. Her body, face, pose, camera,
lighting, background and composition remain completely still.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lf_strength': 1,
            },
        ],
    },

    {
        'file': '84.55. golenie_3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'golenie_3',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

The woman slowly moves the same razor from right to left, returning it to the left side
of the foam-covered skin area. During this returning movement, the razor is held slightly
above the skin and does not touch the shaving foam. The razor is not shaving.

No shaving foam is removed, displaced, smeared, reduced or changed during the return movement.
All foam coverage, all remaining foam strips and all previously shaved areas remain exactly unchanged.

Only her hand, wrist and razor move. Her body, face, pose, camera, lighting,
background and composition remain completely still.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lf_strength': 1,
            },
        ],
    },

    {
        'file': '84.56. golenie_3a.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'golenie_3a',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': """Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons

The woman slowly moves the same razor in one continuous diagonal shaving stroke,
starting at the lower-left side of the selected foam-covered skin area and moving upward
toward the upper-right side at approximately a 45-degree angle. The razor glides gently
over the surface of the crotch and removes only the white shaving foam along one narrow
diagonal path.

The skin remains intact, continuous, smooth and unchanged. The razor does not cut, peel,
lift, pull, tear, remove or deform any skin. Only shaving foam is cleared away from the
surface, leaving small uneven natural traces of foam on the same unbroken skin surface.

All foam outside the selected diagonal path remains unchanged. The previously shaved areas
remain unchanged. Only her hand, wrist and razor move. Her body, face, pose, camera, lighting,
background and composition remain completely still.""",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lf_strength': 1,
            },
        ],
    },

    {
        'file': '84.57. golenie_4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '85.53. Towel_01.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wyciera sie recznikiem',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': """Camera slowly zooms in on one subject in the scene, smoothly pushing closer while keeping them centered and in focus. The subject's face and identity remain fully consistent throughout the motion.

She is already holding a towel at the height of her crotch. She wipes her crotch with the towel using a natural, gentle wiping motion of her hand. Only her hand and the towel move; the rest of her pose and position stay the same.

Her face, identity and features stay fully consistent and sharp throughout the zoom — no distortion, no morphing, no drift in her facial features as the camera moves closer. No other people in frame.""",
                'neg': 'camera shake, jerky zoom, subject leaving frame, changing facial features, identity drift, morphing face, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        'width': 960,
        'height': 512,
    },

    {
        'file': '85.55. Towel_02.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wytarla sie i wstaje',
        'model_class': 'wan',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 4,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visible on screen no other persons. Woman is slowly standing up. No panties, woman is totaly naked. Only keeps towel in hands. Cover the crotch with shy.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'use_lightning': True,
                'workflow': '_I2V_classic_4s1200_nog4gg.json',
            },
        ],
        'width': 960,
        'height': 512,
    },

    {"break": True},

    {
        'file': '85.65. Zoom na zone.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'shaving is finished',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 3,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visible on screen no other persons.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Natalia slave wife ive finished.mp3',
            },
        ],
    },

    {"break": True},

    {
        'file': '85.67. Zoom na policewoman.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'get in the car',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Police woman is steadily looking straight ahead, barely not move. Eyes open.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman get in the car.mp3',
            },
        ],
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'POWRÓT DO DOMU',
    },
    {
        'file': '91.41 wejscie do rezydencji.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'zoom na drzwi',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': "Camera slowly zooms in on one entrance door in the scene, smoothly pushing closer while keeping them centered and in focus. The subject's face and identity remain fully consistent throughout the motion.",
                'neg': 'camera shake, jerky zoom, subject leaving frame, changing facial features, identity drift, morphing face, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
    },

    {"break": True},

    {
        'file': '91.51 samochod wjezdza.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'samochod wjeżdża',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. Car slowly approaches',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {
        'file': '91.53 samochod wjezdza.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '91.61 outro.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'wejście do domu',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': "Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. An exhausted woman shuffles toward the residence's front door. She is wearing black stiletto pumps with very thin high heels",
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {
        'file': '91.63 outro.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '91.67. rozmowa w samochodzie.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'niech wejdzie',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 8,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visible on screen no other persons. The female police officers remain silent; their lips do not move.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'lipsync_audio': 'Jessica policewoman busy day.mp3',
                'lipsync_mode': 'multi',
                'lipsync_multi': [
                    {
                        'audio': 'Jessica policewoman busy day.mp3',
                        'sync_lips': True,
                        'position_index': 1,
                    },
                    {
                        'audio': 'Kasia policewoman absolutely letsgo.mp3',
                        'sync_lips': True,
                        'position_index': 0,
                    },
                ],
            },
        ],
    },

    {"break": True},

    {
        'file': '91.69 outro.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'prezentacja golenia',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': "Camera slowly zooms in on redhead woman's crotch in the scene, smoothly pushing closer while keeping them centered and in focus. The subject's face and identity remain fully consistent throughout the motion.",
                'neg': 'camera shake, jerky zoom, subject leaving frame, changing facial features, identity drift, morphing face, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving',
                'ltx_variant': '20step',
                'frame_interpolation': False,
                'loras': [
                    {
                        'name': 'LTX/LTX-2.3-OmniNFT-RL-Lora_bf16.safetensors',
                        'strength': 1,
                    },
                ],
            },
        ],
        'width': 2048,
        'height': 1152,
    },

    {
        'file': '91.70. outro.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': '91.71 outro.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'multichain',
        'chain_prefix': 'goodbye',
        'model_class': 'ltx',
        'neg': 'blur, noise, watermark, text, low quality, worst quality, deformed',
        'chain': [
            {
                'duration': 6,
                'pos': 'Static, locked-off camera. Focus fixed on the main subject throughout. Only persons visivle on screen no other persons. An exhausted woman shuffles up the stairs; her head is bowed, and she does not turn toward the camera.',
                'neg': 'camera pan, camera tilt, zoom, dolly movement, handheld camera shake, rack focus, focus pull, depth of field shift, new characters, additional people, someone entering or exiting the scene, moving background, shifting walls, furniture moving. Turning back visible redhair woman face',
                'ltx_variant': '20step',
                'frame_interpolation': False,
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
