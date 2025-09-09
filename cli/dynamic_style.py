#!/usr/bin/env python3
"""
Dynamic Style Bank Generator

Creates personalized style descriptions by combining:
1. Coffee profile analysis (based on shot characteristics)
2. Daily mood calculation (birth date + current date)
3. GPT-OSS generation for unique, creative style descriptions
"""

import hashlib
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import requests
import os


def analyze_coffee_profile(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze shot characteristics to determine coffee personality profile.
    
    Args:
        features: Shot features dictionary
        
    Returns:
        Dictionary with coffee profile analysis
    """
    brew_ratio = features.get("brew_ratio", 0)
    shot_time = features.get("shot_end_s", 0)
    peak_pressure = features.get("peak_pressure_bar", 0)
    temp_avg = features.get("temp_avg_c", 0)
    channeling = features.get("channeling_score_0_1", 0)
    rule_hit = features.get("rule_hit", "unknown")
    
    profile = {
        "personality": [],
        "energy_level": "medium",
        "mood": "neutral",
        "characteristics": []
    }
    
    # Analyze based on rule hit
    if rule_hit == "under_extracted_fast":
        profile["personality"].extend(["energetic", "rushed", "dynamic"])
        profile["energy_level"] = "high"
        profile["mood"] = "excited"
        profile["characteristics"].extend(["quick", "impatient", "spontaneous"])
        
    elif rule_hit == "over_extracted_slow":
        profile["personality"].extend(["patient", "methodical", "contemplative"])
        profile["energy_level"] = "low"
        profile["mood"] = "calm"
        profile["characteristics"].extend(["slow", "thorough", "deliberate"])
        
    elif rule_hit == "choking_high_resistance":
        profile["personality"].extend(["intense", "focused", "determined"])
        profile["energy_level"] = "high"
        profile["mood"] = "intense"
        profile["characteristics"].extend(["stubborn", "persistent", "strong-willed"])
        
    elif rule_hit == "channeling_instability":
        profile["personality"].extend(["chaotic", "creative", "unpredictable"])
        profile["energy_level"] = "variable"
        profile["mood"] = "erratic"
        profile["characteristics"].extend(["wild", "artistic", "unconventional"])
        
    elif rule_hit == "temp_low_flat":
        profile["personality"].extend(["mellow", "gentle", "understated"])
        profile["energy_level"] = "low"
        profile["mood"] = "peaceful"
        profile["characteristics"].extend(["quiet", "subtle", "soft"])
        
    elif rule_hit == "temp_high_bitter":
        profile["personality"].extend(["intense", "sharp", "bold"])
        profile["energy_level"] = "high"
        profile["mood"] = "fiery"
        profile["characteristics"].extend(["strong", "assertive", "dramatic"])
        
    elif rule_hit == "sweet_spot":
        profile["personality"].extend(["balanced", "harmonious", "perfect"])
        profile["energy_level"] = "medium"
        profile["mood"] = "content"
        profile["characteristics"].extend(["ideal", "smooth", "well-rounded"])
    
    # Add numerical analysis
    if brew_ratio < 1.5:
        profile["characteristics"].append("concentrated")
    elif brew_ratio > 2.5:
        profile["characteristics"].append("diluted")
    
    if shot_time < 20:
        profile["characteristics"].append("quick")
    elif shot_time > 40:
        profile["characteristics"].append("extended")
    
    if peak_pressure > 10:
        profile["characteristics"].append("high-pressure")
    elif peak_pressure < 7:
        profile["characteristics"].append("low-pressure")
    
    if channeling > 0.2:
        profile["characteristics"].append("unstable")
    elif channeling < 0.05:
        profile["characteristics"].append("stable")
    
    return profile


def analyze_shot_variation(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze shot-specific characteristics for style variation.
    
    Args:
        features: Shot features dictionary
        
    Returns:
        Shot variation analysis
    """
    brew_ratio = features.get("brew_ratio", 0)
    shot_time = features.get("shot_end_s", 0)
    peak_pressure = features.get("peak_pressure_bar", 0)
    temp_avg = features.get("temp_avg_c", 0)
    channeling = features.get("channeling_score_0_1", 0)
    flow_avg = features.get("flow_avg_ml_s", 0)
    
    variation = {
        "intensity": "medium",
        "rhythm": "steady",
        "character": "balanced",
        "energy": "moderate",
        "mood_shift": "neutral"
    }
    
    # Analyze brew ratio for intensity
    if brew_ratio < 1.5:
        variation["intensity"] = "high"
        variation["character"] = "concentrated"
    elif brew_ratio > 2.5:
        variation["intensity"] = "low"
        variation["character"] = "diluted"
    
    # Analyze shot time for rhythm
    if shot_time < 20:
        variation["rhythm"] = "fast"
        variation["energy"] = "high"
    elif shot_time > 40:
        variation["rhythm"] = "slow"
        variation["energy"] = "low"
    
    # Analyze pressure for character
    if peak_pressure > 10:
        variation["character"] = "powerful"
        variation["mood_shift"] = "intense"
    elif peak_pressure < 7:
        variation["character"] = "gentle"
        variation["mood_shift"] = "calm"
    
    # Analyze temperature for energy
    if temp_avg > 95:
        variation["energy"] = "high"
        variation["mood_shift"] = "fiery"
    elif temp_avg < 90:
        variation["energy"] = "low"
        variation["mood_shift"] = "cool"
    
    # Analyze channeling for stability
    if channeling > 0.2:
        variation["rhythm"] = "chaotic"
        variation["character"] = "unstable"
    elif channeling < 0.05:
        variation["rhythm"] = "perfect"
        variation["character"] = "stable"
    
    return variation


def analyze_time_variation(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze time-based characteristics for style variation.
    
    Args:
        features: Shot features dictionary
        
    Returns:
        Time variation analysis
    """
    from datetime import datetime
    
    # Get current time
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    # Get shot timestamp if available
    shot_timestamp = features.get("timestamp", None)
    if shot_timestamp:
        try:
            if isinstance(shot_timestamp, str):
                # Parse ISO format
                shot_time = datetime.fromisoformat(shot_timestamp.replace('Z', '+00:00'))
            else:
                shot_time = datetime.fromtimestamp(shot_timestamp)
            hour = shot_time.hour
            minute = shot_time.minute
        except:
            pass  # Use current time as fallback
    
    variation = {
        "time_of_day": "day",
        "cosmic_phase": "neutral",
        "energy_level": "medium",
        "mood_influence": "balanced"
    }
    
    # Determine time of day
    if 5 <= hour < 12:
        variation["time_of_day"] = "morning"
        variation["cosmic_phase"] = "rising"
        variation["energy_level"] = "high"
        variation["mood_influence"] = "energetic"
    elif 12 <= hour < 17:
        variation["time_of_day"] = "afternoon"
        variation["cosmic_phase"] = "peak"
        variation["energy_level"] = "medium"
        variation["mood_influence"] = "focused"
    elif 17 <= hour < 21:
        variation["time_of_day"] = "evening"
        variation["cosmic_phase"] = "setting"
        variation["energy_level"] = "medium"
        variation["mood_influence"] = "relaxed"
    else:
        variation["time_of_day"] = "night"
        variation["cosmic_phase"] = "deep"
        variation["energy_level"] = "low"
        variation["mood_influence"] = "contemplative"
    
    # Add minute-based micro-variation
    if minute < 15:
        variation["cosmic_phase"] += "-early"
    elif minute > 45:
        variation["cosmic_phase"] += "-late"
    
    return variation


def calculate_daily_mood(user_birth_mmdd: str, current_date: str = None) -> Dict[str, Any]:
    """
    Calculate daily mood based on birth date and current date.
    
    Args:
        user_birth_mmdd: User's birth date in MMDD format
        current_date: Current date in YYYY-MM-DD format (defaults to today)
        
    Returns:
        Dictionary with daily mood analysis
    """
    if current_date is None:
        current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Parse dates
    birth_month = int(user_birth_mmdd[:2])
    birth_day = int(user_birth_mmdd[2:])
    current_dt = datetime.strptime(current_date, "%Y-%m-%d")
    
    # Calculate cosmic influences
    day_of_year = current_dt.timetuple().tm_yday
    birth_day_of_year = (birth_month - 1) * 30 + birth_day  # Simplified
    
    # Distance from birthday (0-365)
    birthday_distance = abs(day_of_year - birth_day_of_year)
    if birthday_distance > 182:
        birthday_distance = 365 - birthday_distance
    
    # Moon phase influence (simplified)
    moon_phase = (day_of_year + birth_day) % 28
    
    # Seasonal influence
    season = get_season_from_date(current_dt)
    
    # Calculate mood factors
    cosmic_energy = (birthday_distance / 182.0) * 100  # 0-100%
    lunar_influence = (moon_phase / 28.0) * 100  # 0-100%
    
    # Determine overall mood
    if cosmic_energy > 80:
        mood_level = "high"
        mood_descriptors = ["energetic", "optimistic", "vibrant"]
    elif cosmic_energy > 60:
        mood_level = "medium-high"
        mood_descriptors = ["positive", "confident", "upbeat"]
    elif cosmic_energy > 40:
        mood_level = "medium"
        mood_descriptors = ["balanced", "steady", "content"]
    elif cosmic_energy > 20:
        mood_level = "medium-low"
        mood_descriptors = ["mellow", "reflective", "calm"]
    else:
        mood_level = "low"
        mood_descriptors = ["peaceful", "contemplative", "serene"]
    
    # Lunar influence
    if lunar_influence > 75:
        lunar_effect = "intense"
    elif lunar_influence > 50:
        lunar_effect = "moderate"
    elif lunar_influence > 25:
        lunar_effect = "gentle"
    else:
        lunar_effect = "subtle"
    
    return {
        "cosmic_energy": cosmic_energy,
        "lunar_influence": lunar_influence,
        "mood_level": mood_level,
        "mood_descriptors": mood_descriptors,
        "lunar_effect": lunar_effect,
        "season": season,
        "birthday_distance": birthday_distance,
        "moon_phase": moon_phase
    }


def get_season_from_date(date: datetime) -> str:
    """Get season from date."""
    month = date.month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"


def generate_dynamic_style_with_gptoss(
    coffee_profile: Dict[str, Any], 
    daily_mood: Dict[str, Any],
    user_birth_mmdd: str,
    shot_variation: Dict[str, Any] = None,
    time_variation: Dict[str, Any] = None
) -> str:
    """
    Generate a unique style description using GPT-OSS.
    
    Args:
        coffee_profile: Coffee personality analysis
        daily_mood: Daily mood analysis
        user_birth_mmdd: User's birth date
        shot_variation: Shot-specific variation analysis
        time_variation: Time-based variation analysis
        
    Returns:
        Unique style description
    """
    # Prepare the prompt
    prompt = f"""
You are a cosmic coffee oracle creating a unique style description for an espresso horoscope reading.

COFFEE PROFILE:
- Personality: {', '.join(coffee_profile['personality'])}
- Energy Level: {coffee_profile['energy_level']}
- Mood: {coffee_profile['mood']}
- Characteristics: {', '.join(coffee_profile['characteristics'])}

DAILY MOOD:
- Cosmic Energy: {daily_mood['cosmic_energy']:.1f}%
- Mood Level: {daily_mood['mood_level']}
- Mood Descriptors: {', '.join(daily_mood['mood_descriptors'])}
- Lunar Effect: {daily_mood['lunar_effect']}
- Season: {daily_mood['season']}

SHOT VARIATION:
- Intensity: {shot_variation.get('intensity', 'medium') if shot_variation else 'medium'}
- Rhythm: {shot_variation.get('rhythm', 'steady') if shot_variation else 'steady'}
- Character: {shot_variation.get('character', 'balanced') if shot_variation else 'balanced'}
- Energy: {shot_variation.get('energy', 'moderate') if shot_variation else 'moderate'}
- Mood Shift: {shot_variation.get('mood_shift', 'neutral') if shot_variation else 'neutral'}

TIME VARIATION:
- Time of Day: {time_variation.get('time_of_day', 'day') if time_variation else 'day'}
- Cosmic Phase: {time_variation.get('cosmic_phase', 'neutral') if time_variation else 'neutral'}
- Energy Level: {time_variation.get('energy_level', 'medium') if time_variation else 'medium'}
- Mood Influence: {time_variation.get('mood_influence', 'balanced') if time_variation else 'balanced'}

USER BIRTH DATE: {user_birth_mmdd}

Create a unique, creative style description that combines:
1. The coffee's personality and characteristics
2. The daily cosmic mood and energy
3. The shot's specific variation and rhythm
4. The time of day and cosmic phase
5. The user's birth date influence

The style should be:
- 2-3 words maximum
- Hyphenated (e.g., "cosmic-rhythm", "stellar-harmony", "morning-pulse", "evening-flow")
- Unique and creative
- Cosmic/astrological themed
- Reflects the combination of ALL factors above

Respond with ONLY the style description, no other text.
"""

    try:
        # Get GPT-OSS endpoint from environment
        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": "You are a cosmic coffee oracle. Create unique, mystical style descriptions."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 100
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            style_text = result["choices"][0]["message"]["content"].strip()
            # Clean up the response
            style_text = style_text.replace('"', '').replace("'", "").strip()
            return style_text
        else:
            print(f"GPT-OSS API error: {response.status_code}", file=sys.stderr)
            return generate_fallback_style(coffee_profile, daily_mood, shot_variation, time_variation)
            
    except Exception as e:
        print(f"Warning: Could not connect to GPT-OSS: {e}", file=sys.stderr)
        return generate_fallback_style(coffee_profile, daily_mood, shot_variation, time_variation)


def generate_fallback_style(
    coffee_profile: Dict[str, Any], 
    daily_mood: Dict[str, Any],
    shot_variation: Dict[str, Any] = None,
    time_variation: Dict[str, Any] = None
) -> str:
    """
    Generate a fallback style when GPT-OSS is not available.
    
    Args:
        coffee_profile: Coffee personality analysis
        daily_mood: Daily mood analysis
        shot_variation: Shot-specific variation analysis
        time_variation: Time-based variation analysis
        
    Returns:
        Fallback style description
    """
    # Combine all characteristics
    coffee_traits = coffee_profile["personality"][:2]  # Take first 2
    mood_traits = daily_mood["mood_descriptors"][:1]   # Take first 1
    
    # Create style combinations with variations
    style_options = []
    
    # Base combinations
    if len(coffee_traits) > 0 and len(mood_traits) > 0:
        style_options.append(f"{coffee_traits[0]}-{mood_traits[0]}")
    else:
        style_options.append("cosmic-balance")
    
    # Add shot variation influences
    if shot_variation:
        shot_rhythm = shot_variation.get("rhythm", "steady")
        shot_character = shot_variation.get("character", "balanced")
        
        if shot_rhythm == "fast":
            style_options.extend(["stellar-pulse", "cosmic-rush", "nebula-burst"])
        elif shot_rhythm == "slow":
            style_options.extend(["lunar-flow", "stellar-drift", "cosmic-patience"])
        elif shot_character == "powerful":
            style_options.extend(["stellar-force", "cosmic-power", "nebula-strength"])
        elif shot_character == "gentle":
            style_options.extend(["lunar-grace", "stellar-soft", "cosmic-tender"])
        else:
            style_options.extend(["cosmic-rhythm", "stellar-harmony", "nebula-balance"])
    else:
        style_options.extend(["stellar-harmony", "lunar-peace", "nebula-flow", "cosmic-rhythm"])
    
    # Add time variation influences
    if time_variation:
        time_of_day = time_variation.get("time_of_day", "day")
        cosmic_phase = time_variation.get("cosmic_phase", "neutral")
        
        if time_of_day == "morning":
            style_options.extend(["dawn-pulse", "morning-rhythm", "rising-energy"])
        elif time_of_day == "evening":
            style_options.extend(["dusk-flow", "evening-harmony", "setting-grace"])
        elif time_of_day == "night":
            style_options.extend(["stellar-deep", "night-rhythm", "cosmic-dream"])
        
        if "early" in cosmic_phase:
            style_options.extend(["early-pulse", "dawn-rhythm"])
        elif "late" in cosmic_phase:
            style_options.extend(["late-flow", "dusk-harmony"])
    
    # Use hash to pick consistently based on all factors
    hash_input = str(coffee_profile) + str(daily_mood) + str(shot_variation) + str(time_variation)
    style_hash = hash(hash_input) % len(style_options)
    return style_options[style_hash]


def get_dynamic_style_bank(
    features: Dict[str, Any], 
    user_birth_mmdd: str,
    use_gptoss: bool = True
) -> str:
    """
    Get dynamic style bank combining coffee profile and daily mood.
    
    Args:
        features: Shot features
        user_birth_mmdd: User's birth date
        use_gptoss: Whether to use GPT-OSS for generation
        
    Returns:
        Dynamic style bank name
    """
    # Analyze coffee profile
    coffee_profile = analyze_coffee_profile(features)
    
    # Calculate daily mood
    daily_mood = calculate_daily_mood(user_birth_mmdd)
    
    # Add shot-specific variation
    shot_variation = analyze_shot_variation(features)
    
    # Add time-based variation
    time_variation = analyze_time_variation(features)
    
    # Generate style with all variations
    if use_gptoss:
        style = generate_dynamic_style_with_gptoss(
            coffee_profile, daily_mood, user_birth_mmdd, shot_variation, time_variation
        )
    else:
        style = generate_fallback_style(
            coffee_profile, daily_mood, shot_variation, time_variation
        )
    
    return style


def main():
    """Test the dynamic style system."""
    # Test data
    test_features = {
        "brew_ratio": 2.1,
        "shot_end_s": 28,
        "peak_pressure_bar": 9.2,
        "temp_avg_c": 91.5,
        "channeling_score_0_1": 0.05,
        "rule_hit": "sweet_spot"
    }
    
    test_birth_date = "1021"
    
    print("🧪 Testing Dynamic Style System")
    print("=" * 50)
    
    # Test coffee profile
    coffee_profile = analyze_coffee_profile(test_features)
    print(f"☕ Coffee Profile: {coffee_profile}")
    
    # Test daily mood
    daily_mood = calculate_daily_mood(test_birth_date)
    print(f"🌙 Daily Mood: {daily_mood}")
    
    # Test dynamic style
    style = get_dynamic_style_bank(test_features, test_birth_date, use_gptoss=False)
    print(f"✨ Dynamic Style: {style}")
    
    # Test with GPT-OSS
    print("\n🤖 Testing with GPT-OSS...")
    style_gptoss = get_dynamic_style_bank(test_features, test_birth_date, use_gptoss=True)
    print(f"✨ GPT-OSS Style: {style_gptoss}")


if __name__ == "__main__":
    main()
