# helpers/cost_calculator.py
"""
Cost calculator for Comfy.icu API
Estimates credits and USD cost based on parameters
"""

def estimate_comfy_icu_cost(params):
    """
    Estimate cost for Comfy.icu generation
    
    Args:
        params: Dict with generation parameters
            - fps: Frames per second (default: 16)
            - duration: Duration in seconds (default: 4)
            - width: Width in pixels (default: 672)
            - height: Height in pixels (default: 896)
            - steps: Sampling steps (default: 20)
            
    Returns:
        Dict with cost estimation:
            - credits: Estimated credits
            - cost_usd: Cost in USD
            - frames: Total frames
            - pixels: Pixels per frame
            - estimated_time_min: Estimated generation time in minutes
            
    Pricing (approximate, based on Comfy.icu):
        - Base: ~4000 credits for 96 frames @ 464x688 @ 20 steps
        - 10,000 credits = $1 USD
        - H100 GPU: ~1 second per frame
        
    Example:
        cost = estimate_comfy_icu_cost({
            'fps': 16,
            'duration': 4,
            'width': 672,
            'height': 896,
            'steps': 20
        })
        print(f"Cost: ${cost['cost_usd']}")
    """
    
    # Extract params with defaults
    fps = params.get('fps', 16)
    duration = params.get('duration', 4)
    width = params.get('width', 672)
    height = params.get('height', 896)
    steps = params.get('steps', 20)
    
    # Calculate total frames
    frames = fps * duration
    
    # Calculate pixels per frame
    pixels = width * height
    
    # ========================================
    # Pricing model (based on empirical data)
    # ========================================
    
    # Base pricing point (observed from Comfy.icu)
    base_credits = 4000
    base_frames = 96
    base_pixels = 464 * 688  # ~319,232
    base_steps = 20
    
    # Scale by frames
    credits_frames = base_credits * (frames / base_frames)
    
    # Scale by pixels (complexity increases with resolution)
    credits_pixels = credits_frames * (pixels / base_pixels)
    
    # Scale by steps (linear relationship)
    credits_steps = credits_pixels * (steps / base_steps)
    
    # Final credits estimate
    credits = round(credits_steps)
    
    # Convert to USD (10,000 credits = $1)
    cost_usd = round(credits / 10000, 2)
    
    # Estimate generation time (H100: ~1-2 seconds per frame)
    # More conservative estimate: 1.5s per frame
    estimated_time_sec = frames * 1.5
    estimated_time_min = round(estimated_time_sec / 60, 1)
    
    return {
        'credits': credits,
        'cost_usd': cost_usd,
        'frames': frames,
        'pixels': pixels,
        'resolution': f"{width}x{height}",
        'estimated_time_min': estimated_time_min,
        'steps': steps,
    }


def estimate_batch_cost(transitions_list):
    """
    Estimate total cost for batch of transitions
    
    Args:
        transitions_list: List of dicts with params for each transition
        
    Returns:
        Dict with total estimation:
            - total_credits: Sum of all credits
            - total_cost_usd: Sum of all costs
            - total_frames: Sum of all frames
            - total_time_min: Sum of all generation times
            - per_transition: List of individual estimates
            
    Example:
        transitions = [
            {'fps': 16, 'duration': 4, 'width': 672, 'height': 896},
            {'fps': 16, 'duration': 3, 'width': 672, 'height': 896},
        ]
        
        batch = estimate_batch_cost(transitions)
        print(f"Total: ${batch['total_cost_usd']}")
    """
    
    estimates = []
    
    total_credits = 0
    total_cost_usd = 0
    total_frames = 0
    total_time_min = 0
    
    for params in transitions_list:
        est = estimate_comfy_icu_cost(params)
        estimates.append(est)
        
        total_credits += est['credits']
        total_cost_usd += est['cost_usd']
        total_frames += est['frames']
        total_time_min += est['estimated_time_min']
    
    return {
        'total_credits': total_credits,
        'total_cost_usd': round(total_cost_usd, 2),
        'total_frames': total_frames,
        'total_time_min': round(total_time_min, 1),
        'count': len(transitions_list),
        'per_transition': estimates,
        'avg_cost_usd': round(total_cost_usd / len(transitions_list), 2) if transitions_list else 0,
    }


def compare_local_vs_cloud(params, local_time_per_frame=8):
    """
    Compare local vs cloud costs and times
    
    Args:
        params: Generation params
        local_time_per_frame: Local generation time (minutes per transition)
            Default: 8 min for 64 frames @ 672x896
            
    Returns:
        Dict with comparison
        
    Example:
        comparison = compare_local_vs_cloud({
            'fps': 16, 'duration': 4, 'width': 672, 'height': 896
        })
        print(f"Cloud: ${comparison['cloud']['cost_usd']}")
        print(f"Local: $0 (FREE)")
    """
    
    cloud = estimate_comfy_icu_cost(params)
    
    frames = params.get('fps', 16) * params.get('duration', 4)
    
    # Local time estimate (scale from base)
    base_frames = 64
    local_time = local_time_per_frame * (frames / base_frames)
    
    return {
        'cloud': {
            'cost_usd': cloud['cost_usd'],
            'time_min': cloud['estimated_time_min'],
            'speed': 'H100 GPU',
        },
        'local': {
            'cost_usd': 0.0,
            'time_min': round(local_time, 1),
            'speed': 'RTX 4090 (estimated)',
        },
        'savings_usd': cloud['cost_usd'],
        'time_difference_min': round(local_time - cloud['estimated_time_min'], 1),
        'cloud_faster': local_time > cloud['estimated_time_min'],
    }


# Test
if __name__ == "__main__":
    # Test single transition
    params = {
        'fps': 16,
        'duration': 4,
        'width': 672,
        'height': 896,
        'steps': 20,
    }
    
    cost = estimate_comfy_icu_cost(params)
    
    print("Single transition estimate:")
    print(f"  Resolution: {cost['resolution']}")
    print(f"  Frames: {cost['frames']}")
    print(f"  Credits: {cost['credits']:,}")
    print(f"  Cost: ${cost['cost_usd']}")
    print(f"  Time: ~{cost['estimated_time_min']} min")
    
    print("\nComparison (local vs cloud):")
    comp = compare_local_vs_cloud(params)
    print(f"  Cloud: ${comp['cloud']['cost_usd']}, ~{comp['cloud']['time_min']} min")
    print(f"  Local: $0, ~{comp['local']['time_min']} min")
    print(f"  Time savings: {comp['time_difference_min']} min" if comp['cloud_faster'] else f"  Time cost: {abs(comp['time_difference_min'])} min")