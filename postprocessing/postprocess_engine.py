# -*- coding: utf-8 -*-
"""
Postprocessing Engine - Main logic for final output
"""

import os
import subprocess
import time
import sys
import shutil
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

# Add parent directory to path for flow_parser import
sys.path.append(str(Path(__file__).parent.parent))
from flow_parser import parse_flow

init(autoreset=True)

# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

def run_postprocessing(config):
    """Main postprocessing entry point"""
    
    pp_config = config['postprocessing']
    
    # Check which processors are enabled
    enabled_processors = []
    if pp_config.get('full_concat', False):
        enabled_processors.append('full_concat')
    if pp_config.get('numbered_flow', False):
        enabled_processors.append('numbered_flow')
    
    if not enabled_processors:
        print(f"{Fore.RED}❌ No processors enabled!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Set 'full_concat': True or 'numbered_flow': True{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{'':20}POSTPROCESSING")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Enabled processors: {', '.join(enabled_processors)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Run enabled processors (numbered_flow BEFORE full_concat)
    results = {}
    
    if 'numbered_flow' in enabled_processors:
        print(f"\n{Fore.YELLOW}{'─'*70}")
        print(f"📌 Running: NUMBERED FLOW")
        print(f"{'─'*70}{Style.RESET_ALL}\n")
        results['numbered_flow'] = run_numbered_flow(config)
    
    if 'full_concat' in enabled_processors:
        print(f"\n{Fore.YELLOW}{'─'*70}")
        print(f"📌 Running: FULL CONCAT")
        print(f"{'─'*70}{Style.RESET_ALL}\n")
        results['full_concat'] = run_full_concat(config)
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{'':20}POSTPROCESSING SUMMARY")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    for processor, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {processor}: {'SUCCESS' if result else 'FAILED'}")
    
    print()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_flow_folders(project_folder):
    """Find all FLOW_* folders in final_outputs/, sorted by timestamp (newest first)"""
    final_outputs = project_folder / 'final_outputs'
    
    if not final_outputs.exists():
        return []
    
    flow_folders = []
    
    for folder in final_outputs.iterdir():
        if folder.is_dir() and folder.name.startswith('FLOW_'):
            # Count video files
            video_count = len([f for f in folder.iterdir() if f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']])
            
            flow_folders.append({
                'path': folder,
                'name': folder.name,
                'timestamp': folder.stat().st_mtime,
                'file_count': video_count,
            })
    
    # Sort by timestamp (newest first)
    flow_folders.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return flow_folders


def select_flow_folder_interactive(flow_folders):
    """
    Interactive selection of FLOW folder
    
    Returns:
        Path or None (if cancelled)
    """
    
    print(f"\n{Fore.YELLOW}Found {len(flow_folders)} FLOW folder(s):{Style.RESET_ALL}\n")
    
    # Show latest (default)
    latest = flow_folders[0]
    print(f"  {Fore.GREEN}[LATEST]{Style.RESET_ALL} {latest['name']} ({latest['file_count']} files) ← DEFAULT")
    
    # Show alternatives
    for i, folder in enumerate(flow_folders[1:], start=1):
        print(f"  [{i}] {folder['name']} ({folder['file_count']} files)")
    
    # Prompt
    options = '/'.join(['yes', 'no'] + [str(i) for i in range(1, len(flow_folders))])
    
    print()
    response = input(f"Use latest FLOW? ({options}): ").strip().lower()
    
    # Parse response
    if response in ['yes', 'y', '']:
        print(f"{Fore.GREEN}✓ Using latest: {latest['name']}{Style.RESET_ALL}")
        return latest['path']
    
    elif response in ['no', 'n']:
        print(f"{Fore.YELLOW}✗ Cancelled by user{Style.RESET_ALL}")
        return None
    
    else:
        # Try to parse as number
        try:
            choice = int(response)
            if 1 <= choice < len(flow_folders):
                selected = flow_folders[choice]
                print(f"{Fore.GREEN}✓ Using: {selected['name']}{Style.RESET_ALL}")
                return selected['path']
            else:
                print(f"{Fore.RED}✗ Invalid choice{Style.RESET_ALL}")
                return None
        except ValueError:
            print(f"{Fore.RED}✗ Invalid input{Style.RESET_ALL}")
            return None


# ============================================================
# CONCAT FUNCTIONS (WITH NORMALIZATION!)
# ============================================================

def concat_simple_copy(video_files, output_path, settings):
    """Simple concat (stream copy - fast but may fail with different formats)"""
    
    # Create concat file
    concat_file = output_path.parent / "concat_list.txt"
    
    with open(concat_file, 'w', encoding='utf-8') as f:
        for video in video_files:
            video_path_str = str(video).replace('\\', '/')
            f.write(f"file '{video_path_str}'\n")
    
    print(f"\n{Fore.GREEN}✓ Created concat list: {concat_file.name}{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}🎬 Running ffmpeg concat (stream copy - fast!)...{Style.RESET_ALL}\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_file),
        '-c', 'copy',
        '-movflags', '+faststart',
        '-y',
        str(output_path)
    ]
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    # Cleanup
    try:
        concat_file.unlink()
    except:
        pass
    
    if result.returncode == 0 and output_path.exists():
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"✅ CONCAT SUCCESSFUL!")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"   Output: {output_path.name}")
        print(f"   Location: {output_path.parent}")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Time: {elapsed:.1f}s")
        print()
        
        return True
    else:
        print(f"\n{Fore.RED}❌ Concat failed!{Style.RESET_ALL}")
        if result.stderr:
            print(f"{Fore.YELLOW}FFmpeg error:{Style.RESET_ALL}")
            print(result.stderr[-500:])
        return False


def concat_with_normalization(video_files, output_path, settings):
    """2-Pass concat with normalization (slower but reliable)"""
    
    print(f"\n{Fore.YELLOW}⚙️  2-PASS CONCAT (with normalization){Style.RESET_ALL}")
    print(f"{Fore.CYAN}This ensures smooth playback by normalizing FPS/codec/resolution{Style.RESET_ALL}\n")
    
    temp_folder = output_path.parent / "temp_normalized"
    temp_folder.mkdir(exist_ok=True)
    
    # PASS 1: Normalize
    print(f"{Fore.YELLOW}{'─'*70}")
    print(f"PASS 1: Normalizing {len(video_files)} files...")
    print(f"{'─'*70}{Style.RESET_ALL}\n")
    
    target_fps = settings.get('fps', 16)
    normalized_files = []
    start_normalize = time.time()
    
    for i, video in enumerate(video_files, 1):
        temp_file = temp_folder / f"normalized_{i:04d}.mp4"
        
        print(f"  [{i:02d}/{len(video_files)}] {video.name}")
        
        cmd = [
            'ffmpeg',
            '-i', str(video),
            '-r', str(target_fps),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '18',
            '-pix_fmt', 'yuv420p',
            '-vsync', 'cfr',
            '-an',  # Remove audio (WAN has no audio anyway)
            '-movflags', '+faststart',
            '-y',
            str(temp_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{Fore.RED}❌ Normalization failed: {video.name}{Style.RESET_ALL}")
            shutil.rmtree(temp_folder, ignore_errors=True)
            return False
        
        normalized_files.append(temp_file)
    
    elapsed_normalize = time.time() - start_normalize
    print(f"\n{Fore.GREEN}✓ Normalization complete ({elapsed_normalize:.1f}s){Style.RESET_ALL}\n")
    
    # PASS 2: Concat
    print(f"{Fore.YELLOW}{'─'*70}")
    print(f"PASS 2: Concatenating normalized files...")
    print(f"{'─'*70}{Style.RESET_ALL}\n")
    
    normalized_concat = temp_folder / "normalized_concat.txt"
    with open(normalized_concat, 'w', encoding='utf-8') as f:
        for temp_file in normalized_files:
            file_path_str = str(temp_file).replace('\\', '/')
            f.write(f"file '{file_path_str}'\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(normalized_concat),
        '-c', 'copy',  # Now safe! (all normalized)
        '-movflags', '+faststart',
        '-y',
        str(output_path)
    ]
    
    start_concat = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed_concat = time.time() - start_concat
    
    success = result.returncode == 0 and output_path.exists()
    
    # Cleanup
    if success:
        print(f"\n{Fore.CYAN}🧹 Cleaning up temporary files...{Style.RESET_ALL}")
        try:
            shutil.rmtree(temp_folder)
            print(f"{Fore.GREEN}✓ Removed {len(normalized_files)} temp files{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Cleanup warning: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Temp files kept for debugging: {temp_folder}{Style.RESET_ALL}")
    
    if success:
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        total_time = elapsed_normalize + elapsed_concat
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"✅ CONCAT SUCCESSFUL!")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"   Output: {output_path.name}")
        print(f"   Location: {output_path.parent}")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Time: {total_time:.1f}s (normalize: {elapsed_normalize:.1f}s + concat: {elapsed_concat:.1f}s)")
        print()
        
        return True
    else:
        print(f"\n{Fore.RED}❌ Concat failed!{Style.RESET_ALL}")
        if result.stderr:
            print(f"{Fore.YELLOW}FFmpeg error:{Style.RESET_ALL}")
            print(result.stderr[-500:])
        return False


def concat_from_flow(flow_folder, output_path, settings):
    """
    Simple concat from FLOW folder (files already prepared)
    With optional normalization
    """
    
    print(f"{Fore.CYAN}📋 Preparing concat from FLOW folder...{Style.RESET_ALL}\n")
    
    # Get all video files (sorted)
    video_files = sorted([f for f in flow_folder.iterdir() if f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']])
    
    if not video_files:
        print(f"{Fore.RED}❌ No video files found in FLOW folder!{Style.RESET_ALL}")
        return False
    
    print(f"{Fore.CYAN}Files to concat ({len(video_files)}):{Style.RESET_ALL}")
    for i, f in enumerate(video_files, 1):
        print(f"  [{i:02d}] {f.name}")
    
    # Check normalization setting
    normalize = settings.get('normalize', True)  # Default ON
    
    if normalize:
        return concat_with_normalization(video_files, output_path, settings)
    else:
        print(f"\n{Fore.YELLOW}⚠️  Normalization disabled - using stream copy{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   This may cause glitches if files have different formats!{Style.RESET_ALL}")
        return concat_simple_copy(video_files, output_path, settings)


def concat_from_project(project_folder, flow, output_path, settings):
    """
    Concat from project source (with transitions logic)
    Respects breaks in FLOW - uses flow_parser
    """
    
    print(f"{Fore.CYAN}📋 Building file list from project...{Style.RESET_ALL}\n")
    
    # Parse FLOW using flow_parser
    parser = parse_flow(flow)
    
    # Get concat list (auto handles breaks, images, transitions)
    files_to_concat = parser.get_concat_list(project_folder, skip_images=True)
    
    if not files_to_concat:
        print(f"\n{Fore.RED}❌ No files to concat!{Style.RESET_ALL}")
        return False
    
    # Show what will be concatenated
    print(f"{Fore.CYAN}Files to concat:{Style.RESET_ALL}")
    for i, file_path in enumerate(files_to_concat, 1):
        file_type = "🎬 Transition" if "transition" in file_path.name else "📹 Source"
        exists_marker = "✓" if file_path.exists() else "✗"
        print(f"  [{i:02d}] {exists_marker} {file_type}: {file_path.name}")
    
    print(f"\n{Fore.GREEN}Total files to concat: {len(files_to_concat)}{Style.RESET_ALL}\n")
    
    # Check normalization setting
    normalize = settings.get('normalize', True)  # Default ON
    
    if normalize:
        return concat_with_normalization(files_to_concat, output_path, settings)
    else:
        print(f"\n{Fore.YELLOW}⚠️  Normalization disabled - using stream copy{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   This may cause glitches if files have different formats!{Style.RESET_ALL}")
        return concat_simple_copy(files_to_concat, output_path, settings)


# ============================================================
# MAIN PROCESSORS
# ============================================================

def run_full_concat(config):
    """Mode 1: Full movie concat (auto-detect source)"""
    
    project_folder = Path(config['project_folder'])
    project_name = project_folder.name
    
    # Output folder
    output_folder = project_folder / 'final_outputs'
    output_folder.mkdir(exist_ok=True)
    
    # Settings
    settings = config['postprocessing'].get('full_concat_settings', {})
    
    # Auto-enable normalization if not specified
    if 'normalize' not in settings:
        settings['normalize'] = True  # Default ON
    
    if 'fps' not in settings:
        settings['fps'] = 16  # Default FPS
    
    # ============================================================
    # AUTO-DETECT SOURCE (FLOW folders or project)
    # ============================================================
    
    print(f"\n{Fore.CYAN}🔍 Searching for FLOW folders in final_outputs/...{Style.RESET_ALL}")
    
    flow_folders = find_flow_folders(project_folder)
    
    source_type = None
    source_path = None
    video_order = []
    output_name = None
    
    if flow_folders:
        # Interactive selection
        selected_flow = select_flow_folder_interactive(flow_folders)
        
        if not selected_flow:
            return False  # User cancelled
        
        source_type = 'flow'
        source_path = selected_flow
        
        # Output name based on FLOW folder name
        flow_folder_name = selected_flow.name
        output_name = f"FULL_MOVIE_from_{flow_folder_name}.mp4"
        
        # Get video files from FLOW folder (sorted by filename)
        video_files = sorted([f for f in source_path.iterdir() if f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']])
        
        video_order = [f.name for f in video_files]
        
        print(f"\n{Fore.CYAN}📁 Source: {source_path.name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   Files: {len(video_order)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   Output: {output_name}{Style.RESET_ALL}\n")
        
    else:
        # Fallback to project
        print(f"\n{Fore.YELLOW}⚠️  No FLOW folders found!{Style.RESET_ALL}\n")
        print(f"Fallback to project source files:")
        print(f"  Source: {project_folder}")
        print(f"  Transitions: {project_folder / 'transitions'}\n")
        
        response = input("Continue with project source? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print(f"{Fore.RED}✗ Cancelled by user{Style.RESET_ALL}")
            return False
        
        source_type = 'project'
        source_path = project_folder
        
        # Output name for project source
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"FULL_MOVIE_pliki_projektu_{project_name}_{timestamp}.mp4"
        
        print(f"\n{Fore.GREEN}✓ Using project source{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Output: {output_name}{Style.RESET_ALL}\n")
    
    # ============================================================
    # RUN CONCAT (different logic for flow vs project)
    # ============================================================
    
    try:
        if source_type == 'flow':
            # Concat from FLOW folder (with normalization!)
            success = concat_from_flow(
                flow_folder=source_path,
                output_path=output_folder / output_name,
                settings=settings
            )
            return success
        else:
            # Concat from project source (with normalization!)
            flow = config.get('flow', [])
            
            success = concat_from_project(
                project_folder=project_folder,
                flow=flow,
                output_path=output_folder / output_name,
                settings=settings
            )
            return success
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error in concat: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


def run_numbered_flow(config):
    """Mode 2: Numbered copies in folder (dense numbering, videos only)"""
    
    try:
        project_folder = Path(config['project_folder'])
        project_name = project_folder.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Output folder
        output_base = project_folder / 'final_outputs'
        output_base.mkdir(exist_ok=True)
        
        settings = config['postprocessing'].get('numbered_flow_settings', {})
        
        output_folder_name = settings.get('output_folder')
        if not output_folder_name:
            output_folder_name = f"FLOW_{project_name}_{timestamp}"
        
        output_folder = output_base / output_folder_name
        output_folder.mkdir(exist_ok=True)
        
        print(f"{Fore.CYAN}📁 Output folder: {output_folder.name}{Style.RESET_ALL}\n")
        
        # Parse FLOW using flow_parser
        flow = config.get('flow', [])
        parser = parse_flow(flow)
        
        # Get numbered flow list
        items = parser.get_numbered_flow_list(project_folder, skip_images=True)
        
        number_format = settings.get('number_format', 'f{:04d}')
        
        counter = 1
        copied = 0
        skipped_images = 0
        missing = 0
        
        for item in items:
            item_type = item['type']
            item_path = item['path']
            item_name = item['name']
            
            if item_type == 'skip':
                print(f"{Fore.CYAN}⊘{Style.RESET_ALL} SKIP ({item['reason']}): {item_name}")
                skipped_images += 1
                continue
            
            if item_type == 'transition':
                if item.get('exists', False):
                    numbered_name = f"{number_format.format(counter)}_{item_name}"
                    dest = output_folder / numbered_name
                    shutil.copy2(item_path, dest)
                    print(f"{Fore.GREEN}✓{Style.RESET_ALL} [{counter:04d}] {item_name}")
                    copied += 1
                    counter += 1
                else:
                    print(f"{Fore.YELLOW}⚠{Style.RESET_ALL} MISSING: {item_name}")
                    missing += 1
            
            elif item_type == 'file':
                if item.get('exists', False):
                    numbered_name = f"{number_format.format(counter)}_{item_name}"
                    dest = output_folder / numbered_name
                    shutil.copy2(item_path, dest)
                    print(f"{Fore.GREEN}✓{Style.RESET_ALL} [{counter:04d}] {item_name}")
                    copied += 1
                    counter += 1
                else:
                    print(f"{Fore.YELLOW}⚠{Style.RESET_ALL} MISSING: {item_name}")
                    missing += 1
        
        print(f"\n{Fore.GREEN}✅ Copied {copied} files to:{Style.RESET_ALL}")
        print(f"   {output_folder}")
        
        if skipped_images > 0:
            print(f"{Fore.CYAN}ℹ️  Skipped {skipped_images} source images (input material only){Style.RESET_ALL}")
        
        if missing > 0:
            print(f"{Fore.YELLOW}⚠️  Missing {missing} files{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error in numbered_flow: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False