#!/usr/bin/env python3
"""
Cross-platform setup script for Espresso Horoscope
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def run_command(cmd, shell=True):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_node_version():
    """Check if Node.js is installed and adequate."""
    success, stdout, stderr = run_command("node --version")
    if not success:
        print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org")
        return False
    
    version_str = stdout.strip().lstrip('v')
    major_version = int(version_str.split('.')[0])
    if major_version < 18:
        print(f"❌ Node.js 18+ required. Current version: {version_str}")
        return False
    
    print(f"✅ Node.js {version_str}")
    return True

def install_python_deps():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    
    # Try different installation methods
    methods = [
        # Method 1: pip install -e . (preferred)
        (f"{sys.executable} -m pip install -e .", "pip install -e ."),
        
        # Method 2: pip install -e . --user (for system Python)
        (f"{sys.executable} -m pip install -e . --user", "pip install -e . --user"),
        
        # Method 3: pip install -e . --break-system-packages (last resort)
        (f"{sys.executable} -m pip install -e . --break-system-packages", "pip install -e . --break-system-packages"),
        
        # Method 4: requirements.txt
        (f"{sys.executable} -m pip install -r requirements.txt", "requirements.txt"),
        
        # Method 5: requirements.txt --user
        (f"{sys.executable} -m pip install -r requirements.txt --user", "requirements.txt --user"),
    ]
    
    for cmd, method_name in methods:
        print(f"   Trying {method_name}...")
        success, stdout, stderr = run_command(cmd)
        if success:
            print(f"✅ Python dependencies installed via {method_name}")
            return True
        else:
            print(f"   ⚠️  {method_name} failed: {stderr.strip()[:100]}...")
    
    print("❌ All installation methods failed")
    print("💡 Try creating a virtual environment:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
    print("   python setup.py")
    return False

def install_node_deps():
    """Install Node.js dependencies."""
    print("📦 Installing Node.js dependencies...")
    
    webui_path = Path("webui")
    if not webui_path.exists():
        print("❌ webui directory not found")
        return False
    
    # Try npm install
    success, stdout, stderr = run_command("npm install", cwd=webui_path)
    if success:
        print("✅ Node.js dependencies installed")
        return True
    
    print("❌ Failed to install Node.js dependencies")
    print("Error:", stderr)
    return False

def check_lm_studio():
    """Check if LM Studio is available (optional)."""
    print("🤖 Checking LM Studio availability...")
    
    # Check if LM Studio is running on default port
    success, stdout, stderr = run_command("curl -s http://localhost:1234/v1/models")
    if success:
        print("✅ LM Studio detected and running")
        return True
    
    print("⚠️  LM Studio not detected (optional)")
    print("   The system will work with fallback content generation")
    print("   To enable AI features, install LM Studio and load gpt-oss-20b model")
    return False

def create_start_scripts():
    """Create platform-specific start scripts."""
    print("📝 Creating start scripts...")
    
    # Create start_backend.py
    backend_script = """#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from web.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
"""
    
    with open("start_backend.py", "w") as f:
        f.write(backend_script)
    
    # Create start_frontend.py
    frontend_script = """#!/usr/bin/env python3
import subprocess
import os
import sys

def main():
    webui_path = os.path.join(os.path.dirname(__file__), "webui")
    if not os.path.exists(webui_path):
        print("❌ webui directory not found")
        sys.exit(1)
    
    try:
        subprocess.run(["npm", "run", "dev"], cwd=webui_path, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to start frontend")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
    
    with open("start_frontend.py", "w") as f:
        f.write(frontend_script)
    
    # Make scripts executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("start_backend.py", 0o755)
        os.chmod("start_frontend.py", 0o755)
    
    print("✅ Start scripts created")
    return True

def create_quick_start_guide():
    """Create a quick start guide."""
    guide = """# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+ ✅
- Node.js 18+ ✅
- Git ✅

## Installation
1. Run: `python setup.py`
2. Wait for dependencies to install

## Start the Application
1. **Terminal 1**: `python start_backend.py`
2. **Terminal 2**: `python start_frontend.py`
3. **Browser**: Open http://localhost:3001

## Demo
1. Enter birth date (MMDD format, e.g., 1007)
2. Click "Generate my espresso horoscope"
3. Enjoy your cosmic reading!

## Optional: AI Features
- Install LM Studio from https://lmstudio.ai
- Download gpt-oss-20b model
- Set: `export OPENAI_BASE_URL="http://localhost:1234/v1"`
- Restart the application

## Troubleshooting
- Backend issues: Check http://127.0.0.1:8000/health
- Frontend issues: Check http://localhost:3001
- Dependencies: Re-run `python setup.py`
"""
    
    with open("QUICK_START.md", "w") as f:
        f.write(guide)
    
    print("✅ Quick start guide created")

def create_virtual_env():
    """Create a virtual environment if needed."""
    print("🐍 Checking for virtual environment...")
    
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Already in virtual environment")
        return True
    
    # Check if venv directory exists
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment exists")
        return True
    
    # Create virtual environment
    print("📦 Creating virtual environment...")
    success, stdout, stderr = run_command(f"{sys.executable} -m venv venv")
    if success:
        print("✅ Virtual environment created")
        print("💡 To activate:")
        if platform.system() == "Windows":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        return True
    else:
        print("⚠️  Failed to create virtual environment")
        print("   Continuing with system Python...")
        return False

def main():
    """Main setup function."""
    print("🎬 Espresso Horoscope Setup")
    print("=" * 40)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.executable}")
    print("")
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    # Try to create virtual environment (optional)
    create_virtual_env()
    
    # Install dependencies
    if not install_python_deps():
        return False
    
    if not install_node_deps():
        return False
    
    # Check optional components
    check_lm_studio()
    
    # Create helper scripts
    create_start_scripts()
    create_quick_start_guide()
    
    print("")
    print("🎉 Setup Complete!")
    print("")
    print("Next steps:")
    print("1. Terminal 1: python start_backend.py")
    print("2. Terminal 2: python start_frontend.py")
    print("3. Browser: http://localhost:3001")
    print("")
    print("📖 See QUICK_START.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
