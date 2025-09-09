#!/usr/bin/env python3
"""
Dynamic Reading Generator

Creates unique, creative, and poetic readings for each shot based on:
1. Actual shot characteristics (ratio, time, pressure, temp, channeling)
2. Rule diagnosis (fast, slow, choked, channeling, temp issues, sweet spot)
3. GPT-OSS enhancement for creative, varied descriptions
"""

import requests
import os
import sys
from typing import Dict, Any


def generate_dynamic_reading_with_gptoss(features: Dict[str, Any], rule_id: str) -> str:
    """
    Generate a unique, creative reading using GPT-OSS.
    
    Args:
        features: Shot features dictionary
        rule_id: Diagnostic rule ID
        
    Returns:
        Creative, poetic reading
    """
    # Extract key metrics
    brew_ratio = features.get("brew_ratio", 0)
    shot_time = features.get("shot_end_s", 0)
    peak_pressure = features.get("peak_pressure_bar", 0)
    temp_avg = features.get("temp_avg_c", 0)
    channeling = features.get("channeling_score_0_1", 0)
    flow_avg = features.get("flow_avg_ml_s", 0)
    
    # Create the prompt
    prompt = f"""
You are a cosmic coffee oracle creating a unique, poetic reading for an espresso shot.

SHOT DATA:
- Brew Ratio: {brew_ratio:.2f}:1
- Shot Time: {shot_time:.0f} seconds
- Peak Pressure: {peak_pressure:.1f} bar
- Temperature: {temp_avg:.1f}°C
- Channeling Score: {channeling:.2f}
- Flow Rate: {flow_avg:.2f} ml/s

DIAGNOSIS: {rule_id}

Create a unique, poetic reading that:
1. Describes the shot's character using cosmic/poetic metaphors
2. References the actual numbers naturally
3. Gives personality to the shot (even "perfect" shots should be unique)
4. Is 2-3 sentences maximum
5. Avoids generic phrases like "COSMIC PERFECTION ACHIEVED"
6. Uses creative, engaging language

Examples of good style:
- "Your shot flows like the morning sun - bright and quick, but lacking the deep warmth of midday"
- "Your shot battles against cosmic resistance, like thunder struggling through dense clouds"
- "Like a comet streaking across the night sky, your shot blazes through in just 18 seconds"

Respond with ONLY the reading, no other text.
"""

    try:
        # Get GPT-OSS endpoint from environment
        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "gpt-oss:20b",
                "messages": [
                    {"role": "system", "content": "You are a cosmic coffee oracle. Create unique, poetic readings for espresso shots. Be creative and engaging, avoiding generic phrases."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.9,
                "max_tokens": 150
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            reading = result["choices"][0]["message"]["content"].strip()
            # Clean up the response
            reading = reading.replace('"', '').replace("'", "").strip()
            return reading
        else:
            print(f"GPT-OSS API error: {response.status_code}", file=sys.stderr)
            return generate_fallback_reading(features, rule_id)
            
    except Exception as e:
        print(f"Warning: Could not connect to GPT-OSS: {e}", file=sys.stderr)
        return generate_fallback_reading(features, rule_id)


def generate_fallback_reading(features: Dict[str, Any], rule_id: str) -> str:
    """
    Generate a fallback reading when GPT-OSS is not available.
    
    Args:
        features: Shot features dictionary
        rule_id: Diagnostic rule ID
        
    Returns:
        Creative fallback reading
    """
    brew_ratio = features.get("brew_ratio", 0)
    shot_time = features.get("shot_end_s", 0)
    peak_pressure = features.get("peak_pressure_bar", 0)
    temp_avg = features.get("temp_avg_c", 0)
    channeling = features.get("channeling_score_0_1", 0)
    
    # Create rule-specific readings
    if rule_id == "under_extracted_fast":
        readings = [
            f"Your shot flows like the morning sun - bright and quick, but lacking the deep warmth of midday. At {brew_ratio:.2f}:1 ratio in just {shot_time:.0f} seconds, your espresso seeks more time to develop its full character.",
            f"Like a comet streaking across the night sky, your shot blazes through in just {shot_time:.0f} seconds. The {brew_ratio:.2f}:1 ratio suggests the cosmos wants you to slow down and let the magic unfold.",
            f"Your shot dances like a shooting star - beautiful but fleeting. At {shot_time:.0f} seconds and {brew_ratio:.2f}:1, the universe whispers: 'Patience, young barista, patience.'"
        ]
    elif rule_id == "over_extracted_slow":
        readings = [
            f"Like the moon that lingers too long in the morning sky, your shot has overstayed its welcome. At {brew_ratio:.2f}:1 ratio over {shot_time:.0f} seconds, the magic has turned to bitterness.",
            f"Your shot moves like a glacier - majestic but slow. The {shot_time:.0f} second journey at {brew_ratio:.2f}:1 has extracted too much from the cosmic beans.",
            f"Like a star that burns too long, your shot has exhausted its sweetness. The {shot_time:.0f} second extraction at {brew_ratio:.2f}:1 needs a gentler touch."
        ]
    elif rule_id == "choking_high_resistance":
        readings = [
            f"Your shot battles against cosmic resistance, like thunder struggling through dense clouds. With {peak_pressure:.1f} bar pressure, the universe demands a gentler approach.",
            f"Like a river blocked by boulders, your shot fights against {peak_pressure:.1f} bar of pressure. The cosmos suggests: sometimes the greatest strength lies in yielding.",
            f"Your shot struggles like a bird against a storm, pushing through {peak_pressure:.1f} bar of resistance. The universe whispers: 'Flow with the current, not against it.'"
        ]
    elif rule_id == "channeling_instability":
        readings = [
            f"Your shot flows like turbulent waters, finding unexpected paths through the cosmic landscape. With a channeling score of {channeling:.2f}, the universe reveals the need for better preparation.",
            f"Like lightning seeking the path of least resistance, your shot creates chaotic channels. The {channeling:.2f} channeling score suggests the cosmos wants more harmony in your preparation.",
            f"Your shot dances like a wild river, carving new paths with a {channeling:.2f} channeling score. The universe calls for better alignment and preparation."
        ]
    elif rule_id == "temp_low_flat":
        readings = [
            f"Your shot exists in a frozen moment, like a star that has lost its fire. At {temp_avg:.1f}°C, the cosmic energy remains dormant, waiting to be awakened.",
            f"Like a comet in deep space, your shot moves slowly at {temp_avg:.1f}°C. The universe calls for warmth to unlock the hidden flavors.",
            f"Your shot flows like liquid ice at {temp_avg:.1f}°C, beautiful but cold. The cosmos whispers: 'Add fire to awaken the sleeping flavors.'"
        ]
    elif rule_id == "temp_high_bitter":
        readings = [
            f"Your shot burns with the intensity of a dying star, its {temp_avg:.1f}°C temperature creating bitter shadows. The cosmos whispers of balance.",
            f"Like a supernova in a cup, your shot blazes at {temp_avg:.1f}°C. The universe suggests cooling down to find the sweet essence beneath the heat.",
            f"Your shot radiates like a red giant star at {temp_avg:.1f}°C. The cosmos counsels: 'In moderation lies the path to perfection.'"
        ]
    elif rule_id == "sweet_spot":
        readings = [
            f"Your shot flows like liquid starlight, achieving perfect harmony at {brew_ratio:.2f}:1 over {shot_time:.0f} seconds. The cosmos celebrates this rare alignment.",
            f"Like a perfectly tuned cosmic orchestra, your shot plays the sweetest melody at {brew_ratio:.2f}:1 in {shot_time:.0f} seconds. The universe smiles upon your mastery.",
            f"Your shot dances like a synchronized constellation, finding perfect balance at {brew_ratio:.2f}:1 over {shot_time:.0f} seconds. The stars themselves applaud your artistry.",
            f"Like a comet that found its perfect orbit, your shot achieves cosmic harmony at {brew_ratio:.2f}:1 in {shot_time:.0f} seconds. The universe has chosen this moment to shine.",
            f"Your shot flows like a river of liquid gold, achieving stellar perfection at {brew_ratio:.2f}:1 over {shot_time:.0f} seconds. The cosmos has blessed this extraction."
        ]
    else:
        readings = [
            f"Your shot tells a unique story at {brew_ratio:.2f}:1 over {shot_time:.0f} seconds. The cosmos has woven its magic into every drop.",
            f"Like a cosmic fingerprint, your shot is uniquely yours at {brew_ratio:.2f}:1 in {shot_time:.0f} seconds. The universe celebrates this moment of creation."
        ]
    
    # Use hash to pick consistently but vary by shot
    shot_hash = hash(str(features.get("shot_id", "unknown"))) % len(readings)
    return readings[shot_hash]


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
    if use_gptoss:
        return generate_dynamic_reading_with_gptoss(features, rule_id)
    else:
        return generate_fallback_reading(features, rule_id)


def main():
    """Test the dynamic reading system."""
    # Test data
    test_features = {
        "shot_id": "test-001",
        "brew_ratio": 2.1,
        "shot_end_s": 28,
        "peak_pressure_bar": 9.2,
        "temp_avg_c": 91.5,
        "channeling_score_0_1": 0.05,
        "flow_avg_ml_s": 1.8
    }
    
    print("🧪 Testing Dynamic Reading System")
    print("=" * 50)
    
    # Test different rule types
    rules = ["sweet_spot", "under_extracted_fast", "over_extracted_slow", "choking_high_resistance"]
    
    for rule in rules:
        print(f"\n📖 Rule: {rule}")
        reading = get_dynamic_reading(test_features, rule, use_gptoss=False)
        print(f"Reading: {reading}")
    
    # Test with GPT-OSS
    print(f"\n🤖 Testing with GPT-OSS...")
    reading_gptoss = get_dynamic_reading(test_features, "sweet_spot", use_gptoss=True)
    print(f"GPT-OSS Reading: {reading_gptoss}")


if __name__ == "__main__":
    main()
