#!/usr/bin/env python3
"""Tạo icon Windows (.ico) và Android (mipmap) từ brand/logo-nam-linh.png: chỉ lấy phần biểu tượng N&L, đặt trên nền sáng.
Dùng: python3 tools/make-icons.py   (cần Pillow)"""
import os
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'brand', 'logo-nam-linh.png')
BG = (243, 248, 253)  # nền sáng của icon

img = Image.open(SRC).convert('RGB')
a = np.asarray(img).astype(float)
lum = a @ np.array([0.299, 0.587, 0.114])
mask = lum < 215  # nét logo (xanh navy và xanh dương); vòng tròn mờ và nền đều sáng hơn
ys, xs = np.where(mask)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
# Tách nền: alpha theo độ đậm, khôi phục màu gốc để không có viền sáng quanh nét
bg = np.array([251.0, 252.0, 254.0])
alpha = np.clip((251.0 - lum) / (251.0 - 150.0), 0, 1)
alpha[~mask & (alpha < 0.08)] = 0
safe = np.maximum(alpha, 1e-3)[..., None]
rgb = np.clip((a - (1 - alpha[..., None]) * bg) / safe, 0, 255)
glyph = Image.fromarray(np.dstack([rgb, alpha[..., None] * 255]).astype('uint8'), 'RGBA').crop((x0, y0, x1, y1))
print('biểu tượng', glyph.size)

def canvas(size, frac, bg=True):
    """Ảnh vuông size×size, biểu tượng chiếm frac chiều rộng, ở giữa."""
    c = Image.new('RGBA', (size, size), BG + (255,) if bg else (0, 0, 0, 0))
    w = int(size * frac); h = int(glyph.height * w / glyph.width)
    g = glyph.resize((w, h), Image.LANCZOS)
    c.alpha_composite(g, ((size - w) // 2, (size - h) // 2))
    return c

res = os.path.join(ROOT, 'mobile', 'android', 'app', 'src', 'main', 'res')
legacy = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
for d, px in legacy.items():
    base = canvas(px * 4, 0.66)
    sq = base.resize((px, px), Image.LANCZOS)
    sq.save(os.path.join(res, f'mipmap-{d}', 'ic_launcher.png'))
    mask_c = Image.new('L', (px * 4, px * 4), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask_c).ellipse((0, 0, px * 4 - 1, px * 4 - 1), fill=255)
    rd = base.copy(); rd.putalpha(mask_c)
    rd.resize((px, px), Image.LANCZOS).save(os.path.join(res, f'mipmap-{d}', 'ic_launcher_round.png'))
    fg = canvas(px * 9 // 4 * 4, 0.58, bg=False)  # lớp trước 108dp; biểu tượng nằm trong vùng an toàn 66%
    fg.resize((px * 9 // 4, px * 9 // 4), Image.LANCZOS).save(os.path.join(res, f'mipmap-{d}', 'ic_launcher_foreground.png'))
with open(os.path.join(res, 'values', 'ic_launcher_background.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#%02X%02X%02X</color>\n</resources>' % BG)

ico = canvas(1024, 0.7)
os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
ico.save(os.path.join(ROOT, 'build', 'icon.ico'), sizes=[(s, s) for s in (256, 128, 64, 48, 32, 24, 16)])
ico.resize((512, 512), Image.LANCZOS).save(os.path.join(ROOT, 'build', 'icon.png'))
print('xong')
