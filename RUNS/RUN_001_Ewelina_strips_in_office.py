# -*- coding: utf-8 -*-
"""
ORCHESTRATOR TEST 001: Mixed cloud + local backends
First transition: CLOUD (01→02)
Second transition: LOCAL (03→04)

Total cost: ~$0.10 (only first transition)
Total time: ~1 min cloud + ~4 min local = ~5 min
"""

# ============================================================
# IMPORTANT: Add parent directory to path (RUNS/ subfolder)
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# Configs and validator
# ============================================================

from config_validator import validate_config_or_exit

# ============================================================
# Import orchestrator
# ============================================================
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\chain_test"

# ============================================================
# FLOW - Mixed backends!
# ============================================================

USE_TEST_FLOW = False  # ← ZMIEŃ NA False dla full production


FLOW_TEST = [
    # ============================================================
    # SEQUENCE 1: Undressing blouse (5 image transitions)
    # ============================================================
    
    {
        "file": "01.03_ewelina_stands_in_skirt.jpg",
        "pos": "shy woman slowly reaches for blouse buttons, hesitant fingers begin unbuttoning from top, gentle nervous movements, gradually opening blouse button by button, natural breathing motion, soft uncertain expression, warm lighting",
        "neg": "fast motion, rushed, aggressive movement, ripping clothes, sudden actions, blurry, distorted",
        "duration": 8,
    },

    {
        "file": "01.04_ewelina_stands_in_unbuttoned_skirt.png",
        "pos": "woman gently grabs open blouse edges, slowly slides fabric off shoulders, arms gradually pulling out of sleeves one by one, blouse falling softly, smooth continuous motion, shy facial expression, natural movement flow",
        "neg": "jerky motion, sudden pull, throwing clothes, fast undressing, abrupt movements, teleporting, blurry",
        "duration": 5,        
    },
    
]
FLOW_FULL = [  
    {
        "file": "00.03. Ewelina spokojnie stoi w marynarce.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "woman standing naturally, subtle breathing, soft lighting",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
    {
        "file": "00.05. Ewelina zdejmuje marynarke.mp4",
        "backend": "local",
        "duration": 2,
        "pos": "woman standing naturally, subtle breathing, soft lighting",
        "neg": "blurry, low quality, sudden movements, pose changes, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
    {
        "file": "00.08. Ewelina wyjmuje koszule z marynarki.mp4",
        "backend": "local",
        "duration": 4,
        "pos": "elegant woman standing confidently, soft ambient lighting, subtle natural movements",
        "neg": "blurry, low quality, jerky motion, frozen, moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
    },
    {
        "file": "01.03_ewelina_stands_in_skirt.jpg",
        "pos": "shy woman slowly reaches for blouse buttons, hesitant fingers begin unbuttoning from top, gentle nervous movements, gradually opening blouse button by button, natural breathing motion, soft uncertain expression, warm lighting",
        "neg": "fast motion, rushed, aggressive movement, ripping clothes, sudden actions, blurry, distorted",
        "duration": 8,
    },
    
    {
        "file": "01.04_ewelina_stands_in_unbuttoned_skirt.png",
        "pos": "woman gently grabs open blouse edges, slowly slides fabric off shoulders, arms gradually pulling out of sleeves one by one, blouse falling softly, smooth continuous motion, shy facial expression, natural movement flow",
        "neg": "jerky motion, sudden pull, throwing clothes, fast undressing, abrupt movements, teleporting, blurry",
        "duration": 5,        
    },
    
    {
        "file": "01.06. Ewelina stands in skirt and bra.png",
        "pos": "standing woman slowly bends knees, hips gradually lowering toward chair, arms reaching back for support, body smoothly descending into sitting position, shy blushing expression, gentle controlled motion, natural sitting transition",
        "neg": "falling, dropping down, sudden sit, jerky movement, losing balance, abrupt motion, distorted",
        "duration": 2,        
    },
    
    {
        "file": "01.08._ewelina_sit_in_skirt_bra.jpg",
        "pos": "seated woman places hands on armrests, slowly pushes body upward, legs gradually straightening, hips rising from chair, smooth controlled ascent, reluctant hesitant movement, natural standing transition, uncertain expression",
        "neg": "jumping up, fast motion, sudden stand, jerky ascent, losing balance, abrupt movement, blurry",
        "duration": 4,        
    },
    
    {
        "file": "01.10. Ewelina stands in skirt and bra.png",
        "pos": "simple transition",
        "neg": "frozen statue, completely static, no movement, sudden actions, blurry, low quality moving background, waving windows, motion outside, cars moving, people moving, wind, ripples, dynamic scene, any movement",
        "duration": 3,        
    },
    
    {
        "file": "01.20. Ewelina undress skirt.mp4",
        "backend": "local",
    },
    
    {"break": True},  # Hard cut (costume/scene change)
    
    {
        "file": "02_ewelina_braOFF.mp4",
        "backend": "local",
    },

    {"break": True},  # Hard cut (costume/scene change)
    
    {
        "file": "03._ewelina_panties_off.mp4",
        "backend": "local",
        "duration": 4,
        "pos": "motion gradually slows down, movement smoothly decelerating, freeze into photograph, cinematic slow-motion stop, graceful halt, natural deceleration into stillness",
        "neg": "sudden stop, abrupt freeze, jerky motion, choppy slowdown, stuttering, unnatural halt",
    },
    
    {"file": "04_ewelina_out.png"},
    
    {
        "chain": [
            {
                "duration": 2, 
                "pos": "woman starts walking down the corridor, hesitant first steps, foot lifting and placing carefully, moving away from camera, body gradually getting smaller in frame, uncertain slow pace"
            },
            {
                "duration": 2, 
                "pos": "woman continues walking deeper into corridor, steady hesitant steps, arms swaying gently, body receding further, getting noticeably smaller in distant view, maintained slow uncertain pace"
            },
            {
                "duration": 2, 
                "pos": "woman walks further down corridor toward far end, very small figure in distance, continued hesitant walking motion, diminishing into corridor depth, distant perspective"
            },
        ],
        "chain_prefix": "ewelina_walks",
        "backend": "local",
        "fps": 16,
        "steps": 20,  # ← Zwiększone z 15 (hi-res quality!)
        "cfg": 5.0,   # ← Zwiększone z 4.0 (stronger guidance)
        "neg": "static, frozen, no movement, distorted, walking towards camera, facing camera, approaching viewer, coming closer, teleporting, jumping, blurry, low quality",
        
        # ============================================================
        # Optional: Transition to next (jeśli dodasz następny plik)
        # ============================================================
        # "transition_to_next": {
        #     "duration": 4,
        #     "steps": 20,
        #     "pos": "woman gradually slows walking pace, steps decelerating smoothly, comes to gentle stop, feet settling into standing position, smooth continuous deceleration, natural halt"
        # }
    },
    
    # === NEXT FILE (opcjonalnie - jeśli masz kolejny plik) ===
    # {"file": "05_next_file.mp4"},

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
# RESOLUTION
# ============================================================

MIN_WIDTH = 336
MIN_HEIGHT = 448
MAX_WIDTH = 336
MAX_HEIGHT = 448
DEFAULT_RESOLUTION = (336, 448)
FORCE_RESOLUTION = (512, 672) #None

# ============================================================
# GENERATION SETTINGS
# ============================================================

DEFAULT_DURATION = 4
DEFAULT_FPS = 16
DEFAULT_STEPS = 20 #15
DEFAULT_CFG = 5.0
DEFAULT_SEED = None

DEFAULT_POSITIVE_PROMPT = "smooth motion, high quality"
DEFAULT_NEGATIVE_PROMPT = "blurry, distorted, artifacts"

SKIP_MISSING = True
SKIP_EXISTED = True  # Always regenerate for test
IMAGE_QUALITY = 95
ASPECT_RATIO_TOLERANCE = 0.11
ASPECT_RATIO_STRATEGY = "most_common"

# ============================================================
# BACKEND-SPECIFIC SETTINGS
# ============================================================

# Cloud (Comfy.icu)
COMFY_ICU_WORKFLOW_ID = "fv9kYUtmjLzC5I8tRR49y"
WORKFLOW_TEMPLATE_PATH = r"D:\streamlit_project\comfyui_integration\workflows\workflow-api-fv9kYUtmjLzC5I8tRR49y.json"

# Local (ComfyUI)
CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"D:\ComfyUI\output\video"

# ============================================================
# POSTPROCESSING CONFIG (opcjonalne)
# ============================================================

POSTPROCESSING = {
    
    'enabled': True,
    'full_concat': True,
    'full_concat_settings': {
        'normalize': True,  # ← Czy to jest?
        'fps': 16,
    },  # ← Master switch - Zmień na True aby uruchomić postprocessing
    
    # === Individual processors (można włączyć kilka naraz) ===
    
    'full_concat': True,  # Tworzy FULL_MOVIE_[project]_[timestamp].mp4
    
    'numbered_flow': False,  # Kopiuje pliki do FLOW_[project]_[timestamp]/
    
    # (Rozwojowo - na później)
    # 'upscale': False,
    # 'color_grade': False,
    # 'audio_overlay': False,
    # 'watermark': False,
    
    # === Settings per processor ===
    
    'full_concat_settings': {
        'output_name': None,  # None = auto: FULL_MOVIE_[project]_[timestamp].mp4
        'check_missing': True,  # Sprawdź kompletność FLOW
        'confirm_if_missing': True,  # Pytaj jeśli brakuje plików
        'video_codec': 'libx264',
        'crf': 18,
        'preset': 'medium',
    },
    
    'numbered_flow_settings': {
        'output_folder': None,  # None = auto: FLOW_[project]_[timestamp]
        'number_format': 'f{:04d}',  # f0001, f0002, ... (max 9999)
        'copy_only_from_flow': True,  # Tylko pliki z FLOW (ignore stare wersje)
    },
}

# ============================================================
# DEBUG SETTINGS
# ============================================================
DEBUG_LOG = True  # True = verbose, False = clean production logs

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    # Auto-build config from global variables + validate
    config = validate_config_or_exit(globals())
    
    # Run!
    run_batch_generation(config)