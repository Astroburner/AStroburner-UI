@echo off
REM Direct Frontend Startup Script for Windows

echo ====================================
echo    AI Studio Frontend
echo ====================================
echo.

REM Change to frontend directory
cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [ERROR] Dependencies not installed!
    echo.
    echo Please run setup first:
    echo   npm install
    echo.
    pause
    exit /b 1
)

echo [INFO] Checking backend connection...
curl -s http://127.0.0.1:8000/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Backend is not running!
    echo.
    echo Please start backend first:
    echo   1. Open new terminal
    echo   2. cd backend
    echo   3. venv\Scripts\activate
    echo   4. python main.py
    echo.
    echo Or use: backend\run.bat
    echo.
    pause
)

echo.
echo ====================================
echo    Starting Tauri Dev
echo ====================================
echo.
echo NOTE: First run may take 5-10 minutes (Rust compilation)
echo.
echo Frontend will be available at: http://localhost:3000
echo Desktop app will open automatically
echo.

REM Start Tauri dev server
call npm run tauri dev

pause
