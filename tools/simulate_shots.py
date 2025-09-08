#!/usr/bin/env python3
"""
Shot Simulator for Espresso Horoscope

Generates a diverse palette of espresso shots that trigger different diagnostic rules.
Each shot includes realistic telemetry data and metadata for rule targeting.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any


def generate_pressure_profile(pattern: str, duration_s: int) -> List[float]:
    """Generate realistic pressure profiles for different shot patterns."""
    profiles = {
        "sweet_spot": [0, 2, 6, 8.5, 9.1, 9.0, 8.8, 8.5, 8.2, 7.8, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0],
        "fast": [0, 1, 3, 5, 6, 6.5, 6.8, 7.0, 6.8, 6.5, 6.2, 5.8, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0],
        "slow": [0, 1, 3, 5, 7, 8, 8.5, 9.0, 9.2, 9.1, 9.0, 8.8, 8.6, 8.4, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.6, 6.4, 6.2, 6.0, 5.8, 5.6, 5.4, 5.2, 5.0, 4.8, 4.6, 4.4, 4.2, 4.0, 3.8, 3.6, 3.4, 3.2, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0],
        "choke": [0, 1, 3, 5, 7, 9, 10, 10.5, 11.0, 11.2, 11.0, 10.8, 10.6, 10.4, 10.2, 10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.8, 8.6, 8.4, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.6, 6.4, 6.2, 6.0, 5.8, 5.6, 5.4, 5.2, 5.0, 4.8, 4.6, 4.4, 4.2, 4.0, 3.8, 3.6, 3.4, 3.2, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0],
        "channel": [0, 2, 6, 8, 7.5, 8.5, 7.0, 8.8, 6.5, 9.0, 6.0, 8.5, 7.5, 8.0, 6.8, 7.2, 6.5, 7.0, 6.2, 6.8, 6.0, 6.5, 5.8, 6.2, 5.5, 6.0, 5.2, 5.8, 5.0, 5.5, 4.8, 5.2, 4.5, 5.0, 4.2, 4.8, 4.0, 4.5, 3.8, 4.2, 3.5, 4.0, 3.2, 3.8, 3.0, 3.5, 2.8, 3.2, 2.5, 3.0, 2.2, 2.8, 2.0, 2.5, 1.8, 2.2, 1.5, 2.0, 1.2, 1.8, 1.0, 1.5, 0.8, 1.2, 0.5, 1.0, 0.2, 0.8, 0],
        "temp_low": [0, 2, 6, 8.5, 9.1, 9.0, 8.8, 8.5, 8.2, 7.8, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0],
        "temp_high": [0, 2, 6, 8.5, 9.1, 9.0, 8.8, 8.5, 8.2, 7.8, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0],
        "overshoot": [0, 1, 3, 5, 7, 9, 10.5, 11.2, 10.8, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0],
        "short_pi": [0, 0.5, 1, 2, 4, 6, 8, 8.5, 9.0, 8.8, 8.5, 8.2, 7.8, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0]
    }
    
    base_profile = profiles.get(pattern, profiles["sweet_spot"])
    
    # Interpolate to match duration
    if len(base_profile) != duration_s + 1:
        # Simple linear interpolation
        result = []
        for i in range(duration_s + 1):
            ratio = i / duration_s
            idx = ratio * (len(base_profile) - 1)
            lower_idx = int(idx)
            upper_idx = min(lower_idx + 1, len(base_profile) - 1)
            weight = idx - lower_idx
            
            if lower_idx == upper_idx:
                result.append(base_profile[lower_idx])
            else:
                interpolated = base_profile[lower_idx] * (1 - weight) + base_profile[upper_idx] * weight
                result.append(round(interpolated, 1))
        
        return result
    
    return base_profile


def generate_flow_profile(pattern: str, duration_s: int) -> List[float]:
    """Generate realistic flow profiles for different shot patterns."""
    profiles = {
        "sweet_spot": [0, 0, 0.5, 1.2, 1.8, 2.0, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0],
        "fast": [0, 0, 0.8, 1.8, 2.5, 2.8, 3.0, 2.9, 2.7, 2.5, 2.3, 2.1, 1.9, 1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3, 0.1, 0],
        "slow": [0, 0, 0.3, 0.8, 1.2, 1.4, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0],
        "choke": [0, 0, 0.2, 0.5, 0.8, 1.0, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0],
        "channel": [0, 0, 0.5, 1.0, 1.5, 2.0, 1.8, 2.2, 1.6, 2.4, 1.4, 2.0, 1.8, 1.9, 1.7, 1.8, 1.6, 1.7, 1.5, 1.6, 1.4, 1.5, 1.3, 1.4, 1.2, 1.3, 1.1, 1.2, 1.0, 1.1, 0.9, 1.0, 0.8, 0.9, 0.7, 0.8, 0.6, 0.7, 0.5, 0.6, 0.4, 0.5, 0.3, 0.4, 0.2, 0.3, 0.1, 0.2, 0],
        "temp_low": [0, 0, 0.5, 1.2, 1.8, 2.0, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0],
        "temp_high": [0, 0, 0.5, 1.2, 1.8, 2.0, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0],
        "overshoot": [0, 0, 0.3, 0.8, 1.2, 1.5, 1.8, 2.0, 1.9, 1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3, 0.1, 0],
        "short_pi": [0, 0, 0.8, 1.5, 2.0, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0]
    }
    
    base_profile = profiles.get(pattern, profiles["sweet_spot"])
    
    # Interpolate to match duration
    if len(base_profile) != duration_s + 1:
        result = []
        for i in range(duration_s + 1):
            ratio = i / duration_s
            idx = ratio * (len(base_profile) - 1)
            lower_idx = int(idx)
            upper_idx = min(lower_idx + 1, len(base_profile) - 1)
            weight = idx - lower_idx
            
            if lower_idx == upper_idx:
                result.append(base_profile[lower_idx])
            else:
                interpolated = base_profile[lower_idx] * (1 - weight) + base_profile[upper_idx] * weight
                result.append(round(interpolated, 1))
        
        return result
    
    return base_profile


def generate_temperature_profile(pattern: str, duration_s: int) -> List[float]:
    """Generate realistic temperature profiles for different shot patterns."""
    base_temp = {
        "sweet_spot": 91.7,
        "fast": 92.0,
        "slow": 91.5,
        "choke": 92.5,
        "channel": 91.8,
        "temp_low": 89.5,  # Low temperature
        "temp_high": 95.2,  # High temperature
        "overshoot": 92.0,
        "short_pi": 91.5
    }
    
    temp = base_temp.get(pattern, 91.7)
    
    # Generate realistic temperature variation
    profile = []
    for i in range(duration_s + 1):
        # Small random variation around base temperature
        variation = random.uniform(-0.5, 0.5)
        profile.append(round(temp + variation, 1))
    
    return profile


def generate_shot_data(pattern: str, rule_hint: str, shot_id: str) -> Dict[str, Any]:
    """Generate a complete shot data structure for a given pattern."""
    
    # Define shot characteristics based on pattern
    characteristics = {
        "sweet_spot": {"duration": 29, "dose": 18.0, "yield": 36.5, "preinfusion": 3000},
        "fast": {"duration": 18, "dose": 18.0, "yield": 27.0, "preinfusion": 2000},
        "slow": {"duration": 45, "dose": 18.0, "yield": 50.4, "preinfusion": 4000},
        "choke": {"duration": 35, "dose": 18.0, "yield": 21.6, "preinfusion": 5000},
        "channel": {"duration": 28, "dose": 18.0, "yield": 37.8, "preinfusion": 2500},
        "temp_low": {"duration": 29, "dose": 18.0, "yield": 36.5, "preinfusion": 3000},
        "temp_high": {"duration": 29, "dose": 18.0, "yield": 36.5, "preinfusion": 3000},
        "overshoot": {"duration": 28, "dose": 18.0, "yield": 37.8, "preinfusion": 2000},
        "short_pi": {"duration": 28, "dose": 18.0, "yield": 37.8, "preinfusion": 1000}
    }
    
    char = characteristics.get(pattern, characteristics["sweet_spot"])
    duration_s = char["duration"]
    
    # Generate telemetry profiles
    pressure = generate_pressure_profile(pattern, duration_s)
    flow = generate_flow_profile(pattern, duration_s)
    temperature = generate_temperature_profile(pattern, duration_s)
    
    # Generate pump profile (percentage)
    pump = [0] + [random.randint(85, 95) for _ in range(duration_s)]
    
    # Calculate first drip time (when flow > 0.5 ml/s)
    first_drip_s = next((i for i, f in enumerate(flow) if f > 0.5), duration_s // 3)
    
    return {
        "pattern": pattern,
        "rule_hint": rule_hint,
        "shot_id": shot_id,
        "timestamp": shot_id,
        "bean_id": "GAGGIUINO",
        "dose_g": char["dose"],
        "target_mass_g": char["yield"],
        "final_weight_g": char["yield"],  # Add this for the loader
        "target_weight_g": char["yield"],  # Add this for the loader
        "pressure_bar": pressure,
        "flow_ml_s": flow,
        "temp_c": temperature,
        "pump_pct": pump,
        "preinfusion_ms": char["preinfusion"],
        "first_drip_s": first_drip_s,
        "shot_end_s": duration_s,
        "duration_s": duration_s,  # Add this for the loader
        "grinder_setting": None,
        "basket": "18g",
        "roast_age_days": None,
        "user_rating": None
    }


def generate_shot_palette() -> List[Dict[str, Any]]:
    """Generate a diverse palette of shots covering all diagnostic rules."""
    
    # Define shot patterns and their expected rules
    patterns = [
        ("sweet_spot", "sweet_spot"),
        ("fast", "under_extracted_fast"),
        ("slow", "over_extracted_slow"),
        ("choke", "choking_high_resistance"),
        ("channel", "channeling_instability"),
        ("temp_low", "temp_low_flat"),
        ("temp_high", "temp_high_bitter"),
        ("overshoot", "pump_overshoot"),
        ("short_pi", "preinfusion_short"),
        # Add some variations
        ("sweet_spot", "sweet_spot"),  # Duplicate for variety
        ("fast", "under_extracted_fast"),  # Duplicate for variety
        ("slow", "over_extracted_slow"),  # Duplicate for variety
        ("channel", "channeling_instability"),  # Duplicate for variety
        ("temp_low", "temp_low_flat"),  # Duplicate for variety
        ("temp_high", "temp_high_bitter"),  # Duplicate for variety
    ]
    
    shots = []
    base_time = datetime.now()
    
    for i, (pattern, rule_hint) in enumerate(patterns):
        # Generate unique shot ID
        shot_time = base_time + timedelta(minutes=i * 5)
        shot_id = shot_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        shot_data = generate_shot_data(pattern, rule_hint, shot_id)
        shots.append(shot_data)
    
    return shots


def main():
    """Generate shot palette and save to JSONL file."""
    print("🎯 Generating shot palette...")
    
    shots = generate_shot_palette()
    
    # Save to JSONL file
    output_path = Path("sample/shots_palette.jsonl")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        for shot in shots:
            f.write(json.dumps(shot) + '\n')
    
    print(f"✅ Generated {len(shots)} shots")
    print(f"📁 Saved to: {output_path}")
    
    # Print summary
    print("\n📊 Shot Palette Summary:")
    pattern_counts = {}
    for shot in shots:
        pattern = shot["pattern"]
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    for pattern, count in sorted(pattern_counts.items()):
        print(f"  {pattern}: {count} shots")


if __name__ == "__main__":
    main()
