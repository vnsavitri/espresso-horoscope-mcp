#!/usr/bin/env python3
"""
Cross-platform runner script for Espresso Horoscope
Replaces Makefile functionality on all platforms
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, cwd=None, shell=True):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=shell, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def find_python():
    """Find the best Python executable."""
    # Try current Python first
    if sys.executable:
        return sys.executable
    
    # Try common Python paths
    for python_cmd in ["python3", "python", "py"]:
        success, _, _ = run_command(f"{python_cmd} --version")
        if success:
            return python_cmd
    
    return "python3"  # Fallback

def demo_user(mmdd):
    """Generate demo cards for a specific birth date."""
    if not mmdd:
        print("❌ Please specify MMDD: python run.py demo_user --mmdd 1007")
        return False
    
    print(f"🎯 Creating demo deck for birth date {mmdd}...")
    
    python_cmd = find_python()
    success, stdout, stderr = run_command(f"{python_cmd} tools/make_demo_deck.py --mmdd {mmdd}")
    
    if success:
        print("🎉 Demo deck created -> out/cards.md")
        return True
    else:
        print("❌ Failed to create demo deck")
        print("Error:", stderr)
        return False

def demo_user_png(mmdd):
    """Generate demo cards with PNG export."""
    if not mmdd:
        print("❌ Please specify MMDD: python run.py demo_user_png --mmdd 1007")
        return False
    
    print(f"🎯 Creating demo deck with PNG cards for birth date {mmdd}...")
    
    python_cmd = find_python()
    success, stdout, stderr = run_command(f"{python_cmd} tools/make_demo_deck.py --mmdd {mmdd} --png --png-dir out/png_cards")
    
    if success:
        print("🎉 Demo deck with PNG cards created -> out/cards.md + out/png_cards/")
        return True
    else:
        print("❌ Failed to create demo deck")
        print("Error:", stderr)
        return False

def start_backend():
    """Start the FastAPI backend."""
    print("🚀 Starting FastAPI backend...")
    
    python_cmd = find_python()
    success, stdout, stderr = run_command(f"{python_cmd} -m uvicorn web.app:app --host 127.0.0.1 --port 8000 --reload")
    
    if not success:
        print("❌ Failed to start backend")
        print("Error:", stderr)
        return False
    
    return True

def start_frontend():
    """Start the Next.js frontend."""
    print("🎨 Starting Next.js frontend...")
    
    webui_path = Path("webui")
    if not webui_path.exists():
        print("❌ webui directory not found")
        return False
    
    success, stdout, stderr = run_command("npm run dev", cwd=webui_path)
    
    if not success:
        print("❌ Failed to start frontend")
        print("Error:", stderr)
        return False
    
    return True

def check_health():
    """Check if services are running."""
    print("🔍 Checking service health...")
    
    # Check backend
    success, stdout, stderr = run_command("curl -s http://127.0.0.1:8000/health")
    if success and "healthy" in stdout:
        print("✅ Backend: Healthy")
    else:
        print("❌ Backend: Not responding")
    
    # Check frontend
    success, stdout, stderr = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:3001")
    if success and stdout.strip() == "200":
        print("✅ Frontend: Healthy")
    else:
        print("❌ Frontend: Not responding")

def export_images():
    """Export card images."""
    print("📸 Exporting card images...")
    
    # Check if backend is running
    success, stdout, stderr = run_command("curl -s http://127.0.0.1:8000/cards.json")
    if not success:
        print("❌ Backend not running. Start with: python run.py backend")
        return False
    
    # Export images
    webui_path = Path("webui")
    success, stdout, stderr = run_command("npm run export:images", cwd=webui_path)
    
    if success:
        print("🎉 Images exported to webui/share/")
        return True
    else:
        print("❌ Failed to export images")
        print("Error:", stderr)
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Espresso Horoscope Runner")
    parser.add_argument("command", choices=[
        "demo_user", "demo_user_png", "backend", "frontend", 
        "health", "export_images", "setup"
    ], help="Command to run")
    parser.add_argument("--mmdd", help="Birth date in MMDD format")
    
    args = parser.parse_args()
    
    if args.command == "demo_user":
        return demo_user(args.mmdd)
    elif args.command == "demo_user_png":
        return demo_user_png(args.mmdd)
    elif args.command == "backend":
        return start_backend()
    elif args.command == "frontend":
        return start_frontend()
    elif args.command == "health":
        check_health()
        return True
    elif args.command == "export_images":
        return export_images()
    elif args.command == "setup":
        print("🔧 Running setup...")
        success, stdout, stderr = run_command(f"{sys.executable} setup.py")
        if success:
            print("✅ Setup complete")
            return True
        else:
            print("❌ Setup failed")
            print("Error:", stderr)
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
