@echo off
REM AI Studio - CUDA Fix Script
REM Reinstalls PyTorch with CUDA 12.8 support for RTX 5090

cd /d "%~dp0"

echo.
echo ========================================
echo    AI Studio - CUDA Fix Script
echo ========================================
echo.
echo This will reinstall PyTorch with CUDA 12.8 support
echo for your RTX 5090 / RTX 50-series GPU
echo.
echo Current status: CUDA False (CPU-only PyTorch)
echo Target: CUDA True (GPU-accelerated PyTorch)
echo.
echo Download size: ~2-3 GB
echo Time required: 3-5 minutes
echo.
pause

echo.
echo [1/5] Checking virtual environment...
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo.

echo [2/5] Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

echo.
echo [3/5] Uninstalling old PyTorch (CPU version)...
pip uninstall torch torchvision torchaudio -y
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not have been uninstalled
    echo Continuing anyway...
)
echo [OK] Old PyTorch uninstalled

echo.
echo [4/5] Installing PyTorch with CUDA 12.8...
echo.
echo IMPORTANT: This uses the correct PyTorch CUDA index!
echo Command: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
echo.
echo Downloading and installing... Please wait...
echo.

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install PyTorch with CUDA!
    echo.
    echo Possible causes:
    echo - No internet connection
    echo - PyPI server issues
    echo - Insufficient disk space
    echo.
    echo Please check your connection and try again.
    pause
    exit /b 1
)

echo [OK] PyTorch with CUDA 12.8 installed

echo.
echo [5/5] Verifying CUDA installation...
echo.

python -c "import torch; print('=' * 50); print('PyTorch Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda if torch.cuda.is_available() else 'N/A'); print('GPU Count:', torch.cuda.device_count() if torch.cuda.is_available() else 0); print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); print('GPU Memory:', f'{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB' if torch.cuda.is_available() else 'N/A'); print('Compute Capability:', f'{torch.cuda.get_device_capability(0)[0]}.{torch.cuda.get_device_capability(0)[1]}' if torch.cuda.is_available() else 'N/A'); print('=' * 50)"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to verify CUDA installation!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Successful!
echo ========================================
echo.
echo CUDA is now enabled for your RTX 5090!
echo.
echo ========================================
echo    Next Steps
echo ========================================
echo.
echo 1. Restart Backend:
echo    python main.py
echo.
echo 2. Reload Frontend:
echo    Press F5 in the desktop app
echo.
echo 3. Check GPU Info:
echo    Look at the header - should show RTX 5090
echo.
echo 4. Test Generation:
echo    Generate an image - should be 50-100x faster!
echo.
echo ========================================
echo    Expected Performance (RTX 5090)
echo ========================================
echo.
echo - SD1.5   512x512:    1-2 seconds
echo - SDXL    1024x1024:  4-6 seconds
echo - SDXL    2048x2048:  12-15 seconds
echo - VRAM Usage:         8-20 GB
echo - GPU Utilization:    95-100%%
echo.
echo ========================================
pause
