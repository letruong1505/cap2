#!/usr/bin/env python3
# Hình minh họa lý thuyết Toán 9 (vẽ chính xác bằng toạ độ). Chạy: python3 tools/build-toan9-figures.py
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

S = 'toan9'
FILL = '#eaf1f8'


def H(x, y, s, size=16, anchor='middle', fill=INK, weight='bold'):
    """Chữ có viền trắng để không bị nét vẽ che."""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s" '
            'stroke="white" stroke-width="4" paint-order="stroke" stroke-linejoin="round">%s</text>'
            % (x, y, anchor, size, weight, fill, escape(s)))


def pt(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg)))


def ARC(cx, cy, r, a1, a2, stroke=INK, w=2, arrow=False, dash=None):
    """Cung từ góc a1 đến a2 (độ, ngược chiều kim đồng hồ trên màn hình)."""
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    span = (a2 - a1) % 360
    large = 1 if span > 180 else 0
    m = ' marker-end="url(#ar)"' if arrow else ''
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<path d="M%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
            % (x1, y1, r, r, large, x2, y2, stroke, w, m, d))


def SECTOR(cx, cy, r, a1, a2, fill, stroke=INK, w=2):
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    large = 1 if (a2 - a1) % 360 > 180 else 0
    return ('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"/>' % (cx, cy, x1, y1, r, r, large, x2, y2, fill, stroke, w))


def axes(ox, oy, s, x0, x1, y0, y1, tx=(), ty=(), size=13):
    o = [L(ox + x0 * s, oy, ox + x1 * s + 12, oy, w=1.8, arrow=True),
         L(ox, oy - y0 * s, ox, oy - y1 * s - 12, w=1.8, arrow=True),
         T(ox + x1 * s + 16, oy + 18, 'x', size=15, weight='bold', anchor='middle'),
         T(ox + 14, oy - y1 * s - 8, 'y', size=15, weight='bold', anchor='middle'),
         T(ox - 9, oy + 16, 'O', size=size)]
    for gx in tx:
        o.append(L(ox + gx * s, oy - 4, ox + gx * s, oy + 4, w=1.5))
        o.append(T(ox + gx * s, oy + 18, ('%g' % gx).replace('-', '−'), size=size))
    for gy in ty:
        o.append(L(ox - 4, oy - gy * s, ox + 4, oy - gy * s, w=1.5))
        o.append(T(ox - 9, oy - gy * s + 5, ('%g' % gy).replace('-', '−'), size=size, anchor='end'))
    return ''.join(o)


def card_text(x, y, lines, size=16, lh=26, fill=LGREY, w=270, pad=14):
    h = pad * 2 + lh * len(lines) - 6
    out = [R(x, y, w, h, fill=fill, stroke=GREY, sw=1.2, rx=8)]
    for i, s in enumerate(lines):
        out.append(T(x + pad, y + pad + 16 + i * lh, s, size=size, anchor='start'))
    return ''.join(out)


# ============================================================ Chương I
def fig_he_pt():
    ox, oy, s = 130, 240, 45
    P = lambda x, y: (ox + x * s, oy - y * s)
    b = [title(720, 'Nghiệm của hệ phương trình = giao điểm hai đường thẳng')]
    b.append(axes(ox, oy, s, -1, 5, -2, 4, tx=(1, 2, 3, 4), ty=(-1, 1, 2, 3)))
    a, c = P(-1, 4), P(4, -1)
    b.append(L(a[0], a[1], c[0], c[1], stroke=BLUE, w=2.6))
    d, e = P(-1, -2), P(5, 4)
    b.append(L(d[0], d[1], e[0], e[1], stroke=ORANGE, w=2.6))
    b.append(T(c[0] + 8, c[1] + 4, 'x + y = 3', size=15, anchor='start', fill=BLUE, weight='bold'))
    b.append(T(e[0] + 8, e[1] + 4, 'x − y = 1', size=15, anchor='start', fill=ORANGE, weight='bold'))
    m = P(2, 1)
    b.append(L(m[0], m[1], m[0], oy, dash='5 4', w=1.2, stroke=GREY))
    b.append(L(m[0], m[1], ox, m[1], dash='5 4', w=1.2, stroke=GREY))
    b.append(dot(m[0], m[1], 5, RED))
    b.append(H(m[0], m[1] - 14, 'M(2; 1)', size=15, fill=RED))
    b.append(card_text(430, 80, ['Hệ phương trình:', 'x + y = 3  và  x − y = 1', '',
                                 'Hai đường thẳng cắt nhau', 'tại M(2; 1) nên hệ có', 'nghiệm duy nhất (2; 1).',
                                 '', 'Thử lại: 2 + 1 = 3 ✓', '              2 − 1 = 1 ✓'], w=270))
    return svg(720, 350, ''.join(b))


def fig_he_pt_3_truong_hop():
    b = [title(720, 'Ba trường hợp của hệ hai phương trình bậc nhất hai ẩn')]
    s = 30
    cases = [
        (0, 'Cắt nhau', '1 nghiệm duy nhất',
         [((-0.5, 3.5), (3.5, -0.5), BLUE, 'x + y = 3'), ((0, -1), (3.5, 2.5), ORANGE, 'x − y = 1')]),
        (240, 'Song song', 'vô nghiệm',
         [((-0.5, 3.5), (3.5, -0.5), BLUE, 'x + y = 3'), ((-0.5, 1.5), (3, -2), ORANGE, 'x + y = 1')]),
        (480, 'Trùng nhau', 'vô số nghiệm',
         [((-0.5, 3.5), (3.5, -0.5), ORANGE, '2x + 2y = 6'), ((-0.5, 3.5), (3.5, -0.5), BLUE, 'x + y = 3')]),
    ]
    for px, name, res, lines in cases:
        ox, oy = px + 80, 140
        P = lambda x, y: (ox + x * s, oy - y * s)
        b.append(axes(ox, oy, s, -2, 4, -2, 3, size=11))
        for k, (p1, p2, col, lab) in enumerate(lines):
            a, c = P(*p1), P(*p2)
            wd = 6 if (name == 'Trùng nhau' and k == 0) else 2.6
            b.append(L(a[0], a[1], c[0], c[1], stroke=col, w=wd))
        b.append(T(px + 120, 232, name, size=17, weight='bold'))
        b.append(T(px + 120, 254, res, size=15))
        eq = ' ;  '.join(l[3] for l in lines)
        b.append(T(px + 120, 276, eq, size=13, fill=GREY))
        if name == 'Cắt nhau':
            m = P(2, 1)
            b.append(dot(m[0], m[1], 4.5, RED))
    return svg(720, 292, ''.join(b))


def fig_bpt():
    b = [title(720, 'Biểu diễn tập nghiệm của bất phương trình trên trục số')]
    X = lambda v: 90 + (v + 4) * 62
    for row, (y, txt, kind, v) in enumerate([(100, '3x − 6 > 0  ⇔  x > 2', 'open', 2),
                                             (200, '2x + 2 ≤ 0  ⇔  x ≤ −1', 'closed', -1)]):
        b.append(T(360, y - 40, txt, size=17, weight='bold'))
        b.append(L(X(-4) - 10, y, X(5) + 25, y, w=2, arrow=True))
        for k in range(-4, 6):
            b.append(L(X(k), y - 5, X(k), y + 5, w=1.5))
            b.append(T(X(k), y + 24, ('%d' % k).replace('-', '−'), size=14))
        if row == 0:
            b.append(L(X(v), y, X(5) + 22, y, stroke=BLUE, w=5, arrow=False))
            b.append(C(X(v), y, 7, fill='white', stroke=BLUE, w=3))
        else:
            b.append(L(X(-4) - 8, y, X(v), y, stroke=BLUE, w=5))
            b.append(C(X(v), y, 7, fill=BLUE, stroke=BLUE, w=3))
    b.append(T(360, 275, '○: không lấy giá trị đó (dấu > hoặc <);   ●: lấy giá trị đó (dấu ≥ hoặc ≤)', size=14, fill=GREY))
    return svg(720, 295, ''.join(b))


def fig_can_bac_hai():
    b = [title(720, 'Căn bậc hai của 9')]
    x0, y0, c = 50, 60, 44
    b.append(R(x0, y0, 3 * c, 3 * c, fill=LBLUE, stroke=INK, sw=2.4))
    for k in (1, 2):
        b.append(L(x0 + k * c, y0, x0 + k * c, y0 + 3 * c, w=1, stroke=GREY))
        b.append(L(x0, y0 + k * c, x0 + 3 * c, y0 + k * c, w=1, stroke=GREY))
    b.append(T(x0 + 1.5 * c, y0 - 8, 'cạnh x = 3', size=15))
    b.append(T(x0 + 1.5 * c, y0 + 1.5 * c + 8, 'S = 9', size=20, weight='bold'))
    b.append(T(x0 + 1.5 * c, y0 + 3 * c + 24, 'x² = 9 ⇒ x = 3', size=15))
    X = lambda v: 480 + v * 40
    y = 130
    b.append(L(X(-4.6), y, X(4.6), y, w=2, arrow=True))
    for k in range(-4, 5):
        b.append(L(X(k), y - 5, X(k), y + 5, w=1.5))
        b.append(T(X(k), y + 24, ('%d' % k).replace('-', '−'), size=14))
    for v, col in ((-3, RED), (3, BLUE), (0, INK)):
        b.append(dot(X(v), y, 6, col))
    b.append(T(X(3), y - 18, '√9 = 3', size=16, fill=BLUE, weight='bold'))
    b.append(T(X(-3), y - 18, '−√9 = −3', size=16, fill=RED, weight='bold'))
    b.append(T(480, y + 60, 'Số dương 9 có hai căn bậc hai: 3 và −3', size=15))
    b.append(T(480, y + 82, '(đối nhau, cách đều gốc O)', size=14, fill=GREY))
    return svg(720, 250, ''.join(b))


def fig_can_bac_ba():
    b = [title(720, 'Căn bậc ba của 27 và −8')]
    x, y, s, dx, dy = 70, 90, 120, 56, -44
    front = [(x, y + s), (x + s, y + s), (x + s, y), (x, y)]
    top = [(x, y), (x + s, y), (x + s + dx, y + dy), (x + dx, y + dy)]
    side = [(x + s, y + s), (x + s + dx, y + s + dy), (x + s + dx, y + dy), (x + s, y)]
    b.append(POLY(front, fill=LBLUE))
    b.append(POLY(top, fill='#c9dcee'))
    b.append(POLY(side, fill='#b7cfe6'))
    for k in (1, 2):
        b.append(L(x + k * s / 3, y, x + k * s / 3, y + s, w=1, stroke=GREY))
        b.append(L(x, y + k * s / 3, x + s, y + k * s / 3, w=1, stroke=GREY))
    b.append(T(x + s / 2, y + s + 22, 'cạnh x = 3', size=15))
    b.append(T(x + s / 2, y + s + 44, 'V = 3³ = 27', size=17, weight='bold'))
    b.append(T(x + s / 2, y + s + 66, '∛27 = 3', size=16, fill=BLUE, weight='bold'))
    # trục số
    X = lambda v: 520 + v * 48
    yy = 130
    b.append(L(X(-3.3), yy, X(3.3), yy, w=2, arrow=True))
    for k in range(-3, 4):
        b.append(L(X(k), yy - 5, X(k), yy + 5, w=1.5))
        b.append(T(X(k), yy + 24, ('%d' % k).replace('-', '−'), size=14))
    b.append(dot(X(-2), yy, 6, RED))
    b.append(dot(X(3), yy, 6, BLUE))
    b.append(H(X(-2), yy - 16, '∛(−8) = −2', size=15, fill=RED))
    b.append(H(X(3) - 10, yy - 16, '∛27 = 3', size=15, fill=BLUE))
    b.append(T(520, yy + 62, 'Mỗi số thực có đúng một căn bậc ba', size=15))
    b.append(T(520, yy + 84, 'Số âm → căn bậc ba âm;  số dương → dương', size=14, fill=GREY))
    return svg(720, 300, ''.join(b))


# ============================================================ Chương IV: tam giác vuông
def fig_luong_giac():
    B, C, A = (110, 250), (430, 250), (430, 10)
    b = [title(720, 'Tỉ số lượng giác của góc nhọn α')]
    B, C, A = (80, 300), (400, 300), (400, 60)
    b.append(POLY([B, C, A], fill=LBLUE, sw=2.4))
    b.append(right_angle(C[0], C[1], B[0], B[1], A[0], A[1], s=16))
    b.append(angle_arc(B[0], B[1], C[0], C[1], A[0], A[1], r=44, color=RED, w=2))
    b.append(T(B[0] + 66, B[1] - 8, 'α', size=20, fill=RED, weight='bold'))
    b.append(T(B[0] - 14, B[1] + 6, 'B', size=17, weight='bold', anchor='end'))
    b.append(T(C[0] + 12, C[1] + 6, 'C', size=17, weight='bold', anchor='start'))
    b.append(T(A[0] + 12, A[1] + 6, 'A', size=17, weight='bold', anchor='start'))
    b.append(H(222, 300 - 60 - 14, 'huyền', size=16, fill=GREEN))
    b.append(H(C[0] + 14, 180, 'đối', size=16, fill=ORANGE, anchor='start'))
    b.append(T(C[0] + 14, 199, '(đối diện α)', size=13, anchor='start', fill=GREY))
    b.append(H(240, C[1] + 26, 'kề α', size=16, fill=BLUE))
    b.append(card_text(480, 70, ['sin α = đối / huyền', 'cos α = kề / huyền', 'tan α = đối / kề', 'cot α = kề / đối',
                                 '', 'Ví dụ: đối 3, kề 4, huyền 5', 'sin α = 3/5,  cos α = 4/5', 'tan α = 3/4,  cot α = 4/3'], w=235,
                       size=15, lh=25))
    return svg(720, 345, ''.join(b))


def fig_goc_dac_biet():
    b = [title(720, 'Hai tam giác vuông đặc biệt')]
    k = 105
    # 30-60-90: cạnh ngắn 1, dài √3, huyền 2
    Bp = (60, 230)
    Cp = (60 + k * math.sqrt(3), 230)
    Ap = (Cp[0], 230 - k)
    b.append(POLY([Bp, Cp, Ap], fill=LBLUE, sw=2.4))
    b.append(right_angle(Cp[0], Cp[1], Bp[0], Bp[1], Ap[0], Ap[1], s=14))
    b.append(angle_arc(Bp[0], Bp[1], Cp[0], Cp[1], Ap[0], Ap[1], r=40, color=RED, w=1.8))
    b.append(H(Bp[0] + 62, Bp[1] - 6, '30°', size=15, fill=RED))
    b.append(angle_arc(Ap[0], Ap[1], Bp[0], Bp[1], Cp[0], Cp[1], r=26, color=RED, w=1.8))
    b.append(H(Ap[0] - 22, Ap[1] + 52, '60°', size=15, fill=RED))
    b.append(H((Bp[0] + Cp[0]) / 2, Bp[1] + 24, '√3', size=17))
    b.append(H(Cp[0] + 18, (Ap[1] + Cp[1]) / 2 + 5, '1', size=17, anchor='start'))
    b.append(H((Bp[0] + Ap[0]) / 2 - 12, (Bp[1] + Ap[1]) / 2 - 8, '2', size=17))
    b.append(T(Bp[0] + 120, 275, 'sin 30° = 1/2;  cos 30° = √3/2;  tan 30° = √3/3', size=14, fill=INK))
    b.append(T(Bp[0] + 120, 296, 'sin 60° = √3/2;  cos 60° = 1/2;  tan 60° = √3', size=14, fill=INK))
    # 45-45-90: hai cạnh góc vuông 1, huyền √2
    k2 = 150
    B2 = (440, 230)
    C2 = (440 + k2, 230)
    A2 = (C2[0], 230 - k2)
    b.append(POLY([B2, C2, A2], fill=LGREEN, sw=2.4))
    b.append(right_angle(C2[0], C2[1], B2[0], B2[1], A2[0], A2[1], s=14))
    b.append(angle_arc(B2[0], B2[1], C2[0], C2[1], A2[0], A2[1], r=40, color=RED, w=1.8))
    b.append(H(B2[0] + 64, B2[1] - 8, '45°', size=15, fill=RED))
    b.append(angle_arc(A2[0], A2[1], B2[0], B2[1], C2[0], C2[1], r=34, color=RED, w=1.8))
    b.append(H(A2[0] - 20, A2[1] + 52, '45°', size=15, fill=RED))
    b.append(H((B2[0] + C2[0]) / 2, B2[1] + 24, '1', size=17))
    b.append(H(C2[0] + 16, (A2[1] + C2[1]) / 2 + 5, '1', size=17, anchor='start'))
    b.append(H((B2[0] + A2[0]) / 2 - 14, (B2[1] + A2[1]) / 2 - 8, '√2', size=17))
    b.append(T(B2[0] + 90, 275, 'sin 45° = cos 45° = √2/2', size=14))
    b.append(T(B2[0] + 90, 296, 'tan 45° = 1', size=14))
    return svg(720, 312, ''.join(b))


def fig_he_thuc_canh_goc():
    A, B, C = (110, 280), (430, 280), (110, 40)
    b = [title(720, 'Hệ thức giữa cạnh và góc trong tam giác vuông')]
    b.append(POLY([A, B, C], fill=LBLUE, sw=2.4))
    b.append(right_angle(A[0], A[1], B[0], B[1], C[0], C[1], s=16))
    b.append(angle_arc(B[0], B[1], C[0], C[1], A[0], A[1], r=46, color=RED, w=2))
    b.append(H(B[0] - 62, B[1] - 8, 'B', size=16, fill=RED))
    b.append(angle_arc(C[0], C[1], A[0], A[1], B[0], B[1], r=34, color=RED, w=2))
    b.append(H(C[0] + 10, C[1] + 50, 'C', size=16, fill=RED))
    b.append(T(A[0] - 14, A[1] + 8, 'A', size=17, weight='bold', anchor='end'))
    b.append(T(B[0] + 12, B[1] + 6, 'B', size=17, weight='bold', anchor='start'))
    b.append(T(C[0] - 14, C[1] + 4, 'C', size=17, weight='bold', anchor='end'))
    b.append(H(A[0] - 18, 160, 'b', size=19, fill=ORANGE, anchor='end'))
    b.append(H(270, A[1] + 26, 'c', size=19, fill=BLUE))
    b.append(H(290, 148, 'a', size=19, fill=GREEN))
    b.append(card_text(500, 50, ['a: cạnh huyền BC', 'b = AC,  c = AB', '', 'b = a·sin B = a·cos C', 'c = a·sin C = a·cos B',
                                 'b = c·tan B = c·cot C', 'c = b·tan C = b·cot B'], w=210, size=14, lh=24))
    return svg(720, 320, ''.join(b))


# ============================================================ Chương V: đường tròn
def fig_duong_tron_co_ban():
    b = [title(720, 'Điểm với đường tròn; dây cung và đường kính')]
    cx, cy, r = 170, 150, 95
    b.append(C(cx, cy, r, fill=LBLUE, stroke=INK, w=2.4))
    b.append(dot(cx, cy, 4))
    b.append(T(cx - 10, cy + 20, 'O', size=16, weight='bold'))
    b.append(L(cx, cy, cx + r, cy, stroke=RED, w=2))
    b.append(H(cx + r / 2, cy - 7, 'R', size=15, fill=RED))
    m1 = (cx - 35, cy - 35)
    m3 = pt(cx, cy, r, 120)
    m2 = (cx + r + 55, cy - 60)
    b.append(dot(*m1, 4, GREEN)); b.append(H(m1[0] + 4, m1[1] - 9, 'M', size=15, fill=GREEN))
    b.append(dot(*m3, 4, BLUE)); b.append(H(m3[0] - 12, m3[1] - 6, 'N', size=15, fill=BLUE))
    b.append(dot(*m2, 4, ORANGE)); b.append(H(m2[0] + 4, m2[1] - 9, 'P', size=15, fill=ORANGE))
    b.append(T(cx, cy + r + 30, 'OM < R: M trong;  ON = R: N trên;  OP > R: P ngoài', size=13.5))
    cx2 = 540
    b.append(C(cx2, cy, r, fill=LBLUE, stroke=INK, w=2.4))
    b.append(dot(cx2, cy, 4))
    b.append(H(cx2 - 6, cy - 8, 'O', size=16, anchor='end'))
    a, bb = pt(cx2, cy, r, 180), pt(cx2, cy, r, 0)
    b.append(L(a[0], a[1], bb[0], bb[1], stroke=RED, w=2.6))
    c1, c2 = pt(cx2, cy, r, 125), pt(cx2, cy, r, 35)
    b.append(L(c1[0], c1[1], c2[0], c2[1], stroke=BLUE, w=2.6))
    b.append(T(a[0] - 10, a[1] + 5, 'A', size=15, weight='bold', anchor='end'))
    b.append(T(bb[0] + 10, bb[1] + 5, 'B', size=15, weight='bold', anchor='start'))
    b.append(T(c1[0] - 8, c1[1] - 6, 'C', size=15, weight='bold', anchor='end'))
    b.append(T(c2[0] + 8, c2[1] - 6, 'D', size=15, weight='bold', anchor='start'))
    b.append(H(cx2, cy + 34, 'đường kính AB = 2R', size=13.5, fill=RED))
    b.append(H(cx2, cy - r - 8, 'dây CD', size=13.5, fill=BLUE))
    b.append(T(cx2, cy + r + 30, 'Đường kính là dây lớn nhất', size=13.5))
    return svg(720, 310, ''.join(b))


def fig_cung_day():
    b = [title(720, 'Góc ở tâm – cung; đường kính vuông góc với dây')]
    cx, cy, r = 180, 160, 100
    A, B = pt(cx, cy, r, 0), pt(cx, cy, r, 70)
    b.append(C(cx, cy, r, fill='white', stroke=GREY, w=2))
    b.append(SECTOR(cx, cy, r, 0, 70, '#fbe3d0', stroke=INK, w=1.8))
    b.append(ARC(cx, cy, r, 0, 70, stroke=RED, w=5))
    b.append(ARC(cx, cy, r, 70, 360, stroke=BLUE, w=2.6))
    b.append(angle_arc(cx, cy, A[0], A[1], B[0], B[1], r=34, color=INK, w=1.8))
    b.append(H(cx + 56, cy - 14, '70°', size=15))
    b.append(dot(cx, cy, 4))
    b.append(T(cx - 6, cy + 20, 'O', size=16, weight='bold', anchor='end'))
    b.append(T(A[0] + 12, A[1] + 5, 'A', size=16, weight='bold', anchor='start'))
    b.append(T(B[0] + 10, B[1] - 8, 'B', size=16, weight='bold', anchor='start'))
    b.append(H(cx + 10, cy + r + 24, 'cung lớn AB = 360° − 70° = 290°', size=13.5, fill=BLUE))
    b.append(H(cx + r + 14, cy - 54, 'cung nhỏ AB = 70°', size=13.5, fill=RED, anchor='start'))
    cx2 = 520
    b.append(C(cx2, cy, r, fill=LBLUE, stroke=INK, w=2.4))
    Cc, Dd = (cx2, cy - r), (cx2, cy + r)
    h = cy - 40
    half = math.sqrt(r * r - 40 * 40)
    Am, Bm = (cx2 - half, h), (cx2 + half, h)
    b.append(L(Cc[0], Cc[1], Dd[0], Dd[1], stroke=RED, w=2.4))
    b.append(L(Am[0], Am[1], Bm[0], Bm[1], stroke=BLUE, w=2.6))
    b.append(dot(cx2, cy, 4))
    b.append(right_angle(cx2, h, cx2, cy, Bm[0], Bm[1], s=12))
    b.append(tick(Am[0], Am[1], cx2, h, 1, 7, GREEN))
    b.append(tick(cx2, h, Bm[0], Bm[1], 1, 7, GREEN))
    b.append(T(Am[0] - 8, Am[1] + 5, 'A', size=15, weight='bold', anchor='end'))
    b.append(T(Bm[0] + 8, Bm[1] + 5, 'B', size=15, weight='bold', anchor='start'))
    b.append(T(Cc[0], Cc[1] - 8, 'C', size=15, weight='bold'))
    b.append(T(Dd[0], Dd[1] + 20, 'D', size=15, weight='bold'))
    b.append(H(cx2 + 12, h + 22, 'H', size=15, anchor='start'))
    b.append(H(cx2 + 10, cy + 20, 'O', size=15, anchor='start'))
    b.append(T(cx2, cy + r + 40, 'CD ⊥ AB tại H ⇒ HA = HB', size=14))
    return svg(720, 320, ''.join(b))


def fig_cung_quat():
    b = [title(720, 'Hình quạt tròn và hình vành khuyên')]
    cx, cy, r = 170, 160, 100
    b.append(C(cx, cy, r, fill='white', stroke=GREY, w=2))
    b.append(SECTOR(cx, cy, r, 0, 60, '#fbe3d0', stroke=INK, w=2))
    b.append(ARC(cx, cy, r, 0, 60, stroke=RED, w=5))
    A, B = pt(cx, cy, r, 0), pt(cx, cy, r, 60)
    b.append(angle_arc(cx, cy, A[0], A[1], B[0], B[1], r=34, color=INK, w=1.8))
    b.append(H(cx + 52, cy - 14, 'n°', size=16))
    b.append(H(cx + r / 2, cy + 18, 'R', size=15, fill=BLUE))
    b.append(H(cx + 28, cy - 62, 'R', size=15, fill=BLUE))
    b.append(H(pt(cx, cy, r + 20, 30)[0] + 4, pt(cx, cy, r + 20, 30)[1], 'l', size=17, fill=RED, anchor='start'))
    b.append(dot(cx, cy, 4))
    b.append(T(cx - 8, cy + 20, 'O', size=16, weight='bold', anchor='end'))
    b.append(T(cx, cy + r + 40, 'l = πRn/180;   S quạt = πR²n/360', size=14))
    cx2, R_, r_ = 540, 100, 55
    d = ('M%.1f,%.1f a%d,%d 0 1,0 %d,0 a%d,%d 0 1,0 %d,0 Z M%.1f,%.1f a%d,%d 0 1,0 %d,0 a%d,%d 0 1,0 %d,0 Z'
         % (cx2 - R_, cy, R_, R_, 2 * R_, R_, R_, -2 * R_, cx2 - r_, cy, r_, r_, 2 * r_, r_, r_, -2 * r_))
    b.append('<path d="%s" fill-rule="evenodd" fill="%s" stroke="%s" stroke-width="2.4"/>' % (d, LBLUE, INK))
    b.append(dot(cx2, cy, 4))
    b.append(T(cx2 - 8, cy + 20, 'O', size=16, weight='bold', anchor='end'))
    p1, p2 = pt(cx2, cy, R_, 40), pt(cx2, cy, r_, 40)
    b.append(L(cx2, cy, p1[0], p1[1], stroke=BLUE, w=2))
    b.append(L(cx2, cy, pt(cx2, cy, r_, 140)[0], pt(cx2, cy, r_, 140)[1], stroke=RED, w=2))
    b.append(H(pt(cx2, cy, 80, 40)[0] + 6, pt(cx2, cy, 80, 40)[1] - 2, 'R', size=15, fill=BLUE, anchor='start'))
    b.append(H(pt(cx2, cy, 30, 140)[0] - 4, pt(cx2, cy, 30, 140)[1] - 4, 'r', size=15, fill=RED, anchor='end'))
    b.append(T(cx2, cy + R_ + 40, 'S = π(R² − r²)', size=14))
    return svg(720, 330, ''.join(b))


def fig_duong_thang_duong_tron():
    b = [title(720, 'Vị trí của đường thẳng a và đường tròn (O; R)')]
    r = 60
    cases = [(120, 35, 'd < R', 'cắt nhau: 2 điểm chung'),
             (360, 60, 'd = R', 'tiếp xúc: 1 điểm chung'),
             (600, 85, 'd > R', 'không giao nhau')]
    for cx, d, cap, sub in cases:
        cy = 100
        b.append(C(cx, cy, r, fill=LBLUE, stroke=INK, w=2.4))
        yl = cy + d
        b.append(L(cx - 100, yl, cx + 100, yl, stroke=BLUE, w=2.6))
        b.append(T(cx + 98, yl - 7, 'a', size=16, weight='bold', fill=BLUE, anchor='end'))
        b.append(dot(cx, cy, 4))
        b.append(T(cx - 8, cy - 8, 'O', size=15, weight='bold', anchor='end'))
        b.append(L(cx, cy, cx, yl, stroke=RED, w=2, dash='5 4'))
        b.append(H(cx + 6, cy + d / 2 + 5, 'd' if d != 60 else 'd = R', size=15, fill=RED, anchor='start'))
        b.append(right_angle(cx, yl, cx, cy, cx + 1, yl, s=10))
        b.append(dot(cx, yl, 3.5, RED))
        b.append(T(cx - 8, yl + 17, 'H', size=14, anchor='end'))
        if d == 35:
            h = math.sqrt(r * r - d * d)
            b.append(dot(cx - h, yl, 5, ORANGE)); b.append(dot(cx + h, yl, 5, ORANGE))
        if d == 60:
            b.append(dot(cx, yl, 5, ORANGE))
        b.append(T(cx, 226, cap, size=17, weight='bold'))
        b.append(T(cx, 248, sub, size=14))
    return svg(720, 262, ''.join(b))


def fig_tiep_tuyen():
    b = [title(720, 'Hai tiếp tuyến cắt nhau tại M')]
    O = (190, 160)
    Rr = 85
    D = 200
    th = math.degrees(math.acos(Rr / D))
    M = (O[0] + D, O[1])
    A, B = pt(O[0], O[1], Rr, th), pt(O[0], O[1], Rr, -th)
    b.append(C(O[0], O[1], Rr, fill=LBLUE, stroke=INK, w=2.4))
    b.append(L(M[0], M[1], A[0], A[1], stroke=BLUE, w=2.6))
    b.append(L(M[0], M[1], B[0], B[1], stroke=BLUE, w=2.6))
    b.append(L(O[0], O[1], A[0], A[1], stroke=RED, w=2))
    b.append(L(O[0], O[1], B[0], B[1], stroke=RED, w=2))
    b.append(L(O[0], O[1], M[0], M[1], stroke=GREY, w=1.6, dash='6 4'))
    b.append(right_angle(A[0], A[1], O[0], O[1], M[0], M[1], s=11))
    b.append(right_angle(B[0], B[1], O[0], O[1], M[0], M[1], s=11))
    b.append(tick(M[0], M[1], A[0], A[1], 1, 7, GREEN))
    b.append(tick(M[0], M[1], B[0], B[1], 1, 7, GREEN))
    b.append(angle_arc(M[0], M[1], A[0], A[1], O[0], O[1], r=40, color=ORANGE, w=2))
    b.append(angle_arc(M[0], M[1], O[0], O[1], B[0], B[1], r=40, color=ORANGE, w=2))
    b.append(angle_arc(O[0], O[1], A[0], A[1], M[0], M[1], r=32, color=ORANGE, w=2))
    b.append(angle_arc(O[0], O[1], M[0], M[1], B[0], B[1], r=32, color=ORANGE, w=2))
    b.append(dot(*O, 4)); b.append(dot(*M, 4)); b.append(dot(*A, 4)); b.append(dot(*B, 4))
    b.append(T(O[0] - 10, O[1] + 20, 'O', size=16, weight='bold', anchor='end'))
    b.append(T(M[0] + 12, M[1] + 5, 'M', size=16, weight='bold', anchor='start'))
    b.append(T(A[0] - 4, A[1] - 12, 'A', size=16, weight='bold'))
    b.append(T(B[0] - 4, B[1] + 22, 'B', size=16, weight='bold'))
    b.append(card_text(440, 70, ['MA, MB là hai tiếp tuyến:', '', 'MA ⊥ OA,  MB ⊥ OB', 'MA = MB',
                                 '∠AMO = ∠BMO', '∠AOM = ∠BOM'], w=250, size=15, lh=25))
    return svg(720, 300, ''.join(b))


def fig_hai_duong_tron():
    b = [title(720, 'Vị trí của hai đường tròn (O; R) và (O′; r),  d = OO′')]
    R_, r_ = 45, 28
    cases = [
        (0, 98, 'd > R + r', 'ở ngoài nhau'),
        (240, 73, 'd = R + r', 'tiếp xúc ngoài'),
        (480, 55, 'R − r < d < R + r', 'cắt nhau (2 điểm chung)'),
        (0, 17, 'd = R − r', 'tiếp xúc trong'),
        (240, 8, 'd < R − r', 'đựng nhau'),
        (480, 0, 'd = 0', 'đồng tâm'),
    ]
    for k, (px, d, cap, sub) in enumerate(cases):
        py = 80 if k < 3 else 240
        ox, oy = px + 70, py
        b.append(C(ox, oy, R_, fill=LBLUE, stroke=BLUE, w=2.4))
        b.append(C(ox + d, oy, r_, fill='#fde3c7', stroke=ORANGE, w=2.4))
        b.append(dot(ox, oy, 3.5))
        if d > 20:
            b.append(T(ox - 4, oy - 6, 'O', size=13, weight='bold', anchor='end'))
        elif d > 0:
            b.append(H(ox - 6, oy - 8, 'O', size=13, anchor='end'))
        else:
            b.append(H(ox, oy + 5 + 24, 'O ≡ O′', size=13))
        if d:
            b.append(L(ox, oy, ox + d, oy, stroke=INK, w=1.2, dash='4 3'))
            b.append(dot(ox + d, oy, 3.5))
            if d > 20:
                b.append(T(ox + d + 4, oy - 6, 'O′', size=13, weight='bold', anchor='start'))
            else:
                b.append(H(ox + d + 6, oy + 20, 'O′', size=13, anchor='start'))
        b.append(T(px + 120, py + 70, cap, size=14, weight='bold'))
        b.append(T(px + 120, py + 88, sub, size=13))
    return svg(720, 345, ''.join(b))


# ============================================================ Chương VI
def fig_parabol():
    b = [title(720, 'Đồ thị hàm số y = ax²  (parabol)')]
    s = 38
    for ox, oy, sgn, name, cap in ((190, 285, 1, 'y = x²', 'a > 0: parabol quay lên, nằm phía trên Ox'),
                                   (540, 70, -1, 'y = −x²', 'a < 0: parabol quay xuống, nằm phía dưới Ox')):
        ys = 6.6
        P = lambda x, y: (ox + x * s, oy - sgn * y * s)
        if sgn == 1:
            b.append(L(ox - 3 * s, oy, ox + 3 * s + 12, oy, w=1.8, arrow=True))
            b.append(L(ox, oy + 22, ox, oy - 6.8 * s, w=1.8, arrow=True))
            b.append(T(ox + 14, oy - 6.8 * s + 4, 'y', size=15, weight='bold'))
        else:
            b.append(L(ox - 3 * s, oy, ox + 3 * s + 12, oy, w=1.8, arrow=True))
            b.append(L(ox, oy + 6.8 * s, ox, oy - 26, w=1.8, arrow=True))
            b.append(T(ox + 14, oy - 22, 'y', size=15, weight='bold'))
        b.append(T(ox + 3 * s + 16, oy + (18 if sgn == 1 else -8), 'x', size=15, weight='bold'))
        b.append(T(ox - 9, oy + 16 if sgn == 1 else oy - 8, 'O', size=13))
        pts = [P(x / 20, (x / 20) ** 2) for x in range(-50, 51)]
        b.append(PL(pts, stroke=BLUE, w=3))
        for x in (-2, -1, 1, 2):
            p = P(x, x * x)
            b.append(dot(p[0], p[1], 4.5, RED))
            sg = '−' if x < 0 else ''
            lab = '(%s%d; %s%d)' % (sg, abs(x), '−' if sgn == -1 else '', x * x)
            b.append(H(p[0] + (-8 if x < 0 else 8), p[1] + (-8 if sgn == 1 else 18), lab, size=12.5,
                       fill=RED, anchor='end' if x < 0 else 'start'))
        b.append(L(ox, oy - sgn * 6.6 * s, ox, oy, stroke=GREY, w=1.2, dash='5 4'))
        b.append(H(ox + 112, oy - sgn * 5.2 * s, name, size=17, fill=BLUE, anchor='start'))
        b.append(T(ox, 350, cap, size=13.5))
    return svg(720, 365, ''.join(b))


def fig_delta():
    b = [title(720, 'Số nghiệm của ax² + bx + c = 0 và đồ thị y = ax² + bx + c  (a > 0)')]
    s = 30
    cases = [(0, -1, 'Δ > 0', '2 nghiệm phân biệt', 'parabol cắt Ox tại 2 điểm'),
             (240, 0, 'Δ = 0', 'nghiệm kép x₁ = x₂', 'parabol tiếp xúc Ox'),
             (480, 1, 'Δ < 0', 'vô nghiệm', 'parabol nằm trên Ox')]
    for px, k, cap, sub, sub2 in cases:
        ox, oy = px + 120, 215
        P = lambda x, y: (ox + x * s, oy - y * s)
        b.append(L(ox - 2.3 * s, oy, ox + 2.3 * s + 10, oy, w=1.8, arrow=True))
        b.append(L(ox, oy + 12, ox, oy - 5.4 * s, w=1.8, arrow=True))
        b.append(T(ox + 2.3 * s + 16, oy + 18, 'x', size=14, weight='bold'))
        b.append(T(ox + 14, oy - 5.4 * s + 2, 'y', size=14, weight='bold'))
        pts = [P(x / 20, (x / 20) ** 2 + k) for x in range(-40, 41)]
        b.append(PL(pts, stroke=BLUE, w=3))
        if k == -1:
            for xr in (-1, 1):
                p = P(xr, 0)
                b.append(dot(p[0], p[1], 5, RED))
            b.append(H(P(-1, 0)[0] - 4, oy + 20, 'x₁', size=14, fill=RED))
            b.append(H(P(1, 0)[0] + 4, oy + 20, 'x₂', size=14, fill=RED))
        if k == 0:
            p = P(0, 0)
            b.append(dot(p[0], p[1], 5, RED))
            b.append(H(p[0] + 20, oy + 20, 'x₁ = x₂', size=14, fill=RED))
        b.append(T(px + 120, 258, cap, size=17, weight='bold'))
        b.append(T(px + 120, 279, sub, size=14))
        b.append(T(px + 120, 298, sub2, size=13, fill=GREY))
    return svg(720, 312, ''.join(b))


def fig_viete():
    b = [title(720, 'Ví dụ: x² − 5x + 6 = 0')]
    ox, oy, s = 80, 285, 38
    P = lambda x, y: (ox + x * s, oy - y * s)
    b.append(axes(ox, oy, s, 0, 5.6, -1, 6.4, tx=(1, 2, 3, 4, 5), ty=(1, 2, 3, 4, 5, 6)))
    pts = [P(x / 20, (x / 20) ** 2 - 5 * (x / 20) + 6) for x in range(0, 101)]
    b.append(PL(pts, stroke=BLUE, w=3))
    for xr in (2, 3):
        p = P(xr, 0)
        b.append(dot(p[0], p[1], 5, RED))
    b.append(H(P(2, 0)[0] - 10, oy + 36, 'x₁ = 2', size=14, fill=RED))
    b.append(H(P(3, 0)[0] + 10, oy + 36, 'x₂ = 3', size=14, fill=RED))
    p = P(0, 6)
    b.append(dot(p[0], p[1], 5, GREEN))
    b.append(H(p[0] + 12, p[1] - 8, 'c = 6', size=14, fill=GREEN, anchor='start'))
    b.append(card_text(380, 70, ['a = 1,  b = −5,  c = 6', '', 'Tổng: x₁ + x₂ = 2 + 3 = 5',
                                 'và −b/a = 5  ✓', '', 'Tích: x₁·x₂ = 2·3 = 6',
                                 'và c/a = 6  ✓'], w=310, size=15, lh=25))
    return svg(720, 345, ''.join(b))


# ============================================================ Chương VII: thống kê
def fig_tan_so():
    b = [title(720, 'Biểu đồ tần số: điểm kiểm tra của 20 học sinh')]
    ox, oy, u = 90, 250, 24
    data = [(6, 3), (7, 5), (8, 7), (9, 4), (10, 1)]
    b.append(L(ox, oy, ox + 5 * 100 + 30, oy, w=1.8, arrow=True))
    b.append(L(ox, oy, ox, oy - 8.2 * u, w=1.8, arrow=True))
    b.append(T(ox + 12, oy - 8.2 * u + 6, 'Tần số', size=13, anchor='start'))
    b.append(T(ox + 5 * 100 + 36, oy + 18, 'Điểm', size=13, anchor='start'))
    for g in range(1, 8):
        b.append(L(ox - 4, oy - g * u, ox + 4, oy - g * u, w=1.4))
        b.append(T(ox - 10, oy - g * u + 5, str(g), size=12, anchor='end'))
    tops = []
    for k, (v, n) in enumerate(data):
        x = ox + 50 + k * 100
        b.append(R(x - 25, oy - n * u, 50, n * u, fill=LBLUE, stroke=BLUE, sw=2))
        b.append(T(x, oy + 20, str(v), size=14))
        b.append(T(x, oy - n * u - 6, str(n), size=14, weight='bold', fill=BLUE))
        tops.append((x, oy - n * u))
    b.append(PL(tops, stroke=ORANGE, w=2.4))
    for p in tops:
        b.append(dot(p[0], p[1], 4, ORANGE))
    b.append(T(ox + 280, 296, 'n = 3 + 5 + 7 + 4 + 1 = 20', size=14.5, weight='bold'))
    b.append(T(ox + 280, 318, 'x̄ = (6·3 + 7·5 + 8·7 + 9·4 + 10·1) : 20 = 155 : 20 = 7,75', size=14.5))
    return svg(720, 330, ''.join(b))


def fig_hinh_quat():
    b = [title(720, 'Biểu đồ hình quạt tròn: môn thể thao yêu thích')]
    cx, cy, r = 200, 165, 105
    data = [('Bóng đá', 40, '#8fb4d9'), ('Cầu lông', 30, '#f7c58a'), ('Bơi', 20, '#a8d5a0'), ('Khác', 10, '#e6a3a4')]
    a = 90.0
    for name, p, col in data:
        th = p * 3.6
        b.append(SECTOR_CW(cx, cy, r, a, a - th, col))
        mid = a - th / 2
        q = pt(cx, cy, r * 0.62, mid)
        b.append(T(q[0], q[1] + 5, '%d%%' % p, size=16, weight='bold'))
        a -= th
    y0 = 70
    b.append(T(434, y0, 'Môn', size=13, weight='bold', anchor='start'))
    b.append(T(546, y0, 'Tần số tương đối', size=13, weight='bold', anchor='middle'))
    b.append(T(636, y0, 'Góc ở tâm', size=13, weight='bold', anchor='start'))
    for k, (name, p, col) in enumerate(data):
        y = y0 + 32 + k * 34
        b.append(R(408, y - 14, 16, 16, fill=col, stroke=INK, sw=1))
        b.append(T(432, y, name, size=14, anchor='start'))
        b.append(T(546, y, '%d%%' % p, size=14, anchor='middle'))
        b.append(T(636, y, '%d°' % round(p * 3.6), size=14, anchor='start'))
    b.append(T(550, y0 + 32 + 4 * 34 + 10, 'Góc ở tâm = f · 360°;  tổng: 100% = 360°', size=13.5, weight='bold', anchor='middle'))
    return svg(720, 320, ''.join(b))


def SECTOR_CW(cx, cy, r, a1, a2, fill):
    """Hình quạt đi theo chiều kim đồng hồ từ góc a1 xuống a2 (a2 < a1)."""
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    large = 1 if (a1 - a2) > 180 else 0
    return ('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 %d 1 %.1f,%.1f Z" fill="%s" stroke="white" stroke-width="2.5" '
            'stroke-linejoin="round"/>' % (cx, cy, x1, y1, r, r, large, x2, y2, fill))


def fig_ghep_nhom():
    b = [title(720, 'Biểu đồ tần số ghép nhóm: chiều cao (cm) của 30 học sinh')]
    ox, oy, u, w = 170, 240, 14, 110
    groups = [(150, 155, 4), (155, 160, 9), (160, 165, 12), (165, 170, 5)]
    b.append(L(ox, oy, ox + 4 * w + 30, oy, w=1.8, arrow=True))
    b.append(L(ox, oy, ox, oy - 14.5 * u, w=1.8, arrow=True))
    b.append(T(ox + 10, oy - 14.5 * u + 4, 'Tần số', size=13, anchor='start'))
    for g in (4, 8, 12):
        b.append(L(ox - 4, oy - g * u, ox + 4, oy - g * u, w=1.4))
        b.append(T(ox - 9, oy - g * u + 5, str(g), size=12, anchor='end'))
        b.append(L(ox, oy - g * u, ox + 4 * w, oy - g * u, w=0.8, stroke='#dde3ea'))
    for k, (a, c, n) in enumerate(groups):
        x = ox + k * w
        b.append(R(x, oy - n * u, w, n * u, fill=LBLUE, stroke=BLUE, sw=2))
        b.append(T(x + w / 2, oy - n * u - 7, str(n), size=15, weight='bold', fill=BLUE))
    for k, v in enumerate((150, 155, 160, 165, 170)):
        b.append(T(ox + k * w, oy + 18, str(v), size=13))
    rows = [('Nhóm', ['[150; 155)', '[155; 160)', '[160; 165)', '[165; 170)']),
            ('Đại diện', ['152,5', '157,5', '162,5', '167,5']),
            ('Tần số tương đối', ['13,3%', '30%', '40%', '16,7%'])]
    for i, (lab, vals) in enumerate(rows):
        y = 280 + i * 22
        b.append(T(20, y, lab, size=12.5, anchor='start', weight='bold'))
        for k, v in enumerate(vals):
            b.append(T(ox + k * w + w / 2, y, v, size=13))
    return svg(720, 350, ''.join(b))


# ============================================================ Chương VIII: xác suất
def fig_cay_xs():
    b = [title(720, 'Sơ đồ cây: tung hai đồng xu (S: sấp, N: ngửa)')]
    root = (100, 150)
    l1 = {'S': (250, 80), 'N': (250, 220)}
    leaves = {('S', 'S'): (420, 45), ('S', 'N'): (420, 115), ('N', 'S'): (420, 185), ('N', 'N'): (420, 255)}
    for k, p in l1.items():
        b.append(L(root[0], root[1], p[0] - 14, p[1], w=2.2, stroke=BLUE))
        b.append(H((root[0] + p[0]) / 2 - 4, (root[1] + p[1]) / 2 + (-6 if k == 'S' else 18), k, size=15, fill=BLUE))
        b.append(C(p[0], p[1], 14, fill=LBLUE, stroke=BLUE, w=2))
        b.append(T(p[0], p[1] + 5, k, size=15, weight='bold'))
    for (a, c), p in leaves.items():
        s0 = l1[a]
        b.append(L(s0[0] + 14, s0[1], p[0] - 16, p[1], w=2.2, stroke=ORANGE))
        b.append(H((s0[0] + p[0]) / 2, (s0[1] + p[1]) / 2 + (-4 if c == 'S' else 16), c, size=15, fill=ORANGE))
        b.append(R(p[0] - 16, p[1] - 16, 56, 32, fill='#fde3c7', stroke=ORANGE, sw=2, rx=6))
        b.append(T(p[0] + 12, p[1] + 5, a + c, size=15, weight='bold'))
    b.append(dot(root[0], root[1], 5))
    b.append(T(root[0] - 10, root[1] + 5, 'Bắt đầu', size=13, anchor='end'))
    b.append(T(230, 16 + 0, '', size=1))
    b.append(T(250, 285, 'Lần 1', size=13, fill=GREY))
    b.append(T(420 + 12, 285, 'Lần 2 → kết quả', size=13, fill=GREY))
    b.append(card_text(500, 80, ['Ω = {SS; SN; NS; NN}', '', 'Không gian mẫu', 'có 4 phần tử.'], w=210, size=15, lh=26))
    return svg(720, 300, ''.join(b))


def fig_bang_xuc_xac():
    b = [title(720, 'Bảng kết quả khi gieo hai xúc xắc (ghi tổng số chấm)')]
    x0, y0, c = 130, 70, 38
    b.append(T(x0 + 3 * c, y0 - 12, 'Xúc xắc thứ hai', size=13, fill=GREY))
    b.append(T(20, y0 + 3 * c + 6, 'Xúc xắc', size=13, fill=GREY, anchor='start'))
    b.append(T(20, y0 + 3 * c + 24, 'thứ nhất', size=13, fill=GREY, anchor='start'))
    for j in range(1, 7):
        b.append(T(x0 + (j - 0.5) * c, y0 + 18, str(j), size=14, weight='bold'))
    for i in range(1, 7):
        b.append(T(x0 - 14, y0 + i * c + 20, str(i), size=14, weight='bold', anchor='end'))
    for i in range(1, 7):
        for j in range(1, 7):
            x = x0 + (j - 1) * c
            y = y0 + 6 + i * c - 6 + 0
            hit = (i + j == 7)
            b.append(R(x, y - 4 + 0, c, c, fill='#fde3c7' if hit else 'white', stroke=GREY, sw=1))
            b.append(T(x + c / 2, y + c / 2 + 1, str(i + j), size=14, weight='bold' if hit else 'normal',
                       fill=RED if hit else INK))
    b.append(card_text(430, 70, ['Ω có 6 × 6 = 36 kết quả.', '', 'A: “tổng bằng 7”', 'Kết quả thuận lợi: 6',
                                 '(1;6), (2;5), (3;4),', '(4;3), (5;2), (6;1)', '', 'P(A) = 6/36 = 1/6'], w=270,
                       size=15, lh=25))
    return svg(720, 345, ''.join(b))


# ============================================================ Chương IX: đường tròn
def inscribed_panel(cx, cy, r, pts_deg, labels, extra, caption, sub):
    out = [C(cx, cy, r, fill=LBLUE, stroke=INK, w=2.4)]
    P = {k: pt(cx, cy, r, d) for k, d in pts_deg.items()}
    out.append(extra(P, cx, cy))
    for k, p in P.items():
        dx, dy = p[0] - cx, p[1] - cy
        n = math.hypot(dx, dy)
        out.append(T(p[0] + dx / n * 14, p[1] + dy / n * 14 + 5, k, size=15, weight='bold'))
    out.append(T(cx, cy + r + 36, caption, size=13.5, weight='bold'))
    out.append(T(cx, cy + r + 56, sub, size=12.5, fill=GREY))
    return ''.join(out)


def fig_goc_noi_tiep():
    b = [title(720, 'Góc nội tiếp')]
    r, cy = 78, 135

    def p1(P, cx, cy):
        o = [L(*P['A'], *P['C'], w=2.2, stroke=BLUE), L(*P['B'], *P['C'], w=2.2, stroke=BLUE),
             L(cx, cy, *P['A'], w=1.8, stroke=RED), L(cx, cy, *P['B'], w=1.8, stroke=RED),
             ARC(cx, cy, r, 230, 310, stroke=ORANGE, w=4.5),
             angle_arc(cx, cy, P['A'][0], P['A'][1], P['B'][0], P['B'][1], r=20, color=RED, w=1.6),
             angle_arc(P['C'][0], P['C'][1], P['A'][0], P['A'][1], P['B'][0], P['B'][1], r=26, color=BLUE, w=1.8),
             dot(cx, cy, 3.5), H(cx, cy + 40, '80°', size=13, fill=RED),
             H(P['C'][0], P['C'][1] + 50, '40°', size=13, fill=BLUE)]
        return ''.join(o)

    def p2(P, cx, cy):
        o = [L(*P['A'], *P['C'], w=2, stroke=BLUE), L(*P['B'], *P['C'], w=2, stroke=BLUE),
             L(*P['A'], *P['D'], w=2, stroke=GREEN), L(*P['B'], *P['D'], w=2, stroke=GREEN),
             ARC(cx, cy, r, 200, 340, stroke=ORANGE, w=4.5),
             angle_arc(P['C'][0], P['C'][1], P['A'][0], P['A'][1], P['B'][0], P['B'][1], r=24, color=BLUE, w=1.8),
             angle_arc(P['D'][0], P['D'][1], P['A'][0], P['A'][1], P['B'][0], P['B'][1], r=20, color=GREEN, w=1.8)]
        return ''.join(o)

    def p3(P, cx, cy):
        o = [L(*P['A'], *P['B'], w=2.2, stroke=RED), L(*P['A'], *P['C'], w=2.2, stroke=BLUE),
             L(*P['B'], *P['C'], w=2.2, stroke=BLUE), right_angle(P['C'][0], P['C'][1], P['A'][0], P['A'][1], P['B'][0], P['B'][1], s=11),
             dot(cx, cy, 3.5), H(cx + 4, cy + 22, 'O', size=13, anchor='start')]
        return ''.join(o)

    b.append(inscribed_panel(120, cy, r, {'A': 230, 'B': 310, 'C': 90}, None, p1, 'Góc nội tiếp = ½ số đo cung chắn',
                             '(∠ACB = ½ ∠AOB)'))
    b.append(inscribed_panel(360, cy, r, {'A': 200, 'B': 340, 'C': 75, 'D': 120}, None, p2,
                             'Cùng chắn một cung: bằng nhau', '(∠ACB = ∠ADB)'))
    b.append(inscribed_panel(600, cy, r, {'A': 180, 'B': 0, 'C': 60}, None, p3, 'Chắn nửa đường tròn: 90°',
                             '(AB là đường kính ⇒ ∠ACB = 90°)'))
    return svg(720, 275, ''.join(b))


def circumcenter(A, B, C):
    ax, ay = A; bx, by = B; cx, cy = C
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy


def incenter(A, B, C):
    a = math.dist(B, C); b_ = math.dist(A, C); c = math.dist(A, B)
    s = a + b_ + c
    I = ((a * A[0] + b_ * B[0] + c * C[0]) / s, (a * A[1] + b_ * B[1] + c * C[1]) / s)
    area = abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])) / 2
    return I, 2 * area / s


def foot(P, A, B):
    ax, ay = A; bx, by = B
    dx, dy = bx - ax, by - ay
    t = ((P[0] - ax) * dx + (P[1] - ay) * dy) / (dx * dx + dy * dy)
    return (ax + t * dx, ay + t * dy)


def fig_ngoai_noi_tiep():
    b = [title(720, 'Đường tròn ngoại tiếp và đường tròn nội tiếp tam giác')]
    off = (0, 20)
    A, B, Cc = (170, 60), (70, 190), (270, 175)
    ox1, oy1 = 20, 20
    tri = [(p[0] + ox1, p[1] + oy1) for p in (A, B, Cc)]
    O = circumcenter(*tri)
    Rr = math.dist(O, tri[0])
    b.append(C(O[0], O[1], Rr, fill='none', stroke=BLUE, w=2.4))
    b.append(POLY(tri, fill=LBLUE, sw=2.4))
    for i in range(3):
        p, q = tri[i], tri[(i + 1) % 3]
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        b.append(L(mid[0], mid[1], O[0], O[1], stroke=RED, w=1.6, dash='5 4'))
        b.append(tick(p[0], p[1], mid[0], mid[1], 1, 6, GREEN))
        b.append(tick(mid[0], mid[1], q[0], q[1], 1, 6, GREEN))
        b.append(dot(*mid, 3, RED))
    b.append(dot(*O, 4.5, RED))
    b.append(H(O[0] + 8, O[1] + 18, 'O', size=15, fill=RED, anchor='start'))
    for n, p, dxy in (('A', tri[0], (0, -10)), ('B', tri[1], (-12, 16)), ('C', tri[2], (12, 16))):
        b.append(T(p[0] + dxy[0], p[1] + dxy[1], n, size=16, weight='bold'))
    b.append(T(190, 335, 'Ngoại tiếp: đi qua 3 đỉnh; tâm O là giao 3 đường trung trực', size=13.5, anchor='middle'))
    assert min(O[0] - Rr, O[1] - Rr) > 0 and O[0] + Rr < 360 and O[1] + Rr < 330, (O, Rr)
    # nội tiếp
    sh = 360
    tri2 = [(p[0] + sh + ox1, p[1] + oy1) for p in (A, B, Cc)]
    I, rr = incenter(*tri2)
    b.append(POLY(tri2, fill=LGREEN, sw=2.4))
    b.append(C(I[0], I[1], rr, fill='white', stroke=ORANGE, w=2.4))
    for p in tri2:
        b.append(L(p[0], p[1], I[0], I[1], stroke=RED, w=1.6, dash='5 4'))
    for i in range(3):
        p, q = tri2[i], tri2[(i + 1) % 3]
        f = foot(I, p, q)
        b.append(L(I[0], I[1], f[0], f[1], stroke=BLUE, w=1.6))
        b.append(dot(*f, 3, BLUE))
    b.append(dot(*I, 4.5, RED))
    b.append(H(I[0] + 6, I[1] - 8, 'I', size=15, fill=RED, anchor='start'))
    for n, p, dxy in (('A', tri2[0], (0, -10)), ('B', tri2[1], (-12, 16)), ('C', tri2[2], (12, 16))):
        b.append(T(p[0] + dxy[0], p[1] + dxy[1], n, size=16, weight='bold'))
    b.append(T(sh + 190, 335, 'Nội tiếp: tiếp xúc 3 cạnh; tâm I là giao 3 đường phân giác', size=13.5, anchor='middle'))
    return svg(720, 350, ''.join(b))


def fig_tam_giac_deu_rr():
    a = 200
    R_ = a / math.sqrt(3)
    r_ = a / (2 * math.sqrt(3))
    cx, cy = 190, 175
    b = [title(720, 'Tam giác đều cạnh a: R = 2r')]
    A = (cx, cy - R_)
    B = (cx - a / 2, cy + r_)
    Cc = (cx + a / 2, cy + r_)
    b.append(C(cx, cy, R_, fill='none', stroke=BLUE, w=2.4))
    b.append(POLY([A, B, Cc], fill=LBLUE, sw=2.4))
    b.append(C(cx, cy, r_, fill='white', stroke=ORANGE, w=2.4))
    Hh = (cx, cy + r_)
    b.append(L(cx, cy, A[0], A[1], stroke=BLUE, w=2.2))
    b.append(L(cx, cy, Hh[0], Hh[1], stroke=ORANGE, w=2.2))
    b.append(right_angle(Hh[0], Hh[1], cx, cy, Cc[0], Cc[1], s=10))
    b.append(dot(cx, cy, 4.5, RED))
    b.append(H(cx + 8, cy + 4, 'O', size=15, fill=RED, anchor='start'))
    b.append(H(cx - 8, (cy + A[1]) / 2 + 4, 'R', size=16, fill=BLUE, anchor='end'))
    b.append(H(cx + 8, (cy + Hh[1]) / 2 + 4, 'r', size=16, fill=ORANGE, anchor='start'))
    b.append(T(A[0], A[1] - 10, 'A', size=16, weight='bold'))
    b.append(T(B[0] - 12, B[1] + 16, 'B', size=16, weight='bold'))
    b.append(T(Cc[0] + 12, Cc[1] + 16, 'C', size=16, weight='bold'))
    b.append(T(Hh[0], Hh[1] + 20, 'H', size=15, weight='bold'))
    b.append(card_text(430, 80, ['O là trọng tâm, đồng thời là', 'tâm hai đường tròn.', '',
                                 'R = a√3/3', 'r = a√3/6', 'R = 2r  (OA = 2·OH)'], w=270, size=15, lh=26))
    return svg(720, 320, ''.join(b))


def fig_tu_giac_noi_tiep():
    b = [title(720, 'Tứ giác nội tiếp')]
    cx, cy, r = 150, 165, 100
    angs = {'A': 200, 'B': 270, 'C': 30, 'D': 110}
    P = {k: pt(cx, cy, r, d) for k, d in angs.items()}
    b.append(C(cx, cy, r, fill='none', stroke=GREY, w=2))
    b.append(POLY([P['A'], P['B'], P['C'], P['D']], fill=LBLUE, sw=2.4))
    want = {'A': 100, 'B': 85, 'C': 80, 'D': 95}
    order = ['A', 'B', 'C', 'D']
    for i, k in enumerate(order):
        pv, nx = P[order[i - 1]], P[order[(i + 1) % 4]]
        v = P[k]
        ang = math.degrees(math.acos(((pv[0] - v[0]) * (nx[0] - v[0]) + (pv[1] - v[1]) * (nx[1] - v[1])) /
                                     (math.dist(pv, v) * math.dist(nx, v))))
        assert abs(ang - want[k]) < 0.01, (k, ang)
        col = RED if k in 'AC' else GREEN
        b.append(angle_arc(v[0], v[1], pv[0], pv[1], nx[0], nx[1], r=22 if k != 'B' else 24, color=col, w=1.8))
        u1 = unit(v[0], v[1], pv[0], pv[1]); u2 = unit(v[0], v[1], nx[0], nx[1])
        bx, by = u1[0] + u2[0], u1[1] + u2[1]
        n = math.hypot(bx, by)
        b.append(H(v[0] + bx / n * 44, v[1] + by / n * 44 + 5, '%d°' % want[k], size=13, fill=col))
        dx, dy = v[0] - cx, v[1] - cy
        d = math.hypot(dx, dy)
        b.append(T(v[0] + dx / d * 14, v[1] + dy / d * 14 + 5, k, size=16, weight='bold'))
    b.append(T(cx, cy + r + 54, 'A + C = 100° + 80° = 180°;  B + D = 85° + 95° = 180°', size=12.5))
    b.append(T(cx, cy + r + 74, 'Tứ giác nội tiếp ⇒ tổng hai góc đối bằng 180°', size=12.5, weight='bold'))
    # hình chữ nhật
    cx2, cy2, r2 = 450, 150, 68
    rect = [pt(cx2, cy2, r2, a) for a in (40, 140, 220, 320)]
    b.append(C(cx2, cy2, r2, fill='none', stroke=GREY, w=2))
    b.append(POLY(rect, fill=LGREEN, sw=2.4))
    b.append(L(*rect[0], *rect[2], w=1.5, stroke=RED, dash='5 4'))
    b.append(L(*rect[1], *rect[3], w=1.5, stroke=RED, dash='5 4'))
    b.append(dot(cx2, cy2, 4, RED))
    b.append(H(cx2 + 4, cy2 + 18, 'O', size=14, fill=RED, anchor='start'))
    for n, p in zip('ABCD', (rect[1], rect[2], rect[3], rect[0])):
        pass
    b.append(T(cx2, cy2 + r2 + 32, 'Hình chữ nhật', size=14, weight='bold'))
    b.append(T(cx2, cy2 + r2 + 52, 'tâm O = giao hai đường chéo', size=12.5))
    # hình thang cân
    cx3, cy3, r3 = 615, 150, 68
    trap = [pt(cx3, cy3, r3, a) for a in (105, 210, 330, 75)]
    b.append(C(cx3, cy3, r3, fill='none', stroke=GREY, w=2))
    b.append(POLY(trap, fill=LYELLOW, sw=2.4))
    b.append(T(cx3, cy3 + r3 + 32, 'Hình thang cân', size=14, weight='bold'))
    b.append(T(cx3, cy3 + r3 + 52, 'cũng nội tiếp được', size=12.5))
    return svg(720, 360, ''.join(b))


def fig_da_giac_deu():
    b = [title(720, 'Đa giác đều: đường tròn ngoại tiếp, nội tiếp và phép quay')]
    r = 90
    panels = [(125, 5, 'Ngũ giác đều', 'góc trong = 3·180°/5 = 108°', 72),
              (360, 6, 'Lục giác đều', 'góc trong = 4·180°/6 = 120°', 60)]
    cy = 160
    for cx, n, name, sub, cen in panels:
        verts = regpoly(cx, cy, r, n)
        rin = r * math.cos(math.pi / n)
        b.append(C(cx, cy, r, fill='none', stroke=BLUE, w=2))
        b.append(POLY(verts, fill=LBLUE, sw=2.4))
        b.append(C(cx, cy, rin, fill='white', stroke=ORANGE, w=2))
        b.append(dot(cx, cy, 4, RED))
        b.append(H(cx + 6, cy + 18, 'O', size=14, fill=RED, anchor='start'))
        b.append(L(cx, cy, *verts[0], w=1.6, stroke=RED))
        b.append(L(cx, cy, *verts[1], w=1.6, stroke=RED))
        b.append(angle_arc(cx, cy, verts[0][0], verts[0][1], verts[1][0], verts[1][1], r=26, color=RED, w=1.8))
        mid = ((verts[0][0] + verts[1][0]) / 2, (verts[0][1] + verts[1][1]) / 2)
        ux, uy = mid[0] - cx, mid[1] - cy
        nn = math.hypot(ux, uy)
        b.append(H(cx + ux / nn * 44, cy + uy / nn * 44 + 5, '%d°' % cen, size=13, fill=RED))
        # góc trong tại đỉnh cuối
        v = verts[2 if n == 5 else 2]
        pv, nx = verts[1], verts[(3) % n]
        b.append(angle_arc(v[0], v[1], pv[0], pv[1], nx[0], nx[1], r=18, color=GREEN, w=1.8))
        b.append(T(cx, cy + r + 36, name, size=15, weight='bold'))
        b.append(T(cx, cy + r + 56, sub, size=13))
        b.append(T(cx, cy + r + 76, 'góc ở tâm = 360°/%d = %d°' % (n, cen), size=13, fill=GREY))
    # phép quay
    cx = 590
    verts = regpoly(cx, cy, r, 5)
    b.append(C(cx, cy, r, fill='none', stroke=GREY, w=1.6))
    b.append(POLY(verts, fill=LGREEN, sw=2.2))
    M, M2 = verts[0], verts[1]
    b.append(L(cx, cy, *M, w=1.8, stroke=BLUE))
    b.append(L(cx, cy, *M2, w=1.8, stroke=ORANGE))
    _a, _b = pt(cx, cy, 34, 90 - 6), pt(cx, cy, 34, 18 + 8)
    b.append('<path d="M%.1f,%.1f A34,34 0 0 1 %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6" marker-end="url(#ar)"/>' % (_a[0], _a[1], _b[0], _b[1], RED))
    b.append(dot(cx, cy, 4, RED))
    b.append(H(cx + 6, cy + 18, 'O', size=14, fill=RED, anchor='start'))
    b.append(T(M[0] + 4, M[1] - 10, 'M', size=15, weight='bold', fill=BLUE))
    b.append(T(M2[0] + 10, M2[1] - 8, "M′", size=15, weight='bold', fill=ORANGE))
    b.append(H(cx + 30, cy - 30, '72°', size=13, fill=RED, anchor='start'))
    b.append(T(cx, cy + r + 36, 'Phép quay tâm O, góc 72°', size=15, weight='bold'))
    b.append(T(cx, cy + r + 56, 'OM′ = OM, ∠MOM′ = 72°', size=13))
    b.append(T(cx, cy + r + 76, 'giữ nguyên ngũ giác đều', size=13, fill=GREY))
    return svg(720, 340, ''.join(b))


# ============================================================ Chương X: hình trụ, nón, cầu
def cyl(cx, top, bot, rx, ry, fill=LBLUE, stroke=INK):
    o = []
    o.append('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="2.2" '
             'stroke-linejoin="round"/>' % (cx - rx, top, cx - rx, bot, rx, ry, cx + rx, bot, cx + rx, top, fill, stroke))
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="2.2"/>'
             % (cx, top, rx, ry, '#d4e3f2', stroke))
    o.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>'
             % (cx - rx, bot, rx, ry, cx + rx, bot, stroke))
    return ''.join(o)


def cone(cx, apex, base, rx, ry, fill=LGREEN, stroke=INK):
    o = []
    o.append('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="2.2" '
             'stroke-linejoin="round"/>' % (cx, apex, cx - rx, base, rx, ry, cx + rx, base, fill, stroke))
    o.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>'
             % (cx - rx, base, rx, ry, cx + rx, base, stroke))
    return ''.join(o)


def fig_tru_non():
    b = [title(720, 'Hình trụ và hình nón')]
    cx, top, bot, rx, ry = 120, 70, 210, 65, 20
    b.append(cyl(cx, top, bot, rx, ry))
    b.append(L(cx, top, cx, bot, stroke=RED, w=1.8, dash='5 4'))
    b.append(L(cx, top, cx + rx, top, stroke=BLUE, w=2.2))
    b.append(dot(cx, top, 3.5)); b.append(dot(cx, bot, 3.5))
    b.append(H(cx + rx / 2, top - 7, 'r', size=15, fill=BLUE))
    b.append(H(cx - 8, (top + bot) / 2 + 5, 'h', size=16, fill=RED, anchor='end'))
    b.append(T(cx, bot + 50, 'Hình trụ', size=16, weight='bold'))
    cx2, apex, base, rx2, ry2 = 350, 50, 210, 75, 22
    b.append(cone(cx2, apex, base, rx2, ry2))
    b.append(L(cx2, apex, cx2, base, stroke=RED, w=1.8, dash='5 4'))
    b.append(L(cx2, base, cx2 + rx2, base, stroke=BLUE, w=2.2))
    b.append(dot(cx2, base, 3.5)); b.append(dot(cx2, apex, 3.5))
    b.append(H(cx2 + rx2 / 2, base - 7, 'r', size=15, fill=BLUE))
    b.append(H(cx2 - 8, (apex + base) / 2 + 5, 'h', size=16, fill=RED, anchor='end'))
    b.append(H(cx2 + rx2 / 2 + 10, (apex + base) / 2 - 4, 'l', size=16, fill=GREEN, anchor='start'))
    b.append(T(cx2, bot + 50, 'Hình nón', size=16, weight='bold'))
    b.append(card_text(480, 60, ['Hình trụ:', '  Sxq = 2πrh', '  V = πr²h', '',
                                 'Hình nón (l: đường sinh):', '  Sxq = πrl', '  V = ⅓πr²h', '  l² = r² + h²'], w=225, size=15, lh=25))
    return svg(720, 300, ''.join(b))


def fig_tao_hinh_tru_non():
    b = [title(720, 'Cách tạo ra hình trụ và hình nón')]
    # chữ nhật quay quanh cạnh trái
    ax = 50
    y0, y1, w = 70, 190, 65
    b.append(L(ax, y0 - 14, ax, y1 + 14, stroke=RED, w=1.8, dash='7 4'))
    b.append(R(ax, y0, w, y1 - y0, fill=LBLUE, stroke=INK, sw=2.2))
    b.append(H(ax + w / 2, y1 - 8, 'r', size=15, fill=BLUE))
    b.append(H(ax + w + 8, (y0 + y1) / 2 + 5, 'h', size=16, fill=RED, anchor='start'))
    b.append(L(ax + w + 38, 130, ax + w + 82, 130, w=2.4, arrow=True, stroke=BLUE))
    b.append(cyl(295, y0, y1, w, 20))
    b.append(T(170, 235, 'Quay hình chữ nhật', size=14, weight='bold'))
    b.append(T(170, 255, 'quanh một cạnh', size=14, weight='bold'))
    # tam giác vuông quay quanh cạnh góc vuông
    ax2 = 410
    b.append(L(ax2, 56, ax2, y1 + 14, stroke=RED, w=1.8, dash='7 4'))
    b.append(POLY([(ax2, 70), (ax2, y1), (ax2 + 70, y1)], fill=LGREEN, sw=2.2))
    b.append(right_angle(ax2, y1, ax2, 70, ax2 + 70, y1, s=11))
    b.append(H(ax2 + 35, y1 - 8, 'r', size=15, fill=BLUE))
    b.append(H(ax2 - 8, 135, 'h', size=16, fill=RED, anchor='end'))
    b.append(H(ax2 + 44, 118, 'l', size=16, fill=GREEN, anchor='start'))
    b.append(L(ax2 + 90, 130, ax2 + 134, 130, w=2.4, arrow=True, stroke=BLUE))
    b.append(cone(615, 70, y1, 70, 20))
    b.append(T(540, 235, 'Quay tam giác vuông quanh', size=14, weight='bold'))
    b.append(T(540, 255, 'một cạnh góc vuông', size=14, weight='bold'))
    return svg(720, 275, ''.join(b))


def fig_hinh_cau():
    b = [title(720, 'Hình cầu và mặt phẳng cắt hình cầu')]
    cx, cy, R_ = 170, 150, 100
    b.append(C(cx, cy, R_, fill='#e6eef7', stroke=INK, w=2.4))
    b.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f" fill="none" stroke="%s" stroke-width="2"/>'
             % (cx - R_, cy, R_, 30, cx + R_, cy, BLUE))
    b.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>'
             % (cx - R_, cy, R_, 30, cx + R_, cy, BLUE))
    b.append(L(cx, cy, cx + R_, cy, stroke=RED, w=2.2))
    b.append(dot(cx, cy, 4.5, RED))
    b.append(T(cx - 8, cy - 8, 'O', size=16, weight='bold', anchor='end'))
    b.append(H(cx + R_ / 2, cy - 7, 'R', size=16, fill=RED))
    b.append(T(cx, cy + R_ + 34, 'Hình cầu tâm O, bán kính R', size=14.5, weight='bold'))
    b.append(T(cx, cy + R_ + 54, 'S = 4πR²;   V = (4/3)πR³', size=14))
    cx2, d = 520, 50
    r_ = math.sqrt(R_ * R_ - d * d)
    b.append(C(cx2, cy, R_, fill='#e6eef7', stroke=INK, w=2.4))
    b.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 4"/>'
             % (cx2 - R_, cy, R_, 30, cx2 + R_, cy, GREY))
    oc = (cx2, cy - d)
    b.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fde3c7" fill-opacity="0.85" stroke="%s" stroke-width="2.2"/>'
             % (oc[0], oc[1], r_, 26, ORANGE))
    P = (cx2 + r_, cy - d)
    b.append(L(cx2, cy, oc[0], oc[1], stroke=RED, w=2, dash='5 4'))
    b.append(L(oc[0], oc[1], P[0], P[1], stroke=BLUE, w=2.2))
    b.append(L(cx2, cy, P[0], P[1], stroke=GREEN, w=2.2))
    b.append(right_angle(oc[0], oc[1], cx2, cy, P[0], P[1], s=10))
    b.append(dot(cx2, cy, 4, RED)); b.append(dot(*oc, 4, RED))
    b.append(T(cx2 - 8, cy + 18, 'O', size=15, weight='bold', anchor='end'))
    b.append(T(oc[0] - 8, oc[1] - 8, "O′", size=15, weight='bold', anchor='end'))
    b.append(H(cx2 + 8, cy - d / 2 + 5, 'd', size=15, fill=RED, anchor='start'))
    b.append(H(cx2 + r_ / 2, oc[1] - 8, 'r', size=15, fill=BLUE))
    b.append(H(cx2 + r_ / 2 + 8, cy - d / 2 + 22, 'R', size=15, fill=GREEN, anchor='start'))
    b.append(T(cx2, cy + R_ + 34, 'Mặt phẳng cắt hình cầu theo hình tròn', size=14.5, weight='bold'))
    b.append(T(cx2, cy + R_ + 54, 'R² = d² + r²;  qua tâm (d = 0): hình tròn lớn, r = R', size=13.5))
    return svg(720, 330, ''.join(b))


FIGS = {
    'c-t9-b1-he-pt.svg': fig_he_pt,
    'c-t9-b2-ba-truong-hop.svg': fig_he_pt_3_truong_hop,
    'c-t9-b6-bpt-truc-so.svg': fig_bpt,
    'c-t9-b7-can-bac-hai.svg': fig_can_bac_hai,
    'c-t9-b10-can-bac-ba.svg': fig_can_bac_ba,
    'c-t9-b11-luong-giac.svg': fig_luong_giac,
    'c-t9-b11-goc-dac-biet.svg': fig_goc_dac_biet,
    'c-t9-b12-he-thuc-canh-goc.svg': fig_he_thuc_canh_goc,
    'c-t9-b13-duong-tron.svg': fig_duong_tron_co_ban,
    'c-t9-b14-cung-day.svg': fig_cung_day,
    'c-t9-b15-quat-vanh-khuyen.svg': fig_cung_quat,
    'c-t9-b16-duong-thang-duong-tron.svg': fig_duong_thang_duong_tron,
    'c-t9-b16-tiep-tuyen.svg': fig_tiep_tuyen,
    'c-t9-b17-hai-duong-tron.svg': fig_hai_duong_tron,
    'c-t9-b18-parabol.svg': fig_parabol,
    'c-t9-b19-delta.svg': fig_delta,
    'c-t9-b20-viete.svg': fig_viete,
    'c-t9-b22-bieu-do-tan-so.svg': fig_tan_so,
    'c-t9-b23-hinh-quat.svg': fig_hinh_quat,
    'c-t9-b24-ghep-nhom.svg': fig_ghep_nhom,
    'c-t9-b25-so-do-cay.svg': fig_cay_xs,
    'c-t9-b26-bang-xuc-xac.svg': fig_bang_xuc_xac,
    'c-t9-b27-goc-noi-tiep.svg': fig_goc_noi_tiep,
    'c-t9-b28-ngoai-noi-tiep.svg': fig_ngoai_noi_tiep,
    'c-t9-b28-tam-giac-deu.svg': fig_tam_giac_deu_rr,
    'c-t9-b29-tu-giac-noi-tiep.svg': fig_tu_giac_noi_tiep,
    'c-t9-b30-da-giac-deu.svg': fig_da_giac_deu,
    'c-t9-b31-tru-non.svg': fig_tru_non,
    'c-t9-b31-tao-hinh.svg': fig_tao_hinh_tru_non,
    'c-t9-b32-hinh-cau.svg': fig_hinh_cau,
}

# (đường dẫn bài, chỉ số khối lý thuyết sau đó chèn hình — tính theo danh sách tại thời điểm chèn, tên hình, chú thích)
ATTACH = [
    ('tap1/chuong-1/bai-1/khai-niem-he-phuong-trinh.json', 3, 'c-t9-b1-he-pt.svg', 'Nghiệm của hệ là giao điểm của hai đường thẳng.'),
    ('tap1/chuong-1/bai-2/giai-he-phuong-trinh.json', 2, 'c-t9-b2-ba-truong-hop.svg', 'Hệ có 1 nghiệm, vô nghiệm hoặc vô số nghiệm.'),
    ('tap1/chuong-2/bai-6/bat-phuong-trinh-bac-nhat.json', 3, 'c-t9-b6-bpt-truc-so.svg', 'Tập nghiệm của bất phương trình biểu diễn trên trục số.'),
    ('tap1/chuong-3/bai-7/can-bac-hai.json', 0, 'c-t9-b7-can-bac-hai.svg', 'Căn bậc hai của 9 là 3 và −3.'),
    ('tap1/chuong-3/bai-10/can-bac-ba.json', 0, 'c-t9-b10-can-bac-ba.svg', 'Căn bậc ba của 27 và của −8.'),
    ('tap1/chuong-4/bai-11/ti-so-luong-giac.json', 1, 'c-t9-b11-luong-giac.svg', 'Cạnh đối, cạnh kề, cạnh huyền của góc nhọn α.'),
    ('tap1/chuong-4/bai-11/ti-so-luong-giac.json', 3, 'c-t9-b11-goc-dac-biet.svg', 'Tam giác vuông với các góc đặc biệt 30°, 60° và 45°.'),
    ('tap1/chuong-4/bai-12/he-thuc-canh-goc.json', 1, 'c-t9-b12-he-thuc-canh-goc.svg', 'Tam giác ABC vuông tại A.'),
    ('tap1/chuong-5/bai-13/mo-dau-duong-tron.json', 3, 'c-t9-b13-duong-tron.svg', 'Điểm với đường tròn; dây cung và đường kính.'),
    ('tap1/chuong-5/bai-14/cung-va-day.json', 2, 'c-t9-b14-cung-day.svg', 'Góc ở tâm, cung nhỏ, cung lớn; đường kính vuông góc với dây.'),
    ('tap1/chuong-5/bai-15/do-dai-cung-dien-tich-quat.json', 2, 'c-t9-b15-quat-vanh-khuyen.svg', 'Hình quạt tròn và hình vành khuyên.'),
    ('tap1/chuong-5/bai-16/vi-tri-duong-thang-duong-tron.json', 0, 'c-t9-b16-duong-thang-duong-tron.svg', 'Ba vị trí của đường thẳng và đường tròn.'),
    ('tap1/chuong-5/bai-16/vi-tri-duong-thang-duong-tron.json', 3, 'c-t9-b16-tiep-tuyen.svg', 'Tính chất hai tiếp tuyến cắt nhau.'),
    ('tap1/chuong-5/bai-17/vi-tri-hai-duong-tron.json', 3, 'c-t9-b17-hai-duong-tron.svg', 'Các vị trí tương đối của hai đường tròn.'),
    ('tap2/chuong-6/bai-18/ham-so-y-ax2.json', 1, 'c-t9-b18-parabol.svg', 'Đồ thị y = x² (a > 0) và y = −x² (a < 0).'),
    ('tap2/chuong-6/bai-19/phuong-trinh-bac-hai.json', 1, 'c-t9-b19-delta.svg', 'Dấu của Δ và số giao điểm của parabol với trục hoành.'),
    ('tap2/chuong-6/bai-20/dinh-li-viete.json', 1, 'c-t9-b20-viete.svg', 'Ví dụ x² − 5x + 6 = 0: S = 5, P = 6.'),
    ('tap2/chuong-7/bai-22/bang-tan-so.json', 2, 'c-t9-b22-bieu-do-tan-so.svg', 'Biểu đồ tần số dạng cột và dạng đoạn thẳng (số liệu minh họa).'),
    ('tap2/chuong-7/bai-23/tan-so-tuong-doi.json', 2, 'c-t9-b23-hinh-quat.svg', 'Biểu đồ hình quạt tròn (số liệu minh họa).'),
    ('tap2/chuong-7/bai-24/tan-so-ghep-nhom.json', 2, 'c-t9-b24-ghep-nhom.svg', 'Biểu đồ tần số ghép nhóm (số liệu minh họa).'),
    ('tap2/chuong-8/bai-25/phep-thu-khong-gian-mau.json', 2, 'c-t9-b25-so-do-cay.svg', 'Sơ đồ cây mô tả không gian mẫu khi tung hai đồng xu.'),
    ('tap2/chuong-8/bai-26/xac-suat-bien-co.json', 2, 'c-t9-b26-bang-xuc-xac.svg', 'Bảng kết quả khi gieo hai xúc xắc và biến cố “tổng bằng 7”.'),
    ('tap2/chuong-9/bai-27/goc-noi-tiep.json', 2, 'c-t9-b27-goc-noi-tiep.svg', 'Góc nội tiếp và các hệ quả.'),
    ('tap2/chuong-9/bai-28/duong-tron-ngoai-noi-tiep-tam-giac.json', 1, 'c-t9-b28-ngoai-noi-tiep.svg', 'Đường tròn ngoại tiếp và đường tròn nội tiếp tam giác.'),
    ('tap2/chuong-9/bai-28/duong-tron-ngoai-noi-tiep-tam-giac.json', 4, 'c-t9-b28-tam-giac-deu.svg', 'Tam giác đều: hai đường tròn đồng tâm, R = 2r.'),
    ('tap2/chuong-9/bai-29/tu-giac-noi-tiep.json', 2, 'c-t9-b29-tu-giac-noi-tiep.svg', 'Tứ giác nội tiếp, hình chữ nhật và hình thang cân nội tiếp.'),
    ('tap2/chuong-9/bai-30/da-giac-deu.json', 2, 'c-t9-b30-da-giac-deu.svg', 'Đa giác đều, đường tròn ngoại tiếp, nội tiếp và phép quay.'),
    ('tap2/chuong-10/bai-31/hinh-tru-hinh-non.json', 1, 'c-t9-b31-tru-non.svg', 'Hình trụ và hình nón.'),
    ('tap2/chuong-10/bai-31/hinh-tru-hinh-non.json', 3, 'c-t9-b31-tao-hinh.svg', 'Hình trụ, hình nón tạo bởi phép quay.'),
    ('tap2/chuong-10/bai-32/hinh-cau.json', 1, 'c-t9-b32-hinh-cau.svg', 'Hình cầu và mặt phẳng cắt hình cầu.'),
]

if __name__ == '__main__':
    write_figs(S, FIGS)
    for a in ATTACH:
        attach(S, *a)
    print('toan9: %d hình' % len(FIGS))
