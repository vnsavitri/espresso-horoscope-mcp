#!/usr/bin/env python3
"""
Community Insights System

Analyzes reading patterns across multiple users to provide
community insights and comparative analytics.
"""

import json
import statistics
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

from seed_util import load_reading_history, get_config_dir


@dataclass
class CommunityInsight:
    """A community insight with statistical backing."""
    title: str
    description: str
    confidence: float  # 0.0 to 1.0
    data_points: int
    category: str  # "trend", "pattern", "comparison", "achievement"
    metadata: Dict[str, Any]


class CommunityAnalyzer:
    """Analyzes community reading patterns and generates insights."""
    
    def __init__(self):
        self.config_dir = get_config_dir()
        self.community_data_file = self.config_dir / "community_data.json"
    
    def load_community_data(self) -> Dict[str, Any]:
        """Load aggregated community data."""
        if not self.community_data_file.exists():
            return {
                "total_readings": 0,
                "users": {},
                "global_patterns": {},
                "last_updated": None
            }
        
        try:
            with open(self.community_data_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {
                "total_readings": 0,
                "users": {},
                "global_patterns": {},
                "last_updated": None
            }
    
    def save_community_data(self, data: Dict[str, Any]) -> None:
        """Save aggregated community data."""
        data["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.community_data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save community data: {e}")
    
    def aggregate_user_data(self, user_id: str) -> Dict[str, Any]:
        """Aggregate data for a specific user."""
        history = load_reading_history(user_id)
        
        if not history:
            return {}
        
        # Basic stats
        total_readings = len(history)
        rule_counts = {}
        style_counts = {}
        consistency_scores = []
        
        for reading in history:
            rule = reading.get("rule_hit", "unknown")
            style = reading.get("style_bank", "unknown")
            
            rule_counts[rule] = rule_counts.get(rule, 0) + 1
            style_counts[style] = style_counts.get(style, 0) + 1
        
        # Calculate consistency score
        sweet_spot_count = rule_counts.get("sweet_spot", 0)
        consistency_score = (sweet_spot_count / total_readings) * 100 if total_readings > 0 else 0
        
        # Extract shot metrics (if available in future versions)
        shot_metrics = self._extract_shot_metrics(history)
        
        return {
            "user_id": user_id,
            "total_readings": total_readings,
            "rule_counts": rule_counts,
            "style_counts": style_counts,
            "consistency_score": consistency_score,
            "shot_metrics": shot_metrics,
            "last_reading": history[-1] if history else None,
            "first_reading": history[0] if history else None
        }
    
    def _extract_shot_metrics(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract shot metrics from reading history."""
        # This would be enhanced when we have more detailed shot data
        return {
            "avg_brew_ratio": 2.0,  # Placeholder
            "avg_shot_time": 28.0,  # Placeholder
            "avg_pressure": 9.0,    # Placeholder
            "avg_temperature": 92.0 # Placeholder
        }
    
    def update_community_data(self, user_id: str) -> None:
        """Update community data with user's latest information."""
        community_data = self.load_community_data()
        user_data = self.aggregate_user_data(user_id)
        
        if user_data:
            community_data["users"][user_id] = user_data
            community_data["total_readings"] = sum(
                user["total_readings"] for user in community_data["users"].values()
            )
            
            # Update global patterns
            community_data["global_patterns"] = self._calculate_global_patterns(community_data["users"])
            
            self.save_community_data(community_data)
    
    def _calculate_global_patterns(self, users: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate global patterns from all users."""
        if not users:
            return {}
        
        # Aggregate rule patterns
        global_rule_counts = {}
        global_style_counts = {}
        consistency_scores = []
        
        for user_data in users.values():
            # Rule patterns
            for rule, count in user_data.get("rule_counts", {}).items():
                global_rule_counts[rule] = global_rule_counts.get(rule, 0) + count
            
            # Style patterns
            for style, count in user_data.get("style_counts", {}).items():
                global_style_counts[style] = global_style_counts.get(style, 0) + count
            
            # Consistency scores
            consistency_scores.append(user_data.get("consistency_score", 0))
        
        # Calculate statistics
        avg_consistency = statistics.mean(consistency_scores) if consistency_scores else 0
        median_consistency = statistics.median(consistency_scores) if consistency_scores else 0
        
        return {
            "rule_patterns": global_rule_counts,
            "style_patterns": global_style_counts,
            "avg_consistency_score": avg_consistency,
            "median_consistency_score": median_consistency,
            "total_users": len(users),
            "consistency_distribution": {
                "excellent": sum(1 for score in consistency_scores if score >= 80),
                "good": sum(1 for score in consistency_scores if 60 <= score < 80),
                "improving": sum(1 for score in consistency_scores if 40 <= score < 60),
                "beginner": sum(1 for score in consistency_scores if score < 40)
            }
        }
    
    def generate_community_insights(self) -> List[CommunityInsight]:
        """Generate insights from community data."""
        community_data = self.load_community_data()
        global_patterns = community_data.get("global_patterns", {})
        users = community_data.get("users", {})
        
        insights = []
        
        if not global_patterns:
            return [CommunityInsight(
                title="Community Growing",
                description="The espresso horoscope community is just getting started! Share your readings to help build community insights.",
                confidence=1.0,
                data_points=len(users),
                category="trend",
                metadata={"total_users": len(users)}
            )]
        
        # Consistency insights
        avg_consistency = global_patterns.get("avg_consistency_score", 0)
        if avg_consistency > 0:
            insights.append(CommunityInsight(
                title="Community Consistency",
                description=f"The community averages {avg_consistency:.1f}% consistency in hitting the sweet spot. {self._get_consistency_comment(avg_consistency)}",
                confidence=0.9,
                data_points=global_patterns.get("total_users", 0),
                category="achievement",
                metadata={"avg_consistency": avg_consistency}
            ))
        
        # Rule pattern insights
        rule_patterns = global_patterns.get("rule_patterns", {})
        if rule_patterns:
            most_common_rule = max(rule_patterns.items(), key=lambda x: x[1])
            total_rule_readings = sum(rule_patterns.values())
            percentage = (most_common_rule[1] / total_rule_readings) * 100
            
            insights.append(CommunityInsight(
                title="Most Common Reading",
                description=f"The most common reading across the community is '{most_common_rule[0].replace('_', ' ').title()}' at {percentage:.1f}% of all readings.",
                confidence=0.8,
                data_points=total_rule_readings,
                category="pattern",
                metadata={"most_common_rule": most_common_rule[0], "percentage": percentage}
            ))
        
        # Style pattern insights
        style_patterns = global_patterns.get("style_patterns", {})
        if style_patterns:
            most_popular_style = max(style_patterns.items(), key=lambda x: x[1])
            total_style_readings = sum(style_patterns.values())
            percentage = (most_popular_style[1] / total_style_readings) * 100
            
            insights.append(CommunityInsight(
                title="Popular Style",
                description=f"The '{most_popular_style[0]}' style is most popular in the community, used in {percentage:.1f}% of readings.",
                confidence=0.8,
                data_points=total_style_readings,
                category="pattern",
                metadata={"most_popular_style": most_popular_style[0], "percentage": percentage}
            ))
        
        # Consistency distribution insights
        consistency_dist = global_patterns.get("consistency_distribution", {})
        if consistency_dist:
            excellent_count = consistency_dist.get("excellent", 0)
            total_users = global_patterns.get("total_users", 0)
            
            if excellent_count > 0:
                percentage = (excellent_count / total_users) * 100
                insights.append(CommunityInsight(
                    title="Coffee Masters",
                    description=f"{excellent_count} community members ({percentage:.1f}%) have achieved 'Coffee Master' status with 80%+ consistency!",
                    confidence=0.9,
                    data_points=total_users,
                    category="achievement",
                    metadata={"excellent_users": excellent_count, "percentage": percentage}
                ))
        
        # Growth insights
        if len(users) > 1:
            insights.append(CommunityInsight(
                title="Community Growth",
                description=f"The espresso horoscope community has {len(users)} active members sharing their coffee journey!",
                confidence=1.0,
                data_points=len(users),
                category="trend",
                metadata={"total_users": len(users)}
            ))
        
        return insights
    
    def _get_consistency_comment(self, score: float) -> str:
        """Get a comment about consistency score."""
        if score >= 80:
            return "That's excellent! The community has mastered the art of consistent extraction."
        elif score >= 60:
            return "Great progress! The community is well on their way to coffee mastery."
        elif score >= 40:
            return "Room for improvement! The community is learning and growing together."
        else:
            return "The community is just starting their coffee journey - every shot is a learning opportunity!"
    
    def compare_user_to_community(self, user_id: str) -> Dict[str, Any]:
        """Compare a user's performance to the community."""
        community_data = self.load_community_data()
        user_data = self.aggregate_user_data(user_id)
        global_patterns = community_data.get("global_patterns", {})
        
        if not user_data or not global_patterns:
            return {"error": "Insufficient data for comparison"}
        
        user_consistency = user_data.get("consistency_score", 0)
        community_avg = global_patterns.get("avg_consistency_score", 0)
        
        # Calculate percentile
        all_users = list(community_data.get("users", {}).values())
        all_consistency_scores = [user.get("consistency_score", 0) for user in all_users]
        all_consistency_scores.append(user_consistency)  # Include current user
        all_consistency_scores.sort()
        
        user_rank = all_consistency_scores.index(user_consistency)
        percentile = (user_rank / len(all_consistency_scores)) * 100
        
        # Style comparison
        user_style_counts = user_data.get("style_counts", {})
        community_style_counts = global_patterns.get("style_patterns", {})
        
        style_comparison = {}
        for style in ["chill", "punchy", "nerdy", "mystical"]:
            user_count = user_style_counts.get(style, 0)
            community_count = community_style_counts.get(style, 0)
            user_total = sum(user_style_counts.values())
            community_total = sum(community_style_counts.values())
            
            if user_total > 0 and community_total > 0:
                user_percentage = (user_count / user_total) * 100
                community_percentage = (community_count / community_total) * 100
                style_comparison[style] = {
                    "user_percentage": user_percentage,
                    "community_percentage": community_percentage,
                    "difference": user_percentage - community_percentage
                }
        
        return {
            "user_consistency": user_consistency,
            "community_avg_consistency": community_avg,
            "consistency_difference": user_consistency - community_avg,
            "percentile": percentile,
            "style_comparison": style_comparison,
            "total_readings": user_data.get("total_readings", 0),
            "community_total_readings": community_data.get("total_readings", 0)
        }


def main():
    """CLI interface for community insights."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Community Insights and Analytics")
    parser.add_argument("--user-id", default="default", help="User ID to analyze")
    parser.add_argument("--update", action="store_true", help="Update community data")
    parser.add_argument("--insights", action="store_true", help="Show community insights")
    parser.add_argument("--compare", action="store_true", help="Compare user to community")
    parser.add_argument("--all", action="store_true", help="Show all information")
    
    args = parser.parse_args()
    
    analyzer = CommunityAnalyzer()
    
    if args.update or args.all:
        analyzer.update_community_data(args.user_id)
        print(f"✅ Updated community data for user: {args.user_id}")
    
    if args.insights or args.all:
        insights = analyzer.generate_community_insights()
        print("\n🌟 Community Insights")
        print("=" * 50)
        
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight.title}")
            print(f"   {insight.description}")
            print(f"   Confidence: {insight.confidence:.1f} | Data Points: {insight.data_points}")
            print(f"   Category: {insight.category}")
            print()
    
    if args.compare or args.all:
        comparison = analyzer.compare_user_to_community(args.user_id)
        if "error" not in comparison:
            print("\n📊 Community Comparison")
            print("=" * 50)
            print(f"Your Consistency: {comparison['user_consistency']:.1f}%")
            print(f"Community Average: {comparison['community_avg_consistency']:.1f}%")
            print(f"Difference: {comparison['consistency_difference']:+.1f}%")
            print(f"Percentile: {comparison['percentile']:.1f}%")
            print(f"Your Readings: {comparison['total_readings']}")
            print(f"Community Total: {comparison['community_total_readings']}")
            
            print("\n🎭 Style Comparison:")
            for style, data in comparison['style_comparison'].items():
                print(f"  {style.title()}: You {data['user_percentage']:.1f}% vs Community {data['community_percentage']:.1f}% ({data['difference']:+.1f}%)")


if __name__ == "__main__":
    main()
