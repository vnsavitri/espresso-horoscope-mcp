#!/usr/bin/env python3
"""
Espresso Horoscope History Viewer

CLI tool for viewing reading history, trends, and insights.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Import the seeding system
from seed_util import (
    load_reading_history, analyze_reading_trends, 
    load_user_config, get_config_dir
)


def format_date(date_str: str) -> str:
    """Format YYYYMMDD date string to readable format."""
    if len(date_str) >= 8:
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    return date_str


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable format."""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return timestamp


def print_reading_timeline(history: List[Dict[str, Any]], limit: int = None) -> None:
    """Print a timeline of readings."""
    if not history:
        print("📅 No reading history found.")
        return
    
    if limit:
        history = history[-limit:]
    
    print(f"📅 Reading Timeline ({len(history)} readings)")
    print("=" * 50)
    
    for i, reading in enumerate(history, 1):
        date = format_date(reading.get("date", "unknown"))
        timestamp = format_timestamp(reading.get("timestamp", ""))
        emoji = reading.get("emoji", "☕")
        title = reading.get("title", "Unknown")
        rule_hit = reading.get("rule_hit", "unknown")
        style = reading.get("style_bank", "unknown")
        
        print(f"{i:2d}. {emoji} {title}")
        print(f"    📅 {date} at {timestamp}")
        print(f"    🎯 Rule: {rule_hit} | 🎭 Style: {style}")
        print()


def print_trend_analysis(trends: Dict[str, Any]) -> None:
    """Print detailed trend analysis."""
    print("📊 Trend Analysis")
    print("=" * 50)
    
    # Basic stats
    total_readings = trends.get("total_readings", 0)
    consistency_score = trends.get("consistency_score", 0)
    
    print(f"📈 Total Readings: {total_readings}")
    print(f"🎯 Consistency Score: {consistency_score:.1f}%")
    print()
    
    # Rule patterns
    rule_patterns = trends.get("rule_patterns", {})
    rule_percentages = trends.get("rule_percentages", {})
    
    if rule_patterns:
        print("🎲 Rule Patterns:")
        for rule, count in sorted(rule_patterns.items(), key=lambda x: x[1], reverse=True):
            percentage = rule_percentages.get(rule, 0)
            print(f"   {rule}: {count} times ({percentage:.1f}%)")
        print()
    
    # Style evolution
    style_evolution = trends.get("style_evolution", [])
    if style_evolution:
        print("🎭 Style Evolution:")
        for entry in style_evolution:
            date = format_date(entry.get("date", ""))
            style = entry.get("style", "unknown")
            print(f"   {date}: {style}")
        print()
    
    # Seasonal patterns
    seasonal_patterns = trends.get("seasonal_patterns", {})
    if seasonal_patterns:
        print("📅 Seasonal Patterns:")
        for season, count in sorted(seasonal_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"   {season.title()}: {count} readings")
        print()
    
    # Time patterns
    time_patterns = trends.get("time_patterns", {})
    if time_patterns:
        print("🕐 Time Patterns:")
        for time_of_day, count in sorted(time_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"   {time_of_day.title()}: {count} readings")
        print()
    
    # Improvement trends
    improvement_trends = trends.get("improvement_trends", {})
    if improvement_trends and improvement_trends.get("trend") != "insufficient_data":
        print("📈 Improvement Trends:")
        print(f"   {improvement_trends.get('message', 'No trend data')}")
        print()


def print_insights(insights: List[str]) -> None:
    """Print personalized insights."""
    if not insights:
        print("💡 No insights available yet.")
        return
    
    print("💡 Personalized Insights")
    print("=" * 50)
    
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    print()


def print_style_suggestions(trends: Dict[str, Any]) -> None:
    """Print style evolution suggestions."""
    style_evolution = trends.get("style_evolution", [])
    if len(style_evolution) < 2:
        print("🎭 Style Evolution: Not enough data for suggestions yet.")
        return
    
    print("🎭 Style Evolution Suggestions")
    print("=" * 50)
    
    current_style = style_evolution[-1]["style"]
    first_style = style_evolution[0]["style"]
    
    print(f"Current style: {current_style}")
    print(f"Started with: {first_style}")
    
    # Style suggestions based on current style
    suggestions = {
        "chill": "Try 'punchy' for more dynamic readings, or 'nerdy' for technical insights",
        "punchy": "Try 'mystical' for cosmic depth, or 'chill' for relaxed vibes",
        "nerdy": "Try 'mystical' for creative flair, or 'punchy' for energetic readings",
        "mystical": "Try 'nerdy' for analytical insights, or 'chill' for peaceful readings"
    }
    
    if current_style in suggestions:
        print(f"💡 Suggestion: {suggestions[current_style]}")
    
    print()


def export_history_json(history: List[Dict[str, Any]], output_file: str) -> None:
    """Export reading history to JSON file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump({
            "metadata": {
                "exported_at": "2025-09-08T15:00:00Z",
                "total_readings": len(history)
            },
            "readings": history
        }, f, indent=2)
    
    print(f"📁 History exported to {output_file}")


def main():
    """CLI interface for history viewing."""
    parser = argparse.ArgumentParser(
        description="View espresso horoscope reading history and trends",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/history.py --timeline                    # Show reading timeline
  python cli/history.py --trends                      # Show trend analysis
  python cli/history.py --insights                    # Show personalized insights
  python cli/history.py --all                         # Show everything
  python cli/history.py --export history.json         # Export to JSON
        """
    )
    
    parser.add_argument(
        '--timeline',
        action='store_true',
        help='Show reading timeline'
    )
    
    parser.add_argument(
        '--trends',
        action='store_true',
        help='Show trend analysis'
    )
    
    parser.add_argument(
        '--insights',
        action='store_true',
        help='Show personalized insights'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Show all information'
    )
    
    parser.add_argument(
        '--export',
        metavar='FILE',
        help='Export history to JSON file'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of readings shown (for timeline)'
    )
    
    parser.add_argument(
        '--user-id',
        default='default',
        help='User ID to analyze (default: default)'
    )
    
    args = parser.parse_args()
    
    # If no specific action requested, show timeline by default
    if not any([args.timeline, args.trends, args.insights, args.all, args.export]):
        args.timeline = True
    
    try:
        # Load data
        history = load_reading_history(args.user_id)
        trends = analyze_reading_trends(args.user_id)
        
        # Show user config
        config = load_user_config()
        print(f"👤 User: {args.user_id}")
        if config.get("birth_mmdd"):
            print(f"🎂 Birth Date: {config['birth_mmdd']}")
        print(f"🎭 Style: {config.get('style_bank', 'chill')}")
        print()
        
        # Export if requested
        if args.export:
            export_history_json(history, args.export)
            return
        
        # Show requested information
        if args.all or args.timeline:
            print_reading_timeline(history, args.limit)
        
        if args.all or args.trends:
            print_trend_analysis(trends)
        
        if args.all or args.insights:
            print_insights(trends.get("insights", []))
            print_style_suggestions(trends)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
