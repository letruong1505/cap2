#!/usr/bin/env python3
# Sinh hình SVG minh họa cho bài tập Toán 7 tập 1 và gắn vào câu hỏi (trường "figure").
# Mỗi hình được vẽ từ đúng số liệu trong đề bài, chỉ hiện các dữ kiện đề đã cho, không lộ đáp án.
# Chạy: python3 tools/build-figures.py
# Ghi file vào content/toan7/figures/ và cập nhật trường "figure" trong các file bài.

import json
import math
import os
from collections import OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONTENT = os.path.join(ROOT, 'content', 'toan7')
FIG_DIR = os.path.join(CONTENT, 'figures')
PALETTE = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#76b7b2', '#b07aa1']
MINUS = '−'


def fmt(v):
    return ('%g' % v).replace('.', ',')


def P(p):
    return f'{p[0]:.1f},{p[1]:.1f}'


def add(p, v, s=1.0):
    return (p[0] + v[0] * s, p[1] + v[1] * s)


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def unit(v):
    n = math.hypot(v[0], v[1])
    return (v[0] / n, v[1] / n)


def dirv(deg):
    # Hướng theo góc toán học (ngược chiều kim đồng hồ, 0° là sang phải), đổi sang tọa độ màn hình (trục y hướng xuống).
    r = math.radians(deg)
    return (math.cos(r), -math.sin(r))


class Fig:
    def __init__(self):
        self.parts = []
        self.xs = []
        self.ys = []

    def pt(self, p):
        self.xs.append(p[0])
        self.ys.append(p[1])

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, anchor="middle", size=20, weight='normal', fill='#1d2733'):
        self.pt((x, y))
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{fill}">{s}</text>')

    def label(self, p, s, **kw):
        # Đặt nhãn lệch xuống 5px để căn giữa theo chiều dọc với điểm neo.
        self.text(p[0], p[1] + 5, s, **kw)

    def line(self, p, q, dash=False, color='#1d2733', width=2):
        self.pt(p)
        self.pt(q)
        d = ' stroke-dasharray="6 5"' if dash else ''
        self.add(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
                 f'stroke="{color}" stroke-width="{width}"{d}/>')

    def path(self, d, fill='none', stroke='#1d2733', width=1.5):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def dot(self, p, color='#1d2733'):
        self.pt(p)
        self.add(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="3.5" fill="{color}"/>')

    def svg(self, pad=40):
        x0 = min(self.xs) - pad
        x1 = max(self.xs) + pad
        y0 = min(self.ys) - pad
        y1 = max(self.ys) + pad
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" '
                f'font-family="Segoe UI, Arial, sans-serif">' + ''.join(self.parts) + '</svg>')


def rays(fig, origin, items, length=120):
    # items: danh sách (tên, góc toán học). Vẽ tia từ gốc và ghi tên ở đầu tia.
    for name, deg in items:
        d = dirv(deg)
        end = add(origin, d, length)
        fig.line(origin, end)
        fig.label(add(end, d, 16), name)


def arc(fig, origin, a_deg, b_deg, text, r=34, text_r=56):
    # Cung góc từ tia a đến tia b, ngược chiều kim đồng hồ (toán học), kèm nhãn ở giữa.
    span = (b_deg - a_deg) % 360
    pa = add(origin, dirv(a_deg), r)
    pb = add(origin, dirv(b_deg), r)
    large = 1 if span > 180 else 0
    fig.path(f'M{P(pa)} A{r} {r} 0 {large} 0 {P(pb)}', stroke='#1f4e79', width=1.5)
    mid = a_deg + span / 2
    fig.label(add(origin, dirv(mid), text_r), text)


def rightmark(fig, v, u, w, s=12):
    p1 = add(v, u, s)
    p2 = add(p1, w, s)
    p3 = add(v, w, s)
    fig.path(f'M{P(p1)} L{P(p2)} L{P(p3)}', stroke='#1d2733', width=1.2)


# ---------- Hình góc cơ bản (bài 8, 11) ----------

def fig_ke_bu(c_deg, label_right, label_left):
    fig = Fig()
    O = (200, 170)
    rays(fig, O, [('A', 180), ('B', 0), ('C', c_deg)])
    fig.dot(O)
    fig.label(add(O, (0, 1), 18), 'O')
    arc(fig, O, 0, c_deg, label_right)
    arc(fig, O, c_deg, 180, label_left)
    return fig.svg()


def fig_doi_dinh(theta, label_xy, label_opp):
    fig = Fig()
    O = (200, 170)
    rays(fig, O, [('x', 0), ("x'", 180), ('y', theta), ("y'", theta + 180)])
    fig.dot(O)
    fig.label(add(O, (0, 1), 18), 'O')
    arc(fig, O, 0, theta, label_xy)
    arc(fig, O, 180, theta + 180, label_opp)
    return fig.svg()


def fig_phan_giac(total, labels):
    # Tia Ox ở 0°, Oy ở total°, Oz ở giữa (phân giác khi bằng nửa).
    fig = Fig()
    O = (200, 170)
    z = total * labels.get('z_frac', 0.5)
    rays(fig, O, [('x', 0), ('y', total)])
    rays(fig, O, [('z', z)], length=90)
    fig.dot(O)
    fig.label(add(O, (0, 1), 18), 'O')
    arc(fig, O, 0, total, '', r=48, text_r=72)
    # Nhãn số đo cả góc đặt ngoài cùng, theo hướng giữa góc, tách khỏi tia Oz.
    fig.label(add(O, dirv(total / 2), 150), labels['total'])
    arc(fig, O, 0, z, labels['xz'], r=30, text_r=60)
    arc(fig, O, z, total, labels['zy'], r=30, text_r=60)
    return fig.svg()


# ---------- Hai đường thẳng cắt cát tuyến (bài 9, 10, 11) ----------

def fig_transversal(labels, slant=True, right=False):
    # Hai đường a, b song song (nằm ngang), đường c cắt cả hai.
    # Góc ở giao điểm A (trên) và B (dưới): UL, UR (phía trên đường), LL, LR (phía dưới đường).
    fig = Fig()
    if slant:
        P0, P1 = (150, 20), (260, 240)
    else:
        P0, P1 = (200, 20), (200, 240)

    def xat(y):
        return P0[0] + (y - P0[1]) * (P1[0] - P0[0]) / (P1[1] - P0[1])

    A = (xat(70), 70)
    B = (xat(190), 190)
    fig.line((40, 70), (330, 70))
    fig.line((40, 190), (330, 190))
    fig.label((24, 70), 'a', anchor='middle')
    fig.label((24, 190), 'b', anchor='middle')
    fig.line(P0, P1)
    fig.label((P0[0] + 14, P0[1] + 2), 'c', anchor='start')
    # Hướng đường c (theo toạ độ màn hình, y hướng xuống) và tâm của bốn miền quanh giao điểm.
    phi = math.degrees(math.atan2(P1[1] - P0[1], P1[0] - P0[0]))
    mids = {'LR': phi / 2, 'LL': (phi + 180) / 2, 'UL': (phi + 360) / 2, 'UR': (phi + 540) / 2}
    for key, txt in labels.items():
        side, pos = key.split('_')
        base = A if side == 'A' else B
        t = math.radians(mids[pos])
        # Khoảng cách tối thiểu để nhãn không chạm đường c (theo bề rộng ước lượng) và đường nằm ngang.
        half_w = (11 * len(txt) + 10) / 2
        need_c = (half_w + 8) / max(abs(math.sin(t - math.radians(phi))), 1e-6)
        need_h = 20 / max(abs(math.sin(t)), 1e-6)
        R = min(max(40, need_c, need_h), 130)
        fig.label((base[0] + R * math.cos(t), base[1] + R * math.sin(t)), txt)
    if right:
        rightmark(fig, A, (-1, 0), (0, 1))
        rightmark(fig, B, (-1, 0), (0, 1))
    return fig.svg()


# ---------- Tam giác ----------

def shape_from_angles(a_deg, b_deg, names=('A', 'B', 'C'), ox=0.0, oy=300.0, base=260.0):
    # Tam giác với góc tại đỉnh thứ nhất a_deg, đỉnh thứ hai b_deg; cạnh đầu nằm ngang.
    a = math.radians(a_deg)
    b = math.radians(b_deg)
    c = math.pi - a - b
    k = math.sin(b) / math.sin(c)  # độ dài cạnh thứ hai khi cạnh đầu bằng 1 (định lí sin)
    pts = [(0, 0), (1, 0), (k * math.cos(a), k * math.sin(a))]
    return {names[i]: (ox + x * base, oy - y * base) for i, (x, y) in enumerate(pts)}


def shape_from_sides(a, b, c, names=('A', 'B', 'C'), ox=0.0, oy=300.0, base=260.0):
    # a = BC, b = CA, c = AB; cạnh AB nằm ngang.
    s = base / c
    cos_a = (b * b + c * c - a * a) / (2 * b * c)
    ang = math.acos(cos_a)
    return {
        names[0]: (ox, oy),
        names[1]: (ox + c * s, oy),
        names[2]: (ox + b * s * math.cos(ang), oy - b * s * math.sin(ang)),
    }


def _edge_key(sides, x, y):
    if (x, y) in sides:
        return sides[(x, y)]
    if (y, x) in sides:
        return sides[(y, x)]
    return None


def draw_tri(fig, P_, names, interior=None, exterior=None, sides=None, ticks=(), right=None):
    n = names
    cen = (sum(P_[v][0] for v in n) / 3, sum(P_[v][1] for v in n) / 3)
    edges = [(n[0], n[1]), (n[1], n[2]), (n[2], n[0])]
    for x, y in edges:
        fig.line(P_[x], P_[y])
    for v in n:
        V = P_[v]
        fig.label(add(V, unit(sub(V, cen)), 22), v)
    for v, txt in (interior or {}).items():
        V = P_[v]
        fig.label(add(V, unit(sub(cen, V)), 46), txt)
    for v, (txt, other) in (exterior or {}).items():
        third = [x for x in n if x not in (v, other)][0]
        e = unit(sub(P_[v], P_[other]))
        u = unit(sub(P_[third], P_[v]))
        bis = unit((u[0] + e[0], u[1] + e[1]))
        fig.line(P_[v], add(P_[v], e, 70), dash=True)
        fig.label(add(P_[v], bis, 46), txt)
    for (x, y), txt in (sides or {}).items():
        mid = ((P_[x][0] + P_[y][0]) / 2, (P_[x][1] + P_[y][1]) / 2)
        out = unit(sub(mid, cen))
        fig.label(add(mid, out, 20), txt)
    for x, y in ticks:
        mid = ((P_[x][0] + P_[y][0]) / 2, (P_[x][1] + P_[y][1]) / 2)
        d = unit(sub(P_[y], P_[x]))
        perp = (-d[1], d[0])
        fig.line(add(mid, perp, -7), add(mid, perp, 7))
    if right:
        others = [x for x in n if x != right]
        V = P_[right]
        rightmark(fig, V, unit(sub(P_[others[0]], V)), unit(sub(P_[others[1]], V)))


def fig_tri(shape, names, interior=None, exterior=None, sides=None, ticks=(), right=None):
    fig = Fig()
    draw_tri(fig, shape, names, interior, exterior, sides, ticks, right)
    return fig.svg()


def fig_two_tri(shape1, names1, shape2, names2, kw1=None, kw2=None):
    fig = Fig()
    draw_tri(fig, shape1, names1, **(kw1 or {}))
    draw_tri(fig, shape2, names2, **(kw2 or {}))
    return fig.svg()


# ---------- Điểm và đường thẳng, số, hình vuông (bài 6, 7, 10, 16) ----------

def fig_point_line():
    fig = Fig()
    fig.line((40, 170), (320, 170))
    fig.label((334, 175), 'd', anchor='start')
    M = (180, 70)
    fig.dot(M)
    fig.label((M[0] + 14, M[1] - 2), 'M', anchor='start')
    return fig.svg()


def fig_square():
    fig = Fig()
    x0, y0, s = 120, 60, 160
    fig.line((x0, y0), (x0 + s, y0))
    fig.line((x0 + s, y0), (x0 + s, y0 + s))
    fig.line((x0 + s, y0 + s), (x0, y0 + s))
    fig.line((x0, y0 + s), (x0, y0))
    fig.label((x0 + s / 2, y0 + s + 24), '?')
    fig.label((x0 + s / 2, y0 + s / 2), 'S = 2,25 m²')
    return fig.svg()


def fig_number_line():
    fig = Fig()
    y = 150
    fig.line((60, y), (410, y))

    def X(v):
        return 100 + (v + 2) * 90

    for v in [-2, -1, 0, 1]:
        fig.line((X(v), y - 6), (X(v), y + 6))
        fig.label((X(v), y + 30), fmt(v).replace('-', MINUS))
    for v in [-1, 0]:
        fig.dot((X(v), y), '#1f4e79')
        fig.label((X(v), y - 20), fmt(v).replace('-', MINUS))
    return fig.svg()


def fig_perp_bisector():
    # AB = 12 cm (20 px/cm), MA = 7,5 cm, M nằm trên đường trung trực của AB.
    fig = Fig()
    A, B, H = (60, 160), (300, 160), (180, 160)
    M = (180, 70)
    fig.line(A, B)
    fig.line((180, 30), (180, 196), dash=True)
    fig.line(A, M)
    fig.line(B, M)
    rightmark(fig, H, (-1, 0), (0, -1))
    fig.dot(M)
    fig.label((M[0] + 14, M[1] - 4), 'M', anchor='start')
    fig.label((A[0] - 14, A[1] + 22), 'A', anchor='end')
    fig.label((B[0] + 14, B[1] + 22), 'B', anchor='start')
    fig.label((H[0] + 14, H[1] + 26), 'H', anchor='start')
    # Pháp tuyến ra ngoài cạnh AM: đẩy nhãn 7,5 cm ra khỏi tam giác.
    mx, my = (A[0] + M[0]) / 2, (A[1] + M[1]) / 2
    nx, ny = -(M[1] - A[1]), (M[0] - A[0])
    nl = math.hypot(nx, ny)
    fig.label((mx + 32 * nx / nl * -1, my + 32 * ny / nl * -1), '7,5 cm')
    fig.label(((B[0] + M[0]) / 2 + 26, (B[1] + M[1]) / 2 - 6), '?')
    fig.label((H[0] - 60, H[1] + 56), '12 cm')
    return fig.svg()


# ---------- Biểu đồ hình quạt (bài 18) ----------

def fig_pie(parts, inside):
    fig = Fig()
    cx, cy, r = 200, 190, 130
    fig.pt((cx - r * 1.6, cy - r * 1.4))
    fig.pt((cx + r * 1.6, cy + r * 1.4))
    a = 90.0
    for i, (name, pct) in enumerate(parts):
        span = pct * 3.6
        p0 = add((cx, cy), dirv(a), r)
        p1 = add((cx, cy), dirv(a - span), r)
        large = 1 if span > 180 else 0
        fig.path(f'M{cx:.1f},{cy:.1f} L{P(p0)} A{r} {r} 0 {large} 1 {P(p1)} Z',
                 fill=PALETTE[i % len(PALETTE)], stroke='#ffffff', width=2)
        mid = a - span / 2
        if name in inside:
            ip = add((cx, cy), dirv(mid), r * 0.6)
            fig.label(ip, inside[name], fill='#ffffff', weight='bold')
        op = add((cx, cy), dirv(mid), r * 1.12)
        c = math.cos(math.radians(mid))
        anchor = 'start' if c > 0.3 else ('end' if c < -0.3 else 'middle')
        fig.label(op, name, anchor=anchor)
        a -= span
    return fig.svg()


# ---------- Biểu đồ đoạn thẳng (bài 19) ----------

def fig_line_chart(xs, vals, ymax, ystep, show_values=True, ticks='all', grid=False, ylabel='cm', xlabel=''):
    fig = Fig()
    x0, y0, H = 70, 300, 230
    spacing = 130 if len(xs) > 1 else 0
    X = [x0 + 80 + i * spacing for i in range(len(xs))]
    xend = X[-1] + 60

    def Y(v):
        return y0 - v / ymax * H

    n_steps = int(round(ymax / ystep))
    for k in range(n_steps + 1):
        v = k * ystep
        yy = Y(v)
        if grid and k > 0:
            fig.line((x0, yy), (xend, yy), color='#dde3ea', width=1)
        fig.line((x0 - 5, yy), (x0, yy))
        show = ticks == 'all' or (ticks == 'zero' and k == 0)
        if show:
            fig.label((x0 - 18, yy), fmt(v), anchor='end', size=14)
    fig.line((x0, y0), (x0, Y(ymax)))
    fig.line((x0, y0), (xend, y0))
    fig.label((x0 - 10, Y(ymax) - 14), ylabel, anchor='middle', size=14)
    if xlabel:
        fig.label((xend, y0 + 44), xlabel, anchor='end', size=14)
    for i, lab in enumerate(xs):
        fig.label((X[i], y0 + 24), lab, size=15)
    for i in range(len(xs) - 1):
        if vals[i] is not None and vals[i + 1] is not None:
            fig.line((X[i], Y(vals[i])), (X[i + 1], Y(vals[i + 1])), color='#1f4e79', width=2.5)
    for i, v in enumerate(vals):
        if v is None:
            continue
        fig.dot((X[i], Y(v)), '#1f4e79')
        if show_values:
            fig.label((X[i], Y(v) - 14), fmt(v), size=15, weight='bold')
    return fig.svg()


# ---------- Danh sách hình: (file bài, mã câu, tên hình, nội dung SVG) ----------

def specs():
    S = []

    def add_fig(lesson, item_id, name, svg):
        S.append((lesson, item_id, name, svg))

    # Chương II
    add_fig('tap1/chuong-2/bai-6/vo-ti-can-bac-hai.json', 'q08', 'hinh-vuong-2-25', fig_square())
    add_fig('tap1/chuong-2/bai-7/tap-so-thuc.json', 'q04', 'truc-so-giua-1-0', fig_number_line())

    # Chương III
    L = 'tap1/chuong-3/bai-8/doi-dinh-ke-bu.json'
    add_fig(L, 'q01', 'ke-bu-70', fig_ke_bu(70, '70°', '?'))
    add_fig(L, 'q02', 'doi-dinh-38', fig_doi_dinh(38, '38°', '?'))
    add_fig(L, 'q04', 'phan-giac-84', fig_phan_giac(84, {'total': '84°', 'xz': '?', 'zy': '?'}))
    add_fig(L, 'q05', 'phan-giac-126', fig_phan_giac(126, {'total': '126°', 'xz': '?', 'zy': '?', 'z_frac': 84 / 126}))
    add_fig(L, 'q07', 'doi-dinh-58', fig_doi_dinh(58, '58°', '?'))

    L = 'tap1/chuong-3/bai-9/song-song-dau-hieu.json'
    add_fig(L, 'q01', 'so-le-65', fig_transversal({'A_LL': '65°', 'B_UR': '?'}))
    add_fig(L, 'q02', 'trong-cung-phia-118', fig_transversal({'A_LR': '118°', 'B_UR': '?'}))
    add_fig(L, 'q03', 'so-le-35', fig_transversal({'A_LL': '35°', 'B_UR': '?'}))
    add_fig(L, 'q04', 'trong-cung-phia-4x', fig_transversal({'A_LR': '4x', 'B_UR': '2x+30°'}))
    add_fig(L, 'q05', 'trong-cung-phia-3x', fig_transversal({'A_LR': '3x+10°', 'B_UR': '2x−10°'}))
    add_fig(L, 'q06', 'so-le-5x', fig_transversal({'A_LL': '5x−30°', 'B_UR': '2x+60°'}))

    L = 'tap1/chuong-3/bai-10/tien-de-euclid.json'
    add_fig(L, 'q01', 'diem-ngoai-duong-thang', fig_point_line())
    add_fig(L, 'q02', 'so-le-57-dong-vi', fig_transversal({'A_LL': '57°', 'B_LL': '?'}))
    add_fig(L, 'q03', 'trong-cung-phia-124', fig_transversal({'A_LR': '124°', 'B_UR': '?'}))
    add_fig(L, 'q04', 'so-le-5x-2x42', fig_transversal({'A_LL': '5x', 'B_UR': '2x+42°'}))
    add_fig(L, 'q05', 'dong-vi-110', fig_transversal({'A_LL': '110°', 'B_LL': '?'}))
    add_fig(L, 'q06', 'trong-cung-phia-4x-10', fig_transversal({'A_LR': '4x−10°', 'B_UR': '2x+10°'}))

    L = 'tap1/chuong-3/bai-11/dinh-li.json'
    add_fig(L, 'q01', 'ke-bu-135', fig_ke_bu(135, '135°', '?'))
    add_fig(L, 'q02', 'vuong-goc-song-song', fig_transversal({'A_LL': '90°', 'B_LL': '?'}, slant=False, right=True))
    add_fig(L, 'q03', 'so-le-64', fig_transversal({'A_LL': '64°', 'B_UR': '?'}))
    add_fig(L, 'q04', 'trong-cung-phia-2x', fig_transversal({'A_LR': '2x', 'B_UR': 'x+60°'}))
    add_fig(L, 'q05', 'dong-vi-3x', fig_transversal({'A_LL': '3x', 'B_LL': '6x−60°'}))

    # Chương IV
    L = 'tap1/chuong-4/bai-12/tong-goc-tam-giac.json'
    add_fig(L, 'q01', 'tam-giac-40-75', fig_tri(shape_from_angles(40, 75), 'ABC',
                                                interior={'A': '40°', 'B': '75°', 'C': '?'}))
    add_fig(L, 'q02', 'tam-giac-vuong-35', fig_tri(shape_from_angles(90, 35), 'ABC',
                                                   interior={'B': '35°', 'C': '?'}, right='A'))
    add_fig(L, 'q04', 'ngoai-130-tai-A', fig_tri(shape_from_angles(50, 50), 'ABC',
                                                 interior={'B': '50°', 'C': '?'},
                                                 exterior={'A': ('130°', 'B')}))
    add_fig(L, 'q05', 'ti-le-2x-3x-4x', fig_tri(shape_from_angles(40, 60), 'ABC',
                                                interior={'A': '2x°', 'B': '3x°', 'C': '4x°'}))
    add_fig(L, 'q06', 'ngoai-130-tai-B', fig_tri(shape_from_angles(70, 50), 'ABC',
                                                 interior={'A': '70°', 'C': '?'},
                                                 exterior={'B': ('130°', 'A')}))
    add_fig(L, 'q07', 'vuong-tai-A-B-2C', fig_tri(shape_from_angles(90, 60), 'ABC',
                                                  interior={'B': '?', 'C': '?'}, right='A'))

    L = 'tap1/chuong-4/bai-13/c-c-c.json'
    s1 = shape_from_sides(6, 5, 4, names=('A', 'B', 'C'))
    s2 = shape_from_sides(6, 5, 4, names=('D', 'E', 'F'), ox=330)
    add_fig(L, 'q01', 'ccc-4-6-5', fig_two_tri(
        s1, 'ABC', s2, 'DEF',
        dict(sides={('A', 'B'): '4', ('B', 'C'): '6', ('C', 'A'): '5'}),
        dict(sides={('D', 'E'): '?', ('E', 'F'): '?', ('F', 'D'): '?'})))
    add_fig(L, 'q02', 'cc-goc-70', fig_two_tri(
        shape_from_angles(70, 50, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(70, 50, names=('M', 'N', 'P'), ox=330), 'MNP',
        dict(interior={'A': '70°'}), dict(interior={'M': '?'})))
    s1 = shape_from_sides(8, 5, 6, names=('A', 'B', 'C'))
    s2 = shape_from_sides(8, 5, 6, names=('D', 'E', 'F'), ox=330)
    add_fig(L, 'q03', 'ccc-6-5-8', fig_two_tri(
        s1, 'ABC', s2, 'DEF',
        dict(sides={('A', 'B'): '6', ('C', 'A'): '5', ('B', 'C'): '?'}),
        dict(sides={('E', 'F'): '8'})))
    s1 = shape_from_sides(9, 7, 5, names=('A', 'B', 'C'))
    s2 = shape_from_sides(9, 7, 5, names=('D', 'E', 'F'), ox=330)
    add_fig(L, 'q04', 'ccc-5-9-7', fig_two_tri(
        s1, 'ABC', s2, 'DEF',
        dict(sides={('A', 'B'): '5', ('B', 'C'): '9', ('C', 'A'): '7'}),
        dict(sides={('D', 'E'): '?', ('E', 'F'): '?', ('F', 'D'): '?'})))
    add_fig(L, 'q05', 'goc-2x10-4x30', fig_two_tri(
        shape_from_angles(50, 60, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(50, 60, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'A': '2x+10°'}), dict(interior={'D': '4x−30°'})))
    s1 = shape_from_sides(9, 8, 11, names=('A', 'B', 'C'))
    s2 = shape_from_sides(9, 8, 11, names=('D', 'E', 'F'), ox=330)
    add_fig(L, 'q06', 'canh-2x1-x5', fig_two_tri(
        s1, 'ABC', s2, 'DEF',
        dict(sides={('A', 'B'): '2x−1 cm'}),
        dict(sides={('D', 'E'): 'x+5 cm'})))

    L = 'tap1/chuong-4/bai-14/c-g-c-g-c.json'
    add_fig(L, 'q01', 'cgc-bc-5', fig_two_tri(
        shape_from_sides(5, 6, 4, names=('A', 'B', 'C')), 'ABC',
        shape_from_sides(5, 6, 4, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(sides={('B', 'C'): '5'}), dict(sides={('E', 'F'): '?'})))
    add_fig(L, 'q02', 'goc-48', fig_two_tri(
        shape_from_angles(60, 48, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(60, 48, names=('M', 'N', 'P'), ox=330), 'MNP',
        dict(interior={'B': '48°'}), dict(interior={'N': '?'})))
    add_fig(L, 'q03', 'gcg-40-70', fig_two_tri(
        shape_from_angles(70, 40, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(70, 40, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': '40°', 'C': '70°'}), dict(interior={'E': '40°', 'F': '?'})))
    add_fig(L, 'q04', 'cgc-3x-1', fig_two_tri(
        shape_from_sides(6, 5, 4, names=('A', 'B', 'C')), 'ABC',
        shape_from_sides(6, 5, 4, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(sides={('A', 'B'): '3x−1'}), dict(sides={('D', 'E'): '2x+4'})))
    add_fig(L, 'q05', 'gcg-3x5', fig_two_tri(
        shape_from_angles(50, 65, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(50, 65, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': '3x+5°'}), dict(interior={'E': '2x+25°'})))

    L = 'tap1/chuong-4/bai-15/tam-giac-vuong.json'
    add_fig(L, 'q01', 'vuong-35', fig_tri(shape_from_angles(90, 35), 'ABC',
                                          interior={'B': '35°', 'C': '?'}, right='A'))
    add_fig(L, 'q02', 'vuong-30-def', fig_tri(shape_from_angles(90, 30, names=('D', 'E', 'F')), 'DEF',
                                               interior={'E': '30°', 'F': '?'}, right='D'))
    add_fig(L, 'q03', 'vuong-E-gap-F', fig_tri(shape_from_angles(90, 60, names=('D', 'E', 'F')), 'DEF',
                                               interior={'E': '?', 'F': '?'}, right='D'))
    add_fig(L, 'q04', 'vuong-can', fig_tri(shape_from_angles(90, 45), 'ABC',
                                           interior={'B': '?', 'C': '?'}, right='A',
                                           ticks=[('A', 'B'), ('A', 'C')]))
    add_fig(L, 'q05', 'hai-vuong-bang-nhau', fig_two_tri(
        shape_from_angles(90, 40, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(90, 40, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': '40°', 'C': '?'}, right='A'), dict(interior={'E': '?'}, right='D')))
    add_fig(L, 'q06', 'hai-vuong-65', fig_two_tri(
        shape_from_angles(90, 65, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(90, 65, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': '65°'}, right='A'), dict(interior={'E': '?'}, right='D')))

    L = 'tap1/chuong-4/bai-16/tam-giac-can-trung-truc.json'
    add_fig(L, 'q01', 'can-50', fig_tri(shape_from_angles(50, 65), 'ABC',
                                        interior={'A': '50°', 'B': '?', 'C': '?'},
                                        ticks=[('A', 'B'), ('A', 'C')]))
    add_fig(L, 'q02', 'deu', fig_tri(shape_from_angles(60, 60), 'ABC',
                                     interior={'A': '?', 'B': '?', 'C': '?'},
                                     ticks=[('A', 'B'), ('B', 'C'), ('C', 'A')]))
    add_fig(L, 'q03', 'can-72', fig_tri(shape_from_angles(36, 72), 'ABC',
                                        interior={'A': '?', 'B': '72°', 'C': '72°'},
                                        ticks=[('A', 'B'), ('A', 'C')]))
    add_fig(L, 'q04', 'can-b65', fig_tri(shape_from_angles(50, 65), 'ABC',
                                         interior={'A': '?', 'B': '65°', 'C': '?'},
                                         ticks=[('A', 'B'), ('A', 'C')]))
    add_fig(L, 'q05', 'can-2x1-3x4', fig_tri(shape_from_sides(8, 11, 11), 'ABC',
                                             sides={('A', 'B'): '2x+1 cm', ('A', 'C'): '3x−4 cm'},
                                             ticks=[('A', 'B'), ('A', 'C')]))
    add_fig(L, 'q06', 'can-ngoai-110', fig_tri(shape_from_angles(40, 70), 'ABC',
                                               interior={'A': '?', 'C': '?'},
                                               exterior={'B': ('110°', 'A')},
                                               ticks=[('A', 'B'), ('A', 'C')]))
    add_fig(L, 'q07', 'trung-truc-7-5', fig_perp_bisector())

    # Chương V
    L = 'tap1/chuong-5/bai-18/bieu-do-hinh-quat.json'
    add_fig(L, 'q05', 'quat-boi-loi', fig_pie(
        [('Bóng đá', 40), ('Bơi lội', 15), ('Cầu lông', 30), ('Bóng bàn', 15)],
        {'Bơi lội': '54°'}))
    add_fig(L, 'q06', 'quat-A-B-C', fig_pie(
        [('A', 45), ('B', 35), ('C', 20)],
        {'A': '45%', 'B': '35%'}))

    L = 'tap1/chuong-5/bai-19/bieu-do-doan-thang.json'
    add_fig(L, 'q01', 'doan-thang-ngay-5-6', fig_line_chart(['Ngày 5', 'Ngày 6'], [2.5, 4.0], 4.5, 0.5))
    add_fig(L, 'q02', 'doan-thang-7-9-gio', fig_line_chart(['7 giờ', '9 giờ'], [20, 25], 30, 5))
    add_fig(L, 'q03', 'doan-thang-ngay-1-3', fig_line_chart(['Ngày 1', 'Ngày 2', 'Ngày 3'],
                                                             [0.8, 1.3, 2.1], 2.5, 0.5, xlabel='Ngày'))
    add_fig(L, 'q05', 'doan-thang-6-12-gio', fig_line_chart(['6 giờ', '12 giờ'], [18, 30], 36, 6))
    add_fig(L, 'q06', 'o-vuong-diem', fig_line_chart(['Ngày 1'], [2.0], 4.0, 0.5, show_values=False,
                                                     ticks='zero', grid=True))
    return S



def fig_number_line_range(points=(), spans=()):
    # Trục số từ −3 đến 3; points: (giá trị, nhãn); spans: (v1, v2, nhãn khoảng cách).
    fig = Fig()
    y = 150

    def X(v):
        return 90 + (v + 3) * 60

    fig.line((60, y), (X(3) + 30, y))
    for v in range(-3, 4):
        fig.line((X(v), y - 6), (X(v), y + 6))
        fig.label((X(v), y + 30), str(v).replace('-', MINUS))
    for v, lab in points:
        fig.dot((X(v), y), '#1f4e79')
        fig.label((X(v), y - 22), lab)
    for v1, v2, lab in spans:
        fig.line((X(v1), y - 50), (X(v2), y - 50))
        fig.line((X(v1), y - 50), (X(v1), y - 40))
        fig.line((X(v2), y - 50), (X(v2), y - 40))
        fig.label(((X(v1) + X(v2)) / 2, y - 60), lab)
    return fig.svg()


def fig_square_plain(side, area):
    fig = Fig()
    x0, y0, s = 120, 60, 160
    fig.line((x0, y0), (x0 + s, y0))
    fig.line((x0 + s, y0), (x0 + s, y0 + s))
    fig.line((x0 + s, y0 + s), (x0, y0 + s))
    fig.line((x0, y0 + s), (x0, y0))
    fig.label((x0 + s / 2, y0 + s + 24), side)
    fig.label((x0 + s / 2, y0 + s / 2), area)
    return fig.svg()


def fig_bisector_plain():
    fig = Fig()
    A, B, H, M = (60, 160), (300, 160), (180, 160), (180, 70)
    fig.line(A, B)
    fig.line((180, 30), (180, 260), dash=True)
    fig.label((200, 40), 'd', anchor='start')
    fig.line(A, M)
    fig.line(B, M)
    rightmark(fig, H, (-1, 0), (0, -1))
    fig.dot(M)
    fig.label((M[0] + 14, M[1] - 4), 'M', anchor='start')
    fig.label((A[0] - 14, A[1] + 22), 'A', anchor='end')
    fig.label((B[0] + 14, B[1] + 22), 'B', anchor='start')
    fig.label((H[0] - 14, H[1] + 26), 'H', anchor='end')
    fig.label(((A[0] + M[0]) / 2 - 30, (A[1] + M[1]) / 2 - 8), 'MA')
    fig.label(((B[0] + M[0]) / 2 + 30, (B[1] + M[1]) / 2 - 8), 'MB')
    return fig.svg()


def fig_euclid():
    fig = Fig()
    fig.line((40, 170), (320, 170))
    fig.label((334, 175), 'd', anchor='start')
    fig.line((40, 60), (320, 60))
    fig.label((334, 65), 'd′', anchor='start')
    fig.dot((180, 60), '#1f4e79')
    fig.label((180, 40), 'M')
    return fig.svg()


def extra_specs():
    # Hình cho các câu còn thiếu.
    return [
        ('tap1/chuong-3/bai-8/doi-dinh-ke-bu.json', 'q03', 'ke-bu-2-7', fig_ke_bu(40, '2k', '7k')),
        ('tap1/chuong-3/bai-8/doi-dinh-ke-bu.json', 'q06', 'ke-bu-3x-x', fig_ke_bu(135, '3x', 'x')),
        ('tap1/chuong-4/bai-12/tong-goc-tam-giac.json', 'q03', 'tam-giac-2-3-4',
         fig_tri(shape_from_angles(40, 60), 'ABC', interior={'A': '2k', 'B': '3k', 'C': '4k'})),
    ]


def theory_specs():
    # (file bài, sau khối lý thuyết số, tên hình, SVG, chú thích)
    T = []
    def t(lesson, after, name, svg, cap):
        T.append((lesson, after, name, svg, cap))
    L = 'tap1/chuong-2/bai-6/vo-ti-can-bac-hai.json'
    t(L, 1, 'lt-hinh-vuong-can-a', fig_square_plain('a', 'S = a²'), 'Hình vuông cạnh a có diện tích a²; khi đó a = √S.')

    L = 'tap1/chuong-2/bai-7/tap-so-thuc.json'
    t(L, 3, 'lt-gia-tri-tuyet-doi', fig_number_line_range(
        points=[(-2, '−2'), (0, '0'), (2, '2')], spans=[(-2, 0, '2'), (0, 2, '2')]),
      '|−2| = 2 là khoảng cách từ −2 đến 0 trên trục số; |2| = 2 là khoảng cách từ 2 đến 0.')

    L = 'tap1/chuong-3/bai-8/doi-dinh-ke-bu.json'
    t(L, 0, 'lt-ke-bu', fig_ke_bu(70, 'α', 'β'), 'Hai góc kề bù: α + β = 180°.')
    t(L, 1, 'lt-doi-dinh', fig_doi_dinh(38, 'α', 'α'), 'Hai góc đối đỉnh: hai góc đều bằng α.')
    t(L, 2, 'lt-phan-giac', fig_phan_giac(80, {'total': '2α', 'xz': 'α', 'zy': 'α'}),
      'Oz là tia phân giác của góc xOy: góc xOz = góc zOy = α.')

    L = 'tap1/chuong-3/bai-9/song-song-dau-hieu.json'
    t(L, 0, 'lt-cap-goc', fig_transversal({'A_LL': '1', 'A_LR': '2', 'A_UL': '3', 'A_UR': '4',
                                          'B_LL': '5', 'B_LR': '6', 'B_UL': '7', 'B_UR': '8'}),
      '∠1 và ∠8 là cặp góc so le trong; ∠1 và ∠5 là cặp góc đồng vị; ∠2 và ∠8 là cặp góc trong cùng phía.')

    L = 'tap1/chuong-3/bai-10/tien-de-euclid.json'
    t(L, 0, 'lt-tien-de-euclid', fig_euclid(),
      'Qua điểm M nằm ngoài d, chỉ có một đường thẳng d′ đi qua M và song song với d.')
    t(L, 1, 'lt-tinh-chat-song-song', fig_transversal({'A_LL': 'α', 'B_LL': 'α', 'B_UR': 'α',
                                                     'A_LR': 'β'}),
      'Khi a ∥ b: các góc so le trong và đồng vị bằng nhau (cùng là α); hai góc trong cùng phía bù nhau (α + β = 180°).')

    L = 'tap1/chuong-3/bai-11/dinh-li.json'
    t(L, 2, 'lt-vuong-goc', fig_transversal({'A_LL': '90°', 'B_LL': '90°'}, slant=False, right=True),
      'Nếu a ∥ b và c ⊥ a thì c ⊥ b: cả hai góc tạo bởi c với a và b đều là góc vuông.')

    L = 'tap1/chuong-4/bai-12/tong-goc-tam-giac.json'
    t(L, 0, 'lt-tong-goc', fig_tri(shape_from_angles(50, 60), 'ABC',
                                  interior={'A': 'α', 'B': 'β', 'C': 'γ'}),
      'Tổng ba góc trong: α + β + γ = 180°.')
    t(L, 1, 'lt-goc-ngoai', fig_tri(shape_from_angles(50, 65), 'ABC',
                                   interior={'A': 'α', 'B': 'β'}, exterior={'C': ('γ′', 'B')}),
      'Góc ngoài tại C (γ′) bằng tổng hai góc trong không kề với C: γ′ = α + β.')

    L = 'tap1/chuong-4/bai-13/c-c-c.json'
    t(L, 1, 'lt-ccc', fig_two_tri(
        shape_from_sides(6, 5, 4, names=('A', 'B', 'C')), 'ABC',
        shape_from_sides(6, 5, 4, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(sides={('A', 'B'): 'c', ('B', 'C'): 'a', ('C', 'A'): 'b'}),
        dict(sides={('D', 'E'): 'c', ('E', 'F'): 'a', ('F', 'D'): 'b'})),
      'ΔABC và ΔDEF có ba cặp cạnh tương ứng bằng nhau: a = a′, b = b′, c = c′.')

    L = 'tap1/chuong-4/bai-14/c-g-c-g-c.json'
    t(L, 1, 'lt-cgc', fig_two_tri(
        shape_from_angles(50, 60, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(50, 60, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'A': 'α'}, ticks=[('A', 'B'), ('A', 'C')]),
        dict(interior={'D': 'α'}, ticks=[('D', 'E'), ('D', 'F')])),
      'Hai cạnh và góc xen giữa (α) bằng nhau thì hai tam giác bằng nhau (c.g.c).')
    t(L, 2, 'lt-gcg', fig_two_tri(
        shape_from_angles(50, 65, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(50, 65, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': 'β', 'C': 'γ'}, ticks=[('B', 'C')]),
        dict(interior={'E': 'β', 'F': 'γ'}, ticks=[('E', 'F')])),
      'Một cạnh và hai góc kề cạnh đó bằng nhau thì hai tam giác bằng nhau (g.c.g).')

    L = 'tap1/chuong-4/bai-15/tam-giac-vuong.json'
    t(L, 0, 'lt-tam-giac-vuong', fig_tri(shape_from_angles(90, 35), 'ABC',
                                        interior={'B': 'góc nhọn', 'C': 'góc nhọn'},
                                        sides={('B', 'C'): 'cạnh huyền'}, right='A'),
      'Tam giác vuông: hai góc nhọn phụ nhau; cạnh đối diện góc vuông là cạnh huyền.')

    L = 'tap1/chuong-4/bai-16/tam-giac-can-trung-truc.json'
    t(L, 0, 'lt-tam-giac-can', fig_tri(shape_from_angles(40, 70), 'ABC',
                                     interior={'B': 'góc đáy', 'C': 'góc đáy'},
                                     sides={('A', 'B'): 'cạnh bên', ('A', 'C'): 'cạnh bên', ('B', 'C'): 'cạnh đáy'},
                                     ticks=[('A', 'B'), ('A', 'C')]),
      'Tam giác cân tại A: hai cạnh bên bằng nhau và hai góc đáy bằng nhau.')
    t(L, 1, 'lt-tam-giac-deu', fig_tri(shape_from_angles(60, 60), 'ABC',
                                     interior={'A': '60°', 'B': '60°', 'C': '60°'},
                                     ticks=[('A', 'B'), ('B', 'C'), ('C', 'A')]),
      'Tam giác đều: ba cạnh bằng nhau và ba góc bằng 60°.')
    t(L, 2, 'lt-trung-truc', fig_bisector_plain(),
      'Đường trung trực d của AB đi qua trung điểm H và vuông góc với AB; mọi điểm M trên d đều cách đều A và B.')

    L = 'tap1/chuong-5/bai-18/bieu-do-hinh-quat.json'
    t(L, 1, 'lt-quat', fig_pie([('Môn A', 25), ('Môn B', 25), ('Môn C', 30), ('Môn D', 20)],
                              {'Môn A': '25%', 'Môn B': '25%', 'Môn C': '30%', 'Môn D': '20%'}),
      'Cả hình tròn ứng với 100%; tổng các phần trăm bằng 100%.')

    L = 'tap1/chuong-5/bai-19/bieu-do-doan-thang.json'
    t(L, 1, 'lt-doan-thang', fig_line_chart(['Ngày 1', 'Ngày 2', 'Ngày 3', 'Ngày 4'],
                                           [1.0, 1.8, 2.2, 3.0], 3.5, 0.5, xlabel='Ngày'),
      'Biểu đồ đoạn thẳng: đoạn nối các điểm cho thấy xu thế tăng của đại lượng theo thời gian.')
    return T


def example_specs():
    # (file bài, chỉ số ví dụ, tên hình, SVG)
    E = []
    def e(lesson, idx, name, svg):
        E.append((lesson, idx, name, svg))
    L = 'tap1/chuong-3/bai-8/doi-dinh-ke-bu.json'
    e(L, 0, 'vd-ke-bu-115', fig_ke_bu(65, '115°', '?'))
    e(L, 1, 'vd-phan-giac-76', fig_phan_giac(76, {'total': '76°', 'xz': '?', 'zy': '?'}))
    L = 'tap1/chuong-3/bai-9/song-song-dau-hieu.json'
    e(L, 0, 'vd-trong-cung-phia-110', fig_transversal({'A_LR': '110°', 'B_UR': '?'}))
    e(L, 1, 'vd-dong-vi-52', fig_transversal({'A_LL': '52°', 'B_LL': '?'}))
    L = 'tap1/chuong-3/bai-10/tien-de-euclid.json'
    e(L, 0, 'vd-so-le-62', fig_transversal({'A_LL': '62°', 'B_UR': '?'}))
    e(L, 1, 'vd-trong-cung-phia-102', fig_transversal({'A_LR': '102°', 'B_UR': '?'}))
    L = 'tap1/chuong-3/bai-11/dinh-li.json'
    e(L, 0, 'ke-bu-135', fig_ke_bu(135, '135°', '?'))
    e(L, 1, 'vuong-goc-song-song', fig_transversal({'A_LL': '90°', 'B_LL': '?'}, slant=False, right=True))
    L = 'tap1/chuong-4/bai-12/tong-goc-tam-giac.json'
    e(L, 0, 'vd-tam-giac-50-60', fig_tri(shape_from_angles(50, 60), 'ABC',
                                         interior={'A': '50°', 'B': '60°', 'C': '?'}))
    e(L, 1, 'vd-ngoai-120', fig_tri(shape_from_angles(55, 65), 'ABC',
                                   interior={'A': '55°', 'B': '?'}, exterior={'C': ('120°', 'B')}))
    L = 'tap1/chuong-4/bai-13/c-c-c.json'
    e(L, 0, 'ccc-6-5-8', fig_two_tri(
        shape_from_sides(8, 5, 6, names=('A', 'B', 'C')), 'ABC',
        shape_from_sides(8, 5, 6, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(sides={('A', 'B'): '6', ('C', 'A'): '5', ('B', 'C'): '?'}),
        dict(sides={('E', 'F'): '8'})))
    e(L, 1, 'ccc-4-6-5', fig_two_tri(
        shape_from_sides(6, 5, 4, names=('A', 'B', 'C')), 'ABC',
        shape_from_sides(6, 5, 4, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(sides={('A', 'B'): '4', ('B', 'C'): '6', ('C', 'A'): '5'}),
        dict(sides={('D', 'E'): '?', ('E', 'F'): '?', ('F', 'D'): '?'})))
    L = 'tap1/chuong-4/bai-14/c-g-c-g-c.json'
    e(L, 0, 'vd-cgc-b60', fig_two_tri(
        shape_from_angles(60, 60, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(60, 60, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': '60°'}), dict(interior={'E': '?'})))
    e(L, 1, 'cgc-bc-5', fig_two_tri(
        shape_from_sides(5, 6, 4, names=('A', 'B', 'C')), 'ABC',
        shape_from_sides(5, 6, 4, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(sides={('B', 'C'): '5'}), dict(sides={('E', 'F'): '?'})))
    L = 'tap1/chuong-4/bai-15/tam-giac-vuong.json'
    e(L, 0, 'vd-vuong-38', fig_tri(shape_from_angles(90, 38), 'ABC',
                                  interior={'B': '38°', 'C': '?'}, right='A'))
    e(L, 1, 'hai-vuong-bang-nhau', fig_two_tri(
        shape_from_angles(90, 40, names=('A', 'B', 'C')), 'ABC',
        shape_from_angles(90, 40, names=('D', 'E', 'F'), ox=330), 'DEF',
        dict(interior={'B': '40°', 'C': '?'}, right='A'), dict(interior={'E': '?'}, right='D')))
    L = 'tap1/chuong-4/bai-16/tam-giac-can-trung-truc.json'
    e(L, 0, 'vd-can-40', fig_tri(shape_from_angles(40, 70), 'ABC',
                                interior={'A': '40°', 'B': '?', 'C': '?'},
                                ticks=[('A', 'B'), ('A', 'C')]))
    e(L, 1, 'vd-can-100', fig_tri(shape_from_angles(100, 40), 'ABC',
                                 interior={'A': '100°', 'B': '?', 'C': '?'},
                                 ticks=[('A', 'B'), ('A', 'C')]))
    L = 'tap1/chuong-5/bai-19/bieu-do-doan-thang.json'
    e(L, 1, 'doan-thang-6-12-gio', fig_line_chart(['6 giờ', '12 giờ'], [18, 30], 36, 6))
    return E


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    svgs = {}
    item_map = {}
    for lesson, item_id, name, svg in specs() + extra_specs():
        svgs[name] = svg
        item_map.setdefault(lesson, {})[item_id] = f'figures/{name}.svg'
    theory_map = {}
    for lesson, after, name, svg, cap in theory_specs():
        svgs[name] = svg
        theory_map.setdefault(lesson, []).append((after, f'figures/{name}.svg', cap))
    example_map = {}
    for lesson, idx, name, svg in example_specs():
        svgs[name] = svg
        example_map.setdefault(lesson, {})[idx] = f'figures/{name}.svg'

    for name, svg in svgs.items():
        with open(os.path.join(FIG_DIR, f'{name}.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)

    lessons = set(item_map) | set(theory_map) | set(example_map)
    for lesson in sorted(lessons):
        path = os.path.join(CONTENT, lesson)
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        # 1) Câu hỏi: gắn trường figure ngay sau đề bài.
        mapping = item_map.get(lesson, {})
        found = set()
        for item in data['items']:
            if item['id'] not in mapping:
                continue
            found.add(item['id'])
            new = OrderedDict()
            for k, v in item.items():
                if k == 'figure':
                    continue
                new[k] = v
                if k == 'stem':
                    new['figure'] = mapping[item['id']]
            if 'figure' not in new:
                new['figure'] = mapping[item['id']]
            item.clear()
            item.update(new)
        missing = set(mapping) - found
        if missing:
            raise SystemExit(f'{lesson}: không tìm thấy câu {sorted(missing)}')

        # 2) Lý thuyết: bỏ khối hình cũ rồi chèn lại theo vị trí khai báo.
        base = [b for b in data['theory'] if b.get('type') != 'figure']
        inserts = {}
        for after, rel, cap in theory_map.get(lesson, []):
            inserts.setdefault(after, []).append({'type': 'figure', 'figure': rel, 'caption': cap})
        theory = []
        for i, b in enumerate(base):
            theory.append(b)
            theory.extend(inserts.get(i, []))
        if max(inserts, default=-1) >= len(base):
            raise SystemExit(f'{lesson}: chỉ số lý thuyết vượt quá số khối')
        data['theory'] = theory

        # 3) Ví dụ: gắn hoặc bỏ trường figure.
        ex_map = example_map.get(lesson, {})
        for i, ex in enumerate(data['examples']):
            ex.pop('figure', None)
            if i in ex_map:
                ex['figure'] = ex_map[i]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
    print(f'Đã tạo {len(svgs)} hình trong {FIG_DIR}')


if __name__ == '__main__':
    main()
