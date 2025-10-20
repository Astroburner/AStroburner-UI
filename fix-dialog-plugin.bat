@echo off
REM Quick Fix for Dialog Plugin Error
REM Stops app, rebuilds Tauri, and restarts

echo.
echo ========================================
echo    Dialog Plugin Quick Fix
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Stopping running applications...
echo.

REM Kill backend
taskkill /F /IM python.exe 2>nul
echo Backend stopped

REM Kill frontend (Tauri)
taskkill /F /IM ai-studio.exe 2>nul
echo Frontend stopped

echo.
echo [2/4] Cleaning Tauri build cache...
cd frontend\src-tauri
if exist "target\" (
    echo Removing old build cache...
    rmdir /s /q "target"
    echo [OK] Cache cleared
) else (
    echo [OK] No cache to clear
)
cd ..\..

echo.
echo [3/4] Rebuilding Tauri with Dialog Plugin...
echo This will take 5-10 minutes (Rust compilation)
echo.
cd frontend
call npm run tauri build

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo    Build Failed
    echo ========================================
    echo.
    echo Try running dev mode instead:
    echo   cd frontend
    echo   npm run tauri dev
    echo.
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo [4/4] Starting AI Studio...
echo.
timeout /t 2 >nul

if exist "start.bat" (
    call start.bat
) else (
    echo Starting manually...
    start cmd /k "cd backend && venv\Scripts\activate && python main.py"
    timeout /t 3 >nul
    start cmd /k "cd frontend && npm run tauri dev"
)

echo.
echo ========================================
echo    Fix Complete!
echo ========================================
echo.
echo The dialog plugin is now working.
echo Try clicking "Durchsuchen" again!
echo.
pause
