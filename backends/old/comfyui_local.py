"""
Local ComfyUI Backend
Transition generation via local ComfyUI instance
"""

import os
import random
from pathlib import Path
from typing import Dict, Optional
import logging

from .base import TransitionBackend

logger = logging.getLogger(__name__)


class ComfyUILocalBackend(TransitionBackend):
    """
    Local ComfyUI backend for transition generation
    
    Uses local ComfyUI instance (free, slower)
    """
    
    def __init__(
        self, 
        api_url: str,
        config_path: str,
        workflows_path: str,
        output_folder: str
    ):
        """
        Initialize local ComfyUI backend
        
        Args:
            api_url: Local ComfyUI API URL (e.g. http://127.0.0.1:8100)
            config_path: Path to workflows config JSON
            workflows_path: Base path to workflow JSON files
            output_folder: ComfyUI output folder
        """
        super().__init__("comfyui_local")
        
        self.api_url = api_url
        self.config_path = config_path
        self.workflows_path = workflows_path
        self.output_folder = output_folder
        
        logger.info(f"Initialized local ComfyUI backend ({api_url})")
    
    def generate(
        self, 
        start_frame: Path, 
        end_frame: Path, 
        params: Dict
    ) -> Optional[Path]:
        """
        Generate transition via local ComfyUI
        
        Args:
            start_frame: Path to start image
            end_frame: Path to end image
            params: Generation parameters
            
        Returns:
            Path to generated video
        """
        
        if not self.validate_params(params):
            return None
        
        try:
            # Import WorkflowRunner (existing code)
            from workflow_runner import WorkflowRunner
            from helpers import adjust_frame_count_for_wan, find_latest_video
            
            # Initialize runner
            runner = WorkflowRunner(
                config_path=self.config_path,
                workflows_base_path=self.workflows_path,
                api_url=self.api_url
            )
            
            # Set images
            runner.set_image(str(start_frame), "start_image")
            runner.set_image(str(end_frame), "end_image")
            
            # Set prompts
            runner.set_text(params['pos_prompt'], "positive")
            runner.set_text(params['neg_prompt'], "negative")
            
            # Set video settings
            runner.set_value(params['width'], "width")
            runner.set_value(params['height'], "height")
            
            # Calculate length (WAN rule)
            length = adjust_frame_count_for_wan(params['fps'] * params['duration'])
            runner.set_value(length, "length")
            
            # Sampling params
            runner.set_value(params.get('steps', 20), "steps")
            runner.set_value(params.get('cfg', 4.0), "cfg")
            
            seed = params.get('seed')
            if seed is None:
                seed = random.randint(0, 2**32 - 1)
            runner.set_value(seed, "seed")
            
            # Run workflow
            logger.info("  🚀 Starting generation on local ComfyUI...")
            result = runner.run(wait_for_completion=True)
            
            if not result['success']:
                logger.error(f"  ❌ Generation failed: {result.get('error', 'Unknown')}")
                return None
            
            # Find generated video
            video_path = find_latest_video(
                self.output_folder,
                min_age_seconds=0
            )
            
            if not video_path:
                logger.error("  ❌ Generated video not found in output folder")
                return None
            
            logger.info(f"  ✅ Generated: {video_path.name}")
            
            return Path(video_path)
            
        except Exception as e:
            logger.error(f"  ❌ Local generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def estimate_cost(self, params: Dict) -> Dict:
        """
        Estimate cost (always free for local)
        
        Returns:
            Cost dict (always $0)
        """
        return {
            'credits': 0,
            'cost_usd': 0.0,
            'backend': self.name
        }
    
    def estimate_time(self, params: Dict) -> int:
        """
        Estimate generation time (seconds)
        
        Based on RTX 5070 Ti benchmarks
        
        Returns:
            Estimated time in seconds
        """
        
        # Benchmark: ~10 min (600s) for 4s @ 336x448
        base_time = 600  # seconds
        base_duration = 4.0
        base_pixels = 336 * 448
        
        # Scale by duration
        duration_factor = params['duration'] / base_duration
        
        # Scale by resolution (somewhat non-linear due to VRAM)
        actual_pixels = params['width'] * params['height']
        resolution_factor = (actual_pixels / base_pixels) ** 1.2  # Slight non-linear
        
        estimated_time = int(base_time * duration_factor * resolution_factor)
        
        return estimated_time
    
    def get_info(self) -> Dict:
        """Get backend info"""
        info = super().get_info()
        info.update({
            'api_url': self.api_url,
            'output_folder': self.output_folder,
            'cost': 'free'
        })
        return info
