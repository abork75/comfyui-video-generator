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

from helpers.chain_handler import ChainHandler

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
                
                # Mark as normal I2V2I (not chain I2V)
                'is_i2v_mode': False,
            }
            
        else:
            # === NORMAL TRANSITION or CHAIN STEP ===
            
            # Determine backend
            backend = from_config.get('backend') or to_config.get('backend') or default_backend
            
            trans_config = {
                'from_file': from_file,
                'to_file': to_file,
                'from_config': from_config,
                'to_config': to_config,
                'backend': backend,
                # Use FROM config first, fallback to TO, then default
                'duration': from_config.get('duration', to_config.get('duration', default_duration)),
                'fps': from_config.get('fps', to_config.get('fps', default_fps)),
                'steps': from_config.get('steps', to_config.get('steps', default_steps)),
                'cfg': from_config.get('cfg', to_config.get('cfg', default_cfg)),
                'seed': from_config.get('seed', to_config.get('seed', default_seed)),
                'positive_prompt': from_config.get('pos', to_config.get('pos', default_positive_prompt)),
                'negative_prompt': from_config.get('neg', to_config.get('neg', default_negative_prompt)),
                
                # I2V mode if to_file is chain
                'is_i2v_mode': to_config.get('_is_chain', False),
            }

        if DEBUG_LOG:
            if is_chain_to_next_transition:
                print(f"   ⛓️→🎬 Chain-to-next transition detected!")
                print(f"   Using transition_to_next prompt: {trans_config['positive_prompt'][:60]}...")
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
    
    # Filter out chain files for AR validation
    non_chain_files = [f.filename for f in parser.get_all_files() if not f.config.get('_is_chain')]
    
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
    
    existing_transitions = []
    missing_transitions = []
    
    for pair_config in pairs:
        trans_name = f"{Path(pair_config['from_file']).stem}_{Path(pair_config['to_file']).stem}_transition.mp4"
        
        # Check if it's a chain transition (output in chains/ folder)
        to_config = pair_config['to_config']
        
        if to_config.get('_is_chain'):
            # Chain file - check chains folder
            chain_handler_temp = ChainHandler(project_folder)
            trans_path = chain_handler_temp.get_chain_output_path(pair_config['to_file'])
        else:
            # Normal transition
            trans_path = transitions_folder / trans_name
        
        if trans_path.exists():
            size_mb = trans_path.stat().st_size / (1024 * 1024)
            existing_transitions.append({
                'name': trans_name,
                'size': size_mb,
                'config': pair_config
            })
        else:
            missing_transitions.append({
                'name': trans_name,
                'config': pair_config
            })
    
    logger.section("Transition Status")
    
    if existing_transitions:
        logger.info(f"\n✓ EXISTING ({len(existing_transitions)}):")
        for t in existing_transitions:
            logger.info(f"  • {t['name']} ({t['size']:.1f} MB)")
    
    if missing_transitions:
        logger.info(f"\n✗ MISSING ({len(missing_transitions)}):")
        for t in missing_transitions:
            logger.info(f"  • {t['name']}")
    
    logger.info(f"\nTotal: {len(pairs)} transitions")
    logger.info(f"Existing: {len(existing_transitions)}")
    logger.info(f"Missing: {len(missing_transitions)}")
    
    if not missing_transitions:
        logger.success("\nAll transitions already exist! Nothing to do.")
        return
    
    # Check skip_existed flag
    if config.get('skip_existed', True):
        logger.info(f"\nSkipping {len(existing_transitions)} existing transitions")
        to_generate = missing_transitions
    else:
        logger.warning("\nRegenerating ALL transitions (skip_existed=False)")
        to_generate = [{'name': f"{Path(p['from_file']).stem}_{Path(p['to_file']).stem}_transition.mp4", 'config': p} for p in pairs]
    
    # ============================================================
    # GENERATE TRANSITIONS (by backend)
    # ============================================================
    
    logger.header(f"GENERATING {len(to_generate)} TRANSITIONS")
    
    # Group by backend
    cloud_transitions = [t for t in to_generate if t['config']['backend'] == 'cloud']
    local_transitions = [t for t in to_generate if t['config']['backend'] == 'local']
    
    logger.section("Backend Distribution")
    logger.info(f"  Cloud: {len(cloud_transitions)}")
    logger.info(f"  Local: {len(local_transitions)}")
    print()
    
    # ============================================================
    # CONFIRMATION PROMPT
    # ============================================================
    
    logger.section("Ready to Generate")
    
    # Calculate estimates
    cloud_cost = len(cloud_transitions) * 0.10
    cloud_time = len(cloud_transitions) * 1.5
    local_time = len(local_transitions) * 4.0
    total_time = cloud_time + local_time
    
    logger.info(f"  Transitions: {len(to_generate)}")
    if cloud_transitions:
        logger.info(f"  Cloud: {len(cloud_transitions)} (est. ${cloud_cost:.2f}, ~{cloud_time:.0f}min)")
    if local_transitions:
        logger.info(f"  Local: {len(local_transitions)} (FREE, ~{local_time:.0f}min)")
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
    
    # ============================================================
    # Initialize Chain Handler
    # ============================================================
    
    chain_handler = ChainHandler(project_folder, logger=logger)
    
    # ============================================================
    # PRE-PROCESS CHAINS
    # ============================================================
    
    # Group chains and resolve dependencies
    chains_info = {}  # {chain_prefix: {'total': int, 'tasks': [...]}}
    chain_frame_cache = {}  # {filename: last_frame_path} - for sequential generation
    
    for trans in to_generate:
        to_config = trans['config'].get('to_config', {})
        
        if chain_handler.is_chain_file(to_config):
            chain_prefix = to_config['_chain_prefix']
            
            if chain_prefix not in chains_info:
                # First time seeing this chain - resolve dependencies
                total_steps = to_config['_chain_total']
                tasks = chain_handler.resolve_dependencies(chain_prefix, total_steps)
                
                chains_info[chain_prefix] = {
                    'total': total_steps,
                    'tasks': tasks
                }
                
                if tasks:
                    logger.info(f"Chain '{chain_prefix}': {len(tasks)} step(s) need generation")
    
    # ============================================================
    # GENERATE TRANSITIONS
    # ============================================================
    
    results = []
    
    for i, trans in enumerate(to_generate, 1):
        trans_config = trans['config']
        backend_type = trans_config['backend']
        
        from_file = trans_config['from_file']
        to_file = trans_config['to_file']
        
        from_config = trans_config.get('from_config', {})
        to_config = trans_config.get('to_config', {})
        
        # ============================================================
        # CHAIN FILE DETECTION
        # ============================================================
        
        is_chain_step = chain_handler.is_chain_file(to_config)
        
        if is_chain_step:
            chain_prefix = to_config['_chain_prefix']
            chain_step = to_config['_chain_step']
            chain_total = to_config['_chain_total']
            
            # Check if this step needs generation
            chain_tasks = chains_info.get(chain_prefix, {}).get('tasks', [])
            needs_generation = any(task['step'] == chain_step for task in chain_tasks)
            
            if not needs_generation:
                # Skip - already exists
                logger.info(f"⛓️  Chain step {chain_step}/{chain_total} ({to_file}) already exists - skipping")
                continue
            
            # Check dependencies
            task = next((t for t in chain_tasks if t['step'] == chain_step), None)
            
            if task and task.get('depends_on'):
                dep_step = task['depends_on']
                dep_file = f"{chain_prefix}_{dep_step:03d}.mp4"
                
                # Check if dependency was generated in this run
                if dep_file not in chain_frame_cache:
                    logger.error(f"⛓️  Dependency {dep_file} not found - cannot generate step {chain_step}")
                    continue
        
        # ============================================================
        # DETERMINE START/END FRAMES
        # ============================================================
        
        # --- START FRAME ---
        
        if chain_handler.is_chain_file(from_config):
            # Previous was chain step - use cached last frame
            start_frame = chain_frame_cache.get(from_file)
            
            if not start_frame:
                # Not in cache - extract from existing chain video
                chain_video_path = chain_handler.get_chain_output_path(from_file)
                if chain_video_path.exists():
                    start_frame = chain_handler.extract_last_frame(
                        chain_video_path,
                        width=target_width,
                        height=target_height
                    )
                    if start_frame:
                        chain_frame_cache[from_file] = start_frame
                
                if not start_frame:
                    logger.error(f"Cannot get start frame from chain file: {from_file}")
                    continue
        else:
            # Normal file - use extracted frame
            from_file_path = project_folder / from_file
            
            if from_file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                # Source is image
                start_frame = frames_folder / f"{Path(from_file).stem}_end.jpg"
            else:
                # Source is video
                start_frame = frames_folder / f"{Path(from_file).stem}_end.jpg"
        
        # --- END FRAME ---
        
        if is_chain_step:
            # This IS a chain step
            task = next((t for t in chain_tasks if t['step'] == chain_step), None)
            
            if task and task['mode'] == 'i2v2i':
                # Gap filling - extract first frame from next existing step
                next_file = task['end_source']
                next_video_path = chain_handler.get_chain_output_path(next_file)
                
                end_frame = chain_handler.extract_first_frame(
                    next_video_path,
                    width=target_width,
                    height=target_height
                )
                
                if not end_frame:
                    logger.error(f"Cannot extract first frame from {next_file} for gap filling")
                    continue
            else:
                # Normal I2V - no end frame
                end_frame = None
            
            # Output to chains folder
            output_path = chain_handler.get_chain_output_path(to_file)
        
        else:
            # Normal transition
            to_file_path = project_folder / to_file
            
            if to_file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                # Target is video
                end_frame = frames_folder / f"{Path(to_file).stem}_start.jpg"
            else:
                # Target is image
                end_frame = frames_folder / f"{Path(to_file).stem}_start.jpg"
            
            # Output to transitions folder
            output_path = transitions_folder / trans['name']
        
        # ============================================================
        # GENERATE
        # ============================================================
        
        if is_chain_step:
            mode_str = task['mode'].upper() if task else 'I2V'
            logger.section(f"⛓️  Chain Step {chain_step}/{chain_total}: {to_file} ({mode_str}, {backend_type.upper()})")
        else:
            logger.section(f"Transition {i}/{len(to_generate)}: {trans['name']} ({backend_type.upper()})")
        
        # Show frames
        logger.info(f"Start frame: {start_frame.name if start_frame else 'None'}")
        logger.info(f"End frame: {end_frame.name if end_frame else 'None (I2V)'}")
        logger.info(f"Output: {output_path.name}")
        
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
            width=target_width,
            height=target_height
        )
        
        # ============================================================
        # POST-GENERATION: Extract last frame (if chain step)
        # ============================================================
        
        if success and is_chain_step:
            # Extract last frame for next chain step
            logger.info("Extracting last frame for next chain step...")
            
            last_frame = chain_handler.extract_last_frame(
                output_path,
                width=target_width,
                height=target_height
            )
            
            if last_frame:
                # Cache for next step
                chain_frame_cache[to_file] = last_frame
            else:
                logger.error("⚠️  Failed to extract last frame - chain may be broken!")
        
        results.append({
            'name': trans['name'],
            'backend': backend_type,
            'success': success,
            'is_chain': is_chain_step
        })
    
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