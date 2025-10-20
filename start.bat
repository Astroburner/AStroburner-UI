@echo off
REM AI Studio Startup Script for Windows

echo Starting AI Studio...

REM Check if virtual environment exists
if not exist "backend\venv\" (
    echo Virtual environment not found!
    echo Run: cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Start backend in new window
echo Starting Backend...
start "AI Studio Backend" cmd /k "cd backend && venv\Scripts\activate && python main.py"

REM Wait for backend
echo Waiting for backend to start...
timeout /t 5 /nobreak

REM Start frontend
echo Starting Frontend...
cd frontend
call npm run tauri dev

pause
