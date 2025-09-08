#!/usr/bin/env python3
"""
Feature Extraction Tool

Extracts brewing features from standardized shot data.
"""

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


def calculate_brew_ratio(shot_data: Dict[str, Any]) -> float:
    """Calculate brew ratio (yield/dose)."""
    yield_g = shot_data.get("target_mass_g", 0)
    dose_g = shot_data.get("dose_g", 1)  # Avoid division by zero
    return yield_g / dose_g if dose_g > 0 else 0.0


def get_peak_pressure(pressure_data: List[float]) -> float:
    """Get peak pressure from pressure curve."""
    if not pressure_data:
        return 0.0
    return max(pressure_data)


def get_shot_duration(shot_data: Dict[str, Any]) -> float:
    """Get shot duration in seconds."""
    return shot_data.get("shot_end_s", 0.0)


def calculate_temp_metrics(temp_data: List[float], shot_duration: float) -> tuple[float, float]:
    """
    Calculate temperature average and standard deviation.
    Uses 5-25s window if possible, otherwise uses available data.
    """
    if not temp_data:
        return 0.0, 0.0
    
    # Determine time window (5-25s if possible)
    start_time = 5.0
    end_time = min(25.0, shot_duration)
    
    # Estimate data points per second (assuming uniform sampling)
    if shot_duration > 0 and len(temp_data) > 1:
        points_per_second = len(temp_data) / shot_duration
        start_idx = int(start_time * points_per_second)
        end_idx = int(end_time * points_per_second)
        
        # Ensure valid indices
        start_idx = max(0, start_idx)
        end_idx = min(len(temp_data), end_idx)
        
        if start_idx < end_idx:
            window_data = temp_data[start_idx:end_idx]
        else:
            # Fallback to all data if window is too small
            window_data = temp_data
    else:
        window_data = temp_data
    
    if not window_data:
        return 0.0, 0.0
    
    avg_temp = statistics.mean(window_data)
    std_temp = statistics.stdev(window_data) if len(window_data) > 1 else 0.0
    
    return avg_temp, std_temp


def calculate_flow_metrics(flow_data: List[float], pressure_data: List[float]) -> tuple[float, float]:
    """
    Calculate flow average and channeling score.
    Channeling score = fraction of timesteps where Δpressure < -0.5 & Δflow > 0.8
    """
    if not flow_data:
        return 0.0, 0.0
    
    # Calculate average flow
    avg_flow = statistics.mean(flow_data)
    
    # Calculate channeling score
    if len(flow_data) < 2 or len(pressure_data) < 2:
        return avg_flow, 0.0
    
    # Ensure both arrays have the same length
    min_length = min(len(flow_data), len(pressure_data))
    flow_data = flow_data[:min_length]
    pressure_data = pressure_data[:min_length]
    
    channeling_count = 0
    total_comparisons = 0
    
    for i in range(1, min_length):
        delta_pressure = pressure_data[i] - pressure_data[i-1]
        delta_flow = flow_data[i] - flow_data[i-1]
        
        total_comparisons += 1
        
        # Channeling condition: pressure drops significantly while flow increases
        if delta_pressure < -0.5 and delta_flow > 0.8:
            channeling_count += 1
    
    channeling_score = channeling_count / total_comparisons if total_comparisons > 0 else 0.0
    
    return avg_flow, channeling_score


def extract_features(shot_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract all features from a single shot.
    
    Args:
        shot_data: Standardized shot data dictionary
        
    Returns:
        Dictionary with extracted features
    """
    # Basic metrics
    brew_ratio = calculate_brew_ratio(shot_data)
    peak_pressure_bar = get_peak_pressure(shot_data.get("pressure_bar", []))
    shot_end_s = get_shot_duration(shot_data)
    
    # Temperature metrics
    temp_data = shot_data.get("temp_c", [])
    temp_avg_c, temp_std_c = calculate_temp_metrics(temp_data, shot_end_s)
    
    # Flow metrics
    flow_data = shot_data.get("flow_ml_s", [])
    pressure_data = shot_data.get("pressure_bar", [])
    flow_avg_ml_s, channeling_score_0_1 = calculate_flow_metrics(flow_data, pressure_data)
    
    # Build feature dictionary
    features = {
        "shot_id": shot_data.get("timestamp", ""),
        "brew_ratio": brew_ratio,
        "peak_pressure_bar": peak_pressure_bar,
        "shot_end_s": shot_end_s,
        "temp_avg_c": temp_avg_c,
        "temp_std_c": temp_std_c,
        "flow_avg_ml_s": flow_avg_ml_s,
        "channeling_score_0_1": channeling_score_0_1
    }
    
    return features


def process_shots(input_file: str, output_file: str) -> None:
    """
    Process shots from JSONL input and write features to JSONL output.
    
    Args:
        input_file: Input JSONL file with shot data
        output_file: Output JSONL file for features
    """
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    processed_count = 0
    error_count = 0
    
    with open(input_file, 'r') as in_f, open(output_file, 'w') as out_f:
        for line_num, line in enumerate(in_f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                shot_data = json.loads(line)
                features = extract_features(shot_data)
                
                # Write features as JSONL
                out_f.write(json.dumps(features) + '\n')
                processed_count += 1
                
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON on line {line_num}: {e}", file=sys.stderr)
                error_count += 1
            except Exception as e:
                print(f"Error processing line {line_num}: {e}", file=sys.stderr)
                error_count += 1
    
    print(f"Completed: {processed_count} shots processed, {error_count} errors", file=sys.stderr)
    print(f"Features written to: {output_file}", file=sys.stderr)
    
    if error_count > 0:
        sys.exit(1)


def main():
    """CLI interface using argparse."""
    parser = argparse.ArgumentParser(
        description="Extract brewing features from standardized shot data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python features/extract.py data/shots.jsonl -o data/features.jsonl
  python features/extract.py data/shots.jsonl -o data/features.jsonl --verbose
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Input JSONL file with shot data'
    )
    
    parser.add_argument(
        '-o', '--out',
        default='data/features.jsonl',
        help='Output JSONL file for features (default: data/features.jsonl)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Input file: {args.input_file}", file=sys.stderr)
        print(f"Output file: {args.out}", file=sys.stderr)
    
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    process_shots(args.input_file, args.out)


if __name__ == "__main__":
    main()
