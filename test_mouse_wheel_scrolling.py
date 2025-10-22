#!/usr/bin/env python3
"""
Test mouse wheel scrolling functionality in device selection area
"""

import tkinter as tk
from tkinter import ttk
import sys

def test_mouse_wheel_scrolling():
    """Test that mouse wheel scrolling works everywhere in the device area"""
    
    print("🖱️  Testing Mouse Wheel Scrolling...")
    
    root = tk.Tk()
    root.title("Mouse Wheel Scrolling Test")
    root.geometry("600x500")
    
    # Apply same styling as main app
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass
    
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    
    # Instructions
    title_label = ttk.Label(main_frame, text="Mouse Wheel Scrolling Test", 
                           font=('Arial', 14, 'bold'))
    title_label.grid(row=0, column=0, pady=(0, 10))
    
    instructions = ttk.Label(main_frame, 
                           text="🖱️  Test scrolling by moving mouse wheel over different areas:\n" +
                                "• Over the device list background\n" +
                                "• Over individual device checkboxes\n" +
                                "• Over the scrollable area\n" +
                                "• Anywhere in the device selection frame",
                           justify=tk.LEFT, foreground="blue")
    instructions.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W,))
    
    # Create device selection area (same as main app)
    device_frame = ttk.LabelFrame(main_frame, text="Device Selection - Scroll Test", padding="5")
    device_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
    device_frame.columnconfigure(0, weight=1)
    device_frame.rowconfigure(1, weight=1)
    
    # Buttons
    btn_frame = ttk.Frame(device_frame)
    btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
    
    ttk.Label(btn_frame, text="Try scrolling over any part of the device list below:", 
             foreground="green").grid(row=0, column=0)
    
    # Device list container
    devices_container = ttk.Frame(device_frame)
    devices_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    devices_container.columnconfigure(0, weight=1)
    devices_container.rowconfigure(0, weight=1)
    
    # Scrollable canvas (same setup as main app)
    canvas = tk.Canvas(devices_container, height=200)
    scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
    devices_list_frame = ttk.Frame(canvas)
    
    # Cross-platform mouse wheel function
    def on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            canvas.yview_scroll(-1, "units")  
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
    
    # Bind to all components for comprehensive scrolling
    canvas.bind("<MouseWheel>", on_mousewheel)
    devices_list_frame.bind("<MouseWheel>", on_mousewheel)
    devices_container.bind("<MouseWheel>", on_mousewheel)
    device_frame.bind("<MouseWheel>", on_mousewheel)
    
    # Linux support
    for widget in [canvas, devices_list_frame, devices_container, device_frame]:
        widget.bind("<Button-4>", on_mousewheel)
        widget.bind("<Button-5>", on_mousewheel)
    
    # Add many test devices to demonstrate scrolling
    test_devices = [
        "Desktop Windows (1920x1080)",
        "Desktop Mac (1440x900)",
        "MacBook Pro 13\" (1280x800)", 
        "MacBook Pro 16\" (1512x982)",
        "iPhone 15 Pro Max (430x932)",
        "iPhone 15 (393x852)",
        "iPhone SE (375x667)",
        "iPad Pro 12.9\" (1024x1366)",
        "iPad Air (820x1180)",
        "Samsung Galaxy S23 (360x800)",
        "Samsung Galaxy Tab (768x1024)",
        "Google Pixel 7 (412x915)",
        "OnePlus 11 (384x854)",
        "Surface Pro (912x1368)",
        "Surface Laptop (1536x1024)",
        "Chrome Desktop (1366x768)",
        "Firefox Desktop (1600x900)",
        "Safari Desktop (1440x900)",
        "Edge Desktop (1920x1200)",
        "Test Device 1 (800x600)",
        "Test Device 2 (1024x768)", 
        "Test Device 3 (1280x1024)"
    ]
    
    # Create checkboxes with mouse wheel binding
    for i, device in enumerate(test_devices):
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(devices_list_frame, text=device, variable=var)
        checkbox.grid(row=i, column=0, sticky=(tk.W,), padx=10, pady=2)
        
        # Bind each checkbox to mouse wheel
        checkbox.bind("<MouseWheel>", on_mousewheel)
        checkbox.bind("<Button-4>", on_mousewheel)
        checkbox.bind("<Button-5>", on_mousewheel)
    
    devices_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=devices_list_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    # Status and close
    status_frame = ttk.Frame(main_frame)
    status_frame.grid(row=3, column=0, pady=(10, 0))
    
    ttk.Label(status_frame, text="✅ Mouse wheel should work everywhere in the device area above", 
             foreground="green", font=('Arial', 10, 'bold')).grid(row=0, column=0)
    
    ttk.Button(status_frame, text="Close Test", 
              command=root.destroy).grid(row=1, column=0, pady=(10, 0))
    
    print("✅ Mouse wheel scrolling test window created")
    print("🖱️  Move mouse over different parts of the device list and use mouse wheel")
    print("📝 Scrolling should work smoothly everywhere, not just on the scrollbar")
    
    root.mainloop()
    return True

if __name__ == "__main__":
    print("🚀 Starting Mouse Wheel Scrolling Test...")
    try:
        success = test_mouse_wheel_scrolling()
        print("✅ Mouse wheel scrolling test completed!")
    except Exception as e:
        print(f"❌ Mouse wheel test failed: {e}")
        sys.exit(1)