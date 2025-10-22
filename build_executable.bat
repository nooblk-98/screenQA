@echo off
REM Windows build script for ScreenQA executable
setlocal enabledelayedexpansion

echo 🚀 Building ScreenQA Executable...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 📦 Installing PyInstaller...
    python -m pip install pyinstaller
)

REM Create assets directory if it doesn't exist
if not exist "assets\" mkdir assets

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist
if exist "__pycache__\" rmdir /s /q __pycache__
del *.spec 2>nul

REM Build using the spec file if it exists, otherwise use direct command
if exist "ScreenQA.spec" (
    echo 📋 Using ScreenQA.spec file for build...
    python -m PyInstaller ScreenQA.spec
) else (
    echo 📋 Building with direct PyInstaller command...
    python -m PyInstaller --onefile --windowed --name "ScreenQA" main.py
)

REM Check if build was successful
if exist "dist\ScreenQA.exe" (
    echo ✅ Build successful!
    echo 📁 Executable location: dist\
    dir dist\
    
    echo.
    echo 🎯 Build Summary:
    echo    • Platform: Windows
    python --version
    echo    • Executable: dist\ScreenQA.exe
    
    REM Get file size
    for %%A in (dist\ScreenQA.exe) do (
        set /a size=%%~zA/1024/1024
        echo    • Size: !size! MB
    )
    
    echo.
    echo 🧪 Running build validation test...
    python test_build.py
    
    echo.
    echo 🏃 To run the executable:
    echo    dist\ScreenQA.exe
    
) else (
    echo ❌ Build failed!
    echo Check the output above for errors.
    exit /b 1
)

pause