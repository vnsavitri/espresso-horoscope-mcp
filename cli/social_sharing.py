#!/usr/bin/env python3
"""
Social Sharing System for Espresso Horoscope

Generates shareable content for social media platforms and creates
beautiful card images for sharing.
"""

import json
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass
class ShareableContent:
    """Shareable content for different platforms."""
    platform: str
    title: str
    text: str
    hashtags: List[str]
    image_url: Optional[str] = None
    metadata: Dict[str, Any] = None


class SocialSharingGenerator:
    """Generates social media content from horoscope cards."""
    
    def __init__(self):
        self.platform_configs = {
            "twitter": {
                "max_length": 280,
                "hashtag_limit": 3,
                "image_size": "1200x675"
            },
            "instagram": {
                "max_length": 2200,
                "hashtag_limit": 30,
                "image_size": "1080x1080"
            },
            "facebook": {
                "max_length": 63206,
                "hashtag_limit": 10,
                "image_size": "1200x630"
            },
            "linkedin": {
                "max_length": 3000,
                "hashtag_limit": 5,
                "image_size": "1200x627"
            }
        }
    
    def generate_shareable_content(self, card_data: Dict[str, Any], platform: str = "twitter") -> ShareableContent:
        """Generate shareable content for a specific platform."""
        config = self.platform_configs.get(platform, self.platform_configs["twitter"])
        
        # Extract card information
        title = card_data.get("card", {}).get("title", "Espresso Horoscope")
        emoji = card_data.get("card", {}).get("emoji", "☕")
        mantra = card_data.get("card", {}).get("mantra", "Brew with intention")
        rule_hit = card_data.get("card", {}).get("rule_hit", "unknown")
        snapshot = card_data.get("card", {}).get("snapshot", {})
        flavour_line = card_data.get("card", {}).get("flavour_line", "")
        
        # Generate platform-specific content
        if platform == "twitter":
            return self._generate_twitter_content(title, emoji, mantra, rule_hit, snapshot, flavour_line, config)
        elif platform == "instagram":
            return self._generate_instagram_content(title, emoji, mantra, rule_hit, snapshot, flavour_line, config)
        elif platform == "facebook":
            return self._generate_facebook_content(title, emoji, mantra, rule_hit, snapshot, flavour_line, config)
        elif platform == "linkedin":
            return self._generate_linkedin_content(title, emoji, mantra, rule_hit, snapshot, flavour_line, config)
        else:
            return self._generate_generic_content(title, emoji, mantra, rule_hit, snapshot, flavour_line)
    
    def _generate_twitter_content(self, title: str, emoji: str, mantra: str, rule_hit: str, 
                                 snapshot: Dict, flavour_line: str, config: Dict) -> ShareableContent:
        """Generate Twitter-optimized content."""
        # Create concise, engaging tweet
        brew_ratio = snapshot.get("brew_ratio", 0)
        shot_time = snapshot.get("shot_time", 0)
        
        text = f"{emoji} {title}\n\n{mantra}\n\n"
        text += f"☕ {brew_ratio:.1f}:1 ratio in {shot_time:.0f}s\n"
        text += f"🎯 {rule_hit.replace('_', ' ').title()}\n\n"
        text += f"{flavour_line}\n\n"
        text += "#EspressoHoroscope #Coffee #BaristaLife"
        
        # Truncate if too long
        if len(text) > config["max_length"]:
            text = text[:config["max_length"]-3] + "..."
        
        hashtags = ["#EspressoHoroscope", "#Coffee", "#BaristaLife"]
        
        return ShareableContent(
            platform="twitter",
            title=f"{emoji} {title}",
            text=text,
            hashtags=hashtags[:config["hashtag_limit"]],
            metadata={"character_count": len(text)}
        )
    
    def _generate_instagram_content(self, title: str, emoji: str, mantra: str, rule_hit: str,
                                   snapshot: Dict, flavour_line: str, config: Dict) -> ShareableContent:
        """Generate Instagram-optimized content."""
        brew_ratio = snapshot.get("brew_ratio", 0)
        shot_time = snapshot.get("shot_time", 0)
        peak_pressure = snapshot.get("peak_pressure", 0)
        temp_avg = snapshot.get("temp_avg", 0)
        
        text = f"{emoji} {title}\n\n"
        text += f"✨ {mantra}\n\n"
        text += f"📊 Shot Details:\n"
        text += f"• Ratio: {brew_ratio:.1f}:1\n"
        text += f"• Time: {shot_time:.0f}s\n"
        text += f"• Pressure: {peak_pressure:.1f} bar\n"
        text += f"• Temp: {temp_avg:.1f}°C\n\n"
        text += f"🔮 {flavour_line}\n\n"
        text += f"#EspressoHoroscope #Coffee #BaristaLife #Espresso #CoffeeLover #SpecialtyCoffee #CoffeeArt #Brewing #CoffeeTime #MorningCoffee #CoffeeAddict #CoffeeShop #CoffeeCulture #CoffeeBeans #CoffeeLife #CoffeeLove #CoffeeGram #CoffeePhotography #CoffeeCommunity #CoffeeInspiration #CoffeeTips #CoffeeHack #CoffeeScience #CoffeeMagic #CosmicCoffee"
        
        hashtags = [
            "#EspressoHoroscope", "#Coffee", "#BaristaLife", "#Espresso", "#CoffeeLover",
            "#SpecialtyCoffee", "#CoffeeArt", "#Brewing", "#CoffeeTime", "#MorningCoffee",
            "#CoffeeAddict", "#CoffeeShop", "#CoffeeCulture", "#CoffeeBeans", "#CoffeeLife",
            "#CoffeeLove", "#CoffeeGram", "#CoffeePhotography", "#CoffeeCommunity", "#CoffeeInspiration",
            "#CoffeeTips", "#CoffeeHack", "#CoffeeScience", "#CoffeeMagic", "#CosmicCoffee"
        ]
        
        return ShareableContent(
            platform="instagram",
            title=f"{emoji} {title}",
            text=text,
            hashtags=hashtags[:config["hashtag_limit"]],
            metadata={"character_count": len(text)}
        )
    
    def _generate_facebook_content(self, title: str, emoji: str, mantra: str, rule_hit: str,
                                  snapshot: Dict, flavour_line: str, config: Dict) -> ShareableContent:
        """Generate Facebook-optimized content."""
        brew_ratio = snapshot.get("brew_ratio", 0)
        shot_time = snapshot.get("shot_time", 0)
        peak_pressure = snapshot.get("peak_pressure", 0)
        temp_avg = snapshot.get("temp_avg", 0)
        channeling = snapshot.get("channeling", 0)
        
        text = f"{emoji} {title}\n\n"
        text += f"✨ {mantra}\n\n"
        text += f"Today's espresso reading reveals cosmic harmony in your brewing! 🌟\n\n"
        text += f"📊 Shot Analysis:\n"
        text += f"• Brew Ratio: {brew_ratio:.2f}:1\n"
        text += f"• Extraction Time: {shot_time:.0f} seconds\n"
        text += f"• Peak Pressure: {peak_pressure:.1f} bar\n"
        text += f"• Temperature: {temp_avg:.1f}°C\n"
        text += f"• Channeling Score: {channeling:.2f}\n\n"
        text += f"🔮 Cosmic Insight: {flavour_line}\n\n"
        text += f"The universe speaks through your coffee! Each shot tells a story of precision, passion, and cosmic alignment. \n\n"
        text += f"#EspressoHoroscope #Coffee #BaristaLife #Espresso #CoffeeLover #SpecialtyCoffee #CoffeeArt #Brewing #CoffeeTime #MorningCoffee"
        
        hashtags = [
            "#EspressoHoroscope", "#Coffee", "#BaristaLife", "#Espresso", "#CoffeeLover",
            "#SpecialtyCoffee", "#CoffeeArt", "#Brewing", "#CoffeeTime", "#MorningCoffee"
        ]
        
        return ShareableContent(
            platform="facebook",
            title=f"{emoji} {title}",
            text=text,
            hashtags=hashtags[:config["hashtag_limit"]],
            metadata={"character_count": len(text)}
        )
    
    def _generate_linkedin_content(self, title: str, emoji: str, mantra: str, rule_hit: str,
                                  snapshot: Dict, flavour_line: str, config: Dict) -> ShareableContent:
        """Generate LinkedIn-optimized content."""
        brew_ratio = snapshot.get("brew_ratio", 0)
        shot_time = snapshot.get("shot_time", 0)
        peak_pressure = snapshot.get("peak_pressure", 0)
        temp_avg = snapshot.get("temp_avg", 0)
        
        text = f"{emoji} {title}\n\n"
        text += f"✨ {mantra}\n\n"
        text += f"Fascinating how data science meets coffee artistry! Today's espresso analysis reveals the perfect balance of precision and creativity.\n\n"
        text += f"📊 Technical Metrics:\n"
        text += f"• Brew Ratio: {brew_ratio:.2f}:1 (optimal range: 1.8-2.2)\n"
        text += f"• Extraction Time: {shot_time:.0f}s (target: 25-30s)\n"
        text += f"• Peak Pressure: {peak_pressure:.1f} bar (ideal: 8-10 bar)\n"
        text += f"• Temperature: {temp_avg:.1f}°C (optimal: 90-95°C)\n\n"
        text += f"🔮 Insight: {flavour_line}\n\n"
        text += f"This demonstrates how systematic analysis and creative interpretation can transform routine tasks into meaningful experiences. The intersection of technology, data, and human creativity never ceases to amaze!\n\n"
        text += f"#DataScience #Coffee #Innovation #Technology #Creativity #Analytics #EspressoHoroscope #CoffeeTech"
        
        hashtags = [
            "#DataScience", "#Coffee", "#Innovation", "#Technology", "#Creativity", 
            "#Analytics", "#EspressoHoroscope", "#CoffeeTech"
        ]
        
        return ShareableContent(
            platform="linkedin",
            title=f"{emoji} {title}",
            text=text,
            hashtags=hashtags[:config["hashtag_limit"]],
            metadata={"character_count": len(text)}
        )
    
    def _generate_generic_content(self, title: str, emoji: str, mantra: str, rule_hit: str,
                                 snapshot: Dict, flavour_line: str) -> ShareableContent:
        """Generate generic shareable content."""
        brew_ratio = snapshot.get("brew_ratio", 0)
        shot_time = snapshot.get("shot_time", 0)
        
        text = f"{emoji} {title}\n\n"
        text += f"✨ {mantra}\n\n"
        text += f"☕ {brew_ratio:.1f}:1 ratio in {shot_time:.0f}s\n"
        text += f"🎯 {rule_hit.replace('_', ' ').title()}\n\n"
        text += f"{flavour_line}\n\n"
        text += f"#EspressoHoroscope #Coffee #BaristaLife"
        
        hashtags = ["#EspressoHoroscope", "#Coffee", "#BaristaLife"]
        
        return ShareableContent(
            platform="generic",
            title=f"{emoji} {title}",
            text=text,
            hashtags=hashtags,
            metadata={"character_count": len(text)}
        )
    
    def generate_card_image_html(self, card_data: Dict[str, Any], style: str = "modern") -> str:
        """Generate HTML for a shareable card image."""
        title = card_data.get("card", {}).get("title", "Espresso Horoscope")
        emoji = card_data.get("card", {}).get("emoji", "☕")
        mantra = card_data.get("card", {}).get("mantra", "Brew with intention")
        snapshot = card_data.get("card", {}).get("snapshot", {})
        flavour_line = card_data.get("card", {}).get("flavour_line", "")
        
        brew_ratio = snapshot.get("brew_ratio", 0)
        shot_time = snapshot.get("shot_time", 0)
        peak_pressure = snapshot.get("peak_pressure", 0)
        temp_avg = snapshot.get("temp_avg", 0)
        
        if style == "modern":
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        margin: 0;
                        padding: 40px;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }}
                    .card {{
                        background: rgba(255, 255, 255, 0.95);
                        color: #333;
                        border-radius: 20px;
                        padding: 40px;
                        max-width: 600px;
                        text-align: center;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                    }}
                    .emoji {{
                        font-size: 4em;
                        margin-bottom: 20px;
                    }}
                    .title {{
                        font-size: 2.5em;
                        font-weight: bold;
                        margin-bottom: 20px;
                        color: #2c3e50;
                    }}
                    .mantra {{
                        font-size: 1.3em;
                        font-style: italic;
                        color: #7f8c8d;
                        margin-bottom: 30px;
                    }}
                    .stats {{
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        gap: 20px;
                        margin: 30px 0;
                    }}
                    .stat {{
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 10px;
                        border-left: 4px solid #3498db;
                    }}
                    .stat-label {{
                        font-size: 0.9em;
                        color: #7f8c8d;
                        margin-bottom: 5px;
                    }}
                    .stat-value {{
                        font-size: 1.5em;
                        font-weight: bold;
                        color: #2c3e50;
                    }}
                    .flavour-line {{
                        font-size: 1.1em;
                        color: #27ae60;
                        margin-top: 30px;
                        padding: 20px;
                        background: #e8f5e8;
                        border-radius: 10px;
                        border-left: 4px solid #27ae60;
                    }}
                    .footer {{
                        margin-top: 30px;
                        font-size: 0.9em;
                        color: #7f8c8d;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="emoji">{emoji}</div>
                    <div class="title">{title}</div>
                    <div class="mantra">"{mantra}"</div>
                    
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-label">Brew Ratio</div>
                            <div class="stat-value">{brew_ratio:.2f}:1</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Time</div>
                            <div class="stat-value">{shot_time:.0f}s</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Pressure</div>
                            <div class="stat-value">{peak_pressure:.1f} bar</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Temperature</div>
                            <div class="stat-value">{temp_avg:.1f}°C</div>
                        </div>
                    </div>
                    
                    <div class="flavour-line">{flavour_line}</div>
                    
                    <div class="footer">
                        Generated by Espresso Horoscope MCP
                    </div>
                </div>
            </body>
            </html>
            """
        
        return "<!-- Card HTML would go here -->"
    
    def save_shareable_content(self, content: ShareableContent, output_dir: str = "out/social") -> str:
        """Save shareable content to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{content.platform}_{timestamp}.txt"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Platform: {content.platform}\n")
            f.write(f"Title: {content.title}\n")
            f.write(f"Character Count: {content.metadata.get('character_count', 0)}\n")
            f.write(f"Hashtags: {', '.join(content.hashtags)}\n")
            f.write(f"\n--- Content ---\n\n")
            f.write(content.text)
        
        return str(filepath)


def main():
    """CLI interface for social sharing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate social media content from horoscope cards")
    parser.add_argument("--json-file", required=True, help="JSON file with card data")
    parser.add_argument("--platform", choices=["twitter", "instagram", "facebook", "linkedin", "all"], 
                       default="twitter", help="Social media platform")
    parser.add_argument("--output-dir", default="out/social", help="Output directory")
    parser.add_argument("--preview", action="store_true", help="Preview content without saving")
    
    args = parser.parse_args()
    
    # Load card data
    with open(args.json_file, 'r') as f:
        card_data = json.load(f)
    
    generator = SocialSharingGenerator()
    
    if args.platform == "all":
        platforms = ["twitter", "instagram", "facebook", "linkedin"]
    else:
        platforms = [args.platform]
    
    for platform in platforms:
        content = generator.generate_shareable_content(card_data, platform)
        
        print(f"\n📱 {platform.title()} Content")
        print("=" * 50)
        print(f"Title: {content.title}")
        print(f"Character Count: {content.metadata.get('character_count', 0)}")
        print(f"Hashtags: {', '.join(content.hashtags)}")
        print(f"\nContent:\n{content.text}")
        
        if not args.preview:
            filepath = generator.save_shareable_content(content, args.output_dir)
            print(f"\n💾 Saved to: {filepath}")


if __name__ == "__main__":
    main()
