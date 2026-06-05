# -*- coding: utf-8 -*-
"""
Frame Extractor - Extract first/last frames from videos and images
"""

import subprocess
from pathlib import Path
from PIL import Image


class FrameExtractor:
    """Extract frames from videos and process images for transitions"""
    
    def __init__(self, project_folder, min_width=256, min_height=256, 
                 max_width=1024, max_height=1024, default_resolution=None,
                 force_resolution=None, image_quality=95):
        """
        Initialize frame extractor
        
        Args:
            project_folder: Path to project folder
            min_width: Minimum output width
            min_height: Minimum output height
            max_width: Maximum output width
            max_height: Maximum output height
            default_resolution: Default resolution tuple (width, height)
            force_resolution: Force specific resolution (overrides auto-detect)
            image_quality: JPEG quality for extracted frames (1-100)
        """
        self.project_folder = Path(project_folder)
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.default_resolution = default_resolution
        self.force_resolution = force_resolution
        self.image_quality = image_quality
    
    def auto_detect_resolution(self, file_list):
        """
        Auto-detect target resolution from files
        
        Args:
            file_list: List of filenames
        
        Returns:
            tuple: (width, height)
        """
        
        if self.force_resolution:
            return self.force_resolution
        
        # Get dimensions from all files
        from .aspect_ratio_validator import get_media_dimensions
        
        dimensions = []
        
        for filename in file_list:
            file_path = self.project_folder / filename
            dims = get_media_dimensions(file_path)
            
            if dims:
                dimensions.append(dims)
        
        if not dimensions:
            # Fallback to default
            if self.default_resolution:
                return self.default_resolution
            else:
                return (512, 512)
        
        # Use most common resolution
        from collections import Counter
        most_common = Counter(dimensions).most_common(1)[0][0]
        
        width, height = most_common
        
        # Clamp to min/max
        width = max(self.min_width, min(width, self.max_width))
        height = max(self.min_height, min(height, self.max_height))
        
        # Round to multiple of 16 (WanVideo ImageResizeKJv2 node uses divisible_by=16)
        width = (width // 16) * 16
        height = (height // 16) * 16
        
        return (width, height)
    
    def extract_end_frame(self, filename, target_width, target_height):
        """
        Extract last frame from video or process image
        
        Args:
            filename: Source filename
            target_width: Target width
            target_height: Target height
        
        Returns:
            Path to extracted frame or None if failed
        """
        
        source_path = self.project_folder / filename
        # PNG: lossless — eliminates second round of lossy compression
        output_filename = f"{source_path.stem}_end.png"

        # Save to frames/ folder (INPUT - not in transitions/)
        frames_folder = self.project_folder / 'frames'
        frames_folder.mkdir(parents=True, exist_ok=True)
        output_path = frames_folder / output_filename

        # Check if image
        if source_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            # Process image
            try:
                with Image.open(source_path) as img:
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Resize
                    img_resized = img.resize((target_width, target_height), Image.LANCZOS)

                    # Save as PNG (lossless — even JPEG sources benefit: no second encode)
                    img_resized.save(output_path, 'PNG')

                    return output_path

            except Exception as e:
                print(f"Error processing image {filename}: {e}")
                return None

        # Check if video
        elif source_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            # ============================================================
            # CRITICAL FIX: Extract ACTUAL last frame (not 1s before end)
            # Old: -sseof -1 gave frame from middle of video
            # New: Count frames → select last by index
            # Output: PNG (lossless)
            # ============================================================

            try:
                # Step 1: Get total frame count
                probe_cmd = [
                    'ffprobe',
                    '-v', 'error',
                    '-select_streams', 'v:0',
                    '-count_frames',
                    '-show_entries', 'stream=nb_read_frames',
                    '-of', 'csv=p=0',
                    str(source_path)
                ]

                result = subprocess.run(probe_cmd, check=True, capture_output=True, text=True)
                total_frames = int(result.stdout.strip())

                # Step 2: Extract last frame (index = total - 1) as PNG
                last_frame_idx = total_frames - 1

                cmd = [
                    'ffmpeg',
                    '-i', str(source_path),
                    '-vf', f'select=eq(n\\,{last_frame_idx}),scale={target_width}:{target_height}',
                    '-frames:v', '1',
                    '-y',
                    str(output_path)
                ]

                result = subprocess.run(cmd, capture_output=True)

                if result.returncode == 0 and output_path.exists():
                    return output_path
                else:
                    print(f"Error extracting last frame from {filename}")
                    return None

            except Exception as e:
                print(f"Error extracting frame: {e}")
                return None
        
        return None
    
    def extract_start_frame(self, filename, target_width, target_height):
        """
        Extract first frame from video or process image
        
        Args:
            filename: Source filename
            target_width: Target width
            target_height: Target height
        
        Returns:
            Path to extracted frame or None if failed
        """
        
        source_path = self.project_folder / filename
        # PNG: lossless — eliminates second round of lossy compression
        output_filename = f"{source_path.stem}_start.png"

        # Save to frames/ folder (INPUT - not in transitions/)
        frames_folder = self.project_folder / 'frames'
        frames_folder.mkdir(parents=True, exist_ok=True)
        output_path = frames_folder / output_filename

        # Check if image
        if source_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            # Process image
            try:
                with Image.open(source_path) as img:
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Resize
                    img_resized = img.resize((target_width, target_height), Image.LANCZOS)

                    # Save as PNG (lossless)
                    img_resized.save(output_path, 'PNG')

                    return output_path

            except Exception as e:
                print(f"Error processing image {filename}: {e}")
                return None

        # Check if video
        elif source_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            # Extract first frame as PNG (lossless)
            try:
                cmd = [
                    'ffmpeg',
                    '-i', str(source_path),
                    '-vframes', '1',
                    '-vf', f'scale={target_width}:{target_height}',
                    '-y',
                    str(output_path)
                ]

                result = subprocess.run(cmd, capture_output=True)

                if result.returncode == 0 and output_path.exists():
                    return output_path
                else:
                    print(f"Error extracting first frame from {filename}")
                    return None

            except Exception as e:
                print(f"Error extracting frame: {e}")
                return None
        
        return None