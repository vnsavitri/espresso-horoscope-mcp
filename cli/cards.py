#!/usr/bin/env python3
"""
Espresso Horoscope Card Generator

Generates astrological horoscope cards from espresso shot features.
Now with seeded variations for consistent yet personalized readings.
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

# Import the seeding system
from seed_util import (
    generate_seed, SeededRandom, load_user_config, save_user_config,
    add_reading_to_history, analyze_reading_trends
)


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


def load_flavour_banks(flavour_file: str) -> Dict[str, Any]:
    """Load flavour variation banks from YAML file."""
    with open(flavour_file, 'r') as f:
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


def get_seeded_variations(rule_id: str, flavour_banks: Dict[str, Any], seed: str) -> Tuple[str, str]:
    """
    Get seeded title and tagline variations for a rule.
    
    Args:
        rule_id: The diagnostic rule ID
        flavour_banks: Loaded flavour banks from YAML
        seed: Deterministic seed for consistent selection
        
    Returns:
        Tuple of (title, tagline)
    """
    sr = SeededRandom(seed)
    
    # Get title options
    title_options = flavour_banks.get("titles", {}).get(rule_id, [f"{rule_id.replace('_', ' ').title()}"])
    title = sr.choice(title_options)
    
    # Get tagline options
    tagline_options = flavour_banks.get("taglines", {}).get(rule_id, ["Brew with intention"])
    tagline = sr.choice(tagline_options)
    
    return title, tagline


def get_personalized_flavour_line(
    features: Dict[str, Any], 
    rule_id: str, 
    flavour_banks: Dict[str, Any], 
    seed: str,
    user_birth_mmdd: str = None
) -> str:
    """
    Generate a personalized flavour line using seeded variations.
    
    Args:
        features: Shot features
        rule_id: Diagnostic rule ID
        flavour_banks: Loaded flavour banks
        seed: Deterministic seed
        user_birth_mmdd: User's birth month/day for personalization
        
    Returns:
        Personalized flavour line
    """
    sr = SeededRandom(seed)
    
    # Get cosmic nouns and verbs
    cosmic_nouns = flavour_banks.get("cosmic_nouns", ["cosmos", "universe"])
    cosmic_verbs = flavour_banks.get("cosmic_verbs", ["dances", "flows"])
    
    # Get tonal variations based on style
    tones = flavour_banks.get("tones", {}).get("chill", ["gentle", "smooth"])
    
    # Select seeded variations
    noun = sr.choice(cosmic_nouns)
    verb = sr.choice(cosmic_verbs)
    tone = sr.choice(tones)
    
    # Create personalized line
    if user_birth_mmdd:
        # Add birth sign personalization (simplified)
        month = int(user_birth_mmdd[:2])
        signs = ["Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini",
                "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius"]
        sign = signs[(month - 1) % 12]
        
        flavour_line = f"Your {sign} energy {verb} through this {tone} {noun}, creating cosmic harmony in every drop."
    else:
        flavour_line = f"Your shot {verb} like a {tone} {noun}, weaving cosmic magic into every sip."
    
    return flavour_line




def generate_card(
    features: Dict[str, Any], 
    rules: Dict[str, Any], 
    astro_map: Dict[str, Any], 
    flavour_banks: Dict[str, Any],
    use_gptoss: bool = False,
    user_birth_mmdd: str = None,
    style_bank: str = "chill"
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a single horoscope card with seeded variations.
    
    Returns:
        Tuple of (markdown_card, json_data)
    """
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
    
    # Generate seed for this shot
    seed = generate_seed(shot_id, user_birth_mmdd or "0101", style_bank)
    
    # Get seeded variations
    title, tagline = get_seeded_variations(rule_id, flavour_banks, seed)
    
    # Get personalized flavour line
    flavour_line = get_personalized_flavour_line(
        features, rule_id, flavour_banks, seed, user_birth_mmdd
    )
    
    # Build card
    emoji = astro_data.get("emoji", "☕")
    template = astro_data.get("template", "Your espresso tells a story...")
    
    # Render template
    rendered_template = render_template(template, features)
    
    # Apply gpt-oss if requested
    if use_gptoss:
        rendered_template = enhance_text_with_gptoss(rendered_template)
    
    # Build markdown card
    card = f"""## {emoji} {title}

**Shot ID:** {shot_id}  
**Mantra:** *{tagline}*

### 📊 Brew Snapshot
- **Ratio:** {brew_ratio:.2f}:1
- **Time:** {shot_end_s:.0f}s
- **Peak Pressure:** {peak_pressure_bar:.1f} bar
- **Temperature:** {temp_avg_c:.1f}°C
- **Channeling:** {channeling_score:.2f}

### 🔮 Cosmic Reading
{rendered_template}

### ✨ Personal Touch
{flavour_line}

### 💡 Brewing Wisdom
"""
    
    # Add advice lines
    advice_list = rule_data.get("advice", [])
    for advice in advice_list:
        card += f"- {advice}\n"
    
    card += "\n---\n\n"
    
    # Build JSON data for structured output
    json_data = {
        "shot_id": shot_id,
        "user_context": {
            "birth_mmdd": user_birth_mmdd,
            "style_preference": style_bank,
            "generation_date": features.get("generation_date", "unknown")
        },
        "card": {
            "emoji": emoji,
            "title": title,
            "mantra": tagline,
            "rule_hit": rule_id,
            "seed": seed,
            "snapshot": {
                "brew_ratio": brew_ratio,
                "shot_time": shot_end_s,
                "peak_pressure": peak_pressure_bar,
                "temp_avg": temp_avg_c,
                "channeling": channeling_score
            },
            "advice": advice_list,
            "flavour_line": flavour_line,
            "template": rendered_template
        }
    }
    
    return card, json_data


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
        '--flavour',
        default='content/flavour.yaml',
        help='YAML file with flavour variation banks (default: content/flavour.yaml)'
    )
    
    parser.add_argument(
        '--out',
        default='out/cards.md',
        help='Output Markdown file for cards (default: out/cards.md)'
    )
    
    parser.add_argument(
        '--json-out',
        help='Output JSON file for structured data (optional)'
    )
    
    parser.add_argument(
        '--style',
        choices=['gptoss'],
        help='Optional style enhancement (gptoss for AI paraphrasing)'
    )
    
    parser.add_argument(
        '--birth-date',
        help='User birth date in MMDD format (e.g., 0615 for June 15th)'
    )
    
    parser.add_argument(
        '--style-bank',
        choices=['chill', 'punchy', 'nerdy', 'mystical'],
        default='chill',
        help='Style preference for tone variations (default: chill)'
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
        print(f"Flavour file: {args.flavour}", file=sys.stderr)
        print(f"Output file: {args.out}", file=sys.stderr)
        print(f"JSON output: {args.json_out}", file=sys.stderr)
        print(f"Style: {args.style}", file=sys.stderr)
        print(f"Birth date: {args.birth_date}", file=sys.stderr)
        print(f"Style bank: {args.style_bank}", file=sys.stderr)
    
    # Validate input files
    for file_path in [args.features, args.rules, args.astro, args.flavour]:
        if not Path(file_path).exists():
            print(f"Error: File '{file_path}' not found", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Load user config or use command line args
        user_config = load_user_config()
        user_birth_mmdd = args.birth_date or user_config.get("birth_mmdd")
        style_bank = args.style_bank or user_config.get("style_bank", "chill")
        
        # If this is first use and no birth date provided, prompt for it
        if user_config.get("first_use", True) and not user_birth_mmdd:
            print("🌟 Welcome to Espresso Horoscope! 🌟", file=sys.stderr)
            print("To personalize your readings, please provide your birth date.", file=sys.stderr)
            print("Example: --birth-date 0615 (for June 15th)", file=sys.stderr)
            print("You can also set it permanently by running with --birth-date once.", file=sys.stderr)
            user_birth_mmdd = "0101"  # Default fallback
        
        # Update config if birth date was provided
        if args.birth_date:
            user_config["birth_mmdd"] = args.birth_date
            user_config["first_use"] = False
            save_user_config(user_config)
        
        # Load data
        features = load_features(args.features)
        rules = load_rules(args.rules)
        astro_map = load_astro_map(args.astro)
        flavour_banks = load_flavour_banks(args.flavour)
        
        if not features:
            print("Error: No features found in input file", file=sys.stderr)
            sys.exit(1)
        
        # Ensure output directory exists
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate cards
        use_gptoss = args.style == 'gptoss'
        cards_content = []
        json_data_list = []
        
        for i, shot_features in enumerate(features):
            if args.verbose:
                print(f"Processing shot {i+1}/{len(features)}: {shot_features.get('shot_id', 'Unknown')}", file=sys.stderr)
            
            card, json_data = generate_card(
                shot_features, rules, astro_map, flavour_banks, 
                use_gptoss, user_birth_mmdd, style_bank
            )
            cards_content.append(card)
            json_data_list.append(json_data)
            
            # Add to reading history
            add_reading_to_history(
                "default",  # user_id
                json_data["shot_id"],
                json_data["card"]["seed"],
                style_bank,
                json_data["card"]["rule_hit"],
                json_data["card"]["title"],
                json_data["card"]["emoji"]
            )
        
        # Write markdown output
        with open(args.out, 'w') as f:
            f.write("# ☕ Espresso Horoscope Cards\n\n")
            f.write(f"*Generated from {len(features)} shot(s)*\n")
            f.write(f"*User: {user_birth_mmdd} | Style: {style_bank}*\n\n")
            f.writelines(cards_content)
        
        # Write JSON output (always write to out/cards.json, plus custom path if specified)
        json_output_path = Path("out/cards.json")
        json_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(json_output_path, 'w') as f:
            json.dump({
                "metadata": {
                    "generated_at": features[0].get("generation_date", "unknown"),
                    "user_birth_mmdd": user_birth_mmdd,
                    "style_bank": style_bank,
                    "total_shots": len(features)
                },
                "readings": json_data_list
            }, f, indent=2)
        
        print(f"Generated structured data in {json_output_path}", file=sys.stderr)
        
        # Also write to custom path if specified
        if args.json_out:
            custom_json_path = Path(args.json_out)
            custom_json_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(custom_json_path, 'w') as f:
                json.dump({
                    "metadata": {
                        "generated_at": features[0].get("generation_date", "unknown"),
                        "user_birth_mmdd": user_birth_mmdd,
                        "style_bank": style_bank,
                        "total_shots": len(features)
                    },
                    "readings": json_data_list
                }, f, indent=2)
            
            print(f"Generated structured data in {args.json_out}", file=sys.stderr)
        
        print(f"Generated {len(features)} horoscope cards in {args.out}", file=sys.stderr)
        
        # Show reading trends if available
        trends = analyze_reading_trends("default")
        if trends["total_readings"] > 1:
            print(f"📊 Reading trends: {trends['total_readings']} total readings", file=sys.stderr)
            if trends["rule_patterns"]:
                most_common = max(trends["rule_patterns"].items(), key=lambda x: x[1])
                print(f"   Most common reading: {most_common[0]} ({most_common[1]} times)", file=sys.stderr)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
