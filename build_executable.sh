#!/bin/bash
# Local build script for ScreenQA executable

echo "🚀 Building ScreenQA Executable..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Create assets directory if it doesn't exist
mkdir -p assets

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ __pycache__/ *.spec

# Build using the spec file if it exists, otherwise use direct command
if [ -f "ScreenQA.spec" ]; then
    echo "📋 Using ScreenQA.spec file for build..."
    pyinstaller ScreenQA.spec
else
    echo "📋 Building with direct PyInstaller command..."
    pyinstaller --onefile --windowed --name "ScreenQA" main.py
fi

# Check if build was successful
if [ -f "dist/ScreenQA" ] || [ -f "dist/ScreenQA.exe" ]; then
    echo "✅ Build successful!"
    echo "📁 Executable location: dist/"
    ls -la dist/
    
    echo ""
    echo "🎯 Build Summary:"
    echo "   • Platform: $(uname -s)"
    echo "   • Python: $(python --version)"
    echo "   • Executable: dist/ScreenQA$([ "$(uname -s)" = "MINGW64_NT" ] && echo ".exe" || echo "")"
    
    # Get file size
    if [ -f "dist/ScreenQA.exe" ]; then
        SIZE=$(stat -c%s "dist/ScreenQA.exe" 2>/dev/null || stat -f%z "dist/ScreenQA.exe" 2>/dev/null)
    else
        SIZE=$(stat -c%s "dist/ScreenQA" 2>/dev/null || stat -f%z "dist/ScreenQA" 2>/dev/null)
    fi
    
    if [ ! -z "$SIZE" ]; then
        echo "   • Size: $(($SIZE / 1024 / 1024)) MB"
    fi
    
    echo ""
    echo "🏃 To run the executable:"
    if [ -f "dist/ScreenQA.exe" ]; then
        echo "   ./dist/ScreenQA.exe"
    else
        echo "   ./dist/ScreenQA"
    fi
    
else
    echo "❌ Build failed!"
    echo "Check the output above for errors."
    exit 1
fi