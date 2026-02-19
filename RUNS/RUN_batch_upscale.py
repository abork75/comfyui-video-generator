# -*- coding: utf-8 -*-
"""
Batch Upscale - Entry Point
Upscale wielu filmów z projektu (source lub numbered_flow)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from postprocessing.batch_upscale import run_batch_upscale
from colorama import Fore, Style, init

init(autoreset=True)

# =============================================================================
#  CONFIGURATION
# =============================================================================

PROJECT_PATH = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\girl_in_nightclub"

# Wybierz tryb:
# 'source' - upscale plików źródłowych (main, chain, transitions)
# 'numbered_flow' - upscale z FLOW_* folders (interactive selection)
SOURCE_MODE = 'source'

# Settings
TARGET_RESOLUTION = (1024, 1024)
UPSCALE_MODEL = 'RealESRGAN_x4plus.pth'
INTERPOLATION = 'lanczos'  # lanczos (best), bicubic, bilinear, nearest
METHOD = 'stretch'  # stretch, crop, fit
COMFYUI_SERVER = 'http://127.0.0.1:8100'
COMFYUI_OUTPUT_FOLDER = 'D:/ComfyUI/output'

# =============================================================================
#  EXECUTION
# =============================================================================

if __name__ == '__main__':
    config = {
        'project_folder': PROJECT_PATH,
        'batch_upscale': {
            'source_mode': SOURCE_MODE,
            'target_resolution': TARGET_RESOLUTION,
            'upscale_model': UPSCALE_MODEL,
            'interpolation': INTERPOLATION,
            'method': METHOD,
            'comfyui_server': COMFYUI_SERVER,
            'comfyui_output_folder': COMFYUI_OUTPUT_FOLDER,
        }
    }
    
    project_name = Path(PROJECT_PATH).name
    
    print(f"""
{Fore.CYAN}{'='*70}
{'':20}BATCH UPSCALE
{'='*70}{Style.RESET_ALL}

Project: {Fore.YELLOW}{project_name}{Style.RESET_ALL}
Mode:    {Fore.YELLOW}{SOURCE_MODE.upper()}{Style.RESET_ALL}
Target:  {Fore.YELLOW}{TARGET_RESOLUTION[0]}x{TARGET_RESOLUTION[1]}{Style.RESET_ALL}
Model:   {Fore.YELLOW}{UPSCALE_MODEL}{Style.RESET_ALL}

{Fore.CYAN}{'='*70}{Style.RESET_ALL}
""")
    
    # Confirmation
    response = input(f"{Fore.YELLOW}Start batch upscaling? [Y/n]: {Style.RESET_ALL}").strip().lower()
    if response and response != 'y':
        print(f"{Fore.RED}✗ Cancelled{Style.RESET_ALL}")
        sys.exit(0)
    
    # Run
    success = run_batch_upscale(config)
    
    if success:
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{'':20}✅ BATCH UPSCALE COMPLETE!")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.RED}{'='*70}")
        print(f"{'':20}❌ BATCH UPSCALE FAILED")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        sys.exit(1)