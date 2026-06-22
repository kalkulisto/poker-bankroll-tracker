from PIL import Image, ImageDraw, ImageFont
import os

def make_icon(size, path):
    img = Image.new('RGB', (size, size), (10, 15, 10))
    draw = ImageDraw.Draw(img)
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill=(26, 74, 42), outline=(201, 168, 76), width=max(2, size//48))
    font_size = int(size * 0.45)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    text = chr(0x2660)
    bbox = draw.textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - size//12
    draw.text((x, y), text, fill=(201, 168, 76), font=font)
    img.save(path, 'PNG')
    print(f'OK {path}')

base = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend'
make_icon(192, f'{base}/icon-192.png')
make_icon(512, f'{base}/icon-512.png')
