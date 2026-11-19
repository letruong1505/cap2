#!/usr/bin/env python3
# Hình minh họa lý thuyết Vật lí 6 (sơ đồ mô phỏng, không theo tỉ lệ thật trừ khi ghi rõ). Chạy: python3 tools/build-ly6-figures.py
import math
import os
import random
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib2 import *

S = 'ly6'


def flame_icon(x, y, s=1.0, col=ORANGE):
    return PATH('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z' % (
        x, y - 16 * s, x + 14 * s, y - 2 * s, x + 12 * s, y + 14 * s, x, y + 14 * s,
        x - 12 * s, y + 14 * s, x - 14 * s, y - 2 * s, x, y - 16 * s), fill=col, stroke=INK, w=1.6)


def bolt(x, y):
    return POLY([(x + 4, y - 14), (x - 8, y + 2), (x - 1, y + 2), (x - 5, y + 14), (x + 8, y - 3), (x + 1, y - 3)],
                fill=INK, stroke=INK, sw=1)


def fig_canh_bao():
    b = [title(720, 'Một số kí hiệu an toàn trong phòng thực hành')]
    y = 110
    xs = [72, 216, 360, 504, 648]
    # 1 cảnh báo nguy hiểm
    x = xs[0]
    b.append(POLY([(x, y - 44), (x + 50, y + 38), (x - 50, y + 38)], fill='#ffd84d', stroke=INK, sw=3.4))
    b.append(T(x, y + 26, '!', size=44, weight='bold'))
    # 2 điện cao thế
    x = xs[1]
    b.append(POLY([(x, y - 44), (x + 50, y + 38), (x - 50, y + 38)], fill='#ffd84d', stroke=INK, sw=3.4))
    b.append(bolt(x, y + 8))
    # 3 cấm lửa
    x = xs[2]
    b.append(C(x, y, 42, fill='white', stroke=RED, w=7))
    b.append(flame_icon(x, y, 1.3))
    b.append(L(x - 30, y - 30, x + 30, y + 30, stroke=RED, w=7))
    # 4 chất dễ cháy
    x = xs[3]
    b.append(POLY([(x, y - 52), (x + 52, y), (x, y + 52), (x - 52, y)], fill='white', stroke=RED, sw=7))
    b.append(flame_icon(x, y + 2, 1.2, col=INK))
    # 5 lối thoát hiểm
    x = xs[4]
    b.append(R(x - 44, y - 44, 88, 88, fill='#2e9e4f', stroke='#2e9e4f', sw=2, rx=4))
    b.append(L(x - 26, y, x + 22, y, stroke='white', w=8))
    b.append(POLY([(x + 34, y), (x + 14, y - 18), (x + 14, y + 18)], fill='white', stroke='white', sw=1))
    caps = [('Cảnh báo', 'nguy hiểm', 'tam giác, nền vàng'), ('Cảnh báo', 'điện cao thế', 'tam giác, nền vàng'),
            ('Cấm lửa', '', 'tròn, viền đỏ, gạch chéo'), ('Chất dễ cháy', '', 'hình thoi, viền đỏ'),
            ('Lối thoát hiểm', '', 'hình vuông, nền xanh lá')]
    for x, (a, a2, c) in zip(xs, caps):
        b.append(T(x, 192, a, size=14, weight='bold'))
        if a2:
            b.append(T(x, 210, a2, size=14, weight='bold'))
        b.append(T(x, 232, c, size=12, fill=GREY))
    return svg(720, 250, ''.join(b))


def fig_do_dai():
    b = [title(720, 'Đo chiều dài bằng thước: GHĐ = 10 cm, ĐCNN = 1 mm')]
    x0, u = 50, 60
    ry = 140
    b.append(R(x0 - 10, ry, 10 * u + 20, 54, fill='#fdf3c8', stroke=INK, sw=2, rx=3))
    for mm in range(0, 101):
        x = x0 + mm * u / 10
        ln = 18 if mm % 10 == 0 else (12 if mm % 5 == 0 else 7)
        b.append(L(x, ry, x, ry + ln, w=1.6 if mm % 10 == 0 else 1))
    for k in range(11):
        b.append(T(x0 + k * u, ry + 38, str(k), size=14, weight='bold'))
    b.append(T(x0 + 10 * u + 28, ry + 38, 'cm', size=13, anchor='start'))
    ln = 7.3
    b.append(R(x0, 92, ln * u, 26, fill='#f7c58a', stroke=INK, sw=2))
    b.append(POLY([(x0 + ln * u, 92), (x0 + ln * u + 22, 105), (x0 + ln * u, 118)], fill='#e7b78a', stroke=INK, sw=2))
    b.append(L(x0, 72, x0, ry + 20, stroke=RED, w=1.4, dash='5 4'))
    b.append(H(x0, 66, 'một đầu vật ngang vạch 0', size=13, fill=RED, anchor='start'))
    xe = x0 + ln * u
    b.append(L(xe, 58, xe, ry, stroke=BLUE, w=1.6, dash='5 4'))
    b.append(ELL(xe, 50, 17, 8, fill='white', w=2))
    b.append(C(xe, 50, 4, fill=INK, stroke=INK, w=1))
    b.append(H(xe - 24, 54, 'mắt nhìn vuông góc với vạch chia', size=13, fill=BLUE, anchor='end'))
    b.append(H(xe, ry + 78, 'Kết quả: 7,3 cm', size=17, fill=INK))
    b.append(T(360, ry + 108, 'Đầu kia của vật nằm đúng vạch thứ 3 sau vạch 7 cm (7 cm + 3 mm)', size=13.5, fill=GREY))
    return svg(720, 275, ''.join(b))


def fig_nhiet_do():
    b = [title(720, 'Nhiệt kế và các thang nhiệt độ')]
    cx = 360
    y0, y100, k = 222, 62, 1.6
    b.append(R(cx - 10, 36, 20, 214, fill='white', stroke=INK, sw=2.4, rx=10))
    b.append(C(cx, 262, 18, fill='white', stroke=INK, w=2.4))
    b.append(R(cx - 5, y0 - 37 * k, 10, 250 - (y0 - 37 * k), fill=RED, stroke=RED, sw=1))
    b.append(C(cx, 262, 13, fill=RED, stroke=RED, w=1))
    rows = [(0, '0 °C', 'nước đá đang tan', '273 K', '32 °F'),
            (37, '37 °C', 'thân nhiệt người', '310 K', '98,6 °F'),
            (100, '100 °C', 'nước đang sôi', '373 K', '212 °F')]
    for t, c, nm, kel, far in rows:
        y = y0 - t * k
        b.append(L(cx - 22, y, cx + 22, y, w=2))
        b.append(T(cx - 30, y + 5, c, size=16, weight='bold', anchor='end'))
        b.append(T(cx - 120, y + 5, nm, size=13, anchor='end', fill=GREY))
        b.append(T(cx + 30, y + 5, kel + '   ' + far, size=15, anchor='start', fill=BLUE, weight='bold'))
    b.append(T(cx - 240, 40, 'Thang Celsius', size=14, weight='bold', anchor='start'))
    b.append(T(cx + 30, 40, 'Thang Kelvin  và  Fahrenheit', size=14, weight='bold', anchor='start'))
    b.append(T(cx, 296, 'T(K) = t(°C) + 273;   t(°F) = 1,8·t(°C) + 32', size=14.5))
    return svg(720, 310, ''.join(b))


def fig_trai_dat_quay():
    b = [title(720, 'Trái Đất tự quay và chuyển động nhìn thấy của Mặt Trời')]
    cx, cy, r = 330, 160, 80
    # Mặt Trời bên trái
    b.append(C(70, cy, 38, fill='#ffd84d', stroke=ORANGE, w=3))
    b.append(T(70, cy + 6, 'Mặt Trời', size=14, weight='bold'))
    for dy in (-60, -30, 0, 30, 60):
        b.append(L(118, cy + dy, 236, cy + dy * 0.9, stroke='#e8b92f', w=1.8, arrow=True))
    b.append(C(cx, cy, r, fill='#1f3b5c', stroke=INK, w=2.4))
    b.append(SECTOR(cx, cy, r, 90, 270, '#8ec1ea', stroke=INK, w=2.4))
    b.append(T(cx - 38, cy + 5, 'Ban ngày', size=14, weight='bold', fill=INK))
    b.append(T(cx + 38, cy + 5, 'Ban đêm', size=14, weight='bold', fill='white'))
    b.append(ARC(cx, cy, r + 22, 20, 160, stroke=RED, w=3, arrow=True))
    b.append(H(cx, cy - r - 36, 'quay từ Tây sang Đông', size=14, fill=RED))
    b.append(dot(cx, cy - r, 5, RED))
    b.append(card_text(470, 90, ['Nhìn từ phía trên', 'Cực Bắc, Trái Đất quay', 'ngược chiều kim đồng hồ,', 'một vòng hết khoảng 24 giờ.', '',
                                 'Người trên mặt đất thấy', 'Mặt Trời mọc ở phía đông,', 'lặn ở phía tây.'], w=236, size=14, lh=22))
    return svg(720, 300, ''.join(b))


def moon_phase(cx, cy, r, theta):
    """Hình mặt Trăng nhìn từ Trái Đất. theta: góc 0..360 (0 = trăng mới, 180 = trăng tròn)."""
    c = math.cos(math.radians(theta))
    out = [C(cx, cy, r, fill='#3b4252', stroke=INK, w=1.6)]
    waxing = theta < 180
    t, bt = (cx, cy - r), (cx, cy + r)
    if abs(c) < 0.999:
        sweep = 0 if c > 0 else 1
        d = 'M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f A%.1f,%.1f 0 0 %d %.1f,%.1f Z' % (
            t[0], t[1], r, r, bt[0], bt[1], r * abs(c), r, sweep, t[0], t[1])
        path = '<path d="%s" fill="#fff6c8" stroke="none"/>' % d
        if not waxing:
            path = '<g transform="translate(%.1f,0) scale(-1,1)">%s</g>' % (2 * cx, path)
        out.append(path)
    elif c < 0:
        out.append(C(cx, cy, r, fill='#fff6c8', stroke=INK, w=1.6))
    out.append(C(cx, cy, r, fill='none', stroke=INK, w=1.6))
    return ''.join(out)


def fig_pha_mat_trang():
    b = [title(720, 'Các pha của Mặt Trăng')]
    ex, ey, R_ = 330, 152, 82
    b.append(C(ex, ey, R_, fill='none', stroke=GREY, w=1.4, dash='5 4'))
    b.append(C(ex, ey, 22, fill='#6fa8dc', stroke=INK, w=2))
    b.append(T(ex, ey + 5, 'Trái Đất', size=11, weight='bold', fill='white'))
    for dy in (-60, -30, 0, 30, 60):
        b.append(L(650, ey + dy, 560, ey + dy, stroke='#e8b92f', w=1.8, arrow=True))
    b.append(T(640, ey + 90, 'Ánh sáng Mặt Trời', size=13, fill='#b8860b', weight='bold', anchor='middle'))
    for i in range(8):
        th = i * 45
        mx, my = pt(ex, ey, R_, th)
        b.append(C(mx, my, 12, fill='#3b4252', stroke=INK, w=1.6))
        b.append('<path d="M%.1f,%.1f A12,12 0 0 1 %.1f,%.1f Z" fill="#fff6c8"/>' % (mx, my - 12, mx, my + 12))
        b.append(C(mx, my, 12, fill='none', stroke=INK, w=1.6))
        lx, ly = pt(ex, ey, R_ + 28, th)
        b.append(T(lx, ly + 5, str(i + 1), size=14, weight='bold', fill=RED))
    names = ['Trăng mới', 'Lưỡi liềm', 'Thượng huyền', 'Trăng khuyết', 'Trăng tròn', 'Trăng khuyết', 'Hạ huyền', 'Lưỡi liềm']
    for i in range(8):
        x = 52 + i * 88
        b.append(moon_phase(x, 318, 26, i * 45))
        b.append(T(x, 362, '%d' % (i + 1), size=14, weight='bold', fill=RED))
        b.append(T(x, 381, names[i], size=11.5))
    b.append(T(360, 410, 'Nhìn từ Trái Đất: nửa sáng của Mặt Trăng luôn hướng về Mặt Trời; phần ta thấy thay đổi theo vị trí', size=12.5, fill=GREY))
    return svg(720, 424, ''.join(b))


def fig_he_mat_troi():
    b = [title(720, 'Hệ Mặt Trời (kích thước và khoảng cách không theo tỉ lệ)')]
    cy = 140
    b.append(C(0, cy, 74, fill='#ffd84d', stroke=ORANGE, w=3))
    b.append(T(8, cy - 80, 'Mặt Trời', size=13, weight='bold', anchor='start'))
    planets = [('Thuỷ tinh', 110, 5, '#b7b7b7'), ('Kim tinh', 168, 9, '#e8c27a'), ('Trái Đất', 228, 9.5, '#4e9be0'),
               ('Hoả tinh', 286, 6.5, '#d9674a'), ('Mộc tinh', 392, 30, '#d8a574'), ('Thổ tinh', 482, 26, '#e3c987'),
               ('Thiên Vương tinh', 562, 15, '#8fd6d8'), ('Hải Vương tinh', 640, 14.5, '#4a68c8')]
    b.append(L(110 - 20, cy, 700, cy, stroke=GREY, w=1, dash='3 5'))
    for k in range(9):
        a = random.Random(5).random() if False else 0
    rnd = random.Random(7)
    for _ in range(26):
        x = 322 + rnd.random() * 34
        b.append(dot(x, cy + rnd.uniform(-34, 34), 1.6, GREY))
    for n, x, r, col in planets:
        b.append(C(x, cy, r, fill=col, stroke=INK, w=1.8))
    b.append(ELL(482, cy, 40, 8, fill='none', stroke='#a58b45', w=1.6))
    for i, (n, x, r, col) in enumerate(planets):
        b.append(T(x, cy + 52 + (i % 2) * 18, n, size=12, weight='bold'))
        b.append(L(x, cy + r + 2, x, cy + 40 + (i % 2) * 18, stroke=GREY, w=0.8))
    b.append(T(339, cy - 46, 'vành đai', size=11, fill=GREY))
    b.append(T(339, cy - 33, 'tiểu hành tinh', size=11, fill=GREY))
    b.append(L(98, 232, 300, 232, stroke=GREEN, w=2))
    b.append(T(199, 252, '4 hành tinh đá', size=13, weight='bold', fill=GREEN))
    b.append(L(372, 232, 664, 232, stroke=BLUE, w=2))
    b.append(T(518, 252, '4 hành tinh khí khổng lồ', size=13, weight='bold', fill=BLUE))
    b.append(T(360, 284, 'Trái Đất cách Mặt Trời khoảng 150 triệu km = 1 đơn vị thiên văn (1 AU)', size=13.5))
    return svg(720, 298, ''.join(b))


def fig_ngan_ha():
    b = [title(720, 'Ngân Hà (sơ đồ minh hoạ nhìn từ phía trên)')]
    cx, cy = 230, 192
    rnd = random.Random(11)
    b.append(ELL(cx, cy, 140, 140, fill='#101a2e', stroke='#101a2e', w=1))
    for arm in range(4):
        for i in range(230):
            t = rnd.uniform(0.2, 4.9)
            rr = 16 + 24 * t + rnd.gauss(0, 3)
            a = t + arm * math.pi / 2 + rnd.gauss(0, 0.05)
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            if math.hypot(x - cx, y - cy) < 138:
                b.append(dot(x, y, rnd.choice((0.9, 1.2, 1.6)), '#dfe8ff'))
    b.append(ELL(cx, cy, 26, 22, fill='#ffe9a8', stroke='none', w=0))
    for _ in range(40):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0, 24)
        b.append(dot(cx + rr * math.cos(a), cy + rr * math.sin(a), 1.3, '#fff7d6'))
    t = 3.0
    rr = 16 + 24 * t
    sx, sy = cx + rr * math.cos(t + math.pi / 2), cy + rr * math.sin(t + math.pi / 2)
    b.append(dot(sx, sy, 5, '#ffd84d'))
    b.append(C(sx, sy, 9, fill='none', stroke='#ffd84d', w=1.5))
    b.append(L(sx + 10, sy, 420, sy, stroke=ORANGE, w=1.5))
    b.append(T(425, sy + 5, 'Hệ Mặt Trời', size=14, weight='bold', anchor='start', fill=ORANGE))
    b.append(L(cx + 8, cy - 10, 420, cy - 70, stroke=GREY, w=1.2))
    b.append(T(425, cy - 65, 'Trung tâm Ngân Hà', size=14, weight='bold', anchor='start'))
    b.append(card_text(420, 215, ['Ngân Hà gồm hàng trăm tỉ', 'ngôi sao; Hệ Mặt Trời nằm', 'trong một nhánh xoắn,', 'không ở trung tâm.'], w=270, size=14, lh=22))
    return svg(720, 346, ''.join(b))


def cart(x, y, w=90, h=36, col='#c9dcee'):
    return (R(x, y, w, h, fill=col, stroke=INK, sw=2.2, rx=3) + C(x + 20, y + h + 8, 8, fill='white', stroke=INK, w=2)
            + C(x + w - 20, y + h + 8, 8, fill='white', stroke=INK, w=2))


def fig_luc():
    b = [title(720, 'Lực tiếp xúc và lực không tiếp xúc')]
    gy = 180
    # đẩy
    b.append(ground(30, 230, gy))
    b.append(R(40, 100, 28, 60, fill='#f7c58a', stroke=INK, sw=2, rx=6))
    b.append(cart(110, 120))
    b.append(force(70, 138, 36, 0, 'F', col=RED, ly=-14))
    b.append(T(130, 218, 'Đẩy xe', size=15, weight='bold'))
    b.append(T(130, 238, '(lực tiếp xúc)', size=13, fill=GREY))
    # kéo
    b.append(ground(260, 460, gy))
    b.append(cart(270, 120))
    b.append(L(360, 138, 420, 138, w=2, stroke=INK))
    b.append(R(420, 108, 28, 60, fill='#f7c58a', stroke=INK, sw=2, rx=6))
    b.append(force(362, 138, 50, 0, 'F', col=RED, ly=-14))
    b.append(T(360, 218, 'Kéo xe', size=15, weight='bold'))
    b.append(T(360, 238, '(lực tiếp xúc)', size=13, fill=GREY))
    # nam châm
    b.append(R(500, 112, 40, 50, fill=RED, stroke=INK, sw=2))
    b.append(R(540, 112, 40, 50, fill=BLUE, stroke=INK, sw=2))
    b.append(T(520, 144, 'N', size=18, weight='bold', fill='white'))
    b.append(T(560, 144, 'S', size=18, weight='bold', fill='white'))
    b.append(C(670, 137, 20, fill='#8d99a6', stroke=INK, w=2.2))
    b.append(force(646, 137, -50, 0, 'F', col=RED, ly=-14))
    b.append(T(600, 218, 'Nam châm hút quả cầu sắt', size=15, weight='bold'))
    b.append(T(600, 238, '(lực không tiếp xúc)', size=13, fill=GREY))
    return svg(720, 255, ''.join(b))


def fig_bieu_dien_luc():
    b = [title(720, 'Biểu diễn lực bằng mũi tên')]
    gy = 190
    b.append(ground(40, 420, gy))
    b.append(R(150, 140, 100, 50, fill='#c9dcee', stroke=INK, sw=2.2, rx=2))
    ax, ay = 150, 165
    b.append(L(ax, ay, ax + 120, ay, stroke=RED, w=3, arrow=True))
    b.append(dot(ax, ay, 5, RED))
    b.append(H(ax + 80, ay - 40, 'F = 30 N', size=16, fill=RED))
    b.append(L(ax, ay + 40, ax - 0, ay + 28, stroke=GREY, w=1))
    b.append(H(ax - 8, ay - 30, 'điểm đặt', size=13, fill=INK, anchor='end'))
    b.append(L(ax - 6, ay - 26, ax - 1, ay - 6, stroke=GREY, w=1))
    b.append(T(210, 222, 'Phương ngang, chiều từ trái sang phải', size=14))
    # tỉ xích
    sx, sy = 470, 150
    b.append(T(sx + 110, sy - 30, 'Tỉ xích: 1 cm ứng với 10 N', size=14, weight='bold'))
    u = 40
    b.append(L(sx, sy, sx + 3 * u, sy, stroke=RED, w=3, arrow=True))
    for k in range(4):
        b.append(L(sx + k * u, sy + 6, sx + k * u, sy + 22, w=1.6))
        b.append(T(sx + k * u, sy + 40, '%d N' % (10 * k), size=12.5))
    b.append(T(sx + 3 * u / 2, sy - 8, '3 cm', size=13, weight='bold', fill=RED))
    b.append(T(sx + 110, sy + 70, '30 N  →  mũi tên dài 3 cm', size=14))
    return svg(720, 250, ''.join(b))


def spring(cx, y1, y2, amp=13, turns=None):
    n = turns or max(6, int((y2 - y1) / 9))
    pts = [(cx, y1)]
    seg = (y2 - y1) / n
    for i in range(n):
        pts.append((cx + (amp if i % 2 == 0 else -amp), y1 + (i + 0.5) * seg))
    pts.append((cx, y2))
    return PL(pts, stroke=INK, w=2.2)


def fig_lo_xo():
    b = [title(720, 'Độ giãn của lò xo treo thẳng đứng')]
    top = 50
    b.append(L(70, top, 650, top, w=3))
    xs = [130, 330, 530]
    l0, step = 80, 30
    for k, cx in enumerate(xs):
        b.append(L(cx - 25, top, cx + 25, top, w=3))
        bot = top + 8 + l0 + k * step
        b.append(spring(cx, top + 8, bot))
        wy = bot
        for j in range(k):
            b.append(R(cx - 18, wy + 4, 36, 18, fill='#8d99a6', stroke=INK, sw=2, rx=2))
            wy += 20
        # đường dóng
        b.append(L(cx + 40, top + 8 + l0, cx + 120, top + 8 + l0, stroke=GREY, w=1, dash='4 4'))
        if k:
            b.append(L(cx + 50, top + 8, cx + 50, bot, stroke=BLUE, w=1.6, arrow=True))
            b.append(H(cx + 78, (top + 8 + bot) / 2 + 4, 'l', size=15, fill=BLUE, anchor='start'))
            b.append(L(cx + 100, top + 8 + l0, cx + 100, bot, stroke=RED, w=2.4, arrow=True))
            b.append(H(cx + 106, (top + 8 + l0 + bot) / 2 + 5, 'Δl', size=15, fill=RED, anchor='start'))
        else:
            b.append(L(cx + 50, top + 8, cx + 50, bot, stroke=BLUE, w=1.8, arrow=True))
            b.append(H(cx + 60, (top + 8 + bot) / 2 + 4, 'l₀', size=15, fill=BLUE, anchor='start'))
        cap = ['Chưa treo vật', 'Treo 1 quả cân', 'Treo 2 quả cân'][k]
        b.append(T(cx, 276, cap, size=14, weight='bold'))
    b.append(T(360, 304, 'Δl = l − l₀;  khi treo 2 quả cân, độ giãn gấp đôi khi treo 1 quả cân', size=14))
    return svg(720, 322, ''.join(b))


def fig_trong_luong():
    b = [title(720, 'Vật khối lượng 6 kg: trên Trái Đất và trên Mặt Trăng')]
    for cx, name, p, lnn, rr, col in ((190, 'Trên Trái Đất', 'P = 10·6 = 60 N', 150, 170, '#4e9be0'),
                                       (530, 'Trên Mặt Trăng', 'P ≈ 60 : 6 = 10 N', 25, 100, '#b9bfc7')):
        gy = 300
        b.append('<path d="M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="2.4"/>'
                 % (cx - 120, gy + 40, rr, rr, cx + 120, gy + 40, col, INK))
        b.append(C(cx, 118, 16, fill='#f7c58a', stroke=INK, w=2.2))
        b.append(force(cx, 118, 0, lnn, None, col=RED, w=2.6))
        b.append(H(cx + 26, 118 + lnn / 2 + 6, 'P', size=17, fill=RED, anchor='start'))
        b.append(T(cx - 26, 124, '6 kg', size=14, weight='bold', anchor='end'))
        b.append(T(cx, 44, name, size=16, weight='bold'))
        b.append(T(cx, 66, p, size=15, fill=RED, weight='bold'))
    b.append(T(360, 346, 'Khối lượng không đổi; trọng lượng trên Mặt Trăng nhỏ hơn khoảng 6 lần', size=13.5, fill=GREY))
    return svg(720, 362, ''.join(b))


def fig_ma_sat():
    b = [title(720, 'Lực ma sát trượt')]
    gy = 170
    b.append(ground(30, 400, gy))
    b.append(R(130, 108, 120, 62, fill='#c9dcee', stroke=INK, sw=2.2, rx=2))
    b.append(force(250, 139, 90, 0, 'F kéo', col=RED, ly=-14))
    b.append(force(130, 158, -76, 0, 'F ms', col=GREEN, ly=-14))
    b.append(L(150, 80, 230, 80, stroke=INK, w=2, arrow=True))
    b.append(T(190, 72, 'chiều chuyển động', size=13))
    b.append(C(440, 150, 42, fill='white', stroke=INK, w=2))
    b.append(T(440, 100, 'phóng to bề mặt', size=12, fill=GREY))
    b.append(PL([(405, 130), (418, 118), (428, 132), (440, 116), (452, 134), (464, 120), (476, 132)], stroke=INK, w=2))
    b.append(PL([(405, 146), (416, 158), (428, 144), (440, 160), (452, 146), (466, 158), (476, 148)], stroke=INK, w=2))
    b.append(T(440, 218, 'Hai bề mặt gồ ghề cọ vào nhau', size=12.5))
    b.append(card_text(500, 70, ['Lực ma sát trượt:', '• xuất hiện ở bề mặt tiếp xúc', '• ngược chiều chuyển động', '• cản trở vật trượt'], w=205, size=13, lh=22))
    return svg(720, 250, ''.join(b))


def fig_dang_nang_luong():
    b = [title(720, 'Một số dạng năng lượng')]
    cells = [('Động năng', 'xe đang chạy'), ('Thế năng hấp dẫn', 'vật ở trên cao'), ('Thế năng đàn hồi', 'lò xo bị nén'),
             ('Quang năng', 'ánh sáng từ đèn'), ('Nhiệt năng', 'ngọn lửa, vật nóng'), ('Năng lượng âm thanh', 'loa phát âm')]
    for i, (n, ex) in enumerate(cells):
        col, row = i % 3, i // 3
        cx, cy = 120 + col * 240, 90 + row * 150
        b.append(R(cx - 108, cy - 52, 216, 126, fill=LGREY, stroke=GREY, sw=1, rx=8))
        if i == 0:
            b.append(R(cx - 40, cy - 8, 80, 26, fill='#c9dcee', stroke=INK, sw=2, rx=5))
            b.append(R(cx - 20, cy - 26, 40, 20, fill='#dbe7f3', stroke=INK, sw=2, rx=4))
            b.append(C(cx - 22, cy + 22, 9, fill=INK, stroke=INK, w=1)); b.append(C(cx + 22, cy + 22, 9, fill=INK, stroke=INK, w=1))
            for k in range(3):
                b.append(L(cx - 58 - k * 10, cy + k * 8 - 4, cx - 80 - k * 10, cy + k * 8 - 4, w=2, stroke=GREY))
        elif i == 1:
            b.append(L(cx - 50, cy + 28, cx + 50, cy + 28, w=2.4))
            b.append(C(cx, cy - 22, 14, fill='#ee6a5a', stroke=INK, w=2))
            b.append(L(cx + 30, cy - 22, cx + 30, cy + 28, stroke=BLUE, w=1.6, arrow=True))
            b.append(L(cx + 30, cy + 28, cx + 30, cy - 22, stroke=BLUE, w=1.6, arrow=True))
            b.append(T(cx + 40, cy + 4, 'h', size=14, fill=BLUE, anchor='start', weight='bold'))
        elif i == 2:
            b.append(L(cx - 54, cy - 10, cx - 54, cy + 24, w=4)); b.append(R(cx - 54, cy - 10, 8, 34, fill=GREY, stroke=INK, sw=1.4))
            b.append(spring_h(cx - 46, cx + 14, cy + 7))
            b.append(R(cx + 14, cy - 14, 30, 42, fill='#c9dcee', stroke=INK, sw=2))
        elif i == 3:
            b.append(bulb(cx, cy - 4, 22, on=True))
            for a in range(0, 360, 45):
                x1, y1 = pt(cx, cy - 4, 30, a); x2, y2 = pt(cx, cy - 4, 42, a)
                b.append(L(x1, y1, x2, y2, stroke='#e8b92f', w=2.4))
            b.append(R(cx - 10, cy + 20, 20, 16, fill=GREY, stroke=INK, sw=2))
        elif i == 4:
            b.append(flame_icon(cx, cy, 1.9))
            b.append(L(cx - 36, cy + 28, cx + 36, cy + 28, w=3))
        else:
            b.append(R(cx - 36, cy - 22, 22, 44, fill='#c9dcee', stroke=INK, sw=2))
            b.append(POLY([(cx - 14, cy - 12), (cx + 8, cy - 32), (cx + 8, cy + 32), (cx - 14, cy + 12)], fill='#dbe7f3', stroke=INK, sw=2))
            for k, rr in enumerate((16, 28, 40)):
                b.append(ARC(cx + 12, cy, rr, -45, 45, stroke=BLUE, w=2))
        b.append(T(cx, cy + 56, n, size=14, weight='bold'))
        b.append(T(cx, cy + 71, ex, size=12, fill=GREY)) if False else None
    return svg(720, 330, ''.join(b))


def spring_h(x1, x2, y, amp=12, n=8):
    pts = [(x1, y)]
    seg = (x2 - x1) / n
    for i in range(n):
        pts.append((x1 + (i + 0.5) * seg, y + (amp if i % 2 == 0 else -amp)))
    pts.append((x2, y))
    return PL(pts, stroke=INK, w=2.2)


def fig_chuyen_hoa():
    b = [title(720, 'Quả bóng rơi: thế năng chuyển hoá thành động năng (bỏ qua sức cản)')]
    gy = 280
    b.append(ground(60, 340, gy))
    levels = [(60, 'Ở trên cao', 1.0, 0.0), (170, 'Ở giữa', 0.5, 0.5), (gy - 14, 'Sát mặt đất', 0.0, 1.0)]
    for y, name, wt, wd in levels:
        b.append(C(200, y, 14, fill='#ee6a5a', stroke=INK, w=2))
        b.append(T(240, y + 5, name, size=14, anchor='start'))
        by = y + 8
        b.append(R(420, by - 30, 220 * wt if wt else 1, 20, fill=BLUE, stroke=BLUE, sw=1))
        b.append(R(420, by - 6, 220 * wd if wd else 1, 20, fill=ORANGE, stroke=ORANGE, sw=1))
        b.append(T(412, by - 15, 'Wt', size=13, anchor='end', weight='bold', fill=BLUE))
        b.append(T(412, by + 9, 'Wđ', size=13, anchor='end', weight='bold', fill=ORANGE))
    b.append(L(200, 76, 200, 250, stroke=GREY, w=1.4, dash='5 4', arrow=True))
    b.append(T(530, 320, 'Tổng Wt + Wđ không đổi: cơ năng được bảo toàn', size=13.5, fill=GREY))
    return svg(720, 336, ''.join(b))


def fig_hao_phi():
    b = [title(720, 'Năng lượng có ích và năng lượng hao phí (sơ đồ định tính)')]
    for y0, name, wl, wh in ((60, 'Đèn sợi đốt', 4, 16), (190, 'Đèn LED', 12, 4)):
        b.append(L(40, y0 + 50, 190, y0 + 50, stroke=BLUE, w=14, arrow=False))
        b.append(POLY([(190, y0 + 38), (206, y0 + 50), (190, y0 + 62)], fill=BLUE, stroke=BLUE, sw=1))
        b.append(T(110, y0 + 32, 'Điện năng', size=14, weight='bold', fill=BLUE))
        b.append(R(210, y0 + 20, 140, 60, fill=LYELLOW, stroke=INK, sw=2.4, rx=8))
        b.append(T(280, y0 + 56, name, size=16, weight='bold'))
        b.append(L(350, y0 + 38, 560, y0 + 38 - 18, stroke='#e8b92f', w=wl, arrow=False))
        b.append(T(570, y0 + 16, 'Quang năng (có ích)', size=14, anchor='start', weight='bold', fill='#b8860b'))
        b.append(L(350, y0 + 64, 560, y0 + 64 + 18, stroke=RED, w=wh, arrow=False))
        b.append(T(570, y0 + 98, 'Nhiệt năng (hao phí)', size=14, anchor='start', weight='bold', fill=RED))
    b.append(T(360, 330, 'Độ rộng của mũi tên chỉ lượng năng lượng (so sánh định tính): đèn LED ít hao phí hơn', size=13, fill=GREY))
    return svg(720, 346, ''.join(b))


def fig_tai_tao():
    b = [title(720, 'Một số nguồn năng lượng tái tạo')]
    # mặt trời + pin mặt trời
    b.append(C(60, 70, 24, fill='#ffd84d', stroke=ORANGE, w=2.4))
    for a in range(0, 360, 45):
        x1, y1 = pt(60, 70, 30, a); x2, y2 = pt(60, 70, 42, a)
        b.append(L(x1, y1, x2, y2, stroke='#e8b92f', w=2.4))
    b.append(POLY([(100, 175), (210, 140), (225, 185), (115, 220)], fill='#2f4f8f', stroke=INK, sw=2.2))
    for k in (1, 2, 3):
        t = k / 4
        b.append(L(100 + t * 125, 175 + t * 10 - t * 35 * 0 - (t * 35 - 0) * 0, 100 + t * 125 + 15 * 0, 175, w=0))
    for i in range(1, 4):
        t = i / 4
        b.append(L(100 + t * 125, 175 - t * 35 + t * 45 * 0, 115 + t * 110, 220 - t * 35, stroke='#9fb4de', w=1.2))
    b.append(L(165, 210, 165, 245, w=3))
    b.append(L(140, 245, 190, 245, w=3))
    b.append(T(165, 275, 'Điện mặt trời', size=15, weight='bold'))
    # gió
    cx = 360
    b.append(L(cx, 150, cx - 5, 245, w=6))
    b.append(L(cx, 150, cx, 245, w=0))
    for a in (90, 210, 330):
        x2, y2 = pt(cx, 150, 62, a)
        b.append(POLY([(cx, 150), pt(cx, 150, 62, a + 7), pt(cx, 150, 62, a - 7)], fill='#e6eef7', stroke=INK, sw=2))
    b.append(C(cx, 150, 7, fill=INK, stroke=INK, w=1))
    for k in range(3):
        b.append(L(270 - k * 6, 90 + k * 22, 308, 90 + k * 22, stroke=BLUE, w=1.8, arrow=True))
    b.append(T(cx, 275, 'Điện gió', size=15, weight='bold'))
    # thuỷ điện
    b.append(POLY([(520, 110), (580, 110), (610, 240), (520, 240)], fill='#b9bfc7', stroke=INK, sw=2.4))
    b.append(R(430, 130, 90, 110, fill='#8ec1ea', stroke=INK, sw=2))
    for k in range(3):
        b.append(PL([(440, 150 + 25 * k), (460, 144 + 25 * k), (480, 150 + 25 * k), (500, 144 + 25 * k)], stroke='white', w=1.6))
    b.append(R(610, 205, 90, 35, fill='#8ec1ea', stroke=INK, sw=2))
    b.append(L(580, 190, 610, 215, stroke=BLUE, w=3, arrow=True))
    b.append(T(560, 275, 'Thuỷ điện', size=15, weight='bold'))
    return svg(720, 292, ''.join(b))


FIGS = {
    'c-l6-b2-ki-hieu-canh-bao.svg': fig_canh_bao,
    'c-l6-b5-do-chieu-dai.svg': fig_do_dai,
    'c-l6-b8-nhiet-ke.svg': fig_nhiet_do,
    'c-l6-b52-trai-dat-quay.svg': fig_trai_dat_quay,
    'c-l6-b53-pha-mat-trang.svg': fig_pha_mat_trang,
    'c-l6-b54-he-mat-troi.svg': fig_he_mat_troi,
    'c-l6-b55-ngan-ha.svg': fig_ngan_ha,
    'c-l6-b40-luc.svg': fig_luc,
    'c-l6-b41-bieu-dien-luc.svg': fig_bieu_dien_luc,
    'c-l6-b42-lo-xo.svg': fig_lo_xo,
    'c-l6-b43-trong-luong.svg': fig_trong_luong,
    'c-l6-b44-ma-sat.svg': fig_ma_sat,
    'c-l6-b47-dang-nang-luong.svg': fig_dang_nang_luong,
    'c-l6-b48-chuyen-hoa.svg': fig_chuyen_hoa,
    'c-l6-b49-hao-phi.svg': fig_hao_phi,
    'c-l6-b50-tai-tao.svg': fig_tai_tao,
}

ATTACH = [
    ('tap1/chuong-1/bai-2/an-toan-phong-thuc-hanh.json', 2, 'c-l6-b2-ki-hieu-canh-bao.svg', 'Một số kí hiệu cảnh báo, cấm và thoát hiểm.'),
    ('tap1/chuong-1/bai-5/do-chieu-dai.json', 2, 'c-l6-b5-do-chieu-dai.svg', 'Cách đặt thước, đặt mắt và đọc kết quả đo chiều dài.'),
    ('tap1/chuong-1/bai-8/do-nhiet-do.json', 2, 'c-l6-b8-nhiet-ke.svg', 'Nhiệt kế và ba thang nhiệt độ Celsius, Kelvin, Fahrenheit.'),
    ('tap1/chuong-10/bai-52/chuyen-dong-mat-troi.json', 2, 'c-l6-b52-trai-dat-quay.svg', 'Trái Đất tự quay quanh trục từ tây sang đông.'),
    ('tap1/chuong-10/bai-53/mat-trang.json', 1, 'c-l6-b53-pha-mat-trang.svg', 'Vị trí của Mặt Trăng trên quỹ đạo và các pha nhìn từ Trái Đất.'),
    ('tap1/chuong-10/bai-54/he-mat-troi.json', 2, 'c-l6-b54-he-mat-troi.svg', 'Mặt Trời và tám hành tinh (không theo tỉ lệ).'),
    ('tap1/chuong-10/bai-55/ngan-ha.json', 1, 'c-l6-b55-ngan-ha.svg', 'Sơ đồ Ngân Hà và vị trí của Hệ Mặt Trời.'),
    ('tap1/chuong-8/bai-40/luc-la-gi.json', 1, 'c-l6-b40-luc.svg', 'Lực tiếp xúc và lực không tiếp xúc.'),
    ('tap1/chuong-8/bai-41/bieu-dien-luc.json', 1, 'c-l6-b41-bieu-dien-luc.svg', 'Biểu diễn lực 30 N với tỉ xích 1 cm ứng với 10 N.'),
    ('tap1/chuong-8/bai-42/bien-dang-lo-xo.json', 1, 'c-l6-b42-lo-xo.svg', 'Độ giãn của lò xo khi treo vật.'),
    ('tap1/chuong-8/bai-43/trong-luong-luc-hap-dan.json', 3, 'c-l6-b43-trong-luong.svg', 'Cùng một vật có trọng lượng khác nhau trên Trái Đất và Mặt Trăng.'),
    ('tap1/chuong-8/bai-44/luc-ma-sat.json', 0, 'c-l6-b44-ma-sat.svg', 'Lực ma sát trượt cản trở chuyển động.'),
    ('tap1/chuong-9/bai-47/mot-so-dang-nang-luong.json', 0, 'c-l6-b47-dang-nang-luong.svg', 'Một số dạng năng lượng thường gặp.'),
    ('tap1/chuong-9/bai-48/su-chuyen-hoa-nang-luong.json', 2, 'c-l6-b48-chuyen-hoa.svg', 'Thế năng chuyển hoá thành động năng khi vật rơi.'),
    ('tap1/chuong-9/bai-49/nang-luong-hao-phi.json', 2, 'c-l6-b49-hao-phi.svg', 'So sánh năng lượng hao phí của đèn sợi đốt và đèn LED.'),
    ('tap1/chuong-9/bai-50/nang-luong-tai-tao.json', 0, 'c-l6-b50-tai-tao.svg', 'Điện mặt trời, điện gió và thuỷ điện.'),
]

if __name__ == '__main__':
    write_figs(S, FIGS)
    for a in ATTACH:
        attach(S, *a)
    print('ly6: %d hình' % len(FIGS))
