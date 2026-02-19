# -*- coding: utf-8 -*-
"""
Cloud Backend - Comfy.icu API execution
Extracted from batch_transitions_cloud.py
"""

import os
import time
import requests
from pathlib import Path
from .base_backend import BaseBackend
from helpers.imgbb_upload import upload_to_imgbb, delete_from_imgbb
from helpers.cost_calculator import estimate_comfy_icu_cost
from workflow_base import Logger

class CloudBackend(BaseBackend):
    """Comfy.icu API backend"""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = Logger()
        
        # Get credentials
        self.api_key = os.getenv('COMFY_ICU_API_KEY', config.get('comfy_icu_api_key', ''))
        self.workflow_id = config.get('comfy_icu_workflow_id', '')
        
        # Tracking for cleanup
        self.uploaded_files = []
    
    def validate_requirements(self):
        """Validate cloud-specific requirements"""
        if not self.api_key:
            raise Exception("COMFY_ICU_API_KEY not set (environment variable)")
        
        if not self.workflow_id:
            raise Exception("comfy_icu_workflow_id not set in config")
        
        imgbb_key = os.getenv('IMGBB_API_KEY')
        if not imgbb_key:
            raise Exception("IMGBB_API_KEY not set (environment variable)")
        
        self.logger.success(f"Cloud backend ready (workflow: {self.workflow_id[:10]}...)")
        return True
    
    def prepare_inputs(self, pair, workflow):
        """Upload frames to ImgBB"""
        self.logger.info(f"  Uploading frames to ImgBB...")
        
        # Upload end frame (becomes start_image in WAN - first frame of transition!)
        end_data = upload_to_imgbb(pair['end_frame'])
        if not end_data:
            raise Exception(f"Failed to upload {pair['end_frame'].name}")
        
        # Upload start frame (becomes end_image in WAN - last frame of transition!)
        start_data = upload_to_imgbb(pair['start_frame'])
        if not start_data:
            raise Exception(f"Failed to upload {pair['start_frame'].name}")
        
        inputs = {
            'end_url': end_data['url'],
            'start_url': start_data['url'],
            'end_delete': end_data['delete_url'],
            'start_delete': start_data['delete_url'],
        }
        
        self.uploaded_files.append(inputs)
        self.logger.success(f"  ✓ Uploaded 2 frames")
        
        return inputs
    
    def execute(self, inputs, params, workflow):
        """Execute on Comfy.icu API"""
        
        # Get template path from config
        template_path = self.config.get('workflow_template_path')
        
        if not template_path:
            self.logger.error("workflow_template_path not set in config")
            return None
        
        template_path = Path(template_path)
        
        if not template_path.exists():
            self.logger.error(f"Workflow template not found: {template_path}")
            return None
        
        
        # Start job
        run_id = self._start_job(
            inputs['start_url'], # ✅ pair['start_frame'] (01_end) = FIRST frame of transition
            inputs['end_url'],   # ✅ pair['end_frame'] (02_start) = LAST frame of transition
            params,
            template_path
        )
        
        if not run_id:
            return None
        
        # Poll for completion
        video_url = self._poll_status(run_id, timeout=3600)
        
        if not video_url:
            return None
        
        # Download result
        output_path = self._download(video_url, params.get('output_path'))
        
        return output_path
    
    def cleanup(self, inputs):
        """Delete uploaded files from ImgBB"""
        if not inputs:
            return
        
        self.logger.info(f"  Cleanup: Deleting from ImgBB...")
        
        deleted = 0
        if delete_from_imgbb(inputs.get('end_delete', '')):
            deleted += 1
        if delete_from_imgbb(inputs.get('start_delete', '')):
            deleted += 1
        
        if deleted == 2:
            self.logger.success(f"  ✓ Cleanup: Deleted 2 files")
        elif deleted > 0:
            self.logger.warning(f"  ⚠️  Cleanup: Deleted {deleted}/2 files")
        else:
            self.logger.warning(f"  ⚠️  Cleanup failed")
    
    def estimate_cost(self, params):
        """Estimate cost for cloud execution"""
        return estimate_comfy_icu_cost(params)
    
    # ============================================================
    # PRIVATE METHODS
    # ============================================================
    
    def _start_job(self, first_frame_url, last_frame_url, params, template_path):
        """Start Comfy.icu job"""
        import json
        import copy
        
        url = f"https://comfy.icu/api/v1/workflows/{self.workflow_id}/runs"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        
        # Load and modify template
        with open(template_path, encoding='utf-8') as f:
            prompt = json.load(f)
        
        prompt = copy.deepcopy(prompt)
        
        # Apply params to template
        prompt["6"]["inputs"]["text"] = params['pos_prompt']
        prompt["7"]["inputs"]["text"] = params['neg_prompt']
        prompt["62"]["inputs"]["image"] = "end.jpg"
        prompt["68"]["inputs"]["image"] = "start.jpg"
        prompt["67"]["inputs"]["width"] = params['width']
        prompt["67"]["inputs"]["height"] = params['height']
        prompt["67"]["inputs"]["length"] = params['length']
        prompt["57"]["inputs"]["steps"] = params['steps']
        prompt["57"]["inputs"]["cfg"] = params['cfg']
        
        # Generate random seed if None
        import random
        seed = params.get('seed')
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        prompt["57"]["inputs"]["noise_seed"] = seed
        
        prompt["58"]["inputs"]["steps"] = params['steps']
        prompt["58"]["inputs"]["cfg"] = params['cfg']
        prompt["71"]["inputs"]["frame_rate"] = params['fps']
        
        # Files mapping
        files = {
            "/input/start.jpg": first_frame_url,
            "/input/end.jpg": last_frame_url,
        }
        
        body = {
            "workflow_id": self.workflow_id,
            "prompt": prompt,
            "files": files
        }
        
        # DEBUG: Save request for inspection
        import json
        from pathlib import Path
        debug_folder = Path("logs")
        debug_folder.mkdir(exist_ok=True)
        debug_file = debug_folder / f"cloud_request_{int(time.time())}.json"
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(body, f, indent=2, ensure_ascii=False)
        self.logger.info(f"  DEBUG: Request saved to {debug_file}")
        
  
        try:
            self.logger.info(f"  Starting Comfy.icu job...")
            response = requests.post(url, headers=headers, json=body, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            run_id = data.get('id') or data.get('run_id')
            
            self.logger.success(f"  Job started: {run_id}")
            return run_id
            
        except Exception as e:
            self.logger.error(f"  API error: {e}")
            if hasattr(e, 'response'):
                self.logger.error(f"  Response: {e.response.text[:200]}")
            return None
    
    def _poll_status(self, run_id, timeout=3600, check_interval=10):
        """Poll job status"""
        url = f"https://comfy.icu/api/v1/workflows/{self.workflow_id}/runs/{run_id}"
        headers = {"authorization": f"Bearer {self.api_key}"}
        
        start_time = time.time()
        last_status = None
        
        self.logger.info(f"  Waiting for completion (timeout: {timeout//60}min)...")
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                status = data.get('status', 'unknown')
                status_lower = status.lower()
                
                if status != last_status:
                    elapsed = time.time() - start_time
                    self.logger.info(f"  [{elapsed:.0f}s] Status: {status}")
                    last_status = status
                
                if status_lower in ['completed', 'succeeded', 'success']:
                    output_list = data.get('output', [])
                    
                    if not output_list:
                        self.logger.error(f"  No output files")
                        return None
                    
                    # Find video
                    for item in output_list:
                        if isinstance(item, dict) and 'url' in item:
                            url_str = item['url']
                            if url_str.endswith('.mp4') or url_str.endswith('.webm'):
                                elapsed = time.time() - start_time
                                self.logger.success(f"  Completed in {elapsed/60:.1f}min")
                                return url_str
                    
                    self.logger.error(f"  No video found in output")
                    return None
                    
                elif status_lower in ['failed', 'error']:
                    error_msg = data.get('error', 'Unknown error')
                    self.logger.error(f"  Job failed: {error_msg}")
                    return None
                
                time.sleep(check_interval)
                
            except Exception as e:
                self.logger.warning(f"  Poll error: {e}")
                time.sleep(check_interval)
        
        self.logger.error(f"  Timeout after {timeout//60}min")
        return None
    
    def _download(self, video_url, output_path):
        """Download result video"""
        self.logger.info(f"  Downloading: {output_path.name}")
        
        try:
            response = requests.get(video_url, stream=True, timeout=300)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.success(f"  Downloaded: {output_path.name}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"  Download exception: {e}")
            return None