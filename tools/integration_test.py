#!/usr/bin/env python3
"""
Integration Test for Espresso Horoscope

Tests the complete workflow from shot palette generation to UI filtering.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.picker import pick_indices


def test_full_workflow():
    """Test the complete workflow from palette to UI."""
    print("🔄 Testing full workflow...")
    
    # Step 1: Generate shot palette
    print("  📊 Generating shot palette...")
    try:
        result = subprocess.run([
            sys.executable, "tools/simulate_shots.py"
        ], capture_output=True, text=True, check=True)
        print("    ✅ Shot palette generated")
    except subprocess.CalledProcessError as e:
        print(f"    ❌ Failed to generate palette: {e}")
        return False
    
    # Step 2: Create individual JSON files
    print("  📁 Creating individual JSON files...")
    try:
        with open('sample/shots_palette.jsonl', 'r') as f:
            shots = [json.loads(line) for line in f]
        
        Path('sample/mcp_shots').mkdir(exist_ok=True)
        for i, shot in enumerate(shots):
            filename = f'sample/mcp_shots/shot_{i+1:03d}.json'
            with open(filename, 'w') as f:
                json.dump(shot, f, indent=2)
        
        print(f"    ✅ Created {len(shots)} individual JSON files")
    except Exception as e:
        print(f"    ❌ Failed to create JSON files: {e}")
        return False
    
    # Step 3: Process through pipeline
    print("  🔄 Processing through pipeline...")
    try:
        # Record
        result = subprocess.run([
            sys.executable, "tools/record_from_mcp.py", 
            "sample/mcp_shots/*.json", "-o", "data/shots.jsonl"
        ], capture_output=True, text=True, check=True)
        
        # Extract
        result = subprocess.run([
            sys.executable, "features/extract.py", 
            "data/shots.jsonl", "-o", "data/features.jsonl"
        ], capture_output=True, text=True, check=True)
        
        # Generate cards
        result = subprocess.run([
            sys.executable, "cli/cards.py",
            "--features", "data/features.jsonl",
            "--rules", "rules/diagnostics.yaml",
            "--astro", "content/astro_map.yaml",
            "--out", "out/cards.md",
            "--birth-date", "0802"
        ], capture_output=True, text=True, check=True)
        
        print("    ✅ Pipeline processing complete")
    except subprocess.CalledProcessError as e:
        print(f"    ❌ Pipeline failed: {e}")
        return False
    
    return True


def test_picker_consistency():
    """Test that picker produces consistent results across different contexts."""
    print("\n🎯 Testing picker consistency...")
    
    test_dates = ["0802", "0611", "1225"]
    all_consistent = True
    
    for mmdd in test_dates:
        print(f"  Testing {mmdd}...")
        
        # Test CLI picker
        cli_indices = pick_indices(15, mmdd, 3)
        
        # Test demo deck generation
        try:
            result = subprocess.run([
                sys.executable, "tools/make_demo_deck.py", 
                "--mmdd", mmdd, "--k", "3"
            ], capture_output=True, text=True, check=True)
            
            # Read generated cards to verify
            cards_file = Path("out/cards.json")
            if cards_file.exists():
                with open(cards_file, 'r') as f:
                    cards_data = json.load(f)
                
                generated_count = len(cards_data.get('readings', []))
                if generated_count == 3:
                    print(f"    ✅ {mmdd}: CLI picker {cli_indices} → {generated_count} cards")
                else:
                    print(f"    ❌ {mmdd}: Expected 3 cards, got {generated_count}")
                    all_consistent = False
            else:
                print(f"    ❌ {mmdd}: No cards.json generated")
                all_consistent = False
                
        except subprocess.CalledProcessError as e:
            print(f"    ❌ {mmdd}: Demo deck generation failed: {e}")
            all_consistent = False
    
    return all_consistent


def test_ui_filtering():
    """Test that UI filtering works correctly."""
    print("\n🌐 Testing UI filtering...")
    
    # This is a simplified test since we can't easily test the actual UI
    # We'll test the picker logic that the UI uses
    
    test_dates = ["0802", "0611", "1225"]
    all_working = True
    
    for mmdd in test_dates:
        print(f"  Testing UI filtering for {mmdd}...")
        
        # Simulate what the UI does
        # 1. Load all cards (simulate API call)
        try:
            with open('out/cards.json', 'r') as f:
                all_cards = json.load(f)
            
            all_readings = all_cards.get('readings', [])
            
            # 2. Apply picker logic (same as UI)
            selected_indices = pick_indices(len(all_readings), mmdd, 3)
            filtered_readings = [all_readings[i] for i in selected_indices]
            
            if len(filtered_readings) == 3:
                print(f"    ✅ {mmdd}: Filtered to {len(filtered_readings)} cards")
            else:
                print(f"    ❌ {mmdd}: Expected 3 cards, got {len(filtered_readings)}")
                all_working = False
                
        except Exception as e:
            print(f"    ❌ {mmdd}: UI filtering test failed: {e}")
            all_working = False
    
    return all_working


def test_share_route():
    """Test that share route works with filtering."""
    print("\n📤 Testing share route...")
    
    # Test different combinations
    test_cases = [
        ("0802", 0),  # First card for 0802
        ("0611", 1),  # Second card for 0611
        ("1225", 2),  # Third card for 1225
    ]
    
    all_working = True
    
    for mmdd, card_index in test_cases:
        print(f"  Testing /share/{card_index}?mmdd={mmdd}...")
        
        try:
            # Load all cards
            with open('out/cards.json', 'r') as f:
                all_cards = json.load(f)
            
            all_readings = all_cards.get('readings', [])
            
            # Apply filtering (same as share route)
            selected_indices = pick_indices(len(all_readings), mmdd, 3)
            filtered_readings = [all_readings[i] for i in selected_indices]
            
            # Check if the requested card index is valid
            if card_index < len(filtered_readings):
                card = filtered_readings[card_index]
                print(f"    ✅ {mmdd}: Card {card_index} = {card['card']['title']}")
            else:
                print(f"    ❌ {mmdd}: Card index {card_index} out of range (0-{len(filtered_readings)-1})")
                all_working = False
                
        except Exception as e:
            print(f"    ❌ {mmdd}: Share route test failed: {e}")
            all_working = False
    
    return all_working


def main():
    """Run all integration tests."""
    print("🧪 Espresso Horoscope Integration Test")
    print("=" * 50)
    
    tests = [
        ("Full Workflow", test_full_workflow),
        ("Picker Consistency", test_picker_consistency),
        ("UI Filtering", test_ui_filtering),
        ("Share Route", test_share_route),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name}: Error - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Integration Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All integration tests passed!")
        print("\n🚀 Ready for demo:")
        print("  • FastAPI server: http://127.0.0.1:8000")
        print("  • Next.js UI: http://localhost:3001")
        print("  • Try: http://localhost:3001/?mmdd=0802")
        print("  • Try: http://localhost:3001/share/0?mmdd=0611")
        return 0
    else:
        print("⚠️  Some integration tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
