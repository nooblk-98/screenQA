#!/usr/bin/env python3
"""
Simple test to verify button text visibility fix
"""

import tkinter as tk
from tkinter import ttk

def test_button_visibility():
    """Quick test for button text visibility"""
    
    root = tk.Tk()
    root.title("Button Text Visibility Test")
    root.geometry("400x200")
    
    # Apply the same styling as the fixed main.py
    style = ttk.Style()
    
    # Use a compatible theme
    try:
        style.theme_use('clam')
    except:
        pass
    
    # Configure button styles for better visibility
    style.configure("TButton", 
                   foreground="black",
                   background="#f0f0f0",
                   relief="raised",
                   borderwidth=1)
    
    style.map("TButton",
             foreground=[('active', 'black'), ('pressed', 'black')],
             background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')])
    
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    ttk.Label(frame, text="Button Text Visibility Test", 
             font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=(0, 15))
    
    # Test the exact same button as in the main app
    capture_btn = ttk.Button(frame, text="Capture Screenshots", 
                           command=lambda: print("✅ Capture button is visible and clickable!"))
    capture_btn.grid(row=1, column=0, pady=5)
    
    validate_btn = ttk.Button(frame, text="Validate", 
                            command=lambda: print("✅ Validate button is visible and clickable!"))
    validate_btn.grid(row=2, column=0, pady=5)
    
    ttk.Label(frame, text="Both buttons should have BLACK text that is clearly visible", 
             foreground="blue").grid(row=3, column=0, pady=(15, 0))
    
    close_btn = ttk.Button(frame, text="Close Test", command=root.destroy)
    close_btn.grid(row=4, column=0, pady=(10, 0))
    
    print("🔍 Button visibility test window opened")
    print("📝 Check that all button text is BLACK and clearly readable")
    
    root.mainloop()

if __name__ == "__main__":
    test_button_visibility()