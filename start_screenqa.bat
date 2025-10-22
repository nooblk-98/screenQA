@echo off
echo Starting ScreenQA Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Navigate to the application directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements if needed
if not exist "venv\Lib\site-packages\selenium\" (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Start the application
echo Starting ScreenQA...
echo.
python main.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error. Press any key to continue...
    pause >nul
)

deactivate