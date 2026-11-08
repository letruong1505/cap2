#!/usr/bin/env python3
# Sinh hình SVG minh họa cho môn KHTN 7 và gắn vào bài (khối "figure" trong lý thuyết, trường "figure" trong câu hỏi).
# Hình vẽ mô phỏng sơ đồ trong sách (nguyên tử, phân tử, tia sáng, nam châm, cây, ...), không phải ảnh chụp.
# Chạy: python3 tools/build-khtn-figures.py
import glob
import json
import math
import os
import re
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

INK = '#1d2733'
GREY = '#9aa5b1'
DEFS = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % INK)


def svg(w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Segoe UI, Arial, sans-serif">'
            % (w, h)) + DEFS + body + '</svg>'


def T(x, y, s, size=16, anchor='middle', weight='normal', fill=INK):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s">%s</text>'
            % (x, y, anchor, size, weight, fill, escape(s)))


def L(x1, y1, x2, y2, stroke=INK, w=2, dash=None, arrow=False, color=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    m = ' marker-end="url(#ar)"' if arrow else ''
    c = color or stroke
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>'
            % (x1, y1, x2, y2, c, w, d, m))


def C(cx, cy, r, fill='none', stroke=INK, w=2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (cx, cy, r, fill, stroke, w, d))


def R(x, y, w, h, fill='none', stroke=INK, sw=2, rx=0, opacity=1):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'opacity="%s"/>' % (x, y, w, h, rx, fill, stroke, sw, opacity))


def POLY(pts, fill, stroke='none', opacity=1, sw=1):
    p = ' '.join('%.1f,%.1f' % q for q in pts)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" opacity="%s"/>' % (p, fill, stroke, sw, opacity)


def PL(pts, stroke=INK, w=2, fill='none'):
    p = ' '.join('%.1f,%.1f' % q for q in pts)
    return '<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (p, fill, stroke, w)


# ---------------------------------------------------------------- nguyên tử
SHELL_R = [30, 58, 86]


def atom(cx, cy, shells, symbol='', charge='', scale=1.0):
    out = []
    base = [r * scale for r in SHELL_R]
    out.append(C(cx, cy, 13 * scale, fill='#f28e2b', stroke='#f28e2b'))
    out.append(T(cx, cy + 5 * scale, symbol, size=int(12 * scale) + 2, weight='bold', fill='#ffffff'))
    for i, n in enumerate(shells):
        r = base[i]
        out.append(C(cx, cy, r, stroke=GREY, w=1.2, dash='4 3'))
        for k in range(n):
            a = 2 * math.pi * k / n - math.pi / 2
            out.append(C(cx + r * math.cos(a), cy + r * math.sin(a), 4.5 * scale, fill='#4e79a7', stroke='#4e79a7'))
    if charge:
        out.append(T(cx + base[len(shells) - 1] * 0.75, cy - base[len(shells) - 1] * 0.75 - 6, charge,
                     size=20, weight='bold', fill='#e15759', anchor='start'))
    return ''.join(out)


def fig_khi_hiem():
    b = []
    names = [('He', [2]), ('Ne', [2, 8]), ('Ar', [2, 8, 8])]
    for i, (sym, sh) in enumerate(names):
        cx = 130 + i * 230
        b.append(atom(cx, 150, sh, sym, scale=1.0))
        b.append(T(cx, 275, 'Lớp ngoài cùng: %d e' % (sh[-1] if len(sh) > 1 else sh[0]), size=15))
    b.append(T(360, 30, 'Mô hình sắp xếp electron trong nguyên tử khí hiếm', size=17, weight='bold'))
    return svg(720, 300, ''.join(b))


def fig_ion_nacl():
    b = []
    b.append(T(360, 28, 'Na nhường 1 electron, Cl nhận 1 electron', size=17, weight='bold'))
    b.append(atom(90, 150, [2, 8, 1], 'Na', scale=0.7))
    b.append(T(90, 245, 'Na (11 e)', size=15))
    b.append(L(156, 150, 186, 150, arrow=True, w=2.5, color='#e15759'))
    b.append(T(171, 136, 'e⁻', size=16, fill='#e15759', weight='bold'))
    b.append(atom(250, 150, [2, 8], 'Na', charge='+', scale=0.7))
    b.append(T(250, 245, 'Ion Na⁺ (10 e)', size=15))
    b.append(atom(430, 150, [2, 8, 7], 'Cl', scale=0.7))
    b.append(T(430, 245, 'Cl (17 e)', size=15))
    b.append(L(496, 150, 526, 150, arrow=True, w=2.5, color='#e15759'))
    b.append(T(511, 136, 'e⁻', size=16, fill='#e15759', weight='bold'))
    b.append(atom(610, 150, [2, 8, 8], 'Cl', charge='−', scale=0.7))
    b.append(T(610, 245, 'Ion Cl⁻ (18 e)', size=15))
    return svg(720, 300, ''.join(b))


# ---------------------------------------------------------------- phân tử
ATOM_COLOR = {'H': ('#ffffff', INK), 'O': ('#e15759', '#ffffff'), 'C': ('#3b4a5a', '#ffffff'),
              'N': ('#4e79a7', '#ffffff'), 'Cl': ('#59a14f', '#ffffff')}


def mol(cx, cy, atoms, bonds):
    """atoms: [(dx, dy, symbol)], bonds: [(i, j, order)] – order 1,2,3 là liên kết đơn, đôi, ba."""
    out = []
    for i, j, k in bonds:
        ax, ay = cx + atoms[i][0], cy + atoms[i][1]
        bx, by = cx + atoms[j][0], cy + atoms[j][1]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        for t in range(k):
            off = (t - (k - 1) / 2) * 7
            out.append(L(ax + px * off, ay + py * off, bx + px * off, by + py * off, w=3))
    for dx, dy, s in atoms:
        fill, txt = ATOM_COLOR[s]
        out.append(C(cx + dx, cy + dy, 19, fill=fill, stroke=INK, w=1.5))
        out.append(T(cx + dx, cy + dy + 6, s, size=17, weight='bold', fill=txt if s != 'H' else INK))
    return ''.join(out)


def fig_phan_tu_don_chat():
    b = [T(360, 28, 'Phân tử đơn chất: các nguyên tử cùng loại dùng chung electron', size=17, weight='bold')]
    b.append(mol(120, 150, [(-40, 0, 'H'), (40, 0, 'H')], [(0, 1, 1)]))
    b.append(T(120, 225, 'H₂ (1 cặp e chung)', size=15))
    b.append(mol(360, 150, [(-40, 0, 'O'), (40, 0, 'O')], [(0, 1, 2)]))
    b.append(T(360, 225, 'O₂ (2 cặp e chung)', size=15))
    b.append(mol(600, 150, [(-40, 0, 'N'), (40, 0, 'N')], [(0, 1, 3)]))
    b.append(T(600, 225, 'N₂ (3 cặp e chung)', size=15))
    return svg(720, 260, ''.join(b))


def fig_phan_tu_hop_chat():
    b = [T(360, 28, 'Phân tử hợp chất: các nguyên tử khác loại dùng chung electron', size=17, weight='bold')]
    b.append(mol(110, 150, [(0, 0, 'O'), (-38, 36, 'H'), (38, 36, 'H')], [(0, 1, 1), (0, 2, 1)]))
    b.append(T(110, 225, 'H₂O', size=15))
    b.append(mol(290, 150, [(-70, 0, 'O'), (0, 0, 'C'), (70, 0, 'O')], [(0, 1, 2), (0, 2, 2)]))
    b.append(T(290, 225, 'CO₂', size=15))
    b.append(mol(480, 150, [(0, 0, 'C'), (-48, -48, 'H'), (48, -48, 'H'), (-48, 48, 'H'), (48, 48, 'H')],
                 [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)]))
    b.append(T(480, 225, 'CH₄', size=15))
    b.append(mol(640, 150, [(-30, 0, 'H'), (30, 0, 'Cl')], [(0, 1, 1)]))
    b.append(T(640, 225, 'HCl', size=15))
    return svg(720, 250, ''.join(b))


def fig_nguyen_tu_o():
    b = [T(200, 26, 'Nguyên tử oxygen (8 proton, 8 neutron, 8 electron)', size=16, weight='bold')]
    b.append(atom(200, 150, [2, 6], 'O', scale=1.25))
    b.append(T(200, 275, 'Hạt nhân: p (+) và n (không mang điện)', size=14))
    return svg(400, 290, ''.join(b))


# ---------------------------------------------------------------- chuyển động
def fig_do_toc_do():
    b = [T(360, 28, 'Đo tốc độ: đo quãng đường s và thời gian t', size=17, weight='bold')]
    b.append(L(60, 150, 660, 150, w=3))
    b.append(L(90, 110, 90, 190, w=3, color='#e15759'))
    b.append(T(90, 98, 'Vạch xuất phát', size=14, fill='#e15759'))
    b.append(L(600, 110, 600, 190, w=3, color='#59a14f'))
    b.append(T(600, 98, 'Vạch đích', size=14, fill='#59a14f'))
    b.append(R(150, 128, 52, 22, fill='#f28e2b', stroke=INK, rx=6))
    b.append(C(165, 152, 6, fill=INK, stroke=INK))
    b.append(C(190, 152, 6, fill=INK, stroke=INK))
    b.append(L(90, 215, 600, 215, arrow=True, w=1.5))
    b.append(T(345, 240, 's: quãng đường đo bằng thước (m)', size=15))
    b.append(T(360, 275, 't: thời gian đo bằng đồng hồ bấm giây hoặc cổng quang điện (s)', size=15))
    b.append(T(600, 255, 'v = s / t', size=16, weight='bold'))
    return svg(720, 290, ''.join(b))


def axes(x0, y0, x1, y1, xmin, xmax, ymin, ymax, xlab, ylab, xticks, yticks):
    out = []
    out.append(L(x0, y1, x0, y0, w=2))
    out.append(L(x0, y1, x1, y1, w=2))
    for tx in xticks:
        X = x0 + (tx - xmin) / (xmax - xmin) * (x1 - x0)
        out.append(L(X, y1, X, y1 + 5, w=1.5))
        out.append(T(X, y1 + 20, ('%g' % tx).replace('.', ','), size=14))
    for ty in yticks:
        Y = y1 - (ty - ymin) / (ymax - ymin) * (y1 - y0)
        out.append(L(x0 - 5, Y, x0, Y, w=1.5))
        out.append(T(x0 - 10, Y + 5, ('%g' % ty).replace('.', ','), size=14, anchor='end'))
        out.append(L(x0, Y, x1, Y, stroke='#e6ebf0', w=1))
    out.append(T((x0 + x1) / 2, y1 + 42, xlab, size=15))
    out.append(T(x0 + 6, y0 - 8, ylab, size=15, anchor='start'))
    return ''.join(out)


def fig_do_thi_s_t():
    x0, x1, y0, y1 = 90, 660, 40, 260
    f = lambda t, s: (x0 + t / 5 * (x1 - x0), y1 - s / 240 * (y1 - y0))
    b = [T(360, 22, 'Đồ thị quãng đường – thời gian của ô tô', size=17, weight='bold')]
    b.append(axes(x0, y0, x1, y1, 0, 5, 0, 240, 't (h)', 's (km)', [0, 1, 2, 3, 4, 5],
                  [0, 60, 120, 180, 240]))
    pts = [f(0, 0), f(3, 180), f(4, 180), f(5, 220)]
    b.append(PL(pts, stroke='#4e79a7', w=3))
    for p in pts:
        b.append(C(p[0], p[1], 4, fill='#4e79a7', stroke='#4e79a7'))
    b.append(T(f(1.5, 90)[0] + 10, f(1.5, 90)[1] + 24, 'Đi đều, tốc độ không đổi', size=14, anchor='start'))
    b.append(T(f(3.5, 180)[0], f(3.5, 180)[1] - 10, 'Dừng nghỉ', size=14))
    return svg(720, 320, ''.join(b))


def fig_bang_khoang_cach():
    x0, x1, y0, y1 = 110, 640, 40, 250
    cats = [('v = 60', 35), ('60 < v ≤ 80', 55), ('80 < v ≤ 100', 70), ('100 < v ≤ 120', 100)]
    b = [T(360, 22, 'Khoảng cách an toàn tối thiểu giữa hai xe (m)', size=17, weight='bold')]
    b.append(L(x0, y1, x1, y1, w=2))
    b.append(L(x0, y1, x0, y0, w=2))
    bw = 80
    gap = (x1 - x0) / len(cats)
    for i, (lab, v) in enumerate(cats):
        h = v / 110 * (y1 - y0)
        cx = x0 + gap * (i + 0.5)
        b.append(R(cx - bw / 2, y1 - h, bw, h, fill='#4e79a7', stroke='none'))
        b.append(T(cx, y1 - h - 8, '%d m' % v, size=15, weight='bold'))
        b.append(T(cx, y1 + 22, lab, size=14))
    b.append(T(360, 300, 'Tốc độ lưu hành (km/h)', size=15))
    return svg(720, 320, ''.join(b))


def fig_song_am():
    b = [T(360, 22, 'Biên độ và tần số của sóng âm', size=17, weight='bold')]

    def wave(x0, x1, yc, amp, cycles, color, label, lx):
        pts = []
        n = 240
        for k in range(n + 1):
            x = x0 + (x1 - x0) * k / n
            y = yc - amp * math.sin(2 * math.pi * cycles * k / n)
            pts.append((x, y))
        out = [L(x0, yc, x1, yc, stroke=GREY, w=1), PL(pts, stroke=color, w=2.5)]
        out.append(T(lx, yc + 75, label, size=14))
        return ''.join(out)

    b.append(wave(40, 340, 90, 25, 3, '#4e79a7', 'Biên độ nhỏ: âm nhỏ', 190))
    b.append(wave(380, 680, 90, 55, 3, '#e15759', 'Biên độ lớn: âm to', 530))
    b.append(wave(40, 340, 230, 35, 2, '#59a14f', 'Tần số thấp: âm trầm', 190))
    b.append(wave(380, 680, 230, 35, 6, '#f28e2b', 'Tần số cao: âm bổng', 530))
    return svg(720, 330, ''.join(b))


def fig_phan_xa_am():
    b = [T(360, 22, 'Âm phản xạ trên mặt chắn', size=17, weight='bold')]
    b.append(R(560, 40, 24, 230, fill=GREY, stroke=INK, sw=1.5))
    b.append(C(90, 150, 14, fill='#f28e2b', stroke=INK))
    b.append(T(90, 190, 'Nguồn âm', size=14))
    b.append(C(90, 255, 12, fill='#59a14f', stroke=INK))
    b.append(T(90, 282, 'Người nghe', size=14))
    I = (560, 120)
    b.append(L(90, 150, I[0], I[1], w=2.5, color='#e15759', arrow=True))
    b.append(L(I[0], I[1], 90, 255, w=2.5, color='#4e79a7', arrow=True))
    b.append(L(I[0], 40, I[0], 270, stroke=GREY, w=1, dash='5 4'))
    b.append(T(520, 110, 'i', size=15))
    b.append(T(600, 110, 'i′', size=15))
    b.append(T(500, 215, 'Âm tới', size=14, fill='#e15759'))
    b.append(T(300, 255, 'Âm phản xạ', size=14, fill='#4e79a7'))
    return svg(720, 300, ''.join(b))


# ---------------------------------------------------------------- ánh sáng
def fig_vung_toi():
    b = [T(360, 22, 'Vùng tối do nguồn sáng hẹp (trái) và nguồn sáng rộng (phải)', size=16, weight='bold')]

    def panel(ox_shift, a, bb, label):
        sx = 70 + ox_shift
        xo = 190 + ox_shift
        xs = 340 + ox_shift
        Ot, Ob = 120, 180
        r = (xs - sx) / (xo - sx)
        tops = [ys * (1 - r) + Ot * r for ys in (a, bb)]
        bots = [ys * (1 - r) + Ob * r for ys in (a, bb)]
        outer_top, outer_bot = min(tops), max(bots)
        inner_top, inner_bot = max(tops), min(bots)
        out = []
        out.append(POLY([(xo, Ot), (xs, outer_top), (xs, outer_bot), (xo, Ob)], fill='#c9d3dd', opacity=0.9))
        if inner_bot > inner_top:
            out.append(POLY([(xo, Ot), (xs, inner_top), (xs, inner_bot), (xo, Ob)], fill='#5b6777', opacity=0.9))
        for ys in (a, bb):
            out.append(L(sx, ys, xo, Ot, color='#f5b041', w=1))
            out.append(L(sx, ys, xo, Ob, color='#f5b041', w=1))
        out.append(R(xo - 6, Ot, 12, Ob - Ot, fill=INK, stroke=INK, sw=1))
        out.append(R(xs - 4, 40, 8, 220, fill=GREY, stroke=INK, sw=1))
        if a == bb:
            out.append(C(sx, a, 6, fill='#f5b041', stroke='#f5b041'))
        else:
            out.append(R(sx - 4, a, 8, bb - a, fill='#f5b041', stroke='#f5b041', sw=1))
        out.append(T(sx + 60 * 0, 280, label, size=15))
        return ''.join(out)

    b.append(panel(0, 150, 150, 'Nguồn sáng hẹp: bóng rõ, có ranh giới sắc nét'))
    return svg(720, 300, ''.join(b))


def fig_vung_toi_2():
    b = [T(360, 22, 'Vùng tối do nguồn sáng rộng: có vùng nửa tối', size=16, weight='bold')]
    sx, xo, xs = 70, 300, 600
    Ot, Ob = 120, 180
    a, bb = 100, 200
    r = (xs - sx) / (xo - sx)
    tops = [ys * (1 - r) + Ot * r for ys in (a, bb)]
    bots = [ys * (1 - r) + Ob * r for ys in (a, bb)]
    outer_top, outer_bot = min(tops), max(bots)
    inner_top, inner_bot = max(tops), min(bots)
    b.append(POLY([(xo, Ot), (xs, outer_top), (xs, outer_bot), (xo, Ob)], fill='#c9d3dd'))
    b.append(POLY([(xo, Ot), (xs, inner_top), (xs, inner_bot), (xo, Ob)], fill='#5b6777'))
    for ys in (a, bb):
        b.append(L(sx, ys, xo, Ot, color='#f5b041', w=1))
        b.append(L(sx, ys, xo, Ob, color='#f5b041', w=1))
    b.append(R(xo - 6, Ot, 12, Ob - Ot, fill=INK, stroke=INK, sw=1))
    b.append(R(xs - 4, 40, 8, 240, fill=GREY, stroke=INK, sw=1))
    b.append(R(sx - 4, a, 8, bb - a, fill='#f5b041', stroke='#f5b041', sw=1))
    b.append(T(xs + 12, 90, 'Vùng sáng', size=14, anchor='start'))
    b.append(T(xs + 12, 150, 'Vùng nửa tối', size=14, anchor='start'))
    b.append(T(xs + 12, 215, 'Vùng tối', size=14, anchor='start'))
    b.append(T(sx, 280, 'Nguồn sáng rộng', size=14))
    return svg(720, 300, ''.join(b))


def fig_phan_xa_anh_sang():
    b = [T(360, 22, 'Phản xạ ánh sáng trên gương phẳng', size=17, weight='bold')]
    b.append(R(40, 200, 640, 16, fill=GREY, stroke=INK, sw=1.5))
    I = (360, 208)
    b.append(L(I[0], 40, I[0], 208, stroke=GREY, w=1.5, dash='6 4'))
    b.append(T(I[0] + 10, 60, 'N', size=15, anchor='start'))
    b.append(L(170, 80, I[0], I[1], w=2.5, color='#e15759', arrow=True))
    b.append(L(I[0], I[1], 550, 80, w=2.5, color='#4e79a7', arrow=True))
    b.append(T(190, 70, 'S (tia tới)', size=14, fill='#e15759'))
    b.append(T(540, 70, 'R (tia phản xạ)', size=14, fill='#4e79a7', anchor='end'))
    b.append(T(I[0] - 40, I[1] - 20, 'i', size=16))
    b.append(T(I[0] + 40, I[1] - 20, 'i′', size=16))
    b.append(T(I[0], 250, 'I: điểm tới   IN: pháp tuyến   Góc i = góc i′', size=14))
    return svg(720, 270, ''.join(b))


def fig_anh_qua_guong():
    b = [T(360, 22, 'Ảnh của vật qua gương phẳng', size=17, weight='bold')]
    gx = 360
    b.append(R(gx - 4, 40, 8, 230, fill=GREY, stroke=INK, sw=1.5))
    ox, top, base = 200, 110, 230
    b.append(L(ox, base, ox, top, w=3, color='#e15759', arrow=True))
    ix = 2 * gx - ox
    b.append(L(ix, base, ix, top, w=3, color='#e15759', dash='6 4'))
    b.append(L(ox, top, gx, top, stroke=GREY, w=1.2, dash='4 3'))
    b.append(L(gx, top, ix, top, stroke=GREY, w=1.2, dash='4 3'))
    b.append(T(ox, 255, 'Vật', size=14))
    b.append(T(ix, 255, 'Ảnh (ảo)', size=14))
    b.append(T((ox + gx) / 2, top - 8, 'd', size=15))
    b.append(T((ix + gx) / 2, top - 8, 'd′', size=15))
    b.append(T(gx, 30, 'Gương', size=14))
    b.append(T(360, 290, 'Ảnh đối xứng với vật qua mặt gương; d = d′', size=14))
    return svg(720, 300, ''.join(b))


# ---------------------------------------------------------------- từ
def fig_nam_cham():
    b = [T(360, 22, 'Tương tác giữa hai nam châm', size=17, weight='bold')]

    def magnet(x, y, horizontal, first):
        w, h = (110, 36) if horizontal else (36, 110)
        if horizontal:
            n_rect = (x, y, w / 2, h) if first == 'N' else (x + w / 2, y, w / 2, h)
            s_rect = (x + w / 2, y, w / 2, h) if first == 'N' else (x, y, w / 2, h)
            out = [R(n_rect[0], n_rect[1], n_rect[2], n_rect[3], fill='#e15759', stroke=INK, sw=1.5),
                   R(s_rect[0], s_rect[1], s_rect[2], s_rect[3], fill='#4e79a7', stroke=INK, sw=1.5)]
            out.append(T(x + w / 4 if first == 'N' else x + 3 * w / 4, y + 24, 'N', size=16, weight='bold',
                         fill='#ffffff'))
            out.append(T(x + 3 * w / 4 if first == 'N' else x + w / 4, y + 24, 'S', size=16, weight='bold',
                         fill='#ffffff'))
            return ''.join(out)
        return ''

    # hàng trên: khác tên (N–S) hút nhau
    b.append(T(200, 60, 'Khác tên (N – S): hút nhau', size=15, weight='bold'))
    b.append(magnet(90, 90, True, 'N'))
    b.append(magnet(260, 90, True, 'S'))
    b.append(L(210, 108, 258, 108, color='#59a14f', w=2.5, arrow=True))
    b.append(L(258, 108, 210, 108, color='#59a14f', w=2.5, arrow=True))
    # hàng dưới: cùng tên (N–N) đẩy nhau
    b.append(T(520, 60, 'Cùng tên (N – N): đẩy nhau', size=15, weight='bold'))
    b.append(magnet(430, 180, True, 'N'))
    b.append(magnet(430 + 0, 230, True, 'N'))
    return svg(720, 300, ''.join(b))


def fig_nam_cham_v2():
    b = [T(360, 22, 'Tương tác giữa hai nam châm', size=17, weight='bold')]

    def bar(x, y, left, right):
        # hai thanh nam châm nằm ngang, mỗi thanh gồm nửa N (đỏ) và nửa S (xanh)
        col = {'N': '#e15759', 'S': '#4e79a7'}
        out = [R(x, y, 60, 34, fill=col[left], stroke=INK, sw=1.5),
               R(x + 60, y, 60, 34, fill=col[right], stroke=INK, sw=1.5)]
        out.append(T(x + 30, y + 23, left, size=16, weight='bold', fill='#ffffff'))
        out.append(T(x + 90, y + 23, right, size=16, weight='bold', fill='#ffffff'))
        return ''.join(out)

    # trái: cực N của thanh 1 đặt cạnh cực S của thanh 2 (khác tên)
    b.append(T(180, 70, 'Khác tên: hút nhau', size=16, weight='bold'))
    b.append(bar(60, 100, 'N', 'S'))
    b.append(bar(180, 100, 'N', 'S'))
    b.append(T(180, 170, 'Cực S và cực N cạnh nhau: hút nhau', size=14))
    # phải: cực N của thanh 1 cạnh cực N của thanh 2 (cùng tên)
    b.append(T(540, 70, 'Cùng tên: đẩy nhau', size=16, weight='bold'))
    b.append(bar(450, 100, 'S', 'N'))
    b.append(bar(570, 100, 'N', 'S'))
    b.append(L(570, 150, 540, 170, color='#e15759', w=2.5, arrow=True))
    b.append(L(570, 150, 600, 170, color='#e15759', w=2.5, arrow=True))
    b.append(T(540, 200, 'Hai cực N đẩy nhau', size=14))
    return svg(720, 230, ''.join(b))


def fig_tu_pho():
    cx, cy = 360, 170
    b = [T(360, 22, 'Đường sức từ quanh một nam châm thẳng', size=17, weight='bold')]
    for L0 in (70, 120, 170):
        pts_r, pts_l = [], []
        for k in range(1, 200):
            th = math.pi * k / 200
            r = L0 * math.sin(th) ** 2
            x = r * math.sin(th)
            y = r * math.cos(th)
            pts_r.append((cx + x, cy - y))
            pts_l.append((cx - x, cy - y))
        b.append(PL(pts_r, stroke='#4e79a7', w=1.4))
        b.append(PL(pts_l, stroke='#4e79a7', w=1.4))
    b.append(R(cx - 14, cy - 42, 28, 84, fill='#e15759', stroke=INK, sw=1.5))
    b.append(R(cx - 14, cy - 42, 28, 42, fill='#e15759', stroke=INK, sw=1.5))
    b.append(R(cx - 14, cy, 28, 42, fill='#4e79a7', stroke=INK, sw=1.5))
    b.append(T(cx, cy - 16, 'N', size=16, weight='bold', fill='#ffffff'))
    b.append(T(cx, cy + 26, 'S', size=16, weight='bold', fill='#ffffff'))
    b.append(T(360, 300, 'Đường sức đi ra từ cực N, đi vào cực S (ở ngoài thanh nam châm)', size=14))
    return svg(720, 320, ''.join(b))


def fig_nam_cham_dien():
    b = [T(360, 22, 'Nam châm điện: ống dây có lõi sắt non', size=17, weight='bold')]
    # nguồn điện
    b.append(L(120, 100, 120, 240, w=2))
    b.append(L(100, 120, 140, 120, w=5))
    b.append(L(108, 140, 132, 140, w=2.5))
    b.append(T(120, 90, 'Nguồn điện', size=14))
    # khoá K
    b.append(L(120, 240, 200, 240, w=2))
    b.append(L(200, 240, 240, 200, w=2))
    b.append(C(240, 200, 0))
    b.append(T(240, 190, 'K', size=14))
    b.append(L(240, 240, 600, 240, w=2))
    b.append(L(600, 240, 600, 100, w=2))
    b.append(L(120, 100, 600, 100, w=2))
    # lõi sắt
    b.append(R(250, 150, 320, 40, fill='#c9d3dd', stroke=INK, sw=1.5))
    # cuộn dây
    for i in range(10):
        X = 280 + i * 28
        b.append(('<ellipse cx="%.1f" cy="170" rx="7" ry="28" fill="none" stroke="#e15759" stroke-width="2.5"/>') % X)
    b.append(T(410, 225, 'Lõi sắt non', size=14))
    b.append(T(410, 90, 'Cuộn dây (ống dây)', size=14, fill='#e15759'))
    b.append(T(360, 290, 'Đóng K: có dòng điện, ống dây thành nam châm; ngắt K: mất từ tính', size=14))
    return svg(720, 310, ''.join(b))


# ---------------------------------------------------------------- thực vật
def fig_la_quang_hop():
    b = [T(360, 22, 'Cấu tạo lá và sự trao đổi chất khi quang hợp', size=17, weight='bold')]
    x0, x1 = 170, 560
    b.append(R(x0, 60, x1 - x0, 24, fill='#dfe9d5', stroke=INK, sw=1.2))
    b.append(T((x0 + x1) / 2, 77, 'Biểu bì trên', size=13))
    b.append(R(x0, 84, x1 - x0, 60, fill='#b9dba5', stroke=INK, sw=1.2))
    for i in range(6):
        for j in range(2):
            X = x0 + 30 + i * 60
            Y = 96 + j * 26
            b.append(R(X, Y, 44, 20, fill='#8fc471', stroke=INK, sw=0.8, rx=4))
            b.append(C(X + 14, Y + 10, 3, fill='#2e7d32', stroke='#2e7d32'))
    b.append(T(x0 - 10, 120, 'Mô giậu', size=13, anchor='end'))
    b.append(R(x0, 144, x1 - x0, 70, fill='#e9f3d9', stroke=INK, sw=1.2))
    for i in range(10):
        X = x0 + 20 + i * 38
        Y = 160 + (i % 2) * 20
        b.append(C(X, Y, 10, fill='#d3e8c0', stroke=INK, w=0.8))
    b.append(T(x0 - 10, 180, 'Mô xốp', size=13, anchor='end'))
    b.append(R(x0, 214, x1 - x0, 24, fill='#dfe9d5', stroke=INK, sw=1.2))
    b.append(T((x0 + x1) / 2, 231, 'Biểu bì dưới (có khí khổng)', size=13))
    b.append(L(110, 210, 165, 200, w=2, color='#4e79a7', arrow=True))
    b.append(T(70, 225, 'CO₂ vào', size=14, fill='#4e79a7'))
    b.append(L(150, 80, 118, 60, w=2, color='#e15759', arrow=True))
    b.append(T(70, 52, 'O₂ ra', size=14, fill='#e15759'))
    return svg(720, 310, ''.join(b))


def fig_nhiet_do_curve(title, xlab, ylab, peak_lo, peak_hi, xmax, note):
    x0, x1, y0, y1 = 90, 660, 40, 250
    f = lambda t: math.exp(-((t - (peak_lo + peak_hi) / 2) / 11.0) ** 2)
    xs = [xmax * k / 120 for k in range(121)]
    pts = [(x0 + x / xmax * (x1 - x0), y1 - f(x) * (y1 - y0) * 0.9) for x in xs]
    b = [T(360, 22, title, size=17, weight='bold')]
    b.append(R(x0 + (peak_lo / xmax) * (x1 - x0), y0, (peak_hi - peak_lo) / xmax * (x1 - x0), y1 - y0,
               fill='#d5ecc7', stroke='none', opacity=0.9))
    b.append(axes(x0, y0, x1, y1, 0, xmax, 0, 1, xlab, ylab, list(range(0, xmax + 1, 10)), []))
    b.append(PL(pts, stroke='#4e79a7', w=3))
    b.append(T((x0 + x1) / 2, 290, note, size=14))
    return svg(720, 310, ''.join(b))


def fig_khi_khong():
    b = [T(360, 22, 'Khí khổng mở và đóng ở lá', size=17, weight='bold')]

    def stoma(cx, cy, open_):
        out = []
        gap = 14 if open_ else 0
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="22" ry="26" fill="#8fc471" stroke="%s" stroke-width="2"/>'
                   % (cx - 14 - gap / 2, cy, INK))
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="22" ry="26" fill="#8fc471" stroke="%s" stroke-width="2"/>'
                   % (cx + 14 + gap / 2, cy, INK))
        if open_:
            out.append(POLY([(cx - 5, cy - 10), (cx + 5, cy - 10), (cx + 5, cy + 10), (cx - 5, cy + 10)],
                            fill='#ffffff', stroke='none'))
        return ''.join(out)

    b.append(stoma(200, 150, True))
    b.append(T(200, 225, 'Mở (cây đủ nước)', size=15))
    b.append(stoma(520, 150, False))
    b.append(T(520, 225, 'Đóng (cây thiếu nước)', size=15))
    b.append(T(360, 275, 'Tế bào hình hạt đậu: khi trương nước thì khe mở ra, thoát hơi nước và trao đổi khí', size=14))
    return svg(720, 290, ''.join(b))


def fig_phan_tu_nuoc():
    b = [T(360, 22, 'Phân tử nước: một nguyên tử O liên kết với hai nguyên tử H', size=16, weight='bold')]
    b.append(mol(360, 150, [(0, 0, 'O'), (-70, 60, 'H'), (70, 60, 'H')], [(0, 1, 1), (0, 2, 1)]))
    b.append(T(360, 250, 'Các nguyên tử H và O tạo góc khoảng 104,5°, electron lệch về phía O', size=14))
    return svg(720, 270, ''.join(b))


def fig_van_chuyen_nuoc():
    b = [T(360, 22, 'Vận chuyển nước và chất khoáng, chất hữu cơ trong cây', size=17, weight='bold')]
    b.append(R(40, 260, 640, 30, fill='#c8a77a', stroke='none', opacity=0.6))
    b.append(T(360, 282, 'Đất', size=14))
    b.append(L(360, 260, 360, 60, stroke='#7b5e3b', w=14))
    b.append(L(340, 260, 340, 60, stroke='#4e79a7', w=4))
    b.append(L(380, 260, 380, 60, stroke='#f28e2b', w=4))
    b.append(T(300, 170, 'Mạch gỗ', size=14, fill='#4e79a7', anchor='end'))
    b.append(T(420, 170, 'Mạch rây', size=14, fill='#f28e2b', anchor='start'))
    b.append(L(330, 245, 330, 80, w=2.5, color='#4e79a7', arrow=True))
    b.append(L(390, 80, 390, 240, w=2.5, color='#f28e2b', arrow=True))
    b.append(T(560, 110, 'Lá: thoát hơi nước', size=14, anchor='start'))
    b.append(L(540, 100, 400, 100, w=2, color='#4e79a7', dash='5 4', arrow=True))
    b.append(T(360, 40, 'Lá', size=14))
    b.append(C(330, 230, 6, fill='#c8a77a', stroke=INK, w=1))
    b.append(T(300, 215, 'Lông hút', size=13, anchor='end'))
    return svg(720, 310, ''.join(b))


def fig_tuan_hoan():
    b = [T(360, 22, 'Hai vòng tuần hoàn ở người', size=17, weight='bold')]
    b.append(R(320, 120, 80, 60, fill='#e15759', stroke=INK, sw=1.5, rx=12))
    b.append(T(360, 156, 'Tim', size=16, weight='bold', fill='#ffffff'))
    b.append(R(120, 40, 120, 50, fill='#4e79a7', stroke=INK, sw=1.5, rx=10))
    b.append(T(180, 70, 'Phổi', size=16, weight='bold', fill='#ffffff'))
    b.append(R(480, 200, 160, 60, fill='#59a14f', stroke=INK, sw=1.5, rx=10))
    b.append(T(560, 236, 'Các cơ quan', size=15, weight='bold', fill='#ffffff'))
    b.append(L(320, 140, 240, 70, w=2.5, color='#4e79a7', arrow=True))
    b.append(L(200, 95, 330, 125, w=2.5, color='#4e79a7', arrow=True))
    b.append(T(240, 110, 'Tuần hoàn nhỏ', size=14, fill='#4e79a7', anchor='end'))
    b.append(L(400, 150, 480, 220, w=2.5, color='#59a14f', arrow=True))
    b.append(L(480, 240, 400, 170, w=2.5, color='#59a14f', arrow=True))
    b.append(T(520, 170, 'Tuần hoàn lớn', size=14, fill='#59a14f', anchor='start'))
    b.append(T(360, 290, 'Máu giàu O₂ được bơm đi nuôi cơ thể; máu nghèo O₂ về tim', size=14))
    return svg(720, 310, ''.join(b))


def fig_huong_sang_cay():
    b = [T(360, 22, 'Thân cây cong về phía có ánh sáng', size=17, weight='bold')]
    b.append(R(40, 270, 640, 20, fill='#c8a77a', stroke='none', opacity=0.6))
    base = (250, 270)
    pts = []
    for k in range(0, 41):
        t = k / 40
        x = base[0] + 80 * t * t
        y = base[1] - 190 * t
        pts.append((x, y))
    b.append(PL(pts, stroke='#59a14f', w=12))
    for dx, dy in [(0, 0)]:
        pass
    for k in range(3):
        y = 90 + k * 40
        b.append(L(620, y, 560, y + 10, w=2.5, color='#f5b041', arrow=True))
    b.append(T(640, 80, 'Ánh sáng', size=14, fill='#f5b041'))
    b.append(T(250, 300, 'Gốc cây', size=14))
    b.append(T(360, 40, 'Ngọn cây hướng về phía ánh sáng', size=14))
    return svg(720, 320, ''.join(b))


def fig_mo_phan_sinh():
    b = [T(360, 22, 'Vị trí mô phân sinh ở thân cây hai lá mầm', size=17, weight='bold')]
    b.append(R(300, 100, 120, 170, fill='#e9f3d9', stroke=INK, sw=1.5))
    b.append(R(300, 100, 120, 14, fill='#e15759', stroke='none'))
    b.append(T(360, 88, 'Mô phân sinh đỉnh (ở ngọn): làm cây cao lên', size=14, fill='#e15759'))
    b.append(R(300, 160, 120, 10, fill='#59a14f', stroke='none'))
    b.append(R(296, 100, 6, 170, fill='#59a14f', stroke='none'))
    b.append(R(418, 100, 6, 170, fill='#59a14f', stroke='none'))
    b.append(T(440, 185, 'Mô phân sinh bên', size=14, fill='#59a14f', anchor='start'))
    b.append(T(440, 201, '(đường kính thân tăng)', size=14, fill='#59a14f', anchor='start'))
    b.append(L(360, 270, 360, 90, w=2, color='#4e79a7', arrow=True))
    b.append(T(360, 290, 'Hướng tăng chiều dài', size=14, fill='#4e79a7'))
    return svg(720, 310, ''.join(b))


def fig_hoa():
    b = [T(360, 22, 'Cấu tạo hoa lưỡng tính', size=17, weight='bold')]
    cx, cy = 360, 150
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        px, py = cx + 62 * math.cos(a), cy + 62 * math.sin(a)
        b.append('<ellipse cx="%.1f" cy="%.1f" rx="28" ry="42" fill="#f6c6d4" stroke="%s" stroke-width="1.5" '
                 'transform="rotate(%d %.1f %.1f)"/>' % (px, py, INK, ang + 90, px, py))
    b.append(C(cx, cy, 8, fill='#2e7d32', stroke='#2e7d32'))
    # nhuỵ ở giữa
    b.append(L(cx, cy, cx, cy - 70, w=3, color='#59a14f'))
    b.append(C(cx, cy - 74, 7, fill='#59a14f', stroke='#59a14f'))
    # nhị
    for ang in (-40, 40):
        a = math.radians(ang - 90)
        ex, ey = cx + 60 * math.cos(a), cy + 60 * math.sin(a)
        b.append(L(cx, cy, ex, ey, w=2, color='#f28e2b'))
        b.append(C(ex, ey, 6, fill='#f28e2b', stroke='#f28e2b'))
    # chú thích ở cột bên phải, có đường dẫn
    notes = [(cy - 74, 'Đầu nhuỵ'), (cy - 40, 'Vòi nhuỵ'), (cy - 6, 'Bầu nhuỵ (chứa noãn)'),
             (cy + 40, 'Nhị gồm chỉ nhị và bao phấn')]
    targets = [(cx, cy - 74), (cx, cy - 40), (cx, cy - 20), (cx + 60 * math.cos(math.radians(-40 - 90)),
                                                               cy + 60 * math.sin(math.radians(-40 - 90)))]
    for (ny, label), (tx, ty) in zip(notes, targets):
        b.append(L(tx + 8, ty, 500, ny - 4, stroke=GREY, w=1))
        b.append(T(506, ny, label, size=13, anchor='start'))
    return svg(720, 310, ''.join(b))


def fig_moi_quan_he():
    b = [T(360, 22, 'Các hoạt động sống của cơ thể có quan hệ với nhau', size=17, weight='bold')]
    cx, cy = 360, 160
    items = [(cx, 60, 'Sinh trưởng và phát triển'), (cx + 170, cy, 'Sinh sản'),
             (cx, 260, 'Cảm ứng'), (cx - 170, cy, 'Trao đổi chất\nvà chuyển hoá năng lượng')]
    b.append(C(cx, cy, 52, fill='#f28e2b', stroke='#f28e2b'))
    b.append(T(cx, cy - 4, 'Trao đổi chất', size=14, weight='bold', fill='#ffffff'))
    b.append(T(cx, cy + 14, 'và chuyển hoá', size=13, fill='#ffffff'))
    b.append(T(cx, cy + 30, 'năng lượng', size=13, fill='#ffffff'))
    for x, y, lab in items[:3]:
        b.append(C(x, y, 42, fill='#dfe9d5', stroke=INK, w=1.5))
        b.append(T(x, y + 5, lab, size=13, weight='bold'))
        b.append(L(x, y, cx, cy, stroke=GREY, w=1, dash='4 3'))
    x, y = items[3][0], items[3][1]
    b.append(C(x, y, 42, fill='#dfe9d5', stroke=INK, w=1.5))
    b.append(T(x, y - 4, 'Trao đổi chất', size=12, weight='bold'))
    b.append(T(x, y + 12, 'và chuyển hoá', size=12, weight='bold'))
    b.append(T(x, y + 27, 'năng lượng', size=12, weight='bold'))
    return svg(720, 320, ''.join(b))


def fig_nguyen_tu_nhan():
    return ''


FIGURES = {
    'khtn-khi-hiem.svg': fig_khi_hiem,
    'khtn-ion-nacl.svg': fig_ion_nacl,
    'khtn-phan-tu-don-chat.svg': fig_phan_tu_don_chat,
    'khtn-phan-tu-hop-chat.svg': fig_phan_tu_hop_chat,
    'khtn-nguyen-tu-o.svg': fig_nguyen_tu_o,
    'khtn-do-toc-do.svg': fig_do_toc_do,
    'khtn-do-thi-s-t.svg': fig_do_thi_s_t,
    'khtn-bang-khoang-cach.svg': fig_bang_khoang_cach,
    'khtn-song-am.svg': fig_song_am,
    'khtn-phan-xa-am.svg': fig_phan_xa_am,
    'khtn-vung-toi.svg': fig_vung_toi_2,
    'khtn-phan-xa-anh-sang.svg': fig_phan_xa_anh_sang,
    'khtn-anh-qua-guong.svg': fig_anh_qua_guong,
    'khtn-nam-cham.svg': fig_nam_cham_v2,
    'khtn-tu-pho.svg': fig_tu_pho,
    'khtn-nam-cham-dien.svg': fig_nam_cham_dien,
    'khtn-la-quang-hop.svg': fig_la_quang_hop,
    'khtn-nhiet-do-quang-hop.svg': lambda: fig_nhiet_do_curve(
        'Ảnh hưởng của nhiệt độ đến quang hợp (minh họa)', 'Nhiệt độ (°C)', 'Cường độ', 25, 35, 50,
        'Khoảng 25 °C đến 35 °C là thuận lợi nhất; quá cao hoặc quá thấp làm giảm quang hợp'),
    'khtn-nhiet-do-sinh-truong.svg': lambda: fig_nhiet_do_curve(
        'Ảnh hưởng của nhiệt độ đến sinh trưởng (minh họa)', 'Nhiệt độ (°C)', 'Sinh trưởng', 23, 37, 50,
        'Mỗi loài có khoảng nhiệt độ thuận lợi riêng để sinh trưởng và phát triển'),
    'khtn-khi-khong.svg': fig_khi_khong,
    'khtn-phan-tu-nuoc.svg': fig_phan_tu_nuoc,
    'khtn-van-chuyen-nuoc.svg': fig_van_chuyen_nuoc,
    'khtn-tuan-hoan.svg': fig_tuan_hoan,
    'khtn-huong-sang-cay.svg': fig_huong_sang_cay,
    'khtn-mo-phan-sinh.svg': fig_mo_phan_sinh,
    'khtn-hoa.svg': fig_hoa,
    'khtn-moi-quan-he.svg': fig_moi_quan_he,
}


def write_figures():
    # KHTN đã tách thành ly7, hoa7, sinh7: mỗi hình được ghi vào thư mục figures của môn đang dùng nó.
    dests = [os.path.join(ROOT, 'content', d, 'figures') for d in ('ly7', 'hoa7', 'sinh7')]
    count = 0
    for name, fn in FIGURES.items():
        for d in dests:
            if os.path.exists(os.path.join(d, name)):
                with open(os.path.join(d, name), 'w', encoding='utf8') as f:
                    f.write(fn())
                count += 1
    print('Đã ghi lại %d hình' % count)


if __name__ == '__main__':
    write_figures()
