@echo off

REM Force script to run in its own directory
cd /d "%~dp0"

REM Prevent window from closing on any error
if "%1" neq "internal" (
    cmd /k "cd /d "%~dp0" && "%~f0" internal"
    exit /b
)

REM AI Studio - Automated Setup Script for Windows
REM This script automates the complete installation process

echo.
echo ========================================
echo    AI Studio - Automated Setup
echo ========================================
echo.
echo This script will:
echo  1. Check system requirements
echo  2. Setup Python virtual environment
echo  3. Install Python dependencies
echo  4. Install PyTorch with CUDA support
echo  5. Setup Node.js frontend
echo  6. Verify installation
echo.
echo Press CTRL+C to cancel or
pause

REM ========================================
REM 1. SYSTEM CHECKS
REM ========================================

echo.
echo [1/6] Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10 or higher:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    goto :end_menu
)

echo [OK] Python found:
python --version

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo.
    echo Please install Node.js 18 or higher:
    echo https://nodejs.org/
    echo.
    pause
    goto :end_menu
)

echo [OK] Node.js found:
node --version

REM Check npm
call npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found!
    echo.
    echo npm should be installed with Node.js.
    echo.
    pause
    goto :end_menu
)

echo [OK] npm found:
call npm --version

REM Check Git (optional)
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Git not found (optional^)
) else (
    echo [OK] Git found:
    git --version
)

REM Check NVIDIA GPU
nvidia-smi >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] NVIDIA GPU or drivers not detected
    echo You can still use CPU, but it will be much slower.
    echo.
    choice /C YN /M "Continue without GPU support"
    if errorlevel 2 goto :end_menu
) else (
    echo [OK] NVIDIA GPU detected:
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
)

echo.
echo All system checks passed!
echo.
pause

REM ========================================
REM 2. BACKEND SETUP
REM ========================================

echo.
echo [2/6] Setting up Python backend...
echo.

cd backend
if %errorlevel% neq 0 (
    echo [ERROR] backend folder not found!
    pause
    goto :end_menu
)

REM Check if venv already exists
if exist "venv\" (
    echo Virtual environment already exists.
    choice /C YN /M "Delete and recreate"
    if errorlevel 2 (
        echo Keeping existing virtual environment...
    ) else (
        echo Deleting old virtual environment...
        rmdir /s /q venv
    )
)

REM Create virtual environment
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        cd ..
        pause
        goto :end_menu
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    cd ..
    pause
    goto :end_menu
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install base requirements
echo.
echo Installing Python dependencies...
echo This may take a few minutes...

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    cd ..
    pause
    goto :end_menu
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies!
    echo.
    echo Check the error messages above.
    cd ..
    pause
    goto :end_menu
)

echo [OK] Python dependencies installed
echo.

REM ========================================
REM 3. PYTORCH INSTALLATION
REM ========================================

echo.
echo [3/6] Installing PyTorch with CUDA support...
echo.

REM Detect GPU and suggest CUDA version
nvidia-smi >nul 2>&1
if %errorlevel% neq 0 (
    echo No NVIDIA GPU detected. Installing PyTorch for CPU...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
) else (
    echo NVIDIA GPU detected!
    echo.
    echo Which GPU series do you have?
    echo.
    echo 1. RTX 5090 / RTX 50-series (CUDA 12.8^)
    echo 2. RTX 4090 / RTX 40-series (CUDA 12.1^)
    echo 3. RTX 3090 / RTX 30-series (CUDA 11.8^)
    echo 4. CPU only (no GPU^)
    echo 5. Let me install manually later
    echo.
    choice /C 12345 /M "Select your GPU"
    
    if errorlevel 5 goto :install_pytorch_skip
    if errorlevel 4 goto :install_pytorch_cpu
    if errorlevel 3 goto :install_pytorch_cu118
    if errorlevel 2 goto :install_pytorch_cu121
    if errorlevel 1 goto :install_pytorch_cu128

    :install_pytorch_cu128
    echo Installing PyTorch for CUDA 12.8...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    goto :verify_pytorch

    :install_pytorch_cu121
    echo Installing PyTorch for CUDA 12.1...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    goto :verify_pytorch

    :install_pytorch_cu118
    echo Installing PyTorch for CUDA 11.8...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    goto :verify_pytorch

    :install_pytorch_cpu
    echo Installing PyTorch for CPU...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    goto :verify_pytorch

    :install_pytorch_skip
    echo.
    echo [SKIPPED] PyTorch installation skipped
    echo You can install manually later with:
    echo   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    goto :skip_pytorch
)

:verify_pytorch
REM Verify PyTorch installation
echo.
echo Verifying PyTorch installation...
python -c "import torch; print(f'PyTorch {torch.__version__} installed'); print(f'CUDA available: {torch.cuda.is_available()}')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] PyTorch verification failed
    echo You may need to install it manually
) else (
    echo [OK] PyTorch installed successfully
)

:skip_pytorch
cd ..

echo.
pause

REM ========================================
REM 4. FRONTEND SETUP
REM ========================================

echo.
echo [4/6] Setting up frontend...
echo.

cd frontend
if %errorlevel% neq 0 (
    echo [ERROR] frontend folder not found!
    cd ..
    pause
    goto :end_menu
)

REM Check if node_modules exists
if exist "node_modules\" (
    echo node_modules already exists.
    choice /C YN /M "Delete and reinstall"
    if errorlevel 2 (
        echo Keeping existing node_modules...
        goto :skip_npm_install
    ) else (
        echo Deleting old node_modules...
        rmdir /s /q node_modules
    )
)

echo Installing Node.js dependencies...
echo This may take 5-10 minutes...
echo.

call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js dependencies!
    echo.
    echo Try manually:
    echo   cd frontend
    echo   npm install
    echo.
    cd ..
    pause
    goto :end_menu
)

:skip_npm_install
echo [OK] Node.js dependencies installed

cd ..

echo.
pause

REM ========================================
REM 5. RUST CHECK (for Tauri)
REM ========================================

echo.
echo [5/6] Checking Rust installation (required for Tauri^)...
echo.

set RUST_MISSING=

rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Rust not found!
    echo.
    echo Rust is required for Tauri (the desktop framework^).
    echo.
    echo To install Rust:
    echo 1. Visit: https://rustup.rs/
    echo 2. Download and run rustup-init.exe
    echo 3. Follow the installation prompts
    echo 4. Restart this terminal
    echo 5. Run setup.bat again
    echo.
    echo Or install now? This will open your browser.
    choice /C YN /M "Open Rust installer website"
    if errorlevel 1 (
        start https://rustup.rs/
    )
    echo.
    echo [IMPORTANT] After installing Rust, restart your terminal and run setup.bat again!
    echo.
    set RUST_MISSING=1
) else (
    echo [OK] Rust found:
    rustc --version
    cargo --version
)

REM Check for Visual Studio Build Tools (Windows)
echo.
echo Checking for Visual Studio Build Tools...
where cl.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Visual Studio Build Tools not detected
    echo.
    echo These are required for Rust compilation on Windows.
    echo.
    echo To install:
    echo 1. Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo 2. Install "Desktop development with C++"
    echo 3. Restart your terminal
    echo.
    choice /C YN /M "Open Visual Studio Build Tools website"
    if errorlevel 1 (
        start https://visualstudio.microsoft.com/visual-cpp-build-tools/
    )
) else (
    echo [OK] Visual Studio Build Tools found
)

echo.
pause

REM ========================================
REM 6. FINAL VERIFICATION
REM ========================================

echo.
echo [6/6] Final verification...
echo.

set SETUP_FAILED=

REM Check backend setup
if not exist "backend\venv\" (
    echo [ERROR] Backend virtual environment not found!
    set SETUP_FAILED=1
) else (
    echo [OK] Backend virtual environment exists
)

REM Check frontend setup
if not exist "frontend\node_modules\" (
    echo [ERROR] Frontend node_modules not found!
    set SETUP_FAILED=1
) else (
    echo [OK] Frontend dependencies installed
)

REM Check if Rust is available
rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Rust not installed (required for desktop app^)
    set RUST_MISSING=1
) else (
    echo [OK] Rust is installed
)

REM Create models directory structure if it doesn't exist
if not exist "models\" (
    echo Creating models directory...
    mkdir models
    echo [OK] models directory created
) else (
    echo [OK] models directory exists
)

echo.
echo ========================================

if defined SETUP_FAILED (
    echo.
    echo [SETUP INCOMPLETE]
    echo.
    echo Some components failed to install.
    echo Please check the error messages above and try again.
    echo.
    echo You can also try manual installation:
    echo - Backend: See README.md section "Backend Setup"
    echo - Frontend: See README.md section "Frontend Setup"
    echo.
    pause
    goto :end_menu
)

if defined RUST_MISSING (
    echo.
    echo [SETUP ALMOST COMPLETE]
    echo.
    echo Backend and Frontend are ready!
    echo.
    echo However, Rust is not installed yet.
    echo You need Rust to build the desktop app.
    echo.
    echo After installing Rust:
    echo 1. Restart your terminal
    echo 2. Run: cd frontend
    echo 3. Run: npm run tauri dev
    echo.
    pause
    goto :end_menu
)

echo.
echo [SETUP COMPLETE!]
echo.
echo ========================================
echo    Installation Summary
echo ========================================
echo.
echo Backend:  Ready (Python + PyTorch^)
echo Frontend: Ready (Node.js + React^)
echo Desktop:  Ready (Rust + Tauri^)
echo.
echo Have fun generating AI art with your RTX 5090! 🚀
echo.

:end_menu
cls
echo.
echo ========================================
echo    AI STUDIO - SETUP COMPLETE
echo ========================================
echo.
echo Installation successful! Backend and Frontend are ready.
echo.
echo ========================================
echo    QUICK ACTIONS
echo ========================================
echo.
echo 1. Start AI Studio (automatic^)
echo 2. Start Backend only
echo 3. Start Frontend only
echo 4. Open project folder
echo 5. View system info
echo 6. Exit
echo.
echo ========================================
echo.

choice /C 123456 /N /M "Select option [1-6]: "

if errorlevel 6 goto :exit_script
if errorlevel 5 goto :action_system_info
if errorlevel 4 goto :action_open_folder
if errorlevel 3 goto :action_start_frontend
if errorlevel 2 goto :action_start_backend
if errorlevel 1 goto :action_start_all

:action_start_all
    echo.
    echo Starting AI Studio...
    echo This will open two terminal windows.
    echo.
    timeout /t 2 >nul
    if exist "start.bat" (
        call start.bat
    ) else (
        echo [ERROR] start.bat not found!
        pause
    )
    goto :end_menu_loop

:action_start_backend
    echo.
    echo Starting Backend only...
    echo.
    start cmd /k "cd backend && venv\Scripts\activate && python main.py"
    goto :end_menu_loop

:action_start_frontend
    echo.
    echo Starting Frontend only...
    echo.
    start cmd /k "cd frontend && call npm run tauri dev"
    goto :end_menu_loop

:action_open_folder
    echo.
    echo Opening project folder...
    start .
    goto :end_menu_loop

:action_system_info
    cls
    echo.
    echo ========================================
    echo    SYSTEM INFORMATION
    echo ========================================
    echo.
    echo Python Version:
    python --version
    echo.
    echo Node.js Version:
    node --version
    echo.
    echo npm Version:
    call npm --version
    echo.
    echo Rust Version:
    rustc --version 2>nul || echo Rust not installed
    echo.
    echo GPU Information:
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader 2>nul || echo No NVIDIA GPU detected
    echo.
    echo ========================================
    echo.
    pause
    goto :end_menu

:end_menu_loop
goto :end_menu

:exit_script
echo.
echo ========================================
echo    Thank you for using AI Studio!
echo ========================================
echo.
echo Closing in 3 seconds...
timeout /t 3 >nul
exit
