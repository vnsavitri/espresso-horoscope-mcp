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
import requests
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


def get_coffee_shot_type(features: Dict[str, Any]) -> str:
    """
    Determine coffee shot type based on brew ratio and extraction time.
    
    Args:
        features: Shot features containing brew_ratio, shot_end_s, dose_g, final_weight_g
        
    Returns:
        Coffee shot type string (e.g., "Ristretto", "Espresso", "Lungo")
    """
    # Try to get brew_ratio directly first, then calculate from dose/weight
    brew_ratio = features.get("brew_ratio")
    
    if brew_ratio is None:
        # Fallback: calculate from dose and final weight
        dose_g = features.get("dose_g", 18.0)
        final_weight_g = features.get("final_weight_g", 36.0)
        brew_ratio = final_weight_g / dose_g if dose_g > 0 else 2.0
    
    shot_end_s = features.get("shot_end_s", 30.0)
    
    # Determine shot type based on ratio
    if brew_ratio <= 1.8:
        return "Ristretto"
    elif brew_ratio <= 2.5:
        return "Espresso"
    elif brew_ratio <= 3.5:
        return "Lungo"
    else:
        return "Americano"


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


def get_zodiac_info(birth_mmdd: str) -> tuple[str, str]:
    """
    Map birth date (MMDD) to zodiac sign and icon.
    
    Returns:
        Tuple of (zodiac_name, zodiac_icon)
    """
    month = int(birth_mmdd[:2])
    day = int(birth_mmdd[2:])
    
    # Zodiac date ranges with fun animal emojis
    zodiac_dates = [
        (1, 20, 2, 18, "Aquarius", "🐬"),
        (2, 19, 3, 20, "Pisces", "🐟"),
        (3, 21, 4, 19, "Aries", "🐏"),
        (4, 20, 5, 20, "Taurus", "🐂"),
        (5, 21, 6, 20, "Gemini", "👯‍♂️"),
        (6, 21, 7, 22, "Cancer", "🦀"),
        (7, 23, 8, 22, "Leo", "🦁"),
        (8, 23, 9, 22, "Virgo", "🦋"),
        (9, 23, 10, 22, "Libra", "🦢"),
        (10, 23, 11, 21, "Scorpio", "🦂"),
        (11, 22, 12, 21, "Sagittarius", "🏹"),
        (12, 22, 1, 19, "Capricorn", "🐐")
    ]
    
    for start_month, start_day, end_month, end_day, zodiac_name, zodiac_icon in zodiac_dates:
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return zodiac_name, zodiac_icon
    
    # Default fallback
    return "Unknown", "☕"


def get_style_bank_for_user(user_birth_mmdd: str) -> str:
    """
    Determine style bank based on user's birth date for variety.
    
    Args:
        user_birth_mmdd: User's birth month/day (MMDD format)
        
    Returns:
        Style bank name (chill, punchy, nerdy, mystical)
    """
    # Use birth date to deterministically select style
    # This ensures same user always gets same style, but different users get different styles
    month = int(user_birth_mmdd[:2])
    day = int(user_birth_mmdd[2:])
    
    # Create a simple hash from month and day
    style_hash = (month * 31 + day) % 4
    
    style_banks = ["chill", "punchy", "nerdy", "mystical"]
    return style_banks[style_hash]


def get_dynamic_style_bank(features: Dict[str, Any], user_birth_mmdd: str, use_gptoss: bool = False) -> str:
    """
    Get dynamic style bank combining coffee profile and daily mood.
    
    Args:
        features: Shot features
        user_birth_mmdd: User's birth date
        use_gptoss: Whether to use GPT-OSS for generation
        
    Returns:
        Dynamic style bank name
    """
    try:
        # Import from the same directory
        import sys
        from pathlib import Path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        from dynamic_style import get_dynamic_style_bank as get_dynamic_style
        style = get_dynamic_style(features, user_birth_mmdd, use_gptoss)
        return style
    except Exception as e:
        print(f"Warning: Could not use dynamic_style: {e}", file=sys.stderr)
        # Fallback to static style bank
        return get_style_bank_for_user(user_birth_mmdd)


def get_dynamic_reading(features: Dict[str, Any], rule_id: str, use_gptoss: bool = True) -> str:
    """
    Get a dynamic, creative reading for the shot.
    
    Args:
        features: Shot features
        rule_id: Diagnostic rule ID
        use_gptoss: Whether to use GPT-OSS for generation
        
    Returns:
        Creative reading
    """
    try:
        # Import from the same directory
        import sys
        from pathlib import Path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        from dynamic_readings import get_dynamic_reading as get_dynamic_reading_func
        return get_dynamic_reading_func(features, rule_id, use_gptoss)
    except Exception as e:
        print(f"Warning: Could not use dynamic_readings: {e}", file=sys.stderr)
        # Fallback to static template
        astro_data = {"template": "Your espresso tells a unique story..."}
        return render_template(astro_data.get("template", "Your espresso tells a story..."), features)


def extract_tones_from_dynamic_style(style_bank: str) -> List[str]:
    """
    Extract tone words from dynamic style bank names.
    
    Args:
        style_bank: Dynamic style bank name (e.g., "cosmic-rhythm", "stellar-intensity")
        
    Returns:
        List of tone words
    """
    # Map dynamic style patterns to tone words
    style_mappings = {
        "cosmic": ["cosmic", "ethereal", "transcendent", "otherworldly"],
        "stellar": ["stellar", "brilliant", "radiant", "luminous"],
        "lunar": ["lunar", "mystical", "dreamy", "serene"],
        "nebula": ["nebula", "flowing", "swirling", "gentle"],
        "stellar": ["stellar", "dynamic", "energetic", "vibrant"],
        "chaos": ["chaotic", "wild", "unpredictable", "creative"],
        "balance": ["balanced", "harmonious", "perfect", "smooth"],
        "rhythm": ["rhythmic", "flowing", "steady", "consistent"],
        "intensity": ["intense", "powerful", "dramatic", "bold"],
        "patience": ["patient", "calm", "peaceful", "contemplative"]
    }
    
    # Extract key words from style name
    style_lower = style_bank.lower()
    tones = []
    
    # Check for known patterns
    for pattern, tone_words in style_mappings.items():
        if pattern in style_lower:
            tones.extend(tone_words)
    
    # If no patterns found, use the style name itself
    if not tones:
        # Split on hyphens and use the words
        words = style_lower.replace("-", " ").split()
        tones = words + ["mystical", "cosmic"]
    
    return tones[:4]  # Return up to 4 tone words


def get_personalized_flavour_line(
    features: Dict[str, Any], 
    rule_id: str, 
    flavour_banks: Dict[str, Any], 
    seed: str,
    user_birth_mmdd: str = None,
    style_bank: str = "chill"
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
    # Handle both static style banks and dynamic style banks
    if style_bank in flavour_banks.get("tones", {}):
        # Static style bank (chill, punchy, nerdy, mystical)
        tones = flavour_banks.get("tones", {}).get(style_bank, ["gentle", "smooth"])
    else:
        # Dynamic style bank - extract tone from the style name
        tones = extract_tones_from_dynamic_style(style_bank)
    
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
    style_bank: str = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a single horoscope card with seeded variations.
    
    Returns:
        Tuple of (markdown_card, json_data)
    """
    # Determine style bank if not provided
    if style_bank is None:
        # Use dynamic style bank that combines coffee profile + daily mood
        style_bank = get_dynamic_style_bank(features, user_birth_mmdd or "0101", use_gptoss)
    
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
    
    # Get zodiac information
    zodiac_name, zodiac_icon = get_zodiac_info(user_birth_mmdd or "0101")
    
    # Get coffee shot type
    coffee_type = get_coffee_shot_type(features)
    
    # Get seeded variations
    base_title, tagline = get_seeded_variations(rule_id, flavour_banks, seed)
    
    # Combine coffee type with title
    title = f"{coffee_type} • {base_title}"
    
    # Get personalized flavour line
    flavour_line = get_personalized_flavour_line(
        features, rule_id, flavour_banks, seed, user_birth_mmdd, style_bank
    )
    
    # Build card
    emoji = astro_data.get("emoji", "☕")
    
    # Generate dynamic, creative reading
    rendered_template = get_dynamic_reading(features, rule_id, use_gptoss)
    
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
    
    # Get current date and time for historical tracking
    from datetime import datetime
    current_datetime = datetime.now()
    
    # Build JSON data for structured output
    json_data = {
        "shot_id": shot_id,
        "timestamp": current_datetime.isoformat(),
        "date": current_datetime.strftime("%Y-%m-%d"),
        "time": current_datetime.strftime("%H:%M"),
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
            "zodiac": zodiac_name,
            "zodiac_icon": zodiac_icon,
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


def generate_png_card(json_data: Dict[str, Any], output_dir: Path = None) -> Optional[bytes]:
    """
    Generate a PNG card by calling the Next.js API.
    
    Args:
        json_data: The card data from generate_card()
        output_dir: Optional directory to save the PNG file
        
    Returns:
        PNG bytes if successful, None if failed
    """
    try:
        # Extract data for API payload
        card_data = json_data["card"]
        snapshot = card_data["snapshot"]
        
        # Map zodiac icon to sign name (remove emoji, get sign name)
        zodiac_icon = card_data.get("zodiac_icon", "☕")
        sign_name = card_data.get("zodiac", "unknown").lower()
        
        # Create API payload
        payload = {
            "sign": sign_name,
            "signLabel": card_data.get("zodiac", "UNKNOWN").upper(),
            "title": card_data.get("title", "Cosmic Reading"),
            "subtitle": f'"{card_data.get("mantra", "Brew with intention.")}"',
            "metrics": {
                "ratio": f"{snapshot['brew_ratio']:.2f}:1",
                "time": f"{snapshot['shot_time']:.0f}s",
                "pressure": f"{snapshot['peak_pressure']:.1f} bar",
                "temp": f"{snapshot['temp_avg']:.1f} °C",
                "rdt": f"{snapshot['channeling']:.2f}"
            },
            "bullets": card_data.get("advice", [])[:3],  # Limit to 3 bullets
            "message": card_data.get("template", "Your espresso tells a story..."),
            "meta": f"seed: {card_data.get('seed', 'unknown')[:8]} • rule: {card_data.get('rule_hit', 'unknown')} • severity: {card_data.get('rule_hit', 'unknown')}",
            "footer": "Espresso Horoscope",
            "format": "png"
        }
        
        # Call the Next.js API
        api_url = "http://localhost:3001/api/card"
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            png_data = response.content
            
            # Save to file if output directory specified
            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                shot_id = json_data.get("shot_id", "unknown")
                filename = f"card_{shot_id}.png"
                filepath = output_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(png_data)
                
                print(f"Saved PNG card: {filepath}", file=sys.stderr)
            
            return png_data
        else:
            print(f"API error: {response.status_code} - {response.text}", file=sys.stderr)
            return None
            
    except requests.exceptions.ConnectionError:
        print("Warning: Could not connect to Next.js API (http://localhost:3001/api/card)", file=sys.stderr)
        print("Make sure the Next.js server is running with: npm run dev", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error generating PNG card: {e}", file=sys.stderr)
        return None


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
        default=None,
        help='Style preference for tone variations (default: auto-detect from birth date)'
    )
    
    parser.add_argument(
        '--png',
        action='store_true',
        help='Generate PNG cards using Next.js API (requires server running)'
    )
    
    parser.add_argument(
        '--png-dir',
        default='out/cards',
        help='Directory to save PNG cards (default: out/cards)'
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
        
        # Use dynamic style bank based on birth date, or override with command line
        if args.style_bank:
            style_bank = args.style_bank
        else:
            # Will be determined dynamically in generate_card based on features
            style_bank = None
        
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
            
            # Generate PNG card if requested
            if args.png:
                png_dir = Path(args.png_dir)
                png_data = generate_png_card(json_data, png_dir)
                if png_data:
                    json_data["png_generated"] = True
                    json_data["png_path"] = str(png_dir / f"card_{json_data['shot_id']}.png")
                else:
                    json_data["png_generated"] = False
                    json_data["png_error"] = "Failed to generate PNG"
        
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
        
        # Summary
        print(f"✅ Generated {len(features)} horoscope cards in {args.out}", file=sys.stderr)
        if args.png:
            png_count = sum(1 for data in json_data_list if data.get("png_generated", False))
            print(f"🖼️  Generated {png_count}/{len(features)} PNG cards in {args.png_dir}", file=sys.stderr)
            if png_count < len(features):
                print("⚠️  Some PNG cards failed to generate. Check Next.js server is running.", file=sys.stderr)
        
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
