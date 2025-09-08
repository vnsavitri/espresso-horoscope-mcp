# Espresso Horoscope — Gaggiuino MCP Edition

Local espresso telemetry → playful "cosmic" cards with numeric next-shot advice.  
Built for the **gpt-oss hackathon**. The project **must apply `gpt-oss:20b`** (local, via Ollama) behind a flag, and run offline by default.

---

## What it does
- Reads **Gaggiuino MCP** shot data (recorded or replayed).
- Normalises to a simple shot schema.
- Extracts features (`features/extract.py`).
- Applies rules (`rules/diagnostics.yaml`) to produce clear diagnostics with numbers.
- Renders Markdown "horoscope" cards (`cli/cards.py`) and a beautiful web interface (`web/app.py`).
- **NEW**: Personalized horoscope cards with birth date integration
- **NEW**: Historical tracking and trend analysis
- **NEW**: Style evolution recommendations
- **NEW**: Community insights and comparisons
- **NEW**: Beautiful shadcn-inspired UI with 5 interactive tabs

---

## Why it fits “Best Local Agent”
- Fully local. No network calls at inference.
- Optional phrasing via **`gpt-oss:20b`** running locally.
- Deterministic numbers. Playful copy layered on top.

---

## Quick start

```bash
# 0) macOS tools (once)
brew install python@3.11 uv pre-commit jq

# 1) create venv and deps
uv venv
uv pip install -e .
pre-commit install

# 2) put recorded MCP JSON(s) here (or use the sample)
# sample/mcp_shots/shot_001.json

# 3) build demo
make demo          # -> data/features.jsonl, out/cards.md

# 4) preview
make web           # open http://127.0.0.1:8000

# 5) Optional: Add AI enhancement (see section below for Ollama or LM Studio setup)
```

## 🎨 **NEW: Beautiful Web Interface**

The web interface now features a beautiful shadcn-inspired design with 5 interactive tabs:

### **☕ Current Cards Tab**
- Your latest horoscope card with GPT-OSS enhanced text
- Beautiful dashboard-style layout with metrics grid
- Personalized content based on your birth date

### **📊 Trends Tab**
- Your coffee journey analytics
- Consistency scores and reading patterns
- Personalized insights based on your history

### **📅 Timeline Tab**
- Visual timeline of your readings
- Reading history and progression
- Style evolution over time

### **🎭 Style Tab**
- Style evolution recommendations
- Seasonal and growth suggestions
- Confidence scores for recommendations

### **🌟 Community Tab**
- Community insights and comparisons
- Global statistics and benchmarks
- See how you compare to other coffee enthusiasts

### **Running the Web Interface**

```bash
# Start the web server
python web/app.py

# Or use the make target
make web

# Open your browser to:
# http://localhost:8000 (or http://127.0.0.1:8000)
```


If you don’t have MCP samples, run the simulator (`tools/simulate_shots.py`) to create synthetic shots.

---

## MCP replay (no machine needed)

We bundle recorded `getShotData` JSON samples in `sample/mcp_shots/`.

Convert and run:

```bash
python tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl
python features/extract.py data/shots.jsonl -o data/features.jsonl
python cli/cards.py --features data/features.jsonl \
  --rules rules/diagnostics.yaml --astro content/astro_map.yaml \
  --out out/cards.md
```

**With a machine (optional):** call MCP tools `getLatestShotId` → `getShotData(id)`, save the JSON, and replay as above.

## 🎯 **NEW: Personalized Horoscope Cards**

The system now supports personalized horoscope cards based on your birth date:

```bash
# Generate personalized cards with your birth date (MMDD format)
python cli/cards.py --features data/features.jsonl \
  --rules rules/diagnostics.yaml --astro content/astro_map.yaml \
  --flavour content/flavour.yaml --out out/cards.md \
  --birth-date 0611 --style-bank chill --style gptoss

# Your birth date will influence:
# - Personalized cosmic readings
# - Style recommendations
# - Historical trend analysis
# - Seeded content generation for consistency
```

### **Birth Date Integration**
- **Format**: MMDD (e.g., 0611 for June 11th)
- **Influence**: Affects cosmic readings, style preferences, and content generation
- **Storage**: Stored locally in `~/.espresso_horoscope/config.yaml`
- **Privacy**: All data stays local, no external sharing

### **Style Banks**
- **chill**: Relaxed, introspective tone
- **punchy**: Energetic, action-oriented tone  
- **nerdy**: Technical, analytical tone
- **mystical**: Spiritual, cosmic tone

---

## Optional local phrasing with gpt-oss:20b

Off by default. When enabled, **only phrasing changes**. Numbers and units stay fixed.

### Option 1: Ollama (Recommended for judges)

```bash
# Install Ollama
brew install ollama

# Start Ollama service
brew services start ollama

# Pull the gpt-oss model (13GB download)
ollama pull gpt-oss:20b

# Set environment variables
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"

# Render with gpt-oss enhancement
python cli/cards.py --features data/features.jsonl \
  --rules rules/diagnostics.yaml --astro content/astro_map.yaml \
  --out out/cards.md --style gptoss
```

### Option 2: LM Studio (If you already have it)

```bash
# If you already have LM Studio with gpt-oss model:
# 1. Open LM Studio
# 2. Go to "Local Server" tab
# 3. Click "Start Server" (usually runs on port 1234)
# 4. Load your gpt-oss model in the Chat tab

# Set environment variables for LM Studio
export OPENAI_BASE_URL="http://localhost:1234/v1"
export OPENAI_API_KEY="ollama"

# Render with gpt-oss enhancement
python cli/cards.py --features data/features.jsonl \
  --rules rules/diagnostics.yaml --astro content/astro_map.yaml \
  --out out/cards.md --style gptoss
```

### Testing the AI Enhancement

```bash
# Test the gptoss helper directly
python cli/gptoss_helper.py "Your shot flows like liquid starlight at 2.03:1 ratio over 29 seconds."

# Should output enhanced text like:
# "Your shot glides like liquid starlight, dancing at a 2.03:1 ratio over 29 seconds, as the cosmos align..."
```

---

## Input schema (normalised shot JSON)

json
{
  "timestamp": "2025-09-06T08:12:22Z",
  "bean_id": "GAGGIUINO",
  "dose_g": 18.0,
  "target_mass_g": 36.5,
  "pressure_bar": [0.0,0.6,2.9,7.2,8.8,9.1,9.0,8.9],
  "flow_ml_s":    [0.0,0.0,0.1,0.8,1.1,1.3,1.4,1.4],
  "temp_c":       [88.0,90.1,91.8,92.1,92.2,92.1,92.0,91.9],
  "pump_pct":     [0,10,25,65,80,80,78,76],
  "preinfusion_ms": 6000,
  "first_drip_s": 7.2,
  "shot_end_s": 28.7,
  "grinder_setting": null,
  "basket": "18g",
  "roast_age_days": null,
  "user_rating": null
}

---

## Make targets

bash
make demo       # record/replay -> extract -> cards
make web        # local preview
make record     # MCP JSON -> data/shots.jsonl
make extract    # features -> data/features.jsonl
make cards      # cards -> out/cards.md
make check      # quick project checks (MCP + gpt-oss hooks)

---

## Project layout


features/extract.py            # compute features from JSONL
rules/diagnostics.yaml         # thresholds and advice
content/astro_map.yaml         # card templates
content/cosmic_lexicon.yaml    # nouns/tones (static, safe)
cli/cards.py                   # rule engine + renderer
web/app.py                     # tiny FastAPI preview
data_sources/gaggiuino_loader.py
tools/record_from_mcp.py       # replay MCP JSON -> shots.jsonl
tools/simulate_shots.py        # synthetic fallback
sample/mcp_shots/*.json        # recorded MCP samples

---

## Safety and privacy

* Anonymised data only. No device IDs. No PII.
* Entertainment tone with clear numeric notes.
* No health claims. Local by default.

---

## Judge checklist

* `make demo` produces `out/cards.md`.
* Sample data included.
* Offline run proven.
* `--style gptoss` shows **`gpt-oss:20b`** use locally (Ollama or LM Studio).
* Web interface at `http://127.0.0.1:8000` shows beautiful cosmic styling.
* ≤3-minute video matches repo steps.

### For AI Enhancement Testing:
* **Option 1 (Ollama)**: `brew install ollama && ollama pull gpt-oss:20b`
* **Option 2 (LM Studio)**: Use existing installation with gpt-oss model
* Set appropriate `OPENAI_BASE_URL` and test with `--style gptoss`

## 🚀 **For Judges and Users Forking This Repo**

### **Complete Setup Instructions**

1. **Clone and Setup**
```bash
git clone https://github.com/vnsavitri/espresso-horoscope-mcp.git
cd espresso-horoscope-mcp
```

2. **Install Dependencies**
```bash
# macOS
brew install python@3.11 jq

# Install Python dependencies
pip install -r requirements.txt
# OR if you have uv:
uv venv && uv pip install -e .
```

3. **Run the Demo**
```bash
# Generate sample data and cards
make demo

# Start the web interface
make web

# Open browser to http://localhost:8000
```

4. **Test AI Enhancement (Optional)**
```bash
# Option 1: Ollama
brew install ollama
ollama pull gpt-oss:20b
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"

# Option 2: LM Studio (if you have it)
# Start LM Studio server, then:
export OPENAI_BASE_URL="http://localhost:1234/v1"
export OPENAI_API_KEY="lm-studio"

# Test with AI enhancement
python cli/cards.py --features data/features.jsonl \
  --rules rules/diagnostics.yaml --astro content/astro_map.yaml \
  --flavour content/flavour.yaml --out out/cards.md \
  --birth-date 0611 --style-bank chill --style gptoss
```

### **Key Features to Test**

1. **Basic Functionality**
   - `make demo` should generate `out/cards.md`
   - Web interface should load at `http://localhost:8000`
   - All 5 tabs should be functional

2. **Personalization**
   - Try different birth dates: `--birth-date 0611`, `--birth-date 1225`
   - Test different style banks: `--style-bank chill`, `--style-bank punchy`
   - Check that content changes based on input

3. **AI Enhancement**
   - Test with `--style gptoss` flag
   - Verify numbers and units remain unchanged
   - Check that text is enhanced with cosmic/playful tone

4. **Web Interface**
   - Navigate between all 5 tabs
   - Check trends and timeline data
   - Verify responsive design

### **Troubleshooting**

- **Port conflicts**: Try different ports (3000, 5000, 8080)
- **Python issues**: Ensure you're using Python 3.11+
- **Dependencies**: Run `pip install -r requirements.txt`
- **LM Studio**: Make sure the server is running and model is loaded

---

## Licence and credits

* Code: MIT.
* Astronomy nouns: curated names only. Credit in `CREDITS.md`.

