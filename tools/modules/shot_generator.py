#!/usr/bin/env python3
"""
Core shot generation logic.
Focused module for creating shot data structures.
"""

import random
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .pressure_curves import generate_pressure_curve
from .flow_curves import generate_flow_curve

def create_shot_data(pattern: str, shot_id: str) -> Dict[str, Any]:
    """Create a complete shot data structure."""
    duration = random.randint(20, 35)
    
    # Generate curves
    pressure_curve = generate_pressure_curve(pattern, duration)
    flow_curve = generate_flow_curve(pattern, duration)
    
    # Calculate metrics
    avg_pressure = sum(pressure_curve) / len(pressure_curve)
    avg_flow = sum(flow_curve) / len(flow_curve)
    total_volume = sum(flow_curve) * 0.1  # Convert to ml
    
    # Calculate brew ratio
    dose = random.uniform(16.0, 20.0)
    brew_ratio = total_volume / dose if dose > 0 else 0
    
    # Determine rule and severity
    rule_id, severity = determine_rule_and_severity(pattern, brew_ratio, avg_pressure, avg_flow)
    
    return {
        "shot_id": shot_id,
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
        "pattern": pattern,
        "duration": duration,
        "dose_grams": round(dose, 1),
        "output_ml": round(total_volume, 1),
        "brew_ratio": round(brew_ratio, 2),
        "avg_pressure_bar": round(avg_pressure, 1),
        "avg_flow_ml_s": round(avg_flow, 2),
        "pressure_curve": [round(p, 1) for p in pressure_curve],
        "flow_curve": [round(f, 2) for f in flow_curve],
        "rule_id": rule_id,
        "severity": severity,
        "rule_hint": get_rule_hint(rule_id)
    }

def determine_rule_and_severity(pattern: str, brew_ratio: float, avg_pressure: float, avg_flow: float) -> tuple:
    """Determine which rule was triggered and severity level."""
    if pattern == "sweet_spot":
        return "perfect_extraction", "info"
    elif pattern == "fast" or brew_ratio < 1.5:
        return "under_extracted", "warning"
    elif pattern == "slow" or brew_ratio > 2.5:
        return "over_extracted", "warning"
    elif pattern == "choke" or avg_pressure > 10.5:
        return "choking", "error"
    elif pattern == "channel":
        return "channeling", "error"
    else:
        return "normal_extraction", "info"

def get_rule_hint(rule_id: str) -> str:
    """Get a hint about the rule that was triggered."""
    hints = {
        "perfect_extraction": "Optimal extraction achieved",
        "under_extracted": "Shot extracted too quickly",
        "over_extracted": "Shot extracted too slowly", 
        "choking": "Machine pressure too high",
        "channeling": "Uneven water distribution",
        "normal_extraction": "Standard extraction"
    }
    return hints.get(rule_id, "Unknown pattern")
