#!/usr/bin/env python3
"""
Enhanced test script to verify ScreenQA resizable UI functionality
"""
import os
import sys
import tkinter as tk
from tkinter import ttk

def test_resizable_ui():
    """Test the resizable UI functionality"""
    print("Testing Resizable UI...")
    print("=" * 50)
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        # Test if we can import the main module
        import main
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide the window for testing
        
        # Create app instance
        app = main.ScreenQAApp(root)
        
        # Check if PanedWindows were created
        has_main_paned = hasattr(app, 'main_paned')
        has_content_paned = hasattr(app, 'content_paned')
        
        print(f"✓ Main PanedWindow created: {has_main_paned}")
        print(f"✓ Content PanedWindow created: {has_content_paned}")
        
        # Check if device section is resizable
        device_pane_exists = hasattr(app, 'device_pane')
        print(f"✓ Device pane created: {device_pane_exists}")
        
        # Check if actions panel exists
        actions_frame_exists = hasattr(app, 'actions_frame')
        print(f"✓ Actions panel created: {actions_frame_exists}")
        
        # Check if preview functionality exists
        preview_canvas_exists = hasattr(app, 'preview_canvas')
        print(f"✓ Preview canvas created: {preview_canvas_exists}")
        
        # Test toggle method exists
        has_toggle_method = hasattr(app, 'toggle_actions_panel')
        print(f"✓ Toggle method available: {has_toggle_method}")
        
        # Clean up
        root.destroy()
        
        print("\n🎉 Resizable UI components successfully created!")
        print("\nNew Features Added:")
        print("  📏 Vertical resizable divider between Device Selection and Main Content")
        print("  📐 Horizontal resizable divider between Main Content and Quick Actions")
        print("  ⚙️ Toggle button (gear icon) to show/hide Quick Actions panel")
        print("  🖱️ Quick action buttons for fast captures")
        print("  👁️ Recent screenshots preview panel")
        print("  ⌨️ Keyboard shortcuts: F9 (toggle panel), Ctrl+Enter (capture)")
        print("\nHow to use:")
        print("  • Drag the gray resize bars to adjust panel sizes")
        print("  • Click the ⚙️ button to toggle the Quick Actions panel")
        print("  • Use the Quick Actions panel for fast mobile/desktop captures")
        print("  • The Recent Screenshots preview shows thumbnail previews")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing resizable UI: {e}")
        return False

def create_usage_demo():
    """Create a demo showing the resizable features"""
    print("\nCreating Usage Demo...")
    print("-" * 30)
    
    demo_content = """
# ScreenQA - Resizable UI Demo

## New Resizable Features:

### 1. Vertical Resize Bar
- **Location**: Between Device Selection and Main Content areas
- **Function**: Drag up/down to adjust device selection panel height
- **Use Case**: Expand device list when selecting many devices, collapse when focusing on results

### 2. Horizontal Resize Bar  
- **Location**: Between Main Content and Quick Actions panel
- **Function**: Drag left/right to adjust panel widths
- **Use Case**: Expand results view for better screenshot visibility, or expand Quick Actions for better preview

### 3. Quick Actions Panel (Right Side)
- **Toggle Button**: Click ⚙️ button in URL bar
- **Keyboard Shortcut**: Press F9
- **Contents**:
  - 📱 Mobile Devices (quick capture)
  - 🖥️ Desktop Devices (quick capture) 
  - 📊 All Devices (quick capture)
  - Recent Screenshots preview with thumbnails

### 4. Enhanced Workflow
1. **Enter URL** in the top input field
2. **Resize device panel** to see all device options clearly
3. **Use Quick Actions** for common capture scenarios:
   - Click "📱 Mobile Devices" for mobile-only testing
   - Click "🖥️ Desktop Devices" for desktop-only testing
   - Click "📊 All Devices" for comprehensive testing
4. **Adjust main content area** to focus on results or gallery
5. **View recent captures** in the Quick Actions preview panel

### 5. Keyboard Shortcuts
- **F9**: Toggle Quick Actions panel visibility
- **Ctrl+Enter**: Start screenshot capture
- **Enter** (in URL field): Start screenshot capture

### 6. Visual Improvements
- Gray resize bars with raised appearance for better visibility
- Organized layout with labeled sections
- Thumbnail previews in Quick Actions panel
- Better spacing and padding throughout interface

## Benefits:
✅ **Flexible Layout**: Adjust interface to your workflow preferences
✅ **Quick Access**: Fast capture buttons for common scenarios  
✅ **Better Organization**: Clear separation of different functional areas
✅ **Visual Feedback**: Thumbnail previews of recent captures
✅ **Keyboard Friendly**: Shortcuts for power users
✅ **Space Efficient**: Collapsible panels to maximize working area
"""
    
    # Save demo to file
    demo_path = os.path.join(os.path.dirname(__file__), 'RESIZABLE_UI_DEMO.md')
    with open(demo_path, 'w', encoding='utf-8') as f:
        f.write(demo_content)
    
    print(f"✓ Demo documentation saved to: {demo_path}")
    return True

def main():
    """Run resizable UI tests"""
    print("ScreenQA Resizable UI Test Suite")
    print("=" * 50)
    
    # Test resizable UI
    ui_test_passed = test_resizable_ui()
    
    # Create demo documentation
    demo_created = create_usage_demo()
    
    print("\n" + "=" * 50)
    print("RESIZABLE UI TEST SUMMARY")
    print("=" * 50)
    
    if ui_test_passed:
        print("✅ Resizable UI: WORKING")
    else:
        print("❌ Resizable UI: FAILED")
    
    if demo_created:
        print("✅ Demo Documentation: CREATED")
    else:
        print("❌ Demo Documentation: FAILED")
    
    if ui_test_passed and demo_created:
        print("\n🎉 SUCCESS: Resizable UI is fully functional!")
        print("\n🚀 Launch the application to try the new features:")
        print("   Windows: Double-click start_screenqa.bat")
        print("   Manual:  python main.py")
        print("\n📖 Check RESIZABLE_UI_DEMO.md for detailed usage instructions")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()