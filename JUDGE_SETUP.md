# 🏆 Judge Setup Guide - Espresso Horoscope

**For OpenAI Open Model Hackathon Judges**

This guide ensures you can run the project locally on **any platform** (Windows, macOS, Linux) in under 5 minutes.

## 🚀 One-Command Setup

```bash
# Clone and setup
git clone https://github.com/vnsavitri/espresso-horoscope-mcp.git
cd espresso-horoscope-mcp
python setup.py
```

**That's it!** The setup script will:

- ✅ Check Python 3.8+ and Node.js 18+
- ✅ Install all dependencies automatically
- ✅ Create cross-platform start scripts
- ✅ Verify everything works

## 🎬 Start the Demo

```bash
# Terminal 1: Start backend
python start_backend.py

# Terminal 2: Start frontend  
python start_frontend.py

# Browser: Open http://localhost:3001
```

## 🎯 Demo the Project

1. **Enter birth date**: `1007` (October 7th)
2. **Click**: "Generate my espresso horoscope"
3. **See**: "Ristretto • Dense Constellation" with Libra zodiac
4. **Try different dates**: `0611`, `0101` for variety

## ✈️ Offline Capability Proof

1. **Turn off Wi-Fi**
2. **Generate another card** (it still works!)
3. **Turn Wi-Fi back on**

## 🤖 AI Features (Optional)

The system works perfectly without AI, but to see GPT-OSS integration:

1. **Install LM Studio**: https://lmstudio.ai
2. **Download model**: `gpt-oss-20b` (search in LM Studio)
3. **Set environment**: `export OPENAI_BASE_URL="http://localhost:1234/v1"`
4. **Restart**: The application will use AI for dynamic content

## 🛠️ Alternative Commands

```bash
# Cross-platform runner (replaces Makefile)
python run.py demo_user --mmdd 1007
python run.py backend
python run.py frontend
python run.py health
```

## 🚨 Troubleshooting

### **"Python not found"**

- **Windows**: Install from https://python.org
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

### **"Node.js not found"**

- Install from https://nodejs.org (LTS version)

### **"Dependencies failed"**

- Re-run: `python setup.py`
- Check internet connection

### **"Backend won't start"**

- Check port 8000 is free
- Try: `python start_backend.py`

### **"Frontend won't start"**

- Check port 3001 is free
- Try: `cd webui && npm run dev`

## 🎯 What Makes This Special

### **Technical Excellence**

- ✅ **Real espresso data**: 98 shot variants with authentic metrics
- ✅ **AI integration**: GPT-OSS for dynamic content generation
- ✅ **Offline capable**: Works without internet
- ✅ **Cross-platform**: Windows, macOS, Linux support
- ✅ **Modern stack**: FastAPI + Next.js + TypeScript

### **Innovation**

- ✅ **Unique concept**: Coffee + astrology + AI
- ✅ **Educational value**: Teaches espresso brewing
- ✅ **Beautiful design**: Professional UI/UX
- ✅ **Real-world application**: Gaggiuino machine integration

### **Hackathon Fit**

- ✅ **GPT-OSS integration**: Demonstrates local AI capabilities
- ✅ **Offline operation**: Proves independence from external APIs
- ✅ **Creative application**: Shows AI in unexpected domain
- ✅ **Technical depth**: Full-stack application with real data

## 📊 Demo Data

The system includes realistic espresso shot data:

- **Ristretto**: 1.8:1 ratio, 20-25s extraction
- **Espresso**: 2.0:1 ratio, 25-30s extraction
- **Lungo**: 3.0:1 ratio, 35-45s extraction
- **Americano**: 4.0:1 ratio, 40-50s extraction

Each shot includes:

- Pressure curves
- Flow rates
- Temperature profiles
- Channeling detection
- Extraction diagnostics

## 🎬 Quick Demo Script

1. **"This is Espresso Horoscope - AI-powered coffee fortune telling"**
2. **Show interface**: Beautiful purple gradient design
3. **Enter 1007**: "Ristretto • Dense Constellation" appears
4. **Enter 0611**: "Americano • Steady Supernova" (different zodiac)
5. **Turn off Wi-Fi**: "Still works offline!"
6. **Show terminal**: API calls and JSON responses
7. **"Built for the OpenAI Open Model Hackathon"**

## 🏆 Why This Wins

- **Innovation**: Unique combination of domains
- **Technical**: Modern stack with AI integration
- **Practical**: Real-world application
- **Beautiful**: Professional design
- **Accessible**: Easy to run and demo
- **Educational**: Teaches real skills

---

**Ready to judge?** The project is (hopefully) bulletproof and will run on (almost) )any system! 🚀
