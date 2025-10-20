#!/bin/bash
# Simple script to create placeholder icons

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick not installed. Creating minimal icons..."
    
    # Create a minimal 32x32 PNG (AI Studio logo placeholder)
    # Using Python PIL if available
    python3 << 'PYTHON'
try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create base image
    img = Image.new('RGB', (1024, 1024), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Draw simple AI Studio icon
    # Draw outer circle
    draw.ellipse([112, 112, 912, 912], fill='#16213e', outline='#0f3460', width=8)
    
    # Draw "AI" text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 400)
    except:
        font = ImageFont.load_default()
    
    draw.text((512, 512), "AI", fill='#e94560', font=font, anchor="mm")
    
    # Save in different sizes
    img.save('icon.png')
    img.resize((512, 512)).save('512x512.png')
    img.resize((256, 256)).save('128x128.png')
    img.resize((128, 128)).save('128x128@2x.png')
    img.resize((32, 32)).save('32x32.png')
    img.save('icon.icns')  # macOS
    
    print("Icons created successfully!")
except ImportError:
    print("PIL not available, creating minimal icon...")
    # Fallback - create minimal valid PNG
    import struct
    
    # 32x32 red square PNG
    def create_png():
        width, height = 32, 32
        img_data = []
        for y in range(height):
            row = [0]  # Filter type
            for x in range(x):
                row.extend([255, 0, 0, 255])  # RGBA red
            img_data.append(bytes(row))
        
        raw_data = b''.join(img_data)
        
        import zlib
        compressed = zlib.compress(raw_data)
        
        # PNG header
        png = b'\x89PNG\r\n\x1a\n'
        
        # IHDR chunk
        ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
        png += struct.pack('>I', 13) + b'IHDR' + ihdr
        png += struct.pack('>I', zlib.crc32(b'IHDR' + ihdr))
        
        # IDAT chunk  
        png += struct.pack('>I', len(compressed)) + b'IDAT' + compressed
        png += struct.pack('>I', zlib.crc32(b'IDAT' + compressed))
        
        # IEND chunk
        png += struct.pack('>I', 0) + b'IEND'
        png += struct.pack('>I', zlib.crc32(b'IEND'))
        
        return png
    
    with open('icon.png', 'wb') as f:
        f.write(create_png())
    
    print("Minimal icon created")
PYTHON

else
    echo "Creating icons with ImageMagick..."
    
    # Create base image with ImageMagick
    convert -size 1024x1024 xc:'#1a1a2e' \
        -fill '#16213e' -draw "circle 512,512 512,100" \
        -fill '#e94560' -pointsize 400 -gravity center \
        -annotate +0+0 'AI' \
        icon.png
    
    # Create different sizes
    convert icon.png -resize 512x512 512x512.png
    convert icon.png -resize 256x256 128x128.png
    convert icon.png -resize 128x128 128x128@2x.png
    convert icon.png -resize 32x32 32x32.png
    
    echo "Icons created successfully!"
fi

# For Windows .ico - we need all sizes
# Using PNG as fallback if ImageMagick not available
cp icon.png icon.ico
