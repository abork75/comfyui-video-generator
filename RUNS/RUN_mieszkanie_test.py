# -*- coding: utf-8 -*-
"""
TEST - Wizualizacja Mieszkania
9 transitions, ALL LOCAL, 3s duration
Kuchnia (2) → Salon (4) → Schody (3)
"""

# ============================================================
# IMPORTANT: Add parent directory to path (RUNS/ subfolder)
# ============================================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# Import orchestrator
# ============================================================
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\pliki_mieszkanie"

# ============================================================
# FLOW - ALL LOCAL
# ============================================================

FLOW = [
    # === KUCHNIA ===
    {"file": "01.01. kuchnia.jpeg", "backend": "local", "duration": 3},
    {"file": "01.02. kuchnia.jpeg", "backend": "local", "duration": 3},
    {"file": "01.03. kuchnia.jpeg"},
    
    {"break": True},
    
    # === SALON ===
    {"file": "02.01. salon.jpeg", "backend": "local", "duration": 3},
    {"file": "02.02. salon.jpeg", "backend": "local", "duration": 3},
    {"file": "02.03. salon.jpeg", "backend": "local", "duration": 3},
    {"file": "02.05. salon.jpeg"},
    
    {"break": True},
    
    # === SCHODY ===
    {"file": "03.01. schody.jpeg", "backend": "local", "duration": 3},
    {"file": "03.02. schody.jpeg", "backend": "local", "duration": 3},
    {"file": "03.03. schody.jpeg", "backend": "local", "duration": 3},
    {"file": "03.04. schody.jpeg"},
]

# ============================================================
# RESOLUTION
# ============================================================

MIN_WIDTH = 512
MIN_HEIGHT = 384
MAX_WIDTH = 2048
MAX_HEIGHT = 1536
DEFAULT_RESOLUTION = (512, 384)
FORCE_RESOLUTION = None

# ============================================================
# GENERATION SETTINGS
# ============================================================

DEFAULT_DURATION = 3
DEFAULT_FPS = 16
DEFAULT_STEPS = 15
DEFAULT_CFG = 4.5
DEFAULT_SEED = None

# Prompty dla architektury
DEFAULT_POSITIVE_PROMPT = (
    "smooth camera movement through interior space, "
    "architectural visualization, professional real estate presentation, "
    "cinematic transition, seamless motion, high-end interior design, "
    "natural lighting, photorealistic rendering"
)

DEFAULT_NEGATIVE_PROMPT = (
    "jerky motion, sudden cuts, abrupt transitions, "
    "distortion, warping, unrealistic physics, blurry details, "
    "low quality, artifacts, flickering, unnatural movement"
)

SKIP_MISSING = True
SKIP_EXISTED = True
IMAGE_QUALITY = 95
ASPECT_RATIO_TOLERANCE = 0.10
ASPECT_RATIO_STRATEGY = "most_common"

# ============================================================
# LOCAL BACKEND ONLY
# ============================================================

CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"D:\ComfyUI\output\video"

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🏠 TEST - WIZUALIZACJA MIESZKANIA")
    print("="*70)
    print(f"Projekt: pliki_mieszkanie")
    print(f"Transitions: 9 (Kuchnia 2 + Salon 4 + Schody 3)")
    print(f"Backend: ALL LOCAL (ComfyUI)")
    print(f"Duration: 3s @ 16 FPS")
    print(f"Cost: FREE")
    print(f"Time: ~18-20 min")
    print("="*70 + "\n")
    
    config = {
        'project_folder': PROJECT_FOLDER,
        'flow': FLOW,
        'default_duration': DEFAULT_DURATION,
        'default_fps': DEFAULT_FPS,
        'default_steps': DEFAULT_STEPS,
        'default_cfg': DEFAULT_CFG,
        'default_seed': DEFAULT_SEED,
        'default_positive_prompt': DEFAULT_POSITIVE_PROMPT,
        'default_negative_prompt': DEFAULT_NEGATIVE_PROMPT,
        'min_width': MIN_WIDTH,
        'min_height': MIN_HEIGHT,
        'max_width': MAX_WIDTH,
        'max_height': MAX_HEIGHT,
        'default_resolution': DEFAULT_RESOLUTION,
        'force_resolution': FORCE_RESOLUTION,
        'skip_missing': SKIP_MISSING,
        'skip_existed': SKIP_EXISTED,
        'image_quality': IMAGE_QUALITY,
        'aspect_ratio_tolerance': ASPECT_RATIO_TOLERANCE,
        'aspect_ratio_strategy': ASPECT_RATIO_STRATEGY,
        
        # Local backend only
        'config_path': CONFIG_PATH,
        'workflows_path': WORKFLOWS_PATH,
        'comfyui_output_folder': COMFYUI_OUTPUT_FOLDER,
    }
    
    run_batch_generation(config)