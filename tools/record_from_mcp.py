#!/usr/bin/env python3
"""
Record from MCP Tool

Processes Gaggiuino MCP shot files and converts them to standardized JSONL format.
"""

import argparse
import glob
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the loader function
from data_sources.gaggiuino_loader import from_mcp_response


def process_files(file_patterns: List[str], output_file: str) -> None:
    """
    Process MCP shot files and write to JSONL output.
    
    Args:
        file_patterns: List of glob patterns for input files
        output_file: Output JSONL file path
    """
    # Expand all glob patterns to get actual file paths
    input_files = []
    for pattern in file_patterns:
        matches = glob.glob(pattern)
        if not matches:
            print(f"Warning: No files found matching pattern '{pattern}'", file=sys.stderr)
        input_files.extend(matches)
    
    if not input_files:
        print("Error: No input files found", file=sys.stderr)
        sys.exit(1)
    
    # Remove duplicates and sort for consistent output
    input_files = sorted(list(set(input_files)))
    
    print(f"Processing {len(input_files)} files...", file=sys.stderr)
    
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    processed_count = 0
    error_count = 0
    
    with open(output_file, 'w') as out_f:
        for input_file in input_files:
            try:
                print(f"Processing: {input_file}", file=sys.stderr)
                
                with open(input_file, 'r') as in_f:
                    raw_data = json.load(in_f)
                
                # Convert to standardized format
                standardized = from_mcp_response(raw_data)
                
                # Write as JSONL line
                out_f.write(json.dumps(standardized) + '\n')
                processed_count += 1
                
            except FileNotFoundError:
                print(f"Error: File '{input_file}' not found", file=sys.stderr)
                error_count += 1
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in '{input_file}': {e}", file=sys.stderr)
                error_count += 1
            except Exception as e:
                print(f"Error processing '{input_file}': {e}", file=sys.stderr)
                error_count += 1
    
    print(f"Completed: {processed_count} files processed, {error_count} errors", file=sys.stderr)
    print(f"Output written to: {output_file}", file=sys.stderr)
    
    if error_count > 0:
        sys.exit(1)


def main():
    """CLI interface using argparse."""
    parser = argparse.ArgumentParser(
        description="Convert Gaggiuino MCP shot files to standardized JSONL format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl
  python tools/record_from_mcp.py shot_001.json shot_002.json -o data/shots.jsonl
        """
    )
    
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input MCP shot files (supports glob patterns like *.json)'
    )
    
    parser.add_argument(
        '-o', '--out',
        default='data/shots.jsonl',
        help='Output JSONL file path (default: data/shots.jsonl)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Input patterns: {args.input_files}", file=sys.stderr)
        print(f"Output file: {args.out}", file=sys.stderr)
    
    process_files(args.input_files, args.out)


if __name__ == "__main__":
    main()
