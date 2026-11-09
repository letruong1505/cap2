#!/usr/bin/env python3
# Sinh hình SVG cho Toán 12 tập 1, chương I (đồ thị khảo sát, tiệm cận, bài tập đọc đồ thị).
# Mỗi đồ thị được vẽ trực tiếp từ công thức hàm số trong sách, không ghi đáp án lên hình.
# Chạy: python3 tools/build-toan12-figures.py
# Ghi file vào content/toan12/figures/.

import math
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FIG_DIR = os.path.join(ROOT, 'content', 'toan12', 'figures')
INK = '#1d2733'
CURVE = '#4e79a7'
DASH = '#9aa5b1'
W, H = 420, 340
PAD = 36


def fmt(v):
    return ('%g' % round(v, 2)).replace('.', ',')


class Plot:
    def __init__(self, xr, yr):
        self.x0, self.x1 = xr
        self.y0, self.y1 = yr
        self.out = []

    def X(self, x):
        return PAD + (x - self.x0) / (self.x1 - self.x0) * (W - 2 * PAD)

    def Y(self, y):
        return H - PAD - (y - self.y0) / (self.y1 - self.y0) * (H - 2 * PAD)

    def axes(self):
        ax_y = self.Y(0) if self.y0 < 0 < self.y1 else H - PAD
        ax_x = self.X(0) if self.x0 < 0 < self.x1 else PAD
        self.out.append(f'<line x1="{PAD-10}" y1="{ax_y:.1f}" x2="{W-PAD+10}" y2="{ax_y:.1f}" stroke="{INK}" stroke-width="1.6"/>')
        self.out.append(f'<line x1="{ax_x:.1f}" y1="{PAD-10}" x2="{ax_x:.1f}" y2="{H-PAD+10}" stroke="{INK}" stroke-width="1.6"/>')
        self.out.append(f'<text x="{W-PAD+12}" y="{ax_y+5:.1f}" font-size="14" fill="{INK}">x</text>')
        self.out.append(f'<text x="{ax_x+8:.1f}" y="{PAD-12}" font-size="14" fill="{INK}">y</text>')
        self.out.append(f'<text x="{ax_x-6:.1f}" y="{ax_y+16:.1f}" font-size="13" text-anchor="end" fill="{INK}">O</text>')
        for t in range(math.ceil(self.x0), math.floor(self.x1) + 1):
            if t == 0:
                continue
            px = self.X(t)
            self.out.append(f'<line x1="{px:.1f}" y1="{ax_y-4:.1f}" x2="{px:.1f}" y2="{ax_y+4:.1f}" stroke="{INK}" stroke-width="1.2"/>')
            self.out.append(f'<text x="{px:.1f}" y="{ax_y+18:.1f}" font-size="12" text-anchor="middle" fill="{INK}">{t}</text>')
        for t in range(math.ceil(self.y0), math.floor(self.y1) + 1):
            if t == 0:
                continue
            py = self.Y(t)
            self.out.append(f'<line x1="{ax_x-4:.1f}" y1="{py:.1f}" x2="{ax_x+4:.1f}" y2="{py:.1f}" stroke="{INK}" stroke-width="1.2"/>')
            self.out.append(f'<text x="{ax_x-7:.1f}" y="{py+4:.1f}" font-size="12" text-anchor="end" fill="{INK}">{t}</text>')

    def curve(self, f, xs, color=CURVE, jump=None):
        pts = []
        for x in xs:
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError):
                y = None
            if y is None or not math.isfinite(y) or y < self.y0 - 1 or y > self.y1 + 1:
                if len(pts) > 1:
                    self._poly(pts, color)
                pts = []
            else:
                pts.append((self.X(x), self.Y(y)))
        if len(pts) > 1:
            self._poly(pts, color)

    def _poly(self, pts, color):
        d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        self.out.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linejoin="round"/>')

    def vline(self, x, label=None, ly=None):
        px = self.X(x)
        self.out.append(f'<line x1="{px:.1f}" y1="{PAD-10}" x2="{px:.1f}" y2="{H-PAD+10}" stroke="{DASH}" stroke-width="1.4" stroke-dasharray="6 4"/>')
        if label:
            self.out.append(f'<text x="{px+6:.1f}" y="{PAD+4}" font-size="13" fill="{INK}">{label}</text>')

    def hline(self, y, label=None, lx=None):
        py = self.Y(y)
        self.out.append(f'<line x1="{PAD-10}" y1="{py:.1f}" x2="{W-PAD+10}" y2="{py:.1f}" stroke="{DASH}" stroke-width="1.4" stroke-dasharray="6 4"/>')
        if label:
            x = self.x1 - 0.2 if lx is None else lx
            self.out.append(f'<text x="{self.X(x):.1f}" y="{py-6:.1f}" font-size="13" text-anchor="end" fill="{INK}">{label}</text>')

    def point(self, x, y, label=None, dx=8, dy=-8):
        px, py = self.X(x), self.Y(y)
        self.out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="{INK}"/>')
        if label:
            self.out.append(f'<text x="{px+dx:.1f}" y="{py+dy:.1f}" font-size="13" fill="{INK}">{label}</text>')

    def text(self, x, y, s, size=14):
        self.out.append(f'<text x="{self.X(x):.1f}" y="{self.Y(y):.1f}" font-size="{size}" fill="{INK}">{s}</text>')

    def svg(self):
        body = '\n'.join(self.out)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
                f'font-family="Segoe UI, Arial, sans-serif">\n{body}\n</svg>\n')


def linspace(a, b, n=600):
    return [a + (b - a) * i / n for i in range(n + 1)]


def write(name, plot):
    with open(os.path.join(FIG_DIR, name), 'w', encoding='utf-8') as fh:
        fh.write(plot.svg())


def figures():
    os.makedirs(FIG_DIR, exist_ok=True)

    # Bài 3 — y = (x² − x + 2)/(x + 1): tiệm cận đứng x = −1 và tiệm cận xiên y = x − 2 (Ví dụ 6)
    p = Plot((-5, 5), (-8, 8))
    p.axes()
    p.vline(-1, 'x = −1')
    p.curve(lambda x: x - 2, [-5, 5], color=DASH)
    p.text(3.4, 1.6, 'y = x − 2', 13)
    p.curve(lambda x: (x * x - x + 2) / (x + 1), linspace(-5, -1.02) + linspace(-0.98, 5))
    write('b3-tiem-can-xien.svg', p)

    # Bài 3 — y = (3 − x)/(x + 2): tiệm cận đứng x = −2, tiệm cận ngang y = −1 (Ví dụ 3, sơ đồ)
    p = Plot((-6, 4), (-6, 6))
    p.axes()
    p.vline(-2, 'x = −2')
    p.hline(-1, 'y = −1')
    p.curve(lambda x: (3 - x) / (x + 2), linspace(-6, -2.02) + linspace(-1.98, 4))
    write('b3-tiem-can-dung.svg', p)

    # Bài 3 — y = (x² + 2)/x: tiệm cận đứng x = 0 (Ví dụ 4)
    p = Plot((-4, 4), (-6, 6))
    p.axes()
    p.vline(0, 'x = 0')
    p.curve(lambda x: (x * x + 2) / x, linspace(-4, -0.02) + linspace(0.02, 4))
    write('b3-tiem-can-x2.svg', p)

    # Bài 4 — y = −x³ + 3x² − 4 (Ví dụ 1)
    p = Plot((-2.5, 3.5), (-6, 3))
    p.axes()
    p.curve(lambda x: -x ** 3 + 3 * x * x - 4, linspace(-2.5, 3.5))
    p.point(0, -4, '(0; −4)', 8, 14)
    p.point(2, 0, '(2; 0)', 8, -8)
    p.point(-1, 0, '(−1; 0)', -40, -8)
    p.point(1, -2, '(1; −2)', 8, 14)
    write('b4-bac-ba-1.svg', p)

    # Bài 4 — y = x³ − 2x² + 2x − 1 (Ví dụ 2)
    p = Plot((-1.5, 3), (-4, 4))
    p.axes()
    p.curve(lambda x: x ** 3 - 2 * x * x + 2 * x - 1, linspace(-1.5, 3))
    p.point(1, 0, '(1; 0)', 8, -8)
    p.point(0, -1, '(0; −1)', 8, -8)
    p.point(2 / 3, -7 / 27, '(2/3; −7/27)', 8, 16)
    write('b4-bac-ba-2.svg', p)

    # Bài 4 — y = (x + 1)/(x − 2) (Ví dụ 3)
    p = Plot((-5, 6), (-6, 6))
    p.axes()
    p.vline(2, 'x = 2')
    p.hline(1, 'y = 1')
    p.curve(lambda x: (x + 1) / (x - 2), linspace(-5, 1.98) + linspace(2.02, 6))
    p.point(2, 1, 'I(2; 1)', 8, -8)
    p.point(-1, 0, '(−1; 0)', 8, -8)
    write('b4-phan-thuc.svg', p)

    # BT 1.1a — Hình 1.11: y = x³ − (3/2)x²
    p = Plot((-1.5, 2.5), (-2, 2.5))
    p.axes()
    p.curve(lambda x: x ** 3 - 1.5 * x * x, linspace(-1.5, 2.5))
    write('bt-1-1a.svg', p)

    # BT 1.1b — Hình 1.12: y = ∛((x² − 4)²)
    p = Plot((-3.5, 3.5), (-0.5, 4))
    p.axes()
    p.curve(lambda x: math.copysign(abs(x * x - 4) ** (2 / 3), 1), linspace(-3.5, 3.5))
    write('bt-1-1b.svg', p)

    # BT 1.8b — y = |x|
    p = Plot((-3, 3), (-1, 3))
    p.axes()
    p.curve(lambda x: abs(x), linspace(-3, 3))
    p.point(0, 0, 'O', 6, 14)
    write('bt-1-8b.svg', p)

    # BT 1.16 — Hình 1.26: y = 2x²/(x² − 1)
    p = Plot((-3, 3), (-4, 4))
    p.axes()
    p.vline(-1, 'x = −1')
    p.vline(1, 'x = 1')
    p.hline(2, 'y = 2', -2.7)
    p.curve(lambda x: 2 * x * x / (x * x - 1), linspace(-3, -1.02) + linspace(-0.98, 0.98) + linspace(1.02, 3))
    write('bt-1-16.svg', p)

    # BT 1.6 — Hình 1.13: đồ thị f'(x) (minh hoạ dấu của f'; đọc từ hình gốc trên các điểm 0, 2, 4, 6)
    p = Plot((-0.5, 7.5), (-3, 3))
    p.axes()
    fp = lambda x: 0.0
    pts = [(0, 0), (1, -1.6), (2, 0), (3, 2.0), (4, 0), (5, -2.5), (6, 0), (7, 1.5)]
    xs = [a for a, _ in pts]
    ys = [b for _, b in pts]
    # nội suy Catmull-Rom đơn giản để đường cong đi qua các điểm đọc được
    samples = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(40):
            t = k / 40
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            samples.append((x, y))
    samples.append(pts[-1])
    cpts = [(p.X(x), p.Y(y)) for x, y in samples]
    p._poly(cpts, CURVE)
    p.text(0.2, 2.6, "y = f'(x)", 13)
    write('bt-1-6.svg', p)


if __name__ == '__main__':
    figures()
    print('ok')
