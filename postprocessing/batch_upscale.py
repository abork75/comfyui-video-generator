# -*- coding: utf-8 -*-
"""
Batch Upscale Engine - GAN Upscaling for video batches
Analogous to postprocess_engine.py structure
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
    """Main batch upscale entry point
    
    Modes:
    - 'source': Upscale from project source files (main, chain, transitions)
    - 'numbered_flow': Upscale from FLOW_* folders (interactive selection)
    """
    
    upscale_config = config['batch_upscale']
    source_mode = upscale_config.get('source_mode', 'source')
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{'':20}BATCH UPSCALE")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Source mode: {source_mode}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    if source_mode == 'source':
        return run_upscale_source(config)
    elif source_mode == 'numbered_flow':
        return run_upscale_numbered_flow(config)
    else:
        print(f"{Fore.RED}❌ Invalid source_mode: {source_mode}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Use 'source' or 'numbered_flow'{Style.RESET_ALL}")
        return False


# ============================================================
# MODE 1: UPSCALE SOURCE FILES
# ============================================================

def run_upscale_source(config):
    """Upscale plików źródłowych (main, chain, transitions)
    
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
        
        # Source categories
        source_dirs = {
            'main': project_folder / 'main',
            'chain': project_folder / 'chain',
            'transitions': project_folder / 'transitions'
        }
        
        # Initialize backend
        backend = _create_backend(upscale_config)
        
        total_upscaled = 0
        total_skipped = 0
        total_failed = 0
        
        # Upscale each category
        for category, source_dir in source_dirs.items():
            if not source_dir.exists():
                print(f"{Fore.YELLOW}⚠ Skipping {category} - directory not found{Style.RESET_ALL}")
                continue
            
            output_dir = output_base / category
            output_dir.mkdir(exist_ok=True)
            
            print(f"\n{Fore.YELLOW}{'─'*70}")
            print(f"📌 Category: {category.upper()}")
            print(f"{'─'*70}{Style.RESET_ALL}\n")
            
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
# MODE 2: UPSCALE NUMBERED FLOW
# ============================================================

def run_upscale_numbered_flow(config):
    """Upscale z FLOW_* folders (interactive selection)
    
    Output structure:
    final_outputs/FLOW_{project}_{timestamp}_UPSCALED/
        ├── f0001_video_upscaled.mp4
        ├── f0002_video_upscaled.mp4
        └── ...
    """
    
    try:
        project_folder = Path(config['project_folder'])
        upscale_config = config['batch_upscale']
        
        # Find FLOW folders
        print(f"\n{Fore.CYAN}🔍 Searching for FLOW folders in final_outputs/...{Style.RESET_ALL}")
        flow_folders = _find_flow_folders(project_folder)
        
        if not flow_folders:
            print(f"\n{Fore.RED}❌ No FLOW folders found!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Run numbered_flow postprocessing first{Style.RESET_ALL}")
            return False
        
        # Interactive selection
        selected_flow = _select_flow_folder_interactive(flow_folders)
        
        if not selected_flow:
            print(f"{Fore.RED}✗ Cancelled by user{Style.RESET_ALL}")
            return False
        
        # Output folder
        flow_name = selected_flow.name
        output_folder = selected_flow.parent / f"{flow_name}_UPSCALED"
        output_folder.mkdir(exist_ok=True)
        
        print(f"\n{Fore.CYAN}📁 Source: {flow_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📁 Output: {output_folder.name}{Style.RESET_ALL}\n")
        
        # Initialize backend
        backend = _create_backend(upscale_config)
        
        # Upscale directory
        stats = _upscale_directory(
            backend=backend,
            source_dir=selected_flow,
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


def _upscale_directory(backend, source_dir, output_dir, upscale_config, suffix=''):
    """Upscale all videos in directory
    
    Returns:
        dict: {'upscaled': int, 'skipped': int, 'failed': int}
    """
    
    # Get video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    video_files = sorted([
        f for f in source_dir.iterdir()
        if f.suffix.lower() in video_extensions
    ])
    
    if not video_files:
        print(f"{Fore.YELLOW}⚠ No video files found in {source_dir.name}{Style.RESET_ALL}")
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
        
        # Upscale - FIXED METHOD CALL!
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


def _find_flow_folders(project_folder):
    """Find all FLOW_* folders in final_outputs/, sorted by timestamp (newest first)
    
    Analogous to postprocess_engine.find_flow_folders()
    """
    
    final_outputs = project_folder / 'final_outputs'
    
    if not final_outputs.exists():
        return []
    
    flow_folders = []
    
    for folder in final_outputs.iterdir():
        if folder.is_dir() and folder.name.startswith('FLOW_') and not folder.name.endswith('_UPSCALED'):
            # Count video files
            video_count = len([
                f for f in folder.iterdir()
                if f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']
            ])
            
            flow_folders.append({
                'path': folder,
                'name': folder.name,
                'timestamp': folder.stat().st_mtime,
                'file_count': video_count,
            })
    
    # Sort by timestamp (newest first)
    flow_folders.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return flow_folders


def _select_flow_folder_interactive(flow_folders):
    """Interactive selection of FLOW folder
    
    Analogous to postprocess_engine.select_flow_folder_interactive()
    """
    
    print(f"\n{Fore.CYAN}Available FLOW folders:{Style.RESET_ALL}\n")
    
    for i, flow in enumerate(flow_folders, 1):
        timestamp_str = datetime.fromtimestamp(flow['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [{i}] {flow['name']}")
        print(f"      Files: {flow['file_count']}, Modified: {timestamp_str}")
    
    print(f"\n  [0] Cancel")
    
    while True:
        try:
            choice = input(f"\n{Fore.YELLOW}Select FLOW folder [1-{len(flow_folders)}]: {Style.RESET_ALL}").strip()
            
            if not choice:
                continue
            
            choice_num = int(choice)
            
            if choice_num == 0:
                return None
            
            if 1 <= choice_num <= len(flow_folders):
                selected = flow_folders[choice_num - 1]
                return selected['path']
            else:
                print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")
                
        except (ValueError, KeyboardInterrupt):
            return None