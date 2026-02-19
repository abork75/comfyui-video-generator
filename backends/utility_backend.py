# -*- coding: utf-8 -*-
"""
Utility Backend - Video processing utilities
Handles upscaling, color grading, etc. (non-transition workflows)

Architecture:
- Separate from transition generation
- Reusable for various video utilities
- Local ComfyUI only (no cloud support needed)
- Uses WorkflowRunner pattern (same as LocalBackend)
"""

import os
import json
import time
import yaml
import copy
import shutil
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List

from workflow_base import Logger


class UtilityBackend:
    """
    Utility backend for video processing tasks
    
    Supported workflows:
    - gan_upscaler: Upscale videos using RealESRGAN
    
    Future workflows:
    - color_grader: Color grading/LUT application
    - audio_processor: Audio normalization/enhancement
    - frame_interpolation: Increase FPS
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize utility backend
        
        Args:
            config: Configuration dict with:
                - workflows_path: Path to workflows folder
                - workflow_configs_path: Path to YAML configs
                - comfyui_output_folder: ComfyUI output folder
                - comfyui_server: ComfyUI API URL
                - utility_workflow: Which utility to use (e.g., 'gan_upscaler')
        """
        self.logger = Logger()
        
        self.workflows_path = Path(config.get('workflows_path', 'workflows'))
        self.configs_path = Path(config.get('workflow_configs_path', 'workflow_configs'))
        self.output_folder = Path(config.get('comfyui_output_folder', 'D:/ComfyUI/output'))
        self.utility_type = config.get('utility_workflow', 'gan_upscaler')
        self.comfyui_server = config.get('comfyui_server', 'http://127.0.0.1:8188')
        
        # Load workflow config
        self.workflow_config = self._load_workflow_config()
        
        # Load workflow JSON template
        self.workflow_template = self._load_workflow_template()
    
    def _load_workflow_config(self) -> Dict[str, Any]:
        """Load YAML workflow config"""
        config_path = self.configs_path / f"{self.utility_type}_config.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Workflow config not found: {config_path}\n"
                f"Expected location: {config_path.absolute()}"
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _load_workflow_template(self) -> Dict[str, Any]:
        """Load workflow JSON template"""
        workflow_file = self.workflows_path / f"utility-{self.utility_type}.json"
        
        if not workflow_file.exists():
            raise FileNotFoundError(
                f"Workflow template not found: {workflow_file}\n"
                f"Expected location: {workflow_file.absolute()}"
            )
        
        with open(workflow_file, 'r', encoding='utf-8') as f:
            template = json.load(f)
        
        return template
    
    def upscale_video(
        self,
        input_video: Path,
        output_path: Path,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        interpolation: Optional[str] = None,
        method: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> bool:
        """
        Upscale video using RealESRGAN
        
        Args:
            input_video: Path to input video
            output_path: Path to save upscaled video
            target_width: Target width after resize (None = use config default)
            target_height: Target height after resize (None = use config default)
            interpolation: Resize interpolation method (None = use config)
            method: Resize method - stretch/crop/fit (None = use config)
            model_name: Upscale model name (None = use config)
        
        Returns:
            True if successful, False otherwise
        """
        
        # ========================================
        # VALIDATION
        # ========================================
        
        if not input_video.exists():
            self.logger.error(f"Input video not found: {input_video}")
            return False
        
        if input_video.suffix.lower() not in self.workflow_config['input']['supported_formats']:
            self.logger.error(f"Unsupported format: {input_video.suffix}")
            self.logger.error(f"Supported: {self.workflow_config['input']['supported_formats']}")
            return False
        
        # Warn for large files
        if self.workflow_config['validation'].get('warn_large_files', True):
            threshold_mb = self.workflow_config['validation'].get('large_file_threshold_mb', 1000)
            size_mb = input_video.stat().st_size / (1024 * 1024)
            
            if size_mb > threshold_mb:
                self.logger.warning(f"Large file detected: {size_mb:.1f} MB")
                self.logger.warning(f"Processing may take significant time/memory")
        
        # ========================================
        # APPLY DEFAULTS
        # ========================================
        
        defaults = self.workflow_config['defaults']
        processing = self.workflow_config['processing']
        
        if target_width is None:
            target_width = processing.get('target_width', defaults['width'])
        
        if target_height is None:
            target_height = processing.get('target_height', defaults['height'])
        
        if interpolation is None:
            interpolation = processing.get('interpolation', defaults['interpolation'])
        
        if method is None:
            method = processing.get('method', defaults['method'])
        
        if model_name is None:
            model_name = self.workflow_config['model']['upscale_model']
        
        # ========================================
        # LOG SETTINGS
        # ========================================
        
        self.logger.info("")
        self.logger.info("="*70)
        self.logger.info("  GAN UPSCALER")
        self.logger.info("="*70)
        self.logger.info("")
        self.logger.info(f"Input:  {input_video.name}")
        self.logger.info(f"Size:   {input_video.stat().st_size / (1024*1024):.1f} MB")
        self.logger.info(f"Output: {output_path.name}")
        self.logger.info(f"Target: {target_width}x{target_height}")
        self.logger.info(f"Model:  {model_name}")
        self.logger.info(f"Resize: {method}, {interpolation}")
        self.logger.info("")
        
        # ========================================
        # PREPARE WORKFLOW
        # ========================================
        
        workflow = copy.deepcopy(self.workflow_template)
        
        nodes = self.workflow_config['nodes']
        
        # Update input video
        workflow[nodes['load_video']]['inputs']['file'] = str(input_video)
        
        # Update model
        workflow[nodes['load_upscale_model']]['inputs']['model_name'] = model_name
        
        # Update resize settings
        workflow[nodes['image_resize']]['inputs'].update({
            'width': target_width,
            'height': target_height,
            'interpolation': interpolation,
            'method': method,
            'condition': processing.get('condition', 'always'),
            'multiple_of': processing.get('multiple_of', 0)
        })
        
        # Update output settings
        output_settings = self.workflow_config['output']
        
        # Determine output prefix
        if output_settings.get('use_subfolder', True):
            # output/video/filename
            output_prefix = f"video/{output_path.stem}"
        else:
            # output/filename
            output_prefix = output_path.stem
        
        workflow[nodes['save_video']]['inputs'].update({
            'filename_prefix': output_prefix,
            'format': output_settings.get('format', 'auto'),
            'codec': output_settings.get('codec', 'auto')
        })
        
        # ========================================
        # QUEUE WORKFLOW
        # ========================================
        
        self.logger.info("Queuing workflow to ComfyUI...")
        self.logger.info("")
        
        success = self._queue_and_wait(workflow)
        
        # ========================================
        # RETRIEVE OUTPUT
        # ========================================
        
        if success:
            self.logger.info("")
            self.logger.info("Retrieving output from ComfyUI...")
            
            # Determine search folder
            if output_settings.get('use_subfolder', True):
                search_folder = "video"
            else:
                search_folder = ""
            
            comfyui_output = self._find_latest_output(
                search_folder, 
                output_path.stem
            )
            
            if comfyui_output and comfyui_output.exists():
                # Create output directory
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy to target location
                shutil.copy2(comfyui_output, output_path)
                
                output_size_mb = output_path.stat().st_size / (1024 * 1024)
                
                self.logger.success("")
                self.logger.success("="*70)
                self.logger.success("  UPSCALE COMPLETE!")
                self.logger.success("="*70)
                self.logger.success("")
                self.logger.success(f"Output: {output_path}")
                self.logger.success(f"Size:   {output_size_mb:.1f} MB")
                self.logger.success("")
                
                return True
            else:
                self.logger.error("")
                self.logger.error("Output file not found in ComfyUI output folder!")
                self.logger.error(f"Expected in: {self.output_folder / search_folder}")
                self.logger.error(f"Pattern: {output_path.stem}*.mp4")
                self.logger.error("")
                return False
        else:
            self.logger.error("")
            self.logger.error("Workflow execution failed!")
            self.logger.error("")
            return False
    
    def _queue_and_wait(self, workflow: Dict[str, Any]) -> bool:
        """
        Queue workflow to ComfyUI and wait for completion
        
        Uses WorkflowRunner pattern (same as LocalBackend)
        
        Args:
            workflow: Workflow JSON
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Queue prompt (WorkflowRunner.run() pattern)
            url = f"{self.comfyui_server}/prompt"
            payload = {
                "prompt": workflow,
                "client_id": f"utility_{self.utility_type}_{int(time.time())}"
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code != 200:
                self.logger.error(f"Failed to queue prompt: HTTP {response.status_code}")
                self.logger.error(f"Response: {response.text}")
                return False
            
            result = response.json()
            prompt_id = result.get('prompt_id')
            
            if not prompt_id:
                self.logger.error("No prompt_id in response!")
                return False
            
            self.logger.info(f"Queued: {prompt_id}")
            self.logger.info("")
            self.logger.info("Processing... (this may take several minutes)")
            self.logger.info("")
            
            # Wait for completion
            return self._wait_for_completion(prompt_id)
        
        except Exception as e:
            self.logger.error(f"Error during workflow execution: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _wait_for_completion(self, prompt_id: str) -> bool:
        """
        Wait for ComfyUI to finish processing
        
        Adapted from WorkflowRunner._wait_for_completion()
        
        Args:
            prompt_id: Prompt ID from queue response
        
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.comfyui_server}/history/{prompt_id}"
        
        max_time = self.workflow_config['advanced'].get('max_processing_time_minutes', 60) * 60
        start_time = time.time()
        last_update = start_time
        
        while True:
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    history = response.json()
                    
                    if prompt_id in history:
                        entry = history[prompt_id]
                        
                        # Check if completed
                        if 'outputs' in entry:
                            elapsed = time.time() - start_time
                            self.logger.info(f"✓ Completed in {elapsed:.0f}s")
                            return True
                        
                        # Check for errors
                        status = entry.get('status', {})
                        if status.get('status_str') == 'error':
                            self.logger.error("Workflow execution error!")
                            if 'messages' in status:
                                for msg in status['messages']:
                                    self.logger.error(f"  {msg}")
                            return False
                
                # Progress indicator
                current_time = time.time()
                if current_time - last_update > 10:  # Every 10 seconds
                    elapsed = current_time - start_time
                    self.logger.info(f"  Still processing... ({elapsed:.0f}s)")
                    last_update = current_time
                
                # Check timeout
                if current_time - start_time > max_time:
                    self.logger.error(f"Timeout! ({max_time/60:.0f} min)")
                    return False
                
                # Wait before next check
                time.sleep(2)
            
            except Exception as e:
                self.logger.warning(f"Check failed: {e}")
                time.sleep(2)
    
    def _find_latest_output(self, folder: str, prefix: str) -> Optional[Path]:
        """
        Find latest output file from ComfyUI
        
        Args:
            folder: Subfolder in output (e.g., 'video')
            prefix: Filename prefix
        
        Returns:
            Path to latest file or None
        """
        if folder:
            search_folder = self.output_folder / folder
        else:
            search_folder = self.output_folder
        
        if not search_folder.exists():
            return None
        
        # Find files matching prefix
        pattern = f"{prefix}*.mp4"
        files = list(search_folder.glob(pattern))
        
        if not files:
            return None
        
        # Return newest
        return max(files, key=lambda p: p.stat().st_mtime)


# ============================================================
# Convenience Functions
# ============================================================

def upscale_video_batch(
    input_videos: List[Path],
    output_folder: Path,
    config: Dict[str, Any]
) -> Dict[str, bool]:
    """
    Batch upscale multiple videos
    
    Args:
        input_videos: List of input video paths
        output_folder: Output folder for upscaled videos
        config: Backend configuration
    
    Returns:
        Dict mapping input filename to success status
    """
    logger = Logger()
    
    backend = UtilityBackend(config)
    results = {}
    
    logger.header(f"BATCH UPSCALE - {len(input_videos)} videos")
    
    for i, video_path in enumerate(input_videos, 1):
        video_path = Path(video_path)
        output_path = output_folder / f"{video_path.stem}_upscaled.mp4"
        
        logger.section(f"Video {i}/{len(input_videos)}: {video_path.name}")
        
        success = backend.upscale_video(
            input_video=video_path,
            output_path=output_path,
            target_width=config.get('target_width'),
            target_height=config.get('target_height'),
            interpolation=config.get('interpolation'),
            method=config.get('method')
        )
        
        results[video_path.name] = success
    
    # Summary
    logger.header("BATCH SUMMARY")
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    logger.info(f"Total:      {len(results)}")
    logger.success(f"Successful: {successful}")
    if failed:
        logger.error(f"Failed:     {failed}")
    
    return results
