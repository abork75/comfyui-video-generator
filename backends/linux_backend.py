# -*- coding: utf-8 -*-
"""
Linux Backend - ComfyUI na Linux/WSL2
Obsługuje oba tryby:
- I2V   (tylko start_frame - wolna generacja)
- I2V2I (start_frame + end_frame - interpolacja tranzycji)
"""

import time
import shutil
from pathlib import Path

from .base_backend import BaseBackend
from workflow_base import WorkflowRunner, Logger


class LinuxBackend(BaseBackend):
    """Linux/WSL2 ComfyUI backend"""

    def __init__(self, config):
        super().__init__(config)
        self.logger = Logger()

        self.config_path = config.get('config_path', '')
        self.workflows_path = config.get('workflows_path', '')
        self.output_folder = config.get('comfyui_output_folder', '')
        self.api_url = config.get('api_url', 'http://127.0.0.1:8188')

        self.workflow_runner = None

    def validate_requirements(self):
        """Walidacja wymagań dla backendu Linux"""

        if not self.config_path or not Path(self.config_path).exists():
            raise Exception(f"Linux config not found: {self.config_path}")

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

        self.workflow_runner = WorkflowRunner(
            self.config_path,
            self.workflows_path,
            api_url=self.api_url
        )

        self.logger.success(f"Linux backend gotowy ({self.api_url})")
        return True

    def prepare_inputs(self, pair, workflow):
        """Przekazuje start_frame i opcjonalny end_frame"""
        return {
            'start_frame': pair['start_frame'],
            'end_frame': pair.get('end_frame'),
        }

    def execute(self, inputs, params, workflow):
        """Wykonaj workflow na lokalnym ComfyUI (Linux)"""

        try:
            # ============================================================
            # DETECT MODE: I2V (tylko start) vs I2V2I (start + end)
            # Identyczna logika jak w local_backend
            # ============================================================

            is_i2v_mode = params.get('is_i2v_mode', False) or inputs['end_frame'] is None

            if is_i2v_mode:
                self.logger.info(f"  Tryb: I2V (wolna generacja - brak end_frame)")
            else:
                self.logger.info(f"  Tryb: I2V2I (interpolacja - tranzycja z end_frame)")

            # ============================================================
            # RESET: Przeładuj runner (czysty stan przed każdym runem)
            # Bez tego drugi run używa ZMODYFIKOWANEGO workflow z pierwszego!
            # ============================================================

            self.workflow_runner = WorkflowRunner(
                self.config_path,
                self.workflows_path,
                api_url=self.api_url
            )

            # ============================================================
            # I2V MODE: Odłącz end_image z node 89 i any_01 z Any Switch (116)
            # I2V2I MODE: end_image zostaje, Any Switch używa any_01 (end frame)
            # ============================================================

            if is_i2v_mode:
                self.logger.info(f"  I2V mode: Odłączam end_image z node 89 i any_01 z node 116")

                # 1. Usuń end_image z WanVideoImageToVideoEncode (node 89)
                wan_node_id = '89'
                if wan_node_id in self.workflow_runner.workflow:
                    wan_inputs = self.workflow_runner.workflow[wan_node_id].get('inputs', {})
                    if 'end_image' in wan_inputs:
                        del wan_inputs['end_image']
                        self.logger.info(f"    ✓ Usunięto end_image z Node {wan_node_id}")

                # 2. Usuń any_01 z Any Switch (node 116)
                # → Switch automatycznie fallbackuje na any_02 (start frame node 67)
                # → Color Match bierze start frame jako referencję koloru
                any_switch_id = '116'
                if any_switch_id in self.workflow_runner.workflow:
                    switch_inputs = self.workflow_runner.workflow[any_switch_id].get('inputs', {})
                    if 'any_01' in switch_inputs:
                        del switch_inputs['any_01']
                        self.logger.info(f"    ✓ Usunięto any_01 z Node {any_switch_id} (Color Match użyje start frame)")

            # ============================================================
            # 1. Ustaw obraz startowy (node 67 - LoadImage)
            # ============================================================

            self.logger.info(f"  Ustawianie start_image...")

            if not self.workflow_runner.set_image(
                str(inputs['start_frame']),
                'start_image'
            ):
                self.logger.error(f"  Błąd ustawiania start_image")
                return None

            # ============================================================
            # 2. Ustaw end_image (TYLKO w trybie I2V2I)
            # Nowy workflow: end frame ma dedykowany LoadImage node 98
            # + Resize node 99 + podłączony do node 89 i Any Switch 116
            # ============================================================

            if not is_i2v_mode:
                self.logger.info(f"  Ustawianie end_image...")

                # Ustaw przez YAML (node 98 - dedykowany LoadImage dla end frame)
                if not self.workflow_runner.set_image(
                    str(inputs['end_frame']),
                    'end_image'
                ):
                    self.logger.error(f"  Błąd ustawiania end_image")
                    return None

                self.logger.info(f"    ✓ Color Match użyje end frame jako referencję koloru")
            else:
                self.logger.info(f"  I2V mode: Pomijam end_image (nie potrzebne)")

            # ============================================================
            # 3. Ustaw prompty
            # ============================================================

            self.logger.info(f"  Ustawianie promptów...")
            self.workflow_runner.set_prompt(params['pos_prompt'], 'positive_prompt')
            self.workflow_runner.set_prompt(params['neg_prompt'], 'negative_prompt')

            # ============================================================
            # 4. Ustaw parametry wideo
            # ============================================================

            self.logger.info(f"  Ustawianie parametrów wideo...")
            self._set_video_params(params)

            # ============================================================
            # 5. Ustaw seed
            # ============================================================

            self.logger.info(f"  Ustawianie seed...")
            self._set_seed(params.get('seed'))

            # ============================================================
            # 6. Wyczyść folder output
            # ============================================================

            self.logger.info(f"  Czyszczenie folderu output...")
            start_time = time.time()
            self._clean_output_folder()

            # ============================================================
            # 7. Uruchom workflow
            # ============================================================

            self.logger.info(f"  Uruchamianie workflow...")

            result = self.workflow_runner.run(wait_for_completion=True)
            elapsed = time.time() - start_time

            if not result:
                self.logger.error(f"  Workflow zakończył się błędem")
                return None

            self.logger.success(f"  Workflow ukończony w {elapsed:.1f}s!")

            # ============================================================
            # 8. Znajdź plik wideo
            # ============================================================

            output_video = self._find_output_video(start_time)

            if not output_video:
                return None

            # ============================================================
            # 9. Przenieś do docelowej lokalizacji
            # ============================================================

            target_path = params.get('output_path')

            if target_path and target_path.exists():
                self.logger.warning(f"  Nadpisywanie: {target_path.name}")
                target_path.unlink()

            if target_path:
                shutil.move(str(output_video), str(target_path))
                self.logger.success(f"  Zapisano: {target_path.name}")
                return target_path
            else:
                self.logger.success(f"  Wideo: {output_video}")
                return output_video

        except Exception as e:
            self.logger.error(f"  Błąd Linux backend: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ============================================================
    # HELPERS
    # ============================================================

    def _set_video_params(self, params):
        """Ustawia parametry wideo przez set_parameter (YAML-driven)"""
        runner = self.workflow_runner

        if 'width' in params:
            # Snap to nearest multiple of 16 — WanVideo node 68 (ImageResizeKJv2)
            # has divisible_by=16; passing non-aligned values causes silent adjustment
            # and makes extracted frames inconsistent with actual video output.
            w = (int(params['width']) // 16) * 16
            if w != params['width']:
                self.logger.info(f"  width {params['width']} → snap to 16 → {w}")
            runner.set_parameter('width', w)

        if 'height' in params:
            h = (int(params['height']) // 16) * 16
            if h != params['height']:
                self.logger.info(f"  height {params['height']} → snap to 16 → {h}")
            runner.set_parameter('height', h)

        if 'length' in params:
            runner.set_parameter('num_frames', params['length'])

        if 'fps' in params:
            runner.set_parameter('frame_rate', params['fps'])

        if 'steps' in params:
            runner.set_parameter('steps', params['steps'])

        if 'cfg' in params:
            runner.set_parameter('cfg_start', params['cfg'])
            runner.set_parameter('cfg_end', params['cfg'])

        if 'blocks_to_swap' in params:
            runner.set_parameter('blocks_to_swap', params['blocks_to_swap'])

        if 'frame_interpolation' in params:
            fi = params['frame_interpolation']
            if fi is not None:
                # True/False → RIFE multiplier (2 = enabled, 1 = disabled)
                multiplier = 2 if fi else 1
                runner.set_parameter('frame_interpolation', multiplier)

        if 'lora_name' in params and params['lora_name']:
            runner.set_parameter('lora_name', params['lora_name'])
            if '97' in runner.workflow:
                runner.workflow['97']['inputs']['lora'] = params['lora_name']
                self.logger.info(f"  LoRA pass2 (node 97) lora = {params['lora_name']}")

        if 'lora_strength' in params and params['lora_strength'] is not None:
            s = float(params['lora_strength'])
            runner.set_parameter('lora_strength', s)
            if '97' in runner.workflow:
                s2 = round(s / 3, 3)
                runner.workflow['97']['inputs']['strength'] = s2
                self.logger.info(f"  LoRA pass2 (node 97) strength = {s2} (={s}/3)")

    def _set_seed(self, seed=None):
        """Ustawia unikalny seed (zapobiega cache ComfyUI)"""
        import random

        if seed is None or seed == -1:
            timestamp_part = int(time.time() * 1000000) % (2**31)
            random_part = random.randint(0, 2**20)
            seed = (timestamp_part + random_part) % (2**63)
            self.logger.info(f"  Wygenerowano seed: {seed}")
        else:
            timestamp_variation = int(time.time() * 1000) % 100000
            seed = (seed + timestamp_variation) % (2**63)
            self.logger.info(f"  Seed z wariancją: {seed}")

        self.workflow_runner.set_parameter('seed', seed)

    def _clean_output_folder(self):
        """Czyści pliki mp4 z folderu output i subfolderu Wan22_I2V/"""
        comfyui_output = Path(self.output_folder)
        cleaned = 0

        for f in comfyui_output.glob("*.mp4"):
            try:
                f.unlink()
                cleaned += 1
            except Exception as e:
                self.logger.warning(f"    Nie można usunąć {f.name}: {e}")

        # Subfolder Wan22_I2V/ (VHS_VideoCombine zapisuje tam wg filename_prefix)
        wan_subfolder = comfyui_output / "Wan22_I2V"
        if wan_subfolder.exists():
            for f in wan_subfolder.glob("*.mp4"):
                try:
                    f.unlink()
                    cleaned += 1
                except Exception as e:
                    self.logger.warning(f"    Nie można usunąć {f.name}: {e}")

        if cleaned > 0:
            self.logger.info(f"    Wyczyszczono {cleaned} starych plików")

    def _find_output_video(self, start_time):
        """Szuka nowo wygenerowanego pliku wideo"""
        comfyui_output = Path(self.output_folder)

        search_dirs = [comfyui_output]

        wan_subfolder = comfyui_output / "Wan22_I2V"
        if wan_subfolder.exists():
            search_dirs.append(wan_subfolder)

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
        steps = params.get('steps', 6)
        estimated_time_min = round((steps * 6 * 1.5) / 60, 1)
        return {
            'credits': 0,
            'cost_usd': 0.0,
            'estimated_time_min': estimated_time_min
        }
