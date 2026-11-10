# Toán 8 bài 7, 8: hằng đẳng thức lập phương bằng khối hộp (hình chiếu xiên minh hoạ, không đo tỉ lệ thật).
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

K = 0.42
C_A3, C_A2B, C_AB2, C_B3 = '#9ec1e6', '#f7c98b', '#b5d9a0', '#d3b6df'
BYN = [C_A3, C_A2B, C_AB2, C_B3]


def mix(hexc, t, to=(255, 255, 255)):
    c = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(int(c[i] + (to[i] - c[i]) * t) for i in range(3))


def P(X0, Y0, x, y, z):
    return (X0 + x + K * z, Y0 - y - K * z)


def face(X0, Y0, pts3, col):
    return POLY([P(X0, Y0, *p) for p in pts3], fill=col, stroke=INK, sw=1.4)


def box(X0, Y0, dx, dy, dz, col):
    return (face(X0, Y0, [(dx, 0, 0), (dx, 0, dz), (dx, dy, dz), (dx, dy, 0)], mix(col, 0.28, (0, 0, 0))) +
            face(X0, Y0, [(0, dy, 0), (dx, dy, 0), (dx, dy, dz), (0, dy, dz)], mix(col, 0.35)) +
            face(X0, Y0, [(0, 0, 0), (dx, 0, 0), (dx, dy, 0), (0, dy, 0)], col))


def b7():
    W, H = 720, 370
    A, B = 74, 38
    S = A + B
    seg = [(0, A), (A, S)]
    b = [title(W, 'Lập phương của một tổng')]
    X0, Y0 = 64, 270
    # mặt phải, mặt trên, mặt trước: tô theo khối nằm sát mặt
    for j in range(2):
        for k in range(2):
            n = 1 + j + k
            (y0, y1), (z0, z1) = seg[j], seg[k]
            b.append(face(X0, Y0, [(S, y0, z0), (S, y0, z1), (S, y1, z1), (S, y1, z0)], mix(BYN[n], 0.28, (0, 0, 0))))
    for i in range(2):
        for k in range(2):
            n = i + 1 + k
            (x0, x1), (z0, z1) = seg[i], seg[k]
            b.append(face(X0, Y0, [(x0, S, z0), (x1, S, z0), (x1, S, z1), (x0, S, z1)], mix(BYN[n], 0.35)))
    for i in range(2):
        for j in range(2):
            n = i + j
            (x0, x1), (y0, y1) = seg[i], seg[j]
            b.append(face(X0, Y0, [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], BYN[n]))
    b.append(T(X0 + A / 2, Y0 + 20, 'A', size=14)); b.append(T(X0 + A + B / 2, Y0 + 20, 'B', size=14))
    b.append(T(X0 - 12, Y0 - A / 2 + 5, 'A', size=14)); b.append(T(X0 - 12, Y0 - A - B / 2 + 5, 'B', size=14))
    b.append(T(X0 + S / 2 + 20, Y0 + 46, 'Cắt thành 8 khối nhỏ;', size=12, fill='#5b6773'))
    b.append(T(X0 + S / 2 + 20, Y0 + 62, '3 mặt nhìn thấy được tô theo khối', size=12, fill='#5b6773'))
    # tám khối tách rời
    pieces = [(A, A, A, 0, '1 khối A³'), (A, A, B, 1, '3 khối A²B'), (A, B, B, 2, '3 khối AB²'), (B, B, B, 3, '1 khối B³')]
    px = [330, 530]
    pos = [(350, 168), (560, 168), (350, 318), (560, 318)]
    for (dx, dy, dz, n, lab), (x, y) in zip(pieces, pos):
        b.append(box(x, y, dx, dy, dz, BYN[n]))
        b.append(T(x + dx / 2 + 10, y + 22, lab, size=14, weight='bold'))
    b.append(RT_(W / 2, 54, '(A + B)³ = A³ + 3A²B + 3AB² + B³'))
    return svg(W, H, ''.join(b))


def RT_(x, y, s):
    return T(x, y, s, size=15, weight='bold', fill='#1a56a0')


def b8():
    W, H = 720, 350
    A, B = 104, 54
    Cc = A - B
    b = [title(W, 'Hiệu hai lập phương: A³ − B³ = (A − B)(A² + AB + B²)')]
    X0, Y0 = 100, 300
    b.append(T(X0 + 70, 62, 'Khối A³ khuyết một góc B³', size=13.5, weight='bold'))
    # P1 đáy
    b.append(box(X0, Y0, A, Cc, A, C_A3))
    # P3 phía sau-trái, P2 phía trước
    # P2: x[0,A], y[Cc,A], z[B,A] (dải phía sau); P3: x[0,Cc], y[Cc,A], z[0,B] (phía trước-trái); góc trước-phải-trên bị khuyết
    x2, y2 = P(X0, Y0, 0, Cc, B)
    b.append(box(x2, y2, A, B, Cc, C_A2B))
    x3, y3 = P(X0, Y0, 0, Cc, 0)
    b.append(box(x3, y3, Cc, B, B, C_B3))
    b.append(T(X0 + A / 2, Y0 + 22, 'A', size=14)); b.append(T(X0 - 12, Y0 - Cc / 2 + 5, 'A − B', size=13, anchor='end'))
    # tách rời
    b.append(T(530, 62, 'Ba khối cùng dày A − B', size=13.5, weight='bold'))
    parts = [(A, Cc, A, C_A3, 'A²(A − B)', 380, 170), (A, B, Cc, C_A2B, 'AB(A − B)', 380, 300), (Cc, B, B, C_B3, 'B²(A − B)', 590, 300)]
    # chiều (dx, dy, dz): mỗi khối có một cạnh bằng A − B
    for dx, dy, dz, col, lab, x, y in parts:
        b.append(box(x, y, dx, dy, dz, col))
        b.append(T(x + dx / 2 + 12, y + 24, lab, size=14, weight='bold'))
    b.append(T(W / 2, H - 8, 'A² + AB + B² là diện tích ba đáy; chiều dày chung là A − B.', size=12, fill='#5b6773'))
    return svg(W, H, ''.join(b))


C_A2B_ = C_A2B
FIGS = [('toan8', 7, 'tn-toan8-b7-lap-phuong.svg', b7, 'Lập phương của một tổng bằng khối hộp'),
        ('toan8', 8, 'tn-toan8-b8-hieu-lap-phuong.svg', b8, 'Hiệu hai lập phương bằng khối hộp')]

if __name__ == '__main__':
    for subj, bai, nm, fn, cap in FIGS:
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf8').write(fn())
        if '--attach' in sys.argv:
            p = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%d' % bai, '*.json'))[0]
            data = json.load(open(p, encoding='utf8'))
            attach(subj, os.path.relpath(p, os.path.join(ROOT, 'content', subj)), len(data['theory']) - 1, nm, cap)
    print('ok')
