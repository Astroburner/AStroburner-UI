@echo off
REM ============================================
REM   AI Studio - Quick Dependency Fix
REM   Installiert fehlende Dependencies
REM ============================================

echo.
echo ====================================
echo    AI Studio - Quick Fix
echo ====================================
echo.
echo Installiere fehlende Dependencies...
echo.

REM Check if we're in the right directory
if not exist "frontend\package.json" (
    echo [FEHLER] Nicht im richtigen Verzeichnis!
    echo Bitte navigiere zu: ai-studio\
    pause
    exit /b 1
)

REM Install Frontend Dependencies
echo [1/2] Installiere Frontend Dependencies...
cd frontend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [FEHLER] Frontend Installation fehlgeschlagen!
    pause
    exit /b 1
)
echo [OK] Frontend Dependencies installiert
echo.

REM Install Backend Dependencies (if venv doesn't exist)
cd ..\backend
if not exist "venv\" (
    echo [2/2] Erstelle Python Virtual Environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [FEHLER] Virtual Environment konnte nicht erstellt werden!
        pause
        exit /b 1
    )
    
    echo [2/2] Installiere Backend Dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [FEHLER] Backend Installation fehlgeschlagen!
        pause
        exit /b 1
    )
    echo [OK] Backend Dependencies installiert
) else (
    echo [2/2] Backend venv existiert bereits (ueberspringe)
)

cd ..

echo.
echo ====================================
echo    Installation Erfolgreich!
echo ====================================
echo.
echo Starte jetzt die App mit: start.bat
echo.
pause
