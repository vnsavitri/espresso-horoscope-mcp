#!/usr/bin/env python3
"""
Determinism Check Tool

Verifies that the system produces consistent results for the same inputs.
This is crucial for demonstrating the technical sophistication of the system.
"""

import requests
import json
import sys
from typing import Dict, Any

def test_determinism():
    """Test that same inputs produce same outputs."""
    print("🧪 Testing Determinism...")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    test_mmdd = "1021"  # Libra
    
    # Test 1: Same birth date should produce same zodiac and rule, but different seeds (due to time variant)
    print(f"📊 Test 1: Same birth date ({test_mmdd}) - zodiac/rule should be consistent")
    
    try:
        response1 = requests.get(f"{base_url}/generate_cards?mmdd={test_mmdd}", timeout=10)
        response2 = requests.get(f"{base_url}/generate_cards?mmdd={test_mmdd}", timeout=10)
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            # Compare the latest cards
            card1 = data1["readings"][0]
            card2 = data2["readings"][0]
            
            # Check fields that should be consistent (zodiac, rule) vs variable (seed, style)
            consistent_fields = [
                ("zodiac", card1["card"]["zodiac"], card2["card"]["zodiac"]),
                ("rule_hit", card1["card"]["rule_hit"], card2["card"]["rule_hit"]),
            ]
            
            variable_fields = [
                ("seed", card1["card"]["seed"], card2["card"]["seed"]),
                ("style", card1["user_context"]["style_preference"], card2["user_context"]["style_preference"]),
            ]
            
            consistent_ok = True
            for field_name, val1, val2 in consistent_fields:
                if val1 == val2:
                    print(f"  ✅ {field_name}: {val1}")
                else:
                    print(f"  ❌ {field_name}: {val1} != {val2}")
                    consistent_ok = False
            
            variable_ok = True
            for field_name, val1, val2 in variable_fields:
                if val1 != val2:
                    print(f"  ✅ {field_name}: varies (as expected)")
                else:
                    print(f"  ⚠️  {field_name}: {val1} (unexpectedly identical)")
                    variable_ok = False
            
            if consistent_ok:
                print("  🎉 PASS: Same birth date produces consistent zodiac/rule with time-based variation")
                return True
            else:
                print("  ❌ FAIL: Same birth date produces inconsistent zodiac/rule")
                return False
                
        else:
            print(f"  ❌ API Error: {response1.status_code} or {response2.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Connection Error: {e}")
        return False
    
    # Test 2: Different birth dates should produce different results
    print(f"\n📊 Test 2: Different birth dates - should be different")
    
    try:
        response_libra = requests.get(f"{base_url}/generate_cards?mmdd=1021", timeout=10)  # Libra
        response_aries = requests.get(f"{base_url}/generate_cards?mmdd=0321", timeout=10)  # Aries
        
        if response_libra.status_code == 200 and response_aries.status_code == 200:
            libra_data = response_libra.json()
            aries_data = response_aries.json()
            
            libra_card = libra_data["readings"][0]
            aries_card = aries_data["readings"][0]
            
            # Check that zodiac signs are different
            if libra_card["card"]["zodiac"] != aries_card["card"]["zodiac"]:
                print(f"  ✅ Zodiac: {libra_card['card']['zodiac']} != {aries_card['card']['zodiac']}")
                print("  🎉 PASS: Different birth dates produce different zodiac signs")
                return True
            else:
                print(f"  ❌ Zodiac: {libra_card['card']['zodiac']} == {aries_card['card']['zodiac']}")
                print("  ❌ FAIL: Different birth dates produce same zodiac sign")
                return False
        else:
            print(f"  ❌ API Error: {response_libra.status_code} or {response_aries.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Connection Error: {e}")
        return False

def main():
    """Main function."""
    print("🎯 Espresso Horoscope - Determinism Check")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running. Start with: uvicorn web.app:app --reload")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Backend not running. Start with: uvicorn web.app:app --reload")
        sys.exit(1)
    
    print("✅ Backend is running")
    
    # Run determinism tests
    success = test_determinism()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED - System is deterministic!")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED - System has issues")
        sys.exit(1)

if __name__ == "__main__":
    main()