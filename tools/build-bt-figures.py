# Hình cho bài tập Toán 6–9: vẽ theo số liệu có trong đề; chỉ ghi các số đề đã cho (không lộ đáp án).
import sys, os, math, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

W, H = 360, 250
FILL = '#eef5fb'
NC = '#1a56a0'


def fit(pts, box=(220, 150), cx=180, cy=112):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = min(box[0] / w if w else 1e9, box[1] / h if h else 1e9)
    ox, oy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return lambda x, y: (cx + (x - ox) * s, cy + (y - oy) * s)


def lab(x, y, s, size=14, col=NC, w='bold'):
    h = T(x, y + 5, s, size=size, weight=w, fill='white').replace('<text ', '<text stroke="white" stroke-width="4" stroke-linejoin="round" ')
    return h + T(x, y + 5, s, size=size, weight=w, fill=col)


def outward(c, p, d):
    ux, uy = unit(c[0], c[1], p[0], p[1])
    return p[0] + ux * d, p[1] + uy * d


def fig(pts, names=None, sides=None, rights=(), diags=(), angles=None, note=None, extra=None, fill=FILL, dash_h=None):
    tr = fit(pts)
    P = [tr(*p) for p in pts]
    n = len(P)
    cx = sum(p[0] for p in P) / n; cy = sum(p[1] for p in P) / n
    o = [POLY(P, fill=fill, stroke=INK, sw=2.2)]
    for k, (i, j, t) in enumerate(diags):
        o.append(L(P[i][0], P[i][1], P[j][0], P[j][1], stroke=GREY, w=1.8, dash='5 4'))
        if t:
            f = 0.5 if k == 0 else 0.25
            mx, my = P[i][0] + (P[j][0] - P[i][0]) * f, P[i][1] + (P[j][1] - P[i][1]) * f
            ux, uy = unit(P[i][0], P[i][1], P[j][0], P[j][1])
            o.append(lab(mx + (-uy) * (12 if k == 0 else -14), my + ux * (12 if k == 0 else -14), t, 13))
    for i in rights:
        a, b = P[(i + 1) % n], P[(i - 1) % n]
        o.append(right_angle(P[i][0], P[i][1], a[0], a[1], b[0], b[1], 11))
    if sides:
        for i, t in sides.items():
            a, b = P[i], P[(i + 1) % n]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ux_, uy_ = unit(cx, cy, mx, my)
            x, y = outward((cx, cy), (mx, my), 15 if abs(uy_) > abs(ux_) else 10 + 3.6 * len(t))
            o.append(lab(x, y, t))
    if angles:
        for i, t in angles.items():
            a, b = P[(i + 1) % n], P[(i - 1) % n]
            ua = unit(P[i][0], P[i][1], a[0], a[1]); ub = unit(P[i][0], P[i][1], b[0], b[1])
            o.append(angle_arc(P[i][0], P[i][1], P[i][0] + ua[0] * 40, P[i][1] + ua[1] * 40, P[i][0] + ub[0] * 40, P[i][1] + ub[1] * 40, r=24, color=RED))
            bx, by = ua[0] + ub[0], ua[1] + ub[1]
            d = math.hypot(bx, by) or 1
            if len(t) > 4:
                o.append(lab(P[i][0] - bx / d * 34 - 6, P[i][1] - by / d * 34 - 4, t, 13, RED))
            else:
                o.append(lab(P[i][0] + bx / d * 44, P[i][1] + by / d * 44, t, 13, RED))
    if names:
        for p, nm in zip(P, names):
            x, y = outward((cx, cy), p, 14)
            o.append(T(x, y + 5, nm, size=15, weight='bold'))
    if dash_h:
        i, (hx, hy), t = dash_h
        q = tr(hx, hy)
        o.append(L(P[i][0], P[i][1], q[0], q[1], stroke=GREY, w=1.8, dash='5 4'))
        o.append(right_angle(q[0], q[1], P[i][0], P[i][1], q[0] + 20, q[1], 9))
        o.append(lab((P[i][0] + q[0]) / 2 + 24, (P[i][1] + q[1]) / 2, t))
    if extra:
        o.append(extra(tr))
    if note:
        o.append(T(W / 2, H - 14, note, size=13, weight='bold', fill=GREY))
    return svg(W, H, ''.join(o))


# ---- hình cơ sở ----
def rect(w=3, h=2, names='ABCD', top=None, left=None, diag=None, both=False, note=None, rights=False, O=False, dl=None):
    pts = [(0, 0), (w, 0), (w, h), (0, h)]
    sides = {}
    if top: sides[0] = top
    if left: sides[3] = left
    dg = []
    if diag: dg.append((0, 2, diag))
    if both or O: dg.append((1, 3, dl))
    ex = None
    if O:
        ex = lambda tr: dot(*tr(w / 2, h / 2)) + T(tr(w / 2, h / 2)[0] + 2, tr(w / 2, h / 2)[1] - 8, 'O', size=14, weight='bold')
    return fig(pts, list(names) if names else None, sides, [0, 1, 2, 3] if rights else (), dg, note=note, extra=ex)


def square(a='', names='ABCD', note=None):
    return fig([(0, 0), (1, 0), (1, 1), (0, 1)], list(names) if names else None, {0: a} if a else {}, [0, 1, 2, 3], note=note)


def tri_r(AB=None, AC=None, BC=None, B=None, C=None, ang=36.87, names='ABC', note=None, med=False, hgt=False, w=None, h=None):
    """Vuông tại A: A(đáy trái), B(đáy phải), C(trên trái)."""
    t = math.tan(math.radians(ang))
    ww = w or 4
    hh = h or ww * t
    pts = [(0, hh), (ww, hh), (0, 0)]
    sides = {}
    if AB: sides[0] = AB
    if BC: sides[1] = BC
    if AC: sides[2] = AC
    ang_ = {}
    if B: ang_[1] = B
    if C: ang_[2] = C
    ex = None
    if med:
        def ex(tr):
            m = tr(ww / 2, hh / 2); a = tr(0, hh)
            return L(a[0], a[1], m[0], m[1], stroke=GREY, w=1.8, dash='5 4') + dot(*m) + T(m[0] + 12, m[1] - 4, 'M', size=14, weight='bold')
    if hgt:
        def ex(tr):
            # chân đường cao H từ A xuống BC
            bx, by, cx_, cy_ = ww, hh, 0, 0
            dx, dy = cx_ - bx, cy_ - by
            tparam = ((0 - bx) * dx + (hh - by) * dy) / (dx * dx + dy * dy)
            hx, hy = bx + tparam * dx, by + tparam * dy
            a = tr(0, hh); hh_ = tr(hx, hy)
            return L(a[0], a[1], hh_[0], hh_[1], stroke=GREY, w=1.8, dash='5 4') + T(hh_[0] + 12, hh_[1] - 2, 'H', size=14, weight='bold')
    return fig(pts, list(names) if names else None, sides, [0], angles=ang_, note=note, extra=ex)


def trap(a, b, h=None, off=None, names='ABCD', top=None, bot=None, side=None, hl=None, iso=True, ang=None, diag=None, note=None):
    off = (b - a) / 2 if (iso and off is None) else (off or 0)
    hh = h or 2
    pts = [(off, 0), (off + a, 0), (b, hh), (0, hh)]
    sides = {}
    if top: sides[0] = top
    if bot: sides[2] = bot
    if side: sides[1] = side; sides[3] = side
    dg = [(0, 2, diag[0]), (1, 3, diag[1])] if diag else []
    dh = (0, (off, hh), hl) if hl else None
    return fig(pts, list(names) if names else None, sides, diags=dg, angles=ang, note=note, dash_h=dh)


def ppar(b, h=None, s=1.2, names='ABCD', base=None, side=None, hl=None, O=False, diagl=None, ang=None, note=None):
    hh = h or b * 0.5
    pts = [(s, 0), (s + b, 0), (b, hh), (0, hh)]
    # đỉnh theo thứ tự A (trên trái) B (trên phải) C (dưới phải) D (dưới trái)
    sides = {}
    if base: sides[0] = base
    if side: sides[3] = side
    dh = (0, (s, hh), hl) if hl else None
    dg = []
    ex = None
    if diagl is not None:
        dg = [(0, 2, diagl[0]), (1, 3, diagl[1])]
    if O:
        ex = lambda tr: dot(*tr(b / 2 + s / 2, hh / 2)) + T(tr(b / 2 + s / 2, hh / 2)[0] + 2, tr(b / 2 + s / 2, hh / 2)[1] - 8, 'O', size=14, weight='bold')
    return fig(pts, list(names) if names else None, sides, diags=dg, angles=ang, note=note, dash_h=dh, extra=ex)


def rhombus(d1=3, d2=2, names=None, d1l=None, d2l=None, side=None, ang=None, note=None):
    pts = [(-d1 / 2, 0), (0, -d2 / 2), (d1 / 2, 0), (0, d2 / 2)]
    dg = []
    if d1l or d2l or True:
        dg = [(0, 2, d1l), (1, 3, d2l)]
    sides = {1: side} if side else {}
    return fig(pts, list(names) if names else None, sides, diags=[] if not (d1l or d2l) else dg, angles=ang, note=note)


def circle_fig(r=85, rad=None, dia=None, name='O', ex=None, note=None, extra_o=''):
    cx, cy = 180, 120
    o = [C(cx, cy, r, fill=FILL, stroke=INK, w=2.2), dot(cx, cy), T(cx + 2, cy + 20, name, size=14, weight='bold')]
    if rad:
        ang = math.radians(-35)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        o.append(L(cx, cy, x, y, stroke=RED, w=2.2)); o.append(lab((cx + x) / 2 + 6, (cy + y) / 2 - 12, rad, 14, RED))
    if dia:
        o.append(L(cx - r, cy, cx + r, cy, stroke=RED, w=2.2)); o.append(lab(cx, cy - 12, dia, 14, RED))
    o.append(extra_o)
    if note: o.append(T(W / 2, H - 14, note, size=13, weight='bold', fill=GREY))
    return svg(W, H, ''.join(o))


def on_circle(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def circ_rect(a, b, la, lb, note=None):
    cx, cy = 180, 122
    d = math.hypot(a, b); k = 90 / (d / 2)
    w, h = a * k, b * k
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    o = [C(cx, cy, 90, fill='none', stroke=INK, w=2.2), POLY(pts, fill=FILL, stroke=INK, sw=2.2), dot(cx, cy), T(cx + 2, cy + 18, 'O', size=13, weight='bold')]
    o.append(L(pts[0][0], pts[0][1], pts[2][0], pts[2][1], stroke=GREY, w=1.6, dash='5 4'))
    for p, nm, (dx, dy) in zip(pts, 'ABCD', ((-12, -6), (12, -6), (12, 14), (-12, 14))):
        o.append(T(p[0] + dx, p[1] + dy, nm, size=15, weight='bold'))
    o.append(lab(cx, pts[0][1] + 14, la)); o.append(lab(pts[0][0] + 14, cy - 22, lb))
    if note: o.append(T(W / 2, H - 14, note, size=13, weight='bold', fill=GREY))
    return svg(W, H, ''.join(o))


def circ_poly(n, note=None, names=True, rot=-90):
    cx, cy, r = 180, 122, 88
    P = regpoly(cx, cy, r, n, rot)
    o = [C(cx, cy, r, fill='none', stroke=INK, w=2.2), POLY(P, fill=FILL, stroke=INK, sw=2.2), dot(cx, cy), T(cx + 2, cy + 18, 'O', size=13, weight='bold')]
    if note: o.append(T(W / 2, H - 14, note, size=13, weight='bold', fill=GREY))
    return svg(W, H, ''.join(o))


def circ_tri_right(AB=None, AC=None, BC=None, R_=None, note=None):
    cx, cy, r = 180, 122, 88
    B = (cx + r, cy); C_ = (cx - r, cy)
    A = on_circle(cx, cy, r, 235)
    o = [C(cx, cy, r, fill='none', stroke=INK, w=2.2), POLY([A, B, C_], fill=FILL, stroke=INK, sw=2.2), dot(cx, cy)]
    o.append(right_angle(A[0], A[1], B[0], B[1], C_[0], C_[1], 11))
    o.append(T(A[0], A[1] - 10, 'A', size=15, weight='bold')); o.append(T(B[0] + 12, B[1] + 5, 'B', size=15, weight='bold')); o.append(T(C_[0] - 12, C_[1] + 5, 'C', size=15, weight='bold'))
    o.append(T(cx + 2, cy + 18, 'O', size=13, weight='bold'))
    if BC: o.append(lab(cx - 48, cy + 34, BC))
    if AB: o.append(lab((A[0] + B[0]) / 2 + 12, (A[1] + B[1]) / 2 - 10, AB))
    if AC: o.append(lab((A[0] + C_[0]) / 2 - 12, (A[1] + C_[1]) / 2 - 10, AC))
    if R_:
        o.append(L(cx, cy, cx + r * math.cos(math.radians(40)), cy + r * math.sin(math.radians(40)), stroke=RED, w=2)); o.append(lab(cx + 62, cy + 30, R_, 14, RED))
    if note: o.append(T(W / 2, H - 14, note, size=13, weight='bold', fill=GREY))
    return svg(W, H, ''.join(o))


def two_circles(R_, r_, ext=True, tl=None):
    k = 7.0
    Rr, rr = R_ * k, r_ * k
    cy = 125
    if ext:
        tot = Rr + rr + 0; x1 = 180 - (Rr + rr) / 2 + 0
        c1, c2 = (180 - (Rr + rr) / 2 + 0 - 0, cy), (180 + (Rr + rr) / 2 - 0, cy)
        c1 = (180 - (Rr + rr) / 2, cy); c2 = (c1[0] + Rr + rr, cy)
        # tâm1 cách đúng R + r
        c1 = (180 - (Rr + rr) / 2, cy); c2 = (c1[0] + Rr + rr, cy)
    else:
        c1 = (180 - (Rr - rr) / 2, cy); c2 = (c1[0] + (Rr - rr), cy)
    o = [C(c1[0], c1[1], Rr, fill=FILL, stroke=INK, w=2.2), C(c2[0], c2[1], rr, fill='#fdeede', stroke=INK, w=2.2), dot(*c1), dot(*c2)]
    o.append(T(c1[0] - 4, c1[1] + 20, 'O', size=14, weight='bold')); o.append(T(c2[0] + 4, c2[1] + 20, "O'", size=14, weight='bold'))
    o.append(L(c1[0], c1[1], c1[0] - Rr * math.cos(math.radians(40)), c1[1] - Rr * math.sin(math.radians(40)), stroke=RED, w=2)); o.append(lab(c1[0] - Rr * 0.5 - 12, c1[1] - Rr * 0.32 - 10, 'R = %d' % R_, 13, RED))
    o.append(L(c2[0], c2[1], c2[0] + rr * math.cos(math.radians(40)), c2[1] - rr * math.sin(math.radians(40)), stroke=RED, w=2)); o.append(lab(c2[0] + rr * 0.5 + 14, c2[1] - rr * 0.32 - 8, 'r = %d' % r_, 13, RED))
    return svg(W, H, ''.join(o))


def diameter_c30():
    cx, cy, r = 180, 122, 88
    A = (cx - r, cy); B = (cx + r, cy)
    Cc = on_circle(cx, cy, r, -60)  # góc ABC = 30° khi cung AC = 60°
    o = [C(cx, cy, r, fill='none', stroke=INK, w=2.2), POLY([A, B, Cc], fill=FILL, stroke=INK, sw=2.2), dot(cx, cy), T(cx + 2, cy + 18, 'O', size=13, weight='bold')]
    o.append(T(A[0] - 12, A[1] + 5, 'A', size=15, weight='bold')); o.append(T(B[0] + 12, B[1] + 5, 'B', size=15, weight='bold')); o.append(T(Cc[0] + 4, Cc[1] - 8, 'C', size=15, weight='bold'))
    o.append(angle_arc(B[0], B[1], A[0], A[1], Cc[0], Cc[1], r=26, color=RED)); o.append(lab(B[0] - 46, B[1] - 10, '30°', 13, RED))
    return svg(W, H, ''.join(o))


def rects_similar():
    o = []
    for (x, y, w, h, t1, t2, f) in ((40, 80, 90, 54, '5 cm', '3 cm', FILL), (195, 40, 150, 90, '10 cm', '6 cm', '#fdeede')):
        o.append(R(x, y, w, h, fill=f, stroke=INK, sw=2.2)); o.append(lab(x + w / 2, y - 12, t1)); o.append(lab(x - 24, y + h / 2, t2))
    return svg(W, H, ''.join(o))


def rect_ab(a, b):  # dùng khi cần ghi chú chiều
    return rect(a, b)


A60 = None

# ---- bảng đặc tả: (môn, bài, id câu) -> hình ----
SPEC = [
    ('toan6', 18, 'q04', lambda: square('9 cm')),
    ('toan6', 18, 'q08', lambda: square('', note='Chu vi 28 m')),
    ('toan6', 19, 'q04', lambda: rect(3.4, 2, top='12 cm', left='7 cm')),
    ('toan6', 19, 'q05', lambda: rhombus(3, 2, names='ABCD', note='Chu vi 36 cm')),
    ('toan6', 19, 'q06', lambda: rect(3.2, 2, diag='AC = 10 cm', both=True, dl='BD = ?')),
    ('toan6', 19, 'q07', lambda: trap(6, 10, 3.46, top='6 cm', bot='10 cm', side='4 cm')),
    ('toan6', 19, 'q08', lambda: ppar(4, 2, base='AB = 7 cm', side='BC = 4 cm') if False else ppar(5, 2.2, base='7 cm', side='4 cm')),
    ('toan6', 19, 'q09', lambda: rect(3.4, 2, top='15 cm', left='?', note='Chu vi 50 cm')),
    ('toan6', 20, 'q03', lambda: square('12 cm')),
    ('toan6', 20, 'q04', lambda: rect(3.2, 2, top='25 m', left='16 m')),
    ('toan6', 20, 'q05', lambda: ppar(5, 2.4, s=1.4, names=None, base='15 cm', hl='8 cm')),
    ('toan6', 20, 'q06', lambda: rhombus(3.125, 5, d1l='10 cm', d2l='16 cm')),
    ('toan6', 20, 'q07', lambda: trap(6, 14, 7, off=1.5, names=None, top='6 cm', bot='14 cm', hl='7 cm', iso=False)),
    ('toan6', 20, 'q08', lambda: square('', note='Chu vi 40 cm')),
    ('toan6', 20, 'q09', lambda: rect(3.2, 2.4, names=None, top='20 m', left='15 m')),
    ('toan7', 6, 'q12', lambda: square('', note='Diện tích 49 cm²')),
    ('toan7', 12, 'q10', lambda: tri_r(B='37°', C='?')),
    ('toan7', 15, 'q07', lambda: tri_r(ang=42, B='42°', C='?')),
    ('toan7', 15, 'q09', lambda: tri_r(ang=67.5, B='3x', C='x')),
    ('toan7', 15, 'q10', lambda: tri_r(B='x', C='x + 20°')),
    ('toan7', 23, 'q06', lambda: rect(3.4, 2, names=None, top='6 cm', left='?', note='Diện tích 24 cm²')),
    ('toan7', 27, 'q07', lambda: rect(3.4, 2, names=None, top='x + 5', left='x + 2')),
    ('toan7', 32, 'q05', lambda: square('6 cm')),
    ('toan7', 32, 'q07', lambda: rect(3.2, 2, top='8 cm', left='5 cm')),
    ('toan8', 2, 'q10', lambda: rect(3.4, 2, names=None, top='x + 3', left='x')),
    ('toan8', 4, 'q10', lambda: rect(3.4, 2, names=None, top='x + 4', left='x + 2')),
    ('toan8', 5, 'q09', lambda: rect(3.4, 2, names=None, top='?', left='3x', note='Diện tích 6x² + 9x')),
    ('toan8', 11, 'q03', lambda: trap(4, 6, 2, ang={0: '110°'})),
    ('toan8', 11, 'q04', lambda: trap(4, 6, 2, ang={0: '110°'})),
    ('toan8', 11, 'q05', lambda: trap(7, 11, 3.46, names=None, top='7 cm', bot='11 cm', side='4 cm')),
    ('toan8', 11, 'q07', lambda: trap(4, 6, 2, note='Ĉ = D̂, Â = B̂ = 3·Ĉ')),
    ('toan8', 11, 'q08', lambda: trap(4, 6, 2, diag=('AC = 9 cm', 'BD = ?'))),
    ('toan8', 11, 'q09', lambda: trap(12, 16, 3, names=None, top='12 cm', bot='16 cm', side='?', note='Chu vi 40 cm')),
    ('toan8', 12, 'q03', lambda: fig([(0, 2), (5, 2), (6.4, 0), (1.4, 0)], list('ABCD'), {}, angles={0: '65°'})),
    ('toan8', 12, 'q04', lambda: fig([(0, 2), (5, 2), (6.4, 0), (1.4, 0)], list('ABCD'), {}, angles={0: '65°'})),
    ('toan8', 12, 'q05', lambda: ppar(5, 2.2, names=None, base='6 cm', side='9 cm')),
    ('toan8', 12, 'q06', lambda: ppar(5, 2.2, O=True, diagl=('AC = 14 cm', None))),
    ('toan8', 12, 'q07', lambda: ppar(5, 2.2, names=None, base='10 cm', side='?', note='Chu vi 36 cm')),
    ('toan8', 12, 'q09', lambda: ppar(5, 2.2, O=True, diagl=(None, 'BD = 12 cm'))),
    ('toan8', 13, 'q04', lambda: rect(3.2, 2, diag='AC = 12 cm', both=True, dl='BD = ?')),
    ('toan8', 13, 'q05', lambda: rect(3.2, 2, O=True, diag='AC = ?', dl='OA = 7 cm') if False else rect(3.2, 2, O=True, diag='OA = 7 cm')),
    ('toan8', 13, 'q06', lambda: rect(3.4, 1.9, names=None, top='9 cm', left='4 cm')),
    ('toan8', 13, 'q07', lambda: tri_r(BC='20 cm', med=True)),
    ('toan8', 13, 'q08', lambda: rect(3.4, 1.4, names=None, top='3x', left='x', note='Chu vi 48 cm')),
    ('toan8', 13, 'q09', lambda: rect(3.4, 2, names=None, top='?', left='5 cm', note='Diện tích 60 cm²')),
    ('toan8', 14, 'q03', lambda: rhombus(3, 2, names='ABCD', side='9 cm')),
    ('toan8', 14, 'q04', lambda: rhombus(3, 2, names='ABCD', side='?', note='Chu vi 52 cm')),
    ('toan8', 14, 'q06', lambda: fig([(-1, 0), (0, -0.577), (1, 0), (0, 0.577)], list('ABCD'), {}, angles={0: '60°'})),
    ('toan8', 14, 'q07', lambda: square('8 cm')),
    ('toan8', 14, 'q09', lambda: rhombus(4.8, 2, d1l='10 cm', d2l='24 cm')) if False else ('toan8', 14, 'q09', lambda: rhombus(2.4, 5.0, d1l='10 cm', d2l='24 cm')),
    ('toan8', 26, 'q04', lambda: rect(3.4, 2, names=None, top='?', left='?', note='Chu vi 60 cm; dài hơn rộng 6 cm')),
    ('toan8', 35, 'q04', lambda: tri_r(AB='3', AC='4', BC='?', ang=53.13)),
    ('toan8', 35, 'q05', lambda: tri_r(AB='9', AC='12', BC='?', ang=53.13, note='Đơn vị: cm')),
    ('toan8', 35, 'q06', lambda: tri_r(AB='5', AC='?', BC='13', ang=67.38, note='Đơn vị: cm')),
    ('toan8', 35, 'q07', lambda: tri_r(AB='8', AC='?', BC='17', ang=61.93, note='Đơn vị: cm')),
    ('toan8', 35, 'q08', lambda: rect(4, 3, names=None, top='8 cm', left='6 cm', diag='?')),
    ('toan8', 35, 'q09', lambda: rhombus(4, 3, d1l='16 cm', d2l='12 cm', side='?')),
    ('toan8', 35, 'q11', lambda: tri_r(AB='6 cm', AC='8 cm', ang=53.13, names=None)),
    ('toan8', 36, 'q06', lambda: tri_r(AB='6', AC='8', BC='10', ang=53.13, hgt=True, note='Đơn vị: cm')),
    ('toan8', 36, 'q07', lambda: tri_r(AB='6', AC='?', BC='10', ang=53.13, hgt=True, note='Đơn vị: cm')),
    ('toan8', 37, 'q04', rects_similar),
    ('toan9', 3, 'q08', lambda: rect(3.4, 2, names=None, top='x + 7', left='x', note='Chu vi 34 m')),
    ('toan9', 11, 'q05', lambda: tri_r(AC='6', BC='10', ang=36.87, B='α', w=4)),
    ('toan9', 11, 'q06', lambda: tri_r(AB='8', BC='10', ang=36.87, B='α', w=4)),
    ('toan9', 11, 'q07', lambda: tri_r(AB='12', AC='5', ang=22.62, B='α', w=4)),
    ('toan9', 12, 'q03', lambda: tri_r(BC='12', B='30°', ang=30)),
    ('toan9', 12, 'q04', lambda: tri_r(BC='8', B='60°', ang=60)),
    ('toan9', 12, 'q05', lambda: tri_r(AC='7', AB='?', B='45°', ang=45)),
    ('toan9', 12, 'q06', lambda: tri_r(B='35°', C='?', ang=35)),
    ('toan9', 13, 'q04', lambda: circle_fig(rad='4 cm')),
    ('toan9', 13, 'q05', lambda: circle_fig(dia='15 cm')),
    ('toan9', 13, 'q07', lambda: circ_tri_right(BC='BC = 10', R_='R = ?')),
    ('toan9', 13, 'q08', lambda: circ_rect(6, 8, '6', '8')),
    ('toan9', 14, 'q05', lambda: circ_poly(6)),
    ('toan9', 14, 'q09', lambda: circ_poly(3)),
    ('toan9', 15, 'q03', lambda: circle_fig(rad='R = 5')),
    ('toan9', 17, 'q06', lambda: two_circles(7, 5, True)),
    ('toan9', 17, 'q07', lambda: two_circles(10, 4, False)),
    ('toan9', 21, 'q03', lambda: rect(3.4, 2, names=None, top='x + 3', left='x', note='Diện tích 70 m²')),
    ('toan9', 21, 'q06', lambda: tri_r(AB='?', AC='?', BC='13 cm', ang=53.13, names=None, note='Hai cạnh góc vuông hơn kém nhau 7 cm')),
    ('toan9', 27, 'q08', diameter_c30),
    ('toan9', 28, 'q03', lambda: circ_tri_right(AB='6', AC='8', R_='R = ?')),
    ('toan9', 28, 'q04', lambda: circ_tri_right(AB='5', AC='12', R_='R = ?')),
    ('toan9', 28, 'q08', lambda: circ_tri_right(BC='?', R_='R = 7,5')),
    ('toan9', 29, 'q05', lambda: circ_poly(4, rot=-135, note='Cạnh hình vuông = 4')),
    ('toan9', 29, 'q07', lambda: circ_rect(5, 12, '5', '12')),
]
SPEC = [s for s in SPEC if isinstance(s, tuple) and len(s) == 4]


def find_lesson(subj, bai):
    hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%d' % bai, '*.json'))
    assert len(hits) == 1, (subj, bai, hits)
    return hits[0]


if __name__ == '__main__':
    done = {}
    for subj, bai, qid, fn in SPEC:
        name = 'bt-%s-b%d-%s.svg' % (subj, bai, qid)
        d = os.path.join(ROOT, 'content', subj, 'figures')
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name), 'w', encoding='utf8').write(fn())
        p = find_lesson(subj, bai)
        data = json.load(open(p, encoding='utf8'))
        found = False
        for sec in ('items', 'examples'):
            for it in data.get(sec, []):
                if it.get('id') == qid:
                    it['figure'] = 'figures/' + name; found = True; break
            if found: break
        assert found, (subj, bai, qid)
        with open(p, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
    print('bt: %d hình' % len(SPEC))
