#!/usr/bin/env python3
"""
Flow curve generation for espresso shots.
Focused module for generating realistic flow patterns.
"""

import random
import math
from typing import List

def generate_flow_curve(pattern: str, duration: int) -> List[float]:
    """Generate realistic flow curves for different shot patterns."""
    if pattern == "sweet_spot":
        # Steady, consistent flow
        return [0.0] + [1.2 + random.uniform(-0.1, 0.1) for _ in range(1, duration)]
    
    elif pattern == "fast":
        # High initial flow, declining
        return [0.0] + [max(0.3, 2.0 - 0.1 * i + random.uniform(-0.2, 0.2)) for i in range(1, duration)]
    
    elif pattern == "slow":
        # Low, steady flow
        return [0.0] + [0.8 + random.uniform(-0.1, 0.1) for _ in range(1, duration)]
    
    elif pattern == "choke":
        # Very low flow
        return [0.0] + [0.4 + random.uniform(-0.1, 0.1) for _ in range(1, duration)]
    
    elif pattern == "channel":
        # Erratic, unstable flow
        return [0.0] + [1.0 + random.uniform(-0.5, 0.5) + 0.3 * math.sin(i * 0.8) for i in range(1, duration)]
    
    else:  # default
        return [0.0] + [1.0 + random.uniform(-0.2, 0.2) for _ in range(1, duration)]
