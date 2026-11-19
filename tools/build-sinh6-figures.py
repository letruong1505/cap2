# Sinh 6: sơ đồ minh họa lý thuyết (không phải ảnh chụp).
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from sinhlib import *


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


# ---------- Bài 3: kính lúp ----------
def fig_kinh_lup():
    b = [title(720, 'Kính lúp và cách quan sát vật mẫu')]
    cx, cy, r = 130, 110, 44
    b.append(C(cx, cy, r, fill='#dbeaf7', stroke=INK, w=3))
    b.append(C(cx, cy, r + 7, fill='none', stroke='#8a6a3a', w=8))
    a = math.radians(45)
    x1, y1 = cx + (r + 11) * math.cos(a), cy + (r + 11) * math.sin(a)
    x2, y2 = x1 + 70 * math.cos(a), y1 + 70 * math.sin(a)
    b.append(L(x1, y1, x2, y2, stroke=INK, w=15))
    b.append(L(x1, y1, x2, y2, stroke='#b8651b', w=11))
    b.append(PATH('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' % (cx - 22, cy - 14, cx - 8, cy - 28, cx + 10, cy - 28), stroke='white', w=3))
    lead(b, cx + 36, cy - 36, 225, 52, 'khung kính', anchor='start')
    lead(b, cx + 14, cy + 6, 225, 100, 'mặt kính (lồi)', anchor='start')
    lead(b, x2 - 10, y2 - 10, 250, 195, 'tay cầm', anchor='start')
    # cách dùng
    ey, ex = 110, 400
    b.append(ELL(ex, ey, 26, 16, fill='white', w=2.4)); b.append(C(ex + 6, ey, 8, fill=INK, stroke=INK, w=1))
    b.append(T(ex, ey + 40, 'mắt', size=14, weight='bold'))
    lx = 480
    b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d Z' % (lx, ey - 40, lx + 14, ey, lx, ey + 40, lx - 14, ey, lx, ey - 40), fill='#cfe6f7', stroke=INK, w=2.2))
    b.append(T(lx, ey + 58, 'kính lúp', size=14, weight='bold'))
    ox = lx + 40
    b.append(L(ox, ey + 40, ox, ey + 15, stroke=BLUE, w=3, arrow=True))
    b.append(T(ox + 4, ey + 62, 'vật', size=14, weight='bold', fill=BLUE, anchor='start'))
    ix = lx + 80
    b.append(L(ix, ey + 40, ix, ey - 20, stroke=RED, w=2.4, dash='5 4', arrow=True))
    b.append(T(ix + 6, ey - 24, 'ảnh ảo', size=14, weight='bold', fill=RED, anchor='start'))
    b.append(L(ex + 30, ey, lx - 16, ey, stroke=GREY, w=1.4, dash='3 3'))
    b.append(T(540, 205, 'Mắt nhìn qua kính thấy ảnh ảo lớn hơn vật', size=13, fill=GREY))
    return svg(720, 222, ''.join(b))


# ---------- Bài 4: kính hiển vi ----------
def fig_kinh_hien_vi():
    b = [title(720, 'Cấu tạo kính hiển vi quang học')]
    P = ((360, 302), (432, 292), (432, 112), (330, 76))
    arm = 'M%d,%d C%d,%d %d,%d %d,%d' % (P[0] + P[1] + P[2] + P[3])
    b.append(PATH(arm, stroke=INK, w=20))
    b.append(PATH(arm, stroke='#9db4c9', w=15))
    b.append(R(215, 296, 160, 20, fill='#9db4c9', stroke=INK, sw=2.4, rx=6))                 # chân
    b.append(R(292, 52, 36, 112, fill='#c9d3dc', stroke=INK, sw=2.4))                          # ống kính
    b.append(R(298, 28, 24, 26, fill='#7d8b99', stroke=INK, sw=2.2))                           # thị kính
    b.append(POLY([(296, 164), (324, 164), (320, 190), (300, 190)], fill='#7d8b99', stroke=INK, sw=2.2))  # vật kính
    b.append(R(250, 226, 106, 9, fill='#c9d3dc', stroke=INK, sw=2.2))                          # bàn kính
    b.append(R(280, 219, 40, 7, fill='#cfe6f7', stroke=INK, sw=1.6))                           # tiêu bản
    b.append(R(272, 220, 5, 8, fill=INK, stroke=INK, sw=1)); b.append(R(323, 220, 5, 8, fill=INK, stroke=INK, sw=1))
    b.append(C(300, 276, 13, fill='#fbf0c9', stroke=INK, w=2.2))                               # nguồn sáng
    for dx in (-8, 0, 8):
        b.append(L(300 + dx, 262, 300 + dx, 240, stroke=ORANGE, w=1.6, dash='3 3'))
    b.append(L(300, 296, 300, 289, stroke=INK, w=2.4))
    mx, my = bez(*P, 0.5)
    b.append(C(mx + 2, my, 17, fill='#7d8b99', stroke=INK, w=2.4))
    b.append(C(mx + 24, my, 9, fill='#7d8b99', stroke=INK, w=2.2))
    tx, ty = bez(*P, 0.82)
    lead(b, 310, 40, 150, 34, 'thị kính', anchor='end')
    lead(b, 298, 112, 150, 98, 'ống kính', anchor='end')
    lead(b, 304, 180, 150, 150, 'vật kính', anchor='end')
    lead(b, 262, 231, 150, 206, 'bàn kính', anchor='end')
    lead(b, 275, 224, 150, 238, 'kẹp giữ mẫu', anchor='end')
    lead(b, 300, 276, 150, 272, 'nguồn sáng', anchor='end')
    lead(b, 240, 306, 150, 306, 'chân kính', anchor='end')
    lead(b, tx + 2, ty - 4, 470, 62, 'thân kính', anchor='start')
    lead(b, mx + 2, my - 14, 480, 150, 'ốc to (chỉnh thô)', anchor='start')
    lead(b, mx + 28, my + 6, 480, 196, 'ốc nhỏ (chỉnh tinh)', anchor='start')
    b.append(card_text(470, 250, ['Độ phóng đại =', 'thị kính × vật kính', 'Ví dụ: 10× và 40×', '→ phóng đại 400 lần'], w=220, size=14, lh=22))
    return svg(720, 372, ''.join(b))


# ---------- Bài 18: hình dạng tế bào ----------
def fig_hinh_dang_te_bao():
    b = [title(720, 'Hình dạng và kích thước tế bào')]
    y = 100
    xs = [80, 220, 360, 500, 640]
    # hình đĩa (hồng cầu)
    b.append(ELL(xs[0], y, 36, 36, fill='#e8908f', stroke=INK, w=2.4)); b.append(ELL(xs[0], y, 15, 15, fill='#f3c1c0', stroke='none', w=0))
    # hình cầu (trứng)
    b.append(C(xs[1], y, 38, fill='#fbf0c9', stroke=INK, w=2.4)); b.append(C(xs[1] - 6, y - 4, 12, fill=NUC, stroke=INK, w=1.6))
    # hình sợi
    b.append(R(xs[2] - 11, y - 52, 22, 104, fill='#e9b8a6', stroke=INK, sw=2.4, rx=11))
    for k in (-28, 0, 28):
        b.append(ELL(xs[2], y + k, 6, 9, fill=NUC, stroke=INK, w=1.2))
    # hình sao (thần kinh)
    cx = xs[3]
    for ang, ln in ((20, 44), (75, 46), (130, 42), (200, 46), (250, 44), (310, 42)):
        x2, y2 = pt(cx, y, ln, ang)
        b.append(L(cx, y, x2, y2, stroke='#6a4c93', w=3))
        for sub in (-30, 30):
            xs2, ys2 = pt(x2, y2, 12, ang + sub)
            b.append(L(x2, y2, xs2, ys2, stroke='#6a4c93', w=2))
    b.append(C(cx, y, 16, fill='#d8c5ee', stroke=INK, w=2.4)); b.append(C(cx, y, 6, fill=NUC, stroke=INK, w=1.2))
    # hình trụ
    for k in (-1, 0, 1):
        b.append(R(xs[4] - 15 + k * 30 - (15 if False else 0) , y - 46, 30, 92, fill='#cfe6d0' if k == 0 else '#e0eed9', stroke=INK, sw=2.2, rx=3))
        b.append(ELL(xs[4] + k * 30, y + 28, 7, 10, fill=NUC, stroke=INK, w=1.2))
    names = [('hình đĩa', 'hồng cầu'), ('hình cầu', 'tế bào trứng'), ('hình sợi', 'tế bào cơ'), ('hình sao', 'tế bào thần kinh'), ('hình trụ', 'tế bào biểu mô')]
    for x, (a, c) in zip(xs, names):
        b.append(T(x, 178, a, size=15, weight='bold')); b.append(T(x, 197, c, size=13, fill=GREY))
    b.append(R(120, 222, 480, 60, fill=LGREY, stroke=GREY, sw=1.4, rx=8))
    b.append(L(150, 252, 250, 252, stroke=INK, w=3)); b.append(L(150, 246, 150, 258, w=2)); b.append(L(250, 246, 250, 258, w=2))
    b.append(T(200, 242, '1 mm', size=13, weight='bold'))
    b.append(T(260, 257, '= 1 000 µm  (đơn vị đo kích thước tế bào là micrômét)', size=13, anchor='start'))
    return svg(720, 300, ''.join(b))


# ---------- Bài 19 ----------
def cell_animal(b, cx, cy, rx=70, ry=58, left=True, right=True, tag=''):
    b.append('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="3"/>'
             % (cx - rx, cy, cx - rx, cy - ry * 0.8, cx - rx * 0.4, cy - ry, cx, cy - ry,
                cx + rx * 0.5, cy - ry, cx + rx, cy - ry * 0.6, cx + rx, cy,
                cx + rx, cy + ry * 0.7, cx + rx * 0.5, cy + ry, cx, cy + ry,
                cx - rx * 0.5, cy + ry, cx - rx, cy + ry * 0.7, cx - rx, cy, CELL, INK))
    b.append(C(cx - 8, cy - 4, 22, fill=NUC, stroke=INK, w=2.4)); b.append(C(cx - 12, cy - 8, 6, fill='#9b7fc4', stroke='none', w=0))
    for (dx, dy) in ((30, 22), (-34, 24), (26, -26)):
        b.append(ELL(cx + dx, cy + dy, 9, 5, fill='#e0c58f', stroke=INK, w=1.2))
    return cx, cy


def cell_plant(b, cx, cy, w=150, h=116):
    b.append(R(cx - w / 2, cy - h / 2, w, h, fill='#a9c79a', stroke=INK, sw=3, rx=10))
    b.append(R(cx - w / 2 + 7, cy - h / 2 + 7, w - 14, h - 14, fill=CELL, stroke='#7a6a45', sw=1.8, rx=6))
    b.append(R(cx + 8, cy - 26, 46, 52, fill='#dbe9f6', stroke='#7a8fa5', sw=1.4, rx=14))
    b.append(C(cx - 36, cy - 18, 18, fill=NUC, stroke=INK, w=2.4)); b.append(C(cx - 40, cy - 22, 5, fill='#9b7fc4', stroke='none', w=0))
    for (dx, dy) in ((-48, 26), (-20, 34), (-52, 2)):
        b.append(ELL(cx + dx, cy + dy, 11, 6, fill=CHL, stroke=INK, w=1.3))


def fig_nhan_so_vs_thuc():
    b = [title(720, 'Tế bào nhân sơ (vi khuẩn) và tế bào nhân thực (động vật)')]
    # nhân sơ
    cx, cy = 175, 140
    b.append(R(cx - 78, cy - 40, 156, 80, fill='#d9c9a3', stroke=INK, sw=3, rx=40))
    b.append(R(cx - 72, cy - 34, 144, 68, fill=CELL, stroke='#7a6a45', sw=1.8, rx=34))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d' % (
        cx - 30, cy, cx - 20, cy - 24, cx - 8, cy + 20, cx + 4, cy - 10, cx + 14, cy - 28, cx + 22, cy + 22, cx + 32, cy - 4, cx + 40, cy - 12, cx + 20, cy + 8, cx - 4, cy + 6), stroke='#6a4c93', w=2.6))
    b.append(squig(cx - 78, cy, cx - 120, cy - 4, amp=4, n=3, stroke=INK, w=2))
    lead(b, cx - 76, cy - 22, 30, 60, 'thành tế bào', anchor='start')
    lead(b, cx - 68, cy + 20, 30, 215, 'màng tế bào', anchor='start')
    lead(b, cx + 40, cy + 16, 170, 215, 'chất tế bào', anchor='start')
    lead(b, cx + 4, cy - 14, 160, 60, 'vùng nhân (chưa có màng nhân)', anchor='start')
    b.append(T(cx, 250, 'Tế bào nhân sơ', size=15, weight='bold'))
    # nhân thực động vật
    cell_animal(b, 520, 140, 90, 70)
    lead(b, 520 + 88, 140 - 14, 622, 70, 'màng tế bào', anchor='start')
    lead(b, 520 + 40, 140 + 28, 622, 205, 'chất tế bào', anchor='start')
    lead(b, 520 - 8, 140 - 4, 400, 60, 'nhân (có màng nhân)', anchor='start')
    b.append(T(520, 250, 'Tế bào nhân thực (động vật)', size=15, weight='bold'))
    return svg(720, 268, ''.join(b))


def fig_thuc_vat_vs_dong_vat():
    b = [title(720, 'Tế bào thực vật và tế bào động vật')]
    cell_plant(b, 175, 140)
    lead(b, 175 - 74, 140 - 40, 30, 52, 'thành tế bào', anchor='start')
    lead(b, 175 - 66, 140 + 28, 20, 232, 'lục lạp', anchor='start')
    lead(b, 175 + 30, 140, 292, 100, 'không bào', anchor='start')
    lead(b, 175 - 36, 140 - 18, 20, 100, 'nhân', anchor='start') if False else lead(b, 175 - 36, 140 - 22, 20, 120, 'nhân', anchor='start')
    lead(b, 175 + 70, 140 + 40, 292, 196, 'chất tế bào', anchor='start')
    b.append(T(175, 250, 'Tế bào thực vật', size=15, weight='bold'))
    cell_animal(b, 530, 140, 90, 70)
    lead(b, 530 + 88, 140 - 14, 632, 70, 'màng tế bào', anchor='start')
    lead(b, 530 + 40, 140 + 28, 632, 205, 'chất tế bào', anchor='start')
    lead(b, 530 - 8, 140 - 4, 400, 60, 'nhân', anchor='start')
    b.append(T(530, 250, 'Tế bào động vật', size=15, weight='bold'))
    b.append(T(360, 275, 'Chỉ tế bào thực vật có thành tế bào và lục lạp', size=13, fill=GREY))
    return svg(720, 290, ''.join(b))


FIGS = {
    'c-s6-b3-kinh-lup.svg': fig_kinh_lup,
    'c-s6-b4-kinh-hien-vi.svg': fig_kinh_hien_vi,
    'c-s6-b18-hinh-dang-te-bao.svg': fig_hinh_dang_te_bao,
    'c-s6-b19-nhan-so-nhan-thuc.svg': fig_nhan_so_vs_thuc,
    'c-s6-b19-thuc-vat-dong-vat.svg': fig_thuc_vat_vs_dong_vat,
}
# (đường dẫn bài, chỉ số khối lý thuyết sau đó chèn, tên hình, chú thích)
ATTACH = [
    ('sinh6/bai-3/su-dung-kinh-lup.json', 1, 'c-s6-b3-kinh-lup.svg', 'Kính lúp: cấu tạo và cách quan sát vật mẫu'),
    ('sinh6/bai-4/su-dung-kinh-hien-vi.json', 1, 'c-s6-b4-kinh-hien-vi.svg', 'Các bộ phận của kính hiển vi quang học'),
    ('sinh6/bai-18/te-bao-don-vi-co-ban.json', 1, 'c-s6-b18-hinh-dang-te-bao.svg', 'Một số hình dạng tế bào (sơ đồ minh họa)'),
    ('sinh6/bai-19/cau-tao-te-bao.json', 1, 'c-s6-b19-nhan-so-nhan-thuc.svg', 'Tế bào nhân sơ và tế bào nhân thực'),
    ('sinh6/bai-19/cau-tao-te-bao.json', 3, 'c-s6-b19-thuc-vat-dong-vat.svg', 'So sánh tế bào thực vật và tế bào động vật'),
]


# ---------- Bài 20: phân chia tế bào ----------
def mini_cell(b, x, y, r=26, nuc=1, split=0.0, dash=False):
    b.append(C(x, y, r, fill=CELL, stroke=INK, w=2.4))
    b.append(C(x, y, r * 0.4, fill=NUC, stroke=INK, w=1.6))


def fig_phan_chia():
    b = [title(720, 'Sự sinh sản (phân chia) của tế bào')]
    y = 100
    # 1) tế bào lớn lên  2) nhân chia  3) chất chia  4) hai tế bào con
    # a: tế bào non nhỏ -> lớn
    b.append(C(60, y + 12, 16, fill=CELL, stroke=INK, w=2.4)); b.append(C(60, y + 12, 6, fill=NUC, stroke=INK, w=1.4))
    b.append(L(88, y, 112, y, w=2.4, arrow=True))
    b.append(C(170, y, 42, fill=CELL, stroke=INK, w=2.6)); b.append(C(170, y, 16, fill=NUC, stroke=INK, w=1.8))
    b.append(T(115, y - 60, 'Lớn lên', size=13, weight='bold', fill=BLUE))
    b.append(L(222, y, 252, y, w=2.4, arrow=True))
    # b: nhân chia
    b.append(C(310, y, 42, fill=CELL, stroke=INK, w=2.6))
    b.append(C(294, y, 11, fill=NUC, stroke=INK, w=1.6)); b.append(C(326, y, 11, fill=NUC, stroke=INK, w=1.6))
    b.append(T(310, y - 56, 'Nhân phân chia', size=13, weight='bold', fill=BLUE))
    b.append(L(362, y, 392, y, w=2.4, arrow=True))
    # c: chất tế bào chia (eo thắt)
    b.append(ELL(450, y, 52, 38, fill=CELL, stroke=INK, w=2.6))
    b.append(L(450, y - 33, 450, y + 33, stroke=INK, w=2.4, dash='4 3'))
    b.append(C(426, y, 11, fill=NUC, stroke=INK, w=1.6)); b.append(C(474, y, 11, fill=NUC, stroke=INK, w=1.6))
    b.append(T(450, y - 56, 'Chất tế bào phân chia', size=13, weight='bold', fill=BLUE))
    b.append(L(512, y, 542, y, w=2.4, arrow=True))
    # d: hai tế bào con
    for dx in (-30, 30):
        b.append(C(610 + dx, y, 28, fill=CELL, stroke=INK, w=2.4)); b.append(C(610 + dx, y, 10, fill=NUC, stroke=INK, w=1.5))
    b.append(T(610, y - 56, '2 tế bào con', size=13, weight='bold', fill=BLUE))
    # hàng dưới: 2^n
    y2 = 215
    b.append(T(360, 170, 'Từ 1 tế bào, sau n lần phân chia: 2ⁿ tế bào', size=14, weight='bold'))
    cols = [(110, 1), (240, 2), (400, 4), (580, 8)]
    for x0, n in cols:
        for k in range(n):
            if n <= 4:
                cxk = x0 + (k - (n - 1) / 2) * 30
                cyk = y2
            else:
                cxk = x0 + (k % 4 - 1.5) * 30
                cyk = y2 - 14 + (k // 4) * 28
            b.append(C(cxk, cyk, 11, fill=CELL, stroke=INK, w=1.8)); b.append(C(cxk, cyk, 4, fill=NUC, stroke='none', w=0))
    labs = [(110, '0 lần: 1 = 2⁰'), (240, '1 lần: 2 = 2¹'), (400, '2 lần: 4 = 2²'), (580, '3 lần: 8 = 2³')]
    for x0, t in labs:
        b.append(T(x0, 262, t, size=13))
    return svg(720, 282, ''.join(b))


# ---------- Bài 22: đơn bào – đa bào ----------
def fig_don_bao_da_bao():
    b = [title(720, 'Cơ thể đơn bào và cơ thể đa bào')]
    b.append(R(20, 44, 320, 220, fill='#f4f9f2', stroke=GREY, sw=1.4, rx=10))
    b.append(R(380, 44, 320, 220, fill='#f4f6fb', stroke=GREY, sw=1.4, rx=10))
    b.append(T(180, 66, 'Cơ thể đơn bào: 1 tế bào', size=15, weight='bold'))
    b.append(T(540, 66, 'Cơ thể đa bào: nhiều tế bào', size=15, weight='bold'))
    # trùng roi
    b.append(ELL(90, 130, 34, 18, fill='#cfe6c4', stroke=INK, w=2.4)); b.append(C(96, 130, 7, fill=NUC, stroke=INK, w=1.4))
    b.append(squig(56, 130, 28, 118, amp=3, n=2, stroke=INK, w=2))
    b.append(T(90, 170, 'trùng roi xanh', size=13))
    # vi khuẩn que
    b.append(R(165, 118, 56, 24, fill=CELL, stroke=INK, sw=2.4, rx=12))
    b.append(T(193, 170, 'vi khuẩn', size=13))
    # nấm men
    b.append(C(275, 134, 18, fill=CELL, stroke=INK, w=2.4)); b.append(C(299, 120, 10, fill=CELL, stroke=INK, w=2.2))
    b.append(C(275, 134, 6, fill=NUC, stroke=INK, w=1.2))
    b.append(T(285, 170, 'nấm men', size=13))
    b.append(T(180, 215, 'Một tế bào thực hiện mọi', size=13, fill=GREY)); b.append(T(180, 233, 'chức năng sống', size=13, fill=GREY))
    # đa bào: cụm tế bào các loại khác nhau
    import random
    rnd = random.Random(7)
    cols = ['#cfe6c4', '#e9b8a6', '#d8c5ee', '#cfe0f0']
    kinds = [(420, 100), (460, 100), (500, 100), (440, 130), (480, 130), (520, 130), (420, 160), (460, 160), (500, 160)]
    for i, (x, y) in enumerate(kinds):
        b.append(R(x - 18, y - 14, 36, 28, fill=cols[(i // 3) % 3], stroke=INK, sw=1.8, rx=4))
        b.append(C(x, y, 4.5, fill=NUC, stroke='none', w=0))
    b.append(L(540, 130, 586, 130, stroke=INK, w=2, arrow=True)) if False else None
    for k, (nm, col) in enumerate((('mô biểu bì', '#cfe6c4'), ('mô cơ', '#e9b8a6'), ('mô thần kinh', '#d8c5ee'))):
        b.append(R(590, 90 + k * 26, 22, 18, fill=col, stroke=INK, sw=1.4, rx=3))
        b.append(T(620, 104 + k * 26, nm, size=13, anchor='start'))
    b.append(T(540, 215, 'Mỗi loại tế bào đảm nhận', size=13, fill=GREY)); b.append(T(540, 233, 'một chức năng khác nhau', size=13, fill=GREY))
    b.append(T(540, 255, 'ví dụ: cây xoài, con chó, con người', size=13))
    b.append(T(180, 255, 'ví dụ: vi khuẩn, trùng roi, nấm men', size=13))
    return svg(720, 280, ''.join(b))


# ---------- Bài 23: tổ chức cơ thể đa bào ----------
def heart_shape(cx, cy, s=1.0, fill='#e15759'):
    return PATH('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z' % (
        cx, cy + 22 * s, cx - 30 * s, cy + 4 * s, cx - 28 * s, cy - 24 * s, cx - 10 * s, cy - 18 * s,
        cx - 4 * s, cy - 16 * s, cx - 1 * s, cy - 12 * s, cx, cy - 8 * s,
        cx + 1 * s, cy - 12 * s, cx + 4 * s, cy - 16 * s, cx + 10 * s, cy - 18 * s,
        cx + 28 * s, cy - 24 * s, cx + 30 * s, cy + 4 * s, cx, cy + 22 * s), fill=fill, stroke=INK, w=2.2)


def person(cx, cy, s=1.0, fill='#cfe0f0'):
    o = [C(cx, cy - 36 * s, 10 * s, fill=fill, stroke=INK, w=2)]
    o.append(R(cx - 12 * s, cy - 24 * s, 24 * s, 40 * s, fill=fill, stroke=INK, sw=2, rx=6 * s))
    o.append(L(cx - 12 * s, cy - 20 * s, cx - 22 * s, cy + 6 * s, stroke=INK, w=4 * s))
    o.append(L(cx + 12 * s, cy - 20 * s, cx + 22 * s, cy + 6 * s, stroke=INK, w=4 * s))
    o.append(L(cx - 5 * s, cy + 16 * s, cx - 7 * s, cy + 46 * s, stroke=INK, w=5 * s))
    o.append(L(cx + 5 * s, cy + 16 * s, cx + 7 * s, cy + 46 * s, stroke=INK, w=5 * s))
    return ''.join(o)


def fig_cap_to_chuc_nguoi():
    b = [title(720, 'Các cấp độ tổ chức của cơ thể đa bào (ví dụ ở người)')]
    xs = [70, 215, 360, 505, 650]
    y = 120
    # tế bào cơ tim
    b.append(R(xs[0] - 8, y - 38, 16, 76, fill='#e9b8a6', stroke=INK, sw=2.2, rx=8)); b.append(ELL(xs[0], y, 5, 8, fill=NUC, stroke=INK, w=1))
    # mô cơ: nhiều tế bào song song
    for k in range(-2, 3):
        b.append(R(xs[1] + k * 14 - 6, y - 36, 12, 72, fill='#e9b8a6', stroke=INK, sw=1.8, rx=6))
        b.append(ELL(xs[1] + k * 14, y + (k % 2) * 10 - 5, 3.5, 6, fill=NUC, stroke='none', w=0))
    # cơ quan: tim
    b.append(heart_shape(xs[2], y, 1.3))
    # hệ cơ quan: tim + mạch máu
    b.append(heart_shape(xs[3], y - 10, 0.8))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (xs[3] - 10, y - 30, xs[3] - 50, y - 60, xs[3] - 60, y + 20, xs[3] - 20, y + 40), stroke='#c0392b', w=3))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (xs[3] + 10, y - 30, xs[3] + 50, y - 60, xs[3] + 60, y + 20, xs[3] + 20, y + 40), stroke=BLUE, w=3))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (xs[3] - 20, y + 40, xs[3] - 10, y + 52, xs[3] + 10, y + 52, xs[3] + 20, y + 40), stroke=INK, w=2))
    # cơ thể
    b.append(person(xs[4], y, 1.7))
    for i in range(4):
        b.append(L(xs[i] + 52, y, xs[i + 1] - 52, y, stroke=GREY, w=2, arrow=True)) if False else b.append(L(xs[i] + 50, y, xs[i + 1] - 50, y, stroke=BLUE, w=2.4, arrow=True))
    names = ['Tế bào', 'Mô', 'Cơ quan', 'Hệ cơ quan', 'Cơ thể']
    exs = ['tế bào cơ tim', 'mô cơ tim', 'tim', 'hệ tuần hoàn', 'cơ thể người']
    for x, n, e in zip(xs, names, exs):
        b.append(T(x, 232, n, size=16, weight='bold')); b.append(T(x, 252, e, size=13, fill=GREY))
    b.append(T(360, 286, 'Tế bào → Mô → Cơ quan → Hệ cơ quan → Cơ thể', size=14, weight='bold', fill=BLUE))
    return svg(720, 304, ''.join(b))


def fig_he_co_quan_thuc_vat():
    b = [title(720, 'Hai hệ cơ quan ở thực vật: hệ chồi và hệ rễ')]
    gx = 360
    b.append(R(120, 210, 480, 60, fill='#cdb48f', stroke=INK, sw=2, rx=3))  # đất
    b.append(L(120, 210, 600, 210, w=2.4))
    b.append(L(gx, 210, gx, 100, stroke='#6d8f3b', w=10))                  # thân
    for (dx, dy, ang) in ((-1, 150, 1), (1, 130, 1), (-1, 112, 1)):
        x2 = gx + dx * 62
        b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d Z' % (gx, dy, gx + dx * 32, dy - 26, x2, dy - 10, gx + dx * 32, dy + 14, gx, dy), fill='#7fbf6a', stroke=INK, w=2))
    b.append(PATH('M%d,%d Q%d,%d %d,%d' % (gx, 100, gx + 6, 78, gx, 60), stroke='#6d8f3b', w=6)) if False else None
    b.append(C(gx, 86, 14, fill='#f6c9d4', stroke=INK, w=2))             # hoa
    for a in range(0, 360, 72):
        px, py = pt(gx, 86, 16, a)
        b.append(C(px, py, 9, fill='#f4a6bd', stroke=INK, w=1.4))
    b.append(C(gx, 86, 6, fill='#f3c744', stroke=INK, w=1.2))
    b.append(C(gx + 56, 168, 11, fill='#e8863a', stroke=INK, w=2)) # quả
    b.append(L(gx + 56, 168, gx + 12, 160, stroke='#6d8f3b', w=3))
    # rễ
    for dx in (-90, -48, 0, 48, 90):
        b.append(PATH('M%d,%d Q%d,%d %d,%d' % (gx, 212, gx + dx * 0.5, 240, gx + dx, 262), stroke='#8a5a2b', w=3.5))
    b.append(PATH('M%d,%d L%d,%d' % (gx, 212, gx, 266), stroke='#8a5a2b', w=5))
    # ngoặc nhóm
    b.append(PATH('M%d,%d L%d,%d L%d,%d' % (500, 56, 510, 56, 510, 204), stroke=GREEN, w=2.4))
    b.append(T(520, 82, 'Hệ chồi', size=16, weight='bold', fill=GREEN, anchor='start'))
    b.append(T(520, 102, 'thân, lá, hoa, quả', size=13, anchor='start'))
    b.append(PATH('M%d,%d L%d,%d L%d,%d' % (500, 214, 510, 214, 510, 268), stroke='#8a5a2b', w=2.4))
    b.append(T(520, 236, 'Hệ rễ', size=16, weight='bold', fill='#8a5a2b', anchor='start'))
    lead(b, gx - 62, 140, 190, 120, 'lá', anchor='end')
    lead(b, gx, 190, 190, 168, 'thân', anchor='end')
    lead(b, gx - 14, 86, 190, 70, 'hoa', anchor='end')
    lead(b, gx + 60, 172, 440, 190, 'quả', anchor='start') if False else None
    b.append(T(gx + 82, 176, 'quả', size=13, anchor='start'))
    return svg(720, 284, ''.join(b))


# ---------- Bài 25: phân loại ----------
def fig_bac_phan_loai():
    b = [title(720, 'Các bậc phân loại (từ thấp đến cao) – ví dụ: người')]
    ranks = ['Loài', 'Chi (giống)', 'Họ', 'Bộ', 'Lớp', 'Ngành', 'Giới']
    ex = ['Homo sapiens (người)', 'Homo', 'Hominidae', 'Linh trưởng', 'Thú', 'Dây sống', 'Động vật']
    n = len(ranks)
    for i, (r_, e) in enumerate(zip(ranks, ex)):
        y = 262 - i * 32
        w = 120 + i * 36
        x = 40
        shade = ['#fbe6d4', '#f9dcc0', '#f6d2ad', '#f3c79a', '#f0bc87', '#eeb174', '#ec9f56'][i]
        b.append(R(x, y, w, 28, fill=shade, stroke=INK, sw=1.8, rx=5))
        b.append(T(x + w / 2, y + 19, r_, size=14, weight='bold'))
        b.append(T(x + w + 14, y + 19, e, size=14, anchor='start', fill=INK))
    b.append(L(580, 250, 580, 56, stroke=BLUE, w=2.4, arrow=True))
    b.append(T(596, 150, 'bậc cao', size=13, fill=BLUE, anchor='start')) if False else None
    b.append(T(600, 70, 'bậc cao hơn', size=13, fill=BLUE, anchor='start'))
    b.append(T(600, 255, 'bậc thấp', size=13, fill=BLUE, anchor='start'))
    return svg(720, 300, ''.join(b))


def fig_nam_gioi():
    b = [title(720, 'Hệ thống năm giới sinh vật')]
    items = [('Khởi sinh', ['vi khuẩn'], 'nhân sơ', '#f7d9a8'), ('Nguyên sinh', ['tảo,', 'trùng giày'], 'nhân thực', '#cfe6c4'),
             ('Nấm', ['nấm men,', 'nấm rơm'], 'nhân thực', '#e9c6d5'), ('Thực vật', ['rêu, dương xỉ,', 'cây hạt'], 'nhân thực', '#b8dba6'),
             ('Động vật', ['giun, cá,', 'chim, thú'], 'nhân thực', '#cfe0f0')]
    for i, (g, ex, f, col) in enumerate(items):
        x = 20 + i * 140
        b.append(R(x, 60, 128, 150, fill=col, stroke=INK, sw=2, rx=10))
        b.append(T(x + 64, 92, 'Giới', size=13, fill=GREY)); b.append(T(x + 64, 114, g, size=16, weight='bold'))
        b.append(L(x + 14, 126, x + 114, 126, stroke=INK, w=1))
        b.append(TL(x + 64, 148, ex, size=12.5))
        b.append(T(x + 64, 196, f, size=11.5, fill=GREY))
    b.append(T(360, 238, 'Giới Khởi sinh: tế bào nhân sơ; bốn giới còn lại: tế bào nhân thực', size=13, weight='bold', fill=BLUE))
    return svg(720, 258, ''.join(b))

FIGS.update({
    'c-s6-b20-phan-chia.svg': fig_phan_chia,
    'c-s6-b22-don-bao-da-bao.svg': fig_don_bao_da_bao,
    'c-s6-b23-cap-to-chuc.svg': fig_cap_to_chuc_nguoi,
    'c-s6-b23-he-co-quan-thuc-vat.svg': fig_he_co_quan_thuc_vat,
    'c-s6-b25-bac-phan-loai.svg': fig_bac_phan_loai,
    'c-s6-b25-nam-gioi.svg': fig_nam_gioi,
})
ATTACH += [
    ('sinh6/bai-20/lon-len-sinh-san-te-bao.json', 1, 'c-s6-b20-phan-chia.svg', 'Quá trình phân chia tế bào và số tế bào sau n lần phân chia'),
    ('sinh6/bai-22/co-the-sinh-vat.json', 2, 'c-s6-b22-don-bao-da-bao.svg', 'Cơ thể đơn bào và cơ thể đa bào (sơ đồ minh họa)'),
    ('sinh6/bai-23/to-chuc-co-the-da-bao.json', 2, 'c-s6-b23-cap-to-chuc.svg', 'Các cấp độ tổ chức của cơ thể đa bào'),
    ('sinh6/bai-23/to-chuc-co-the-da-bao.json', 5, 'c-s6-b23-he-co-quan-thuc-vat.svg', 'Hệ chồi và hệ rễ ở thực vật'),
    ('sinh6/bai-25/he-thong-phan-loai.json', 2, 'c-s6-b25-bac-phan-loai.svg', 'Các bậc phân loại sinh vật'),
    ('sinh6/bai-25/he-thong-phan-loai.json', 4, 'c-s6-b25-nam-gioi.svg', 'Năm giới sinh vật'),
]


# ---------- Bài 26: khoá lưỡng phân ----------
def qbox(b, x, y, text, w=150, h=40, fill='#fbf0c9'):
    b.append(R(x - w / 2, y - h / 2, w, h, fill=fill, stroke=INK, sw=2, rx=8))
    b.append(T(x, y + 5, text, size=14, weight='bold'))


def fig_khoa_luong_phan():
    b = [title(720, 'Ví dụ khoá lưỡng phân: 4 sinh vật – 3 bước chia')]
    qbox(b, 330, 62, 'Có lông vũ?')
    qbox(b, 500, 150, 'Có lông mao?')
    qbox(b, 600, 240, 'Có chân?')
    leaf = lambda x, y, t: (b.append(R(x - 55, y - 20, 110, 40, fill=LGREEN, stroke=INK, sw=2, rx=20)), b.append(T(x, y + 5, t, size=14, weight='bold')))
    leaf(150, 150, 'Chim bồ câu'); leaf(370, 240, 'Thỏ'); leaf(505, 320, 'Ếch'); leaf(645, 320, 'Cá chép')
    def edge(x1, y1, x2, y2, t, tx, ty):
        b.append(L(x1, y1, x2, y2, stroke=INK, w=2, arrow=True))
        b.append(H(tx, ty, t, size=13, fill=BLUE))
    edge(290, 80, 175, 128, 'Có', 215, 96)
    edge(370, 80, 460, 130, 'Không', 440, 96)
    edge(460, 168, 395, 218, 'Có', 418, 186)
    edge(540, 168, 580, 218, 'Không', 580, 190)
    edge(575, 258, 530, 298, 'Có', 538, 274)
    edge(625, 258, 640, 298, 'Không', 660, 278)
    b.append(T(110, 290, 'n = 4 sinh vật', size=13, weight='bold'))
    b.append(T(110, 310, 'cần n − 1 = 3 bước', size=13, weight='bold'))
    return svg(720, 350, ''.join(b))


# ---------- Bài 27: vi khuẩn ----------
def fig_vi_khuan():
    b = [title(720, 'Cấu tạo và hình dạng của vi khuẩn')]
    cx, cy = 195, 150
    for k in range(-5, 6):
        for sgn in (-1, 1):
            b.append(L(cx + k * 15, cy + sgn * 48, cx + k * 15 + 3, cy + sgn * 60, stroke='#8a7a55', w=1.6)) if abs(k) < 4 else None
    b.append(R(cx - 100, cy - 48, 200, 96, fill='#d9c9a3', stroke=INK, sw=3, rx=48))
    b.append(R(cx - 94, cy - 42, 188, 84, fill=CELL, stroke='#7a6a45', sw=1.8, rx=42))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d' % (
        cx - 36, cy + 4, cx - 24, cy - 28, cx - 8, cy + 26, cx + 6, cy - 12, cx + 18, cy - 32, cx + 28, cy + 26, cx + 40, cy - 4, cx + 50, cy - 14, cx + 24, cy + 10, cx - 4, cy + 8), stroke='#6a4c93', w=3))
    b.append(squig(cx - 100, cy, cx - 168, cy + 8, amp=6, n=4, stroke=INK, w=2.4))
    lead(b, cx - 150, cy + 6, 20, 215, 'roi', anchor='start')
    lead(b, cx + 60, cy - 55, 255, 52, 'lông', anchor='start')
    lead(b, cx + 98, cy - 20, 330, 82, 'thành tế bào', anchor='start')
    lead(b, cx + 90, cy + 20, 330, 218, 'màng tế bào', anchor='start')
    lead(b, cx - 50, cy + 25, 40, 234, 'chất tế bào', anchor='start') if False else lead(b, cx - 60, cy + 26, 75, 236, 'chất tế bào', anchor='start')
    lead(b, cx + 18, cy - 14, 200, 90, 'vùng nhân', anchor='start') if False else lead(b, cx + 18, cy - 14, 130, 74, 'vùng nhân', anchor='start')
    # hình dạng
    shapes = [(470, 90, 'hình cầu', 'cầu khuẩn'), (630, 90, 'hình que', 'trực khuẩn'), (470, 200, 'hình xoắn', 'xoắn khuẩn'), (630, 200, 'hình dấu phẩy', 'phẩy khuẩn')]
    for x, y, a, c in shapes:
        pass
    for dx in (-18, 0, 18):
        b.append(C(470 + dx, 76, 11, fill=CELL, stroke=INK, w=2))
    b.append(C(470 - 9, 98, 11, fill=CELL, stroke=INK, w=2)); b.append(C(470 + 9, 98, 11, fill=CELL, stroke=INK, w=2))
    b.append(R(600, 70, 60, 20, fill=CELL, stroke=INK, sw=2, rx=10)); b.append(R(610, 94, 60, 20, fill=CELL, stroke=INK, sw=2, rx=10))
    pts = [(440 + t * 60 / 60, 202 + 12 * math.sin(2 * math.pi * 3 * t / 60)) for t in range(61)]
    b.append(PL(pts, stroke=INK, w=8)); b.append(PL(pts, stroke=CELL, w=4.5))
    b.append(PATH('M610,176 Q650,176 648,206 Q647,218 640,224', stroke=INK, w=10)); b.append(PATH('M610,176 Q650,176 648,206 Q647,218 640,224', stroke=CELL, w=6.5))
    for x, y, a, c in shapes:
        b.append(T(x, y + 50 if y < 150 else y + 50, a, size=14, weight='bold')); b.append(T(x, y + 68, c, size=12.5, fill=GREY))
    return svg(720, 300, ''.join(b))


# ---------- Bài 29: virus ----------
def hexagon(cx, cy, r, rot=0):
    return [(cx + r * math.cos(math.radians(rot + 60 * k)), cy + r * math.sin(math.radians(rot + 60 * k))) for k in range(6)]


def fig_virus():
    b = [title(720, 'Cấu tạo và hình dạng một số virus (sơ đồ)')]
    # dạng xoắn
    x0, y0 = 40, 100
    b.append(R(x0, y0, 150, 34, fill='#cfe0f0', stroke=INK, sw=2.4, rx=6))
    for k in range(0, 150, 10):
        b.append(L(x0 + k, y0, x0 + k + 10, y0 + 34, stroke='#7fa6cf', w=1.6))
    b.append(L(x0 + 6, y0 + 17, x0 + 144, y0 + 17, stroke=RED, w=3))
    lead(b, x0 + 30, y0, 20, 62, 'vỏ protein', anchor='start')
    lead(b, x0 + 100, y0 + 17, 70, 186, 'lõi vật chất di truyền', anchor='start')
    b.append(T(x0 + 75, 224, 'Dạng xoắn', size=14, weight='bold')); b.append(T(x0 + 75, 243, '(virus khảm thuốc lá)', size=12.5, fill=GREY))
    # dạng khối
    cx, cy = 360, 125
    b.append(POLY(hexagon(cx, cy, 52, 0), fill='#cfe0f0', stroke=INK, sw=2.6))
    b.append(POLY(hexagon(cx, cy, 26, 0), fill='#f7c8c8', stroke=RED, sw=2))
    for (px, py) in hexagon(cx, cy, 52, 0):
        ex, ey = cx + (px - cx) * 1.28, cy + (py - cy) * 1.28
        b.append(L(px, py, ex, ey, stroke=INK, w=2)); b.append(C(ex, ey, 4, fill=INK, stroke=INK, w=1))
    lead(b, cx - 40, cy - 30, 290, 50, 'vỏ protein', anchor='end') if False else lead(b, cx - 46, cy - 22, 262, 50, 'vỏ protein', anchor='end')
    lead(b, cx, cy, 440, 62, 'lõi (vật chất di truyền)', anchor='start') if False else lead(b, cx + 10, cy, 410, 46, 'lõi vật chất di truyền', anchor='start')
    b.append(T(cx, 224, 'Dạng khối', size=14, weight='bold')); b.append(T(cx, 243, '(virus adeno)', size=12.5, fill=GREY))
    # thể thực khuẩn
    px, py = 610, 78
    b.append(POLY(hexagon(px, py, 30, 30), fill='#cfe0f0', stroke=INK, sw=2.4))
    b.append(POLY(hexagon(px, py, 15, 30), fill='#f7c8c8', stroke=RED, sw=1.8))
    b.append(R(px - 6, py + 28, 12, 62, fill='#9db4c9', stroke=INK, sw=2))
    b.append(POLY([(px - 18, py + 90), (px + 18, py + 90), (px + 14, py + 100), (px - 14, py + 100)], fill='#7d8b99', stroke=INK, sw=2))
    for dx in (-30, -16, 16, 30):
        b.append(PL([(px + dx * 0.4, py + 98), (px + dx, py + 118), (px + dx * 1.4, py + 134)], stroke=INK, w=2))
    lead(b, px + 14, py - 6, 668, 52, 'vỏ protein', anchor='start') if False else lead(b, px + 20, py - 14, 650, 42, 'vỏ protein', anchor='start')
    lead(b, px, py, 530, 56, 'lõi', anchor='end') if False else lead(b, px - 8, py - 4, 548, 70, 'lõi', anchor='end')
    b.append(T(px, 224, 'Dạng hỗn hợp', size=14, weight='bold')); b.append(T(px, 243, '(thể thực khuẩn)', size=12.5, fill=GREY))
    b.append(T(360, 275, 'Virus chưa có cấu tạo tế bào; kích thước khoảng 20–300 nm', size=13, fill=GREY))
    return svg(720, 292, ''.join(b))


# ---------- Bài 30: nguyên sinh vật ----------
def fig_nguyen_sinh_vat():
    b = [title(720, 'Một số nguyên sinh vật (sơ đồ)')]
    # trùng roi xanh
    cx, cy = 120, 120
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx - 50, cy, cx - 40, cy - 40, cx + 30, cy - 38, cx + 55, cy, cx + 30, cy + 38, cx - 40, cy + 40, cx - 50, cy), fill='#cfe6c4', stroke=INK, w=2.6))
    b.append(squig(cx - 50, cy, cx - 90, cy - 14, amp=4, n=2.5, stroke=INK, w=2.2))
    b.append(C(cx + 20, cy - 6, 10, fill=NUC, stroke=INK, w=1.8))
    for (dx, dy) in ((-14, 14), (-24, -12), (2, 18)):
        b.append(ELL(cx + dx, cy + dy, 7, 4, fill=CHL, stroke=INK, w=1.2))
    b.append(C(cx - 40, cy - 6, 3.5, fill=RED, stroke='none', w=0))
    lead(b, cx - 86, cy - 12, 20, 52, 'roi', anchor='start')
    lead(b, cx - 40, cy - 6, 70, 66, 'điểm mắt', anchor='start') if False else lead(b, cx - 40, cy - 7, 6, 168, 'điểm mắt', anchor='start')
    lead(b, cx + 22, cy - 10, 140, 52, 'nhân', anchor='start')
    lead(b, cx - 14, cy + 15, 90, 205, 'hạt diệp lục', anchor='start')
    b.append(T(cx, 238, 'Trùng roi xanh', size=14, weight='bold')); b.append(T(cx, 257, '(tự dưỡng)', size=12.5, fill=GREY))
    # trùng giày
    cx, cy = 370, 120
    b.append(ELL(cx, cy, 78, 36, fill='#fbf0c9', stroke=INK, w=2.6))
    for k in range(24):
        th = 2 * math.pi * k / 24
        x1_, y1_ = cx + 78 * math.cos(th), cy + 36 * math.sin(th)
        nx, ny = math.cos(th) / 78, math.sin(th) / 36
        nl = math.hypot(nx, ny)
        b.append(L(x1_, y1_, x1_ + 8 * nx / nl, y1_ + 8 * ny / nl, stroke='#8a7a55', w=1.5))
    b.append(C(cx + 6, cy - 2, 12, fill=NUC, stroke=INK, w=1.8))
    b.append(C(cx - 40, cy + 12, 8, fill='#dbe9f6', stroke='#7a8fa5', w=1.4)); b.append(C(cx + 48, cy + 8, 8, fill='#dbe9f6', stroke='#7a8fa5', w=1.4))
    lead(b, cx - 40, cy - 40, 280, 52, 'lông bơi', anchor='start') if False else lead(b, cx + 40, cy - 40, 420, 50, 'lông bơi', anchor='start')
    lead(b, cx + 6, cy - 2, 410, 205, 'nhân', anchor='start') if False else lead(b, cx + 6, cy + 4, 440, 195, 'nhân', anchor='start')
    lead(b, cx - 40, cy + 14, 270, 205, 'không bào co bóp', anchor='start') if False else lead(b, cx - 40, cy + 18, 296, 205, 'không bào co bóp', anchor='start')
    b.append(T(cx, 238, 'Trùng giày', size=14, weight='bold')); b.append(T(cx, 257, '(dị dưỡng)', size=12.5, fill=GREY))
    # trùng biến hình
    cx, cy = 610, 118
    pts = []
    for k in range(120):
        th = 2 * math.pi * k / 120
        r_ = 38 + 4 * math.sin(3 * th + 1)
        for ang, amp in ((200, 34), (320, 26), (80, 22)):
            d = math.atan2(math.sin(th - math.radians(ang)), math.cos(th - math.radians(ang)))
            r_ += amp * math.exp(-(d / 0.28) ** 2)
        pts.append((cx + r_ * math.cos(th), cy - r_ * math.sin(th) * 0.9))
    b.append(POLY(pts, fill='#fbe3d0', stroke=INK, sw=2.6))
    b.append(C(cx, cy + 2, 13, fill=NUC, stroke=INK, w=1.8)); b.append(C(cx + 30, cy + 16, 9, fill='#dbe9f6', stroke='#7a8fa5', w=1.4))
    lead(b, cx - 68, cy + 2, 520, 62, 'chân giả', anchor='start') if False else lead(b, cx - 63, cy + 22, 505, 178, 'chân giả', anchor='start')
    lead(b, cx, cy - 10, 590, 56, 'nhân', anchor='start') if False else lead(b, cx + 2, cy - 4, 640, 56, 'nhân', anchor='start')
    lead(b, cx + 32, cy + 20, 640, 205, 'không bào tiêu hoá', anchor='start') if False else lead(b, cx + 34, cy + 22, 520, 205, 'không bào tiêu hoá', anchor='start')
    b.append(T(cx, 238, 'Trùng biến hình', size=14, weight='bold')); b.append(T(cx, 257, '(dị dưỡng)', size=12.5, fill=GREY))
    return svg(720, 276, ''.join(b))

FIGS.update({
    'c-s6-b26-khoa-luong-phan.svg': fig_khoa_luong_phan,
    'c-s6-b27-vi-khuan.svg': fig_vi_khuan,
    'c-s6-b29-virus.svg': fig_virus,
    'c-s6-b30-nguyen-sinh-vat.svg': fig_nguyen_sinh_vat,
})
ATTACH += [
    ('sinh6/bai-26/khoa-luong-phan.json', 1, 'c-s6-b26-khoa-luong-phan.svg', 'Ví dụ về khoá lưỡng phân'),
    ('sinh6/bai-27/vi-khuan.json', 0, 'c-s6-b27-vi-khuan.svg', 'Cấu tạo và hình dạng vi khuẩn'),
    ('sinh6/bai-29/virus.json', 1, 'c-s6-b29-virus.svg', 'Cấu tạo và hình dạng một số virus'),
    ('sinh6/bai-30/nguyen-sinh-vat.json', 1, 'c-s6-b30-nguyen-sinh-vat.svg', 'Một số nguyên sinh vật'),
]


# ---------- Bài 32: nấm ----------
def fig_nam():
    b = [title(720, 'Một số dạng nấm (sơ đồ)')]
    # nấm men nảy chồi
    b.append(C(80, 130, 26, fill=CELL, stroke=INK, w=2.4)); b.append(C(80, 130, 9, fill=NUC, stroke=INK, w=1.4))
    b.append(C(114, 112, 14, fill=CELL, stroke=INK, w=2.2)); b.append(C(114, 112, 5, fill=NUC, stroke=INK, w=1.2))
    b.append(C(52, 172, 12, fill=CELL, stroke=INK, w=2)); b.append(C(52, 172, 4, fill=NUC, stroke=INK, w=1))
    lead(b, 118, 106, 170, 64, 'chồi', anchor='start')
    b.append(T(90, 232, 'Nấm men', size=14, weight='bold')); b.append(T(90, 251, '(đơn bào, nảy chồi)', size=12.5, fill=GREY))
    # nấm mốc: sợi nấm + túi bào tử
    ox, oy = 300, 190
    b.append(L(ox - 80, oy, ox + 80, oy, stroke='#8a7a55', w=3))
    for dx in (-50, 0, 50):
        b.append(PL([(ox + dx, oy), (ox + dx, oy - 50)], stroke='#8a7a55', w=3))
        b.append(C(ox + dx, oy - 58, 12, fill='#9bb7a8', stroke=INK, w=2))
        for k in range(5):
            a = math.radians(30 + k * 30)
            b.append(C(ox + dx + 20 * math.cos(a), oy - 58 - 20 * math.sin(a), 2.2, fill=INK, stroke='none', w=0))
    for dx in (-70, -25, 25, 70):
        b.append(PL([(ox + dx, oy), (ox + dx - 8, oy + 22), (ox + dx - 2, oy + 34)], stroke='#8a7a55', w=1.8))
    lead(b, ox - 50, oy - 30, 200, 70, 'sợi nấm', anchor='start') if False else lead(b, ox - 40, oy, 210, 232, 'sợi nấm', anchor='start') if False else None
    lead(b, ox, oy - 58, 340, 54, 'túi bào tử', anchor='start')
    lead(b, ox - 20, oy, 215, 215, 'sợi nấm', anchor='start') if False else lead(b, ox + 30, oy, 365, 214, 'sợi nấm', anchor='start')
    b.append(T(ox, 249, 'Nấm mốc', size=14, weight='bold')); b.append(T(ox, 268, '(đa bào, hệ sợi nấm)', size=12.5, fill=GREY))
    # nấm lớn
    cx = 560
    b.append(R(cx - 120, 196, 240, 14, fill='#cdb48f', stroke=INK, sw=2, rx=3))
    b.append(PATH('M%d,%d Q%d,%d %d,%d Z' % (cx - 56, 112, cx, 40, cx + 56, 112), fill='#d9a36a', stroke=INK, w=2.6))
    b.append(L(cx - 54, 112, cx + 54, 112, stroke=INK, w=2.6))
    for k in range(-4, 5):
        b.append(L(cx + k * 12, 112, cx + k * 11, 124, stroke='#8a6a3a', w=1.6))
    b.append(R(cx - 11, 112, 22, 84, fill='#f4e6cd', stroke=INK, sw=2.4))
    for dx in (-80, -40, 40, 80):
        b.append(PL([(cx + dx * 0.3, 210), (cx + dx * 0.6, 236), (cx + dx, 246)], stroke='#8a7a55', w=2))
    lead(b, cx + 40, 78, 650, 46, 'mũ nấm', anchor='start')
    lead(b, cx + 11, 150, 650, 150, 'thân nấm', anchor='start')
    lead(b, cx + 58, 241, 640, 232, 'sợi nấm trong đất', anchor='end') if False else lead(b, cx + 50, 242, 650, 236, 'hệ sợi nấm', anchor='start')
    b.append(T(cx, 268, 'Nấm lớn (nấm rơm, nấm hương…)', size=14, weight='bold')) if False else b.append(T(cx - 20, 268, 'Nấm lớn (ví dụ: nấm rơm)', size=14, weight='bold'))
    b.append(T(360, 292, 'Nấm không có lục lạp nên sống dị dưỡng; nấm lớn sinh sản bằng bào tử', size=13, fill=GREY))
    return svg(720, 310, ''.join(b))


# ---------- Bài 34: các nhóm thực vật ----------
def fig_nhom_thuc_vat():
    b = [title(720, 'Các nhóm thực vật chính')]
    xs = [95, 275, 455, 635]
    gy = 190
    for x in xs:
        b.append(L(x - 70, gy, x + 70, gy, stroke='#8a5a2b', w=3))
    # rêu
    for dx in (-30, -12, 8, 26):
        b.append(L(xs[0] + dx, gy, xs[0] + dx, gy - 30, stroke='#4a7d3a', w=3))
        for k in range(5):
            b.append(L(xs[0] + dx, gy - 6 - k * 5, xs[0] + dx + (6 if k % 2 else -6), gy - 10 - k * 5, stroke='#4a7d3a', w=1.6))
    for dx in (-22, 4, 22):
        b.append(L(xs[0] + dx, gy, xs[0] + dx - 2, gy + 14, stroke='#a89070', w=1.4))
    # dương xỉ
    x = xs[1]
    b.append(PATH('M%d,%d Q%d,%d %d,%d' % (x, gy, x - 6, gy - 60, x + 16, gy - 108), stroke='#4a7d3a', w=3))
    for k in range(8):
        t = k / 8
        px = x + (-6 * 2 * t * (1 - t) * 1 + 16 * t * t) * 1.0
        yy = gy - 108 * t
        ln = 30 * (1 - 0.7 * t)
        b.append(PL([(px, yy - 8), (px - ln, yy - 2)], stroke='#4a7d3a', w=3)) if False else None
        b.append(PL([(x + 6 * math.sin(t * 2) * 0 + 16 * t * t - 6 * 2 * t * (1 - t), yy), (x + 16 * t * t - 12 * t * (1 - t) - ln, yy - 10)], stroke='#59a14f', w=3.5))
        b.append(PL([(x + 16 * t * t - 12 * t * (1 - t), yy), (x + 16 * t * t - 12 * t * (1 - t) + ln, yy - 10)], stroke='#59a14f', w=3.5))
    for dx in (-24, 0, 24):
        b.append(PL([(x, gy), (x + dx * .6, gy + 14), (x + dx, gy + 22)], stroke='#8a5a2b', w=2))
    # hạt trần: thông + nón
    x = xs[2]
    b.append(R(x - 5, gy - 28, 10, 28, fill='#8a5a2b', stroke=INK, sw=1.6))
    for k, (w_, y_) in enumerate(((52, 54), (42, 90), (32, 124))):
        b.append(POLY([(x - w_, gy - 26 - k * 0 - (-0) - y_ + 54 + 0 - 54 + 54 if False else gy - 20 - (y_ - 54) * 1.0 - 0), (x + w_, gy - 20 - (y_ - 54) * 1.0), (x, gy - 62 - (y_ - 54) * 1.0)], fill='#3d7a4a', stroke=INK, sw=1.8)) if False else None
    for k in range(3):
        w_ = 52 - k * 12
        yb = gy - 26 - k * 32
        b.append(POLY([(x - w_, yb), (x + w_, yb), (x, yb - 50)], fill='#3d7a4a', stroke=INK, sw=1.8))
    b.append(ELL(x + 30, gy - 18, 6, 10, fill='#a8763c', stroke=INK, w=1.4))
    # hạt kín: cây có hoa, quả
    x = xs[3]
    b.append(R(x - 6, gy - 54, 12, 54, fill='#8a5a2b', stroke=INK, sw=1.6))
    b.append(C(x, gy - 82, 40, fill='#7fbf6a', stroke=INK, w=2.2))
    for (dx, dy) in ((-18, -92), (14, -100), (-6, -70)):
        b.append(C(x + dx, gy + dy, 6, fill='#f4a6bd', stroke=INK, w=1.2)); b.append(C(x + dx, gy + dy, 2, fill='#f3c744', stroke='none', w=0))
    for (dx, dy) in ((22, -72), (-26, -66)):
        b.append(C(x + dx, gy + dy, 6, fill='#e8863a', stroke=INK, w=1.4))
    names = ['Rêu', 'Dương xỉ', 'Hạt trần', 'Hạt kín']
    ex = ['(rêu tản, rêu tường)', '', '(thông, vạn tuế)', '(lúa, xoài, cam)']
    ex[1] = '(dương xỉ, rau bợ)'
    traits = [['chưa có mạch dẫn', 'chưa có rễ thật', 'sinh sản bằng bào tử'], ['có mạch dẫn, rễ thật', 'không có hoa, quả, hạt', 'bào tử ở mặt dưới lá'],
              ['có mạch dẫn', 'có hạt, không có quả', 'hạt không được bao bọc'], ['có mạch dẫn', 'có hoa, quả, hạt', 'hạt nằm trong quả']]
    for x, n, e, tr in zip(xs, names, ex, traits):
        b.append(T(x, 238, n, size=16, weight='bold')); b.append(T(x, 256, e, size=12, fill=GREY))
        b.append(TL(x, 278, tr, size=12.5, lh=17))
    return svg(720, 340, ''.join(b))


# ---------- Bài 36: động vật ----------
def fig_dong_vat():
    b = [title(720, 'Phân chia các nhóm động vật')]
    b.append(R(285, 44, 150, 36, fill='#cfe0f0', stroke=INK, sw=2.2, rx=8)); b.append(T(360, 67, 'Động vật', size=16, weight='bold'))
    b.append(R(10, 120, 320, 34, fill='#f6d9c2', stroke=INK, sw=2.2, rx=8)); b.append(T(170, 142, 'Không xương sống', size=15, weight='bold'))
    b.append(R(350, 120, 360, 34, fill='#d6e8cb', stroke=INK, sw=2.2, rx=8)); b.append(T(530, 142, 'Có xương sống', size=15, weight='bold'))
    b.append(PL([(360, 80), (360, 100), (170, 100), (170, 120)], stroke=INK, w=2)); b.append(PL([(360, 100), (530, 100), (530, 120)], stroke=INK, w=2))
    left = [('Ruột khoang', ['sứa,', 'san hô']), ('Giun', ['giun đất,', 'sán']), ('Thân mềm', ['ốc, trai,', 'mực']), ('Chân khớp', ['tôm, cua,', 'côn trùng'])]
    right = [('Cá', ['cá chép']), ('Lưỡng cư', ['ếch, cóc']), ('Bò sát', ['rắn,', 'thằn lằn']), ('Chim', ['bồ câu']), ('Thú', ['thỏ, hổ'])]
    def leafs(items, x0, x1, fill, parent_x):
        n = len(items)
        w = (x1 - x0) / n - 6
        b.append(PL([(parent_x, 154), (parent_x, 172)], stroke=INK, w=2))
        b.append(L(x0 + w / 2, 172, x1 - w / 2 - 6, 172, stroke=INK, w=2))
        for i, (nm, ex) in enumerate(items):
            x = x0 + i * (x1 - x0) / n
            b.append(L(x + w / 2, 172, x + w / 2, 186, stroke=INK, w=2))
            b.append(R(x, 186, w, 84, fill=fill, stroke=INK, sw=1.8, rx=6))
            b.append(T(x + w / 2, 208, nm, size=11, weight='bold'))
            b.append(TL(x + w / 2, 232, ex, size=12, lh=15, fill=GREY))
    leafs(left, 10, 330, '#fbeadc', 170)
    leafs(right, 350, 710, '#e7f1df', 530)
    return svg(720, 292, ''.join(b))


# ---------- Bài 38: đa dạng sinh học ----------
def fig_da_dang_sinh_hoc():
    b = [title(720, 'Đa dạng sinh học: nguyên nhân suy giảm và biện pháp bảo vệ')]
    causes = [['Phá rừng'], ['Săn bắt, buôn bán', 'động vật hoang dã'], ['Ô nhiễm môi trường'], ['Biến đổi khí hậu'], ['Du nhập loài ngoại lai']]
    fixes = [['Vườn quốc gia,', 'khu bảo tồn'], ['Cấm săn bắt,', 'buôn bán'], ['Trồng rừng'], ['Tuyên truyền, nâng', 'cao ý thức'], ['Xây dựng Sách Đỏ']]
    for i, c in enumerate(causes):
        y = 48 + i * 52
        b.append(R(15, y, 200, 42, fill='#f9d9d6', stroke=INK, sw=1.8, rx=8))
        b.append(TL(115, y + (26 if len(c) == 1 else 18), c, size=13, lh=15))
        b.append(L(215, y + 21, 258, 150, stroke=RED, w=1.6))
    for i, c in enumerate(fixes):
        y = 48 + i * 52
        b.append(R(505, y, 200, 42, fill='#d6e8cb', stroke=INK, sw=1.8, rx=8))
        b.append(TL(605, y + (26 if len(c) == 1 else 18), c, size=13, lh=15))
        b.append(L(505, y + 21, 462, 150, stroke=GREEN, w=1.6))
    b.append(R(250, 100, 210, 100, fill=LYELLOW, stroke=INK, sw=2.6, rx=12))
    b.append(TL(355, 138, ['Đa dạng', 'sinh học'], size=17, lh=22, weight='bold'))
    b.append(T(355, 188, '(số loài, số cá thể, môi trường sống)', size=10.5, fill=GREY)) if False else None
    b.append(T(115, 322, 'Nguyên nhân làm suy giảm', size=13, weight='bold', fill=RED))
    b.append(T(605, 322, 'Biện pháp bảo vệ', size=13, weight='bold', fill=GREEN))
    b.append(T(355, 232, 'Đa dạng sinh học: sự phong phú về số loài,', size=12.5, fill=GREY))
    b.append(T(355, 250, 'số cá thể trong loài và môi trường sống', size=12.5, fill=GREY))
    return svg(720, 340, ''.join(b))


# ---------- Bài 39: các bước tìm hiểu sinh vật ngoài thiên nhiên ----------
def fig_tim_hieu_sinh_vat():
    b = [title(720, 'Các bước tìm hiểu sinh vật ngoài thiên nhiên')]
    steps = [('1', ['Quan sát sinh vật', 'ở môi trường sống']), ('2', ['Chụp ảnh, ghi chép', 'đặc điểm']), ('3', ['Nhận biết, phân loại', '(khoá lưỡng phân)']), ('4', ['Làm báo cáo'])]
    xs = [20, 190, 360, 530]
    for i, (n, ls) in enumerate(steps):
        x = xs[i]
        b.append(R(x, 56, 160, 90, fill='#e7f1df', stroke=INK, sw=2.2, rx=10))
        b.append(C(x + 22, 78, 13, fill=BLUE, stroke=INK, w=1.6)); b.append(T(x + 22, 83, n, size=15, weight='bold', fill='white'))
        b.append(TL(x + 80, 110 + (6 if len(ls) == 1 else 0), ls, size=13.5, lh=18, weight='bold')) if False else b.append(TL(x + 82, 104 + (8 if len(ls) == 1 else 0), ls, size=13.5, lh=18, weight='bold'))
        if i < 3:
            b.append(L(x + 162, 101, xs[i + 1] - 4, 101, stroke=BLUE, w=2.6, arrow=True))
    b.append(R(20, 170, 330, 96, fill=LGREY, stroke=GREY, sw=1.4, rx=10))
    b.append(T(185, 192, 'Dụng cụ', size=14, weight='bold'))
    b.append(TL(185, 214, ['kính lúp, ống nhòm, máy ảnh, vợt bắt côn trùng,', 'kẹp, lọ đựng mẫu, sổ ghi chép'], size=12.5, lh=17))
    b.append(R(370, 170, 330, 96, fill='#fdecea', stroke=RED, sw=1.6, rx=10))
    b.append(T(535, 192, 'An toàn và bảo vệ môi trường', size=14, weight='bold', fill=RED))
    b.append(TL(535, 214, ['không tự ý tách đoàn; không bắt, chạm sinh vật lạ,', 'độc; không phá cây, bắt động vật bừa bãi'], size=12.5, lh=17))
    return svg(720, 284, ''.join(b))

FIGS.update({
    'c-s6-b32-nam.svg': fig_nam,
    'c-s6-b34-nhom-thuc-vat.svg': fig_nhom_thuc_vat,
    'c-s6-b36-dong-vat.svg': fig_dong_vat,
    'c-s6-b38-da-dang-sinh-hoc.svg': fig_da_dang_sinh_hoc,
    'c-s6-b39-cac-buoc.svg': fig_tim_hieu_sinh_vat,
})
ATTACH += [
    ('sinh6/bai-32/nam.json', 1, 'c-s6-b32-nam.svg', 'Một số dạng nấm'),
    ('sinh6/bai-34/thuc-vat.json', 2, 'c-s6-b34-nhom-thuc-vat.svg', 'Các nhóm thực vật chính'),
    ('sinh6/bai-36/dong-vat.json', 2, 'c-s6-b36-dong-vat.svg', 'Phân chia các nhóm động vật'),
    ('sinh6/bai-38/da-dang-sinh-hoc.json', 3, 'c-s6-b38-da-dang-sinh-hoc.svg', 'Nguyên nhân suy giảm và biện pháp bảo vệ đa dạng sinh học'),
    ('sinh6/bai-39/tim-hieu-sinh-vat.json', 1, 'c-s6-b39-cac-buoc.svg', 'Các bước tìm hiểu sinh vật ngoài thiên nhiên'),
]
if __name__ == '__main__':
    write_figs('sinh6', FIGS)
    for rel, after, name, cap in ATTACH:
        subj, path = rel.split('/', 1)
        # tìm file thật (có thư mục tập/chương)
        import glob
        hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', path)) + glob.glob(os.path.join(ROOT, 'content', subj, '*', path))
        assert hits, rel
        attach(subj, os.path.relpath(hits[0], os.path.join(ROOT, 'content', subj)), after, name, cap)
    print('sinh6: %d hình' % len(FIGS))
