# -*- coding: utf-8 -*-
"""
Batch Transition Generator - ADVANCED MODE
Zaawansowany silnik z FLOW (video + images, custom params per transition)
Nie edytuj tego pliku! Uzyj RUN_setup*.py dla konfiguracji.
"""

import os
import subprocess
import time
import shutil
from pathlib import Path
from PIL import Image
from collections import Counter
import statistics
from workflow_base import WorkflowRunner, Logger
from colorama import Fore, Style

# ============================================================
# FUNKCJE POMOCNICZE - PODSTAWOWE
# ============================================================

def check_ffmpeg():
    """Sprawdza czy ffmpeg jest zainstalowany"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def round_to_multiple(value, multiple=8):
    """Zaokragla do wielokrotnosci 8 (wymog modelu)"""
    return int(value // multiple * multiple)

def calculate_scaled_resolution(width, height, max_width, max_height):
    """Oblicza rozdzielczosc z zachowaniem proporcji + zaokraglenie do 8"""
    if width <= max_width and height <= max_height:
        return round_to_multiple(width), round_to_multiple(height)
    
    scale_w = max_width / width
    scale_h = max_height / height
    scale = min(scale_w, scale_h)
    
    new_width = round_to_multiple(width * scale)
    new_height = round_to_multiple(height * scale)
    
    return new_width, new_height

def adjust_frame_count_for_wan(frame_count):
    """
    Dostosowuje liczbe klatek do wymagan modelu WAN.
    Regula: length % 4 == 1
    """
    remainder = frame_count % 4
    
    if remainder == 1:
        return frame_count
    elif remainder == 0:
        return frame_count + 1
    elif remainder == 2:
        return frame_count - 1
    else:  # remainder == 3
        return frame_count + 2

# ============================================================
# FUNKCJE POMOCNICZE - PLIKI (VIDEO + IMAGES)
# ============================================================

def get_item_type(path):
    """
    Rozpoznaje czy to film czy zdjecie
    
    Returns:
        'video', 'image', lub 'unknown'
    """
    ext = path.suffix.lower()
    if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        return 'video'
    elif ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
        return 'image'
    else:
        return 'unknown'

def get_frame_filename(item_path, position):
    """Generuje nazwe pliku klatki"""
    item_stem = item_path.stem
    filename = f"{item_stem}_{position}.jpg"
    return filename

def get_image_resolution(image_path):
    """Pobiera rozdzielczosc obrazu"""
    try:
        with Image.open(image_path) as img:
            return img.size  # (width, height)
    except Exception:
        return None

def scale_image(image_path, target_width, target_height, image_quality=95):
    """Skaluje obraz do docelowej rozdzielczosci"""
    logger = Logger()
    
    try:
        with Image.open(image_path) as img:
            original_size = img.size
            
            if original_size == (target_width, target_height):
                return True
            
            logger.info(f"    Skalowanie {original_size[0]}x{original_size[1]} -> {target_width}x{target_height}")
            
            img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            img_resized.save(image_path, quality=image_quality, optimize=True)
            
            return True
            
    except Exception as e:
        logger.error(f"    Blad skalowania: {e}")
        return False

# ============================================================
# EKSTRAKCJA KLATEK (VIDEO + IMAGES)
# ============================================================

def extract_frame_from_video(video_path, output_path, position='last', image_quality=95):
    """
    Wyciaga klatke z filmu
    
    Args:
        video_path: Path do filmu
        output_path: Path gdzie zapisac klatke
        position: 'last' lub 'first'
        image_quality: Jakosc JPEG (0-100)
    
    Returns:
        True jezeli sukces, False jezeli blad
    """
    logger = Logger()
    
    if position == 'last':
        # REVERSE method - gwarantuje ostatnia klatke
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', 'reverse,select=eq(n\\,0)',
            '-vframes', '1',
            '-q:v', str(100 - image_quality),
            '-y', str(output_path)
        ]
    else:  # first
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', 'select=eq(n\\,0)',
            '-vframes', '1',
            '-q:v', str(100 - image_quality),
            '-y', str(output_path)
        ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    
    if result.returncode == 0:
        return True
    else:
        logger.error(f"  Blad ffmpeg: {result.stderr[:100]}")
        return False

def prepare_frame_from_image(image_path, output_path, target_resolution, image_quality=95):
    """
    Przygotowuje klatke ze zdjecia (kopiuje + skaluje)
    
    Args:
        image_path: Path do zdjecia
        output_path: Path gdzie zapisac klatke
        target_resolution: (width, height)
        image_quality: Jakosc JPEG (0-100)
    
    Returns:
        True jezeli sukces
    """
    try:
        with Image.open(image_path) as img:
            # Konwertuj do RGB (na wypadek RGBA, etc)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Skaluj do target resolution
            target_w, target_h = target_resolution
            img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Zapisz
            img_resized.save(output_path, quality=image_quality, optimize=True)
            
            return True
    except Exception as e:
        logger = Logger()
        logger.error(f"  Blad przygotowania obrazu: {e}")
        return False

def ensure_frame_exists(item_path, item_type, output_path, position, target_resolution, image_quality=95):
    """
    Zapewnia ze klatka istnieje (ZAWSZE nadpisuje - gwarantuje aktualnosc!)
    
    Args:
        item_path: Path do filmu/zdjecia
        item_type: 'video' lub 'image'
        output_path: Path gdzie zapisac klatke
        position: 'last' lub 'first' (tylko dla video)
        target_resolution: (width, height)
        image_quality: Jakosc JPEG
    
    Returns:
        True jezeli sukces
    """
    logger = Logger()
    
    if output_path.exists():
        logger.info(f"    Nadpisuje: {output_path.name}")
    else:
        logger.info(f"    Wyciaganie: {output_path.name}")
    
    if item_type == 'video':
        # Wyciagnij klatke z filmu
        if not extract_frame_from_video(item_path, output_path, position, image_quality):
            return False
    elif item_type == 'image':
        # Przygotuj klatke ze zdjecia
        if not prepare_frame_from_image(item_path, output_path, target_resolution, image_quality):
            return False
    else:
        logger.error(f"  Nieznany typ: {item_type}")
        return False
    
    logger.success(f"    ✓ {output_path.name}")
    
    return True

# ============================================================
# FLOW PARSING
# ============================================================

def resolve_prompt(prompt_value, prompt_type, generic_prompts, default_prompt):
    """
    Rozwiazuje prompt - obsluguje [generic], custom text, None
    
    Args:
        prompt_value: "[generic_name]", "custom text", lub None
        prompt_type: "pos" lub "neg"
        generic_prompts: Dict z GENERIC_PROMPTS
        default_prompt: Fallback prompt z defaults
    
    Returns:
        str: Resolved prompt
    """
    # None → użyj default
    if prompt_value is None:
        return default_prompt
    
    # [generic] → lookup
    if isinstance(prompt_value, str) and prompt_value.startswith("[") and prompt_value.endswith("]"):
        generic_name = prompt_value[1:-1]  # Usuń [ ]
        
        if generic_name not in generic_prompts:
            raise ValueError(f"Nieznany generic prompt: '{generic_name}'. Dostępne: {list(generic_prompts.keys())}")
        
        return generic_prompts[generic_name][prompt_type]
    
    # Custom text → użyj jak jest
    return prompt_value

def parse_flow_item(item, defaults, generic_prompts):
    """
    Parsuje jeden item z FLOW z fallback do defaults
    
    Args:
        item: Dict z FLOW
        defaults: Dict z wartościami domyślnymi
        generic_prompts: Dict z GENERIC_PROMPTS
    
    Returns:
        Dict z resolved values
    """
    # File (wymagane)
    if "file" not in item:
        raise ValueError(f"Item nie ma klucza 'file': {item}")
    
    file_path = item["file"]
    
    # Duration - fallback do default
    duration = item.get("duration", defaults["duration"])
    
    # FPS - fallback do default
    fps = item.get("fps", defaults["fps"])
    
    # Steps - fallback do default
    steps = item.get("steps", defaults["steps"])
    
    # CFG - fallback do default
    cfg = item.get("cfg", defaults["cfg"])
    
    # Seed - fallback do default
    seed = item.get("seed", defaults["seed"])
    
    # Prompty - resolve z generic lub custom
    pos_prompt = resolve_prompt(
        item.get("pos", None),
        "pos",
        generic_prompts,
        defaults["positive_prompt"]
    )
    
    neg_prompt = resolve_prompt(
        item.get("neg", None),
        "neg",
        generic_prompts,
        defaults["negative_prompt"]
    )
    
    return {
        "file": file_path,
        "duration": duration,
        "fps": fps,
        "steps": steps,
        "cfg": cfg,
        "seed": seed,
        "pos_prompt": pos_prompt,
        "neg_prompt": neg_prompt,
    }

def parse_flow(flow, defaults, generic_prompts):
    """
    Parsuje FLOW do listy items + skip_transitions
    
    Args:
        flow: Lista dict z {"file": ..., ...} lub {"break": True}
        defaults: Dict z wartościami domyślnymi
        generic_prompts: Dict z GENERIC_PROMPTS
    
    Returns:
        tuple: (items, skip_transitions)
    """
    items = []
    skip_transitions = set()
    
    for i, entry in enumerate(flow):
        # Sprawdź czy to break
        if entry.get("break", False):
            if items:
                skip_transitions.add(len(items) - 1)
            continue
        
        # Parsuj item z fallback
        try:
            parsed_item = parse_flow_item(entry, defaults, generic_prompts)
            items.append(parsed_item)
        except ValueError as e:
            raise ValueError(f"Błąd w FLOW entry [{i}]: {e}")
    
    return items, skip_transitions

# ============================================================
# WALIDACJA
# ============================================================

def validate_aspect_ratios(items, project_path, tolerance=0.1, strategy="most_common"):
    """
    Waliduje aspect ratio wszystkich plikow
    
    Args:
        items: Lista parsed items z FLOW
        project_path: Path do projektu
        tolerance: Dozwolona roznica AR (0.1 = ±10%)
        strategy: Strategia wyboru baseline AR:
            - "most_common" - najczęstszy AR (REKOMENDOWANE)
            - "first_video" - pierwszy film
            - "first" - pierwszy plik
            - "median" - mediana wszystkich AR
    
    Returns:
        tuple: (valid: bool, aspect_ratios: list)
    """
    logger = Logger()
    
    aspect_ratios = []
    
    for item in items:
        file_path = project_path / item["file"]
        
        if not file_path.exists():
            continue  # Skip missing (obsluzone przez SKIP_MISSING)
        
        item_type = get_item_type(file_path)
        
        if item_type == 'video':
            # Wyciągnij klatke tymczasowa
            temp_frame = project_path / f"temp_ar_check_{file_path.stem}.jpg"
            if extract_frame_from_video(file_path, temp_frame, 'first', 95):
                res = get_image_resolution(temp_frame)
                if res:
                    aspect_ratios.append((item["file"], res[0] / res[1], res))
                temp_frame.unlink()
        elif item_type == 'image':
            res = get_image_resolution(file_path)
            if res:
                aspect_ratios.append((item["file"], res[0] / res[1], res))
    
    if not aspect_ratios:
        return True, []
    
    # ========================================
    # WYBÓR BASELINE AR (STRATEGIA)
    # ========================================
    
    if strategy == "most_common":
        # Znajdź najczęstszy AR
        ar_values = [ar for _, ar, _ in aspect_ratios]
        ar_counter = Counter([round(ar, 3) for ar in ar_values])  # Zaokrąglij do 3 miejsc
        most_common_ar = ar_counter.most_common(1)[0][0]
        base_ar = most_common_ar
        logger.info(f"  Baseline AR (most_common): {base_ar:.3f} (występuje {ar_counter[most_common_ar]}x)")
    
    elif strategy == "first_video":
        # Pierwszy film
        base_ar = None
        for file_name, ar, res in aspect_ratios:
            # Sprawdź czy to video
            ext = Path(file_name).suffix.lower()
            if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                base_ar = ar
                logger.info(f"  Baseline AR (first_video): {base_ar:.3f} ({file_name})")
                break
        
        if base_ar is None:
            # Brak video - użyj pierwszego
            base_ar = aspect_ratios[0][1]
            logger.warning(f"  Brak video - użyto pierwszego pliku: {base_ar:.3f}")
    
    elif strategy == "median":
        # Mediana wszystkich AR
        ar_values = [ar for _, ar, _ in aspect_ratios]
        base_ar = statistics.median(ar_values)
        logger.info(f"  Baseline AR (median): {base_ar:.3f}")
    
    else:  # "first" (default)
        base_ar = aspect_ratios[0][1]
        logger.info(f"  Baseline AR (first): {base_ar:.3f} ({aspect_ratios[0][0]})")
    
    # ========================================
    # WALIDACJA względem baseline
    # ========================================
    
    valid = True
    
    for file_name, ar, res in aspect_ratios:
        diff = abs(ar - base_ar) / base_ar
        
        if diff > tolerance:
            logger.error(f"  {file_name}: AR={ar:.3f} ({res[0]}x{res[1]}) - różni się od bazowego {base_ar:.3f} o {diff*100:.1f}%")
            valid = False
        else:
            # Pokazuj tylko jeśli jest różnica
            if diff > 0.001:
                logger.info(f"  {file_name}: AR={ar:.3f} - różnica {diff*100:.1f}% (OK)")
    
    return valid, aspect_ratios

# ============================================================
# POMOCNICZE - TRANSITIONS
# ============================================================

def find_latest_video(output_folder, before_time=None):
    """Znajduje najnowszy plik video w folderze output ComfyUI"""
    output_path = Path(output_folder)
    
    if not output_path.exists():
        return None
    
    video_files = []
    for ext in ['.mp4', '.avi', '.mov', '.mkv']:
        video_files.extend(output_path.glob(f'*{ext}'))
    
    if not video_files:
        return None
    
    if before_time:
        video_files = [f for f in video_files if f.stat().st_mtime > before_time]
    
    if not video_files:
        return None
    
    latest = max(video_files, key=lambda f: f.stat().st_mtime)
    return latest

def rename_and_move_transition(source_file, dest_folder, item_a_stem, item_b_stem):
    """Przenosi i zmienia nazwe wygenerowanego przejscia"""
    logger = Logger()
    
    if not source_file or not source_file.exists():
        logger.error(f"  Plik zrodlowy nie istnieje: {source_file}")
        return None
    
    dest_path = Path(dest_folder)
    dest_path.mkdir(exist_ok=True)
    
    new_name = f"{item_a_stem}_{item_b_stem}_transition.mp4"
    dest_file = dest_path / new_name
    
    try:
        shutil.move(str(source_file), str(dest_file))
        logger.success(f"  Zapisano: {new_name}")
        return dest_file
        
    except Exception as e:
        logger.error(f"  Blad przenoszenia: {e}")
        return None

# ============================================================
# GLOWNA FUNKCJA
# ============================================================

def run_batch_generation_adv(config):
    """
    Glowna funkcja - ADVANCED mode z FLOW
    
    Args:
        config: Dictionary z parametrami konfiguracyjnymi
    """
    logger = Logger()
    
    logger.header("BATCH TRANSITION GENERATOR - ADVANCED MODE")
    
    # ------------------------------------------------------------
    # ROZPAKUJ CONFIG
    # ------------------------------------------------------------
    
    PROJECT_FOLDER = config['project_folder']
    FLOW = config['flow']
    GENERIC_PROMPTS = config.get('generic_prompts', {})
    
    # Defaults
    DEFAULTS = {
        'duration': config.get('default_duration', 4),
        'fps': config.get('default_fps', 16),
        'steps': config.get('default_steps', 20),
        'cfg': config.get('default_cfg', 4.0),
        'seed': config.get('default_seed', None),
        'positive_prompt': config.get('default_positive_prompt', ''),
        'negative_prompt': config.get('default_negative_prompt', ''),
    }
    
    SKIP_MISSING = config.get('skip_missing', True)
    SKIP_EXISTED = config.get('skip_existed', True)
    MAX_WIDTH = config.get('max_width', 600)
    MAX_HEIGHT = config.get('max_height', 900)
    IMAGE_QUALITY = config.get('image_quality', 95)
    
    # Aspect Ratio validation
    ASPECT_RATIO_TOLERANCE = config.get('aspect_ratio_tolerance', 0.05)
    ASPECT_RATIO_STRATEGY = config.get('aspect_ratio_strategy', 'most_common')
    
    # Resolution settings
    DEFAULT_RESOLUTION = config.get('default_resolution', (336, 448))
    FORCE_RESOLUTION = config.get('force_resolution', None)
    
    CONFIG_PATH = config.get('config_path', '')
    WORKFLOWS_PATH = config.get('workflows_path', '')
    COMFYUI_OUTPUT_FOLDER = config.get('comfyui_output_folder', '')
    
    # ------------------------------------------------------------
    # WALIDACJA
    # ------------------------------------------------------------
    
    if not check_ffmpeg():
        logger.error("ffmpeg nie znaleziony!")
        return
    
    logger.success("ffmpeg OK")
    
    project_path = Path(PROJECT_FOLDER)
    if not project_path.exists():
        logger.error(f"Folder nie istnieje: {PROJECT_FOLDER}")
        return
    
    logger.success(f"Projekt: {project_path.name}")
    
    # Walidacja resolution settings
    if FORCE_RESOLUTION:
        force_w, force_h = FORCE_RESOLUTION
        if force_w % 8 != 0 or force_h % 8 != 0:
            logger.error(f"FORCE_RESOLUTION musi być podzielna przez 8! Otrzymano: {force_w}x{force_h}")
            return
        logger.info(f"FORCE_RESOLUTION aktywne: {force_w}x{force_h}")
    
    if DEFAULT_RESOLUTION:
        def_w, def_h = DEFAULT_RESOLUTION
        if def_w % 8 != 0 or def_h % 8 != 0:
            logger.error(f"DEFAULT_RESOLUTION musi być podzielna przez 8! Otrzymano: {def_w}x{def_h}")
            return
    
    # ------------------------------------------------------------
    # PARSOWANIE FLOW
    # ------------------------------------------------------------
    
    logger.section("Parsowanie FLOW")
    
    try:
        items, skip_transitions = parse_flow(FLOW, DEFAULTS, GENERIC_PROMPTS)
    except ValueError as e:
        logger.error(f"Błąd parsowania FLOW: {e}")
        return
    
    logger.success(f"Znaleziono {len(items)} plików")
    logger.info(f"Breaks (hard cuts): {len(skip_transitions)}")
    
    if len(items) < 2:
        logger.error("FLOW musi mieć minimum 2 pliki!")
        return
    
    num_transitions = len(items) - 1 - len(skip_transitions)
    logger.info(f"Transitions do wygenerowania: {num_transitions}")
    
    # ------------------------------------------------------------
    # WERYFIKACJA PLIKOW
    # ------------------------------------------------------------
    
    logger.section(f"Weryfikacja {len(items)} plikow")
    
    existing_items = []
    missing = []
    
    for i, item in enumerate(items):
        file_path = project_path / item["file"]
        item_type = get_item_type(file_path)
        
        if file_path.exists():
            existing_items.append((i, item, file_path, item_type))
            
            type_icon = "🎬" if item_type == 'video' else "📷" if item_type == 'image' else "❓"
            print(f"  [{i:02d}] {type_icon} {item['file']}")
        else:
            missing.append(item["file"])
            print(f"  [{i:02d}] ❌ BRAK: {item['file']}")
    
    if missing:
        if SKIP_MISSING:
            logger.warning(f"\nBrakuje {len(missing)} plikow - POMIJAM")
            for m in missing:
                print(f"  > {m}")
        else:
            logger.error(f"\nBrakuje {len(missing)} plikow!")
            return
    
    if len(existing_items) < 2:
        logger.error(f"Potrzeba minimum 2 pliki, znaleziono: {len(existing_items)}")
        return
    
    logger.success(f"Pliki OK! ({len(existing_items)} znalezionych)")
    
    # ------------------------------------------------------------
    # WALIDACJA ASPECT RATIO
    # ------------------------------------------------------------
    
    logger.section("Walidacja aspect ratio")
    
    valid_ar, aspect_ratios = validate_aspect_ratios(
        items, 
        project_path, 
        tolerance=ASPECT_RATIO_TOLERANCE,
        strategy=ASPECT_RATIO_STRATEGY
    )
    
    if aspect_ratios:
        print(f"  Znaleziono {len(aspect_ratios)} plikow:")
        for file_name, ar, res in aspect_ratios:
            ar_type = "landscape" if ar > 1 else "portrait" if ar < 1 else "square"
            print(f"    {file_name}: {res[0]}x{res[1]} (AR={ar:.3f}, {ar_type})")
    
    if not valid_ar:
        logger.error("\nRozne aspect ratio! Wszystkie pliki musza miec podobne proporcje.")
        logger.error("Popraw pliki (crop/resize) LUB zwieksz ASPECT_RATIO_TOLERANCE w setupie.")
        return
    
    logger.success("Aspect ratio OK - wszystkie pliki podobne")
    
    # ------------------------------------------------------------
    # EKSTRAKCJA KLATEK
    # ------------------------------------------------------------
    
    logger.header("EKSTRAKCJA KLATEK")
    
    frames_folder = project_path / "frames"
    frames_folder.mkdir(exist_ok=True)
    
    # ========================================
    # AUTO-DETECT ROZDZIELCZOŚCI
    # ========================================
    
    logger.section("Auto-wykrywanie rozdzielczosci")
    
    if FORCE_RESOLUTION:
        # Wymuszona rozdzielczość - pomiń auto-detect
        target_w, target_h = FORCE_RESOLUTION
        target_resolution = (target_w, target_h)
        logger.info(f"  FORCE_RESOLUTION: {target_w}x{target_h} (auto-detect pominięty)")
        
    else:
        # Auto-detect: Preferuj pierwszy VIDEO
        first_video = None
        for item_idx, item_data, item_path, item_type in existing_items:
            if item_type == 'video':
                first_video = (item_data, item_path)
                logger.info(f"  Reference: {item_data['file']} (pierwszy video)")
                break
        
        if first_video:
            # Użyj rozdzielczości z video
            item_data, item_path = first_video
            temp_frame = project_path / "temp_resolution_check.jpg"
            extract_frame_from_video(item_path, temp_frame, 'first', IMAGE_QUALITY)
            original_resolution = get_image_resolution(temp_frame)
            temp_frame.unlink()
            
            if not original_resolution:
                logger.error("Nie mozna wykryc rozdzielczosci z video!")
                return
            
            orig_w, orig_h = original_resolution
            target_w, target_h = calculate_scaled_resolution(orig_w, orig_h, MAX_WIDTH, MAX_HEIGHT)
            target_resolution = (target_w, target_h)
            
            print(f"  Oryginalna (video): {orig_w}x{orig_h}")
            print(f"  Docelowa: {target_w}x{target_h}")
            
            if (orig_w, orig_h) != (target_w, target_h):
                logger.warning(f"  Bedzie skalowanie (limit: {MAX_WIDTH}x{MAX_HEIGHT})")
            
        else:
            # Brak video - użyj DEFAULT_RESOLUTION
            target_w, target_h = DEFAULT_RESOLUTION
            target_resolution = (target_w, target_h)
            logger.warning(f"  Brak video w FLOW - użyto DEFAULT_RESOLUTION: {target_w}x{target_h}")
            logger.info(f"  Wszystkie obrazki zostaną przeskalowane do tej rozdzielczości")
    
    # Upewnij się że jest podzielna przez 8
    target_w = round_to_multiple(target_w, 8)
    target_h = round_to_multiple(target_h, 8)
    target_resolution = (target_w, target_h)
    
    logger.success(f"  Finalna rozdzielczość: {target_w}x{target_h}")
    
    # Przygotuj pary klatek
    logger.section(f"Przygotowanie klatek (ZAWSZE swieze!)")
    
    start_extract_time = time.time()
    
    frame_pairs = []
    total_frames_extracted = 0
    
    # Iteruj przez istniejące items (pomijając brakujące)
    for idx in range(len(existing_items) - 1):
        i_a, item_a, path_a, type_a = existing_items[idx]
        i_b, item_b, path_b, type_b = existing_items[idx + 1]
        
        # Sprawdź czy to nie jest break
        if i_a in skip_transitions:
            logger.info(f"\n  BREAK po [{i_a}] {item_a['file']} - pomijam transition")
            continue
        
        print(f"\n  [{idx+1}] {item_a['file']} → {item_b['file']}")
        
        # End frame z A
        if type_a == 'video':
            end_frame_name = get_frame_filename(path_a, 'end')
            end_frame_path = frames_folder / end_frame_name
            
            end_ok = ensure_frame_exists(path_a, type_a, end_frame_path, 'last', target_resolution, IMAGE_QUALITY)
        else:  # image
            end_frame_name = get_frame_filename(path_a, 'end')
            end_frame_path = frames_folder / end_frame_name
            
            end_ok = ensure_frame_exists(path_a, type_a, end_frame_path, None, target_resolution, IMAGE_QUALITY)
        
        # Start frame z B
        if type_b == 'video':
            start_frame_name = get_frame_filename(path_b, 'start')
            start_frame_path = frames_folder / start_frame_name
            
            start_ok = ensure_frame_exists(path_b, type_b, start_frame_path, 'first', target_resolution, IMAGE_QUALITY)
        else:  # image
            start_frame_name = get_frame_filename(path_b, 'start')
            start_frame_path = frames_folder / start_frame_name
            
            start_ok = ensure_frame_exists(path_b, type_b, start_frame_path, None, target_resolution, IMAGE_QUALITY)
        
        if not (end_ok and start_ok):
            logger.error(f"  Blad ekstrakcji klatek")
            continue
        
        total_frames_extracted += 2
        
        frame_pairs.append({
            'id': idx,
            'item_a': item_a,
            'item_b': item_b,
            'end_frame': end_frame_path,
            'start_frame': start_frame_path,
            'from_name': path_a.stem,
            'to_name': path_b.stem,
        })
    
    extract_elapsed = time.time() - start_extract_time
    
    logger.success(f"\nWszystkie klatki gotowe!")
    print(f"  Wyciagniete: {total_frames_extracted}")
    print(f"  Czas ekstrakcji: {extract_elapsed:.1f}s")
    print(f"  Lokalizacja: {frames_folder}")
    
    if len(frame_pairs) == 0:
        logger.warning("Brak transitions do wygenerowania!")
        return
    
    # ------------------------------------------------------------
    # PODSUMOWANIE PRZED GENERACJA
    # ------------------------------------------------------------
    
    logger.header("GENERACJA PRZEJSC")
    
    transitions_folder = project_path / "transitions"
    transitions_folder.mkdir(exist_ok=True)
    
    logger.section("Podsumowanie konfiguracji")
    print(f"  Projekt: {project_path.name}")
    print(f"  Plikow: {len(existing_items)}")
    print(f"  Przejsc: {len(frame_pairs)}")
    print(f"  Rozdzielczosc: {target_w}x{target_h}")
    if FORCE_RESOLUTION:
        print(f"  Resolution mode: FORCE (wymuszona)")
    else:
        if first_video:
            print(f"  Resolution mode: AUTO (z pierwszego video)")
        else:
            print(f"  Resolution mode: DEFAULT (brak video)")
    print(f"  Defaults: FPS={DEFAULTS['fps']}, Steps={DEFAULTS['steps']}, CFG={DEFAULTS['cfg']}")
    print(f"  Skip existed: {SKIP_EXISTED}")
    print(f"  AR tolerance: {ASPECT_RATIO_TOLERANCE*100:.0f}% ({ASPECT_RATIO_STRATEGY})")
    print(f"  Folder klatek: {frames_folder}")
    print(f"  Folder przejsc: {transitions_folder}")
    
    # Szacowany czas
    total_frames = sum(pair['item_a']['fps'] * pair['item_a']['duration'] for pair in frame_pairs)
    estimated_min = len(frame_pairs) * 10
    print(f"  Lacznie klatek: {total_frames}")
    print(f"  Szacowany czas: ~{estimated_min//60}h {estimated_min%60}min")
    
    # ------------------------------------------------------------
    # PRE-CHECK: Sprawdź które transitions już istnieją
    # ------------------------------------------------------------
    
    if SKIP_EXISTED:
        logger.section("Pre-check: Sprawdzanie istniejących transitions")
        
        to_generate = []
        already_exist = []
        
        for pair in frame_pairs:
            output_name = f"{pair['from_name']}_{pair['to_name']}_transition.mp4"
            output_path = transitions_folder / output_name
            
            if output_path.exists():
                already_exist.append((pair['id'], output_name))
            else:
                to_generate.append((pair['id'], output_name, pair))
        
        if already_exist:
            logger.warning(f"Znaleziono {len(already_exist)} istniejących transitions:")
            for tid, name in already_exist:
                print(f"  [{tid:02d}] ⏭️  {name}")
        
        if to_generate:
            logger.section(f"Do wygenerowania: {len(to_generate)} transitions")
            for tid, name, pair in to_generate:
                duration = pair['item_a']['duration']
                print(f"  [{tid:02d}] 🎬 {name} ({duration}s)")
            
            estimated_min = len(to_generate) * 10
            print(f"\n  Szacowany czas: ~{estimated_min//60}h {estimated_min%60}min")
        else:
            logger.success("Wszystkie transitions już istnieją!")
            logger.info("Ustaw SKIP_EXISTED = False lub skasuj wybrane transitions")
            return
    else:
        logger.section("Lista przejsc do wygenerowania")
        for pair in frame_pairs:
            output_name = f"{pair['from_name']}_{pair['to_name']}_transition.mp4"
            duration = pair['item_a']['duration']
            print(f"  [{pair['id']:02d}] {output_name} ({duration}s)")
    
    # Wyświetl custom params
    logger.section("Przegląd parametrów custom")
    
    has_custom = False
    for pair in frame_pairs:
        item_a = pair['item_a']
        custom_params = []
        
        if item_a['duration'] != DEFAULTS['duration']:
            custom_params.append(f"duration={item_a['duration']}")
        if item_a['fps'] != DEFAULTS['fps']:
            custom_params.append(f"fps={item_a['fps']}")
        if item_a['steps'] != DEFAULTS['steps']:
            custom_params.append(f"steps={item_a['steps']}")
        if item_a['cfg'] != DEFAULTS['cfg']:
            custom_params.append(f"cfg={item_a['cfg']}")
        if item_a['seed'] != DEFAULTS['seed']:
            custom_params.append(f"seed={item_a['seed']}")
        
        if custom_params:
            has_custom = True
            print(f"  [{pair['id']:02d}] {item_a['file']}: {', '.join(custom_params)}")
    
    if not has_custom:
        print(f"  (wszystkie używają defaults)")
    
    response = input(f"\n{Fore.YELLOW}Nacisnij ENTER aby rozpoczac (lub 'q' aby anulowac): {Style.RESET_ALL}")
    
    if response.lower() in ['q', 'quit', 'exit', 'n', 'no']:
        logger.warning("\nAnulowano")
        return
    
    logger.info("Rozpoczynam generacje...\n")
    
    # ------------------------------------------------------------
    # PETLA GENERACJI
    # ------------------------------------------------------------
    
    logger.header(f"GENEROWANIE PRZEJSC")
    
    successful = 0
    failed = 0
    skipped = 0
    start_time = time.time()
    
    for pair in frame_pairs:
        transition_num = pair['id'] + 1
        
        output_name = f"{pair['from_name']}_{pair['to_name']}_transition.mp4"
        output_path = transitions_folder / output_name
        
        if SKIP_EXISTED and output_path.exists():
            logger.warning(f"\n  PRZEJSCIE [{transition_num}] - JUZ ISTNIEJE - POMIJAM")
            print(f"  Plik: {output_name}")
            skipped += 1
            continue
        
        item_a = pair['item_a']
        
        logger.section(f"PRZEJSCIE [{transition_num}]")
        print(f"  Od: {item_a['file']}")
        print(f"  Do: {pair['item_b']['file']}")
        print(f"  Duration: {item_a['duration']}s")
        print(f"  FPS: {item_a['fps']}")
        print(f"  Steps: {item_a['steps']}")
        print(f"  CFG: {item_a['cfg']}")
        print(f"  Seed: {item_a['seed'] if item_a['seed'] else 'random'}")
        print(f"  Pos: {item_a['pos_prompt'][:60]}...")
        print(f"  Neg: {item_a['neg_prompt'][:60]}...")
        
        try:
            time_before_generation = time.time()
            
            runner = WorkflowRunner(
                config_path=CONFIG_PATH,
                workflows_base_path=WORKFLOWS_PATH
            )
            
            runner.set_image(str(pair['end_frame']), "start_image")
            runner.set_image(str(pair['start_frame']), "end_image")
            runner.set_prompt(item_a['pos_prompt'], "positive_prompt")
            runner.set_prompt(item_a['neg_prompt'], "negative_prompt")
            
            base_length = item_a['fps'] * item_a['duration']
            final_length = adjust_frame_count_for_wan(base_length)
            
            if base_length != final_length:
                logger.info(f"    Dostosowano klatki: {base_length} -> {final_length} (WAN rule)")
            
            runner.set_video_params(
                width=target_w,
                height=target_h,
                fps=item_a['fps'],
                length=final_length
            )
            
            runner.set_sampling_params(
                steps=item_a['steps'],
                cfg=item_a['cfg'],
                seed=item_a['seed']
            )
            
            print(f"\n  Rozpoczynam generacje...\n")
            
            result = runner.run(wait_for_completion=True)
            
            if result:
                logger.info(f"\n  Szukam wygenerowanego pliku...")
                latest_video = find_latest_video(COMFYUI_OUTPUT_FOLDER, before_time=time_before_generation)
                
                if latest_video:
                    logger.success(f"  Znaleziono: {latest_video.name}")
                    
                    moved_file = rename_and_move_transition(
                        latest_video,
                        transitions_folder,
                        pair['from_name'],
                        pair['to_name']
                    )
                    
                    if moved_file:
                        successful += 1
                        logger.success(f"\n  PRZEJSCIE [{transition_num}] GOTOWE!")
                        logger.success(f"  Lokalizacja: {moved_file.relative_to(project_path)}")
                    else:
                        failed += 1
                        logger.error(f"\n  Blad przenoszenia")
                else:
                    failed += 1
                    logger.error(f"\n  Nie znaleziono wygenerowanego pliku!")
            else:
                failed += 1
                logger.error(f"\n  NIEUDANE")
        
        except Exception as e:
            failed += 1
            logger.error(f"\n  WYJATEK: {e}")
            import traceback
            traceback.print_exc()
        
        # Postep
        elapsed = time.time() - start_time
        processed = successful + failed + skipped
        total_to_process = len(frame_pairs)
        avg_time = elapsed / processed if processed > 0 else 0
        remaining = avg_time * (total_to_process - processed)
        
        logger.section("POSTEP")
        print(f"  Przetworzone: {processed}/{total_to_process}")
        print(f"  Ukonczone: {successful}")
        print(f"  Pominiete: {skipped}")
        print(f"  Nieudane: {failed}")
        print(f"  Czas: {elapsed/60:.1f}min")
        print(f"  Pozostalo: ~{remaining/60:.1f}min")
        print(f"  Procent: {(processed/total_to_process)*100:.1f}%")
        print()
    
    # ------------------------------------------------------------
    # FINALNE PODSUMOWANIE
    # ------------------------------------------------------------
    
    total_time = time.time() - start_time
    
    logger.header("FINALNE PODSUMOWANIE")
    print(f"  Projekt: {project_path.name}")
    print(f"  Transitions total: {len(frame_pairs)}")
    print(f"  Nowo wygenerowane: {successful}")
    print(f"  Pominiete: {skipped}")
    print(f"  Nieudane: {failed}")
    print(f"  Czas: {total_time/3600:.2f}h ({total_time/60:.1f}min)")
    print(f"  Lokalizacja klatek: {frames_folder}")
    print(f"  Lokalizacja transitions: {transitions_folder}")
    
    total_ok = successful + skipped
    
    if total_ok == len(frame_pairs) and failed == 0:
        logger.success("\nWszystkie transitions dostepne!")
        if skipped > 0:
            logger.info(f"  ({skipped} bylo juz wczesniej)")
    elif successful > 0:
        logger.warning(f"\nWygenerowano: {successful}, Pominieto: {skipped}, Nieudane: {failed}")
        if failed > 0:
            logger.warning("Sprawdz logi i uruchom ponownie")
    else:
        if skipped == len(frame_pairs):
            logger.success("\nWszystkie juz istnialy")
        else:
            logger.error("\nBrak udanych generacji")