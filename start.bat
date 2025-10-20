@echo off
REM AI Studio Startup Script for Windows

echo ====================================
echo    AI Studio Startup
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv\" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please setup backend first:
    echo 1. cd backend
    echo 2. python -m venv venv
    echo 3. venv\Scripts\activate
    echo 4. pip install -r requirements.txt
    echo 5. pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    echo.
    pause
    exit /b 1
)

REM Check if Node modules exist
if not exist "frontend\node_modules\" (
    echo [ERROR] Frontend dependencies not found!
    echo.
    echo Please setup frontend first:
    echo 1. cd frontend
    echo 2. npm install
    echo.
    pause
    exit /b 1
)

REM Start backend in new window
echo [1/3] Starting Backend...
start "AI Studio Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python main.py"

REM Wait for backend to initialize
echo [2/3] Waiting for backend to start...
timeout /t 8 /nobreak >nul

REM Test backend connection
echo [3/3] Testing backend connection...
curl -s http://127.0.0.1:8000/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Backend may not be ready yet. Check the Backend window for errors.
    echo.
    pause
)

REM Start frontend
echo.
echo Starting Frontend (Tauri)...
echo This may take a few minutes on first run (Rust compilation)...
echo.
cd frontend
call npm run tauri dev

pause
