# Hình cho bài tập Vật lí 6, 7, 8, 9, 12 (đồ thị, phản xạ, gương phẳng, thấu kính, lực kế).
# Sơ đồ minh họa vẽ theo số liệu trong đề; các đại lượng cần tìm ghi "?" và không ghi giá trị trên trục.
import sys, os, math, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

NAVY = '#1a56a0'


def txt(x, y, s, size=13, fill=INK, anchor='middle', weight='normal'):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s" stroke="white" '
            'stroke-width="3" paint-order="stroke">%s</text>' % (x, y, anchor, size, weight, fill, s))


def plot(xl, yl, xmax, ymax, xt, yt, curves, pts, W=400, H=280, ttl=None):
    """xt, yt: [(giá trị, nhãn)]; curves: [(điểm, màu, dash)]; pts: [(x, y, nhãn, dx, dy, anchor, guide)]."""
    ml, mr, mt, mb = 64, 24, 48 if ttl else 22, 46
    fx = lambda v: ml + v / xmax * (W - ml - mr)
    fy = lambda v: H - mb - v / ymax * (H - mb - mt)
    b = []
    if ttl:
        b.append(T(W / 2, 20, ttl, size=15, weight='bold'))
    b.append(L(ml, H - mb, W - mr + 6, H - mb, arrow=True))
    b.append(L(ml, H - mb, ml, mt - 10, arrow=True))
    for v, s in xt:
        b.append(L(fx(v), H - mb, fx(v), H - mb + 5, w=1.5)); b.append(T(fx(v), H - mb + 20, s, size=13))
    for v, s in yt:
        b.append(L(ml - 5, fy(v), ml, fy(v), w=1.5)); b.append(T(ml - 8, fy(v) + 4, s, size=13, anchor='end'))
    b.append(T(W - mr - 4, H - 8, xl, size=14, anchor='end'))
    b.append(T(ml + 6, mt - 10, yl, size=14, anchor='start'))
    b.append(T(ml - 8, H - mb + 18, 'O', size=13, anchor='end'))
    for p, col, dash in curves:
        b.append(PL([(fx(x), fy(y)) for x, y in p], stroke=col, w=3, dash=dash))
    for x, y, s, dx, dy, an, g in pts:
        if g:
            b.append(L(fx(x), fy(y), fx(x), H - mb, stroke=GREY, w=1.3, dash='4 3'))
            b.append(L(fx(x), fy(y), ml, fy(y), stroke=GREY, w=1.3, dash='4 3'))
        b.append(dot(fx(x), fy(y), 4.5, fill=RED))
        if s:
            b.append(txt(fx(x) + dx, fy(y) + dy, s, size=13, fill=NAVY, anchor=an, weight='bold'))
    return svg(W, H, ''.join(b))


# ---------- Lí 7 ----------
def st_graph():
    return plot('t (h)', 's (km)', 5.4, 240, [(i, str(i)) for i in range(1, 6)], [(60 * i, str(60 * i)) for i in range(1, 5)],
                [([(0, 0), (3, 180), (4, 180), (5, 220)], BLUE, None)],
                [(3, 180, '(3 h; 180 km)', -8, -10, 'end', True), (4, 180, '(4 h; 180 km)', 0, 24, 'middle', False),
                 (5, 220, '(5 h; 220 km)', -8, -12, 'end', True)], W=440, H=290, ttl='Đồ thị s – t của ô tô')


def reflect(mode):
    W, H = 400, 250
    ox, oy, ln = 200, 190, 135
    i = {'q06': 30, 'q07': 60, 'q08': 30}[mode]
    ri = math.radians(i)
    sx, sy = ox - ln * math.sin(ri), oy - ln * math.cos(ri)
    rx, ry = ox + ln * math.sin(ri), oy - ln * math.cos(ri)
    b = [T(W / 2, 22, 'Phản xạ ánh sáng trên gương phẳng', size=15, weight='bold')]
    b.append(R(50, oy, 300, 10, fill=LGREY, stroke=INK, sw=2))
    for k in range(0, 300, 14):
        b.append(L(50 + k + 10, oy + 10, 50 + k, oy + 20, stroke=GREY, w=1.5))
    b.append(L(ox, oy, ox, 48, stroke=GREY, w=1.5, dash='6 4'))
    b.append(T(ox + 8, 56, 'N', size=14, anchor='start', weight='bold'))
    b.append(L(sx, sy, ox, oy, stroke=ORANGE, w=3, arrow=True))
    b.append(L(ox, oy, rx, ry, stroke=ORANGE, w=3, arrow=True))
    b.append(dot(ox, oy, 4)); b.append(T(ox + 10, oy + 26, 'I', size=14, weight='bold'))
    b.append(T(sx - 8, sy - 6, 'S', size=14, anchor='end', weight='bold'))
    b.append(T(rx + 8, ry - 6, 'R', size=14, anchor='start', weight='bold'))
    r = 44
    if mode == 'q06':
        b.append(angle_arc(ox, oy, ox, 100, sx, sy, r, BLUE, 2)); b.append(txt(ox - 38, oy - 58, 'i = 30°', 13, BLUE, 'middle', 'bold'))
        b.append(angle_arc(ox, oy, ox, 100, rx, ry, r, RED, 2)); b.append(txt(ox + 38, oy - 58, 'i′ = ?', 13, RED, 'middle', 'bold'))
    elif mode == 'q07':
        b.append(angle_arc(ox, oy, ox - 100, oy, sx, sy, 50, BLUE, 2)); b.append(txt(ox - 78, oy - 20, '30°', 13, BLUE, 'middle', 'bold'))
        b.append(angle_arc(ox, oy, ox, 100, sx, sy, 36, RED, 2)); b.append(txt(ox - 18, oy - 92, 'i = ?', 13, RED, 'end', 'bold'))
    else:
        b.append(angle_arc(ox, oy, ox, 100, sx, sy, 50, BLUE, 2)); b.append(txt(ox - 42, oy - 62, 'i = 30°', 13, BLUE, 'end', 'bold'))
        b.append(angle_arc(ox, oy, sx, sy, rx, ry, 100, RED, 2)); b.append(txt(ox, oy - 108, '? ', 15, RED, 'middle', 'bold'))
    return svg(W, H, ''.join(b))


def mirror(d, who):
    W, H = 440, 220
    s = 28
    mx = 220
    b = [T(W / 2, 22, 'Ảnh của vật qua gương phẳng', size=15, weight='bold')]
    b.append(R(mx - 5, 44, 10, 150, fill=LGREY, stroke=INK, sw=2))
    for k in range(0, 150, 12):
        b.append(L(mx + 5, 54 + k, mx + 15, 44 + k, stroke=GREY, w=1.5))
    ox, ix = mx - d * s, mx + d * s
    y0 = 160
    b.append(L(ox, y0, ox, y0 - 60, stroke=INK, w=4, arrow=True)); b.append(T(ox, y0 + 18, who, size=14, weight='bold'))
    b.append(L(ix, y0, ix, y0 - 60, stroke=GREY, w=3, dash='5 4', arrow=True)); b.append(T(ix, y0 + 18, 'ảnh', size=14, weight='bold', fill=GREY))
    b.append(L(mx, y0 - 76, ox, y0 - 76, stroke=BLUE, w=1.8)); b.append(L(mx, y0 - 82, mx, y0 - 70, stroke=BLUE, w=1.8)); b.append(L(ox, y0 - 82, ox, y0 - 70, stroke=BLUE, w=1.8))
    b.append(txt((mx + ox) / 2, y0 - 82, '%d m' % d, 14, BLUE, 'middle', 'bold'))
    b.append(L(mx, y0 - 76, ix, y0 - 76, stroke=RED, w=1.8, dash='5 4')); b.append(L(ix, y0 - 82, ix, y0 - 70, stroke=RED, w=1.8))
    b.append(txt((mx + ix) / 2, y0 - 82, '? m', 14, RED, 'middle', 'bold'))
    return svg(W, H, ''.join(b))


# ---------- Lí 12 ----------
def boyle(v1, p1, v2, p2, vmax, pmax, xl, yl, xt, yt, vlab, plab):
    k = v1 * p1
    pts = [(v, k / v) for v in [vmax * 0.12 + i * (vmax * 0.88 / 40) for i in range(41)] if k / v <= pmax * 0.97]
    return plot(xl, yl, vmax, pmax, xt, yt, [(pts, BLUE, None)],
                [(v1, p1, vlab[0], -4, 24, 'end', True), (v2, p2, vlab[1], 12, -8, 'start', True)], W=400, H=290, ttl='Quá trình đẳng nhiệt')


def charles():
    return plot('T (K)', 'V (L)', 700, 10, [(300, '300'), (600, '600')], [(4, '4')],
                [([(0, 0), (650, 650 / 75)], BLUE, None)],
                [(300, 4, '(300 K; 4 L)', 12, 18, 'start', True), (600, 8, '(600 K; V = ?)', -10, -12, 'end', True)], W=400, H=290, ttl='Quá trình đẳng áp')


def isochoric():
    return plot('T (K)', 'p (10⁵ Pa)', 500, 4, [(300, '300'), (450, '450')], [(2, '2')],
                [([(0, 0), (480, 3.2)], BLUE, None)],
                [(300, 2, '(300 K; 2·10⁵ Pa)', 12, 18, 'start', True), (450, 3, '(450 K; p = ?)', -10, -12, 'end', True)], W=400, H=290, ttl='Quá trình đẳng tích')


def decay():
    data = [(0, 151), (30, 85), (60, 55), (120, 31), (180, 22), (240, 15), (300, 11), (360, 9)]
    return plot('t (s)', 'H (Bq)', 380, 170, [(60 * i, str(60 * i)) for i in range(1, 7)], [(40 * i, str(40 * i)) for i in range(1, 5)],
                [(data, BLUE, None)], [(x, y, '', 0, 0, 'start', False) for x, y in data],
                W=440, H=290, ttl='Bảng 25.1: độ phóng xạ H theo thời gian t')


# ---------- Lí 9: thấu kính hội tụ ----------
def lens(f, d, s):
    W, H = 440, 260
    ox, y0, h = 225, 118, 44
    dp = f * d / (d - f)
    b = [T(W / 2, 22, 'Thấu kính hội tụ: f = %d cm, d = %d cm' % (f, d), size=15, weight='bold')]
    b.append(L(20, y0, W - 20, y0, stroke=GREY, w=1.5))
    b.append(L(ox, y0, ox, y0 - 66, w=2.5, arrow=True)); b.append(L(ox, y0, ox, y0 + 62, w=2.5, arrow=True))
    xo = ox - d * s
    b.append(L(xo, y0, xo, y0 - h, stroke=INK, w=3.5, arrow=True)); b.append(T(xo, y0 + 16, 'A', size=13, weight='bold'))
    ix, ih = ox + dp * s, h * dp / d
    top = (ix, y0 + ih)
    b.append(L(xo, y0 - h, ox, y0 - h, stroke=ORANGE, w=2))
    b.append(L(ox, y0 - h, top[0], top[1], stroke=ORANGE, w=2))
    b.append(L(xo, y0 - h, ox, y0, stroke=BLUE, w=2))
    b.append(L(ox, y0, top[0], top[1], stroke=BLUE, w=2))
    b.append(L(ix, y0, ix, y0 + ih, stroke=GREY, w=3, dash='5 4', arrow=True))
    for x, n in ((ox - f * s, 'F'), (ox + f * s, 'F′'), (ox, 'O')):
        b.append(L(x, y0 - 4, x, y0 + 4, w=2)); b.append(txt(x, y0 - 8 if n != 'O' else y0 + 16, n, 13, INK, 'middle', 'bold'))
    b.append(txt(ix + 8, y0 + ih + 16, 'ảnh', 13, GREY, 'start', 'bold'))
    yd = y0 + 78
    b.append(L(xo, yd, ox, yd, stroke=BLUE, w=1.6)); b.append(L(xo, yd - 5, xo, yd + 5, stroke=BLUE, w=1.6)); b.append(L(ox, yd - 5, ox, yd + 5, stroke=BLUE, w=1.6))
    b.append(txt((xo + ox) / 2, yd + 18, 'd = %d cm' % d, 13, BLUE, 'middle', 'bold'))
    yf = y0 + 112
    b.append(L(ox, yf, ox + f * s, yf, stroke=GREEN, w=1.6)); b.append(L(ox, yf - 5, ox, yf + 5, stroke=GREEN, w=1.6)); b.append(L(ox + f * s, yf - 5, ox + f * s, yf + 5, stroke=GREEN, w=1.6))
    b.append(txt(ox + f * s / 2, yf + 18, 'f = %d cm' % f, 13, GREEN, 'middle', 'bold'))
    b.append(L(ox, yf + 36 - 14, ix, yf + 36 - 14, stroke=RED, w=1.6, dash='5 4')) if False else None
    b.append(txt(ix, y0 - 24 if ih > 0 else y0, "d′ = ? cm", 13, RED, 'middle', 'bold'))
    return svg(W, H + 24, ''.join(b))


# ---------- Lí 6, 8: lực kế ----------
def ruler_n():
    W, H = 380, 130
    x0, x1, y = 40, 340, 60
    b = [T(W / 2, 22, 'Một khoảng 1 N trên lực kế', size=15, weight='bold')]
    b.append(R(x0 - 14, y - 22, x1 - x0 + 28, 44, fill=LYELLOW, stroke=INK, sw=2, rx=4))
    for k in range(6):
        x = x0 + k * (x1 - x0) / 5
        b.append(L(x, y - 22, x, y + (2 if k in (0, 5) else -4), w=2 if k in (0, 5) else 1.5))
    b.append(T(x0, y + 40, '0', size=14, weight='bold')); b.append(T(x1, y + 40, '1 N', size=14, weight='bold'))
    b.append(L(x0, y + 60 - 8, x0 + (x1 - x0) / 5, y + 60 - 8, stroke=RED, w=2)); b.append(txt(x0 + (x1 - x0) / 10, y + 68, '1 vạch = ? N', 13, RED, 'middle', 'bold'))
    return svg(W, H + 16, ''.join(b))


def scale_body(x, y, top_label):
    b = [R(x - 18, y, 36, 70, fill=LYELLOW, stroke=INK, sw=2, rx=4)]
    for k in range(6):
        b.append(L(x - 18, y + 9 + k * 10, x - 8, y + 9 + k * 10, w=1.2))
    b.append(L(x, y - 24, x, y, w=2)); b.append(C(x, y - 30, 6, stroke=INK, w=2))
    return ''.join(b)


def archimedes():
    W, H = 440, 280
    b = [T(W / 2, 22, 'Lực kế khi treo quả cầu', size=15, weight='bold')]
    b.append(L(40, 40, 400, 40, w=3))
    # trong không khí
    x = 110
    b.append(L(x, 40, x, 70, w=2)); b.append(scale_body(x, 100, ''))
    b.append(L(x, 170, x, 192, w=2)); b.append(C(x, 208, 16, fill='#c9ced6', stroke=INK, w=2))
    b.append(txt(x + 36, 140, '8 N', 15, NAVY, 'start', 'bold')); b.append(T(x, 276, 'Ngoài không khí', size=13))
    # trong nước
    x = 310
    b.append(L(x, 40, x, 70, w=2)); b.append(scale_body(x, 100, ''))
    b.append(R(x - 55, 172, 110, 84, fill='#cfe3f5', stroke=INK, sw=2))
    b.append(L(x, 170, x, 192, w=2)); b.append(C(x, 208, 16, fill='#c9ced6', stroke=INK, w=2))
    b.append(txt(x + 36, 140, '6,5 N', 15, NAVY, 'start', 'bold')); b.append(T(x, 276, 'Nhúng trong nước', size=13))
    return svg(W, H + 6, ''.join(b))


SPEC = [
    ('ly7', 10, 'q05', st_graph), ('ly7', 10, 'q06', st_graph), ('ly7', 10, 'q07', st_graph),
    ('ly7', 16, 'q06', lambda: reflect('q06')), ('ly7', 16, 'q07', lambda: reflect('q07')), ('ly7', 16, 'q08', lambda: reflect('q08')),
    ('ly7', 17, 'q06', lambda: mirror(3, 'Vật')), ('ly7', 17, 'q07', lambda: mirror(4, 'A')), ('ly7', 17, 'q08', lambda: mirror(5, 'Vật')),
    ('ly12', 9, 'q06', lambda: boyle(5, 2, 2.5, 4, 6, 6, 'V (L)', 'p (10⁵ Pa)', [(5, '5')], [(2, '2'), (4, '4')], ('(5 L; 2·10⁵ Pa)', '(V = ?; 4·10⁵ Pa)'), None)),
    ('ly12', 9, 'q07', lambda: boyle(30, 2, 15, 4, 40, 6, 'V (cm³)', 'p (atm)', [(30, '30'), (15, '15')], [(2, '2')], ('(30 cm³; 2 atm)', '(15 cm³; p = ?)'), None)),
    ('ly12', 9, 'q08', lambda: boyle(8, 3, 6, 4, 10, 6, 'V (L)', 'p (atm)', [(8, '8'), (6, '6')], [(3, '3')], ('(8 L; 3 atm)', '(6 L; p = ?)'), None)),
    ('ly12', 10, 'q06', charles), ('ly12', 13, 'q03', isochoric),
    ('ly12', 25, 'q07', decay), ('ly12', 25, 'q08', decay),
    ('ly9', 8, 'q05', lambda: lens(20, 60, 3.2)), ('ly9', 8, 'q06', lambda: lens(12, 24, 7)), ('ly9', 10, 'q07', lambda: lens(15, 30, 5.5)),
    ('ly6', 40, 'q06', ruler_n), ('ly8', 17, 'q08', archimedes),
]


def find(subj, bai):
    hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%d' % bai, '*.json'))
    assert len(hits) == 1, (subj, bai, hits)
    return hits[0]


if __name__ == '__main__':
    for subj, bai, qid, fn in SPEC:
        name = 'bt-%s-b%d-%s.svg' % (subj, bai, qid)
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name), 'w', encoding='utf8').write(fn())
        p = find(subj, bai)
        data = json.load(open(p, encoding='utf8'))
        ok = False
        for sec in ('items', 'examples'):
            for it in data.get(sec, []):
                if it.get('id') == qid:
                    it['figure'] = 'figures/' + name; ok = True; break
            if ok: break
        assert ok, (subj, bai, qid)
        with open(p, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
    print('ly-bt: %d hình' % len(SPEC))
