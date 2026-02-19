# helpers/imgur_upload.py
"""
Imgur uploader for cloud API
Uploads images and returns public URLs
"""

import requests
import os
from pathlib import Path

# Imgur Client ID (anonymous uploads - bez logowania)
# To jest publiczny client ID dla anonymous uploads (rate limit: 50/hour)
# Możesz stworzyć własny na: https://api.imgur.com/oauth2/addclient
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')

def upload_to_imgur(image_path, client_id=None):
    """
    Upload image to Imgur and return public URL
    
    Args:
        image_path: Path to image file (str or Path)
        client_id: Imgur Client ID (optional, uses env or default)
        
    Returns:
        str: Public image URL or None if failed
        
    Example:
        url = upload_to_imgur("frame.jpg")
        # Returns: "https://i.imgur.com/ABC123.jpg"
    """
    if client_id is None:
        client_id = IMGUR_CLIENT_ID
    
    image_path = Path(image_path)
    
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return None
    
    url = "https://api.imgur.com/3/upload"
    
    headers = {
        'Authorization': f'Client-ID {client_id}'
    }
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(url, headers=headers, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data['data']['link']
            return image_url
        else:
            print(f"❌ Imgur upload failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Exception during upload: {e}")
        return None


def upload_multiple(image_paths, client_id=None):
    """
    Upload multiple images to Imgur
    
    Args:
        image_paths: List of image paths
        client_id: Imgur Client ID (optional)
        
    Returns:
        dict: {filename: url} mapping
        
    Example:
        urls = upload_multiple(["frame1.jpg", "frame2.jpg"])
        # Returns: {"frame1.jpg": "https://...", "frame2.jpg": "https://..."}
    """
    results = {}
    
    for path in image_paths:
        path = Path(path)
        url = upload_to_imgur(path, client_id)
        if url:
            results[path.name] = url
        else:
            results[path.name] = None
    
    return results


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python imgur_upload.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print(f"Uploading: {image_path}")
    url = upload_to_imgur(image_path)
    
    if url:
        print(f"✅ Success: {url}")
    else:
        print("❌ Failed")