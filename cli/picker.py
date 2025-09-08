#!/usr/bin/env python3
"""
Deterministic Shot Picker

Selects a subset of shots from a palette based on birth date (MMDD).
Uses stable hashing to ensure same birth date always gets same shots.
"""

import hashlib
import random
from typing import List


def pick_indices(n_total: int, mmdd: str, k: int = 3) -> List[int]:
    """
    Pick k unique indices from range [0, n_total) using deterministic hashing.
    
    Args:
        n_total: Total number of shots available
        mmdd: Birth date in MMDD format (e.g., "0802")
        k: Number of shots to pick (default 3)
    
    Returns:
        List of k unique indices
    """
    if n_total == 0:
        return []
    
    if k >= n_total:
        # If we want more shots than available, return all indices
        return list(range(n_total))
    
    # Create deterministic seed from birth date
    seed_bytes = hashlib.sha256(mmdd.encode('utf-8')).digest()
    seed = int.from_bytes(seed_bytes[:8], byteorder='big')
    
    # Use seeded random to ensure reproducibility
    rng = random.Random(seed)
    
    # Sample k unique indices
    indices = rng.sample(range(n_total), k)
    
    return sorted(indices)


def pick_shots_from_palette(palette_file: str, mmdd: str, k: int = 3) -> List[dict]:
    """
    Pick k shots from a palette file based on birth date.
    
    Args:
        palette_file: Path to JSONL file containing shot palette
        mmdd: Birth date in MMDD format
        k: Number of shots to pick
    
    Returns:
        List of selected shot data
    """
    import json
    from pathlib import Path
    
    # Read all shots from palette
    shots = []
    with open(palette_file, 'r') as f:
        for line in f:
            if line.strip():
                shots.append(json.loads(line))
    
    # Pick indices
    indices = pick_indices(len(shots), mmdd, k)
    
    # Return selected shots
    return [shots[i] for i in indices]


def main():
    """CLI interface for testing the picker."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test deterministic shot picker")
    parser.add_argument("--mmdd", required=True, help="Birth date in MMDD format")
    parser.add_argument("--k", type=int, default=3, help="Number of shots to pick")
    parser.add_argument("--total", type=int, default=15, help="Total number of shots available")
    
    args = parser.parse_args()
    
    # Test the picker
    indices = pick_indices(args.total, args.mmdd, args.k)
    
    print(f"🎯 Picking {args.k} shots for birth date {args.mmdd}")
    print(f"📊 Available shots: {args.total}")
    print(f"🎲 Selected indices: {indices}")
    
    # Test reproducibility
    indices2 = pick_indices(args.total, args.mmdd, args.k)
    print(f"🔄 Reproducibility test: {indices2}")
    print(f"✅ Same result: {indices == indices2}")


if __name__ == "__main__":
    main()
