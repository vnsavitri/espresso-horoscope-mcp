#!/usr/bin/env python3
"""
Pressure curve generation for espresso shots.
Focused module for generating realistic pressure patterns.
"""

import random
import math
from typing import List

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
    
    else:  # default
        return [0.0] + [8.0 + random.uniform(-1.0, 1.0) for _ in range(1, duration)]
