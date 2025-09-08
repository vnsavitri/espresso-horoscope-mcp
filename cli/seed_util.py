#!/usr/bin/env python3
"""
Deterministic seeding system for espresso horoscope generation.
Ensures consistent yet varied readings based on shot data, user context, and temporal factors.
"""

import datetime
import hashlib
import random
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def get_local_date() -> str:
    """Get current local date in YYYYMMDD format."""
    return datetime.datetime.now().strftime("%Y%m%d")


def get_season() -> str:
    """Get current season for flavor variation."""
    month = datetime.datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"


def get_time_of_day() -> str:
    """Get time of day for mood variation."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def generate_seed(shot_id: str, user_birth_mmdd: str, style_bank: str) -> str:
    """
    Generate deterministic seed for consistent yet varied readings.
    
    Args:
        shot_id: Unique identifier for the shot
        user_birth_mmdd: User's birth month and day (MMDD format)
        style_bank: User's style preference (chill, punchy, nerdy, etc.)
    
    Returns:
        Deterministic seed string
    """
    local_date = get_local_date()
    season = get_season()
    time_of_day = get_time_of_day()
    
    # Create seed string with all variation factors
    seed_string = f"{shot_id}_{local_date}_{user_birth_mmdd}_{style_bank}_{season}_{time_of_day}"
    
    # Generate hash for consistent seed
    seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
    return seed_hash


class SeededRandom:
    """Deterministic random number generator using seed."""
    
    def __init__(self, seed: str):
        self.seed = seed
        self.rng = random.Random(seed)
    
    def choice(self, items: List[Any]) -> Any:
        """Choose random item from list deterministically."""
        return self.rng.choice(items)
    
    def choices(self, items: List[Any], k: int = 1) -> List[Any]:
        """Choose k random items from list deterministically."""
        return self.rng.choices(items, k=k)
    
    def random(self) -> float:
        """Generate random float between 0 and 1 deterministically."""
        return self.rng.random()
    
    def randint(self, a: int, b: int) -> int:
        """Generate random integer between a and b deterministically."""
        return self.rng.randint(a, b)


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    config_dir = Path.home() / ".espresso_horoscope"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def load_user_config() -> Dict[str, Any]:
    """Load user configuration from ~/.espresso_horoscope/config.yaml."""
    config_file = get_config_dir() / "config.yaml"
    
    if not config_file.exists():
        return {
            "birth_mmdd": None,
            "style_bank": "chill",
            "first_use": True
        }
    
    try:
        import yaml
        with open(config_file, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {
            "birth_mmdd": None,
            "style_bank": "chill",
            "first_use": True
        }


def save_user_config(config: Dict[str, Any]) -> None:
    """Save user configuration to ~/.espresso_horoscope/config.yaml."""
    config_file = get_config_dir() / "config.yaml"
    
    try:
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        print(f"Warning: Could not save config: {e}")


def load_reading_history(user_id: str = "default") -> List[Dict[str, Any]]:
    """Load reading history for a user."""
    history_file = get_config_dir() / f"history_{user_id}.json"
    
    if not history_file.exists():
        return []
    
    try:
        with open(history_file, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def save_reading_history(user_id: str, history: List[Dict[str, Any]]) -> None:
    """Save reading history for a user."""
    history_file = get_config_dir() / f"history_{user_id}.json"
    
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save history: {e}")


def add_reading_to_history(
    user_id: str,
    shot_id: str,
    seed: str,
    style_bank: str,
    rule_hit: str,
    title: str,
    emoji: str
) -> None:
    """Add a new reading to the user's history."""
    history = load_reading_history(user_id)
    
    new_reading = {
        "date": get_local_date(),
        "shot_id": shot_id,
        "seed": seed,
        "style_bank": style_bank,
        "rule_hit": rule_hit,
        "title": title,
        "emoji": emoji,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    history.append(new_reading)
    
    # Keep only last 100 readings to prevent file from growing too large
    if len(history) > 100:
        history = history[-100:]
    
    save_reading_history(user_id, history)


def analyze_reading_trends(user_id: str = "default") -> Dict[str, Any]:
    """Analyze comprehensive reading trends for a user."""
    history = load_reading_history(user_id)
    
    if not history:
        return {
            "rule_patterns": {},
            "style_evolution": [],
            "seasonal_patterns": {},
            "time_patterns": {},
            "total_readings": 0,
            "insights": [],
            "improvement_trends": {},
            "consistency_score": 0.0
        }
    
    # Count rule patterns with percentages
    rule_counts = {}
    for reading in history:
        rule = reading.get("rule_hit", "unknown")
        rule_counts[rule] = rule_counts.get(rule, 0) + 1
    
    total_readings = len(history)
    rule_percentages = {rule: (count / total_readings) * 100 for rule, count in rule_counts.items()}
    
    # Track style evolution with timestamps
    style_evolution = []
    for reading in history:
        style_evolution.append({
            "style": reading.get("style_bank", "unknown"),
            "date": reading.get("date", ""),
            "timestamp": reading.get("timestamp", "")
        })
    
    # Enhanced seasonal patterns
    seasonal_patterns = {}
    seasonal_rule_patterns = {}
    for reading in history:
        date_str = reading.get("date", "")
        if len(date_str) >= 8:
            month = int(date_str[4:6])
            if month in [12, 1, 2]:
                season = "winter"
            elif month in [3, 4, 5]:
                season = "spring"
            elif month in [6, 7, 8]:
                season = "summer"
            else:
                season = "autumn"
            
            seasonal_patterns[season] = seasonal_patterns.get(season, 0) + 1
            
            # Track rule patterns by season
            if season not in seasonal_rule_patterns:
                seasonal_rule_patterns[season] = {}
            rule = reading.get("rule_hit", "unknown")
            seasonal_rule_patterns[season][rule] = seasonal_rule_patterns[season].get(rule, 0) + 1
    
    # Time patterns (extract hour from timestamp)
    time_patterns = {}
    for reading in history:
        timestamp = reading.get("timestamp", "")
        if timestamp:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                hour = dt.hour
                time_of_day = get_time_of_day_from_hour(hour)
                time_patterns[time_of_day] = time_patterns.get(time_of_day, 0) + 1
            except:
                pass
    
    # Calculate consistency score (how often user hits sweet_spot)
    sweet_spot_count = rule_counts.get("sweet_spot", 0)
    consistency_score = (sweet_spot_count / total_readings) * 100 if total_readings > 0 else 0
    
    # Generate insights
    insights = generate_insights(rule_counts, rule_percentages, style_evolution, seasonal_patterns, consistency_score)
    
    # Improvement trends (compare recent vs older readings)
    improvement_trends = analyze_improvement_trends(history)
    
    return {
        "rule_patterns": rule_counts,
        "rule_percentages": rule_percentages,
        "style_evolution": style_evolution,
        "seasonal_patterns": seasonal_patterns,
        "seasonal_rule_patterns": seasonal_rule_patterns,
        "time_patterns": time_patterns,
        "total_readings": total_readings,
        "insights": insights,
        "improvement_trends": improvement_trends,
        "consistency_score": consistency_score
    }


def get_time_of_day_from_hour(hour: int) -> str:
    """Get time of day category from hour."""
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def generate_insights(
    rule_counts: Dict[str, int], 
    rule_percentages: Dict[str, float], 
    style_evolution: List[Dict], 
    seasonal_patterns: Dict[str, int],
    consistency_score: float
) -> List[str]:
    """Generate personalized insights from reading trends."""
    insights = []
    
    # Consistency insights
    if consistency_score >= 80:
        insights.append("🌟 You're a coffee master! Your consistency score is {:.1f}% - you've achieved the sweet spot most of the time.".format(consistency_score))
    elif consistency_score >= 60:
        insights.append("☕ Great progress! Your consistency score is {:.1f}% - you're well on your way to coffee mastery.".format(consistency_score))
    elif consistency_score >= 40:
        insights.append("🌱 Room for improvement! Your consistency score is {:.1f}% - focus on grind consistency and puck preparation.".format(consistency_score))
    else:
        insights.append("🔧 Time to refine your technique! Your consistency score is {:.1f}% - consider adjusting your grind and extraction parameters.".format(consistency_score))
    
    # Rule pattern insights
    if rule_counts:
        most_common_rule = max(rule_counts.items(), key=lambda x: x[1])
        if most_common_rule[0] == "sweet_spot":
            insights.append("✨ You've mastered the art of balanced extraction - keep up the excellent work!")
        elif most_common_rule[0] == "under_extracted_fast":
            insights.append("⚡ You tend to under-extract - try grinding finer and extending your shot time.")
        elif most_common_rule[0] == "over_extracted_slow":
            insights.append("🐌 You often over-extract - consider coarsening your grind or reducing dose.")
        elif most_common_rule[0] == "choking_high_resistance":
            insights.append("🚫 You frequently encounter choking - try reducing dose or coarsening grind.")
        elif most_common_rule[0] == "channeling_instability":
            insights.append("🌊 Channeling is your main challenge - focus on WDT and even tamping.")
    
    # Style evolution insights
    if len(style_evolution) > 1:
        first_style = style_evolution[0]["style"]
        recent_style = style_evolution[-1]["style"]
        if first_style != recent_style:
            insights.append("🎭 Your style has evolved from '{}' to '{}' - your coffee journey is growing!".format(first_style, recent_style))
    
    # Seasonal insights
    if seasonal_patterns:
        most_active_season = max(seasonal_patterns.items(), key=lambda x: x[1])
        insights.append("📅 You're most active during {} with {} readings - seasonal coffee vibes!".format(most_active_season[0], most_active_season[1]))
    
    return insights


def analyze_improvement_trends(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze improvement trends over time."""
    if len(history) < 4:
        return {"trend": "insufficient_data", "message": "Need at least 4 readings to analyze trends"}
    
    # Split into early and recent readings
    mid_point = len(history) // 2
    early_readings = history[:mid_point]
    recent_readings = history[mid_point:]
    
    # Count sweet_spot hits in each period
    early_sweet_spots = sum(1 for r in early_readings if r.get("rule_hit") == "sweet_spot")
    recent_sweet_spots = sum(1 for r in recent_readings if r.get("rule_hit") == "sweet_spot")
    
    early_percentage = (early_sweet_spots / len(early_readings)) * 100
    recent_percentage = (recent_sweet_spots / len(recent_readings)) * 100
    
    improvement = recent_percentage - early_percentage
    
    if improvement > 10:
        trend = "improving"
        message = "📈 You're improving! Sweet spot rate increased from {:.1f}% to {:.1f}%".format(early_percentage, recent_percentage)
    elif improvement < -10:
        trend = "declining"
        message = "📉 Your consistency has declined from {:.1f}% to {:.1f}% - time to refocus!".format(early_percentage, recent_percentage)
    else:
        trend = "stable"
        message = "📊 Your performance is stable around {:.1f}% sweet spot rate".format(recent_percentage)
    
    return {
        "trend": trend,
        "message": message,
        "early_percentage": early_percentage,
        "recent_percentage": recent_percentage,
        "improvement": improvement
    }


if __name__ == "__main__":
    # Test the seeding system
    print("🧪 Testing Seeded Random System")
    print("=" * 40)
    
    # Test seed generation
    test_shot_id = "20241201_143022"
    test_birth = "0615"  # June 15th
    test_style = "chill"
    
    seed = generate_seed(test_shot_id, test_birth, test_style)
    print(f"Generated seed: {seed}")
    print(f"Local date: {get_local_date()}")
    print(f"Season: {get_season()}")
    print(f"Time of day: {get_time_of_day()}")
    
    # Test seeded random
    sr = SeededRandom(seed)
    test_items = ["option1", "option2", "option3", "option4"]
    
    print(f"\nSeeded choices from {test_items}:")
    for i in range(5):
        choice = sr.choice(test_items)
        print(f"  Choice {i+1}: {choice}")
    
    # Test config system
    print(f"\nConfig directory: {get_config_dir()}")
    config = load_user_config()
    print(f"Current config: {config}")
    
    # Test history system
    history = load_reading_history("test_user")
    print(f"Current history length: {len(history)}")
    
    print("\n✅ Seeding system test complete!")
