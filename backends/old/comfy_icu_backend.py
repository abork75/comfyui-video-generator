"""
Comfy.icu Cloud Backend
Transition generation via comfy.icu API
"""

import os
import time
import requests
import random
from pathlib import Path
from typing import Dict, Optional
import logging

from .base import TransitionBackend

logger = logging.getLogger(__name__)


class ComfyICUBackend(TransitionBackend):
    """
    Comfy.icu cloud backend for transition generation
    
    Uses WAN I2V workflow with start + end frames
    """
    
    # Cost model (from benchmarks)
    CREDITS_PER_TRANSITION_BASE = 4096  # 4s @ 336x448, 16fps, 65 frames
    BASE_DURATION = 4.0
    BASE_RESOLUTION = (336, 448)
    DOLLARS_PER_CREDIT = 0.0001
    
    def __init__(self, api_key: str, workflow_id: str):
        """
        Initialize Comfy.icu backend
        
        Args:
            api_key: Comfy.icu API key (from env COMFY_ICU_API_KEY)
            workflow_id: Workflow ID (from comfy.icu workflow URL)
        """
        super().__init__("comfy_icu")
        
        self.api_key = api_key
        self.workflow_id = workflow_id
        self.base_url = "https://comfy.icu/api/v1"
        
        if not self.api_key:
            raise ValueError("Comfy.icu API key required (COMFY_ICU_API_KEY)")
        
        if not self.workflow_id:
            raise ValueError("Comfy.icu workflow ID required")
        
        logger.info(f"Initialized Comfy.icu backend (workflow: {workflow_id[:8]}...)")
    
    def generate(
        self, 
        start_frame: Path, 
        end_frame: Path, 
        params: Dict
    ) -> Optional[Path]:
        """
        Generate transition via comfy.icu API
        
        Args:
            start_frame: Path to start image
            end_frame: Path to end image
            params: Generation parameters
            
        Returns:
            Path to generated video (temporary file)
        """
        
        if not self.validate_params(params):
            return None
        
        try:
            # 1. Upload images
            logger.info("  📤 Uploading frames to comfy.icu...")
            start_id = self._upload_image(start_frame)
            end_id = self._upload_image(end_frame)
            logger.info(f"    Start: {start_id[:16]}...")
            logger.info(f"    End: {end_id[:16]}...")
            
            # 2. Prepare workflow inputs
            workflow_inputs = self._prepare_inputs(
                start_id, 
                end_id, 
                params
            )
            
            # 3. Run workflow
            logger.info("  🚀 Starting generation on comfy.icu...")
            run_id = self._run_workflow(workflow_inputs)
            logger.info(f"    Run ID: {run_id[:16]}...")
            
            # 4. Wait for completion
            logger.info("  ⏳ Waiting for completion...")
            video_url = self._wait_for_completion(run_id, timeout=600)
            
            # 5. Download result
            logger.info("  💾 Downloading result...")
            local_path = self._download_video(video_url)
            
            logger.info(f"  ✅ Generated: {local_path.name}")
            
            return local_path
            
        except Exception as e:
            logger.error(f"  ❌ Comfy.icu generation failed: {e}")
            return None
    
    def _upload_image(self, image_path: Path) -> str:
        """
        Upload image to comfy.icu storage
        
        Returns:
            Image ID for workflow input
        """
        
        url = f"{self.base_url}/upload"
        
        with open(image_path, 'rb') as f:
            files = {'file': (image_path.name, f, 'image/jpeg')}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
        
        data = response.json()
        
        # Check response format (może być różny)
        if 'id' in data:
            return data['id']
        elif 'file_id' in data:
            return data['file_id']
        elif 'url' in data:
            return data['url']
        else:
            raise ValueError(f"Unexpected upload response: {data}")
    
    def _prepare_inputs(self, start_id: str, end_id: str, params: Dict) -> Dict:
        """
        Prepare workflow inputs from params
        """
        
        # Calculate frame count (WAN rule: length % 4 == 1)
        from helpers import adjust_frame_count_for_wan
        length = adjust_frame_count_for_wan(params['fps'] * params['duration'])
        
        # Map params to workflow inputs
        # (Based on workflow structure from screenshot)
        inputs = {
            # Images
            "start_image": start_id,
            "end_image": end_id,
            
            # Prompts
            "positive": params['pos_prompt'],
            "negative": params['neg_prompt'],
            
            # Video settings
            "width": params['width'],
            "height": params['height'],
            "length": length,
            
            # Sampling
            "steps": params.get('steps', 20),
            "cfg": params.get('cfg', 4.0),
            "seed": params.get('seed') or random.randint(0, 2**32 - 1),
            
            # Model settings (if needed)
            "sampler_name": params.get('sampler', 'euler'),
            "scheduler": params.get('scheduler', 'simple'),
        }
        
        return inputs
    
    def _run_workflow(self, inputs: Dict) -> str:
        """
        Execute workflow on comfy.icu
        
        Returns:
            Run ID for status polling
        """
        
        url = f"{self.base_url}/workflows/{self.workflow_id}/runs"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'inputs': inputs
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract run ID
        if 'id' in data:
            return data['id']
        elif 'run_id' in data:
            return data['run_id']
        else:
            raise ValueError(f"Unexpected run response: {data}")
    
    def _wait_for_completion(self, run_id: str, timeout: int = 600) -> str:
        """
        Poll run status until completion
        
        Args:
            run_id: Run ID to poll
            timeout: Max wait time in seconds
            
        Returns:
            Video URL for download
        """
        
        url = f"{self.base_url}/workflows/{self.workflow_id}/runs/{run_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        start_time = time.time()
        last_status = None
        
        while True:
            # Check timeout
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Run {run_id} timed out after {timeout}s")
            
            # Poll status
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            status = data.get('status', 'unknown')
            
            # Log status changes
            if status != last_status:
                logger.info(f"    Status: {status}")
                last_status = status
            
            # Check completion
            if status == 'completed' or status == 'succeeded':
                # Extract video URL
                outputs = data.get('outputs', [])
                
                if not outputs:
                    raise ValueError("No outputs in completed run")
                
                # Find video output
                for output in outputs:
                    if 'url' in output:
                        return output['url']
                    elif 'file_url' in output:
                        return output['file_url']
                
                raise ValueError(f"No video URL in outputs: {outputs}")
            
            elif status == 'failed' or status == 'error':
                error_msg = data.get('error', 'Unknown error')
                raise Exception(f"Run failed: {error_msg}")
            
            # Wait before next poll
            time.sleep(5)
    
    def _download_video(self, url: str) -> Path:
        """
        Download video from comfy.icu to local temp file
        
        Args:
            url: Video URL
            
        Returns:
            Path to downloaded video
        """
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create temp file
        temp_path = Path(f"temp_comfyicu_{int(time.time())}_{random.randint(1000,9999)}.mp4")
        
        # Download with progress
        total_size = int(response.headers.get('content-length', 0))
        
        with open(temp_path, 'wb') as f:
            if total_size == 0:
                # Unknown size
                f.write(response.content)
            else:
                # Known size - could add progress bar
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
        
        return temp_path
    
    def estimate_cost(self, params: Dict) -> Dict:
        """
        Estimate credits and cost for generation
        
        Args:
            params: Generation parameters
            
        Returns:
            Dict with cost info
        """
        
        # Base cost
        base_credits = self.CREDITS_PER_TRANSITION_BASE
        
        # Scale by duration
        duration_factor = params['duration'] / self.BASE_DURATION
        
        # Scale by resolution (area)
        base_pixels = self.BASE_RESOLUTION[0] * self.BASE_RESOLUTION[1]
        actual_pixels = params['width'] * params['height']
        resolution_factor = actual_pixels / base_pixels
        
        # Calculate
        estimated_credits = int(base_credits * duration_factor * resolution_factor)
        estimated_cost = estimated_credits * self.DOLLARS_PER_CREDIT
        
        return {
            'credits': estimated_credits,
            'cost_usd': round(estimated_cost, 2),
            'backend': self.name
        }
    
    def estimate_time(self, params: Dict) -> int:
        """
        Estimate generation time (seconds)
        
        Args:
            params: Generation parameters
            
        Returns:
            Estimated time in seconds
        """
        
        # Base: ~63s for 4s video (from benchmark)
        base_time = 63
        duration_factor = params['duration'] / self.BASE_DURATION
        
        # Cloud might scale better than linear (parallel processing)
        # Conservative estimate: linear
        estimated_time = int(base_time * duration_factor)
        
        return estimated_time
    
    def get_info(self) -> Dict:
        """Get backend info"""
        info = super().get_info()
        info.update({
            'workflow_id': self.workflow_id,
            'api_url': self.base_url,
            'cost_model': {
                'base_credits': self.CREDITS_PER_TRANSITION_BASE,
                'base_duration': self.BASE_DURATION,
                'base_resolution': self.BASE_RESOLUTION,
                'dollars_per_credit': self.DOLLARS_PER_CREDIT
            }
        })
        return info
