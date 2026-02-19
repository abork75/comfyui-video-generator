# -*- coding: utf-8 -*-
"""
Base Backend Interface
All backends must implement this interface
"""

from abc import ABC, abstractmethod
from pathlib import Path

def calculate_optimal_frames(duration, fps):
    """
    Calculate optimal frame count for WAN (must be n*4 + 1)
    
    WAN requires frame count to be: n*4 + 1 (where n >= 1)
    Valid counts: 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65...
    
    Args:
        duration: Duration in seconds
        fps: Frames per second
    
    Returns:
        int: Nearest valid frame count
    
    Examples:
        >>> calculate_optimal_frames(4, 16)
        65  # 64 → 65 (16*4 + 1)
        >>> calculate_optimal_frames(2, 8)
        17  # 16 → 17 (4*4 + 1)
    """
    target_frames = int(duration * fps)
    
    # Check if already valid (n*4 + 1)
    remainder = target_frames % 4
    
    if remainder == 1:
        # Already valid
        return target_frames
    
    # Find nearest n*4 + 1
    if remainder == 0:
        # target = n*4, so n*4 + 1 is just +1
        return target_frames + 1
    elif remainder == 2:
        # Options: -1 or +3
        # -1 is closer
        return target_frames - 1
    else:  # remainder == 3
        # Options: -2 or +2
        # Equal distance, prefer +2 (more frames = smoother)
        return target_frames + 2

class BaseBackend(ABC):
    """Abstract base class for execution backends"""
    
    def __init__(self, config):
        """
        Initialize backend with config
        
        Args:
            config: Full config dict from RUN file
        """
        self.config = config
    
    @abstractmethod
    def validate_requirements(self):
        """
        Validate backend-specific requirements
        
        Returns:
            bool: True if all requirements met
        
        Raises:
            Exception: If requirements not met
        """
        pass
    
    @abstractmethod
    def prepare_inputs(self, pair, workflow):
        """
        Prepare inputs for this backend
        
        Args:
            pair: Frame pair dict with end_frame, start_frame, etc.
            workflow: Workflow instance
            
        Returns:
            dict: Backend-specific prepared inputs
        """
        pass
    
    @abstractmethod
    def execute(self, inputs, params, workflow):
        """
        Execute generation
        
        Args:
            inputs: Prepared inputs from prepare_inputs()
            params: Workflow parameters
            workflow: Workflow instance
            
        Returns:
            Path: Path to generated output file, or None if failed
        """
        pass
    
    @abstractmethod
    def cleanup(self, inputs):
        """
        Cleanup temporary resources
        
        Args:
            inputs: Inputs dict from prepare_inputs()
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, params):
        """
        Estimate cost for this generation
        
        Args:
            params: Generation parameters
            
        Returns:
            dict: Cost estimation (credits, usd, time_min)
        """
        pass
    
    def get_name(self):
        """Get backend name"""
        return self.__class__.__name__.replace('Backend', '').lower()
        
    def generate_transition(self, start_frame, end_frame, output_path, 
                      duration, fps, steps, cfg, seed,
                      positive_prompt, negative_prompt,
                      width, height):
        """
        High-level wrapper for transition generation
        
        This method wraps the lower-level interface for compatibility
        with batch_transitions.py orchestrator:
            prepare_inputs() → execute() → cleanup()
        
        Args:
            start_frame: Path to start frame image
            end_frame: Path to end frame image (or None for I2V mode)
            output_path: Path to save output video
            duration: Duration in seconds
            fps: Frames per second
            steps: Number of diffusion steps
            cfg: CFG scale
            seed: Random seed (or None)
            positive_prompt: Positive prompt
            negative_prompt: Negative prompt
            width: Video width
            height: Video height
        
        Returns:
            bool: True if successful, False otherwise
        """
        
        from pathlib import Path
        
        try:
            # ============================================================
            # DETECT MODE: I2V (chain) vs V2V (normal)
            # ============================================================
            
            is_i2v_mode = end_frame is None
            
            # Build pair dict (matches old interface)
            pair = {
                'start_frame': Path(start_frame),
                'end_frame': Path(end_frame) if end_frame is not None else None,  # ✅ Allow None
            }
            
            # Build params dict (matches old interface)
            params = {
                'output_path': Path(output_path),
                'duration': duration,
                'fps': fps,
                'steps': steps,
                'cfg': cfg,
                'seed': seed,
                'pos_prompt': positive_prompt,
                'neg_prompt': negative_prompt,
                'width': width,
                'height': height,
                'length': calculate_optimal_frames(duration, fps),  # Total frames
                'is_i2v_mode': is_i2v_mode,  # ✅ Flag for subclasses
            }
            
            # Use existing interface (implemented by subclasses)
            inputs = self.prepare_inputs(pair, workflow=None)
            result = self.execute(inputs, params, workflow=None)
            
            # Cleanup
            self.cleanup(inputs)
            
            # Return success
            return result is not None and Path(output_path).exists()
            
        except Exception as e:
            print(f"Error in {self.get_name()} generate_transition: {e}")
            import traceback
            traceback.print_exc()
            return False