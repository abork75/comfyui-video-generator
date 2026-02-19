# -*- coding: utf-8 -*-
"""
Test Flow Parser - Chain expansion
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from flow_parser import parse_flow

# ============================================================
# TEST FLOW
# ============================================================

FLOW = [
    # === Starting point: Image ===
    {
        "file": "01_ewelina_sit.jpg",
    },
    
    # === CHAIN: 3-step sequence ===
    {
        "chain": [
            {"duration": 3, "pos": "stands up"},
            {"duration": 2, "pos": "waves"},
            {"duration": 2, "pos": "shy face"},
        ],
        "chain_prefix": "ewelina_stands",
        "backend": "local",
        "fps": 16,
    },
    
    # === File B ===
    {"file": "02_ewelina_braOFF.mp4"},
    
    {"break": True},  # Hard cut
    
    # === Transition 2: Video→Image (LOCAL) ===
    {
        "file": "03._ewelina_panties_off.mp4",
        "backend": "local",
        "duration": 4,
        "pos": "[video_to_image]",
        "neg": "[video_to_image]",
    },
    
    # === File D ===
    {"file": "04_ewelina_out.png"},
]

# ============================================================
# PARSE
# ============================================================

print("="*70)
print("FLOW PARSER TEST - Chain Expansion")
print("="*70)
print()

parser = parse_flow(FLOW)

# ============================================================
# PRINT SUMMARY
# ============================================================

parser.print_summary()

print()
print("="*70)
print("DETAILED BREAKDOWN")
print("="*70)
print()

# ============================================================
# ALL FILES
# ============================================================

print("─"*70)
print("📁 ALL FILES")
print("─"*70)

for i, flow_file in enumerate(parser.get_all_files(), 1):
    icon = "📷" if flow_file.is_image() else "🎬"
    chain_marker = "⛓️ " if flow_file.config.get('_is_chain') else ""
    
    print(f"{i:2d}. {icon} {chain_marker}{flow_file.filename}")
    
    if flow_file.config.get('_is_chain'):
        step = flow_file.config.get('_chain_step')
        total = flow_file.config.get('_chain_total')
        prefix = flow_file.config.get('_chain_prefix')
        print(f"    Chain: {prefix} (step {step}/{total})")
    
    # Show config (without metadata)
    clean_config = {k: v for k, v in flow_file.config.items() if not k.startswith('_')}
    if clean_config:
        print(f"    Config: {clean_config}")
    
    print()

# ============================================================
# TRANSITIONS
# ============================================================

print("─"*70)
print("🔗 TRANSITIONS")
print("─"*70)

for i, pair in enumerate(parser.get_transition_pairs(), 1):
    from_chain = "⛓️ " if pair.from_config.get('_is_chain') else ""
    to_chain = "⛓️ " if pair.to_config.get('_is_chain') else ""
    
    print(f"{i:2d}. {from_chain}{pair.from_file}")
    print(f"     ↓")
    print(f"    {to_chain}{pair.to_file}")
    print(f"    Output: {pair.get_transition_name()}")
    
    # Show to_config (user settings)
    clean_config = {k: v for k, v in pair.to_config.items() if not k.startswith('_')}
    if clean_config:
        print(f"    Config: {clean_config}")
    
    print()

# ============================================================
# SEGMENTS
# ============================================================

print("─"*70)
print("📑 SEGMENTS")
print("─"*70)

for i, segment in enumerate(parser.segments, 1):
    print(f"Segment {i}:")
    print(f"  Files: {len(segment.files)}")
    print(f"  Transitions: {len(segment.transitions)}")
    print(f"  Files list:")
    
    for flow_file in segment.files:
        chain_marker = "⛓️ " if flow_file.config.get('_is_chain') else "  "
        print(f"    {chain_marker} {flow_file.filename}")
    
    print()

# ============================================================
# VALIDATION
# ============================================================

print("="*70)
print("✅ VALIDATION")
print("="*70)
print()

errors = []

# Check: 'file' key should NOT be in configs
for flow_file in parser.get_all_files():
    if 'file' in flow_file.config:
        errors.append(f"❌ File '{flow_file.filename}' has 'file' key in config!")

# Check: chain files should have metadata
for flow_file in parser.get_all_files():
    if flow_file.config.get('_is_chain'):
        required = ['_chain_prefix', '_chain_step', '_chain_total']
        for key in required:
            if key not in flow_file.config:
                errors.append(f"❌ Chain file '{flow_file.filename}' missing '{key}'")

# Check: chain filenames match pattern
for flow_file in parser.get_all_files():
    if flow_file.config.get('_is_chain'):
        prefix = flow_file.config.get('_chain_prefix')
        step = flow_file.config.get('_chain_step')
        expected = f"{prefix}_{step:03d}.mp4"
        
        if flow_file.filename != expected:
            errors.append(f"❌ Chain filename mismatch: got '{flow_file.filename}', expected '{expected}'")

# Check: transition count
expected_transitions = len(parser.get_all_files()) - 1 - 1  # -1 for total, -1 for break
actual_transitions = len(parser.get_transition_pairs())

if actual_transitions != expected_transitions:
    errors.append(f"❌ Transition count mismatch: got {actual_transitions}, expected {expected_transitions}")

# Print results
if errors:
    for error in errors:
        print(error)
else:
    print("✅ All validations passed!")
    print()
    print(f"  ✓ No 'file' keys in configs")
    print(f"  ✓ Chain metadata complete")
    print(f"  ✓ Chain filenames correct")
    print(f"  ✓ Transition count correct ({actual_transitions})")

print()
print("="*70)
print("TEST COMPLETE")
print("="*70)