@echo off
echo 🎬 Espresso Horoscope Setup (Windows)
echo =====================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Run the Python setup script
echo 🚀 Running setup...
python setup.py

if errorlevel 1 (
    echo ❌ Setup failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup Complete!
echo.
echo Next steps:
echo 1. Terminal 1: python start_backend.py
echo 2. Terminal 2: python start_frontend.py
echo 3. Browser: http://localhost:3001
echo.
pause
