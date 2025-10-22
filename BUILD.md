# ScreenQA Build Instructions

This document explains how to build ScreenQA as a standalone executable.

## 🚀 Automated Builds (GitHub Actions)

The project includes GitHub Actions that automatically build executables for Windows, Linux, and macOS:

### Triggers
- **Push to main branch**: Creates development builds
- **Pull requests**: Creates test builds  
- **Releases**: Creates release builds and uploads to GitHub Releases

### Artifacts
- **Windows**: `ScreenQA-Windows.exe`
- **Linux**: `ScreenQA-Linux`
- **macOS**: `ScreenQA-macOS.dmg`

### Downloading Builds
1. Go to the [Actions tab](https://github.com/nooblk-98/screenQA/actions)
2. Click on the latest successful build
3. Download the artifact for your platform

## 🛠️ Local Build

### Prerequisites
```bash
pip install pyinstaller
pip install -r requirements.txt
```

### Quick Build

#### Windows
```bash
build_executable.bat
```

#### Linux/macOS
```bash
chmod +x build_executable.sh
./build_executable.sh
```

### Manual Build

#### Basic Build
```bash
pyinstaller --onefile --windowed --name "ScreenQA" main.py
```

#### Advanced Build (using spec file)
```bash
pyinstaller ScreenQA.spec
```

## 📁 Build Configuration

### PyInstaller Spec File
The `ScreenQA.spec` file provides advanced build configuration:
- Includes all necessary data files
- Hidden imports for dependencies
- Icon configuration
- Windowed mode (no console)

### Build Files Structure
```
ScreenQA/
├── .github/workflows/       # GitHub Actions
├── assets/                  # Icons and resources
├── build/                   # Build cache (auto-generated)
├── dist/                    # Output executables
├── ScreenQA.spec           # PyInstaller configuration
├── build_executable.bat    # Windows build script
└── build_executable.sh     # Linux/macOS build script
```

## 🎯 Platform-Specific Notes

### Windows
- Output: `dist/ScreenQA.exe`
- Includes Chrome driver support
- Windowed mode (no console)
- Optional icon support

### Linux
- Output: `dist/ScreenQA`
- Requires system Chrome installation
- Includes tkinter dependencies
- Console mode for debugging

### macOS  
- Output: `dist/ScreenQA`
- Creates `.app` bundle
- Optional DMG creation
- Signed for distribution

## 🔧 Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
# Install all requirements
pip install -r requirements.txt
pip install pyinstaller pillow
```

#### Chrome Driver Issues
- Windows: Auto-installs via Chocolatey in CI
- Linux: Install `google-chrome-stable`
- macOS: Install via `brew install --cask google-chrome`

#### Import Errors
Check `hiddenimports` in `ScreenQA.spec` for missing modules.

#### Large File Size
The executable includes Python runtime and all dependencies (~50-100MB is normal).

### Debug Mode
To enable console for debugging:
```python
# In ScreenQA.spec, change:
console=True  # Shows console window
```

## 📊 Build Status

### GitHub Actions Status
[![Build Status](https://github.com/nooblk-98/screenQA/workflows/Build%20ScreenQA%20Executable/badge.svg)](https://github.com/nooblk-98/screenQA/actions)

### Latest Releases
Check the [Releases page](https://github.com/nooblk-98/screenQA/releases) for the latest stable builds.

## 🚢 Distribution

### GitHub Releases
1. Create a new release tag (e.g., `v1.0.0`)
2. GitHub Actions automatically builds and uploads executables
3. Users can download from the Releases page

### Manual Distribution
1. Build locally using the scripts
2. Test the executable thoroughly
3. Package with any additional files needed
4. Distribute via your preferred method

## 📝 Development

### Testing Builds Locally
```bash
# After building
cd dist

# Windows
ScreenQA.exe

# Linux/macOS
./ScreenQA
```

### Modifying Build Configuration
1. Edit `ScreenQA.spec` for advanced settings
2. Update build scripts for new dependencies
3. Test locally before committing
4. GitHub Actions will pick up changes automatically