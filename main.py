import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import os
import sys
from PIL import Image, ImageTk
import webbrowser
import subprocess
from datetime import datetime
import json
import threading

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from screenshot_capture import ScreenshotCapture, AsyncScreenshotCapture


class ScreenQAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScreenQA - Website Screenshot Testing Tool")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialize capture engines
        self.capture = ScreenshotCapture()
        self.async_capture = AsyncScreenshotCapture()
        
        # Variables
        self.url_var = tk.StringVar()
        self.selected_devices = []
        self.current_results = {}
        self.device_vars = {}  # Initialize device variables dictionary
        self.screenshot_mode_var = tk.StringVar(value="full_page")  # Screenshot mode selection
        self.result_data = {}  # Store result data for tree items
        
        # Setup UI
        self.setup_ui()
        self.load_devices()
        
        # Bind keyboard shortcuts
        self.root.bind('<F9>', lambda e: self.toggle_actions_panel())
        self.root.bind('<Control-Return>', lambda e: self.start_capture())
        self.root.bind('<Control-l>', lambda e: self.clear_log())
        self.root.bind('<Control-L>', lambda e: self.clear_log())
        self.root.bind('<Control-s>', lambda e: self.save_log())
        self.root.bind('<Control-S>', lambda e: self.save_log())
        
    def setup_ui(self):
        """Setup the modern user interface with improved layout and UX"""
        # Configure root
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)  # Changed to 1 to accommodate menu
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Set modern style
        self.setup_modern_style()
        
        # Main container with better padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))  # Changed to row 1
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header section with URL and controls
        header_frame = ttk.Frame(main_container, style='Header.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        self.setup_header_section(header_frame)
        
        # Main content area with horizontal layout
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(1, weight=2)  # Give more space to results
        content_frame.columnconfigure(2, weight=1)  # Less space for sidebar
        content_frame.rowconfigure(0, weight=1)
        
        # Left sidebar - Device Selection (compact)
        device_frame = ttk.LabelFrame(content_frame, text="🖥️ Device Selection", padding="10")
        device_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        device_frame.columnconfigure(0, weight=1)
        device_frame.rowconfigure(1, weight=1)
        self.setup_device_section_compact(device_frame)
        
        # Center - Main results area
        results_frame = ttk.Frame(content_frame)
        results_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        self.setup_results_section(results_frame)
        
        # Right sidebar - Quick actions and info
        self.sidebar_frame = ttk.Frame(content_frame)
        self.sidebar_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.sidebar_frame.columnconfigure(0, weight=1)
        self.setup_sidebar(self.sidebar_frame)
        
        # Bottom status bar
        status_frame = ttk.Frame(main_container, style='Status.TFrame')
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        self.setup_status_bar_modern(status_frame)
    
    def setup_url_section(self, parent, row):
        """Setup URL input section"""
        url_frame = ttk.LabelFrame(parent, text="Website URL", padding="5")
        url_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, padx=(0, 5))
        
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 10))
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        url_entry.bind('<Return>', lambda e: self.start_capture())
        
        validate_btn = ttk.Button(url_frame, text="Validate", command=self.validate_url)
        validate_btn.grid(row=0, column=2, padx=(0, 5))
        
        self.capture_btn = ttk.Button(url_frame, text="Capture Screenshots", 
                                     command=self.start_capture)
        self.capture_btn.grid(row=0, column=3, padx=(0, 5))
        
        # Toggle panel button
        toggle_btn = ttk.Button(url_frame, text="⚙️", width=3,
                               command=self.toggle_actions_panel)
        toggle_btn.grid(row=0, column=4)
        
        # Quick URL presets
        presets_frame = ttk.Frame(url_frame)
        presets_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(presets_frame, text="Quick URLs:").grid(row=0, column=0, padx=(0, 5))
        
        preset_urls = ["google.com", "github.com", "stackoverflow.com", "responsive-design-test.com"]
        for i, url in enumerate(preset_urls):
            btn = ttk.Button(presets_frame, text=url, width=20,
                           command=lambda u=url: self.url_var.set(u))
            btn.grid(row=0, column=i+1, padx=2)
        
        # Screenshot mode selection
        mode_frame = ttk.Frame(url_frame)
        mode_frame.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(mode_frame, text="Screenshot Mode:").grid(row=0, column=0, padx=(0, 10))
        
        self.screenshot_mode_var = tk.StringVar(value="full_page")
        
        # Radio buttons for screenshot mode
        modes = [
            ("full_page", "🔖 Full Page", "Capture entire page content (scrollable)"),
            ("viewport_only", "🖼️ Viewport Only", "Capture visible area only (faster)"),
            ("auto", "🤖 Auto Detect", "Smart detection based on content length")
        ]
        
        for i, (value, text, tooltip) in enumerate(modes):
            radio = ttk.Radiobutton(mode_frame, text=text, variable=self.screenshot_mode_var, 
                                  value=value)
            radio.grid(row=0, column=i+1, padx=(0, 15), sticky=(tk.W,))
            
            # Add tooltip-like label (smaller text with description)
            desc_label = ttk.Label(mode_frame, text=tooltip, font=('Arial', 8), 
                                 foreground='gray')
            desc_label.grid(row=1, column=i+1, padx=(0, 15), sticky=(tk.W,))
    
    def setup_device_section(self, parent, row):
        """Setup device selection section"""
        device_frame = ttk.LabelFrame(parent, text="Device Selection", padding="5")
        device_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        device_frame.columnconfigure(0, weight=1)
        
        # Device selection buttons
        btn_frame = ttk.Frame(device_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(btn_frame, text="Select All", command=self.select_all_devices).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all_devices).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(btn_frame, text="Mobile Only", command=self.select_mobile_devices).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(btn_frame, text="Desktop Only", command=self.select_desktop_devices).grid(row=0, column=3, padx=(0, 5))
        
        # Device list with checkboxes
        devices_container = ttk.Frame(device_frame)
        devices_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        devices_container.columnconfigure(0, weight=1)
        
        # Scrollable frame for devices
        canvas = tk.Canvas(devices_container, height=120)
        scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
        self.devices_frame = ttk.Frame(canvas)
        
        self.devices_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.devices_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        devices_container.rowconfigure(0, weight=1)
        
        self.device_vars = {}
    
    def setup_device_section_resizable(self, parent):
        """Setup resizable device selection section"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Device selection frame
        device_frame = ttk.LabelFrame(parent, text="Device Selection", padding="5")
        device_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        device_frame.columnconfigure(0, weight=1)
        device_frame.rowconfigure(1, weight=1)
        
        # Device selection buttons
        btn_frame = ttk.Frame(device_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(btn_frame, text="Select All", command=self.select_all_devices).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all_devices).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(btn_frame, text="Mobile Only", command=self.select_mobile_devices).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(btn_frame, text="Desktop Only", command=self.select_desktop_devices).grid(row=0, column=3, padx=(0, 5))
        
        # Device list with checkboxes (scrollable)
        devices_container = ttk.Frame(device_frame)
        devices_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        devices_container.columnconfigure(0, weight=1)
        devices_container.rowconfigure(0, weight=1)
        
        # Scrollable canvas for devices
        canvas = tk.Canvas(devices_container, height=150)
        scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
        self.devices_frame = ttk.Frame(canvas)
        
        self.devices_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.devices_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mouse wheel scrolling support (cross-platform)
        def on_mousewheel(event):
            # Windows and MacOS
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            # Linux
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
        
        # Bind mouse wheel to canvas and devices frame (Windows/Mac)
        canvas.bind("<MouseWheel>", on_mousewheel)
        self.devices_frame.bind("<MouseWheel>", on_mousewheel)
        devices_container.bind("<MouseWheel>", on_mousewheel)
        device_frame.bind("<MouseWheel>", on_mousewheel)
        
        # Linux mouse wheel support
        canvas.bind("<Button-4>", on_mousewheel)
        canvas.bind("<Button-5>", on_mousewheel)
        self.devices_frame.bind("<Button-4>", on_mousewheel)
        self.devices_frame.bind("<Button-5>", on_mousewheel)
        devices_container.bind("<Button-4>", on_mousewheel)
        devices_container.bind("<Button-5>", on_mousewheel)
        device_frame.bind("<Button-4>", on_mousewheel)
        device_frame.bind("<Button-5>", on_mousewheel)
        
        # Store canvas reference for later use
        self.device_canvas = canvas
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initialize device variables if not already done
        if not hasattr(self, 'device_vars'):
            self.device_vars = {}
    
    def setup_tabs_resizable(self, parent):
        """Setup resizable tabbed interface"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        notebook = ttk.Notebook(parent)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Progress Tab
        self.progress_frame = ttk.Frame(notebook)
        notebook.add(self.progress_frame, text="Progress & Results")
        self.setup_progress_tab(self.progress_frame)
        
        # Screenshot Gallery Tab
        self.gallery_frame = ttk.Frame(notebook)
        notebook.add(self.gallery_frame, text="Screenshot Gallery")
        self.setup_gallery_tab(self.gallery_frame)
        
        # History Tab
        self.history_frame = ttk.Frame(notebook)
        notebook.add(self.history_frame, text="History")
        self.setup_history_tab(self.history_frame)
        
        # QA Features Tab
        self.qa_frame = ttk.Frame(notebook)
        notebook.add(self.qa_frame, text="QA Tools")
        self.setup_qa_tab(self.qa_frame)
    
    def setup_actions_panel(self, parent):
        """Setup quick actions panel (right side)"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Actions panel
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions", padding="5")
        actions_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        actions_frame.columnconfigure(0, weight=1)
        
        # Quick capture buttons
        ttk.Label(actions_frame, text="Quick Captures:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=(tk.W,), pady=(0, 5))
        
        quick_buttons = [
            ("📱 Mobile Devices", lambda: self.quick_capture_mobile()),
            ("🖥️ Desktop Devices", lambda: self.quick_capture_desktop()),
            ("📊 All Devices", lambda: self.quick_capture_all()),
        ]
        
        for i, (text, command) in enumerate(quick_buttons, 1):
            btn = ttk.Button(actions_frame, text=text, command=command, width=20)
            btn.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Separator
        ttk.Separator(actions_frame, orient='horizontal').grid(row=len(quick_buttons)+1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Recent screenshots preview
        preview_frame = ttk.LabelFrame(actions_frame, text="Recent Screenshots", padding="5")
        preview_frame.grid(row=len(quick_buttons)+2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        
        # Refresh button for previews
        ttk.Button(preview_frame, text="🔄 Refresh", command=self.refresh_preview).grid(row=0, column=0, pady=(0, 5))
        
        # Preview area (scrollable)
        preview_canvas = tk.Canvas(preview_frame, height=200)
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=preview_canvas.yview)
        self.preview_content = ttk.Frame(preview_canvas)
        
        self.preview_content.bind("<Configure>", lambda e: preview_canvas.configure(scrollregion=preview_canvas.bbox("all")))
        
        preview_canvas.create_window((0, 0), window=self.preview_content, anchor="nw")
        preview_canvas.configure(yscrollcommand=preview_scrollbar.set)
        
        preview_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Store references
        self.preview_canvas = preview_canvas
        
        # Initialize with recent screenshots
        self.refresh_preview()
    
    def configure_paned_windows(self):
        """Configure the appearance of paned windows for better visibility"""
        try:
            # Configure main paned window
            self.main_paned.configure(
                relief=tk.RAISED,
                borderwidth=2,
                sashwidth=8,
                sashrelief=tk.RAISED,
                sashpad=2,
                bg='#d0d0d0'
            )
            
            # Configure content paned window  
            self.content_paned.configure(
                relief=tk.RAISED,
                borderwidth=2,
                sashwidth=8,
                sashrelief=tk.RAISED,
                sashpad=2,
                bg='#d0d0d0'
            )
            
            # Set initial sash positions after the window is mapped
            self.root.after(100, self.set_initial_sash_positions)
            
        except Exception as e:
            print(f"Error configuring paned windows: {e}")
    
    def set_initial_sash_positions(self):
        """Set initial positions for the paned window sashes"""
        try:
            # Set device panel height (about 20% of window)
            window_height = self.root.winfo_height()
            device_height = max(180, int(window_height * 0.2))
            self.main_paned.sash_place(0, 0, device_height)
            
            # Set actions panel width (about 25% of window)
            window_width = self.content_paned.winfo_width()
            if window_width > 100:  # Ensure window is properly initialized
                actions_width = int(window_width * 0.75)
                self.content_paned.sash_place(0, actions_width, 0)
                
        except Exception as e:
            print(f"Error setting initial sash positions: {e}")

    def setup_modern_style(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles
        style.configure('Header.TFrame', background='#f8f9fa', relief='solid', borderwidth=1)
        style.configure('Status.TFrame', background='#e9ecef', relief='solid', borderwidth=1)
        style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)
        style.configure('Sidebar.TFrame', background='#f8f9fa')
        
        # Button styles
        style.configure('Primary.TButton', background='#007bff', foreground='white')
        style.configure('Success.TButton', background='#28a745', foreground='white')
        style.configure('Warning.TButton', background='#ffc107', foreground='black')
        style.configure('Danger.TButton', background='#dc3545', foreground='white')
        
        # Label styles
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 10), foreground='#6c757d')
        style.configure('Success.TLabel', foreground='#28a745')
        style.configure('Error.TLabel', foreground='#dc3545')

    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Capture", command=self.start_capture, accelerator="Ctrl+Enter")
        file_menu.add_separator()
        file_menu.add_command(label="Open Screenshots Folder", command=self.open_screenshots_folder)
        file_menu.add_command(label="Export Report", command=self.generate_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Clear Log", command=self.clear_log, accelerator="Ctrl+L")
        tools_menu.add_command(label="Save Log", command=self.save_log, accelerator="Ctrl+S")
        tools_menu.add_separator()
        tools_menu.add_command(label="Refresh Gallery", command=self.refresh_gallery)
        tools_menu.add_command(label="Toggle Sidebar", command=self.toggle_actions_panel, accelerator="F9")
        
        # Device selection submenu
        devices_menu = tk.Menu(tools_menu, tearoff=0)
        tools_menu.add_cascade(label="Device Selection", menu=devices_menu)
        devices_menu.add_command(label="Select All Devices", command=self.select_all_devices)
        devices_menu.add_command(label="Clear All Devices", command=self.clear_all_devices)
        devices_menu.add_separator()
        devices_menu.add_command(label="Mobile Only", command=self.select_mobile_devices)
        devices_menu.add_command(label="Desktop Only", command=self.select_desktop_devices)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About ScreenQA", command=self.show_about_tab)
        help_menu.add_command(label="GitHub Repository", command=lambda: self.open_url("https://github.com/nooblk-98/screenQA"))
        help_menu.add_command(label="Report Issue", command=lambda: self.open_url("https://github.com/nooblk-98/screenQA/issues"))
        help_menu.add_separator()
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)

    def show_about_tab(self):
        """Switch to the About tab"""
        try:
            # Find and select the About tab
            for i in range(self.notebook.index("end")):
                if "About" in self.notebook.tab(i, "text"):
                    self.notebook.select(i)
                    break
            self.log_message("INFO", "ℹ️ Switched to About tab")
        except Exception as e:
            self.log_message("ERROR", f"❌ Failed to switch to About tab: {str(e)}")
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_window = tk.Toplevel(self.root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("400x300")
        shortcuts_window.resizable(False, False)
        
        # Center the window
        shortcuts_window.transient(self.root)
        shortcuts_window.grab_set()
        
        main_frame = ttk.Frame(shortcuts_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="⌨️ Keyboard Shortcuts", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        shortcuts = [
            ("Ctrl + Enter", "Start screenshot capture"),
            ("F9", "Toggle sidebar panel"),
            ("Ctrl + L", "Clear log"),
            ("Ctrl + S", "Save log to file"),
            ("Alt + F4", "Exit application"),
            ("Double-click", "Open screenshot (in results)")
        ]
        
        for shortcut, description in shortcuts:
            shortcut_frame = ttk.Frame(main_frame)
            shortcut_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(shortcut_frame, text=shortcut, font=('Arial', 10, 'bold'), 
                     width=15).pack(side=tk.LEFT)
            ttk.Label(shortcut_frame, text=description, font=('Arial', 10)).pack(side=tk.LEFT, padx=(10, 0))
        
        close_btn = ttk.Button(main_frame, text="Close", 
                              command=shortcuts_window.destroy)
        close_btn.pack(pady=(20, 0))

    def setup_header_section(self, parent):
        """Setup modern header with URL input and main controls"""
        # Title and logo area
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="📸 ScreenQA", style='Title.TLabel', font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=(tk.W,))
        
        subtitle_label = ttk.Label(title_frame, text="Website Screenshot Testing Tool", style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, sticky=(tk.W,))
        
        # URL input section
        url_frame = ttk.LabelFrame(parent, text="🌐 Website URL", padding="15")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        # URL entry with better styling
        ttk.Label(url_frame, text="URL:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=(0, 10), sticky=(tk.W,))
        
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 11), width=50)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        url_entry.bind('<Return>', lambda e: self.start_capture())
        
        # Control buttons with modern styling
        button_frame = ttk.Frame(url_frame)
        button_frame.grid(row=0, column=2)
        
        validate_btn = ttk.Button(button_frame, text="✓ Validate", command=self.validate_url, style='Warning.TButton')
        validate_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.capture_btn = ttk.Button(button_frame, text="📸 Capture Screenshots", 
                                     command=self.start_capture, style='Primary.TButton')
        self.capture_btn.grid(row=0, column=1, padx=(0, 5))
        
        settings_btn = ttk.Button(button_frame, text="⚙️", width=3, command=self.toggle_actions_panel)
        settings_btn.grid(row=0, column=2)
        
        # Quick URL presets
        presets_frame = ttk.Frame(url_frame)
        presets_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W,), pady=(10, 0))
        
        ttk.Label(presets_frame, text="Quick URLs:", font=('Arial', 9)).grid(row=0, column=0, padx=(0, 10))
        
        quick_urls = ["google.com", "github.com", "stackoverflow.com", "responsive-design-test"]
        for i, url in enumerate(quick_urls):
            btn = ttk.Button(presets_frame, text=url, width=15,
                           command=lambda u=url: self.url_var.set(f"https://{u}" if not u.startswith("http") else u))
            btn.grid(row=0, column=i+1, padx=(0, 5))

    def setup_device_section_compact(self, parent):
        """Setup compact device selection with better organization"""
        # Device selection controls
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        controls_frame.columnconfigure(0, weight=1)
        
        # Selection buttons in a more compact layout
        btn_frame1 = ttk.Frame(controls_frame)
        btn_frame1.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame1, text="Select All", command=self.select_all_devices).grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        ttk.Button(btn_frame1, text="Clear All", command=self.clear_all_devices).grid(row=0, column=1, padx=(0, 5), sticky=(tk.W, tk.E))
        
        btn_frame2 = ttk.Frame(controls_frame)
        btn_frame2.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(btn_frame2, text="📱 Mobile", command=self.select_mobile_devices).grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        ttk.Button(btn_frame2, text="🖥️ Desktop", command=self.select_desktop_devices).grid(row=0, column=1, padx=(0, 5), sticky=(tk.W, tk.E))
        
        # Configure button columns
        for frame in [btn_frame1, btn_frame2]:
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
        
        # Device list with improved scrolling
        devices_container = ttk.Frame(parent)
        devices_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        devices_container.columnconfigure(0, weight=1)
        devices_container.rowconfigure(0, weight=1)
        
        # Scrollable canvas for devices
        canvas = tk.Canvas(devices_container, height=200, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
        self.devices_frame = ttk.Frame(canvas)
        
        self.devices_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.devices_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
        
        for widget in [canvas, self.devices_frame, devices_container, parent]:
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
        
        self.device_canvas = canvas
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def setup_results_section(self, parent):
        """Setup the main results area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress & Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="📊 Progress & Results")
        self.setup_progress_tab(self.results_frame)
        
        # Screenshot Gallery tab
        self.gallery_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.gallery_frame, text="🖼️ Screenshot Gallery")
        self.setup_gallery_tab(self.gallery_frame)
        
        # History tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📋 History")
        self.setup_history_tab(self.history_frame)
        
        # QA Tools tab
        self.qa_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.qa_frame, text="🔧 QA Tools")
        self.setup_qa_tab(self.qa_frame)
        
        # About tab
        self.about_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.about_frame, text="ℹ️ About")
        self.setup_about_tab(self.about_frame)

    def setup_sidebar(self, parent):
        """Setup the right sidebar with quick actions and info"""
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=0)
        parent.rowconfigure(2, weight=1)
        
        # Quick Captures section
        quick_frame = ttk.LabelFrame(parent, text="⚡ Quick Captures", padding="10")
        quick_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        quick_frame.columnconfigure(0, weight=1)
        
        ttk.Button(quick_frame, text="📱 Mobile Devices", 
                  command=lambda: self.quick_capture_mobile(), 
                  style='Success.TButton').grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(quick_frame, text="🖥️ Desktop Devices", 
                  command=lambda: self.quick_capture_desktop(), 
                  style='Success.TButton').grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(quick_frame, text="🌐 All Devices", 
                  command=lambda: self.quick_capture_all(), 
                  style='Primary.TButton').grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Settings section
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Settings", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(0, weight=1)
        
        # Screenshot mode
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(mode_frame, text="Screenshot Mode:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=(tk.W,))
        
        mode_radio_frame = ttk.Frame(mode_frame)
        mode_radio_frame.grid(row=1, column=0, sticky=(tk.W,), pady=(5, 0))
        
        ttk.Radiobutton(mode_radio_frame, text="📄 Full Page", variable=self.screenshot_mode_var, 
                       value="full_page").grid(row=0, column=0, sticky=(tk.W,))
        ttk.Radiobutton(mode_radio_frame, text="👁️ Viewport", variable=self.screenshot_mode_var, 
                       value="viewport").grid(row=1, column=0, sticky=(tk.W,))
        ttk.Radiobutton(mode_radio_frame, text="🤖 Auto Detect", variable=self.screenshot_mode_var, 
                       value="auto").grid(row=2, column=0, sticky=(tk.W,))
        
        # Recent Screenshots section
        recent_frame = ttk.LabelFrame(parent, text="📁 Recent Screenshots", padding="10")
        recent_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        recent_frame.columnconfigure(0, weight=1)
        recent_frame.rowconfigure(1, weight=1)
        
        refresh_btn = ttk.Button(recent_frame, text="🔄 Refresh", command=self.refresh_recent_screenshots)
        refresh_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scrollable list for recent screenshots
        recent_list_frame = ttk.Frame(recent_frame)
        recent_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        recent_list_frame.columnconfigure(0, weight=1)
        recent_list_frame.rowconfigure(0, weight=1)
        
        self.recent_listbox = tk.Listbox(recent_list_frame, height=8, font=('Arial', 9))
        recent_scrollbar = ttk.Scrollbar(recent_list_frame, orient="vertical", command=self.recent_listbox.yview)
        self.recent_listbox.configure(yscrollcommand=recent_scrollbar.set)
        
        self.recent_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        recent_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.recent_listbox.insert(0, "No screenshots yet")

    def setup_status_bar_modern(self, parent):
        """Setup modern status bar with better information display"""
        # Status indicator
        status_icon = ttk.Label(parent, text="●", foreground="#28a745", font=('Arial', 12))
        status_icon.grid(row=0, column=0, padx=(10, 5))
        
        # Status text
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(parent, textvariable=self.status_var, font=('Arial', 10))
        status_label.grid(row=0, column=1, sticky=(tk.W,), padx=(0, 20))
        
        # Device count with icon
        device_icon = ttk.Label(parent, text="🖥️", font=('Arial', 10))
        device_icon.grid(row=0, column=2, padx=(20, 5))
        
        self.device_count_var = tk.StringVar(value="0 devices selected")
        device_count_label = ttk.Label(parent, textvariable=self.device_count_var, font=('Arial', 10))
        device_count_label.grid(row=0, column=3, sticky=(tk.W,), padx=(0, 20))
        
        # Progress indicator (when capturing)
        self.progress_var = tk.StringVar(value="")
        progress_label = ttk.Label(parent, textvariable=self.progress_var, font=('Arial', 10), style='Success.TLabel')
        progress_label.grid(row=0, column=4, sticky=(tk.E,), padx=(0, 10))

    # Quick capture methods
    def quick_capture_mobile(self):
        """Quick capture for mobile devices"""
        self.select_mobile_devices()
        if self.url_var.get().strip():
            self.start_capture()
        else:
            messagebox.showwarning("No URL", "Please enter a URL first")
    
    def quick_capture_desktop(self):
        """Quick capture for desktop devices"""
        self.select_desktop_devices()
        if self.url_var.get().strip():
            self.start_capture()
        else:
            messagebox.showwarning("No URL", "Please enter a URL first")
    
    def quick_capture_all(self):
        """Quick capture for all devices"""
        self.select_all_devices()
        if self.url_var.get().strip():
            self.start_capture()
        else:
            messagebox.showwarning("No URL", "Please enter a URL first")
    
    def refresh_recent_screenshots(self):
        """Refresh the recent screenshots list"""
        # This will be implemented to show actual recent files
        self.recent_listbox.delete(0, tk.END)
        try:
            # Look for recent screenshot files
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            if os.path.exists(screenshots_dir):
                files = sorted([f for f in os.listdir(screenshots_dir) if f.endswith(('.png', '.jpg'))], 
                             key=lambda x: os.path.getmtime(os.path.join(screenshots_dir, x)), reverse=True)[:10]
                for file in files:
                    self.recent_listbox.insert(tk.END, file)
            else:
                self.recent_listbox.insert(0, "No screenshots directory found")
        except Exception as e:
            self.recent_listbox.insert(0, f"Error: {str(e)}")

    def toggle_actions_panel(self):
        """Toggle the sidebar visibility"""
        # This can be implemented to hide/show the sidebar
        pass

    def log_message(self, level, message):
        """Add a timestamped message to the log with appropriate formatting"""
        if not hasattr(self, 'log_text'):
            return
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Level icons
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DEBUG": "🔍"
        }
        
        icon = icons.get(level, "📝")
        formatted_message = f"[{timestamp}] {icon} {message}\n"
        
        # Insert the message with appropriate tag
        self.log_text.insert(tk.END, formatted_message, level)
        
        # Auto-scroll if enabled
        if hasattr(self, 'auto_scroll_var') and self.auto_scroll_var.get():
            self.log_text.see(tk.END)
        
        # Update the UI immediately
        self.root.update_idletasks()

    def clear_log(self):
        """Clear the log text area"""
        if hasattr(self, 'log_text'):
            self.log_text.delete(1.0, tk.END)
            self.log_message("INFO", "🧹 Log cleared")

    def save_log(self):
        """Save the current log to a file"""
        if not hasattr(self, 'log_text'):
            return
            
        try:
            from tkinter import filedialog
            from datetime import datetime
            
            # Default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"screenqa_log_{timestamp}.txt"
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialvalue=default_filename
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message("SUCCESS", f"💾 Log saved to: {filename}")
        except Exception as e:
            self.log_message("ERROR", f"Failed to save log: {str(e)}")

    def update_progress_status(self, message, progress_type="INFO"):
        """Update both progress label and log with a message"""
        self.progress_var.set(message)
        self.log_message(progress_type, message)
    
    def setup_tabs(self, parent, row):
        """Setup tabbed interface for different views"""
        notebook = ttk.Notebook(parent)
        notebook.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Progress Tab
        self.progress_frame = ttk.Frame(notebook)
        notebook.add(self.progress_frame, text="Progress & Results")
        self.setup_progress_tab(self.progress_frame)
        
        # Screenshot Gallery Tab
        self.gallery_frame = ttk.Frame(notebook)
        notebook.add(self.gallery_frame, text="Screenshot Gallery")
        self.setup_gallery_tab(self.gallery_frame)
        
        # History Tab
        self.history_frame = ttk.Frame(notebook)
        notebook.add(self.history_frame, text="History")
        self.setup_history_tab(self.history_frame)
        
        # QA Features Tab
        self.qa_frame = ttk.Frame(notebook)
        notebook.add(self.qa_frame, text="QA Tools")
        self.setup_qa_tab(self.qa_frame)
    
    def setup_progress_tab(self, parent):
        """Setup progress and results tab with detailed logging"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Progress bar and status
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(1, weight=1)
        
        ttk.Label(progress_frame, text="Progress:").grid(row=0, column=0, padx=(0, 5))
        
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Live logging area
        log_frame = ttk.LabelFrame(parent, text="📝 Capture Log", padding="5")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area with scrollbar
        log_container = ttk.Frame(log_frame)
        log_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_container, height=8, wrap=tk.WORD, font=('Consolas', 9))
        log_scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure text tags for colored logging
        self.log_text.tag_configure("INFO", foreground="#0066cc")
        self.log_text.tag_configure("SUCCESS", foreground="#28a745")
        self.log_text.tag_configure("WARNING", foreground="#ffc107")
        self.log_text.tag_configure("ERROR", foreground="#dc3545")
        self.log_text.tag_configure("DEBUG", foreground="#6c757d")
        
        # Log controls
        log_controls = ttk.Frame(log_frame)
        log_controls.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        clear_btn = ttk.Button(log_controls, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=0, column=0, padx=(0, 5))
        
        save_btn = ttk.Button(log_controls, text="Save Log", command=self.save_log)
        save_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Auto-scroll checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_cb = ttk.Checkbutton(log_controls, text="Auto-scroll", variable=self.auto_scroll_var)
        auto_scroll_cb.grid(row=0, column=2)
        
        # Add keyboard shortcut info
        ttk.Label(log_controls, text="💡 Ctrl+L: Clear Log | Ctrl+S: Save Log", 
                 font=('Arial', 8), foreground='#6c757d').grid(row=0, column=3, padx=(20, 0))
        
        # Add initial log entry
        self.log_message("INFO", "🚀 ScreenQA initialized and ready for capture")
        self.log_message("INFO", "💡 Press F9 to toggle sidebar | Ctrl+Enter to start capture")
        self.log_message("INFO", "ℹ️ Check the About tab for developer info and GitHub link")
        
        # Results area
        results_frame = ttk.LabelFrame(parent, text="📊 Capture Results", padding="5")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for results
        columns = ('Device', 'Status', 'Resolution', 'Mode', 'File Size', 'Actions')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            if col == 'Device':
                self.results_tree.column(col, width=180)
            elif col == 'Mode':
                self.results_tree.column(col, width=100)
            elif col == 'Actions':
                self.results_tree.column(col, width=80)
            elif col in ['Status', 'File Size']:
                self.results_tree.column(col, width=90)
            else:
                self.results_tree.column(col, width=80)
        
        # Scrollbars for results tree
        results_scrollbar_v = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        results_scrollbar_h = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=results_scrollbar_v.set, xscrollcommand=results_scrollbar_h.set)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        results_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind double-click to open screenshot
        self.results_tree.bind('<Double-1>', self.open_screenshot)
    
    def setup_gallery_tab(self, parent):
        """Setup screenshot gallery tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Gallery controls
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(controls_frame, text="Refresh Gallery", command=self.refresh_gallery).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(controls_frame, text="Open Screenshots Folder", command=self.open_screenshots_folder).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(controls_frame, text="Generate Report", command=self.generate_report).grid(row=0, column=2)
        
        # Gallery area
        gallery_container = ttk.Frame(parent)
        gallery_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        gallery_container.columnconfigure(0, weight=1)
        gallery_container.rowconfigure(0, weight=1)
        
        # Canvas for gallery with scrolling
        self.gallery_canvas = tk.Canvas(gallery_container)
        gallery_scrollbar_v = ttk.Scrollbar(gallery_container, orient="vertical", command=self.gallery_canvas.yview)
        gallery_scrollbar_h = ttk.Scrollbar(gallery_container, orient="horizontal", command=self.gallery_canvas.xview)
        
        self.gallery_content = ttk.Frame(self.gallery_canvas)
        self.gallery_content.bind("<Configure>", lambda e: self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all")))
        
        self.gallery_canvas.create_window((0, 0), window=self.gallery_content, anchor="nw")
        self.gallery_canvas.configure(yscrollcommand=gallery_scrollbar_v.set, xscrollcommand=gallery_scrollbar_h.set)
        
        self.gallery_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        gallery_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        gallery_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def setup_history_tab(self, parent):
        """Setup history tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # History controls
        hist_controls = ttk.Frame(parent)
        hist_controls.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(hist_controls, text="Refresh History", command=self.refresh_history).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(hist_controls, text="Clear History", command=self.clear_history).grid(row=0, column=1)
        
        # History list
        hist_frame = ttk.Frame(parent)
        hist_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        hist_frame.columnconfigure(0, weight=1)
        hist_frame.rowconfigure(0, weight=1)
        
        hist_columns = ('Timestamp', 'Domain', 'Device', 'File Size')
        self.history_tree = ttk.Treeview(hist_frame, columns=hist_columns, show='headings')
        
        for col in hist_columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        hist_scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=hist_scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        hist_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.history_tree.bind('<Double-1>', self.open_history_screenshot)
    
    def setup_qa_tab(self, parent):
        """Setup QA tools tab"""
        parent.columnconfigure(0, weight=1)
        
        # QA Tools
        qa_label = ttk.Label(parent, text="QA Testing Features", font=('Arial', 12, 'bold'))
        qa_label.grid(row=0, column=0, pady=(0, 10))
        
        # Responsive breakpoints
        breakpoints_frame = ttk.LabelFrame(parent, text="Responsive Breakpoints", padding="10")
        breakpoints_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(breakpoints_frame, text="Test common responsive breakpoints:").grid(row=0, column=0, columnspan=3, sticky=(tk.W,))
        
        breakpoint_buttons = [
            ("Mobile (320px)", lambda: self.test_breakpoint(320)),
            ("Tablet (768px)", lambda: self.test_breakpoint(768)),
            ("Desktop (1024px)", lambda: self.test_breakpoint(1024)),
            ("Large (1440px)", lambda: self.test_breakpoint(1440))
        ]
        
        for i, (text, command) in enumerate(breakpoint_buttons):
            ttk.Button(breakpoints_frame, text=text, command=command).grid(row=1, column=i, padx=5, pady=5)
        
        # Performance testing
        perf_frame = ttk.LabelFrame(parent, text="Performance Testing", padding="10")
        perf_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(perf_frame, text="Test Load Time", command=self.test_load_time).grid(row=0, column=0, padx=5)
        ttk.Button(perf_frame, text="Mobile Performance", command=self.test_mobile_performance).grid(row=0, column=1, padx=5)
        
        # Comparison tools
        comp_frame = ttk.LabelFrame(parent, text="Screenshot Comparison", padding="10")
        comp_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(comp_frame, text="Compare Screenshots", command=self.compare_screenshots).grid(row=0, column=0, padx=5)
        ttk.Button(comp_frame, text="Batch Analysis", command=self.batch_analysis).grid(row=0, column=1, padx=5)

    def setup_about_tab(self, parent):
        """Setup About tab with developer information"""
        # Configure scrollable frame
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Main container with scrolling
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header section
        header_frame = ttk.Frame(scrollable_frame, style='Card.TFrame', padding="20")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # App title and icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        app_title = ttk.Label(title_frame, text="📸 ScreenQA", 
                             font=('Arial', 24, 'bold'), foreground='#007bff')
        app_title.pack()
        
        app_subtitle = ttk.Label(title_frame, text="Website Screenshot Testing Tool", 
                                font=('Arial', 14), foreground='#6c757d')
        app_subtitle.pack(pady=(5, 0))
        
        version_label = ttk.Label(title_frame, text="Version 1.0.0", 
                                 font=('Arial', 10), foreground='#28a745')
        version_label.pack(pady=(5, 0))
        
        # Developer information
        dev_frame = ttk.LabelFrame(scrollable_frame, text="👨‍💻 Developer Information", padding="20")
        dev_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Developer details
        dev_info = [
            ("Name:", "Lahiru Sandaruwan Liyanage"),
            ("Location:", "Sri Lanka 🇱🇰"),
            ("Profession:", "DevOps Engineer"),
            ("Specialization:", "Infrastructure, Automation & Testing Tools")
        ]
        
        for i, (label, value) in enumerate(dev_info):
            info_frame = ttk.Frame(dev_frame)
            info_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(info_frame, text=label, font=('Arial', 10, 'bold'), 
                     width=15).pack(side=tk.LEFT)
            ttk.Label(info_frame, text=value, font=('Arial', 10)).pack(side=tk.LEFT, padx=(10, 0))
        
        # GitHub section
        github_frame = ttk.LabelFrame(scrollable_frame, text="🔗 Source Code & Contact", padding="20")
        github_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # GitHub repository
        github_info_frame = ttk.Frame(github_frame)
        github_info_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(github_info_frame, text="GitHub Repository:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        github_url = "https://github.com/nooblk-98/screenQA"
        github_link_frame = ttk.Frame(github_info_frame)
        github_link_frame.pack(fill=tk.X, pady=(5, 0))
        
        github_link = ttk.Label(github_link_frame, text=github_url, 
                               font=('Arial', 10, 'underline'), foreground='#007bff', 
                               cursor='hand2')
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: self.open_url(github_url))
        
        copy_btn = ttk.Button(github_link_frame, text="📋 Copy", width=8,
                             command=lambda: self.copy_to_clipboard(github_url))
        copy_btn.pack(side=tk.RIGHT)
        
        # Action buttons
        actions_frame = ttk.Frame(github_frame)
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        github_btn = ttk.Button(actions_frame, text="🌐 Open GitHub", 
                               command=lambda: self.open_url(github_url),
                               style='Primary.TButton')
        github_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        issues_btn = ttk.Button(actions_frame, text="🐛 Report Issue", 
                               command=lambda: self.open_url(f"{github_url}/issues"),
                               style='Warning.TButton')
        issues_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Application features
        features_frame = ttk.LabelFrame(scrollable_frame, text="✨ Key Features", padding="20")
        features_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        features = [
            "📱 Multi-device screenshot capture (Mobile, Tablet, Desktop)",
            "🌐 Cross-browser compatibility testing",
            "📊 Real-time progress tracking and logging",
            "🎯 Responsive design testing",
            "📁 Organized screenshot gallery",
            "⚡ Batch processing capabilities",
            "🔧 QA tools and utilities",
            "💾 Export and reporting features"
        ]
        
        for feature in features:
            feature_label = ttk.Label(features_frame, text=f"  {feature}", 
                                     font=('Arial', 10))
            feature_label.pack(anchor=tk.W, pady=1)
        
        # Technical information
        tech_frame = ttk.LabelFrame(scrollable_frame, text="🔧 Technical Details", padding="20")
        tech_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tech_info = [
            ("Framework:", "Python 3.11+ with Tkinter GUI"),
            ("Web Driver:", "Selenium WebDriver"),
            ("Image Processing:", "PIL/Pillow"),
            ("Build System:", "PyInstaller"),
            ("CI/CD:", "GitHub Actions"),
            ("License:", "MIT License")
        ]
        
        for label, value in tech_info:
            tech_info_frame = ttk.Frame(tech_frame)
            tech_info_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(tech_info_frame, text=label, font=('Arial', 10, 'bold'), 
                     width=15).pack(side=tk.LEFT)
            ttk.Label(tech_info_frame, text=value, font=('Arial', 10)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Footer
        footer_frame = ttk.Frame(scrollable_frame, style='Card.TFrame', padding="20")
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        footer_text = ttk.Label(footer_frame, 
                               text="Thank you for using ScreenQA! 🙏\nBuilt with ❤️ for the testing community",
                               font=('Arial', 11), foreground='#6c757d', justify=tk.CENTER)
        footer_text.pack()
        
        # Configure canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)

    def open_url(self, url):
        """Open URL in default browser"""
        try:
            import webbrowser
            webbrowser.open(url)
            self.log_message("INFO", f"🌐 Opened URL: {url}")
        except Exception as e:
            self.log_message("ERROR", f"❌ Failed to open URL: {str(e)}")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.log_message("SUCCESS", f"📋 Copied to clipboard: {text}")
        except Exception as e:
            self.log_message("ERROR", f"❌ Failed to copy to clipboard: {str(e)}")
    
    def setup_status_bar(self, parent, row):
        """Setup status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=0, sticky=(tk.W,))
        
        # Device count
        self.device_count_var = tk.StringVar(value="0 devices selected")
        ttk.Label(status_frame, textvariable=self.device_count_var).grid(row=0, column=2, sticky=(tk.E,))
    
    def load_devices(self):
        """Load available devices into the UI using a grid layout"""
        devices_by_platform = self.capture.get_available_devices()
        
        # Configure grid columns for better space utilization
        columns = 3  # Number of columns for device layout
        for col in range(columns):
            self.devices_frame.columnconfigure(col, weight=1)
        
        row = 0
        for platform, devices in devices_by_platform.items():
            # Platform header spanning all columns
            platform_label = ttk.Label(self.devices_frame, text=platform, font=('Arial', 10, 'bold'))
            platform_label.grid(row=row, column=0, columnspan=columns, sticky=(tk.W,), pady=(10 if row > 0 else 0, 5))
            row += 1
            
            # Device checkboxes in grid layout
            col = 0
            for device in devices:
                var = tk.BooleanVar()
                self.device_vars[device['name']] = var
                
                checkbox = ttk.Checkbutton(
                    self.devices_frame, 
                    text=f"{device['name']} ({device['resolution']})",
                    variable=var,
                    command=self.update_device_selection
                )
                checkbox.grid(row=row, column=col, sticky=(tk.W,), padx=10, pady=2)
                
                # Add mouse wheel scrolling to each checkbox
                if hasattr(self, 'device_canvas'):
                    def checkbox_mousewheel(event):
                        if event.delta:
                            self.device_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                        elif event.num == 4:
                            self.device_canvas.yview_scroll(-1, "units")
                        elif event.num == 5:
                            self.device_canvas.yview_scroll(1, "units")
                    
                    checkbox.bind("<MouseWheel>", checkbox_mousewheel)
                    checkbox.bind("<Button-4>", checkbox_mousewheel)
                    checkbox.bind("<Button-5>", checkbox_mousewheel)
                
                # Move to next column, wrap to next row if needed
                col += 1
                if col >= columns:
                    col = 0
                    row += 1
            
            # If we ended in the middle of a row, move to next row for next platform
            if col > 0:
                row += 1
        
        self.update_device_selection()
    
    def update_device_selection(self):
        """Update selected devices list and UI"""
        self.selected_devices = [name for name, var in self.device_vars.items() if var.get()]
        count = len(self.selected_devices)
        self.device_count_var.set(f"{count} device{'s' if count != 1 else ''} selected")
        
        # Enable/disable capture button
        self.capture_btn.config(state='normal' if count > 0 and self.url_var.get().strip() else 'disabled')
    
    def select_all_devices(self):
        """Select all devices"""
        for var in self.device_vars.values():
            var.set(True)
        self.update_device_selection()
        self.log_message("INFO", f"📱 Selected all devices ({len(self.device_vars)} total)")
    
    def clear_all_devices(self):
        """Clear all device selections"""
        for var in self.device_vars.values():
            var.set(False)
        self.update_device_selection()
        self.log_message("INFO", "🧹 Cleared all device selections")
    
    def select_mobile_devices(self):
        """Select only mobile devices"""
        self.clear_all_devices()
        mobile_keywords = ['iPhone', 'Android', 'Mobile', 'Galaxy', 'Pixel']
        selected_count = 0
        for name, var in self.device_vars.items():
            if any(keyword in name for keyword in mobile_keywords):
                var.set(True)
                selected_count += 1
        self.update_device_selection()
        self.log_message("INFO", f"📱 Selected {selected_count} mobile devices")
    
    def select_desktop_devices(self):
        """Select only desktop devices"""
        self.clear_all_devices()
        desktop_keywords = ['Desktop', 'MacBook', 'Windows', 'Mac']
        selected_count = 0
        for name, var in self.device_vars.items():
            if any(keyword in name for keyword in desktop_keywords):
                var.set(True)
                selected_count += 1
        self.update_device_selection()
        self.log_message("INFO", f"🖥️ Selected {selected_count} desktop devices")
    
    def validate_url(self):
        """Validate the entered URL with logging"""
        url = self.url_var.get().strip()
        if not url:
            self.log_message("WARNING", "⚠️ No URL entered for validation")
            messagebox.showwarning("Invalid URL", "Please enter a URL")
            return
        
        self.log_message("INFO", f"🔍 Validating URL: {url}")
        self.status_var.set("Validating URL...")
        self.root.update()
        
        valid, result = self.capture.validate_url(url)
        if valid:
            self.url_var.set(result)  # Set the corrected URL
            self.status_var.set(f"URL is valid: {result}")
            self.log_message("SUCCESS", f"✅ URL is valid and accessible: {result}")
            messagebox.showinfo("Valid URL", f"URL is accessible: {result}")
        else:
            self.status_var.set(f"URL validation failed: {result}")
            self.log_message("ERROR", f"❌ URL validation failed: {result}")
            messagebox.showerror("Invalid URL", f"URL validation failed: {result}")
            messagebox.showerror("Invalid URL", f"URL validation failed: {result}")
    
    def start_capture(self):
        """Start screenshot capture process with detailed logging"""
        url = self.url_var.get().strip()
        if not url:
            self.log_message("WARNING", "⚠️ No URL provided - capture cancelled")
            messagebox.showwarning("Missing URL", "Please enter a URL")
            return
        
        if not self.selected_devices:
            self.log_message("WARNING", "⚠️ No devices selected - capture cancelled")
            messagebox.showwarning("No Devices", "Please select at least one device")
            return
        
        self.log_message("INFO", f"🔍 Starting capture process for URL: {url}")
        self.log_message("INFO", f"📱 Selected devices: {len(self.selected_devices)}")
        
        # Validate URL first
        self.update_progress_status("🔍 Validating URL...", "INFO")
        valid, validated_url = self.capture.validate_url(url)
        if not valid:
            error_msg = f"URL validation failed: {validated_url}"
            self.log_message("ERROR", f"❌ {error_msg}")
            messagebox.showerror("Invalid URL", error_msg)
            return
        
        self.url_var.set(validated_url)
        self.log_message("SUCCESS", f"✅ URL validated: {validated_url}")
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.current_results = {}
        self.result_data = {}  # Clear previous result data
        self.log_message("INFO", "🧹 Cleared previous results")
        
        # Start progress indication
        self.progress_bar.start(10)
        self.capture_btn.config(state='disabled')
        self.update_progress_status("🚀 Starting screenshot capture...", "INFO")
        
        # Get selected screenshot mode
        screenshot_mode = self.screenshot_mode_var.get()
        self.log_message("INFO", f"📄 Screenshot mode: {screenshot_mode}")
        
        # Log device details
        for device in self.selected_devices:
            self.log_message("DEBUG", f"🖥️ Will capture: {device}")
        
        # Start async capture with selected mode
        success, message = self.async_capture.capture_async(
            validated_url, 
            self.selected_devices,
            progress_callback=self.update_progress_enhanced,
            complete_callback=self.capture_complete_enhanced,
            screenshot_mode=screenshot_mode
        )
        
        if not success:
            error_msg = f"Failed to start capture: {message}"
            self.log_message("ERROR", f"❌ {error_msg}")
            messagebox.showerror("Capture Error", message)
            self.progress_bar.stop()
            self.capture_btn.config(state='normal')
            self.update_progress_status("❌ Capture failed to start", "ERROR")
    
    def update_progress(self, message):
        """Update progress display"""
        self.progress_var.set(message)
        self.status_var.set(message)
        self.root.update()

    def update_progress_enhanced(self, message):
        """Enhanced progress update with logging"""
        self.progress_var.set(message)
        self.status_var.set(message)
        self.log_message("INFO", f"📊 {message}")
        self.root.update()

    def capture_complete(self, results):
        """Handle capture completion"""
        self.current_results = results
        
        # Stop progress bar
        self.progress_bar.stop()
        self.capture_btn.config(state='normal')
        
        # Update results tree
        success_count = 0
        for device_name, result in results.items():
            status = "Success" if result['success'] else "Failed"
            if result['success']:
                success_count += 1
                
                # Get file size
                try:
                    file_size = os.path.getsize(result['screenshot_path'])
                    size_str = f"{file_size / 1024:.1f} KB"
                except:
                    size_str = "Unknown"
                
                resolution = f"{result['device_info']['width']}x{result['device_info']['height']}"
            else:
                size_str = "N/A"
                resolution = "N/A"

    def capture_complete_enhanced(self, results):
        """Enhanced capture completion with detailed logging"""
        self.current_results = results
        
        # Stop progress bar and re-enable capture button
        self.progress_bar.stop()
        self.capture_btn.config(state='normal')
        
        total_devices = len(results)
        success_count = 0
        failed_count = 0
        
        self.log_message("INFO", "📊 Processing capture results...")
        
        # Update results tree and log each result
        for device_name, result in results.items():
            status = "Success" if result['success'] else "Failed"
            
            if result['success']:
                success_count += 1
                
                # Get file size
                try:
                    file_size = os.path.getsize(result['screenshot_path'])
                    size_str = f"{file_size / 1024:.1f} KB"
                    self.log_message("SUCCESS", f"✅ {device_name}: Screenshot saved ({size_str}) - {result['screenshot_path']}")
                except Exception as e:
                    size_str = "Unknown"
                    self.log_message("WARNING", f"⚠️ {device_name}: File size unknown - {str(e)}")
                
                resolution = f"{result['device_info']['width']}x{result['device_info']['height']}"
            else:
                failed_count += 1
                size_str = "N/A"
                resolution = "N/A"
                error_msg = result.get('error', 'Unknown error')
                self.log_message("ERROR", f"❌ {device_name}: Capture failed - {error_msg}")
            
            # Add to results tree
            mode = result.get('screenshot_mode', 'Unknown')
            item_id = self.results_tree.insert('', 'end', values=(
                device_name, status, resolution, mode, size_str, "View"
            ))
            
            # Store result reference for actions using tags (safer than trying to add to non-existent column)
            try:
                # Store the result path as a tag for later retrieval
                result_path = result.get('screenshot_path', '')
                self.results_tree.set(item_id, '#1', device_name)  # Ensure device name is set
                # Store result data in a class variable for actions
                if not hasattr(self, 'result_data'):
                    self.result_data = {}
                self.result_data[item_id] = result
            except Exception as e:
                self.log_message("ERROR", f"📊 Error storing result data: {str(e)}")
        
        # Final summary
        self.log_message("INFO", f"📈 Capture completed: {success_count}/{total_devices} successful")
        if failed_count > 0:
            self.log_message("WARNING", f"⚠️ {failed_count} captures failed")
        
        # Log summary statistics
        if success_count > 0:
            total_size = 0
            for device_name, result in results.items():
                if result['success']:
                    try:
                        file_size = os.path.getsize(result['screenshot_path'])
                        total_size += file_size
                    except:
                        pass
            
            if total_size > 0:
                if total_size > 1024 * 1024:  # > 1MB
                    size_str = f"{total_size / (1024*1024):.1f} MB"
                else:
                    size_str = f"{total_size / 1024:.1f} KB"
                self.log_message("INFO", f"💾 Total screenshots size: {size_str}")
        
        # Update status
        if success_count == total_devices:
            status_msg = f"✅ All {total_devices} captures successful"
            self.update_progress_status(status_msg, "SUCCESS")
        elif success_count > 0:
            status_msg = f"⚠️ {success_count}/{total_devices} captures successful"
            self.update_progress_status(status_msg, "WARNING")
        else:
            status_msg = "❌ All captures failed"
            self.update_progress_status(status_msg, "ERROR")
        
        # Update UI elements
        self.refresh_preview()
        self.refresh_gallery()
        
        # Show completion notification
        if success_count > 0:
            self.log_message("SUCCESS", f"🎉 Screenshot capture completed! Check the results above.")
        else:
            self.log_message("ERROR", f"😞 No screenshots were captured successfully.")
            
            # Get screenshot mode display name
            mode = result.get('screenshot_mode', 'full_page')
            mode_display = {
                'full_page': '📜 Full Page',
                'viewport_only': '🖼️ Viewport',
                'auto': '🤖 Auto'
            }.get(mode, mode)
            
            self.results_tree.insert('', 'end', values=(
                device_name, 
                status, 
                resolution,
                mode_display,
                size_str,
                "View" if result['success'] else "Error"
            ))
        
        # Update status
        total = len(results)
        mode_used = self.screenshot_mode_var.get()
        mode_name = {
            'full_page': 'Full Page',
            'viewport_only': 'Viewport Only', 
            'auto': 'Auto Detect'
        }.get(mode_used, mode_used)
        
        self.status_var.set(f"Capture complete: {success_count}/{total} successful ({mode_name} mode)")
        self.progress_var.set(f"Complete: {success_count}/{total} screenshots captured using {mode_name} mode")
        
        # Show completion message
        if success_count == total:
            messagebox.showinfo("Capture Complete", f"All {total} screenshots captured successfully!")
        elif success_count > 0:
            messagebox.showwarning("Partial Success", f"{success_count}/{total} screenshots captured successfully")
        else:
            messagebox.showerror("Capture Failed", "No screenshots were captured successfully")
        
        # Refresh gallery and history
        self.refresh_gallery()
        self.refresh_history()
    
    def open_screenshot(self, event):
        """Open selected screenshot"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = self.results_tree.item(selection[0])
        device_name = item['values'][0]
        
        if device_name in self.current_results and self.current_results[device_name]['success']:
            screenshot_path = self.current_results[device_name]['screenshot_path']
            if os.path.exists(screenshot_path):
                if sys.platform.startswith('win'):
                    os.startfile(screenshot_path)
                elif sys.platform.startswith('darwin'):
                    subprocess.call(['open', screenshot_path])
                else:
                    subprocess.call(['xdg-open', screenshot_path])
    
    def refresh_gallery(self):
        """Refresh the screenshot gallery"""
        # Clear existing gallery
        for widget in self.gallery_content.winfo_children():
            widget.destroy()
        
        # Load recent screenshots
        screenshots = self.capture.get_screenshot_history()[:20]  # Limit to recent 20
        
        if not screenshots:
            ttk.Label(self.gallery_content, text="No screenshots found", 
                     font=('Arial', 12)).grid(row=0, column=0, pady=20)
            return
        
        # Display screenshots in grid
        cols = 4
        for i, screenshot in enumerate(screenshots):
            row = i // cols
            col = i % cols
            
            frame = ttk.Frame(self.gallery_content, padding="5", relief="solid", borderwidth=1)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            try:
                # Load and resize image
                img = Image.open(screenshot['filepath'])
                img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Image label
                img_label = ttk.Label(frame, image=photo)
                img_label.image = photo  # Keep a reference
                img_label.grid(row=0, column=0)
                img_label.bind("<Button-1>", lambda e, path=screenshot['filepath']: self.open_file(path))
                
                # Info label
                info_text = f"{screenshot['device']}\\n{screenshot['created']}"
                ttk.Label(frame, text=info_text, font=('Arial', 8)).grid(row=1, column=0)
                
            except Exception as e:
                ttk.Label(frame, text=f"Error loading\\n{screenshot['filename']}").grid(row=0, column=0)
    
    def refresh_history(self):
        """Refresh the history list"""
        # Clear existing history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Load history
        screenshots = self.capture.get_screenshot_history()
        
        for screenshot in screenshots:
            size_mb = screenshot['size'] / 1024 / 1024
            size_str = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{screenshot['size'] / 1024:.1f} KB"
            
            self.history_tree.insert('', 'end', values=(
                screenshot['created'],
                screenshot['domain'],
                screenshot['device'],
                size_str
            ))
    
    def open_history_screenshot(self, event):
        """Open screenshot from history"""
        selection = self.history_tree.selection()
        if not selection:
            return
        
        item = self.history_tree.item(selection[0])
        # Find the screenshot file
        screenshots = self.capture.get_screenshot_history()
        for screenshot in screenshots:
            if (screenshot['created'] == item['values'][0] and 
                screenshot['domain'] == item['values'][1] and
                screenshot['device'] == item['values'][2]):
                self.open_file(screenshot['filepath'])
                break
    
    def open_file(self, filepath):
        """Open file with system default program"""
        if os.path.exists(filepath):
            if sys.platform.startswith('win'):
                os.startfile(filepath)
            elif sys.platform.startswith('darwin'):
                subprocess.call(['open', filepath])
            else:
                subprocess.call(['xdg-open', filepath])
    
    def open_screenshots_folder(self):
        """Open screenshots folder"""
        screenshots_dir = self.capture.screenshots_dir
        if os.path.exists(screenshots_dir):
            self.open_file(screenshots_dir)
        else:
            messagebox.showwarning("Folder Not Found", "Screenshots folder not found")
    
    def clear_history(self):
        """Clear screenshot history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to delete all screenshots?"):
            try:
                for filename in os.listdir(self.capture.screenshots_dir):
                    if filename.endswith('.png'):
                        os.remove(os.path.join(self.capture.screenshots_dir, filename))
                self.refresh_history()
                self.refresh_gallery()
                messagebox.showinfo("History Cleared", "All screenshots have been deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear history: {str(e)}")
    
    def generate_report(self):
        """Generate a QA report"""
        if not self.current_results:
            messagebox.showwarning("No Results", "Please capture some screenshots first")
            return
        
        # Simple report generation
        report_path = os.path.join(os.path.dirname(self.capture.screenshots_dir), 'reports', 
                                 f'qa_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        try:
            self.create_html_report(report_path)
            messagebox.showinfo("Report Generated", f"Report saved to: {report_path}")
            self.open_file(report_path)
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {str(e)}")
    
    def create_html_report(self, report_path):
        """Create HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ScreenQA Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .screenshot {{ margin: 10px; padding: 10px; border: 1px solid #ddd; display: inline-block; }}
                .screenshot img {{ max-width: 300px; max-height: 200px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ScreenQA Testing Report</h1>
                <p><strong>URL:</strong> {self.url_var.get()}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Total Devices:</strong> {len(self.current_results)}</p>
                <p><strong>Successful Screenshots:</strong> {sum(1 for r in self.current_results.values() if r['success'])}</p>
            </div>
            
            <h2>Screenshots</h2>
        """
        
        for device_name, result in self.current_results.items():
            if result['success']:
                # Convert absolute path to relative for HTML
                rel_path = os.path.relpath(result['screenshot_path'], os.path.dirname(report_path))
                html_content += f"""
                <div class="screenshot">
                    <h3>{device_name}</h3>
                    <p class="success">✓ Success</p>
                    <p>Resolution: {result['device_info']['width']}x{result['device_info']['height']}</p>
                    <img src="{rel_path}" alt="{device_name} screenshot">
                </div>
                """
            else:
                html_content += f"""
                <div class="screenshot">
                    <h3>{device_name}</h3>
                    <p class="error">✗ Failed: {result['error']}</p>
                </div>
                """
        
        html_content += """
            </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    # QA Tools Methods
    def test_breakpoint(self, width):
        """Test specific breakpoint"""
        messagebox.showinfo("Breakpoint Test", f"Testing breakpoint: {width}px\\n\\nThis would capture screenshots at {width}px width with various heights.")
    
    def test_load_time(self):
        """Test load time"""
        messagebox.showinfo("Load Time Test", "Load time testing feature would measure page load performance across devices.")
    
    def test_mobile_performance(self):
        """Test mobile performance"""
        messagebox.showinfo("Mobile Performance", "Mobile performance testing would analyze mobile-specific metrics.")
    
    def compare_screenshots(self):
        """Compare screenshots"""
        messagebox.showinfo("Screenshot Comparison", "Screenshot comparison feature would allow side-by-side analysis.")
    
    def batch_analysis(self):
        """Batch analysis"""
        messagebox.showinfo("Batch Analysis", "Batch analysis would process multiple URLs and generate comprehensive reports.")
    
    # Quick Action Methods for Resizable UI
    def quick_capture_mobile(self):
        """Quick capture for mobile devices only"""
        if not self.url_var.get().strip():
            messagebox.showwarning("Missing URL", "Please enter a URL first")
            return
        self.select_mobile_devices()
        self.start_capture()
    
    def quick_capture_desktop(self):
        """Quick capture for desktop devices only"""
        if not self.url_var.get().strip():
            messagebox.showwarning("Missing URL", "Please enter a URL first")
            return
        self.select_desktop_devices()
        self.start_capture()
    
    def quick_capture_all(self):
        """Quick capture for all devices"""
        if not self.url_var.get().strip():
            messagebox.showwarning("Missing URL", "Please enter a URL first")
            return
        self.select_all_devices()
        self.start_capture()
    
    def refresh_preview(self):
        """Refresh the preview panel with recent screenshots"""
        try:
            # Clear existing previews
            for widget in self.preview_content.winfo_children():
                widget.destroy()
            
            # Get recent screenshots
            screenshots = self.capture.get_screenshot_history()[:5]  # Last 5
            
            if not screenshots:
                ttk.Label(self.preview_content, text="No screenshots yet", 
                         font=('Arial', 9), foreground='gray').grid(row=0, column=0, pady=10)
                return
            
            # Display preview thumbnails
            for i, screenshot in enumerate(screenshots):
                try:
                    # Create preview frame
                    preview_frame = ttk.Frame(self.preview_content, padding="2", relief="solid", borderwidth=1)
                    preview_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2, padx=2)
                    preview_frame.columnconfigure(1, weight=1)
                    
                    # Load and resize image for thumbnail
                    img = Image.open(screenshot['filepath'])
                    img.thumbnail((60, 45), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Thumbnail
                    img_label = ttk.Label(preview_frame, image=photo)
                    img_label.image = photo  # Keep reference
                    img_label.grid(row=0, column=0, rowspan=2, padx=(0, 5))
                    img_label.bind("<Button-1>", lambda e, path=screenshot['filepath']: self.open_file(path))
                    
                    # Info
                    info_text = f"{screenshot['device']}"
                    ttk.Label(preview_frame, text=info_text, font=('Arial', 8)).grid(row=0, column=1, sticky=(tk.W,))
                    
                    time_text = screenshot['created']
                    ttk.Label(preview_frame, text=time_text, font=('Arial', 7), foreground='gray').grid(row=1, column=1, sticky=(tk.W,))
                    
                except Exception as e:
                    # Error loading preview
                    error_frame = ttk.Frame(self.preview_content)
                    error_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
                    ttk.Label(error_frame, text=f"Error: {screenshot['filename']}", 
                             font=('Arial', 8), foreground='red').grid(row=0, column=0)
                    
        except Exception as e:
            print(f"Error refreshing preview: {e}")
    
    def toggle_actions_panel(self):
        """Toggle the visibility of the actions panel"""
        try:
            # Get current position of the sash (divider)
            sash_coord = self.content_paned.sash_coord(0)
            window_width = self.content_paned.winfo_width()
            
            # If panel is mostly hidden (sash near right edge), show it
            if sash_coord[0] > window_width * 0.8:
                # Show panel (move sash to 70% position)
                new_pos = int(window_width * 0.7)
                self.content_paned.sash_place(0, new_pos, sash_coord[1])
            else:
                # Hide panel (move sash near right edge)
                new_pos = int(window_width * 0.95)
                self.content_paned.sash_place(0, new_pos, sash_coord[1])
                
        except Exception as e:
            print(f"Error toggling actions panel: {e}")


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Set up modern theme
    style = ttk.Style()
    
    # Use a compatible theme
    try:
        style.theme_use('clam')  # More reliable than default
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
    
    app = ScreenQAApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()