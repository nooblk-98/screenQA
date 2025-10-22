"""
Additional styling and improvements for ScreenQA resizable UI
"""
import tkinter as tk
from tkinter import ttk

def configure_modern_style(root):
    """Configure modern styling for the application"""
    style = ttk.Style()
    
    # Configure modern button styles
    style.configure("Accent.TButton", 
                   foreground="white",
                   background="#0078d4",
                   focuscolor="none")
    
    style.map("Accent.TButton",
              background=[('active', '#106ebe'),
                         ('pressed', '#005a9e')])
    
    # Configure frame styles
    style.configure("Card.TFrame",
                   background="white",
                   relief="solid",
                   borderwidth=1)
    
    # Configure label styles
    style.configure("Heading.TLabel",
                   font=('Segoe UI', 12, 'bold'),
                   background="white")
    
    style.configure("Subheading.TLabel",
                   font=('Segoe UI', 9),
                   foreground="#666666",
                   background="white")

def add_resize_handle_styling(paned_window):
    """Add visual styling to make resize handles more obvious"""
    try:
        # Configure paned window appearance
        paned_window.configure(
            sashwidth=10,
            sashrelief=tk.RAISED,
            sashpad=3,
            bg='#e1e1e1',
            relief=tk.FLAT,
            borderwidth=1
        )
        
        # Add hover effects (if supported)
        def on_sash_enter(event):
            paned_window.configure(bg='#d4d4d4')
            
        def on_sash_leave(event):
            paned_window.configure(bg='#e1e1e1')
        
        paned_window.bind('<Enter>', on_sash_enter)
        paned_window.bind('<Leave>', on_sash_leave)
        
    except Exception as e:
        print(f"Could not apply advanced styling: {e}")

def add_panel_indicators(parent_frame, panel_name):
    """Add visual indicators to panels to show they are resizable"""
    indicator_frame = ttk.Frame(parent_frame, style="Card.TFrame")
    indicator_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
    
    # Panel name label
    name_label = ttk.Label(indicator_frame, text=panel_name, 
                          style="Heading.TLabel")
    name_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    # Resize hint
    hint_label = ttk.Label(indicator_frame, text="⇅ Resizable", 
                          style="Subheading.TLabel")
    hint_label.pack(side=tk.RIGHT, padx=5, pady=2)

# Create an enhanced status message for the application
ENHANCED_FEATURES_MESSAGE = """
🎉 ScreenQA Enhanced with Resizable UI!

✨ NEW FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📏 VERTICAL RESIZE BAR
   • Location: Between Device Selection and Main Content
   • Drag up/down to adjust device list height
   • Perfect for when you need more space for device selection

📐 HORIZONTAL RESIZE BAR  
   • Location: Between Main Content and Quick Actions panel
   • Drag left/right to balance screenshot viewing and controls
   • Ideal for focusing on results or accessing quick tools

⚙️ QUICK ACTIONS PANEL
   • Toggle with gear button (⚙️) or press F9
   • Fast capture buttons: Mobile Only, Desktop Only, All Devices
   • Recent screenshots preview with clickable thumbnails
   • Collapsible to maximize screenshot viewing area

⌨️ KEYBOARD SHORTCUTS
   • F9: Toggle Quick Actions panel
   • Ctrl+Enter: Start screenshot capture
   • Enter (in URL field): Start capture

🎯 IMPROVED WORKFLOW:
   1. Enter website URL
   2. Resize panels to your preference
   3. Use Quick Actions for common scenarios
   4. View results in optimized layout
   5. Toggle panels as needed for focus

💡 PRO TIPS:
   • Collapse Quick Actions when viewing large screenshot galleries
   • Expand device panel when selecting many specific devices
   • Use quick capture buttons for rapid testing workflows
   • Resize based on your monitor size and preferences
   • Preview panel shows recent work for quick access

Ready to use! Launch ScreenQA and drag the gray resize bars to customize your layout.
"""