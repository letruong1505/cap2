#!/usr/bin/env python3
# Hình minh họa lý thuyết Vật lí 8 và 9 (sơ đồ mô phỏng). Chạy: python3 tools/build-ly89-figures.py
import math
import os
import random
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib2 import *

WATER = '#b9d9f0'
WATER2 = '#8ec1ea'


def cube(x, y, s, fill, dx=34, dy=-26, label=None):
    front = [(x, y + s), (x + s, y + s), (x + s, y), (x, y)]
    top = [(x, y), (x + s, y), (x + s + dx, y + dy), (x + dx, y + dy)]
    side = [(x + s, y + s), (x + s + dx, y + s + dy), (x + s + dx, y + dy), (x + s, y)]
    return POLY(front, fill=fill) + POLY(top, fill='#ffffff55' if False else fill, stroke=INK) + POLY(side, fill=fill)


def tank(x, y, w, h, level, fill=WATER):
    """Bình hở trên: (x,y) góc trên trái; level: mực nước tính từ đáy (0..1)."""
    top = y + h * (1 - level)
    return (R(x, top, w, y + h - top, fill=fill, stroke='none', sw=0) + L(x, y, x, y + h, w=2.6) + L(x + w, y, x + w, y + h, w=2.6)
            + L(x, y + h, x + w, y + h, w=2.6))


# ======================================================================= Lí 8
def fig_khoi_luong_rieng():
    b = [title(720, 'Ba khối có cùng thể tích 1 m³ nhưng khối lượng khác nhau')]
    items = [(90, 'Nước', '#bcd9f0', '1 000 kg'), (300, 'Nhôm', '#cfd5db', '2 700 kg'), (510, 'Sắt', '#8d98a5', '7 800 kg')]
    for x, name, col, m in items:
        b.append(cube(x, 90, 96, col))
        b.append(T(x + 63, 56, name, size=16, weight='bold'))
        b.append(T(x + 63, 222, 'V = 1 m³,  m = ' + m, size=14))
        b.append(T(x + 63, 244, 'D = ' + m.replace('kg', 'kg/m³'), size=15, weight='bold', fill=BLUE))
    b.append(T(360, 280, 'D = m / V:  cùng thể tích, khối lượng càng lớn thì khối lượng riêng càng lớn', size=13.5, fill=GREY))
    return svg(720, 296, ''.join(b))


def fig_the_tich_soi():
    b = [title(720, 'Đo thể tích hòn sỏi bằng ống đong')]
    def cyl(cx, level, stone):
        o = [R(cx - 36, 52, 72, 210, fill='white', stroke=INK, sw=2.4, rx=3)]
        yl = 262 - 2 * level
        o.append(R(cx - 36, yl, 72, 262 - yl, fill=WATER, stroke='none', sw=0))
        o.append(R(cx - 36, 52, 72, 210, fill='none', stroke=INK, sw=2.4, rx=3))
        for v in range(0, 101, 10):
            y = 262 - 2 * v
            o.append(L(cx - 36, y, cx - 22, y, w=1.6))
            o.append(T(cx - 42, y + 4, str(v), size=11, anchor='end'))
        if stone:
            o.append(ELL(cx, 248, 16, 11, fill='#8d99a6', stroke=INK, w=2))
        o.append(L(cx + 36, yl, cx + 70, yl, stroke=RED, w=1.6, dash='4 3'))
        return ''.join(o)
    b.append(cyl(170, 50, False))
    b.append(cyl(480, 70, True))
    b.append(T(170, 292, 'Chưa thả sỏi', size=14, weight='bold'))
    b.append(T(170, 312, 'V₁ = 50 mL (cm³)', size=14, fill=RED))
    b.append(T(480, 292, 'Đã thả sỏi (ngập hoàn toàn)', size=14, weight='bold'))
    b.append(T(480, 312, 'V₂ = 70 mL (cm³)', size=14, fill=RED))
    b.append(L(250, 150, 360, 150, stroke=BLUE, w=2.4, arrow=True))
    b.append(T(305, 138, 'thả sỏi vào', size=13, fill=BLUE))
    b.append(card_text(556, 90, ['Thể tích sỏi:', 'V = V₂ − V₁', '= 70 − 50', '= 20 cm³'], w=150, size=14, lh=24))
    return svg(720, 330, ''.join(b))


def fig_ap_suat_be_mat():
    b = [title(720, 'Cùng áp lực, diện tích bị ép càng nhỏ thì áp suất càng lớn')]
    sy = 200
    for cx, w, h, sink, cap in ((190, 140, 56, 6, 'Đặt nằm: S lớn → lún ít'), (500, 56, 140, 24, 'Đặt đứng: S nhỏ → lún nhiều')):
        b.append(R(cx - 160, sy, 320, 52, fill='#ecdca8', stroke=INK, sw=1.6))
        rnd = random.Random(int(cx))
        for _ in range(60):
            b.append(dot(cx - 156 + rnd.random() * 312, sy + 4 + rnd.random() * 44, 1.2, '#b8a266'))
        bx, by = cx - w / 2, sy + sink - h
        b.append(R(bx, by, w, h, fill='#8d99a6', stroke=INK, sw=2.2))
        b.append(T(cx, by + h / 2 + 5, 'cùng khối lượng', size=12, fill='white') if w > 100 else '')
        b.append(force(cx, by - 4 - 40, 0, 40, None, col=RED, w=2.6))
        b.append(H(cx + 14, by - 20, 'P (áp lực)', size=13, fill=RED, anchor='start'))
        b.append(T(cx, sy + 80, cap, size=14.5, weight='bold'))
    b.append(T(360, 318, 'p = F / S', size=16, weight='bold', fill=BLUE))
    return svg(720, 332, ''.join(b))


def fig_ap_suat_chat_long():
    b = [title(720, 'Áp suất chất lỏng tăng theo độ sâu')]
    x, y, w, h = 190, 50, 240, 210
    b.append(tank(x, y, w, h, 1.0))
    b.append(L(x - 8, y, x + w + 8, y, stroke=BLUE, w=1.6, dash='5 4'))
    for yy in (95, 150, 205):
        ln = (yy - y) * 0.42
        b.append(L(x + w, yy, x + w + ln, yy, stroke=RED, w=2.2, arrow=True))
        b.append(L(x, yy, x - ln, yy, stroke=RED, w=2.2, arrow=True))
    for xx in (x + 60, x + 130, x + 200):
        b.append(L(xx, y + h, xx, y + h + 28, stroke=RED, w=2.2, arrow=True))
    b.append(T(x + w / 2, y + h + 50, 'Càng xuống sâu, mũi tên (áp suất) càng dài', size=13.5))
    cx = 600
    b.append(C(cx, 150, 24, fill='#f7c58a', stroke=INK, w=2.2))
    for a in range(0, 360, 45):
        x1, y1 = pt(cx, 150, 28, a); x2, y2 = pt(cx, 150, 62, a)
        b.append(L(x2, y2, x1, y1, stroke=RED, w=2.2, arrow=True))
    b.append(T(cx, 250, 'Chất lỏng gây áp suất', size=14, weight='bold'))
    b.append(T(cx, 270, 'theo mọi phương lên vật', size=14, weight='bold'))
    return svg(720, 290, ''.join(b))


def fig_khi_quyen_coc():
    b = [title(720, 'Áp suất khí quyển giữ nước trong cốc úp ngược')]
    cx = 200
    b.append(R(cx - 60, 50, 120, 140, fill=WATER, stroke=INK, sw=2.6, rx=3))
    b.append(L(cx - 66, 192, cx + 66, 192, stroke=INK, w=3))
    for k in range(-2, 3):
        b.append(L(cx + k * 22, 244, cx + k * 22, 200, stroke=RED, w=2.2, arrow=True))
    b.append(T(cx, 276, 'Áp suất khí quyển tác dụng lên tấm nylon', size=13.5, fill=RED, weight='bold'))
    b.append(T(cx + 78, 196, 'tấm nylon', size=13, anchor='start'))
    b.append(L(cx, 48, cx, 70, w=0))
    b.append(force(cx, 80, 0, 40, None, col=BLUE, w=2.2))
    b.append(H(cx + 70, 104, 'trọng lượng nước', size=12.5, fill=BLUE, anchor='start'))
    b.append(card_text(430, 80, ['Áp suất khí quyển hướng lên', 'lớn hơn áp suất do cột nước', 'gây ra nên nước không rơi,', 'dù tấm nylon chỉ đậy kín.'], w=270, size=14, lh=24))
    return svg(720, 292, ''.join(b))


def fig_noi_chim():
    b = [title(720, 'Điều kiện nổi, chìm của vật trong chất lỏng')]
    xs = [120, 360, 600]
    specs = [(205, 40, 16, 'P > F_A', 'vật chìm'), (150, 30, 30, 'P = F_A', 'vật lơ lửng'), (140, 20, 44, 'P < F_A', 'vật nổi lên')]
    for cx, (cy, lp, lf, cond, name) in zip(xs, specs):
        b.append(tank(cx - 80, 50, 160, 200, 0.8, fill=WATER))
        b.append(L(cx - 86, 90, cx + 86, 90, stroke=BLUE, w=1.4, dash='4 3'))
        b.append(R(cx - 18, cy - 18, 36, 36, fill='#f7c58a', stroke=INK, sw=2.2))
        b.append(force(cx - 8, cy, 0, lp, None, col=RED, w=2.4))
        b.append(H(cx - 24, cy + lp, 'P', size=14, fill=RED, anchor='end'))
        b.append(force(cx + 8, cy, 0, -lf, None, col=BLUE, w=2.4))
        b.append(H(cx + 24, cy - lf + 6, 'F_A', size=14, fill=BLUE, anchor='start'))
        b.append(T(cx, 280, cond, size=16, weight='bold'))
        b.append(T(cx, 302, name, size=14))
    return svg(720, 318, ''.join(b))


def spring_scale(cx, top, reading_n, label=None):
    o = [R(cx - 22, top, 44, 150, fill='white', stroke=INK, sw=2.2, rx=4), L(cx, top - 16, cx, top, w=3), C(cx, top - 20, 5, fill='none', stroke=INK, w=2)]
    for n in range(0, 7):
        y = top + 14 + n * 20
        o.append(L(cx - 22, y, cx - 10, y, w=1.6))
        o.append(T(cx - 28, y + 4, str(n), size=11, anchor='end'))
    py = top + 14 + reading_n * 20
    o.append(L(cx - 22, py, cx + 22, py, stroke=RED, w=2.4))
    o.append(L(cx, top + 150, cx, top + 170, w=2.4))
    return ''.join(o)


def fig_luc_ke():
    b = [title(720, 'Đo lực đẩy Archimedes bằng lực kế')]
    top = 66
    b.append(spring_scale(170, top, 5))
    b.append(R(150, top + 170, 40, 36, fill='#8d99a6', stroke=INK, sw=2.2))
    b.append(T(170, top + 236, 'Ngoài không khí', size=14, weight='bold'))
    b.append(T(170, top + 258, 'P = 5 N', size=15, fill=RED, weight='bold'))
    b.append(spring_scale(490, top, 3))
    b.append(R(421, top + 176, 138, 120, fill=WATER, stroke='none', sw=0))
    b.append(L(420, top + 176, 420, top + 296, w=2.6)); b.append(L(560, top + 176, 560, top + 296, w=2.6)); b.append(L(420, top + 296, 560, top + 296, w=2.6))
    b.append(L(490, top + 150, 490, top + 200, w=2.4))
    b.append(R(470, top + 200, 40, 36, fill='#8d99a6', stroke=INK, sw=2.2))
    b.append(T(490, top + 326, 'Nhúng trong nước', size=14, weight='bold'))
    b.append(T(490, top + 348, 'F = 3 N', size=15, fill=RED, weight='bold'))
    b.append(card_text(560, 76, ['Lực đẩy Archimedes:', 'F_A = P − F', '= 5 − 3 = 2 N'], w=150, size=13, lh=24))
    return svg(720, 440, ''.join(b))


def fig_moment():
    b = [title(720, 'Cùng một lực, càng xa trục quay thì tác dụng làm quay càng lớn')]
    for oy, d, cap in ((90, 260, 'Lực đặt xa bản lề (d lớn): dễ mở cửa'), (230, 80, 'Lực đặt gần bản lề (d nhỏ): khó mở cửa')):
        hx = 100
        b.append(R(hx, oy - 6, 340, 12, fill='#d9b382', stroke=INK, sw=2))
        b.append(C(hx, oy, 8, fill=INK, stroke=INK, w=1))
        b.append(T(hx - 14, oy + 5, 'O (bản lề)', size=13, weight='bold', anchor='end'))
        fx = hx + d
        b.append(force(fx, oy, 0, -44, 'F', col=RED, lx=14, w=2.6))
        b.append(L(hx, oy + 24, fx, oy + 24, stroke=BLUE, w=1.8, arrow=True))
        b.append(L(fx, oy + 24, hx, oy + 24, stroke=BLUE, w=1.8, arrow=True))
        b.append(H((hx + fx) / 2, oy + 42, 'd', size=15, fill=BLUE))
        b.append(T(570, oy + 4, cap, size=13, anchor='middle'))
    b.append(T(360, 316, 'Moment lực M = F · d', size=15, weight='bold'))
    return svg(720, 332, ''.join(b))


def fig_don_bay():
    b = [title(720, 'Đòn bẩy: điểm tựa O, các lực và khoảng cách đến điểm tựa')]
    y = 170
    # loại 1
    b.append(T(190, 56, 'Loại 1: điểm tựa O ở giữa hai lực', size=14, weight='bold'))
    b.append(R(40, y - 6, 300, 12, fill='#d9b382', stroke=INK, sw=2))
    b.append(POLY([(190, y + 6), (172, y + 44), (208, y + 44)], fill=GREY, stroke=INK, sw=2))
    b.append(T(190, y + 64, 'O', size=15, weight='bold'))
    b.append(force(130, y + 6, 0, 60, None, col=RED, w=2.6)); b.append(H(146, y + 46, 'F₁', size=15, fill=RED, anchor='start'))
    b.append(force(310, y + 6, 0, 30, None, col=RED, w=2.6)); b.append(H(326, y + 30, 'F₂', size=15, fill=RED, anchor='start'))
    for a, c, nm in ((130, 190, 'd₁'), (190, 310, 'd₂')):
        b.append(L(a, y - 30, c, y - 30, stroke=BLUE, w=1.6, arrow=True)); b.append(L(c, y - 30, a, y - 30, stroke=BLUE, w=1.6, arrow=True))
        b.append(H((a + c) / 2, y - 38, nm, size=13, fill=BLUE))
    b.append(T(190, 282, 'F₁·d₁ = F₂·d₂ (cân bằng)', size=13.5))
    # loại 2
    b.append(T(520, 56, 'Loại 2: điểm tựa O ngoài khoảng giữa hai lực', size=14, weight='bold'))
    b.append(R(400, y - 6, 240, 12, fill='#d9b382', stroke=INK, sw=2))
    b.append(POLY([(400, y + 6), (382, y + 44), (418, y + 44)], fill=GREY, stroke=INK, sw=2))
    b.append(T(400, y + 64, 'O', size=15, weight='bold'))
    b.append(force(460, y + 6, 0, 60, None, col=RED, w=2.6)); b.append(H(476, y + 46, 'F₁', size=15, fill=RED, anchor='start'))
    b.append(force(580, y - 6, 0, -20, None, col=RED, w=2.6)); b.append(H(596, y - 14, 'F₂', size=15, fill=RED, anchor='start'))
    b.append(L(400, y - 30, 460, y - 30, stroke=BLUE, w=1.6, arrow=True)); b.append(L(460, y - 30, 400, y - 30, stroke=BLUE, w=1.6, arrow=True))
    b.append(H(430, y - 38, 'd₁', size=13, fill=BLUE))
    b.append(L(400, y - 64, 580, y - 64, stroke=BLUE, w=1.6, arrow=True)); b.append(L(580, y - 64, 400, y - 64, stroke=BLUE, w=1.6, arrow=True))
    b.append(H(490, y - 72, 'd₂', size=13, fill=BLUE))
    b.append(T(520, 282, 'F₂ ở xa O hơn F₁ nên F₂ < F₁ (lợi về lực)', size=13.5))
    return svg(720, 300, ''.join(b))


def fig_nhiem_dien():
    b = [title(720, 'Nguyên tử và sự nhiễm điện do cọ xát')]
    cx, cy = 130, 150
    for rr in (30, 55, 80):
        b.append(ELL(cx, cy, rr, rr, fill='none', stroke=GREY, w=1.4))
    b.append(C(cx, cy, 14, fill=RED, stroke=INK, w=1.6)); b.append(T(cx, cy + 5, '+', size=17, weight='bold', fill='white'))
    for rr, a in ((30, 40), (55, 160), (80, 280), (55, 300), (80, 100)):
        x, y = pt(cx, cy, rr, a)
        b.append(C(x, y, 8, fill=BLUE, stroke=INK, w=1.4)); b.append(T(x, y + 5, '−', size=14, weight='bold', fill='white'))
    b.append(T(cx, 258, 'Hạt nhân mang điện dương (+),', size=13)); b.append(T(cx, 276, 'electron mang điện âm (−)', size=13))
    # thanh thuỷ tinh và lụa
    b.append(R(300, 90, 180, 24, fill='#dcecf7', stroke=INK, sw=2.2, rx=10))
    b.append(T(390, 80, 'Thanh thuỷ tinh (+)', size=14, weight='bold'))
    for k in range(5):
        b.append(T(318 + k * 36, 108, '+', size=15, weight='bold', fill=RED))
    b.append(R(300, 190, 180, 24, fill='#f0d7e6', stroke=INK, sw=2.2, rx=10))
    b.append(T(390, 238, 'Mảnh lụa (−)', size=14, weight='bold'))
    for k in range(5):
        b.append(T(318 + k * 36, 208, '−', size=15, weight='bold', fill=BLUE))
    b.append(L(390, 118, 390, 186, stroke=BLUE, w=2.4, arrow=True))
    b.append(H(432, 156, 'electron', size=13, fill=BLUE, anchor='start'))
    b.append(card_text(530, 70, ['Cọ xát thuỷ tinh', 'với lụa: electron', 'chuyển từ thuỷ tinh', 'sang lụa.', '', 'Thuỷ tinh thiếu', 'electron → mang (+);', 'lụa thừa electron', '→ mang (−).'], w=176, size=13, lh=22))
    return svg(720, 292, ''.join(b))


def fig_ki_hieu_mach():
    b = [title(720, 'Kí hiệu trong sơ đồ mạch điện')]
    names = ['Nguồn điện (pin)', 'Bóng đèn', 'Công tắc đóng', 'Công tắc mở', 'Dây dẫn', 'Điện trở', 'Ampe kế', 'Vôn kế']
    for i, n in enumerate(names):
        col, row = i % 4, i // 4
        cx, cy = 90 + col * 180, 90 + row * 120
        b.append(R(cx - 78, cy - 40, 156, 96, fill=LGREY, stroke=GREY, sw=1, rx=8))
        if i == 0:
            b.append(L(cx - 50, cy, cx - 6, cy, w=2)); b.append(battery(cx, cy)); b.append(L(cx + 6, cy, cx + 50, cy, w=2))
        elif i == 1:
            b.append(L(cx - 50, cy, cx - 16, cy, w=2)); b.append(bulb(cx, cy, 16)); b.append(L(cx + 16, cy, cx + 50, cy, w=2))
        elif i == 2:
            b.append(L(cx - 50, cy, cx - 18, cy, w=2)); b.append(switch(cx, cy, True)); b.append(L(cx + 18, cy, cx + 50, cy, w=2))
        elif i == 3:
            b.append(L(cx - 50, cy, cx - 18, cy, w=2)); b.append(switch(cx, cy, False)); b.append(L(cx + 18, cy, cx + 50, cy, w=2))
        elif i == 4:
            b.append(L(cx - 54, cy, cx + 54, cy, w=2.4))
        elif i == 5:
            b.append(L(cx - 50, cy, cx - 22, cy, w=2)); b.append(resistor(cx, cy)); b.append(L(cx + 22, cy, cx + 50, cy, w=2))
        elif i == 6:
            b.append(L(cx - 50, cy, cx - 15, cy, w=2)); b.append(meter(cx, cy, 'A')); b.append(L(cx + 15, cy, cx + 50, cy, w=2))
        else:
            b.append(L(cx - 50, cy, cx - 15, cy, w=2)); b.append(meter(cx, cy, 'V')); b.append(L(cx + 15, cy, cx + 50, cy, w=2))
        b.append(T(cx, cy + 40, n, size=13, weight='bold'))
    return svg(720, 290, ''.join(b))


def fig_mach_do():
    b = [title(720, 'Mạch điện đo cường độ dòng điện và hiệu điện thế')]
    x1, x2, y1, y2 = 90, 500, 80, 230
    b.append(L(x1, y1, 130, y1, w=2.4)); b.append(switch(150, y1, True)); b.append(L(168, y1, 270, y1, w=2.4))
    b.append(L(270, y1, 294, y1, w=2.4)); b.append(bulb(310, y1, 16, on=True)); b.append(L(326, y1, x2, y1, w=2.4))
    b.append(L(x2, y1, x2, 122, w=2.4)); b.append(meter(x2, 138, 'A')); b.append(L(x2, 153, x2, y2, w=2.4))
    b.append(L(x2, y2, 330, y2, w=2.4)); b.append(battery(310, y2)); b.append(L(290, y2, x1, y2, w=2.4)); b.append(L(x1, y2, x1, y1, w=2.4))
    # vôn kế song song với đèn
    b.append(L(270, y1, 270, 34, w=2.4)); b.append(L(270, 34, 295, 34, w=2.4)); b.append(meter(310, 34, 'V')); b.append(L(325, 34, 350, 34, w=2.4)); b.append(L(350, 34, 350, y1, w=2.4))
    b.append(dot(270, y1, 4)); b.append(dot(350, y1, 4))
    b.append(L(x1 + 18, 200, x1 + 18, 130, stroke=RED, w=2, arrow=True)); b.append(L(180, y1 + 18, 240, y1 + 18, stroke=RED, w=2, arrow=True))
    b.append(L(x2 - 18, 180, x2 - 18, 120, stroke=RED, w=2, arrow=True) if False else L(x2 + 18, 120, x2 + 18, 180, stroke=RED, w=2, arrow=True))
    b.append(T(210, y1 + 44, 'chiều dòng điện', size=12.5, fill=RED))
    b.append(H(x2 + 22, 128, '+', size=15, fill=INK, anchor='start') if False else '')
    b.append(card_text(552, 40, ['Ampe kế A mắc', 'nối tiếp với đèn.', '', 'Vôn kế V mắc', 'song song với đèn.', '', 'Dòng điện đi vào', 'chốt (+) của mỗi', 'dụng cụ đo.'], w=150, size=12.5, lh=21))
    return svg(720, 262, ''.join(b))


def fig_chuyen_dong_nhiet():
    b = [title(720, 'Chuyển động nhiệt của các phân tử')]
    rnd = random.Random(3)
    pos = [(rnd.uniform(24, 276), rnd.uniform(34, 176), rnd.uniform(0, 360)) for _ in range(14)]
    for ox, name, ln, col in ((30, 'Nhiệt độ thấp: phân tử chuyển động chậm', 14, '#dbe7f3'), (390, 'Nhiệt độ cao: phân tử chuyển động nhanh', 30, '#fbe3d0')):
        b.append(R(ox, 50, 300, 210, fill=col, stroke=INK, sw=2.2, rx=6))
        for x, y, a in pos:
            px, py = ox + x, 50 + y + 10
            b.append(C(px, py, 8, fill=BLUE if ln < 20 else RED, stroke=INK, w=1.4))
            ex, ey = px + ln * math.cos(math.radians(a)), py - ln * math.sin(math.radians(a))
            b.append(L(px, py, ex, ey, stroke=INK, w=1.6, arrow=True))
        b.append(T(ox + 150, 286, name, size=13.5, weight='bold'))
    return svg(720, 302, ''.join(b))


def fig_truyen_nhiet():
    b = [title(720, 'Ba hình thức truyền nhiệt')]
    # dẫn nhiệt
    b.append(R(30, 120, 190, 22, fill='#e2a76f', stroke=INK, sw=2.2, rx=2))
    b.append(flame_icon(36, 168, 1.1))
    b.append(L(70, 108, 190, 108, stroke=RED, w=2.2, arrow=True))
    b.append(T(125, 98, 'nhiệt truyền dọc thanh', size=12, fill=RED))
    b.append(T(125, 214, 'Dẫn nhiệt', size=15, weight='bold'))
    b.append(T(125, 234, '(chất rắn)', size=12.5, fill=GREY))
    # đối lưu
    cx = 360
    b.append(tank(cx - 70, 70, 140, 130, 0.9, fill=WATER))
    b.append(flame_icon(cx, 220, 1.2))
    b.append(L(cx, 190, cx, 100, stroke=RED, w=2.2, arrow=True))
    b.append(L(cx - 55, 100, cx - 55, 180, stroke=BLUE, w=2.2, arrow=True)); b.append(L(cx + 55, 100, cx + 55, 180, stroke=BLUE, w=2.2, arrow=True))
    b.append(PL([(cx, 100), (cx - 30, 84), (cx - 55, 100)], stroke=GREY, w=1.4, dash='3 3')); b.append(PL([(cx, 100), (cx + 30, 84), (cx + 55, 100)], stroke=GREY, w=1.4, dash='3 3'))
    b.append(T(cx, 266, 'Đối lưu', size=15, weight='bold'))
    b.append(T(cx, 286, '(chất lỏng, chất khí)', size=12.5, fill=GREY))
    # bức xạ
    b.append(C(560, 100, 26, fill='#ffd84d', stroke=ORANGE, w=2.4))
    for (xa, ya, xb, yb) in ((600, 92, 650, 136), (590, 108, 642, 150), (584, 124, 634, 166)):
        b.append(L(xa, ya, xb, yb, stroke='#e8b92f', w=2, arrow=True))
    b.append(C(680, 170, 22, fill='#4e9be0', stroke=INK, w=2))
    b.append(T(620, 214, 'Bức xạ nhiệt', size=15, weight='bold'))
    b.append(T(620, 234, '(truyền qua chân không)', size=12.5, fill=GREY))
    return svg(720, 300, ''.join(b))


def fig_bang_kep():
    b = [title(720, 'Băng kép: khi nóng, băng kép cong về phía thanh nở ít hơn')]
    b.append(R(60, 120, 240, 16, fill='#9aa5b1', stroke=INK, sw=2))
    b.append(R(60, 136, 240, 16, fill='#e2a76f', stroke=INK, sw=2))
    b.append(T(180, 106, 'Sắt (nở ít)', size=13, fill=GREY, weight='bold'))
    b.append(T(180, 176, 'Đồng (nở nhiều)', size=13, fill='#b8651b', weight='bold'))
    b.append(T(180, 236, 'Ở nhiệt độ thường: thẳng', size=14, weight='bold'))
    cx, cy = 540, 40
    for r_, col in ((150, '#e2a76f'), (134, '#9aa5b1')):
        dx, dy = r_ * math.sin(math.radians(40)), r_ * math.cos(math.radians(40))
        b.append('<path d="M%.1f,%.1f A%d,%d 0 0 0 %.1f,%.1f" fill="none" stroke="%s" stroke-width="16"/>' % (cx - dx, cy + dy, r_, r_, cx + dx, cy + dy, col))
    b.append(flame_icon(cx, 258, 1.2))
    b.append(T(cx, 222, 'Đồng (ngoài chỗ cong)', size=13, fill='#b8651b', weight='bold'))
    b.append(T(cx, 112, 'Sắt (trong chỗ cong)', size=13, fill=GREY, weight='bold'))
    b.append(T(cx, 300, 'Khi bị nung nóng: cong về phía thanh nở ít (sắt)', size=14, weight='bold'))
    return svg(720, 316, ''.join(b))


def fig_nuoc_4c():
    b = [title(720, 'Nước nở vì nhiệt đặc biệt (sơ đồ minh hoạ)')]
    ox, oy = 90, 230
    b.append(L(ox, oy, 560, oy, w=1.8, arrow=True)); b.append(L(ox, oy, ox, 50, w=1.8, arrow=True))
    b.append(T(570, oy + 5, 't (°C)', size=13, anchor='start', weight='bold'))
    b.append(T(ox + 6, 52, 'Thể tích của 1 kg nước', size=13, anchor='start', weight='bold'))
    pts = [(ox + 30 + t * 44, oy - 40 - 5.4 * (t - 4) ** 2 * 0.0 - (0.0)) for t in range(0)]
    curve = [(ox + 30 + t * 4.3, 90 + 0.62 * (t - 4) ** 2 * 1.0) for t in [i / 10 for i in range(0, 101)]]
    b.append(PL([(ox + 30 + t * 44, 176 - 4.4 * (t - 4) ** 2) for t in [i / 20 for i in range(0, 181)]], stroke=BLUE, w=3))
    for t in (0, 4, 8):
        x = ox + 30 + t * 44
        b.append(L(x, oy - 4, x, oy + 4, w=1.6)); b.append(T(x, oy + 22, str(t), size=13))
    b.append(L(ox + 30 + 4 * 44, 176, ox + 30 + 4 * 44, oy, stroke=RED, w=1.4, dash='5 4'))
    b.append(dot(ox + 30 + 4 * 44, 176, 5, RED))
    b.append(H(ox + 30 + 4 * 44 + 14, 202, 'ở 4 °C: thể tích nhỏ nhất,', size=13, fill=RED, anchor='start'))
    b.append(H(ox + 30 + 4 * 44 + 14, 220, 'khối lượng riêng lớn nhất', size=13, fill=RED, anchor='start'))
    b.append(T(ox + 30 + 1.3 * 44, 70, '0–4 °C: nóng lên thì co lại', size=12.5, fill=GREY))
    b.append(T(ox + 30 + 6.6 * 44, 70, 'trên 4 °C: nóng lên thì nở ra', size=12.5, fill=GREY))
    return svg(720, 262, ''.join(b))


# ======================================================================= Lí 9
def fig_co_nang():
    b = [title(720, 'Con lắc đơn: động năng và thế năng chuyển hoá, cơ năng không đổi')]
    px, py, Lh = 190, 44, 160
    angs = [-50, -25, 0]
    names = ['A', 'M', 'B']
    full = 1 - math.cos(math.radians(50))
    b.append(L(px - 40, py, px + 40, py, w=3))
    b.append(PATH('M%.1f,%.1f A%d,%d 0 0 0 %.1f,%.1f' % (px + Lh * math.sin(math.radians(-50)), py + Lh * math.cos(math.radians(-50)), Lh, Lh, px + Lh * math.sin(math.radians(50)), py + Lh * math.cos(math.radians(50))), stroke=GREY, w=1.2))
    rows = []
    for a, n in zip(angs, names):
        x, y = px + Lh * math.sin(math.radians(a)), py + Lh * math.cos(math.radians(a))
        b.append(L(px, py, x, y, stroke=GREY, w=1.4))
        b.append(C(x, y, 11, fill='#ee6a5a', stroke=INK, w=2))
        b.append(H(x + (-22 if a < 0 else 22), y + 22, n, size=15, anchor='middle'))
        wt = (1 - math.cos(math.radians(a))) / full
        rows.append((n, wt, 1 - wt))
    b.append(L(px, py, px, py + Lh + 20, stroke=GREY, w=1, dash='4 4'))
    for i, (n, wt, wd) in enumerate(rows):
        y = 70 + i * 76
        b.append(T(370, y + 30, n, size=17, weight='bold', anchor='end'))
        for j, (lab, val, col) in enumerate((('Wt', wt, BLUE), ('Wđ', wd, ORANGE), ('W', 1.0, GREEN))):
            b.append(T(402, y + 14 + j * 22 - 2, lab, size=12, anchor='end', weight='bold', fill=col))
            b.append(R(408, y + j * 22 + 2, max(1, 270 * val), 14, fill=col, stroke=col, sw=1))
    b.append(T(540, 322, 'Bỏ qua ma sát: W = Wđ + Wt luôn không đổi', size=13.5, fill=GREY))
    return svg(720, 336, ''.join(b))


def person(x, y, s=1.0):
    return (C(x, y - 62 * s, 10 * s, fill='#f7c58a', stroke=INK, w=2) + L(x, y - 52 * s, x, y - 18 * s, w=3)
            + L(x, y - 18 * s, x - 10 * s, y, w=3) + L(x, y - 18 * s, x + 10 * s, y, w=3))


def fig_cong():
    b = [title(720, 'Điều kiện để lực thực hiện công')]
    gy = 190
    b.append(ground(30, 340, gy))
    b.append(R(110, 140, 70, 50, fill='#c9dcee', stroke=INK, sw=2.2))
    b.append(force(180, 165, 70, 0, 'F', col=RED, ly=-14))
    b.append(L(110, 214, 250, 214, stroke=BLUE, w=1.8, arrow=True))
    b.append(H(180, 232, 's', size=15, fill=BLUE))
    b.append(T(190, 266, 'F cùng phương với dịch chuyển', size=13.5, weight='bold'))
    b.append(T(190, 286, '→ có công: A = F·s', size=13.5, fill=GREEN, weight='bold'))
    b.append(ground(390, 700, gy))
    b.append(person(470, gy))
    b.append(R(488, 138, 30, 22, fill='#b9855b', stroke=INK, sw=2))
    b.append(L(470, 130, 500, 138, w=2))
    b.append(force(503, 138, 0, -48, 'F', col=RED, lx=14))
    b.append(L(450, 214, 600, 214, stroke=BLUE, w=1.8, arrow=True))
    b.append(H(525, 232, 's', size=15, fill=BLUE))
    b.append(T(545, 266, 'F vuông góc với dịch chuyển', size=13.5, weight='bold'))
    b.append(T(545, 286, '→ lực F không sinh công', size=13.5, fill=RED, weight='bold'))
    return svg(720, 304, ''.join(b))


def fig_khuc_xa():
    b = [title(720, 'Khúc xạ ánh sáng: n₁ = 1 (không khí), n₂ = 1,5 (thuỷ tinh)')]
    ox, oy = 280, 150
    b.append(R(40, oy, 480, 130, fill='#dff0fa', stroke='none', sw=0))
    b.append(L(40, oy, 520, oy, w=2.4))
    b.append(L(ox, 40, ox, 270, stroke=GREY, w=1.6, dash='6 4'))
    b.append(T(ox + 8, 52, 'pháp tuyến', size=12.5, anchor='start', fill=GREY))
    i = 45.0
    r = math.degrees(math.asin(math.sin(math.radians(i)) / 1.5))
    sx, sy = ox - 120 * math.sin(math.radians(i)), oy - 120 * math.cos(math.radians(i))
    b.append(L(sx, sy, ox, oy, stroke=RED, w=2.6, arrow=True))
    ex, ey = ox + 110 * math.sin(math.radians(r)), oy + 110 * math.cos(math.radians(r))
    b.append(L(ox, oy, ex, ey, stroke=BLUE, w=2.6, arrow=True))
    rx, ry = ox + 90 * math.sin(math.radians(i)), oy - 90 * math.cos(math.radians(i))
    b.append(L(ox, oy, rx, ry, stroke=GREY, w=1.4, dash='4 3', arrow=True))
    b.append(ARC(ox, oy, 46, 90, 90 + 0, stroke=RED, w=0))
    b.append(ARC(ox, oy, 52, 90 - 0, 90 + i, stroke=RED, w=1.8))
    b.append(H(ox - 30, oy - 62, 'i', size=16, fill=RED))
    b.append(ARC(ox, oy, 56, -90 - r, -90, stroke=BLUE, w=1.8))
    b.append(H(ox + 22, oy + 74, 'r', size=16, fill=BLUE))
    b.append(T(70, 76, 'Môi trường 1 (n₁ = 1)', size=13.5, anchor='start', weight='bold'))
    b.append(T(70, 262, 'Môi trường 2 (n₂ = 1,5)', size=13.5, anchor='start', weight='bold'))
    b.append(H(sx + 4, sy - 8, 'tia tới', size=13, fill=RED, anchor='start'))
    b.append(H(ex + 8, ey, 'tia khúc xạ', size=13, fill=BLUE, anchor='start'))
    b.append(card_text(545, 80, ['n₁·sin i = n₂·sin r', '', 'i = 45°:', 'sin r = sin 45° : 1,5', '≈ 0,471', 'r ≈ 28,1° < i', '', 'Tia khúc xạ lệch', 'lại gần pháp tuyến.'], w=170, size=12.5, lh=21))
    return svg(720, 292, ''.join(b))


def fig_phan_xa_toan_phan():
    b = [title(720, 'Ánh sáng đi từ thuỷ tinh (n₁ = 1,5) ra không khí (n₂ = 1):  i_th ≈ 41,8°')]
    ith = math.degrees(math.asin(1 / 1.5))
    cases = [(120, 30.0, 'i < i_th', 'có tia khúc xạ và tia phản xạ'), (360, ith, 'i = i_th', 'tia khúc xạ sát mặt phân cách'), (600, 60.0, 'i > i_th', 'phản xạ toàn phần')]
    oy = 140
    for ox, i, cap, sub in cases:
        b.append(R(ox - 110, oy, 220, 100, fill='#dff0fa', stroke='none', sw=0))
        b.append(L(ox - 110, oy, ox + 110, oy, w=2.4))
        b.append(L(ox, 50, ox, 240, stroke=GREY, w=1.4, dash='6 4'))
        sx, sy = ox - 90 * math.sin(math.radians(i)), oy + 90 * math.cos(math.radians(i))
        b.append(L(sx, sy, ox, oy, stroke=RED, w=2.4, arrow=True))
        s = 1.5 * math.sin(math.radians(i))
        if s < 0.9999:
            r = math.degrees(math.asin(min(1, s)))
            b.append(L(ox, oy, ox + 90 * math.sin(math.radians(r)), oy - 90 * math.cos(math.radians(r)), stroke=BLUE, w=2.4, arrow=True))
            b.append(L(ox, oy, ox + 55 * math.sin(math.radians(i)), oy + 55 * math.cos(math.radians(i)), stroke=GREY, w=1.2, dash='4 3', arrow=True)) if i < ith - 1 else None
        elif i <= ith + 0.01:
            b.append(L(ox, oy, ox + 95, oy - 2, stroke=BLUE, w=2.4, arrow=True))
        else:
            pass
        if i > ith + 0.01:
            b.append(L(ox, oy, ox + 90 * math.sin(math.radians(i)), oy + 90 * math.cos(math.radians(i)), stroke=GREEN, w=2.8, arrow=True))
        elif i >= ith - 0.01:
            pass
        b.append(H(ox - 70, oy + 100 - 8, 'thuỷ tinh', size=12, fill=GREY, weight='normal') if False else '')
        b.append(T(ox, 266, cap, size=15, weight='bold'))
        b.append(T(ox, 286, sub, size=12.5))
    b.append(T(70, 60, 'không khí', size=12, anchor='start', fill=GREY)); b.append(T(70, 232, 'thuỷ tinh', size=12, anchor='start', fill=GREY))
    return svg(720, 304, ''.join(b))


def fig_lang_kinh():
    b = [title(720, 'Lăng kính tán sắc ánh sáng trắng')]
    A, B_, C_ = (300, 60), (220, 200), (380, 200)
    b.append(POLY([A, B_, C_], fill='#dbeaf5', stroke=INK, sw=2.4))
    P = (A[0] + (B_[0] - A[0]) * 0.5, A[1] + (B_[1] - A[1]) * 0.5)
    Q = (A[0] + (C_[0] - A[0]) * 0.5, A[1] + (C_[1] - A[1]) * 0.5)
    b.append(L(60, P[1] + 28, P[0], P[1], stroke='#7d8794', w=3.2))
    b.append(L(P[0], P[1], Q[0], Q[1], stroke='#7d8794', w=2.4))
    cols = [('đỏ', '#e53935', 9), ('da cam', '#fb8c00', 11.5), ('vàng', '#f6c600', 14), ('lục', '#43a047', 16.5), ('lam', '#1e88e5', 19), ('chàm', '#3949ab', 21.5), ('tím', '#8e24aa', 24)]
    for k, (nm, col, ang) in enumerate(cols):
        ex, ey = Q[0] + 250 * math.cos(math.radians(ang)), Q[1] + 250 * math.sin(math.radians(ang))
        b.append(L(Q[0], Q[1], ex, ey, stroke=col, w=2.6))
    b.append(L(600, 60, 600, 280, stroke=GREY, w=2))
    for k, (nm, col, ang) in enumerate(cols):
        yy = Q[1] + 220 * math.tan(math.radians(ang))
        pass
    b.append(T(110, P[1] + 8, 'Ánh sáng trắng', size=13.5, weight='bold'))
    b.append(H(600 + 8, Q[1] + 255 * math.sin(math.radians(9)) + 14, 'đỏ', size=13, fill='#e53935', anchor='start'))
    b.append(H(600 + 8, Q[1] + 255 * math.sin(math.radians(24)) + 24, 'tím', size=13, fill='#8e24aa', anchor='start'))
    b.append(T(300, 232, 'Lăng kính', size=14, weight='bold'))
    b.append(T(560, 296, 'Đỏ lệch ít nhất, tím lệch nhiều nhất', size=13.5, fill=GREY))
    return svg(720, 316, ''.join(b))


def lens_shape(x, y0, hh=90):
    return PATH('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z' % (x, y0 - hh, x + 24, y0, x, y0 + hh, x - 24, y0, x, y0 - hh), fill='#cfe6f7', stroke=INK, w=2.2)


def fig_thau_kinh_that():
    b = [title(720, 'Ảnh thật qua thấu kính hội tụ (d = 90 > f = 60): ảnh ngược chiều')]
    lx, y0, f, d, h = 400, 150, 60, 90, 40
    b.append(L(40, y0, 680, y0, w=1.6, stroke=GREY))
    b.append(lens_shape(lx, y0))
    for xx, nm in ((lx - f, 'F'), (lx + f, "F′")):
        b.append(dot(xx, y0, 4)); b.append(T(xx, y0 + 20, nm, size=14, weight='bold'))
    b.append(T(lx, y0 + 108, 'O', size=14, weight='bold'))
    ox_ = lx - d
    b.append(L(ox_, y0, ox_, y0 - h, stroke=BLUE, w=3, arrow=True))
    b.append(T(ox_, y0 + 20, 'AB', size=14, weight='bold', fill=BLUE)) if False else b.append(H(ox_ - 10, y0 - h - 6, 'B', size=14, fill=BLUE))
    b.append(H(ox_ - 10, y0 + 18, 'A', size=14, fill=BLUE))
    dp = 180
    ix = lx + dp
    b.append(L(ix, y0, ix, y0 + 2 * h, stroke=RED, w=3, arrow=True))
    b.append(H(ix + 12, y0 + 2 * h + 4, "B′", size=14, fill=RED, anchor='start'))
    b.append(H(ix + 12, y0 - 8, "A′", size=14, fill=RED, anchor='start'))
    top = (ox_, y0 - h)
    b.append(PL([top, (lx, y0 - h), (ix, y0 + 2 * h)], stroke=ORANGE, w=1.8))
    b.append(L(top[0], top[1], ix, y0 + 2 * h, stroke=GREEN, w=1.8))
    b.append(PL([top, (lx, y0 + 2 * h), (ix, y0 + 2 * h)], stroke=BLUE, w=1.8))
    b.append(T(360, 270, 'Ba tia đặc biệt: song song trục → qua F′; qua O → thẳng; qua F → song song trục', size=12.5, fill=GREY))
    b.append(T(360, 288, '', size=12.5))
    return svg(720, 304, ''.join(b))


def fig_thau_kinh_ao():
    b = [title(720, 'Ảnh ảo qua thấu kính hội tụ (d = 30 < f = 60): ảnh cùng chiều, lớn hơn vật')]
    lx, y0, f, d, h = 400, 170, 60, 30, 30
    b.append(L(40, y0, 680, y0, w=1.6, stroke=GREY))
    b.append(lens_shape(lx, y0))
    for xx, nm in ((lx - f, 'F'), (lx + f, "F′")):
        b.append(dot(xx, y0, 4)); b.append(T(xx, y0 + 20, nm, size=14, weight='bold'))
    b.append(T(lx, y0 + 108, 'O', size=14, weight='bold'))
    ox_ = lx - d
    b.append(L(ox_, y0, ox_, y0 - h, stroke=BLUE, w=3, arrow=True))
    b.append(H(ox_ + 6, y0 - h - 8, 'B', size=14, fill=BLUE, anchor='start'))
    b.append(H(ox_ + 6, y0 + 18, 'A', size=14, fill=BLUE, anchor='start'))
    ix, ih = lx - 60, 2 * h
    b.append(L(ix, y0, ix, y0 - ih, stroke=RED, w=2.4, dash='5 4', arrow=True))
    b.append(H(ix - 10, y0 - ih + 4, "B′", size=14, fill=RED, anchor='end'))
    b.append(H(ix - 8, y0 + 18, "A′", size=14, fill=RED, anchor='end'))
    top = (ox_, y0 - h)
    b.append(PL([top, (lx, y0 - h), (lx + 160, y0 - h + 80)], stroke=ORANGE, w=1.8))
    b.append(L(lx, y0 - h, ix, y0 - ih, stroke=ORANGE, w=1.4, dash='5 4'))
    b.append(L(top[0], top[1], lx + 100, y0 + 100 - 0, stroke=BLUE, w=1.8))
    b.append(L(top[0], top[1], ix, y0 - ih, stroke=BLUE, w=1.4, dash='5 4'))
    b.append(T(360, 300, 'Các tia ló phân kì; kéo dài ngược lại gặp nhau tại B′ (ảnh ảo)', size=12.5, fill=GREY))
    return svg(720, 316, ''.join(b))


def fig_ohm():
    b = [title(720, 'Đồ thị cường độ dòng điện theo hiệu điện thế (R = 10 Ω)')]
    ox, oy = 90, 300
    ux, iy = 48, 330
    b.append(L(ox, oy, ox + 6.6 * ux, oy, w=1.8, arrow=True)); b.append(L(ox, oy, ox, oy - 0.68 * iy, w=1.8, arrow=True))
    b.append(T(ox + 6.6 * ux + 14, oy + 18, 'U (V)', size=13, weight='bold')); b.append(T(ox + 8, oy - 0.68 * iy - 4, 'I (A)', size=13, weight='bold', anchor='start'))
    b.append(T(ox - 9, oy + 16, 'O', size=13))
    for u in (2, 4, 6):
        b.append(L(ox + u * ux, oy - 4, ox + u * ux, oy + 4, w=1.5)); b.append(T(ox + u * ux, oy + 20, str(u), size=13))
    for i in (0.2, 0.4, 0.6):
        b.append(L(ox - 4, oy - i * iy, ox + 4, oy - i * iy, w=1.5)); b.append(T(ox - 10, oy - i * iy + 5, ('%.1f' % i).replace('.', ','), size=13, anchor='end'))
    b.append(L(ox, oy, ox + 6.4 * ux, oy - 0.64 * iy, stroke=BLUE, w=3))
    for u in (2, 4, 6):
        b.append(dot(ox + u * ux, oy - u / 10 * iy, 4.5, RED))
        b.append(L(ox + u * ux, oy - u / 10 * iy, ox + u * ux, oy, stroke=GREY, w=1, dash='4 3'))
    b.append(card_text(440, 70, ['Đồ thị là đường thẳng', 'đi qua gốc toạ độ:', 'I tỉ lệ thuận với U.', '', 'I = U / R', 'U = 6 V → I = 0,6 A', '(R = 10 Ω)'], w=250, size=14.5, lh=24))
    return svg(720, 336, ''.join(b))


def fig_noi_tiep_song_song():
    b = [title(720, 'Đoạn mạch nối tiếp và song song')]
    # nối tiếp
    x1, x2, y1, y2 = 40, 330, 90, 220
    b.append(L(x1, y1, 130, y1, w=2.4)); b.append(resistor(160, y1)); b.append(L(182, y1, 218, y1, w=2.4)); b.append(resistor(240, y1)); b.append(L(262, y1, x2, y1, w=2.4))
    b.append(L(x2, y1, x2, y2, w=2.4)); b.append(L(x2, y2, 200, y2, w=2.4)); b.append(battery(185, y2)); b.append(L(165, y2, x1, y2, w=2.4)); b.append(L(x1, y2, x1, y1, w=2.4))
    b.append(T(160, y1 - 14, 'R₁', size=14, weight='bold')); b.append(T(240, y1 - 14, 'R₂', size=14, weight='bold'))
    b.append(T(185, 268, 'Nối tiếp', size=15, weight='bold'))
    b.append(T(185, 288, 'I chung; U = U₁ + U₂; R = R₁ + R₂', size=12.5))
    # song song
    X1, X2 = 400, 690
    b.append(L(X1, y1 + 10, X1, y2, w=2.4)); b.append(L(X1, y1 + 10, 480, y1 + 10, w=2.4))
    b.append(L(480, y1 - 30, 480, y1 + 60, w=2.4))
    b.append(L(480, y1 - 30, 520, y1 - 30, w=2.4)); b.append(resistor(550, y1 - 30)); b.append(L(572, y1 - 30, 610, y1 - 30, w=2.4))
    b.append(L(480, y1 + 60, 520, y1 + 60, w=2.4)); b.append(resistor(550, y1 + 60)); b.append(L(572, y1 + 60, 610, y1 + 60, w=2.4))
    b.append(L(610, y1 - 30, 610, y1 + 60, w=2.4)); b.append(L(610, y1 + 10, X2, y1 + 10, w=2.4)); b.append(L(X2, y1 + 10, X2, y2, w=2.4))
    b.append(L(X2, y2, 560, y2, w=2.4)); b.append(battery(545, y2)); b.append(L(525, y2, X1, y2, w=2.4))
    b.append(dot(480, y1 + 10, 4)); b.append(dot(610, y1 + 10, 4))
    b.append(T(550, y1 - 44, 'R₁', size=14, weight='bold')); b.append(T(550, y1 + 84, 'R₂', size=14, weight='bold'))
    b.append(T(545, 268, 'Song song', size=15, weight='bold'))
    b.append(T(545, 288, 'U chung; I = I₁ + I₂; 1/R = 1/R₁ + 1/R₂', size=12.5))
    return svg(720, 304, ''.join(b))


def fig_cam_ung():
    b = [title(720, 'Cảm ứng điện từ và dòng điện xoay chiều')]
    cx, cy = 150, 140
    for k in range(5):
        b.append(ELL(cx + 40 + k * 14, cy, 18, 40, fill='none', stroke='#b8651b', w=3))
    b.append(L(cx + 40, cy - 40, cx + 40, cy - 70, stroke='#b8651b', w=2.4)); b.append(L(cx + 40 + 56, cy - 40, cx + 40 + 56, cy - 70, stroke='#b8651b', w=2.4))
    b.append(L(cx + 40, cy - 70, cx + 40 + 56, cy - 70, stroke='#b8651b', w=2.4))
    b.append(L(cx + 40, cy + 40, cx + 40, cy + 70, stroke='#b8651b', w=2.4)); b.append(L(cx + 96, cy + 40, cx + 96, cy + 70, stroke='#b8651b', w=2.4))
    b.append(L(cx + 40, cy + 70, cx + 96, cy + 70, stroke='#b8651b', w=2.4)) if False else None
    b.append(R(cx - 90, cy - 16, 40, 32, fill=RED, stroke=INK, sw=2)); b.append(R(cx - 50, cy - 16, 40, 32, fill=BLUE, stroke=INK, sw=2))
    b.append(T(cx - 70, cy + 6, 'N', size=16, weight='bold', fill='white')); b.append(T(cx - 30, cy + 6, 'S', size=16, weight='bold', fill='white'))
    b.append(L(cx - 100, cy - 36, cx - 20, cy - 36, stroke=INK, w=2, arrow=True)); b.append(T(cx - 60, cy - 46, 'đưa nam châm vào', size=12.5))
    b.append(meter(cx + 68, cy + 96, 'G'))
    b.append(PL([(cx + 40, cy + 40), (cx + 40, cy + 96), (cx + 53, cy + 96)], stroke='#b8651b', w=2.4)); b.append(PL([(cx + 96, cy + 40), (cx + 96, cy + 96), (cx + 83, cy + 96)], stroke='#b8651b', w=2.4))
    b.append(T(cx + 68, cy + 130, 'Điện kế G lệch: có dòng điện cảm ứng', size=12.5)) if False else b.append(T(cx + 20, cy + 134, 'Điện kế G lệch: có dòng điện cảm ứng', size=12.5))
    ox, oy = 400, 140
    b.append(L(ox, oy, ox + 290, oy, w=1.8, arrow=True)); b.append(L(ox, oy + 80, ox, oy - 80, w=1.8, arrow=True))
    b.append(T(ox + 292, oy - 10, 't (s)', size=13, anchor='end', weight='bold')); b.append(T(ox + 8, oy - 78, 'i', size=14, weight='bold', anchor='start'))
    b.append(PL([(ox + t * 2.6, oy - 60 * math.sin(2 * math.pi * t / 100)) for t in range(0, 101)], stroke=BLUE, w=3))
    b.append(L(ox + 260, oy - 4, ox + 260, oy + 4, w=1.5)); b.append(T(ox + 260, oy + 20, '0,02', size=12.5))
    b.append(L(ox + 130, oy - 4, ox + 130, oy + 4, w=1.5)); b.append(T(ox + 130, oy + 20, '0,01', size=12.5))
    b.append(T(ox + 65, oy - 70, '+', size=18, weight='bold', fill=RED)); b.append(T(ox + 195, oy + 78, '−', size=22, weight='bold', fill=BLUE))
    b.append(T(ox + 140, 262, 'Dòng điện xoay chiều: chu kì T = 0,02 s (tần số 50 Hz)', size=13, weight='bold'))
    return svg(720, 280, ''.join(b))


def fig_vong_nang_luong():
    b = [title(720, 'Vòng năng lượng: từ Mặt Trời đến nhiên liệu hoá thạch')]
    boxes = [(75, ['Mặt Trời'], '#ffe9a8'), (255, ['Thực vật'], '#dfe9d5'), (435, ['Nhiên liệu', 'hoá thạch'], '#c8ccd2'), (615, ['Nhiệt, điện,', 'động lực'], '#fbe3d0')]
    arrows = ['quang hợp', 'chôn vùi lâu năm', 'đốt cháy']
    for x, nm, col in boxes:
        b.append(R(x - 65, 90, 130, 70, fill=col, stroke=INK, sw=2.2, rx=8))
        for j, line in enumerate(nm):
            b.append(T(x, (125 if len(nm) == 1 else 117 + 18 * j), line, size=14, weight='bold'))
    for k, nm in enumerate(arrows):
        xa, xb = boxes[k][0] + 67, boxes[k + 1][0] - 67
        b.append(L(xa, 125, xb, 125, stroke=BLUE, w=2.4, arrow=True))
        b.append(T((xa + xb) / 2, 76, nm, size=12, fill=BLUE))
    b.append(T(435, 182, '(than đá, dầu mỏ, khí tự nhiên)', size=12, fill=GREY))
    b.append(L(615, 162, 615, 214, stroke=RED, w=2.2, arrow=True))
    b.append(T(560, 238, 'thải CO₂ → hiệu ứng nhà kính', size=13, weight='bold', fill=RED))
    return svg(720, 256, ''.join(b))


def flame_icon(x, y, s=1.0, col=ORANGE):
    return PATH('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z' % (
        x, y - 16 * s, x + 14 * s, y - 2 * s, x + 12 * s, y + 14 * s, x, y + 14 * s,
        x - 12 * s, y + 14 * s, x - 14 * s, y - 2 * s, x, y - 16 * s), fill=col, stroke=INK, w=1.6)


FIGS8 = {
    'c-l8-b13-khoi-luong-rieng.svg': fig_khoi_luong_rieng,
    'c-l8-b14-the-tich-soi.svg': fig_the_tich_soi,
    'c-l8-b15-ap-suat-be-mat.svg': fig_ap_suat_be_mat,
    'c-l8-b16-ap-suat-chat-long.svg': fig_ap_suat_chat_long,
    'c-l8-b16-khi-quyen-coc.svg': fig_khi_quyen_coc,
    'c-l8-b17-noi-chim.svg': fig_noi_chim,
    'c-l8-b17-luc-ke.svg': fig_luc_ke,
    'c-l8-b18-moment.svg': fig_moment,
    'c-l8-b19-don-bay.svg': fig_don_bay,
    'c-l8-b20-nhiem-dien.svg': fig_nhiem_dien,
    'c-l8-b22-ki-hieu-mach.svg': fig_ki_hieu_mach,
    'c-l8-b25-mach-do.svg': fig_mach_do,
    'c-l8-b26-chuyen-dong-nhiet.svg': fig_chuyen_dong_nhiet,
    'c-l8-b28-truyen-nhiet.svg': fig_truyen_nhiet,
    'c-l8-b29-bang-kep.svg': fig_bang_kep,
    'c-l8-b29-nuoc-4c.svg': fig_nuoc_4c,
}
FIGS9 = {
    'c-l9-b3-co-nang.svg': fig_co_nang,
    'c-l9-b4-cong.svg': fig_cong,
    'c-l9-b5-khuc-xa.svg': fig_khuc_xa,
    'c-l9-b6-phan-xa-toan-phan.svg': fig_phan_xa_toan_phan,
    'c-l9-b7-lang-kinh.svg': fig_lang_kinh,
    'c-l9-b8-thau-kinh-that.svg': fig_thau_kinh_that,
    'c-l9-b8-thau-kinh-ao.svg': fig_thau_kinh_ao,
    'c-l9-b11-ohm.svg': fig_ohm,
    'c-l9-b12-noi-tiep-song-song.svg': fig_noi_tiep_song_song,
    'c-l9-b14-cam-ung.svg': fig_cam_ung,
    'c-l9-b16-vong-nang-luong.svg': fig_vong_nang_luong,
}

ATTACH8 = [
    ('tap1/chuong-3/bai-13/khoi-luong-rieng.json', 3, 'c-l8-b13-khoi-luong-rieng.svg', 'Cùng thể tích 1 m³, các chất có khối lượng khác nhau.'),
    ('tap1/chuong-3/bai-14/thuc-hanh-khoi-luong-rieng.json', 3, 'c-l8-b14-the-tich-soi.svg', 'Đo thể tích vật rắn bằng ống đong: V = V₂ − V₁.'),
    ('tap1/chuong-3/bai-15/ap-suat-tren-be-mat.json', 1, 'c-l8-b15-ap-suat-be-mat.svg', 'Độ lún phụ thuộc diện tích bị ép.'),
    ('tap1/chuong-3/bai-16/ap-suat-chat-long-khi-quyen.json', 0, 'c-l8-b16-ap-suat-chat-long.svg', 'Áp suất chất lỏng tăng theo độ sâu và tác dụng theo mọi phương.'),
    ('tap1/chuong-3/bai-16/ap-suat-chat-long-khi-quyen.json', 4, 'c-l8-b16-khi-quyen-coc.svg', 'Áp suất khí quyển giữ nước trong cốc úp ngược.'),
    ('tap1/chuong-3/bai-17/luc-day-archimedes.json', 1, 'c-l8-b17-noi-chim.svg', 'Điều kiện chìm, lơ lửng, nổi.'),
    ('tap1/chuong-3/bai-17/luc-day-archimedes.json', 5, 'c-l8-b17-luc-ke.svg', 'Xác định lực đẩy Archimedes bằng lực kế.'),
    ('tap1/chuong-4/bai-18/tac-dung-lam-quay-moment.json', 3, 'c-l8-b18-moment.svg', 'Lực càng xa trục quay, tác dụng làm quay càng lớn.'),
    ('tap1/chuong-4/bai-19/don-bay-ung-dung.json', 3, 'c-l8-b19-don-bay.svg', 'Hai loại đòn bẩy.'),
    ('tap1/chuong-5/bai-20/nhiem-dien-co-xat.json', 3, 'c-l8-b20-nhiem-dien.svg', 'Nguyên tử và sự chuyển electron khi cọ xát.'),
    ('tap1/chuong-5/bai-22/mach-dien-don-gian.json', 1, 'c-l8-b22-ki-hieu-mach.svg', 'Kí hiệu các bộ phận trong sơ đồ mạch điện.'),
    ('tap1/chuong-5/bai-25/thuc-hanh-do-i-u.json', 1, 'c-l8-b25-mach-do.svg', 'Cách mắc ampe kế và vôn kế trong mạch điện.'),
    ('tap1/chuong-6/bai-26/nang-luong-nhiet-noi-nang.json', 1, 'c-l8-b26-chuyen-dong-nhiet.svg', 'Nhiệt độ càng cao, phân tử chuyển động càng nhanh.'),
    ('tap1/chuong-6/bai-28/su-truyen-nhiet.json', 3, 'c-l8-b28-truyen-nhiet.svg', 'Dẫn nhiệt, đối lưu và bức xạ nhiệt.'),
    ('tap1/chuong-6/bai-29/su-no-vi-nhiet.json', 1, 'c-l8-b29-bang-kep.svg', 'Băng kép bị uốn cong khi nóng lên.'),
    ('tap1/chuong-6/bai-29/su-no-vi-nhiet.json', 4, 'c-l8-b29-nuoc-4c.svg', 'Thể tích của nước thay đổi theo nhiệt độ.'),
]
ATTACH9 = [
    ('tap1/chuong-1/bai-3/co-nang.json', 2, 'c-l9-b3-co-nang.svg', 'Con lắc đơn: cơ năng được bảo toàn.'),
    ('tap1/chuong-1/bai-4/cong-va-cong-suat.json', 1, 'c-l9-b4-cong.svg', 'Khi nào lực sinh công.'),
    ('tap1/chuong-2/bai-5/khuc-xa-anh-sang.json', 3, 'c-l9-b5-khuc-xa.svg', 'Khúc xạ ánh sáng qua mặt phân cách không khí – thuỷ tinh.'),
    ('tap1/chuong-2/bai-6/phan-xa-toan-phan.json', 2, 'c-l9-b6-phan-xa-toan-phan.svg', 'Góc giới hạn và phản xạ toàn phần.'),
    ('tap1/chuong-2/bai-7/lang-kinh.json', 1, 'c-l9-b7-lang-kinh.svg', 'Lăng kính tán sắc ánh sáng trắng.'),
    ('tap1/chuong-2/bai-8/thau-kinh.json', 2, 'c-l9-b8-thau-kinh-that.svg', 'Dựng ảnh thật bằng ba tia đặc biệt.'),
    ('tap1/chuong-2/bai-8/thau-kinh.json', 4, 'c-l9-b8-thau-kinh-ao.svg', 'Dựng ảnh ảo của vật đặt trong khoảng tiêu cự.'),
    ('tap1/chuong-3/bai-11/dien-tro-dinh-luat-ohm.json', 2, 'c-l9-b11-ohm.svg', 'Đồ thị I theo U của dây dẫn có điện trở không đổi.'),
    ('tap1/chuong-3/bai-12/doan-mach-noi-tiep-song-song.json', 1, 'c-l9-b12-noi-tiep-song-song.svg', 'Sơ đồ đoạn mạch nối tiếp và song song.'),
    ('tap1/chuong-4/bai-14/cam-ung-dien-tu.json', 2, 'c-l9-b14-cam-ung.svg', 'Dòng điện cảm ứng và dòng điện xoay chiều.'),
    ('tap1/chuong-5/bai-16/vong-nang-luong-hoa-thach.json', 0, 'c-l9-b16-vong-nang-luong.svg', 'Nguồn gốc năng lượng hoá thạch.'),
]

if __name__ == '__main__':
    write_figs('ly8', FIGS8)
    for a in ATTACH8:
        attach('ly8', *a)
    write_figs('ly9', FIGS9)
    for a in ATTACH9:
        attach('ly9', *a)
    print('ly8: %d hình, ly9: %d hình' % (len(FIGS8), len(FIGS9)))
