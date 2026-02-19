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
        
        # Initialize workflow runner
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
            # ========================================
            
            self.workflow_runner = WorkflowRunner(
                self.config_path,
                self.workflows_path
            )            
            
            # ========================================
            # SETUP workflow (przed run!)
            # ========================================
            
            # 1. Upload and set images
            self.logger.info(f"  Setting up images...")
            
            # End frame → start_image in WAN (FIRST frame of transition)
            if not self.workflow_runner.set_image(
                str(inputs['end_frame']), 
                'start_image'
            ):
                self.logger.error(f"  Failed to set start_image")
                return None
            
            # Start frame → end_image in WAN (LAST frame of transition)
            if not self.workflow_runner.set_image(
                str(inputs['start_frame']),
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
            
            # 5. Clean output folder BEFORE run (prevent cache issues)
            self.logger.info(f"  Cleaning output folder...")
            output_folder = Path(self.output_folder)
            cleaned_count = 0
            for old_file in output_folder.glob("*.mp4"):
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
            start_time = time.time()
            
            result = self.workflow_runner.run(wait_for_completion=True)
            
            elapsed = time.time() - start_time
            
            if not result:
                self.logger.error(f"  Workflow execution failed")
                return None
            
            self.logger.success(f"  Workflow completed in {elapsed:.1f}s!")
            
            # ========================================
            # DEBUG: Check what we got
            # ========================================
            
            self.logger.info(f"  DEBUG: Result type: {type(result)}")
            self.logger.info(f"  DEBUG: Result keys: {result.keys() if isinstance(result, dict) else 'N/A'}")
            
            # ========================================
            # Find output video
            # ========================================
            
            self.logger.info(f"  Finding output video...")
            
            # STRATEGY 1: Extract from outputs (preferred)
            video_filename = None
            outputs = result.get('outputs', {})
            
            if outputs:
                self.logger.info(f"  DEBUG: Found outputs with {len(outputs)} nodes")
                
                for node_id, node_output in outputs.items():
                    self.logger.info(f"  DEBUG: Node {node_id} output: {node_output.keys() if isinstance(node_output, dict) else type(node_output)}")
                    
                    if isinstance(node_output, dict) and 'videos' in node_output:
                        videos_list = node_output['videos']
                        self.logger.info(f"  DEBUG: Node {node_id} has {len(videos_list)} videos")
                        
                        if videos_list and len(videos_list) > 0:
                            video_filename = videos_list[0].get('filename')
                            if video_filename:
                                self.logger.info(f"    Output from node {node_id}: {video_filename}")
                                break
            else:
                self.logger.warning(f"  DEBUG: No outputs in result!")
            
            # STRATEGY 2: Fallback - search for NEW files ONLY
            if not video_filename:
                self.logger.warning(f"  No filename in outputs, searching by timestamp...")
                
                # Find files created AFTER workflow start
                recent_files = []
                for f in output_folder.glob("*.mp4"):
                    file_age = time.time() - f.stat().st_mtime
                    
                    # File must be created during this run (elapsed time + 10s buffer)
                    if file_age < elapsed + 10:
                        recent_files.append((f, file_age))
                        self.logger.info(f"    Found recent: {f.name} (age: {file_age:.1f}s)")
                
                if not recent_files:
                    self.logger.error(f"  No recent video files found in {output_folder}")
                    self.logger.error(f"  Workflow elapsed: {elapsed:.1f}s, but no files created in that time!")
                    
                    # List ALL files for debug
                    all_files = list(output_folder.glob("*.mp4"))
                    if all_files:
                        self.logger.warning(f"  Files in output folder:")
                        for f in all_files:
                            age = time.time() - f.stat().st_mtime
                            self.logger.warning(f"    • {f.name} (age: {age:.1f}s)")
                    else:
                        self.logger.error(f"  Output folder is EMPTY!")
                    
                    return None
                
                # Sort by age (youngest first)
                recent_files.sort(key=lambda x: x[1])
                source_video = recent_files[0][0]
                self.logger.info(f"  Using newest: {source_video.name}")
            else:
                # Use filename from outputs
                source_video = output_folder / video_filename
            
            # Verify file exists
            if not source_video.exists():
                self.logger.error(f"  Output video not found: {source_video}")
                return None
            
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