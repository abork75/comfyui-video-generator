# -*- coding: utf-8 -*-
"""
Batch Upscale Engine - GAN Upscaling for video batches
Analogous to postprocess_engine.py structure

Modes:
- SOURCE: Upscale from project source (main, chain, transitions)
- NUMBERED_FLOW: Upscale from FLOW_* folders
- FULL_MOVIE: Upscale single full movie file

Structure support:
- main: videos in root folder OR main/ subfolder
- chain: videos in transitions/chains/ subfolder
- transitions: videos in transitions/ folder (excluding subfolders)
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from backends.utility_backend import UtilityBackend
from flow_parser import parse_flow

init(autoreset=True)

# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

def run_batch_upscale(config):
    """Main batch upscale entry point with INTERACTIVE source selection"""
    
    project_folder = Path(config['project_folder'])
    
    # Interactive source selection
    source_mode, source_path = select_source_interactive(project_folder)
    
    if source_mode is None:
        print(f"{Fore.RED}✗ No source selected{Style.RESET_ALL}")
        return False
    
    # Update config with selected mode
    config['batch_upscale']['source_mode'] = source_mode
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{'':20}BATCH UPSCALE")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Source mode: {source_mode}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    if source_mode == 'source':
        return run_upscale_source(config)
    elif source_mode == 'numbered_flow':
        return run_upscale_numbered_flow_direct(config, source_path)
    elif source_mode == 'full_movie':
        return run_upscale_full_movie(config, source_path)
    else:
        print(f"{Fore.RED}❌ Invalid source_mode: {source_mode}{Style.RESET_ALL}")
        return False


# ============================================================
# INTERACTIVE SOURCE SELECTION
# ============================================================

def select_source_interactive(project_folder):
    """Interactive source selection
    
    Detects:
    - main: root folder videos OR main/ subfolder
    - chain: transitions/chains/ subfolder
    - transitions: transitions/ folder (direct files only)
    - FLOW folders
    - Full movie files
    
    Returns:
        tuple: (source_mode, source_path)
            source_mode: 'source', 'numbered_flow', or 'full_movie'
            source_path: Path to source (or None for 'source' mode)
    """
    
    project_folder = Path(project_folder)
    final_outputs = project_folder / 'final_outputs'
    
    sources = []
    
    # Option 1: Project source files (main/chain/transitions)
    source_dirs = {}
    
    # Check for 'main' - root folder OR main/ subfolder
    main_folder = project_folder / 'main'
    if main_folder.exists() and main_folder.is_dir():
        source_dirs['main'] = main_folder
    else:
        # No 'main' folder - check root for videos
        root_videos = [f for f in project_folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']]
        if root_videos:
            source_dirs['main (root)'] = project_folder
    
    # Check for 'chain' - transitions/chains/ subfolder
    chains_folder = project_folder / 'transitions' / 'chains'
    if chains_folder.exists() and chains_folder.is_dir():
        source_dirs['chain'] = chains_folder
    
    # Check for 'transitions' - transitions/ direct files (no subfolders)
    transitions_folder = project_folder / 'transitions'
    if transitions_folder.exists() and transitions_folder.is_dir():
        source_dirs['transitions'] = transitions_folder
    
    # Count videos in each source
    source_video_count = 0
    source_details = []
    for category, path in source_dirs.items():
        if category == 'main (root)':
            # Root: only video files, skip images/folders
            count = len([f for f in path.iterdir() 
                        if f.is_file() and f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']])
        elif category == 'transitions':
            # Transitions: only direct files, skip subfolders (like chains/)
            count = len([f for f in path.iterdir() 
                        if f.is_file() and f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']])
        else:
            # Other: all videos in folder
            count = len([f for f in path.iterdir() 
                        if f.is_file() and f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']])
        
        if count > 0:
            source_video_count += count
            source_details.append(f"{category}: {count}")
    
    if source_video_count > 0:
        sources.append({
            'type': 'source',
            'label': f"Project source files ({', '.join(source_details)} videos)",
            'path': None
        })
    
    # Option 2: FLOW folders
    if final_outputs.exists():
        for folder in sorted(final_outputs.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if folder.is_dir() and folder.name.startswith('FLOW_') and not folder.name.endswith('_UPSCALED'):
                video_count = len([
                    f for f in folder.iterdir()
                    if f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']
                ])
                
                if video_count > 0:
                    sources.append({
                        'type': 'numbered_flow',
                        'label': f"FLOW folder: {folder.name} ({video_count} files)",
                        'path': folder
                    })
    
    # Option 3: Full movie files
    if final_outputs.exists():
        for file in sorted(final_outputs.glob("FULL_MOVIE_*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True):
            size_mb = file.stat().st_size / (1024 * 1024)
            sources.append({
                'type': 'full_movie',
                'label': f"Full movie: {file.name} ({size_mb:.1f} MB)",
                'path': file
            })
    
    # Show menu
    if not sources:
        print(f"\n{Fore.RED}❌ No video sources found!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Check:{Style.RESET_ALL}")
        print(f"  - Project has videos in root or main/ folder")
        print(f"  - Or transitions/ and transitions/chains/ folders")
        print(f"  - Or run numbered_flow postprocessing first")
        print(f"  - Or create full movie with concat postprocessing")
        return None, None
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{'':20}SELECT SOURCE")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Available sources:{Style.RESET_ALL}\n")
    
    for i, source in enumerate(sources, 1):
        print(f"  [{i}] {source['label']}")
    
    print(f"\n  [0] Cancel")
    
    while True:
        try:
            choice = input(f"\n{Fore.YELLOW}Select source [1-{len(sources)}]: {Style.RESET_ALL}").strip()
            
            if not choice:
                continue
            
            choice_num = int(choice)
            
            if choice_num == 0:
                return None, None
            
            if 1 <= choice_num <= len(sources):
                selected = sources[choice_num - 1]
                return selected['type'], selected['path']
            else:
                print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")
                
        except (ValueError, KeyboardInterrupt):
            return None, None


# ============================================================
# MODE 1: UPSCALE SOURCE FILES
# ============================================================

def run_upscale_source(config):
    """Upscale plików źródłowych (main, chain, transitions)
    
    Supports:
    - main: root folder videos OR main/ subfolder
    - chain: transitions/chains/ subfolder
    - transitions: transitions/ direct files (excluding subfolders)
    
    Output structure:
    final_outputs/source_UPSCALED/
        ├── main/
        ├── chain/
        └── transitions/
    """
    
    try:
        project_folder = Path(config['project_folder'])
        upscale_config = config['batch_upscale']
        
        # Output folder
        output_base = project_folder / 'final_outputs' / 'source_UPSCALED'
        output_base.mkdir(parents=True, exist_ok=True)
        
        print(f"{Fore.CYAN}📁 Output: {output_base.relative_to(project_folder)}{Style.RESET_ALL}\n")
        
        # Determine source directories with proper structure
        source_dirs = {}
        
        # 1. Check for 'main' - root OR main/ subfolder
        main_folder = project_folder / 'main'
        if main_folder.exists() and main_folder.is_dir():
            source_dirs['main'] = main_folder
        else:
            # No 'main' folder - check root for videos
            root_videos = [f for f in project_folder.iterdir() 
                          if f.is_file() and f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']]
            if root_videos:
                source_dirs['main'] = project_folder
        
        # 2. Check for 'chain' - transitions/chains/
        chains_folder = project_folder / 'transitions' / 'chains'
        if chains_folder.exists() and chains_folder.is_dir():
            source_dirs['chain'] = chains_folder
        
        # 3. Check for 'transitions' - transitions/ direct files
        transitions_folder = project_folder / 'transitions'
        if transitions_folder.exists() and transitions_folder.is_dir():
            source_dirs['transitions'] = transitions_folder
        
        # Initialize backend
        backend = _create_backend(upscale_config)
        
        total_upscaled = 0
        total_skipped = 0
        total_failed = 0
        
        # Upscale each category
        for category, source_dir in source_dirs.items():
            output_dir = output_base / category
            output_dir.mkdir(exist_ok=True)
            
            print(f"\n{Fore.YELLOW}{'─'*70}")
            print(f"📌 Category: {category.upper()}")
            print(f"   Source: {source_dir}")
            print(f"{'─'*70}{Style.RESET_ALL}\n")
            
            # Special handling based on category
            if category == 'main' and source_dir == project_folder:
                # Root folder - only videos, skip images/folders
                stats = _upscale_directory(
                    backend=backend,
                    source_dir=source_dir,
                    output_dir=output_dir,
                    upscale_config=upscale_config,
                    filter_files_only=True  # Skip subfolders/images
                )
            elif category == 'transitions':
                # Transitions - only direct files, skip subfolders like chains/
                stats = _upscale_directory(
                    backend=backend,
                    source_dir=source_dir,
                    output_dir=output_dir,
                    upscale_config=upscale_config,
                    filter_files_only=True  # Skip subfolders
                )
            else:
                # Other - normal processing
                stats = _upscale_directory(
                    backend=backend,
                    source_dir=source_dir,
                    output_dir=output_dir,
                    upscale_config=upscale_config
                )
            
            total_upscaled += stats['upscaled']
            total_skipped += stats['skipped']
            total_failed += stats['failed']
        
        # Summary
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{'':20}UPSCALE SUMMARY")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}✅ Upscaled: {total_upscaled}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⊘ Skipped: {total_skipped}{Style.RESET_ALL}")
        if total_failed > 0:
            print(f"{Fore.RED}❌ Failed: {total_failed}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Output: {output_base}{Style.RESET_ALL}\n")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error in upscale_source: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================
# MODE 2: UPSCALE NUMBERED FLOW (DIRECT)
# ============================================================

def run_upscale_numbered_flow_direct(config, flow_folder):
    """Upscale konkretnego FLOW folder (już wybranego przez interactive selection)
    
    Output structure:
    final_outputs/FLOW_{project}_{timestamp}_UPSCALED/
        ├── f0001_video_upscaled.mp4
        ├── f0002_video_upscaled.mp4
        └── ...
    """
    
    try:
        upscale_config = config['batch_upscale']
        flow_folder = Path(flow_folder)
        
        # Output folder
        flow_name = flow_folder.name
        output_folder = flow_folder.parent / f"{flow_name}_UPSCALED"
        output_folder.mkdir(exist_ok=True)
        
        print(f"{Fore.CYAN}📁 Source: {flow_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📁 Output: {output_folder.name}{Style.RESET_ALL}\n")
        
        # Initialize backend
        backend = _create_backend(upscale_config)
        
        # Upscale directory
        stats = _upscale_directory(
            backend=backend,
            source_dir=flow_folder,
            output_dir=output_folder,
            upscale_config=upscale_config,
            suffix='_upscaled'
        )
        
        # Summary
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{'':20}UPSCALE SUMMARY")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}✅ Upscaled: {stats['upscaled']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⊘ Skipped: {stats['skipped']}{Style.RESET_ALL}")
        if stats['failed'] > 0:
            print(f"{Fore.RED}❌ Failed: {stats['failed']}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Output: {output_folder}{Style.RESET_ALL}\n")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error in upscale_numbered_flow: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================
# MODE 3: UPSCALE FULL MOVIE (SINGLE FILE)
# ============================================================

def run_upscale_full_movie(config, movie_path):
    """Upscale pojedynczego pliku (full concat movie)
    
    Output:
    final_outputs/FULL_MOVIE_*_UPSCALED.mp4
    """
    
    try:
        movie_path = Path(movie_path)
        upscale_config = config['batch_upscale']
        
        # Output path
        output_name = movie_path.stem + "_UPSCALED" + movie_path.suffix
        output_path = movie_path.parent / output_name
        
        print(f"\n{Fore.CYAN}📁 Source: {movie_path.name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   Size:   {movie_path.stat().st_size / (1024*1024):.1f} MB{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📁 Output: {output_name}{Style.RESET_ALL}\n")
        
        # Check if already exists
        if output_path.exists():
            print(f"{Fore.YELLOW}⚠ Output already exists!{Style.RESET_ALL}")
            response = input("Overwrite? [y/N]: ").strip().lower()
            if response != 'y':
                print(f"{Fore.RED}✗ Cancelled{Style.RESET_ALL}")
                return False
        
        # Initialize backend
        backend = _create_backend(upscale_config)
        
        # Settings
        target_resolution = upscale_config.get('target_resolution', [1024, 1024])
        target_width = target_resolution[0]
        target_height = target_resolution[1]
        upscale_model = upscale_config.get('upscale_model', 'RealESRGAN_x4plus.pth')
        interpolation = upscale_config.get('interpolation', 'lanczos')
        method = upscale_config.get('method', 'stretch')
        
        # Upscale
        print(f"{Fore.YELLOW}⚙ Upscaling full movie...{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}This may take significant time (large file)!{Style.RESET_ALL}\n")
        
        success = backend.upscale_video(
            input_video=movie_path,
            output_path=output_path,
            target_width=target_width,
            target_height=target_height,
            interpolation=interpolation,
            method=method,
            model_name=upscale_model
        )
        
        # Summary
        if success:
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{'':20}UPSCALE SUMMARY")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            print(f"{Fore.GREEN}✅ Success!{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}Output: {output_path}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Size:   {output_path.stat().st_size / (1024*1024):.1f} MB{Style.RESET_ALL}\n")
            return True
        else:
            print(f"\n{Fore.RED}❌ Failed to upscale full movie{Style.RESET_ALL}\n")
            return False
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error in upscale_full_movie: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _create_backend(upscale_config):
    """Create UtilityBackend with config"""
    
    backend_config = {
        'workflows_path': 'workflows',
        'workflow_configs_path': 'workflow_configs',
        'comfyui_output_folder': upscale_config.get('comfyui_output_folder', 'D:/ComfyUI/output'),
        'comfyui_server': upscale_config.get('comfyui_server', 'http://127.0.0.1:8100'),
        'utility_workflow': 'gan_upscaler'
    }
    
    return UtilityBackend(backend_config)


def _upscale_directory(backend, source_dir, output_dir, upscale_config, suffix='', filter_files_only=False):
    """Upscale all videos in directory
    
    Args:
        filter_files_only: If True, only process direct files (skip subfolders)
    
    Returns:
        dict: {'upscaled': int, 'skipped': int, 'failed': int}
    """
    
    # Get video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    
    if filter_files_only:
        # Only direct files, skip subfolders
        video_files = sorted([
            f for f in source_dir.iterdir()
            if f.is_file() and f.suffix.lower() in video_extensions
        ])
    else:
        # All video files
        video_files = sorted([
            f for f in source_dir.iterdir()
            if f.is_file() and f.suffix.lower() in video_extensions
        ])
    
    if not video_files:
        print(f"{Fore.YELLOW}⚠ No video files found{Style.RESET_ALL}")
        return {'upscaled': 0, 'skipped': 0, 'failed': 0}
    
    print(f"{Fore.CYAN}Found {len(video_files)} videos{Style.RESET_ALL}\n")
    
    # Settings
    target_resolution = upscale_config.get('target_resolution', [1024, 1024])
    target_width = target_resolution[0]
    target_height = target_resolution[1]
    upscale_model = upscale_config.get('upscale_model', 'RealESRGAN_x4plus.pth')
    interpolation = upscale_config.get('interpolation', 'lanczos')
    method = upscale_config.get('method', 'stretch')
    
    upscaled = 0
    skipped = 0
    failed = 0
    
    for i, video_file in enumerate(video_files, 1):
        # Output filename
        output_name = video_file.stem + suffix + video_file.suffix
        output_path = output_dir / output_name
        
        # Skip if exists
        if output_path.exists():
            print(f"{Fore.CYAN}⊘{Style.RESET_ALL} [{i:03d}/{len(video_files)}] SKIP (exists): {video_file.name}")
            skipped += 1
            continue
        
        print(f"{Fore.YELLOW}⚙{Style.RESET_ALL} [{i:03d}/{len(video_files)}] Upscaling: {video_file.name}")
        
        # Upscale
        try:
            success = backend.upscale_video(
                input_video=video_file,
                output_path=output_path,
                target_width=target_width,
                target_height=target_height,
                interpolation=interpolation,
                method=method,
                model_name=upscale_model
            )
            
            if success:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL} [{i:03d}/{len(video_files)}] Done: {output_name}")
                upscaled += 1
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL} [{i:03d}/{len(video_files)}] FAILED: {video_file.name}")
                failed += 1
            
        except Exception as e:
            print(f"{Fore.RED}✗{Style.RESET_ALL} [{i:03d}/{len(video_files)}] FAILED: {video_file.name}")
            print(f"   Error: {e}")
            failed += 1
    
    return {'upscaled': upscaled, 'skipped': skipped, 'failed': failed}