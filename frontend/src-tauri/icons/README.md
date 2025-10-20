# AI Studio Icons

Application icons for Tauri desktop app (Windows, macOS, Linux).

## ⚠️ Important: 8-Bit Color Depth Required

Tauri requires **8-bit RGBA PNG** format. Icons with 16-bit depth will cause build errors:
```
error: failed to decode icon: Unsupported PNG bit depth: Sixteen
```

All icons in this directory are pre-configured with 8-bit depth. ✅

## 📁 Files

| File | Size | Purpose |
|------|------|---------|
| `icon.png` | 1024x1024 | Base icon for all platforms |
| `icon.ico` | Multi-size | Windows icon (16, 32, 48, 64, 128, 256) |
| `512x512.png` | 512x512 | macOS/Linux high-res |
| `128x128.png` | 256x256 | Standard display |
| `128x128@2x.png` | 128x128 | Retina display |
| `32x32.png` | 32x32 | Small size (taskbar) |

## 🎨 Design

**AI Studio Logo:**
- Background: Dark navy (`#1a1a2e`)
- Circle: Navy blue (`#16213e`)
- Text "AI": Vibrant red (`#e94560`)
- Font: Arial Bold
- Style: Modern, minimal

## 🔧 Regenerating Icons

### Windows

**Requirements:**
- ImageMagick: https://imagemagick.org/script/download.php
  - Check "Add to PATH" during installation

**Run:**
```cmd
cd frontend\src-tauri\icons
create_icons_windows.bat
```

### Linux/macOS

**Requirements:**
```bash
# macOS
brew install imagemagick

# Ubuntu/Debian
sudo apt install imagemagick

# Arch
sudo pacman -S imagemagick
```

**Run:**
```bash
cd frontend/src-tauri/icons
chmod +x create_icons.sh
./create_icons.sh
```

## 🎨 Creating Custom Icons

### Option 1: Replace Base Icon

1. **Create your 1024x1024 PNG image**
2. **Replace `icon.png`** with your design
3. **Run icon generation script:**
   - Windows: `create_icons_windows.bat`
   - Linux/Mac: `./create_icons.sh`
4. **Rebuild app**: All sizes regenerated automatically

### Option 2: Manual with ImageMagick

**Create 8-bit PNG:**
```bash
magick your-icon.png -depth 8 -define png:color-type=6 icon.png
```

**Create Windows ICO:**
```bash
magick icon.png -depth 8 -define png:color-type=6 \
  \( -clone 0 -resize 256x256 \) \
  \( -clone 0 -resize 128x128 \) \
  \( -clone 0 -resize 64x64 \) \
  \( -clone 0 -resize 48x48 \) \
  \( -clone 0 -resize 32x32 \) \
  \( -clone 0 -resize 16x16 \) \
  -delete 0 -colors 256 icon.ico
```

**Create size variants:**
```bash
magick icon.png -resize 512x512 -depth 8 -define png:color-type=6 512x512.png
magick icon.png -resize 256x256 -depth 8 -define png:color-type=6 128x128.png
magick icon.png -resize 128x128 -depth 8 -define png:color-type=6 128x128@2x.png
magick icon.png -resize 32x32 -depth 8 -define png:color-type=6 32x32.png
```

### Option 3: Online Tools

**For quick testing without ImageMagick:**

1. **Create PNG icon** (1024x1024)
   - Use any design tool (Photoshop, GIMP, Canva, etc.)

2. **Convert to ICO online:**
   - Visit: https://www.icoconverter.com/
   - Upload your PNG
   - Select all sizes: 16, 32, 48, 64, 128, 256
   - Download `icon.ico`

3. **Ensure 8-bit depth:**
   - Open in GIMP → Image → Mode → RGB Color
   - Export as PNG → 8 bits/color channel
   - Save as `icon.png`

4. **Copy to project:**
   ```cmd
   copy icon.png frontend\src-tauri\icons\
   copy icon.ico frontend\src-tauri\icons\
   ```

## 🔍 Verifying Icons

### Check bit depth:

**Windows (PowerShell):**
```powershell
Get-Item *.png | ForEach-Object { 
    [System.Drawing.Image]::FromFile($_.FullName).PixelFormat 
}
```

**Linux/macOS:**
```bash
file *.png *.ico | grep "8-bit"
```

**Should show:**
```
icon.png: PNG image data, 1024 x 1024, 8-bit/color RGBA
icon.ico: MS Windows icon resource - 6 icons, 256x256 with PNG image data, 256 x 256, 8-bit/color RGBA
```

## ❌ Common Issues

### Issue: "Unsupported PNG bit depth: Sixteen"

**Cause:** Icon has 16-bit color depth instead of 8-bit

**Fix:**
```bash
# Convert to 8-bit
magick icon.png -depth 8 -define png:color-type=6 icon-fixed.png
mv icon-fixed.png icon.png

# Regenerate ICO
magick icon.png -depth 8 ... icon.ico
```

### Issue: "Icon not found"

**Cause:** Icons not in correct directory

**Fix:**
```cmd
# Check path
dir frontend\src-tauri\icons\icon.ico

# Should exist in: frontend/src-tauri/icons/
```

### Issue: Icon looks pixelated

**Cause:** Base icon too small or low quality

**Fix:**
- Use high-resolution base image (1024x1024 minimum)
- Ensure vector graphics or high-DPI source
- Avoid upscaling small images

## 📐 Recommended Dimensions

| Platform | Recommended Sizes |
|----------|-------------------|
| Windows | 16, 32, 48, 64, 128, 256 |
| macOS | 16, 32, 128, 256, 512, 1024 |
| Linux | 32, 48, 64, 128, 256, 512 |

**Our ICO contains:** 16, 32, 48, 64, 128, 256 (covers all platforms)

## 🔗 Resources

- **ImageMagick:** https://imagemagick.org/
- **ICO Converter:** https://www.icoconverter.com/
- **GIMP:** https://www.gimp.org/
- **Tauri Icons Guide:** https://tauri.app/v1/guides/features/icons/

## 📝 Technical Specifications

```
Format: PNG
Color Type: 6 (RGBA - True Color with Alpha)
Bit Depth: 8 bits per channel (32 bits per pixel)
Compression: PNG compression
Interlacing: None

Windows ICO:
- Container format for multiple PNG images
- 6 embedded sizes: 16, 32, 48, 64, 128, 256
- Color depth: 8-bit per channel
- Max colors: 256 per icon (ICO limitation)
```

## ✅ Pre-Built Icons Status

All icons in this directory are:
- ✅ **8-bit color depth** (Tauri compatible)
- ✅ **RGBA format** (supports transparency)
- ✅ **Multiple sizes** (all platforms covered)
- ✅ **Tested and verified** (builds successfully)

**No manual icon creation needed!** Just use the provided icons or run the generation script to create new ones.
