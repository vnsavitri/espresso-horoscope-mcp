#!/usr/bin/env python3
"""
Performance monitoring for the espresso horoscope system.
Tracks commit times, file sizes, and optimization metrics.
"""

import time
import os
import subprocess
from pathlib import Path
from typing import Dict, Any

def measure_commit_time() -> float:
    """Measure time for a test commit."""
    start_time = time.time()
    
    # Create a small test file
    test_file = Path("test_performance.txt")
    test_file.write_text(f"Performance test at {time.time()}")
    
    # Add and commit
    subprocess.run(["git", "add", str(test_file)], capture_output=True)
    subprocess.run(["git", "commit", "-m", "Performance test"], capture_output=True)
    
    # Clean up
    test_file.unlink()
    subprocess.run(["git", "reset", "--hard", "HEAD~1"], capture_output=True)
    
    return time.time() - start_time

def analyze_file_sizes() -> Dict[str, Any]:
    """Analyze file sizes in the project."""
    sizes = {}
    
    # Check tools directory
    tools_path = Path("tools")
    if tools_path.exists():
        for file_path in tools_path.rglob("*.py"):
            size = file_path.stat().st_size
            sizes[str(file_path)] = size
    
    return sizes

def get_git_stats() -> Dict[str, Any]:
    """Get Git performance statistics."""
    try:
        # Get repository size
        result = subprocess.run(["du", "-sh", ".git"], capture_output=True, text=True)
        repo_size = result.stdout.strip().split()[0]
        
        # Get file count
        result = subprocess.run(["find", ".", "-name", "*.py", "-type", "f"], capture_output=True, text=True)
        file_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        
        return {
            "repository_size": repo_size,
            "python_files": file_count
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    """Run performance analysis."""
    print("📊 Espresso Horoscope Performance Analysis")
    print("=" * 50)
    
    # Measure commit time
    print("⏱️  Measuring commit performance...")
    commit_time = measure_commit_time()
    print(f"   Commit time: {commit_time:.3f} seconds")
    
    # Analyze file sizes
    print("\n📁 Analyzing file sizes...")
    sizes = analyze_file_sizes()
    large_files = {k: v for k, v in sizes.items() if v > 5000}  # Files > 5KB
    
    if large_files:
        print("   Large files (>5KB):")
        for file_path, size in sorted(large_files.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {file_path}: {size:,} bytes")
    else:
        print("   ✅ No large files found")
    
    # Git stats
    print("\n🔧 Git repository stats:")
    stats = get_git_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Performance recommendations
    print("\n💡 Performance Recommendations:")
    if commit_time > 1.0:
        print("   ⚠️  Commit time is slow - consider further optimization")
    else:
        print("   ✅ Commit performance is good")
    
    if len(large_files) > 3:
        print("   ⚠️  Many large files - consider modularization")
    else:
        print("   ✅ File sizes are optimized")

if __name__ == "__main__":
    main()
