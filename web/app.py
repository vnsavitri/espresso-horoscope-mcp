#!/usr/bin/env python3
"""
Espresso Horoscope Web Application

FastAPI web server that serves horoscope cards as HTML.
"""

import json
import re
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown to HTML with enhanced formatting for beautiful cards.
    """
    html = markdown_text
    
    # Extract shot ID and mantra for special styling
    shot_id_match = re.search(r'\*\*Shot ID:\*\* (.+)', html)
    mantra_match = re.search(r'\*\*Mantra:\*\* \*(.+?)\*', html)
    
    # Headers with enhanced styling
    html = re.sub(r'^# (.+)$', r'<div class="page-header"><h1>\1</h1></div>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<div class="card"><h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Shot ID styling
    if shot_id_match:
        shot_id = shot_id_match.group(1)
        html = re.sub(r'\*\*Shot ID:\*\* (.+)', f'<div class="shot-id">{shot_id}</div>', html)
    
    # Mantra styling
    if mantra_match:
        mantra = mantra_match.group(1)
        html = re.sub(r'\*\*Mantra:\*\* \*(.+?)\*', f'<div class="mantra">"{mantra}"</div>', html)
    
    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Code blocks (inline)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Enhanced list formatting for snapshot
    html = re.sub(r'^### 📊 Brew Snapshot', r'<h3>📊 Brew Snapshot</h3><div class="snapshot-grid">', html, flags=re.MULTILINE)
    
    # Convert snapshot items to grid items
    html = re.sub(r'^- \*\*(.+?):\*\* (.+)$', r'<div class="snapshot-item"><div class="snapshot-label">\1</div><div class="snapshot-value">\2</div></div>', html, flags=re.MULTILINE)
    
    # Close snapshot grid after the last snapshot item
    html = re.sub(r'(</div>\n\n### 🔮)', r'</div>\1', html)
    
    # Cosmic reading section
    html = re.sub(r'^### 🔮 Cosmic Reading', r'<div class="cosmic-reading"><h3>🔮 Cosmic Reading</h3>', html, flags=re.MULTILINE)
    
    # Personal touch section
    html = re.sub(r'^### ✨ Personal Touch', r'</div><div class="personal-touch"><h3>✨ Personal Touch</h3>', html, flags=re.MULTILINE)
    
    # Close personal touch and card
    html = re.sub(r'(\n\n### ✨ Personal Touch.*?)(\n\n|$)', r'\1</div></div>', html, flags=re.DOTALL)
    
    # Close cosmic reading if no personal touch
    if 'personal-touch' not in html and 'cosmic-reading' in html:
        html = re.sub(r'(cosmic-reading.*?)(\n\n|$)', r'\1</div></div>', html, flags=re.DOTALL)
    
    # Line breaks
    html = html.replace('\n', '<br>\n')
    
    # Horizontal rules
    html = html.replace('---', '<hr>')
    
    # Regular lists (non-snapshot)
    lines = html.split('<br>\n')
    in_list = False
    processed_lines = []
    
    for line in lines:
        if line.strip().startswith('- ') and 'snapshot-item' not in line:
            if not in_list:
                processed_lines.append('<ul>')
                in_list = True
            list_item = line.strip()[2:]  # Remove '- '
            processed_lines.append(f'<li>{list_item}</li>')
        else:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append(line)
    
    if in_list:
        processed_lines.append('</ul>')
    
    html = '<br>\n'.join(processed_lines)
    
    return html


def load_cards_markdown(cards_file: str = "out/cards.md") -> str:
    """Load the cards markdown file."""
    cards_path = Path(cards_file)
    
    if not cards_path.exists():
        raise FileNotFoundError(f"Cards file not found: {cards_file}")
    
    with open(cards_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_historical_data(user_id: str = "default") -> Dict[str, Any]:
    """Load historical data for a user."""
    try:
        # Import here to avoid circular imports
        import sys
        sys.path.append(str(Path(__file__).parent.parent))
        from cli.seed_util import load_reading_history, analyze_reading_trends, load_user_config
        
        history = load_reading_history(user_id)
        trends = analyze_reading_trends(user_id)
        config = load_user_config()
        
        return {
            "history": history,
            "trends": trends,
            "config": config
        }
    except Exception as e:
        return {
            "history": [],
            "trends": {},
            "config": {},
            "error": str(e)
        }


def format_date(date_str: str) -> str:
    """Format YYYYMMDD date string to readable format."""
    if len(date_str) >= 8:
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    return date_str


def create_trends_html(trends: Dict[str, Any]) -> str:
    """Create HTML for trends display."""
    if not trends or trends.get("total_readings", 0) == 0:
        return "<div class='trends-section'><h2>📊 Your Coffee Journey</h2><p>No reading history available yet. Generate some horoscope cards to see your trends!</p></div>"
    
    html = "<div class='trends-section'>"
    html += "<h2>📊 Your Coffee Journey</h2>"
    
    # Basic stats
    total_readings = trends.get("total_readings", 0)
    consistency_score = trends.get("consistency_score", 0)
    
    html += f"<div class='stats-grid'>"
    html += f"<div class='stat-card'><h3>{total_readings}</h3><p>Total Readings</p></div>"
    html += f"<div class='stat-card'><h3>{consistency_score:.1f}%</h3><p>Consistency Score</p></div>"
    html += "</div>"
    
    # Rule patterns
    rule_patterns = trends.get("rule_patterns", {})
    if rule_patterns:
        html += "<h3>🎲 Reading Patterns</h3>"
        html += "<div class='patterns-list'>"
        for rule, count in sorted(rule_patterns.items(), key=lambda x: x[1], reverse=True):
            percentage = trends.get("rule_percentages", {}).get(rule, 0)
            html += f"<div class='pattern-item'><span class='rule-name'>{rule.replace('_', ' ').title()}</span><span class='rule-count'>{count} ({percentage:.1f}%)</span></div>"
        html += "</div>"
    
    # Insights
    insights = trends.get("insights", [])
    if insights:
        html += "<h3>💡 Personalized Insights</h3>"
        html += "<div class='insights-list'>"
        for insight in insights:
            html += f"<div class='insight-item'>{insight}</div>"
        html += "</div>"
    
    # Improvement trends
    improvement_trends = trends.get("improvement_trends", {})
    if improvement_trends and improvement_trends.get("trend") != "insufficient_data":
        html += "<h3>📈 Improvement Trends</h3>"
        html += f"<div class='improvement-trend'>{improvement_trends.get('message', 'No trend data')}</div>"
    
    html += "</div>"
    return html


def create_timeline_html(history: List[Dict[str, Any]], limit: int = 10) -> str:
    """Create HTML for reading timeline."""
    if not history:
        return "<div class='timeline-section'><h2>📅 Recent Readings</h2><p>No reading history available yet.</p></div>"
    
    if limit:
        history = history[-limit:]
    
    html = "<div class='timeline-section'>"
    html += f"<h2>📅 Recent Readings ({len(history)} shown)</h2>"
    html += "<div class='timeline'>"
    
    for i, reading in enumerate(history, 1):
        date = format_date(reading.get("date", "unknown"))
        emoji = reading.get("emoji", "☕")
        title = reading.get("title", "Unknown")
        rule_hit = reading.get("rule_hit", "unknown")
        style = reading.get("style_bank", "unknown")
        
        html += f"""
        <div class='timeline-item'>
            <div class='timeline-marker'>{emoji}</div>
            <div class='timeline-content'>
                <h4>{title}</h4>
                <p class='timeline-date'>{date}</p>
                <p class='timeline-details'>Rule: {rule_hit.replace('_', ' ').title()} | Style: {style}</p>
            </div>
        </div>
        """
    
    html += "</div></div>"
    return html


def create_style_recommendations_html() -> str:
    """Create HTML for style recommendations tab."""
    return """
    <div class="style-section">
        <h2>🎭 Style Evolution</h2>
        <p>Discover your next style evolution based on seasonal patterns, personal growth, and optimal timing.</p>
        
        <div class="recommendations-grid">
            <div class="recommendation-card">
                <h3>🌱 Seasonal Recommendation</h3>
                <p>Perfect for autumn vibes - analytical mindset and cozy introspection</p>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: 80%"></div>
                </div>
                <span class="confidence-text">80% confidence</span>
            </div>
            
            <div class="recommendation-card">
                <h3>📈 Growth Suggestion</h3>
                <p>Ready to evolve from chill to punchy - natural progression in your journey</p>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: 70%"></div>
                </div>
                <span class="confidence-text">70% confidence</span>
            </div>
            
            <div class="recommendation-card">
                <h3>🕐 Time-Based</h3>
                <p>Ideal for afternoon - focused work and productive energy</p>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: 75%"></div>
                </div>
                <span class="confidence-text">75% confidence</span>
            </div>
        </div>
        
        <div class="style-evolution-timeline">
            <h3>Your Style Journey</h3>
            <div class="evolution-steps">
                <div class="evolution-step completed">
                    <div class="step-icon">🌱</div>
                    <div class="step-label">Chill</div>
                    <div class="step-time">Started</div>
                </div>
                <div class="evolution-step completed">
                    <div class="step-icon">⚡</div>
                    <div class="step-label">Punchy</div>
                    <div class="step-time">Evolved</div>
                </div>
                <div class="evolution-step current">
                    <div class="step-icon">🔬</div>
                    <div class="step-label">Nerdy</div>
                    <div class="step-time">Current</div>
                </div>
                <div class="evolution-step future">
                    <div class="step-icon">✨</div>
                    <div class="step-label">Mystical</div>
                    <div class="step-time">Next</div>
                </div>
            </div>
        </div>
    </div>
    """


def create_social_sharing_html() -> str:
    """Create HTML for social sharing tab."""
    return """
    <div class="social-section">
        <h2>📱 Share Your Coffee Journey</h2>
        <p>Share your espresso horoscope with the world! Choose your platform and get ready-to-post content.</p>
        
        <div class="platform-selector">
            <button class="platform-btn active" onclick="selectPlatform('twitter')">🐦 Twitter</button>
            <button class="platform-btn" onclick="selectPlatform('instagram')">📸 Instagram</button>
            <button class="platform-btn" onclick="selectPlatform('facebook')">👥 Facebook</button>
            <button class="platform-btn" onclick="selectPlatform('linkedin')">💼 LinkedIn</button>
        </div>
        
        <div class="social-content-preview">
            <div class="preview-header">
                <h3>✨ Universal Balance</h3>
                <p class="preview-mantra">"Universal balance restored."</p>
            </div>
            
            <div class="preview-stats">
                <div class="stat-item">☕ 2.03:1 ratio in 29s</div>
                <div class="stat-item">🎯 Sweet Spot</div>
            </div>
            
            <div class="preview-text">
                Your Gemini energy descends through this relaxed comet, creating cosmic harmony in every drop.
            </div>
            
            <div class="preview-hashtags">
                #EspressoHoroscope #Coffee #BaristaLife
            </div>
            
            <div class="character-count">
                <span class="count">156</span> / 280 characters
            </div>
        </div>
        
        <div class="sharing-actions">
            <button class="action-btn primary" onclick="copyToClipboard()">📋 Copy Text</button>
            <button class="action-btn" onclick="generateImage()">🖼️ Generate Image</button>
            <button class="action-btn" onclick="downloadCard()">💾 Download Card</button>
        </div>
        
        <div class="sharing-tips">
            <h4>💡 Sharing Tips</h4>
            <ul>
                <li>Post during peak coffee hours (7-9 AM, 2-4 PM)</li>
                <li>Use relevant hashtags to reach the coffee community</li>
                <li>Share your brewing journey, not just results</li>
                <li>Engage with other coffee enthusiasts</li>
            </ul>
        </div>
    </div>
    """


def create_community_insights_html() -> str:
    """Create HTML for community insights tab."""
    return """
    <div class="community-section">
        <h2>🌟 Community Insights</h2>
        <p>See how your coffee journey compares to the global espresso horoscope community!</p>
        
        <div class="community-stats">
            <div class="stat-card">
                <h3>6</h3>
                <p>Active Members</p>
            </div>
            <div class="stat-card">
                <h3>100%</h3>
                <p>Avg Consistency</p>
            </div>
            <div class="stat-card">
                <h3>Sweet Spot</h3>
                <p>Most Common</p>
            </div>
            <div class="stat-card">
                <h3>Chill</h3>
                <p>Popular Style</p>
            </div>
        </div>
        
        <div class="insights-grid">
            <div class="insight-card">
                <h3>🏆 Coffee Masters</h3>
                <p>6 community members (100%) have achieved 'Coffee Master' status with 80%+ consistency!</p>
                <div class="insight-confidence">Confidence: 90%</div>
            </div>
            
            <div class="insight-card">
                <h3>📊 Community Consistency</h3>
                <p>The community averages 100.0% consistency in hitting the sweet spot. That's excellent! The community has mastered the art of consistent extraction.</p>
                <div class="insight-confidence">Confidence: 90%</div>
            </div>
            
            <div class="insight-card">
                <h3>🎭 Popular Style</h3>
                <p>The 'chill' style is most popular in the community, used in 50.0% of readings.</p>
                <div class="insight-confidence">Confidence: 80%</div>
            </div>
        </div>
        
        <div class="user-comparison">
            <h3>📈 Your Performance vs Community</h3>
            <div class="comparison-stats">
                <div class="comparison-item">
                    <span class="label">Your Consistency:</span>
                    <span class="value">100.0%</span>
                </div>
                <div class="comparison-item">
                    <span class="label">Community Average:</span>
                    <span class="value">100.0%</span>
                </div>
                <div class="comparison-item">
                    <span class="label">Your Percentile:</span>
                    <span class="value">100.0%</span>
                </div>
                <div class="comparison-item">
                    <span class="label">Your Readings:</span>
                    <span class="value">6</span>
                </div>
            </div>
            
            <div class="achievement-badge">
                🏆 You're in the top tier of the community! Keep up the excellent work!
            </div>
        </div>
        
        <div class="community-tips">
            <h4>🤝 Community Tips</h4>
            <ul>
                <li>Share your readings to help build community insights</li>
                <li>Learn from other members' brewing techniques</li>
                <li>Celebrate community achievements together</li>
                <li>Help newcomers on their coffee journey</li>
            </ul>
        </div>
    </div>
    """


def create_html_page(markdown_content: str, include_history: bool = True) -> str:
    """Create a complete HTML page with styling."""
    html_content = markdown_to_html(markdown_content)
    
    # Load historical data if requested
    historical_html = ""
    if include_history:
        try:
            historical_data = load_historical_data()
            trends_html = create_trends_html(historical_data.get("trends", {}))
            timeline_html = create_timeline_html(historical_data.get("history", []), limit=5)
            # Get additional Phase 3 content
            style_recommendations_html = create_style_recommendations_html()
            community_insights_html = create_community_insights_html()
            
            historical_html = f"""
            <div class="nav-tabs">
                <button class="nav-tab active" onclick="showTab('cards')">☕ Current Cards</button>
                <button class="nav-tab" onclick="showTab('trends')">📊 Trends</button>
                <button class="nav-tab" onclick="showTab('timeline')">📅 Timeline</button>
                <button class="nav-tab" onclick="showTab('style')">🎭 Style</button>
                <button class="nav-tab" onclick="showTab('community')">🌟 Community</button>
            </div>
            
            <div id="cards" class="tab-content active">
                {html_content}
            </div>
            
            <div id="trends" class="tab-content">
                {trends_html}
            </div>
            
            <div id="timeline" class="tab-content">
                {timeline_html}
            </div>
            
            <div id="style" class="tab-content">
                {style_recommendations_html}
            </div>
            
            <div id="community" class="tab-content">
                {community_insights_html}
            </div>
            
            <script>
                function showTab(tabName) {{
                    // Hide all tab contents
                    const contents = document.querySelectorAll('.tab-content');
                    contents.forEach(content => content.classList.remove('active'));
                    
                    // Remove active class from all tabs
                    const tabs = document.querySelectorAll('.nav-tab');
                    tabs.forEach(tab => tab.classList.remove('active'));
                    
                    // Show selected tab content
                    document.getElementById(tabName).classList.add('active');
                    
                    // Add active class to clicked tab
                    event.target.classList.add('active');
                }}
            </script>
            """
        except Exception as e:
            historical_html = html_content
    
    if not historical_html:
        historical_html = html_content
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>☕ Espresso Horoscope</title>
    <style>
        :root {{
            --radius: 0.65rem;
            --background: oklch(1 0 0);
            --foreground: oklch(0.141 0.005 285.823);
            --card: oklch(1 0 0);
            --card-foreground: oklch(0.141 0.005 285.823);
            --popover: oklch(1 0 0);
            --popover-foreground: oklch(0.141 0.005 285.823);
            --primary: oklch(0.606 0.25 292.717);
            --primary-foreground: oklch(0.969 0.016 293.756);
            --secondary: oklch(0.967 0.001 286.375);
            --secondary-foreground: oklch(0.21 0.006 285.885);
            --muted: oklch(0.967 0.001 286.375);
            --muted-foreground: oklch(0.552 0.016 285.938);
            --accent: oklch(0.967 0.001 286.375);
            --accent-foreground: oklch(0.21 0.006 285.885);
            --destructive: oklch(0.577 0.245 27.325);
            --border: oklch(0.92 0.004 286.32);
            --input: oklch(0.92 0.004 286.32);
            --ring: oklch(0.606 0.25 292.717);
            --chart-1: oklch(0.646 0.222 41.116);
            --chart-2: oklch(0.6 0.118 184.704);
            --chart-3: oklch(0.398 0.07 227.392);
            --chart-4: oklch(0.828 0.189 84.429);
            --chart-5: oklch(0.769 0.188 70.08);
        }}

        .dark {{
            --background: oklch(0.141 0.005 285.823);
            --foreground: oklch(0.985 0 0);
            --card: oklch(0.21 0.006 285.885);
            --card-foreground: oklch(0.985 0 0);
            --popover: oklch(0.21 0.006 285.885);
            --popover-foreground: oklch(0.985 0 0);
            --primary: oklch(0.541 0.281 293.009);
            --primary-foreground: oklch(0.969 0.016 293.756);
            --secondary: oklch(0.274 0.006 286.033);
            --secondary-foreground: oklch(0.985 0 0);
            --muted: oklch(0.274 0.006 286.033);
            --muted-foreground: oklch(0.705 0.015 286.067);
            --accent: oklch(0.274 0.006 286.033);
            --accent-foreground: oklch(0.985 0 0);
            --destructive: oklch(0.704 0.191 22.216);
            --border: oklch(1 0 0 / 10%);
            --input: oklch(1 0 0 / 15%);
            --ring: oklch(0.541 0.281 293.009);
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
            background: var(--background);
            color: var(--foreground);
            min-height: 100vh;
        }}
        
        /* Dashboard Card Styling */
        .page-header {{
            text-align: center;
            margin-bottom: 32px;
            padding: 24px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        }}
        
        .page-header h1 {{
            font-size: 2rem;
            font-weight: 600;
            color: var(--foreground);
            margin: 0;
            letter-spacing: -0.025em;
        }}
        
        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 32px;
            margin: 24px 0;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        }}
        
        .card h2 {{
            color: var(--foreground);
            margin-bottom: 24px;
            font-size: 1.875rem;
            font-weight: 600;
            letter-spacing: -0.025em;
            text-align: center;
        }}
        
        .shot-id {{
            background: var(--muted);
            color: var(--muted-foreground);
            padding: 8px 16px;
            border-radius: calc(var(--radius) - 2px);
            font-size: 0.875rem;
            font-weight: 500;
            display: inline-block;
            margin-bottom: 16px;
            border: 1px solid var(--border);
        }}
        
        .mantra {{
            text-align: center;
            font-size: 1.125rem;
            color: var(--primary);
            font-weight: 500;
            font-style: italic;
            margin: 16px 0 24px 0;
            padding: 16px;
            background: var(--muted);
            border-radius: var(--radius);
            border: 1px solid var(--border);
        }}
        
        .snapshot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 16px;
            margin: 24px 0;
            padding: 24px;
            background: var(--muted);
            border-radius: var(--radius);
            border: 1px solid var(--border);
        }}
        
        .snapshot-item {{
            text-align: center;
            padding: 16px 12px;
            background: var(--card);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}
        
        .snapshot-item:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }}
        
        .snapshot-label {{
            font-size: 0.75rem;
            color: var(--muted-foreground);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
            font-weight: 500;
        }}
        
        .snapshot-value {{
            font-size: 1.5rem;
            color: var(--foreground);
            font-weight: 600;
            letter-spacing: -0.025em;
        }}
        
        .cosmic-reading {{
            background: var(--muted);
            padding: 24px;
            border-radius: var(--radius);
            margin: 24px 0;
            border: 1px solid var(--border);
        }}
        
        .cosmic-reading h3 {{
            color: var(--foreground);
            margin: 0 0 16px 0;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .cosmic-reading p {{
            font-size: 1rem;
            line-height: 1.6;
            color: var(--foreground);
            margin: 0;
            font-weight: 400;
        }}
        
        .personal-touch {{
            background: var(--accent);
            padding: 24px;
            border-radius: var(--radius);
            margin: 24px 0;
            border: 1px solid var(--border);
        }}
        
        .personal-touch h3 {{
            color: var(--accent-foreground);
            margin: 0 0 16px 0;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .personal-touch p {{
            margin: 0;
            font-size: 1rem;
            color: var(--accent-foreground);
            line-height: 1.6;
            font-weight: 400;
        }}
        
        .card h3 {{
            color: var(--foreground);
            margin: 24px 0 12px 0;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .card p {{
            margin: 12px 0;
            line-height: 1.6;
            color: var(--foreground);
            font-size: 1rem;
            font-weight: 400;
        }}
        
        .card ul {{
            margin: 16px 0;
            padding: 0;
            list-style: none;
        }}
        
        .card li {{
            margin: 8px 0;
            padding: 12px 16px;
            background: var(--muted);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            color: var(--foreground);
            font-size: 1rem;
            line-height: 1.5;
            font-weight: 400;
        }}
        
        .card strong {{
            color: var(--foreground);
            font-weight: 600;
        }}
        
        .card em {{
            color: var(--muted-foreground);
            font-style: italic;
            font-weight: 400;
        }}
        
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        
        h3 {{
            color: #2980b9;
            margin-top: 25px;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        em {{
            color: #7f8c8d;
            font-style: italic;
        }}
        
        code {{
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            color: #e74c3c;
        }}
        
        ul {{
            margin: 15px 0;
            padding-left: 20px;
        }}
        
        li {{
            margin: 8px 0;
            color: #555;
        }}
        
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(to right, #3498db, #9b59b6);
            margin: 30px 0;
            border-radius: 1px;
        }}
        
        .snapshot {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .cosmic-reading {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        
        .cosmic-reading h3 {{
            color: white;
            margin-top: 0;
        }}
        
        .brewing-wisdom {{
            background: #e8f5e8;
            border-left: 4px solid #27ae60;
            padding: 15px;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .brewing-wisdom h3 {{
            color: #27ae60;
            margin-top: 0;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        /* Trends and Timeline Styling */
        .trends-section, .timeline-section {{
            margin: 24px 0;
            padding: 24px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }}
        
        .stat-card {{
            background: var(--muted);
            padding: 24px;
            border-radius: var(--radius);
            text-align: center;
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }}
        
        .stat-card h3 {{
            font-size: 2rem;
            color: var(--primary);
            margin: 0 0 8px 0;
            font-weight: 600;
        }}
        
        .stat-card p {{
            color: var(--muted-foreground);
            margin: 0;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .patterns-list, .insights-list {{
            margin: 16px 0;
        }}
        
        .pattern-item, .insight-item {{
            background: var(--muted);
            padding: 16px;
            margin: 8px 0;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}
        
        .pattern-item:hover, .insight-item:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }}
        
        .pattern-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .rule-name {{
            font-weight: 600;
            color: var(--foreground);
        }}
        
        .rule-count {{
            color: var(--muted-foreground);
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .insight-item {{
            border-left: 3px solid var(--primary);
        }}
        
        .improvement-trend {{
            background: var(--muted);
            padding: 16px;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            border-left: 4px solid var(--primary);
        }}
        
        .timeline {{
            position: relative;
            padding-left: 32px;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 16px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: var(--border);
        }}
        
        .timeline-item {{
            position: relative;
            margin: 16px 0;
        }}
        
        .timeline-marker {{
            position: absolute;
            left: -24px;
            top: 0;
            width: 32px;
            height: 32px;
            background: var(--primary);
            border: 2px solid var(--background);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-foreground);
            font-size: 0.875rem;
        }}
        
        .timeline-content {{
            background: var(--muted);
            padding: 16px;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            margin-left: 20px;
            transition: all 0.2s ease;
        }}
        
        .timeline-content:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }}
        
        .timeline-content h4 {{
            margin: 0 0 8px 0;
            color: var(--foreground);
            font-weight: 600;
            font-size: 1rem;
        }}
        
        .timeline-date {{
            color: var(--muted-foreground);
            font-size: 0.75rem;
            margin: 0 0 8px 0;
            font-weight: 500;
        }}
        
        .timeline-details {{
            color: var(--muted-foreground);
            font-size: 0.875rem;
            margin: 0;
            font-weight: 400;
        }}
        
        .nav-tabs {{
            display: flex;
            margin: 24px 0;
            border-bottom: 1px solid var(--border);
            background: var(--card);
            border-radius: var(--radius) var(--radius) 0 0;
            padding: 0 16px;
        }}
        
        .nav-tab {{
            padding: 12px 16px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 0.875rem;
            color: var(--muted-foreground);
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
            font-weight: 500;
            border-radius: var(--radius) var(--radius) 0 0;
            margin-right: 0;
        }}
        
        .nav-tab:hover {{
            color: var(--foreground);
            background: var(--muted);
        }}
        
        .nav-tab.active {{
            color: var(--primary);
            border-bottom-color: var(--primary);
            background: var(--muted);
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        /* Phase 3 Styling */
        .style-section, .social-section, .community-section {{
            margin: 24px 0;
            padding: 24px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        }}
        
        .recommendations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }}
        
        .recommendation-card {{
            background: var(--muted);
            padding: 24px;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}
        
        .recommendation-card:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }}
        
        .confidence-bar {{
            width: 100%;
            height: 8px;
            background: var(--muted);
            border-radius: var(--radius);
            margin: 12px 0;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        
        .confidence-fill {{
            height: 100%;
            background: var(--primary);
            border-radius: var(--radius);
            transition: width 0.3s ease;
        }}
        
        .confidence-text {{
            font-size: 0.875rem;
            color: var(--muted-foreground);
            font-weight: 500;
        }}
        
        .style-evolution-timeline {{
            margin: 24px 0;
        }}
        
        .evolution-steps {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 24px 0;
        }}
        
        .evolution-step {{
            text-align: center;
            flex: 1;
            position: relative;
        }}
        
        .evolution-step::after {{
            content: '';
            position: absolute;
            top: 20px;
            right: -50%;
            width: 100%;
            height: 2px;
            background: var(--border);
            z-index: 1;
        }}
        
        .evolution-step:last-child::after {{
            display: none;
        }}
        
        .step-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--muted);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
            font-size: 1.5em;
            border: 2px solid var(--border);
        }}
        
        .evolution-step.completed .step-icon {{
            background: var(--primary);
            border-color: var(--primary);
            color: var(--primary-foreground);
        }}
        
        .evolution-step.current .step-icon {{
            background: var(--primary);
            border-color: var(--primary);
            color: var(--primary-foreground);
        }}
        
        .evolution-step.future .step-icon {{
            background: var(--muted);
            border-color: var(--border);
            color: var(--muted-foreground);
        }}
        
        .step-label {{
            font-weight: 600;
            color: var(--foreground);
            font-size: 0.875rem;
        }}
        
        .step-time {{
            font-size: 0.75rem;
            color: var(--muted-foreground);
            font-weight: 500;
        }}
        
        .platform-selector {{
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .platform-btn {{
            padding: 12px 20px;
            border: 1px solid var(--border);
            background: var(--muted);
            border-radius: var(--radius);
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
            font-size: 0.875rem;
        }}
        
        .platform-btn:hover {{
            border-color: var(--primary);
            background: var(--accent);
            transform: translateY(-1px);
        }}
        
        .platform-btn.active {{
            background: var(--primary);
            border-color: var(--primary);
            color: var(--primary-foreground);
        }}
        
        .social-content-preview {{
            background: var(--muted);
            padding: 24px;
            border-radius: var(--radius);
            margin: 24px 0;
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}
        
        .social-content-preview:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }}
        
        .preview-header h3 {{
            margin: 0 0 12px 0;
            color: var(--foreground);
            font-weight: 600;
            font-size: 1.25rem;
        }}
        
        .preview-mantra {{
            font-style: italic;
            color: var(--muted-foreground);
            margin: 0 0 16px 0;
            font-size: 1rem;
        }}
        
        .preview-stats {{
            display: flex;
            gap: 12px;
            margin: 16px 0;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            background: var(--card);
            padding: 8px 12px;
            border-radius: var(--radius);
            font-size: 0.875rem;
            color: var(--foreground);
            border: 1px solid var(--border);
            font-weight: 500;
        }}
        
        .preview-text {{
            margin: 16px 0;
            color: var(--foreground);
            line-height: 1.6;
            font-size: 1rem;
        }}
        
        .preview-hashtags {{
            color: var(--primary);
            font-weight: 600;
            margin: 16px 0;
        }}
        
        .character-count {{
            text-align: right;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        
        .count {{
            font-weight: bold;
            color: #27ae60;
        }}
        
        .sharing-actions {{
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .action-btn {{
            padding: 12px 20px;
            border: 2px solid #3498db;
            background: white;
            color: #3498db;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .action-btn.primary {{
            background: #3498db;
            color: white;
        }}
        
        .action-btn:hover {{
            background: #2980b9;
            color: white;
        }}
        
        .sharing-tips, .community-tips {{
            background: #e8f5e8;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #27ae60;
            margin: 20px 0;
        }}
        
        .sharing-tips h4, .community-tips h4 {{
            color: #27ae60;
            margin: 0 0 15px 0;
        }}
        
        .sharing-tips ul, .community-tips ul {{
            margin: 0;
            padding-left: 20px;
        }}
        
        .sharing-tips li, .community-tips li {{
            margin: 8px 0;
            color: #555;
        }}
        
        .community-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .insight-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #9b59b6;
        }}
        
        .insight-card h3 {{
            color: #2c3e50;
            margin: 0 0 15px 0;
        }}
        
        .insight-card p {{
            color: #555;
            line-height: 1.5;
            margin: 0 0 15px 0;
        }}
        
        .insight-confidence {{
            font-size: 0.9em;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .user-comparison {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid #ecf0f1;
        }}
        
        .comparison-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .comparison-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        
        .comparison-item .label {{
            color: #7f8c8d;
        }}
        
        .comparison-item .value {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .achievement-badge {{
            background: linear-gradient(135deg, #f39c12, #e67e22);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
        }}
        
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .timeline {{
                padding-left: 20px;
            }}
            
            .timeline-marker {{
                left: -15px;
                width: 25px;
                height: 25px;
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {historical_html}
        <div class="footer">
            <p>☕ Generated by Espresso Horoscope MCP</p>
        </div>
    </div>
</body>
</html>"""


# Create FastAPI app
app = FastAPI(
    title="Espresso Horoscope",
    description="Mystical espresso shot analysis and horoscope generation",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_cards():
    """Serve the horoscope cards as HTML."""
    try:
        markdown_content = load_cards_markdown()
        html_page = create_html_page(markdown_content)
        return HTMLResponse(content=html_page)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading cards: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "espresso-horoscope"}


@app.get("/cards/raw")
async def get_raw_cards():
    """Get raw markdown cards."""
    try:
        markdown_content = load_cards_markdown()
        return {"content": markdown_content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/cards.json")
async def get_cards_json():
    """Get structured JSON data for horoscope cards."""
    try:
        cards_file = Path(__file__).parent.parent / "out/cards.json"
        if not cards_file.exists():
            raise HTTPException(status_code=404, detail="Cards JSON file not found. Run the card generator first.")
        
        with open(cards_file, 'r') as f:
            cards_data = json.load(f)
        
        return JSONResponse(
            content=cards_data,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in cards file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading cards JSON: {str(e)}")


def get_user_cards_file(mmdd: str) -> Path:
    """Get the user-specific cards file path."""
    project_root = Path(__file__).parent.parent
    user_dir = project_root / "out" / "users"
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir / f"cards_{mmdd}.json"


def load_user_cards(mmdd: str) -> dict:
    """Load existing cards for a user."""
    user_file = get_user_cards_file(mmdd)
    if user_file.exists():
        try:
            with open(user_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Return empty structure if no existing cards
    return {
        "metadata": {
            "user_birth_mmdd": mmdd,
            "total_cards": 0,
            "last_updated": None
        },
        "readings": []
    }


def save_user_cards(mmdd: str, cards_data: dict):
    """Save cards for a user."""
    user_file = get_user_cards_file(mmdd)
    with open(user_file, 'w') as f:
        json.dump(cards_data, f, indent=2)


@app.get("/generate_cards")
async def generate_cards_for_date(mmdd: str):
    """Generate new horoscope cards for a specific birth date and add to user's history."""
    try:
        import subprocess
        import sys
        from datetime import datetime
        
        # Validate mmdd format
        if not mmdd or len(mmdd) != 4 or not mmdd.isdigit():
            raise HTTPException(status_code=400, detail="Invalid birth date format. Use MMDD format (e.g., 1021)")
        
        # Load existing user cards
        user_cards = load_user_cards(mmdd)
        
        # Generate a time variant for shot selection variation
        current_time = datetime.now()
        time_variant = current_time.strftime("%Y-%m-%d-%H:%M")
        
        # Run the demo deck generator for this specific date with time variant
        project_root = Path(__file__).parent.parent
        result = subprocess.run([
            sys.executable, "tools/make_demo_deck.py", 
            "--mmdd", mmdd,
            "--time-variant", time_variant
        ], cwd=project_root, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to generate cards: {result.stderr}")
        
        # Load the newly generated card
        cards_file = project_root / "out/cards.json"
        if not cards_file.exists():
            raise HTTPException(status_code=500, detail="Cards were generated but file not found")
        
        with open(cards_file, 'r') as f:
            new_cards_data = json.load(f)
        
        # Add the new card to user's history
        new_reading = new_cards_data["readings"][0]  # We know there's only 1 card now
        
        # Add to user's readings list
        user_cards["readings"].append(new_reading)
        
        # Sort by timestamp (newest first)
        user_cards["readings"].sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Update metadata
        user_cards["metadata"]["total_cards"] = len(user_cards["readings"])
        user_cards["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Save updated user cards
        save_user_cards(mmdd, user_cards)
        
        return JSONResponse(
            content=user_cards,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error generating cards: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cards: {str(e)}")


@app.get("/user_cards/{mmdd}")
async def get_user_cards(mmdd: str):
    """Get existing cards for a specific birth date without generating new ones."""
    try:
        # Validate mmdd format
        if not mmdd or len(mmdd) != 4 or not mmdd.isdigit():
            raise HTTPException(status_code=400, detail="Invalid birth date format. Use MMDD format (e.g., 1021)")
        
        # Load existing user cards
        user_cards = load_user_cards(mmdd)
        
        return JSONResponse(
            content=user_cards,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading user cards: {str(e)}")


@app.get("/history")
async def get_history(user_id: str = "default"):
    """Get reading history for a user."""
    try:
        historical_data = load_historical_data(user_id)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading history: {str(e)}")


@app.get("/trends")
async def get_trends(user_id: str = "default"):
    """Get trend analysis for a user."""
    try:
        historical_data = load_historical_data(user_id)
        return historical_data.get("trends", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading trends: {str(e)}")


@app.get("/timeline")
async def get_timeline(user_id: str = "default", limit: int = 10):
    """Get reading timeline for a user."""
    try:
        historical_data = load_historical_data(user_id)
        history = historical_data.get("history", [])
        if limit:
            history = history[-limit:]
        return {"readings": history, "total": len(historical_data.get("history", []))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading timeline: {str(e)}")


@app.get("/style-recommendations")
async def get_style_recommendations(user_id: str = "default"):
    """Get style evolution recommendations for a user."""
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from cli.style_evolution import StyleEvolutionTracker
        
        tracker = StyleEvolutionTracker(user_id)
        recommendations = tracker.generate_style_recommendations()
        
        return {
            "recommendations": [
                {
                    "style": rec.style,
                    "confidence": rec.confidence,
                    "reason": rec.reason,
                    "factors": {
                        "seasonal": rec.seasonal_factor,
                        "growth": rec.growth_factor,
                        "time_based": rec.usage_factor
                    }
                }
                for rec in recommendations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading style recommendations: {str(e)}")


@app.get("/social-content")
async def get_social_content(user_id: str = "default", platform: str = "twitter"):
    """Get social media content for sharing."""
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from cli.social_sharing import SocialSharingGenerator
        
        # Get latest card data
        historical_data = load_historical_data(user_id)
        history = historical_data.get("history", [])
        
        if not history:
            raise HTTPException(status_code=404, detail="No reading history found")
        
        # Create mock card data from latest reading
        latest_reading = history[-1]
        card_data = {
            "card": {
                "title": latest_reading.get("title", "Espresso Reading"),
                "emoji": latest_reading.get("emoji", "☕"),
                "mantra": "Brew with intention",  # Would come from actual card data
                "rule_hit": latest_reading.get("rule_hit", "unknown"),
                "snapshot": {
                    "brew_ratio": 2.03,  # Would come from actual shot data
                    "shot_time": 29.0,
                    "peak_pressure": 9.1,
                    "temp_avg": 91.7
                },
                "flavour_line": "Your cosmic energy flows through this perfect brew!"
            }
        }
        
        generator = SocialSharingGenerator()
        content = generator.generate_shareable_content(card_data, platform)
        
        return {
            "platform": content.platform,
            "title": content.title,
            "text": content.text,
            "hashtags": content.hashtags,
            "metadata": content.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating social content: {str(e)}")


@app.get("/community-insights")
async def get_community_insights():
    """Get community insights and analytics."""
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from cli.community_insights import CommunityAnalyzer
        
        analyzer = CommunityAnalyzer()
        insights = analyzer.generate_community_insights()
        
        return {
            "insights": [
                {
                    "title": insight.title,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "data_points": insight.data_points,
                    "category": insight.category,
                    "metadata": insight.metadata
                }
                for insight in insights
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading community insights: {str(e)}")


@app.get("/user-comparison")
async def get_user_comparison(user_id: str = "default"):
    """Compare user performance to community."""
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from cli.community_insights import CommunityAnalyzer
        
        analyzer = CommunityAnalyzer()
        comparison = analyzer.compare_user_to_community(user_id)
        
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading user comparison: {str(e)}")


def main():
    """Run the FastAPI server."""
    import uvicorn
    
    print("☕ Starting Espresso Horoscope Web Server...")
    print("📱 Open your browser to: http://127.0.0.1:8000")
    print("🔍 Health check: http://127.0.0.1:8000/health")
    print("📄 Raw cards: http://127.0.0.1:8000/cards/raw")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run(
        "web.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
