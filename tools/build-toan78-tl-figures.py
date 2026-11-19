# Toán 8 bài 25 (cân thăng bằng), Toán 7 bài 22, 23 (tỉ lệ thuận/nghịch): bảng và đồ thị minh hoạ.
import sys, os, json, glob, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *


def _load(name, fn):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(__file__), fn))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


tn = _load('tn789', 'build-toan789-figures.py')
Ax, halo, NAVY = tn.Ax, tn.halo, tn.NAVY


def scale(cx, y, left, right):
    """Cân thăng bằng tại tâm cx, trục ngang ở độ cao y. left/right: [(chữ, rộng, màu)] xếp cạnh nhau trên đĩa."""
    b = [POLY([(cx, y), (cx - 26, y + 98), (cx + 26, y + 98)], fill='#cdd5dd', stroke=INK, sw=2),
         L(cx - 105, y, cx + 105, y, w=5), C(cx, y, 6, fill=INK)]
    for sx, items in ((-105, left), (105, right)):
        px = cx + sx
        b.append(L(px, y, px - 50, y + 64, w=1.4)); b.append(L(px, y, px + 50, y + 64, w=1.4))
        b.append(PATH('M%d,%d Q%d,%d %d,%d' % (px - 52, y + 64, px, y + 98, px + 52, y + 64), fill='#e8edf2', w=2.4))
        tot = sum(w for _, w, _ in items) + 4 * (len(items) - 1)
        x = px - tot / 2
        for s, w, col in items:
            b.append(R(x, y + 64 - 34, w, 34, fill=col, stroke=INK, sw=1.8, rx=4))
            b.append(T(x + w / 2, y + 64 - 11, s, size=17, weight='bold'))
            x += w + 4
    return ''.join(b)


def t8_can():
    W, H = 720, 345
    b = [title(W, 'Giải phương trình bằng cân thăng bằng')]
    XO, GR = '#f7c98b', '#cdd5dd'
    b.append(T(170, 62, '3x − 12 = 0  ⇒  chuyển vế:  3x = 12', size=14.5, weight='bold', fill=NAVY))
    b.append(scale(170, 130, [('x', 30, XO)] * 3, [('12', 70, GR)]))
    b.append(L(334, 150, 386, 150, arrow=True)); b.append(T(360, 130, 'chia hai vế', size=12.5)); b.append(T(360, 176, 'cho 3', size=12.5))
    b.append(T(550, 62, 'x = 12 : 3 = 4', size=14.5, weight='bold', fill=NAVY))
    b.append(scale(550, 130, [('x', 30, XO)], [('4', 30, GR)]))
    b.append(T(W / 2, 276, 'Chia (hoặc nhân) cả hai vế với cùng một số khác 0: cân vẫn thăng bằng.', size=13, fill='#5b6773'))
    b.append(T(W / 2, 302, 'Tổng quát: ax + b = 0 (a ≠ 0) ⇔ ax = −b ⇔ x = −b/a', size=14, weight='bold'))
    b.append(T(W / 2, 328, 'Hình minh hoạ cho ví dụ 3x − 12 = 0; x là ẩn, số 12 là tổng khối lượng ở đĩa phải.', size=11.5, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def table(x, y, head, rows, cw=64, rh=34, hw=70):
    """Bảng ngang: head là nhãn cột đầu của từng hàng; rows: [(nhãn, [giá trị])]."""
    n = len(rows[0][1])
    b = []
    for r, (lab, vals) in enumerate(rows):
        yy = y + r * rh
        b.append(R(x, yy, hw, rh, fill='#e8f1fa', stroke=INK, sw=1.6)); b.append(T(x + hw / 2, yy + 23, lab, size=15, weight='bold'))
        for i, v in enumerate(vals):
            b.append(R(x + hw + i * cw, yy, cw, rh, fill='white', stroke=INK, sw=1.6)); b.append(T(x + hw + i * cw + cw / 2, yy + 23, v, size=15))
    return ''.join(b)


def t7_thuan():
    W, H = 720, 330
    b = [title(W, 'Đại lượng tỉ lệ thuận: y = k · x')]
    b.append(T(190, 58, 'Ví dụ: y = 4x', size=14, weight='bold', fill=NAVY))
    b.append(table(30, 76, None, [('x', ['3', '5']), ('y', ['12', '20'])], cw=80, rh=36, hw=60))
    b.append(T(190, 176, 'y/x = 12/3 = 20/5 = 4 = k', size=14.5, weight='bold'))
    b.append(T(190, 204, 'Tỉ số y₁/y₂ = x₁/x₂:  12/20 = 3/5', size=14))
    b.append(T(190, 240, 'x tăng bao nhiêu lần thì y', size=13, fill='#5b6773')); b.append(T(190, 258, 'tăng bấy nhiêu lần', size=13, fill='#5b6773'))
    A = Ax(0, 6.2, 0, 26, 420, 690, 270, 64)
    b.append(T(555, 58, 'Đồ thị y = 4x (đi qua gốc O)', size=14, weight='bold', fill=NAVY))
    b.append(A.axes())
    b.append(PL([A.pt(0, 0), A.pt(6, 24)], stroke=BLUE, w=3))
    for x, y in [(3, 12), (5, 20)]:
        px, py = A.pt(x, y)
        b.append(L(px, py, px, A.fy(0), stroke=GREY, w=1.3, dash='4 3')); b.append(L(px, py, A.fx(0), py, stroke=GREY, w=1.3, dash='4 3'))
        b.append(dot(px, py, 5, fill=RED)); b.append(T(px, A.fy(0) + 17, str(x), size=13)); b.append(T(A.fx(0) - 6, py + 5, str(y), size=13, anchor='end'))
    b.append(T(555, H - 28, 'Hai điểm (3; 12) và (5; 20)', size=12, fill='#5b6773')); b.append(T(555, H - 12, 'cùng nằm trên một đường thẳng qua O', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


def t7_nghich():
    W, H = 720, 330
    b = [title(W, 'Đại lượng tỉ lệ nghịch: x · y = a')]
    b.append(T(190, 58, 'Ví dụ: x · y = 24', size=14, weight='bold', fill=NAVY))
    b.append(table(30, 76, None, [('x', ['4', '8']), ('y', ['6', '3'])], cw=80, rh=36, hw=60))
    b.append(T(190, 176, 'x · y:  4 · 6 = 8 · 3 = 24 = a', size=14.5, weight='bold'))
    b.append(T(190, 214, 'x tăng 2 lần (4 → 8)', size=13.5)); b.append(T(190, 236, 'thì y giảm 2 lần (6 → 3)', size=13.5))
    A = Ax(0, 10.4, 0, 11, 420, 690, 270, 64)
    b.append(T(555, 58, 'Đồ thị y = 24/x (x > 0)', size=14, weight='bold', fill=NAVY))
    b.append(A.axes())
    b.append(PL([A.pt(x, 24 / x) for x in [2.3 + 0.1 * i for i in range(82)]], stroke=BLUE, w=3))
    for x, y in [(4, 6), (8, 3)]:
        px, py = A.pt(x, y)
        b.append(L(px, py, px, A.fy(0), stroke=GREY, w=1.3, dash='4 3')); b.append(L(px, py, A.fx(0), py, stroke=GREY, w=1.3, dash='4 3'))
        b.append(dot(px, py, 5, fill=RED)); b.append(T(px, A.fy(0) + 17, str(x), size=13)); b.append(T(A.fx(0) - 6, py + 5, str(y), size=13, anchor='end'))
    b.append(T(555, H - 12, 'Đồ thị là đường cong; x tăng thì y giảm', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


FIGS = [('toan8', 25, 'tn-toan8-b25-can.svg', t8_can, 'Giải phương trình 3x − 12 = 0 bằng cân thăng bằng'),
        ('toan7', 22, 'tn-toan7-b22-ti-le-thuan.svg', t7_thuan, 'Đại lượng tỉ lệ thuận: bảng và đồ thị'),
        ('toan7', 23, 'tn-toan7-b23-ti-le-nghich.svg', t7_nghich, 'Đại lượng tỉ lệ nghịch: bảng và đồ thị')]

if __name__ == '__main__':
    for subj, bai, nm, fn, cap in FIGS:
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf8').write(fn())
        if '--attach' in sys.argv:
            p = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%d' % bai, '*.json'))[0]
            data = json.load(open(p, encoding='utf8'))
            attach(subj, os.path.relpath(p, os.path.join(ROOT, 'content', subj)), len(data['theory']) - 1, nm, cap)
    print('ok')
