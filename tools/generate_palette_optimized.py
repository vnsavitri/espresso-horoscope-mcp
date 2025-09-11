#!/usr/bin/env python3
"""
Optimized shot palette generator.
Uses modular approach for better performance and maintainability.
"""

import json
import random
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.shot_generator import create_shot_data

def generate_shot_palette(count: int = 75) -> List[Dict[str, Any]]:
    """Generate a diverse palette of espresso shots."""
    patterns = ["sweet_spot", "fast", "slow", "choke", "channel"]
    weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Sweet spot most common
    
    shots = []
    for i in range(count):
        pattern = random.choices(patterns, weights=weights)[0]
        shot_id = f"shot_{i+1:03d}"
        shot_data = create_shot_data(pattern, shot_id)
        shots.append(shot_data)
    
    return shots

def main():
    """Generate and save shot palette."""
    print("🎯 Generating optimized shot palette...")
    shots = generate_shot_palette(75)
    
    # Save to JSONL
    with open("sample/shots_palette_optimized.jsonl", "w") as f:
        for shot in shots:
            f.write(json.dumps(shot) + "\n")
    
    print(f"✅ Generated {len(shots)} shots in optimized format")
    print("📁 Saved to: sample/shots_palette_optimized.jsonl")

if __name__ == "__main__":
    main()
