#!/usr/bin/env python3
"""
Advanced Style Evolution System

Tracks user style preferences over time and provides intelligent recommendations
based on seasonal patterns, usage history, and personal growth.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from seed_util import load_reading_history, load_user_config, save_user_config


@dataclass
class StyleRecommendation:
    """A style recommendation with reasoning."""
    style: str
    confidence: float  # 0.0 to 1.0
    reason: str
    seasonal_factor: bool
    growth_factor: bool
    usage_factor: bool


class StyleEvolutionTracker:
    """Tracks and analyzes style evolution patterns."""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.config_dir = Path.home() / ".espresso_horoscope"
        self.style_history_file = self.config_dir / f"style_evolution_{user_id}.json"
        
    def load_style_history(self) -> List[Dict[str, Any]]:
        """Load style evolution history."""
        if not self.style_history_file.exists():
            return []
        
        try:
            with open(self.style_history_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def save_style_history(self, history: List[Dict[str, Any]]) -> None:
        """Save style evolution history."""
        self.config_dir.mkdir(exist_ok=True)
        
        try:
            with open(self.style_history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save style history: {e}")
    
    def track_style_usage(self, style: str, context: Dict[str, Any] = None) -> None:
        """Track a style usage event."""
        history = self.load_style_history()
        
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "style": style,
            "context": context or {},
            "season": self.get_current_season(),
            "time_of_day": self.get_time_of_day(),
            "user_mood": self.infer_user_mood(style, context)
        }
        
        history.append(event)
        
        # Keep only last 100 events to prevent file from growing too large
        if len(history) > 100:
            history = history[-100:]
        
        self.save_style_history(history)
    
    def get_current_season(self) -> str:
        """Get current season."""
        month = datetime.datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
    
    def get_time_of_day(self) -> str:
        """Get current time of day."""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def infer_user_mood(self, style: str, context: Dict[str, Any]) -> str:
        """Infer user mood from style choice and context."""
        mood_mapping = {
            "chill": "relaxed",
            "punchy": "energetic", 
            "nerdy": "focused",
            "mystical": "contemplative"
        }
        
        # Check if there are any contextual clues
        if context:
            rule_hit = context.get("rule_hit", "")
            if rule_hit == "sweet_spot":
                return "satisfied"
            elif rule_hit in ["under_extracted_fast", "over_extracted_slow"]:
                return "frustrated"
            elif rule_hit == "choking_high_resistance":
                return "determined"
        
        return mood_mapping.get(style, "neutral")
    
    def analyze_style_patterns(self) -> Dict[str, Any]:
        """Analyze style usage patterns."""
        history = self.load_style_history()
        
        if not history:
            return {
                "total_events": 0,
                "style_frequency": {},
                "seasonal_patterns": {},
                "time_patterns": {},
                "mood_patterns": {},
                "evolution_trend": "insufficient_data"
            }
        
        # Count style frequency
        style_counts = {}
        for event in history:
            style = event.get("style", "unknown")
            style_counts[style] = style_counts.get(style, 0) + 1
        
        # Seasonal patterns
        seasonal_patterns = {}
        for event in history:
            season = event.get("season", "unknown")
            style = event.get("style", "unknown")
            if season not in seasonal_patterns:
                seasonal_patterns[season] = {}
            seasonal_patterns[season][style] = seasonal_patterns[season].get(style, 0) + 1
        
        # Time patterns
        time_patterns = {}
        for event in history:
            time_of_day = event.get("time_of_day", "unknown")
            style = event.get("style", "unknown")
            if time_of_day not in time_patterns:
                time_patterns[time_of_day] = {}
            time_patterns[time_of_day][style] = time_patterns[time_of_day].get(style, 0) + 1
        
        # Mood patterns
        mood_patterns = {}
        for event in history:
            mood = event.get("user_mood", "unknown")
            style = event.get("style", "unknown")
            if mood not in mood_patterns:
                mood_patterns[mood] = {}
            mood_patterns[mood][style] = mood_patterns[mood].get(style, 0) + 1
        
        # Evolution trend
        evolution_trend = self.analyze_evolution_trend(history)
        
        return {
            "total_events": len(history),
            "style_frequency": style_counts,
            "seasonal_patterns": seasonal_patterns,
            "time_patterns": time_patterns,
            "mood_patterns": mood_patterns,
            "evolution_trend": evolution_trend
        }
    
    def analyze_evolution_trend(self, history: List[Dict[str, Any]]) -> str:
        """Analyze how user's style preferences have evolved."""
        if len(history) < 4:
            return "insufficient_data"
        
        # Split into early and recent periods
        mid_point = len(history) // 2
        early_styles = [event.get("style") for event in history[:mid_point]]
        recent_styles = [event.get("style") for event in history[mid_point:]]
        
        # Find most common style in each period
        early_most_common = max(set(early_styles), key=early_styles.count) if early_styles else "unknown"
        recent_most_common = max(set(recent_styles), key=recent_styles.count) if recent_styles else "unknown"
        
        # Analyze trend
        if early_most_common == recent_most_common:
            return "stable"
        else:
            # Check if it's a progression
            style_progression = ["chill", "punchy", "nerdy", "mystical"]
            try:
                early_index = style_progression.index(early_most_common)
                recent_index = style_progression.index(recent_most_common)
                if recent_index > early_index:
                    return "progressing"
                else:
                    return "regressing"
            except ValueError:
                return "changing"
    
    def generate_style_recommendations(self) -> List[StyleRecommendation]:
        """Generate intelligent style recommendations."""
        patterns = self.analyze_style_patterns()
        current_season = self.get_current_season()
        current_time = self.get_time_of_day()
        
        recommendations = []
        
        # Seasonal recommendations
        seasonal_recs = self.get_seasonal_recommendations(current_season, patterns)
        recommendations.extend(seasonal_recs)
        
        # Growth recommendations
        growth_recs = self.get_growth_recommendations(patterns)
        recommendations.extend(growth_recs)
        
        # Time-based recommendations
        time_recs = self.get_time_based_recommendations(current_time, patterns)
        recommendations.extend(time_recs)
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def get_seasonal_recommendations(self, season: str, patterns: Dict[str, Any]) -> List[StyleRecommendation]:
        """Get seasonal style recommendations."""
        seasonal_mapping = {
            "spring": {
                "chill": 0.7,
                "punchy": 0.8,
                "nerdy": 0.6,
                "mystical": 0.5
            },
            "summer": {
                "chill": 0.9,
                "punchy": 0.6,
                "nerdy": 0.4,
                "mystical": 0.7
            },
            "autumn": {
                "chill": 0.6,
                "punchy": 0.5,
                "nerdy": 0.8,
                "mystical": 0.9
            },
            "winter": {
                "chill": 0.8,
                "punchy": 0.4,
                "nerdy": 0.7,
                "mystical": 0.9
            }
        }
        
        recommendations = []
        seasonal_scores = seasonal_mapping.get(season, {})
        
        for style, score in seasonal_scores.items():
            if score > 0.6:  # Only recommend if score is above threshold
                reason = f"Perfect for {season} vibes - {self.get_seasonal_reason(season, style)}"
                recommendations.append(StyleRecommendation(
                    style=style,
                    confidence=score,
                    reason=reason,
                    seasonal_factor=True,
                    growth_factor=False,
                    usage_factor=False
                ))
        
        return recommendations
    
    def get_seasonal_reason(self, season: str, style: str) -> str:
        """Get seasonal reasoning for style recommendation."""
        reasons = {
            "spring": {
                "chill": "gentle awakening energy",
                "punchy": "renewed vitality and enthusiasm",
                "nerdy": "analytical spring planning",
                "mystical": "spiritual renewal and growth"
            },
            "summer": {
                "chill": "cool, relaxed summer vibes",
                "punchy": "high energy summer activities",
                "nerdy": "indoor study and analysis",
                "mystical": "long summer contemplations"
            },
            "autumn": {
                "chill": "cozy, reflective mood",
                "punchy": "harvest energy and productivity",
                "nerdy": "back-to-school analytical mindset",
                "mystical": "deep autumn introspection"
            },
            "winter": {
                "chill": "warm, cozy winter comfort",
                "punchy": "holiday energy and celebration",
                "nerdy": "indoor focus and planning",
                "mystical": "winter solstice contemplation"
            }
        }
        
        return reasons.get(season, {}).get(style, "seasonal harmony")
    
    def get_growth_recommendations(self, patterns: Dict[str, Any]) -> List[StyleRecommendation]:
        """Get growth-based style recommendations."""
        evolution_trend = patterns.get("evolution_trend", "insufficient_data")
        style_frequency = patterns.get("style_frequency", {})
        
        recommendations = []
        
        if evolution_trend == "stable":
            # User is stable, suggest next step in progression
            most_used = max(style_frequency.items(), key=lambda x: x[1])[0] if style_frequency else "chill"
            progression = ["chill", "punchy", "nerdy", "mystical"]
            
            try:
                current_index = progression.index(most_used)
                if current_index < len(progression) - 1:
                    next_style = progression[current_index + 1]
                    recommendations.append(StyleRecommendation(
                        style=next_style,
                        confidence=0.7,
                        reason=f"Ready to evolve from {most_used} to {next_style} - natural progression",
                        seasonal_factor=False,
                        growth_factor=True,
                        usage_factor=False
                    ))
            except ValueError:
                pass
        
        elif evolution_trend == "progressing":
            # User is progressing well, encourage continued growth
            most_used = max(style_frequency.items(), key=lambda x: x[1])[0] if style_frequency else "chill"
            recommendations.append(StyleRecommendation(
                style=most_used,
                confidence=0.8,
                reason=f"Great progress with {most_used}! Continue exploring this style",
                seasonal_factor=False,
                growth_factor=True,
                usage_factor=False
            ))
        
        return recommendations
    
    def get_time_based_recommendations(self, time_of_day: str, patterns: Dict[str, Any]) -> List[StyleRecommendation]:
        """Get time-based style recommendations."""
        time_mapping = {
            "morning": {
                "chill": 0.6,
                "punchy": 0.9,
                "nerdy": 0.7,
                "mystical": 0.4
            },
            "afternoon": {
                "chill": 0.7,
                "punchy": 0.8,
                "nerdy": 0.9,
                "mystical": 0.5
            },
            "evening": {
                "chill": 0.9,
                "punchy": 0.5,
                "nerdy": 0.6,
                "mystical": 0.8
            },
            "night": {
                "chill": 0.8,
                "punchy": 0.3,
                "nerdy": 0.4,
                "mystical": 0.9
            }
        }
        
        recommendations = []
        time_scores = time_mapping.get(time_of_day, {})
        
        for style, score in time_scores.items():
            if score > 0.7:  # Only recommend if score is above threshold
                reason = f"Ideal for {time_of_day} - {self.get_time_reason(time_of_day, style)}"
                recommendations.append(StyleRecommendation(
                    style=style,
                    confidence=score,
                    reason=reason,
                    seasonal_factor=False,
                    growth_factor=False,
                    usage_factor=True
                ))
        
        return recommendations
    
    def get_time_reason(self, time_of_day: str, style: str) -> str:
        """Get time-based reasoning for style recommendation."""
        reasons = {
            "morning": {
                "chill": "gentle start to the day",
                "punchy": "energetic morning boost",
                "nerdy": "analytical morning planning",
                "mystical": "spiritual morning reflection"
            },
            "afternoon": {
                "chill": "relaxed afternoon break",
                "punchy": "productive afternoon energy",
                "nerdy": "focused afternoon work",
                "mystical": "contemplative afternoon pause"
            },
            "evening": {
                "chill": "unwinding evening vibes",
                "punchy": "social evening energy",
                "nerdy": "evening study and reflection",
                "mystical": "deep evening contemplation"
            },
            "night": {
                "chill": "peaceful night comfort",
                "punchy": "late night energy",
                "nerdy": "night owl analysis",
                "mystical": "midnight spiritual journey"
            }
        }
        
        return reasons.get(time_of_day, {}).get(style, "perfect timing")


def main():
    """CLI interface for style evolution tracking."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Style Evolution Tracker")
    parser.add_argument("--user-id", default="default", help="User ID to analyze")
    parser.add_argument("--track", help="Track a style usage event")
    parser.add_argument("--analyze", action="store_true", help="Analyze style patterns")
    parser.add_argument("--recommend", action="store_true", help="Get style recommendations")
    parser.add_argument("--all", action="store_true", help="Show all information")
    
    args = parser.parse_args()
    
    tracker = StyleEvolutionTracker(args.user_id)
    
    if args.track:
        tracker.track_style_usage(args.track)
        print(f"✅ Tracked style usage: {args.track}")
    
    if args.analyze or args.all:
        patterns = tracker.analyze_style_patterns()
        print("📊 Style Evolution Analysis")
        print("=" * 40)
        print(f"Total Events: {patterns['total_events']}")
        print(f"Evolution Trend: {patterns['evolution_trend']}")
        
        if patterns['style_frequency']:
            print("\nStyle Frequency:")
            for style, count in sorted(patterns['style_frequency'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {style}: {count} times")
    
    if args.recommend or args.all:
        recommendations = tracker.generate_style_recommendations()
        print("\n💡 Style Recommendations")
        print("=" * 40)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec.style.title()} (confidence: {rec.confidence:.1f})")
            print(f"   {rec.reason}")
            factors = []
            if rec.seasonal_factor:
                factors.append("seasonal")
            if rec.growth_factor:
                factors.append("growth")
            if rec.usage_factor:
                factors.append("time-based")
            print(f"   Factors: {', '.join(factors)}")
            print()


if __name__ == "__main__":
    main()
