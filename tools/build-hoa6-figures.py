#!/usr/bin/env python3
# Hình minh họa lý thuyết Hoá học 6 (sơ đồ mô phỏng). Chạy: python3 tools/build-hoa6-figures.py
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

S = 'hoa6'


def fig_vat_the_chat():
    b = [title(720, 'Vật thể và chất tạo nên vật thể')]
    rows = [
        ('Ấm đun nước', 'bằng nhôm', 'Vật thể nhân tạo', 'Chất: nhôm'),
        ('Cốc', 'bằng thuỷ tinh', 'Vật thể nhân tạo', 'Chất: thuỷ tinh'),
        ('Cây cối, đá, nước biển', '', 'Vật thể tự nhiên', 'Do một hay nhiều chất tạo nên'),
    ]
    y = 50
    for name, mat, kind, chat in rows:
        fill = LBLUE if 'nhân tạo' in kind else LGREEN
        b.append(R(30, y, 210, 70, fill=fill, rx=8))
        b.append(T(135, y + 30, name, size=16, weight='bold'))
        b.append(T(135, y + 52, mat or kind, size=14))
        b.append(L(245, y + 35, 330, y + 35, arrow=True))
        b.append(R(335, y, 160, 70, fill=LYELLOW, rx=8))
        b.append(T(415, y + 42, kind, size=14, weight='bold'))
        b.append(L(500, y + 35, 540, y + 35, arrow=True))
        b.append(R(545, y, 150, 70, fill='#ffffff', rx=8))
        b.append(TL(620, y + 30, chat.replace(': ', ':\n').split('\n') if len(chat) < 22 else ['Do một hay nhiều', 'chất tạo nên'], size=14))
        y += 90
    return svg(720, 320, ''.join(b))


def particles_solid(x, y, w, h):
    out = []
    n_c, n_r = 6, 5
    dx, dy = w / (n_c + 0.5), h / (n_r + 0.5)
    for r in range(n_r):
        for c in range(n_c):
            out.append(C(x + dx * (c + 0.75), y + dy * (r + 0.75), 8, fill=BLUE, stroke=BLUE))
    return ''.join(out)


def particles_liquid(x, y, w, h):
    out = []
    import random
    rnd = random.Random(5)
    pts = []
    n_c, n_r = 6, 3
    dx, dy = w / (n_c + 0.5), (h * 0.62) / (n_r + 0.3)
    for r in range(n_r):
        for c in range(n_c):
            px = x + dx * (c + 0.75) + rnd.uniform(-5, 5)
            py = y + h * 0.38 + dy * (r + 0.7) + rnd.uniform(-4, 4)
            pts.append((px, py))
    for px, py in pts:
        out.append(C(px, py, 8, fill=BLUE, stroke=BLUE))
    return ''.join(out)


def particles_gas(x, y, w, h):
    pos = [(0.15, 0.2), (0.5, 0.12), (0.82, 0.3), (0.3, 0.45), (0.68, 0.55), (0.12, 0.72), (0.45, 0.8), (0.85, 0.85)]
    return ''.join(C(x + w * a, y + h * b, 8, fill=BLUE, stroke=BLUE) for a, b in pos)


def fig_ba_the():
    b = [title(720, 'Ba thể của chất và sự chuyển thể (mô hình các hạt)')]
    px = [30, 280, 530]
    names = ['Thể rắn', 'Thể lỏng', 'Thể khí']
    for x, n, f in zip(px, names, (particles_solid, particles_liquid, particles_gas)):
        b.append(T(x + 80, 52, n, size=16, weight='bold'))
        b.append(R(x, 62, 160, 150, fill=LGREY, stroke=INK, sw=1.5))
        b.append(f(x + 2, 64, 156, 146))
    notes = [TL(110, 232, ['Hạt xếp sát nhau,', 'hình dạng, thể tích xác định'], size=12),
             TL(360, 232, ['Hạt chưa sát nhau,', 'thể tích xác định,', 'hình dạng không xác định'], size=12),
             TL(610, 232, ['Hạt chuyển động tự do,', 'không có hình dạng', 'và thể tích xác định'], size=12)]
    b += notes
    # mũi tên chuyển thể ở hai khoảng giữa
    for x0, up, down, temp in ((190, 'Nóng chảy', 'Đông đặc', '0 °C'), (440, 'Bay hơi', 'Ngưng tụ', '100 °C')):
        b.append(T(x0 + 45, 112, up, size=13, weight='bold'))
        b.append(L(x0 + 5, 120, x0 + 85, 120, arrow=True))
        b.append(L(x0 + 85, 148, x0 + 5, 148, arrow=True))
        b.append(T(x0 + 45, 168, down, size=13, weight='bold'))
        b.append(T(x0 + 45, 190, temp, size=12, fill='#555'))
    b.append(T(360, 300, 'Nhiệt độ ghi trên mũi tên ứng với nước: nóng chảy/đông đặc ở 0 °C, sôi ở 100 °C', size=12, fill='#555'))
    return svg(720, 312, ''.join(b))


def fig_khong_khi():
    cx, cy, r = 190, 165, 115
    parts = [('Nitrogen', 78, BLUE), ('Oxygen', 21, ORANGE), ('Khí khác', 1, GREY)]
    b = [title(720, 'Thành phần của không khí (theo thể tích, xấp xỉ)')]
    ang = -90.0
    for name, v, col in parts:
        a2 = ang + v * 3.6
        x1, y1 = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
        large = 1 if v > 50 else 0
        b.append(PATH('M%.1f,%.1f L%.1f,%.1f A%d,%d 0 %d 1 %.1f,%.1f Z' % (cx, cy, x1, y1, r, r, large, x2, y2), fill=col, stroke='#fff', w=2))
        ang = a2
    ly = 100
    for name, v, col in parts:
        b.append(R(380, ly - 14, 22, 22, fill=col, stroke=col))
        b.append(T(412, ly + 3, '%s: khoảng %d%%' % (name, v), size=17, anchor='start'))
        ly += 44
    b.append(TL(380, ly + 6, ['Khí khác gồm carbon dioxide, hơi nước,', 'khí hiếm… (khoảng 1%)'], size=14, anchor='start'))
    return svg(720, 300, ''.join(b))


def fig_vat_lieu():
    b = [title(720, 'Một số vật liệu thông dụng')]
    cards = [
        ('Kim loại', ['Dẫn điện tốt', 'Dẫn nhiệt tốt', 'Dễ uốn'], 'Dây điện|Nồi, xoong', '#d8dee6'),
        ('Nhựa', ['Nhẹ, bền', 'Cách điện'], 'Vỏ dây điện|Đồ dùng', LBLUE),
        ('Cao su', ['Đàn hồi', 'Cách điện', 'Không thấm nước'], 'Lốp xe|Găng tay', '#e4dccb'),
        ('Thuỷ tinh', ['Trong suốt', 'Giòn, dễ vỡ'], 'Cốc|Kính cửa sổ', '#d9eef0'),
        ('Gốm, sứ', ['Cứng', 'Cách điện', 'Cách nhiệt'], 'Bát, đĩa|Gạch men', LYELLOW),
    ]
    w = 128
    for i, (n, props, use, col) in enumerate(cards):
        x = 12 + i * (w + 8)
        b.append(R(x, 44, w, 200, fill=col, rx=8))
        b.append(T(x + w / 2, 72, n, size=16, weight='bold'))
        b.append(TL(x + w / 2, 100, props, size=12, lh=19))
        b.append(L(x + 14, 164, x + w - 14, 164, stroke=GREY, w=1))
        b.append(T(x + w / 2, 186, 'Dùng làm:', size=12, fill='#555'))
        b.append(TL(x + w / 2, 206, use.split('|'), size=12, lh=18))
    return svg(720, 258, ''.join(b))


def fig_nguyen_lieu():
    b = [title(720, 'Từ nguyên liệu đến sản phẩm')]
    rows = [('Quặng sắt', 'Gang, thép'), ('Đá vôi', 'Vôi, xi măng'), ('Cát', 'Thuỷ tinh'),
            ('Dầu mỏ', 'Nhiên liệu, chất dẻo'), ('Mủ cao su', 'Sản phẩm cao su')]
    y = 46
    b.append(T(130, y, 'Nguyên liệu', size=14, weight='bold', fill='#555'))
    b.append(T(560, y, 'Sản phẩm', size=14, weight='bold', fill='#555'))
    for a, p in rows:
        y += 46
        b.append(R(40, y - 22, 180, 36, fill=LGREEN, rx=8))
        b.append(T(130, y + 2, a, size=16, weight='bold'))
        b.append(L(228, y - 4, 400, y - 4, arrow=True))
        b.append(T(314, y - 10, 'chế biến', size=12, fill='#555'))
        b.append(R(408, y - 22, 280, 36, fill=LYELLOW, rx=8))
        b.append(T(548, y + 2, p, size=16))
    return svg(720, 300, ''.join(b))


def flame(x, y, s=1.0, col='#f28e2b'):
    d = ('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z'
         % (x, y - 34 * s, x + 6 * s, y - 20 * s, x + 20 * s, y - 14 * s, x + 14 * s, y,
            x + 10 * s, y + 8 * s, x - 10 * s, y + 8 * s, x - 14 * s, y,
            x - 18 * s, y - 10 * s, x - 6 * s, y - 20 * s, x, y - 34 * s))
    return PATH(d, fill=col, stroke='#c9701a', w=1.5)


def fig_nhien_lieu():
    b = [title(720, 'Phân loại nhiên liệu'), R(280, 40, 160, 38, fill=LYELLOW, rx=8),
         T(360, 65, 'Nhiên liệu', size=17, weight='bold')]
    cols = [('Nhiên liệu rắn', ['Than', 'Củi'], 120, '#e4dccb'),
            ('Nhiên liệu lỏng', ['Xăng', 'Dầu', 'Cồn'], 360, LBLUE),
            ('Nhiên liệu khí', ['Khí thiên nhiên', 'Khí gas', 'Biogas'], 600, '#d9eef0')]
    for name, ex, x, col in cols:
        b.append(L(360, 78, x, 110, w=1.5))
        b.append(R(x - 95, 110, 190, 38, fill=col, rx=8))
        b.append(T(x, 135, name, size=16, weight='bold'))
        yy = 170
        for e in ex:
            b.append(R(x - 70, yy, 140, 30, fill='#fff', rx=6, sw=1.5))
            b.append(T(x, yy + 21, e, size=15))
            yy += 38
        b.append(flame(x - 100 + 8, 200, 0.8))
    b.append(T(360, 305, 'Khi cháy, nhiên liệu toả nhiệt và phát sáng', size=14, fill='#555'))
    return svg(720, 322, ''.join(b))


def fig_chat_dinh_duong():
    b = [title(720, 'Các nhóm chất dinh dưỡng trong thực phẩm')]
    cards = [
        ('Carbohydrate', 'Cung cấp năng lượng|chủ yếu', 'Gạo, ngô, khoai, sắn', LYELLOW),
        ('Protein', 'Xây dựng,|tái tạo tế bào', 'Thịt, cá, trứng, sữa', '#f4d9d9'),
        ('Lipid (chất béo)', 'Dự trữ năng lượng,|hoà tan vitamin', 'Dầu ăn, mỡ', '#e4dccb'),
        ('Vitamin, chất khoáng', 'Tham gia các|hoạt động sống', 'Rau, quả', LGREEN),
    ]
    w = 168
    for i, (n, fn, ex, col) in enumerate(cards):
        x = 10 + i * (w + 9)
        b.append(R(x, 44, w, 190, fill=col, rx=8))
        b.append(TL(x + w / 2, 72, n.replace(' (', '\n(').replace(', ', ',\n').split('\n'), size=15, weight='bold', lh=18))
        b.append(TL(x + w / 2, 124, fn.split('|'), size=13, lh=18))
        b.append(L(x + 14, 168, x + w - 14, 168, stroke=GREY, w=1))
        b.append(T(x + w / 2, 190, 'Có nhiều trong:', size=12, fill='#555'))
        b.append(TL(x + w / 2, 210, [ex], size=13))
    return svg(720, 250, ''.join(b))


def fig_hon_hop():
    b = [title(720, 'Chất tinh khiết và hỗn hợp (mô hình các hạt)')]
    boxes = [(20, 'Chất tinh khiết', 'Nước cất'), (200, 'Hỗn hợp đồng nhất', 'Nước đường'),
             (380, 'Hỗn hợp không đồng nhất', 'Nước phù sa'), (560, 'Nhũ tương', 'Dầu trộn nước')]
    for x, n, ex in boxes:
        b.append(T(x + 70, 48, n, size=13, weight='bold'))
        b.append(R(x, 58, 140, 140, fill=LGREY, sw=1.5))
        b.append(T(x + 70, 222, ex, size=14))
    # tinh khiết: một loại hạt
    import random
    rnd = random.Random(3)
    for k in range(16):
        b.append(C(20 + 20 + (k % 4) * 33 + rnd.uniform(-3, 3), 58 + 24 + (k // 4) * 33 + rnd.uniform(-3, 3), 7, fill=BLUE, stroke=BLUE))
    # đồng nhất: hai loại hạt phân bố đều
    for k in range(16):
        col = BLUE if k % 2 == 0 else ORANGE
        b.append(C(200 + 20 + (k % 4) * 33, 58 + 24 + (k // 4) * 33, 7, fill=col, stroke=col))
    # không đồng nhất: hạt rắn lắng ở đáy
    b.append(R(380, 58, 140, 140, fill='#d9eef0', sw=1.5))
    rnd = random.Random(8)
    for k in range(10):
        b.append(C(380 + 14 + (k % 5) * 28 + rnd.uniform(-3, 3), 198 - 10 - (k // 5) * 17 + rnd.uniform(-2, 2), 7, fill='#8c6d46', stroke='#8c6d46'))
    for k in range(5):
        b.append(C(380 + 22 + k * 25, 90 + rnd.uniform(-8, 20), 3.5, fill='#8c6d46', stroke='#8c6d46'))
    # nhũ tương: giọt dầu phân tán trong nước
    b.append(R(560, 58, 140, 140, fill='#d9eef0', sw=1.5))
    for (a, c, r) in [(590, 90, 14), (655, 85, 11), (620, 135, 16), (675, 150, 12), (585, 170, 11)]:
        b.append(C(a, c, r, fill='#f5d76e', stroke='#c9a227', w=1.5))
    b.append(TL(360, 250, ['Chất tinh khiết: chỉ một loại chất. Hỗn hợp: hai hay nhiều chất trộn lẫn.'], size=13, fill='#555'))
    return svg(720, 268, ''.join(b))


def funnel_panel(x):
    out = []
    out.append(T(x + 100, 52, 'Lọc', size=16, weight='bold'))
    # phễu: hình thang ngược + cuống
    out.append(POLY([(x + 40, 85), (x + 160, 85), (x + 112, 150), (x + 88, 150)], fill=LGREY))
    out.append(PL([(x + 40, 85), (x + 100, 128), (x + 160, 85)], stroke=GREY, w=1.5))  # giấy lọc
    out.append(R(x + 94, 150, 12, 26, fill=LGREY, sw=2))
    out.append(R(x + 50, 188, 100, 62, fill='#ffffff', sw=2))
    out.append(R(x + 52, 214, 96, 34, fill='#d9eef0', stroke='none', sw=0))
    for k in range(3):
        out.append(C(x + 100, 178 + k * 0, 0.1))
    out.append(C(x + 100, 186, 2.2, fill=BLUE, stroke=BLUE))
    for (a, c) in [(70, 98), (105, 112), (125, 100), (92, 104)]:
        out.append(C(x + a, c, 3, fill='#8c6d46', stroke='#8c6d46'))
    out.append(T(x + 100, 272, 'Cát còn lại trên giấy lọc;', size=12))
    out.append(T(x + 100, 288, 'nước trong chảy xuống cốc', size=12))
    return ''.join(out)


def evap_panel(x):
    out = []
    out.append(T(x + 100, 52, 'Cô cạn', size=16, weight='bold'))
    # chén sứ (nửa hình tròn) trên kiềng, đèn cồn bên dưới
    out.append(PATH('M%d,120 L%d,120 Q%d,175 %d,120 Z' % (x + 55, x + 145, x + 100, x + 55), fill='#fff', stroke=INK, w=2))
    out.append(PATH('M%d,130 L%d,130 Q%d,165 %d,130 Z' % (x + 62, x + 138, x + 100, x + 62), fill='#d9eef0', stroke='none', w=0))
    out.append(L(x + 50, 150, x + 150, 150, w=3))  # kiềng
    out.append(L(x + 60, 150, x + 60, 262, w=3))
    out.append(L(x + 140, 150, x + 140, 262, w=3))
    # đèn cồn
    out.append(R(x + 78, 226, 44, 36, fill='#e0e6ec', rx=6))
    out.append(R(x + 94, 214, 12, 12, fill='#e0e6ec'))
    out.append(flame(x + 100, 214, 0.55))
    # hơi nước bay lên
    for dx in (-18, 0, 18):
        out.append(PATH('M%d,108 q6,-10 0,-20 q-6,-10 0,-20' % (x + 100 + dx), stroke=GREY, w=1.5))
    out.append(T(x + 100, 282, 'Nước bay hơi, muối', size=12))
    out.append(T(x + 100, 298, 'còn lại trong chén sứ', size=12))
    return ''.join(out)


def sep_funnel_panel(x):
    out = []
    out.append(T(x + 100, 52, 'Chiết', size=16, weight='bold'))
    out.append(PATH('M%d,82 L%d,82 L%d,150 L%d,190 L%d,190 L%d,150 Z' % (x + 85, x + 115, x + 140, x + 108, x + 92, x + 60), fill='#ffffff', stroke=INK, w=2))
    # lớp nước (dưới) và dầu (trên)
    out.append(PATH('M%d,150 L%d,150 L%d,190 L%d,190 Z' % (x + 60, x + 140, x + 108, x + 92), fill='#bcd7ee', stroke='none', w=0))
    out.append(PATH('M%d,104 L%d,104 L%d,150 L%d,150 Z' % (x + 76, x + 124, x + 140, x + 60), fill='#f5d76e', stroke='none', w=0))
    out.append(PATH('M%d,82 L%d,82 L%d,150 L%d,190 L%d,190 L%d,150 Z' % (x + 85, x + 115, x + 140, x + 108, x + 92, x + 60), fill='none', stroke=INK, w=2))
    out.append(L(x + 60, 150, x + 140, 150, stroke=GREY, w=1, dash='4 3'))
    out.append(R(x + 92, 190, 16, 12, fill=LGREY))
    out.append(L(x + 90, 196, x + 110, 196, w=2))
    out.append(R(x + 76, 214, 48, 40, fill='#fff', sw=2))
    out.append(R(x + 78, 236, 44, 16, fill='#bcd7ee', stroke='none', sw=0))
    out.append(T(x + 160, 128, 'Dầu ăn', size=12, anchor='start'))
    out.append(T(x + 160, 172, 'Nước', size=12, anchor='start'))
    out.append(T(x + 100, 276, 'Hai chất lỏng không hoà tan:', size=12))
    out.append(T(x + 100, 292, 'mở khoá để tháo lớp nước ra', size=12))
    return ''.join(out)


def fig_tach_chat():
    b = [title(720, 'Một số cách tách chất khỏi hỗn hợp')]
    b.append(funnel_panel(10))
    b.append(evap_panel(250))
    b.append(sep_funnel_panel(490))
    return svg(720, 310, ''.join(b))


FIGS = {
    'c-hoa6-b9-vat-the.svg': fig_vat_the_chat,
    'c-hoa6-b10-ba-the.svg': fig_ba_the,
    'c-hoa6-b11-khong-khi.svg': fig_khong_khi,
    'c-hoa6-b12-vat-lieu.svg': fig_vat_lieu,
    'c-hoa6-b13-nguyen-lieu.svg': fig_nguyen_lieu,
    'c-hoa6-b14-nhien-lieu.svg': fig_nhien_lieu,
    'c-hoa6-b15-chat-dinh-duong.svg': fig_chat_dinh_duong,
    'c-hoa6-b16-hon-hop.svg': fig_hon_hop,
    'c-hoa6-b17-tach-chat.svg': fig_tach_chat,
}

ATTACH = [
    ('tap1/chuong-2/bai-9/su-da-dang-cua-chat.json', 0, 'c-hoa6-b9-vat-the.svg', 'Vật thể tự nhiên, vật thể nhân tạo và chất tạo nên vật thể.'),
    ('tap1/chuong-2/bai-10/cac-the-cua-chat.json', 0, 'c-hoa6-b10-ba-the.svg', 'Ba thể của chất và các quá trình chuyển thể.'),
    ('tap1/chuong-2/bai-11/oxygen-khong-khi.json', 2, 'c-hoa6-b11-khong-khi.svg', 'Thành phần của không khí theo thể tích (xấp xỉ).'),
    ('tap1/chuong-3/bai-12/mot-so-vat-lieu.json', 1, 'c-hoa6-b12-vat-lieu.svg', 'Tính chất và ứng dụng của một số vật liệu.'),
    ('tap1/chuong-3/bai-13/mot-so-nguyen-lieu.json', 0, 'c-hoa6-b13-nguyen-lieu.svg', 'Một số nguyên liệu và sản phẩm chế biến từ chúng.'),
    ('tap1/chuong-3/bai-14/mot-so-nhien-lieu.json', 0, 'c-hoa6-b14-nhien-lieu.svg', 'Phân loại nhiên liệu: rắn, lỏng, khí.'),
    ('tap1/chuong-3/bai-15/luong-thuc-thuc-pham.json', 1, 'c-hoa6-b15-chat-dinh-duong.svg', 'Các nhóm chất dinh dưỡng và vai trò của chúng.'),
    ('tap1/chuong-4/bai-16/hon-hop-cac-chat.json', 2, 'c-hoa6-b16-hon-hop.svg', 'Chất tinh khiết và các loại hỗn hợp (mô hình các hạt).'),
    ('tap1/chuong-4/bai-17/tach-chat-khoi-hon-hop.json', 1, 'c-hoa6-b17-tach-chat.svg', 'Dụng cụ và cách tách chất: lọc, cô cạn, chiết.'),
]

if __name__ == '__main__':
    write_figs(S, FIGS)
    for a in ATTACH:
        attach(S, *a)
    print('hoa6: %d hình' % len(FIGS))
