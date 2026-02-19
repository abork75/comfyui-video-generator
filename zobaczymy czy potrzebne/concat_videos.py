# -*- coding: utf-8 -*-
"""
Video Concat Engine - Łączenie filmów z przejściami
Nie edytuj tego pliku! Użyj RUN_setup*.py dla konfiguracji.
"""

import os
from pathlib import Path
import subprocess
import time
import shutil
from colorama import Fore, Style, init

init(autoreset=True)

# ============================================================
# FUNKCJE POMOCNICZE
# ============================================================

def print_header(text):
    """Wyświetla nagłówek"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{' '*20}{text}")
    print(f"{'='*70}{Style.RESET_ALL}\n")

def print_section(text):
    """Wyświetla sekcję"""
    print(f"\n{Fore.YELLOW}{'-'*70}")
    print(f"📌 {text}")
    print(f"{'-'*70}{Style.RESET_ALL}")

def print_success(text):
    """Zielony success"""
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")

def print_error(text):
    """Czerwony błąd"""
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_warning(text):
    """Żółty warning"""
    print(f"{Fore.YELLOW}⚠️  {text}{Style.RESET_ALL}")

def print_info(text):
    """Info"""
    print(f"{Fore.CYAN}ℹ️  {text}{Style.RESET_ALL}")

def check_ffmpeg():
    """Sprawdza czy ffmpeg jest zainstalowany"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_video_stem(video_path):
    """Pobiera nazwę filmu bez rozszerzenia"""
    return Path(video_path).stem

def get_transition_filename(video_a_stem, video_b_stem):
    """Generuje nazwę pliku przejścia"""
    return f"{video_a_stem}_{video_b_stem}_transition.mp4"

def check_files_exist(project_path, video_order):
    """
    Sprawdza czy wszystkie potrzebne pliki istnieją
    
    Returns:
        tuple: (all_exist: bool, missing: list, files_list: list)
    """
    transitions_folder = project_path / "transitions"
    
    missing = []
    files_list = []
    
    for i, video_name in enumerate(video_order):
        video_path = project_path / video_name
        
        if video_path.exists():
            files_list.append(('video', video_path, video_name))
        else:
            missing.append(('video', video_name))
        
        if i < len(video_order) - 1:
            next_video = video_order[i + 1]
            
            video_a_stem = get_video_stem(video_name)
            video_b_stem = get_video_stem(next_video)
            
            transition_name = get_transition_filename(video_a_stem, video_b_stem)
            transition_path = transitions_folder / transition_name
            
            if transition_path.exists():
                files_list.append(('transition', transition_path, transition_name))
            else:
                missing.append(('transition', transition_name))
    
    all_exist = len(missing) == 0
    return all_exist, missing, files_list

def create_concat_file(files_list, project_path):
    """Tworzy plik concat.txt dla FFmpeg"""
    concat_file = project_path / "concat_list.txt"
    
    with open(concat_file, 'w', encoding='utf-8') as f:
        for file_type, file_path, file_name in files_list:
            file_path_str = str(file_path).replace('\\', '/')
            f.write(f"file '{file_path_str}'\n")
    
    return concat_file

def has_audio_stream(video_path):
    """Sprawdza czy plik ma ścieżkę audio"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'a:0',
        '-show_entries', 'stream=codec_type',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              creationflags=subprocess.CREATE_NO_WINDOW)
        return result.stdout.strip() == 'audio'
    except:
        return False

def normalize_video_with_audio(input_path, output_path, fps=16):
    """Normalizuje video - ujednolica FPS, codec, timestampy. Dodaje silent audio jeśli brak"""
    has_audio = has_audio_stream(input_path)
    
    cmd = ['ffmpeg', '-i', str(input_path)]
    
    if not has_audio:
        cmd.extend([
            '-f', 'lavfi',
            '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100'
        ])
    
    cmd.extend([
        '-r', str(fps),
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-vsync', 'cfr',
    ])
    
    if has_audio:
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', '192k',
            '-ar', '44100',
            '-ac', '2',
        ])
    else:
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-ac', '2',
            '-shortest',
        ])
    
    cmd.extend([
        '-movflags', '+faststart',
        '-y',
        str(output_path)
    ])
    
    result = subprocess.run(cmd, capture_output=True, 
                          creationflags=subprocess.CREATE_NO_WINDOW)
    return result.returncode == 0

def concat_videos_internal(concat_file, output_path):
    """Łączy filmy z normalizacją (2-pass)"""
    print_info("Wczytuję listę plików...")
    
    with open(concat_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    file_paths = []
    for line in lines:
        if line.startswith("file '"):
            path = line.strip()[6:-1]
            file_paths.append(Path(path))
    
    print_success(f"Znaleziono {len(file_paths)} plików do połączenia")
    
    # PASS 1: Normalizacja
    print_section("PASS 1: Normalizacja plików (dodanie audio, fix timestampów)")
    
    temp_folder = concat_file.parent / "temp_normalized"
    temp_folder.mkdir(exist_ok=True)
    
    normalized_files = []
    start_normalize = time.time()
    
    for i, original_path in enumerate(file_paths):
        temp_file = temp_folder / f"normalized_{i:04d}.mp4"
        
        has_audio = has_audio_stream(original_path)
        audio_status = "✅ audio" if has_audio else "🔇 dodaję silent audio"
        
        print(f"  [{i+1:02d}/{len(file_paths)}] {original_path.name} ({audio_status})")
        
        if not normalize_video_with_audio(original_path, temp_file):
            print_error(f"Błąd normalizacji: {original_path.name}")
            shutil.rmtree(temp_folder, ignore_errors=True)
            return False
        
        normalized_files.append(temp_file)
    
    elapsed_normalize = time.time() - start_normalize
    print_success(f"Normalizacja zakończona ({elapsed_normalize:.1f}s)")
    
    # PASS 2: Concat
    print_section("PASS 2: Łączenie znormalizowanych plików")
    
    normalized_concat = temp_folder / "normalized_concat.txt"
    with open(normalized_concat, 'w', encoding='utf-8') as f:
        for temp_file in normalized_files:
            file_path_str = str(temp_file).replace('\\', '/')
            f.write(f"file '{file_path_str}'\n")
    
    print_info("Łączenie plików (concat)...")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(normalized_concat),
        '-c', 'copy',
        '-movflags', '+faststart',
        '-y',
        str(output_path)
    ]
    
    start_concat = time.time()
    result = subprocess.run(cmd)
    success = result.returncode == 0
    elapsed_concat = time.time() - start_concat
    
    if success:
        print_success(f"Concat zakończony ({elapsed_concat:.1f}s)")
    
    # CLEANUP
    if success:
        print_info("Usuwanie plików tymczasowych...")
        try:
            shutil.rmtree(temp_folder)
            print_success(f"Usunięto {len(normalized_files)} plików tymczasowych")
        except Exception as e:
            print_warning(f"Nie udało się usunąć temp folder: {e}")
    else:
        print_warning(f"Pliki tymczasowe zachowane w: {temp_folder}")
    
    return success

# ============================================================
# GŁÓWNA FUNKCJA
# ============================================================

def run_concat(config):
    """
    Główna funkcja - łączenie filmów
    
    Args:
        config: Dictionary z parametrami konfiguracyjnymi
    """
    PROJECT_FOLDER = config['project_folder']
    VIDEO_ORDER = config['video_order']
    OUTPUT_FILENAME = config['output_filename']
    VIDEO_CODEC = config.get('video_codec', 'libx264')
    CRF = config.get('crf', 18)
    PRESET = config.get('preset', 'medium')
    
    print_header("VIDEO CONCAT - ŁĄCZENIE FILMÓW Z PRZEJŚCIAMI")
    
    # Walidacja
    if not check_ffmpeg():
        print_error("ffmpeg nie znaleziony! Zainstaluj: https://ffmpeg.org/download.html")
        return
    
    print_success("ffmpeg OK")
    
    project_path = Path(PROJECT_FOLDER)
    if not project_path.exists():
        print_error(f"Folder nie istnieje: {PROJECT_FOLDER}")
        return
    
    print_success(f"Projekt: {project_path.name}")
    
    # Sprawdzanie plików
    num_videos = len(VIDEO_ORDER)
    num_transitions = num_videos - 1
    
    print_section(f"Weryfikacja {num_videos} filmów + {num_transitions} przejść")
    
    all_exist, missing, files_list = check_files_exist(project_path, VIDEO_ORDER)
    
    if not all_exist:
        print_error(f"Brakuje {len(missing)} plików!\n")
        
        for file_type, file_name in missing:
            if file_type == 'video':
                print(f"  ❌ Film: {file_name}")
            else:
                print(f"  ❌ Przejście: {file_name}")
        
        print_warning("\nNapraw brakujące pliki i uruchom ponownie.")
        return
    
    print_success(f"Wszystkie pliki istnieją! ({len(files_list)} plików)")
    
    # Wyświetlenie listy
    print_section("Lista plików do połączenia")
    
    total_duration = 0
    
    for i, (file_type, file_path, file_name) in enumerate(files_list):
        if file_type == 'video':
            icon = "🎬"
            duration = 6
            desc = "Film"
        else:
            icon = "🔗"
            duration = 2
            desc = "Przejście"
        
        total_duration += duration
        
        print(f"  [{i:02d}] {icon} {desc:10} {file_name}")
    
    print(f"\n  Łącznie plików: {len(files_list)}")
    print(f"  Szacowany czas finalnego filmu: ~{total_duration}s ({total_duration/60:.1f}min)")
    
    # Podsumowanie konfiguracji
    print_section("Konfiguracja wyjściowa")
    
    output_path = project_path / OUTPUT_FILENAME
    
    print(f"  Nazwa: {OUTPUT_FILENAME}")
    print(f"  Lokalizacja: {output_path}")
    print(f"  Codec: {VIDEO_CODEC}")
    print(f"  Jakość (CRF): {CRF}")
    print(f"  Preset: {PRESET}")
    
    estimated_size_mb = (total_duration * 2)
    print(f"  Szacowany rozmiar: ~{estimated_size_mb}MB")
    
    # Potwierdzenie
    print_section("POTWIERDŹ GENERACJĘ")
    
    response = input(f"\n{Fore.YELLOW}Wszystko wygląda OK? Naciśnij ENTER aby rozpocząć (lub 'q' aby anulować): {Style.RESET_ALL}")
    
    if response.lower() in ['q', 'quit', 'exit', 'n', 'no']:
        print_warning("\nAnulowano przez użytkownika")
        return
    
    # Generacja
    print_section("ŁĄCZENIE FILMÓW")
    
    print_info("Tworzenie pliku concat.txt...")
    concat_file = create_concat_file(files_list, project_path)
    print_success(f"Zapisano: {concat_file.name}")
    
    print_info(f"Rozpoczynam proces łączenia {len(files_list)} plików...\n")
    
    start_time = time.time()
    
    success = concat_videos_internal(concat_file, output_path)
    
    elapsed = time.time() - start_time
    
    # Podsumowanie
    print_header("PODSUMOWANIE")
    
    if success and output_path.exists():
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        print_success("Łączenie zakończone pomyślnie!")
        print(f"\n  Finalny film: {output_path.name}")
        print(f"  Lokalizacja: {output_path}")
        print(f"  Rozmiar: {file_size_mb:.1f} MB")
        print(f"  Czas generacji: {elapsed:.1f}s ({elapsed/60:.1f}min)")
        
        try:
            concat_file.unlink()
            print_info("Plik tymczasowy concat.txt usunięty")
        except:
            pass
        
    else:
        print_error("Błąd podczas łączenia filmów!")
        print_warning("Sprawdź logi FFmpeg powyżej")
        
        try:
            if concat_file and concat_file.exists():
                print_info(f"Plik concat.txt zachowany do debugowania: {concat_file}")
        except:
            pass