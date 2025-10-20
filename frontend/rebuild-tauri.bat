@echo off
REM Rebuild Tauri with Dialog Plugin
REM This script rebuilds the Tauri app after adding the dialog plugin

echo.
echo ========================================
echo    Rebuilding Tauri with Dialog Plugin
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Cleaning old build files...
if exist "src-tauri\target\" (
    echo Removing old target directory...
    rmdir /s /q "src-tauri\target"
)
echo [OK] Clean complete

echo.
echo [2/3] Updating Rust dependencies...
cd src-tauri
cargo fetch
if %errorlevel% neq 0 (
    echo [ERROR] Failed to fetch Rust dependencies!
    cd ..
    pause
    exit /b 1
)
echo [OK] Dependencies fetched

echo.
echo [3/3] Building Tauri app...
echo This may take 5-10 minutes on first build...
echo.
cd ..
call npm run tauri build
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Build failed or was interrupted
    echo.
    echo You can also run the dev server to test:
    echo   npm run tauri dev
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo The dialog plugin is now integrated.
echo You can now use the file picker for LoRAs.
echo.
pause
