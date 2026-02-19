# -*- coding: utf-8 -*-
"""
Local Backend - Local ComfyUI execution
Extracted from batch_transitions_adv.py
"""

from pathlib import Path
from .base_backend import BaseBackend
from workflow_base import WorkflowRunner, Logger

class LocalBackend(BaseBackend):
    """Local ComfyUI backend"""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = Logger()
        
        # Get local paths
        self.config_path = config.get('config_path', '')
        self.workflows_path = config.get('workflows_path', '')
        self.output_folder = config.get('comfyui_output_folder', '')
        
        self.workflow_runner = None
    
    def validate_requirements(self):
        """Validate local-specific requirements"""
        if not self.config_path or not Path(self.config_path).exists():
            raise Exception(f"Local config not found: {self.config_path}")
        
        if not self.workflows_path or not Path(self.workflows_path).exists():
            raise Exception(f"Workflows path not found: {self.workflows_path}")
        
        if not self.output_folder or not Path(self.output_folder).exists():
            raise Exception(f"ComfyUI output folder not found: {self.output_folder}")
        
        # Initialize workflow runner (for validation only)
        self.workflow_runner = WorkflowRunner(
            self.config_path,
            self.workflows_path
        )
        
        self.logger.success(f"Local backend ready (ComfyUI)")
        return True
    
    def prepare_inputs(self, pair, workflow):
        """No preparation needed for local (uses file paths directly)"""
        return {
            'end_frame': pair['end_frame'],
            'start_frame': pair['start_frame'],
        }
    
    def execute(self, inputs, params, workflow):
        """Execute on local ComfyUI"""
        
        try:
            self.logger.info(f"  Starting local ComfyUI workflow...")
            
            # ========================================
            # ⚠️ CRITICAL: Reload workflow runner (reset to clean state)
            # Without this, second run uses MODIFIED workflow from first run!
            # This matches batch_transitions_adv.py logic (new runner per run)
            # ========================================
            
            self.workflow_runner = WorkflowRunner(
                self.config_path,
                self.workflows_path
            )
            
            # ========================================
            # SETUP workflow
            # ========================================
            
            # 1. Upload and set images
            self.logger.info(f"  Setting up images...")
            
            # Start frame (end z poprzedniego pliku) → start_image in WAN (FIRST frame of transition)
            if not self.workflow_runner.set_image(
                str(inputs['start_frame']),   # ✅ POPRAWNE!
                'start_image'
            ):
                self.logger.error(f"  Failed to set start_image")
                return None
            
            # End frame (start z następnego pliku) → end_image in WAN (LAST frame of transition)
            if not self.workflow_runner.set_image(
                str(inputs['end_frame']),     # ✅ POPRAWNE!
                'end_image'
            ):
                self.logger.error(f"  Failed to set end_image")
                return None
            
            # 2. Set prompts
            self.logger.info(f"  Setting prompts...")
            self.workflow_runner.set_prompt(params['pos_prompt'], 'positive_prompt')
            self.workflow_runner.set_prompt(params['neg_prompt'], 'negative_prompt')
            
            # 3. Set video parameters
            self.logger.info(f"  Setting video params...")
            self.workflow_runner.set_video_params(
                width=params['width'],
                height=params['height'],
                fps=params['fps'],
                length=params['length']
            )
            
            # 4. Set sampling parameters
            self.logger.info(f"  Setting sampling params...")
            self.workflow_runner.set_sampling_params(
                steps=params['steps'],
                cfg=params['cfg'],
                seed=params.get('seed')
            )
            
            # 5. Clean output folder (prevent finding old files)
            self.logger.info(f"  Cleaning output folder...")
            comfyui_output = Path(self.output_folder)
            
            cleaned_count = 0
            for old_file in comfyui_output.glob("*.mp4"):
                try:
                    old_file.unlink()
                    cleaned_count += 1
                except Exception as e:
                    self.logger.warning(f"    Could not delete {old_file.name}: {e}")
            
            # Also clean 'video' subfolder (VHS_VideoCombine quirk)
            video_subfolder = comfyui_output / "video"
            if video_subfolder.exists():
                for old_file in video_subfolder.glob("*.mp4"):
                    try:
                        old_file.unlink()
                        cleaned_count += 1
                    except Exception as e:
                        self.logger.warning(f"    Could not delete {old_file.name}: {e}")
            
            if cleaned_count > 0:
                self.logger.info(f"    Cleaned {cleaned_count} old files")
            
            # 6. Run workflow
            self.logger.info(f"  Executing workflow...")
            import time
            start_time = time.time()  # Timestamp BEFORE run
            
            result = self.workflow_runner.run(wait_for_completion=True)
            
            elapsed = time.time() - start_time
            
            if not result:
                self.logger.error(f"  Workflow execution failed")
                return None
            
            self.logger.success(f"  Workflow completed in {elapsed:.1f}s!")
            
            # ========================================
            # Find output video (batch_transitions_adv logic)
            # ========================================
            
            self.logger.info(f"  Finding output video...")
            
            # Search for video files (all extensions)
            video_files = []
            for ext in ['.mp4', '.avi', '.mov', '.mkv']:
                video_files.extend(comfyui_output.glob(f'*{ext}'))
            
            # Also check 'video' subfolder (VHS_VideoCombine quirk)
            if video_subfolder.exists():
                for ext in ['.mp4', '.avi', '.mov', '.mkv']:
                    video_files.extend(video_subfolder.glob(f'*{ext}'))
            
            if not video_files:
                self.logger.error(f"  No video files found in {comfyui_output}")
                if video_subfolder.exists():
                    self.logger.error(f"  Also checked: {video_subfolder}")
                return None
            
            # Filter: only files created AFTER workflow start
            recent_files = [f for f in video_files if f.stat().st_mtime > start_time]
            
            if not recent_files:
                self.logger.error(f"  No recent video files found")
                self.logger.error(f"  Workflow started at timestamp: {start_time}")
                
                # DEBUG: show all files with timestamps
                self.logger.warning(f"  All files in output folder:")
                for f in video_files:
                    created_at = f.stat().st_mtime
                    is_after = "✓" if created_at > start_time else "✗"
                    age = time.time() - created_at
                    self.logger.warning(f"    {is_after} {f.name} (age: {age:.1f}s, created: {created_at}, needed: >{start_time})")
                
                return None
            
            # Take newest file
            source_video = max(recent_files, key=lambda f: f.stat().st_mtime)
            
            self.logger.info(f"  Found: {source_video.name}")
            
            # ========================================
            # Move to final location
            # ========================================
            
            target_path = params.get('output_path')
            
            if target_path.exists():
                self.logger.warning(f"  Overwriting existing: {target_path.name}")
                target_path.unlink()
            
            import shutil
            shutil.move(str(source_video), str(target_path))
            
            self.logger.success(f"  Moved: {target_path.name}")
            return target_path
            
        except Exception as e:
            self.logger.error(f"  Local execution error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def cleanup(self, inputs):
        """No cleanup needed for local"""
        pass
    
    def estimate_cost(self, params):
        """Local is free (but estimate time)"""
        frames = params.get('fps', 16) * params.get('duration', 4)
        
        # Base estimate: 64 frames ≈ 4 minutes on local GPU
        base_frames = 64
        base_time_min = 4.0
        
        # Scale linearly by frame count
        estimated_time_min = base_time_min * (frames / base_frames)
        
        return {
            'credits': 0,
            'cost_usd': 0.0,
            'estimated_time_min': round(estimated_time_min, 1)
        }