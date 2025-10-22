#!/usr/bin/env python3
"""
Test script to verify button styling and visibility in ScreenQA
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

def test_button_styles():
    """Test button visibility with different styling approaches"""
    
    print("🔍 Testing Button Visibility...")
    
    # Create test window
    root = tk.Tk()
    root.title("Button Styling Test")
    root.geometry("600x400")
    
    # Apply the same styling as main app
    style = ttk.Style()
    
    # Configure custom styles (same as main.py)
    style.configure("Accent.TButton", 
                   foreground="white", 
                   background="#0078d4",
                   focuscolor="none")
    style.map("Accent.TButton",
             background=[('active', '#106ebe'), ('pressed', '#005a9e')],
             foreground=[('active', 'white'), ('pressed', 'white')])
    
    # Ensure default button text is visible
    style.configure("TButton", foreground="black", background="lightgray")
    style.map("TButton",
             background=[('active', '#e1e1e1'), ('pressed', '#d6d6d6')],
             foreground=[('active', 'black'), ('pressed', 'black')])
    
    # Create test frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Test label
    ttk.Label(main_frame, text="Button Visibility Test", 
             font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    # Test buttons with different styles
    buttons_data = [
        ("Default Button", "TButton", lambda: print("✅ Default button clicked")),
        ("Accent Button", "Accent.TButton", lambda: print("✅ Accent button clicked")),
        ("Capture Screenshots", "Accent.TButton", lambda: print("✅ Capture button clicked")),
    ]
    
    for i, (text, style_name, command) in enumerate(buttons_data, 1):
        btn = ttk.Button(main_frame, text=text, style=style_name, command=command)
        btn.grid(row=i, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))
        main_frame.columnconfigure(0, weight=1)
        
        # Add status label for each button
        status_label = ttk.Label(main_frame, text=f"Style: {style_name}", 
                               foreground="gray", font=('Arial', 8))
        status_label.grid(row=i, column=1, padx=(10, 0), sticky=(tk.W,))
    
    # Instructions
    ttk.Label(main_frame, text="Click buttons to test visibility and functionality", 
             foreground="blue").grid(row=len(buttons_data)+2, column=0, columnspan=3, pady=(20, 0))
    
    # Close button
    ttk.Button(main_frame, text="✅ Tests Pass - Close", 
              command=root.destroy).grid(row=len(buttons_data)+3, column=0, columnspan=3, pady=10)
    
    print("✅ Button test window created")
    print("📝 Check that all button text is clearly visible")
    print("🎯 'Capture Screenshots' should have white text on blue background")
    print("🎯 Other buttons should have black text on gray background")
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Button Visibility Test...")
    try:
        success = test_button_styles()
        print("✅ Button styling test completed successfully!")
    except Exception as e:
        print(f"❌ Button test failed: {e}")
        sys.exit(1)