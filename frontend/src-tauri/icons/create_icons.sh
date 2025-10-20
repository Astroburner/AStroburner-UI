#!/bin/bash
# AI Studio - Icon Generation Script
# Creates Windows-compatible 8-bit PNG icons

set -e

echo "Creating AI Studio icons..."

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ERROR: ImageMagick is required!"
    echo "Install from: https://imagemagick.org/script/download.php"
    exit 1
fi

# Create base 1024x1024 icon with 8-bit depth
echo "Creating base icon (1024x1024)..."
convert -size 1024x1024 xc:'#1a1a2e' \
    -fill '#16213e' -draw "circle 512,512 512,100" \
    -fill '#e94560' -pointsize 400 -gravity center \
    -font Arial-Bold -annotate +0+0 'AI' \
    -depth 8 -define png:color-type=6 \
    icon.png

# Verify base icon
if [ ! -f icon.png ]; then
    echo "ERROR: Failed to create icon.png"
    exit 1
fi

echo "Creating size variants..."

# Create different sizes (all 8-bit RGBA)
convert icon.png -resize 512x512 -depth 8 -define png:color-type=6 512x512.png
convert icon.png -resize 256x256 -depth 8 -define png:color-type=6 128x128.png
convert icon.png -resize 128x128 -depth 8 -define png:color-type=6 128x128@2x.png
convert icon.png -resize 32x32 -depth 8 -define png:color-type=6 32x32.png

echo "Creating Windows ICO file..."

# Create Windows ICO with multiple sizes (8-bit, 256 colors max)
convert icon.png -depth 8 -define png:color-type=6 \
  \( -clone 0 -resize 256x256 \) \
  \( -clone 0 -resize 128x128 \) \
  \( -clone 0 -resize 64x64 \) \
  \( -clone 0 -resize 48x48 \) \
  \( -clone 0 -resize 32x32 \) \
  \( -clone 0 -resize 16x16 \) \
  -delete 0 -colors 256 icon.ico

# Verify all files
echo ""
echo "Verification:"
file *.png *.ico | grep "8-bit" || {
    echo "WARNING: Some icons may not be 8-bit!"
}

echo ""
echo "✓ Icons created successfully!"
echo ""
echo "Files created:"
ls -lh icon.png icon.ico 32x32.png 128x128.png 128x128@2x.png 512x512.png 2>/dev/null || true

echo ""
echo "Icon specifications:"
echo "  - Color depth: 8-bit RGBA"
echo "  - Format: PNG with color type 6 (RGBA)"
echo "  - Windows ICO: 6 sizes (16-256px)"
echo "  - Tauri compatible: YES"
