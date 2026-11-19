#!/usr/bin/env python3
# Hình minh họa lý thuyết Hoá học 9 (sơ đồ mô phỏng). Chạy: python3 tools/build-hoa9-figures.py
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

S = 'hoa9'
CU = '#b87333'


def box(x, y, w, h, lines, fill=LYELLOW, size=14, bold=False, rx=8):
    out = [R(x, y, w, h, fill=fill, rx=rx)]
    n = len(lines)
    lh = size + 4
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, s in enumerate(lines):
        out.append(T(x + w / 2, y0 + i * lh, s, size=size, weight='bold' if bold else 'normal'))
    return ''.join(out)


def center_struct(atoms, cx, cy):
    mx, my = mol_center(atoms)
    return struct(atoms, BOND_PLACEHOLDER, cx - mx, cy - my)


# ---------------------------------------------------------------- bài 18
def fig_kim_loai_vat_li():
    b = [title(720, 'Tính chất vật lí chung của kim loại')]
    tiles = [('Tính dẻo', 'Kéo thành sợi,', 'dát mỏng'), ('Dẫn điện', 'Dẫn điện tốt', 'nhất là Ag'),
             ('Dẫn nhiệt', 'Nồi, xoong', 'làm bằng kim loại'), ('Ánh kim', 'Bề mặt sáng', 'óng ánh')]
    w = 168
    for i, (h, l1, l2) in enumerate(tiles):
        x = 10 + i * (w + 9)
        b.append(box(x, 44, w, 80, [h, l1, l2], fill='#d8dee6', size=13))
    b.append(T(360, 158, 'Thứ tự dẫn điện giảm dần:', size=14, weight='bold'))
    order = ['Ag', 'Cu', 'Au', 'Al', 'Fe']
    for i, s in enumerate(order):
        x = 110 + i * 110
        b.append(C(x, 205, 26, fill=['#e6e6ea', '#e3a46b', '#f2cf5a', '#cfd5db', '#b4bcc6'][i], stroke=INK, w=1.5))
        b.append(T(x, 211, s, size=17, weight='bold'))
        if i < 4:
            b.append(T(x + 55, 211, '>', size=20, weight='bold'))
    b.append(T(360, 258, 'Hg là kim loại lỏng ở nhiệt độ thường; W nóng chảy ở 3 410 °C.', size=12, fill='#444'))
    return svg(720, 276, ''.join(b))


def fig_fe_cuso4():
    b = [title(720, 'Sắt đẩy đồng ra khỏi dung dịch muối: Fe + CuSO₄ → FeSO₄ + Cu')]
    # trước
    b.append(T(170, 54, 'Trước phản ứng', size=14, weight='bold'))
    b.append(beaker(110, 80, 120, 130, '#5aa7e0', 0.7))
    b.append(R(164, 62, 12, 120, fill='#9aa3ad', stroke=INK, sw=1.5, rx=2))
    b.append(TL(170, 234, ['Đinh sắt trong dung dịch', 'CuSO₄ (màu xanh lam)'], size=12, lh=16))
    b.append(L(270, 140, 440, 140, arrow=True))
    b.append(T(355, 130, 'Sau một thời gian', size=12))
    # sau
    b.append(T(540, 54, 'Sau phản ứng', size=14, weight='bold'))
    b.append(beaker(480, 80, 120, 130, '#cfe8cf', 0.7))
    b.append(R(534, 62, 12, 120, fill=CU, stroke=INK, sw=1.5, rx=2))
    b.append(TL(540, 234, ['Đinh sắt phủ lớp đồng đỏ;', 'dung dịch FeSO₄ nhạt màu'], size=12, lh=16))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- bài 19
def fig_day_hoat_dong():
    b = [title(720, 'Dãy hoạt động hoá học của một số kim loại')]
    syms = ['K', 'Na', 'Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Pb', 'H', 'Cu', 'Ag', 'Au']
    w = 52
    x0 = 36
    for i, s in enumerate(syms):
        x = x0 + i * (w + 2)
        col = '#f3c6c6' if i < 3 else ('#f7e3b5' if i < 8 else ('#e6e6ea' if s == 'H' else '#d9eef0'))
        if s == 'H':
            col = '#ffffff'
        b.append(R(x, 56, w, 46, fill=col, rx=6, sw=2 if s != 'H' else 2))
        b.append(T(x + w / 2, 87, s if s != 'H' else '(H)', size=19, weight='bold'))
    b.append(L(40, 124, 680, 124, arrow=True))
    b.append(T(360, 144, 'Mức độ hoạt động hoá học giảm dần', size=13))
    cx = lambda i: x0 + i * (w + 2) + w / 2
    # ba ý nghĩa
    def brace(i1, i2, y, text1, text2):
        a, bb = cx(i1) - w / 2 + 2, cx(i2) + w / 2 - 2
        return (PL([(a, y), (a, y + 8), (bb, y + 8), (bb, y)], w=1.5)
                + TL((a + bb) / 2, y + 28, [text1, text2], size=12, lh=16))
    b.append(brace(0, 2, 168, 'Phản ứng với nước ở', 'nhiệt độ thường → base + H₂'))
    b.append(brace(0, 7, 232, 'Đứng trước H: phản ứng với HCl, H₂SO₄ loãng → muối + H₂', ''))
    b.append(brace(9, 11, 168, 'Đứng sau H: không phản ứng', 'với HCl, H₂SO₄ loãng'))
    b.append(TL(360, 300, ['Kim loại đứng trước (trừ K, Na, Ca) đẩy được kim loại đứng sau', 'ra khỏi dung dịch muối.'], size=13, fill='#444'))
    return svg(720, 336, ''.join(b))


# ---------------------------------------------------------------- bài 20
def fig_tach_kim_loai():
    b = [title(720, 'Phương pháp tách kim loại theo mức độ hoạt động')]
    rows = [(['Na', 'Mg', 'Al'], 'Kim loại mạnh', 'Điện phân nóng chảy', '#f3c6c6'),
            (['Zn', 'Fe', 'Pb', 'Cu'], 'Kim loại trung bình', 'Dùng chất khử (C, CO, H₂) ở nhiệt độ cao', '#f7e3b5'),
            (['Ag', 'Au'], 'Kim loại yếu', 'Có thể tồn tại ở dạng tự do', '#d9eef0')]
    y = 50
    for syms, lab, how, col in rows:
        b.append(R(20, y, 130, 64, fill=col, rx=8))
        b.append(TL(85, y + 28, [lab], size=13, weight='bold'))
        b.append(T(85, y + 48, ' '.join(syms), size=15))
        b.append(L(156, y + 32, 200, y + 32, arrow=True))
        b.append(box(206, y, 488, 64, [how], fill='#ffffff', size=15))
        y += 78
    b.append(T(360, 300, 'Hoạt động giảm dần từ trên xuống dưới.', size=12, fill='#444'))
    return svg(720, 316, ''.join(b))


def fig_hop_kim():
    b = [title(720, 'Gang, thép và một số hợp kim thông dụng')]
    # thanh hàm lượng carbon 0 - 5 %
    x0, w = 60, 120
    b.append(T(360, 52, 'Hàm lượng carbon trong hợp kim của sắt', size=14, weight='bold'))
    b.append(R(x0, 70, 2 * w, 40, fill='#cfd8e3', sw=1.5))
    b.append(R(x0 + 2 * w, 70, 3 * w * 0.5 * 2 / 2 * 1.0, 40, fill='#8a97a6', sw=1.5)) if False else None
    b.append(R(x0 + 2 * w - 0, 70, 3 * w * 1.0, 40, fill='#8a97a6', sw=1.5))
    b.append(T(x0 + w, 96, 'Thép: dưới 2% C', size=15, weight='bold'))
    b.append(T(x0 + 3.5 * w, 96, 'Gang: 2% đến 5% C', size=15, weight='bold', fill='#ffffff'))
    for v in (0, 1, 2, 3, 4, 5):
        x = x0 + v * w * 1.0 if v <= 2 else x0 + 2 * w + (v - 2) * w
        b.append(L(x, 110, x, 118, w=1.5))
        b.append(T(x, 134, '%d%%' % v, size=12))
    cards = [('Inox', 'Thép không gỉ,', 'có Cr, Ni'), ('Duralumin', 'Al, Cu, Mn, Mg;', 'nhẹ, bền')]
    for i, (n, l1, l2) in enumerate(cards):
        b.append(box(120 + i * 250, 170, 220, 80, [n, l1, l2], fill=LYELLOW, size=14))
    b.append(T(360, 280, 'Hợp kim thường cứng hơn, bền hơn, ít bị ăn mòn hơn kim loại thành phần.', size=12, fill='#444'))
    return svg(720, 296, ''.join(b))


# ---------------------------------------------------------------- bài 21
def fig_kl_pk():
    b = [title(720, 'So sánh kim loại và phi kim')]
    rows = [('Thể', 'Thường rắn (trừ Hg)', 'Cả ba thể: rắn (C, S, P), lỏng (Br₂), khí (O₂, N₂, Cl₂)'),
            ('Ánh kim', 'Có ánh kim', 'Thường không có ánh kim'),
            ('Dẫn điện, nhiệt', 'Dẫn điện, dẫn nhiệt tốt', 'Dẫn điện, nhiệt kém (trừ than chì dẫn điện)'),
            ('Xu hướng', 'Nhường electron → ion dương', 'Nhận electron → ion âm'),
            ('Oxide', 'Thường là oxide base', 'Thường là oxide acid')]
    b.append(box(130, 44, 270, 34, ['Kim loại'], fill='#d8dee6', bold=True, size=15))
    b.append(box(406, 44, 294, 34, ['Phi kim'], fill=LGREEN, bold=True, size=15))
    y = 84
    for h, a, c in rows:
        hh = 52 if len(c) > 40 else 40
        b.append(box(10, y, 114, hh, [h], fill=LGREY, size=12, bold=True))
        b.append(box(130, y, 270, hh, [a], fill='#ffffff', size=12))
        if len(c) > 40:
            cut = c.rfind(',', 0, 44) + 1 if ',' in c[:46] else 44
            b.append(box(406, y, 294, hh, [c[:cut].strip(), c[cut:].strip()], fill='#ffffff', size=12))
        else:
            b.append(box(406, y, 294, hh, [c], fill='#ffffff', size=12))
        y += hh + 6
    return svg(720, y + 10, ''.join(b))


# ---------------------------------------------------------------- hữu cơ: cấu tạo
def S_CH4():
    return {'C': (0, 0, 'C'), 'H1': (0, -34, 'H'), 'H2': (0, 34, 'H'), 'H3': (-34, 0, 'H'), 'H4': (34, 0, 'H')}, \
        [('C', 'H1', 1), ('C', 'H2', 1), ('C', 'H3', 1), ('C', 'H4', 1)]


def S_alkane(n):
    atoms, bonds = {}, []
    step = 40
    for i in range(n):
        x = i * step
        atoms['C%d' % i] = (x, 0, 'C')
        atoms['U%d' % i] = (x, -34, 'H')
        atoms['D%d' % i] = (x, 34, 'H')
        bonds += [('C%d' % i, 'U%d' % i, 1), ('C%d' % i, 'D%d' % i, 1)]
        if i > 0:
            bonds.append(('C%d' % (i - 1), 'C%d' % i, 1))
    atoms['L'] = (-34, 0, 'H')
    atoms['R'] = ((n - 1) * step + 34, 0, 'H')
    bonds += [('C0', 'L', 1), ('C%d' % (n - 1), 'R', 1)]
    return atoms, bonds


def S_C2H4():
    atoms = {'C1': (-22, 0, 'C'), 'C2': (22, 0, 'C'), 'a': (-44, -30, 'H'), 'b': (-44, 30, 'H'),
             'c': (44, -30, 'H'), 'd': (44, 30, 'H')}
    return atoms, [('C1', 'C2', 2), ('C1', 'a', 1), ('C1', 'b', 1), ('C2', 'c', 1), ('C2', 'd', 1)]


def S_ethanol():
    atoms, bonds = S_alkane(2)
    del atoms['R']
    bonds = [bd for bd in bonds if bd[1] != 'R']
    atoms['O'] = (80, 0, 'O')
    atoms['Ho'] = (114, 0, 'H')
    bonds += [('C1', 'O', 1), ('O', 'Ho', 1)]
    return atoms, bonds


def S_acetic():
    atoms = {'C1': (0, 0, 'C'), 'C2': (40, 0, 'C'), 'a': (0, -34, 'H'), 'b': (0, 34, 'H'), 'L': (-34, 0, 'H'),
             'O1': (40, -36, 'O'), 'O2': (78, 18, 'O'), 'Ho': (112, 18, 'H')}
    bonds = [('C1', 'C2', 1), ('C1', 'a', 1), ('C1', 'b', 1), ('C1', 'L', 1), ('C2', 'O1', 2), ('C2', 'O2', 1), ('O2', 'Ho', 1)]
    return atoms, bonds


def put(fn, cx, cy, *args, **kw):
    atoms, bonds = fn(*args)
    mx, my = mol_center(atoms)
    return struct(atoms, bonds, cx - mx, cy - my, **kw)


# ---------------------------------------------------------------- bài 22
def fig_huu_co_phan_loai():
    b = [title(720, 'Phân loại hợp chất hữu cơ'), box(250, 40, 220, 38, ['Hợp chất hữu cơ'], fill=LYELLOW, bold=True, size=16)]
    cols = [(180, 'Hydrocarbon', 'Chỉ chứa C và H', 'CH₄, C₂H₄', '#d9eef0'),
            (540, 'Dẫn xuất của hydrocarbon', 'Ngoài C, H còn có O, N, Cl…', 'C₂H₅OH, CH₃COOH', LGREEN)]
    for x, h, d, ex, col in cols:
        b.append(L(360, 78, x, 110, w=1.5))
        b.append(R(x - 150, 110, 300, 110, fill=col, rx=8))
        b.append(T(x, 138, h, size=15, weight='bold'))
        b.append(T(x, 164, d, size=13))
        b.append(T(x, 196, 'Ví dụ: ' + ex, size=14))
    b.append(T(360, 250, 'Hoá trị trong hợp chất hữu cơ: C (IV), H (I), O (II).', size=13, fill='#444'))
    return svg(720, 268, ''.join(b))


def fig_huu_co_cau_tao():
    b = [title(720, 'Công thức cấu tạo: C có hoá trị IV, H hoá trị I, O hoá trị II')]
    items = [('CH₄', S_CH4, ()), ('CH₃–CH₃', S_alkane, (2,)), ('CH₂=CH₂', S_C2H4, ()), ('CH₃–CH₂–OH', S_ethanol, ())]
    xs = [95, 270, 450, 625]
    names = ['Methane', 'Ethane', 'Ethylene', 'Ethylic alcohol']
    for x, (f, fn, args), nm in zip(xs, items, names):
        b.append(put(fn, x, 120, *args))
        b.append(T(x, 205, nm, size=13, weight='bold'))
        b.append(T(x, 224, f, size=13))
    b.append(T(360, 262, 'Mỗi nét gạch là một liên kết cộng hoá trị; nét đôi là liên kết đôi.', size=12, fill='#444'))
    return svg(720, 280, ''.join(b))


# ---------------------------------------------------------------- bài 23
def fig_alkane():
    b = [title(720, 'Một số alkane (công thức chung CₙH₂ₙ₊₂)')]
    for n, nm, f, cx, cy in ((1, 'Methane', 'CH₄', 110, 100), (2, 'Ethane', 'C₂H₆', 330, 100), (3, 'Propane', 'C₃H₈', 570, 100),
                             (4, 'Butane', 'C₄H₁₀', 360, 250)):
        b.append(put(S_CH4, cx, cy) if n == 1 else put(S_alkane, cx, cy, n))
        b.append(T(cx, cy + 70, nm, size=14, weight='bold'))
        b.append(T(cx, cy + 90, f, size=13))
    b.append(T(360, 366, 'Alkane từ C₁ đến C₄ ở thể khí, không tan trong nước, nhẹ hơn nước.', size=13, fill='#444'))
    return svg(720, 382, ''.join(b))


# ---------------------------------------------------------------- bài 24
def fig_alkene():
    b = [title(720, 'Ethylene (alkene đơn giản nhất) và phản ứng đặc trưng')]
    b.append(put(S_C2H4, 90, 100))
    b.append(T(90, 160, 'Ethylene C₂H₄', size=14, weight='bold'))
    b.append(T(90, 178, 'có liên kết đôi C=C', size=12))
    # cộng brom
    b.append(T(400, 62, 'Phản ứng cộng với nước bromine (làm mất màu)', size=13, weight='bold'))
    b.append(tube(300, 80, 36, 100, '#f2a33a', 0.6))
    b.append(T(300, 206, 'Nước bromine', size=12) + T(300, 222, 'màu da cam', size=12))
    b.append(L(345, 130, 450, 130, arrow=True) + T(398, 118, '+ C₂H₄', size=13))
    b.append(tube(500, 80, 36, 100, '#f1f1f1', 0.6))
    b.append(T(500, 206, 'Dung dịch mất màu', size=12) + T(500, 222, 'C₂H₄ + Br₂ → C₂H₄Br₂', size=12))
    # trùng hợp
    b.append(T(360, 262, 'Trùng hợp: n CH₂=CH₂ → (–CH₂–CH₂–)ₙ  (polyethylene, PE)', size=13, fill='#444'))
    return svg(720, 282, ''.join(b))


# ---------------------------------------------------------------- bài 25
def fig_chung_cat():
    b = [title(720, 'Chưng cất dầu mỏ (sơ đồ tháp chưng cất)')]
    x0, x1, y0, y1 = 250, 350, 50, 320
    b.append(R(x0, y0, x1 - x0, y1 - y0, fill='#eef1f4', sw=2.5, rx=6))
    outs = [('Khí', 68), ('Xăng', 118), ('Dầu hoả', 168), ('Dầu diesel', 218), ('Dầu mazut', 268), ('Nhựa đường', 312)]
    for i, (n, y) in enumerate(outs):
        if i < len(outs) - 1:
            b.append(L(x0, y + 22, x1, y + 22, stroke=GREY, w=1.2, dash='5 3'))
        b.append(L(x1, y, 440, y, arrow=True))
        b.append(T(450, y + 5, n, size=15, anchor='start', weight='bold'))
    b.append(L(130, 270, x0, 270, arrow=True, w=2.5))
    b.append(TL(130, 300, ['Dầu mỏ đã', 'nung nóng'], size=12, lh=15))
    b.append(L(200, 300, 200, 80, arrow=True, w=1.5, stroke=GREY))
    b.append(TL(160, 130, ['Nhiệt độ', 'sôi giảm', 'dần lên', 'phía trên'], size=11, lh=14))
    b.append(T(360, 346, 'Các hydrocarbon được tách dựa vào nhiệt độ sôi khác nhau.', size=12, fill='#444'))
    return svg(720, 362, ''.join(b))


# ---------------------------------------------------------------- bài 26
def fig_ethanol():
    b = [title(720, 'Ethylic alcohol (ethanol)')]
    b.append(put(S_ethanol, 120, 100))
    b.append(T(120, 160, 'C₂H₅OH', size=15, weight='bold'))
    b.append(TL(120, 186, ['Chất lỏng không màu,', 'sôi ở 78,3 °C, tan vô hạn', 'trong nước'], size=12, lh=16))
    # độ cồn
    b.append(T(500, 58, 'Độ cồn: rượu 40°', size=14, weight='bold'))
    b.append(T(500, 86, '100 mL hỗn hợp (ethanol tan lẫn trong nước)', size=12))
    b.append(R(350, 100, 300 * 0.4, 56, fill='#f7e29b', sw=2))
    b.append(R(350 + 120, 100, 300 * 0.6, 56, fill='#cfe3f4', sw=2))
    b.append(TL(410, 124, ['40 mL', 'ethanol'], size=13, lh=16))
    b.append(TL(560, 124, ['60 mL nước'], size=13))
    b.append(T(500, 190, 'Độ cồn 40° nghĩa là cứ 100 mL hỗn hợp', size=12))
    b.append(T(500, 208, 'có 40 mL ethanol nguyên chất', size=12))
    return svg(720, 230, ''.join(b))


# ---------------------------------------------------------------- bài 27
def fig_acetic():
    b = [title(720, 'Acetic acid và phản ứng ester hoá')]
    b.append(put(S_acetic, 130, 84))
    b.append(T(130, 160, 'CH₃COOH', size=15, weight='bold'))
    b.append(TL(130, 184, ['Chất lỏng không màu, vị chua', 'Giấm ăn: dung dịch 2–5%'], size=12, lh=16))
    b.append(box(300, 54, 400, 160, [], fill=LGREY))
    b.append(T(500, 82, 'Phản ứng ester hoá', size=14, weight='bold'))
    b.append(TL(500, 118, ['CH₃COOH + C₂H₅OH', '⇌ CH₃COOC₂H₅ + H₂O'], size=15, lh=24))
    b.append(TL(500, 182, ['Xúc tác H₂SO₄ đặc, đun nóng', 'Sản phẩm: ethyl acetate'], size=12, lh=16))
    return svg(720, 236, ''.join(b))


# ---------------------------------------------------------------- bài 28
def fig_lipid():
    b = [title(720, 'Chất béo và phản ứng xà phòng hoá')]
    # cấu tạo: glycerol + 3 acid béo
    b.append(R(40, 54, 22, 120, fill=LYELLOW, stroke=INK, sw=1.5, rx=4))
    b.append('<text transform="rotate(-90 51 114)" x="51" y="119" text-anchor="middle" font-size="13" font-weight="bold" fill="%s">Glycerol</text>' % INK)
    for i in range(3):
        y = 74 + i * 40
        b.append(L(62, y, 200, y, w=3, stroke=ORANGE))
        b.append(T(210, y + 5, 'gốc acid béo', size=12, anchor='start'))
    b.append(TL(130, 200, ['Chất béo là triester của', 'glycerol với các acid béo'], size=12, lh=16))
    # xà phòng hoá
    b.append(box(350, 66, 110, 50, ['Chất béo', '+ NaOH'], fill=LYELLOW, size=13))
    b.append(L(464, 91, 520, 91, arrow=True))
    b.append(box(524, 54, 176, 38, ['Glycerol'], fill=LBLUE, size=14))
    b.append(box(524, 100, 176, 38, ['Muối của acid béo (xà phòng)'], fill=LGREEN, size=12))
    b.append(T(525, 170, '1 g chất béo cho khoảng 38 kJ', size=13, anchor='start'))
    b.append(T(525, 192, 'Hoà tan vitamin A, D, E, K', size=13, anchor='start'))
    return svg(720, 222, ''.join(b))


# ---------------------------------------------------------------- bài 29
def fig_glucose():
    b = [title(720, 'Carbohydrate: glucose và saccharose')]
    b.append(box(20, 50, 160, 46, ['Glucose', 'C₆H₁₂O₆'], fill=LYELLOW, size=14))
    b.append(box(20, 150, 160, 46, ['Saccharose', 'C₁₂H₂₂O₁₁'], fill=LYELLOW, size=14))
    b.append(L(186, 73, 262, 73, arrow=True))
    b.append(T(224, 63, 'Lên men', size=12))
    b.append(box(268, 50, 250, 46, ['2C₂H₅OH + 2CO₂'], fill=LGREEN, size=14))
    b.append(T(393, 112, '(enzyme)', size=12, fill='#555'))
    b.append(L(186, 173, 262, 173, arrow=True))
    b.append(T(224, 163, 'Thuỷ phân', size=12))
    b.append(box(268, 150, 250, 46, ['Glucose + Fructose'], fill=LGREEN, size=14))
    b.append(T(393, 212, '(xúc tác acid hoặc enzyme)', size=12, fill='#555'))
    b.append(TL(612, 90, ['Có nhiều', 'trong quả chín', '(nhất là nho)'], size=12, lh=16))
    b.append(TL(612, 168, ['Có trong mía,', 'củ cải đường,', 'thốt nốt'], size=12, lh=16))
    return svg(720, 236, ''.join(b))


# ---------------------------------------------------------------- bài 30
def fig_tinh_bot():
    b = [title(720, 'Tinh bột và cellulose')]
    # chuỗi mắt xích
    b.append(T(180, 58, 'Phân tử polymer (C₆H₁₀O₅)ₙ', size=14, weight='bold'))
    for i in range(6):
        b.append(C(40 + i * 46, 100, 16, fill=LYELLOW, stroke=INK, w=1.5))
        if i < 5:
            b.append(L(56 + i * 46, 100, 70 + i * 46, 100, w=2))
    b.append(T(180, 140, 'Nhiều mắt xích C₆H₁₀O₅ nối với nhau', size=12))
    b.append(TL(180, 190, ['Tinh bột: gạo, ngô, khoai, sắn', 'Cellulose: bông, gỗ, tre'], size=13, lh=18))
    # nhận biết bằng iodine
    b.append(T(520, 58, 'Nhận biết tinh bột bằng iodine', size=14, weight='bold'))
    b.append(tube(450, 80, 34, 100, '#f1f1f1', 0.6))
    b.append(L(492, 130, 548, 130, arrow=True) + T(520, 118, '+ iodine', size=12))
    b.append(tube(590, 80, 34, 100, '#3b3f9a', 0.6))
    b.append(T(450, 206, 'Hồ tinh bột', size=12))
    b.append(T(590, 206, 'Màu xanh tím', size=12))
    return svg(720, 232, ''.join(b))


# ---------------------------------------------------------------- bài 31
def fig_protein():
    b = [title(720, 'Protein được tạo từ nhiều amino acid')]
    cols = [LYELLOW, LGREEN, LBLUE, '#f4d9d9']
    for i in range(8):
        x = 60 + i * 52
        b.append(C(x, 100, 18, fill=cols[i % 4], stroke=INK, w=1.5))
        if i < 7:
            b.append(L(x + 18, 100, x + 34, 100, w=2))
    b.append(T(260, 142, 'Mỗi vòng tròn: một amino acid; các amino acid nối thành chuỗi dài', size=12))
    b.append(L(540, 100, 600, 100, arrow=True)) if False else None
    b.append(T(360, 190, 'Thuỷ phân (acid, base hoặc enzyme) → các amino acid', size=14))
    b.append(T(360, 226, 'Đun nóng hoặc gặp acid, base, muối kim loại nặng → protein đông tụ', size=14))
    b.append(T(360, 262, 'Khi cháy có mùi khét', size=14))
    return svg(720, 284, ''.join(b))


# ---------------------------------------------------------------- bài 32
def fig_polymer():
    b = [title(720, 'Polymer và phân loại polymer')]
    b.append(T(180, 56, 'n CH₂=CH₂  →  (–CH₂–CH₂–)ₙ', size=15, weight='bold'))
    b.append(T(180, 78, 'Ethylene (monomer) → polyethylene (PE)', size=12))
    for i in range(7):
        b.append(C(40 + i * 40, 120, 14, fill=LYELLOW, stroke=INK, w=1.5))
        if i < 6:
            b.append(L(54 + i * 40, 120, 66 + i * 40, 120, w=2))
    b.append(T(180, 158, 'Mắt xích –CH₂–CH₂– lặp lại nhiều lần', size=12))
    b.append(box(370, 50, 170, 36, ['Polymer thiên nhiên'], fill=LGREEN, size=13, bold=True))
    b.append(TL(455, 112, ['Tinh bột, cellulose,', 'protein, cao su thiên nhiên'], size=12, lh=16))
    b.append(box(552, 50, 160, 36, ['Polymer tổng hợp'], fill=LBLUE, size=13, bold=True))
    b.append(TL(632, 112, ['PE, PVC, nylon,', 'cao su buna'], size=12, lh=16))
    b.append(T(360, 222, 'Polymer thường là chất rắn, không bay hơi, không tan trong nước.', size=13, fill='#444'))
    return svg(720, 240, ''.join(b))


# ---------------------------------------------------------------- bài 33
def fig_vo_trai_dat():
    b = [title(720, 'Thành phần các nguyên tố trong vỏ Trái Đất (theo khối lượng, xấp xỉ)')]
    cx, cy, r = 190, 160, 105
    parts = [('Oxygen', 46, BLUE), ('Silicon', 28, ORANGE), ('Còn lại', 26, GREY)]
    ang = -90.0
    for name, v, col in parts:
        a2 = ang + v * 3.6
        x1, y1 = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
        b.append(PATH('M%.1f,%.1f L%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f Z' % (cx, cy, x1, y1, r, r, x2, y2), fill=col, stroke='#fff', w=2))
        ang = a2
    ly = 100
    for name, v, col in parts:
        b.append(R(380, ly - 14, 22, 22, fill=col, stroke=col))
        b.append(T(412, ly + 3, '%s: khoảng %d%%' % (name, v), size=16, anchor='start'))
        ly += 40
    b.append(TL(380, ly + 4, ['“Còn lại” gồm nhôm, sắt, calcium,', 'sodium, potassium, magnesium…'], size=13, anchor='start'))
    return svg(720, 292, ''.join(b))


# ---------------------------------------------------------------- bài 34
def fig_da_voi():
    b = [title(720, 'Từ đá vôi đến vôi sống và vôi tôi')]
    b.append(box(20, 80, 140, 50, ['Đá vôi', 'CaCO₃'], fill='#e4dccb', size=14))
    b.append(L(166, 105, 270, 105, arrow=True) + T(218, 95, 'Nung', size=12))
    b.append(box(276, 60, 150, 46, ['Vôi sống CaO'], fill=LYELLOW, size=14))
    b.append(box(276, 114, 150, 46, ['Khí CO₂'], fill=LBLUE, size=14))
    b.append(L(432, 83, 520, 83, arrow=True) + T(476, 73, '+ H₂O', size=12))
    b.append(box(526, 60, 170, 46, ['Vôi tôi Ca(OH)₂'], fill=LGREEN, size=14))
    b.append(TL(360, 200, ['CaCO₃ → CaO + CO₂', 'CaO + H₂O → Ca(OH)₂'], size=14, lh=22))
    return svg(720, 244, ''.join(b))


def fig_silicate():
    b = [title(720, 'Nguyên liệu của một số sản phẩm silicate')]
    b.append(box(20, 60, 230, 74, ['Cát (SiO₂)', 'đá vôi, soda (Na₂CO₃)'], fill='#e4dccb', size=13))
    b.append(L(256, 97, 340, 97, arrow=True) + T(298, 87, 'Nấu chảy', size=12))
    b.append(box(346, 74, 130, 46, ['Thuỷ tinh'], fill=LBLUE, size=14, bold=True))
    b.append(box(20, 170, 230, 74, ['Đá vôi, đất sét', '(nghiền với thạch cao)'], fill='#e4dccb', size=13))
    b.append(L(256, 207, 340, 207, arrow=True) + T(298, 197, 'Nung', size=12))
    b.append(box(346, 184, 130, 46, ['Xi măng'], fill=LGREY, size=14, bold=True))
    b.append(TL(600, 98, ['Đồ gốm, sứ cũng thuộc', 'công nghiệp silicate'], size=12, lh=16))
    return svg(720, 262, ''.join(b))


# ---------------------------------------------------------------- bài 35
def arrow_between(x1, y1, x2, y2, label, lx, ly, anchor='middle'):
    return L(x1, y1, x2, y2, arrow=True, w=2, stroke='#3a5a82') + T(lx, ly, label, size=12, anchor=anchor)


def fig_chu_trinh_carbon():
    b = [title(720, 'Chu trình carbon')]
    ATM = (360, 66)
    b.append(R(270, 44, 180, 46, fill=LBLUE, rx=10) + T(360, 64, 'Khí quyển', size=15, weight='bold') + T(360, 82, 'CO₂', size=13))
    b.append(box(40, 170, 150, 46, ['Thực vật'], fill=LGREEN, size=15, bold=True))
    b.append(box(530, 170, 150, 46, ['Động vật'], fill='#f4d9d9', size=15, bold=True))
    b.append(box(40, 300, 190, 50, ['Xác sinh vật,', 'chất thải trong đất'], fill='#e4dccb', size=13))
    b.append(box(490, 300, 190, 50, ['Nhiên liệu hoá thạch', '(than, dầu, khí)'], fill=LGREY, size=13))
    b.append(arrow_between(290, 94, 170, 168, 'Quang hợp', 188, 122, 'end'))
    b.append(arrow_between(190, 193, 528, 193, 'Làm thức ăn', 360, 184))
    b.append(arrow_between(580, 168, 430, 92, 'Hô hấp', 532, 124, 'start'))
    b.append(arrow_between(115, 218, 115, 296, 'Chết', 126, 262, 'start'))
    b.append(arrow_between(590, 218, 200, 298, 'Chết', 420, 262))
    b.append(arrow_between(235, 310, 330, 92, 'Phân giải', 262, 232, 'start'))
    b.append(arrow_between(540, 298, 408, 92, 'Đốt nhiên liệu', 520, 270, 'start'))
    b.append(T(360, 374, 'Thực vật cũng thải CO₂ qua hô hấp.', size=12, fill='#444'))
    return svg(720, 390, ''.join(b))


FIGS = {
    'c-hoa9-b18-vat-li.svg': fig_kim_loai_vat_li,
    'c-hoa9-b18-fe-cuso4.svg': fig_fe_cuso4,
    'c-hoa9-b19-day-hoat-dong.svg': fig_day_hoat_dong,
    'c-hoa9-b20-tach-kim-loai.svg': fig_tach_kim_loai,
    'c-hoa9-b20-hop-kim.svg': fig_hop_kim,
    'c-hoa9-b21-kl-pk.svg': fig_kl_pk,
    'c-hoa9-b22-phan-loai.svg': fig_huu_co_phan_loai,
    'c-hoa9-b22-cau-tao.svg': fig_huu_co_cau_tao,
    'c-hoa9-b23-alkane.svg': fig_alkane,
    'c-hoa9-b24-alkene.svg': fig_alkene,
    'c-hoa9-b25-chung-cat.svg': fig_chung_cat,
    'c-hoa9-b26-ethanol.svg': fig_ethanol,
    'c-hoa9-b27-acetic.svg': fig_acetic,
    'c-hoa9-b28-lipid.svg': fig_lipid,
    'c-hoa9-b29-glucose.svg': fig_glucose,
    'c-hoa9-b30-tinh-bot.svg': fig_tinh_bot,
    'c-hoa9-b31-protein.svg': fig_protein,
    'c-hoa9-b32-polymer.svg': fig_polymer,
    'c-hoa9-b33-vo-trai-dat.svg': fig_vo_trai_dat,
    'c-hoa9-b34-da-voi.svg': fig_da_voi,
    'c-hoa9-b34-silicate.svg': fig_silicate,
    'c-hoa9-b35-chu-trinh-carbon.svg': fig_chu_trinh_carbon,
}

C6 = 'tap1/chuong-6/'
ATTACH = [
    (C6 + 'bai-18/tinh-chat-chung-kim-loai.json', 0, 'c-hoa9-b18-vat-li.svg', 'Tính chất vật lí chung của kim loại.'),
    (C6 + 'bai-18/tinh-chat-chung-kim-loai.json', 3, 'c-hoa9-b18-fe-cuso4.svg', 'Sắt đẩy đồng ra khỏi dung dịch CuSO₄.'),
    (C6 + 'bai-19/day-hoat-dong-hoa-hoc.json', 0, 'c-hoa9-b19-day-hoat-dong.svg', 'Dãy hoạt động hoá học và ý nghĩa của dãy.'),
    (C6 + 'bai-20/tach-kim-loai-hop-kim.json', 0, 'c-hoa9-b20-tach-kim-loai.svg', 'Phương pháp tách kim loại theo mức độ hoạt động.'),
    (C6 + 'bai-20/tach-kim-loai-hop-kim.json', 2, 'c-hoa9-b20-hop-kim.svg', 'Gang, thép và một số hợp kim thông dụng.'),
    (C6 + 'bai-21/phi-kim-va-kim-loai.json', 2, 'c-hoa9-b21-kl-pk.svg', 'So sánh tính chất của kim loại và phi kim.'),
    ('tap1/chuong-7/bai-22/gioi-thieu-hop-chat-huu-co.json', 2, 'c-hoa9-b22-phan-loai.svg', 'Phân loại hợp chất hữu cơ.'),
    ('tap1/chuong-7/bai-22/gioi-thieu-hop-chat-huu-co.json', 3, 'c-hoa9-b22-cau-tao.svg', 'Công thức cấu tạo của một số hợp chất hữu cơ.'),
    ('tap1/chuong-7/bai-23/alkane.json', 0, 'c-hoa9-b23-alkane.svg', 'Công thức cấu tạo của một số alkane.'),
    ('tap1/chuong-7/bai-24/alkene.json', 2, 'c-hoa9-b24-alkene.svg', 'Cấu tạo ethylene và phản ứng cộng với nước bromine.'),
    ('tap1/chuong-7/bai-25/nguon-nhien-lieu.json', 1, 'c-hoa9-b25-chung-cat.svg', 'Sơ đồ chưng cất dầu mỏ.'),
    ('tap1/chuong-8/bai-26/ethylic-alcohol.json', 1, 'c-hoa9-b26-ethanol.svg', 'Cấu tạo ethanol và ý nghĩa của độ cồn.'),
    ('tap1/chuong-8/bai-27/acetic-acid.json', 2, 'c-hoa9-b27-acetic.svg', 'Cấu tạo acetic acid và phản ứng ester hoá.'),
    ('tap1/chuong-9/bai-28/lipid.json', 2, 'c-hoa9-b28-lipid.svg', 'Cấu tạo chất béo và phản ứng xà phòng hoá.'),
    ('tap1/chuong-9/bai-29/glucose-saccharose.json', 2, 'c-hoa9-b29-glucose.svg', 'Phản ứng lên men glucose và thuỷ phân saccharose.'),
    ('tap1/chuong-9/bai-30/tinh-bot-cellulose.json', 2, 'c-hoa9-b30-tinh-bot.svg', 'Mắt xích của tinh bột, cellulose và phép thử iodine.'),
    ('tap1/chuong-9/bai-31/protein.json', 0, 'c-hoa9-b31-protein.svg', 'Protein là chuỗi nhiều amino acid.'),
    ('tap1/chuong-9/bai-32/polymer.json', 1, 'c-hoa9-b32-polymer.svg', 'Mắt xích và phân loại polymer.'),
    ('tap1/chuong-10/bai-33/hoa-hoc-vo-trai-dat.json', 0, 'c-hoa9-b33-vo-trai-dat.svg', 'Thành phần các nguyên tố trong vỏ Trái Đất (xấp xỉ).'),
    ('tap1/chuong-10/bai-34/da-voi-silicate.json', 0, 'c-hoa9-b34-da-voi.svg', 'Nung đá vôi và tôi vôi.'),
    ('tap1/chuong-10/bai-34/da-voi-silicate.json', 2, 'c-hoa9-b34-silicate.svg', 'Nguyên liệu sản xuất thuỷ tinh và xi măng.'),
    ('tap1/chuong-10/bai-35/chu-trinh-carbon.json', 2, 'c-hoa9-b35-chu-trinh-carbon.svg', 'Chu trình carbon trong tự nhiên.'),
]

if __name__ == '__main__':
    write_figs(S, FIGS)
    for a in ATTACH:
        attach(S, *a)
    print('hoa9: %d hình' % len(FIGS))
