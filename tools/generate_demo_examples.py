#!/usr/bin/env python3
"""
Demo Examples Generator
Creates a variety of demo cards to showcase different features
"""

import requests
import json
import time
from typing import List, Dict, Any

def generate_demo_cards() -> List[Dict[str, Any]]:
    """Generate a variety of demo cards for the video."""
    
    demo_birth_dates = [
        ("1007", "October 7th (Sister's Birthday)"),
        ("0611", "June 11th (Gemini)"),
        ("0101", "January 1st (Capricorn)"),
        ("0321", "March 21st (Aries)"),
        ("1205", "December 5th (Sagittarius)")
    ]
    
    demo_cards = []
    
    print("🎬 Generating demo cards for video...")
    
    for mmdd, description in demo_birth_dates:
        print(f"  Generating card for {mmdd} ({description})...")
        
        try:
            response = requests.get(f"http://127.0.0.1:8000/generate_cards?mmdd={mmdd}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("readings"):
                    card = data["readings"][0]
                    demo_cards.append({
                        "birth_date": mmdd,
                        "description": description,
                        "title": card["card"]["title"],
                        "zodiac": card["card"]["zodiac"],
                        "zodiac_icon": card["card"]["zodiac_icon"],
                        "style": card["user_context"]["style_preference"],
                        "shot_ratio": card["card"]["snapshot"]["brew_ratio"],
                        "shot_time": card["card"]["snapshot"]["shot_time"],
                        "reading_preview": card["card"]["template"][:100] + "..."
                    })
                    print(f"    ✅ {card['card']['title']}")
                else:
                    print(f"    ❌ No readings returned")
            else:
                print(f"    ❌ API error: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        time.sleep(1)  # Be nice to the API
    
    return demo_cards

def print_demo_summary(cards: List[Dict[str, Any]]):
    """Print a summary of demo cards for the video script."""
    
    print("\n" + "="*60)
    print("🎬 DEMO VIDEO CARD EXAMPLES")
    print("="*60)
    
    for i, card in enumerate(cards, 1):
        print(f"\n{i}. {card['description']} ({card['birth_date']})")
        print(f"   Title: {card['title']}")
        print(f"   Zodiac: {card['zodiac_icon']} {card['zodiac']}")
        print(f"   Style: {card['style']}")
        print(f"   Shot: {card['shot_ratio']:.2f}:1 ratio, {card['shot_time']:.0f}s")
        print(f"   Reading: {card['reading_preview']}")
    
    print("\n" + "="*60)
    print("🎯 DEMO SCRIPT SUGGESTIONS")
    print("="*60)
    
    # Find variety examples
    coffee_types = set()
    zodiac_signs = set()
    
    for card in cards:
        coffee_type = card['title'].split(' • ')[0]
        coffee_types.add(coffee_type)
        zodiac_signs.add(card['zodiac'])
    
    print(f"\nCoffee Shot Types Available: {', '.join(sorted(coffee_types))}")
    print(f"Zodiac Signs Available: {', '.join(sorted(zodiac_signs))}")
    
    print(f"\n📝 Suggested Demo Flow:")
    print(f"1. Start with {cards[0]['birth_date']} → {cards[0]['title']}")
    print(f"2. Show variety with {cards[1]['birth_date']} → {cards[1]['title']}")
    print(f"3. Highlight different zodiac: {cards[2]['birth_date']} → {cards[2]['title']}")
    
    if len(cards) > 3:
        print(f"4. Show more variety: {cards[3]['birth_date']} → {cards[3]['title']}")

def save_demo_data(cards: List[Dict[str, Any]]):
    """Save demo data to JSON file."""
    
    demo_data = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_cards": len(cards),
        "cards": cards
    }
    
    with open("out/demo_cards.json", "w") as f:
        json.dump(demo_data, f, indent=2)
    
    print(f"\n💾 Demo data saved to out/demo_cards.json")

def main():
    """Main function to generate demo examples."""
    
    print("🎬 Espresso Horoscope Demo Video Preparation")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running. Please start with:")
            print("   cd web && uvicorn app:app --host 127.0.0.1 --port 8000 --reload &")
            return
    except:
        print("❌ Backend not accessible. Please start with:")
        print("   cd web && uvicorn app:app --host 127.0.0.1 --port 8000 --reload &")
        return
    
    print("✅ Backend is running")
    
    # Generate demo cards
    cards = generate_demo_cards()
    
    if cards:
        print_demo_summary(cards)
        save_demo_data(cards)
        print(f"\n🎉 Generated {len(cards)} demo cards ready for video!")
    else:
        print("\n❌ No demo cards generated. Check backend status.")

if __name__ == "__main__":
    main()
