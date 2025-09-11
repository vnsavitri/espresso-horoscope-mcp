#!/bin/bash
echo "🎬 Espresso Horoscope Setup (Unix)"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Run the Python setup script
echo "🚀 Running setup..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo "❌ Setup failed"
    exit 1
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Terminal 1: python3 start_backend.py"
echo "2. Terminal 2: python3 start_frontend.py"
echo "3. Browser: http://localhost:3001"
echo ""
