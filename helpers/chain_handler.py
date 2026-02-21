# -*- coding: utf-8 -*-
"""
Chain Handler - Manages chain step generation and caching

This module handles:
- Chain file detection
- Path management (chains folder, frames cache)
- Frame extraction (first/last frames from chain videos)
- Gap resolution (smart dependency tracking)
"""

from pathlib import Path
import subprocess
from typing import List, Dict, Any, Optional


class ChainHandler:
    """
    Handles chain step generation, caching, and dependency resolution
    """
    
    def __init__(self, project_folder, logger=None):
        self.project_folder = Path(project_folder)
        self.chains_folder = self.project_folder / 'transitions' / 'chains'
        self.frames_folder = self.project_folder / 'frames'  # ✅ INPUT folder (not in transitions/)
        self.logger = logger
        
        # Create folders
        self.chains_folder.mkdir(parents=True, exist_ok=True)
        self.frames_folder.mkdir(parents=True, exist_ok=True)
    
    def is_chain_file(self, file_config):
        """
        Check if file config represents a chain step
        
        Args:
            file_config: File config dict (from FlowFile.config)
        
        Returns:
            True if chain file, False otherwise
        """
        return file_config.get('_is_chain', False)
    
    def get_chain_output_path(self, filename):
        """
        Get output path for chain step video
        
        Args:
            filename: Chain step filename (e.g., 'ewelina_stands_001.mp4')
        
        Returns:
            Path to chain video in chains/ folder
        """
        return self.chains_folder / filename
    
    def get_chain_last_frame_path(self, filename):
        """
        Get path for cached last frame
        
        Args:
            filename: Chain step filename
        
        Returns:
            Path to last frame (for next chain step start)
        """
        stem = Path(filename).stem
        return self.frames_folder / f"{stem}_last.jpg"
    
    def get_chain_first_frame_path(self, filename):
        """
        Get path for cached first frame
        
        Args:
            filename: Chain step filename
        
        Returns:
            Path to first frame (for gap filling end)
        """
        stem = Path(filename).stem
        return self.frames_folder / f"{stem}_first.jpg"
    
    def extract_last_frame(self, video_path, width, height):
        """
        Extract last frame from chain video
        (Uses FrameExtractor - unified implementation)
        
        Args:
            video_path: Path to generated chain video
            width: Target width
            height: Target height
        
        Returns:
            Path to extracted last frame (or None if failed)
        """
        
        if not video_path.exists():
            if self.logger:
                self.logger.error(f"Chain video not found: {video_path}")
            return None
        
        from utils.frame_extractor import FrameExtractor
        
        # Create extractor
        extractor = FrameExtractor(
            project_folder=self.project_folder,
            image_quality=95
        )
        
        # Get relative path from project folder
        try:
            # If video_path is in chains/ subfolder, we need to include that in the path
            relative_path = video_path.relative_to(self.project_folder)
        except ValueError:
            # If not relative to project_folder, use the filename
            relative_path = video_path.name
        
        # Use unified method
        result = extractor.extract_end_frame(
            str(relative_path),  # Filename relative to project
            width,
            height
        )
        
        if result and self.logger:
            self.logger.success(f"✓ Extracted last frame: {result.name}")
        elif not result and self.logger:
            self.logger.error(f"Failed to extract last frame from {video_path.name}")
        
        return result
    
    def extract_first_frame(self, video_path, width, height):
        """
        Extract FIRST frame from existing chain video
        (Uses FrameExtractor - unified implementation)
        
        Args:
            video_path: Path to existing chain video
            width: Target width
            height: Target height
        
        Returns:
            Path to extracted first frame (or None if failed)
        """
        
        if not video_path.exists():
            if self.logger:
                self.logger.error(f"Chain video not found: {video_path}")
            return None
        
        from utils.frame_extractor import FrameExtractor
        
        # Create extractor
        extractor = FrameExtractor(
            project_folder=self.project_folder,
            image_quality=95
        )
        
        # Get relative path from project folder
        try:
            relative_path = video_path.relative_to(self.project_folder)
        except ValueError:
            relative_path = video_path.name
        
        # Use unified method
        result = extractor.extract_start_frame(
            str(relative_path),  # Filename relative to project
            width,
            height
        )
        
        if result and self.logger:
            self.logger.success(f"✓ Extracted first frame: {result.name}")
        elif not result and self.logger:
            self.logger.error(f"Failed to extract first frame from {video_path.name}")
        
        return result
    
    def resolve_dependencies(self, chain_prefix, total_steps):
        """
        Resolve which chain steps need generation and how
        
        Smart gap resolution:
        - Single isolated gap → I2V2I (use neighbors)
        - Consecutive gaps → I2V forward generation
        - All missing → I2V forward generation
        
        Args:
            chain_prefix: Chain prefix (e.g., 'ewelina_stands')
            total_steps: Total number of steps in chain
        
        Returns:
            List of generation tasks: [
                {
                    'step': int,
                    'mode': 'i2v', 'i2v2i', or 'i2v_only',
                    'start_source': filename or 'entry_point',
                    'end_source': filename or None,
                    'depends_on': step_idx or None
                },
                ...
            ]
        """
        
        # Find existing files
        existing_files = set()
        
        for step_idx in range(1, total_steps + 1):
            step_filename = f"{chain_prefix}_{step_idx:03d}.mp4"
            step_path = self.get_chain_output_path(step_filename)
            
            if step_path.exists():
                existing_files.add(step_filename)
        
        # Resolve gaps
        tasks = self._resolve_chain_gaps(existing_files, total_steps, chain_prefix)
        
        if self.logger and len(tasks) > 0:
            self.logger.info(f"Chain '{chain_prefix}': {len(tasks)} step(s) to generate")
        
        return tasks
    
    def _resolve_chain_gaps(self, existing_files, total_steps, prefix):
        """
        Smart chain gap resolution algorithm
        
        Returns list of generation tasks
        """
        
        # Find missing steps
        missing = []
        for step_idx in range(1, total_steps + 1):
            step_file = f"{prefix}_{step_idx:03d}.mp4"
            if step_file not in existing_files:
                missing.append(step_idx)
        
        if not missing:
            return []  # Nothing to do
        
        # Group consecutive gaps
        gap_ranges = []
        current_range = [missing[0]]
        
        for step in missing[1:]:
            if step == current_range[-1] + 1:
                # Consecutive
                current_range.append(step)
            else:
                # New range
                gap_ranges.append(current_range)
                current_range = [step]
        
        gap_ranges.append(current_range)
        
        # Generate tasks
        tasks = []
        
        for gap_range in gap_ranges:
            if len(gap_range) == 1:
                # ===== SINGLE GAP → I2V2I (if possible) =====
                step = gap_range[0]
                
                prev_step = step - 1
                next_step = step + 1
                
                prev_file = f"{prefix}_{prev_step:03d}.mp4" if prev_step >= 1 else None
                next_file = f"{prefix}_{next_step:03d}.mp4" if next_step <= total_steps else None
                
                # Check if we can do I2V2I
                can_use_next = next_file and next_file in existing_files
                
                if can_use_next:
                    # I2V2I mode
                    tasks.append({
                        'step': step,
                        'mode': 'i2v2i',
                        'start_source': prev_file if prev_file else 'entry_point',
                        'end_source': next_file,
                        'depends_on': None
                    })
                else:
                    # ✅ NEW: Check if this is the LAST step in chain
                    is_last_step = (step == total_steps)
                    
                    if is_last_step:
                        # ✅ TRUE I2V - pure forward generation (no end frame)
                        tasks.append({
                            'step': step,
                            'mode': 'i2v_only',  # ← New mode!
                            'start_source': prev_file if prev_file else 'entry_point',
                            'end_source': None,
                            'depends_on': None
                        })
                    else:
                        # Standard I2V (middle of chain, next doesn't exist yet)
                        tasks.append({
                            'step': step,
                            'mode': 'i2v',
                            'start_source': prev_file if prev_file else 'entry_point',
                            'end_source': None,
                            'depends_on': None
                        })
            
            else:
                # ===== CONSECUTIVE GAPS → I2V forward =====
                for i, step in enumerate(gap_range):
                    if i == 0:
                        # First in range - use previous existing
                        prev_step = step - 1
                        prev_file = f"{prefix}_{prev_step:03d}.mp4" if prev_step >= 1 else None
                        start_source = prev_file if prev_file else 'entry_point'
                        depends_on = None
                    else:
                        # Depends on previous in range
                        start_source = f"{prefix}_{gap_range[i-1]:03d}.mp4"
                        depends_on = gap_range[i-1]
                    
                    # ✅ NEW: Check if this is the LAST step in chain
                    is_last_step = (step == total_steps)
                    
                    if is_last_step:
                        # ✅ TRUE I2V for last step
                        mode = 'i2v_only'
                    else:
                        # Standard I2V for middle steps
                        mode = 'i2v'
                    
                    tasks.append({
                        'step': step,
                        'mode': mode,
                        'start_source': start_source,
                        'end_source': None,
                        'depends_on': depends_on
                    })
        
        return tasks