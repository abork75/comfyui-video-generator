# -*- coding: utf-8 -*-
"""
EVALUATE MODE - Cost estimation only (NO generation!)
Quick check ile kosztowałoby cloud generation
"""

from helpers.cost_calculator import estimate_comfy_icu_cost, estimate_batch_cost, compare_local_vs_cloud

# ============================================================
# KONFIGURACJA - DOSTOSUJ DO SWOJEGO PROJEKTU!
# ============================================================

# C:\Users\abork\AppData\Local\CapCut\Videos\klub_pliki\mixed_story
PROJECT_NAME = "mixed_story"

# FLOW z RUN_adv_001 (dla porównania)
FLOW = [
    {"file": "01_ewelina_sit.jpg", "duration": 2},      # → transition do 02
    {"file": "02_ewelina_braOFF.mp4"},                   # BREAK po tym
    {"break": True},                                     # Hard cut
    {"file": "03._ewlina_panties_off.mp4", "duration": 4},  # → transition do 04
    {"file": "04_ewlina_out.png"},                       # Ostatni
]

# Resolution (jak w RUN_adv_001)
MIN_WIDTH = 672
MIN_HEIGHT = 896

# Defaults (jak w RUN_adv_001)
DEFAULT_DURATION = 4
DEFAULT_FPS = 16
DEFAULT_STEPS = 20

# ============================================================
# OBLICZ TRANSITIONS (pomijając breaks)
# ============================================================

transitions = []

# Symuluj parsowanie FLOW (uproszczone - bez generics)
items = [item for item in FLOW if not item.get("break", False)]

for i in range(len(items) - 1):
    item = items[i]
    
    # Duration - użyj custom lub default
    duration = item.get("duration", DEFAULT_DURATION)
    
    transitions.append({
        'fps': DEFAULT_FPS,
        'duration': duration,
        'width': MIN_WIDTH,
        'height': MIN_HEIGHT,
        'steps': DEFAULT_STEPS,
    })

# Usuń transition po break (02 → 03)
# W Twoim FLOW:
# items[0] = 01_ewelina_sit.jpg → transition do items[1]
# items[1] = 02_ewelina_braOFF.mp4 → BREAK (nie ma transition)
# items[2] = 03._ewlina_panties_off.mp4 → transition do items[3]

# Więc mamy 2 transitions:
# - 01 → 02 (duration=2)
# - 03 → 04 (duration=4)

# Ale powyższa pętla zrobi 3 transitions, więc poprawmy:

transitions = []

# Transition 1: 01 → 02 (duration=2)
transitions.append({
    'fps': DEFAULT_FPS,
    'duration': 2,
    'width': MIN_WIDTH,
    'height': MIN_HEIGHT,
    'steps': DEFAULT_STEPS,
})

# Transition 2: BRAK (break)

# Transition 3: 03 → 04 (duration=4)
transitions.append({
    'fps': DEFAULT_FPS,
    'duration': 4,
    'width': MIN_WIDTH,
    'height': MIN_HEIGHT,
    'steps': DEFAULT_STEPS,
})

# ============================================================
# ESTYMACJA
# ============================================================

print("\n" + "="*70)
print("💰 COST ESTIMATION - CLOUD GENERATION")
print("="*70)

batch_cost = estimate_batch_cost(transitions)

print(f"\nProject: {PROJECT_NAME}")
print(f"Transitions: {batch_cost['count']}")
print(f"Resolution: {MIN_WIDTH}x{MIN_HEIGHT}")
print(f"Total frames: {batch_cost['total_frames']}")
print()

print("Per transition:")
for i, est in enumerate(batch_cost['per_transition'], 1):
    print(f"  [{i}] Duration: {est['frames'] // DEFAULT_FPS}s ({est['frames']} frames)")
    print(f"      Resolution: {est['resolution']}")
    print(f"      Credits: {est['credits']:,}")
    print(f"      Cost: ${est['cost_usd']}")
    print(f"      Time: ~{est['estimated_time_min']} min")
    print()

print("-" * 70)
print(f"CLOUD TOTAL:")
print(f"  Total credits: {batch_cost['total_credits']:,}")
print(f"  Total cost: ${batch_cost['total_cost_usd']}")
print(f"  Avg per transition: ${batch_cost['avg_cost_usd']}")
print(f"  Total time: ~{batch_cost['total_time_min']:.0f} min")
print()

# Porównanie z local
local_time_per_transition = 8  # Twoje doświadczenie (średnio)
local_total_time = local_time_per_transition * batch_cost['count']

print(f"LOCAL TOTAL (for comparison):")
print(f"  Total cost: $0.00 (FREE)")
print(f"  Total time: ~{local_total_time} min")
print()

print("="*70)
print("COMPARISON:")
print(f"  💰 Money: Cloud costs ${batch_cost['total_cost_usd']} (Local FREE)")
print(f"  ⏱️  Time: Cloud saves {local_total_time - batch_cost['total_time_min']:.0f} min")
print(f"  🎯 Use case: Worth it for urgent/deadline, not for overnight batches")
print("="*70)

print("\n📌 NOTE: This is ESTIMATION only - no actual generation")
print("   To run actual cloud generation, use RUN_cloud_urgent.py")
print()

# Detailed comparison dla każdego transition
print("\n" + "="*70)
print("DETAILED COMPARISON (per transition):")
print("="*70)

for i, params in enumerate(transitions, 1):
    comp = compare_local_vs_cloud(params, local_time_per_frame=8)
    
    duration = params['duration']
    frames = params['fps'] * duration
    
    print(f"\n[{i}] Transition ({duration}s, {frames} frames):")
    print(f"  Cloud: ${comp['cloud']['cost_usd']}, ~{comp['cloud']['time_min']} min ({comp['cloud']['speed']})")
    print(f"  Local: ${comp['local']['cost_usd']}, ~{comp['local']['time_min']} min ({comp['local']['speed']})")
    print(f"  💡 Time savings: {comp['time_difference_min']} min" if comp['cloud_faster'] else f"  💡 Time cost: {abs(comp['time_difference_min'])} min")
    print(f"  💰 Money trade-off: ${comp['savings_usd']} (pay for speed)")

print("\n" + "="*70)