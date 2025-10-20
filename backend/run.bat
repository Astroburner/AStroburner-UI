@echo off
REM Direct Backend Startup Script for Windows

echo ====================================
echo    AI Studio Backend
echo ====================================
echo.

REM Change to backend directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

REM Check Python and PyTorch
echo [INFO] Checking Python and PyTorch installation...
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] PyTorch not installed correctly!
    echo.
    echo Please install PyTorch:
    echo   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================
echo    Starting FastAPI Server
echo ====================================
echo.
echo Server will run on: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

REM Start the server
python main.py

pause
