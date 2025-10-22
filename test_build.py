#!/usr/bin/env python3
"""
Test script to validate the built ScreenQA executable
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_executable():
    """Test the built executable for basic functionality"""
    
    print("🧪 Testing ScreenQA Executable...")
    
    # Check if executable exists
    exe_path = Path("dist/ScreenQA.exe")
    if not exe_path.exists():
        print(f"❌ Executable not found at {exe_path}")
        return False
    
    # Get file size
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"📦 Executable size: {size_mb:.1f} MB")
    
    # Check if size is reasonable (should be 20-50MB typically)
    if size_mb < 10:
        print("⚠️  Warning: Executable seems unusually small, might be missing dependencies")
    elif size_mb > 100:
        print("⚠️  Warning: Executable seems large, consider optimizing")
    else:
        print("✅ Executable size looks good")
    
    # Test if executable can start (quick launch and exit)
    print("🚀 Testing executable startup...")
    try:
        # Start the process with a timeout
        process = subprocess.Popen(
            [str(exe_path)], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Check if process is still running (good sign)
        if process.poll() is None:
            print("✅ Executable started successfully")
            
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Executable terminated cleanly")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️  Had to force-kill process")
            
            return True
        else:
            # Process exited immediately, check for errors
            stdout, stderr = process.communicate()
            print(f"❌ Executable exited immediately")
            if stderr:
                print(f"Error output: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start executable: {e}")
        return False

def validate_build_artifacts():
    """Validate build artifacts and structure"""
    
    print("\n📋 Validating Build Artifacts...")
    
    # Check dist directory
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist directory not found")
        return False
    
    # List all files in dist
    dist_files = list(dist_dir.glob("*"))
    print(f"📁 Files in dist/: {[f.name for f in dist_files]}")
    
    # Check for required files
    exe_file = dist_dir / "ScreenQA.exe"
    if exe_file.exists():
        print("✅ ScreenQA.exe found")
    else:
        print("❌ ScreenQA.exe not found")
        return False
    
    # Check build directory
    build_dir = Path("build")
    if build_dir.exists():
        print("✅ Build directory exists (contains build cache)")
    
    # Check spec file
    spec_file = Path("ScreenQA.spec")
    if spec_file.exists():
        print("✅ Spec file generated")
    
    return True

def main():
    """Main test function"""
    
    print("🔍 ScreenQA Build Validation Test")
    print("=" * 40)
    
    # Test 1: Validate artifacts
    artifacts_ok = validate_build_artifacts()
    
    # Test 2: Test executable
    if artifacts_ok:
        exe_ok = test_executable()
    else:
        exe_ok = False
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    print(f"   Build Artifacts: {'✅ PASS' if artifacts_ok else '❌ FAIL'}")
    print(f"   Executable Test: {'✅ PASS' if exe_ok else '❌ FAIL'}")
    
    if artifacts_ok and exe_ok:
        print("\n🎉 All tests passed! ScreenQA executable is ready for distribution.")
        print("\n📋 Distribution Notes:")
        print("   • Executable is self-contained (no Python required)")
        print("   • Chrome browser still required on target machine")
        print("   • Can be distributed as single .exe file")
        print("   • Compatible with Windows 10+ x64")
        return True
    else:
        print("\n❌ Some tests failed. Check the output above for issues.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        sys.exit(1)