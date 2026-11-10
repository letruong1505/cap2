# Toán 7, Toán 8, Toán 12 (đợt hình lý thuyết): đồ thị, hình diện tích, sơ đồ phân loại.
# Chỉ dựng từ khái niệm có trong bài; đồ thị là minh hoạ (hàm số ghi rõ khi dùng ví dụ cụ thể).
import sys, os, json, glob, math, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *


def _load(name, fn):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(__file__), fn))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


su2 = _load('su2', 'build-su2-figures.py')
HEAD, SOFT = su2.HEAD, su2.SOFT
NAVY = '#1a56a0'


def halo(x, y, s, size=13, fill=INK, anchor='middle', weight='normal'):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s" stroke="white" '
            'stroke-width="3" paint-order="stroke">%s</text>' % (x, y, anchor, size, weight, fill, s))


def RT(x, y, markup, size=15, anchor='middle', weight='normal', fill=INK):
    """Chữ có thẻ <tspan> tuỳ ý (chỉ số trên/dưới); markup không bị escape."""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s">%s</text>'
            % (x, y, anchor, size, weight, fill, markup))


def ig(lo, hi):
    return ('∫<tspan dy="9" font-size="11">%s</tspan><tspan dy="-17" dx="-5" font-size="11">%s</tspan>'
            '<tspan dy="8" dx="2">&#160;</tspan>' % (lo, hi))


def sb(t):
    return '<tspan dy="4" font-size="11">%s</tspan><tspan dy="-4">&#8203;</tspan>' % t


def rr(x, y, w, h, fill, op=1.0, stroke=INK, sw=1.5):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, fill, op, stroke, sw))


class Ax:
    def __init__(s, x0, x1, y0, y1, px0, px1, py0, py1):
        s.x0, s.x1, s.y0, s.y1, s.px0, s.px1, s.py0, s.py1 = x0, x1, y0, y1, px0, px1, py0, py1

    def fx(s, x): return s.px0 + (x - s.x0) / (s.x1 - s.x0) * (s.px1 - s.px0)
    def fy(s, y): return s.py0 - (y - s.y0) / (s.y1 - s.y0) * (s.py0 - s.py1)
    def pt(s, x, y): return (s.fx(x), s.fy(y))

    def curve(s, f, a, b, n=80):
        return [s.pt(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]

    def axes(s, o=True):
        ax_y = s.fy(0) if s.y0 <= 0 <= s.y1 else s.fy(s.y0)
        ax_x = s.fx(0) if s.x0 <= 0 <= s.x1 else s.fx(s.x0)
        b = [L(s.px0 - 4, ax_y, s.px1 + 8, ax_y, arrow=True), L(ax_x, s.py0 + 4, ax_x, s.py1 - 8, arrow=True),
             T(s.px1 + 8, ax_y + 18, 'x', size=14), T(ax_x + 12, s.py1 - 6, 'y', size=14)]
        if o:
            b.append(T(ax_x - 8, ax_y + 17, 'O', size=13, anchor='end'))
        return ''.join(b)

    def area(s, f, a, b, fill, g=None, n=60, op=1.0):
        up = s.curve(f, a, b, n)
        if g is None:
            lo = [(s.fx(b), s.fy(0)), (s.fx(a), s.fy(0))]
        else:
            lo = list(reversed(s.curve(g, a, b, n)))
        pts = up + lo
        p = ' '.join('%.1f,%.1f' % q for q in pts)
        return '<polygon points="%s" fill="%s" fill-opacity="%s" stroke="none"/>' % (p, fill, op)


# ====================== Toán 12 ======================
def t12_cuc_tri():
    W, H = 720, 305
    b = [title(W, 'Dấu của f′(x) và cực trị')]
    for k, (x0, ttl) in enumerate([(14, 'y = x³ − 3x,   f′(x) = 3(x − 1)(x + 1)'), (374, 'y = x³,   f′(x) = 3x²')]):
        lim = 2.1 if k == 0 else 1.45
        A = Ax(-2.1, 2.1, -3.2, 3.2, x0, x0 + 332, 222, 80)
        b.append(T(x0 + 166, 46, ttl, size=13.5, weight='bold'))
        b.append(A.axes())
        f = (lambda x: x ** 3 - 3 * x) if k == 0 else (lambda x: x ** 3)
        b.append(PL(A.curve(f, -lim, lim), stroke=BLUE, w=3))
        strip = 236
        b.append(T(x0 + 166, strip, 'Dấu của f′(x)', size=12.5, fill='#5b6773'))
        if k == 0:
            for xv, yv, lab, dy in [(-1, 2, 'cực đại, y_CĐ = 2', -12), (1, -2, 'cực tiểu, y_CT = −2', 24)]:
                px, py = A.pt(xv, yv)
                b.append(L(px, py, px, A.fy(0), stroke=GREY, w=1.3, dash='4 3'))
                b.append(dot(px, py, 4.5, fill=RED))
                b.append(halo(px, py + dy, lab, 12.5, NAVY, 'middle', 'bold'))
            b.append(T(A.fx(-1), A.fy(0) + 17, '−1', size=13)); b.append(T(A.fx(1), A.fy(0) - 8, '1', size=13))
            xs = [A.fx(-1), A.fx(1)]
            seq = [('+', (A.px0 + xs[0]) / 2), ('0', xs[0]), ('−', (xs[0] + xs[1]) / 2), ('0', xs[1]), ('+', (xs[1] + A.px1) / 2)]
            for s, x in seq:
                b.append(T(x, strip + 22, s, size=16, weight='bold', fill=RED if s == '0' else INK))
            for s, x in [('đồng biến', (A.px0 + xs[0]) / 2), ('nghịch biến', (xs[0] + xs[1]) / 2), ('đồng biến', (xs[1] + A.px1) / 2)]:
                b.append(T(x, strip + 44, s, size=12.5))
        else:
            px, py = A.pt(0, 0)
            b.append(dot(px, py, 4.5, fill=RED))
            b.append(halo(px - 10, A.fy(1.8), 'x = 0: không là cực trị', 12.5, NAVY, 'end', 'bold'))
            xs = A.fx(0)
            for s, x in [('+', (A.px0 + xs) / 2), ('0', xs), ('+', (xs + A.px1) / 2)]:
                b.append(T(x, strip + 22, s, size=16, weight='bold', fill=RED if s == '0' else INK))
            b.append(T(x0 + 166, strip + 44, 'f′ bằng 0 nhưng không đổi dấu', size=12.5))
    return svg(W, H, ''.join(b))


def t12_gtln():
    W, H = 580, 330
    A = Ax(-2, 3, -3, 9.5, 50, 520, 270, 50)
    f = lambda x: x ** 3 - 3 * x
    a, bb, x0 = -1.5, 2.5, 1
    b = [title(W, 'Giá trị lớn nhất, nhỏ nhất trên đoạn [a; b]'), A.axes()]
    b.append(PL(A.curve(f, a, bb), stroke=BLUE, w=3))
    bot = A.fy(-3)
    for xv, lab in [(a, 'a'), (x0, 'x₀'), (bb, 'b')]:
        b.append(L(A.fx(xv), A.fy(f(xv)), A.fx(xv), bot, stroke=GREY, w=1.3, dash='4 3'))
        b.append(T(A.fx(xv), bot + 17, lab, size=14, weight='bold'))
    for xv, yv, lab in [(bb, f(bb), 'M = f(b)'), (x0, f(x0), 'm = f(x₀)')]:
        b.append(L(A.fx(xv), A.fy(yv), A.fx(0), A.fy(yv), stroke=GREY, w=1.3, dash='4 3'))
        b.append(halo(A.fx(0) - 8, A.fy(yv) + 5, lab, 13.5, NAVY, 'end', 'bold'))
    b.append(dot(*A.pt(a, f(a)), 4.5, fill=BLUE)); b.append(dot(*A.pt(bb, f(bb)), 5.5, fill=RED)); b.append(dot(*A.pt(x0, f(x0)), 5.5, fill=RED))
    b.append(T(W / 2, H - 6, 'Ví dụ y = x³ − 3x trên [−1,5; 2,5]: GTLN tại đầu mút b; GTNN tại điểm cực tiểu x₀ = 1', size=12.5, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def t12_phan_vi():
    W, H = 720, 270
    b = [title(W, 'Khoảng biến thiên và khoảng tứ phân vị')]
    xa, q1, q2, q3, xb = 70, 230, 330, 500, 650
    y = 112
    b.append(L(xa, y, q1, y, stroke=INK, w=2.2)); b.append(L(q3, y, xb, y, stroke=INK, w=2.2))
    b.append(L(xa, y - 14, xa, y + 14, w=2.2)); b.append(L(xb, y - 14, xb, y + 14, w=2.2))
    b.append(R(q1, y - 24, q3 - q1, 48, fill=LBLUE, stroke=BLUE, sw=2.2))
    b.append(L(q2, y - 24, q2, y + 24, stroke=BLUE, w=2.6))
    for x, mk in [(xa, 'a₁'), (q1, 'Q₁'), (q2, 'Q₂'), (q3, 'Q₃'), (xb, 'a' + sb('k+1'))]:
        b.append(RT(x, y - 38, mk, size=15, weight='bold'))
    yq = 170
    b.append(L(q1, yq, q3, yq, stroke=ORANGE, w=2.5)); b.append(L(q1, yq - 8, q1, yq + 8, stroke=ORANGE, w=2.5)); b.append(L(q3, yq - 8, q3, yq + 8, stroke=ORANGE, w=2.5))
    b.append(RT((q1 + q3) / 2, yq + 24, 'Khoảng tứ phân vị  Δ' + sb('Q') + ' = Q₃ − Q₁', size=14, weight='bold', fill='#b3601a'))
    yr = 218
    b.append(L(xa, yr, xb, yr, stroke=GREEN, w=2.5)); b.append(L(xa, yr - 8, xa, yr + 8, stroke=GREEN, w=2.5)); b.append(L(xb, yr - 8, xb, yr + 8, stroke=GREEN, w=2.5))
    b.append(RT((xa + xb) / 2, yr + 22, 'Khoảng biến thiên  R = a' + sb('k+1') + ' − a₁', size=14, weight='bold', fill='#2f6b2a'))
    b.append(T(W / 2, H - 6, 'Sơ đồ minh hoạ vị trí các giá trị; khoảng cách không theo tỉ lệ. Δ_Q chỉ phụ thuộc nửa giữa của mẫu.', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def t12_nguyen_ham():
    W, H = 720, 300
    b = [title(W, 'Nguyên hàm: F′(x) = f(x)')]
    # trái: sơ đồ hai chiều
    b.append(R(14, 96, 104, 56, fill=SOFT[0], stroke=HEAD[0], sw=2, rx=8)); b.append(T(66, 132, 'F(x)', size=20, weight='bold'))
    b.append(R(236, 96, 104, 56, fill=SOFT[1], stroke=HEAD[1], sw=2, rx=8)); b.append(T(288, 132, 'f(x)', size=20, weight='bold'))
    b.append(L(122, 110, 232, 110, arrow=True)); b.append(T(177, 100, 'lấy đạo hàm', size=12.5))
    b.append(L(232, 140, 122, 140, arrow=True)); b.append(T(177, 160, 'lấy nguyên hàm', size=12.5))
    b.append(T(177, 208, 'Mọi nguyên hàm của f(x) đều có dạng', size=13))
    b.append(T(177, 230, 'F(x) + C   (C là hằng số)', size=15, weight='bold', fill=NAVY))
    b.append(T(177, 256, '∫f(x)dx = F(x) + C', size=15, weight='bold', fill=NAVY))
    # phải: họ đường cong
    A = Ax(-1.8, 1.8, -1.8, 3.6, 380, 650, 262, 88)
    b.append(T(515, 50, 'Ví dụ f(x) = 2x, F(x) = x² + C', size=13.5, weight='bold'))
    b.append(A.axes())
    cols = [(-1, BLUE), (0, ORANGE), (1, GREEN)]
    for c, col in cols:
        b.append(PL(A.curve(lambda x, c=c: x * x + c, -1.6, 1.6), stroke=col, w=2.8))
        b.append(T(A.fx(1.6) + 6, A.fy(1.6 ** 2 + c) + 4, 'C = %s' % ('−1' if c == -1 else str(c)), size=12.5, anchor='start', weight='bold', fill=col))
    b.append(L(A.fx(1), A.fy(2.15), A.fx(1), A.fy(-1.8), stroke=GREY, w=1.3, dash='4 3'))
    b.append(T(A.fx(1), A.fy(-1.8) + 16, 'x₀', size=14, weight='bold'))
    for c, col in cols:
        y0 = 1 + c
        b.append(L(A.fx(0.55), A.fy(y0 - 0.9), A.fx(1.45), A.fy(y0 + 0.9), stroke=INK, w=2))
        b.append(dot(A.fx(1), A.fy(y0), 4, fill=RED))
    b.append(T(515, H - 8, 'Tiếp tuyến tại x₀ của các đường song song với nhau (cùng hệ số góc f(x₀))', size=11.5, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def _f12(x): return 2 + math.sin(0.9 * x)


def t12_tich_phan():
    W, H = 720, 320
    b = [title(W, 'Tích phân và diện tích hình thang cong')]
    for k, x0 in enumerate([14, 372]):
        A = Ax(0, 6, 0, 3.7, x0 + 10, x0 + 330, 240, 80)
        b.append(A.axes(o=False))
        a_, b_ = 1.0, 5.0
        if k == 0:
            b.append(A.area(_f12, a_, b_, LBLUE))
            b.append(T(*A.pt(3.0, 1.0), 'S', size=20, weight='bold', fill=NAVY))
        else:
            c_ = 3.0
            b.append(A.area(_f12, a_, c_, LBLUE)); b.append(A.area(_f12, c_, b_, '#fde3bd'))
            b.append(L(A.fx(c_), A.fy(0), A.fx(c_), A.fy(_f12(c_)), stroke=INK, w=1.6, dash='5 3'))
        b.append(PL(A.curve(_f12, 0.15, 5.95), stroke=BLUE, w=3))
        for xv, lab in ([(a_, 'a'), (b_, 'b')] if k == 0 else [(a_, 'a'), (3.0, 'c'), (b_, 'b')]):
            b.append(L(A.fx(xv), A.fy(0), A.fx(xv), A.fy(_f12(xv)), stroke=GREY if xv not in (3.0,) else INK, w=1.5, dash='4 3'))
            b.append(T(A.fx(xv), A.fy(0) + 17, lab, size=14, weight='bold'))
        b.append(T(A.fx(5.95) - 4, A.fy(_f12(5.95)) - 22, 'y = f(x)', size=13, anchor='end', weight='bold', fill=NAVY))
        if k == 0:
            b.append(RT(x0 + 165, 290, 'S = ' + ig('a', 'b') + 'f(x)dx = F(b) − F(a)', size=15, weight='bold', fill=NAVY))
            b.append(T(x0 + 165, 52, 'Hình thang cong giới hạn bởi y = f(x), Ox, x = a, x = b', size=12.5, fill='#5b6773'))
        else:
            b.append(RT(x0 + 165, 290, ig('a', 'b') + 'f(x)dx = ' + ig('a', 'c') + 'f(x)dx + ' + ig('c', 'b') + 'f(x)dx', size=15, weight='bold', fill=NAVY))
            b.append(T(x0 + 165, 52, 'Tính chất cộng: a < c < b', size=12.5, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def t12_ung_dung():
    W, H = 720, 320
    b = [title(W, 'Ứng dụng hình học của tích phân')]
    pw = 232
    # (a) giữa đồ thị và trục Ox
    x0 = 8
    A = Ax(0, 6, -1.9, 1.9, x0 + 6, x0 + pw - 14, 230, 70)
    fa = lambda x: 1.5 * math.sin(1.1 * x)
    ca, cb = 0.4, 5.2
    b.append(T(x0 + pw / 2, 52, 'Giữa đồ thị và trục Ox', size=13, weight='bold'))
    b.append(A.area(fa, ca, cb, LBLUE)); b.append(A.axes(o=False))
    b.append(PL(A.curve(fa, 0.15, 5.8), stroke=BLUE, w=3))
    for xv, lab, up in [(ca, 'a', False), (cb, 'b', True)]:
        b.append(L(A.fx(xv), A.fy(0), A.fx(xv), A.fy(fa(xv)), stroke=GREY, w=1.4, dash='4 3'))
        b.append(T(A.fx(xv), A.fy(0) + (-8 if up else 17), lab, size=14, weight='bold'))
    b.append(T(*A.pt(1.65, 0.55), 'S', size=17, weight='bold', fill=NAVY))
    b.append(RT(x0 + pw / 2, 276, 'S = ' + ig('a', 'b') + '|f(x)|dx', size=14.5, weight='bold', fill=NAVY))
    # (b) giữa hai đồ thị
    x0 = 244
    A = Ax(0, 6, 0, 3.4, x0 + 6, x0 + pw - 14, 230, 70)
    ff = lambda x: 2.4 + 0.6 * math.sin(x)
    gg = lambda x: 0.8 + 0.5 * math.cos(x)
    ca, cb = 0.6, 5.4
    b.append(T(x0 + pw / 2, 52, 'Giữa hai đồ thị', size=13, weight='bold'))
    b.append(A.area(ff, ca, cb, '#fde3bd', g=gg)); b.append(A.axes(o=False))
    b.append(PL(A.curve(ff, 0.15, 5.8), stroke=BLUE, w=3)); b.append(PL(A.curve(gg, 0.15, 5.8), stroke=GREEN, w=3))
    for xv, lab in [(ca, 'a'), (cb, 'b')]:
        b.append(L(A.fx(xv), A.fy(0), A.fx(xv), A.fy(ff(xv)), stroke=GREY, w=1.4, dash='4 3'))
        b.append(T(A.fx(xv), A.fy(0) + 17, lab, size=14, weight='bold'))
    b.append(halo(A.fx(5.8) - 2, A.fy(ff(5.8)) - 10, 'y = f(x)', 12.5, NAVY, 'end', 'bold'))
    b.append(halo(A.fx(5.8) - 2, A.fy(gg(5.8)) + 34, 'y = g(x)', 12.5, '#2f6b2a', 'end', 'bold'))
    b.append(T(*A.pt(3.0, 1.55), 'S', size=17, weight='bold', fill=NAVY))
    b.append(RT(x0 + pw / 2, 276, 'S = ' + ig('a', 'b') + '|f(x) − g(x)|dx', size=14.5, weight='bold', fill=NAVY))
    # (c) khối tròn xoay
    x0 = 480
    A = Ax(0, 6, -2.2, 2.2, x0 + 6, x0 + pw - 14, 230, 70)
    fc = lambda x: 1.15 + 0.45 * math.sin(0.8 * x)
    ca, cb, cc = 0.8, 5.2, 3.0
    b.append(T(x0 + pw / 2, 52, 'Khối tròn xoay quanh Ox', size=13, weight='bold'))
    up = A.curve(fc, ca, cb); lo = A.curve(lambda x: -fc(x), ca, cb)
    pts = up + list(reversed(lo))
    b.append('<polygon points="%s" fill="%s" stroke="none"/>' % (' '.join('%.1f,%.1f' % q for q in pts), LBLUE))
    b.append(A.axes(o=False))
    b.append(PL(up, stroke=BLUE, w=3)); b.append(PL(lo, stroke=BLUE, w=3))
    for xv, dash in [(ca, None), (cb, None), (cc, '4 3')]:
        ry = A.fy(0) - A.fy(fc(xv))
        e = '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="2"%s/>' % (
            A.fx(xv), A.fy(0), ry * 0.28, ry, 'none' if xv != cb else LBLUE, BLUE if dash is None else INK,
            ' stroke-dasharray="%s"' % dash if dash else '')
        b.append(e)
    b.append(L(A.fx(cc), A.fy(0), A.fx(cc), A.fy(fc(cc)), stroke=RED, w=2.2))
    b.append(halo(A.fx(cc) + 6, A.fy(fc(cc) / 2) + 4, 'f(x)', 12.5, '#a02a2c', 'start', 'bold'))
    for xv, lab in [(ca, 'a'), (cb, 'b')]:
        b.append(L(A.fx(xv), A.fy(-1.75), A.fx(xv), A.fy(-2.2), stroke=GREY, w=1.4, dash='4 3'))
        b.append(T(A.fx(xv), A.fy(-2.2) + 16, lab, size=14, weight='bold'))
    b.append(RT(x0 + pw / 2, 276, 'V = π' + ig('a', 'b') + 'f²(x)dx', size=14.5, weight='bold', fill=NAVY))
    b.append(T(W / 2, H - 10, 'Đồ thị minh hoạ; f(x) ≥ 0 khi tính thể tích khối tròn xoay.', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


# ====================== Toán 8 ======================
def t8_hang_dang_thuc():
    W, H = 720, 548
    b = [title(W, 'Hằng đẳng thức bằng hình diện tích')]
    A_, B_ = 112, 52
    # ---- (A+B)^2
    x0, y0 = 100, 116
    b.append(T(190, 58, 'Bình phương của một tổng', size=14, weight='bold'))
    b.append(T(190, 80, '(A + B)² = A² + 2AB + B²', size=14, weight='bold', fill=NAVY))
    b.append(rr(x0, y0, A_, A_, LBLUE)); b.append(T(x0 + A_ / 2, y0 + A_ / 2 + 6, 'A²', size=18, weight='bold'))
    b.append(rr(x0 + A_, y0, B_, A_, '#fde3bd')); b.append(T(x0 + A_ + B_ / 2, y0 + A_ / 2 + 5, 'AB', size=15, weight='bold'))
    b.append(rr(x0, y0 + A_, A_, B_, '#fde3bd')); b.append(T(x0 + A_ / 2, y0 + A_ + B_ / 2 + 5, 'AB', size=15, weight='bold'))
    b.append(rr(x0 + A_, y0 + A_, B_, B_, LGREEN)); b.append(T(x0 + A_ + B_ / 2, y0 + A_ + B_ / 2 + 5, 'B²', size=15, weight='bold'))
    b.append(T(x0 + A_ / 2, y0 - 7, 'A', size=14)); b.append(T(x0 + A_ + B_ / 2, y0 - 7, 'B', size=14))
    b.append(T(x0 - 9, y0 + A_ / 2 + 5, 'A', size=14, anchor='end')); b.append(T(x0 - 9, y0 + A_ + B_ / 2 + 5, 'B', size=14, anchor='end'))
    # ---- (A-B)^2
    x1 = 462
    S = 164
    b.append(T(540, 58, 'Bình phương của một hiệu', size=14, weight='bold'))
    b.append(T(540, 80, '(A − B)² = A² − 2AB + B²', size=14, weight='bold', fill=NAVY))
    ab = S - 48
    b.append(rr(x1, y0, S, S, '#ffffff'))
    b.append(rr(x1, y0, ab, ab, LBLUE)); b.append(T(x1 + ab / 2, y0 + ab / 2 + 6, '(A − B)²', size=16, weight='bold'))
    b.append(rr(x1 + ab, y0, 48, S, '#f28e2b', 0.45)); b.append(rr(x1, y0 + ab, S, 48, '#f28e2b', 0.45))
    b.append(T(x1 + ab + 24, y0 + ab / 2 + 5, 'AB', size=14, weight='bold')); b.append(T(x1 + ab / 2, y0 + ab + 29, 'AB', size=14, weight='bold'))
    b.append(T(x1 + ab + 24, y0 + ab + 29, 'B²', size=13, weight='bold'))
    b.append(rr(x1, y0, S, S, 'none', 1, INK, 2))
    b.append(T(x1 + ab / 2, y0 - 7, 'A − B', size=14)); b.append(T(x1 + ab + 24, y0 - 7, 'B', size=14))
    b.append(T(x1 - 9, y0 + ab / 2 + 5, 'A − B', size=14, anchor='end')); b.append(T(x1 - 9, y0 + ab + 29, 'B', size=14, anchor='end'))
    b.append(T(540, y0 + S + 26, 'Bỏ hai dải AB khỏi A²:', size=12, fill='#5b6773')); b.append(T(540, y0 + S + 43, 'góc B² bị bỏ hai lần nên cộng lại một lần', size=12, fill='#5b6773'))
    # ---- A^2 - B^2
    y3 = 396
    b.append(T(W / 2, 344, 'Hiệu hai bình phương:  A² − B² = (A − B)(A + B)', size=14, weight='bold', fill=NAVY))
    A2, B2 = 112, 44
    xl = 60
    b.append(rr(xl, y3, A2, A2 - B2, LBLUE)); b.append(rr(xl, y3 + A2 - B2, A2 - B2, B2, '#fde3bd'))
    b.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="5 3"/>' % (xl + A2 - B2, y3 + A2 - B2, B2, B2, GREY))
    b.append(T(xl + A2 - B2 / 2, y3 + A2 - B2 / 2 + 5, 'B²', size=13, fill=GREY))
    b.append(T(xl + A2 / 2, y3 - 7, 'A', size=14)); b.append(T(xl - 9, y3 + (A2 - B2) / 2 + 5, 'A − B', size=14, anchor='end'))
    b.append(T(xl - 9, y3 + A2 - B2 / 2 + 5, 'B', size=14, anchor='end'))
    b.append(T(xl + 100, y3 + A2 + 24, 'Hình chữ L có diện tích A² − B²', size=12, fill='#5b6773'))
    b.append(L(240, y3 + 36, 322, y3 + 36, arrow=True)); b.append(T(281, y3 + 26, 'ghép lại', size=12.5))
    xr = 360
    b.append(rr(xr, y3, A2, A2 - B2, LBLUE)); b.append(rr(xr + A2, y3, B2, A2 - B2, '#fde3bd'))
    b.append(T(xr + (A2 + B2) / 2, y3 - 7, 'A + B', size=14)); b.append(T(xr + A2 + B2 + 9, y3 + (A2 - B2) / 2 + 5, 'A − B', size=14, anchor='start'))
    b.append(T(xr + (A2 + B2) / 2, y3 + A2 - B2 + 24, 'Hình chữ nhật (A − B)(A + B)', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def t8_don_thuc():
    W, H = 720, 345
    b = [title(W, 'Đơn thức thu gọn và đơn thức đồng dạng')]
    b.append(R(14, 52, 250, 92, fill=SOFT[0], stroke=HEAD[0], sw=2, rx=8))
    b.append(T(139, 80, 'Đơn thức thu gọn', size=14, weight='bold')); b.append(TL(139, 103, ['tích của một số với các biến;', 'mỗi biến chỉ xuất hiện một lần'], size=13, lh=21))
    b.append(T(358, 114, '7', size=52, anchor='end', weight='bold', fill=BLUE))
    b.append(T(366, 114, 'x²y', size=52, anchor='start', weight='bold', fill=ORANGE))
    b.append(L(322, 130, 358, 130, stroke=BLUE, w=2.5)); b.append(T(340, 152, 'hệ số', size=13, weight='bold', fill=BLUE))
    b.append(L(366, 130, 452, 130, stroke=ORANGE, w=2.5)); b.append(T(409, 152, 'phần biến', size=13, weight='bold', fill='#b3601a'))
    b.append(L(462, 96, 528, 96, arrow=True))
    b.append(R(532, 62, 172, 66, fill=SOFT[2], stroke=HEAD[2], sw=2, rx=8))
    b.append(TL(618, 88, ['Bậc của đơn thức', 'là tổng số mũ: 2 + 1 = 3'], size=13, lh=22))
    b.append(T(W / 2, 200, 'Hai đơn thức đồng dạng: hệ số khác 0 và cùng phần biến', size=14, weight='bold'))
    for x, s in [(60, '3x²y'), (230, '5x²y'), (400, 'x²y')]:
        b.append(R(x, 218, 120, 52, fill=LGREY, stroke=INK, sw=2, rx=8)); b.append(T(x + 60, 252, s, size=22, weight='bold'))
    b.append(T(205, 252, '+', size=26, weight='bold')); b.append(T(375, 252, '−', size=26, weight='bold'))
    b.append(L(60, 288, 520, 288, stroke=ORANGE, w=2.5)); b.append(L(60, 282, 60, 294, stroke=ORANGE, w=2.5)); b.append(L(520, 282, 520, 294, stroke=ORANGE, w=2.5))
    b.append(T(290, 312, 'cùng phần biến x²y', size=13, weight='bold', fill='#b3601a'))
    b.append(T(542, 252, '=', size=26, weight='bold'))
    b.append(R(560, 214, 148, 60, fill=SOFT[1], stroke=HEAD[1], sw=2, rx=8))
    b.append(TL(634, 240, ['(3 + 5 − 1)x²y', '= 7x²y'], size=15, weight='bold', lh=24))
    b.append(T(634, 296, 'cộng (trừ) hệ số,', size=12, fill='#5b6773')); b.append(T(634, 312, 'giữ nguyên phần biến', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def _node(x, y, w, h, lines, ci, bold_first=True, size=13):
    b = [R(x - w / 2, y, w, h, fill=SOFT[ci], stroke=HEAD[ci], sw=2, rx=8)]
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * 9.5 + 5
    for i, s in enumerate(lines):
        b.append(T(x, y0 + i * 19, s, size=size, weight='bold' if (i == 0 and bold_first) else 'normal'))
    return ''.join(b)


def t8_phan_loai():
    W, H = 780, 392
    b = [title(W, 'Phân loại dữ liệu')]
    root = (390, 44, 160, 40)
    b.append(_node(390, 44, 160, 40, ['Dữ liệu'], 3, size=15))
    l1 = [(200, ['Dữ liệu định tính', 'không phải là số', 'vd: màu sắc, môn học yêu thích'], 0), (570, ['Dữ liệu định lượng', 'là số', 'vd: chiều cao, số anh chị em'], 1)]
    for cx, ln, ci in l1:
        b.append(L(390, 84, cx, 124, stroke=GREY, w=2))
    for cx, ln, ci in l1:
        b.append(_node(cx, 124, 270, 82, ln, ci))
    l2 = [(455, ['Số liệu rời rạc', 'đếm được', 'vd: số học sinh, số bàn thắng'], 2), (672, ['Số liệu liên tục', 'thu được từ đo lường', 'vd: chiều cao, cân nặng'], 2)]
    for cx, ln, ci in l2:
        b.append(L(570, 206, cx, 246, stroke=GREY, w=2))
    for cx, ln, ci in l2:
        b.append(_node(cx, 246, 206, 82, ln, ci, size=12.5))
    b.append(_node(164, 246, 300, 96, ['Cách thu thập dữ liệu', 'Trực tiếp: quan sát, phỏng vấn,', 'lập phiếu hỏi, làm thí nghiệm', 'Gián tiếp: sách, báo, tài liệu, internet'], 3, size=12.5))
    b.append(T(W / 2, 372, 'Dữ liệu phải hợp lí: tuổi một học sinh lớp 8 là 100, hay số học sinh nam là 20,5, là dữ liệu không hợp lí.', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


# ====================== Toán 7 ======================
def t7_phan_loai_dl():
    W, H = 780, 392
    b = [title(W, 'Phân loại dữ liệu')]
    b.append(_node(390, 44, 160, 40, ['Dữ liệu'], 3, size=15))
    l1 = [(200, ['Dữ liệu là số', '(định lượng)', 'vd: cân nặng, số giờ'], 1), (570, ['Dữ liệu không là số', '(định tính)', ''], 0)]
    for cx, ln, ci in l1:
        b.append(L(390, 84, cx, 124, stroke=GREY, w=2))
    b.append(_node(200, 124, 270, 82, ['Dữ liệu là số', '(định lượng)', 'vd: cân nặng, số giờ'], 1))
    b.append(_node(570, 124, 270, 82, ['Dữ liệu không là số', '(định tính)'], 0))
    l2 = [(455, ['Không sắp thứ tự được', 'vd: tên tỉnh'], 2), (672, ['Sắp thứ tự được', 'vd: Rất tốt, Tốt,', 'Trung bình, Kém'], 2)]
    for cx, ln, ci in l2:
        b.append(L(570, 206, cx, 246, stroke=GREY, w=2))
    for cx, ln, ci in l2:
        b.append(_node(cx, 246, 206, 82, ln, ci, size=12.5))
    b.append(_node(164, 246, 300, 96, ['Lưu ý về mã số', 'Số hiệu tuyến xe buýt chỉ là nhãn,', 'không phải dữ liệu số'], 1, size=12.5))
    b.append(T(W / 2, 372, 'Muốn kết luận cho cả tập thể, cần khảo sát mẫu ngẫu nhiên đủ rộng (tính đại diện).', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def t7_truc_so():
    W, H = 720, 236
    b = [title(W, 'Biểu diễn số hữu tỉ trên trục số')]
    cx, u, y = 360, 120, 140
    b.append(L(40, y, 686, y, arrow=True))
    for i in range(-10, 11):
        x = cx + i * u / 5
        major = i % 5 == 0
        b.append(L(x, y - (9 if major else 5), x, y + (9 if major else 5), w=2 if major else 1.4))
    for v in range(-2, 3):
        b.append(T(cx + v * u, y + 28, str(v).replace('-', '−'), size=14))
    for v, lab in [(-6 / 5, '−6/5 = −1,2'), (6 / 5, '6/5')]:
        x = cx + v * u
        b.append(dot(x, y, 5.5, fill=RED)); b.append(T(x, y - 18, lab, size=14, weight='bold', fill=NAVY))
    b.append(L(cx, 84, cx + u, 84, stroke=ORANGE, w=2.2)); b.append(L(cx, 78, cx, 90, stroke=ORANGE, w=2.2)); b.append(L(cx + u, 78, cx + u, 90, stroke=ORANGE, w=2.2))
    b.append(T(cx + u / 2 + 40, 70, 'chia đoạn đơn vị thành 5 phần bằng nhau', size=12.5, fill='#b3601a', weight='bold'))
    yd = 190
    for x1, x2 in [(cx - 6 * u / 5, cx), (cx, cx + 6 * u / 5)]:
        b.append(L(x1, yd, x2, yd, stroke=GREEN, w=2.4)); b.append(L(x1, yd - 7, x1, yd + 7, stroke=GREEN, w=2.4)); b.append(L(x2, yd - 7, x2, yd + 7, stroke=GREEN, w=2.4))
    b.append(T(cx, yd + 28, '−6/5 và 6/5 là hai số đối nhau: nằm hai phía của O, cách O cùng một khoảng', size=12.5, fill='#2f6b2a', weight='bold'))
    return svg(W, H, ''.join(b))


def t7_nhom_so():
    W, H = 720, 270
    b = [title(W, 'Số hữu tỉ: các dạng viết quen thuộc')]
    rows = [('Số nguyên', '3 = 3/1'), ('Số thập phân hữu hạn', '−1,2 = −6/5'), ('Hỗn số', '1 4/5 = 9/5')]
    for i, (h, e) in enumerate(rows):
        y = 50 + i * 72
        b.append(R(20, y, 270, 58, fill=SOFT[i], stroke=HEAD[i], sw=2, rx=8))
        b.append(T(155, y + 24, h, size=14, weight='bold')); b.append(T(155, y + 46, e, size=15, fill=NAVY, weight='bold'))
        b.append(L(292, y + 29, 426, 118 + i * 30, arrow=True))
    b.append(R(430, 88, 274, 120, fill=SOFT[3], stroke=HEAD[3], sw=2.5, rx=10))
    b.append(TL(567, 118, ['Số hữu tỉ', 'viết được dưới dạng a/b', 'a, b là số nguyên, b ≠ 0', 'Kí hiệu: ℚ'], size=14, lh=24))
    return svg(W, H, ''.join(b))


def t7_bien_co():
    W, H = 720, 340
    b = [title(W, 'Gieo một con xúc xắc: ba loại biến cố')]
    rows = [('Biến cố chắc chắn', 'số chấm nhỏ hơn 7', lambda n: n < 7, 'Cả 6 mặt đều thoả: luôn xảy ra', 0),
            ('Biến cố không thể', 'số chấm bằng 0', lambda n: n == 0, 'Không mặt nào thoả: không bao giờ xảy ra', 1),
            ('Biến cố ngẫu nhiên', 'số chấm là số chẵn', lambda n: n % 2 == 0, 'Mặt 2, 4, 6 thoả: không biết trước có xảy ra', 2)]
    for i, (h, d, p, v, ci) in enumerate(rows):
        y = 48 + i * 90
        b.append(R(14, y, 210, 74, fill=SOFT[ci], stroke=HEAD[ci], sw=2, rx=8))
        b.append(T(119, y + 30, h, size=14, weight='bold')); b.append(T(119, y + 54, d, size=13))
        for n in range(1, 7):
            x = 244 + (n - 1) * 52
            ok = p(n)
            b.append(R(x, y + 14, 44, 44, fill=LGREEN if ok else LGREY, stroke=GREEN if ok else GREY, sw=2.4 if ok else 1.5, rx=7))
            b.append(T(x + 22, y + 43, str(n), size=18, weight='bold', fill=INK if ok else '#7a8591'))
        b.append(TL(566, y + 30, wrap2(v, 24), size=12.5, anchor='start', lh=17))
    b.append(T(W / 2, H - 10, 'Ô xanh: mặt xúc xắc làm cho biến cố xảy ra.', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def wrap2(s, n):
    return su2.wrap(s, n)


FIG = []   # (môn, bài, tên file, hàm, chú thích)


def add(subj, bai, tag, fn, cap):
    FIG.append((subj, bai, 'tn-%s-b%s-%s.svg' % (subj, bai, tag), fn, cap))


add('toan12', 1, 'cuc-tri', t12_cuc_tri, 'Dấu của f′(x) và cực trị')
add('toan12', 2, 'gtln', t12_gtln, 'Giá trị lớn nhất, nhỏ nhất trên đoạn [a; b]')
add('toan12', 9, 'phan-vi', t12_phan_vi, 'Khoảng biến thiên và khoảng tứ phân vị')
add('toan12', 11, 'ho-nguyen-ham', t12_nguyen_ham, 'Họ nguyên hàm F(x) + C')
add('toan12', 12, 'tich-phan', t12_tich_phan, 'Tích phân và diện tích hình thang cong')
add('toan12', 13, 'ung-dung', t12_ung_dung, 'Diện tích hình phẳng và thể tích khối tròn xoay')
add('toan8', 1, 'don-thuc', t8_don_thuc, 'Đơn thức thu gọn và đơn thức đồng dạng')
add('toan8', 6, 'hang-dang-thuc', t8_hang_dang_thuc, 'Hằng đẳng thức bằng hình diện tích')
add('toan8', 18, 'phan-loai', t8_phan_loai, 'Phân loại dữ liệu')
add('toan7', 1, 'truc-so', t7_truc_so, 'Biểu diễn số hữu tỉ trên trục số')
add('toan7', 1, 'dang-viet', t7_nhom_so, 'Các dạng viết của số hữu tỉ')
add('toan7', 17, 'phan-loai', t7_phan_loai_dl, 'Phân loại dữ liệu')
add('toan7', 29, 'bien-co', t7_bien_co, 'Ba loại biến cố khi gieo xúc xắc')


def find(subj, bai):
    hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%s' % bai, '*.json'))
    assert len(hits) == 1, (subj, bai, hits)
    return hits[0]


if __name__ == '__main__':
    for subj, bai, nm, fn, cap in FIG:
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf8').write(fn())
    print('toan789: %d hình' % len(FIG))
    if '--attach' in sys.argv:
        for subj, bai, nm, fn, cap in FIG:
            p = find(subj, bai)
            data = json.load(open(p, encoding='utf8'))
            attach(subj, os.path.relpath(p, os.path.join(ROOT, 'content', subj)), len(data['theory']) - 1, nm, cap)
        print('đã gắn vào bài')
