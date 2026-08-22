# -*- coding: utf-8 -*-
"""
LTX Backend - ComfyUI na Linux/WSL2 (ta sama instancja co WAN, port 8189)

Dwa tryby - wybór PLIKU workflow (nie patch w locie jak w WAN):
- FF   (tylko start_frame)      -> _LTX23_FF.json
- FFLF (start_frame + end_frame) -> _LTX23_FFLF.json (LTXVAddGuide/LTXVCropGuides)

Wariant 8-step / 20-step to NIEZALEŻNA oś - patch w locie (sigmas + cfg),
dotyczy obu plików tak samo. Distilled speed LoRA (node 2199) zostaje wpięty
dla obu wariantów (świadoma decyzja - stabilizuje obraz, usuwa artefakty).
"""

import random
import shutil
import time
from pathlib import Path

from .base_backend import BaseBackend
from workflow_base import WorkflowRunner, Logger
from utils.video_utils import ensure_24fps

# Default model = full precision (NOT gguf) - node 2213 (UNETLoader), distilled variant
_DEFAULT_LTX_MODEL = "ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors"


class LtxBackend(BaseBackend):
    """LTX 2.3 backend (linux/WSL2 ComfyUI)"""

    def __init__(self, config):
        super().__init__(config)
        self.logger = Logger()

        self.config_path_ff   = config.get('config_path_ff', '')
        self.config_path_fflf = config.get('config_path_fflf', '')
        self.workflows_path   = config.get('workflows_path', '')
        self.output_folder    = config.get('comfyui_output_folder', '')
        self.api_url          = config.get('api_url', 'http://127.0.0.1:8189')

        self.workflow_runner = None

    def validate_requirements(self):
        """Walidacja wymagań dla backendu LTX"""

        if not self.config_path_ff or not Path(self.config_path_ff).exists():
            raise Exception(f"LTX FF config not found: {self.config_path_ff}")

        if not self.config_path_fflf or not Path(self.config_path_fflf).exists():
            raise Exception(f"LTX FFLF config not found: {self.config_path_fflf}")

        if not self.workflows_path or not Path(self.workflows_path).exists():
            raise Exception(f"Workflows path not found: {self.workflows_path}")

        if not self.output_folder or not Path(self.output_folder).exists():
            raise Exception(f"ComfyUI output folder not found: {self.output_folder}")

        try:
            import requests
            response = requests.get(f"{self.api_url}/system_stats", timeout=5)
            if response.status_code != 200:
                raise Exception(f"ComfyUI API zwróciło {response.status_code}")
        except Exception as e:
            raise Exception(f"Brak połączenia z ComfyUI ({self.api_url}): {e}")

        self.logger.success(f"LTX backend gotowy ({self.api_url})")
        return True

    def prepare_inputs(self, pair, workflow):
        """Przekazuje start_frame i opcjonalny end_frame"""
        return {
            'start_frame': pair['start_frame'],
            'end_frame': pair.get('end_frame'),
        }

    def execute(self, inputs, params, workflow):
        """Wykonaj workflow na ComfyUI (LTX 2.3)"""

        try:
            # ============================================================
            # DETECT MODE: wybór PLIKU (nie patch w locie jak WAN)
            # FF (brak end_frame) vs FFLF (start_frame + end_frame)
            # ============================================================

            is_fflf_mode = inputs['end_frame'] is not None

            if is_fflf_mode:
                self.logger.info("  Tryb: FFLF (kotwica na końcu - end_frame)")
                config_path = self.config_path_fflf
            else:
                self.logger.info("  Tryb: FF (brak end_frame)")
                config_path = self.config_path_ff

            # ============================================================
            # RESET: świeży runner na każdy run (jak w WAN - bez tego drugi
            # run używa zmodyfikowanego workflow z pierwszego)
            # ============================================================

            self.workflow_runner = WorkflowRunner(
                config_path,
                self.workflows_path,
                api_url=self.api_url,
            )

            # ============================================================
            # WARIANT 8-step / 20-step: patch w locie, PRZED ustawieniem
            # obrazów/promptów (swap przepina połączenia w grafie)
            # ============================================================

            ltx_variant = params.get('ltx_variant') or '8step'
            if ltx_variant == '20step':
                self._swap_to_20step(self.workflow_runner, params)
            # 8-step: nic nie robić, to baked-in default w pliku

            # ============================================================
            # MODEL: pełny (.safetensors, node 2213) vs GGUF (node 187).
            # Musi nastąpić PRZED ustawieniem obrazów/promptów - przepina
            # źródło dla node 2201 (base loader) i node 2107 (bypass distilled
            # LoRA dla pełnego modelu - patrz _set_model).
            # ============================================================

            self._set_model(self.workflow_runner, params.get('ltx_model'), params.get('lora_strength'))

            # ============================================================
            # 1. Ustaw obraz startowy (FIRST FRAME)
            # ============================================================

            self.logger.info("  Ustawianie start_image...")
            if not self.workflow_runner.set_image(str(inputs['start_frame']), 'start_image'):
                self.logger.error("  Błąd ustawiania start_image")
                return None

            # ============================================================
            # 2. Ustaw obraz końcowy (TYLKO w trybie FFLF - LAST FRAME)
            # ============================================================

            if is_fflf_mode:
                self.logger.info("  Ustawianie end_image...")
                if not self.workflow_runner.set_image(str(inputs['end_frame']), 'end_image'):
                    self.logger.error("  Błąd ustawiania end_image")
                    return None
            else:
                self.logger.info("  FF mode: pomijam end_image (nie potrzebne)")

            # ============================================================
            # 3. Ustaw prompty
            # ============================================================

            self.logger.info("  Ustawianie promptów...")
            self.workflow_runner.set_prompt(params['pos_prompt'], 'positive_prompt')
            self.workflow_runner.set_prompt(params['neg_prompt'], 'negative_prompt')

            # ============================================================
            # 4. Ustaw parametry wideo
            # ============================================================

            self.logger.info("  Ustawianie parametrów wideo...")
            self._set_video_params(params, is_fflf_mode)

            # ============================================================
            # 5. Content LoRAs (lista, Power Lora Loader node 2107)
            # ============================================================

            self._inject_loras(self.workflow_runner, params.get('loras') or [])

            # ============================================================
            # 6. Ustaw seed
            # ============================================================

            self.logger.info("  Ustawianie seed...")
            self._set_seed(params.get('seed'))

            # ============================================================
            # 7. Wyczyść folder output
            # ============================================================

            self.logger.info("  Czyszczenie folderu output...")
            start_time = time.time()
            self._clean_output_folder()

            # ============================================================
            # 8. Uruchom workflow
            # ============================================================

            self.logger.info("  Uruchamianie workflow...")

            result = self.workflow_runner.run(wait_for_completion=True)
            elapsed = time.time() - start_time

            if not result:
                self.logger.error("  Workflow zakończył się błędem")
                return None

            self.logger.success(f"  Workflow ukończony w {elapsed:.1f}s!")

            # ============================================================
            # 9. Znajdź plik wideo
            # ============================================================

            output_video = self._find_output_from_history(result) or self._find_output_video(start_time)

            if not output_video:
                return None

            # ============================================================
            # 10. Przenieś do docelowej lokalizacji
            # ============================================================

            target_path = params.get('output_path')

            if target_path and target_path.exists():
                self.logger.warning(f"  Nadpisywanie: {target_path.name}")
                target_path.unlink()

            if target_path:
                shutil.move(str(output_video), str(target_path))
                self.logger.success(f"  Zapisano: {target_path.name}")
                ensure_24fps(target_path, self.logger)
                return target_path
            else:
                self.logger.success(f"  Wideo: {output_video}")
                ensure_24fps(output_video, self.logger)
                return output_video

        except Exception as e:
            self.logger.error(f"  Błąd LTX backend: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ============================================================
    # HELPERS
    # ============================================================

    def _set_video_params(self, params, is_fflf_mode):
        """Ustawia parametry wideo przez set_parameter (YAML-driven)"""
        runner = self.workflow_runner

        if 'width' in params:
            # Snap do wielokrotności 64 - target rozdzielczość (po pass2 upscale x2),
            # pass1 silnik wymaga /32, więc target musi być /64 (patrz notatka pamięci LTX)
            w = (int(params['width']) // 64) * 64
            runner.set_parameter('width', w)

        if 'height' in params:
            h = (int(params['height']) // 64) * 64
            runner.set_parameter('height', h)

        if 'duration' in params:
            runner.set_parameter('duration', int(round(params['duration'])))

        if params.get('ff_strength') is not None:
            runner.set_parameter('ff_strength', float(params['ff_strength']))

        if is_fflf_mode and params.get('lf_strength') is not None:
            runner.set_parameter('lf_strength', float(params['lf_strength']))

        # lora_strength (distilled) is handled in _set_model() - it's coupled to
        # which loader/bypass is active, not a plain leaf parameter.

        if 'filename_prefix' in params:
            runner.set_parameter('filename_prefix', params['filename_prefix'])

        fi = params.get('frame_interpolation')
        if fi is not None:
            # True/False -> RIFE multiplier (2 = enabled, 1 = disabled)
            multiplier = 2 if fi else 1
            runner.set_parameter('frame_interpolation', multiplier)

    def _set_model(self, runner, model_filename, lora_strength):
        """Przełącza bazowy model: GGUF (node 187, UnetLoaderGGUF) vs pełny .safetensors
        (node 2213, UNETLoader). Rozstrzyga po rozszerzeniu nazwy pliku.

        Dla pełnego modelu (.safetensors) BYPASSUJE distilled speed LoRA (node 2199)
        całkowicie - przepina node 2107 (Power Lora Loader) tak, by brał model
        bezpośrednio z node 2203, z pominięciem 2199. Ustawienie strength_model=0
        NIE wystarczy - node i tak ładowałby się do VRAM (czas + ryzyko OOM).
        Dla GGUF (domyślne zachowanie) 2199 zostaje wpięty normalnie, ze skonfigurowaną
        (lub domyślną 0.61) siłą."""
        wf = runner.workflow
        name = (model_filename or _DEFAULT_LTX_MODEL).strip()
        is_gguf = name.lower().endswith('.gguf')

        if is_gguf:
            if '187' in wf:
                wf['187']['inputs']['unet_name'] = name
            if '2201' in wf:
                wf['2201']['inputs']['model'] = ['187', 0]
            if '2107' in wf:
                wf['2107']['inputs']['model'] = ['2199', 0]
            if '2199' in wf:
                wf['2199']['inputs']['strength_model'] = float(lora_strength) if lora_strength is not None else 0.61
            self.logger.info(f"  Model: GGUF {name} (distilled LoRA aktywna)")
        else:
            if '2213' in wf:
                wf['2213']['inputs']['unet_name'] = name
            if '2201' in wf:
                wf['2201']['inputs']['model'] = ['2213', 0]
            if '2107' in wf:
                # Bypass node 2199 entirely - nie tylko strength=0, żeby nie ładował się do VRAM
                wf['2107']['inputs']['model'] = ['2203', 0]
            self.logger.info(f"  Model: pełny {name} (distilled LoRA bypass - nieużywana)")

    def _swap_to_20step(self, runner, params):
        """Przełącza wariant 8-step -> 20-step: sigmas (pass1: 215->2, pass2: 216->5)
        + cfg (pass1 node 36: 1->3, pass2 node 8: 1->2). Distilled LoRA (node 2199)
        NIE jest wyłączany - zostaje wpięty dla obu wariantów (świadoma decyzja user)."""
        wf = runner.workflow
        if '13' in wf:
            wf['13']['inputs']['sigmas'] = ['2', 0]
        if '21' in wf:
            wf['21']['inputs']['sigmas'] = ['5', 0]
        cfg_pass1 = float(params.get('cfg_pass1') or 3)
        cfg_pass2 = float(params.get('cfg_pass2') or 2)
        if '36' in wf:
            wf['36']['inputs']['cfg'] = cfg_pass1
        if '8' in wf:
            wf['8']['inputs']['cfg'] = cfg_pass2
        self.logger.info(
            f"  🎨 20-step: sigmas 215→2 (pass1), 216→5 (pass2), "
            f"cfg pass1={cfg_pass1} pass2={cfg_pass2}"
        )

    def _inject_loras(self, runner, loras: list) -> None:
        """Wstrzykuje listę content LoRA do node 2107 (Power Lora Loader rgthree).
        Kształt (potwierdzony z realnego eksportu ComfyUI): lora_N: {on, lora, strength},
        N od 1. Usuwa najpierw wszystkie istniejące lora_N z załadowanego pliku bazowego
        (na wypadek gdyby template miał baked-in wpisy z eksportu testowego)."""
        wf = runner.workflow
        if '2107' not in wf:
            return
        node_inputs = wf['2107']['inputs']
        for k in [k for k in node_inputs if k.startswith('lora_')]:
            del node_inputs[k]
        added = []
        for i, lora in enumerate(loras, start=1):
            name = (lora.get('name') or '').strip()
            if not name:
                continue
            node_inputs[f'lora_{i}'] = {
                'on': True,
                'lora': name,
                'strength': float(lora.get('strength', 1.0)),
            }
            added.append(name)
        if added:
            names = ", ".join(Path(n).stem for n in added)
            self.logger.info(f"  LoRAs ({len(added)}): {names}")

    def _set_seed(self, seed=None):
        """Ustawia unikalne seedy dla obu RandomNoise (node 15 = pass1, node 14 = pass2).
        LTX ma dwa niezależne RandomNoise, nie jeden 'seed' param jak WAN."""

        def _unique(base):
            if base is None or base == -1:
                timestamp_part = int(time.time() * 1_000_000) % (2**31)
                random_part = random.randint(0, 2**20)
                return (timestamp_part + random_part) % (2**63)
            timestamp_variation = int(time.time() * 1000) % 100000
            return (base + timestamp_variation) % (2**63)

        wf = self.workflow_runner.workflow
        seed_pass1 = _unique(seed)
        seed_pass2 = _unique((seed + 1) if seed not in (None, -1) else None)
        if '15' in wf:
            wf['15']['inputs']['noise_seed'] = seed_pass1
        if '14' in wf:
            wf['14']['inputs']['noise_seed'] = seed_pass2
        self.logger.info(f"  Seed pass1={seed_pass1}, pass2={seed_pass2}")

    def _clean_output_folder(self):
        """Czyści pliki mp4 z podfolderów Ltx23_FF/ i Ltx23_FFLF/"""
        comfyui_output = Path(self.output_folder)
        cleaned = 0

        for subfolder_name in ('Ltx23_FF', 'Ltx23_FFLF'):
            subfolder = comfyui_output / subfolder_name
            if not subfolder.exists():
                continue
            for f in subfolder.glob("*.mp4"):
                try:
                    f.unlink()
                    cleaned += 1
                except Exception as e:
                    self.logger.warning(f"    Nie można usunąć {f.name}: {e}")

        if cleaned > 0:
            self.logger.info(f"    Wyczyszczono {cleaned} starych plików")

    def _find_output_from_history(self, run_result: dict):
        """
        Znajdź plik wideo na podstawie outputs zwróconych przez ComfyUI history.
        Bardziej niezawodne niż timestamp-scan (patrz linux_backend.py - ten sam wzorzec).
        """
        outputs = run_result.get('outputs') if isinstance(run_result, dict) else None
        if not outputs:
            return None

        comfyui_output = Path(self.output_folder)

        for node_id, node_out in outputs.items():
            for key in ('videos', 'images', 'gifs'):
                for item in node_out.get(key, []):
                    if item.get('type') != 'output':
                        continue
                    subfolder = item.get('subfolder', '')
                    filename  = item.get('filename', '')
                    if not filename:
                        continue
                    candidate = comfyui_output / subfolder / filename if subfolder else comfyui_output / filename
                    if candidate.exists() and candidate.suffix.lower() in ('.mp4', '.avi', '.mov', '.mkv'):
                        self.logger.info(f"  Znaleziono (history): {candidate.name}")
                        return candidate

        return None

    def _find_output_video(self, start_time):
        """Szuka nowo wygenerowanego pliku wideo (fallback: timestamp-scan)"""
        comfyui_output = Path(self.output_folder)

        search_dirs = [comfyui_output]
        for subfolder_name in ('Ltx23_FF', 'Ltx23_FFLF'):
            sf = comfyui_output / subfolder_name
            if sf.exists():
                search_dirs.append(sf)

        video_files = []
        for search_dir in search_dirs:
            for ext in ['.mp4', '.avi', '.mov', '.mkv']:
                video_files.extend(search_dir.glob(f'*{ext}'))

        if not video_files:
            self.logger.error(f"  Brak plików wideo w {comfyui_output}")
            return None

        recent = [f for f in video_files if f.stat().st_mtime > start_time]

        if not recent:
            self.logger.error(f"  Brak nowych plików wideo (timestamp > {start_time:.0f})")
            for f in video_files:
                age = time.time() - f.stat().st_mtime
                self.logger.warning(f"    {f.name} (wiek: {age:.0f}s)")
            return None

        newest = max(recent, key=lambda f: f.stat().st_mtime)
        self.logger.info(f"  Znaleziono: {newest.name}")
        return newest

    def cleanup(self, inputs):
        pass

    def estimate_cost(self, params):
        # LTX 2-pass GGUF, wolniejszy niż WAN Lightning
        return {
            'credits': 0,
            'cost_usd': 0.0,
            'estimated_time_min': 20.0,
        }
