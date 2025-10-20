# AI Studio Icons

Application icons for Tauri desktop app.

## Files

- `icon.png` - 1024x1024 base icon
- `icon.ico` - Windows multi-size icon (16, 32, 48, 64, 128, 256)
- `512x512.png` - macOS/Linux
- `128x128.png` - Standard size
- `128x128@2x.png` - Retina display
- `32x32.png` - Small size

## Design

- Background: Dark blue (#1a1a2e)
- Circle: Navy blue (#16213e)
- Text "AI": Red (#e94560)

## Regenerating Icons

To create new icons from a source image:

```bash
# Run the icon generation script
./create_icons.sh

# Or manually with ImageMagick:
convert icon.png \
  \( -clone 0 -resize 256x256 \) \
  \( -clone 0 -resize 128x128 \) \
  \( -clone 0 -resize 64x64 \) \
  \( -clone 0 -resize 48x48 \) \
  \( -clone 0 -resize 32x32 \) \
  \( -clone 0 -resize 16x16 \) \
  -delete 0 icon.ico
```

## Custom Icons

To use your own icon:
1. Replace `icon.png` with your 1024x1024 PNG image
2. Run `./create_icons.sh` to regenerate all sizes
3. Rebuild the app

## Requirements

- ImageMagick (for icon generation)
- Square PNG image (recommended: 1024x1024)
