# Espresso Horoscope Demo Script

This script demonstrates the complete Espresso Horoscope workflow, from data processing to visual card generation and export.

## Prerequisites

- Python 3.12+ with required dependencies installed
- LM Studio running with `gpt-oss-20b` model loaded
- Node.js and npm for the web UI
- Playwright installed for image export

## Demo Steps

### 1. Generate Horoscope Cards

First, let's generate the horoscope cards from the sample data:

```bash
# Generate cards with default settings
make demo
```

This will:
- Process sample MCP shot data (`sample/mcp_shots/*.json`)
- Extract brewing features (ratio, pressure, temperature, etc.)
- Generate personalized horoscope cards
- Create both Markdown (`out/cards.md`) and JSON (`out/cards.json`) outputs

**Expected Output:**
```
Generated structured data in out/cards.json
Generated 1 horoscope cards in out/cards.md
📊 Reading trends: X total readings
   Most common reading: sweet_spot (X times)
```

### 2. Open Local Web UI

Start the FastAPI server to serve the horoscope data:

```bash
# Start the FastAPI server
make web
```

The server will start on `http://127.0.0.1:8000` with:
- **Main Interface**: `http://127.0.0.1:8000/` (tabbed web interface)
- **JSON API**: `http://127.0.0.1:8000/cards.json` (structured data)

In another terminal, start the Next.js UI:

```bash
# Start the modern web UI
cd webui && npm run dev
```

The Next.js UI will be available at `http://localhost:3000` with:
- **Main Page**: Scrollable list of horoscope cards
- **Share Routes**: `http://localhost:3000/share/0` (individual cards)

### 3. Export High-Quality Images

Export horoscope cards as social media-ready images:

```bash
# Export images (requires FastAPI server running)
make export_images
```

This will:
- Check that FastAPI server is running on `127.0.0.1:8000`
- Export cards in both portrait (1080×1350) and OG (1200×630) formats
- Save both PNG and JPG versions with 90% quality
- Output to `webui/share/` directory

**Expected Output:**
```
✅ FastAPI server is running
📸 Exporting card images...
🎉 Images exported to webui/share/
```

**Generated Files:**
- `webui/share/card_0.png` - Portrait format (1080×1350)
- `webui/share/card_0.jpg` - Portrait format (compressed)
- `webui/share/card_0_og.png` - OG format (1200×630)
- `webui/share/card_0_og.jpg` - OG format (compressed)

### 4. Demonstrate AI Enhancement with LM Studio

Show how the system can enhance phrasing while keeping numbers fixed:

#### 4.1. First, ensure LM Studio is running:
- Open LM Studio
- Load the `gpt-oss-20b` model
- Start the local server (usually on `http://localhost:1234`)

#### 4.2. Set environment variables:
```bash
export OPENAI_BASE_URL="http://localhost:1234/v1"
export OPENAI_API_KEY="lm-studio"
```

#### 4.3. Generate cards with AI enhancement:
```bash
# Generate cards with GPT-OSS enhancement
python3 cli/cards.py \
  --features data/features.jsonl \
  --rules rules/diagnostics.yaml \
  --astro content/astro_map.yaml \
  --out out/cards.md \
  --style gptoss \
  --birth-date 0802
```

#### 4.4. Compare the results:

**Without AI Enhancement:**
- Title: "Stellar Alignment"
- Mantra: "Balance achieved through precision"
- Advice: "Maintain 1.9-2.2 ratio, 25-32s extraction"

**With AI Enhancement:**
- Title: "Cosmic Harmony" (may vary)
- Mantra: "The stars align in perfect brewing symphony" (may vary)
- Advice: "Keep that golden 1.9-2.2 ratio flowing for 25-32 magical seconds" (may vary)

**Key Points to Highlight:**
- ✅ **Numbers Stay Fixed**: Ratios, times, temperatures remain identical
- ✅ **Phrasing Changes**: Titles, mantras, and advice get creative rewording
- ✅ **Consistent Seeding**: Same birth date + same day = same enhanced phrasing
- ✅ **Fallback Handling**: If AI fails, original text is preserved

### 5. Test Different Birth Dates

Demonstrate how birth dates affect the horoscope:

```bash
# Test different zodiac signs
python3 cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md --birth-date 1225  # Capricorn 🐐
python3 cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md --birth-date 0601  # Gemini 👯‍♂️
python3 cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md --birth-date 0301  # Pisces 🐟
```

**Expected Variations:**
- **Zodiac Icons**: 🐐 (Capricorn), 👯‍♂️ (Gemini), 🐟 (Pisces)
- **Flavour Lines**: "Capricorn energy", "Gemini duality", "Pisces flow"
- **Seeds**: Different deterministic seeds for each birth date
- **Numbers**: Identical brewing metrics across all variations

### 6. Advanced Features Demo

#### 6.1. Historical Analysis:
```bash
# View reading history and trends
python3 cli/history.py --format=detailed
```

#### 6.2. Style Evolution:
```bash
# Get personalized style recommendations
python3 cli/style_evolution.py --birth-date 0802
```

#### 6.3. Community Insights:
```bash
# View community analytics (mock data)
python3 cli/community_insights.py
```

## Demo Checklist

- [ ] **Data Pipeline**: `make demo` generates cards successfully
- [ ] **Web Interface**: FastAPI server serves data at `http://127.0.0.1:8000`
- [ ] **Modern UI**: Next.js interface displays cards at `http://localhost:3000`
- [ ] **Image Export**: `make export_images` creates social media images
- [ ] **AI Enhancement**: LM Studio integration changes phrasing, keeps numbers
- [ ] **Birth Date Variation**: Different zodiac signs show different animal emojis
- [ ] **Deterministic Seeding**: Same inputs produce same outputs
- [ ] **Fallback Handling**: System works without AI enhancement

## Troubleshooting

### Common Issues:

1. **"Address already in use"**: Kill existing Python processes:
   ```bash
   pkill -9 python
   ```

2. **"Module not found"**: Ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **"LM Studio connection failed"**: Check LM Studio is running and API is enabled

4. **"Export images failed"**: Ensure both FastAPI and Next.js servers are running

### Verification Commands:

```bash
# Check FastAPI server
curl -s http://127.0.0.1:8000/cards.json | jq '.readings | length'

# Check Next.js server
curl -s http://localhost:3000 | grep -o "Espresso Horoscope"

# Check exported images
ls -la webui/share/*.png webui/share/*.jpg
```

## Key Features Demonstrated

1. **Data Processing**: Raw MCP → Normalized → Features → Cards
2. **Personalization**: Birth date → Zodiac → Animal emojis → Seeded content
3. **AI Integration**: LM Studio → Enhanced phrasing → Fixed numbers
4. **Visual Polish**: Neutral backgrounds → Typography → Consistent spacing
5. **Export Capabilities**: PNG/JPG → Portrait/OG → Social media ready
6. **Deterministic Seeding**: Same inputs → Same outputs → Reproducible results

This demo showcases a complete, production-ready system for generating personalized espresso horoscope cards with AI enhancement and professional visual output.
