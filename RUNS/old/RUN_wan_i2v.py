"""
WAN 2.2 14B Image-to-Video - Standardowa generacja
Uruchomienie: python run_wan_i2v.py
"""

from workflow_base import WorkflowRunner, Logger
from colorama import Fore, Style

# ============================================================
# 🔧 KONFIGURACJA - EDYTUJ TO!
# ============================================================

# Ścieżki
CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"

# Obrazy
START_IMAGE = r"D:\streamlit_project\images\01_end.png"
END_IMAGE = r"D:\streamlit_project\images\02_start.png"

# Parametry wideo
WIDTH = 464
HEIGHT = 688
FPS = 16
DURATION_SEC = 3

# Parametry modelu
STEPS = 20
CFG = 4.0
SEED = 123456

# Prompty
POSITIVE_PROMPT = "Smooth cinematic transition, high quality, detailed"
NEGATIVE_PROMPT = "blurry, low quality, distorted"

# ============================================================
# WYKONANIE
# ============================================================

if __name__ == "__main__":
    Logger().header("WAN 2.2 14B - Image to Video (Standard)")
    
    # Inicjalizacja
    runner = WorkflowRunner(
        config_path=CONFIG_PATH,
        workflows_base_path=WORKFLOWS_PATH
    )
    
    Logger().section("Konfiguracja parametrów")
    
    # Ustawienia
    runner.set_image(START_IMAGE, "start_image")
    runner.set_image(END_IMAGE, "end_image")
    runner.set_prompt(POSITIVE_PROMPT, "positive_prompt")
    runner.set_prompt(NEGATIVE_PROMPT, "negative_prompt")
    
    runner.set_video_params(
        width=WIDTH,
        height=HEIGHT,
        fps=FPS,
        length=FPS * DURATION_SEC
    )
    
    runner.set_sampling_params(
        steps=STEPS,
        cfg=CFG,
        seed=SEED
    )
    
    # Podsumowanie
    runner.print_summary()
    
    # Uruchomienie
    input(f"\n{Fore.YELLOW}Naciśnij ENTER aby uruchomić...{Style.RESET_ALL}")
    
    result = runner.run(wait_for_completion=True)
    
    # Wynik
    if result:
        Logger().header("SUKCES!")
        print(f"{Fore.GREEN}Sprawdź: C:\\ComfyUI\\output\\video\\{Style.RESET_ALL}")
    else:
        Logger().header("BŁĄD GENERACJI")