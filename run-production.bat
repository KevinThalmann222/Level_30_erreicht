@echo off
REM Production startup script for David's 30th Birthday Party application (Windows)

echo.
echo 🎉 Starting David's 30th Birthday Party - Production Deployment
echo ===============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9 or later.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade production dependencies
echo 📥 Installing production dependencies...
python -m pip install --upgrade pip
pip install -r requirements-prod.txt

REM Load environment configuration
if exist ".env.production" (
    echo 📄 Loading production environment from .env.production...
    for /f "tokens=*" %%i in (type .env.production ^| findstr /v "^#") do set %%i
) else (
    echo ⚠️  .env.production not found. Using default configuration.
)

REM Set production mode
set FLASK_ENV=production
set FLASK_DEBUG=False

REM Generate secure SECRET_KEY if not set
if "%SECRET_KEY%"=="" (
    echo 🔐 Generating secure SECRET_KEY...
    for /f "tokens=*" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY=%%i
    echo    Generated: %SECRET_KEY%
    echo    Add this to .env.production for consistency across restarts
)

REM Number of Gunicorn workers (4x CPU cores recommended)
if "%GUNICORN_WORKERS%"=="" set GUNICORN_WORKERS=4
if "%FLASK_HOST%"=="" set FLASK_HOST=0.0.0.0
if "%FLASK_PORT%"=="" set FLASK_PORT=5000

echo.
echo 🚀 Launching Gunicorn with configuration:
echo    Workers: %GUNICORN_WORKERS%
echo    Host: %FLASK_HOST%
echo    Port: %FLASK_PORT%
echo    Environment: production
echo.
echo 📌 Access the application at: http://%FLASK_HOST%:%FLASK_PORT%
echo 📌 Press Ctrl+C to stop the server
echo.

REM Start Gunicorn
gunicorn ^
    --workers=%GUNICORN_WORKERS% ^
    --worker-class=sync ^
    --bind=%FLASK_HOST%:%FLASK_PORT% ^
    --timeout=120 ^
    --access-logfile=- ^
    --error-logfile=- ^
    --log-level=info ^
    app:app

pause
