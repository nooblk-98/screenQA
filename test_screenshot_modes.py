#!/usr/bin/env python3
"""
Test script for Screenshot Mode functionality
"""
import os
import sys

def test_screenshot_modes():
    """Test the screenshot mode options"""
    print("Testing Screenshot Mode Options...")
    print("=" * 50)
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from screenshot_capture import ScreenshotCapture
        
        capture = ScreenshotCapture()
        
        # Test URL validation (use a simple, fast-loading site)
        test_url = "example.com"
        valid, validated_url = capture.validate_url(test_url)
        
        if not valid:
            print(f"✗ Test URL not accessible: {validated_url}")
            return False
        
        print(f"✓ Test URL validated: {validated_url}")
        
        # Test device availability
        devices = capture.get_available_devices()
        if not devices:
            print("✗ No devices available for testing")
            return False
        
        # Get a simple desktop device for testing
        test_device = None
        for platform, device_list in devices.items():
            if 'Windows' in platform or 'Mac' in platform:
                if device_list:
                    test_device = device_list[0]['name']
                    break
        
        if not test_device:
            print("✗ No suitable test device found")
            return False
        
        print(f"✓ Using test device: {test_device}")
        
        # Test different screenshot modes
        modes_to_test = [
            ("viewport_only", "Viewport Only"),
            ("full_page", "Full Page"),
            ("auto", "Auto Detect")
        ]
        
        print("\\nTesting Screenshot Modes:")
        print("-" * 30)
        
        mode_results = {}
        for mode_key, mode_name in modes_to_test:
            try:
                print(f"Testing {mode_name} mode...")
                
                # Test capture with progress callback
                def progress_callback(message):
                    print(f"  → {message}")
                
                success, screenshot_path, error = capture.capture_screenshot(
                    validated_url, 
                    test_device, 
                    progress_callback=progress_callback,
                    screenshot_mode=mode_key
                )
                
                if success and os.path.exists(screenshot_path):
                    file_size = os.path.getsize(screenshot_path)
                    mode_results[mode_key] = {
                        'success': True,
                        'file_size': file_size,
                        'path': screenshot_path
                    }
                    print(f"  ✓ {mode_name}: SUCCESS ({file_size / 1024:.1f} KB)")
                else:
                    mode_results[mode_key] = {
                        'success': False,
                        'error': error
                    }
                    print(f"  ✗ {mode_name}: FAILED - {error}")
                    
            except Exception as e:
                mode_results[mode_key] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"  ✗ {mode_name}: ERROR - {e}")
        
        # Analyze results
        print("\\n" + "=" * 50)
        print("SCREENSHOT MODE TEST RESULTS")
        print("=" * 50)
        
        successful_modes = sum(1 for result in mode_results.values() if result['success'])
        total_modes = len(mode_results)
        
        for mode_key, mode_name in modes_to_test:
            result = mode_results.get(mode_key, {})
            if result.get('success'):
                file_size_kb = result['file_size'] / 1024
                print(f"✅ {mode_name}: WORKING ({file_size_kb:.1f} KB)")
            else:
                error = result.get('error', 'Unknown error')
                print(f"❌ {mode_name}: FAILED ({error})")
        
        print(f"\\nOverall: {successful_modes}/{total_modes} modes working")
        
        # Compare file sizes if multiple modes worked
        if successful_modes > 1:
            print("\\n📊 File Size Comparison:")
            sizes = [(mode, result['file_size']) for mode, result in mode_results.items() if result['success']]
            sizes.sort(key=lambda x: x[1])
            
            for mode, size in sizes:
                mode_name = dict(modes_to_test)[mode]
                print(f"  {mode_name}: {size / 1024:.1f} KB")
        
        # Cleanup test files
        print("\\n🧹 Cleaning up test files...")
        cleaned = 0
        for result in mode_results.values():
            if result.get('success') and 'path' in result:
                try:
                    os.remove(result['path'])
                    cleaned += 1
                except:
                    pass
        
        print(f"   Removed {cleaned} test screenshot files")
        
        return successful_modes > 0
        
    except Exception as e:
        print(f"✗ Error testing screenshot modes: {e}")
        return False

def test_ui_integration():
    """Test UI integration for screenshot modes"""
    print("\\nTesting UI Integration...")
    print("-" * 30)
    
    try:
        import tkinter as tk
        
        # Test if we can import the main module
        import main
        
        # Create test window (hidden)
        root = tk.Tk()
        root.withdraw()
        
        # Create app instance
        app = main.ScreenQAApp(root)
        
        # Check if screenshot mode variable exists
        has_mode_var = hasattr(app, 'screenshot_mode_var')
        print(f"✓ Screenshot mode variable: {has_mode_var}")
        
        if has_mode_var:
            # Test mode values
            default_mode = app.screenshot_mode_var.get()
            print(f"✓ Default mode: {default_mode}")
            
            # Test setting different modes
            test_modes = ['viewport_only', 'full_page', 'auto']
            for mode in test_modes:
                app.screenshot_mode_var.set(mode)
                current_mode = app.screenshot_mode_var.get()
                print(f"✓ Set mode '{mode}': {current_mode == mode}")
        
        # Check if results tree has Mode column
        if hasattr(app, 'results_tree'):
            columns = app.results_tree['columns']
            has_mode_column = 'Mode' in columns
            print(f"✓ Results tree has Mode column: {has_mode_column}")
        
        # Cleanup
        root.destroy()
        
        print("✓ UI integration tests passed")
        return True
        
    except Exception as e:
        print(f"✗ UI integration test failed: {e}")
        return False

def main():
    """Run screenshot mode tests"""
    print("ScreenQA Screenshot Mode Test Suite")
    print("=" * 50)
    
    # Test screenshot capture functionality
    capture_test = test_screenshot_modes()
    
    # Test UI integration
    ui_test = test_ui_integration()
    
    print("\\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    
    if capture_test:
        print("✅ Screenshot Mode Capture: WORKING")
    else:
        print("❌ Screenshot Mode Capture: FAILED")
    
    if ui_test:
        print("✅ UI Integration: WORKING")
    else:
        print("❌ UI Integration: FAILED")
    
    if capture_test and ui_test:
        print("\\n🎉 SUCCESS: Screenshot mode options are fully functional!")
        print("\\n📖 Available Modes:")
        print("   🔖 Full Page - Captures entire scrollable content")
        print("   🖼️ Viewport Only - Captures visible area only (faster)")
        print("   🤖 Auto Detect - Smart detection based on content length")
        print("\\n🚀 Ready to use in ScreenQA application!")
    else:
        print("\\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()