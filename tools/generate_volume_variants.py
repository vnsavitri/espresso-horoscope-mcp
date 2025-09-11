#!/usr/bin/env python3
"""
Generate volume-based shot variants for espresso horoscope system.
Adds ristretto, lungo, americano, and other realistic coffee types.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

def generate_ristretto_shots(count: int = 8) -> List[Dict[str, Any]]:
    """Generate ristretto shots (15-20ml, 1:1-1.5 ratio)"""
    shots = []
    base_time = datetime.now() - timedelta(days=30)
    
    for i in range(count):
        # Ristretto characteristics: short, intense, high ratio
        dose = random.uniform(18.0, 20.0)
        target_mass = random.uniform(20.0, 30.0)  # 1:1 to 1:1.5 ratio
        shot_time = random.uniform(15, 25)  # Shorter extraction
        
        # Generate realistic pressure curve (higher resistance)
        pressure_curve = generate_pressure_curve(shot_time, base_pressure=9.5, max_pressure=10.5)
        flow_curve = generate_flow_curve(shot_time, max_flow=1.2)
        temp_curve = generate_temp_curve(shot_time, base_temp=92.0)
        pump_curve = generate_pump_curve(shot_time)
        
        shot = {
            "pattern": "ristretto",
            "rule_hint": "sweet_spot" if random.random() > 0.3 else "under_extracted_fast",
            "shot_id": (base_time + timedelta(hours=i*3)).isoformat() + "Z",
            "timestamp": (base_time + timedelta(hours=i*3)).isoformat() + "Z",
            "bean_id": "GAGGIUINO",
            "dose_g": round(dose, 1),
            "target_mass_g": round(target_mass, 1),
            "final_weight_g": round(target_mass, 1),
            "target_weight_g": round(target_mass, 1),
            "pressure_bar": pressure_curve,
            "flow_ml_s": flow_curve,
            "temp_c": temp_curve,
            "pump_pct": pump_curve,
            "preinfusion_ms": random.randint(2000, 4000),
            "first_drip_s": random.randint(2, 4),
            "shot_end_s": int(shot_time),
            "duration_s": int(shot_time),
            "grinder_setting": None,
            "basket": "18g",
            "roast_age_days": None,
            "user_rating": None
        }
        shots.append(shot)
    
    return shots

def generate_lungo_shots(count: int = 8) -> List[Dict[str, Any]]:
    """Generate lungo shots (60-90ml, 1:3-4 ratio)"""
    shots = []
    base_time = datetime.now() - timedelta(days=25)
    
    for i in range(count):
        # Lungo characteristics: long, diluted, lower ratio
        dose = random.uniform(18.0, 20.0)
        target_mass = random.uniform(60.0, 80.0)  # 1:3 to 1:4 ratio
        shot_time = random.uniform(35, 50)  # Longer extraction
        
        # Generate realistic pressure curve (lower resistance)
        pressure_curve = generate_pressure_curve(shot_time, base_pressure=8.0, max_pressure=9.0)
        flow_curve = generate_flow_curve(shot_time, max_flow=2.0)
        temp_curve = generate_temp_curve(shot_time, base_temp=90.0)
        pump_curve = generate_pump_curve(shot_time)
        
        shot = {
            "pattern": "lungo",
            "rule_hint": "over_extracted_slow" if random.random() > 0.4 else "sweet_spot",
            "shot_id": (base_time + timedelta(hours=i*4)).isoformat() + "Z",
            "timestamp": (base_time + timedelta(hours=i*4)).isoformat() + "Z",
            "bean_id": "GAGGIUINO",
            "dose_g": round(dose, 1),
            "target_mass_g": round(target_mass, 1),
            "final_weight_g": round(target_mass, 1),
            "target_weight_g": round(target_mass, 1),
            "pressure_bar": pressure_curve,
            "flow_ml_s": flow_curve,
            "temp_c": temp_curve,
            "pump_pct": pump_curve,
            "preinfusion_ms": random.randint(3000, 5000),
            "first_drip_s": random.randint(3, 5),
            "shot_end_s": int(shot_time),
            "duration_s": int(shot_time),
            "grinder_setting": None,
            "basket": "18g",
            "roast_age_days": None,
            "user_rating": None
        }
        shots.append(shot)
    
    return shots

def generate_double_shots(count: int = 6) -> List[Dict[str, Any]]:
    """Generate double espresso shots (50-60ml, 1:2 ratio)"""
    shots = []
    base_time = datetime.now() - timedelta(days=20)
    
    for i in range(count):
        # Double characteristics: standard ratio, double dose
        dose = random.uniform(36.0, 40.0)  # Double dose
        target_mass = random.uniform(50.0, 60.0)  # 1:2 ratio
        shot_time = random.uniform(25, 35)  # Standard extraction
        
        # Generate realistic pressure curve
        pressure_curve = generate_pressure_curve(shot_time, base_pressure=9.0, max_pressure=9.5)
        flow_curve = generate_flow_curve(shot_time, max_flow=1.8)
        temp_curve = generate_temp_curve(shot_time, base_temp=91.5)
        pump_curve = generate_pump_curve(shot_time)
        
        shot = {
            "pattern": "double",
            "rule_hint": "sweet_spot" if random.random() > 0.2 else "over_extracted_slow",
            "shot_id": (base_time + timedelta(hours=i*5)).isoformat() + "Z",
            "timestamp": (base_time + timedelta(hours=i*5)).isoformat() + "Z",
            "bean_id": "GAGGIUINO",
            "dose_g": round(dose, 1),
            "target_mass_g": round(target_mass, 1),
            "final_weight_g": round(target_mass, 1),
            "target_weight_g": round(target_mass, 1),
            "pressure_bar": pressure_curve,
            "flow_ml_s": flow_curve,
            "temp_c": temp_curve,
            "pump_pct": pump_curve,
            "preinfusion_ms": random.randint(2500, 4000),
            "first_drip_s": random.randint(3, 4),
            "shot_end_s": int(shot_time),
            "duration_s": int(shot_time),
            "grinder_setting": None,
            "basket": "18g",
            "roast_age_days": None,
            "user_rating": None
        }
        shots.append(shot)
    
    return shots

def generate_americano_shots(count: int = 6) -> List[Dict[str, Any]]:
    """Generate americano-style shots (150-200ml, 1:8-10 ratio)"""
    shots = []
    base_time = datetime.now() - timedelta(days=15)
    
    for i in range(count):
        # Americano characteristics: very long, very diluted
        dose = random.uniform(18.0, 20.0)
        target_mass = random.uniform(150.0, 200.0)  # 1:8 to 1:10 ratio
        shot_time = random.uniform(45, 65)  # Very long extraction
        
        # Generate realistic pressure curve (low resistance)
        pressure_curve = generate_pressure_curve(shot_time, base_pressure=7.0, max_pressure=8.5)
        flow_curve = generate_flow_curve(shot_time, max_flow=2.5)
        temp_curve = generate_temp_curve(shot_time, base_temp=88.0)
        pump_curve = generate_pump_curve(shot_time)
        
        shot = {
            "pattern": "americano",
            "rule_hint": "over_extracted_slow" if random.random() > 0.3 else "temp_low_flat",
            "shot_id": (base_time + timedelta(hours=i*6)).isoformat() + "Z",
            "timestamp": (base_time + timedelta(hours=i*6)).isoformat() + "Z",
            "bean_id": "GAGGIUINO",
            "dose_g": round(dose, 1),
            "target_mass_g": round(target_mass, 1),
            "final_weight_g": round(target_mass, 1),
            "target_weight_g": round(target_mass, 1),
            "pressure_bar": pressure_curve,
            "flow_ml_s": flow_curve,
            "temp_c": temp_curve,
            "pump_pct": pump_curve,
            "preinfusion_ms": random.randint(4000, 6000),
            "first_drip_s": random.randint(4, 6),
            "shot_end_s": int(shot_time),
            "duration_s": int(shot_time),
            "grinder_setting": None,
            "basket": "18g",
            "roast_age_days": None,
            "user_rating": None
        }
        shots.append(shot)
    
    return shots

def generate_pressure_curve(duration: float, base_pressure: float = 9.0, max_pressure: float = 9.5) -> List[float]:
    """Generate realistic pressure curve"""
    points = int(duration)
    curve = []
    
    for i in range(points):
        if i < 3:  # Preinfusion
            pressure = random.uniform(0.0, 2.0)
        elif i < 8:  # Ramp up
            progress = (i - 3) / 5
            pressure = 2.0 + progress * (max_pressure - 2.0)
        elif i < points - 5:  # Stable
            pressure = random.uniform(base_pressure - 0.5, base_pressure + 0.5)
        else:  # Decline
            progress = (points - i) / 5
            pressure = base_pressure * progress
            pressure = max(0.0, pressure)
        
        curve.append(round(pressure, 1))
    
    return curve

def generate_flow_curve(duration: float, max_flow: float = 1.8) -> List[float]:
    """Generate realistic flow curve"""
    points = int(duration)
    curve = []
    
    for i in range(points):
        if i < 3:  # Preinfusion
            flow = 0.0
        elif i < 8:  # Ramp up
            progress = (i - 3) / 5
            flow = progress * max_flow
        elif i < points - 5:  # Stable
            flow = random.uniform(max_flow - 0.3, max_flow + 0.2)
        else:  # Decline
            progress = (points - i) / 5
            flow = max_flow * progress
            flow = max(0.0, flow)
        
        curve.append(round(flow, 1))
    
    return curve

def generate_temp_curve(duration: float, base_temp: float = 91.0) -> List[float]:
    """Generate realistic temperature curve"""
    points = int(duration)
    curve = []
    
    for i in range(points):
        # Temperature varies slightly around base
        temp = base_temp + random.uniform(-1.5, 1.5)
        curve.append(round(temp, 1))
    
    return curve

def generate_pump_curve(duration: float) -> List[int]:
    """Generate realistic pump percentage curve"""
    points = int(duration)
    curve = []
    
    for i in range(points):
        if i < 3:  # Preinfusion
            pump = random.randint(0, 20)
        elif i < 8:  # Ramp up
            pump = random.randint(80, 95)
        elif i < points - 5:  # Stable
            pump = random.randint(85, 95)
        else:  # Decline
            pump = random.randint(0, 30)
        
        curve.append(pump)
    
    return curve

def main():
    """Generate all volume-based shot variants"""
    print("🎯 Generating volume-based shot variants...")
    
    # Generate different shot types
    ristretto_shots = generate_ristretto_shots(8)
    lungo_shots = generate_lungo_shots(8)
    double_shots = generate_double_shots(6)
    americano_shots = generate_americano_shots(6)
    
    # Combine all new shots
    all_new_shots = ristretto_shots + lungo_shots + double_shots + americano_shots
    
    print(f"✅ Generated {len(all_new_shots)} new volume-based shots:")
    print(f"  - Ristretto: {len(ristretto_shots)} shots")
    print(f"  - Lungo: {len(lungo_shots)} shots")
    print(f"  - Double: {len(double_shots)} shots")
    print(f"  - Americano: {len(americano_shots)} shots")
    
    # Save to file
    with open("sample/volume_variants.jsonl", "w") as f:
        for shot in all_new_shots:
            f.write(json.dumps(shot) + "\n")
    
    print(f"💾 Saved to sample/volume_variants.jsonl")
    
    return all_new_shots

if __name__ == "__main__":
    main()
