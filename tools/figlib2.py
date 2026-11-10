# Bổ sung tiện ích vẽ dùng chung cho Lí và Sinh (sơ đồ mô phỏng).
import math
from figlib import *


def H(x, y, s, size=16, anchor='middle', fill=INK, weight='bold'):
    """Chữ có viền trắng để không bị nét vẽ che."""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s" '
            'stroke="white" stroke-width="4" paint-order="stroke" stroke-linejoin="round">%s</text>'
            % (x, y, anchor, size, weight, fill, escape(s)))


def pt(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg)))


def ARC(cx, cy, r, a1, a2, stroke=INK, w=2, arrow=False, dash=None):
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    large = 1 if (a2 - a1) % 360 > 180 else 0
    m = ' marker-end="url(#ar)"' if arrow else ''
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<path d="M%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
            % (x1, y1, r, r, large, x2, y2, stroke, w, m, d))


def SECTOR(cx, cy, r, a1, a2, fill, stroke=INK, w=2):
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    large = 1 if (a2 - a1) % 360 > 180 else 0
    return ('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"/>' % (cx, cy, x1, y1, r, r, large, x2, y2, fill, stroke, w))


def ELL(cx, cy, rx, ry, fill='none', stroke=INK, w=2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (cx, cy, rx, ry, fill, stroke, w, d))


def card_text(x, y, lines, size=16, lh=26, fill=LGREY, w=270, pad=14):
    h = pad * 2 + lh * len(lines) - 6
    out = [R(x, y, w, h, fill=fill, stroke=GREY, sw=1.2, rx=8)]
    for i, s in enumerate(lines):
        out.append(T(x + pad, y + pad + 16 + i * lh, s, size=size, anchor='start'))
    return ''.join(out)


def force(x, y, dx, dy, label=None, col=RED, w=3.2, lx=0, ly=0, size=15, anchor='middle'):
    """Mũi tên lực từ (x,y) theo vectơ (dx,dy)."""
    o = L(x, y, x + dx, y + dy, stroke=col, w=w, arrow=True)
    if label:
        o += H(x + dx / 2 + lx, y + dy / 2 + ly, label, size=size, fill=col, anchor=anchor)
    return o


def box(x, y, w, h, fill='#c9dcee', stroke=INK, sw=2.2, rx=2):
    return R(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def ground(x1, x2, y, hatch=True):
    o = [L(x1, y, x2, y, w=2.4)]
    if hatch:
        x = x1
        while x < x2:
            o.append(L(x, y, x - 8, y + 9, w=1.2, stroke=GREY))
            x += 12
    return ''.join(o)


def bulb(x, y, r=14, on=False):
    o = [C(x, y, r, fill='#fff3b0' if on else 'white', stroke=INK, w=2),
         L(x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7, w=1.6),
         L(x - r * 0.7, y + r * 0.7, x + r * 0.7, y - r * 0.7, w=1.6)]
    return ''.join(o)


def battery(x, y):
    """Kí hiệu nguồn điện: vạch dài (+) bên trái... trả về SVG ở tâm (x,y)."""
    return (L(x - 6, y - 14, x - 6, y + 14, w=3) + L(x + 6, y - 8, x + 6, y + 8, w=3)
            + T(x - 15, y - 12, '+', size=14, weight='bold') + T(x + 16, y - 12, '−', size=14, weight='bold'))


def switch(x, y, closed=True):
    o = dot(x - 18, y, 3) + dot(x + 18, y, 3)
    o += L(x - 18, y, x + 18, y, w=2.2) if closed else L(x - 18, y, x + 12, y - 16, w=2.2)
    return o


def resistor(x, y, w=44, h=14):
    return R(x - w / 2, y - h / 2, w, h, fill='white', stroke=INK, sw=2)


def meter(x, y, letter, col=INK):
    return C(x, y, 15, fill='white', stroke=col, w=2.2) + T(x, y + 6, letter, size=17, weight='bold', fill=col)
