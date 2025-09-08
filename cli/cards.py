#!/usr/bin/env python3
"""
Espresso Horoscope Card Generator

Generates astrological horoscope cards from espresso shot features.
"""

import argparse
import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Import the gpt-oss helper
from gptoss_helper import enhance_text_with_gptoss


def safe_eval(expression: str, variables: Dict[str, Any]) -> bool:
    """
    Safely evaluate a boolean expression with only numeric operations.
    
    Args:
        expression: Boolean expression string
        variables: Dictionary of variable values
        
    Returns:
        Boolean result of evaluation
    """
    # Only allow safe operations and variable names
    allowed_ops = ['and', 'or', 'not', '<=', '>=', '<', '>', '==', '!=', '+', '-', '*', '/', '(', ')']
    allowed_vars = set(variables.keys())
    
    # Replace variable names with their values
    expr = expression
    for var_name, var_value in variables.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(var_name) + r'\b'
        expr = re.sub(pattern, str(var_value), expr)
    
    # Check for any remaining variable names (security check)
    remaining_vars = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expr)
    for var in remaining_vars:
        if var not in ['and', 'or', 'not', 'True', 'False']:
            raise ValueError(f"Unsafe variable '{var}' found in expression")
    
    try:
        return eval(expr, {"__builtins__": {}}, {})
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expression}': {e}")


def load_features(features_file: str) -> List[Dict[str, Any]]:
    """Load features from JSONL file."""
    features = []
    with open(features_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                features.append(json.loads(line))
    return features


def load_rules(rules_file: str) -> Dict[str, Any]:
    """Load diagnostic rules from YAML file."""
    with open(rules_file, 'r') as f:
        return yaml.safe_load(f)


def load_astro_map(astro_file: str) -> Dict[str, Any]:
    """Load astrological mappings from YAML file."""
    with open(astro_file, 'r') as f:
        return yaml.safe_load(f)


def find_matching_rule(features: Dict[str, Any], rules: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Find the highest severity rule that matches the shot features.
    
    Returns:
        Tuple of (rule_id, rule_data)
    """
    # Severity order: error > warning > success
    severity_order = {"error": 3, "warning": 2, "success": 1}
    
    matching_rules = []
    
    for rule_id, rule_data in rules.get("rules", {}).items():
        try:
            when_expr = rule_data.get("when", "")
            if when_expr and safe_eval(when_expr, features):
                matching_rules.append((rule_id, rule_data))
        except Exception as e:
            print(f"Warning: Error evaluating rule '{rule_id}': {e}", file=sys.stderr)
            continue
    
    if not matching_rules:
        # Fallback to sweet_spot
        sweet_spot_rule = rules.get("rules", {}).get("sweet_spot")
        if sweet_spot_rule:
            return "sweet_spot", sweet_spot_rule
        else:
            raise ValueError("No matching rules found and no sweet_spot fallback available")
    
    # Sort by severity (highest first)
    matching_rules.sort(key=lambda x: severity_order.get(x[1].get("severity", "success"), 1), reverse=True)
    
    return matching_rules[0]


def render_template(template: str, features: Dict[str, Any]) -> str:
    """Render template string with feature values."""
    try:
        return template.format(**features)
    except KeyError as e:
        print(f"Warning: Missing variable {e} in template", file=sys.stderr)
        return template




def generate_card(features: Dict[str, Any], rules: Dict[str, Any], astro_map: Dict[str, Any], use_gptoss: bool = False) -> str:
    """Generate a single horoscope card."""
    # Find matching rule
    rule_id, rule_data = find_matching_rule(features, rules)
    
    # Get astrological mapping
    astro_data = astro_map.get("astro_map", {}).get(rule_id, {})
    
    # Extract shot info
    shot_id = features.get("shot_id", "Unknown")
    brew_ratio = features.get("brew_ratio", 0)
    shot_end_s = features.get("shot_end_s", 0)
    peak_pressure_bar = features.get("peak_pressure_bar", 0)
    temp_avg_c = features.get("temp_avg_c", 0)
    channeling_score = features.get("channeling_score_0_1", 0)
    
    # Build card
    emoji = astro_data.get("emoji", "☕")
    title = astro_data.get("title", "Espresso Reading")
    mantra = astro_data.get("mantra", "Brew with intention")
    template = astro_data.get("template", "Your espresso tells a story...")
    
    # Render template
    rendered_template = render_template(template, features)
    
    # Apply gpt-oss if requested
    if use_gptoss:
        rendered_template = enhance_text_with_gptoss(rendered_template)
    
    # Build markdown card
    card = f"""## {emoji} {title}

**Shot ID:** {shot_id}  
**Mantra:** *{mantra}*

### 📊 Brew Snapshot
- **Ratio:** {brew_ratio:.2f}:1
- **Time:** {shot_end_s:.0f}s
- **Peak Pressure:** {peak_pressure_bar:.1f} bar
- **Temperature:** {temp_avg_c:.1f}°C
- **Channeling:** {channeling_score:.2f}

### 🔮 Cosmic Reading
{rendered_template}

### 💡 Brewing Wisdom
"""
    
    # Add advice lines
    advice_list = rule_data.get("advice", [])
    for advice in advice_list:
        card += f"- {advice}\n"
    
    card += "\n---\n\n"
    
    return card


def main():
    """CLI interface using argparse."""
    parser = argparse.ArgumentParser(
        description="Generate espresso horoscope cards from shot features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md
  python cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md --style gptoss
        """
    )
    
    parser.add_argument(
        '--features',
        required=True,
        help='Input JSONL file with shot features'
    )
    
    parser.add_argument(
        '--rules',
        required=True,
        help='YAML file with diagnostic rules'
    )
    
    parser.add_argument(
        '--astro',
        required=True,
        help='YAML file with astrological mappings'
    )
    
    parser.add_argument(
        '--out',
        default='out/cards.md',
        help='Output Markdown file for cards (default: out/cards.md)'
    )
    
    parser.add_argument(
        '--style',
        choices=['gptoss'],
        help='Optional style enhancement (gptoss for AI paraphrasing)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Features file: {args.features}", file=sys.stderr)
        print(f"Rules file: {args.rules}", file=sys.stderr)
        print(f"Astro file: {args.astro}", file=sys.stderr)
        print(f"Output file: {args.out}", file=sys.stderr)
        print(f"Style: {args.style}", file=sys.stderr)
    
    # Validate input files
    for file_path in [args.features, args.rules, args.astro]:
        if not Path(file_path).exists():
            print(f"Error: File '{file_path}' not found", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Load data
        features = load_features(args.features)
        rules = load_rules(args.rules)
        astro_map = load_astro_map(args.astro)
        
        if not features:
            print("Error: No features found in input file", file=sys.stderr)
            sys.exit(1)
        
        # Ensure output directory exists
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate cards
        use_gptoss = args.style == 'gptoss'
        cards_content = []
        
        for i, shot_features in enumerate(features):
            if args.verbose:
                print(f"Processing shot {i+1}/{len(features)}: {shot_features.get('shot_id', 'Unknown')}", file=sys.stderr)
            
            card = generate_card(shot_features, rules, astro_map, use_gptoss)
            cards_content.append(card)
        
        # Write output
        with open(args.out, 'w') as f:
            f.write("# ☕ Espresso Horoscope Cards\n\n")
            f.write(f"*Generated from {len(features)} shot(s)*\n\n")
            f.writelines(cards_content)
        
        print(f"Generated {len(features)} horoscope cards in {args.out}", file=sys.stderr)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
