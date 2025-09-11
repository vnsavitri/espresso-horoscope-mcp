# Testing Instructions - Espresso Horoscope MCP

## Quick Start (2 minutes)

### Prerequisites
- Python 3.12+ and Node.js 18+
- LM Studio with GPT-OSS 20B model loaded
- Local model serving at `http://localhost:1234/v1`

### One-Command Setup
```bash
# Clone and setup
git clone https://github.com/vnsavitri/espresso-horoscope-mcp.git
cd espresso-horoscope-mcp

# Cross-platform setup (handles dependencies automatically)
./setup.sh    # macOS/Linux
# OR
setup.bat     # Windows
```

### Run Demo
```bash
# Start services and run offline demo
./tools/quick_demo.sh
```

## Testing Scenarios

### 1. Basic Functionality Test
- **Input:** Birth date `1007` (October 7th)
- **Expected:** Generate horoscope card with Libra sign
- **Verify:** Card displays with pressure curve, flow rate, and cosmic reading

### 2. Offline Proof Test
- **Step 1:** Run `./tools/quick_demo.sh`
- **Step 2:** Turn off Wi-Fi when prompted
- **Step 3:** Generate new card with birth date `0321`
- **Expected:** System works without internet, LM Studio shows live token generation

### 3. Determinism Test
- **Input:** Same birth date `0802` twice
- **Expected:** Same core reading, different AI-generated style variations
- **Verify:** Technical metrics consistent, creative content varies

### 4. Sample Data Test
- **Location:** `sample/mcp_shots/` contains 15 realistic shot files
- **Test:** Generate cards using different sample shots
- **Expected:** Each shot produces unique pressure/flow patterns

## Health Checks

### Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

### Frontend Health
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3001
# Expected: 200
```

### AI Model Health
```bash
curl -s http://localhost:1234/v1/models
# Expected: JSON with model list including "openai/gpt-oss-20b"
```

## Troubleshooting

### Common Issues
- **Port conflicts:** Backend uses 8000, frontend uses 3001
- **Model not loaded:** Ensure LM Studio has GPT-OSS 20B active
- **Dependencies:** Run `./setup.sh` to auto-install requirements

### Environment Variables
```bash
export OPENAI_BASE_URL="http://localhost:1234/v1"
export OPENAI_API_KEY="lm-studio"
```

## Sample Data

### Real Shot Data
- **Location:** `sample/mcp_shots/shot_001.json` through `shot_015.json`
- **Format:** JSON with pressure curves, flow rates, extraction metrics
- **Usage:** Automatically loaded when no live MCP data available

### Test Birth Dates
- `0321` - Aries (March 21)
- `0802` - Leo (August 2) 
- `1007` - Libra (October 7)
- `1225` - Capricorn (December 25)

## Expected Outputs

### Successful Card Generation
- Beautiful horoscope card with zodiac sign
- Real pressure/flow curve visualization
- AI-generated cosmic reading
- Technical extraction diagnostics

### LM Studio Activity
- Live token generation in dev logs
- Response time: 2-5 seconds per card
- No internet dependency once model loaded

## Performance Benchmarks
- **Card generation:** 2-5 seconds
- **Memory usage:** <1GB RAM
- **Offline capability:** 100% functional without internet
- **Cross-platform:** macOS, Linux, Windows supported
