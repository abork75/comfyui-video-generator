"""
Moduł bazowy dla ComfyUI workflow automation
Zawiera klasy Logger i WorkflowRunner
"""

import yaml
import json
import requests
import os
import time
import random
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style

# Inicjalizacja kolorów
init(autoreset=True)


class Logger:
    """Kolorowe logowanie do terminala"""
    
    @staticmethod
    def info(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}] ℹ️  {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def success(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.GREEN}[{timestamp}] ✅ {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.YELLOW}[{timestamp}] ⚠️  {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def error(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.RED}[{timestamp}] ❌ {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def header(msg):
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}{msg.center(70)}")
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}\n")
    
    @staticmethod
    def section(msg):
        print(f"\n{Fore.BLUE}{'─'*70}")
        print(f"{Fore.BLUE}📌 {msg}")
        print(f"{Fore.BLUE}{'─'*70}{Style.RESET_ALL}")


def interrupt_comfyui(api_url: str, timeout: float = 5.0) -> dict:
    """POST {api_url}/interrupt — ComfyUI's own standard endpoint to abort
    whatever prompt is CURRENTLY EXECUTING on that instance, immediately.

    2026-09-11 (user request): none of the app's existing "cancel"/"stop"
    actions (chain_service.cancel_chain, single_transition_service.cancel,
    process_service.stop) call this — they only stop OUR side from waiting
    on the result (task.cancel() / subprocess.terminate()). The actual GPU
    work inside ComfyUI keeps running regardless until ComfyUI itself
    finishes, which is why the only way to truly stop a stuck job was
    killing the whole WSL2 instance. This is the missing piece: a direct
    call to ComfyUI's own interrupt API. No body needed — ComfyUI interrupts
    whatever is running on THAT instance, there's no per-job scoping (matches
    how ComfyUI itself only ever executes one prompt at a time)."""
    try:
        r = requests.post(f"{api_url}/interrupt", timeout=timeout)
        return {"ok": r.status_code == 200, "status_code": r.status_code}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


class WorkflowRunner:
    """Uniwersalny runner dla różnych workflow ComfyUI"""
    
    def __init__(self, config_path, workflows_base_path, api_url="http://127.0.0.1:8100"):
        """
        Inicjalizacja runnera
        
        Args:
            config_path: Ścieżka do pliku YAML z konfiguracją
            workflows_base_path: Folder gdzie są pliki JSON workflow
            api_url: Adres API ComfyUI (domyślnie localhost:8100)
        """
        self.logger = Logger()
        self.api_url = api_url
        self.workflows_base_path = workflows_base_path
        
        # Wczytaj konfigurację YAML
        self.logger.info(f"Ładowanie konfiguracji: {os.path.basename(config_path)}")
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        workflow_name = self.config.get('workflow_name', 'Unknown')
        self.logger.success(f"Załadowano: {workflow_name}")
        
        # Wczytaj workflow JSON
        workflow_file = self.config['workflow_file']
        workflow_path = os.path.join(workflows_base_path, workflow_file)
        
        self.logger.info(f"Ładowanie workflow: {workflow_file}")
        with open(workflow_path, 'r', encoding='utf-8') as f:
            self.workflow = json.load(f)
        
        self.logger.success(f"Workflow zawiera {len(self.workflow)} node'ów")
        
        # Statystyki
        self.stats = {
            'parameters_set': 0,
            'images_uploaded': 0,
        }
    
    def _validate_value(self, param_name, value):
        """Sprawdza czy wartość spełnia ograniczenia z YAML"""
        if 'constraints' not in self.config:
            return True
        
        constraints = self.config['constraints']
        
        if param_name in constraints:
            rules = constraints[param_name]
            
            if 'min' in rules and value < rules['min']:
                self.logger.warning(f"{param_name}={value} < minimum {rules['min']}")
                return False
            if 'max' in rules and value > rules['max']:
                self.logger.warning(f"{param_name}={value} > maximum {rules['max']}")
                return False
            
            if 'divisible_by' in rules and value % rules['divisible_by'] != 0:
                self.logger.warning(f"{param_name}={value} musi być podzielne przez {rules['divisible_by']}")
                return False
            
            if 'allowed' in rules and value not in rules['allowed']:
                self.logger.warning(f"{param_name}={value} nie jest dozwolone: {rules['allowed']}")
                return False
        
        return True
    
    def set_parameter(self, param_name, value):
        """
        Uniwersalna metoda do ustawiania parametrow w workflow
        
        Args:
            param_name: Nazwa parametru z konfiguracji (np. 'start_image', 'positive_prompt')
            value: Wartość do ustawienia
        
        Returns:
            bool: True jeśli sukces, False jeśli błąd
        """
        logger = self.logger
        
        # Sprawdz czy parametr istnieje w konfiguracji
        if param_name not in self.config['parameters']:
            logger.error(f"Nieznany parametr: {param_name}")
            logger.error(f"Dostepne parametry: {list(self.config['parameters'].keys())}")
            return False
        
        param_config = self.config['parameters'][param_name]
        node_id = str(param_config['node_id'])
        
        # Sprawdz czy node istnieje w workflow
        if node_id not in self.workflow:
            logger.error(f"Node {node_id} nie istnieje w workflow!")
            return False
        
        # Pobierz typ parametru
        param_type = param_config.get('type', 'string')
        
        if param_type == 'image':
            # Dla obrazow, value to nazwa pliku
            param_input = param_config.get('param_name', 'image')
            self.workflow[node_id]['inputs'][param_input] = value
            logger.success(f"  OK {param_name} -> Node {node_id}.{param_input} = {value}")
            
        elif param_type == 'string':
            # Dla tekstow (prompty)
            param_input = param_config.get('param_name', 'text')
            self.workflow[node_id]['inputs'][param_input] = value
            logger.success(f"  OK {param_name} -> Node {node_id}.{param_input} = {value}")
            
        else:
            # Dla innych typow (liczby, itp.)
            param_input = param_config.get('param_name')
            if param_input:
                self.workflow[node_id]['inputs'][param_input] = value
                logger.success(f"  OK {param_name} -> Node {node_id}.{param_input} = {value}")
            else:
                logger.error(f"Brak param_name dla {param_name}")
                return False
        
        return True
    
    def upload_image(self, image_path):
        """Przesyła obraz do ComfyUI przez API"""
        if not os.path.exists(image_path):
            self.logger.error(f"Plik nie istnieje: {image_path}")
            return None

        filename = os.path.basename(image_path)
        self.logger.info(f"Upload obrazu: {filename}")

        url = f"{self.api_url}/upload/image"

        try:
            with open(image_path, 'rb') as f:
                files = {'image': (filename, f)}
                data = {'overwrite': 'true'}
                response = requests.post(url, files=files, data=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                uploaded_name = result.get('name', filename)
                self.logger.success(f"  ✓ Przesłano jako: {uploaded_name}")
                self.stats['images_uploaded'] += 1
                return uploaded_name
            else:
                self.logger.error(f"  ✗ Błąd HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"  ✗ Wyjątek: {e}")
            return None
    
    def set_image(self, image_path, image_type='start_image'):
        """Przesyła i ustawia obraz w workflow"""
        uploaded_name = self.upload_image(image_path)
        if uploaded_name:
            return self.set_parameter(image_type, uploaded_name)
        return False
    
    def set_prompt(self, text, prompt_type='positive_prompt'):
        """Ustawia prompt"""
        return self.set_parameter(prompt_type, text)
    
    def set_video_params(self, width=688, height=464, fps=16, length=48):
        """Ustawia parametry wideo (rozdzielczosc, FPS, dlugosc)"""
        logger = self.logger
        
        # Parametry wideo (width, height, length)
        if "video_config" in self.config['parameters']:  # ← POPRAWIONE!
            video_config = self.config['parameters']['video_config']
            node_id = str(video_config['node_id'])
            
            logger.info(f"Ustawianie video_config -> Node {node_id}")
            
            self.workflow[node_id]['inputs']['width'] = width
            self.workflow[node_id]['inputs']['height'] = height
            self.workflow[node_id]['inputs']['length'] = length
            
            logger.success(f"  OK width = {width}")
            logger.success(f"  OK height = {height}")
            logger.success(f"  OK length = {length}")
        
        # FPS
        if "fps_config" in self.config['parameters']:  # ← POPRAWIONE!
            fps_config = self.config['parameters']['fps_config']
            node_id = str(fps_config['node_id'])
            param_name = fps_config.get('param_name', 'fps')
            
            logger.info(f"Ustawianie fps -> Node {node_id}")
            
            self.workflow[node_id]['inputs'][param_name] = fps
            logger.success(f"  OK fps = {fps}")
    
    # ========================================
    # 🔧 ZMIANA TUTAJ - FIX DLA UNIQUE SEED
    # ========================================
    def set_sampling_params(self, steps=20, cfg=4.0, seed=None):
        """
        Ustawia parametry samplingu dla dwoch samplerow (high i low)
        Wspiera dwuetapowy sampling z ComfyUI
        """
        logger = self.logger
        
        # ========================================
        # CRITICAL FIX: Force unique seed (prevent ComfyUI cache)
        # Without this, ComfyUI returns cached result (0.03s instead of 2min)
        # Problem: seed 608297159670858 był identyczny między runami
        # ========================================

        try:
            from debug_state import get_fix_seed
            _forced = get_fix_seed()
        except Exception:
            _forced = None

        if _forced is not None:
            # FIX-seed DEBUG mode (UI toggle) — verbatim seed, NO jitter, so
            # A/B runs are directly comparable. ComfyUI may cache-hit on an
            # otherwise-identical workflow; that's the accepted trade-off.
            seed = _forced
            logger.info(f"  ⚠️ FIX-seed DEBUG: seed = {seed} (verbatim, no jitter)")
        elif seed is None:
            # Generate unique seed using timestamp + random
            timestamp_part = int(time.time() * 1000000) % (2**31)  # Microseconds
            random_part = random.randint(0, 2**20)
            seed = (timestamp_part + random_part) % (2**63)  # Keep within int64 range
            logger.info(f"  Generated unique seed: {seed}")
        else:
            # Even if user provided seed, add timestamp variation to prevent cache
            timestamp_variation = int(time.time() * 1000) % 100000
            original_seed = seed
            seed = (seed + timestamp_variation) % (2**63)
            logger.info(f"  Using seed {original_seed} + timestamp variation = {seed}")
        
        # ========================================
        # SAMPLER HIGH
        # ========================================
        if "sampler_high" in self.config['parameters']:
            sampler_high = self.config['parameters']['sampler_high']
            node_id = str(sampler_high['node_id'])
            
            logger.info(f"Ustawianie sampler_high -> Node {node_id}")
            
            # Wartości do ustawienia (dla sampler HIGH)
            values_to_set = {
                'seed': seed,
                'steps': steps,
                'cfg': cfg,
                'start_at_step': 0,
                'end_at_step': 10,
                'return_with_leftover_noise': 'enable'
            }
            
            # Ustaw parametry wedlug mappingu z YAML
            for param_name, value_key in sampler_high['params'].items():
                # param_name = nazwa parametru w workflow (np. "noise_seed")
                # value_key = klucz wartości (np. "seed")
                
                if value_key in values_to_set:
                    value = values_to_set[value_key]
                    self.workflow[node_id]['inputs'][param_name] = value
                    logger.success(f"  OK {param_name} = {value}")
        
        # ========================================
        # SAMPLER LOW
        # ========================================
        if "sampler_low" in self.config['parameters']:
            sampler_low = self.config['parameters']['sampler_low']
            node_id = str(sampler_low['node_id'])
            
            logger.info(f"Ustawianie sampler_low -> Node {node_id}")
            
            # Wartości do ustawienia (dla sampler LOW)
            values_to_set = {
                'steps': steps,
                'cfg': cfg,
                'start_at_step': 10,
                'end_at_step': 10000,
                'return_with_leftover_noise': 'disable'
            }
            
            # Ustaw parametry wedlug mappingu z YAML
            for param_name, value_key in sampler_low['params'].items():
                if value_key in values_to_set:
                    value = values_to_set[value_key]
                    self.workflow[node_id]['inputs'][param_name] = value
                    logger.success(f"  OK {param_name} = {value}")
    
    def print_summary(self):
        """Wyświetla podsumowanie ustawionych parametrów"""
        self.logger.section("Podsumowanie konfiguracji")
        
        key_params = {
            'Start Image': self.workflow.get('80', {}).get('inputs', {}).get('image', 'NOT SET'),
            'End Image': self.workflow.get('89', {}).get('inputs', {}).get('image', 'NOT SET'),
            'Width': self.workflow.get('81', {}).get('inputs', {}).get('width', 'DEFAULT'),
            'Height': self.workflow.get('81', {}).get('inputs', {}).get('height', 'DEFAULT'),
            'Length': self.workflow.get('81', {}).get('inputs', {}).get('length', 'DEFAULT'),
            'FPS': self.workflow.get('86', {}).get('inputs', {}).get('fps', 'DEFAULT'),
            'Steps': self.workflow.get('84', {}).get('inputs', {}).get('steps', 'DEFAULT'),
            'CFG': self.workflow.get('84', {}).get('inputs', {}).get('cfg', 'DEFAULT'),
            'Seed': self.workflow.get('84', {}).get('inputs', {}).get('noise_seed', 'RANDOM'),
        }
        
        for key, value in key_params.items():
            print(f"  {Fore.WHITE}• {key:15s}: {Fore.CYAN}{value}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.WHITE}Parametrów ustawionych: {Fore.GREEN}{self.stats['parameters_set']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Obrazów przesłanych:   {Fore.GREEN}{self.stats['images_uploaded']}{Style.RESET_ALL}")
    
    def run(self, wait_for_completion=False):
        """Wysyła workflow do ComfyUI"""
        self.logger.section("Wysyłanie workflow do ComfyUI")
        
        # ========================================
        # ZMIANA: Logi do folderu logs/
        # ========================================
        logs_folder = Path("logs")
        logs_folder.mkdir(exist_ok=True)
        
        debug_file = logs_folder / f"debug_workflow_{int(time.time())}.json"
        
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(self.workflow, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Debug: zapisano do {debug_file}")
        # ========================================
        
        url = f"{self.api_url}/prompt"
        payload = {
            "prompt": self.workflow,
            "client_id": f"workflow_runner_{int(time.time())}"
        }
        
        try:
            self.logger.info("Wysyłanie request do API...")
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                prompt_id = result.get('prompt_id')
                
                self.logger.success(f"Workflow wysłany pomyślnie!")
                self.logger.info(f"Prompt ID: {Fore.YELLOW}{prompt_id}{Style.RESET_ALL}")
                
                if wait_for_completion:
                    self.logger.info("Oczekiwanie na zakończenie...")
                    outputs = self._wait_for_completion(prompt_id)
                    return {'prompt_id': prompt_id, 'outputs': outputs}
                
                return {'prompt_id': prompt_id}
                
            else:
                self.logger.error(f"HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Wyjątek: {e}")
            return None
    
    def _wait_for_completion(self, prompt_id, timeout=14400, check_interval=5):
        """Czeka aż generacja się skończy.

        timeout=14400 (4h, było 3600/1h — 2026-09-11): realne generacje WAN
        na trudniejszych scenach/rozdzielczościach potrafią przekroczyć
        godzinę (potwierdzone: 21min pass wysoki + ~56min pass niski = >77min
        na jednym kroku). Krótki timeout tu nic nie oszczędza — porzucenie
        czekania NIE zatrzymuje ComfyUI, GPU liczy dalej niezależnie — tylko
        fałszywie zgłasza błąd apce, mimo że generacja i tak się skończy.
        Do prawdziwego przerywania służy /interrupt (patrz workflow_base.
        interrupt_comfyui), nie ten timeout."""
        url = f"{self.api_url}/history/{prompt_id}"
        start_time = time.time()

        # 2026-09-28 (user-reported multi-hour stall, cause not pinned down):
        # this loop can legitimately run for up to `timeout` seconds (4h)
        # with ZERO log output otherwise - `self.logger` below is a plain
        # print() (see class Logger above), never reaches logs/gen_*.log, so
        # a genuine network/ComfyUI stall here was previously indistinguishable
        # from "just a slow generation" after the fact. Heartbeat every ~5min
        # through process_service.log_sys (same persisted/UI-visible channel
        # as the rest of the app's generation log) so a future stall shows
        # either regular heartbeats with no completion (ComfyUI/WSL2-side) or
        # heartbeats stopping outright (a single HTTP call stuck past its own
        # stated timeout - a known class of WSL2 virtual-adapter flakiness).
        # Lazy/guarded: this module also runs standalone outside the FastAPI
        # app (legacy subprocess scripts) where app.services isn't importable;
        # heartbeat silently no-ops there instead of breaking generation.
        def _heartbeat(elapsed_s: float) -> None:
            try:
                from app.services.process_service import process_service
                process_service.log_sys(
                    f"  ⏳ Nadal czekam na ComfyUI (prompt_id={prompt_id}, {elapsed_s/60:.1f} min)..."
                )
            except Exception:
                pass

        last_heartbeat = start_time

        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    history = response.json()

                    if prompt_id in history:
                        result = history[prompt_id]

                        if "outputs" in result:
                            elapsed = time.time() - start_time
                            print()
                            self.logger.success(f"Generacja zakończona! Czas: {elapsed:.1f}s")
                            return result["outputs"]

                        if "status" in result:
                            status = result["status"]
                            if status.get("status_str") == "error":
                                print()
                                self.logger.error(f"Błąd: {status.get('messages', [])}")
                                return None

                print(".", end="", flush=True)
                now = time.time()
                if now - last_heartbeat >= 300:
                    _heartbeat(now - start_time)
                    last_heartbeat = now
                time.sleep(check_interval)

            except Exception as e:
                print()
                self.logger.warning(f"Błąd sprawdzania: {e}")
                now = time.time()
                if now - last_heartbeat >= 300:
                    _heartbeat(now - start_time)
                    last_heartbeat = now
                time.sleep(check_interval)

        print()
        self.logger.error(f"Timeout po {timeout}s")
        return None