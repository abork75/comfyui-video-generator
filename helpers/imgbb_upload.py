# helpers/imgbb_upload.py
"""
ImgBB uploader for cloud API
Uploads images and returns public URLs for Comfy.icu
UPDATED: Returns delete_url for cleanup
"""

import requests
import os
from pathlib import Path

# ImgBB API key from environment variable
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY', '')

def upload_to_imgbb(image_path, api_key=None):
    """
    Upload image to ImgBB and return public URL + delete URL
    
    Args:
        image_path: Path to image file (str or Path)
        api_key: ImgBB API key (optional, uses env variable)
        
    Returns:
        dict: {'url': public_url, 'delete_url': delete_url} or None if failed
        
    Example:
        result = upload_to_imgbb("frame.jpg")
        # Returns: {'url': 'https://i.ibb.co/ABC123/frame.jpg', 
        #           'delete_url': 'https://ibb.co/delete/XYZ789'}
    """
    if api_key is None:
        api_key = IMGBB_API_KEY
    
    if not api_key:
        print("❌ Error: IMGBB_API_KEY not set!")
        print("   Set environment variable:")
        print("   PowerShell: $env:IMGBB_API_KEY = 'your_key'")
        print("   Bash: export IMGBB_API_KEY='your_key'")
        return None
    
    image_path = Path(image_path)
    
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return None
    
    url = "https://api.imgbb.com/1/upload"
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            params = {'key': api_key}
            response = requests.post(url, params=params, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                image_url = data['data']['url']
                delete_url = data['data']['delete_url']
                
                return {
                    'url': image_url,
                    'delete_url': delete_url,
                }
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                print(f"❌ Upload failed: {error_msg}")
                return None
        else:
            print(f"❌ ImgBB upload failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Exception during upload: {e}")
        return None


def delete_from_imgbb(delete_url):
    """
    Delete image from ImgBB using delete URL
    
    Args:
        delete_url: Delete URL returned from upload
        
    Returns:
        bool: True if success, False if failed
        
    Example:
        delete_from_imgbb("https://ibb.co/delete/XYZ789")
    """
    if not delete_url:
        return False
    
    try:
        response = requests.get(delete_url, timeout=10)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        return False


def upload_multiple(image_paths, api_key=None):
    """
    Upload multiple images to ImgBB
    
    Args:
        image_paths: List of image paths
        api_key: ImgBB API key (optional)
        
    Returns:
        dict: {filename: {'url': ..., 'delete_url': ...}} mapping
    """
    results = {}
    
    for path in image_paths:
        path = Path(path)
        result = upload_to_imgbb(path, api_key)
        results[path.name] = result
    
    return results


# Alias for backward compatibility with imgur naming
upload_to_imgur = upload_to_imgbb


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python imgbb_upload.py <image_path>")
        print("\nMake sure IMGBB_API_KEY environment variable is set:")
        print("  PowerShell: $env:IMGBB_API_KEY = 'your_key'")
        print("  Bash: export IMGBB_API_KEY='your_key'")
        print("\nGet your API key from: https://api.imgbb.com/")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print(f"Uploading: {image_path}")
    result = upload_to_imgbb(image_path)
    
    if result:
        print(f"✅ Success!")
        print(f"   URL: {result['url']}")
        print(f"   Delete URL: {result['delete_url']}")
        
        # Ask if user wants to test delete
        test_delete = input("\nTest delete? (yes/no): ")
        if test_delete.lower() == 'yes':
            if delete_from_imgbb(result['delete_url']):
                print("✅ Delete successful!")
            else:
                print("❌ Delete failed")
    else:
        print("❌ Failed")