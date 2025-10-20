@echo off
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
    exit /b 1
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
    exit /b 1
)

echo [OK] Node.js found:
node --version

REM Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found!
    echo.
    echo npm should come with Node.js. Please reinstall Node.js.
    echo.
    pause
    exit /b 1
)

echo [OK] npm found:
npm --version

REM Check Git (optional)
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Git not found (optional)
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
    if errorlevel 2 exit /b 1
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
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install base requirements
echo.
echo Installing Python dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies!
    pause
    exit /b 1
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
if %errorlevel% equ 0 (
    echo NVIDIA GPU detected!
    echo.
    echo Which GPU series do you have?
    echo.
    echo 1. RTX 5090 / RTX 50-series (CUDA 12.8)
    echo 2. RTX 4090 / RTX 40-series (CUDA 12.1)
    echo 3. RTX 3090 / RTX 30-series (CUDA 11.8)
    echo 4. CPU only (no GPU)
    echo 5. Let me install manually later
    echo.
    choice /C 12345 /M "Select your GPU"
    
    if errorlevel 5 (
        echo.
        echo [SKIPPED] PyTorch installation skipped
        echo You can install manually later with:
        echo   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
        goto :skip_pytorch
    )
    if errorlevel 4 (
        echo Installing PyTorch for CPU...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    )
    if errorlevel 3 (
        echo Installing PyTorch for CUDA 11.8...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    )
    if errorlevel 2 (
        echo Installing PyTorch for CUDA 12.1...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    )
    if errorlevel 1 (
        echo Installing PyTorch for CUDA 12.8...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    )
) else (
    echo No NVIDIA GPU detected. Installing PyTorch for CPU...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
)

:skip_pytorch

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyTorch!
    echo.
    echo You can install manually later with:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    echo.
    pause
)

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
    pause
    exit /b 1
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
echo [5/6] Checking Rust installation (required for Tauri)...
echo.

rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Rust not found!
    echo.
    echo Rust is required for Tauri (the desktop framework).
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
    pause
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
    echo [WARNING] Rust not installed (required for desktop app)
    set RUST_MISSING=1
) else (
    echo [OK] Rust is installed
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
    exit /b 1
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
    exit /b 0
)

echo.
echo [SETUP COMPLETE!]
echo.
echo ========================================
echo    Installation Summary
echo ========================================
echo.
echo Backend:  Ready (Python + PyTorch)
echo Frontend: Ready (Node.js + React)
echo Desktop:  Ready (Rust + Tauri)
echo.
echo ========================================
echo    Next Steps
echo ========================================
echo.
echo Start the application:
echo.
echo Option 1 - Separate terminals (Recommended):
echo   Terminal 1:  cd backend  ^&^& run.bat
echo   Terminal 2:  cd frontend ^&^& run.bat
echo.
echo Option 2 - Automatic start:
echo   start.bat
echo.
echo ========================================
echo.
echo First run will take 5-10 minutes (Rust compilation)
echo Subsequent runs will be much faster!
echo.
echo For help, see:
echo - README.md
echo - QUICKSTART.md
echo - TROUBLESHOOTING.md
echo.
echo Have fun generating AI art with your RTX 5090! 🚀
echo.
pause
