#!/usr/bin/env python3
# Hình minh họa lý thuyết Toán 6 (sơ đồ vẽ chính xác bằng toạ độ). Chạy: python3 tools/build-toan6-figures.py
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

S = 'toan6'
FILL = '#eaf1f8'
AX = RED


def shape(pts, fill=FILL):
    return POLY(pts, fill=fill, stroke=INK, sw=2.2)


def numline(x0, x1, y, vals, labels=None, step=None, arrow_left=False):
    out = [L(x0, y, x1, y, w=2, arrow=True)]
    if arrow_left:
        out.append(L(x1 - 0, y, x0, y, w=2, arrow=True))
    return ''.join(out)


# ---------------------------------------------------------------- Chương I
def fig_tap_hop():
    b = [title(720, 'Tập hợp A = {0; 1; 2; 3}')]
    b.append('<ellipse cx="250" cy="130" rx="130" ry="80" fill="#eaf1f8" stroke="%s" stroke-width="2.5"/>' % INK)
    b.append(T(150, 78, 'A', size=20, weight='bold'))
    for (x, y, s) in ((200, 110, '0'), (270, 100, '1'), (215, 155, '2'), (290, 150, '3')):
        b.append(dot(x - 14, y - 4, 3.5))
        b.append(T(x, y, s, size=18))
    b.append(dot(480, 130, 3.5))
    b.append(T(500, 135, '5', size=18, anchor='start'))
    b.append(TL(560, 100, ['2 ∈ A', '(2 thuộc A)'], size=15, anchor='start', lh=20))
    b.append(TL(560, 170, ['5 ∉ A', '(5 không thuộc A)'], size=15, anchor='start', lh=20))
    return svg(720, 240, ''.join(b))


def fig_tia_so():
    b = [title(720, 'Biểu diễn số tự nhiên trên tia số')]
    y = 110
    b.append(L(40, y, 690, y, w=2.5, arrow=True))
    for k in range(0, 10):
        x = 70 + k * 62
        b.append(L(x, y - 7, x, y + 7, w=2))
        b.append(T(x, y + 28, str(k), size=16))
    b.append(dot(70 + 2 * 62, y, 5, RED) + dot(70 + 6 * 62, y, 5, RED))
    b.append(T(70 + 2 * 62, y - 20, 'a = 2', size=14, fill=RED, weight='bold'))
    b.append(T(70 + 6 * 62, y - 20, 'b = 6', size=14, fill=RED, weight='bold'))
    b.append(L(70 + 6 * 62 - 6, 60, 70 + 2 * 62 + 6, 60, w=1.5, arrow=True, stroke=GREY))
    b.append(T(70 + 4 * 62, 50, 'Điểm biểu diễn số nhỏ hơn nằm bên trái: 2 < 6', size=13))
    b.append(T(360, 190, 'Số 0 là số tự nhiên nhỏ nhất; không có số tự nhiên lớn nhất.', size=13, fill='#444'))
    return svg(720, 210, ''.join(b))


def venn(cx1, cx2, cy, rx, ry, left, right, both, tl, tr, tb):
    out = []
    out.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#cfe3f4" fill-opacity="0.7" stroke="%s" stroke-width="2.2"/>' % (cx1, cy, rx, ry, INK))
    out.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#f7e29b" fill-opacity="0.7" stroke="%s" stroke-width="2.2"/>' % (cx2, cy, rx, ry, INK))
    mid = (cx1 + cx2) / 2
    out.append(TL(cx1 - 52, cy - 6, left, size=15, lh=22))
    out.append(TL(cx2 + 52, cy - 6, right, size=15, lh=22))
    out.append(TL(mid, cy - 6, both, size=15, lh=22, weight='bold'))
    out.append(T(cx1 - 20, cy - ry - 10, tl, size=14, weight='bold'))
    out.append(T(cx2 + 20, cy - ry - 10, tr, size=14, weight='bold'))
    out.append(T(mid, cy + ry + 26, tb, size=14, fill=RED, weight='bold'))
    return ''.join(out)


def fig_ucln():
    b = [title(720, 'Ước chung và ước chung lớn nhất của 12 và 18')]
    b.append(venn(270, 450, 160, 150, 90, ['4', '12'], ['9', '18'], ['1;  2', '3;  6'], 'Ư(12)', 'Ư(18)',
                  'ƯC(12, 18) = {1; 2; 3; 6},  ƯCLN(12, 18) = 6'))
    return svg(720, 300, ''.join(b))


def fig_bcnn():
    b = [title(720, 'Bội chung và bội chung nhỏ nhất của 4 và 6')]
    b.append(venn(270, 450, 160, 150, 90, ['4', '8', '16', '20'], ['6', '18', '30'], ['12', '24'], 'B(4)', 'B(6)',
                  'BC(4, 6) gồm 12; 24; 36; …   BCNN(4, 6) = 12'))
    b.append(T(360, 314, 'Chỉ liệt kê các bội khác 0 không vượt quá 30.', size=12, fill='#555'))
    return svg(720, 330, ''.join(b))


def fig_truc_so_nguyen():
    b = [title(720, 'Trục số và hai số đối nhau')]
    y = 110
    b.append(L(30, y, 690, y, w=2.5, arrow=True) + L(690, y, 30, y, w=2.5, arrow=True))
    for k in range(-5, 6):
        x = 360 + k * 56
        b.append(L(x, y - 7, x, y + 7, w=2))
        b.append(T(x, y + 28, str(k).replace('-', '−'), size=16, weight='bold' if k == 0 else 'normal'))
    b.append(dot(360 - 3 * 56, y, 5, RED) + dot(360 + 3 * 56, y, 5, RED))
    b.append(T(360 - 3 * 56, y - 18, '−3', size=14, fill=RED, weight='bold'))
    b.append(T(360 + 3 * 56, y - 18, '3', size=14, fill=RED, weight='bold'))
    b.append(PATH('M%d,%d Q360,40 %d,%d' % (360 - 3 * 56, y - 28, 360 + 3 * 56, y - 28), stroke=GREY, w=1.5))
    b.append(T(360, 52, 'cách đều điểm 0: 3 và −3 là hai số đối nhau', size=13))
    b.append(TL(120, 175, ['Bên trái 0:', 'số nguyên âm'], size=13, lh=17))
    b.append(TL(600, 175, ['Bên phải 0:', 'số nguyên dương'], size=13, lh=17))
    b.append(T(360, 200, 'Điểm nằm bên trái biểu diễn số nhỏ hơn.', size=13, fill='#444'))
    return svg(720, 222, ''.join(b))


def fig_cong_so_nguyen():
    b = [title(720, 'Cộng số nguyên trên trục số')]
    def line(y, ex, a, b_, res, label):
        out = [L(40, y, 680, y, w=2, arrow=True)]
        for k in range(-6, 7):
            x = 360 + k * 46
            out.append(L(x, y - 5, x, y + 5, w=1.5))
            out.append(T(x, y + 22, str(k).replace('-', '−'), size=12))
        xa, xb = 360 + a * 46, 360 + (a + b_) * 46
        out.append(dot(xa, y, 4.5, BLUE))
        out.append(PATH('M%d,%d Q%d,%d %d,%d' % (xa, y - 6, (xa + xb) / 2, y - 48, xb, y - 6), stroke=RED, w=2.5))
        out.append(L(xb - 2, y - 8, xb + (1 if b_ > 0 else -1), y - 6, w=2, arrow=True, stroke=RED))
        out.append(dot(xb, y, 4.5, RED))
        out.append(T(360, y - 62, label, size=15, weight='bold'))
        return ''.join(out)
    b.append(line(110, 0, -3, 5, 2, '(−3) + 5 = 2'))
    b.append(line(220, 0, -2, -3, -5, '(−2) + (−3) = −5'))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- Chương IV
def fig_tg_vuong_lucgiac():
    b = [title(720, 'Tam giác đều, hình vuông, lục giác đều')]
    # tam giác đều
    s = 130
    A, B, Cc = (115, 190 - s * math.sqrt(3) / 2), (50, 190), (180, 190)
    b.append(shape([A, B, Cc]))
    for p, q in ((A, B), (B, Cc), (Cc, A)):
        b.append(tick(*p, *q))
    for p, q1, q2 in ((A, B, Cc), (B, Cc, A), (Cc, A, B)):
        b.append(angle_arc(*p, *q1, *q2, r=22))
    b.append(T(115, 160, '60°', size=12) + T(80, 182, '60°', size=12) + T(150, 182, '60°', size=12))
    b.append(TL(115, 222, ['Tam giác đều', 'ba cạnh bằng nhau, mỗi góc 60°'], size=12, lh=16, weight='normal'))
    # hình vuông
    x0, y0, a = 300, 80, 110
    P = [(x0, y0), (x0 + a, y0), (x0 + a, y0 + a), (x0, y0 + a)]
    b.append(shape(P))
    b.append(L(*P[0], *P[2], stroke=GREY, w=1.5, dash='5 3') + L(*P[1], *P[3], stroke=GREY, w=1.5, dash='5 3'))
    for i in range(4):
        b.append(tick(*P[i], *P[(i + 1) % 4]))
        b.append(right_angle(*P[i], *P[(i + 1) % 4], *P[i - 1], s=10))
    b.append(TL(x0 + a / 2, 222, ['Hình vuông: bốn cạnh bằng nhau,', 'bốn góc vuông,', 'hai đường chéo bằng nhau'], size=12, lh=16))
    # lục giác đều
    cx, cy, r = 600, 135, 62
    H = regpoly(cx, cy, r, 6, rot=0)
    b.append(shape(H))
    for k in range(3):
        b.append(L(*H[k], *H[k + 3], stroke=GREY, w=1.5, dash='5 3'))
        b.append(tick(*H[k], *H[k + 3], n=2) if False else '')
    for k in range(6):
        b.append(tick(*H[k], *H[(k + 1) % 6]))
    b.append(angle_arc(*H[0], *H[1], *H[5], r=16))
    b.append(T(H[0][0] + 8, H[0][1] + 4, '120°', size=11, anchor='start'))
    b.append(TL(cx, 222, ['Lục giác đều: sáu cạnh bằng nhau,', 'mỗi góc 120°,', 'ba đường chéo chính bằng nhau'], size=12, lh=16))
    return svg(720, 262, ''.join(b))


def fig_tu_giac():
    b = [title(720, 'Hình chữ nhật, hình thoi, hình bình hành, hình thang cân')]
    # HCN
    x, y, w, h = 20, 70, 150, 90
    P = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    b.append(shape(P))
    for i in range(4):
        b.append(right_angle(*P[i], *P[(i + 1) % 4], *P[i - 1], s=10))
    b.append(tick(*P[0], *P[1]) + tick(*P[2], *P[3]) + tick(*P[1], *P[2], n=2) + tick(*P[3], *P[0], n=2))
    b.append(L(*P[0], *P[2], stroke=GREY, w=1.5, dash='5 3') + L(*P[1], *P[3], stroke=GREY, w=1.5, dash='5 3'))
    b.append(tick(*P[0], *P[2], n=3) if False else '')
    b.append(TL(x + w / 2, 190, ['Hình chữ nhật', 'bốn góc vuông;', 'hai đường chéo bằng nhau'], size=11, lh=15))
    # thoi
    cx, cy = 275, 115
    Q = [(cx, cy - 55), (cx + 70, cy), (cx, cy + 55), (cx - 70, cy)]
    b.append(shape(Q))
    for i in range(4):
        b.append(tick(*Q[i], *Q[(i + 1) % 4]))
    b.append(L(*Q[0], *Q[2], stroke=GREY, w=1.5, dash='5 3') + L(*Q[1], *Q[3], stroke=GREY, w=1.5, dash='5 3'))
    b.append(right_angle(cx, cy, cx + 1, cy - 1, cx - 1, cy - 1, s=9) if False else right_angle(cx, cy, cx, cy - 10, cx + 10, cy, s=9))
    b.append(TL(cx, 190, ['Hình thoi', 'bốn cạnh bằng nhau;', 'hai đường chéo vuông góc'], size=11, lh=15))
    # bình hành
    P2 = [(380, 160), (500, 160), (540, 70), (420, 70)]
    b.append(shape(P2))
    b.append(tick(*P2[0], *P2[1]) + tick(*P2[2], *P2[3]) + tick(*P2[1], *P2[2], n=2) + tick(*P2[3], *P2[0], n=2))
    b.append(L(*P2[0], *P2[2], stroke=GREY, w=1.5, dash='5 3') + L(*P2[1], *P2[3], stroke=GREY, w=1.5, dash='5 3'))
    ox, oy = (P2[0][0] + P2[2][0]) / 2, (P2[0][1] + P2[2][1]) / 2
    b.append(dot(ox, oy, 3.5, RED))
    b.append(TL(460, 190, ['Hình bình hành', 'cạnh đối song song, bằng nhau;', 'hai đường chéo cắt nhau', 'tại trung điểm mỗi đường'], size=11, lh=15))
    # thang cân
    P3 = [(570, 160), (700, 160), (672, 70), (598, 70)]
    b.append(shape(P3))
    b.append(tick(*P3[1], *P3[2]) + tick(*P3[3], *P3[0]))
    b.append(L(*P3[0], *P3[2], stroke=GREY, w=1.5, dash='5 3') + L(*P3[1], *P3[3], stroke=GREY, w=1.5, dash='5 3'))
    b.append(TL(635, 190, ['Hình thang cân', 'hai đáy song song;', 'hai cạnh bên bằng nhau;', 'hai đường chéo bằng nhau'], size=11, lh=15))
    return svg(720, 262, ''.join(b))


def fig_dien_tich():
    b = [title(720, 'Công thức chu vi và diện tích một số tứ giác')]
    # vuông
    b.append(shape([(20, 60), (100, 60), (100, 140), (20, 140)]))
    b.append(T(60, 54, 'a', size=14, weight='bold') + T(112, 105, 'a', size=14, weight='bold'))
    b.append(TL(60, 172, ['Hình vuông', 'S = a²', 'C = 4a'], size=12, lh=17))
    # chữ nhật
    b.append(shape([(150, 70), (270, 70), (270, 140), (150, 140)]))
    b.append(T(210, 62, 'a', size=14, weight='bold') + T(282, 109, 'b', size=14, weight='bold'))
    b.append(TL(210, 172, ['Hình chữ nhật', 'S = a · b', 'C = 2(a + b)'], size=12, lh=17))
    # thang
    b.append(shape([(320, 140), (440, 140), (415, 70), (350, 70)]))
    b.append(L(375, 70, 375, 140, stroke=RED, w=1.5, dash='4 3'))
    b.append(right_angle(375, 140, 440, 140, 375, 70, s=8))
    b.append(T(383, 62, 'a', size=14, weight='bold') + T(380, 158, 'b', size=14, weight='bold') + T(381, 108, 'h', size=14, weight='bold', anchor='start'))
    b.append(TL(380, 185, ['Hình thang', 'S = (a + b) · h : 2'], size=12, lh=17))
    # bình hành
    b.append(shape([(470, 140), (570, 140), (600, 70), (500, 70)]))
    b.append(L(570, 70, 570, 140, stroke=RED, w=1.5, dash='4 3') if False else L(500, 70, 500, 140, stroke=RED, w=1.5, dash='4 3'))
    b.append(right_angle(500, 140, 570, 140, 500, 70, s=8))
    b.append(T(520, 160, 'a', size=14, weight='bold') + T(490, 108, 'h', size=14, weight='bold', anchor='end'))
    b.append(TL(535, 185, ['Hình bình hành', 'S = a · h'], size=12, lh=17))
    # thoi
    cx, cy = 665, 105
    Q = [(cx, cy - 40), (cx + 45, cy), (cx, cy + 40), (cx - 45, cy)]
    b.append(shape(Q))
    b.append(L(*Q[0], *Q[2], stroke=RED, w=1.5, dash='4 3') + L(*Q[1], *Q[3], stroke=RED, w=1.5, dash='4 3'))
    b.append(T(cx + 8, cy - 12, 'n', size=14, weight='bold', anchor='start') + T(cx + 22, cy + 18, 'm', size=14, weight='bold'))
    b.append(TL(cx, 185, ['Hình thoi', 'S = m · n : 2'], size=12, lh=17))
    b.append(T(360, 250, 'Chu vi hình bình hành, hình thang, hình thoi bằng tổng độ dài các cạnh.', size=12, fill='#444'))
    return svg(720, 266, ''.join(b))


def axes_shape(kind, cx, cy, size=48):
    """Trả về (hình, các trục đối xứng) cho từng loại hình."""
    s = size
    if kind == 'tamgiac':
        r = s * 1.15
        P = regpoly(cx, cy + 6, r, 3)
        out = [shape(P)]
        ax = []
        for k in range(3):
            q = P[k]
            m = ((P[(k + 1) % 3][0] + P[(k + 2) % 3][0]) / 2, (P[(k + 1) % 3][1] + P[(k + 2) % 3][1]) / 2)
            ux, uy = unit(*q, *m)
            ax.append((q[0] - ux * 10, q[1] - uy * 10, m[0] + ux * 10, m[1] + uy * 10))
        return out, ax
    if kind == 'vuong':
        P = [(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s)]
        e = s + 12
        ax = [(cx - e, cy - e, cx + e, cy + e), (cx - e, cy + e, cx + e, cy - e), (cx - e, cy, cx + e, cy), (cx, cy - e, cx, cy + e)]
        return [shape(P)], ax
    if kind == 'hcn':
        P = [(cx - s * 1.3, cy - s * 0.75), (cx + s * 1.3, cy - s * 0.75), (cx + s * 1.3, cy + s * 0.75), (cx - s * 1.3, cy + s * 0.75)]
        ax = [(cx - s * 1.3 - 12, cy, cx + s * 1.3 + 12, cy), (cx, cy - s * 0.75 - 12, cx, cy + s * 0.75 + 12)]
        return [shape(P)], ax
    if kind == 'thoi':
        P = [(cx, cy - s), (cx + s * 1.3, cy), (cx, cy + s), (cx - s * 1.3, cy)]
        ax = [(cx, cy - s - 12, cx, cy + s + 12), (cx - s * 1.3 - 12, cy, cx + s * 1.3 + 12, cy)]
        return [shape(P)], ax
    if kind == 'thangcan':
        P = [(cx - s * 1.3, cy + s * 0.7), (cx + s * 1.3, cy + s * 0.7), (cx + s * 0.7, cy - s * 0.7), (cx - s * 0.7, cy - s * 0.7)]
        ax = [(cx, cy - s * 0.7 - 12, cx, cy + s * 0.7 + 12)]
        return [shape(P)], ax
    if kind == 'lucgiac':
        P = regpoly(cx, cy, s * 1.05, 6, rot=0)
        ax = []
        for k in range(3):
            # đường chéo chính
            a, bq = P[k], P[k + 3]
            ux, uy = unit(*a, *bq)
            ax.append((a[0] - ux * 10, a[1] - uy * 10, bq[0] + ux * 10, bq[1] + uy * 10))
            # đường nối trung điểm hai cạnh đối
            m1 = ((P[k][0] + P[(k + 1) % 6][0]) / 2, (P[k][1] + P[(k + 1) % 6][1]) / 2)
            m2 = ((P[k + 3][0] + P[(k + 4) % 6][0]) / 2, (P[k + 3][1] + P[(k + 4) % 6][1]) / 2)
            ux, uy = unit(*m1, *m2)
            ax.append((m1[0] - ux * 10, m1[1] - uy * 10, m2[0] + ux * 10, m2[1] + uy * 10))
        return [shape(P)], ax
    if kind == 'tron':
        r = s * 1.05
        ax = []
        for k in range(4):
            a = math.radians(45 * k)
            ax.append((cx - (r + 12) * math.cos(a), cy - (r + 12) * math.sin(a), cx + (r + 12) * math.cos(a), cy + (r + 12) * math.sin(a)))
        return [C(cx, cy, r, fill=FILL, stroke=INK, w=2.2)], ax
    if kind == 'binhhanh':
        P = [(cx - s * 1.5, cy + s * 0.7), (cx + s * 0.6, cy + s * 0.7), (cx + s * 1.5, cy - s * 0.7), (cx - s * 0.6, cy - s * 0.7)]
        return [shape(P)], []
    raise KeyError(kind)


def fig_truc_doi_xung():
    b = [title(720, 'Trục đối xứng của một số hình (nét đứt đỏ)')]
    cells = [('tamgiac', 'Tam giác đều: 3 trục'), ('vuong', 'Hình vuông: 4 trục'), ('hcn', 'Hình chữ nhật: 2 trục'),
             ('thoi', 'Hình thoi: 2 trục'), ('thangcan', 'Hình thang cân: 1 trục'), ('lucgiac', 'Lục giác đều: 6 trục'),
             ('tron', 'Đường tròn: vô số trục'), ('binhhanh', 'Hình bình hành: không có trục')]
    for i, (k, lab) in enumerate(cells):
        cx = 100 + (i % 4) * 175
        cy = 110 + (i // 4) * 150
        shp, axes = axes_shape(k, cx, cy, 40)
        b += shp
        for a in axes:
            b.append(L(*a, stroke=AX, w=1.6, dash='5 3'))
        b.append(T(cx, cy + 66, lab, size=12))
    return svg(720, 330, ''.join(b))


def fig_tam_doi_xung():
    b = [title(720, 'Tâm đối xứng của một số hình')]
    cells = [('hcn', 'Hình chữ nhật', True), ('thoi', 'Hình thoi', True), ('vuong', 'Hình vuông', True),
             ('binhhanh', 'Hình bình hành', True), ('lucgiac', 'Lục giác đều', True), ('tron', 'Đường tròn', True),
             ('tamgiac', 'Tam giác đều: không có', False), ('thangcan', 'Hình thang cân: không có', False)]
    for i, (k, lab, has) in enumerate(cells):
        cx = 100 + (i % 4) * 175
        cy = 110 + (i // 4) * 150
        shp, axes = axes_shape(k, cx, cy, 40)
        b += shp
        if has:
            b.append(dot(cx, cy, 4.5, RED))
            b.append(T(cx + 9, cy - 5, 'O', size=13, anchor='start', fill=RED, weight='bold'))
        b.append(T(cx, cy + 66, lab, size=12))
    b.append(T(360, 360, 'Chấm đỏ O: tâm đối xứng (quay nửa vòng 180° quanh O thì hình chồng khít với hình ban đầu).', size=12, fill='#444'))
    return svg(720, 376, ''.join(b))



# ---------------------------------------------------------------- Tập 2: phân số, số thập phân
def fbar(x, y, w, h, parts, shaded, col=BLUE):
    out = []
    pw = w / parts
    for i in range(parts):
        out.append(R(x + i * pw, y, pw, h, fill=col if i < shaded else '#ffffff', stroke=INK, sw=1.5))
    return ''.join(out)


def fig_phan_so_bang_nhau():
    b = [title(720, 'Phân số bằng nhau: 1/2 = 2/4 = 4/8')]
    for i, (parts, sh, lab) in enumerate(((2, 1, '1/2'), (4, 2, '2/4'), (8, 4, '4/8'))):
        y = 56 + i * 56
        b.append(fbar(120, y, 440, 36, parts, sh))
        b.append(T(90, y + 25, lab, size=17, weight='bold', anchor='end'))
    b.append(T(360, 236, 'Cùng một phần của hình: phần tô màu bằng nhau trong cả ba hình.', size=13, fill='#444'))
    b.append(T(360, 258, 'Nhân (hoặc chia) cả tử và mẫu với cùng một số khác 0 được phân số bằng nó.', size=13, fill='#444'))
    return svg(720, 276, ''.join(b))


def fig_so_sanh_ps():
    b = [title(720, 'So sánh 2/3 và 3/4 (quy đồng mẫu: 8/12 và 9/12)')]
    b.append(fbar(110, 56, 480, 40, 12, 8))
    b.append(T(88, 82, '2/3 = 8/12', size=15, anchor='end', weight='bold'))
    b.append(fbar(110, 118, 480, 40, 12, 9, col=ORANGE))
    b.append(T(88, 144, '3/4 = 9/12', size=15, anchor='end', weight='bold'))
    b.append(T(360, 196, 'Cùng mẫu 12: tử 8 < 9 nên 2/3 < 3/4.', size=14))
    return svg(720, 216, ''.join(b))


def fig_hon_so():
    b = [title(720, 'Hỗn số: 7/3 = 2 1/3')]
    for k in range(3):
        parts_shaded = 3 if k < 2 else 1
        b.append(fbar(40 + k * 215, 70, 200, 44, 3, parts_shaded))
    b.append(T(140, 138, '1', size=14) + T(355, 138, '1', size=14) + T(570, 138, '1/3', size=14))
    b.append(T(360, 178, 'Có 7 phần, mỗi phần là 1/3 đơn vị: 2 đơn vị đầy đủ và còn 1/3.', size=14))
    return svg(720, 198, ''.join(b))


def grid100(x, y, cell, shaded, col=BLUE):
    out = []
    for r in range(10):
        for c in range(10):
            idx = r * 10 + c
            out.append(R(x + c * cell, y + r * cell, cell, cell, fill=col if idx < shaded else '#ffffff', stroke=GREY, sw=1))
    out.append(R(x, y, cell * 10, cell * 10, fill='none', stroke=INK, sw=2))
    return ''.join(out)


def fig_thap_phan():
    b = [title(720, 'Số thập phân')]
    b.append(grid100(40, 50, 18, 7))
    b.append(TL(130, 258, ['7 ô trong 100 ô', '7/100 = 0,07'], size=14, lh=20))
    # trục số
    y = 130
    b.append(L(290, y, 700, y, w=2.5, arrow=True) + L(700, y, 290, y, w=2.5, arrow=True))
    for k in range(-2, 3):
        x = 495 + k * 90
        b.append(L(x, y - 6, x, y + 6, w=2))
        b.append(T(x, y + 26, str(k).replace('-', '−'), size=14))
    xm = 495 - 1.3 * 90
    b.append(dot(xm, y, 5, RED))
    b.append(T(xm, y - 16, '−1,3', size=14, fill=RED, weight='bold'))
    b.append(T(495, 190, '−13/10 = −1,3', size=14))
    b.append(T(495, 214, 'Số đối của 1,5 là −1,5.', size=13, fill='#555'))
    return svg(720, 300, ''.join(b))


def fig_phan_tram():
    b = [title(720, 'Tỉ số phần trăm của 18 và 24: 75%')]
    b.append(grid100(60, 50, 22, 75))
    b.append(TL(480, 110, ['18/24 · 100% = 0,75 · 100%', '= 75%'], size=17, lh=28, anchor='middle'))
    b.append(TL(480, 190, ['75 ô tô màu trong 100 ô', 'ứng với 75%'], size=14, lh=20))
    return svg(720, 292, ''.join(b))


# ---------------------------------------------------------------- Hình học cơ bản
def ptlabel(x, y, s, dx=0, dy=-10):
    return T(x + dx, y + dy, s, size=15, weight='bold')


def fig_diem_duong_thang():
    b = [title(720, 'Điểm, đường thẳng')]
    # A thuộc d, B không thuộc d
    b.append(L(20, 150, 190, 90, w=2.2))
    b.append(T(196, 88, 'd', size=15, weight='bold', anchor='start'))
    b.append(dot(70, 132) + ptlabel(70, 132, 'A'))
    b.append(dot(110, 56) + ptlabel(110, 56, 'B'))
    b.append(TL(105, 190, ['A ∈ d (A thuộc d)', 'B ∉ d (B không thuộc d)'], size=12, lh=17))
    # đường thẳng AB
    b.append(L(240, 160, 420, 90, w=2.2))
    b.append(dot(285, 142) + ptlabel(285, 142, 'A', dy=18))
    b.append(dot(375, 107) + ptlabel(375, 107, 'B', dy=18))
    b.append(TL(330, 190, ['Qua hai điểm A, B', 'có một và chỉ một đường thẳng'], size=12, lh=17))
    # thẳng hàng / không thẳng hàng
    b.append(L(470, 170, 700, 170, w=2.2))
    for x, n in ((500, 'A'), (580, 'B'), (660, 'C')):
        b.append(dot(x, 170) + ptlabel(x, 170, n, dy=-10))
    b.append(T(585, 196, 'A, B, C thẳng hàng', size=12))
    b.append(dot(520, 100) + ptlabel(520, 100, 'D', dy=-10) + dot(580, 72) + ptlabel(580, 72, 'E', dy=-10) + dot(650, 102) + ptlabel(650, 102, 'F', dy=-10))
    b.append(L(520, 100, 580, 72, w=1.2, stroke=GREY, dash='4 3') + L(580, 72, 650, 102, w=1.2, stroke=GREY, dash='4 3'))
    b.append(T(585, 126, 'D, E, F không thẳng hàng', size=12))
    # cắt nhau, song song
    b.append(L(40, 250, 200, 330, w=2.2) + L(40, 330, 200, 250, w=2.2) + dot(120, 290, 4, RED))
    b.append(TL(120, 358, ['Hai đường thẳng cắt nhau:', 'một giao điểm'], size=12, lh=16))
    b.append(L(280, 255, 460, 255, w=2.2) + L(280, 305, 460, 305, w=2.2))
    b.append(TL(370, 358, ['Hai đường thẳng song song:', 'không có điểm chung'], size=12, lh=16))
    b.append(L(540, 262, 690, 322, w=2.2) + L(540, 322, 690, 262, w=2.2) if False else '')
    return svg(720, 392, ''.join(b))


def fig_tia():
    b = [title(720, 'Điểm nằm giữa, tia, hai tia đối nhau')]
    y = 80
    b.append(L(30, y, 330, y, w=2.2))
    for x, n in ((70, 'A'), (180, 'M'), (290, 'B')):
        b.append(dot(x, y) + ptlabel(x, y, n, dy=-12))
    b.append(T(180, 118, 'M nằm giữa A và B', size=13))
    # tia Ox, Oy
    b.append(L(400, y, 700, y, w=2.2))
    b.append(dot(550, y, 4, RED) + T(550, y - 12, 'O', size=15, weight='bold'))
    b.append(L(550, y, 700, y, w=3.5, stroke=BLUE) + L(550, y, 400, y, w=3.5, stroke=ORANGE))
    b.append(T(715, y + 5, 'y', size=14, anchor='end') if False else '')
    b.append(T(690, y - 12, 'y', size=14, weight='bold') + T(410, y - 12, 'x', size=14, weight='bold'))
    b.append(TL(550, 118, ['Ox và Oy là hai tia đối nhau', '(chung gốc O, tạo thành đường thẳng xy)'], size=13, lh=18))
    # tia trùng nhau
    y2 = 190
    b.append(L(60, y2, 330, y2, w=2.2, arrow=True))
    b.append(dot(60, y2, 4, RED) + T(60, y2 - 12, 'O', size=15, weight='bold'))
    b.append(dot(200, y2, 3) + T(200, y2 - 10, 'A', size=14, weight='bold') + dot(300, y2, 3) + T(300, y2 - 10, 'B', size=14, weight='bold'))
    b.append(TL(190, y2 + 32, ['Tia OA và tia OB là hai tia trùng nhau', '(chung gốc O, tia này nằm trên tia kia)'], size=13, lh=18))
    b.append(TL(550, 200, ['Mỗi điểm trên đường thẳng', 'là gốc của hai tia đối nhau'], size=13, lh=18))
    return svg(720, 258, ''.join(b))


def fig_doan_thang():
    b = [title(720, 'Đoạn thẳng và độ dài đoạn thẳng')]
    y = 100
    b.append(L(70, y, 650, y, w=3))
    for x, n in ((70, 'A'), (298, 'M'), (650, 'B')):
        b.append(dot(x, y, 5) + T(x, y - 14, n, size=16, weight='bold'))
    b.append(PL([(70, y + 22), (70, y + 30), (298, y + 30), (298, y + 22)], w=1.5) + T(184, y + 52, 'AM = 3 cm', size=14))
    b.append(PL([(298, y + 22), (298, y + 30), (650, y + 30), (650, y + 22)], w=1.5) + T(474, y + 52, 'MB = 5 cm', size=14))
    b.append(PL([(70, y + 70), (70, y + 78), (650, y + 78), (650, y + 70)], w=1.5) + T(360, y + 100, 'AB = AM + MB = 3 + 5 = 8 cm', size=15, weight='bold'))
    return svg(720, 228, ''.join(b))


def fig_trung_diem():
    b = [title(720, 'Trung điểm của đoạn thẳng')]
    y = 100
    b.append(L(70, y, 650, y, w=3))
    for x, n in ((70, 'A'), (360, 'M'), (650, 'B')):
        b.append(dot(x, y, 5, RED if n == 'M' else INK) + T(x, y - 14, n, size=16, weight='bold'))
    b.append(tick(70, y, 360, y, n=1, size=9) + tick(360, y, 650, y, n=1, size=9))
    b.append(PL([(70, y + 22), (70, y + 30), (650, y + 30), (650, y + 22)], w=1.5) + T(360, y + 52, 'AB = 14 cm', size=14))
    b.append(TL(360, y + 86, ['M là trung điểm của AB:  MA = MB = AB : 2 = 14 : 2 = 7 cm'], size=15, weight='bold'))
    return svg(720, 220, ''.join(b))


def fig_goc():
    b = [title(720, 'Góc')]
    # góc xOy
    O = (110, 160)
    X = (260, 160)
    Y = (200, 60)
    b.append(L(*O, *X, w=2.5) + L(*O, *Y, w=2.5))
    b.append(angle_arc(*O, *X, *Y, r=30, color=RED, w=2))
    b.append(dot(*O, 4) + T(O[0] - 14, O[1] + 20, 'O', size=15, weight='bold') + T(X[0] + 8, X[1] + 6, 'x', size=15, weight='bold', anchor='start') + T(Y[0] + 6, Y[1] - 4, 'y', size=15, weight='bold', anchor='start'))
    b.append(TL(170, 205, ['Góc xOy: đỉnh O,', 'hai cạnh là tia Ox và Oy'], size=12, lh=16))
    # góc bẹt
    b.append(L(340, 160, 520, 160, w=2.5))
    b.append(dot(430, 160, 4) + T(430, 182, 'O', size=15, weight='bold') + T(345, 150, 'x', size=15, weight='bold', anchor='start') + T(515, 150, 'y', size=15, weight='bold', anchor='end'))
    b.append(PATH('M400,160 A30,30 0 0 1 460,160', stroke=RED, w=2))
    b.append(TL(430, 205, ['Góc bẹt: hai cạnh', 'là hai tia đối nhau'], size=12, lh=16))
    # điểm M trong góc
    O2 = (570, 160)
    X2 = (700, 160)
    Y2 = (650, 60)
    b.append(L(*O2, *X2, w=2.5) + L(*O2, *Y2, w=2.5))
    b.append(dot(655, 130, 4, RED) + T(662, 126, 'M', size=14, weight='bold', anchor='start'))
    b.append(TL(640, 205, ['Điểm M nằm trong góc xOy'], size=12))
    return svg(720, 232, ''.join(b))


def fig_loai_goc():
    b = [title(720, 'Các loại góc')]
    specs = [(40, 'Góc nhọn', '0° < số đo < 90°', 50, 100), (200, 'Góc vuông', 'số đo = 90°', 90, 100),
             (360, 'Góc tù', '90° < số đo < 180°', 130, 100), (520, 'Góc bẹt', 'số đo = 180°', 180, 70)]
    for x0, n, d, ang, r in specs:
        ox, oy = x0 + 20, 150
        if ang == 180:
            ox = x0 + 80
        ex, ey = ox + r, oy
        px, py = ox + r * math.cos(math.radians(ang)), oy - r * math.sin(math.radians(ang))
        b.append(L(ox, oy, ex, ey, w=2.5) + L(ox, oy, px, py, w=2.5))
        if ang == 90:
            b.append(right_angle(ox, oy, ex, ey, px, py, s=14))
        else:
            rr = 26
            b.append(PATH('M%.1f,%.1f A%d,%d 0 0 0 %.1f,%.1f' % (ox + rr, oy, rr, rr, ox + rr * math.cos(math.radians(ang)), oy - rr * math.sin(math.radians(ang))), stroke=RED, w=2))
        b.append(dot(ox, oy, 4))
        b.append(T(x0 + 80, 190, n, size=14, weight='bold'))
        b.append(T(x0 + 80, 210, d, size=12))
    return svg(720, 228, ''.join(b))


def fig_thuoc_do_goc():
    b = [title(720, 'Đo góc bằng thước đo góc (ví dụ: góc 60°)')]
    cx, cy, R0 = 360, 220, 190
    b.append(PATH('M%d,%d A%d,%d 0 0 1 %d,%d Z' % (cx - R0, cy, R0, R0, cx + R0, cy), fill='#e8f3fb', stroke=INK, w=2))
    for deg in range(0, 181, 5):
        a = math.radians(deg)
        ln = 14 if deg % 10 == 0 else 7
        x1, y1 = cx + R0 * math.cos(a), cy - R0 * math.sin(a)
        x2, y2 = cx + (R0 - ln) * math.cos(a), cy - (R0 - ln) * math.sin(a)
        b.append(L(x1, y1, x2, y2, w=1.2))
    b.append(L(cx - R0 - 20, cy, cx + R0 + 20, cy, w=2.5))
    # góc 60°
    a60 = math.radians(60)
    b.append(L(cx, cy, cx + (R0 + 20) * math.cos(a60), cy - (R0 + 20) * math.sin(a60), w=3, stroke=RED))
    b.append(L(cx, cy, cx + R0 + 20, cy, w=3, stroke=RED))
    for deg in range(0, 181, 30):
        a = math.radians(deg)
        yy = cy - (R0 - 32) * math.sin(a) + 5
        if deg in (0, 180):
            yy = cy - 12
        b.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="13" fill="%s" stroke="#e8f3fb" stroke-width="4" paint-order="stroke">%d</text>'
                 % (cx + (R0 - 32) * math.cos(a), yy, INK, deg))
    b.append(dot(cx, cy, 5, RED) + T(cx - 14, cy + 22, 'O', size=15, weight='bold'))
    b.append(T(cx + 70, cy - 24, '60°', size=15, weight='bold', fill=RED))
    b.append(TL(120, 120, ['Tâm thước', 'trùng đỉnh O'], size=12, lh=16))
    b.append(L(150, 138, cx - 12, cy - 4, w=1, stroke=GREY, arrow=True))
    b.append(TL(620, 205, ['Một cạnh đi', 'qua vạch 0'], size=12, lh=16))
    b.append(L(612, 212, cx + R0 - 20, cy - 4, w=1, stroke=GREY, arrow=True))
    b.append(TL(560, 100, ['Cạnh kia đi qua', 'vạch 60: số đo', 'góc là 60°'], size=12, lh=16))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- Thống kê, xác suất
def book_icon(x, y, half=False, w=34, h=26):
    out = []
    ww = w / 2 if half else w
    out.append(R(x, y, ww, h, fill=ORANGE, stroke=INK, sw=1.5, rx=2))
    out.append(L(x + 5, y, x + 5, y + h, w=1.5, stroke=INK))
    return ''.join(out)


def fig_bieu_do_tranh():
    b = [title(720, 'Biểu đồ tranh (ví dụ minh họa)')]
    rows = [('Lớp 6A', 4.5), ('Lớp 6B', 3), ('Lớp 6C', 5)]
    for i, (n, v) in enumerate(rows):
        y = 56 + i * 42
        b.append(T(100, y + 20, n, size=15, anchor='end', weight='bold'))
        k = int(v)
        for j in range(k):
            b.append(book_icon(120 + j * 40, y))
        if v - k >= 0.5:
            b.append(book_icon(120 + k * 40, y, half=True))
        b.append(T(120 + 5 * 40 + 56, y + 20, '= %d quyển' % int(v * 10), size=13, anchor='start', fill='#444'))
    b.append(book_icon(110, 192) + T(156, 210, ': 10 quyển sách (nửa hình: 5 quyển)', size=14, anchor='start'))
    b.append(T(360, 248, 'Đọc biểu đồ: đếm số biểu tượng ở mỗi dòng rồi nhân với giá trị của một biểu tượng (lớp 6A: 4,5 · 10 = 45).', size=12, fill='#444'))
    return svg(720, 266, ''.join(b))


def bar_chart(x0, y0, w, h, cats, series, ymax, step, cols, legend=None, title_y=None):
    out = []
    out.append(L(x0, y0, x0, y0 - h, w=2, arrow=True))
    out.append(L(x0, y0, x0 + w, y0, w=2, arrow=True))
    for v in range(0, ymax + 1, step):
        yy = y0 - v * h / ymax * 0.95
        out.append(L(x0 - 5, yy, x0, yy, w=1.5))
        out.append(T(x0 - 9, yy + 4, str(v), size=12, anchor='end'))
        if v > 0:
            out.append(L(x0, yy, x0 + w - 10, yy, w=0.8, stroke='#d5dbe2'))
    n = len(cats)
    gw = (w - 20) / n
    ns = len(series)
    bw = min(46, (gw - 20) / ns)
    for i, c in enumerate(cats):
        gx = x0 + 10 + i * gw + gw / 2
        for j in range(ns):
            v = series[j][i]
            bh = v * h / ymax * 0.95
            bx = gx - ns * bw / 2 + j * bw
            out.append(R(bx, y0 - bh, bw, bh, fill=cols[j], stroke=INK, sw=1.5))
            out.append(T(bx + bw / 2, y0 - bh - 5, str(v), size=12, weight='bold'))
        out.append(T(gx, y0 + 20, c, size=13))
    return ''.join(out)


def fig_bieu_do_cot():
    b = [title(720, 'Biểu đồ cột: số học sinh thích mỗi môn')]
    b.append(bar_chart(120, 230, 480, 170, ['Toán', 'Văn', 'Anh'], [[12, 8, 10]], 14, 2, [BLUE]))
    b.append(T(70, 130, 'Số HS', size=12, anchor='middle'))
    b.append(T(360, 270, 'Tổng: 12 + 8 + 10 = 30 học sinh', size=13, fill='#444'))
    return svg(720, 286, ''.join(b))


def fig_bieu_do_cot_kep():
    b = [title(720, 'Biểu đồ cột kép: số học sinh giỏi')]
    b.append(bar_chart(110, 230, 400, 170, ['Lớp 6A', 'Lớp 6B'], [[12, 10], [15, 14]], 16, 4, [BLUE, ORANGE]))
    b.append(R(540, 90, 18, 18, fill=BLUE, stroke=INK, sw=1.5) + T(566, 104, 'Kì I', size=14, anchor='start'))
    b.append(R(540, 120, 18, 18, fill=ORANGE, stroke=INK, sw=1.5) + T(566, 134, 'Kì II', size=14, anchor='start'))
    b.append(T(360, 270, 'Học sinh giỏi kì II của hai lớp: 15 + 14 = 29', size=13, fill='#444'))
    return svg(720, 286, ''.join(b))


def dice(x, y, n, s=56):
    pos = {1: [(0.5, 0.5)], 2: [(0.25, 0.25), (0.75, 0.75)], 3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
           4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
           5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
           6: [(0.25, 0.22), (0.75, 0.22), (0.25, 0.5), (0.75, 0.5), (0.25, 0.78), (0.75, 0.78)]}
    out = [R(x, y, s, s, fill='#ffffff', stroke=INK, sw=2, rx=8)]
    for a, c in pos[n]:
        out.append(C(x + a * s, y + c * s, 5, fill=INK, stroke=INK, w=1))
    return ''.join(out)


def fig_ket_qua():
    b = [title(720, 'Các kết quả có thể')]
    b.append(T(130, 56, 'Tung một đồng xu: 2 kết quả', size=14, weight='bold'))
    for x, lab, name in ((70, 'S', 'Sấp'), (170, 'N', 'Ngửa')):
        b.append(C(x, 110, 34, fill='#f2cf5a', stroke=INK, w=2))
        b.append(T(x, 118, lab, size=24, weight='bold'))
        b.append(T(x, 168, name, size=13))
    b.append(T(500, 56, 'Gieo một con xúc xắc: 6 kết quả', size=14, weight='bold'))
    for i in range(6):
        b.append(dice(370 + (i % 3) * 80, 74 + (i // 3) * 76, i + 1))
    return svg(720, 230, ''.join(b))


def fig_xs_thuc_nghiem():
    b = [title(720, 'Xác suất thực nghiệm (ví dụ: tung đồng xu 50 lần)')]
    b.append(R(60, 70, 600 * 22 / 50, 50, fill=ORANGE, stroke=INK, sw=2))
    b.append(R(60 + 600 * 22 / 50, 70, 600 * 28 / 50, 50, fill='#cfe3f4', stroke=INK, sw=2))
    b.append(T(60 + 600 * 22 / 100, 101, 'Ngửa: 22 lần', size=15, weight='bold'))
    b.append(T(60 + 600 * 22 / 50 + 600 * 28 / 100, 101, 'Sấp: 28 lần', size=15, weight='bold'))
    b.append(PL([(60, 135), (60, 143), (660, 143), (660, 135)], w=1.5) + T(360, 165, 'Tổng số lần thực hiện: 50', size=14))
    b.append(T(360, 210, 'Xác suất thực nghiệm mặt ngửa = 22 : 50 = 0,44 = 44%', size=16, weight='bold'))
    return svg(720, 232, ''.join(b))


FIGS = {
    'c-t6-b1-tap-hop.svg': fig_tap_hop,
    'c-t6-b3-tia-so.svg': fig_tia_so,
    'c-t6-b11-ucln.svg': fig_ucln,
    'c-t6-b12-bcnn.svg': fig_bcnn,
    'c-t6-b13-truc-so.svg': fig_truc_so_nguyen,
    'c-t6-b14-cong-so-nguyen.svg': fig_cong_so_nguyen,
    'c-t6-b18-hinh-deu.svg': fig_tg_vuong_lucgiac,
    'c-t6-b19-tu-giac.svg': fig_tu_giac,
    'c-t6-b20-dien-tich.svg': fig_dien_tich,
    'c-t6-b21-truc-doi-xung.svg': fig_truc_doi_xung,
    'c-t6-b22-tam-doi-xung.svg': fig_tam_doi_xung,
    'c-t6-b23-ps-bang-nhau.svg': fig_phan_so_bang_nhau,
    'c-t6-b24-so-sanh.svg': fig_so_sanh_ps,
    'c-t6-b24-hon-so.svg': fig_hon_so,
    'c-t6-b28-thap-phan.svg': fig_thap_phan,
    'c-t6-b31-phan-tram.svg': fig_phan_tram,
    'c-t6-b32-diem-duong-thang.svg': fig_diem_duong_thang,
    'c-t6-b33-tia.svg': fig_tia,
    'c-t6-b34-doan-thang.svg': fig_doan_thang,
    'c-t6-b35-trung-diem.svg': fig_trung_diem,
    'c-t6-b36-goc.svg': fig_goc,
    'c-t6-b37-loai-goc.svg': fig_loai_goc,
    'c-t6-b37-thuoc-do.svg': fig_thuoc_do_goc,
    'c-t6-b39-bieu-do-tranh.svg': fig_bieu_do_tranh,
    'c-t6-b40-bieu-do-cot.svg': fig_bieu_do_cot,
    'c-t6-b41-cot-kep.svg': fig_bieu_do_cot_kep,
    'c-t6-b42-ket-qua.svg': fig_ket_qua,
    'c-t6-b43-xs-thuc-nghiem.svg': fig_xs_thuc_nghiem,
}

ATTACH = [
    ('tap1/chuong-1/bai-1/tap-hop.json', 2, 'c-t6-b1-tap-hop.svg', 'Tập hợp A và quan hệ thuộc, không thuộc.'),
    ('tap1/chuong-1/bai-3/thu-tu-so-tu-nhien.json', 0, 'c-t6-b3-tia-so.svg', 'Biểu diễn số tự nhiên trên tia số.'),
    ('tap1/chuong-2/bai-11/uoc-chung-ucln.json', 0, 'c-t6-b11-ucln.svg', 'Ước chung và ước chung lớn nhất của 12 và 18.'),
    ('tap1/chuong-2/bai-12/boi-chung-bcnn.json', 0, 'c-t6-b12-bcnn.svg', 'Bội chung và bội chung nhỏ nhất của 4 và 6.'),
    ('tap1/chuong-3/bai-13/tap-hop-so-nguyen.json', 2, 'c-t6-b13-truc-so.svg', 'Trục số và hai số đối nhau.'),
    ('tap1/chuong-3/bai-14/cong-tru-so-nguyen.json', 1, 'c-t6-b14-cong-so-nguyen.svg', 'Cộng số nguyên trên trục số.'),
    ('tap1/chuong-4/bai-18/tam-giac-deu-hinh-vuong-luc-giac.json', 2, 'c-t6-b18-hinh-deu.svg', 'Tam giác đều, hình vuông, lục giác đều.'),
    ('tap1/chuong-4/bai-19/hcn-thoi-binh-hanh-thang-can.json', 3, 'c-t6-b19-tu-giac.svg', 'Hình chữ nhật, hình thoi, hình bình hành, hình thang cân.'),
    ('tap1/chuong-4/bai-20/chu-vi-dien-tich-tu-giac.json', 4, 'c-t6-b20-dien-tich.svg', 'Công thức chu vi, diện tích một số tứ giác.'),
    ('tap1/chuong-5/bai-21/truc-doi-xung.json', 1, 'c-t6-b21-truc-doi-xung.svg', 'Trục đối xứng của một số hình.'),
    ('tap1/chuong-5/bai-22/tam-doi-xung.json', 1, 'c-t6-b22-tam-doi-xung.svg', 'Tâm đối xứng của một số hình.'),
    ('tap2/chuong-6/bai-23/mo-rong-phan-so.json', 1, 'c-t6-b23-ps-bang-nhau.svg', 'Các phân số bằng nhau biểu diễn cùng một phần của hình.'),
    ('tap2/chuong-6/bai-24/so-sanh-phan-so.json', 1, 'c-t6-b24-so-sanh.svg', 'So sánh hai phân số bằng cách quy đồng mẫu.'),
    ('tap2/chuong-6/bai-24/so-sanh-phan-so.json', 3, 'c-t6-b24-hon-so.svg', 'Hỗn số 2 1/3 bằng phân số 7/3.'),
    ('tap2/chuong-7/bai-28/so-thap-phan.json', 1, 'c-t6-b28-thap-phan.svg', 'Biểu diễn số thập phân.'),
    ('tap2/chuong-7/bai-31/ti-so-phan-tram.json', 1, 'c-t6-b31-phan-tram.svg', 'Tỉ số phần trăm minh họa trên lưới 100 ô.'),
    ('tap2/chuong-8/bai-32/diem-duong-thang.json', 3, 'c-t6-b32-diem-duong-thang.svg', 'Điểm, đường thẳng và vị trí của hai đường thẳng.'),
    ('tap2/chuong-8/bai-33/diem-nam-giua-tia.json', 2, 'c-t6-b33-tia.svg', 'Điểm nằm giữa, tia, hai tia đối nhau, hai tia trùng nhau.'),
    ('tap2/chuong-8/bai-34/doan-thang.json', 2, 'c-t6-b34-doan-thang.svg', 'M nằm giữa A và B thì AM + MB = AB.'),
    ('tap2/chuong-8/bai-35/trung-diem.json', 1, 'c-t6-b35-trung-diem.svg', 'M là trung điểm của đoạn thẳng AB.'),
    ('tap2/chuong-8/bai-36/goc.json', 2, 'c-t6-b36-goc.svg', 'Góc, góc bẹt và điểm nằm trong góc.'),
    ('tap2/chuong-8/bai-37/so-do-goc.json', 1, 'c-t6-b37-loai-goc.svg', 'Phân loại góc theo số đo.'),
    ('tap2/chuong-8/bai-37/so-do-goc.json', 2, 'c-t6-b37-thuoc-do.svg', 'Cách đo góc bằng thước đo góc.'),
    ('tap2/chuong-9/bai-39/bang-thong-ke-bieu-do-tranh.json', 2, 'c-t6-b39-bieu-do-tranh.svg', 'Biểu đồ tranh (số liệu minh họa).'),
    ('tap2/chuong-9/bai-40/bieu-do-cot.json', 2, 'c-t6-b40-bieu-do-cot.svg', 'Biểu đồ cột số học sinh thích các môn.'),
    ('tap2/chuong-9/bai-41/bieu-do-cot-kep.json', 2, 'c-t6-b41-cot-kep.svg', 'Biểu đồ cột kép số học sinh giỏi hai kì.'),
    ('tap2/chuong-9/bai-42/ket-qua-co-the-su-kien.json', 0, 'c-t6-b42-ket-qua.svg', 'Kết quả có thể khi tung đồng xu, gieo xúc xắc.'),
    ('tap2/chuong-9/bai-43/xac-suat-thuc-nghiem.json', 2, 'c-t6-b43-xs-thuc-nghiem.svg', 'Ví dụ tính xác suất thực nghiệm.'),
]

if __name__ == '__main__':
    write_figs(S, FIGS)
    for a in ATTACH:
        attach(S, *a)
    print('toan6: %d hình' % len(FIGS))
