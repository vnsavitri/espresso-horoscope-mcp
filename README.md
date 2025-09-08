# ☕ Espresso Horoscope

*Turn your espresso shots into mystical horoscope readings*

Hey there! 👋 I built this project because I'm obsessed with both espresso and the mystical side of things. What if your morning shot could tell you about your day ahead? That's exactly what this does - it analyzes your espresso shot data and generates personalized horoscope cards that are both scientifically accurate and delightfully cosmic.

## 🌟 What Makes This Special

This isn't just another data visualization tool. It's a **personalized experience** where:

- **Your birth date determines your readings** - Each person gets their own unique set of horoscope cards
- **Real brewing science meets cosmic wisdom** - Every reading is based on actual shot parameters (pressure, flow, temperature, etc.)
- **Deterministic yet varied** - Same birth date always gets the same cards, but different people get completely different experiences
- **Beautiful, shareable results** - Clean UI with high-quality image export for social media

## 🚀 Quick Start

Want to see it in action? Here's how to get started:

### Prerequisites

- Python 3.9+
- Node.js 18+ (for the web UI)
- A sense of wonder ✨

### Installation

```bash
# Clone the repo
git clone https://github.com/vnsavitri/espresso-horoscope-mcp.git
cd espresso-horoscope-mcp

# Install Python dependencies
pip install pyyaml requests fastapi uvicorn pydantic python-dotenv

# Install Node.js dependencies for the web UI
cd webui
npm install
cd ..
```

### Generate Your First Horoscope

```bash
# Generate a personalized deck for your birth date (MMDD format)
MMDD=0802 make demo_user

# Start the web server
make web

# In another terminal, start the modern UI
cd webui && npm run dev
```

Then open http://localhost:3001/?mmdd=0802 (replace 0802 with your birth date) and see your personalized horoscope cards!

## 🎯 How It Works

### The Magic Behind the Scenes

1. **Shot Palette Generation** - I created a diverse collection of 15 realistic espresso shots covering all brewing scenarios (fast, slow, choked, channeled, temperature issues, etc.)
2. **Deterministic Selection** - Your birth date (MMDD) is used to deterministically select 3 unique shots from the palette. Same birth date = same shots, different birth date = different shots.
3. **Feature Extraction** - Each shot gets analyzed for brewing metrics: brew ratio, shot time, peak pressure, temperature, and channeling score.
4. **Rule-Based Diagnostics** - The system applies diagnostic rules to identify what went right or wrong with each shot.
5. **Cosmic Interpretation** - Each diagnostic gets mapped to a mystical theme with personalized advice, powered by your zodiac sign and seeded randomness.
6. **Beautiful Rendering** - Everything comes together in gorgeous horoscope cards with your zodiac animal emoji and personalized cosmic wisdom.

### The Technical Stack

- **Backend**: Python with FastAPI serving JSON data
- **Frontend**: Next.js with TypeScript, Tailwind CSS, and shadcn/ui components
- **Data Pipeline**: Shot simulation → Feature extraction → Rule evaluation → Card generation
- **Personalization**: Deterministic hashing based on birth date + zodiac mapping
- **Export**: Playwright for high-quality image generation

## 🎨 Features

### Personalized Horoscope Cards

- **Zodiac Integration**: Your birth date determines your zodiac sign with fun animal emojis (🦁 Leo, 🐐 Capricorn, 🐟 Pisces, etc.)
- **Seeded Randomness**: Same shot + same user + same date = same phrasing, but different users get different cosmic interpretations
- **Real Brewing Data**: Every reading is based on actual shot parameters, not random text

### Modern Web Interface

- **Clean Design**: Minimalist, browser-friendly layout (768×1024) that looks great on any screen
- **Real-time Filtering**: Add `?mmdd=0802` to any URL to see personalized cards
- **Shareable Links**: Direct links to specific cards for specific users
- **Responsive**: Works perfectly on desktop and mobile

### High-Quality Export

- **Social Media Ready**: Export cards as PNG/JPG images in portrait (768×1024) or OG (1200×630) formats
- **Batch Export**: Generate all cards at once with a single command
- **Professional Quality**: Perfect for sharing on Instagram, Twitter, or anywhere else

## 🛠️ Make Targets

I've set up convenient make targets to streamline the workflow:

```bash
# Generate a personalized deck for your birth date
MMDD=0802 make demo_user

# Generate the full shot palette (15 diverse shots)
make demo

# Start the FastAPI server
make web

# Export high-quality images (requires server running)
make export_images

# Run all tests
make check
```

## 🎭 Demo Examples

Try these URLs to see different personalized experiences:

- **All cards**: http://localhost:3001/
- **User born Aug 2**: http://localhost:3001/?mmdd=0802
- **User born June 11**: http://localhost:3001/?mmdd=0611
- **User born Dec 25**: http://localhost:3001/?mmdd=1225
- **Share first card for Aug 2 user**: http://localhost:3001/share/0?mmdd=0802

Each birth date gets a completely different set of horoscope cards, but the same birth date always gets the same cards (perfect for consistency).

## 🤖 Optional AI Enhancement

Want to make the horoscope text even more creative? You can integrate with a local LLM:

### Option 1: LM Studio (Recommended)

```bash
# Install LM Studio and load gpt-oss-20b model
# Enable the API server in LM Studio GUI
export OPENAI_BASE_URL="http://localhost:1234/v1"
export OPENAI_API_KEY="lm-studio"

# Generate cards with AI enhancement
python3 cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md --style gptoss --birth-date 0802
```

### Option 2: Ollama

```bash
# Install Ollama and pull the model
brew install ollama
ollama pull gpt-oss:20b

# Set environment variables
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"

# Generate enhanced cards
python3 cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md --style gptoss --birth-date 0802
```

The AI enhancement keeps all numbers and units exactly the same while making the cosmic interpretations more creative and varied.

## 🧪 Testing & Quality

I've built comprehensive testing to ensure everything works reliably:

```bash
# Test determinism (same inputs = same outputs)
python3 tools/determinism_check.py

# Test full integration
python3 tools/integration_test.py

# Test specific birth date
python3 cli/picker.py --mmdd 0802 --k 3 --total 15
```

All tests pass, ensuring that:

- Same birth date always gets same cards
- Different birth dates get different cards
- Metrics formatting is consistent
- The full pipeline works end-to-end

## 📁 Project Structure

```
espresso-horoscope-mcp/
├── cli/                    # Command-line tools
│   ├── cards.py           # Main card generator
│   └── picker.py          # Deterministic shot picker
├── content/               # Configuration files
│   ├── astro_map.yaml    # Rule → cosmic theme mapping
│   └── flavour.yaml      # Text banks for variety
├── data_sources/          # Data processing
│   └── gaggiuino_loader.py
├── features/              # Feature extraction
│   └── extract.py
├── rules/                 # Diagnostic rules
│   └── diagnostics.yaml
├── tools/                 # Utilities
│   ├── simulate_shots.py  # Shot palette generator
│   ├── make_demo_deck.py  # User-specific deck builder
│   ├── determinism_check.py
│   └── integration_test.py
├── web/                   # FastAPI backend
│   └── app.py
├── webui/                 # Next.js frontend
│   ├── src/app/          # Pages and components
│   ├── src/lib/          # Utilities (picker logic)
│   └── scripts/          # Export scripts
└── sample/               # Demo data
    ├── mcp_shots/        # Individual shot files
    └── shots_palette.jsonl
```

## 🎯 For Judges & Contributors

### What Makes This Fun (In a Weird Way)

1. **Real Personalization**: Not just random text - each user gets a scientifically-based, personalized experience that's actually meaningful
2. **Deterministic Yet Varied**: Same user always gets same results, but different users get completely different experiences (it's like having your own cosmic fingerprint)
3. **Full-Stack Integration**: Everything works together seamlessly from data generation to beautiful UI (no duct tape required!)
4. **Actually Works**: Comprehensive testing, error handling, and documentation (because nothing's worse than a broken demo)
5. **Extensible**: Easy to add new shot patterns, diagnostic rules, or cosmic themes (the universe is your oyster)

### Key Technical Details

- **Deterministic Hashing**: Consistent shot selection across CLI and UI (same birth date = same cosmic destiny)
- **Realistic Data Generation**: 15 diverse shots covering all brewing scenarios (because real espresso is messy)
- **Modern Web Stack**: Next.js + TypeScript + Tailwind + shadcn/ui (keeping up with the times)
- **High-Quality Export**: Playwright-based image generation (for when you want to share your cosmic wisdom on social media)
- **Comprehensive Testing**: Determinism, integration, and consistency tests (because we all make mistakes)

### How to Evaluate

1. **Try different birth dates** - See how each gets unique cards
2. **Test consistency** - Same birth date should always give same results
3. **Check the UI** - Modern, responsive, and shareable
4. **Export images** - High-quality social media ready outputs
5. **Run tests** - Everything should pass determinism and integration tests

## 🤝 Contributing

Found a bug? Have an idea for a new cosmic theme? Want to add support for different espresso machines?

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Run the tests to ensure nothing breaks
5. Submit a pull request

I'm particularly interested in:

- New diagnostic rules for different brewing issues
- Additional cosmic themes and zodiac interpretations
- Support for other espresso machine data formats
- UI/UX improvements

## 📄 License

MIT License - feel free to use this for your own mystical espresso adventures!

## 🙏 Acknowledgments

- The espresso community for sharing shot data and brewing wisdom
- The open source projects that made this possible (FastAPI, Next.js, Tailwind, etc.)
- Everyone who's ever wondered if their morning shot has cosmic significance (it does!)

---

*May your shots be perfectly extracted and your horoscopes be ever in your favor* ☕✨

**Built with ☕ and ✨ by someone who believes every espresso shot tells a story**
