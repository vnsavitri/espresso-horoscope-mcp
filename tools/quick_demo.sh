#!/bin/bash

# 🎬 Espresso Horoscope MCP - Quick Demo Setup
# For OpenAI Open Model Hackathon

echo "🚀 Setting up Espresso Horoscope MCP Demo..."
echo "=============================================="

# Check if LM Studio is running
echo "📡 Checking LM Studio connection..."
if curl -s "http://10.10.0.178:1234/v1/models" | grep -q "gpt-oss"; then
    echo "✅ LM Studio with gpt-oss-20b is running!"
else
    echo "❌ LM Studio not running. Please start LM Studio and load gpt-oss-20b model"
    exit 1
fi

# Set environment variables
echo "🔧 Setting up environment..."
export OPENAI_BASE_URL="http://10.10.0.178:1234/v1"
echo "✅ OPENAI_BASE_URL set to: $OPENAI_BASE_URL"

# Test GPT-OSS connection
echo "🤖 Testing GPT-OSS connection..."
RESPONSE=$(curl -s -X POST "http://10.10.0.178:1234/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": "Say hello in one word"}],
    "max_tokens": 10
  }' | jq -r '.choices[0].message.content')

if [ "$RESPONSE" != "" ] && [ "$RESPONSE" != "null" ]; then
    echo "✅ GPT-OSS responding: $RESPONSE"
else
    echo "❌ GPT-OSS not responding properly"
    exit 1
fi

# Start FastAPI backend
echo "🌐 Starting FastAPI backend..."
pkill -f "uvicorn web.app:app" 2>/dev/null || true
sleep 2
uvicorn web.app:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
echo "✅ FastAPI backend started (PID: $BACKEND_PID)"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
if curl -s "http://127.0.0.1:8000/health" | grep -q "ok"; then
    echo "✅ Backend is responding"
else
    echo "❌ Backend not responding"
    exit 1
fi

# Start Next.js frontend
echo "🎨 Starting Next.js frontend..."
cd webui
pkill -f "next dev" 2>/dev/null || true
sleep 2
npm run dev &
FRONTEND_PID=$!
echo "✅ Next.js frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Test frontend
if curl -s "http://localhost:3000" | grep -q "Espresso Horoscope"; then
    echo "✅ Frontend is responding"
else
    echo "❌ Frontend not responding"
    exit 1
fi

echo ""
echo "🎉 DEMO READY!"
echo "==============="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://127.0.0.1:8000"
echo "🤖 GPT-OSS:  http://10.10.0.178:1234"
echo ""
echo "📝 Demo Steps:"
echo "1. Open http://localhost:3000"
echo "2. Enter birth date (e.g., 1021 for October 21st)"
echo "3. Click 'Generate my espresso horoscope'"
echo "4. Show the personalized reading with GPT-OSS generated style"
echo "5. Try different birth dates to show variety"
echo ""
echo "🎬 For video recording:"
echo "- Show terminal with API calls"
echo "- Show web interface generating readings"
echo "- Highlight GPT-OSS integration"
echo "- Demonstrate offline capability"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep script running
trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
wait
