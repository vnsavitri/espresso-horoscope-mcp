#!/usr/bin/env python3
"""
Demo Deck Builder

Creates a user-specific deck of horoscope cards by selecting shots from the palette
and running them through the full pipeline.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.picker import pick_shots_from_palette


def get_user_birth_date() -> str:
    """Get user birth date from config file or prompt."""
    config_path = Path.home() / ".espresso_horoscope" / "config.yaml"
    
    if config_path.exists():
        try:
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                birth_mmdd = config.get('birth_mmdd')
                if birth_mmdd:
                    return birth_mmdd
        except Exception as e:
            print(f"Warning: Could not read config file: {e}")
    
    # Prompt for birth date
    while True:
        birth_input = input("Enter your birth date (MMDD format, e.g., 0802): ").strip()
        if len(birth_input) == 4 and birth_input.isdigit():
            month = int(birth_input[:2])
            day = int(birth_input[2:])
            if 1 <= month <= 12 and 1 <= day <= 31:
                return birth_input
        print("Invalid format. Please enter MMDD (e.g., 0802 for August 2nd)")


def create_demo_deck(mmdd: str, k: int = 3, generate_png: bool = False, png_dir: str = "out/png_cards", time_variant: str = None) -> None:
    """
    Create a demo deck for a specific user.
    
    Args:
        mmdd: Birth date in MMDD format
        k: Number of shots to include in deck
    """
    print(f"🎯 Creating demo deck for birth date {mmdd}")
    
    # Step 1: Pick shots from palette
    palette_file = "sample/shots_palette.jsonl"
    if not Path(palette_file).exists():
        print(f"❌ Error: Palette file not found: {palette_file}")
        print("Run 'python3 tools/simulate_shots.py' first to generate the palette")
        return
    
    selected_shots = pick_shots_from_palette(palette_file, mmdd, k, time_variant)
    print(f"📊 Selected {len(selected_shots)} shots from palette")
    
    # Step 2: Write selected shots to data/shots.jsonl
    shots_output = Path("data/shots.jsonl")
    shots_output.parent.mkdir(exist_ok=True)
    
    with open(shots_output, 'w') as f:
        for shot in selected_shots:
            f.write(json.dumps(shot) + '\n')
    
    print(f"💾 Wrote selected shots to {shots_output}")
    
    # Step 3: Extract features
    print("🔍 Extracting features...")
    try:
        result = subprocess.run([
            sys.executable, "features/extract.py", 
            str(shots_output), "-o", "data/features.jsonl"
        ], capture_output=True, text=True, check=True)
        print("✅ Features extracted successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error extracting features: {e}")
        print(f"stderr: {e.stderr}")
        return
    
    # Step 4: Generate cards
    print("🎨 Generating horoscope cards...")
    try:
        cmd = [
            sys.executable, "cli/cards.py",
            "--features", "data/features.jsonl",
            "--rules", "rules/diagnostics.yaml", 
            "--astro", "content/astro_map.yaml",
            "--out", "out/cards.md",
            "--birth-date", mmdd,
            "--style", "gptoss"
        ]
        
        # Add PNG generation arguments if requested
        if generate_png:
            cmd.extend(["--png", "--png-dir", png_dir])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Cards generated successfully")
        if generate_png:
            print(f"🖼️  PNG cards saved to {png_dir}/")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating cards: {e}")
        print(f"stderr: {e.stderr}")
        return
    
    # Step 5: Show summary
    print(f"\n🎉 Demo deck created successfully!")
    print(f"📁 Output files:")
    print(f"  - out/cards.md (Markdown cards)")
    print(f"  - out/cards.json (Structured data)")
    print(f"  - data/features.jsonl (Extracted features)")
    print(f"  - data/shots.jsonl (Selected shots)")
    
    # Show which shots were selected
    print(f"\n📊 Selected shots:")
    for i, shot in enumerate(selected_shots):
        print(f"  {i+1}. {shot['pattern']} → {shot['rule_hint']} (ID: {shot['shot_id']})")


def main():
    """CLI interface for demo deck builder."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create a user-specific demo deck")
    parser.add_argument("--mmdd", help="Birth date in MMDD format (if not provided, will prompt)")
    parser.add_argument("--k", type=int, default=1, help="Number of shots to include (default: 1)")
    parser.add_argument("--png", action="store_true", help="Generate PNG cards using Next.js API")
    parser.add_argument("--png-dir", default="out/png_cards", help="Directory to save PNG cards (default: out/png_cards)")
    parser.add_argument("--time-variant", help="Time variant for shot selection (e.g., '2025-09-09-14:30')")
    
    args = parser.parse_args()
    
    # Get birth date
    mmdd = args.mmdd
    if not mmdd:
        mmdd = get_user_birth_date()
    
    # Create demo deck
    create_demo_deck(mmdd, args.k, args.png, args.png_dir, args.time_variant)


if __name__ == "__main__":
    main()
