# ☕ Espresso Horoscope MCP

**Transform your espresso shots into personalized cosmic readings!**

A mystical fusion of espresso shot analysis and astrological horoscopes, powered by real Gaggiuino machine data or simulated shot patterns. Generate beautiful, personalized horoscope cards based on your birth date and espresso shot characteristics.

![Espresso Horoscope Demo](https://img.shields.io/badge/Status-MVP%20Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Next.js](https://img.shields.io/badge/Next.js-15+-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)

## 🌟 What Makes This Fun in a Weird Way

- **Real Espresso Data**: Uses actual shot metrics from Gaggiuino machines or realistic simulations
- **Astrological Integration**: Each birth date generates unique zodiac-based readings
- **Deterministic Yet Varied**: Same date = same cards, different date = completely different experience
- **Beautiful Visual Design**: Cosmic-themed cards with proper typography and layout
- **Real-time Generation**: Dynamic card creation for any birth date
- **MCP Integration**: Works as a Model Context Protocol server for AI assistants

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** (for the web interface)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vnsavitri/espresso-horoscope-mcp.git
   cd espresso-horoscope-mcp
   ```

2. **Install Python dependencies**
   ```bash
   pip install -e .
   ```

3. **Install Node.js dependencies**
   ```bash
   cd webui
   npm install
   cd ..
   ```

## 🎯 Usage Scenarios

### Scenario 1: Demo Mode (No Gaggiuino Machine)

Perfect for judges, users, or anyone who wants to experience the horoscope system without a physical machine.

#### Setup
```bash
# Start the FastAPI backend
make serve

# In a new terminal, start the web interface
cd webui && npm run dev
```

#### Experience
1. **Open browser**: `http://localhost:3000`
2. **Enter birth date**: Input MMDD format (e.g., `1021` for October 21st)
3. **Click**: "Generate my espresso horoscope"
4. **View cards**: See 3 personalized horoscope cards with cosmic guidance
5. **Try different dates**: Click "Try Different Date" to explore different zodiac signs

#### Demo Birth Dates to Try
- `1021` - Libra (October 21st)
- `0611` - Gemini (June 11th) 
- `0301` - Pisces (March 1st)
- `0701` - Cancer (July 1st)
- `1201` - Sagittarius (December 1st)
- `0802` - Leo (August 2nd)

### Scenario 2: Gaggiuino Machine Integration

For users with a Gaggiuino-equipped espresso machine.

#### Supported Gaggiuino Models
- **Gaggia Classic** (all variants)
- **Gaggia Classic Pro**
- **Gaggia Classic Evo**
- **Gaggia New Baby**
- **Gaggia Carezza**

*Note: Requires Gaggiuino firmware with MCP data export capability*

#### Setup
```bash
# Configure your Gaggiuino machine to export shot data
# Place shot data files in the data/ directory

# Start the system
make serve
cd webui && npm run dev
```

#### Data Format
The system expects shot data in JSONL format with the following structure:
```json
{
  "timestamp": "2025-01-09T10:30:00Z",
  "brew_ratio": 2.1,
  "shot_time": 28,
  "peak_pressure": 9.0,
  "temp_avg": 92.5,
  "channeling": 0.05,
  "flow_rate": 1.2
}
```

## 🎨 Features

### Dynamic Card Generation
- **Real-time Creation**: Each birth date generates completely new cards
- **Zodiac Integration**: 12 different zodiac signs with unique personalities
- **Deterministic Results**: Same date always produces the same cards
- **Varied Content**: Different dates produce different readings and advice

### Beautiful Web Interface
- **Cosmic Design**: Purple-blue gradient background with glass morphism
- **Responsive Layout**: Works on desktop and mobile
- **Smooth Animations**: Elegant transitions and loading states
- **Clean Typography**: Professional card design with proper spacing

### Technical Architecture
- **FastAPI Backend**: RESTful API with real-time card generation
- **Next.js Frontend**: Modern React application with TypeScript
- **SVG Card System**: Scalable vector graphics for crisp card rendering
- **MCP Protocol**: Model Context Protocol integration for AI assistants

## 🛠️ Development

### Project Structure
```
espresso-horoscope-mcp/
├── cli/                    # Command-line tools
├── web/                    # FastAPI backend
├── webui/                  # Next.js frontend
├── data_sources/           # Data loading utilities
├── features/               # Feature extraction
├── content/                # Astrological content
├── rules/                  # Diagnostic rules
├── tools/                  # Utility scripts
└── sample/                 # Sample data
```

### Key Commands
```bash
# Generate demo cards for a specific birth date
make demo_user MMDD=1021

# Generate cards with PNG export
make demo_user_png MMDD=1021

# Start backend server
make serve

# Run tests
make test

# Clean generated files
make clean
```

### API Endpoints
- `GET /` - Main web interface
- `GET /cards.json` - Get existing cards
- `GET /generate_cards?mmdd=1021` - Generate new cards for birth date
- `POST /api/card` - Generate PNG card image
- `GET /health` - Health check

## 🎭 Key Technical Details

### Deterministic Generation
The system uses a sophisticated seeding mechanism:
```python
seed = hash(shot_id + YYYYMMDD + user_birth_mmdd + style_bank + season + time_of_day)
```

This ensures:
- Same user + same date = same cards
- Different users = different cards
- Different dates = different cards
- Consistent results across sessions

### Zodiac Integration
Each birth date maps to a zodiac sign:
- **Aries** (March 21 - April 19): 🐏
- **Taurus** (April 20 - May 20): 🐂
- **Gemini** (May 21 - June 20): 👯‍♂️
- **Cancer** (June 21 - July 22): 🦀
- **Leo** (July 23 - August 22): 🦁
- **Virgo** (August 23 - September 22): 🦋
- **Libra** (September 23 - October 22): 🦢
- **Scorpio** (October 23 - November 21): 🦂
- **Sagittarius** (November 22 - December 21): 🏹
- **Capricorn** (December 22 - January 19): 🐐
- **Aquarius** (January 20 - February 18): 🐬
- **Pisces** (February 19 - March 20): 🐟

### Card Structure
Each horoscope card includes:
- **Zodiac Sign**: Visual icon and label
- **Title**: Cosmic-themed card name
- **Mantra**: Inspirational quote
- **Espresso Metrics**: Ratio, time, pressure, temperature, channeling
- **Cosmic Guidance**: Personalized advice
- **Narrative**: Flowing description
- **Metadata**: Seed, rule, severity information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Gaggiuino Community** for the amazing open-source espresso machine modifications
- **Astrological Traditions** for the cosmic inspiration
- **Espresso Enthusiasts** worldwide for the passion and dedication

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/vnsavitri/espresso-horoscope-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vnsavitri/espresso-horoscope-mcp/discussions)
- **Documentation**: [Wiki](https://github.com/vnsavitri/espresso-horoscope-mcp/wiki)

---

**May your shots be perfectly extracted and your cosmic readings be ever enlightening!** ☕✨