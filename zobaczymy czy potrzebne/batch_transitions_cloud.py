# -*- coding: utf-8 -*-
"""
Batch Transition Generator - CLOUD MODE (Comfy.icu API)
Based on ADVANCED mode - FLOW support (video + images, custom params)
Sequential processing (no parallel - cost control)

BASED ON: batch_transitions_adv.py
CHANGES: 
- Upload frames → ImgBB (public URLs)
- Generation → Comfy.icu API (WORKING!)
- Download results → local transitions/
- AUTO CLEANUP → Delete uploaded images from ImgBB after use

CHANGELOG:
- 2026-02-08: Initial cloud implementation (based on ADV)
- 2026-02-08: Added CRITICAL validations (FORCE/DEFAULT % 8)
- 2026-02-08: Added detailed upscaling logs (cost awareness)
- 2026-02-08: Improved error messages (MIN/MAX)
- 2026-02-08: Added ImgBB cleanup after generation
- 2026-02-08: FIXED Comfy.icu API integration (working!)
"""

import os
import subprocess
import time
import shutil
import requests
import json
import copy
from pathlib import Path
from PIL import Image
from collections import Counter
import statistics
from workflow_base import WorkflowRunner, Logger
from colorama import Fore, Style

# Cloud helpers
from helpers.imgbb_upload import upload_to_imgbb, delete_from_imgbb
from helpers.cost_calculator import estimate_comfy_icu_cost, estimate_batch_cost

# ============================================================
# FUNKCJE POMOCNICZE - PODSTAWOWE (IDENTYCZNE JAK ADV)
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
    
    UPDATED (2026-02-08): Wspiera MIN_WIDTH/MIN_HEIGHT dla wymuszenia upscalingu
    """
    
    # KROK 1: Force upscaling jeśli za małe
    if min_width is not None or min_height is not None:
        min_w = min_width if min_width is not None else 0
        min_h = min_height if min_height is not None else 0
        
        if width < min_w or height < min_h:
            scale_w = min_w / width if width < min_w else 1.0
            scale_h = min_h / height if height < min_h else 1.0
            scale = max(scale_w, scale_h)
            
            width = int(width * scale)
            height = int(height * scale)
    
    # KROK 2: Skaluj w dół jeśli > maximum
    if width <= max_width and height <= max_height:
        return round_to_multiple(width), round_to_multiple(height)
    
    scale_w = max_width / width
    scale_h = max_height / height
    scale = min(scale_w, scale_h)
    
    new_width = round_to_multiple(width * scale)
    new_height = round_to_multiple(height * scale)
    
    return new_width, new_height

def adjust_frame_count_for_wan(frame_count):
    """Dostosowuje liczbe klatek do wymagan modelu WAN. Regula: length % 4 == 1"""
    remainder = frame_count % 4
    
    if remainder == 1:
        return frame_count
    elif remainder == 0:
        return frame_count + 1
    elif remainder == 2:
        return frame_count - 1
    else:
        return frame_count + 2

# ============================================================
# FUNKCJE POMOCNICZE - PLIKI (IDENTYCZNE JAK ADV)
# ============================================================

def get_item_type(path):
    """Rozpoznaje czy to film czy zdjecie"""
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
            return img.size
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
# EKSTRAKCJA KLATEK (IDENTYCZNE JAK ADV)
# ============================================================

def extract_frame_from_video(video_path, output_path, position='last', image_quality=95):
    """Wyciaga klatke z filmu"""
    logger = Logger()
    
    if position == 'last':
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', 'reverse,select=eq(n\\,0)',
            '-vframes', '1',
            '-q:v', str(100 - image_quality),
            '-y', str(output_path)
        ]
    else:
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
    """Przygotowuje klatke ze zdjecia"""
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            target_w, target_h = target_resolution
            img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            img_resized.save(output_path, quality=image_quality, optimize=True)
            
            return True
    except Exception as e:
        logger = Logger()
        logger.error(f"  Blad przygotowania obrazu: {e}")
        return False

def ensure_frame_exists(item_path, item_type, output_path, position, target_resolution, image_quality=95):
    """Zapewnia ze klatka istnieje (ZAWSZE nadpisuje)"""
    logger = Logger()
    
    if output_path.exists():
        logger.info(f"    Nadpisuje: {output_path.name}")
    else:
        logger.info(f"    Wyciaganie: {output_path.name}")
    
    if item_type == 'video':
        if not extract_frame_from_video(item_path, output_path, position, image_quality):
            return False
    elif item_type == 'image':
        if not prepare_frame_from_image(item_path, output_path, target_resolution, image_quality):
            return False
    else:
        logger.error(f"  Nieznany typ: {item_type}")
        return False
    
    logger.success(f"    ✓ {output_path.name}")
    return True

# ============================================================
# FLOW PARSING (IDENTYCZNE JAK ADV)
# ============================================================

def resolve_prompt(prompt_value, prompt_type, generic_prompts, default_prompt):
    """Rozwiazuje prompt - obsluguje [generic], custom text, None"""
    if prompt_value is None:
        return default_prompt
    
    if isinstance(prompt_value, str) and prompt_value.startswith("[") and prompt_value.endswith("]"):
        generic_name = prompt_value[1:-1]
        
        if generic_name not in generic_prompts:
            raise ValueError(f"Nieznany generic prompt: '{generic_name}'. Dostępne: {list(generic_prompts.keys())}")
        
        return generic_prompts[generic_name][prompt_type]
    
    return prompt_value

def parse_flow_item(item, defaults, generic_prompts):
    """Parsuje jeden item z FLOW z fallback do defaults"""
    if "file" not in item:
        raise ValueError(f"Item nie ma klucza 'file': {item}")
    
    file_path = item["file"]
    duration = item.get("duration", defaults["duration"])
    fps = item.get("fps", defaults["fps"])
    steps = item.get("steps", defaults["steps"])
    cfg = item.get("cfg", defaults["cfg"])
    seed = item.get("seed", defaults["seed"])
    
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
    """Parsuje FLOW do listy items + skip_transitions"""
    items = []
    skip_transitions = set()
    
    for i, entry in enumerate(flow):
        if entry.get("break", False):
            if items:
                skip_transitions.add(len(items) - 1)
            continue
        
        try:
            parsed_item = parse_flow_item(entry, defaults, generic_prompts)
            items.append(parsed_item)
        except ValueError as e:
            raise ValueError(f"Błąd w FLOW entry [{i}]: {e}")
    
    return items, skip_transitions

# ============================================================
# WALIDACJA (IDENTYCZNE JAK ADV)
# ============================================================

def validate_aspect_ratios(items, project_path, tolerance=0.1, strategy="most_common"):
    """Waliduje aspect ratio wszystkich plikow"""
    logger = Logger()
    
    aspect_ratios = []
    
    for item in items:
        file_path = project_path / item["file"]
        
        if not file_path.exists():
            continue
        
        item_type = get_item_type(file_path)
        
        if item_type == 'video':
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
    
    if strategy == "most_common":
        ar_values = [ar for _, ar, _ in aspect_ratios]
        ar_counter = Counter([round(ar, 3) for ar in ar_values])
        most_common_ar = ar_counter.most_common(1)[0][0]
        base_ar = most_common_ar
        logger.info(f"  Baseline AR (most_common): {base_ar:.3f} (występuje {ar_counter[most_common_ar]}x)")
    
    elif strategy == "first_video":
        base_ar = None
        for file_name, ar, res in aspect_ratios:
            ext = Path(file_name).suffix.lower()
            if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                base_ar = ar
                logger.info(f"  Baseline AR (first_video): {base_ar:.3f} ({file_name})")
                break
        
        if base_ar is None:
            base_ar = aspect_ratios[0][1]
            logger.warning(f"  Brak video - użyto pierwszego pliku: {base_ar:.3f}")
    
    elif strategy == "median":
        ar_values = [ar for _, ar, _ in aspect_ratios]
        base_ar = statistics.median(ar_values)
        logger.info(f"  Baseline AR (median): {base_ar:.3f}")
    
    else:
        base_ar = aspect_ratios[0][1]
        logger.info(f"  Baseline AR (first): {base_ar:.3f} ({aspect_ratios[0][0]})")
    
    valid = True
    
    for file_name, ar, res in aspect_ratios:
        diff = abs(ar - base_ar) / base_ar
        
        if diff > tolerance:
            logger.error(f"  {file_name}: AR={ar:.3f} ({res[0]}x{res[1]}) - różni się od bazowego {base_ar:.3f} o {diff*100:.1f}%")
            valid = False
        else:
            if diff > 0.001:
                logger.info(f"  {file_name}: AR={ar:.3f} - różnica {diff*100:.1f}% (OK)")
    
    return valid, aspect_ratios

# ============================================================
# CLOUD API FUNCTIONS - FIXED!
# ============================================================

def prepare_workflow_prompt(params, start_image_name, end_image_name, template_path):
    """
    Prepare workflow prompt from template
    
    Args:
        params: Dict with generation params (width, height, fps, etc.)
        start_image_name: Filename for start image (e.g. "start.jpg")
        end_image_name: Filename for end image (e.g. "end.jpg")
        template_path: Path to workflow JSON template
        
    Returns:
        dict: Modified workflow prompt
    """
    with open(template_path, encoding='utf-8') as f:
        prompt = json.load(f)
    
    prompt = copy.deepcopy(prompt)
    
    # Modify prompts
    prompt["6"]["inputs"]["text"] = params['pos_prompt']
    prompt["7"]["inputs"]["text"] = params['neg_prompt']
    
    # Modify images
    prompt["62"]["inputs"]["image"] = end_image_name
    prompt["68"]["inputs"]["image"] = start_image_name
    
    # Modify video params
    prompt["67"]["inputs"]["width"] = params['width']
    prompt["67"]["inputs"]["height"] = params['height']
    prompt["67"]["inputs"]["length"] = params['length']
    
    # Modify sampling
    prompt["57"]["inputs"]["steps"] = params['steps']
    prompt["57"]["inputs"]["cfg"] = params['cfg']
    prompt["57"]["inputs"]["noise_seed"] = params.get('seed', 42)
    prompt["58"]["inputs"]["steps"] = params['steps']
    prompt["58"]["inputs"]["cfg"] = params['cfg']
    
    # Modify FPS
    prompt["71"]["inputs"]["frame_rate"] = params['fps']
    
    return prompt


def start_comfy_icu_generation(api_key, workflow_id, start_image_url, end_image_url, params, template_path):
    """
    Start generation on Comfy.icu API
    
    Args:
        api_key: Comfy.icu API key
        workflow_id: Workflow ID on Comfy.icu
        start_image_url: Public URL of start frame
        end_image_url: Public URL of end frame
        params: Dict with generation params (fps, duration, width, height, etc.)
        template_path: Path to workflow JSON template
        
    Returns:
        str: run_id or None if failed
    """
    logger = Logger()
    
    # FIXED URL:
    url = f"https://comfy.icu/api/v1/workflows/{workflow_id}/runs"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    # Prepare prompt from template
    prompt = prepare_workflow_prompt(params, "start.jpg", "end.jpg", template_path)
    
    # Files mapping
    files = {
        "/input/start.jpg": start_image_url,
        "/input/end.jpg": end_image_url,
    }
    
    body = {
        "workflow_id": workflow_id,
        "prompt": prompt,
        "files": files
    }
    
    try:
        logger.info(f"  Starting Comfy.icu job...")
        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        run_id = data.get('id') or data.get('run_id')
        
        logger.success(f"  Job started: {run_id}")
        return run_id
        
    except Exception as e:
        logger.error(f"  API error: {e}")
        if hasattr(e, 'response'):
            logger.error(f"  Response: {e.response.text[:200]}")
        return None


def poll_comfy_icu_status(api_key, workflow_id, run_id, timeout=3600, check_interval=10):
    """
    Poll Comfy.icu job status until complete
    
    Args:
        api_key: Comfy.icu API key
        workflow_id: Workflow ID
        run_id: Run ID from start_comfy_icu_generation
        timeout: Maximum wait time in seconds (default: 1 hour)
        check_interval: Seconds between checks (default: 10s)
        
    Returns:
        str: video_url or None if failed/timeout
    """
    logger = Logger()
    
    url = f"https://comfy.icu/api/v1/workflows/{workflow_id}/runs/{run_id}"
    headers = {"authorization": f"Bearer {api_key}"}
    
    start_time = time.time()
    last_status = None
    
    logger.info(f"  Waiting for completion (timeout: {timeout//60}min)...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            status = data.get('status', 'unknown')
            status_lower = status.lower()
            
            # Log status changes
            if status != last_status:
                elapsed = time.time() - start_time
                logger.info(f"  [{elapsed:.0f}s] Status: {status}")
                last_status = status
            
            # Check if completed
            if status_lower in ['completed', 'succeeded', 'success']:
                # Get output LIST (not 'outputs')
                output_list = data.get('output', [])
                
                if not output_list:
                    logger.error(f"  No output files")
                    return None
                
                # Find video in output list
                for item in output_list:
                    if isinstance(item, dict) and 'url' in item:
                        url_str = item['url']
                        if url_str.endswith('.mp4') or url_str.endswith('.webm'):
                            elapsed = time.time() - start_time
                            logger.success(f"  Completed in {elapsed/60:.1f}min")
                            return url_str
                
                logger.error(f"  No video found in output")
                return None
                
            elif status_lower in ['failed', 'error']:
                error_msg = data.get('error', 'Unknown error')
                logger.error(f"  Job failed: {error_msg}")
                return None
            
            # Still running - wait
            time.sleep(check_interval)
            
        except Exception as e:
            logger.warning(f"  Poll error: {e}")
            time.sleep(check_interval)
    
    logger.error(f"  Timeout after {timeout//60}min")
    return None


def download_video(video_url, output_path):
    """
    Download video from URL to local file
    
    Args:
        video_url: Public URL of video
        output_path: Local path to save video
        
    Returns:
        bool: True if success, False if failed
    """
    logger = Logger()
    
    try:
        logger.info(f"  Downloading: {output_path.name}")
        
        response = requests.get(video_url, stream=True, timeout=300)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        logger.success(f"  Downloaded: {output_path.name}")
        return True
        
    except Exception as e:
        logger.error(f"  Download exception: {e}")
        return False

# ============================================================
# GLOWNA FUNKCJA - CLOUD MODE
# ============================================================

def run_batch_generation_cloud(config):
    """
    Glowna funkcja - CLOUD mode (Comfy.icu API) - BASED ON ADV
    
    Args:
        config: Dictionary z parametrami konfiguracyjnymi + cloud settings
        
    NOWE parametry cloud:
        comfy_icu_api_key: API key dla Comfy.icu (optional - uses env)
        comfy_icu_workflow_id: Workflow ID na Comfy.icu
        workflow_template_path: Path to workflow JSON template
    """
    logger = Logger()
    
    logger.header("BATCH TRANSITION GENERATOR - CLOUD MODE (Comfy.icu)")
    
    # ------------------------------------------------------------
    # ROZPAKUJ CONFIG
    # ------------------------------------------------------------
    
    PROJECT_FOLDER = config['project_folder']
    FLOW = config['flow']
    GENERIC_PROMPTS = config.get('generic_prompts', {})
    
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
    MIN_WIDTH = config.get('min_width', None)
    MIN_HEIGHT = config.get('min_height', None)
    
    IMAGE_QUALITY = config.get('image_quality', 95)
    
    ASPECT_RATIO_TOLERANCE = config.get('aspect_ratio_tolerance', 0.05)
    ASPECT_RATIO_STRATEGY = config.get('aspect_ratio_strategy', 'most_common')
    
    DEFAULT_RESOLUTION = config.get('default_resolution', (336, 448))
    FORCE_RESOLUTION = config.get('force_resolution', None)
    
    # CLOUD-SPECIFIC settings
    COMFY_ICU_API_KEY = os.getenv('COMFY_ICU_API_KEY', config.get('comfy_icu_api_key', ''))
    COMFY_ICU_WORKFLOW_ID = config.get('comfy_icu_workflow_id', '')
    WORKFLOW_TEMPLATE_PATH = config.get('workflow_template_path', '')
    
    if not COMFY_ICU_API_KEY:
        logger.error("COMFY_ICU_API_KEY nie ustawiony!")
        logger.error("Ustaw zmienną środowiskową: $env:COMFY_ICU_API_KEY = 'your_key'")
        return
    
    if not COMFY_ICU_WORKFLOW_ID:
        logger.error("COMFY_ICU_WORKFLOW_ID jest wymagany!")
        logger.error("Ustaw w RUN config file")
        return
    
    if not WORKFLOW_TEMPLATE_PATH:
        logger.error("WORKFLOW_TEMPLATE_PATH jest wymagany!")
        logger.error("Ustaw w RUN config file")
        return
    
    template_path = Path(WORKFLOW_TEMPLATE_PATH)
    if not template_path.exists():
        logger.error(f"Workflow template nie istnieje: {WORKFLOW_TEMPLATE_PATH}")
        return
    
    logger.success(f"Workflow template: {template_path.name}")
    
    # ============================================================
    # WALIDACJA
    # ============================================================
    
    if not check_ffmpeg():
        logger.error("ffmpeg nie znaleziony!")
        return
    
    logger.success("ffmpeg OK")
    
    project_path = Path(PROJECT_FOLDER)
    if not project_path.exists():
        logger.error(f"Folder nie istnieje: {PROJECT_FOLDER}")
        return
    
    logger.success(f"Projekt: {project_path.name}")
    
    # ============================================================
    # CRITICAL FIX: Walidacja FORCE_RESOLUTION i DEFAULT_RESOLUTION
    # ============================================================
    
    if FORCE_RESOLUTION:
        force_w, force_h = FORCE_RESOLUTION
        if force_w % 8 != 0 or force_h % 8 != 0:
            logger.error(f"FORCE_RESOLUTION musi być podzielna przez 8!")
            logger.error(f"  Otrzymano: {force_w}x{force_h}")
            logger.error(f"  Popraw na: {round_to_multiple(force_w, 8)}x{round_to_multiple(force_h, 8)}")
            return
        logger.info(f"FORCE_RESOLUTION aktywne: {force_w}x{force_h}")
    
    if DEFAULT_RESOLUTION:
        def_w, def_h = DEFAULT_RESOLUTION
        if def_w % 8 != 0 or def_h % 8 != 0:
            logger.error(f"DEFAULT_RESOLUTION musi być podzielna przez 8!")
            logger.error(f"  Otrzymano: {def_w}x{def_h}")
            logger.error(f"  Popraw na: {round_to_multiple(def_w, 8)}x{round_to_multiple(def_h, 8)}")
            return
    
    # ============================================================
    # IMPROVED: MIN/MAX validation (z helpful messages)
    # ============================================================
    
    if MIN_WIDTH is not None and MIN_WIDTH > MAX_WIDTH:
        logger.error(f"BLAD KONFIGURACJI!")
        logger.error(f"  MIN_WIDTH ({MIN_WIDTH}) > MAX_WIDTH ({MAX_WIDTH})")
        logger.error(f"")
        logger.error(f"Rozwiazanie:")
        logger.error(f"  1. Zwieksz MAX_WIDTH do co najmniej {MIN_WIDTH}")
        logger.error(f"  2. Lub zmniejsz MIN_WIDTH do max {MAX_WIDTH}")
        logger.error(f"  3. Lub ustaw MIN_WIDTH = None (bez minimum)")
        return
    
    if MIN_HEIGHT is not None and MIN_HEIGHT > MAX_HEIGHT:
        logger.error(f"BLAD KONFIGURACJI!")
        logger.error(f"  MIN_HEIGHT ({MIN_HEIGHT}) > MAX_HEIGHT ({MAX_HEIGHT})")
        logger.error(f"")
        logger.error(f"Rozwiazanie:")
        logger.error(f"  1. Zwieksz MAX_HEIGHT do co najmniej {MIN_HEIGHT}")
        logger.error(f"  2. Lub zmniejsz MIN_HEIGHT do max {MAX_HEIGHT}")
        logger.error(f"  3. Lub ustaw MIN_HEIGHT = None (bez minimum)")
        return
    
    # Parse FLOW
    logger.section("Parsowanie FLOW")
    
    try:
        items, skip_transitions = parse_flow(FLOW, DEFAULTS, GENERIC_PROMPTS)
    except ValueError as e:
        logger.error(f"Błąd parsowania FLOW: {e}")
        return
    
    logger.success(f"Znaleziono {len(items)} plików")
    logger.info(f"Breaks: {len(skip_transitions)}")
    
    if len(items) < 2:
        logger.error("FLOW musi mieć minimum 2 pliki!")
        return
    
    # Weryfikacja plikow
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
        logger.error(f"Potrzeba minimum 2 pliki")
        return
    
    logger.success(f"Pliki OK! ({len(existing_items)} znalezionych)")
    
    # Aspect ratio validation
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
    
    # ============================================================
    # EKSTRAKCJA KLATEK
    # ============================================================
    
    logger.header("EKSTRAKCJA KLATEK")
    
    frames_folder = project_path / "frames"
    frames_folder.mkdir(exist_ok=True)
    
    logger.section("Auto-wykrywanie rozdzielczosci")
    
    if FORCE_RESOLUTION:
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
            
            # Apply MIN/MAX scaling
            target_w, target_h = calculate_scaled_resolution(
                orig_w, orig_h, 
                MAX_WIDTH, MAX_HEIGHT,
                MIN_WIDTH, MIN_HEIGHT
            )
            target_resolution = (target_w, target_h)
            
            print(f"  Oryginalna (video): {orig_w}x{orig_h}")
            print(f"  Docelowa: {target_w}x{target_h}")
            
            # Detailed scaling logs
            if (orig_w, orig_h) != (target_w, target_h):
                if target_w > orig_w or target_h > orig_h:
                    scale_factor = target_w / orig_w
                    pixels_orig = orig_w * orig_h
                    pixels_target = target_w * target_h
                    pixels_increase = pixels_target / pixels_orig
                    
                    logger.warning(f"  Upscaling {scale_factor:.2f}x ({pixels_increase:.1f}x więcej pikseli)")
                    if MIN_WIDTH or MIN_HEIGHT:
                        logger.info(f"  Powód: wymuszenie minimum {MIN_WIDTH}x{MIN_HEIGHT}")
                    logger.info(f"  Piksele: {pixels_orig:,} → {pixels_target:,}")
                    logger.warning(f"  💰 Uwaga: Więcej pikseli = wyższy koszt cloud!")
                else:
                    scale_factor = target_w / orig_w
                    logger.warning(f"  Downscaling {scale_factor:.2f}x")
                    logger.info(f"  Powód: przekroczenie limitu {MAX_WIDTH}x{MAX_HEIGHT}")
            else:
                logger.success(f"  Bez skalowania (w limitach)")
            
        else:
            # Brak video - użyj DEFAULT_RESOLUTION
            orig_w, orig_h = DEFAULT_RESOLUTION
            
            # Apply MIN/MAX scaling
            target_w, target_h = calculate_scaled_resolution(
                orig_w, orig_h,
                MAX_WIDTH, MAX_HEIGHT,
                MIN_WIDTH, MIN_HEIGHT
            )
            target_resolution = (target_w, target_h)
            
            logger.warning(f"  Brak video w FLOW - użyto DEFAULT_RESOLUTION jako base: {orig_w}x{orig_h}")
            
            if (orig_w, orig_h) != (target_w, target_h):
                if target_w > orig_w or target_h > orig_h:
                    scale_factor = target_w / orig_w
                    pixels_orig = orig_w * orig_h
                    pixels_target = target_w * target_h
                    pixels_increase = pixels_target / pixels_orig
                    
                    logger.warning(f"  Upscaling {scale_factor:.2f}x ({pixels_increase:.1f}x więcej pikseli)")
                    if MIN_WIDTH or MIN_HEIGHT:
                        logger.info(f"  Powód: wymuszenie minimum {MIN_WIDTH}x{MIN_HEIGHT}")
                    logger.info(f"  Piksele: {pixels_orig:,} → {pixels_target:,}")
                    logger.warning(f"  💰 Uwaga: Więcej pikseli = wyższy koszt cloud!")
                else:
                    scale_factor = target_w / orig_w
                    logger.warning(f"  Downscaling {scale_factor:.2f}x")
                    logger.info(f"  Powód: przekroczenie limitu {MAX_WIDTH}x{MAX_HEIGHT}")
                
                logger.success(f"  Finalna: {target_w}x{target_h}")
            else:
                logger.info(f"  DEFAULT_RESOLUTION w limitach - bez skalowania: {target_w}x{target_h}")
    
    # Upewnij się że jest podzielna przez 8
    target_w = round_to_multiple(target_w, 8)
    target_h = round_to_multiple(target_h, 8)
    target_resolution = (target_w, target_h)
    
    logger.success(f"  Finalna rozdzielczość: {target_w}x{target_h}")
    
    # Extract frames
    logger.section(f"Przygotowanie klatek")
    
    start_extract_time = time.time()
    frame_pairs = []
    total_frames_extracted = 0
    
    for idx in range(len(existing_items) - 1):
        i_a, item_a, path_a, type_a = existing_items[idx]
        i_b, item_b, path_b, type_b = existing_items[idx + 1]
        
        if i_a in skip_transitions:
            logger.info(f"\n  BREAK po [{i_a}] {item_a['file']} - pomijam transition")
            continue
        
        print(f"\n  [{idx+1}] {item_a['file']} → {item_b['file']}")
        
        # End frame z A
        end_frame_name = get_frame_filename(path_a, 'end')
        end_frame_path = frames_folder / end_frame_name
        
        if type_a == 'video':
            end_ok = ensure_frame_exists(path_a, type_a, end_frame_path, 'last', target_resolution, IMAGE_QUALITY)
        else:  # image
            end_ok = ensure_frame_exists(path_a, type_a, end_frame_path, None, target_resolution, IMAGE_QUALITY)
        
        # Start frame z B
        start_frame_name = get_frame_filename(path_b, 'start')
        start_frame_path = frames_folder / start_frame_name
        
        if type_b == 'video':
            start_ok = ensure_frame_exists(path_b, type_b, start_frame_path, 'first', target_resolution, IMAGE_QUALITY)
        else:  # image
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
    
    # ============================================================
    # CLOUD-SPECIFIC: UPLOAD FRAMES TO IMGBB
    # UPDATED: Zapisz delete_url dla cleanup
    # ============================================================
    
    logger.header("UPLOAD FRAMES TO IMGBB")
    
    for pair in frame_pairs:
        logger.info(f"  Uploading: {pair['end_frame'].name}")
        end_data = upload_to_imgbb(pair['end_frame'])
        
        if not end_data:
            logger.error(f"  Failed to upload {pair['end_frame'].name}")
            pair['upload_failed'] = True
            continue
        
        logger.info(f"  Uploading: {pair['start_frame'].name}")
        start_data = upload_to_imgbb(pair['start_frame'])
        
        if not start_data:
            logger.error(f"  Failed to upload {pair['start_frame'].name}")
            pair['upload_failed'] = True
            continue
        
        # Zapisz URLs + delete URLs
        pair['end_url'] = end_data['url']
        pair['start_url'] = start_data['url']
        pair['end_delete'] = end_data['delete_url']
        pair['start_delete'] = start_data['delete_url']
        pair['upload_failed'] = False
        
        logger.success(f"  ✓ Uploaded pair {pair['id']}")
    
    # Filter out failed uploads
    frame_pairs = [p for p in frame_pairs if not p.get('upload_failed', False)]
    
    if len(frame_pairs) == 0:
        logger.error("All uploads failed!")
        return
    
    logger.success(f"All frames uploaded! ({len(frame_pairs)} pairs)")
    
    # ============================================================
    # COST ESTIMATION
    # ============================================================
    
    logger.header("COST ESTIMATION")
    
    transitions_list = []
    for pair in frame_pairs:
        item_a = pair['item_a']
        transitions_list.append({
            'fps': item_a['fps'],
            'duration': item_a['duration'],
            'width': target_w,
            'height': target_h,
            'steps': item_a['steps'],
        })
    
    batch_cost = estimate_batch_cost(transitions_list)
    
    print(f"  Transitions: {batch_cost['count']}")
    print(f"  Resolution: {target_w}x{target_h}")
    print(f"  Total frames: {batch_cost['total_frames']}")
    print(f"  Total credits: {batch_cost['total_credits']:,}")
    print(f"  TOTAL COST: ${batch_cost['total_cost_usd']}")
    print(f"  Avg per transition: ${batch_cost['avg_cost_usd']}")
    print(f"  Estimated time: ~{batch_cost['total_time_min']:.0f} min")
    
    response = input(f"\n{Fore.YELLOW}💰 Continue? You will be charged ${batch_cost['total_cost_usd']}. (yes/no): {Style.RESET_ALL}")
    
    if response.lower() != 'yes':
        logger.warning("\nCancelled by user")
        return
    
    # ============================================================
    # GENERACJA CLOUD
    # UPDATED: Cleanup po successful download
    # ============================================================
    
    logger.header(f"GENEROWANIE PRZEJSC (CLOUD)")
    
    transitions_folder = project_path / "transitions"
    transitions_folder.mkdir(exist_ok=True)
    
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
        print(f"  Resolution: {target_w}x{target_h}")
        print(f"  Seed: {item_a['seed'] if item_a['seed'] else 'random'}")
        print(f"  Pos: {item_a['pos_prompt'][:60]}...")
        print(f"  Neg: {item_a['neg_prompt'][:60]}...")
        
        try:
            # Prepare params
            base_length = item_a['fps'] * item_a['duration']
            final_length = adjust_frame_count_for_wan(base_length)
            
            if base_length != final_length:
                logger.info(f"    Dostosowano klatki: {base_length} -> {final_length} (WAN rule)")
            
            params = {
                'width': target_w,
                'height': target_h,
                'length': final_length,
                'fps': item_a['fps'],
                'steps': item_a['steps'],
                'cfg': item_a['cfg'],
                'pos_prompt': item_a['pos_prompt'],
                'neg_prompt': item_a['neg_prompt'],
            }
            
            if item_a['seed']:
                params['seed'] = item_a['seed']
            
            # Start cloud generation
            run_id = start_comfy_icu_generation(
                COMFY_ICU_API_KEY,
                COMFY_ICU_WORKFLOW_ID,
                pair['end_url'],
                pair['start_url'],
                params,
                template_path
            )
            
            if not run_id:
                failed += 1
                logger.error(f"  Failed to start job")
                continue
            
            # Poll until complete
            video_url = poll_comfy_icu_status(
                COMFY_ICU_API_KEY,
                COMFY_ICU_WORKFLOW_ID,
                run_id,
                timeout=3600,
                check_interval=10
            )
            
            if not video_url:
                failed += 1
                logger.error(f"  Generation failed or timeout")
                continue
            
            # Download result
            if download_video(video_url, output_path):
                successful += 1
                logger.success(f"\n  PRZEJSCIE [{transition_num}] GOTOWE!")
                logger.success(f"  Lokalizacja: {output_path.relative_to(project_path)}")
                
                # ========================================
                # CLEANUP: Delete uploaded frames from ImgBB
                # ========================================
                logger.info(f"  Cleanup: Usuwam tymczasowe pliki z ImgBB...")
                
                deleted_count = 0
                if delete_from_imgbb(pair.get('end_delete', '')):
                    deleted_count += 1
                
                if delete_from_imgbb(pair.get('start_delete', '')):
                    deleted_count += 1
                
                if deleted_count == 2:
                    logger.success(f"  ✓ Cleanup: Usunięto 2 pliki z ImgBB")
                elif deleted_count > 0:
                    logger.warning(f"  ⚠️  Cleanup: Usunięto {deleted_count}/2 plików")
                else:
                    logger.warning(f"  ⚠️  Cleanup: Nie udało się usunąć plików")
            else:
                failed += 1
                logger.error(f"  Download failed")
        
        except Exception as e:
            failed += 1
            logger.error(f"\n  WYJATEK: {e}")
            import traceback
            traceback.print_exc()
        
        # Progress
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
    
    # ============================================================
    # FINALNE PODSUMOWANIE
    # ============================================================
    
    total_time = time.time() - start_time
    
    logger.header("FINALNE PODSUMOWANIE - CLOUD")
    print(f"  Projekt: {project_path.name}")
    print(f"  Transitions total: {len(frame_pairs)}")
    print(f"  Nowo wygenerowane: {successful}")
    print(f"  Pominiete: {skipped}")
    print(f"  Nieudane: {failed}")
    print(f"  Czas: {total_time/60:.1f}min")
    print(f"  Koszt estymowany: ${batch_cost['total_cost_usd']}")
    
    if successful > 0:
        actual_cost = batch_cost['avg_cost_usd'] * successful
        print(f"  Faktyczny koszt: ${actual_cost:.2f} (za {successful} transitions)")
    
    total_ok = successful + skipped
    
    if total_ok == len(frame_pairs) and failed == 0:
        logger.success("\nWszystkie transitions gotowe!")
        if skipped > 0:
            logger.info(f"  ({skipped} bylo juz wczesniej)")
    elif successful > 0:
        logger.warning(f"\nWygenerowano: {successful}, Pominieto: {skipped}, Nieudane: {failed}")
        if failed > 0:
            logger.warning("Sprawdz logi i uruchom ponownie dla brakujacych")
    else:
        if skipped == len(frame_pairs):
            logger.success("\nWszystkie juz istnialy")
        else:
            logger.error("\nBrak udanych generacji")