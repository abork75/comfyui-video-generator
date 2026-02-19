# -*- coding: utf-8 -*-
"""
FLOW Parser - Single source of truth for FLOW parsing

This module is the ONLY place where FLOW structure is parsed.
All scripts (batch_transitions, postprocessing, etc.) use this parser.

Adding new FLOW features (like 'chain', 'loop', etc.) only requires
changes in this file - all scripts automatically support them.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TransitionPair:
    """Represents a transition between two files"""
    from_file: str
    to_file: str
    from_config: Dict[str, Any]
    to_config: Dict[str, Any]
    
    def get_transition_name(self) -> str:
        """Generate transition filename"""
        stem_a = Path(self.from_file).stem
        stem_b = Path(self.to_file).stem
        return f"{stem_a}_{stem_b}_transition.mp4"


@dataclass
class FlowFile:
    """Represents a file in FLOW"""
    filename: str
    config: Dict[str, Any]
    
    def is_image(self) -> bool:
        """Check if file is an image"""
        ext = Path(self.filename).suffix.lower()
        return ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    def is_video(self) -> bool:
        """Check if file is a video"""
        ext = Path(self.filename).suffix.lower()
        return ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']


class FlowSegment:
    """Represents one segment (between breaks)"""
    
    def __init__(self):
        self.files: List[FlowFile] = []
        self.transitions: List[TransitionPair] = []
    
    def add_file(self, filename: str, config: Dict[str, Any]):
        """Add file to segment"""
        self.files.append(FlowFile(filename, config))
    
    def add_transition(self, pair: TransitionPair):
        """Add transition between files"""
        self.transitions.append(pair)
    
    def __repr__(self):
        return f"<FlowSegment files={len(self.files)} transitions={len(self.transitions)}>"


class FlowParser:
    """
    Parse FLOW structure into structured data
    
    Usage:
        parser = parse_flow(flow)
        
        # Get transition pairs for generation
        pairs = parser.get_transition_pairs()
        
        # Get files for concat
        files = parser.get_concat_list(project_folder)
        
        # Get files for numbered flow
        items = parser.get_numbered_flow_list(project_folder)
    """
    
    def __init__(self, flow: List[Dict[str, Any]]):
        self.flow = flow
        self.segments: List[FlowSegment] = []
        self.all_transitions: List[TransitionPair] = []
        self.all_files: List[FlowFile] = []
    
    def parse(self) -> 'FlowParser':
        """Parse FLOW and build structured data"""
        
        current_segment = FlowSegment()
        prev_file = None
        prev_config = None
        
        for item in self.flow:
            # ===== BREAK =====
            if isinstance(item, dict) and 'break' in item:
                if current_segment.files:
                    self.segments.append(current_segment)
                current_segment = FlowSegment()
                prev_file = None
                prev_config = None
                continue
            
            # ===== CHAIN ===== (FIXED!)
            if isinstance(item, dict) and 'chain' in item:
                chain_steps = item['chain']
                chain_base_config = {k: v for k, v in item.items() if k not in ['chain', 'chain_prefix', 'transition_to_next']}
                chain_prefix = item.get('chain_prefix', 'chain_step')
                transition_to_next = item.get('transition_to_next', None)
                
                # Expand each step as virtual file
                for step_idx, step_config in enumerate(chain_steps, 1):
                    merged_config = {**chain_base_config, **step_config}
                    
                    # Add chain metadata
                    merged_config['_is_chain'] = True
                    merged_config['_chain_prefix'] = chain_prefix
                    merged_config['_chain_step'] = step_idx
                    merged_config['_chain_total'] = len(chain_steps)
                    
                    # Add transition_to_next ONLY to LAST step
                    if step_idx == len(chain_steps) and transition_to_next:
                        merged_config['transition_to_next'] = transition_to_next
                    
                    # Virtual filename
                    virtual_file = f"{chain_prefix}_{step_idx:03d}.mp4"
                    
                    # Add as normal file
                    current_segment.add_file(virtual_file, merged_config)
                    self.all_files.append(FlowFile(virtual_file, merged_config))
                    
                    # ========================================
                    # FIX: CREATE TRANSITION PAIRS FOR CHAIN!
                    # ========================================
                    
                    if step_idx == 1:
                        # FIRST STEP: prev_file → chain_001
                        if prev_file:
                            pair = TransitionPair(
                                from_file=prev_file,
                                to_file=virtual_file,
                                from_config=prev_config,
                                to_config=merged_config
                            )
                            current_segment.add_transition(pair)
                            self.all_transitions.append(pair)
                    else:
                        # INTERNAL STEPS: chain_N → chain_N+1
                        prev_virtual = f"{chain_prefix}_{step_idx-1:03d}.mp4"
                        prev_virtual_config = {**chain_base_config, **chain_steps[step_idx-2]}
                        prev_virtual_config['_is_chain'] = True
                        prev_virtual_config['_chain_prefix'] = chain_prefix
                        prev_virtual_config['_chain_step'] = step_idx - 1
                        prev_virtual_config['_chain_total'] = len(chain_steps)
                        
                        pair = TransitionPair(
                            from_file=prev_virtual,
                            to_file=virtual_file,
                            from_config=prev_virtual_config,
                            to_config=merged_config
                        )
                        current_segment.add_transition(pair)
                        self.all_transitions.append(pair)
                    
                    # Update prev for next iteration
                    prev_file = virtual_file
                    prev_config = merged_config
                
                # Chain expansion complete - prev_file now points to last chain step
                continue
            
            # ===== FILE =====
            if isinstance(item, dict) and 'file' in item:
                current_file = item['file']
                current_config = {k: v for k, v in item.items() if k != 'file'}
                
                # Add file to segment
                current_segment.add_file(current_file, current_config)
                self.all_files.append(FlowFile(current_file, current_config))
                
                # ✅ Add transition if prev exists
                # This handles:
                # - File → File (normal)
                # - Chain_last → File (automatically, because prev_file is chain_last)
                if prev_file:
                    pair = TransitionPair(
                        from_file=prev_file,
                        to_file=current_file,
                        from_config=prev_config,
                        to_config=current_config
                    )
                    current_segment.add_transition(pair)
                    self.all_transitions.append(pair)
                
                prev_file = current_file
                prev_config = current_config
        
        # Save last segment
        if current_segment.files:
            self.segments.append(current_segment)
        
        return self
    
    def get_transition_pairs(self) -> List[TransitionPair]:
        """
        Get all transition pairs for generation
        
        Returns:
            List of TransitionPair objects
        """
        return self.all_transitions
    
    def get_all_files(self) -> List[FlowFile]:
        """Get all files in FLOW"""
        return self.all_files
    
    def get_concat_list(self, project_folder: Path, skip_images: bool = True) -> List[Path]:
        """Get list of files for concat (with transitions)"""
        transitions_folder = project_folder / 'transitions'
        chains_folder = transitions_folder / 'chains'
        concat_list = []
        
        for segment in self.segments:
            prev_file = None
            prev_is_chain = False
            
            for flow_file in segment.files:
                current_file = flow_file.filename
                current_is_chain = flow_file.config.get('_is_chain', False)
                
                # ===== TRANSITION =====
                if prev_file:
                    # ✅ ONLY File → File transitions
                    if not prev_is_chain and not current_is_chain:
                        trans_name = f"{Path(prev_file).stem}_{Path(current_file).stem}_transition.mp4"
                        trans_path = transitions_folder / trans_name
                        
                        if trans_path.exists():
                            concat_list.append(trans_path)
                
                # ===== SOURCE FILE =====
                if current_is_chain:
                    current_path = chains_folder / current_file
                else:
                    current_path = project_folder / current_file
                
                should_add = False
                
                if skip_images:
                    if flow_file.is_video() and current_path.exists():
                        should_add = True
                else:
                    if current_path.exists():
                        should_add = True
                
                if should_add:
                    concat_list.append(current_path)
                
                prev_file = current_file
                prev_is_chain = current_is_chain
        
        return concat_list
    
    def get_numbered_flow_list(self, project_folder: Path, skip_images: bool = True) -> List[Dict[str, Any]]:
        """Get list for numbered flow copying"""
        transitions_folder = project_folder / 'transitions'
        chains_folder = transitions_folder / 'chains'
        numbered_list = []
        
        for segment in self.segments:
            prev_file = None
            prev_is_chain = False
            
            for flow_file in segment.files:
                current_file = flow_file.filename
                current_is_chain = flow_file.config.get('_is_chain', False)
                
                # ===== TRANSITION =====
                if prev_file:
                    # ✅ COMPLETE FIX: Skip ANY transition involving chain
                    # - Chain steps ARE transitions (nie potrzebują osobnych)
                    # - File → Chain: pierwszy chain step = transition z File
                    # - Chain → Chain: chain sekwencja (no transition)
                    # - Chain → File: tylko jeśli explicit transition_to_next
                    
                    if not prev_is_chain and not current_is_chain:
                        # ✅ ONLY File → File (normal transition)
                        trans_name = f"{Path(prev_file).stem}_{Path(current_file).stem}_transition.mp4"
                        trans_path = transitions_folder / trans_name
                        
                        numbered_list.append({
                            'type': 'transition',
                            'path': trans_path,
                            'name': trans_name,
                            'exists': trans_path.exists()
                        })
                
                # ===== SOURCE FILE =====
                if current_is_chain:
                    current_path = chains_folder / current_file
                else:
                    current_path = project_folder / current_file
                
                if skip_images and flow_file.is_image():
                    numbered_list.append({
                        'type': 'skip',
                        'path': current_path,
                        'name': current_file,
                        'reason': 'image'
                    })
                else:
                    numbered_list.append({
                        'type': 'file',
                        'path': current_path,
                        'name': current_file,
                        'exists': current_path.exists()
                    })
                
                prev_file = current_file
                prev_is_chain = current_is_chain
        
        return numbered_list
    
    def print_summary(self):
        """Print FLOW summary (for debugging)"""
        print(f"FLOW Summary:")
        print(f"  Segments: {len(self.segments)}")
        print(f"  Total files: {len(self.all_files)}")
        print(f"  Total transitions: {len(self.all_transitions)}")
        print()
        
        for i, segment in enumerate(self.segments, 1):
            print(f"  Segment {i}:")
            print(f"    Files: {len(segment.files)}")
            print(f"    Transitions: {len(segment.transitions)}")


# ============================================================
# CONVENIENCE FUNCTION
# ============================================================

def parse_flow(flow: List[Dict[str, Any]]) -> FlowParser:
    """
    Parse FLOW structure (convenience function)
    
    Args:
        flow: FLOW list from config
    
    Returns:
        Parsed FlowParser object
    
    Example:
        parser = parse_flow(config['flow'])
        pairs = parser.get_transition_pairs()
    """
    parser = FlowParser(flow)
    return parser.parse()