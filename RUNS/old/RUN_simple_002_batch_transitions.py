# -*- coding: utf-8 -*-
"""
SETUP 001: rome_slaves
Complete Video Pipeline Configuration

Historia zmian:
- 2026-02-06: Initial setup
- 2026-02-06: Duration 4s dla wszystkich
- 2026-02-06: Dodano SKIP_EXISTED (domyslnie True)
"""

# ============================================================
# KONTROLA WORKFLOW - CO MA SIĘ WYKONAĆ
# ============================================================

WYKONAJ_RAMKI = True       # True = wyciągnij klatki z filmów
WYKONAJ_TRANSITIONS = True  # True = generuj przejścia AI
WYKONAJ_LACZENIE = False    # True = połącz wszystko w jeden film

# ============================================================
# KONFIGURACJA PROJEKTU (wspólna dla wszystkich)
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\rome_slaves\slave1"


# ALL_VIDEOS = [
    # "01.13. slave1.mp4",
    # "01.13. slave1_01.01. slave1_transition.mp4",
# ]

ALL_VIDEOS = [
    "01.13. slave1.mp4",
    "01.01. slave1.mp4",
    "01.14. slave1.mp4",
    "01.03. slave1.mp4",
    "01.11. slave1.mp4",
    "01.07. slave1.mp4",
    "01.05. slave1.mp4",
    "01.06. slave1.mp4",
    "01.08. slave1.mp4",
    "01.09. slave1.mp4",
    "01.02. slave1.mp4",
    "01.04. slave1.mp4",
    "01.12. slave1.mp4",
]

# Aktywne filmy
VIDEO_ORDER = ALL_VIDEOS  # Wszystkie
# VIDEO_ORDER = ALL_VIDEOS[:5]  # Test - pierwsze 5

# ============================================================
# KONFIGURACJA: TRANSITIONS
# ============================================================

# Tryb pracy
SKIP_MISSING = True   # Pomijaj brakujące filmy w VIDEO_ORDER
SKIP_EXISTED = True   # Pomijaj już wygenerowane transitions (BEZPIECZNE!)

# Parametry klatek
MAX_WIDTH = 600
MAX_HEIGHT = 900
IMAGE_QUALITY = 95

# Długość przejść
DURATION_SEC = 2  # Jedna długość dla wszystkich

# LUB wektor (zakomentuj DURATION_SEC powyżej):
# DURATION_VECTOR = [4] * 10 + [3] * 2  # Pierwsze 10: 4s, reszta: 3s
DURATION_VECTOR = None

# Parametry generacji
FPS = 16
STEPS = 20
CFG = 4.0
SEED = None  # None = losowy, lub konkretny np. 336550362530194

POSITIVE_PROMPT = "very slow smooth motion, constant speed throughout, natural fluid movement, no sudden changes"

NEGATIVE_PROMPT = "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走, fast motion, speed up, sudden movement, jerky motion, acceleration"

# Workflow config
CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"C:\ComfyUI\output\video"

# ============================================================
# KONFIGURACJA: CONCAT (łączenie)
# ============================================================

OUTPUT_FILENAME = "rome_slaves_FINAL.mp4"
VIDEO_CODEC = "libx264"  # lub "libx265"
CRF = 18  # 18 = bardzo dobra jakość, 23 = dobra, 28 = słabsza
PRESET = "medium"  # ultrafast, fast, medium, slow, veryslow

# ============================================================
# URUCHOMIENIE
# ============================================================

if __name__ == "__main__":
    
    # ========================================
    # FAZA 1+2: RAMKI + TRANSITIONS
    # ========================================
    
    if WYKONAJ_RAMKI or WYKONAJ_TRANSITIONS:
        from batch_transitions_simple import run_batch_generation
        
        # Określ tryb
        if WYKONAJ_RAMKI and not WYKONAJ_TRANSITIONS:
            frame_only = True
            print("\n🎬 TRYB: Tylko wyciąganie ramek\n")
        else:
            frame_only = False
            print("\n🎬 TRYB: Ramki + generacja transitions\n")
        
        # Przygotuj config
        config_transitions = {
            'project_folder': PROJECT_FOLDER,
            'video_order': VIDEO_ORDER,
            'frame_only': frame_only,
            'skip_missing': SKIP_MISSING,
            'skip_existed': SKIP_EXISTED,
            'max_width': MAX_WIDTH,
            'max_height': MAX_HEIGHT,
            'image_quality': IMAGE_QUALITY,
            'duration_sec': DURATION_SEC,
            'duration_vector': DURATION_VECTOR,
            'fps': FPS,
            'steps': STEPS,
            'cfg': CFG,
            'seed': SEED,
            'positive_prompt': POSITIVE_PROMPT,
            'negative_prompt': NEGATIVE_PROMPT,
            'config_path': CONFIG_PATH,
            'workflows_path': WORKFLOWS_PATH,
            'comfyui_output_folder': COMFYUI_OUTPUT_FOLDER,
        }
        
        # Uruchom
        run_batch_generation(config_transitions)
    
    # ========================================
    # FAZA 3: ŁĄCZENIE
    # ========================================
    
    if WYKONAJ_LACZENIE:
        from concat_videos import run_concat
        
        print("\n🎬 TRYB: Łączenie filmów\n")
        
        # Przygotuj config
        config_concat = {
            'project_folder': PROJECT_FOLDER,
            'video_order': VIDEO_ORDER,
            'output_filename': OUTPUT_FILENAME,
            'video_codec': VIDEO_CODEC,
            'crf': CRF,
            'preset': PRESET,
        }
        
        # Uruchom
        run_concat(config_concat)
    
    # ========================================
    # ZAKOŃCZENIE
    # ========================================
    
    if not (WYKONAJ_RAMKI or WYKONAJ_TRANSITIONS or WYKONAJ_LACZENIE):
        print("\n⚠️  Wszystkie flagi wyłączone! Ustaw co najmniej jedną na True:")
        print("  - WYKONAJ_RAMKI = True")
        print("  - WYKONAJ_TRANSITIONS = True")
        print("  - WYKONAJ_LACZENIE = True\n")