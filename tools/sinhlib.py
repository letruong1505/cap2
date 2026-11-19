# Tiện ích vẽ riêng cho hình Sinh học (sơ đồ minh họa).
import math
from figlib2 import *

CELL = '#f6e7c8'     # chất tế bào
NUC = '#c9b6e4'      # nhân
CHL = '#59a14f'      # lục lạp


def lead(b, x1, y1, x2, y2, text, anchor=None, size=13, col=INK):
    """Chú thích có đường dẫn: chấm tại (x1,y1) -> chữ tại (x2,y2)."""
    b.append(L(x1, y1, x2, y2, stroke='#6b7785', w=1.3))
    b.append(C(x1, y1, 2.6, fill='#6b7785', stroke='none', w=0))
    if anchor is None:
        anchor = 'end' if x2 < x1 else 'start'
    dx = -5 if anchor == 'end' else 5
    b.append(H(x2 + dx, y2 + 4, text, size=size, anchor=anchor, fill=col, weight='normal'))


def squig(x1, y1, x2, y2, amp=6, n=6, stroke=INK, w=2):
    pts = []
    for i in range(61):
        t = i / 60
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t + amp * math.sin(2 * math.pi * n * t)
        pts.append((x, y))
    return PL(pts, stroke=stroke, w=w)


def arrow_box(b, x, y, w, h, text, fill=LGREY, size=14, lines=None, bold=True):
    b.append(R(x, y, w, h, fill=fill, stroke=INK, sw=2, rx=8))
    ls = lines or [text]
    n = len(ls)
    for i, s in enumerate(ls):
        b.append(T(x + w / 2, y + h / 2 + 5 + (i - (n - 1) / 2) * (size + 3) - (0 if n == 1 else 2), s, size=size, weight='bold' if bold else 'normal'))


def PLA(pts, stroke=INK, w=2.4, dash=None):
    """Đường gấp khúc có mũi tên ở cuối."""
    p = ' '.join('%.1f,%.1f' % q for q in pts)
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s marker-end="url(#ar)"/>'
            % (p, stroke, w, d))


def bone(x1, y1, x2, y2, w=9, fill='#f1e6c8', stroke=INK):
    """Xương dạng thanh tròn đầu."""
    return L(x1, y1, x2, y2, stroke=stroke, w=w + 3) + L(x1, y1, x2, y2, stroke=fill, w=w)
