# Espresso Horoscope — Gaggiuino MCP Edition

Local espresso telemetry → playful “cosmic” cards with numeric next-shot advice.  
Built for the **gpt-oss hackathon**. The project **must apply `gpt-oss:20b`** (local, via Ollama) behind a flag, and run offline by default.

---

## What it does
- Reads **Gaggiuino MCP** shot data (recorded or replayed).
- Normalises to a simple shot schema.
- Extracts features (`features/extract.py`).
- Applies rules (`rules/diagnostics.yaml`) to produce clear diagnostics with numbers.
- Renders Markdown “horoscope” cards (`cli/cards.py`) and a tiny local web preview (`web/app.py`).

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


If you don’t have MCP samples, run the simulator (`tools/simulate_shots.py`) to create synthetic shots.

---

## MCP replay (no machine needed)

We bundle recorded `getShotData` JSON samples in `sample/mcp_shots/`.

Convert and run:

bash
python tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl
python features/extract.py data/shots.jsonl -o data/features.jsonl
python cli/cards.py --features data/features.jsonl \
  --rules rules/diagnostics.yaml --astro content/astro_map.yaml \
  --out out/cards.md
```

**With a machine (optional):** call MCP tools `getLatestShotId` → `getShotData(id)`, save the JSON, and replay as above.

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

---

## Licence and credits

* Code: MIT.
* Astronomy nouns: curated names only. Credit in `CREDITS.md`.

