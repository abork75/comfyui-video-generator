# RUN_adv_001_batch_transitions.py
# -*- coding: utf-8 -*-
"""
SETUP ADV 001: mixed_story (ADVANCED MODE)
Mixed video + images z custom params per transition

Historia zmian:
- 2026-02-07: Initial setup - ADV mode
- 2026-02-08: Fixed MIN/MAX resolution, removed WYKONAJ_RAMKI
"""

# ============================================================
# KONTROLA WORKFLOW
# ============================================================

WYKONAJ_TRANSITIONS = True
WYKONAJ_LACZENIE = False

# Uwaga: ADV mode zawsze wyciąga klatki przed generacją
# (nie ma trybu frame_only jak w simple)

# ============================================================
# DEFAULTS - Wartości domyślne
# ============================================================

DEFAULT_DURATION = 4
DEFAULT_FPS = 16
DEFAULT_STEPS = 20
DEFAULT_CFG = 4.0
DEFAULT_SEED = None

DEFAULT_POSITIVE_PROMPT = "very slow smooth motion, constant speed throughout, natural fluid movement"
DEFAULT_NEGATIVE_PROMPT = "fast motion, speed up, sudden movement, jerky motion"

# ============================================================
# GENERIC PROMPTS - Biblioteka
# ============================================================

GENERIC_PROMPTS = {
    "default": {
        "pos": DEFAULT_POSITIVE_PROMPT,
        "neg": DEFAULT_NEGATIVE_PROMPT,
    },

    "video_to_video": {
        "pos": "smooth continuous motion, seamless transition, natural flow between scenes, consistent movement",
        "neg": "sudden cuts, abrupt changes, jerky transition, speed changes, static frames",
    },
    
    "video_to_image": {
        "pos": "motion gradually slows down, freeze into photograph, cinematic stop",
        "neg": "sudden stop, abrupt freeze, jerky motion",
    },
    
    "image_to_video": {
        "pos": "photograph springs to life, motion begins smoothly, gradual acceleration",
        "neg": "static photo, no motion, stays frozen, sudden jump",
    },
    
    "image_to_image": {
        "pos": "artistic fade between photographs, gentle blend, gallery transition",
        "neg": "video motion, camera movement, motion blur, dynamic action",
    },
}

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\mixed_story"

# ============================================================
# FLOW - Definicja projektu
# ============================================================

FLOW = [
    # === Plik A - parametry dla transition A→B ===
    {
        "file": "01_ewelina_sit.jpg",
        "duration": 2,
        "pos": "[image_to_video]",
        "neg": "[image_to_video]",
    },
    
    # === Plik B - brak transition po nim (jest break) ===
    {"file": "02_ewelina_braOFF.mp4"},
    
    {"break": True},  # Hard cut - brak transition po B
    
    # === Plik C - parametry dla transition C→D ===
    {
        "file": "03._ewlina_panties_off.mp4",
        "duration": 4,
        "pos": "[video_to_image]",
        "neg": "[video_to_image]",
    },
    
    # === Plik D - ostatni ===
    {"file": "04_ewlina_out.png"},
]

# ============================================================
# Resolution Settings
# ============================================================

# Wymuszenie MINIMUM (force upscaling)
# Gwarantuje jakość anatomii - nie mniej niż:
MIN_WIDTH = 336   # 2x upscale z 672
MIN_HEIGHT = 448  # 2x upscale 896

# Maksymalne wymiary (upper limit)
MAX_WIDTH = 1200   # Musi być >= MIN_WIDTH!
MAX_HEIGHT = 1800  # Musi być >= MIN_HEIGHT!

# Domyślna rozdzielczość (używana gdy brak video w FLOW - uwaga, ale jest upscle/downscale jeżeli poza zakresem min/max powyżej)
# To jest BASE - potem zostanie przeskalowana przez MIN/MAX!
DEFAULT_RESOLUTION = (336, 448)  # (width, height) - MUSI być podzielna przez 8!

# Wymuś rozdzielczość dla WSZYSTKICH (ignoruje auto-detect i MIN/MAX)
# None = auto-detect z video (lub DEFAULT) + apply MIN/MAX
FORCE_RESOLUTION = None

# FORCE_RESOLUTION:
  # ✅ Nadpisuje WSZYSTKO
  # ❌ Ignoruje MIN/MAX
  # ❌ Ignoruje auto-detect
  # 🎯 Use: Absolutna kontrola

# DEFAULT_RESOLUTION:
  # ✅ Używane TYLKO gdy brak video
  # ✅ Potem apply MIN/MAX
  # 🎯 Use: Fallback dla image-only FLOW

# MIN/MAX:
  # ✅ Stosowane zawsze (oprócz FORCE)
  # ✅ Upscale jeśli < MIN
  # ✅ Downscale jeśli > MAX
  # 🎯 Use: Quality control + GPU limits

# ============================================================
# Pozostałe parametry
# ============================================================

SKIP_MISSING = True
SKIP_EXISTED = True
IMAGE_QUALITY = 95

# Aspect Ratio Validation
ASPECT_RATIO_TOLERANCE = 0.10       # 10% tolerancja
ASPECT_RATIO_STRATEGY = "most_common"  # Dopasuj do najczęstszego AR

# Dostępne strategie:
# - "most_common" - najczęstszy AR (REKOMENDOWANE dla mixed content)
# - "first_video" - pierwszy film (dobre dla video-heavy)
# - "first" - pierwszy plik (stare zachowanie)
# - "median" - mediana (dobre dla outlierów)

CONFIG_PATH = r"D:\streamlit_project\comfyui_integration\workflow_configs\wan_i2v_config.yaml"
WORKFLOWS_PATH = r"D:\streamlit_project\comfyui_integration\workflows"
COMFYUI_OUTPUT_FOLDER = r"D:\ComfyUI\output\video"

# ============================================================
# URUCHOMIENIE
# ============================================================

if __name__ == "__main__":
    
    if WYKONAJ_TRANSITIONS:
        from batch_transitions_adv import run_batch_generation_adv
        
        print("\n🎬 TRYB: ADVANCED - Transitions z FLOW\n")
        
        config_transitions = {
            'project_folder': PROJECT_FOLDER,
            'flow': FLOW,
            'generic_prompts': GENERIC_PROMPTS,
            'default_duration': DEFAULT_DURATION,
            'default_fps': DEFAULT_FPS,
            'default_steps': DEFAULT_STEPS,
            'default_cfg': DEFAULT_CFG,
            'default_seed': DEFAULT_SEED,
            'default_positive_prompt': DEFAULT_POSITIVE_PROMPT,
            'default_negative_prompt': DEFAULT_NEGATIVE_PROMPT,
            'skip_missing': SKIP_MISSING,
            'skip_existed': SKIP_EXISTED,
            'max_width': MAX_WIDTH,
            'max_height': MAX_HEIGHT,
            'min_width': MIN_WIDTH,      # ← NOWE!
            'min_height': MIN_HEIGHT,    # ← NOWE!
            'image_quality': IMAGE_QUALITY,
            'default_resolution': DEFAULT_RESOLUTION,
            'force_resolution': FORCE_RESOLUTION,
            'aspect_ratio_tolerance': ASPECT_RATIO_TOLERANCE,
            'aspect_ratio_strategy': ASPECT_RATIO_STRATEGY,
            'config_path': CONFIG_PATH,
            'workflows_path': WORKFLOWS_PATH,
            'comfyui_output_folder': COMFYUI_OUTPUT_FOLDER,
        }
        
        run_batch_generation_adv(config_transitions)
    
    if WYKONAJ_LACZENIE:
        from concat_videos import run_concat
        
        print("\n🎬 TRYB: Łączenie filmów\n")
        
        # TODO: Concat dla ADV mode
        # Musi wspierać FLOW (mieszane video + images + transitions)
        # Na razie concat działa tylko z prostą listą VIDEO_ORDER
        
        logger = Logger()
        logger.warning("Concat dla ADV mode - TODO!")
        logger.info("Na razie użyj manual concat w edytorze video")
    
    if not (WYKONAJ_TRANSITIONS or WYKONAJ_LACZENIE):
        print("\n⚠️  Wszystkie flagi wyłączone!")