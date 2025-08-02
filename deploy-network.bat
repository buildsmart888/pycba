@echo off
echo ========================================
echo   PyCBA Suite - Local Network Deploy
echo ========================================

echo.
echo Checking Python virtual environment...
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Getting local IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set "ip=%%a"
    goto :found
)
:found
set ip=%ip: =%

echo.
echo ========================================
echo   Starting PyCBA Suite Server
echo ========================================
echo.
echo Local access: http://localhost:8501
echo Network access: http://%ip%:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================

streamlit run home.py --server.address 0.0.0.0 --server.port 8501
