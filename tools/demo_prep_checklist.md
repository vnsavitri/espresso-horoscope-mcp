# 🎬 Demo Video Preparation Checklist

## 🔧 Technical Setup (5 minutes before recording)

### **Services Status:**
- [ ] Backend running: `curl http://127.0.0.1:8000/health` returns `{"status":"healthy"}`
- [ ] Frontend running: `http://localhost:3001` loads the interface
- [ ] Both services stable (no errors in terminal)

### **Browser Setup:**
- [ ] Clean browser window (no other tabs)
- [ ] Zoom level appropriate (100% recommended)
- [ ] Developer tools closed
- [ ] Full screen mode ready

### **Demo Data Ready:**
- [ ] Test birth dates work: `1007`, `0611`, `0101`
- [ ] Cards generate successfully
- [ ] Coffee shot types show variety (Ristretto, Espresso, Lungo, Americano)
- [ ] Different zodiac signs appear
- [ ] Dynamic styles vary

## 🎯 Quick Test Run (2 minutes)

### **Test Sequence:**
1. Enter `1007` → Should show Libra with coffee shot type
2. Enter `0611` → Should show Gemini with different shot type  
3. Enter `0101` → Should show Capricorn with another variation
4. Check terminal shows API calls working
5. Verify no errors in browser console

### **Backup Plans:**
- [ ] Have README.md open for reference
- [ ] Terminal ready to show API calls
- [ ] Screenshots of different cards ready
- [ ] GitHub repository tab open

## 🎥 Recording Environment

### **Screen Setup:**
- [ ] Screen resolution: 1920x1080 or higher
- [ ] Recording software ready (OBS, QuickTime, etc.)
- [ ] Audio levels tested
- [ ] Clean desktop background

### **Content Ready:**
- [ ] Demo script printed or on second screen
- [ ] Key talking points memorized
- [ ] Technical details ready to explain
- [ ] Enthusiasm level: HIGH! 🚀

## 🚨 Emergency Fixes

### **If Backend Stops:**
```bash
cd web && uvicorn app:app --host 127.0.0.1 --port 8000 --reload &
```

### **If Frontend Stops:**
```bash
cd webui && npm run dev &
```

### **If Cards Don't Load:**
- Check browser console for errors
- Verify API is responding
- Try different birth date
- Show terminal API calls as backup

### **If Recording Fails:**
- Have static screenshots ready
- Show code walkthrough
- Demonstrate API endpoints
- Explain the concept verbally

## 🎯 Key Demo Points to Hit

1. **Opening:** "AI-powered espresso fortune telling"
2. **Core Demo:** Show `1007` → "Ristretto • Dense Constellation"
3. **Variety:** Show `0611` → "Americano • Steady Supernova"  
4. **Technical:** Show API calls and JSON responses
5. **Real-world:** Explain Gaggiuino integration
6. **Closing:** "Built for OpenAI Open Model Hackathon"

## 📱 Mobile Demo (Optional)

If you want to show mobile responsiveness:
- [ ] Test on phone/tablet
- [ ] Show touch interactions
- [ ] Demonstrate responsive design
- [ ] Highlight mobile-friendly interface

## 🎬 Final Recording Tips

- **Energy:** Be excited about your creation!
- **Pacing:** Don't rush, let cards load naturally
- **Clarity:** Speak clearly, explain technical terms
- **Variety:** Show different examples, not just one
- **Professional:** Clean interface, smooth interactions
- **Unique:** Emphasize what makes this special

---

**You've got this!** 🌟 Your project is amazing and the judges will love it!
