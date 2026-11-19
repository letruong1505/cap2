# Hình cho bài tập Toán 6 (đoạn thẳng, đồng hồ, đường thẳng cắt nhau, biểu đồ, bảng, chữ cái).
import sys, os, math, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

NAVY = '#1a56a0'
W = 360


def lab(x, y, s, size=13, col=NAVY, w='bold', anchor='middle'):
    return T(x, y, s, size=size, weight=w, fill=col, anchor=anchor)


def seg(points, braces=(), ticks=(), ray=False, H=170):
    """points: [(tên, giá trị)]; braces: [(tên1, tên2, chữ, 'up'|'down')]; ticks: [(tên1, tên2, n)] đánh dấu đoạn bằng nhau."""
    vals = [v for _, v in points]
    lo, hi = min(vals), max(vals)
    x0, x1, y = 50, 310, 90
    f = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    pos = {n: f(v) for n, v in points}
    b = [L(x0 - 20, y, x1 + 24, y, w=2.2, arrow=ray)]
    for n, v in points:
        b.append(C(f(v), y, 4.5, fill=INK, stroke=INK, w=1)); b.append(T(f(v), y + 24, n, size=15, weight='bold'))
    for a, c, n in ticks:
        mx = (pos[a] + pos[c]) / 2
        for k in range(n):
            o = (k - (n - 1) / 2) * 5
            b.append(L(mx + o, y - 8, mx + o, y + 8, w=2, stroke=RED))
    for a, c, t, d in braces:
        xa, xc = pos[a], pos[c]
        if d == 'up':
            yy = y - 24 - 0
            b.append(PL([(xa, yy + 8), (xa, yy), (xc, yy), (xc, yy + 8)], stroke=GREY, w=1.6)); b.append(lab((xa + xc) / 2, yy - 6, t))
        else:
            yy = y + 44
            b.append(PL([(xa, yy - 8), (xa, yy), (xc, yy), (xc, yy - 8)], stroke=GREY, w=1.6)); b.append(lab((xa + xc) / 2, yy + 17, t))
    return svg(W, H, ''.join(b))


def clock(h):
    cx, cy, r = 180, 95, 78
    b = [C(cx, cy, r, fill='#f6f9fc', stroke=INK, w=3)]
    for k in range(12):
        a = math.radians(k * 30 - 90)
        b.append(L(cx + (r - 10) * math.cos(a), cy + (r - 10) * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a), w=2))
        b.append(T(cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a) + 5, str(12 if k == 0 else k), size=13, weight='bold'))
    ah = math.radians(h * 30 - 90)
    b.append(L(cx, cy, cx + 36 * math.cos(ah), cy + 36 * math.sin(ah), w=5, stroke=INK))
    b.append(L(cx, cy, cx, cy - 48, w=3, stroke=RED))
    b.append(C(cx, cy, 4, fill=INK, stroke=INK, w=1))
    b.append(lab(cx, 192, '%d giờ đúng' % h, 14))
    return svg(W, 206, ''.join(b))


def lines(kind):
    b = []
    if kind == 'cross':
        b += [L(60, 120, 300, 40, w=2.4), L(60, 40, 300, 120, w=2.4), C(180, 80, 4.5, fill=INK, stroke=INK, w=1), T(196, 100, 'O', size=16, weight='bold')]
    elif kind == 'concur':
        b += [L(50, 80, 310, 80, w=2.4), L(80, 130, 280, 30, w=2.4), L(80, 30, 280, 130, w=2.4), C(180, 80, 4.5, fill=INK, stroke=INK, w=1), T(192, 100, 'O', size=16, weight='bold')]
    elif kind == 'tri':
        P = [(120, 55), (240, 55), (180, 130)]
        for p, q in ((P[0], P[1]), (P[1], P[2]), (P[2], P[0])):
            dx, dy = q[0] - p[0], q[1] - p[1]
            b.append(L(p[0] - dx * 0.3, p[1] - dy * 0.3, q[0] + dx * 0.3, q[1] + dy * 0.3, w=2.4))
        for p in P: b.append(C(p[0], p[1], 4.5, fill=INK, stroke=INK, w=1))
    return svg(W, 160, ''.join(b))


def bars(data, ymax, step, unit, ttl):
    x0, y0, w, h = 70, 200, 250, 150
    b = [lab(180, 22, ttl, 13, INK)]
    b.append(L(x0, y0, x0, y0 - h - 6, w=2, arrow=True)); b.append(L(x0, y0, x0 + w + 6, y0, w=2))
    for v in range(0, ymax + 1, step):
        yy = y0 - v / ymax * h
        b.append(L(x0 - 4, yy, x0 + w, yy, w=0.8 if v else 2, stroke='#d4d9df' if v else INK)); b.append(T(x0 - 8, yy + 4, str(v), size=11, anchor='end'))
    n = len(data); bw = w / n * 0.5
    for i, (k, v) in enumerate(data):
        cx = x0 + w / n * (i + 0.5)
        b.append(R(cx - bw / 2, y0 - v / ymax * h, bw, v / ymax * h, fill='#8fc1ee', stroke=INK, sw=1.6)); b.append(T(cx, y0 - v / ymax * h - 5, str(v), size=12, weight='bold'))
        b.append(T(cx, y0 + 18, k, size=12.5, weight='bold'))
    b.append(T(x0 - 8, y0 - h - 12, unit, size=11, anchor='end', fill=GREY))
    return svg(W, 232, ''.join(b))


def dbars(cats, series, ymax, step, ttl):
    x0, y0, w, h = 60, 200, 250, 140
    b = [lab(180, 22, ttl, 13, INK)]
    b.append(L(x0, y0, x0, y0 - h - 6, w=2, arrow=True)); b.append(L(x0, y0, x0 + w + 6, y0, w=2))
    for v in range(0, ymax + 1, step):
        yy = y0 - v / ymax * h
        b.append(L(x0 - 4, yy, x0 + w, yy, w=0.8 if v else 2, stroke='#d4d9df' if v else INK)); b.append(T(x0 - 8, yy + 4, str(v), size=11, anchor='end'))
    cols = ['#8fc1ee', '#f2a33a']
    n = len(cats)
    for i, c in enumerate(cats):
        gx = x0 + w / n * (i + 0.5)
        for j, (nm, vals) in enumerate(series):
            v = vals[i]; bw = 34
            xx = gx + (j - 1) * bw
            b.append(R(xx, y0 - v / ymax * h, bw, v / ymax * h, fill=cols[j], stroke=INK, sw=1.5)); b.append(T(xx + bw / 2, y0 - v / ymax * h - 5, str(v), size=12, weight='bold'))
        b.append(T(gx, y0 + 18, c, size=12.5, weight='bold'))
    for j, (nm, _) in enumerate(series):
        b.append(R(250 + j * 56, 34, 12, 12, fill=cols[j], stroke=INK, sw=1)); b.append(T(266 + j * 56, 45, nm, size=12, anchor='start'))
    return svg(W, 232, ''.join(b))


def table(head, rows, ttl):
    b = [lab(180, 22, ttl, 13, INK)]
    n = len(head); cw = 300 / n; x0 = 30; y0 = 40
    for j, hh in enumerate(head):
        b.append(R(x0 + j * cw, y0, cw, 34, fill='#e8f1fa', stroke=INK, sw=1.5)); b.append(T(x0 + j * cw + cw / 2, y0 + 23, hh, size=13, weight='bold'))
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            b.append(R(x0 + j * cw, y0 + 34 + i * 34, cw, 34, fill='white', stroke=INK, sw=1.5)); b.append(T(x0 + j * cw + cw / 2, y0 + 34 + i * 34 + 23, str(v), size=14))
    return svg(W, int(y0 + 34 * (len(rows) + 1) + 20), ''.join(b))


def letters(ls):
    b = [lab(180, 24, 'Các chữ cái in hoa', 13, INK)]
    n = len(ls); cw = 300 / n
    for i, c in enumerate(ls):
        x = 30 + i * cw
        b.append(R(x + 4, 44, cw - 8, 90, fill='#f6f9fc', stroke=GREY, sw=1.2, rx=8)); b.append(T(x + cw / 2, 108, c, size=54, weight='bold'))
    return svg(W, 150, ''.join(b))


SPEC = [
    ('toan6', 32, 'q06', lambda: lines('cross')), ('toan6', 32, 'q07', lambda: lines('tri')),
    ('toan6', 33, 'q08', lambda: lines('cross')), ('toan6', 33, 'q09', lambda: lines('concur')),
    ('toan6', 36, 'q05', lambda: lines('cross')), ('toan6', 36, 'q06', lambda: lines('cross')),
    ('toan6', 33, 'q07', lambda: seg([('A', 0), ('B', 4), ('C', 9)])),
    ('toan6', 34, 'q05', lambda: seg([('O', 0), ('A', 3), ('B', 8)], [('O', 'A', 'OA = 3 cm', 'up'), ('O', 'B', 'OB = 8 cm', 'down')], ray=True)),
    ('toan6', 34, 'q06', lambda: seg([('A', 0), ('B', 2), ('C', 5), ('D', 9)], [('A', 'B', '2', 'up'), ('B', 'C', '3', 'up'), ('C', 'D', '4', 'up'), ('A', 'D', 'AD = ?', 'down')])),
    ('toan6', 35, 'q03', lambda: seg([('A', 0), ('M', 4.5), ('B', 9)], [('A', 'B', 'AB = 9 cm', 'up'), ('M', 'B', 'MB = ?', 'down')], [('A', 'M', 1), ('M', 'B', 1)])),
    ('toan6', 35, 'q04', lambda: seg([('E', 0), ('I', 6), ('F', 12)], [('E', 'I', 'EI = 6 cm', 'up'), ('E', 'F', 'EF = ?', 'down')], [('E', 'I', 1), ('I', 'F', 1)])),
    ('toan6', 35, 'q05', lambda: seg([('O', 0), ('A', 4), ('M', 7), ('B', 10)], [('O', 'A', 'OA = 4 cm', 'up'), ('O', 'B', 'OB = 10 cm', 'down')], [('A', 'M', 1), ('M', 'B', 1)], ray=True)),
    ('toan6', 35, 'q06', lambda: seg([('A', 0), ('N', 4), ('M', 8), ('B', 16)], [('A', 'B', 'AB = 16 cm', 'up'), ('A', 'N', 'AN = ?', 'down')], [('A', 'N', 1), ('N', 'M', 1), ('M', 'B', 2)])),
    ('toan6', 35, 'q09', lambda: seg([('A', 0), ('M', 10), ('B', 20)], [('A', 'M', 'MA = 2x', 'up'), ('A', 'B', 'AB = 20', 'down')], [('A', 'M', 1), ('M', 'B', 1)])),
    ('toan6', 36, 'q08', lambda: clock(3)), ('toan6', 37, 'q04', lambda: clock(4)), ('toan6', 37, 'q05', lambda: clock(9)),
    ('toan6', 37, 'q06', lambda: clock(1)), ('toan6', 37, 'q09', lambda: clock(5)),
    ('toan6', 39, 'q05', lambda: table(['Ngày', 'Số chiếc bán'], [['Thứ Hai', 25], ['Thứ Ba', 30], ['Thứ Tư', 45]], 'Số chiếc bán theo ngày')),
    ('toan6', 39, 'q06', lambda: table(['Ngày', 'Số chiếc bán'], [['Thứ Hai', 25], ['Thứ Ba', 30], ['Thứ Tư', 45]], 'Số chiếc bán theo ngày')),
    ('toan6', 39, 'q09', lambda: table(['Điểm', 'Số bạn'], [[5, 2], [7, 5], [9, 3]], 'Bảng điểm')),
    ('toan6', 40, 'q03', lambda: bars([('Tháng 1', 20), ('Tháng 2', 15), ('Tháng 3', 10)], 25, 5, 'ngày', 'Số ngày mưa theo tháng')),
    ('toan6', 40, 'q04', lambda: bars([('Tháng 1', 20), ('Tháng 2', 15), ('Tháng 3', 10)], 25, 5, 'ngày', 'Số ngày mưa theo tháng')),
    ('toan6', 40, 'q06', lambda: bars([('Lớp A', 45), ('Lớp B', 60), ('Lớp C', 55)], 70, 10, 'quyển', 'Số sách của các lớp')),
    ('toan6', 41, 'q03', lambda: dbars(['Toán', 'Văn'], [('Nam', [8, 7]), ('Nữ', [9, 8])], 10, 2, 'Điểm trung bình theo môn')),
    ('toan6', 21, 'q07', lambda: letters(list('ABHNZ'))),
    ('toan6', 22, 'q05', lambda: letters(list('HNSZA'))),
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
    print('bt6: %d hình' % len(SPEC))
