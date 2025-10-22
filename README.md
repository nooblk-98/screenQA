# ScreenQA - Website Screenshot Testing Tool

![ScreenQA Logo](https://img.shields.io/badge/ScreenQA-Website%20Testing-blue?style=for-the-badge&logo=selenium)

A comprehensive Python application with a modern, professional GUI for capturing website screenshots across different device sizes and platforms for easy QA testing. Features a 3-column device layout, real-time logging system, and viewport-first screenshot mode for faster testing. Perfect for testing responsive designs, cross-device compatibility, and generating detailed QA reports.

## 🚀 Features

### Core Functionality
- **Multi-Device Screenshot Capture**: Capture screenshots across 15+ predefined device configurations
- **Real Browser Automation**: Uses Selenium WebDriver for authentic browser rendering
- **Flexible Screenshot Modes**: Choose between Full Page, Viewport Only, or Auto Detect capture
- **Responsive Design Testing**: Test websites at different breakpoints and resolutions
- **Performance Analysis**: Measure load times and performance metrics across devices

### Device Support
- **Desktop**: Windows (1920x1080), Mac (1440x900), MacBook Pro 13" & 16"
- **Mobile**: iPhone 15 Pro Max, iPhone 15, iPhone SE, Samsung Galaxy S24 Ultra/S24, Google Pixel 8 Pro
- **Tablets**: iPad Pro 12.9", iPad Air, Samsung Galaxy Tab S9, Generic Tablet

### Recent Enhancements (v2.0)
- **🎨 Modern UI Design**: Complete interface overhaul with professional 3-column layout
- **⚡ Viewport Mode Default**: Faster screenshot capture with viewport-first approach
- **📊 Real-Time Logging**: Comprehensive color-coded logging system with timestamps
- **👨‍💻 Developer Attribution**: Professional About page with GitHub integration
- **🔄 Streamlined Interface**: Removed unnecessary sections for cleaner user experience
- **🖥️ Cross-Platform Builds**: Automated builds for Windows, macOS, and Linux

### User Interface
- **Simple Tkinter GUI**: Easy-to-use interface, no web server required
- **Resizable Layout**: Drag resize bars to customize panel sizes
- **Screenshot Mode Selection**: Radio buttons to choose capture mode
- **Progress Tracking**: Real-time progress updates during capture
- **History Management**: View and manage screenshot history
- **Batch Operations**: Capture multiple devices simultaneously
- **Export Options**: Save screenshots and generate reports

## � UI Screenshots

### Main Application Interface
![ScreenQA Main Interface](assets/Screenshot%202025-10-22%20122424.png)

*Main application showing the device selection grid, URL input, screenshot mode options, and real-time logging system*

### About Page & Developer Information
![ScreenQA About Page](assets/Screenshot%202025-10-22%20122454.png)

*About page displaying developer details, GitHub integration, and comprehensive feature overview*

The modern interface features:
- **3-Column Device Layout**: Efficient horizontal space utilization with device categories
- **Real-Time Logging**: Color-coded log messages with timestamps for complete transparency
- **Professional Design**: Clean, intuitive interface with proper spacing and visual hierarchy
- **Viewport Mode Default**: Faster screenshot capture with viewport-only mode as default
- **Developer Attribution**: Complete developer information with GitHub profile integration

## �📋 Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Chrome Browser**: Required for Selenium WebDriver
- **Internet Connection**: For downloading ChromeDriver and accessing websites

## ⚡ Quick Start

### Option 1: Download Executable (Recommended) 
[![Build Status](https://github.com/nooblk-98/screenQA/workflows/Build%20ScreenQA%20Executable/badge.svg)](https://github.com/nooblk-98/screenQA/actions)

1. **Download the latest release**:
   - Go to [Releases](https://github.com/nooblk-98/screenQA/releases)
   - Download `ScreenQA-Windows.exe` for Windows
   - Download `ScreenQA-Linux` for Linux
   - Download `ScreenQA-macOS.dmg` for macOS

2. **Run the executable**:
   - **Windows**: Double-click `ScreenQA-Windows.exe`
   - **Linux**: `chmod +x ScreenQA-Linux && ./ScreenQA-Linux`
   - **macOS**: Open `ScreenQA-macOS.dmg` and run the app

### Option 2: Easy Start (Windows - from source)
1. **Download/Clone** this repository
2. **Double-click** `start_screenqa.bat`
3. The script will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Launch the application

### Option 3: Manual Installation (from source)
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd screenQA
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## 💻 Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Modern Interface Overview**:
   - **Device Selection**: Use the 3-column grid layout for easy device selection
   - **Screenshot Mode**: Viewport mode is now the default for faster captures
   - **Real-Time Logging**: Monitor capture progress with color-coded log messages
   - **Professional Layout**: Enjoy the enhanced UI with better spacing and organization

3. **Capture Screenshots**:
   - **Enter Website URL**: Input the URL you want to test
   - **Select Devices**: Choose from desktop, mobile, and tablet configurations
   - **Choose Mode**: Viewport (default, faster) or Full Page (complete content)
   - **Monitor Progress**: Watch real-time logs showing capture status

4. **Advanced Features**:
   - **Batch Selection**: Use "Select All", "Mobile Only", or "Desktop Only" buttons
   - **Save Logs**: Export capture logs for documentation
   - **About Page**: Access developer information and GitHub links
   - **History Management**: View previous captures and results

### Advanced Features

#### Performance Testing
- **Load Time Analysis**: Measure page load performance across devices
- **Mobile Performance**: Analyze mobile-specific performance metrics
- **Recommendations**: Get automatic optimization suggestions

#### Responsive Testing
- **Breakpoint Testing**: Test at common responsive breakpoints (320px, 768px, 1024px, 1440px)
- **Layout Analysis**: Detect horizontal scrolling, mobile menu presence
- **Font Size Analysis**: Check appropriate font sizes for different screen sizes

#### QA Analysis
- **Accessibility Check**: Validate alt text, heading structure, form labels
- **SEO Analysis**: Check title tags, meta descriptions, heading hierarchy
- **Color Contrast**: Basic color contrast validation

#### Reports & Export
- **HTML Reports**: Comprehensive visual reports with all screenshots
- **PDF Reports**: Printable reports with statistics and analysis
- **Screenshot Gallery**: Visual browsing of captured screenshots
- **History Management**: Track all previous captures with timestamps

## 📁 Project Structure

```
screenQA/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── start_screenqa.bat         # Windows launcher script
├── README.md                  # This file
├── src/                       # Source code modules
│   ├── screenshot_capture.py   # Core screenshot capture logic
│   ├── screenshot_management.py # Screenshot organization & reports
│   └── qa_features.py         # QA analysis features
├── config/                    # Configuration files
│   └── devices.json          # Device definitions and settings
├── screenshots/               # Captured screenshots (auto-created)
├── reports/                   # Generated reports (auto-created)
└── venv/                     # Virtual environment (auto-created)
```

## 🔧 Configuration

### Adding Custom Devices
Edit `config/devices.json` to add new device configurations:

```json
{
  "devices": {
    "Custom Device": {
      "width": 1366,
      "height": 768,
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      "platform": "Desktop",
      "description": "Custom Desktop Resolution"
    }
  }
}
```

### Customizing Settings
- **Screenshot Quality**: Modify Chrome options in `screenshot_capture.py`
- **Timeout Settings**: Adjust wait times for slow-loading sites
- **Output Formats**: Customize report templates in `screenshot_management.py`

## 📊 Example Workflow

### Responsive Design QA
1. Enter your website URL
2. Select "Mobile Only" devices for mobile testing
3. Capture screenshots
4. Use "QA Tools" > "Test Breakpoints" for responsive analysis
5. Generate HTML report for stakeholder review

### Performance Testing
1. Select representative devices (Desktop + Mobile)
2. Use "QA Tools" > "Test Load Time"
3. Review performance recommendations
4. Generate PDF report with metrics

### Accessibility Audit
1. Capture screenshots across all devices
2. Use built-in accessibility checker
3. Review alt text and heading structure issues
4. Export comprehensive accessibility report

## 🛠️ Dependencies

- **selenium**: Web browser automation
- **Pillow**: Image processing and manipulation
- **webdriver-manager**: Automatic ChromeDriver management
- **requests**: HTTP requests for URL validation
- **beautifulsoup4**: HTML parsing for analysis
- **matplotlib**: Performance charts and visualizations
- **reportlab**: PDF report generation

## 🔍 Troubleshooting

### Common Issues

**Chrome/ChromeDriver Issues**:
- Ensure Chrome browser is installed
- Application automatically downloads compatible ChromeDriver
- If issues persist, try updating Chrome browser

**Screenshot Failures**:
- Check internet connection
- Verify URL is accessible in browser
- Some sites may block automated access
- Try with different user agents

**Performance Issues**:
- Reduce number of simultaneous device captures
- Close other applications to free up memory
- For large sites, expect longer capture times

**GUI Issues**:
- Ensure tkinter is installed with Python
- On Linux: `sudo apt-get install python3-tk`
- Update display drivers if rendering issues occur

### Getting Help
1. Check the **Progress & Results** tab for detailed error messages
2. Review the **History** tab for successful configurations
3. Validate URLs before capturing to avoid network issues
4. Use fewer devices for testing if experiencing resource constraints

## 🎯 Use Cases

- **Web Development**: Test responsive designs across devices
- **QA Testing**: Automated visual regression testing
- **Client Presentations**: Generate professional QA reports
- **Performance Optimization**: Identify device-specific performance issues
- **Accessibility Compliance**: Basic accessibility validation
- **SEO Auditing**: Technical SEO analysis across device types

## 📈 Future Enhancements

- Visual difference detection between screenshots
- Integration with CI/CD pipelines
- Batch URL processing
- Advanced accessibility testing
- Performance budgeting and alerts
- Cloud screenshot storage
- Mobile app testing capabilities

## 📝 License

This project is open source and available under the MIT License.

## 🏗️ Building Executables

### Automatic Builds
The project includes GitHub Actions that automatically create executables for all platforms:
- **Windows**: `ScreenQA-Windows.exe`
- **Linux**: `ScreenQA-Linux`
- **macOS**: `ScreenQA-macOS.dmg`

Builds are triggered on:
- Push to main branch
- Pull requests 
- New releases

### Local Build
```bash
# Windows
build_executable.bat

# Linux/macOS  
chmod +x build_executable.sh
./build_executable.sh
```

For detailed build instructions, see [BUILD.md](BUILD.md).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- New device configurations
- Additional QA features
- Performance improvements
- Bug fixes
- Documentation improvements

---

**Made with ❤️ for the QA community**

*Simplifying cross-device website testing, one screenshot at a time.*
