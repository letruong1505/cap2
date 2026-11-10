# Toán 12: hình cho câu hỏi diện tích hình phẳng và thể tích khối tròn xoay (chương IV).
# Hình chỉ vẽ miền/vật thể mà đề đã nêu (không ghi kết quả); đồ thị minh hoạ, không phải bản vẽ đo.
import sys, os, json, glob, math, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *


def _load(name, fn):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(__file__), fn))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


tn = _load('tn789', 'build-toan789-figures.py')
Ax, halo, NAVY = tn.Ax, tn.halo, tn.NAVY
W, H = 460, 300
pi = math.pi
F_BLUE, F_ORANGE = '#cfe0f2', '#fde3bd'


def _axes_ticks(A, xt, b):
    b.append(A.axes(o=False))
    ya = A.fy(0) if A.y0 <= 0 <= A.y1 else A.fy(A.y0)
    for x, s in xt:
        b.append(L(A.fx(x), ya - 4, A.fx(x), ya + 4, w=1.6))
        b.append(halo(A.fx(x), ya + 18, s, 13, INK, 'middle', 'bold'))


def area_fig(xr, yr, curves, region, xt, labs, ttl=None):
    A = Ax(xr[0], xr[1], yr[0], yr[1], 30, W - 26, H - 34, 38 if ttl else 24)
    b = []
    if ttl:
        b.append(T(W / 2, 20, ttl, size=14, weight='bold'))
    f, g, a, c = region
    b.append(A.area(f, a, c, F_BLUE, g=g, op=0.95))
    _axes_ticks(A, xt, b)
    for fn, x0, x1, col, dash in curves:
        b.append(PL(A.curve(fn, x0, x1, 120), stroke=col, w=3, dash=dash))
    for x in (a, c):
        y2 = g(x) if g else 0
        b.append(L(A.fx(x), A.fy(y2), A.fx(x), A.fy(f(x)), stroke=INK, w=1.8, dash='5 3'))
    for s, x, y, an, col in labs:
        b.append(halo(A.fx(x), A.fy(y), s, 13.5, col, an, 'bold'))
    return svg(W, H, ''.join(b))


def rev_fig(xr, yr, prof, a, c, xt, labs, extra=None, ttl=None, half=True, cap_a=True):
    A = Ax(xr[0], xr[1], yr[0], yr[1], 30, W - 26, H - 34, 38 if ttl else 24)
    b = []
    if ttl:
        b.append(T(W / 2, 20, ttl, size=14, weight='bold'))
    up = A.curve(prof, a, c, 100); lo = A.curve(lambda x: -prof(x), a, c, 100)
    pts = up + list(reversed(lo))
    b.append('<polygon points="%s" fill="%s" stroke="none"/>' % (' '.join('%.1f,%.1f' % q for q in pts), '#e4eef8'))
    if half:
        b.append('<polygon points="%s" fill="%s" stroke="none"/>' % (
            ' '.join('%.1f,%.1f' % q for q in up + [(A.fx(c), A.fy(0)), (A.fx(a), A.fy(0))]), F_ORANGE))
    _axes_ticks(A, xt, b)
    if extra:
        b.append(PL(A.curve(extra[0], extra[1], extra[2], 120), stroke=GREY, w=1.8, dash='5 4'))
    b.append(PL(up, stroke=BLUE, w=3)); b.append(PL(lo, stroke=BLUE, w=2, dash='6 4'))
    for x in (a, c):
        r = prof(x)
        if r < 1e-6:
            continue
        ry = A.fy(0) - A.fy(r)
        b.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="2"/>' % (A.fx(x), A.fy(0), ry * 0.26, ry, BLUE))
    for s, x, y, an, col in labs:
        b.append(halo(A.fx(x), A.fy(y), s, 13.5, col, an, 'bold'))
    return svg(W, H, ''.join(b))


def sq(x): return math.sqrt(x)


SPEC = {}


def reg(name, fn):
    SPEC[name] = fn


# ---------- bài 13 ----------
reg('b13-q01', lambda: area_fig((-0.4, 2.5), (-1, 9.5), [(lambda x: x ** 3, 0, 2.3, BLUE, None)], (lambda x: x ** 3, None, 0, 2),
                                [(0, '0'), (2, '2')], [('y = x³', 1.75, 6.2, 'end', NAVY)]))
reg('b13-q02', lambda: area_fig((-0.4, 6.9), (-1.5, 1.5), [(math.sin, 0, 2 * pi, BLUE, None)], (math.sin, None, 0, 2 * pi),
                                [(0, '0'), (2 * pi, '2π')], [('y = sin x', 1.35, 1.2, 'middle', NAVY)]))
reg('b13-q03', lambda: area_fig((-0.6, 3.6), (-5, 6), [(lambda x: x * x - 4, 0, 3.3, BLUE, None)], (lambda x: x * x - 4, None, 0, 3),
                                [(0, '0'), (3, '3')], [('y = x² − 4', 3.3, 5.0, 'end', NAVY)]))
reg('b13-q04', lambda: area_fig((-1.7, 1.7), (-0.6, 4.6), [(lambda x: 4 - x * x, -1.4, 1.4, BLUE, None), (lambda x: x * x, -1.4, 1.4, GREEN, None)],
                                (lambda x: 4 - x * x, lambda x: x * x, -1, 1), [(-1, '−1'), (1, '1')],
                                [('y = 4 − x²', 1.65, 3.8, 'end', NAVY), ('y = x²', 1.65, 0.9, 'end', '#2f6b2a')]))
reg('b13-q05', lambda: area_fig((-0.2, 1.7), (-0.25, 1.35), [(math.sin, 0, 1.55, BLUE, None), (math.cos, 0, 1.55, ORANGE, None)],
                                (math.cos, math.sin, 0, pi / 4), [(0, '0'), (pi / 4, 'π/4')],
                                [('y = cos x', 0.3, 1.2, 'middle', '#b3601a'), ('y = sin x', 1.6, 1.06, 'end', NAVY)]))
reg('b13-q06', lambda: area_fig((-0.2, 4.7), (-2.4, 2.8), [(sq, 0, 4.5, BLUE, None), (lambda x: x - 2, 0, 4.5, GREEN, None)],
                                (sq, lambda x: x - 2, 1, 4), [(1, '1'), (4, '4')],
                                [('y = √x', 2.6, 2.4, 'end', NAVY), ('y = x − 2', 4.6, 0.95, 'end', '#2f6b2a')]))
reg('b13-q10', lambda: rev_fig((-0.25, 1.4), (-1.35, 1.35), sq, 0, 1, [(0, '0'), (1, '1')],
                               [('y = √x', 0.55, 1.18, 'middle', NAVY)]))
reg('b13-q12', lambda: rev_fig((-0.5, 4.8), (-2.9, 2.9), lambda x: x / 2, 0, 4, [(0, '0'), (4, '4')],
                               [('y = x/2', 2.0, 1.45, 'end', NAVY)]))


def _trap():
    A = Ax(-0.6, 4.2, -2.6, 2.6, 30, W - 26, H - 34, 24)
    h, R, r = 3.0, 2.0, 1.0
    b = []
    prof = lambda x: r + (R - r) * x / h
    up = A.curve(prof, 0, h, 50); lo = A.curve(lambda x: -prof(x), 0, h, 50)
    b.append('<polygon points="%s" fill="#e4eef8"/>' % ' '.join('%.1f,%.1f' % q for q in up + list(reversed(lo))))
    b.append('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in [A.pt(0, 0), A.pt(h, 0), A.pt(h, R), A.pt(0, r)]), F_ORANGE))
    b.append(A.axes(o=False))
    b.append(PL(up, stroke=BLUE, w=3)); b.append(PL(lo, stroke=BLUE, w=2, dash='6 4'))
    for x, rad in [(0, r), (h, R)]:
        ry = A.fy(0) - A.fy(rad)
        b.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="2"/>' % (A.fx(x), A.fy(0), ry * 0.26, ry, BLUE))
    b.append(L(A.fx(0), A.fy(0), A.fx(0), A.fy(r), stroke=INK, w=2)); b.append(L(A.fx(h), A.fy(0), A.fx(h), A.fy(R), stroke=INK, w=2))
    for s, x, y, an in [('O', -0.12, -0.28, 'end'), ('A', h + 0.1, -0.3, 'start'), ('B', h + 0.1, R + 0.1, 'start'), ('C', -0.1, r + 0.2, 'end'),
                        ('OA = h', 1.5, -0.38, 'middle'), ('AB = R', h + 0.1, R / 2, 'start'), ('OC = r', 0.1, r / 2 + 0.05, 'start')]:
        b.append(halo(A.fx(x), A.fy(y), s, 13.5, NAVY if '=' in s else INK, an, 'bold'))
    return svg(W, H, ''.join(b))


reg('b13-q13', _trap)


def _tri():
    A = Ax(-0.6, 4.4, -2.4, 2.4, 30, W - 26, H - 34, 24)
    a, al = 3.2, math.radians(30)
    hgt = a * math.tan(al)
    b = []
    prof = lambda x: x * math.tan(al)
    up = A.curve(prof, 0, a, 40); lo = A.curve(lambda x: -prof(x), 0, a, 40)
    b.append('<polygon points="%s" fill="#e4eef8"/>' % ' '.join('%.1f,%.1f' % q for q in up + list(reversed(lo))))
    b.append('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in [A.pt(0, 0), A.pt(a, 0), A.pt(a, hgt)]), F_ORANGE))
    b.append(A.axes(o=False))
    b.append(PL(up, stroke=BLUE, w=3)); b.append(PL(lo, stroke=BLUE, w=2, dash='6 4'))
    ry = A.fy(0) - A.fy(hgt)
    b.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="2"/>' % (A.fx(a), A.fy(0), ry * 0.26, ry, BLUE))
    b.append(L(A.fx(a), A.fy(0), A.fx(a), A.fy(hgt), stroke=INK, w=2))
    b.append(right_angle(A.fx(a), A.fy(0), A.fx(a) - 1, A.fy(0), A.fx(a), A.fy(0) - 1, s=11))
    b.append(angle_arc(A.fx(0), A.fy(0), A.fx(1), A.fy(0), A.fx(1), A.fy(math.tan(al)), r=38, color=RED, w=2))
    for s, x, y, an in [('O', -0.12, -0.3, 'end'), ('A', a + 0.1, -0.32, 'start'), ('B', a + 0.1, hgt + 0.1, 'start'),
                        ('OA = a', a / 2, -0.38, 'middle'), ('α', 0.95, 0.17, 'start')]:
        b.append(halo(A.fx(x), A.fy(y), s, 14, '#a02a2c' if s == 'α' else (NAVY if '=' in s else INK), an, 'bold'))
    return svg(W, H, ''.join(b))


reg('b13-q23', _tri)
reg('b13-q17', lambda: area_fig((-0.5, 5.4), (-1.2, 7), [(lambda x: 5 * x - x * x, 0, 5, BLUE, None), (lambda x: x, 0, 5, GREEN, None)],
                                (lambda x: 5 * x - x * x, lambda x: x, 0, 4), [(0, '0'), (4, '4')],
                                [('y = 5x − x²', 4.9, 2.2, 'end', NAVY), ('y = x', 5.3, 5.0, 'end', '#2f6b2a')]))
reg('b13-q18', lambda: area_fig((-1.6, 1.6), (-1.35, 3.1), [(math.exp, -1.45, 1.1, BLUE, None), (lambda x: x * x - 1, -1.45, 1.45, GREEN, None)],
                                (math.exp, lambda x: x * x - 1, -1, 1), [(-1, '−1'), (1, '1')],
                                [('y = eˣ', 0.9, 2.95, 'end', NAVY), ('y = x² − 1', 1.5, 1.15, 'end', '#2f6b2a')]))
reg('b13-q19', lambda: area_fig((-0.2, 1.4), (-0.2, 1.35), [(sq, 0, 1.2, BLUE, None), (lambda x: x * x, 0, 1.15, GREEN, None)],
                                (sq, lambda x: x * x, 0, 1), [(0, '0'), (1, '1')],
                                [('y = √x', 0.5, 0.95, 'end', NAVY), ('y = x²', 1.38, 0.9, 'end', '#2f6b2a')]))
reg('b13-q20', lambda: area_fig((-3.4, 3.4), (-1.2, 10.4), [(lambda x: 9 - x * x, -3, 3, BLUE, None), (lambda x: 2 * x * x, -2.25, 2.25, GREEN, None)],
                                (lambda x: 9 - x * x, lambda x: 2 * x * x, -math.sqrt(3), math.sqrt(3)),
                                [(-math.sqrt(3), '−√3'), (math.sqrt(3), '√3')],
                                [('y = 9 − x²', 3.35, 1.4, 'end', NAVY), ('y = 2x²', -1.3, 9.0, 'end', '#2f6b2a')]))
reg('b13-q21', lambda: rev_fig((-0.3, 2.5), (-1.4, 1.4), lambda x: 2 * x - x * x, 0, 2, [(0, '0'), (2, '2')],
                               [('y = 2x − x²', 1.0, 1.2, 'middle', NAVY)]))


def _binh():
    A = Ax(-3, 33, -15, 15, 34, W - 22, H - 34, 30)
    f = lambda x: x * x / 175 + 3 * x / 35 + 5
    b = [T(W / 2, 20, 'Mặt cắt dọc theo trục Ox', size=14, weight='bold')]
    inner = A.curve(f, 0, 30, 100); outer = A.curve(lambda x: f(x) + 1, 0, 30, 100)
    b.append('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in outer + list(reversed(inner))), '#f0c88f'))
    inl = A.curve(lambda x: -f(x), 0, 30, 100); outl = A.curve(lambda x: -f(x) - 1, 0, 30, 100)
    b.append('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in outl + list(reversed(inl))), '#f0c88f'))
    _axes_ticks(A, [(0, '0'), (30, '30')], b)
    b.append(PL(inner, stroke=BLUE, w=2.6)); b.append(PL(outer, stroke=ORANGE, w=2.6))
    b.append(PL(inl, stroke=BLUE, w=2.6)); b.append(PL(outl, stroke=ORANGE, w=2.6))
    b.append(halo(A.fx(16), A.fy(f(16)) + 22, 'mặt trong: y = f(x)', 12.5, NAVY, 'middle', 'bold'))
    b.append(halo(A.fx(12), A.fy(f(12) + 1) - 14, 'mặt ngoài: f(x) + 1', 12.5, '#b3601a', 'middle', 'bold'))
    b.append(T(W / 2, H - 6, 'Thành bình dày 1 cm (phần màu cam); x tính bằng cm', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


reg('b13-q26', _binh)

# ---------- ôn tập chương IV ----------
reg('c4-q05', lambda: area_fig((-0.5, 3.6), (-1.6, 5), [(lambda x: x * x - 2 * x, 0, 3.3, BLUE, None), (lambda x: -x * x + 4 * x, 0, 3.3, GREEN, None)],
                               (lambda x: -x * x + 4 * x, lambda x: x * x - 2 * x, 0, 3), [(0, '0'), (3, '3')],
                               [('y = −x² + 4x', 3.55, 1.2, 'end', '#2f6b2a'), ('y = x² − 2x', 3.55, 3.7, 'end', NAVY)]))
reg('c4-q18', lambda: area_fig((-0.3, 1.5), (-0.3, 3.1), [(math.exp, 0, 1.1, BLUE, None), (lambda x: x, 0, 1.3, GREEN, None)],
                               (math.exp, lambda x: x, 0, 1), [(0, '0'), (1, '1')],
                               [('y = eˣ', 1.1, 2.9, 'end', NAVY), ('y = x', 1.48, 1.0, 'end', '#2f6b2a')]))
reg('c4-q07', lambda: rev_fig((-1.5, 1.7), (-1.35, 1.5), lambda x: math.sqrt(max(0, 1 - x * x)), -1, 1, [(-1, '−1'), (1, '1')],
                              [('y = √(1 − x²)', 0.0, 1.25, 'middle', NAVY)]))
reg('c4-q19', lambda: rev_fig((-1.5, 1.7), (-1.35, 1.5), lambda x: 1 - x * x, -1, 1, [(-1, '−1'), (1, '1')],
                              [('y = 1 − x²', 0.0, 1.25, 'middle', NAVY)]))
reg('c4-q20', lambda: rev_fig((-0.4, 5.6), (-5.5, 5.5), lambda x: math.sqrt(25 - x * x), 2, 4, [(2, '2'), (4, '4')],
                              [('y = √(25 − x²)', 3.0, 5.2, 'middle', NAVY)], extra=(lambda x: math.sqrt(max(0, 25 - x * x)), 0, 5)))


TARGET = {
    'b13': ('toan12', 'content/toan12/*/*/bai-13/*.json'),
    'c4': ('toan12', 'content/toan12/tap2/chuong-4/on-tap/*.json'),
}


def main():
    n = 0
    figdir = os.path.join(ROOT, 'content', 'toan12', 'figures'); os.makedirs(figdir, exist_ok=True)
    byfile = {}
    for key, fn in SPEC.items():
        grp, qid = key.split('-')
        nm = 'bt12-%s-%s.svg' % (grp, qid)
        open(os.path.join(figdir, nm), 'w', encoding='utf8').write(fn())
        byfile.setdefault(grp, []).append((qid, nm)); n += 1
    if '--attach' in sys.argv:
        for grp, items in byfile.items():
            path = glob.glob(os.path.join(ROOT, TARGET[grp][1]))
            assert len(path) == 1, path
            d = json.load(open(path[0], encoding='utf8'))
            ids = {i['id']: i for i in d['items']}
            for qid, nm in items:
                ids[qid]['figure'] = 'figures/' + nm
            with open(path[0], 'w', encoding='utf8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2); f.write('\n')
    print('toan12 bt: %d hình' % n)


if __name__ == '__main__':
    main()
