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
        
        # Setup UI
        self.setup_ui()
        self.load_devices()
        
        # Bind keyboard shortcuts
        self.root.bind('<F9>', lambda e: self.toggle_actions_panel())
        self.root.bind('<Control-Return>', lambda e: self.start_capture())
        
    def setup_ui(self):
        """Setup the main user interface with resizable panes"""
        # Configure root grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main container
        main_container = ttk.Frame(self.root, padding="5")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # URL Input Section (fixed at top)
        url_container = ttk.Frame(main_container)
        url_container.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        url_container.columnconfigure(0, weight=1)
        self.setup_url_section(url_container, row=0)
        
        # Main resizable paned window (vertical split)
        self.main_paned = tk.PanedWindow(main_container, orient=tk.VERTICAL, 
                                        sashrelief=tk.RAISED, sashwidth=8,
                                        bg='#e0e0e0')
        self.main_paned.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Top pane - Device Selection (resizable height)
        self.device_pane = ttk.Frame(self.main_paned)
        self.main_paned.add(self.device_pane, minsize=120, height=180)
        self.setup_device_section_resizable(self.device_pane)
        
        # Bottom pane - Main content with horizontal split
        self.content_paned = tk.PanedWindow(self.main_paned, orient=tk.HORIZONTAL,
                                           sashrelief=tk.RAISED, sashwidth=8,
                                           bg='#e0e0e0')
        self.main_paned.add(self.content_paned, minsize=300)
        
        # Left side - Tabs (main content)
        self.tabs_frame = ttk.Frame(self.content_paned)
        self.content_paned.add(self.tabs_frame, minsize=600, width=800)
        self.setup_tabs_resizable(self.tabs_frame)
        
        # Right side - Quick Actions Panel (collapsible)
        self.actions_frame = ttk.Frame(self.content_paned)
        self.content_paned.add(self.actions_frame, minsize=200, width=300)
        self.setup_actions_panel(self.actions_frame)
        
        # Status bar (fixed at bottom)
        status_container = ttk.Frame(main_container)
        status_container.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        status_container.columnconfigure(0, weight=1)
        self.setup_status_bar(status_container, row=0)
        
        # Configure paned window appearance
        self.configure_paned_windows()
    
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
                                     command=self.start_capture, style="Accent.TButton")
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
        parent.rowconfigure(1, weight=1)
        
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
        canvas = tk.Canvas(devices_container)
        scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
        self.devices_frame = ttk.Frame(canvas)
        
        self.devices_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.devices_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
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
        """Setup progress and results tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
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
        
        # Results area
        results_frame = ttk.LabelFrame(parent, text="Capture Results", padding="5")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for results
        columns = ('Device', 'Status', 'Resolution', 'File Size', 'Actions')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            if col == 'Device':
                self.results_tree.column(col, width=200)
            elif col == 'Actions':
                self.results_tree.column(col, width=100)
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
        """Load available devices into the UI"""
        devices_by_platform = self.capture.get_available_devices()
        
        row = 0
        for platform, devices in devices_by_platform.items():
            # Platform header
            platform_label = ttk.Label(self.devices_frame, text=platform, font=('Arial', 10, 'bold'))
            platform_label.grid(row=row, column=0, sticky=(tk.W,), pady=(5 if row > 0 else 0, 2))
            row += 1
            
            # Device checkboxes
            for device in devices:
                var = tk.BooleanVar()
                self.device_vars[device['name']] = var
                
                checkbox = ttk.Checkbutton(
                    self.devices_frame, 
                    text=f"{device['name']} ({device['resolution']})",
                    variable=var,
                    command=self.update_device_selection
                )
                checkbox.grid(row=row, column=0, sticky=(tk.W,), padx=20)
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
    
    def clear_all_devices(self):
        """Clear all device selections"""
        for var in self.device_vars.values():
            var.set(False)
        self.update_device_selection()
    
    def select_mobile_devices(self):
        """Select only mobile devices"""
        self.clear_all_devices()
        mobile_keywords = ['iPhone', 'Android', 'Mobile', 'Galaxy', 'Pixel']
        for name, var in self.device_vars.items():
            if any(keyword in name for keyword in mobile_keywords):
                var.set(True)
        self.update_device_selection()
    
    def select_desktop_devices(self):
        """Select only desktop devices"""
        self.clear_all_devices()
        desktop_keywords = ['Desktop', 'MacBook', 'Windows', 'Mac']
        for name, var in self.device_vars.items():
            if any(keyword in name for keyword in desktop_keywords):
                var.set(True)
        self.update_device_selection()
    
    def validate_url(self):
        """Validate the entered URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Invalid URL", "Please enter a URL")
            return
        
        self.status_var.set("Validating URL...")
        self.root.update()
        
        valid, result = self.capture.validate_url(url)
        if valid:
            self.url_var.set(result)  # Set the corrected URL
            self.status_var.set(f"URL is valid: {result}")
            messagebox.showinfo("Valid URL", f"URL is accessible: {result}")
        else:
            self.status_var.set(f"URL validation failed: {result}")
            messagebox.showerror("Invalid URL", f"URL validation failed: {result}")
    
    def start_capture(self):
        """Start screenshot capture process"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a URL")
            return
        
        if not self.selected_devices:
            messagebox.showwarning("No Devices", "Please select at least one device")
            return
        
        # Validate URL first
        valid, validated_url = self.capture.validate_url(url)
        if not valid:
            messagebox.showerror("Invalid URL", f"URL validation failed: {validated_url}")
            return
        
        self.url_var.set(validated_url)
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.current_results = {}
        
        # Start progress indication
        self.progress_bar.start(10)
        self.capture_btn.config(state='disabled')
        
        # Start async capture
        success, message = self.async_capture.capture_async(
            validated_url, 
            self.selected_devices,
            progress_callback=self.update_progress,
            complete_callback=self.capture_complete
        )
        
        if not success:
            messagebox.showerror("Capture Error", message)
            self.progress_bar.stop()
            self.capture_btn.config(state='normal')
    
    def update_progress(self, message):
        """Update progress display"""
        self.progress_var.set(message)
        self.status_var.set(message)
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
            
            self.results_tree.insert('', 'end', values=(
                device_name, 
                status, 
                resolution,
                size_str,
                "View" if result['success'] else "Error"
            ))
        
        # Update status
        total = len(results)
        self.status_var.set(f"Capture complete: {success_count}/{total} successful")
        self.progress_var.set(f"Complete: {success_count}/{total} screenshots captured")
        
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
    
    # Configure some custom styles
    style.configure("Accent.TButton", foreground="white")
    
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