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
        
        flow_list = list(self.flow)  # ensure indexable for lookahead
        for _idx, item in enumerate(flow_list):
            # ===== BREAK =====
            if isinstance(item, dict) and ('break' in item or item.get('type') == 'scene_break'):
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

                # Lookahead: find the next non-break physical file after this chain.
                # Used to set _chain_end_target on the last step so batch generation
                # can use it as the I2V2I end frame ("dociągnij do następnego ujęcia").
                _chain_end_target = None
                for _nxt in flow_list[_idx + 1:]:
                    if isinstance(_nxt, dict) and ('break' in _nxt or _nxt.get('type') == 'scene_break'):
                        break  # segment boundary — no target
                    if isinstance(_nxt, dict) and 'chain' in _nxt:
                        break  # another chain immediately after — no target
                    if isinstance(_nxt, dict) and _nxt.get('type') == 'talk':
                        break  # talk after chain — no end-frame target
                    if isinstance(_nxt, dict) and 'file' in _nxt:
                        _chain_end_target = _nxt['file']
                        break
                    if isinstance(_nxt, str):
                        _chain_end_target = _nxt
                        break
                
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

                    # Mark last step with end-target so batch can use I2V2I
                    if step_idx == len(chain_steps) and _chain_end_target:
                        merged_config['_chain_end_target'] = _chain_end_target
                    
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
            
            # ===== TALK =====
            if isinstance(item, dict) and item.get('type') == 'talk':
                # Prefer explicit prefix (avoids collisions when same mp3 is reused
                # in multiple talk items throughout the flow)
                explicit_prefix = (item.get('prefix') or '').strip()
                if explicit_prefix:
                    virtual_file = f"talk_{explicit_prefix}.mp4"
                else:
                    raw_audio = item.get('audio', '')
                    if isinstance(raw_audio, list):
                        first = raw_audio[0] if raw_audio else 'unknown'
                    else:
                        first = raw_audio
                    # audio entry may be a dict {file, pos, neg} or a plain string
                    if isinstance(first, dict):
                        first = first.get('file', 'unknown')
                    stem = Path(first).stem
                    virtual_file = f"talk_{stem}.mp4"

                # Store source image so batch pipeline can pass it to generation
                talk_config = {**item, '_is_talk': True, '_source_image': prev_file}
                current_segment.add_file(virtual_file, talk_config)
                self.all_files.append(FlowFile(virtual_file, talk_config))

                # Create a generation pair (source → talk) so that the talk
                # clip becomes a first-class item in the batch retry loop.
                # The pair uses _is_talk on to_config so the loop can dispatch
                # it to the InfiniteTalk backend instead of ComfyUI.
                if prev_file:
                    pair = TransitionPair(
                        from_file=prev_file,
                        to_file=virtual_file,
                        from_config=prev_config or {},
                        to_config=talk_config,
                    )
                    current_segment.add_transition(pair)
                    self.all_transitions.append(pair)

                # Keep prev_file = talk clip so the next item (chain/image)
                # gets a proper start-frame pair anchored to talk's end frame.
                prev_file = virtual_file
                prev_config = talk_config
                continue

            # ===== MULTITALK =====
            if isinstance(item, dict) and item.get('type') == 'multitalk':
                clip_name = (item.get('name') or '').strip()
                if not clip_name:
                    clip_name = f"multitalk_{id(item) & 0xFFFF}"
                if not clip_name.endswith('.mp4'):
                    clip_name += '.mp4'
                virtual_file = f"transitions/multitalk/{clip_name}"

                multitalk_config = {**item, '_is_multitalk': True, '_source_image': prev_file}
                current_segment.add_file(virtual_file, multitalk_config)
                self.all_files.append(FlowFile(virtual_file, multitalk_config))

                prev_file   = virtual_file
                prev_config = multitalk_config
                continue

            # ===== FILE =====
            if isinstance(item, dict) and 'file' in item:
                current_file = item['file']
                current_config = {k: v for k, v in item.items() if k != 'file'}
                
                # Add file to segment
                current_segment.add_file(current_file, current_config)
                self.all_files.append(FlowFile(current_file, current_config))
                
                # Add transition pair only when appropriate:
                # - File → File (normal bridge)
                # - Chain_last → File only if transition_to_next is set on last step
                # - Talk → File: NO bridge (talk clips cut to next scene by default)
                #   (future: add bridge if talk has explicit 'transition:' config)
                if prev_file:
                    _prev_is_talk  = (prev_config or {}).get('_is_talk', False)
                    _prev_is_chain = (prev_config or {}).get('_is_chain', False)

                    _should_pair = True
                    if _prev_is_talk:
                        _should_pair = False  # talk → file: always cut (chain snaps via end frame)
                    elif _prev_is_chain:
                        # chain → file: bridge only when explicitly requested
                        _should_pair = bool((prev_config or {}).get('transition_to_next'))

                    if _should_pair:
                        # For talk→file bridge: overlay transition params from
                        # talk's 'transition:' sub-dict so batch reads correct
                        # duration/fps/steps/cfg/pos/neg for this bridge clip.
                        _to_cfg = current_config
                        if _prev_is_talk:
                            _talk_trans = (prev_config or {}).get('transition') or {}
                            if _talk_trans:
                                _to_cfg = {**current_config}
                                for _k in ('duration', 'fps', 'steps', 'cfg', 'pos', 'neg', 'backend'):
                                    if _k in _talk_trans:
                                        _to_cfg[_k] = _talk_trans[_k]

                        pair = TransitionPair(
                            from_file=prev_file,
                            to_file=current_file,
                            from_config=prev_config,
                            to_config=_to_cfg
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
        talks_folder = transitions_folder / 'talks'
        concat_list = []

        for segment in self.segments:
            prev_file = None
            prev_flow_file = None

            for flow_file in segment.files:
                current_file = flow_file.filename
                current_is_chain = flow_file.config.get('_is_chain', False)
                current_is_talk  = flow_file.config.get('_is_talk',  False)

                # ===== TRANSITION =====
                if prev_file:
                    prev_is_chain = prev_flow_file.config.get('_is_chain', False)
                    prev_is_talk  = prev_flow_file.config.get('_is_talk',  False)

                    # Determine if we should add transition
                    should_add_transition = False

                    if not prev_is_chain and not prev_is_talk and not current_is_chain and not current_is_talk:
                        # Normal file → file
                        should_add_transition = True
                    elif prev_is_chain and not current_is_chain:
                        # Chain → file - check for transition_to_next
                        if prev_flow_file.config.get('transition_to_next'):
                            should_add_transition = True
                    elif prev_is_talk:
                        pass

                    if should_add_transition:
                        trans_name = f"{Path(prev_file).stem}_{Path(current_file).stem}_transition.mp4"
                        trans_path = transitions_folder / trans_name

                        if trans_path.exists():
                            concat_list.append(trans_path)

                # ===== SOURCE FILE =====
                if current_is_chain:
                    current_path = chains_folder / current_file
                elif current_is_talk:
                    current_path = talks_folder / current_file
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
                prev_flow_file = flow_file
        
        return concat_list
    
    def get_numbered_flow_list(self, project_folder: Path, skip_images: bool = True) -> List[Dict[str, Any]]:
        """Get list for numbered flow copying"""
        transitions_folder = project_folder / 'transitions'
        chains_folder = transitions_folder / 'chains'
        talks_folder  = transitions_folder / 'talks'
        numbered_list = []

        for segment in self.segments:
            prev_file = None
            prev_flow_file = None

            for flow_file in segment.files:
                current_file = flow_file.filename
                current_is_chain = flow_file.config.get('_is_chain', False)
                current_is_talk  = flow_file.config.get('_is_talk',  False)

                # ===== TRANSITION =====
                if prev_file:
                    prev_is_chain = prev_flow_file.config.get('_is_chain', False)
                    prev_is_talk  = prev_flow_file.config.get('_is_talk',  False)

                    should_add_transition = False

                    if not prev_is_chain and not prev_is_talk and not current_is_chain and not current_is_talk:
                        # Normal file → file
                        should_add_transition = True
                    elif prev_is_chain and not current_is_chain:
                        # Chain → file - check for transition_to_next
                        if prev_flow_file.config.get('transition_to_next'):
                            should_add_transition = True
                    elif prev_is_talk:
                        pass

                    if should_add_transition:
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
                elif current_is_talk:
                    current_path = talks_folder / current_file
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
                prev_flow_file = flow_file
        
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