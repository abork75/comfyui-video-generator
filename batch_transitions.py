# -*- coding: utf-8 -*-
"""
Batch Transition Generator - Orchestrator Mode
Unified system supporting multiple backends and workflow types
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.logger import Logger
from flow_parser import parse_flow

# Backend modules
from backends.cloud_backend import CloudBackend
from backends.local_backend import LocalBackend
from backends.linux_backend import LinuxBackend

from helpers.chain_handler import ChainHandler
from backends.atlascloud_video_backend import AtlasCloudVideoBackend

def _upscale_video_inplace(video_path: Path, width: int, height: int) -> bool:
    """
    Rescale a video to the target resolution using ffmpeg, replacing the file in-place.
    Returns True on success, False on failure (original file is preserved on failure).
    """
    import subprocess
    tmp = video_path.with_name(video_path.stem + "._upscale_tmp.mp4")
    try:
        cmd = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vf", f"scale={width}:{height}:flags=lanczos",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-c:a", "copy",
            str(tmp),
        ]
        r = subprocess.run(cmd, capture_output=True, timeout=600)
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.replace(video_path)
            return True
    except Exception:
        pass
    if tmp.exists():
        try:
            tmp.unlink()
        except Exception:
            pass
    return False


def run_batch_generation(config):
    """
    Main orchestrator - unified batch generation
    Supports multiple backends + workflow types
    
    Args:
        config: Configuration dict with:
            - project_folder
            - flow
            - generic_prompts
            - default_* (duration, fps, etc.)
            - backend-specific settings
    """
    # Get debug flag from config (local variable)
    DEBUG_LOG = config.get('debug_log', True)
   
    # ============================================================
    # INITIALIZE LOGGER (FIRST!)
    # ============================================================
    logger = Logger()
    
    # ============================================================
    # CHECK POSTPROCESSING MODE (BEFORE NORMAL FLOW)
    # ============================================================
    
    postprocessing_config = config.get('postprocessing', {})
    
    if postprocessing_config.get('enabled', False):
        print("\n" + "="*70)
        print("⚠️  POSTPROCESSING MODE ENABLED")
        print("="*70)
        print("Transition generation will be SKIPPED.")
        
        # Show enabled processors
        enabled = []
        if postprocessing_config.get('full_concat'): enabled.append('full_concat')
        if postprocessing_config.get('numbered_flow'): enabled.append('numbered_flow')
        if postprocessing_config.get('upscale'): enabled.append('upscale')
        
        print(f"Processors enabled: {', '.join(enabled) if enabled else 'NONE'}")
        print("="*70 + "\n")
        
        response = input("Continue with postprocessing? (yes/no): ").strip().lower()

        if response not in ['yes', 'y']:
            print("❌ Cancelled by user")
            return
        
        # Import postprocessing engine
        from postprocessing.postprocess_engine import run_postprocessing
        
        # Run postprocessing instead
        run_postprocessing(config)
        return  # Exit early - skip transition generation
    
    # ============================================================
    # NORMAL FLOW - Transition Generation
    # ============================================================
    
    logger.header("BATCH GENERATOR - ORCHESTRATOR MODE")
    
    # Validate config
    required = ['project_folder', 'flow']
    missing = [k for k in required if k not in config]
    if missing:
        logger.error(f"Missing required config: {', '.join(missing)}")
        return
    
    project_folder = Path(config['project_folder'])
    flow = config['flow']

    # ── Frame path helpers ─────────────────────────────────────────────────────
    # New projects: PNG (lossless). Old projects: fall back to JPEG.
    def _frame_path(stem: str, suffix: str) -> Path:
        """Return frames/{stem}_{suffix}.png, falling back to .jpg if .png absent."""
        png = project_folder / 'frames' / f"{stem}_{suffix}.png"
        if png.exists():
            return png
        jpg = project_folder / 'frames' / f"{stem}_{suffix}.jpg"
        return jpg   # may not exist either — caller checks .exists()

    def _real_frame_path(stem: str) -> Path:
        """Return frames/{stem}_real.png — actual last frame of the transition
        that generated the file 'stem'. Written after each generation so that
        the next clip starts from exactly where the previous one ended, not from
        the static source image (which WAN never reaches precisely)."""
        return project_folder / 'frames' / f"{stem}_real.png"

    # Folder paths — defined early so all sections can reference them
    transitions_folder = project_folder / 'transitions'
    transitions_folder.mkdir(parents=True, exist_ok=True)
    talks_folder = transitions_folder / 'talks'
    talks_folder.mkdir(exist_ok=True)

    # Defaults
    default_backend = config.get('default_backend', 'local')
    default_duration = config.get('default_duration', 16)
    default_fps = config.get('default_fps', 8)
    default_steps = config.get('default_steps', 25)
    default_cfg = config.get('default_cfg', 2.5)
    default_seed = config.get('default_seed', -1)
    default_positive_prompt = config.get('default_positive_prompt', '')
    default_negative_prompt = config.get('default_negative_prompt', '')
    default_audio_prompt         = config.get('default_audio_prompt', '')
    default_audio_negative_prompt = config.get('default_audio_negative_prompt', '')
    default_blocks_to_swap      = config.get('default_blocks_to_swap', None)
    default_frame_interpolation = config.get('default_frame_interpolation', True)

    # If global auto_blocks_to_swap is enabled, let generate_transition() calculate
    # BTS per-clip from the auto_bts_table (based on resolution). Setting default to
    # None here ensures the fallback chain (lines below) yields None for unconfigured
    # tiles, which triggers auto-calculation in base_backend.generate_transition().
    try:
        from app.services.app_config_service import get_defaults as _get_gdefs
        if _get_gdefs().get("auto_blocks_to_swap", False):
            default_blocks_to_swap = None
    except Exception:
        pass

    # Check ffmpeg
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        logger.success("ffmpeg OK")
    except:
        logger.error("ffmpeg not found! Install: https://ffmpeg.org/download.html")
        return
    
    logger.success(f"Project: {project_folder.name}")
    
    # ============================================================
    # PARSE FLOW (using flow_parser module)
    # ============================================================
    
    logger.section("Parsing FLOW")
    
    parser = parse_flow(flow)
    transition_pairs = parser.get_transition_pairs()
    
    logger.success(f"Found {len(parser.get_all_files())} files")
    logger.info(f"Breaks: {len(parser.segments) - 1}")
    
    # Build pairs for processing (with metadata), tagged by segment index
    pairs = []
    for seg_idx, segment in enumerate(parser.segments):
      for pair in segment.transitions:
        from_file = pair.from_file
        to_file = pair.to_file
        from_config = pair.from_config
        to_config = pair.to_config
        
        if DEBUG_LOG:
            # 🐛 DEBUG
            print(f"\n🐛 DEBUG Transition {from_file} → {to_file}")
            print(f"   from_config: {from_config}")
            print(f"   to_config: {to_config}")
            print(f"   default_backend: {default_backend}")    
        
        # ============================================================
        # DETECT: Is this a chain→next transition?
        # FIX: Check '_is_chain' flag instead of 'chain' key
        # ============================================================
        
        is_chain_to_next_transition = (
            from_config.get('_is_chain', False) and  # ← FROM jest chain step
            not to_config.get('_is_chain', False) and  # ← TO NIE jest chain step  
            'transition_to_next' in from_config  # ← Ma transition_to_next config
        )
        
        
        # ============================================================
        # BUILD TRANSITION CONFIG
        # ============================================================
        
        if is_chain_to_next_transition:
            # === CHAIN→NEXT TRANSITION ===
            # Inherit parameters from chain config
            # Use transition_to_next for prompts/duration
            # Allow override of any parameter in transition_to_next
            
            chain_config = from_config
            transition_to_next = chain_config.get('transition_to_next', {})
            
            # Backend priority: transition_to_next > to_config > chain > default
            backend = transition_to_next.get('backend') or to_config.get('backend') or chain_config.get('backend') or default_backend
            
            trans_config = {
                'from_file': from_file,
                'to_file': to_file,
                'from_config': from_config,
                'to_config': to_config,
                'backend': backend,
                
                # Priority: transition_to_next > chain_config > default
                'fps': transition_to_next.get('fps', chain_config.get('fps', default_fps)),
                'steps': transition_to_next.get('steps', chain_config.get('steps', default_steps)),
                'cfg': transition_to_next.get('cfg', chain_config.get('cfg', default_cfg)),
                'seed': transition_to_next.get('seed', chain_config.get('seed', default_seed)),
                'duration': transition_to_next.get('duration', default_duration),
                'positive_prompt': transition_to_next.get('pos', default_positive_prompt),
                'negative_prompt': transition_to_next.get('neg', chain_config.get('neg', default_negative_prompt)),
                'width': transition_to_next.get('width', chain_config.get('width', None)),
                'height': transition_to_next.get('height', chain_config.get('height', None)),
                'blocks_to_swap': transition_to_next.get('blocks_to_swap', chain_config.get('blocks_to_swap', default_blocks_to_swap)),
                'frame_interpolation': transition_to_next.get('frame_interpolation', chain_config.get('frame_interpolation', default_frame_interpolation)),
                'lora_name':     transition_to_next.get('lora_name',     chain_config.get('lora_name')),
                'lora_strength': transition_to_next.get('lora_strength', chain_config.get('lora_strength')),
                'lora_high':     transition_to_next.get('lora_high',     chain_config.get('lora_high')),
                'lora_low':      transition_to_next.get('lora_low',      chain_config.get('lora_low')),
                'generate_count': transition_to_next.get('generate_count', chain_config.get('generate_count', 1)),
                'use_lightning':  transition_to_next.get('use_lightning',  chain_config.get('use_lightning')),

                # Mark as normal I2V2I (not chain I2V)
                'is_i2v_mode': False,
                'atlascloud_resolution':    transition_to_next.get('atlascloud_resolution',    chain_config.get('atlascloud_resolution')),
                'atlascloud_prompt_extend': transition_to_next.get('atlascloud_prompt_extend', chain_config.get('atlascloud_prompt_extend')),
            }
            
        else:
            # === NORMAL TRANSITION or CHAIN STEP ===

            # Determine backend
            backend = from_config.get('backend') or to_config.get('backend') or default_backend

            # ============================================================
            # ✅ FIX: Different priority for chain files vs normal transitions
            # ============================================================

            is_from_talk = from_config.get('_is_talk', False)
            is_to_chain = to_config.get('_is_chain', False)
            
            if is_to_chain:
                # CHAIN FILE - use TO config (chain params) first!
                trans_config = {
                    'from_file': from_file,
                    'to_file': to_file,
                    'from_config': from_config,
                    'to_config': to_config,
                    'backend': backend,
                    # Priority: TO (chain) > FROM > default
                    'duration': to_config.get('duration', from_config.get('duration', default_duration)),
                    'fps': to_config.get('fps', from_config.get('fps', default_fps)),
                    'steps': to_config.get('steps', from_config.get('steps', default_steps)),
                    'cfg': to_config.get('cfg', from_config.get('cfg', default_cfg)),
                    'seed': to_config.get('seed', from_config.get('seed', default_seed)),
                    'positive_prompt': to_config.get('pos', from_config.get('pos', default_positive_prompt)),
                    'negative_prompt': to_config.get('neg', from_config.get('neg', default_negative_prompt)),
                    'audio_prompt': to_config.get('audio_prompt', from_config.get('audio_prompt', default_audio_prompt)),
                    'audio_negative_prompt': to_config.get('audio_negative_prompt', from_config.get('audio_negative_prompt', default_audio_negative_prompt)),
                    # ✅ FIX: talk clips carry their own portrait width/height (e.g. 608x832)
                    # which must NOT bleed into the chain resolution — skip them.
                    'width': to_config.get('width') or (None if is_from_talk else from_config.get('width')),
                    'height': to_config.get('height') or (None if is_from_talk else from_config.get('height')),
                    'blocks_to_swap': to_config.get('blocks_to_swap', from_config.get('blocks_to_swap', default_blocks_to_swap)),
                    'frame_interpolation': to_config.get('frame_interpolation', from_config.get('frame_interpolation', default_frame_interpolation)),
                    'lora_name':     to_config.get('lora_name',     from_config.get('lora_name')),
                    'lora_strength': to_config.get('lora_strength', from_config.get('lora_strength')),
                    'lora_high':     to_config.get('lora_high',     from_config.get('lora_high')),
                    'lora_low':      to_config.get('lora_low',      from_config.get('lora_low')),
                    'generate_count': to_config.get('generate_count', from_config.get('generate_count', 1)),
                    'use_lightning':  to_config.get('use_lightning'),
                    'is_i2v_mode': True,  # Chain is always I2V
                    'atlascloud_resolution':    to_config.get('atlascloud_resolution',    from_config.get('atlascloud_resolution')),
                    'atlascloud_prompt_extend': to_config.get('atlascloud_prompt_extend', from_config.get('atlascloud_prompt_extend')),
                }
            else:
                # NORMAL TRANSITION - use FROM config first
                trans_config = {
                    'from_file': from_file,
                    'to_file': to_file,
                    'from_config': from_config,
                    'to_config': to_config,
                    'backend': backend,
                    # Priority: FROM > TO > default
                    'duration': from_config.get('duration', to_config.get('duration', default_duration)),
                    'fps': from_config.get('fps', to_config.get('fps', default_fps)),
                    'steps': from_config.get('steps', to_config.get('steps', default_steps)),
                    'cfg': from_config.get('cfg', to_config.get('cfg', default_cfg)),
                    'seed': from_config.get('seed', to_config.get('seed', default_seed)),
                    'positive_prompt': from_config.get('pos', to_config.get('pos', default_positive_prompt)),
                    'negative_prompt': from_config.get('neg', to_config.get('neg', default_negative_prompt)),
                    'audio_prompt': from_config.get('audio_prompt', to_config.get('audio_prompt', default_audio_prompt)),
                    'audio_negative_prompt': from_config.get('audio_negative_prompt', to_config.get('audio_negative_prompt', default_audio_negative_prompt)),
                    # ✅ FIX: talk clips have their own width/height (e.g. 480x832 portrait)
                    # which must NOT be inherited as the transition resolution — skip them.
                    'width': (None if is_from_talk else from_config.get('width', None)) or to_config.get('width', None),
                    'height': (None if is_from_talk else from_config.get('height', None)) or to_config.get('height', None),
                    'blocks_to_swap': from_config.get('blocks_to_swap', to_config.get('blocks_to_swap', default_blocks_to_swap)),
                    'frame_interpolation': from_config.get('frame_interpolation', to_config.get('frame_interpolation', default_frame_interpolation)),
                    'lora_name':     from_config.get('lora_name',     to_config.get('lora_name')),
                    'lora_strength': from_config.get('lora_strength', to_config.get('lora_strength')),
                    'lora_high':     from_config.get('lora_high',     to_config.get('lora_high')),
                    'lora_low':      from_config.get('lora_low',      to_config.get('lora_low')),
                    'generate_count': from_config.get('generate_count', to_config.get('generate_count', 1)),
                    'use_lightning':  from_config.get('use_lightning',  to_config.get('use_lightning')),
                    'is_i2v_mode': False,
                    'atlascloud_resolution':    from_config.get('atlascloud_resolution',    to_config.get('atlascloud_resolution')),
                    'atlascloud_prompt_extend': from_config.get('atlascloud_prompt_extend', to_config.get('atlascloud_prompt_extend')),
                }

        if DEBUG_LOG:
            if is_chain_to_next_transition:
                print(f"   ⛓️→🎬 Chain-to-next transition detected!")
                print(f"   Using transition_to_next prompt: {trans_config['positive_prompt'][:60]}...")
            elif is_to_chain:
                print(f"   ⛓️ Chain file generation")
                print(f"   Duration: {trans_config['duration']}s")
                print(f"   Using prompt: {trans_config['positive_prompt'][:60]}...")
            else:
                print(f"   📁 Normal transition")
                print(f"   Using prompt: {trans_config['positive_prompt'][:60]}...")        
        
        
        trans_config['_segment_idx'] = seg_idx
        pairs.append(trans_config)
    
    if not pairs:
        logger.warning("No transitions to generate (check for breaks or single file)")
        return
    
    # ============================================================
    # VERIFY FILES
    # ============================================================

    # Peek at only_transitions early — when targeting specific files,
    # missing source files outside that subset should warn but not block.
    _early_only_filter = config.get('only_transitions') or os.environ.get('ONLY_TRANSITIONS', '').strip()
    if _early_only_filter:
        if isinstance(_early_only_filter, str):
            _early_only_names = {n.strip() for n in _early_only_filter.split(',') if n.strip()}
        else:
            _early_only_names = {str(n).strip() for n in _early_only_filter if str(n).strip()}
    else:
        _early_only_names = set()

    logger.section(f"Verifying {len(parser.get_all_files())} files")

    all_files_ok = True

    for i, flow_file in enumerate(parser.get_all_files()):
        # Skip chain files (they don't exist yet)
        if flow_file.config.get('_is_chain'):
            chain_marker = "⛓️ "
            logger.info(f"[{i:02d}] {chain_marker} {flow_file.filename} (virtual - will be generated)")
            continue

        # Talk files are generated by the web UI talk_service
        if flow_file.config.get('_is_talk'):
            talk_dest = talks_folder / flow_file.filename
            status = "✓ exists" if talk_dest.exists() else "⏳ pending generation"
            logger.info(f"[{i:02d}] 🎙️  {flow_file.filename} ({status})")
            continue

        file_path = project_folder / flow_file.filename

        if not file_path.exists():
            if _early_only_names:
                # Targeted re-gen: warn but don't block — the missing file
                # may not be needed for the specific transition requested.
                logger.warning(f"[{i:02d}] ⚠ Missing (not needed for target): {flow_file.filename}")
            else:
                logger.error(f"[{i:02d}] Missing: {flow_file.filename}")
                all_files_ok = False
        else:
            file_type = "📷" if flow_file.is_image() else "🎬"
            backend_marker = "💻"  # Default local

            if flow_file.config.get('backend') == 'cloud':
                backend_marker = "☁️"

            logger.info(f"[{i:02d}] {file_type} {backend_marker} {flow_file.filename}")

    if not all_files_ok:
        logger.error("Some files are missing!")
        return

    logger.success(f"Files OK! ({len(parser.get_all_files())} found)")
    
    # ============================================================
    # VALIDATE ASPECT RATIOS
    # ============================================================
    
    logger.section("Validating aspect ratios")
    
    from utils.aspect_ratio_validator import validate_aspect_ratios
    
    aspect_ratio_tolerance = config.get('aspect_ratio_tolerance', 0.02)
    aspect_ratio_strategy = config.get('aspect_ratio_strategy', 'most_common')
    
    # Filter out virtual files (chain, talk) for AR validation and resolution detection
    non_chain_files = [
        f.filename for f in parser.get_all_files()
        if not f.config.get('_is_chain') and not f.config.get('_is_talk')
    ]
    
    ar_valid, ar_info = validate_aspect_ratios(
        project_folder,
        non_chain_files,
        tolerance=aspect_ratio_tolerance,
        strategy=aspect_ratio_strategy
    )
    
    if not ar_valid:
        logger.error("Aspect ratio validation failed!")
        logger.error(ar_info.get('error', 'Unknown error'))
        
        if not config.get('skip_ar_validation', False):
            return
        else:
            logger.warning("Continuing anyway (skip_ar_validation=True)")
    else:
        baseline_ar = ar_info.get('baseline_ar', 'N/A')
        logger.info(f"Baseline AR (most_common): {baseline_ar:.3f}")
        logger.success("Aspect ratios OK")
    
    # ============================================================
    # FRAME EXTRACTION
    # ============================================================
    
    logger.header("FRAME EXTRACTION")
    
    from utils.frame_extractor import FrameExtractor
    
    extractor = FrameExtractor(
        project_folder=project_folder,
        min_width=config.get('min_width', 256),
        min_height=config.get('min_height', 256),
        max_width=config.get('max_width', 1024),
        max_height=config.get('max_height', 1024),
        default_resolution=config.get('default_resolution', None),
        force_resolution=config.get('force_resolution', None),
        image_quality=config.get('image_quality', 95)
    )
    
    # Auto-detect resolution
    logger.section("Auto-detecting resolution")

    target_width, target_height = extractor.auto_detect_resolution(non_chain_files)

    # Safety snap: ensure divisible by 16 — WanVideo ImageResizeKJv2 (node 68)
    # uses divisible_by=16. Passing a non-aligned value causes silent adjustment
    # and makes extracted frames inconsistent with actual video output.
    _tw_snapped = (target_width  // 16) * 16
    _th_snapped = (target_height // 16) * 16
    if _tw_snapped != target_width or _th_snapped != target_height:
        logger.warning(
            f"  Resolution {target_width}x{target_height} not divisible by 16 "
            f"— snapping to {_tw_snapped}x{_th_snapped}"
        )
        target_width, target_height = _tw_snapped, _th_snapped

    logger.success(f"Final resolution: {target_width}x{target_height}")
    
    # Extract frames (only for non-chain files)
    logger.section("Preparing frames")
    
    frames_folder = project_folder / 'frames'
    
    for i, flow_file in enumerate(parser.get_all_files(), 1):
        if flow_file.config.get('_is_chain'):
            continue  # Skip chain files - frames extracted during generation
        if flow_file.config.get('_is_talk'):
            # If talk clip already exists, extract its end-frame now so that
            # chain/transition anchoring to it can find the frame in pass 1.
            _talk_clip = talks_folder / flow_file.filename
            if _talk_clip.exists():
                _rel_talk = str(Path('transitions') / 'talks' / flow_file.filename)
                _ef = extractor.extract_end_frame(_rel_talk, target_width, target_height)
                _status = f"end-frame {'ok' if (_ef and _ef.exists()) else 'FAILED'}"
            else:
                _status = "pending generation"
            logger.info(f"[{i}] 🎙️  {flow_file.filename} ({_status})")
            continue
        
        filename = flow_file.filename
        logger.info(f"\n[{i}] {filename}")
        
        if flow_file.is_video():
            # Extract start and end frames
            extractor.extract_start_frame(filename, target_width, target_height)
            extractor.extract_end_frame(filename, target_width, target_height)
        else:
            # Image - only extract end frame (for transitions FROM this file)
            extractor.extract_start_frame(filename, target_width, target_height)
            extractor.extract_end_frame(filename, target_width, target_height)
    
    logger.success(f"\nFrames ready!")

    # ── Extract _real.png for already-existing normal transitions ──────────────
    # When batch is re-run with skip_existed=True, existing transition videos
    # are not regenerated — but downstream items (next transition or talk) still
    # need _real.png to know where the video actually ended. Extract it now if
    # the transition file exists but _real.png is missing.
    # Initialize chain handler early — needed by pre-extraction pass below
    # (also used again at line ~551 but ChainHandler is cheap to create once here)
    chain_handler = ChainHandler(project_folder, logger=logger)

    # This block runs before the existing/missing split so it covers all cases.
    logger.section("Pre-extracting _real.png for existing transitions")
    _real_preextract_count = 0
    for _pair in pairs:
        _tc = _pair.get('to_config', {})

        # ── Chain last step with end-target image ────────────────────────
        # When the last chain step targets a static image (e.g. chain ends
        # with _chain_end_target='11.53. siedzi na pilce.png'), the next
        # item anchored to that image (typically a talk clip) should start
        # from the chain's actual last frame, not the static source image.
        # Write the chain's last frame as {target}_real.png so the existing
        # talk-source-frame logic picks it up without any other changes.
        if _tc.get('_is_chain'):
            _end_target = _tc.get('_chain_end_target')
            _is_last    = (_tc.get('_chain_step') == _tc.get('_chain_total'))
            if _end_target and _is_last:
                _target_real = _real_frame_path(Path(_end_target).stem)
                if not _target_real.exists():
                    _chain_vid = chain_handler.get_chain_output_path(_pair['to_file'])
                    if _chain_vid.exists():
                        _extracted = extractor.extract_last_frame_to(
                            _chain_vid, target_width, target_height, _target_real
                        )
                        if _extracted:
                            _real_preextract_count += 1
                            logger.info(
                                f"  💾 {Path(_end_target).stem}_real.png "
                                f"(from chain last step {_pair['to_file']})"
                            )
            continue  # chains have no _real of their own in this pass

        if _tc.get('_is_talk'):
            continue  # talks have no _real

        _to_stem = Path(_pair['to_file']).stem
        _real_p  = project_folder / 'frames' / f"{_to_stem}_real.png"
        if _real_p.exists():
            continue  # already fresh
        _trans_name = f"{Path(_pair['from_file']).stem}_{Path(_pair['to_file']).stem}_transition.mp4"
        _trans_path = transitions_folder / _trans_name
        if not _trans_path.exists():
            continue  # not yet generated — will be written after generation
        _extracted = extractor.extract_last_frame_to(
            _trans_path, target_width, target_height, _real_p
        )
        if _extracted:
            _real_preextract_count += 1
            logger.info(f"  💾 {_to_stem}_real.png (from existing transition)")
    if _real_preextract_count:
        logger.success(f"  Pre-extracted {_real_preextract_count} _real.png file(s)")
    else:
        logger.info("  (none needed)")

    # ============================================================
    # CHECK EXISTING TRANSITIONS
    # ============================================================
    
    logger.header("CHECKING EXISTING TRANSITIONS")
    
    existing_transitions = []
    missing_transitions = []
    
    # ✅ Build transition list from pairs
    all_transitions = []
    for pair_config in pairs:
        to_config = pair_config.get('to_config', {})
        
        # ✅ FIX: Use correct name for display
        if to_config.get('_is_chain', False):
            trans_name = pair_config['to_file']          # chain_001.mp4
        elif to_config.get('_is_talk', False):
            trans_name = pair_config['to_file']          # talk_foo.mp4
        else:
            trans_name = f"{Path(pair_config['from_file']).stem}_{Path(pair_config['to_file']).stem}_transition.mp4"
        
        all_transitions.append({
            'name': trans_name,
            'from_file': pair_config['from_file'],
            'to_file': pair_config['to_file'],
            'from_config': pair_config.get('from_config', {}),
            'to_config': to_config,
            'config': pair_config
        })
    
    # ============================================================
    # ✅ VALIDATOR (v1.3.0 LOGIC)
    # ============================================================
    
    # Now validate each transition
    for trans in all_transitions:
        trans_name = trans['name']
        to_config = trans.get('to_config', {})
        to_file = trans.get('to_file')
        
        # ✅ SIMPLIFIED: Check if target is chain
        is_to_chain = to_config.get('_is_chain', False)
        
        # ============================================================
        # Determine correct output path
        # ============================================================
        
        if is_to_chain:
            output_path = chain_handler.get_chain_output_path(to_file)
        elif to_config.get('_is_talk', False):
            output_path = talks_folder / to_file
        else:
            output_path = transitions_folder / trans_name

        # Check if exists
        if output_path.exists():
            # ── Resolution sanity check ───────────────────────────────────
            # Files generated with old workflow (divisible_by=32) come out at
            # 864×1184 instead of 880×1184. Show warning — do NOT auto-delete.
            # User decides what to regenerate manually via UI.
            _is_talk_out = to_config.get('_is_talk', False)
            if not _is_talk_out:
                try:
                    _probe = subprocess.run(
                        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                         '-show_entries', 'stream=width,height',
                         '-of', 'csv=p=0', str(output_path)],
                        capture_output=True, text=True, timeout=15
                    )
                    _res_str = _probe.stdout.strip()
                    if _res_str:
                        _fw, _fh = map(int, _res_str.split(','))
                        if _fw != target_width or _fh != target_height:
                            logger.warning(
                                f"  ⚠️  Resolution mismatch: {output_path.name} "
                                f"is {_fw}x{_fh}, expected {target_width}x{target_height} "
                                f"— delete manually to regenerate"
                            )
                except Exception as _probe_err:
                    logger.warning(f"  Could not probe {output_path.name}: {_probe_err}")
            existing_transitions.append(trans)
        else:
            missing_transitions.append(trans)
    
    # Wyświetl podsumowanie
    logger.section("Transition Status")

    if existing_transitions:
        logger.success(f"\n✓ EXISTING ({len(existing_transitions)}):")
        for trans in existing_transitions:
            # Determine correct path for size check
            to_config = trans['config'].get('to_config', {})
            is_to_chain = to_config.get('_is_chain', False)

            _tc = trans['config'].get('to_config', {})
            if _tc.get('_is_chain'):
                file_path = chain_handler.get_chain_output_path(trans['to_file'])
            elif _tc.get('_is_talk'):
                file_path = talks_folder / trans['to_file']
            else:
                file_path = transitions_folder / trans['name']

            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                logger.info(f"    • {trans['name']} ({size_mb:.1f} MB)")
            else:
                logger.info(f"    • {trans['name']}")

    if missing_transitions:
        logger.warning(f"\n⚠ MISSING ({len(missing_transitions)}):")
        for trans in missing_transitions:
            logger.info(f"    • {trans['name']}")

    # ============================================================
    # TALK clips — status report (generation happens in retry loop)
    # ============================================================
    talk_files = [f for f in parser.get_all_files() if f.config.get('_is_talk')]
    if talk_files:
        _talk_ready   = sum(1 for tf in talk_files if (talks_folder / tf.filename).exists())
        _talk_missing = len(talk_files) - _talk_ready
        logger.info(f"\n🎙️  TALK clips: {_talk_ready}/{len(talk_files)} ready"
                    + (f"  ({_talk_missing} pending)" if _talk_missing else ""))

    logger.info(f"\nTotal items: {len(all_transitions)}")
    logger.info(f"  Existing : {len(existing_transitions)}")
    logger.info(f"  Missing  : {len(missing_transitions)}")

    # ============================================================
    # SETUP: Talk service (used in retry loop for _is_talk items)
    # ============================================================
    _gen_fn       = None
    _talk_url     = None
    _linux_input  = None
    _linux_output = None
    try:
        from app.services.talk_service import generate_talk_clip_sync
        from app.core.config import settings as _app_settings
        _linux_input  = Path(_app_settings.comfyui_linux_input_dir)
        _linux_output = Path(_app_settings.comfyui_linux_output_dir)
        _talk_url     = _app_settings.comfyui_url
        _gen_fn       = generate_talk_clip_sync
    except Exception as _e:
        logger.warning(f"⚠ Talk service not available ({_e}) — talk items will be skipped.")

    # Allow force-regen via env var (set by process_service when force_all=True)
    # IMPORTANT: must be checked BEFORE the "all exist" early exit below.
    if os.environ.get('FORCE_REGEN', '').strip() == '1':
        config['skip_existed'] = False

    # Early exit only when skip_existed=True (normal mode) and nothing is missing.
    # When force_all / skip_existed=False we must continue to regenerate everything.
    if len(missing_transitions) == 0 and config.get('skip_existed', True):
        logger.success(f"\n✓ All items already exist! Nothing to do.")
        return {
            'success': True,
            'total': len(all_transitions),
            'generated': 0,
            'skipped': len(existing_transitions),
            'failed': 0,
        }

    # Check skip_existed flag
    if config.get('skip_existed', True):
        logger.info(f"\nSkipping {len(existing_transitions)} existing transitions")
        to_generate = missing_transitions
    else:
        logger.warning("\nRegenerating ALL transitions (skip_existed=False)")
        to_generate = all_transitions

    # ============================================================
    # FILTER: only_transitions  (targeted single-file re-generation)
    # Set via config['only_transitions'] or env var ONLY_TRANSITIONS=a.mp4,b.mp4
    # Overrides skip_existed — forces (re-)generation of just these files.
    # ============================================================

    only_filter = config.get('only_transitions') or os.environ.get('ONLY_TRANSITIONS', '').strip()
    if only_filter:
        if isinstance(only_filter, str):
            only_names = {n.strip() for n in only_filter.split(',') if n.strip()}
        else:
            only_names = {str(n).strip() for n in only_filter if str(n).strip()}
        # Pick from all_transitions so we always have the full config struct
        to_generate = [t for t in all_transitions if t['name'] in only_names]
        logger.info(f"\n🎯 Cel (only_transitions): {', '.join(sorted(only_names))}")
        if not to_generate:
            logger.warning("   Żadna tranzycja nie pasuje do filtra — sprawdź nazwy plików.")
            return

    # ============================================================
    # GENERATE TRANSITIONS (by backend)
    # ============================================================
    
    # Helper: generate_count per transition (default 1)
    def _gc(t):
        return max(1, int(t['config'].get('generate_count') or 1))

    total_runs = sum(_gc(t) for t in to_generate)
    multi_suffix = f" (×{total_runs} runs)" if total_runs != len(to_generate) else ""
    logger.header(f"GENERATING {len(to_generate)} TRANSITIONS{multi_suffix}")

    # Group by backend
    cloud_transitions      = [t for t in to_generate if t['config']['backend'] == 'cloud']
    local_transitions      = [t for t in to_generate if t['config']['backend'] == 'local']
    linux_transitions      = [t for t in to_generate if t['config']['backend'] == 'linux']
    atlascloud_transitions = [t for t in to_generate if t['config']['backend'] == 'atlascloud']

    def _runs_str(lst):
        runs = sum(_gc(t) for t in lst)
        return f" ×{runs} runs" if runs != len(lst) else ""

    logger.section("Backend Distribution")
    logger.info(f"  Cloud:       {len(cloud_transitions)}{_runs_str(cloud_transitions)}")
    logger.info(f"  Local:       {len(local_transitions)}{_runs_str(local_transitions)}")
    logger.info(f"  Linux:       {len(linux_transitions)}{_runs_str(linux_transitions)}")
    logger.info(f"  AtlasCloud:  {len(atlascloud_transitions)}{_runs_str(atlascloud_transitions)}")
    print()

    # ============================================================
    # CONFIRMATION PROMPT
    # ============================================================

    logger.section("Ready to Generate")

    # Calculate estimates (multiply by generate_count per transition)
    cloud_runs      = sum(_gc(t) for t in cloud_transitions)
    local_runs      = sum(_gc(t) for t in local_transitions)
    linux_runs      = sum(_gc(t) for t in linux_transitions)
    atlascloud_runs = sum(_gc(t) for t in atlascloud_transitions)

    cloud_cost = cloud_runs * 0.10
    cloud_time = cloud_runs * 1.5
    local_time = local_runs * 4.0
    linux_time = linux_runs * 4.0
    # AtlasCloud WAN 2.7: ~$0.15/s, default 5s → ~$0.75/clip, ~3min generation
    _ac_default_dur = config.get('duration', 5)
    ac_cost = atlascloud_runs * _ac_default_dur * 0.15
    ac_time = atlascloud_runs * 3.0
    total_time = cloud_time + local_time + linux_time + ac_time
    total_cost = cloud_cost + ac_cost

    def _runs_label(lst, runs):
        return f" (×{runs} runs)" if runs != len(lst) else ""

    logger.info(f"  Transitions: {len(to_generate)}{' (' + str(total_runs) + ' runs total)' if total_runs != len(to_generate) else ''}")
    if cloud_transitions:
        logger.info(f"  Cloud:      {len(cloud_transitions)}{_runs_label(cloud_transitions, cloud_runs)} (est. ${cloud_cost:.2f}, ~{cloud_time:.0f}min)")
    if local_transitions:
        logger.info(f"  Local:      {len(local_transitions)}{_runs_label(local_transitions, local_runs)} (FREE, ~{local_time:.0f}min)")
    if linux_transitions:
        logger.info(f"  Linux:      {len(linux_transitions)}{_runs_label(linux_transitions, linux_runs)} (FREE, ~{linux_time:.0f}min)")
    if atlascloud_transitions:
        logger.info(f"  AtlasCloud: {len(atlascloud_transitions)}{_runs_label(atlascloud_transitions, atlascloud_runs)} (est. ${ac_cost:.2f}, ~{ac_time:.0f}min) ⚠ ~${ac_cost/max(atlascloud_runs,1):.2f}/run")
    logger.info(f"  Total estimate: ${total_cost:.2f}, ~{total_time:.0f}min")
    print()
    
    # Ask for confirmation
    from colorama import Fore, Style
    response = input(f"{Fore.YELLOW}Proceed with generation? [Y/n]: {Style.RESET_ALL}").strip().lower()

    if response in ['n', 'no']:
        logger.warning("Generation cancelled by user.")
        print()
        return

    if response and response not in ['y', 'yes', '']:
        logger.warning(f"Invalid response '{response}' - treating as 'no'")
        logger.warning("Generation cancelled.")
        print()
        return
    
    logger.success("Starting generation...")
    print()
    
    # ============================================================
    # Initialize backends
    # ============================================================
    
    backends = {}

    if cloud_transitions:
        backends['cloud'] = CloudBackend(config)

    if local_transitions:
        backends['local'] = LocalBackend(config)

    if linux_transitions:
        backends['linux'] = LinuxBackend(config)

    if atlascloud_transitions:
        backends['atlascloud'] = AtlasCloudVideoBackend(config)
    
    # ============================================================
    # GENERATE TRANSITIONS — segment-level isolation
    # Failure in a segment skips remaining transitions in that segment
    # but continues with the next segment (ujęcie) independently.
    # ============================================================

    results = []
    chain_frame_cache = {}   # {filename: last_frame_path}

    # ── Resolve chain dependencies (once, before generation) ─────────
    chains_info: dict = {}
    for trans in to_generate:
        to_config_pre = trans['config'].get('to_config', {})
        if chain_handler.is_chain_file(to_config_pre):
            chain_prefix_pre = to_config_pre['_chain_prefix']
            if chain_prefix_pre not in chains_info:
                total_steps_pre = to_config_pre['_chain_total']
                tasks_pre = chain_handler.resolve_dependencies(
                    chain_prefix_pre, total_steps_pre
                )
                chains_info[chain_prefix_pre] = {
                    'total': total_steps_pre,
                    'tasks': tasks_pre,
                }
                if tasks_pre:
                    logger.info(
                        f"Chain '{chain_prefix_pre}': "
                        f"{len(tasks_pre)} step(s) need generation"
                    )

    # ── Group to_generate by segment ─────────────────────────────────
    seg_groups: dict[int, list] = {}
    for trans in to_generate:
        sidx = trans['config'].get('_segment_idx', 0)
        seg_groups.setdefault(sidx, []).append(trans)

    total_segs = len(parser.segments)

    for seg_idx in sorted(seg_groups.keys()):
        seg_items = seg_groups[seg_idx]

        if total_segs > 1:
            logger.section(
                f"Ujęcie {seg_idx + 1}/{total_segs} "
                f"({len(seg_items)} tranzycji)"
            )

        _segment_done = False  # set True after first failure → skip rest

        for i, trans in enumerate(seg_items, 1):
            trans_config = trans['config']
            backend_type = trans_config['backend']

            from_file   = trans_config['from_file']
            to_file     = trans_config['to_file']
            from_config = trans_config.get('from_config', {})
            to_config   = trans_config.get('to_config', {})

            # ── Segment already failed — skip remaining items ─────────
            if _segment_done:
                logger.info(f"  ⏭ {trans['name']}: pomijam (ujęcie przerwane)")
                results.append({'name': trans['name'], 'backend': backend_type,
                                'success': False, 'is_chain': chain_handler.is_chain_file(to_config),
                                'skipped': True})
                continue

            # ── Talk clip generation ──────────────────────────────────
            if to_config.get('_is_talk'):
                talk_dest = talks_folder / to_file

                if talk_dest.exists() and config.get('skip_existed', True):
                    _rel = str(Path('transitions') / 'talks' / to_file)
                    extractor.extract_end_frame(_rel, target_width, target_height)
                    results.append({'name': to_file, 'backend': backend_type,
                                    'success': True, 'is_chain': False})
                    continue

                if not _gen_fn:
                    logger.error(f"  🎙️  {to_file}: talk service unavailable")
                    results.append({'name': to_file, 'backend': backend_type,
                                    'success': False, 'is_chain': False})
                    continue

                # Source frame = end-frame of previous item
                if chain_handler.is_chain_file(from_config):
                    _talk_src = chain_frame_cache.get(from_file)
                    if not _talk_src:
                        _cv = chain_handler.get_chain_output_path(from_file)
                        if _cv.exists():
                            _talk_src = chain_handler.extract_last_frame(
                                _cv, target_width, target_height)
                            if _talk_src:
                                chain_frame_cache[from_file] = _talk_src
                else:
                    # Prefer _real.png (actual last frame of preceding transition)
                    # over static _end.png (source image) to avoid visual jump.
                    _real = _real_frame_path(Path(from_file).stem)
                    if not _real.exists():
                        # Check if a chain step targeted from_file as its end-target.
                        # In chain→image→talk sequences the chain's last step should
                        # "reach" the static image, so the talk clip must start from
                        # the chain's actual last frame (not the static source image).
                        _chain_targeting = None
                        for _p in pairs:
                            _ptc = _p.get('to_config', {})
                            if (_ptc.get('_is_chain')
                                    and _ptc.get('_chain_end_target') == from_file
                                    and _ptc.get('_chain_step') == _ptc.get('_chain_total')):
                                _chain_targeting = _p
                                break
                        if _chain_targeting:
                            _ct_file = _chain_targeting['to_file']
                            _talk_src = chain_frame_cache.get(_ct_file)
                            if not _talk_src:
                                _ct_vid = chain_handler.get_chain_output_path(_ct_file)
                                if _ct_vid.exists():
                                    _talk_src = chain_handler.extract_last_frame(
                                        _ct_vid, target_width, target_height)
                                    if _talk_src:
                                        chain_frame_cache[_ct_file] = _talk_src
                                        logger.info(
                                            f"  💾 Extracted last frame of chain "
                                            f"'{_ct_file}' for talk source")
                            if _talk_src:
                                # Also persist as _real.png so next runs skip extraction
                                _extracted = extractor.extract_last_frame_to(
                                    chain_handler.get_chain_output_path(_ct_file),
                                    target_width, target_height, _real)
                                if _extracted:
                                    logger.info(
                                        f"  💾 {Path(from_file).stem}_real.png "
                                        f"(from chain end-target)")
                            else:
                                logger.info(
                                    f"  ℹ️  Chain video for '{_ct_file}' not ready — "
                                    f"używam static end frame dla {from_file}")
                                _talk_src = _frame_path(Path(from_file).stem, 'end')
                        else:
                            logger.info(
                                f"  ℹ️  Brak _real.png dla {from_file} — używam static end frame")
                            _talk_src = _frame_path(Path(from_file).stem, 'end')
                    else:
                        _talk_src = _real

                if not _talk_src or not Path(_talk_src).exists():
                    logger.error(f"  ❌ {to_file}: brak source frame — pomijam")
                    results.append({'name': to_file, 'backend': backend_type,
                                    'success': False, 'is_chain': False})
                    _segment_done = True
                    continue

                # Build audio entries
                _talk_cfg   = to_config
                _def_pos    = str(_talk_cfg.get('pos', '') or '')
                _def_neg    = str(_talk_cfg.get('neg', '') or '')
                _raw_audio  = _talk_cfg.get('audio', '')
                _audio_list = _raw_audio if isinstance(_raw_audio, list) else [_raw_audio]

                _audio_entries = []
                _audio_ok = True
                for _a in _audio_list:
                    if isinstance(_a, dict):
                        _af  = _a.get('file', '') or _a.get('audio', '')
                        _ap2 = _a.get('pos', _def_pos) or _def_pos
                        _an2 = _a.get('neg', _def_neg) or _def_neg
                    else:
                        _af = str(_a)
                        _ap2, _an2 = _def_pos, _def_neg
                    _apath = project_folder / _af
                    if not _apath.exists():
                        logger.error(f"  ✗ {to_file}: audio not found: {_af}")
                        _audio_ok = False
                        break
                    _audio_entries.append({'path': _apath, 'pos': _ap2, 'neg': _an2})

                if not _audio_ok or not _audio_entries:
                    results.append({'name': to_file, 'backend': backend_type,
                                    'success': False, 'is_chain': False})
                    _segment_done = True
                    continue

                _tw = int(_talk_cfg.get('width',  480))
                _th = int(_talk_cfg.get('height', 832))
                logger.section(
                    f"🎙️  Talk {i}/{len(seg_items)}: {to_file}")
                logger.info(f"  source : {Path(_talk_src).name}")
                logger.info(f"  audio  : {[e['path'].name for e in _audio_entries]}")
                logger.info(f"  size   : {_tw}x{_th}")

                _t_success = _gen_fn(
                    comfyui_url=_talk_url,
                    linux_input_dir=_linux_input,
                    linux_output_dir=_linux_output,
                    source_image=Path(_talk_src),
                    audio_entries=_audio_entries,
                    dest_path=talk_dest,
                    width=_tw,
                    height=_th,
                    log_fn=lambda msg: logger.info(f"  {msg}"),
                )

                if not _t_success:
                    # Backend failure (OOM, timeout, etc.) → soft-fail so retry
                    # loop tries again after other items (model may be freed)
                    logger.error(f"  ❌ {to_file}: backend failed — pomijam")
                    results.append({'name': to_file, 'backend': backend_type,
                                    'success': False, 'is_chain': False})
                    _segment_done = True
                    continue

                if _t_success:
                    # Upscale to force_resolution
                    _force_res = config.get('force_resolution')
                    if (_force_res and isinstance(_force_res, (list, tuple))
                            and len(_force_res) == 2):
                        _fw, _fh = int(_force_res[0]), int(_force_res[1])
                        if (_tw, _th) != (_fw, _fh):
                            logger.info(f"  upscaling {_tw}x{_th} -> {_fw}x{_fh} ...")
                            if _upscale_video_inplace(talk_dest, _fw, _fh):
                                logger.info(f"  upscaled")
                            else:
                                logger.warning(f"  upscale failed")
                    # Extract end-frame for downstream items
                    _rel = str(Path('transitions') / 'talks' / to_file)
                    _ef  = extractor.extract_end_frame(_rel, target_width, target_height)
                    if _ef and _ef.exists():
                        logger.info(f"  end-frame -> {_ef.name}")
                    _smb = talk_dest.stat().st_size / (1024 * 1024)
                    logger.success(f"  {to_file} ({_smb:.1f} MB)")
                else:
                    logger.error(f"  {to_file}: generation failed")

                results.append({'name': to_file, 'backend': backend_type,
                                'success': _t_success, 'is_chain': False})
                continue

            # ── Chain file detection ──────────────────────────────────
            is_chain_step = chain_handler.is_chain_file(to_config)

            if is_chain_step:
                chain_prefix = to_config['_chain_prefix']
                chain_step   = to_config['_chain_step']
                chain_total  = to_config['_chain_total']

                chain_tasks     = chains_info.get(chain_prefix, {}).get('tasks', [])
                needs_generation = any(
                    task['step'] == chain_step for task in chain_tasks
                )

                if not needs_generation:
                    logger.info(
                        f"⛓️  Chain step {chain_step}/{chain_total} "
                        f"({to_file}) already exists - skipping"
                    )
                    continue

                task = next(
                    (t for t in chain_tasks if t['step'] == chain_step), None
                )

                if task and task.get('depends_on'):
                    dep_step = task['depends_on']
                    dep_file = f"{chain_prefix}_{dep_step:03d}.mp4"

                    if dep_file not in chain_frame_cache:
                        logger.error(
                            f"❌ Chain dep {dep_file} nie wygenerowany — pomijam {to_file}"
                        )
                        results.append({'name': trans['name'], 'backend': backend_type,
                                        'success': False, 'is_chain': True})
                        _segment_done = True
                        continue

            # ── Determine start frame ─────────────────────────────────
            if chain_handler.is_chain_file(from_config):
                start_frame = chain_frame_cache.get(from_file)

                if not start_frame:
                    chain_video_path = chain_handler.get_chain_output_path(from_file)
                    if chain_video_path.exists():
                        start_frame = chain_handler.extract_last_frame(
                            chain_video_path,
                            width=target_width,
                            height=target_height,
                        )
                        if start_frame:
                            chain_frame_cache[from_file] = start_frame

                if not start_frame:
                    logger.error(
                        f"❌ {trans['name']}: brak start frame z chain {from_file} — pomijam"
                    )
                    results.append({'name': trans['name'], 'backend': backend_type,
                                    'success': False, 'is_chain': is_chain_step})
                    _segment_done = True
                    continue
            else:
                # Normal file (image or video incl. talk clip).
                # Prefer _real.png (actual last frame of the transition that
                # reached this file) over _end.png (static source image).
                # This eliminates the visual jump caused by WAN not reaching
                # the target end frame exactly.
                # Guard: only use _real.png if from_file is actually the target
                # of some transition in the current run. If it's a section start
                # (no preceding transition ends here), a stale _real.png from a
                # previous run with different config must not be used.
                _real = _real_frame_path(Path(from_file).stem)
                _has_prev_transition = (
                    any(p['to_file'] == from_file for p in pairs)
                    # flow_parser marks files that immediately follow a talk tile
                    # (_is_talk pairs are not created so the normal check misses them)
                    or from_config.get('_preceded_by_talk', False)
                )
                if _real.exists() and _has_prev_transition:
                    start_frame = _real
                    logger.info(f"  🎯 {Path(from_file).stem}: using _real.png as start frame")
                else:
                    start_frame = _frame_path(Path(from_file).stem, 'end')
                    if _real.exists() and not _has_prev_transition:
                        logger.info(f"  ℹ️  {Path(from_file).stem}: ignoring stale _real.png (section start — no preceding transition)")
                    else:
                        logger.info(f"  ℹ️  {Path(from_file).stem}: no _real.png — using static end frame")
                if not start_frame.exists():
                    logger.error(
                        f"❌ {trans['name']}: brak start frame ({from_file}) — pomijam"
                    )
                    results.append({'name': trans['name'], 'backend': backend_type,
                                    'success': False, 'is_chain': is_chain_step})
                    _segment_done = True
                    continue

            # ── Determine end frame ───────────────────────────────────
            if is_chain_step:
                task = next(
                    (t for t in chain_tasks if t['step'] == chain_step), None
                )

                if task and task['mode'] == 'i2v2i':
                    next_file       = task['end_source']
                    next_video_path = chain_handler.get_chain_output_path(next_file)

                    end_frame = chain_handler.extract_first_frame(
                        next_video_path,
                        width=target_width,
                        height=target_height,
                    )

                    if not end_frame:
                        logger.error(
                            f"❌ {trans['name']}: brak gap-fill source {next_file} — pomijam"
                        )
                        results.append({'name': trans['name'], 'backend': backend_type,
                                        'success': False, 'is_chain': True})
                        _segment_done = True
                        continue
                else:
                    # I2V mode — but check if flow marked an end-target image
                    # (_chain_end_target set on last chain step by flow_parser)
                    chain_end_target = to_config.get('_chain_end_target')
                    if chain_end_target:
                        _et_frame = _frame_path(Path(chain_end_target).stem, 'start')
                        if _et_frame.exists():
                            end_frame = _et_frame
                            logger.info(
                                f"⛓️  Using end-target frame: {_et_frame.name}"
                            )
                        else:
                            logger.warning(
                                f"⛓️  End-target frame not ready "
                                f"({chain_end_target}) — generating I2V"
                            )
                            end_frame = None
                    else:
                        end_frame = None

                output_path = chain_handler.get_chain_output_path(to_file)

            else:
                end_frame   = _frame_path(Path(to_file).stem, 'start')
                output_path = transitions_folder / trans['name']

            # ── Generate ──────────────────────────────────────────────
            if is_chain_step:
                mode_str = task['mode'].upper() if task else 'I2V'
                logger.section(
                    f"⛓️  Chain Step {chain_step}/{chain_total}: "
                    f"{to_file} ({mode_str}, {backend_type.upper()})"
                )
            else:
                _gc_label = f" ×{_gc(trans)}" if _gc(trans) > 1 else ""
                logger.section(
                    f"Transition {i}/{len(seg_items)}: "
                    f"{trans['name']} ({backend_type.upper()}{_gc_label})"
                )

            # ── Generation summary ────────────────────────────────────
            _sf_name = start_frame.name if start_frame else 'None'
            _sf_tag  = (' 🎯 real' if '_real' in _sf_name
                        else ' (static)' if '_end' in _sf_name
                        else '')
            _ef_name = end_frame.name if end_frame else 'I2V'
            logger.info(f"  start : {_sf_name}{_sf_tag}")
            logger.info(f"  end   : {_ef_name}")
            logger.info(f"  output: {output_path.name}")
            logger.info(
                f"  params: {trans_config['duration']}s · "
                f"{trans_config['fps']}fps · "
                f"steps={trans_config['steps']} · "
                f"cfg={trans_config['cfg']}"
            )
            _pw = trans_config.get('width') or target_width
            _ph = trans_config.get('height') or target_height
            logger.info(f"  size  : {_pw}x{_ph}")

            backend = backends[backend_type]

            # Guard: duration=0 would produce 1 frame and waste ~5min of GPU time.
            # Fail immediately with a clear error so the user can fix the YAML.
            if not trans_config['duration']:
                logger.error(
                    f"  ❌ {trans['name']}: duration=0 — ustaw duration > 0 "
                    f"dla pliku '{from_file}' w YAML i uruchom ponownie."
                )
                results.append({'name': trans['name'], 'backend': backend_type,
                                'success': False, 'is_chain': is_chain_step})
                continue

            # Resolve use_lightning: tile config → LIGHTNING_OVERRIDE env var → default True
            _use_lightning = trans_config.get('use_lightning')
            _lo = os.environ.get('LIGHTNING_OVERRIDE', '').strip()
            if _lo:
                _use_lightning = (_lo == '1')
            if _use_lightning is None:
                _use_lightning = True

            _gt_kwargs = dict(
                start_frame=start_frame,
                end_frame=end_frame,
                output_path=output_path,
                duration=trans_config['duration'],
                fps=trans_config['fps'],
                steps=trans_config['steps'],
                cfg=trans_config['cfg'],
                seed=trans_config['seed'],
                positive_prompt=trans_config['positive_prompt'],
                negative_prompt=trans_config['negative_prompt'],
                width=trans_config.get('width') or target_width,
                height=trans_config.get('height') or target_height,
                blocks_to_swap=trans_config.get('blocks_to_swap'),
                frame_interpolation=trans_config.get('frame_interpolation'),
                lora_name=trans_config.get('lora_name'),
                lora_strength=trans_config.get('lora_strength'),
                lora_high=trans_config.get('lora_high'),
                lora_low=trans_config.get('lora_low'),
                audio_prompt=trans_config.get('audio_prompt', ''),
                audio_negative_prompt=trans_config.get('audio_negative_prompt', ''),
                use_lightning=_use_lightning,
            )
            # Pass AtlasCloud-specific per-item overrides (ignored by other backends)
            if backend_type == 'atlascloud':
                _ac_res = trans_config.get('atlascloud_resolution')
                _ac_pe  = trans_config.get('atlascloud_prompt_extend')
                if _ac_res is not None:
                    backend.config['atlascloud_resolution']    = _ac_res
                if _ac_pe is not None:
                    backend.config['atlascloud_prompt_extend'] = _ac_pe

            gen_count = max(1, int(trans_config.get('generate_count') or 1))
            success = False
            for _gen_i in range(gen_count):
                if gen_count > 1:
                    logger.info(f"  🎲 Generacja {_gen_i + 1}/{gen_count}")
                # Archive the previous result before each re-run (not before the first)
                if _gen_i > 0 and output_path.exists():
                    _ts   = datetime.now().strftime('%y%m%d%H%M%S')
                    _arch = output_path.with_name(
                        f"{output_path.stem}_ver{_ts}{output_path.suffix}"
                    )
                    shutil.move(str(output_path), str(_arch))
                    logger.info(f"  📦 {output_path.name} → {_arch.name}")
                success = backend.generate_transition(**_gt_kwargs)
                if not success:
                    logger.error(f"  ❌ generacja {_gen_i + 1}/{gen_count} nie powiodła się")
                    break
            if gen_count > 1 and success:
                print(f"[VERSIONS_READY]{trans['name']}", flush=True)

            # ── Post-generation: cache chain end-frame ────────────────
            if success and is_chain_step:
                logger.info("Extracting last frame for next chain step...")
                last_frame = chain_handler.extract_last_frame(
                    output_path,
                    width=target_width,
                    height=target_height,
                )
                if last_frame:
                    chain_frame_cache[to_file] = last_frame
                else:
                    logger.error("⚠️  Failed to extract last frame - chain may be broken!")

                # If this is the last chain step and it has an end-target image,
                # write the chain's real last frame as {target}_real.png.
                # This lets the next item anchored to that image (e.g. a talk clip)
                # start from where the chain actually ended instead of the static
                # source image — eliminating the visual jump at the boundary.
                _end_target = to_config.get('_chain_end_target')
                _is_last    = (to_config.get('_chain_step') == to_config.get('_chain_total'))
                if _end_target and _is_last and last_frame:
                    _target_real = _real_frame_path(Path(_end_target).stem)
                    _extracted = extractor.extract_last_frame_to(
                        output_path, target_width, target_height, _target_real
                    )
                    if _extracted:
                        logger.info(
                            f"  💾 {Path(_end_target).stem}_real.png "
                            f"(chain end-target — eliminates jump to next talk/item)"
                        )

            # ── Post-generation: save _real.png for normal transitions ─
            # _real.png = actual last frame of the generated video.
            # The next clip (transition or talk) will use this instead of
            # the static _end.png so there is no jump at the boundary.
            if success and not is_chain_step and not to_config.get('_is_talk'):
                _real_out = _real_frame_path(Path(to_file).stem)
                _extracted = extractor.extract_last_frame_to(
                    output_path, target_width, target_height, _real_out
                )
                if _extracted:
                    logger.info(f"  💾 _real.png saved for {to_file}")
                else:
                    logger.warning(f"  ⚠️  Failed to save _real.png for {to_file}")

            if success:
                results.append({
                    'name':     trans['name'],
                    'backend':  backend_type,
                    'success':  True,
                    'is_chain': is_chain_step,
                })
            else:
                logger.error(
                    f"  ❌ {trans['name']}: backend failed — pomijam"
                )
                results.append({'name': trans['name'], 'backend': backend_type,
                                'success': False, 'is_chain': is_chain_step})
                _segment_done = True

        if _segment_done:
            seg_failed_count = sum(1 for r in results if not r['success'] and not r.get('skipped'))
            seg_skip_count   = sum(1 for r in results[-len(seg_items):] if r.get('skipped'))
            if seg_skip_count:
                logger.warning(
                    f"  ⏭ Ujęcie {seg_idx + 1}: {seg_skip_count} tranzycji pominiętych po błędzie"
                )
    
    # ============================================================
    # SUMMARY
    # ============================================================
    
    logger.header("GENERATION SUMMARY")
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    logger.info(f"Total: {len(results)}")
    logger.success(f"Successful: {len(successful)}")
    
    if failed:
        logger.error(f"Failed: {len(failed)}")
        for r in failed:
            logger.error(f"  • {r['name']} ({r['backend']})")
    else:
        logger.success("\n🎉 All transitions generated successfully!")
    
    logger.info("\n" + "="*70)
    logger.info("Batch generation complete!")
    logger.info("="*70)


if __name__ == "__main__":
    print("This module should be imported, not run directly.")
    print("Use RUN_*.py scripts in the RUNS/ folder.")