@echo off
REM AI Studio - Windows Icon Generation Script
REM Requires ImageMagick: https://imagemagick.org/script/download.php

echo Creating AI Studio icons for Windows...
echo.

REM Check if ImageMagick is installed
where magick >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: ImageMagick not found!
    echo.
    echo Please install ImageMagick from:
    echo https://imagemagick.org/script/download.php
    echo.
    echo Make sure to check "Add to PATH" during installation!
    pause
    exit /b 1
)

echo [1/5] Creating base icon (1024x1024)...
magick -size 1024x1024 xc:#1a1a2e ^
    -fill #16213e -draw "circle 512,512 512,100" ^
    -fill #e94560 -pointsize 400 -gravity center ^
    -font Arial-Bold -annotate +0+0 "AI" ^
    -depth 8 -define png:color-type=6 ^
    icon.png

if not exist icon.png (
    echo ERROR: Failed to create icon.png
    pause
    exit /b 1
)

echo [2/5] Creating 512x512...
magick icon.png -resize 512x512 -depth 8 -define png:color-type=6 512x512.png

echo [3/5] Creating 128x128 variants...
magick icon.png -resize 256x256 -depth 8 -define png:color-type=6 128x128.png
magick icon.png -resize 128x128 -depth 8 -define png:color-type=6 128x128@2x.png

echo [4/5] Creating 32x32...
magick icon.png -resize 32x32 -depth 8 -define png:color-type=6 32x32.png

echo [5/5] Creating Windows ICO file...
magick icon.png -depth 8 -define png:color-type=6 ^
  ( -clone 0 -resize 256x256 ) ^
  ( -clone 0 -resize 128x128 ) ^
  ( -clone 0 -resize 64x64 ) ^
  ( -clone 0 -resize 48x48 ) ^
  ( -clone 0 -resize 32x32 ) ^
  ( -clone 0 -resize 16x16 ) ^
  -delete 0 -colors 256 icon.ico

echo.
echo ========================================
echo    Icons Created Successfully!
echo ========================================
echo.
dir /b icon.png icon.ico 32x32.png 128x128.png 128x128@2x.png 512x512.png
echo.
echo Specifications:
echo   - Color depth: 8-bit RGBA
echo   - Windows ICO: 6 sizes (16-256px)
echo   - Tauri compatible: YES
echo.
echo ========================================
pause
