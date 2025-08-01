@echo off
echo ================================================================
echo           PyCBA Continuous Beam Analysis - Deployment
echo ================================================================
echo.

echo [1/6] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✓ Docker is installed

echo.
echo [2/6] Checking Docker service...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker service is not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)
echo ✓ Docker service is running

echo.
echo [3/6] Building Docker image...
docker build -t pycba-app .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build Docker image
    pause
    exit /b 1
)
echo ✓ Docker image built successfully

echo.
echo [4/6] Stopping existing containers...
docker-compose down 2>nul

echo.
echo [5/6] Starting application...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start application
    pause
    exit /b 1
)

echo.
echo [6/6] Waiting for application to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ================================================================
echo                    🎉 DEPLOYMENT SUCCESSFUL! 🎉
echo ================================================================
echo.
echo Your PyCBA Continuous Beam Analysis application is now running at:
echo.
echo    ➤ Local:    http://localhost:8501
echo    ➤ Network:  http://YOUR_IP:8501
echo.
echo To view logs:        docker-compose logs -f
echo To stop:            docker-compose down
echo To restart:         docker-compose restart
echo.
echo ================================================================

echo Opening application in browser...
start http://localhost:8501

echo.
echo Press any key to exit...
pause >nul
