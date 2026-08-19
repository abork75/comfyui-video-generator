# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_005 - SamanthaNothing.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_005 - SamanthaNothing.yaml"))
# Generated: 2026-08-17 19:47:03
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'E:\\FILMY\\RUN_005 - NothingGonnaStopMeNow'

FORCE_RESOLUTION = (
    624,
    416,
)
DEFAULT_RESOLUTION = (
    624,
    416,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 20
DEFAULT_CFG            = 5
DEFAULT_DURATION       = 4
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
CONFIG_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflow_configs\\wan_i2v_config.yaml'
WORKFLOWS_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflows'
COMFYUI_OUTPUT_FOLDER = 'D:\\ComfyUI\\output\\video'
API_URL = 'http://127.0.0.1:8189'

USE_TEST_FLOW = False

# ============================================================
# FLOW
# ============================================================

FLOW_FULL = [
    {
        'file': '02.03 start.png',
        'backend': 'local',
        'duration': 1.2,
        'pos': 'Smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '02.05 start.png',
        'backend': 'local',
        'duration': 4,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '03.03 jacht.png',
        'backend': 'local',
        'duration': 2,
        'pos': "Woman's close-up face with white sunglasses and cherry fades out via smooth dissolve. In her place, a yacht appears with group of topless women on deck, sunny sea, boat moving forward. Retro 80s vibe, crossfade transition, cinematic, 3 sec.",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.05 jacht.png',
        'backend': 'local',
        'duration': 4,
        'pos': 'A group of vibrant young women on a luxurious yacht at sea, joyfully waving to the camera with infectious enthusiasm.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.07 jacht.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '04.05 jacht.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Speedboat with woman driving moves across frame from left to right. Camera smoothly pans right, boat glides forward and slowly exits frame until only the stern remains visible. Sunny day, blue water, bikini woman at helm, cinematic tracking shot, 4 sec.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '04.07 jacht.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '05.05 salon.png',
        'backend': 'local',
        'duration': 6,
        'pos': 'Blonde woman in white robe sits thoughtfully on sofa in sunny bedroom. She stands, camera pulls back slowly, drops robe to reveal full nudity, then sits back in same exact pose — hands near face, side view. Elegant sensual reveal, natural window light, cinematic dolly out, 6 sec.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '05.07 salon.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '06.05 salon.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Close-up profile of nude blonde woman by window, dreamy expression. Camera slowly pulls back as she stands and walks toward the large sunny window, ending in medium shot of her full nude figure in profile against bright backlight. Sensual, warm morning light, smooth cinematic dolly out, 4 sec.',
    },
    {
        'file': '06.07 salon.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '07.05 salon.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Close-up side profile of blonde woman fades out slowly. Simultaneously, nude blonde woman standing back to window fades in – same lighting and room. Overlapping faces/bodies during 2-second dreamy cross-dissolve transition, warm backlight, cinematic, 2 sec.',
    },
    {
        'file': '07.07 salon.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.05 samochod.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Woman strides confidently toward camera, two shopping bags in hands, white dress over right shoulder, 3 sec.',
    },
    {
        'file': '08.07 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.09 samochod.png',
        'backend': 'local',
        'duration': 3.1,
        'pos': '3.1s 90s VHS: fully nude blonde woman in white high-heels only, energetically climbs over door into dark Alfa Romeo convertible – one leg on sill, swings in, slides to seat, slams door hard, low side camera, grainy analog, sunny day, dynamic motion.',
    },
    {
        'file': '08.11 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.31 samochod.png',
        'backend': 'local',
        'duration': 2,
        'pos': '2s aerial pull-back: vintage open-top convertible sports car racing forward on empty rural road, camera starts tight above/behind driver then quickly pulls backward revealing full car and road, blonde woman driving, 1980s retro vibe, sunny day, windblown hair, motion blur, film grain, cinematic dynamic shot',
    },
    {
        'file': '08.33 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.35 samochod.png',
        'backend': 'local',
        'duration': 0.5,
        'pos': '0.5s 90s VHS: fully nude blonde woman drives a car',
    },
    {
        'file': '08.37 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.39 samochod.png',
        'backend': 'local',
        'duration': 2.1,
        'pos': '2.1s side view: classic open-top convertible racing forward on country road, blonde woman driver with wind in hair, mouth open singing/talking passionately, eyes forward, fast blurred dynamic background, 1980s retro style, sunny day, motion blur, film grain, energetic cinematic shot',
    },
    {
        'file': '08.41 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.43 samochod.png',
        'backend': 'local',
        'duration': 2.1,
        'pos': '2.1s dynamic follow shot: black classic Alfa Romeo Spider cabriolet racing fast on mountain coastal road, camera tracks right behind the car at same speed, blonde woman driving with hair flying in wind, extremely blurred rushing background – hills, road, guardrail streaking, 80s retro feel, sunny day, strong motion blur, film grain, high-energy cinematic',
    },
    {
        'file': '08.45 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '08.57 samochod.png',
        'backend': 'local',
        'duration': 4.5,
        'pos': '4.5s side view: classic open-top convertible racing forward on country road, blonde woman driver with wind in hair, mouth open singing/talking passionately, eyes forward, fast blurred dynamic background, 1980s retro style, sunny day, motion blur, film grain, energetic cinematic shot',
    },
    {
        'file': '08.59 samochod.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '09.05 samolot.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Female pilot in cockpit transfers hand from dashboard to control yoke, firm grip, close-up on hands and arms, 2 sec.',
    },
    {
        'file': '09.07 samolot.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '10.05 samolot.png',
        'backend': 'local',
        'duration': 4,
        'pos': 'Girl in close-up raises right arm then left arm, crosses both arms over her chest, then gives a huge radiant smile to camera. Joyful expression, smooth movement, 4 sec.',
    },
    {
        'file': '10.07 samolot.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '11.05 samolot.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Girl in pilot seat faces camera with big smile. She slowly turns around to face forward (back to camera), smooth motion, cockpit view, 3 sec.',
    },
    {
        'file': '11.07 samolot.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '12.05 rower.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Girl bikes from left to right past camera, smiling at lens. Camera pans right smoothly to follow her, side view tracking shot, fast blurred background, 3 sec.',
    },
    {
        'file': '12.07 rower.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Girl bikes from left to right past camera, smiling at lens. Camera pans right smoothly to follow her, side view tracking shot, fast blurred background, 3 sec.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '12.09 rower.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '13.05 taniec.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Woman and man dancing: right hands at waist, left arms raised high. They rotate together half-turn (180°) around their center. Close embrace, elegant spin, vintage style, medium shot, 2 sec.',
    },
    {
        'file': '13.07 taniec.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '14.05 idzie.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Blonde woman walks through city street. She turns to camera, smiles and points finger straight at lens. Side-tracking camera follows her, fast moving blurred background, dynamic sunny scene, 3 sec.',
    },
    {
        'file': '14.07 idzie.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '15.05 ladowanie.png',
        'backend': 'local',
        'duration': 5,
        'pos': 'Woman exits airplane with dancing steps down stairs, walks forward. Smooth tracking shot, playful rhythmic walk, sunny airport, 5 sec.',
    },
    {
        'file': '15.07 ladowanie.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '15.51 basen.png',
        'backend': 'local',
        'duration': 1,
        'pos': 'Smooth crossfade transition between two completely different images, 3-5 seconds, first image slowly fades out while the second image simultaneously fades in, perfect dissolve effect, no abrupt cut, gradual opacity change, cinematic and elegant fade, natural blending during transition, maintain consistent lighting mood if possible, high quality, no artifacts, no distortion, no motion unless slight subtle camera drift, clean professional transition --motion 2 --ar 16:9. Woman is totaly naked.',
    },
    {
        'file': '15.53 basen.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '15.55 basen.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '16.05 idzie 2.png',
        'backend': 'local',
        'duration': 2.1,
        'pos': 'Blonde woman fully naked walks through city street. She turns to camera, smiles and points finger straight at lens. Side-tracking camera follows her, fast moving blurred background, dynamic sunny scene, 2.1 sec.',
    },
    {
        'file': '16.07 idzie 2.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '17.05 molo 1.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Woman walking on a pier, camera smoothly follows from behind at walking pace, sunny day, 2 sec.',
    },
    {
        'file': '17.07 molo 1.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '18.05 idzie 3.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Blonde woman walks through city street. She turns to camera, smiles and points finger straight at lens. Side-tracking camera follows her, fast moving blurred background, dynamic sunny scene, 3 sec',
    },
    {
        'file': '18.07 idzie 3.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '19.05 molo 2.png',
        'backend': 'local',
        'duration': 1,
        'pos': 'Woman walking on a pier, camera smoothly follows , sunny day, 2 sec.',
    },
    {
        'file': '19.07 molo 2.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '20.05 idzie 4.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Blonde woman walks through city street. She turns to camera, smiles and points finger straight at lens. Side-tracking camera follows her, fast moving blurred background, dynamic sunny scene, 3 sec',
    },
    {
        'file': '20.07 idzie 4.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '21.05 plynie zblizenie.png',
        'backend': 'local',
        'duration': 8.1,
        'pos': """Exact starting frame: blonde woman driving speedboat, hands on wheel, excited expression.
8-second locked-to-boat close-up on her face and upper body. Subtle handheld camera micro-shakes, tiny sways and breathing drifts for natural dynamism. Speedboat moving forward, wind in hair, sunny water background, 8 sec.""",
    },
    {
        'file': '21.07 plynie zblizenie.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '22.05 plynie oddalenie.jpg',
        'backend': 'local',
        'duration': 7,
        'pos': 'Fast 7s forward-facing boat-mounted stabilized shot, only bow + water in frame, extreme horizontal water streak blur rushing past at high speed, vintage VHS, heavy motion blur on ripples, analog grain & tracking, no boat interior or people visible, pure speed sensation through water texture',
    },
    {
        'file': '22.07 plynie oddalenie.jpg',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '23.01 lodz poklad.png',
        'backend': 'local',
        'duration': 3,
        'pos': """3-second vintage 1990s VHS-style clip, grainy analog video, slight chromatic aberration, tracking lines, dated home video aesthetic.
Stabilized low-angle camera framing a beautiful woman lying on her back on the white deck of a classic speedboat (red and blue racing stripes visible). She is nude / topless, natural daylight, calm blue water in soft background bokeh.
Action sequence (slow and cinematic):
0-1 sec: relaxed pose, lying flat, wearing sunglasses, head tilted slightly back
1-2 sec: slowly removes sunglasses with one hand, sliding them up and to the side
2-3 sec: still lying down, gently lifts head ~10 cm off the deck, looks directly into camera with calm/intense gaze, subtle smile or neutral expression, hair lightly moving in breeze
Film grain heavy, warm analog colors, mild motion blur on hand and head movement, no modern sharpening, authentic 90s camcorder feel, 24 fps, 16:9 aspect ratio.""",
    },
    {
        'file': '23.03 lodz poklad.png',
        'backend': 'local',
        'duration': 4,
        'pos': '4s 90s VHS style clip: topless blonde woman lying on stomach on speeding white speedboat deck, red ensign flag waving, water wake spraying. Low side camera. She slowly rolls onto her right side over 3 seconds – smooth body rotation, ends facing camera on side pose, direct gaze, wind in hair. Grainy analog video, tracking lines, warm light, no sharpening.',
    },
    {
        'file': '23.07 lodz poklad.png',
        'backend': 'local',
        'duration': 1,
        'pos': '1s vintage VHS cross-dissolve: start with naked woman lying prone on speeding boat deck with red flag & wake → smooth fade into her standing silhouette on turquoise beach beside yellow umbrella, same woman, sunny 90s home video style, grainy, tracking lines, warm tones, fluid blend, no cut.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '23.09 plaza.png',
        'backend': 'local',
        'duration': 1,
        'pos': '2s 90s VHS cross-dissolve: start with distant wide shot topless woman + yellow umbrella in shallow turquoise sea → smooth fade into close side-profile of the same nude woman walking, umbrella aligned during transition, distant scene vanishes completely by 2s, final 1s full close-up reveal, grainy analog video, hazy sunny look.',
    },
    {
        'file': '23.11 plaza.png',
        'backend': 'local',
        'duration': 1.1,
        'pos': 'Woman walking freely',
    },
    {
        'file': '23.13 plaza.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'Woman walking freely',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '23.15 plaza.png',
        'backend': 'local',
        'duration': 1,
        'pos': 'Woman walking freely',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '23.17 plaza.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '23.19 plaza.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Woman walking freely',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '23.21 plaza.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '23.23 plaza.png',
        'backend': 'local',
        'duration': 2.5,
        'pos': 'Woman walking freely towards camera',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '23.25 plaza.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '23.27 plaza.png',
        'backend': 'local',
        'duration': 3.5,
        'pos': 'Woman is laying on the ground',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '23.29 plaza.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '24.05 konie.png',
        'backend': 'local',
        'duration': 1,
        'pos': '1s 90s VHS cross-dissolve: start with close-up galloping pinto & chestnut horses splashing in shallow sea → smooth fade into topless blonde woman riding white horse bareback in same surf, nude, reins in hand, waves around legs, grainy analog video preserved in transition.',
        'neg': 'sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '24.07 konie.png',
        'backend': 'local',
        'duration': 1.1,
        'pos': 'Woman is riding a horse, moving up and down',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '24.09 konie.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'Woman is riding a horse, moving up and down',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '25.05 basen.png',
        'backend': 'local',
        'duration': 2,
        'pos': '2s 90s VHS: nude blonde woman at infinity pool edge drops white robe to reveal full naked body, immediately jumps in, sunlit turquoise water, grainy analog video, tracking lines, warm light.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '25.07 basen.png',
        'backend': 'local',
        'duration': 3,
        'pos': '2s 90s VHS: fully nude woman dives cleanly into turquoise infinity pool from edge, body vanishes under water after small splash, only swirling ripples and bubbles left on surface, grainy analog video, sunny haze, tracking lines.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '25.09 basen.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'Woman is riding a horse, moving up and down',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '25.11 basen.png',
        'backend': 'local',
        'duration': 2,
        'pos': '2s 90s VHS underwater: nude blonde woman floats in turquoise pool, holds retro microphone to mouth, eyes dramatic, wildly waves arms like conducting, kicks legs energetically, hair floating, bubbles rising, grainy analog video, sunny caustics, playful vibe. She is nude from begining to the end of film.',
        'neg': 'low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '25.13 basen.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '25.15 basen.png',
        'backend': 'local',
        'duration': 3,
        'pos': """3-second vintage 1990s VHS clip, grainy analog video, slight chromatic aberration, tracking lines, warm sunny daylight, authentic camcorder feel, no modern sharpening, 24 fps, 16:9.
A fully nude blonde woman in her 30s stands in bright turquoise shallow infinity pool water up to her thighs, facing camera directly, arms relaxed at sides.
Action – explosive upward launch:
0.0–0.5 sec: she bends knees deeply, then powerfully jumps straight up with force, body fully extended vertically
0.5–2.0 sec: she rockets upward, breasts bouncing and waving heavily from the momentum, head quickly rises and disappears above the top frame edge, long hair trailing upward, arms start moving behind her head mid-air
2.0–3.0 sec: she reaches peak height (only lower body and waving breasts still visible in frame), arms now fully behind head in arched pose, body beginning slow descent, sun glints on wet skin, water droplets flying
Static low-angle camera from water level, framing centered on her torso and head (head exits frame naturally), heavy film grain, nostalgic sunny pool video aesthetic.""",
        'neg': '',
    },
    {
        'file': '25.17 basen.png',
        'backend': 'local',
        'duration': 3,
        'pos': """3-second vintage 1990s VHS clip, grainy analog video, slight chromatic aberration, tracking lines, warm sunny daylight, authentic camcorder feel, no modern sharpening, 24 fps, 16:9.
Continuation – same fully nude blonde woman in mid-air descent into bright turquoise infinity pool, arms locked behind her head, body arched backward gracefully.
Action – slow, cinematic fall and emergence:
0.0–1.2 sec: she falls downward in slow-motion feel, arms still behind head, breasts gently swaying, long hair floating upward relative to descent, expression relaxed/ecstatic
1.2–1.8 sec: her mouth and chin touch the water surface first, lips part slightly as she begins submerging, small splash around face, water rises to cover mouth and nose
1.8–3.0 sec: she fully submerges face-first up to eyes/forehead for a split second, then powerfully pushes back up with arms spreading wide outward in dramatic V-shape, emerging from water with hair slicked back, water streaming down face and breasts, eyes open, mouth slightly open catching breath, triumphant/pleasured expression
Static low-angle camera from water level, centered framing (head re-enters frame naturally), sun caustics and water ripples intensify on re-emergence, heavy analog grain and color bleed throughout, nostalgic 90s home video style.""",
        'neg': '',
    },
    {
        'file': '25.19 basen.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '26.05 idzie 3.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'Blonde woman walks through city street. She approaches table and finger person at the table. Side-tracking camera follows her, fast moving blurred background, dynamic sunny scene, 2 sec.',
        'neg': '',
    },
    {
        'file': '26.07 idzie 3.png',
        'backend': 'local',
        'duration': 1,
        'pos': "Blonde woman points at man's nose",
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '26.09 idzie 3.png',
        'backend': 'local',
        'duration': 0.5,
        'pos': 'Smooth move backwards',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '26.11 idzie 3.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '26.21 idzie 3.png',
        'backend': 'local',
        'duration': 3.5,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '26.23 idzie 3.png',
        'backend': 'local',
        'duration': 3.5,
        'pos': 'Woman is walking. Side-tracking camera follows her, fast moving blurred background, dynamic sunny scene, 2 sec.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '26.25 idzie 3.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '27.05 lodz rybacka.png',
        'backend': 'local',
        'duration': 6,
        'pos': '4s 90s VHS: blonde woman in striped top and beige hat stands on speedboat deck, smiles warmly at camera, right hand on hip then waves cheerfully, left hand on blue railing, sunny sea background, grainy analog video, tracking lines, happy relaxed vibe.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '27.07 lodz rybacka.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '28.05 lodz rybacka.png',
        'backend': 'local',
        'duration': 3,
        'pos': '4s 90s VHS: blonde woman smooth transition',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '28.07 lodz rybacka.png',
        'backend': 'local',
        'duration': 3,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '28.09 lodz rybacka.png',
        'backend': 'local',
        'duration': 0,
        'pos': '',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '29.05 limo1.png',
        'backend': 'local',
        'duration': 2.5,
        'pos': 'Woman talks',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '29.07 limo1.png',
        'backend': 'local',
        'duration': 2.5,
        'pos': 'Woman talks',
        'neg': '',
    },
    {
        'file': '29.09 limo1.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {"break": True},

    {
        'file': '30.05 limo2.png',
    },
    {
        "chain": [
            {
                'duration': 4.1,
                'pos': 'Woman is waving to the crowd and smiling',
            },
        ],
        "chain_prefix": 'waving',
        'backend': 'local',
        'neg': 'static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality',
    },

    {"break": True},

    {
        'file': '31.05 final zblizenie.png',
        'backend': 'local',
        'duration': 3,
        'pos': 'Woman is waving to the crowd and smiling',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '31.07 final zblizenie.png',
        'backend': 'local',
        'duration': 3,
        'pos': "3-second cinematic scene: Start with extreme close-up on beautiful woman's face on a boat, then camera slowly pulls back to reveal her full body silhouette sitting on the edge.slow-motion, intimate mood, ultra-realistic, shallow DOF",
        'neg': '',
    },
    {
        'file': '32.05 finalna scena.png',
        'backend': 'local',
        'pos': """5-second sensual slow-motion scene: beautiful woman in wet white shirt sits on small boat at sunset.
She slowly caresses her breasts → slides hands down stomach → glides over thighs → finally slips both hands intimately between her pressed-together thighs.
Golden hour, cinematic, intimate close-ups, erotic mood, ultra-realistic, shallow DOF""",
        'duration': 5.1,
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '32.07 finalna scena.png',
        'backend': 'local',
        'duration': 0,
        'pos': 'NONE',
        'neg': '',
    },
]

FLOW_TEST = [
    {
        'file': '03.05 jacht.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'A group of vibrant young women on a luxurious yacht at sea, joyfully waving to the camera with infectious enthusiasm.',
        'neg': 'blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement',
    },
    {
        'file': '03.07 jacht.png',
        'backend': 'local',
        'duration': 2,
        'pos': 'PROMPT',
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
