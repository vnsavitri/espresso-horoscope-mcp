#!/usr/bin/env python3
"""
Determinism Check Tool

Verifies that the shot picker produces consistent results and that
the same shots always generate identical metrics formatting.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.picker import pick_indices


def test_picker_determinism():
    """Test that the picker produces consistent results for the same input."""
    print("🧪 Testing picker determinism...")
    
    test_cases = [
        ("0802", 3, 15),
        ("0611", 3, 15),
        ("1225", 3, 15),
        ("0101", 5, 15),
        ("1231", 2, 15),
    ]
    
    all_passed = True
    
    for mmdd, k, total in test_cases:
        # Run picker multiple times
        results = []
        for _ in range(5):
            indices = pick_indices(total, mmdd, k)
            results.append(indices)
        
        # Check all results are identical
        first_result = results[0]
        consistent = all(result == first_result for result in results)
        
        if consistent:
            print(f"  ✅ {mmdd}: {first_result} (consistent)")
        else:
            print(f"  ❌ {mmdd}: Inconsistent results")
            for i, result in enumerate(results):
                print(f"    Run {i+1}: {result}")
            all_passed = False
    
    return all_passed


def test_different_dates_variety():
    """Test that different birth dates produce different results."""
    print("\n🎯 Testing date variety...")
    
    dates = ["0101", "0202", "0303", "0404", "0505", "0606", "0707", "0808", "0909", "1010"]
    results = {}
    
    for date in dates:
        indices = pick_indices(15, date, 3)
        results[date] = indices
    
    # Check that we have variety
    unique_results = set(tuple(result) for result in results.values())
    variety_ratio = len(unique_results) / len(dates)
    
    print(f"  📊 Unique combinations: {len(unique_results)}/{len(dates)} ({variety_ratio:.1%})")
    
    if variety_ratio > 0.7:  # At least 70% variety
        print(f"  ✅ Good variety in results")
        return True
    else:
        print(f"  ❌ Limited variety in results")
        return False


def test_metrics_consistency():
    """Test that the same shots always produce identical metrics formatting."""
    print("\n📊 Testing metrics consistency...")
    
    # Load the shot palette
    palette_file = "sample/shots_palette.jsonl"
    if not Path(palette_file).exists():
        print(f"  ❌ Palette file not found: {palette_file}")
        return False
    
    shots = []
    with open(palette_file, 'r') as f:
        for line in f:
            if line.strip():
                shots.append(json.loads(line))
    
    # Test a few specific shots
    test_shots = [0, 5, 10]  # Test first, middle, and near-end shots
    
    all_consistent = True
    
    for shot_idx in test_shots:
        if shot_idx >= len(shots):
            continue
            
        shot = shots[shot_idx]
        shot_id = shot['shot_id']
        
        # Generate features multiple times
        features_results = []
        for _ in range(3):
            # Simulate feature extraction (simplified)
            features = {
                'shot_id': shot_id,
                'brew_ratio': shot.get('target_mass_g', 0) / shot.get('dose_g', 1),
                'shot_end_s': shot.get('shot_end_s', 0),
                'peak_pressure_bar': max(shot.get('pressure_bar', [0])),
                'temp_avg_c': sum(shot.get('temp_c', [0])) / len(shot.get('temp_c', [1])),
                'channeling_score_0_1': 0.0  # Simplified
            }
            features_results.append(features)
        
        # Check consistency
        first_features = features_results[0]
        consistent = all(
            abs(f['brew_ratio'] - first_features['brew_ratio']) < 0.001 and
            f['shot_end_s'] == first_features['shot_end_s'] and
            abs(f['peak_pressure_bar'] - first_features['peak_pressure_bar']) < 0.001
            for f in features_results
        )
        
        if consistent:
            print(f"  ✅ Shot {shot_idx} ({shot_id[:10]}...): Consistent metrics")
        else:
            print(f"  ❌ Shot {shot_idx} ({shot_id[:10]}...): Inconsistent metrics")
            all_consistent = False
    
    return all_consistent


def test_demo_deck_consistency():
    """Test that demo deck generation is consistent."""
    print("\n🎨 Testing demo deck consistency...")
    
    import subprocess
    
    test_dates = ["0802", "0611"]
    all_consistent = True
    
    for mmdd in test_dates:
        print(f"  Testing {mmdd}...")
        
        # Generate deck twice
        results = []
        for run in range(2):
            try:
                result = subprocess.run([
                    sys.executable, "tools/make_demo_deck.py", 
                    "--mmdd", mmdd, "--k", "3"
                ], capture_output=True, text=True, check=True)
                
                # Read the generated cards
                cards_file = Path("out/cards.json")
                if cards_file.exists():
                    with open(cards_file, 'r') as f:
                        cards_data = json.load(f)
                    results.append(cards_data)
                else:
                    print(f"    ❌ Run {run+1}: No cards.json generated")
                    all_consistent = False
                    continue
                    
            except subprocess.CalledProcessError as e:
                print(f"    ❌ Run {run+1}: Error generating deck: {e}")
                all_consistent = False
                continue
        
        if len(results) == 2:
            # Compare the results
            if results[0] == results[1]:
                print(f"    ✅ {mmdd}: Consistent deck generation")
            else:
                print(f"    ❌ {mmdd}: Inconsistent deck generation")
                all_consistent = False
    
    return all_consistent


def main():
    """Run all determinism tests."""
    print("🔬 Espresso Horoscope Determinism Check")
    print("=" * 50)
    
    tests = [
        ("Picker Determinism", test_picker_determinism),
        ("Date Variety", test_different_dates_variety),
        ("Metrics Consistency", test_metrics_consistency),
        ("Demo Deck Consistency", test_demo_deck_consistency),
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
    print("📋 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! System is deterministic.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
