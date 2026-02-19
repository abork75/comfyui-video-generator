# -*- coding: utf-8 -*-
"""
Batch Transition Generator - Engine
Nie edytuj tego pliku! Uzyj RUN_setup*.py dla konfiguracji.

CHANGELOG:
- 2026-02-08: Dodano MIN_WIDTH/MIN_HEIGHT dla wymuszenia upscalingu
- 2026-02-08: Dodano walidację MIN <= MAX
"""

import os
import subprocess
import time
import shutil
from pathlib import Path
from PIL import Image
from workflow_base import WorkflowRunner, Logger
from colorama import Fore, Style

# ============================================================
# FUNKCJE POMOCNICZE
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

def calculate_scaled_resolution(width, height, max_width, max_height, min_width=None, min_height=None):
    """
    Oblicza rozdzielczosc z zachowaniem proporcji + zaokraglenie do 8
    
    NOWE (2026-02-08): Wspiera MIN_WIDTH/MIN_HEIGHT dla wymuszenia upscalingu
    
    Args:
        width: Szerokość źródłowa
        height: Wysokość źródłowa
        max_width: Maksymalna szerokość (upper limit)
        max_height: Maksymalna wysokość (upper limit)
        min_width: Minimalna szerokość (force upscaling jeśli mniejsze) - opcjonalne
        min_height: Minimalna wysokość (force upscaling jeśli mniejsze) - opcjonalne
    
    Returns:
        (width, height): Tuple z docelową rozdzielczością
    
    Logika:
        1. Jeśli źródło < minimum → upscale DO minimum (zachowując proporcje)
        2. Jeśli wynik > maximum → downscale DO maximum (zachowując proporcje)
        3. Zaokrąglenie do wielokrotności 8
    """
    
    # ========================================
    # KROK 1: Force upscaling jeśli za małe
    # ========================================
    if min_width is not None or min_height is not None:
        # Użyj 0 jeśli nie podano (żeby nie wymuszać)
        min_w = min_width if min_width is not None else 0
        min_h = min_height if min_height is not None else 0
        
        if width < min_w or height < min_h:
            # Oblicz scale factor żeby oba wymiary >= minimum
            scale_w = min_w / width if width < min_w else 1.0
            scale_h = min_h / height if height < min_h else 1.0
            scale = max(scale_w, scale_h)  # Wybierz większy scale
            
            width = int(width * scale)
            height = int(height * scale)
            
            # Debug info (zostanie wyświetlone przez logger w głównej funkcji)
    
    # ========================================
    # KROK 2: Skaluj w dół jeśli > maximum
    # ========================================
    if width <= max_width and height <= max_height:
        # Mieści się w limitach - tylko zaokrąglij
        return round_to_multiple(width), round_to_multiple(height)
    
    # Przekracza limity - skaluj w dół
    scale_w = max_width / width
    scale_h = max_height / height
    scale = min(scale_w, scale_h)  # Wybierz mniejszy scale (żeby oba <= max)
    
    new_width = round_to_multiple(width * scale)
    new_height = round_to_multiple(height * scale)
    
    return new_width, new_height

def get_frame_filename(video_path, position, transition_id=None):
    """
    Generuje nazwe pliku klatki bazujac na nazwie filmu
    
    Args:
        video_path: Path do filmu
        position: 'end' lub 'start'
        transition_id: Numer przejscia (nie uzywany, zachowany dla kompatybilnosci)
    
    Returns:
        Nazwa pliku: "01.13. slave1_end.jpg"
    """
    video_stem = video_path.stem
    filename = f"{video_stem}_{position}.jpg"
    return filename

def extract_frame(video_path, output_path, position='last', image_quality=95):
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
        # REVERSE method - gwarantuje rzeczywista ostatnia klatke
        # reverse = odwraca kolejnosc klatek
        # select=eq(n,0) = wybiera pierwsza klatke odwroconego filmu (= ostatnia oryginalna)
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', 'reverse,select=eq(n\\,0)',
            '-vframes', '1',
            '-q:v', str(100 - image_quality),
            '-y', str(output_path)
        ]
    else:  # first
        # SELECT first frame (standardowa metoda)
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

def adjust_frame_count_for_wan(frame_count):
    """
    Dostosowuje liczbe klatek do wymagan modelu WAN.
    Regula: length % 4 == 1
    
    Args:
        frame_count: Poczatkowa liczba klatek (FPS * duration)
    
    Returns:
        int: Dostosowana liczba klatek
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

def ensure_frame_exists(video_path, output_path, position, target_resolution=None, image_quality=95):
    """
    Wyciaga klatke z filmu (ZAWSZE nadpisuje - gwarantuje aktualnosc!)
    
    WAZNE: Zawsze wyciaga klatki na nowo, nawet jesli istnieja.
    Dlaczego? Gwarantuje zgodnosc z aktualnym filmem (np. po edycji/przycianiu).
    Ekstrakcja klatek = sekundy, generacja transitions = godziny.
    Lepiej stracic 20 sekund niz generowac z blednych klatek!
    
    Args:
        video_path: Path do filmu
        output_path: Path gdzie zapisac klatke
        position: 'last' lub 'first'
        target_resolution: (width, height) lub None
        image_quality: Jakosc JPEG
    
    Returns:
        True jezeli sukces, False jezeli blad
    """
    logger = Logger()
    
    # ZAWSZE wyciagaj na nowo (gwarantuje zgodnosc z filmem)
    if output_path.exists():
        logger.info(f"    Nadpisuje: {output_path.name}")
    else:
        logger.info(f"    Wyciaganie: {output_path.name}")
    
    if not extract_frame(video_path, output_path, position, image_quality):
        return False
    
    logger.success(f"    ✓ {output_path.name}")
    
    if target_resolution:
        scale_image(output_path, *target_resolution, image_quality)
    
    return True

def find_latest_video(output_folder, before_time=None):
    """
    Znajduje najnowszy plik video w folderze output ComfyUI
    
    Args:
        output_folder: Folder gdzie ComfyUI zapisuje filmy
        before_time: Timestamp - szuka plikow nowszych niz ten czas
    
    Returns:
        Path do najnowszego pliku lub None
    """
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

def rename_and_move_transition(source_file, dest_folder, video_a_stem, video_b_stem):
    """
    Przenosi i zmienia nazwe wygenerowanego przejscia
    
    Args:
        source_file: Path do wygenerowanego pliku
        dest_folder: Folder docelowy (transitions)
        video_a_stem: Nazwa pierwszego filmu (bez rozszerzenia)
        video_b_stem: Nazwa drugiego filmu (bez rozszerzenia)
    
    Returns:
        Path do przeniesionego pliku lub None
    """
    logger = Logger()
    
    if not source_file or not source_file.exists():
        logger.error(f"  Plik zrodlowy nie istnieje: {source_file}")
        return None
    
    dest_path = Path(dest_folder)
    dest_path.mkdir(exist_ok=True)
    
    new_name = f"{video_a_stem}_{video_b_stem}_transition.mp4"
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

def run_batch_generation(config):
    """
    Glowna funkcja - ekstrakcja klatek + generacja przejsc
    
    Args:
        config: Dictionary z parametrami konfiguracyjnymi
        
    NOWE parametry (2026-02-08):
        min_width: Minimalna szerokość (force upscaling) - opcjonalne
        min_height: Minimalna wysokość (force upscaling) - opcjonalne
    """
    logger = Logger()
    
    # Rozpakuj konfiguracje
    PROJECT_FOLDER = config['project_folder']
    VIDEO_ORDER = config['video_order']
    FRAME_ONLY = config.get('frame_only', False)
    SKIP_MISSING = config.get('skip_missing', True)
    SKIP_EXISTED = config.get('skip_existed', True)
    MAX_WIDTH = config.get('max_width', 600)
    MAX_HEIGHT = config.get('max_height', 900)
    MIN_WIDTH = config.get('min_width', None)      # ← NOWE!
    MIN_HEIGHT = config.get('min_height', None)    # ← NOWE!
    IMAGE_QUALITY = config.get('image_quality', 95)
    DURATION_SEC = config.get('duration_sec', 2)
    DURATION_VECTOR = config.get('duration_vector', None)
    FPS = config.get('fps', 16)
    STEPS = config.get('steps', 20)
    CFG = config.get('cfg', 4.0)
    SEED = config.get('seed', None)
    POSITIVE_PROMPT = config.get('positive_prompt', '')
    NEGATIVE_PROMPT = config.get('negative_prompt', '')
    CONFIG_PATH = config.get('config_path', '')
    WORKFLOWS_PATH = config.get('workflows_path', '')
    COMFYUI_OUTPUT_FOLDER = config.get('comfyui_output_folder', '')
    
    if FRAME_ONLY:
        logger.header("FRAME EXTRACTION ONLY MODE")
    else:
        logger.header("BATCH TRANSITION GENERATOR - ALL-IN-ONE")
    
    # ============================================================
    # WALIDACJA PARAMETRÓW RESOLUTION - NOWE! (2026-02-08)
    # ============================================================
    
    if MIN_WIDTH is not None and MIN_WIDTH > MAX_WIDTH:
        logger.error(f"BLAD KONFIGURACJI!")
        logger.error(f"  MIN_WIDTH ({MIN_WIDTH}) > MAX_WIDTH ({MAX_WIDTH})")
        logger.error(f"")
        logger.error(f"Rozwiazanie:")
        logger.error(f"  1. Zwieksz MAX_WIDTH do co najmniej {MIN_WIDTH}")
        logger.error(f"  2. Lub zmniejsz MIN_WIDTH do max {MAX_WIDTH}")
        logger.error(f"  3. Lub ustaw MIN_WIDTH = None (bez minimum)")
        logger.error(f"")
        logger.error(f"Przyklad poprawnej konfiguracji:")
        logger.error(f"  MIN_WIDTH = 672")
        logger.error(f"  MAX_WIDTH = 1200  # >= MIN_WIDTH")
        return
    
    if MIN_HEIGHT is not None and MIN_HEIGHT > MAX_HEIGHT:
        logger.error(f"BLAD KONFIGURACJI!")
        logger.error(f"  MIN_HEIGHT ({MIN_HEIGHT}) > MAX_HEIGHT ({MAX_HEIGHT})")
        logger.error(f"")
        logger.error(f"Rozwiazanie:")
        logger.error(f"  1. Zwieksz MAX_HEIGHT do co najmniej {MIN_HEIGHT}")
        logger.error(f"  2. Lub zmniejsz MIN_HEIGHT do max {MAX_HEIGHT}")
        logger.error(f"  3. Lub ustaw MIN_HEIGHT = None (bez minimum)")
        logger.error(f"")
        logger.error(f"Przyklad poprawnej konfiguracji:")
        logger.error(f"  MIN_HEIGHT = 896")
        logger.error(f"  MAX_HEIGHT = 1800  # >= MIN_HEIGHT")
        return
    
    # ============================================================
    # WALIDACJA - ffmpeg, folder, filmy
    # ============================================================
    
    if not check_ffmpeg():
        logger.error("ffmpeg nie znaleziony! Zainstaluj: https://ffmpeg.org/download.html")
        return
    
    logger.success("ffmpeg OK")
    
    project_path = Path(PROJECT_FOLDER)
    if not project_path.exists():
        logger.error(f"Folder nie istnieje: {PROJECT_FOLDER}")
        return
    
    logger.success(f"Projekt: {project_path.name}")
    
    # Sprawdz filmy
    logger.section(f"Weryfikacja {len(VIDEO_ORDER)} filmow")
    
    videos = []
    missing = []
    
    for i, video_name in enumerate(VIDEO_ORDER):
        video_path = project_path / video_name
        if video_path.exists():
            videos.append(video_path)
            print(f"  [{i:02d}] OK {video_name}")
        else:
            missing.append(video_name)
            print(f"  [{i:02d}] BRAK: {video_name}")
    
    if missing:
        if SKIP_MISSING:
            logger.warning(f"\nBrakuje {len(missing)} plikow - POMIJAM (SKIP_MISSING=True)")
            for m in missing:
                print(f"  > {m}")
        else:
            logger.error(f"\nBrakuje {len(missing)} plikow!")
            for m in missing:
                print(f"  - {m}")
            return
    
    if len(videos) < 2:
        logger.error(f"Potrzeba minimum 2 filmow, znaleziono: {len(videos)}")
        return
    
    num_transitions = len(videos) - 1
    logger.success(f"\nFilmy OK! Przejsc do wygenerowania: {num_transitions}")
    
    # ------------------------------------------------------------
    # DLUGOSCI PRZEJSC
    # ------------------------------------------------------------
    
    if DURATION_VECTOR is not None:
        if len(DURATION_VECTOR) != num_transitions:
            logger.error(f"DURATION_VECTOR ma {len(DURATION_VECTOR)} elementow, potrzeba {num_transitions}!")
            return
        durations = DURATION_VECTOR
        logger.info(f"Dlugosci: wektor (osobne dla kazdego)")
    else:
        durations = [DURATION_SEC] * num_transitions
        logger.info(f"Dlugosci: {DURATION_SEC}s dla wszystkich")
    
    # ------------------------------------------------------------
    # EKSTRAKCJA KLATEK
    # ------------------------------------------------------------
    
    logger.header("EKSTRAKCJA KLATEK")
    
    # Stworz folder frames
    frames_folder = project_path / "frames"
    frames_folder.mkdir(exist_ok=True)
    
    logger.section("Auto-wykrywanie rozdzielczosci")
    
    temp_frame = project_path / "temp_resolution_check.jpg"
    extract_frame(videos[0], temp_frame, 'last', IMAGE_QUALITY)
    
    original_resolution = get_image_resolution(temp_frame)
    
    if not original_resolution:
        logger.error("Nie mozna wykryc rozdzielczosci!")
        return
    
    orig_w, orig_h = original_resolution
    
    # ========================================
    # Użyj MIN_WIDTH/MIN_HEIGHT
    # ========================================
    target_w, target_h = calculate_scaled_resolution(
        orig_w, orig_h, 
        MAX_WIDTH, MAX_HEIGHT,
        MIN_WIDTH, MIN_HEIGHT
    )
    target_resolution = (target_w, target_h)
    
    print(f"  Oryginalna: {orig_w}x{orig_h}")
    print(f"  Docelowa: {target_w}x{target_h}")
    
    # ========================================
    # Wyświetl info o skalowaniu
    # ========================================
    if (orig_w, orig_h) != (target_w, target_h):
        if target_w > orig_w or target_h > orig_h:
            # Upscaling
            scale_factor = target_w / orig_w
            pixels_orig = orig_w * orig_h
            pixels_target = target_w * target_h
            pixels_increase = (pixels_target / pixels_orig)
            
            logger.warning(f"  Upscaling {scale_factor:.2f}x ({pixels_increase:.1f}x więcej pikseli)")
            logger.info(f"  Powód: wymuszenie minimum {MIN_WIDTH}x{MIN_HEIGHT}")
            logger.info(f"  Piksele: {pixels_orig:,} → {pixels_target:,}")
        else:
            # Downscaling
            scale_factor = target_w / orig_w
            logger.warning(f"  Downscaling {scale_factor:.2f}x")
            logger.info(f"  Powód: przekroczenie limitu {MAX_WIDTH}x{MAX_HEIGHT}")
    else:
        logger.success(f"  Bez skalowania (w limitach)")
    
    temp_frame.unlink()
    
    # Przygotuj pary klatek
    logger.section(f"Przygotowanie {num_transitions} par klatek (ZAWSZE swieze!)")
    
    start_extract_time = time.time()
    
    frame_pairs = []
    total_frames_extracted = 0
    
    for i in range(num_transitions):
        video_a = videos[i]
        video_b = videos[i + 1]
        
        print(f"\n  [{i+1}/{num_transitions}] {video_a.stem} -> {video_b.stem}")
        
        end_frame_name = get_frame_filename(video_a, 'end', i)
        start_frame_name = get_frame_filename(video_b, 'start', i)
        
        # Klatki w podfolderze frames/
        end_frame_path = frames_folder / end_frame_name
        start_frame_path = frames_folder / start_frame_name
        
        print(f"    Klatki: {end_frame_name} + {start_frame_name}")
        
        # ZAWSZE wyciagaj na nowo (nie ma skip!)
        end_ok = ensure_frame_exists(video_a, end_frame_path, 'last', target_resolution, IMAGE_QUALITY)
        start_ok = ensure_frame_exists(video_b, start_frame_path, 'first', target_resolution, IMAGE_QUALITY)
        
        if not (end_ok and start_ok):
            logger.error(f"  Blad ekstrakcji klatek dla przejscia {i}")
            continue
        
        total_frames_extracted += 2
        
        frame_pairs.append({
            'id': i,
            'end_frame': end_frame_path,
            'start_frame': start_frame_path,
            'from_video': video_a.stem,
            'to_video': video_b.stem,
            'duration': durations[i]
        })
    
    extract_elapsed = time.time() - start_extract_time
    
    if len(frame_pairs) != num_transitions:
        logger.error(f"\nPrzygotowano tylko {len(frame_pairs)}/{num_transitions} par!")
        return
    
    logger.success(f"\nWszystkie klatki gotowe!")
    print(f"  Wyciagniete: {total_frames_extracted}")
    print(f"  Czas ekstrakcji: {extract_elapsed:.1f}s")
    print(f"  Lokalizacja: {frames_folder}")
    
    # ------------------------------------------------------------
    # TRYB FRAME_ONLY
    # ------------------------------------------------------------
    
    if FRAME_ONLY:
        logger.header("FRAME EXTRACTION COMPLETE")
        
        logger.section("Wyciagniete pary klatek")
        for pair in frame_pairs:
            print(f"  [{pair['id']:02d}] {pair['end_frame'].name} + {pair['start_frame'].name}")
            print(f"       ({pair['from_video']} -> {pair['to_video']})")
        
        logger.success("\nGOTOWE! Klatki wyciagniete i gotowe do testow w ComfyUI.")
        logger.info("Aby wygenerowac filmy, ustaw: FRAME_ONLY = False")
        return
    
    # ------------------------------------------------------------
    # PODSUMOWANIE PRZED GENERACJA
    # ------------------------------------------------------------
    
    logger.header("GENERACJA PRZEJSC")
    
    transitions_folder = project_path / "transitions"
    transitions_folder.mkdir(exist_ok=True)
    
    logger.section("Podsumowanie konfiguracji")
    print(f"  Projekt: {project_path.name}")
    print(f"  Filmow: {len(videos)}")
    print(f"  Przejsc: {num_transitions}")
    print(f"  Rozdzielczosc: {target_w}x{target_h}")
    if MIN_WIDTH or MIN_HEIGHT:
        print(f"  Minimum: {MIN_WIDTH or 'auto'}x{MIN_HEIGHT or 'auto'}")
    print(f"  Maximum: {MAX_WIDTH}x{MAX_HEIGHT}")
    print(f"  FPS: {FPS}")
    print(f"  Steps: {STEPS}")
    print(f"  CFG: {CFG}")
    print(f"  Skip existed: {SKIP_EXISTED}")
    print(f"  Folder klatek: {frames_folder}")
    print(f"  Folder przejsc: {transitions_folder}")
    
    total_frames = sum(FPS * pair['duration'] for pair in frame_pairs)
    print(f"  Lacznie klatek: {total_frames}")
    
    estimated_min_per_transition = 10
    total_estimated_min = num_transitions * estimated_min_per_transition
    print(f"  Szacowany czas: ~{total_estimated_min//60}h {total_estimated_min%60}min")
    
    # ------------------------------------------------------------
    # PRE-CHECK: Sprawdź które transitions już istnieją
    # ------------------------------------------------------------
    
    if SKIP_EXISTED:
        logger.section("Pre-check: Sprawdzanie istniejących transitions")
        
        to_generate = []
        already_exist = []
        
        for pair in frame_pairs:
            output_name = f"{pair['from_video']}_{pair['to_video']}_transition.mp4"
            output_path = transitions_folder / output_name
            
            if output_path.exists():
                already_exist.append((pair['id'], output_name))
            else:
                to_generate.append((pair['id'], output_name, pair['duration']))
        
        # Wyświetl istniejące
        if already_exist:
            logger.warning(f"Znaleziono {len(already_exist)} istniejących transitions (zostaną pominięte):")
            for tid, name in already_exist:
                print(f"  [{tid:02d}] ⏭️  {name}")
        
        # Wyświetl do wygenerowania
        if to_generate:
            logger.section(f"Do wygenerowania: {len(to_generate)} transitions")
            for tid, name, duration in to_generate:
                print(f"  [{tid:02d}] 🎬 {name} ({duration}s)")
            
            # Zaktualizowany szacowany czas
            estimated_min = len(to_generate) * 10
            print(f"\n  Szacowany czas: ~{estimated_min//60}h {estimated_min%60}min")
        else:
            logger.success("Wszystkie transitions już istnieją - nic do generowania!")
            logger.info("Jeśli chcesz regenerować, ustaw SKIP_EXISTED = False lub skasuj wybrane transitions")
            return
    else:
        # SKIP_EXISTED = False - pokaż wszystkie
        logger.section("Lista przejsc do wygenerowania")
        for pair in frame_pairs:
            output_name = f"{pair['from_video']}_{pair['to_video']}_transition.mp4"
            print(f"  [{pair['id']:02d}] {output_name} ({pair['duration']}s)")
    
    response = input(f"\n{Fore.YELLOW}Nacisnij ENTER aby rozpoczac generacje (lub 'q' aby anulowac): {Style.RESET_ALL}")
    
    if response.lower() in ['q', 'quit', 'exit', 'n', 'no']:
        logger.warning("\nAnulowano przez uzytkownika")
        return
    
    logger.info("Rozpoczynam generacje...\n")
    
    # ------------------------------------------------------------
    # PETLA GENERACJI
    # ------------------------------------------------------------
    
    logger.header(f"GENEROWANIE {num_transitions} PRZEJSC")
    
    successful = 0
    failed = 0
    skipped = 0
    start_time = time.time()
    
    for i, pair in enumerate(frame_pairs):
        transition_num = i + 1
        
        # ========================================
        # SPRAWDŹ CZY JUŻ ISTNIEJE
        # ========================================
        
        output_name = f"{pair['from_video']}_{pair['to_video']}_transition.mp4"
        output_path = transitions_folder / output_name
        
        if SKIP_EXISTED and output_path.exists():
            logger.warning(f"\n  PRZEJSCIE [{transition_num}/{num_transitions}] - JUZ ISTNIEJE - POMIJAM")
            print(f"  Plik: {output_name}")
            skipped += 1
            continue
        
        # ========================================
        # GENERUJ (tylko jeśli nie istnieje)
        # ========================================
        
        logger.section(f"PRZEJSCIE [{transition_num}/{num_transitions}]")
        print(f"  Od: {pair['from_video']}")
        print(f"  Do: {pair['to_video']}")
        print(f"  Dlugosc: {pair['duration']}s ({FPS * pair['duration']} klatek)")
        print(f"  Klatka start: {pair['end_frame'].name}")
        print(f"  Klatka end: {pair['start_frame'].name}")
        
        try:
            time_before_generation = time.time()
            
            runner = WorkflowRunner(
                config_path=CONFIG_PATH,
                workflows_base_path=WORKFLOWS_PATH
            )
            
            runner.set_image(str(pair['end_frame']), "start_image")
            runner.set_image(str(pair['start_frame']), "end_image")
            runner.set_prompt(POSITIVE_PROMPT, "positive_prompt")
            runner.set_prompt(NEGATIVE_PROMPT, "negative_prompt")
            
            base_length = FPS * pair['duration']
            final_length = adjust_frame_count_for_wan(base_length)
            
            if base_length != final_length:
                logger.info(f"    Dostosowano klatki: {base_length} -> {final_length} (WAN rule: length%4=1)")
            
            runner.set_video_params(
                width=target_w,
                height=target_h,
                fps=FPS,
                length=final_length
            )
            
            runner.set_sampling_params(
                steps=STEPS,
                cfg=CFG,
                seed=SEED
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
                        pair['from_video'],
                        pair['to_video']
                    )
                    
                    if moved_file:
                        successful += 1
                        logger.success(f"\n  PRZEJSCIE {transition_num}/{num_transitions} GOTOWE!")
                        logger.success(f"  Lokalizacja: {moved_file.relative_to(project_path)}")
                    else:
                        failed += 1
                        logger.error(f"\n  PRZEJSCIE {transition_num}/{num_transitions} - blad przenoszenia")
                else:
                    failed += 1
                    logger.error(f"\n  Nie znaleziono wygenerowanego pliku w {COMFYUI_OUTPUT_FOLDER}!")
            else:
                failed += 1
                logger.error(f"\n  PRZEJSCIE {transition_num}/{num_transitions} NIEUDANE")
        
        except Exception as e:
            failed += 1
            logger.error(f"\n  WYJATEK: {e}")
            import traceback
            traceback.print_exc()
        
        # Postep
        elapsed = time.time() - start_time
        processed = successful + failed + skipped
        avg_time = elapsed / processed if processed > 0 else 0
        remaining = avg_time * (num_transitions - processed)
        
        logger.section("POSTEP")
        print(f"  Przetworzone: {processed}/{num_transitions}")
        print(f"  Ukonczone: {successful}")
        print(f"  Pominiete: {skipped}")
        print(f"  Nieudane: {failed}")
        print(f"  Czas wykonania: {elapsed/60:.1f}min")
        print(f"  Pozostalo: ~{remaining/60:.1f}min")
        print(f"  Procent: {(processed/num_transitions)*100:.1f}%")
        print()
    
    # ------------------------------------------------------------
    # FINALNE PODSUMOWANIE
    # ------------------------------------------------------------
    
    total_time = time.time() - start_time
    
    logger.header("FINALNE PODSUMOWANIE")
    print(f"  Projekt: {project_path.name}")
    print(f"  Przejsc total: {num_transitions}")
    print(f"  Nowo wygenerowane: {successful}")
    print(f"  Pominiete (juz byly): {skipped}")
    print(f"  Nieudane: {failed}")
    print(f"  Calkowity czas: {total_time/3600:.2f}h ({total_time/60:.1f}min)")
    print(f"  Lokalizacja klatek: {frames_folder}")
    print(f"  Lokalizacja transitions: {transitions_folder}")
    
    total_ok = successful + skipped
    
    if total_ok == num_transitions and failed == 0:
        logger.success("\nWszystkie przejscia dostepne!")
        if skipped > 0:
            logger.info(f"  ({skipped} bylo juz wczesniej)")
    elif successful > 0:
        logger.warning(f"\nNowo wygenerowano: {successful}, Pominieto: {skipped}, Nieudane: {failed}")
        if failed > 0:
            logger.warning("Sprawdz logi powyzej i uruchom ponownie dla brakujacych")
    else:
        if skipped == num_transitions:
            logger.success("\nWszystkie przejscia juz istnialy - nic do generowania")
        else:
            logger.error("\nBrak udanych generacji - sprawdz konfiguracje i logi")