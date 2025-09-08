#!/usr/bin/env python3
"""
Gaggiuino MCP Data Loader

Converts raw Gaggiuino MCP responses to standardized schema.
Uses getShotData from Gaggiuino MCP server.
"""

import json
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime


def from_mcp_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert raw Gaggiuino MCP response to standardized schema.
    
    Args:
        raw: Raw MCP response dictionary
        
    Returns:
        Standardized shot data dictionary
    """
    # Extract pressure data with fallback
    pressure = raw.get("pressure") or raw.get("pressure_bar", [])
    
    # Extract flow data with fallback
    flow = raw.get("flow_ml_s") or raw.get("flow", [])
    
    # Extract temperature data with fallback
    temp = raw.get("temp_c") or raw.get("temperature_c", [])
    
    # Extract pump percentage data
    pump = raw.get("pump_pct", [])
    
    # Calculate duration - use provided duration or estimate from pressure data
    duration = raw.get("duration_s")
    if duration is None and pressure:
        duration = len(pressure) * 0.1
    
    # Extract final weight with fallback to target weight
    final_weight = raw.get("final_weight_g") or raw.get("target_weight_g", 0)
    
    # Calculate dose (assume 18g basket for now)
    dose_g = 18.0  # Default dose for 18g basket
    
    # Build standardized response
    result = {
        "timestamp": raw.get("timestamp", datetime.now().isoformat() + "Z"),
        "bean_id": "GAGGIUINO",
        "dose_g": dose_g,
        "target_mass_g": final_weight,
        "pressure_bar": pressure,
        "flow_ml_s": flow,
        "temp_c": temp,
        "pump_pct": pump,
        "preinfusion_ms": raw.get("preinfusion_ms", 0),
        "first_drip_s": raw.get("first_drip_s", 0),
        "shot_end_s": duration or 0,
        "grinder_setting": None,
        "basket": "18g",
        "roast_age_days": None,
        "user_rating": None
    }
    
    return result


def main():
    """CLI interface for testing the loader."""
    if len(sys.argv) != 2:
        print("Usage: python -m data_sources.gaggiuino_loader <input_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            raw_data = json.load(f)
        
        # Convert to standardized format
        standardized = from_mcp_response(raw_data)
        
        # Output as JSONL
        print(json.dumps(standardized))
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{input_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
