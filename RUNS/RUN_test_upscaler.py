# -*- coding: utf-8 -*-
"""
TEST: GAN Upscaler
Upscale single video using RealESRGAN

Usage:
    python RUN_test_upscaler.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backends.utility_backend import UtilityBackend

# ============================================================
# INPUT/OUTPUT CONFIGURATION
# ============================================================

# Input video (your SadTalker output or any video)
INPUT_VIDEO = r"D:\ComfyUI\output\20260213075946.mp4"

# Output folder and filename
OUTPUT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\girl_in_nightclub\upscaled"
OUTPUT_NAME = "sadtalker_upscaled_1024.mp4"

# ============================================================
# UPSCALE SETTINGS
# ============================================================

# Target resolution (after upscale + resize)
TARGET_WIDTH = 1024
TARGET_HEIGHT = 1024

# Resize method
INTERPOLATION = "lanczos"  # lanczos (best), bicubic, bilinear, nearest
METHOD = "stretch"          # stretch, crop, fit

# Model (optional - uses config default if None)
MODEL_NAME = None  # or "RealESRGAN_x4plus.pth", "RealESRGAN_x2plus.pth"

# ============================================================
# BACKEND CONFIGURATION
# ============================================================

CONFIG = {
    # Paths
    'workflows_path': r"D:\streamlit_project\comfyui_integration\workflows",
    'workflow_configs_path': r"D:\streamlit_project\comfyui_integration\workflow_configs",
    'comfyui_output_folder': r"D:\ComfyUI\output",
    'comfyui_server': 'http://127.0.0.1:8100',
    
    # Utility type
    'utility_workflow': 'gan_upscaler',
    
    # Settings (optional - override YAML defaults)
    'target_width': TARGET_WIDTH,
    'target_height': TARGET_HEIGHT,
    'interpolation': INTERPOLATION,
    'method': METHOD,
}

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print()
    print("="*70)
    print("  GAN UPSCALER - TEST RUN")
    print("="*70)
    print()
    print(f"Input:  {Path(INPUT_VIDEO).name}")
    print(f"        ({Path(INPUT_VIDEO).stat().st_size / (1024*1024):.1f} MB)")
    print()
    print(f"Output: {OUTPUT_NAME}")
    print(f"Folder: {OUTPUT_FOLDER}")
    print()
    print(f"Target: {TARGET_WIDTH}x{TARGET_HEIGHT}")
    print(f"Method: {METHOD}, interpolation={INTERPOLATION}")
    print()
    print("="*70)
    print()
    
    # Confirmation
    response = input("Start upscaling? [Y/n]: ").strip().lower()
    
    if response in ['n', 'no']:
        print("Cancelled.")
        sys.exit(0)
    
    print()
    
    # Initialize backend
    try:
        backend = UtilityBackend(CONFIG)
    except Exception as e:
        print(f"ERROR: Failed to initialize backend!")
        print(f"  {e}")
        print()
        print("Check:")
        print("  1. ComfyUI is running (python main.py)")
        print("  2. Paths in CONFIG are correct")
        print("  3. YAML config exists: workflow_configs/gan_upscaler_config.yaml")
        print("  4. JSON workflow exists: workflows/workflow-gan-upscaler.json")
        sys.exit(1)
    
    # Upscale
    input_path = Path(INPUT_VIDEO)
    output_path = Path(OUTPUT_FOLDER) / OUTPUT_NAME
    
    success = backend.upscale_video(
        input_video=input_path,
        output_path=output_path,
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        interpolation=INTERPOLATION,
        method=METHOD,
        model_name=MODEL_NAME
    )
    
    # Result
    print()
    
    if success:
        print("="*70)
        print("  ✅ SUCCESS!")
        print("="*70)
        print()
        print(f"Upscaled video saved to:")
        print(f"  {output_path}")
        print()
        print("Next steps:")
        print("  1. Play video to verify quality")
        print("  2. Compare with original")
        print("  3. Integrate into postprocessing pipeline")
        print()
    else:
        print("="*70)
        print("  ❌ FAILED!")
        print("="*70)
        print()
        print("Check:")
        print("  1. ComfyUI terminal for errors")
        print("  2. Input video path is correct")
        print("  3. Output folder exists and is writable")
        print("  4. VRAM available (~15 GB needed)")
        print()