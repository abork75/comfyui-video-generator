# -*- coding: utf-8 -*-
"""
RUN_005: Samantha Fox - Nothing Gonna Stop Me Now
WITH BATCH UPSCALING POSTPROCESSING

Complete workflow:
1. Video generation (batch_transitions)
2. Numbered flow (copy to FLOW_* folder)
3. Full concat (merge all clips)
4. Batch upscale (GAN upscaling with interactive source selection)

Author: abork75
Date: 2026-02-19
"""

# ============================================================
# IMPORTANT: Add parent directory to path (RUNS/ subfolder)
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# Core imports: Config validation and orchestrator
# ============================================================
from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\muszelka_pliki\MKK\praca w postapo\film"

# ============================================================
# FLOW - Select test or full production
# ============================================================

USE_TEST_FLOW = False  # ← Change to False for full production run

FLOW_TEST = [
    # ============================================================
    # SEQUENCE 1: PRZED USC
    # ============================================================
    
     {
        "file": "05.05. ZOOM_1.png",
        "backend": "linux",
        "duration": 2,
        "pos": "Smooth transition",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
  
    {
        "file": "05.09. ZOOM_2.png",
        "backend": "linux",
        "duration": 2,
        "pos": "NONE",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    
]

FLOW_FULL = [  

    # ============================================================
    # SEQUENCE 1: Scena na jachcie
    # ============================================================

    # {
        # "file": "10.47. Empty_street.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": "Man slowly walks in, woman shows in window",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },
  

    # {
        # "file": "10.49. near_building_Queue_2.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": "Smooth transistion - camera zoom in into women in window",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },
  
    # {
        # "file": "10.51. Panienka z okienka.mp4",
        # "backend": "linux",
        # "duration": 5,
        # "pos": "???",
        # "neg": "bra disappearing, clothes morphing, teleporting bra, blurry hands, unnatural motion, blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    {
        "file": "15.51. bedroom_2.png",
        "backend": "linux",
        "duration": 5,
        "pos": "Camera slowly and smoothly zooms in from a medium shot to a close-up on the woman's face while she is sitting seductively on the bed. The final framing clearly shows her breasts at the top, belly in the center, and upper thighs at the bottom. Slow continuous zoom-in, elegant and sensual movement, cinematic lighting, intimate atmosphere, 5 seconds, high detail, photorealistic, woman slighlty moves her head smiles a little, move her hand and finger.",
        "neg": """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement, 
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement, 
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions, 
low quality, blurry motion, motion blur, artifact, glitch, flickering, 
text, watermark, logo, overlay, 
overexposed, underexposed, wrong lighting, warm colors, 
multiple angles, split screen, changing camera angle too fast, 
unnatural camera movement, orbiting too quickly, spinning camera""",
    },

    {
        "file": "15.53. bedroom_2zoom.png",
        "backend": "linux",
        "duration": 5,
        "pos": "NONE",
        "neg": "bra disappearing, clothes morphing, teleporting bra, blurry hands, unnatural motion, blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },

    {"break": True},

    {
        "file": "15.51. bedroom_2.png",
        "backend": "linux",
        "duration": 5,
        "pos": "NONE",
        "neg": "NONE",
    },

    {
        "chain": [
            {
                "duration": 5, 
                "pos": "Camera slowly and smoothly zooms in from a medium shot to a close-up on the woman's face while she is sitting seductively on the bed. The final framing clearly shows her breasts at the top, belly in the center, and upper thighs at the bottom. Slow continuous zoom-in, elegant and sensual movement, cinematic lighting, intimate atmosphere, 5 seconds, high detail, photorealistic, woman slighlty moves her head smiles a little, move her hand and finger.",
                "neg": """camera shake, shaky cam, jitter, stuttering, sudden movements, fast motion, quick pan, rapid zoom, jerky movement, 
woman moving, breathing, blinking, hair moving, body twitching, leg movement, arm movement, 
deformed anatomy, extra limbs, missing limbs, distorted body, bad proportions, 
low quality, blurry motion, motion blur, artifact, glitch, flickering, 
text, watermark, logo, overlay, 
overexposed, underexposed, wrong lighting, warm colors, 
multiple angles, split screen, changing camera angle too fast, 
unnatural camera movement, orbiting too quickly, spinning camera"""
            },
            # {
                # "duration": 2, 
                # "pos": "Woman continue walking down the street",
            # },
        ],
        "chain_prefix": "around_woman",
        "backend": "linux",
        "fps": 16,
        "steps": 6,  # ← Zwiększone z 15 (hi-res quality!)
        "cfg": 2.0,   # ← Zwiększone z 4.0 (stronger guidance)
        "neg": "static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality",
    },

    # {"break": True},

    # {
        # "file": "05.23 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": "Throw trausers away from scene",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },
  
    # {
        # "file": "05.25 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": """Beautiful woman sitting on bed, wearing a bra. She slowly reaches back, unhooks her bra, slides both straps off her shoulders with graceful movements, pulls the bra forward and completely removes it. She then throws the bra out of frame to the side with one hand. After that she places both hands on her bare breasts, covering them gently. Very slow, natural and sensual sequence of movements, realistic cloth physics, detailed fingers, smooth 5-second motion, cinematic intimate lighting, high quality""",
        # "neg": "bra disappearing, clothes morphing, teleporting bra, blurry hands, unnatural motion, blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    # {
        # "file": "05.27 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": """Beautiful woman sitting on bed in panties. She slowly rises to standing, seductively pulls her panties down her hips and thighs with both hands. She lets the panties slide naturally down her legs and fall to the floor outside the frame. After they drop, she lifts one leg and rests her foot on the bed in a confident pose. Very slow, smooth and realistic fabric physics, gravity-based falling motion, no clipping through legs, detailed sensual movement, intimate cinematic lighting, 5-6 seconds""",
        # "neg": "panties disappearing, clothes morphing, teleporting underwear, blurry legs, unnatural motion, floating panties, blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    # {
        # "file": "05.29 END.png",
        # "backend": "linux",
        # "duration": 3,
        # "pos": "smooth transition - dance movement",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

   # {
        # "file": "05.31 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": """Create a short, seductive video from this image:

# She begins a slow, provocative erotic dance – very confident and bold. She sways her hips in wide, circular, teasing movements, rolling them seductively forward and backward, accentuating every curve of her body.

# She arches her back deeply, pushing her chest forward to emphasize her cleavage, then runs her hands slowly down her sides, over her waist, hips and thighs.

# She turns around slowly, showing her back and buttocks, bending slightly at the waist while continuing the hypnotic hip rolls.

# She faces the camera again, biting her lip, maintaining intense eye contact, lifting her arms above her head to stretch her body and highlight her figure.

# Her movements are fluid, sensual, deliberately exhibitionistic – she proudly exposes and accentuates her breasts, waist, hips, legs and curves with every sway and twist. The dance is unapologetically provocative and inviting.

# Camera: static medium-wide shot at first, then slowly zooms in slightly during the most intense hip movements, keeping her full body in frame most of the time. Realistic motion, smooth and natural animation, high detail, cinematic moody lighting with soft blue city lights reflecting on her skin, office background unchanged.""",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

   # {
        # "file": "05.33 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": """Create a short, erotic video from this image:

# She slowly turns her back to the camera, facing away completely.

# Then she bends forward at the waist, keeping her legs straight or very slightly bent, arches her back deeply, and places both hands on her knees (or just above them) for support. Her posture is very pronounced: ass pushed out toward the camera, back arched, head slightly lowered or turned to the side so part of her face is visible in profile.

# In this position she starts provocatively twerking / circling her hips and ass — slow, deliberate, seductive movements: rolling her hips in wide circles, then short, teasing up-and-down bounces, making her buttocks bounce and sway enticingly. Every motion is meant to invite and arouse, very exhibitionistic and confident.

# She keeps this inviting, ass-out pose the whole time, hands staying on her knees, back arched, occasionally glancing back over her shoulder with a naughty, knowing look or biting her lip.

# Camera remains static in a medium-low angle shot from behind, slightly below hip level, emphasizing her curves and movements. Realistic motion, smooth and fluid animation, high detail, cinematic moody lighting with city lights reflecting on her skin, office background unchanged.""",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

   # {
        # "file": "05.35 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": """Create a 5-second cinematic erotic dance video, highly detailed and hyper-realistic

# Action sequence (5 seconds total, fluid and provocative movements):

# 0-1 second (Introduction):
# - She stands center-frame facing camera at medium shot, hips swaying seductively side-to-side.
# - Slowly tosses her long hair back dramatically with both hands, arching her back slightly, lips parted in invitation.

# 1-3 seconds (Build-up):
# - Raises both arms gracefully, interlacing fingers behind her head, elbows out - thrusting her chest forward prominently.
# - Body undulates in slow waves: shoulders roll, torso twists erotically, hips circle teasingly while maintaining arched posture.

# 3-4 seconds (Intensification):
# - Hands glide down sensually from behind head, tracing neck, over shoulders, down sides of body.
# - Fingers trail provocatively over breasts, then lower to caress inner thighs and intimate areas through sheer fabric - lingering touches with slight hip thrusts.

# 4-5 seconds (Climax):
# - Both hands cup and squeeze her full breasts firmly from below, lifting and presenting them to camera.
# - Ends with a sultry gaze directly into lens, biting lower lip, body frozen in this pose as subtle hip sway fades out.

# Camera work:
# - Starts with smooth tracking shot circling from front at eye level.
# - Transitions to slight low-angle tilt-up emphasizing curves and movements.
# - Static hold in final second for intimate close-up on face and bust.
# - Realistic motion blur, depth of field with sharp focus on body, bokeh lights in background.""",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

   # {
        # "file": "05.37 END.png",
        # "backend": "linux",
        # "duration": 5,
        # "pos": """A provocative erotic dancer finishes her routine with a graceful rightward turn and exit, 5-second cinematic video featuring STRICTLY STATIC CAMERA - no movement, pans, or orbits; dancer simply rotates and walks off-frame with poise, nothing more.

# Action sequence (precise 5-second progression at 24fps, fluid slow-motion 0.25x; STATIC CAMERA ONLY):
# • 0-2s (Beginning): Stands center-frame facing camera at slight angle, exhales from performance, arms dropping naturally; slowly pivots clockwise on heels, turning rightward with elegant hip shift
# • 2-4s (Development): Completes 180-degree turn facing right edge of frame, body elongated gracefully, hair cascading over shoulder; takes two poised steps forward
# • 4-5s (End): Glides smoothly out of frame right with final sway, leaving empty space center; static frame holds on vacated spot with lingering light trails

# Camera and movement:
# • STRICTLY STATIC LOCKED-OFF CAMERA at fixed medium-wide angle, eye-level height, no panning, tilting, zooming, or tracking - dancer moves through frame naturally
# • Fixed shallow DoF (f/2.0) isolating subject against softly blurred background throughout

# Technical rendering:
# Cinematic hyper-realistic 8K resolution, HDR high contrast, precise motion blur on hair and fabrics, photorealistic skin textures and lace details, subtle depth haze.""",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    # {
        # "file": "05.31 END.png",
        # "backend": "linux",
        # "duration": 3,
        # "pos": "Woman is smoothly sits on bed",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    # {
        # "file": "06.05 END.png",
        # "backend": "linux",
        # "duration": 3,
        # "pos": "smooth transition - dance movement",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    # {
        # "chain": [
            # {
                # "duration": 2, 
                # "pos": "Camera slowly turns around woman showing her spread legs"
            # },
            # {
                # "duration": 2, 
                # "pos": "zoom in woman's legs"
            # },
        # ],
        # "chain_prefix": "around_woman",
        # "backend": "linux",
        # "fps": 16,
        # "steps": 6,  # ← Zwiększone z 15 (hi-res quality!)
        # "cfg": 2.0,   # ← Zwiększone z 4.0 (stronger guidance)
        # "neg": "static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality",
        
        # ============================================================
        # Optional: Transition to next (jeśli dodasz następny plik)
        # ============================================================
        # "transition_to_next": {
            # "duration": 4,
            # "steps": 20,
            # "pos": "woman gradually slows walking pace, steps decelerating smoothly, comes to gentle stop, feet settling into standing position, smooth continuous deceleration, natural halt"
        # }

    # {
        # "file": "05.41 koniec.png",
        # "backend": "local",
        # "duration": 3,
        # "pos": "dominant woman slowly turns 180 degrees with perfect elegant posture, chin high, dignified walk away from camera into dark shadows, slow confident swaying steps, glossy latex reflecting red and green lights. Static camera, shallow depth of field, focus stays on empty space where she stood and the motionless submissive woman facing wall.",
        # "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    # },

    # {"file": "05.41 koniec_2.png"},
  

]

FLOW = FLOW_TEST if USE_TEST_FLOW else FLOW_FULL

# ============================================================
# GENERIC PROMPTS
# ============================================================

GENERIC_PROMPTS = {
    "image_to_video": {
        "pos": "photograph springs to life, motion begins smoothly, gradual acceleration",
        "neg": "static photo, no motion, stays frozen, sudden jump",
    },
    "video_to_image": {
        "pos": "motion gradually slows down, freeze into photograph, cinematic stop",
        "neg": "sudden stop, abrupt freeze, jerky motion",
    },
}

# ============================================================
# RESOLUTION SETTINGS
# ============================================================

MIN_WIDTH = 336
MIN_HEIGHT = 448
MAX_WIDTH = 336
MAX_HEIGHT = 448
DEFAULT_RESOLUTION = (336, 448)
# FORCE_RESOLUTION = (544, 960)  # None for auto
FORCE_RESOLUTION = (512, 512)  # None for auto

# ============================================================
# GENERATION SETTINGS
# ============================================================

DEFAULT_DURATION = 2
DEFAULT_FPS = 16
DEFAULT_STEPS = 6
DEFAULT_CFG = 2.0
DEFAULT_SEED = None

DEFAULT_POSITIVE_PROMPT = "smooth motion, high quality"
DEFAULT_NEGATIVE_PROMPT = "blurry, distorted, artifacts"

SKIP_MISSING = True
SKIP_EXISTED = True
IMAGE_QUALITY = 95
ASPECT_RATIO_TOLERANCE = 0.13
ASPECT_RATIO_STRATEGY = "most_common"

# ============================================================
# BACKEND-SPECIFIC SETTINGS
# ============================================================

# Cloud (Comfy.icu)
COMFY_ICU_WORKFLOW_ID = "fv9kYUtmjLzC5I8tRR49y"
WORKFLOW_TEMPLATE_PATH = r"D:\streamlit_project\comfyui_integration\workflows\_IMAGE2VIDEO_FULL_wan2.2.json"

# Local (ComfyUI)
CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"D:\ComfyUI\output"
API_URL = "http://127.0.0.1:8189"
# ============================================================
# POSTPROCESSING CONFIG
# Sequential execution: numbered_flow → full_concat → upscale
# ============================================================

POSTPROCESSING = {
    # Master switch
    'enabled': False,  # ← Set to True to enable postprocessing
    
    # === Individual processors (executed in order) ===
    
    # Step 1: Copy to numbered FLOW folder
    'numbered_flow': True,  # Creates FLOW_[project]_[timestamp]/ with f0001, f0002, ...
    
    # Step 2: Concatenate all clips into single movie
    'full_concat': False,  # Creates FULL_MOVIE_[project]_[timestamp].mp4
    
    # Step 3: Upscale (NEW!)
    'upscale': False,  # Batch GAN upscaling with interactive source selection
    
    # Future processors (disabled for now)
    # 'color_grade': False,
    # 'audio_overlay': False,
    # 'watermark': False,
    
    # === Settings per processor ===
    
    'numbered_flow_settings': {
        'output_folder': None,  # None = auto: FLOW_[project]_[timestamp]
        'number_format': 'f{:04d}',  # f0001, f0002, ... (max 9999)
        'copy_only_from_flow': True,  # Only files from FLOW (ignore old versions)
    },
    
    'full_concat_settings': {
        'output_name': None,  # None = auto: FULL_MOVIE_[project]_[timestamp].mp4
        'check_missing': True,  # Check FLOW completeness
        'confirm_if_missing': True,  # Ask if files missing
        'video_codec': 'libx264',
        'crf': 18,
        'preset': 'medium',
        'fps': 16,
    },
    
    'upscale_settings': {
        # Source selection mode:
        # 'interactive' - Ask user to choose (project source / FLOW folder / full movie)
        # 'source' - Upscale from project dirs (main, chain, transitions)
        # 'numbered_flow' - Upscale latest FLOW folder
        # 'full_movie' - Upscale full concat movie
        'source_mode': 'interactive',
        
        # Upscale parameters
        'target_resolution': (1920, 1440),
        'upscale_model': 'RealESRGAN_x4plus.pth',
        'interpolation': 'lanczos',  # lanczos (best), bicubic, bilinear, nearest
        'method': 'stretch',  # stretch, crop, fit
        
        # ComfyUI connection
        'comfyui_server': 'http://127.0.0.1:8100',
        'comfyui_output_folder': 'D:/ComfyUI/output',
    },
}

# ============================================================
# DEBUG SETTINGS
# ============================================================

DEBUG_LOG = True  # True = verbose, False = clean production logs

# ============================================================
# RUN - Minimal execution code (logic in orchestrators)
# ============================================================

if __name__ == "__main__":
    # Auto-build config from global variables + validate
    config = validate_config_or_exit(globals())
    
    # Run batch generation (includes postprocessing if enabled)
    run_batch_generation(config)