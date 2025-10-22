#!/usr/bin/env python3
"""
Simple test script to verify ScreenQA functionality
"""
import os
import sys
import json

def test_basic_imports():
    """Test basic imports"""
    try:
        print("Testing basic imports...")
        
        # Test tkinter
        import tkinter as tk
        print("✓ tkinter imported successfully")
        
        # Test selenium
        from selenium import webdriver
        print("✓ selenium imported successfully")
        
        # Test PIL
        from PIL import Image
        print("✓ PIL imported successfully")
        
        # Test webdriver manager
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config_loading():
    """Test configuration loading"""
    try:
        print("\nTesting configuration loading...")
        
        config_path = os.path.join('config', 'devices.json')
        if not os.path.exists(config_path):
            print(f"✗ Config file not found: {config_path}")
            return False
            
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        devices = config.get('devices', {})
        print(f"✓ Loaded {len(devices)} device configurations")
        
        # List some devices
        for i, (name, info) in enumerate(list(devices.items())[:3]):
            resolution = f"{info['width']}x{info['height']}"
            platform = info.get('platform', 'Unknown')
            print(f"  - {name}: {resolution} ({platform})")
            
        return True
        
    except Exception as e:
        print(f"✗ Config loading error: {e}")
        return False

def test_screenshot_capture():
    """Test screenshot capture functionality"""
    try:
        print("\nTesting screenshot capture module...")
        
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from screenshot_capture import ScreenshotCapture
        print("✓ ScreenshotCapture imported successfully")
        
        capture = ScreenshotCapture()
        devices = capture.get_available_devices()
        
        total_devices = sum(len(device_list) for device_list in devices.values())
        print(f"✓ Available devices loaded: {total_devices} devices across {len(devices)} platforms")
        
        # List platforms
        for platform, device_list in devices.items():
            print(f"  - {platform}: {len(device_list)} devices")
            
        return True
        
    except Exception as e:
        print(f"✗ Screenshot capture test error: {e}")
        return False

def test_url_validation():
    """Test URL validation"""
    try:
        print("\nTesting URL validation...")
        
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from screenshot_capture import ScreenshotCapture
        
        capture = ScreenshotCapture()
        
        # Test valid URL
        valid, result = capture.validate_url("example.com")
        if valid:
            print(f"✓ URL validation works: {result}")
        else:
            print(f"✗ URL validation failed: {result}")
            
        return valid
        
    except Exception as e:
        print(f"✗ URL validation test error: {e}")
        return False

def test_directories():
    """Test directory structure"""
    print("\nTesting directory structure...")
    
    directories = ['src', 'config', 'screenshots', 'reports']
    all_good = True
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ {directory}/ exists")
        else:
            print(f"✗ {directory}/ missing")
            all_good = False
            
    return all_good

def main():
    """Run all tests"""
    print("ScreenQA Test Suite")
    print("=" * 50)
    
    tests = [
        ("Directory Structure", test_directories),
        ("Basic Imports", test_basic_imports),
        ("Configuration Loading", test_config_loading),
        ("Screenshot Capture Module", test_screenshot_capture),
        ("URL Validation", test_url_validation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! ScreenQA is ready to use.")
        print("\nTo start the application:")
        print("  Windows: Double-click start_screenqa.bat")
        print("  Manual:  python main.py")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the issues above.")
        
    return passed == len(results)

if __name__ == "__main__":
    main()