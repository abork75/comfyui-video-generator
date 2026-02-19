# -*- coding: utf-8 -*-
"""
Video Concat - Łączenie filmów z przejściami w jeden finalny film

Edytuj tylko sekcję KONFIGURACJA!
"""

import os
from pathlib import Path
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# ============================================================
# KONFIGURACJA - EDYTUJ TO!
# ============================================================

# Folder z filmami CapCut
PROJECT_FOLDER = r"C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\chair_spanking"

# ============================================================
# PEŁNA LISTA WSZYSTKICH FILMÓW (w kolejności)
# ============================================================

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


# ALL_VIDEOS = [
    # "chair_spanking_01.mp4",
    # "chair_spanking_02.mp4",
    # "chair_spanking_03.mp4",
    # "chair_spanking_04.mp4",
    # "chair_spanking_06.mp4",
    # "chair_spanking_08.mp4",
    # "chair_spanking_10.mp4",
    # "chair_spanking_11.mp4",
    # "chair_spanking_12.mp4",
    # "chair_spanking_13.mp4",
    # "chair_spanking_14.mp4",
    # "chair_spanking_15.mp4",
    # "chair_spanking_17.mp4",
    # "chair_spanking_21.mp4",
    # "chair_spanking_22.mp4",
    # "chair_spanking_23.mp4",
    # "chair_spanking_24.mp4",
    # "chair_spanking_25.mp4",
    # "chair_spanking_18.mp4",
    # "chair_spanking_09.mp4",
    # "chair_spanking_07.mp4",
    # "chair_spanking_05.mp4",
    # "chair_spanking-3.mp4",
# ]

# ============================================================
# LISTA AKTYWNA - EDYTUJ TĄ!
# ============================================================

# Test - pierwsze 3 filmy (2 przejścia)
# VIDEO_ORDER = ALL_VIDEOS[:3]

# Wszystkie filmy (odkomentuj gdy gotowy):
VIDEO_ORDER = ALL_VIDEOS

# ------------------------------------------------------------
# USTAWIENIA WYJŚCIOWE
# ------------------------------------------------------------

# Nazwa finalnego filmu
OUTPUT_FILENAME = "chair_spanking_FINAL.mp4"

# Codec video (h264 = standard, h265 = lepsza kompresja)
VIDEO_CODEC = "libx264"  # lub "libx265"

# Jakość (17-28, niższe = lepsza jakość, większy plik)
# 18 = bardzo dobra, 23 = dobra, 28 = słabsza
CRF = 18

# Preset (ultrafast, fast, medium, slow, veryslow)
# slower = lepsza kompresja ale dłużej trwa
PRESET = "medium"

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
    files_list = []  # Lista (typ, ścieżka, nazwa) do wyświetlenia
    
    # Sprawdź filmy i przejścia
    for i, video_name in enumerate(video_order):
        video_path = project_path / video_name
        
        # Sprawdź film
        if video_path.exists():
            files_list.append(('video', video_path, video_name))
        else:
            missing.append(('video', video_name))
        
        # Sprawdź przejście (jeśli nie ostatni film)
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
    """
    Tworzy plik concat.txt dla FFmpeg
    
    Args:
        files_list: Lista (typ, Path, nazwa)
        project_path: Path do projektu
    
    Returns:
        Path do pliku concat.txt
    """
    concat_file = project_path / "concat_list.txt"
    
    with open(concat_file, 'w', encoding='utf-8') as f:
        for file_type, file_path, file_name in files_list:
            # FFmpeg wymaga forward slashes nawet na Windows
            file_path_str = str(file_path).replace('\\', '/')
            f.write(f"file '{file_path_str}'\n")
    
    return concat_file

def has_audio_stream(video_path):
    """
    Sprawdza czy plik ma ścieżkę audio
    
    Returns:
        bool: True jeśli ma audio
    """
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
    """
    Normalizuje video - ujednolica FPS, codec, timestampy
    Dodaje silent audio jeśli brak
    
    Args:
        input_path: Ścieżka do oryginalnego pliku
        output_path: Ścieżka do znormalizowanego pliku
        fps: Docelowy FPS (default: 16)
    
    Returns:
        bool: True jeśli sukces
    """
    has_audio = has_audio_stream(input_path)
    
    cmd = ['ffmpeg', '-i', str(input_path)]
    
    # Jeśli brak audio - dodaj silent
    if not has_audio:
        cmd.extend([
            '-f', 'lavfi',
            '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100'
        ])
    
    # Wspólne parametry
    cmd.extend([
        '-r', str(fps),  # Wymuszony FPS
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-vsync', 'cfr',  # Constant frame rate - fix timestampów!
    ])
    
    # Audio
    if has_audio:
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', '192k',
            '-ar', '44100',
            '-ac', '2',
        ])
    else:
        # Silent audio - dopasuj do długości video
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-ac', '2',
            '-shortest',  # Dopasuj audio do długości video
        ])
    
    # Output
    cmd.extend([
        '-movflags', '+faststart',
        '-y',
        str(output_path)
    ])
    
    result = subprocess.run(cmd, capture_output=True, 
                          creationflags=subprocess.CREATE_NO_WINDOW)
    return result.returncode == 0

def concat_videos(concat_file, output_path, codec, crf, preset):
    """
    Łączy filmy z normalizacją (ujednolicenie FPS, timestampów, dodanie audio)
    
    Args:
        concat_file: Path do pliku concat.txt
        output_path: Path do wyjściowego filmu
        codec: Codec video (libx264, libx265)
        crf: Jakość (17-28)
        preset: Preset (nie używany w tej wersji - używamy fast dla normalizacji)
    
    Returns:
        bool: True jeśli sukces
    """
    # Wczytaj listę plików z concat_file
    print_info("Wczytuję listę plików...")
    
    with open(concat_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    file_paths = []
    for line in lines:
        if line.startswith("file '"):
            path = line.strip()[6:-1]  # Usuń "file '" i "'"
            file_paths.append(Path(path))
    
    print_success(f"Znaleziono {len(file_paths)} plików do połączenia")
    
    # ------------------------------------------------------------
    # PASS 1: Normalizacja wszystkich plików
    # ------------------------------------------------------------
    
    print_section("PASS 1: Normalizacja plików (dodanie audio, fix timestampów)")
    
    temp_folder = concat_file.parent / "temp_normalized"
    temp_folder.mkdir(exist_ok=True)
    
    normalized_files = []
    
    import time
    start_normalize = time.time()
    
    for i, original_path in enumerate(file_paths):
        temp_file = temp_folder / f"normalized_{i:04d}.mp4"
        
        # Sprawdź czy ma audio
        has_audio = has_audio_stream(original_path)
        audio_status = "✅ audio" if has_audio else "🔇 dodaję silent audio"
        
        print(f"  [{i+1:02d}/{len(file_paths)}] {original_path.name} ({audio_status})")
        
        if not normalize_video_with_audio(original_path, temp_file):
            print_error(f"Błąd normalizacji: {original_path.name}")
            # Cleanup
            import shutil
            shutil.rmtree(temp_folder, ignore_errors=True)
            return False
        
        normalized_files.append(temp_file)
    
    elapsed_normalize = time.time() - start_normalize
    print_success(f"Normalizacja zakończona ({elapsed_normalize:.1f}s)")
    
    # ------------------------------------------------------------
    # PASS 2: Concat (teraz bez problemów!)
    # ------------------------------------------------------------
    
    print_section("PASS 2: Łączenie znormalizowanych plików")
    
    # Utwórz nowy concat file dla znormalizowanych
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
        '-c', 'copy',  # Teraz możemy użyć copy - wszystko ujednolicone!
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
    
    # ------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------
    
    if success:
        print_info("Usuwanie plików tymczasowych...")
        import shutil
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

def run_concat():
    """Główna funkcja - łączenie filmów"""
    
    print_header("VIDEO CONCAT - ŁĄCZENIE FILMÓW Z PRZEJŚCIAMI")
    
    # ------------------------------------------------------------
    # WALIDACJA
    # ------------------------------------------------------------
    
    # Sprawdź ffmpeg
    if not check_ffmpeg():
        print_error("ffmpeg nie znaleziony! Zainstaluj: https://ffmpeg.org/download.html")
        return
    
    print_success("ffmpeg OK")
    
    # Sprawdź folder
    project_path = Path(PROJECT_FOLDER)
    if not project_path.exists():
        print_error(f"Folder nie istnieje: {PROJECT_FOLDER}")
        return
    
    print_success(f"Projekt: {project_path.name}")
    
    # ------------------------------------------------------------
    # SPRAWDZANIE PLIKÓW
    # ------------------------------------------------------------
    
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
    
    # ------------------------------------------------------------
    # WYŚWIETLENIE LISTY
    # ------------------------------------------------------------
    
    print_section("Lista plików do połączenia")
    
    total_duration = 0
    
    for i, (file_type, file_path, file_name) in enumerate(files_list):
        if file_type == 'video':
            icon = "🎬"
            duration = 6  # Przyjmujemy 6s (można pobrać z ffprobe)
            desc = "Film"
        else:
            icon = "🔗"
            duration = 2  # Przyjmujemy 2s
            desc = "Przejście"
        
        total_duration += duration
        
        print(f"  [{i:02d}] {icon} {desc:10} {file_name}")
    
    print(f"\n  Łącznie plików: {len(files_list)}")
    print(f"  Szacowany czas finalnego filmu: ~{total_duration}s ({total_duration/60:.1f}min)")
    
    # ------------------------------------------------------------
    # PODSUMOWANIE KONFIGURACJI
    # ------------------------------------------------------------
    
    print_section("Konfiguracja wyjściowa")
    
    output_path = project_path / OUTPUT_FILENAME
    
    print(f"  Nazwa: {OUTPUT_FILENAME}")
    print(f"  Lokalizacja: {output_path}")
    print(f"  Codec: {VIDEO_CODEC}")
    print(f"  Jakość (CRF): {CRF}")
    print(f"  Preset: {PRESET}")
    
    # Szacunkowy rozmiar
    estimated_size_mb = (total_duration * 2)  # ~2MB/s dla CRF=18
    print(f"  Szacowany rozmiar: ~{estimated_size_mb}MB")
    
    # ------------------------------------------------------------
    # POTWIERDZENIE
    # ------------------------------------------------------------
    
    print_section("POTWIERDŹ GENERACJĘ")
    
    response = input(f"\n{Fore.YELLOW}Wszystko wygląda OK? Naciśnij ENTER aby rozpocząć (lub 'q' aby anulować): {Style.RESET_ALL}")
    
    # Sprawdź czy użytkownik chce anulować
    if response.lower() in ['q', 'quit', 'exit', 'n', 'no']:
        print_warning("\nAnulowano przez użytkownika")
        return
    
    # ------------------------------------------------------------
    # GENERACJA
    # ------------------------------------------------------------
    
    print_section("ŁĄCZENIE FILMÓW")
    
    # Utwórz plik concat.txt
    print_info("Tworzenie pliku concat.txt...")
    concat_file = create_concat_file(files_list, project_path)
    print_success(f"Zapisano: {concat_file.name}")
    
    # Uruchom FFmpeg (2-pass: normalize + concat)
    print_info(f"Rozpoczynam proces łączenia {len(files_list)} plików...\n")
    
    import time
    start_time = time.time()
    
    success = concat_videos(concat_file, output_path, VIDEO_CODEC, CRF, PRESET)
    
    elapsed = time.time() - start_time
    
    # ------------------------------------------------------------
    # PODSUMOWANIE
    # ------------------------------------------------------------
    
    print_header("PODSUMOWANIE")
    
    if success and output_path.exists():
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        print_success("Łączenie zakończone pomyślnie!")
        print(f"\n  Finalny film: {output_path.name}")
        print(f"  Lokalizacja: {output_path}")
        print(f"  Rozmiar: {file_size_mb:.1f} MB")
        print(f"  Czas generacji: {elapsed:.1f}s ({elapsed/60:.1f}min)")
        
        # Usuń plik concat.txt
        try:
            concat_file.unlink()
            print_info("Plik tymczasowy concat.txt usunięty")
        except:
            pass
        
    else:
        print_error("Błąd podczas łączenia filmów!")
        print_warning("Sprawdź logi FFmpeg powyżej")
        
        # Pozostaw concat.txt do debugowania
        try:
            if concat_file and concat_file.exists():
                print_info(f"Plik concat.txt zachowany do debugowania: {concat_file}")
        except:
            pass

# ============================================================
# URUCHOMIENIE
# ============================================================

if __name__ == "__main__":
    try:
        run_concat()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Anulowano przez użytkownika{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Nieoczekiwany błąd: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()