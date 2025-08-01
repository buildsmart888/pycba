@echo off
echo ================================================================
echo     PyCBA Continuous Beam Analysis - Local Deployment
echo ================================================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python is installed

echo.
echo [2/4] Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else (
    echo WARNING: Virtual environment not found, using system Python
)

echo.
echo [3/4] Installing/updating dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [4/4] Starting Streamlit application...
echo.
echo ================================================================
echo                🚀 LAUNCHING APPLICATION! 🚀
echo ================================================================
echo.
echo Your PyCBA Continuous Beam Analysis application will open at:
echo    ➤ http://localhost:8501
echo.
echo To stop the application: Press Ctrl+C in this window
echo ================================================================
echo.

streamlit run advanced_app.py --server.port=8501 --server.address=localhost
