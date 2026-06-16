# -*- coding: utf-8 -*-
"""
Transition Workflow - Image/Video to Video transitions
"""

from pathlib import Path
from .base_workflow import BaseWorkflow

def adjust_frame_count_for_wan(frame_count):
    """WAN rule: length % 4 == 1"""
    remainder = frame_count % 4
    if remainder == 1:
        return frame_count
    elif remainder == 0:
        return frame_count + 1
    elif remainder == 2:
        return frame_count - 1
    else:
        return frame_count + 2

class TransitionWorkflow(BaseWorkflow):
    """Standard transition workflow (i2v, v2v)"""
    
    def validate_item(self, item, config):
        """Validate transition-specific requirements"""
        # Duration required and must be > 0
        if 'duration' not in item and 'default_duration' not in config:
            raise ValueError("Transition requires 'duration' parameter")
        duration = item.get('duration', config.get('default_duration', 4))
        if float(duration) <= 0:
            raise ValueError(f"Duration must be > 0 (got {duration}). Minimum ~0.3s generates 5 frames required by WAN+RIFE.")

        # File required (unless chain)
        if 'file' not in item and not item.get('chain', False):
            raise ValueError("Transition requires 'file' parameter")
    
    def prepare_params(self, item, pair, config, target_resolution):
        """Prepare transition parameters"""
        
        # Basic params
        duration = item.get('duration', config.get('default_duration', 4))
        fps = item.get('fps', config.get('default_fps', 16))
        steps = item.get('steps', config.get('default_steps', 20))
        cfg = item.get('cfg', config.get('default_cfg', 4.0))
        seed = item.get('seed', config.get('default_seed', None))
        
        # Prompts
        pos_prompt = item.get('pos_prompt', config.get('default_positive_prompt', ''))
        neg_prompt = item.get('neg_prompt', config.get('default_negative_prompt', ''))
        
        # Calculate frame count (WAN rule; minimum 5 so RIFE gets ≥ 2 frames)
        base_length = fps * duration
        final_length = max(adjust_frame_count_for_wan(base_length), 5)
        
        # Output path
        transitions_folder = Path(config['project_folder']) / "transitions"
        transitions_folder.mkdir(exist_ok=True)
        
        output_name = f"{pair['from_name']}_{pair['to_name']}_transition.mp4"
        output_path = transitions_folder / output_name
        
        return {
            'width': target_resolution[0],
            'height': target_resolution[1],
            'length': final_length,
            'fps': fps,
            'duration': duration,
            'steps': steps,
            'cfg': cfg,
            'seed': seed,
            'pos_prompt': pos_prompt,
            'neg_prompt': neg_prompt,
            'output_path': output_path,
        }
    
    def get_template_path(self, config):
        """Get transition workflow template"""
        template_path = config.get('workflow_template_path', '')
        
        if not template_path:
            # Fallback to default
            base_path = Path(__file__).parent.parent
            template_path = base_path / "workflows" / "workflow-api-fv9kYUtmjLzC5I8tRR49y.json"
        
        return Path(template_path)