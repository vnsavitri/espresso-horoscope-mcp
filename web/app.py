#!/usr/bin/env python3
"""
Espresso Horoscope Web Application

FastAPI web server that serves horoscope cards as HTML.
"""

import re
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown to HTML with basic formatting.
    Lightweight implementation for horoscope cards.
    """
    html = markdown_text
    
    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold text
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # Italic text
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Code blocks (inline)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Line breaks
    html = html.replace('\n', '<br>\n')
    
    # Horizontal rules
    html = html.replace('---', '<hr>')
    
    # Lists
    lines = html.split('<br>\n')
    in_list = False
    processed_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
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


def create_html_page(markdown_content: str) -> str:
    """Create a complete HTML page with styling."""
    html_content = markdown_to_html(markdown_content)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>☕ Espresso Horoscope</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
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
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
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
