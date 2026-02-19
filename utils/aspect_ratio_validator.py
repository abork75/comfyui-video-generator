# -*- coding: utf-8 -*-
"""
Aspect Ratio Validator - Ensure consistent video dimensions
"""

from pathlib import Path
from PIL import Image
import subprocess
import json


def get_media_dimensions(file_path):
    """
    Get width and height of image or video
    
    Returns:
        tuple: (width, height) or None if failed
    """
    file_path = Path(file_path)
    
    # Check if image
    if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
        try:
            with Image.open(file_path) as img:
                return img.size  # (width, height)
        except Exception as e:
            print(f"Error reading image {file_path.name}: {e}")
            return None
    
    # Check if video
    elif file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                str(file_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # Find video stream
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        width = stream.get('width')
                        height = stream.get('height')
                        
                        if width and height:
                            return (width, height)
            
            return None
            
        except Exception as e:
            print(f"Error reading video {file_path.name}: {e}")
            return None
    
    return None


def validate_aspect_ratios(project_folder, file_list, tolerance=0.02, strategy='most_common'):
    """
    Validate that all files have consistent aspect ratios
    
    Args:
        project_folder: Path to project folder
        file_list: List of filenames to check
        tolerance: Acceptable aspect ratio deviation (default 0.02 = 2%)
        strategy: 'most_common' (use most common AR as baseline) or 'first' (use first file)
    
    Returns:
        tuple: (is_valid: bool, info: dict)
    """
    
    project_folder = Path(project_folder)
    
    # Get dimensions for all files
    file_data = []
    
    for filename in file_list:
        file_path = project_folder / filename
        
        if not file_path.exists():
            continue
        
        dims = get_media_dimensions(file_path)
        
        if dims:
            width, height = dims
            aspect_ratio = width / height
            
            file_data.append({
                'filename': filename,
                'width': width,
                'height': height,
                'aspect_ratio': aspect_ratio
            })
    
    if not file_data:
        return False, {'error': 'No valid files found'}
    
    # Determine baseline aspect ratio
    if strategy == 'most_common':
        # Group by similar aspect ratios
        ar_groups = {}
        
        for data in file_data:
            ar = data['aspect_ratio']
            
            # Find existing group (within tolerance)
            found_group = False
            
            for group_ar in ar_groups:
                if abs(ar - group_ar) / group_ar <= tolerance:
                    ar_groups[group_ar].append(data)
                    found_group = True
                    break
            
            if not found_group:
                ar_groups[ar] = [data]
        
        # Find most common group
        most_common_ar = max(ar_groups.keys(), key=lambda ar: len(ar_groups[ar]))
        baseline_ar = most_common_ar
        
    else:  # strategy == 'first'
        baseline_ar = file_data[0]['aspect_ratio']
    
    # Check all files against baseline
    mismatches = []
    
    for data in file_data:
        ar = data['aspect_ratio']
        deviation = abs(ar - baseline_ar) / baseline_ar
        
        if deviation > tolerance:
            mismatches.append({
                'filename': data['filename'],
                'aspect_ratio': ar,
                'deviation': deviation * 100,  # as percentage
                'dimensions': f"{data['width']}x{data['height']}"
            })
    
    # Validation result
    is_valid = len(mismatches) == 0
    
    info = {
        'baseline_ar': baseline_ar,
        'total_files': len(file_data),
        'mismatches': mismatches,
        'tolerance_percent': tolerance * 100
    }
    
    if not is_valid:
        error_msg = f"Found {len(mismatches)} file(s) with mismatched aspect ratios:\n"
        for m in mismatches:
            error_msg += f"  • {m['filename']} ({m['dimensions']}) - deviation: {m['deviation']:.1f}%\n"
        
        info['error'] = error_msg
    
    return is_valid, info