#!/usr/bin/env python3
# Hình minh họa lý thuyết Hoá học 8 (sơ đồ mô phỏng). Chạy: python3 tools/build-hoa8-figures.py
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

S = 'hoa8'
HC = '#cfd8e3'   # hydrogen
OC = '#e15759'   # oxygen


def atom_h(x, y):
    return C(x, y, 8, fill=HC, stroke=INK, w=1.5)


def atom_o(x, y):
    return C(x, y, 13, fill=OC, stroke=INK, w=1.5)


def mol_h2(x, y):
    return atom_h(x - 8, y) + atom_h(x + 8, y)


def mol_o2(x, y):
    return atom_o(x - 13, y) + atom_o(x + 13, y)


def mol_h2o(x, y):
    return (L(x, y, x - 14, y + 17, w=1.5, stroke=GREY) + L(x, y, x + 14, y + 17, w=1.5, stroke=GREY)
            + atom_o(x, y) + atom_h(x - 14, y + 17) + atom_h(x + 14, y + 17))


# ---------------------------------------------------------------- bài 1
def fig_dung_cu():
    b = [title(720, 'Một số dụng cụ lấy và đun hoá chất')]
    # ống nghiệm
    b.append(tube(60, 60, 26, 110, '#bcd7ee', 0.5))
    b.append(T(60, 195, 'Ống nghiệm', size=13))
    # ống hút nhỏ giọt: bầu cao su + ống thuỷ tinh
    b.append(PATH('M170,56 Q170,44 180,44 Q190,44 190,56 L190,84 L170,84 Z', fill='#c9701a', stroke=INK, w=2))
    b.append(R(172, 84, 16, 14, fill=LGREY))
    b.append(PATH('M174,98 L186,98 L182,166 L178,166 Z', fill='#ffffff', stroke=INK, w=2))
    b.append(C(180, 172, 2.5, fill='#7aa7d1', stroke='#7aa7d1'))
    b.append(TL(180, 195, ['Ống hút', 'nhỏ giọt'], size=13, lh=16))
    # thìa
    b.append(L(290, 60, 290, 150, w=3))
    b.append(PATH('M290,150 q-18,6 -18,22 q18,10 36,0 q0,-16 -18,-22 Z', fill='#e0e6ec', stroke=INK, w=2))
    b.append(TL(290, 195, ['Thìa lấy', 'chất rắn'], size=13, lh=16))
    # panh (kẹp gắp)
    b.append(PL([(410, 60), (430, 120), (420, 168)], w=3))
    b.append(PL([(450, 60), (430, 120), (440, 168)], w=3))
    b.append(L(412, 60, 448, 60, w=3))
    b.append(T(430, 195, 'Panh gắp', size=13))
    # kẹp gỗ
    b.append(R(540, 62, 14, 100, fill='#d9b382', rx=3, sw=1.5))
    b.append(R(560, 62, 14, 100, fill='#d9b382', rx=3, sw=1.5))
    b.append(L(554, 70, 560, 70, w=2))
    b.append(T(557, 195, 'Kẹp gỗ', size=13))
    # đèn cồn
    b.append(lamp(660, 160))
    b.append(T(660, 195, 'Đèn cồn', size=13))
    b.append(T(360, 250, 'Lấy chất rắn dạng bột, hạt nhỏ: thìa. Hạt to, dây, thanh: panh. Lấy lượng nhỏ chất lỏng: ống hút nhỏ giọt.',
               size=12, fill='#555'))
    return svg(720, 262, ''.join(b))


def fig_dun_ong_nghiem():
    b = [title(720, 'Đun hoá chất trong ống nghiệm')]
    mx, my = 400, 70          # tâm miệng ống
    H = 170                   # chiều dài ống
    b.append('<g transform="translate(%d,%d) rotate(45)">' % (mx, my))
    b.append(tube(0, 0, 30, H, '#bcd7ee', 0.28))
    # kẹp gỗ ở khoảng 1/3 ống tính từ miệng
    ky = H / 3
    b.append(R(-19, ky - 7, 38, 14, fill='#d9b382', stroke=INK, sw=1.5, rx=2))
    b.append(R(-80, ky - 5, 62, 10, fill='#d9b382', stroke=INK, sw=1.5, rx=2))
    b.append('</g>')
    ux, uy = -math.sin(math.radians(45)), math.cos(math.radians(45))   # hướng từ miệng đến đáy
    bx, by = mx + ux * H, my + uy * H
    b.append(lamp(bx + 14, 292))
    b.append(T(540, 78, 'Miệng ống nghiêng về phía', size=13, anchor='start'))
    b.append(T(540, 96, 'không có người', size=13, anchor='start'))
    b.append(L(536, 88, mx + 24, my - 8, stroke=GREY, w=1, arrow=True))
    b.append(T(540, 168, 'Kẹp gỗ kẹp ở khoảng 1/3', size=13, anchor='start'))
    b.append(T(540, 186, 'ống tính từ miệng', size=13, anchor='start'))
    kx, ky2 = mx + ux * H / 3, my + uy * H / 3
    b.append(L(536, 178, kx + 22, ky2, stroke=GREY, w=1, arrow=True))
    b.append(T(540, 262, 'Hơ nóng đều cả ống, rồi đun', size=13, anchor='start'))
    b.append(T(540, 280, 'tại chỗ có hoá chất', size=13, anchor='start'))
    b.append(L(536, 272, bx + 24, by + 6, stroke=GREY, w=1, arrow=True))
    return svg(720, 320, ''.join(b))


# ---------------------------------------------------------------- bài 2
def fig_phan_ung_h2o():
    b = [title(720, 'Phản ứng hoá học: các nguyên tử sắp xếp lại (2H₂ + O₂ → 2H₂O)')]
    b.append(R(20, 50, 300, 140, fill=LGREY, rx=8))
    b.append(R(400, 50, 300, 140, fill=LGREY, rx=8))
    b.append(T(170, 72, 'Chất phản ứng', size=14, weight='bold'))
    b.append(T(550, 72, 'Sản phẩm', size=14, weight='bold'))
    b.append(mol_h2(70, 120) + mol_h2(70, 160) + mol_o2(220, 140))
    b.append(T(70, 182, '2H₂', size=13) + T(220, 182, 'O₂', size=13))
    b.append(mol_h2o(480, 105) + mol_h2o(600, 105))
    b.append(T(540, 182, '2H₂O', size=13))
    b.append(L(330, 120, 392, 120, arrow=True))
    b.append(T(361, 108, 'Phản ứng', size=12))
    b.append(TL(360, 220, ['Liên kết trong phân tử chất đầu bị phá vỡ, các nguyên tử sắp xếp lại tạo liên kết mới.',
                           'Trước và sau phản ứng đều có 4 nguyên tử H và 2 nguyên tử O.'], size=13, fill='#444'))
    b.append(atom_h(40, 262) + T(54, 267, ': hydrogen', size=12, anchor='start') + atom_o(160, 262) + T(178, 267, ': oxygen', size=12, anchor='start'))
    return svg(720, 285, ''.join(b))


def fig_toa_thu_nhiet():
    b = [title(720, 'Phản ứng toả nhiệt và phản ứng thu nhiệt (sơ đồ năng lượng, minh họa)')]
    for x0, name, hi, lo, lab_hi, lab_lo, arrow_dir, note in (
            (40, 'Phản ứng toả nhiệt', 70, 150, 'Chất phản ứng', 'Sản phẩm', 'down', 'Giải phóng nhiệt ra môi trường'),
            (400, 'Phản ứng thu nhiệt', 150, 70, 'Chất phản ứng', 'Sản phẩm', 'up', 'Nhận nhiệt từ môi trường')):
        b.append(T(x0 + 140, 54, name, size=15, weight='bold'))
        b.append(L(x0 + 10, 60, x0 + 10, 200, arrow=True))
        b.append(T(x0 + 10, 216, 'Năng lượng', size=12, anchor='start', fill='#555'))
        lvl_a = hi if arrow_dir == 'down' else 150
        lvl_b = lo if arrow_dir == 'down' else 70
        b.append(L(x0 + 40, lvl_a + 20, x0 + 120, lvl_a + 20, w=4, stroke=BLUE))
        b.append(L(x0 + 180, lvl_b + 20, x0 + 260, lvl_b + 20, w=4, stroke=ORANGE))
        b.append(T(x0 + 80, lvl_a + 10, 'Chất phản ứng', size=12))
        b.append(T(x0 + 220, lvl_b + 10, 'Sản phẩm', size=12))
        b.append(L(x0 + 120, lvl_a + 20, x0 + 180, lvl_b + 20, w=1.5, dash='4 3', arrow=True))
        b.append(T(x0 + 140, 242, note, size=13))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- bài 3
def fig_mol():
    b = [title(720, 'Chuyển đổi giữa khối lượng, số mol và thể tích khí')]
    for x, head, sub in ((30, 'Khối lượng m', '(gam)'), (290, 'Số mol n', '(mol)'), (550, 'Thể tích khí V', '(lít, 25 °C, 1 bar)')):
        b.append(R(x, 80, 140, 80, fill=LYELLOW, rx=10))
        b.append(T(x + 70, 114, head, size=15, weight='bold'))
        b.append(T(x + 70, 136, sub, size=12, fill='#444'))
    b.append(L(176, 100, 284, 100, arrow=True) + T(230, 92, 'n = m / M', size=14))
    b.append(L(284, 140, 176, 140, arrow=True) + T(230, 160, 'm = n · M', size=14))
    b.append(L(436, 100, 544, 100, arrow=True) + T(490, 92, 'V = 24,79 · n', size=14))
    b.append(L(544, 140, 436, 140, arrow=True) + T(490, 160, 'n = V / 24,79', size=14))
    b.append(TL(360, 205, ['M: khối lượng mol (g/mol).  1 mol chứa 6,022·10²³ hạt (số Avogadro).',
                           'Ở 25 °C và 1 bar, 1 mol khí bất kì chiếm 24,79 lít.'], size=13, fill='#444'))
    return svg(720, 250, ''.join(b))


# ---------------------------------------------------------------- bài 4
def fig_dung_dich():
    b = [title(720, 'Dung dịch chưa bão hoà và dung dịch bão hoà (mô hình các hạt)')]
    # chưa bão hoà
    b.append(beaker(70, 60, 170, 120, '#e3eff9', 0.7))
    for (px, py) in [(100, 120), (140, 105), (190, 135), (210, 112), (120, 150)]:
        b.append(C(px, py, 5, fill=ORANGE, stroke=ORANGE))
    b.append(T(155, 205, 'Dung dịch chưa bão hoà', size=14, weight='bold'))
    b.append(T(155, 223, 'còn hoà tan thêm được chất tan', size=12))
    # bão hoà
    b.append(beaker(430, 60, 170, 120, '#e3eff9', 0.7))
    for (px, py) in [(460, 110), (500, 100), (550, 118), (575, 105), (480, 135), (535, 140), (515, 122)]:
        b.append(C(px, py, 5, fill=ORANGE, stroke=ORANGE))
    for k in range(7):
        b.append(R(448 + k * 18, 166, 14, 12, fill='#e8a95f', stroke='#b97a2a', sw=1))
    b.append(T(515, 205, 'Dung dịch bão hoà', size=14, weight='bold'))
    b.append(T(515, 223, 'không hoà tan thêm được chất tan', size=12))
    b.append(T(360, 250, 'Chấm cam: chất tan đã hoà tan. Khối vuông ở đáy: chất tan dư không tan thêm.', size=12, fill='#444'))
    return svg(720, 268, ''.join(b))


def fig_do_tan():
    b = [title(720, 'Ảnh hưởng của nhiệt độ đến độ tan (xu hướng chung, minh họa)')]
    for x0, name, pts, note in (
            (30, 'Chất rắn', [(50, 160), (110, 130), (170, 95), (230, 55)], 'Đa số tăng khi nhiệt độ tăng'),
            (390, 'Chất khí', [(50, 85), (110, 110), (170, 135), (230, 160)], 'Thường giảm khi nhiệt độ tăng')):
        b.append(T(x0 + 150, 52, name, size=15, weight='bold'))
        b.append(L(x0 + 30, 190, x0 + 30, 66, arrow=True))
        b.append(L(x0 + 30, 190, x0 + 290, 190, arrow=True))
        b.append(T(x0 + 38, 78, 'Độ tan', size=12, anchor='start'))
        b.append(T(x0 + 290, 208, 'Nhiệt độ', size=12, anchor='end'))
        b.append(PL([(x0 + px, py + 10) for px, py in pts], stroke=BLUE, w=3))
        b.append(T(x0 + 150, 232, note, size=13))
    return svg(720, 250, ''.join(b))


# ---------------------------------------------------------------- bài 5
def fig_bao_toan():
    b = [title(720, 'Định luật bảo toàn khối lượng: 4Al + 3O₂ → 2Al₂O₃')]
    heads = [(40, 'Al', 108, '4 · 27'), (220, 'O₂', 96, '3 · 32'), (500, 'Al₂O₃', 204, '2 · 102')]
    for x, f, m, calc in heads:
        b.append(R(x, 70, 130, 70, fill=LYELLOW if f != 'Al₂O₃' else LGREEN, rx=10))
        b.append(T(x + 65, 96, f, size=17, weight='bold'))
        b.append(T(x + 65, 116, '%s = %d g' % (calc, m), size=13))
        b.append(T(x + 65, 132, '(tính theo gam)', size=11, fill='#555'))
    b.append(T(190, 112, '+', size=24, weight='bold'))
    b.append(L(360, 105, 490, 105, arrow=True))
    b.append(T(425, 96, 'phản ứng', size=12))
    b.append(TL(360, 180, ['Tổng khối lượng chất tham gia: 108 + 96 = 204 g', 'Khối lượng sản phẩm: 204 g'], size=14))
    b.append(TL(360, 232, ['Tỉ lệ khối lượng Al : O₂ : Al₂O₃ = 108 : 96 : 204 = 9 : 8 : 17',
                           'Tỉ lệ số mol (cũng là tỉ lệ hệ số): 4 : 3 : 2'], size=13, fill='#444'))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- bài 6
def fig_tinh_theo_pt():
    b = [title(720, 'Các bước tính theo phương trình hoá học (ví dụ Zn + 2HCl → ZnCl₂ + H₂)')]
    steps = [('1. Viết và cân bằng', 'phương trình', 'Zn + 2HCl → ZnCl₂ + H₂'),
             ('2. Đổi ra số mol', 'n = m / M', 'n(Zn) = 0,65 / 65 = 0,01 mol'),
             ('3. Tỉ lệ hệ số', 'số mol chất cần tính', 'n(ZnCl₂) = n(Zn) = 0,01 mol'),
             ('4. Đổi ra khối lượng', 'm = n · M', 'm(ZnCl₂) = 0,01 · 136 = 1,36 g')]
    w = 164
    for i, (h1, h2, ex) in enumerate(steps):
        x = 14 + i * (w + 14)
        b.append(R(x, 50, w, 100, fill=LYELLOW, rx=10))
        b.append(T(x + w / 2, 80, h1, size=14, weight='bold'))
        b.append(T(x + w / 2, 102, h2, size=13))
        b.append(R(x, 160, w, 56, fill='#ffffff', rx=8, sw=1.5))
        b.append(TL(x + w / 2, 183, [ex.split(' = ')[0] + ' =', ' = '.join(ex.split(' = ')[1:])] if ' = ' in ex else [ex], size=12, lh=17))
        if i < 3:
            b.append(L(x + w + 1, 100, x + w + 13, 100, arrow=True))
    b.append(T(360, 244, 'Nếu hiệu suất H < 100%, lượng sản phẩm thực tế nhỏ hơn lượng tính theo phương trình.', size=12, fill='#444'))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- bài 7
def fig_toc_do():
    b = [title(720, 'Các yếu tố ảnh hưởng đến tốc độ phản ứng')]
    import random
    rnd = random.Random(2)
    cw = 164
    xs = [14 + i * (cw + 14) for i in range(4)]
    heads = ['Nồng độ', 'Nhiệt độ', 'Diện tích tiếp xúc', 'Chất xúc tác']
    for x, h in zip(xs, heads):
        b.append(R(x, 44, cw, 230, fill=LGREY, rx=8))
        b.append(T(x + cw / 2, 68, h, size=15, weight='bold'))
    # nồng độ: ít hạt / nhiều hạt
    x = xs[0]
    for (bx, n, lab) in ((x + 12, 4, 'Thấp'), (x + 90, 12, 'Cao')):
        b.append(R(bx, 82, 62, 78, fill='#fff', sw=1.5))
        for k in range(n):
            b.append(C(bx + 10 + (k % 4) * 14 + rnd.uniform(-2, 2), 94 + (k // 4) * 22 + rnd.uniform(-3, 3), 4.5, fill=ORANGE, stroke=ORANGE))
        b.append(T(bx + 31, 178, lab, size=12))
    b.append(TL(x + cw / 2, 206, ['Nồng độ càng lớn,', 'phản ứng càng nhanh'], size=12, lh=17))
    # nhiệt độ: mũi tên ngắn/dài
    x = xs[1]
    for (bx, ln, lab) in ((x + 12, 10, 'Thấp'), (x + 90, 24, 'Cao')):
        b.append(R(bx, 82, 62, 78, fill='#fff', sw=1.5))
        for (px, py) in ((bx + 14, 108), (bx + 34, 130), (bx + 18, 140)):
            b.append(C(px, py, 4.5, fill=ORANGE, stroke=ORANGE))
            b.append(L(px, py, px + ln, py - ln * 0.4, w=1.5, arrow=True))
        b.append(T(bx + 31, 178, lab, size=12))
    b.append(TL(x + cw / 2, 206, ['Nhiệt độ càng cao,', 'phản ứng càng nhanh'], size=12, lh=17))
    # diện tích: một khối / nhiều khối nhỏ
    x = xs[2]
    b.append(R(x + 20, 104, 48, 48, fill='#d6bd95', stroke='#8c6d46', sw=1.5))
    b.append(T(x + 44, 178, 'Khối lớn', size=12))
    for i in range(3):
        for j in range(3):
            b.append(R(x + 98 + i * 17, 104 + j * 17, 14, 14, fill='#d6bd95', stroke='#8c6d46', sw=1))
    b.append(T(x + 122, 178, 'Nghiền nhỏ', size=12))
    b.append(TL(x + cw / 2, 206, ['Chất rắn nghiền nhỏ', 'phản ứng nhanh hơn'], size=12, lh=17))
    # xúc tác
    x = xs[3]
    b.append(TL(x + cw / 2, 108, ['H₂O₂ phân huỷ', 'nhanh hơn khi có MnO₂'], size=12, lh=17))
    b.append(TL(x + cw / 2, 158, ['Sau phản ứng, MnO₂ vẫn', 'giữ nguyên khối lượng', 'và tính chất hoá học'], size=12, lh=17))
    b.append(TL(x + cw / 2, 220, ['Chất xúc tác làm tăng', 'tốc độ phản ứng'], size=12, lh=17))
    return svg(720, 292, ''.join(b))


# ---------------------------------------------------------------- bài 8
def fig_acid():
    b = [title(720, 'Tính chất của dung dịch acid')]
    # quỳ tím + acid -> đỏ
    b.append(T(180, 56, 'Tác dụng với quỳ tím', size=14, weight='bold'))
    b.append(beaker(120, 80, 120, 100, '#f6d1d1', 0.6))
    b.append(R(168, 60, 24, 100, fill='#f0b3b3', stroke=INK, sw=1.5))
    b.append(T(180, 205, 'Dung dịch acid', size=13))
    b.append(T(180, 223, 'làm quỳ tím chuyển sang màu đỏ', size=12))
    # kim loại + acid -> khí H2
    b.append(T(530, 56, 'Tác dụng với kim loại (Mg, Zn, Fe,...)', size=14, weight='bold'))
    b.append(tube(530, 80, 40, 120, '#e3eff9', 0.62))
    b.append(R(517, 160, 26, 14, fill='#b9c4d0', stroke=INK, sw=1.5))
    for (px, py, r) in ((522, 150, 3), (538, 136, 4), (528, 120, 3.5), (540, 108, 4), (530, 94, 3)):
        b.append(C(px, py, r, fill='none', stroke=GREY, w=1.5))
    b.append(T(530, 224, 'Mg + 2HCl → MgCl₂ + H₂↑', size=13))
    b.append(T(530, 242, 'Có bọt khí hydrogen thoát ra', size=12))
    return svg(720, 258, ''.join(b))


# ---------------------------------------------------------------- bài 9
PH_COL = ['#d7263d', '#e5483a', '#ef6f2a', '#f59e24', '#f4c430', '#c8d63a', '#7fc241',
          '#3fae5a', '#1f9d8a', '#2380b0', '#2c5fb0', '#3a46a8', '#4b3a9c', '#5a2f8c']


def fig_thang_ph():
    b = [title(720, 'Thang pH')]
    x0, w, y0 = 30, 48, 50
    for i in range(14):
        b.append(R(x0 + i * w, y0, w, 40, fill=PH_COL[i], stroke='#ffffff', sw=1))
        b.append(T(x0 + i * w + w / 2, y0 + 26, str(i + 1), size=15, weight='bold', fill='#ffffff'))
    # vùng acid / trung tính / base
    b.append(PL([(x0 + 2, y0 + 50), (x0 + 2, y0 + 56), (x0 + 6 * w - 2, y0 + 56), (x0 + 6 * w - 2, y0 + 50)], w=1.5))
    b.append(T(x0 + 3 * w, y0 + 76, 'Môi trường acid (pH < 7)', size=14, weight='bold'))
    b.append(PL([(x0 + 6 * w + 2, y0 + 50), (x0 + 6 * w + 2, y0 + 56), (x0 + 7 * w - 2, y0 + 56), (x0 + 7 * w - 2, y0 + 50)], w=1.5))
    b.append(T(x0 + 6.5 * w, y0 + 76, 'Trung tính', size=13, weight='bold'))
    b.append(T(x0 + 6.5 * w, y0 + 93, '(pH = 7)', size=13))
    b.append(PL([(x0 + 7 * w + 2, y0 + 50), (x0 + 7 * w + 2, y0 + 56), (x0 + 14 * w - 2, y0 + 56), (x0 + 14 * w - 2, y0 + 50)], w=1.5))
    b.append(T(x0 + 10.5 * w, y0 + 76, 'Môi trường base (pH > 7)', size=14, weight='bold'))
    # ví dụ đánh số trên thang
    ex = [(1.0, '1', 'HCl 0,1 M: pH = 1'), (2.5, '2', 'Dịch vị dạ dày: pH khoảng 1,5 – 3,5 (đánh dấu ở giữa khoảng)'),
          (3.0, '3', 'CH₃COOH 0,1 M: pH ≈ 3'), (7.4, '4', 'Máu người: pH khoảng 7,35 – 7,45')]
    for val, num, lab in ex:
        x = x0 + (val - 1) * w + w / 2
        b.append(L(x, y0, x, y0 - 6, stroke=INK, w=1.5))
        b.append(C(x, y0 - 14, 9, fill='#ffffff', stroke=INK, w=1.5))
        b.append(T(x, y0 - 9, num, size=12, weight='bold'))
    yy = y0 + 124
    for val, num, lab in ex:
        b.append(C(60, yy - 5, 9, fill='#ffffff', stroke=INK, w=1.5))
        b.append(T(60, yy - 1, num, size=12, weight='bold'))
        b.append(T(80, yy, lab, size=14, anchor='start'))
        yy += 26
    b.append(T(360, yy + 14, 'pH càng nhỏ, acid càng mạnh; pH càng lớn, base càng mạnh.', size=13, fill='#444'))
    return svg(720, yy + 30, ''.join(b))


def fig_chi_thi():
    b = [title(720, 'Chất chỉ thị trong dung dịch acid và dung dịch kiềm')]
    tubes = [(130, '#e8e8e8', 'Quỳ tím trong dung dịch acid', 'chuyển đỏ', '#e5483a'),
             (360, '#e8e8e8', 'Quỳ tím trong dung dịch kiềm', 'chuyển xanh', '#3a6fb0'),
             (590, '#e8e8e8', 'Phenolphthalein trong dung dịch kiềm', 'chuyển hồng', '#e86aa6')]
    for x, _, h, res, col in tubes:
        b.append(tube(x, 70, 40, 130, col, 0.65))
        b.append(T(x, 232, h.split(' trong ')[0] + ' trong', size=12))
        b.append(T(x, 248, h.split(' trong ')[1], size=12))
        b.append(T(x, 268, res, size=13, weight='bold', fill=col))
    return svg(720, 284, ''.join(b))


# ---------------------------------------------------------------- bài 10
def fig_oxide():
    b = [title(720, 'Phân loại oxide theo tính chất hoá học'), R(280, 38, 160, 36, fill=LYELLOW, rx=8), T(360, 62, 'Oxide', size=17, weight='bold')]
    cols = [('Oxide base', ['CuO, CaO,', 'Fe₂O₃, Na₂O'], ['Tác dụng với dung dịch', 'acid → muối + nước'], '#d9eef0'),
            ('Oxide acid', ['CO₂, SO₂,', 'SO₃, P₂O₅'], ['Tác dụng với dung dịch', 'base → muối + nước'], '#f4d9d9'),
            ('Oxide lưỡng tính', ['Al₂O₃, ZnO'], ['Tác dụng được', 'với cả acid và base'], LGREEN),
            ('Oxide trung tính', ['CO, NO'], ['Không tác dụng', 'với acid và base'], LGREY)]
    w = 168
    for i, (n, ex, pr, col) in enumerate(cols):
        x = 10 + i * (w + 9)
        b.append(L(360, 74, x + w / 2, 100, w=1.5))
        b.append(R(x, 100, w, 170, fill=col, rx=8))
        b.append(T(x + w / 2, 126, n, size=15, weight='bold'))
        b.append(TL(x + w / 2, 156, ex, size=14))
        b.append(L(x + 14, 190, x + w - 14, 190, stroke=GREY, w=1))
        b.append(TL(x + w / 2, 214, pr, size=12, lh=18))
    return svg(720, 288, ''.join(b))


# ---------------------------------------------------------------- bài 11
def fig_tinh_tan():
    b = [title(720, 'Tính tan của một số muối trong nước')]
    rows = [('Muối nitrate (–NO₃)', 'Đều tan', LGREEN, ''),
            ('Muối chloride (–Cl)', 'Phần lớn tan', LGREEN, 'Trừ AgCl (không tan)'),
            ('Muối sulfate (=SO₄)', 'Phần lớn tan', LGREEN, 'Trừ BaSO₄ (không tan); CaSO₄ ít tan'),
            ('Muối carbonate (=CO₃)', 'Phần lớn không tan', '#f4d9d9', 'Trừ muối của Na, K, NH₄ (tan)')]
    b.append(T(130, 56, 'Loại muối', size=14, weight='bold', fill='#555'))
    b.append(T(340, 56, 'Tính tan', size=14, weight='bold', fill='#555'))
    b.append(T(570, 56, 'Ngoại lệ', size=14, weight='bold', fill='#555'))
    y = 66
    for n, t, col, ex in rows:
        b.append(R(20, y, 220, 46, fill=LGREY, rx=6))
        b.append(T(130, y + 29, n, size=14))
        b.append(R(246, y, 190, 46, fill=col, rx=6))
        b.append(T(341, y + 29, t, size=14, weight='bold'))
        b.append(R(442, y, 258, 46, fill='#ffffff', rx=6, sw=1.5))
        b.append(T(571, y + 29, ex or 'Không có', size=12))
        y += 54
    return svg(720, 292, ''.join(b))


# ---------------------------------------------------------------- bài 12
def fig_phan_bon():
    b = [title(720, 'Các loại phân bón hoá học thông dụng')]
    cards = [('Phân đạm', 'N', ['Cung cấp nitrogen', 'Thân, rễ, lá phát triển'], 'Urea, NH₄NO₃', LGREEN),
             ('Phân lân', 'P', ['Cung cấp phosphorus', 'Rễ phát triển, nở hoa, đậu quả'], 'Superphosphate', '#f4d9d9'),
             ('Phân kali', 'K', ['Cung cấp potassium', 'Hút nước, chịu lạnh, chống đổ ngã'], 'KCl, K₂SO₄', LYELLOW),
             ('Phân NPK', 'NPK', ['Chứa đồng thời', 'N, P, K'], 'Phân hỗn hợp', LBLUE)]
    w = 168
    for i, (n, sym, pr, ex, col) in enumerate(cards):
        x = 10 + i * (w + 9)
        b.append(R(x, 44, w, 210, fill=col, rx=8))
        b.append(T(x + w / 2, 70, n, size=16, weight='bold'))
        b.append(C(x + w / 2, 112, 28, fill='#ffffff', stroke=INK, w=1.5))
        b.append(T(x + w / 2, 119, sym, size=20 if len(sym) < 3 else 15, weight='bold'))
        b.append(TL(x + w / 2, 168, pr[0:1], size=12))
        b.append(TL(x + w / 2, 186, ['%s' % pr[1]] if len(pr[1]) < 24 else [pr[1][:pr[1].rfind(',') + 1], pr[1][pr[1].rfind(',') + 1:].strip()], size=12, lh=16))
        b.append(L(x + 14, 222, x + w - 14, 222, stroke=GREY, w=1))
        b.append(T(x + w / 2, 242, ex, size=12))
    b.append(T(360, 276, 'Bón phân “4 đúng”: đúng liều, đúng loại, đúng lúc, đúng nơi.', size=13, fill='#444'))
    return svg(720, 292, ''.join(b))


FIGS = {
    'c-hoa8-b1-dung-cu.svg': fig_dung_cu,
    'c-hoa8-b1-dun-ong-nghiem.svg': fig_dun_ong_nghiem,
    'c-hoa8-b2-phan-ung.svg': fig_phan_ung_h2o,
    'c-hoa8-b2-toa-thu-nhiet.svg': fig_toa_thu_nhiet,
    'c-hoa8-b3-mol.svg': fig_mol,
    'c-hoa8-b4-dung-dich.svg': fig_dung_dich,
    'c-hoa8-b4-do-tan.svg': fig_do_tan,
    'c-hoa8-b5-bao-toan.svg': fig_bao_toan,
    'c-hoa8-b6-tinh-theo-pt.svg': fig_tinh_theo_pt,
    'c-hoa8-b7-toc-do.svg': fig_toc_do,
    'c-hoa8-b8-acid.svg': fig_acid,
    'c-hoa8-b9-thang-ph.svg': fig_thang_ph,
    'c-hoa8-b9-chi-thi.svg': fig_chi_thi,
    'c-hoa8-b10-oxide.svg': fig_oxide,
    'c-hoa8-b11-tinh-tan.svg': fig_tinh_tan,
    'c-hoa8-b12-phan-bon.svg': fig_phan_bon,
}

ATTACH = [
    ('tap1/mo-dau/bai-1/su-dung-hoa-chat-thiet-bi.json', 2, 'c-hoa8-b1-dung-cu.svg', 'Một số dụng cụ lấy hoá chất và đèn cồn.'),
    ('tap1/mo-dau/bai-1/su-dung-hoa-chat-thiet-bi.json', 3, 'c-hoa8-b1-dun-ong-nghiem.svg', 'Cách đun hoá chất trong ống nghiệm.'),
    ('tap1/chuong-1/bai-2/phan-ung-hoa-hoc.json', 2, 'c-hoa8-b2-phan-ung.svg', 'Trong phản ứng hoá học, các nguyên tử sắp xếp lại.'),
    ('tap1/chuong-1/bai-2/phan-ung-hoa-hoc.json', 4, 'c-hoa8-b2-toa-thu-nhiet.svg', 'Sơ đồ năng lượng của phản ứng toả nhiệt và thu nhiệt.'),
    ('tap1/chuong-1/bai-3/mol-ti-khoi-chat-khi.json', 4, 'c-hoa8-b3-mol.svg', 'Mối liên hệ giữa khối lượng, số mol và thể tích khí.'),
    ('tap1/chuong-1/bai-4/dung-dich-nong-do.json', 0, 'c-hoa8-b4-dung-dich.svg', 'Dung dịch chưa bão hoà và dung dịch bão hoà.'),
    ('tap1/chuong-1/bai-4/dung-dich-nong-do.json', 3, 'c-hoa8-b4-do-tan.svg', 'Xu hướng thay đổi độ tan theo nhiệt độ.'),
    ('tap1/chuong-1/bai-5/bao-toan-khoi-luong-pthh.json', 4, 'c-hoa8-b5-bao-toan.svg', 'Khối lượng chất tham gia bằng khối lượng sản phẩm.'),
    ('tap1/chuong-1/bai-6/tinh-theo-pthh.json', 2, 'c-hoa8-b6-tinh-theo-pt.svg', 'Các bước tính theo phương trình hoá học.'),
    ('tap1/chuong-1/bai-7/toc-do-phan-ung-xuc-tac.json', 2, 'c-hoa8-b7-toc-do.svg', 'Các yếu tố ảnh hưởng đến tốc độ phản ứng.'),
    ('tap1/chuong-2/bai-8/acid.json', 2, 'c-hoa8-b8-acid.svg', 'Dung dịch acid đổi màu quỳ tím và phản ứng với kim loại.'),
    ('tap1/chuong-2/bai-9/base-thang-ph.json', 2, 'c-hoa8-b9-chi-thi.svg', 'Màu của quỳ tím và phenolphthalein trong dung dịch.'),
    ('tap1/chuong-2/bai-9/base-thang-ph.json', 5, 'c-hoa8-b9-thang-ph.svg', 'Thang pH và giá trị pH của một số dung dịch.'),
    ('tap1/chuong-2/bai-10/oxide.json', 3, 'c-hoa8-b10-oxide.svg', 'Bốn loại oxide theo tính chất hoá học.'),
    ('tap1/chuong-2/bai-11/muoi.json', 2, 'c-hoa8-b11-tinh-tan.svg', 'Tính tan của một số muối trong nước.'),
    ('tap1/chuong-2/bai-12/phan-bon-hoa-hoc.json', 2, 'c-hoa8-b12-phan-bon.svg', 'Phân đạm, phân lân, phân kali và phân NPK.'),
]

if __name__ == '__main__':
    write_figs(S, FIGS)
    for a in ATTACH:
        attach(S, *a)
    print('hoa8: %d hình' % len(FIGS))
