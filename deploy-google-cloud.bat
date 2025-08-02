@echo off
echo ================================================================
echo         🚀 PyCBA Google Cloud Deployment Script 🚀
echo ================================================================
echo.
echo This script will deploy your PyCBA application to Google Cloud Run
echo.

echo [1/8] Checking Google Cloud CLI installation...
gcloud version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Google Cloud CLI is not installed
    echo.
    echo Please install it from: https://cloud.google.com/sdk/docs/install
    echo After installation, run: gcloud auth login
    pause
    exit /b 1
)
echo ✓ Google Cloud CLI is installed

echo.
echo [2/8] Checking authentication...
gcloud auth list --filter=status:ACTIVE --format="value(account)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not authenticated with Google Cloud
    echo Running authentication...
    gcloud auth login
)
echo ✓ Authenticated with Google Cloud

echo.
echo [3/8] Setting up project...
set /p PROJECT_ID="Enter your Google Cloud Project ID (or press Enter for default): "
if "%PROJECT_ID%"=="" (
    set PROJECT_ID=pycba-app
    echo Using default project ID: %PROJECT_ID%
)

gcloud config set project %PROJECT_ID%
echo ✓ Project set to: %PROJECT_ID%

echo.
echo [4/8] Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
echo ✓ APIs enabled

echo.
echo [5/8] Building container image...
gcloud builds submit --tag gcr.io/%PROJECT_ID%/pycba-app --file=Dockerfile.gcloud .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build container image
    pause
    exit /b 1
)
echo ✓ Container image built successfully

echo.
echo [6/8] Deploying to Cloud Run...
gcloud run deploy pycba-app ^
    --image gcr.io/%PROJECT_ID%/pycba-app ^
    --platform managed ^
    --region asia-southeast1 ^
    --allow-unauthenticated ^
    --memory=1Gi ^
    --cpu=1 ^
    --port=8080 ^
    --max-instances=10

if %errorlevel% neq 0 (
    echo ERROR: Failed to deploy to Cloud Run
    pause
    exit /b 1
)

echo.
echo [7/8] Getting service URL...
for /f "tokens=*" %%i in ('gcloud run services describe pycba-app --platform managed --region asia-southeast1 --format="value(status.url)"') do set SERVICE_URL=%%i

echo.
echo [8/8] Setting up custom domain (optional)...
echo If you want to use a custom domain, follow these steps:
echo 1. Go to Google Cloud Console ^> Cloud Run ^> Manage Custom Domains
echo 2. Map your domain to the service
echo 3. Update your DNS records

echo.
echo ================================================================
echo                🎉 DEPLOYMENT SUCCESSFUL! 🎉
echo ================================================================
echo.
echo Your PyCBA application is now live at:
echo    🌐 %SERVICE_URL%
echo.
echo Features:
echo    ✓ Auto-scaling (0 to 10 instances)
echo    ✓ HTTPS enabled by default
echo    ✓ Global CDN
echo    ✓ 99.95%% uptime SLA
echo.
echo Management commands:
echo    View logs:    gcloud run services logs read pycba-app --region=asia-southeast1
echo    Update app:   gcloud run deploy pycba-app --image gcr.io/%PROJECT_ID%/pycba-app
echo    Delete app:   gcloud run services delete pycba-app --region=asia-southeast1
echo.
echo Monthly cost estimate: $0-10 USD (depending on usage)
echo ================================================================

echo Opening application...
start %SERVICE_URL%

echo.
echo Press any key to exit...
pause >nul
