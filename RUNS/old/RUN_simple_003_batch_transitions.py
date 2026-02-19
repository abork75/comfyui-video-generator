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

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\ewelina_dream\office_naked"


# ALL_VIDEOS = [
    # "01.13. slave1.mp4",
    # "01.13. slave1_01.01. slave1_transition.mp4",
# ]

ALL_VIDEOS = [
    "05_office_naked.mp4",
    "06_office_naked.mp4",
    # "07_office_naked.mp4",
    # "08_office_naked.mp4",
]

# Aktywne filmy
VIDEO_ORDER = ALL_VIDEOS  # Wszystkie
# VIDEO_ORDER = ALL_VIDEOS[:5]  # Test - pierwsze 5

# ============================================================
# KONFIGURACJA: TRANSITIONSq
# ============================================================

# Tryb pracy
SKIP_MISSING = True   # Pomijaj brakujące filmy w VIDEO_ORDER
SKIP_EXISTED = True   # Pomijaj już wygenerowane transitions (BEZPIECZNE!)

# Parametry klatek
MAX_WIDTH = 704
MAX_HEIGHT = 904

MIN_WIDTH = 672   # ← Force minimum (2x upscale z 336)
MIN_HEIGHT = 896  # ← Force minimum (2x upscale z 448)

IMAGE_QUALITY = 95

# Długość przejść
DURATION_SEC = 3  # Jedna długość dla wszystkich

# LUB wektor (zakomentuj DURATION_SEC powyżej):
# DURATION_VECTOR = [4] * 10 + [3] * 2  # Pierwsze 10: 4s, reszta: 3s
DURATION_VECTOR = None

# Parametry generacji
FPS = 16
STEPS = 20
CFG = 4.0
SEED = None  # None = losowy, lub konkretny np. 336550362530194

POSITIVE_PROMPT = "very slow smooth motion, constant speed throughout, natural fluid movement, no sudden changes, natural female anatomy, realistic body proportions, detailed chest anatomy, natural breasts with visible areola and nipples, anatomically correct, photorealistic skin texture"

NEGATIVE_PROMPT = "blurry, low quality, static, deformed, disfigured, bad anatomy, mutation, extra limbs, missing limbs, bad proportions, fast motion, speed up, sudden movement, jerky motion, acceleration"

# Workflow config
CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"C:\ComfyUI\output\video"

# ============================================================
# KONFIGURACJA: CONCAT (łączenie)
# ============================================================

OUTPUT_FILENAME = "ewlina_office_naked_FINAL.mp4"
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
            'min_width': MIN_WIDTH,
            'min_height': MIN_HEIGHT, 
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