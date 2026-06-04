# -*- coding: utf-8 -*-
"""
Batch Transition Generator - Orchestrator Mode
Unified system supporting multiple backends and workflow types
"""

import os
import sys
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
    
    # Defaults
    default_backend = config.get('default_backend', 'local')
    default_duration = config.get('default_duration', 16)
    default_fps = config.get('default_fps', 8)
    default_steps = config.get('default_steps', 25)
    default_cfg = config.get('default_cfg', 2.5)
    default_seed = config.get('default_seed', -1)
    default_positive_prompt = config.get('default_positive_prompt', '')
    default_negative_prompt = config.get('default_negative_prompt', '')
    default_blocks_to_swap      = config.get('default_blocks_to_swap', None)
    default_frame_interpolation = config.get('default_frame_interpolation', True)
    
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
    
    # Build pairs for processing (with metadata)
    pairs = []
#########################    
    for pair in transition_pairs:
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

                # Mark as normal I2V2I (not chain I2V)
                'is_i2v_mode': False,
            }
            
        else:
            # === NORMAL TRANSITION or CHAIN STEP ===
            
            # Determine backend
            backend = from_config.get('backend') or to_config.get('backend') or default_backend
            
            # ============================================================
            # ✅ FIX: Different priority for chain files vs normal transitions
            # ============================================================
            
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
                    'width': to_config.get('width', from_config.get('width', None)),
                    'height': to_config.get('height', from_config.get('height', None)),
                    'blocks_to_swap': to_config.get('blocks_to_swap', from_config.get('blocks_to_swap', default_blocks_to_swap)),
                    'frame_interpolation': to_config.get('frame_interpolation', from_config.get('frame_interpolation', default_frame_interpolation)),
                    'is_i2v_mode': True,  # Chain is always I2V
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
                    'width': from_config.get('width', to_config.get('width', None)),
                    'height': from_config.get('height', to_config.get('height', None)),
                    'blocks_to_swap': from_config.get('blocks_to_swap', to_config.get('blocks_to_swap', default_blocks_to_swap)),
                    'frame_interpolation': from_config.get('frame_interpolation', to_config.get('frame_interpolation', default_frame_interpolation)),
                    'is_i2v_mode': False,
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
        
        
        pairs.append(trans_config)
#############################
    
    if not pairs:
        logger.warning("No transitions to generate (check for breaks or single file)")
        return
    
    # ============================================================
    # VERIFY FILES
    # ============================================================
    
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
            talk_dest = project_folder / 'transitions' / flow_file.filename
            status = "✓ exists" if talk_dest.exists() else "⏳ generate via web UI"
            logger.info(f"[{i:02d}] 🎙️  {flow_file.filename} ({status})")
            continue
        
        file_path = project_folder / flow_file.filename
        
        if not file_path.exists():
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
    
    logger.success(f"Final resolution: {target_width}x{target_height}")
    
    # Extract frames (only for non-chain files)
    logger.section("Preparing frames")
    
    frames_folder = project_folder / 'frames'
    
    for i, flow_file in enumerate(parser.get_all_files(), 1):
        if flow_file.config.get('_is_chain'):
            continue  # Skip chain files - frames extracted during generation
        if flow_file.config.get('_is_talk'):
            # If talk clip already exists, extract its end-frame now so that
            # chain transitions anchoring to it can find the frame in pass 1
            # (without needing a retry).  Newly-generated talks get the same
            # treatment right after they are created further below.
            _talk_clip = project_folder / 'transitions' / flow_file.filename
            if _talk_clip.exists():
                _rel_talk = str(Path('transitions') / flow_file.filename)
                _ef = extractor.extract_end_frame(_rel_talk, target_width, target_height)
                _status = f"end-frame {'ok' if (_ef and _ef.exists()) else 'FAILED'}"
            else:
                _status = "not yet generated"
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
    
   
    # ============================================================
    # CHECK EXISTING TRANSITIONS
    # ============================================================
    
    logger.header("CHECKING EXISTING TRANSITIONS")
    
    transitions_folder = project_folder / 'transitions'
    transitions_folder.mkdir(exist_ok=True)
    
    # ✅ Initialize chain handler for validation
    chain_handler = ChainHandler(project_folder, logger=logger)
    
    existing_transitions = []
    missing_transitions = []
    
    # ✅ Build transition list from pairs
    all_transitions = []
    for pair_config in pairs:
        to_config = pair_config.get('to_config', {})
        
        # ✅ FIX: Use correct name for display
        if to_config.get('_is_chain', False):
            trans_name = pair_config['to_file']  # koniec_001.mp4
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
            # Target is chain - output goes to chains/
            output_path = chain_handler.get_chain_output_path(to_file)
        else:
            # Normal transition
            output_path = transitions_folder / trans_name
        
        # Check if exists
        if output_path.exists():
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

            if is_to_chain:
                file_path = chain_handler.get_chain_output_path(trans['to_file'])
            else:
                file_path = transitions_folder / trans['name']

            size_mb = file_path.stat().st_size / (1024 * 1024)
            logger.info(f"    • {trans['name']} ({size_mb:.1f} MB)")

    if missing_transitions:
        logger.warning(f"\n⚠ MISSING ({len(missing_transitions)}):")
        for trans in missing_transitions:
            logger.info(f"    • {trans['name']}")

    # ============================================================
    # TALK clips — reported separately (generated via web UI)
    # ============================================================
    talk_files    = [f for f in parser.get_all_files() if f.config.get('_is_talk')]
    talk_existing = []
    talk_missing  = []
    if talk_files:
        for tf in talk_files:
            talk_path = transitions_folder / tf.filename
            if talk_path.exists():
                size_mb = talk_path.stat().st_size / (1024 * 1024)
                talk_existing.append((tf.filename, size_mb))
            else:
                talk_missing.append(tf.filename)

        logger.info(f"\n🎙️  TALK clips ({len(talk_files)} total):")
        for name, size_mb in talk_existing:
            logger.info(f"    ✓ {name} ({size_mb:.1f} MB)")
        for name in talk_missing:
            logger.warning(f"    ⚠ {name}  ← generate via web UI (Talk button)")

    logger.info(f"\nTotal: {len(all_transitions)} transitions")
    logger.info(f"  Existing: {len(existing_transitions)}")
    logger.info(f"  Missing: {len(missing_transitions)}")
    if talk_files:
        logger.info(f"  Talk clips: {len(talk_existing)}/{len(talk_files)} ready")

    # ============================================================
    # GENERATE MISSING TALK CLIPS
    # ============================================================
    talk_generated = 0
    talk_failed    = 0

    if talk_missing:
        logger.header("TALK CLIP GENERATION")

        # Load talk service + settings (app context optional — settings may
        # not be available when running the script standalone; in that case
        # we skip auto-generation and remind the user to use the web UI).
        _gen_fn = None
        try:
            from app.services.talk_service import generate_talk_clip_sync
            from app.core.config import settings as _app_settings
            _linux_input  = Path(_app_settings.comfyui_linux_input_dir)
            _linux_output = Path(_app_settings.comfyui_linux_output_dir)
            _talk_url     = _app_settings.comfyui_url
            _gen_fn = generate_talk_clip_sync
        except Exception as _e:
            logger.warning(f"⚠ Could not load talk service settings ({_e}).")
            logger.warning("  Generate talk clips manually via the web UI Talk button.")

        # ── Confirmation prompt (mirrors standard-transition prompt) ────────
        if _gen_fn:
            logger.section("Ready to Generate Talk Clips")
            logger.info(f"  Talk clips missing: {len(talk_missing)}")
            for _tn in talk_missing:
                logger.info(f"    • {_tn}")
            from colorama import Fore, Style
            _talk_resp = input(
                f"{Fore.YELLOW}Generate {len(talk_missing)} talk clip(s)? [Y/n]: "
                f"{Style.RESET_ALL}"
            ).strip().lower()
            if _talk_resp in ('n', 'no'):
                logger.warning("Talk clip generation skipped by user.")
                _gen_fn = None   # disable generation below
            else:
                logger.success("Starting talk clip generation...")
            print()

        if _gen_fn:
            # Build lookup: talk filename → FlowFile
            talk_file_map = {tf.filename: tf for tf in talk_files}

            for talk_name in talk_missing:
                tf = talk_file_map.get(talk_name)
                if tf is None:
                    continue

                talk_cfg = tf.config
                source_image_name = talk_cfg.get('_source_image')
                if not source_image_name:
                    logger.warning(f"  ⚠ {talk_name}: no source image in flow, skipping")
                    talk_failed += 1
                    continue

                # Width/height needed early for on-the-fly frame extraction
                width  = int(talk_cfg.get("width",  480))
                height = int(talk_cfg.get("height", 832))

                # Resolve source image — if previous file is a video, use the
                # extracted end-frame JPEG.  Chain-step videos live in
                # transitions/chains/ and may not have a pre-extracted frame;
                # extract on-the-fly with FrameExtractor (same approach as chain).
                _vid_exts = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
                if Path(source_image_name).suffix.lower() in _vid_exts:
                    frame_path = project_folder / 'frames' / f"{Path(source_image_name).stem}_end.jpg"
                    if frame_path.exists():
                        source_path = frame_path
                    else:
                        # Frame missing — locate the source video then extract.
                        video_src = project_folder / source_image_name
                        if not video_src.exists():
                            video_src = project_folder / 'transitions' / 'chains' / source_image_name
                        if video_src.exists():
                            try:
                                rel = str(video_src.relative_to(project_folder))
                            except ValueError:
                                rel = video_src.name
                            from utils.frame_extractor import FrameExtractor
                            _fe = FrameExtractor(project_folder=project_folder, image_quality=95)
                            extracted = _fe.extract_end_frame(rel, width, height)
                            source_path = extracted if (extracted and extracted.exists()) else None
                            if source_path:
                                logger.info(f"  📷 Wyekstrahowano klatkę: {source_path.name}")
                            else:
                                logger.error(f"  ✗ {talk_name}: nie udało się wyciągnąć klatki z: {source_image_name}")
                        else:
                            source_path = None
                else:
                    source_path = project_folder / source_image_name
                    if not source_path.exists():
                        chain_path = project_folder / 'transitions' / 'chains' / source_image_name
                        source_path = chain_path if chain_path.exists() else None

                if not source_path:
                    logger.error(f"  ✗ {talk_name}: source image not found: {source_image_name}")
                    talk_failed += 1
                    continue

                # Build per-segment audio entries
                default_pos = str(talk_cfg.get("pos", "") or "")
                default_neg = str(talk_cfg.get("neg", "") or "")
                raw_audio   = talk_cfg.get("audio", "")
                audio_list  = raw_audio if isinstance(raw_audio, list) else [raw_audio]

                audio_entries = []
                ok = True
                for a in audio_list:
                    if isinstance(a, dict):
                        fname   = a.get("file", "")
                        seg_pos = a.get("pos", default_pos) or default_pos
                        seg_neg = a.get("neg", default_neg) or default_neg
                    else:
                        fname   = str(a)
                        seg_pos = default_pos
                        seg_neg = default_neg
                    ap = project_folder / fname
                    if not ap.exists():
                        logger.error(f"  ✗ {talk_name}: audio not found: {fname}")
                        ok = False
                        break
                    audio_entries.append({"path": ap, "pos": seg_pos, "neg": seg_neg})

                if not ok or not audio_entries:
                    talk_failed += 1
                    continue

                dest   = transitions_folder / talk_name

                audio_names = [e["path"].name for e in audio_entries]
                logger.info(f"\n  🎙️  {talk_name}")
                logger.info(f"      source : {source_image_name}")
                logger.info(f"      audio  : {audio_names}")
                logger.info(f"      size   : {width}×{height}")

                success = _gen_fn(
                    comfyui_url=_talk_url,
                    linux_input_dir=_linux_input,
                    linux_output_dir=_linux_output,
                    source_image=source_path,
                    audio_entries=audio_entries,
                    dest_path=dest,
                    width=width,
                    height=height,
                    log_fn=lambda msg: logger.info(f"      {msg}"),
                )

                if success:
                    # ── Upscale to project force_resolution ──────────────────
                    _force_res = config.get('force_resolution')
                    if (
                        _force_res
                        and isinstance(_force_res, (list, tuple))
                        and len(_force_res) == 2
                    ):
                        _fw, _fh = int(_force_res[0]), int(_force_res[1])
                        _tw = int(talk_cfg.get("width", 480))
                        _th = int(talk_cfg.get("height", 832))
                        if (_tw, _th) != (_fw, _fh):
                            logger.info(
                                f"      ↑ upscaling {_tw}×{_th} → {_fw}×{_fh} ..."
                            )
                            if _upscale_video_inplace(dest, _fw, _fh):
                                logger.info(f"      ✓ upscaled to {_fw}×{_fh}")
                            else:
                                logger.warning(
                                    "      ⚠ upscale failed – keeping original resolution"
                                )

                    # ── Extract end-frame so chains/transitions can anchor ────
                    _rel_talk = str(Path("transitions") / talk_name)
                    _end_frame = extractor.extract_end_frame(
                        _rel_talk, target_width, target_height
                    )
                    if _end_frame and _end_frame.exists():
                        logger.info(f"      📷 end-frame → {_end_frame.name}")

                    size_mb = dest.stat().st_size / (1024 * 1024)
                    logger.success(f"  ✓ {talk_name} ({size_mb:.1f} MB)")
                    talk_generated += 1
                else:
                    logger.error(f"  ✗ {talk_name}: generation failed")
                    talk_failed += 1

        # Update talk summary counters
        talk_still_missing = len(talk_missing) - talk_generated

    if len(missing_transitions) == 0 and not config.get('skip_existed', True):
        logger.success(f"\n✓\nAll transitions already exist!")
    elif len(missing_transitions) == 0:
        still_pending = (len(talk_missing) if talk_files else 0) - talk_generated
        if still_pending > 0:
            logger.warning(f"\n⚠ Standard transitions complete — {still_pending} talk clip(s) still pending.")
        else:
            logger.success(f"\n✓\nAll transitions already exist! Nothing to do.")

        # ============================================================
        # ✅ KONIEC - jeśli SKIP_EXISTED=True i brak missing
        # ============================================================
        if config.get('skip_existed', True) and (talk_generated + talk_failed == len(talk_missing) if talk_files else True):
            return {
                'success': True,
                'total': len(all_transitions),
                'generated': talk_generated,
                'skipped': len(existing_transitions),
                'failed': talk_failed,
            }
    
    # Check skip_existed flag
    if config.get('skip_existed', True):
        logger.info(f"\nSkipping {len(existing_transitions)} existing transitions")
        to_generate = missing_transitions
    else:
        logger.warning("\nRegenerating ALL transitions (skip_existed=False)")
        to_generate = [{'name': f"{Path(p['from_file']).stem}_{Path(p['to_file']).stem}_transition.mp4", 'config': p} for p in pairs]

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
    
    logger.header(f"GENERATING {len(to_generate)} TRANSITIONS")
    
    # Group by backend
    cloud_transitions = [t for t in to_generate if t['config']['backend'] == 'cloud']
    local_transitions = [t for t in to_generate if t['config']['backend'] == 'local']
    linux_transitions = [t for t in to_generate if t['config']['backend'] == 'linux']

    logger.section("Backend Distribution")
    logger.info(f"  Cloud: {len(cloud_transitions)}")
    logger.info(f"  Local: {len(local_transitions)}")
    logger.info(f"  Linux: {len(linux_transitions)}")
    print()

    # ============================================================
    # CONFIRMATION PROMPT
    # ============================================================

    logger.section("Ready to Generate")

    # Calculate estimates
    cloud_cost = len(cloud_transitions) * 0.10
    cloud_time = len(cloud_transitions) * 1.5
    local_time = len(local_transitions) * 4.0
    linux_time = len(linux_transitions) * 4.0
    total_time = cloud_time + local_time + linux_time

    logger.info(f"  Transitions: {len(to_generate)}")
    if cloud_transitions:
        logger.info(f"  Cloud: {len(cloud_transitions)} (est. ${cloud_cost:.2f}, ~{cloud_time:.0f}min)")
    if local_transitions:
        logger.info(f"  Local: {len(local_transitions)} (FREE, ~{local_time:.0f}min)")
    if linux_transitions:
        logger.info(f"  Linux: {len(linux_transitions)} (FREE, ~{linux_time:.0f}min)")
    logger.info(f"  Total estimate: ${cloud_cost:.2f}, ~{total_time:.0f}min")
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
    
    # ============================================================
    # GENERATE TRANSITIONS — retry loop
    # Each pass generates what it can; items whose dependencies are
    # not yet satisfied (soft-fail) are retried in the next pass.
    # Two consecutive passes with the same set of failures → deadlock.
    # ============================================================

    results = []
    pending_transitions   = list(to_generate)
    chain_frame_cache     = {}   # {filename: last_frame_path} – persists across passes
    _last_soft_failed_names: set | None = None
    _pass_num = 0

    while pending_transitions:
        _pass_num += 1
        if _pass_num > 1:
            logger.section(
                f"🔄 Retry pass {_pass_num} "
                f"— {len(pending_transitions)} transition(s) still pending"
            )

        # ── Resolve chain dependencies for THIS pass ─────────────────
        chains_info: dict = {}
        for trans in pending_transitions:
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

        _soft_failed_this_pass: list = []

        for i, trans in enumerate(pending_transitions, 1):
            trans_config = trans['config']
            backend_type = trans_config['backend']

            from_file   = trans_config['from_file']
            to_file     = trans_config['to_file']
            from_config = trans_config.get('from_config', {})
            to_config   = trans_config.get('to_config', {})

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
                        logger.warning(
                            f"⏳ Chain dep {dep_file} not ready "
                            f"— will retry after other transitions"
                        )
                        _soft_failed_this_pass.append(trans)
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
                    logger.warning(
                        f"⏳ Start frame from chain {from_file} not ready "
                        f"— will retry"
                    )
                    _soft_failed_this_pass.append(trans)
                    continue
            else:
                # Normal file (image or video incl. talk clip)
                start_frame = frames_folder / f"{Path(from_file).stem}_end.jpg"
                if not start_frame.exists():
                    logger.warning(
                        f"⏳ Start frame missing for {trans['name']} "
                        f"(source: {from_file}) — will retry"
                    )
                    _soft_failed_this_pass.append(trans)
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
                        logger.warning(
                            f"⏳ Gap-fill source {next_file} not ready — will retry"
                        )
                        _soft_failed_this_pass.append(trans)
                        continue
                else:
                    # I2V mode — but check if flow marked an end-target image
                    # (_chain_end_target set on last chain step by flow_parser)
                    chain_end_target = to_config.get('_chain_end_target')
                    if chain_end_target:
                        _et_frame = frames_folder / f"{Path(chain_end_target).stem}_start.jpg"
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
                end_frame   = frames_folder / f"{Path(to_file).stem}_start.jpg"
                output_path = transitions_folder / trans['name']

            # ── Generate ──────────────────────────────────────────────
            if is_chain_step:
                mode_str = task['mode'].upper() if task else 'I2V'
                logger.section(
                    f"⛓️  Chain Step {chain_step}/{chain_total}: "
                    f"{to_file} ({mode_str}, {backend_type.upper()})"
                )
            else:
                logger.section(
                    f"Transition {i}/{len(pending_transitions)}: "
                    f"{trans['name']} ({backend_type.upper()})"
                )

            logger.info(f"Start frame: {start_frame.name if start_frame else 'None'}")
            logger.info(f"End frame: {end_frame.name if end_frame else 'None (I2V)'}")
            logger.info(f"Output: {output_path.name}")

            if DEBUG_LOG and is_chain_step:
                print(f"   ⛓️ Chain params:")
                print(f"      Duration: {trans_config['duration']}s")
                print(f"      FPS: {trans_config['fps']}")
                print(f"      Steps: {trans_config['steps']}")
                print(f"      CFG: {trans_config['cfg']}")
                print(f"      Prompt: {trans_config['positive_prompt'][:60]}...")

            backend = backends[backend_type]

            success = backend.generate_transition(
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
            )

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

            results.append({
                'name':     trans['name'],
                'backend':  backend_type,
                'success':  success,
                'is_chain': is_chain_step,
            })

        # ── Deadlock detection ────────────────────────────────────────
        _current_soft_names = {t['name'] for t in _soft_failed_this_pass}
        if _current_soft_names and _current_soft_names == _last_soft_failed_names:
            logger.error(
                f"\n❌ Deadlock: {len(_soft_failed_this_pass)} transition(s) "
                f"blocked by missing dependencies after {_pass_num} passes:"
            )
            for _t in _soft_failed_this_pass:
                logger.error(f"    • {_t['name']}")
                results.append({
                    'name':     _t['name'],
                    'backend':  _t['config']['backend'],
                    'success':  False,
                    'is_chain': chain_handler.is_chain_file(
                        _t['config'].get('to_config', {})
                    ),
                })
            break

        _last_soft_failed_names = _current_soft_names
        pending_transitions = _soft_failed_this_pass
    
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