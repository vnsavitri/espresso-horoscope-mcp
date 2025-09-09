#!/usr/bin/env python3
"""
Generate a diverse palette of espresso shot data for horoscope generation.

This script creates 50-75 realistic shot patterns covering various scenarios:
- Sweet spot shots (perfect extraction)
- Under-extracted shots (fast, sour)
- Over-extracted shots (slow, bitter)
- Channeling issues (unstable flow)
- Temperature variations (too hot/cold)
- Pressure problems (choking, low pressure)
- Flow rate variations
- Different dose sizes and ratios
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import math

def generate_pressure_curve(pattern: str, duration: int) -> List[float]:
    """Generate realistic pressure curves for different shot patterns."""
    if pattern == "sweet_spot":
        # Smooth ramp up, stable peak, gentle decline
        return [0.0] + [min(9.5, 0.5 * i + random.uniform(-0.5, 0.5)) for i in range(1, duration//3)] + \
               [9.0 + random.uniform(-0.3, 0.3) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 9.0 - 0.3 * (i - 2*duration//3) + random.uniform(-0.5, 0.5)) for i in range(2*duration//3, duration)]
    
    elif pattern == "fast":
        # Quick ramp, lower peak, fast decline
        return [0.0] + [min(7.0, 1.0 * i + random.uniform(-0.3, 0.3)) for i in range(1, duration//4)] + \
               [6.5 + random.uniform(-0.5, 0.5) for _ in range(duration//4, duration//2)] + \
               [max(0, 6.5 - 0.5 * (i - duration//2) + random.uniform(-0.3, 0.3)) for i in range(duration//2, duration)]
    
    elif pattern == "slow":
        # Slow ramp, high peak, gradual decline
        return [0.0] + [min(9.5, 0.3 * i + random.uniform(-0.2, 0.2)) for i in range(1, duration//2)] + \
               [9.2 + random.uniform(-0.2, 0.2) for _ in range(duration//2, 3*duration//4)] + \
               [max(0, 9.2 - 0.2 * (i - 3*duration//4) + random.uniform(-0.3, 0.3)) for i in range(3*duration//4, duration)]
    
    elif pattern == "choke":
        # High pressure, low flow
        return [0.0] + [min(11.5, 0.8 * i + random.uniform(-0.3, 0.3)) for i in range(1, duration//3)] + \
               [11.0 + random.uniform(-0.5, 0.5) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 11.0 - 0.4 * (i - 2*duration//3) + random.uniform(-0.3, 0.3)) for i in range(2*duration//3, duration)]
    
    elif pattern == "channel":
        # Unstable, erratic pressure
        base_pressure = 8.0
        return [0.0] + [base_pressure + random.uniform(-2.0, 2.0) + 0.5 * math.sin(i * 0.5) for i in range(1, duration)]
    
    elif pattern == "temp_low":
        # Normal pressure but low temperature
        return [0.0] + [min(9.0, 0.4 * i + random.uniform(-0.3, 0.3)) for i in range(1, duration//3)] + \
               [8.5 + random.uniform(-0.3, 0.3) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 8.5 - 0.3 * (i - 2*duration//3) + random.uniform(-0.3, 0.3)) for i in range(2*duration//3, duration)]
    
    elif pattern == "temp_high":
        # Normal pressure but high temperature
        return [0.0] + [min(9.5, 0.5 * i + random.uniform(-0.3, 0.3)) for i in range(1, duration//3)] + \
               [9.2 + random.uniform(-0.3, 0.3) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 9.2 - 0.3 * (i - 2*duration//3) + random.uniform(-0.3, 0.3)) for i in range(2*duration//3, duration)]
    
    else:  # Default sweet spot
        return [0.0] + [min(9.0, 0.4 * i + random.uniform(-0.3, 0.3)) for i in range(1, duration//3)] + \
               [8.8 + random.uniform(-0.3, 0.3) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 8.8 - 0.3 * (i - 2*duration//3) + random.uniform(-0.3, 0.3)) for i in range(2*duration//3, duration)]

def generate_flow_curve(pattern: str, duration: int) -> List[float]:
    """Generate realistic flow curves based on pressure patterns."""
    if pattern == "sweet_spot":
        # Smooth flow progression
        return [0.0] + [min(2.5, 0.1 * i + random.uniform(-0.1, 0.1)) for i in range(1, duration//4)] + \
               [2.0 + random.uniform(-0.2, 0.2) for _ in range(duration//4, 3*duration//4)] + \
               [max(0, 2.0 - 0.1 * (i - 3*duration//4) + random.uniform(-0.1, 0.1)) for i in range(3*duration//4, duration)]
    
    elif pattern == "fast":
        # High flow rate
        return [0.0] + [min(3.5, 0.2 * i + random.uniform(-0.2, 0.2)) for i in range(1, duration//3)] + \
               [3.0 + random.uniform(-0.3, 0.3) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 3.0 - 0.2 * (i - 2*duration//3) + random.uniform(-0.2, 0.2)) for i in range(2*duration//3, duration)]
    
    elif pattern == "slow":
        # Low flow rate
        return [0.0] + [min(1.5, 0.05 * i + random.uniform(-0.05, 0.05)) for i in range(1, duration//2)] + \
               [1.2 + random.uniform(-0.1, 0.1) for _ in range(duration//2, 3*duration//4)] + \
               [max(0, 1.2 - 0.05 * (i - 3*duration//4) + random.uniform(-0.05, 0.05)) for i in range(3*duration//4, duration)]
    
    elif pattern == "choke":
        # Very low flow rate
        return [0.0] + [min(1.0, 0.03 * i + random.uniform(-0.03, 0.03)) for i in range(1, duration//2)] + \
               [0.8 + random.uniform(-0.1, 0.1) for _ in range(duration//2, 3*duration//4)] + \
               [max(0, 0.8 - 0.03 * (i - 3*duration//4) + random.uniform(-0.03, 0.03)) for i in range(3*duration//4, duration)]
    
    elif pattern == "channel":
        # Erratic flow
        base_flow = 1.5
        return [0.0] + [max(0, base_flow + random.uniform(-0.8, 0.8) + 0.3 * math.sin(i * 0.3)) for i in range(1, duration)]
    
    else:  # Default
        return [0.0] + [min(2.0, 0.1 * i + random.uniform(-0.1, 0.1)) for i in range(1, duration//3)] + \
               [1.8 + random.uniform(-0.2, 0.2) for _ in range(duration//3, 2*duration//3)] + \
               [max(0, 1.8 - 0.1 * (i - 2*duration//3) + random.uniform(-0.1, 0.1)) for i in range(2*duration//3, duration)]

def generate_temp_curve(pattern: str, duration: int) -> List[float]:
    """Generate temperature curves based on patterns."""
    if pattern == "temp_low":
        # Low temperature (85-89°C)
        base_temp = 87.0
    elif pattern == "temp_high":
        # High temperature (94-98°C)
        base_temp = 96.0
    else:
        # Normal temperature (90-93°C)
        base_temp = 91.5
    
    return [base_temp + random.uniform(-1.0, 1.0) + 0.5 * math.sin(i * 0.1) for i in range(duration)]

def generate_pump_curve(duration: int) -> List[int]:
    """Generate pump percentage curve."""
    return [0] + [random.randint(85, 95) for _ in range(duration - 1)]

def generate_shot_data(pattern: str, rule_hint: str, shot_id: str) -> Dict[str, Any]:
    """Generate a complete shot data entry."""
    
    # Pattern-specific parameters
    if pattern == "sweet_spot":
        duration = random.randint(25, 32)
        dose = random.uniform(17.5, 18.5)
        ratio = random.uniform(1.8, 2.2)
        preinfusion = random.randint(2500, 3500)
        first_drip = random.randint(3, 5)
    elif pattern == "fast":
        duration = random.randint(15, 22)
        dose = random.uniform(17.0, 18.0)
        ratio = random.uniform(1.2, 1.8)
        preinfusion = random.randint(1500, 2500)
        first_drip = random.randint(1, 3)
    elif pattern == "slow":
        duration = random.randint(35, 50)
        dose = random.uniform(18.0, 19.0)
        ratio = random.uniform(2.3, 2.8)
        preinfusion = random.randint(3500, 4500)
        first_drip = random.randint(5, 8)
    elif pattern == "choke":
        duration = random.randint(30, 40)
        dose = random.uniform(18.5, 19.5)
        ratio = random.uniform(1.0, 1.4)
        preinfusion = random.randint(4000, 6000)
        first_drip = random.randint(6, 10)
    elif pattern == "channel":
        duration = random.randint(20, 35)
        dose = random.uniform(17.5, 18.5)
        ratio = random.uniform(1.5, 2.3)
        preinfusion = random.randint(2000, 3000)
        first_drip = random.randint(2, 5)
    elif pattern == "temp_low":
        duration = random.randint(25, 35)
        dose = random.uniform(17.5, 18.5)
        ratio = random.uniform(1.8, 2.2)
        preinfusion = random.randint(2500, 3500)
        first_drip = random.randint(3, 5)
    elif pattern == "temp_high":
        duration = random.randint(25, 35)
        dose = random.uniform(17.5, 18.5)
        ratio = random.uniform(1.8, 2.2)
        preinfusion = random.randint(2500, 3500)
        first_drip = random.randint(3, 5)
    else:
        duration = random.randint(25, 32)
        dose = random.uniform(17.5, 18.5)
        ratio = random.uniform(1.8, 2.2)
        preinfusion = random.randint(2500, 3500)
        first_drip = random.randint(3, 5)
    
    # Calculate final weight
    final_weight = dose * ratio
    
    # Generate curves
    pressure = generate_pressure_curve(pattern, duration)
    flow = generate_flow_curve(pattern, duration)
    temp = generate_temp_curve(pattern, duration)
    pump = generate_pump_curve(duration)
    
    # Calculate channeling score
    if pattern == "channel":
        channeling = random.uniform(0.1, 0.3)
    elif pattern == "sweet_spot":
        channeling = random.uniform(0.0, 0.05)
    else:
        channeling = random.uniform(0.05, 0.15)
    
    return {
        "pattern": pattern,
        "rule_hint": rule_hint,
        "shot_id": shot_id,
        "timestamp": shot_id,
        "bean_id": "GAGGIUINO",
        "dose_g": round(dose, 1),
        "target_mass_g": round(final_weight, 1),
        "final_weight_g": round(final_weight, 1),
        "target_weight_g": round(final_weight, 1),
        "pressure_bar": [round(p, 1) for p in pressure],
        "flow_ml_s": [round(f, 1) for f in flow],
        "temp_c": [round(t, 1) for t in temp],
        "pump_pct": pump,
        "preinfusion_ms": preinfusion,
        "first_drip_s": first_drip,
        "shot_end_s": duration,
        "duration_s": duration,
        "grinder_setting": None,
        "basket": "18g",
        "roast_age_days": None,
        "user_rating": None
    }

def main():
    """Generate a diverse palette of shot data."""
    
    # Define patterns and their frequencies
    patterns = [
        ("sweet_spot", "sweet_spot", 15),  # 15 perfect shots
        ("fast", "under_extracted_fast", 12),  # 12 fast shots
        ("slow", "over_extracted_slow", 10),  # 10 slow shots
        ("choke", "choking_high_resistance", 8),  # 8 choked shots
        ("channel", "channeling_instability", 8),  # 8 channeling shots
        ("temp_low", "temp_low_flat", 6),  # 6 low temp shots
        ("temp_high", "temp_high_bitter", 6),  # 6 high temp shots
        ("sweet_spot", "perfect_extraction", 5),  # 5 more perfect shots
    ]
    
    shots = []
    base_time = datetime(2025, 9, 8, 19, 0, 0)
    
    for pattern, rule_hint, count in patterns:
        for i in range(count):
            # Generate unique timestamp
            timestamp = base_time + timedelta(minutes=5 * len(shots))
            shot_id = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Generate shot data
            shot_data = generate_shot_data(pattern, rule_hint, shot_id)
            shots.append(shot_data)
    
    # Shuffle to randomize order
    random.shuffle(shots)
    
    # Write to file
    output_file = "sample/shots_palette.jsonl"
    with open(output_file, 'w') as f:
        for shot in shots:
            f.write(json.dumps(shot) + '\n')
    
    print(f"✅ Generated {len(shots)} diverse shot patterns")
    print(f"📁 Saved to {output_file}")
    print(f"🎯 Patterns included:")
    for pattern, rule_hint, count in patterns:
        print(f"   - {pattern} ({rule_hint}): {count} shots")

if __name__ == "__main__":
    main()
