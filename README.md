# ScreenQA - Website Screenshot Testing Tool

![ScreenQA Logo](https://img.shields.io/badge/ScreenQA-Website%20Testing-blue?style=for-the-badge&logo=selenium)

A comprehensive Python application with a simple GUI for capturing website screenshots across different device sizes and platforms for easy QA testing. Perfect for testing responsive designs, cross-device compatibility, and generating detailed QA reports.

## 🚀 Features

### Core Functionality
- **Multi-Device Screenshot Capture**: Capture screenshots across 15+ predefined device configurations
- **Real Browser Automation**: Uses Selenium WebDriver for authentic browser rendering
- **Responsive Design Testing**: Test websites at different breakpoints and resolutions
- **Performance Analysis**: Measure load times and performance metrics across devices

### Device Support
- **Desktop**: Windows (1920x1080), Mac (1440x900), MacBook Pro 13" & 16"
- **Mobile**: iPhone 15 Pro Max, iPhone 15, iPhone SE, Samsung Galaxy S24 Ultra/S24, Google Pixel 8 Pro
- **Tablets**: iPad Pro 12.9", iPad Air, Samsung Galaxy Tab S9, Generic Tablet

### QA Features
- **Screenshot Gallery**: Visual gallery with thumbnails and organization
- **Comparison Tools**: Side-by-side screenshot comparison
- **Performance Testing**: Load time analysis and optimization recommendations
- **Accessibility Checking**: Basic accessibility validation (alt text, headings, contrast)
- **SEO Analysis**: Title tags, meta descriptions, heading structure analysis
- **Responsive Breakpoint Testing**: Test common responsive breakpoints
- **HTML & PDF Reports**: Generate comprehensive QA reports

### User Interface
- **Simple Tkinter GUI**: Easy-to-use interface, no web server required
- **Progress Tracking**: Real-time progress updates during capture
- **History Management**: View and manage screenshot history
- **Batch Operations**: Capture multiple devices simultaneously
- **Export Options**: Save screenshots and generate reports

## 📋 Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Chrome Browser**: Required for Selenium WebDriver
- **Internet Connection**: For downloading ChromeDriver and accessing websites

## ⚡ Quick Start

### Option 1: Easy Start (Windows)
1. **Download/Clone** this repository
2. **Double-click** `start_screenqa.bat`
3. The script will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Launch the application

### Option 2: Manual Installation
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

## 🖥️ Usage Guide

### Basic Screenshot Capture
1. **Enter URL**: Type or paste the website URL you want to test
2. **Select Devices**: Choose from 15+ predefined device configurations
   - Use "Select All" for comprehensive testing
   - Use "Mobile Only" or "Desktop Only" for focused testing
3. **Validate URL**: Click "Validate" to check if the URL is accessible
4. **Capture Screenshots**: Click "Capture Screenshots" to start the process
5. **View Results**: Screenshots appear in the Results tab with status and file information

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
