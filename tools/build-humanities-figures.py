#!/usr/bin/env python3
# Sinh hình SVG minh họa cho môn Lịch sử 7 (content/lichsu7) và Địa lí 7 (content/diali7).
# Hình là sơ đồ, trục thời gian, biểu đồ vẽ lại từ số liệu trong sách; bản đồ chỉ là sơ đồ minh họa, không đúng tỉ lệ.
# Chạy: python3 tools/build-humanities-figures.py
import importlib.util
import math
import os
import random

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_spec = importlib.util.spec_from_file_location('khtn_fig', os.path.join(ROOT, 'tools', 'build-khtn-figures.py'))
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)
svg, T, L, C, R, POLY, PL = K.svg, K.T, K.L, K.C, K.R, K.POLY, K.PL
INK, GREY = K.INK, K.GREY
PAL = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#76b7b2', '#b07aa1']


def wrap(text, n):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        lines.append(cur)
    return lines


def TX(x, y, text, n=22, size=13, anchor='middle', weight='normal', fill=INK, lh=16):
    return ''.join(T(x, y + i * lh, ln, size=size, anchor=anchor, weight=weight, fill=fill)
                   for i, ln in enumerate(wrap(text, n)))


def box(x, y, w, h, text, fill='#eaf1f8', stroke='#4e79a7', n=None, size=13, weight='normal', tc=INK):
    n = n or max(8, int(w / 7.2))
    lines = wrap(text, n)
    out = R(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=8)
    y0 = y + h / 2 - (len(lines) - 1) * 8 + 5
    out += ''.join(T(x + w / 2, y0 + i * 16, ln, size=size, weight=weight, fill=tc) for i, ln in enumerate(lines))
    return out


def arrow(x1, y1, x2, y2, color=INK, w=2):
    return L(x1, y1, x2, y2, w=w, arrow=True, color=color)


def timeline(title, events, width=720, y=None, h=None, colors=None):
    """events: [(nhãn thời gian, mô tả)] xen kẽ phía trên và phía dưới trục."""
    n = len(events)
    x0, x1 = 50, width - 50
    per = max(14, int((x1 - x0) / n / 6.4))
    wr = [wrap(w, per) for _, w in events]
    up_lines = max([len(wr[i]) for i in range(0, n, 2)] or [1])
    dn_lines = max([len(wr[i]) for i in range(1, n, 2)] or [1])
    y = 50 + 64 + up_lines * 15
    h = y + 74 + dn_lines * 15 + 16
    b = [T(width / 2, 26, title, size=17, weight='bold')]
    b.append(L(x0 - 10, y, x1 + 10, y, w=3, arrow=True))
    for i, (when, what) in enumerate(events):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        col = (colors or PAL)[i % len(PAL)]
        b.append(C(x, y, 7, fill=col, stroke=col))
        up = i % 2 == 0
        b.append(L(x, y, x, y - 36 if up else y + 36, stroke=GREY, w=1.2))
        b.append(T(x, y - 44 if up else y + 56, when, size=14, weight='bold', fill=col))
        lines = wr[i]
        for k, ln in enumerate(lines):
            b.append(T(x, (y - 64 - (len(lines) - 1 - k) * 15) if up else (y + 74 + k * 15), ln, size=12))
    return svg(width, h, ''.join(b))


# ================================================================== LỊCH SỬ
def fig_giai_cap_phong_kien():
    b = [T(360, 24, 'Sự hình thành hai giai cấp cơ bản ở Tây Âu thời phong kiến', size=16, weight='bold')]
    b.append(box(40, 60, 180, 56, 'Quý tộc thị tộc Giéc-man', fill='#fdf0e0', stroke='#f28e2b'))
    b.append(box(40, 130, 180, 56, 'Quý tộc La Mã quy thuận', fill='#fdf0e0', stroke='#f28e2b'))
    b.append(box(280, 85, 160, 76, 'Lãnh chúa phong kiến', fill='#f9d9d9', stroke='#e15759', weight='bold'))
    b.append(arrow(220, 88, 280, 110))
    b.append(arrow(220, 158, 280, 136))
    b.append(box(40, 250, 180, 56, 'Nông dân tự do bị mất ruộng đất', fill='#e5f3e1', stroke='#59a14f'))
    b.append(box(40, 320, 180, 56, 'Nô lệ được giải phóng', fill='#e5f3e1', stroke='#59a14f'))
    b.append(box(280, 275, 160, 76, 'Nông nô', fill='#d8ecd3', stroke='#59a14f', weight='bold'))
    b.append(arrow(220, 278, 280, 300))
    b.append(arrow(220, 348, 280, 326))
    b.append(L(360, 161, 360, 275, w=2.5, color='#e15759', arrow=True))
    b.append(L(360, 275, 360, 161, w=2.5, color='#59a14f', arrow=True))
    b.append(TX(520, 205, 'Lãnh chúa bóc lột nông nô bằng tô, thuế và chi phối đời sống của họ', 26, anchor='start'))
    b.append(TX(520, 250, 'Nông nô nhận ruộng đất, nộp tô, thuế cho lãnh chúa', 26, anchor='start'))
    return svg(720, 400, ''.join(b))


def fig_lanh_dia():
    b = [T(360, 24, 'Sơ đồ một lãnh địa phong kiến ở Tây Âu (minh họa)', size=16, weight='bold')]
    b.append(R(40, 50, 640, 320, fill='#eef5e6', stroke='#59a14f', sw=2, rx=14))
    b.append(R(70, 80, 230, 150, fill='#f7e9d4', stroke='#b07a3a', sw=2, rx=8))
    b.append(POLY([(110, 150), (110, 110), (130, 110), (130, 120), (150, 120), (150, 110), (170, 110), (170, 150)], '#b9a18a', INK))
    b.append(T(140, 175, 'Lâu đài', size=14, weight='bold'))
    b.append(R(200, 120, 40, 40, fill='#c9d3dd', stroke=INK, sw=1.5))
    b.append(POLY([(200, 120), (220, 98), (240, 120)], '#8d7b6a', INK))
    b.append(T(220, 175, 'Nhà thờ', size=13))
    b.append(T(185, 210, 'Khu ở của lãnh chúa có hào nước bao quanh', size=11))
    b.append(R(340, 80, 150, 90, fill='#f6e7b0', stroke='#c9a227', sw=1.5, rx=6))
    b.append(T(415, 130, 'Đất của lãnh chúa', size=13, weight='bold'))
    b.append(R(510, 80, 150, 90, fill='#dcecc4', stroke='#59a14f', sw=1.5, rx=6))
    b.append(TX(585, 120, 'Đất khẩu phần của nông nô', 16, size=13, weight='bold'))
    b.append(R(340, 200, 150, 70, fill='#e6d3c0', stroke='#8d6b4a', sw=1.5, rx=6))
    b.append(TX(415, 230, 'Nhà ở của nông nô, chuồng trại, nhà kho', 20, size=12))
    b.append(R(510, 200, 150, 70, fill='#cfe6f5', stroke='#4e79a7', sw=1.5, rx=6))
    b.append(TX(585, 232, 'Đồng cỏ, rừng, ao hồ', 18, size=13))
    b.append(TX(360, 320, 'Mỗi lãnh địa có quân đội, luật pháp, toà án, thuế khoá, tiền tệ riêng; kinh tế tự cấp tự túc.', 70, size=13))
    return svg(720, 390, ''.join(b))


def fig_phat_kien():
    return timeline('Các cuộc phát kiến địa lí lớn cuối thế kỉ XV – đầu thế kỉ XVI', [
        ('1487', 'B. Đi-a-xơ đến mũi Hảo Vọng (cực Nam châu Phi)'),
        ('1492', 'C. Cô-lôm-bô vượt Đại Tây Dương, tìm ra châu Mỹ'),
        ('1497', 'V. Ga-ma vòng qua cực Nam châu Phi, cập bến Ca-li-cút (Ấn Độ)'),
        ('1519 – 1522', 'Ph. Ma-gien-lăng (đoàn thám hiểm) đi vòng quanh thế giới bằng đường biển')], h=330)


def fig_trieu_dai_tq():
    items = [('Đường', 618, 907), ('Ngũ đại', 907, 960), ('Tống', 960, 1279), ('Nguyên', 1271, 1368),
             ('Minh', 1368, 1644), ('Thanh', 1644, 1911)]
    x0, x1 = 60, 680
    f = lambda v: x0 + (v - 600) / (1920 - 600) * (x1 - x0)
    b = [T(360, 24, 'Các triều đại phong kiến Trung Quốc (thế kỉ VII – giữa thế kỉ XIX)', size=16, weight='bold')]
    b.append(L(x0, 250, x1, 250, w=2))
    for v in range(600, 1901, 200):
        b.append(L(f(v), 246, f(v), 256, w=1.5))
        b.append(T(f(v), 274, str(v), size=12))
    for i, (name, a, z) in enumerate(items):
        y = 70 + i * 28
        b.append(R(f(a), y, max(f(z) - f(a), 14), 22, fill=PAL[i % 6], stroke='none', rx=4, opacity=0.9))
        long_bar = f(z) - f(a) > 150
        if long_bar:
            b.append(T(f(a) + 4, y + 16, '%s (%d – %d)' % (name, a, z), size=12, anchor='start', fill='#ffffff'))
        elif f(z) > 600:
            b.append(T(f(a) - 6, y + 16, '%s (%d – %d)' % (name, a, z), size=12, anchor='end'))
        else:
            b.append(T(f(z) + 6, y + 16, '%s (%d – %d)' % (name, a, z), size=12, anchor='start'))
    b.append(TX(360, 310, 'Nhà Nguyên bắt đầu từ năm 1271 (Hốt Tất Liệt đặt quốc hiệu), thống trị toàn Trung Quốc từ năm 1279.', 90, size=12))
    return svg(720, 340, ''.join(b))


def fig_an_do():
    return timeline('Ấn Độ dưới thời các vương triều (thế kỉ IV – giữa thế kỉ XIX)', [
        ('Đầu thế kỉ IV', 'Vương triều Gúp-ta, thời hoàng kim; thống nhất lưu vực sông Hằng'),
        ('1206', 'Vương triều Hồi giáo Đê-li được thành lập'),
        ('Đầu thế kỉ XVI', 'Vương triều Mô-gôn lật đổ Đê-li; thịnh vượng dưới thời vua A-cơ-ba'),
        ('Giữa thế kỉ XIX', 'Mô-gôn suy yếu, Ấn Độ bị thực dân Anh xâm lược')], h=340)


def fig_dna_vuong_quoc():
    rows = [('Vương quốc Pa-gan → Mi-an-ma', 'lưu vực sông I-ra-oa-đi'),
            ('Vương quốc Ha-ri-pun-giay-a', 'lưu vực sông Chao Phray-a'),
            ('Đại Việt, Chăm-pa, Cam-pu-chia', 'bán đảo Đông Dương'),
            ('Vương quốc Sri Vi-giay-a', 'đảo Xu-ma-tra'),
            ('Vương triều Mô-giô-pa-hít', 'đảo Gia-va (thế kỉ XIII)'),
            ('A-út-thay-a (người Thái), Lan Xang (người Lào), Ma-lắc-ca', 'thế kỉ XIII – XV')]
    b = [T(360, 24, 'Các vương quốc phong kiến Đông Nam Á tiêu biểu', size=16, weight='bold')]
    b.append(R(40, 44, 640, 30, fill='#4e79a7', stroke='none', rx=4))
    b.append(T(240, 65, 'Vương quốc', size=14, weight='bold', fill='#ffffff'))
    b.append(T(540, 65, 'Khu vực / thời gian', size=14, weight='bold', fill='#ffffff'))
    for i, (a, c) in enumerate(rows):
        y = 78 + i * 40
        b.append(R(40, y, 640, 38, fill='#f5f8fb' if i % 2 else '#ffffff', stroke='#d6e0ea', sw=1))
        b.append(T(50, y + 24, a, size=13, anchor='start'))
        b.append(T(670, y + 24, c, size=13, anchor='end'))
    return svg(720, 330, ''.join(b))


def fig_lao_campuchia():
    return timeline('Vương quốc Cam-pu-chia và Vương quốc Lào', [
        ('Năm 802', 'Giay-a-vác-man II thống nhất, đặt tên nước Cam-pu-chia'),
        ('Thế kỉ IX – XV', 'Thời kì Ăng-co rực rỡ (Ăng-co Vát, Ăng-co Thom)'),
        ('Năm 1353', 'Pha Ngừm thống nhất các mường Lào, lập Vương quốc Lan Xang'),
        ('Thế kỉ XV', 'Cam-pu-chia suy yếu, dời kinh đô về phía nam Biển Hồ (Phnôm Pênh)')], h=340)


def fig_939_1009():
    return timeline('Đất nước buổi đầu độc lập (939 – 1009)', [
        ('939', 'Ngô Quyền xưng vương, đóng đô ở Cổ Loa'),
        ('944', 'Ngô Quyền mất; đất nước loạn 12 sứ quân'),
        ('968', 'Đinh Bộ Lĩnh dẹp loạn, lên ngôi, đặt tên nước Đại Cồ Việt'),
        ('981', 'Lê Hoàn đại phá quân Tống'),
        ('1009', 'Nhà Tiền Lê kết thúc, Lý Công Uẩn lên ngôi')], h=340)


def fig_dong_thoi_gian_vn():
    items = [('Ngô', 939, 965), ('Đinh', 968, 980), ('Tiền Lê', 980, 1009), ('Lý', 1009, 1225), ('Trần', 1226, 1400),
             ('Hồ', 1400, 1407), ('Minh đô hộ', 1407, 1427), ('Lê sơ', 1428, 1527)]
    x0, x1 = 50, 690
    f = lambda v: x0 + (v - 900) / (1550 - 900) * (x1 - x0)
    b = [T(360, 24, 'Các triều đại Việt Nam từ năm 939 đến năm 1527', size=16, weight='bold')]
    b.append(L(x0, 230, x1, 230, w=2))
    for v in range(900, 1551, 100):
        b.append(L(f(v), 226, f(v), 236, w=1.5))
        b.append(T(f(v), 254, str(v), size=12))
    for i, (name, a, z) in enumerate(items):
        y = 50 + i * 21
        col = '#9aa5b1' if name.startswith('Minh') else PAL[i % 6]
        b.append(R(f(a), y, max(f(z) - f(a), 10), 17, fill=col, stroke='none', rx=3))
        lab = '%s (%d – %d)' % (name, a, z)
        if f(z) - f(a) >= 150:
            b.append(T(f(a) + 4, y + 13, lab, size=12, anchor='start', fill='#ffffff'))
        elif f(z) > 640:
            b.append(T(f(a) - 6, y + 13, lab, size=12, anchor='end'))
        else:
            b.append(T(f(z) + 6, y + 13, lab, size=12, anchor='start'))
    return svg(720, 280, ''.join(b))


def fig_bo_may_ly():
    b = [T(360, 24, 'Tổ chức chính quyền nhà Lý', size=16, weight='bold')]
    b.append(box(260, 44, 200, 44, 'Vua (cha truyền con nối)', fill='#f9d9d9', stroke='#e15759', weight='bold'))
    b.append(box(150, 118, 160, 44, 'Quan văn', fill='#eaf1f8'))
    b.append(box(410, 118, 160, 44, 'Quan võ', fill='#eaf1f8'))
    b.append(arrow(330, 88, 250, 118))
    b.append(arrow(390, 88, 470, 118))
    b.append(box(220, 196, 280, 44, '24 lộ, phủ (miền núi gọi là châu)', fill='#e5f3e1', stroke='#59a14f'))
    b.append(box(260, 270, 200, 40, 'Hương, huyện', fill='#fdf0e0', stroke='#f28e2b'))
    b.append(box(280, 340, 160, 40, 'Xã (cấp cơ sở)', fill='#f3e8f7', stroke='#b07aa1'))
    b.append(arrow(250, 162, 320, 196))
    b.append(arrow(470, 162, 400, 196))
    b.append(arrow(360, 240, 360, 270))
    b.append(arrow(360, 310, 360, 340))
    return svg(720, 400, ''.join(b))


def fig_bo_may_le_so():
    b = [T(360, 24, 'Bộ máy nhà nước thời Lê sơ (hoàn chỉnh dưới thời Lê Thánh Tông)', size=15, weight='bold')]
    b.append(box(240, 44, 240, 44, 'Hoàng đế nắm mọi quyền hành', fill='#f9d9d9', stroke='#e15759', weight='bold'))
    for i, nm in enumerate(['Lại', 'Hộ', 'Lễ', 'Binh', 'Hình', 'Công']):
        x = 60 + i * 100
        b.append(box(x, 130, 88, 40, 'Bộ ' + nm, fill='#eaf1f8'))
        b.append(L(360, 88, x + 44, 130, stroke=GREY, w=1.2))
    b.append(T(360, 195, 'Sáu bộ, đứng đầu mỗi bộ là Thượng thư', size=13))
    b.append(box(240, 220, 240, 40, 'Đạo / thừa tuyên', fill='#e5f3e1', stroke='#59a14f'))
    b.append(box(240, 285, 240, 40, 'Phủ → huyện, châu', fill='#fdf0e0', stroke='#f28e2b'))
    b.append(box(240, 350, 240, 40, 'Xã / sách / động', fill='#f3e8f7', stroke='#b07aa1'))
    b.append(arrow(360, 260, 360, 285))
    b.append(arrow(360, 325, 360, 350))
    return svg(720, 410, ''.join(b))


def fig_chong_tong():
    b = [T(360, 24, 'Sơ đồ cuộc kháng chiến chống Tống (1077) – minh họa', size=16, weight='bold')]
    b.append(R(40, 50, 640, 80, fill='#f3e0e0', stroke='none'))
    b.append(T(120, 80, 'Đất Tống', size=14, weight='bold', fill='#a63a3d'))
    b.append(R(40, 260, 640, 100, fill='#e6f1df', stroke='none'))
    b.append(T(120, 330, 'Đại Việt', size=14, weight='bold', fill='#3b7a31'))
    b.append(PL([(40, 205), (200, 195), (360, 215), (520, 200), (680, 210)], stroke='#4e79a7', w=8))
    b.append(T(80, 188, 'Sông Như Nguyệt', size=13, fill='#4e79a7', weight='bold', anchor='start'))
    b.append(L(320, 130, 320, 190, w=3, color='#a63a3d', arrow=True))
    b.append(T(270, 160, 'Quân bộ nhà Tống', size=13, anchor='end', fill='#a63a3d'))
    b.append(L(560, 140, 600, 190, w=3, color='#a63a3d', arrow=True, dash='6 4'))
    b.append(T(670, 130, 'Thuỷ binh Tống bị chặn ở ven biển', size=12, anchor='end', fill='#a63a3d'))
    b.append(R(250, 225, 150, 12, fill='#59a14f', stroke='none'))
    b.append(T(325, 252, 'Phòng tuyến của Lý Thường Kiệt', size=13, weight='bold', fill='#3b7a31'))
    b.append(L(450, 300, 450, 225, w=3, color='#59a14f', arrow=True))
    b.append(T(460, 300, 'Phản công đêm', size=12, anchor='start', fill='#3b7a31'))
    b.append(TX(360, 385, 'Năm 1075: Lý Thường Kiệt chủ động đánh Ung Châu ("tiến công trước để tự vệ"); năm 1077: chặn giặc ở sông Như Nguyệt.', 90, size=12))
    return svg(720, 420, ''.join(b))


def fig_mong_nguyen():
    return timeline('Ba lần kháng chiến chống quân Mông – Nguyên thời Trần', [
        ('1258', 'Chống Mông Cổ; "vườn không nhà trống"; thắng ở Đông Bộ Đầu'),
        ('1285', 'Chống Nguyên lần 1: Hội nghị Diên Hồng; thắng Tây Kết, Hàm Tử, Chương Dương'),
        ('1287 – 1288', 'Chống Nguyên lần 2: Vân Đồn – Cửa Lục; đại thắng trên sông Bạch Đằng')], h=340)


def fig_ho_quy_ly():
    cols = [('Chính trị, quân sự', ['Củng cố quân chủ tập quyền', 'Xây thành luỹ (Tây Đô)', 'Chế tạo súng thần cơ']),
            ('Kinh tế, xã hội', ['Hạn điền, hạn nô', 'Phát hành tiền giấy', 'Thống nhất đo lường']),
            ('Văn hoá, giáo dục', ['Cải cách học tập, thi cử', 'Kì thi Thái học sinh (1400)', 'Khuyến khích chữ Nôm'])]
    b = [T(360, 24, 'Một số nội dung cải cách của Hồ Quý Ly', size=16, weight='bold')]
    for i, (h, ls) in enumerate(cols):
        x = 30 + i * 225
        b.append(R(x, 50, 210, 36, fill=PAL[i], stroke='none', rx=6))
        b.append(T(x + 105, 74, h, size=14, weight='bold', fill='#ffffff'))
        for j, t in enumerate(ls):
            b.append(box(x, 98 + j * 58, 210, 48, t, fill='#f5f8fb', stroke=PAL[i]))
    return svg(720, 290, ''.join(b))


def fig_lam_son():
    return timeline('Các mốc chính của khởi nghĩa Lam Sơn', [
        ('1416', 'Hội thề Lũng Nhai (Lê Lợi cùng 18 hào kiệt)'),
        ('1418', 'Lê Lợi dựng cờ khởi nghĩa, xưng Bình Định Vương'),
        ('1424', 'Giải phóng Nghệ An, mở rộng đến đèo Hải Vân'),
        ('Cuối 1426', 'Thắng Tốt Động – Chúc Động'),
        ('Cuối 1427', 'Thắng Chi Lăng – Xương Giang; Liễu Thăng bị giết'),
        ('1427 – 1428', 'Hội thề Đông Quan (10 – 12 – 1427); Lê Lợi lên ngôi (1428)')], h=370)


def fig_champa_nam_bo():
    return timeline('Vương quốc Chăm-pa (từ đầu thế kỉ X đến đầu thế kỉ XVI)', [
        ('988', 'Vương triều Vi-giay-a; kinh đô Vi-giay-a (Bình Định)'),
        ('1069', 'Vua Chăm-pa cắt ba châu Bố Chính, Địa Lý, Ma Linh cho Đại Việt'),
        ('1220 – 1353', 'Thời kì thịnh đạt nhất của Vương triều Vi-giay-a'),
        ('1471', 'Vi-giay-a suy sụp; lãnh thổ chia thành nhiều tiểu quốc')], h=340)


# ---------- Hoàng Sa - Trường Sa
def fig_hoang_sa_timeline():
    return timeline('Việt Nam xác lập và thực thi chủ quyền ở Hoàng Sa, Trường Sa', [
        ('Thế kỉ XVII', 'Chúa Nguyễn lập đội Hoàng Sa (kiêm quản đội Bắc Hải) ra khai thác, đo đạc'),
        ('1776', 'Lê Quý Đôn ghi chép về Hoàng Sa trong "Phủ biên tạp lục"'),
        ('1816', 'Vua Gia Long sai thuỷ quân cùng đội Hoàng Sa ra Hoàng Sa, cắm cờ, đo đạc thuỷ trình'),
        ('1833 – 1836', 'Vua Minh Mạng sai dựng miếu, lập bia, trồng cây, vẽ bản đồ, cắm mốc chủ quyền'),
        ('2012', 'Quốc hội thông qua Luật Biển Việt Nam, khẳng định chủ quyền')], h=370)


LAT0, LAT1, LON0, LON1 = 2.0, 24.0, 99.0, 121.0
MS = 28.5  # px / độ
MX, MY = 42, 50


def px(lon, lat):
    return MX + (lon - LON0) * MS, MY + (LAT1 - lat) * MS


def poly(points, fill, stroke='#8a97a8', w=1.2):
    return POLY([px(*p) for p in points], fill, stroke=stroke, sw=w)


def fig_ban_do_bien_dong():
    W, H = 720, 720
    b = [T(360, 26, 'Biển Đông và các quần đảo Hoàng Sa, Trường Sa của Việt Nam', size=17, weight='bold')]
    b.append(R(MX, MY, (LON1 - LON0) * MS, (LAT1 - LAT0) * MS, fill='#dcecf7', stroke='#8aa5bd', sw=1.5))
    # lưới kinh vĩ
    for lon in range(100, 121, 5):
        x, _ = px(lon, 0)
        b.append(L(x, MY, x, MY + (LAT1 - LAT0) * MS, stroke='#c3d6e6', w=1, dash='3 4'))
        b.append(T(x, MY + (LAT1 - LAT0) * MS + 18, '%d°Đ' % lon, size=12))
    for lat in range(4, 24, 4):
        _, y = px(0, lat)
        b.append(L(MX, y, MX + (LON1 - LON0) * MS, y, stroke='#c3d6e6', w=1, dash='3 4'))
        b.append(T(MX - 6, y + 4, '%d°B' % lat, size=12, anchor='end'))
    mainland = [(99, 24), (121, 24), (121, 23.3), (120.1, 23.0), (117.3, 23.4), (114.2, 22.3), (111.0, 21.5),
                (110.5, 20.4), (110.2, 20.3), (109.8, 21.0), (109.6, 21.6), (108.0, 21.5), (107.1, 20.9),
                (106.3, 20.2), (105.9, 19.8), (105.7, 18.8), (106.6, 18.1), (106.8, 17.5), (107.3, 16.8),
                (108.2, 16.1), (108.8, 15.4), (109.0, 14.7), (109.3, 13.7), (109.3, 12.9), (109.2, 12.2),
                (109.2, 11.6), (108.5, 11.1), (107.1, 10.3), (106.8, 10.4), (106.6, 9.9), (106.2, 9.5),
                (105.5, 9.0), (105.0, 8.6), (104.8, 8.8), (104.9, 9.6), (105.1, 10.0), (104.5, 10.4),
                (103.5, 10.6), (102.9, 11.6), (102.3, 12.2), (101.5, 12.6), (100.9, 13.4), (100.5, 13.5),
                (100.0, 13.4), (99.9, 12.6), (99.6, 11.0), (99.2, 10.0), (99.4, 9.2), (99.0, 8.9), (99, 2),
                (103.5, 2), (103.4, 4.0), (102.4, 6.1), (101.9, 6.9), (101.0, 6.9), (100.4, 7.2), (100.0, 8.2),
                (99.0, 9.0)]
    mainland = mainland[:-3]
    b.append(poly(mainland, '#e8e4dc'))
    vn = [(102.15, 22.4), (103.0, 22.7), (104.0, 22.8), (104.8, 23.3), (105.8, 23.1), (106.6, 22.9),
          (107.4, 22.4), (108.0, 21.5), (107.1, 20.9), (106.3, 20.2), (105.9, 19.8), (105.7, 18.8),
          (106.6, 18.1), (106.8, 17.5), (107.3, 16.8), (108.2, 16.1), (108.8, 15.4), (109.0, 14.7),
          (109.3, 13.7), (109.3, 12.9), (109.2, 12.2), (109.2, 11.6), (108.5, 11.1), (107.1, 10.3),
          (106.8, 10.4), (106.6, 9.9), (106.2, 9.5), (105.5, 9.0), (105.0, 8.6), (104.8, 8.8), (104.9, 9.6),
          (105.1, 10.0), (104.5, 10.4), (105.0, 10.9), (105.8, 10.9), (106.4, 11.7), (107.0, 12.2),
          (107.6, 13.0), (107.6, 14.4), (107.4, 15.2), (107.1, 16.5), (106.5, 17.4), (105.6, 18.0),
          (104.4, 19.5), (103.9, 20.5), (102.9, 21.8)]
    b.append(poly(vn, '#cfe8c3', stroke='#59a14f', w=1.6))
    # các đảo của nước khác (xám)
    b.append(poly([(108.6, 19.1), (109.5, 20.0), (110.6, 20.1), (111.0, 19.6), (110.4, 18.8), (109.6, 18.2), (108.7, 18.5)], '#e8e4dc'))
    b.append(poly([(117.3, 8.3), (117.6, 8.5), (119.6, 11.2), (119.2, 11.6), (118.4, 10.6), (117.5, 9.2)], '#e8e4dc'))
    b.append(poly([(120.4, 18.5), (120.6, 18.0), (120.1, 16.0), (119.9, 15.9), (120.0, 14.8), (120.6, 14.2),
                   (120.9, 14.0), (121, 14.5), (121, 18.5)], '#e8e4dc'))
    b.append(poly([(109.0, 2.0), (109.7, 2.0), (111.0, 2.7), (113.0, 3.2), (114.3, 4.4), (115.2, 5.4), (116.0, 6.1),
                   (116.8, 6.9), (117.3, 7.0), (117.7, 6.4), (118.1, 5.8), (119.2, 5.3), (118.4, 4.5),
                   (117.9, 4.2), (118.1, 3.0), (117.5, 2.0)], '#e8e4dc'))
    b.append(poly([(120.1, 23.0), (120.8, 22.0), (121, 22.0), (121, 24), (120.2, 24)], '#e8e4dc'))
    # đảo ven bờ của Việt Nam
    for nm, lon, lat, dx, dy, anc in [('Bạch Long Vĩ', 107.72, 20.13, 8, 4, 'start'), ('Cồn Cỏ', 107.34, 17.16, 8, 4, 'start'),
                                      ('Lý Sơn', 109.1, 15.38, 8, 4, 'start'), ('Phú Quý', 108.93, 10.52, 8, 4, 'start'),
                                      ('Côn Đảo', 106.6, 8.7, 8, 4, 'start'), ('Phú Quốc', 103.9, 10.2, -8, 4, 'end')]:
        x, y = px(lon, lat)
        b.append(C(x, y, 3, fill='#e15759', stroke='#e15759'))
        b.append(T(x + dx, y + dy, nm, size=11, anchor=anc))
    # quần đảo Hoàng Sa
    rnd = random.Random(7)
    hs = [(111.20 + rnd.random() * 1.7, 15.8 + rnd.random() * 1.3) for _ in range(24)]
    hx, hy = px(112.0, 16.5)
    b.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#e15759" stroke-width="1.5" stroke-dasharray="4 3"/>'
             % (hx, hy, 1.0 * MS * 1.15, 0.8 * MS * 1.1))
    for lon, lat in hs:
        x, y = px(lon, lat)
        b.append(C(x, y, 2.4, fill='#e15759', stroke='#e15759'))
    b.append(T(hx, hy - 30, 'Quần đảo Hoàng Sa', size=14, weight='bold', fill='#c0392b'))
    b.append(T(hx, hy - 15, '(Việt Nam)', size=12, fill='#c0392b'))
    # quần đảo Trường Sa
    rnd = random.Random(11)
    ts = []
    for _ in range(46):
        lon = 111.6 + rnd.random() * 5.5
        lat = 6.9 + rnd.random() * 4.6
        if lon - 111.6 < (11.6 - lat) * 0.9 + 0.6 and rnd.random() < 0.4:
            continue
        ts.append((lon, lat))
    tx, ty = px(114.4, 9.2)
    b.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#e15759" stroke-width="1.5" stroke-dasharray="4 3"/>'
             % (tx, ty, 3.1 * MS, 2.6 * MS))
    for lon, lat in ts:
        x, y = px(lon, lat)
        b.append(C(x, y, 2.4, fill='#e15759', stroke='#e15759'))
    for nm, lon, lat in [('Song Tử Tây', 114.33, 11.43), ('Sinh Tồn', 114.33, 9.88), ('Trường Sa Lớn', 111.92, 8.65),
                         ('An Bang', 112.92, 7.88)]:
        x, y = px(lon, lat)
        b.append(C(x, y, 3.6, fill='#c0392b', stroke='#ffffff', w=1))
        b.append(T(x + 7, y + 4, nm, size=11, anchor='start'))
    b.append(T(tx + 10, ty + 3.0 * MS + 16, 'Quần đảo Trường Sa (Việt Nam)', size=14, weight='bold', fill='#c0392b'))
    # nhãn
    b.append(T(*px(114.0, 14.0), 'BIỂN ĐÔNG', size=22, weight='bold', fill='#3d6d99'))
    b.append(T(*px(103.3, 19.6), 'VIỆT NAM', size=14, weight='bold', fill='#2f7a3a'))
    b.append(T(*px(100.8, 18.5), 'LÀO / THÁI LAN', size=12, fill='#6b7785'))
    b.append(T(*px(103.4, 12.8), 'CAM-PU-CHIA', size=12, fill='#6b7785'))
    b.append(T(*px(106.8, 23.7), 'TRUNG QUỐC', size=12, fill='#6b7785'))
    b.append(T(*px(119.0, 12.5), 'PHI-LIP-PIN', size=12, fill='#6b7785'))
    b.append(T(*px(113.0, 3.0), 'Bru-nây / Ma-lai-xi-a', size=12, fill='#6b7785'))
    for nm, lon, lat in [('Hà Nội', 105.85, 21.03), ('Đà Nẵng', 108.2, 16.05), ('TP. Hồ Chí Minh', 106.7, 10.8)]:
        x, y = px(lon, lat)
        b.append(R(x - 3, y - 3, 6, 6, fill=INK, stroke='none'))
        b.append(T(x - 7, y + 4, nm, size=11, anchor='end'))
    b.append(R(MX + 10, MY + (LAT1 - LAT0) * MS - 52, 218, 42, fill='#ffffff', stroke='#8aa5bd', sw=1, rx=6, opacity=0.92))
    b.append(C(MX + 24, MY + (LAT1 - LAT0) * MS - 36, 3, fill='#e15759', stroke='#e15759'))
    b.append(T(MX + 34, MY + (LAT1 - LAT0) * MS - 32, 'Đảo, quần đảo của Việt Nam', size=12, anchor='start'))
    b.append(T(MX + 22, MY + (LAT1 - LAT0) * MS - 16, 'Sơ đồ minh họa, không đúng tỉ lệ', size=11, anchor='start', fill='#6b7785'))
    return svg(W, H, ''.join(b))


LICH_SU_FIGS = {
    'ls-giai-cap-phong-kien.svg': fig_giai_cap_phong_kien,
    'ls-lanh-dia.svg': fig_lanh_dia,
    'ls-phat-kien-dia-li.svg': fig_phat_kien,
    'ls-trieu-dai-trung-quoc.svg': fig_trieu_dai_tq,
    'ls-an-do.svg': fig_an_do,
    'ls-dong-nam-a.svg': fig_dna_vuong_quoc,
    'ls-lao-campuchia.svg': fig_lao_campuchia,
    'ls-939-1009.svg': fig_939_1009,
    'ls-trieu-dai-viet-nam.svg': fig_dong_thoi_gian_vn,
    'ls-bo-may-nha-ly.svg': fig_bo_may_ly,
    'ls-chong-tong.svg': fig_chong_tong,
    'ls-mong-nguyen.svg': fig_mong_nguyen,
    'ls-cai-cach-ho-quy-ly.svg': fig_ho_quy_ly,
    'ls-lam-son.svg': fig_lam_son,
    'ls-bo-may-le-so.svg': fig_bo_may_le_so,
    'ls-champa.svg': fig_champa_nam_bo,
    'ls-hoang-sa-truong-sa-timeline.svg': fig_hoang_sa_timeline,
    'bien-dong-hoang-sa-truong-sa.svg': fig_ban_do_bien_dong,
}


# ================================================================== ĐỊA LÍ
def hbar(title, rows, unit='', maxv=None, width=720, colors=None, note=None):
    maxv = maxv or max(v for _, v in rows)
    n = len(rows)
    h = 70 + n * 44 + (30 if note else 0)
    b = [T(width / 2, 26, title, size=16, weight='bold')]
    for i, (name, v) in enumerate(rows):
        y = 52 + i * 44
        w = (width - 330) * v / maxv
        col = (colors or PAL)[i % 6]
        b.append(T(210, y + 20, name, size=13, anchor='end'))
        b.append(R(220, y, w, 28, fill=col, stroke='none', rx=4))
        b.append(T(228 + w, y + 20, ('%s %s' % (('%g' % v).replace('.', ','), unit)).strip(), size=13, anchor='start', weight='bold'))
    if note:
        b.append(T(width / 2, h - 12, note, size=12, fill='#6b7785'))
    return svg(width, h, ''.join(b))


def fig_dien_tich_chau():
    return hbar('Diện tích một số châu lục (triệu km²)', [('Châu Á', 44.4), ('Châu Phi', 30.3), ('Châu Âu', 10), ('Ô-xtrây-li-a', 7.7)],
                note='Châu Âu: trên 10 triệu km²; Ô-xtrây-li-a: lục địa lớn nhất của châu Đại Dương')


def fig_do_thi_hoa():
    return hbar('Tỉ lệ dân thành thị (%) ở một số khu vực', [('Châu Âu', 75), ('Bắc Mỹ', 82.6), ('Trung và Nam Mỹ', 80), ('Ô-xtrây-li-a', 86)],
                unit='%', maxv=100, note='Trung và Nam Mỹ: khoảng 80%')


def fig_dan_so_au():
    b = [T(360, 26, 'Cơ cấu dân số theo nhóm tuổi của châu Âu (%)', size=16, weight='bold')]
    data = {'1990': (20.5, 66.9, 12.6), '2020': (16.1, 64.8, 19.1)}
    cols = ['#4e79a7', '#59a14f', '#e15759']
    for k, (yr, vals) in enumerate(data.items()):
        y = 60 + k * 90
        b.append(T(40, y + 26, yr, size=15, weight='bold', anchor='middle'))
        x = 70
        for j, v in enumerate(vals):
            w = 600 * v / 100
            b.append(R(x, y, w, 40, fill=cols[j], stroke='#ffffff', sw=1))
            b.append(T(x + w / 2, y + 26, ('%g%%' % v).replace('.', ','), size=14, weight='bold', fill='#ffffff'))
            x += w
    for j, (nm, c) in enumerate(zip(['Dưới 15 tuổi', 'Từ 15 đến 64 tuổi', 'Từ 65 tuổi trở lên'], cols)):
        b.append(R(120 + j * 190, 245, 14, 14, fill=c, stroke='none'))
        b.append(T(140 + j * 190, 257, nm, size=13, anchor='start'))
    b.append(TX(360, 290, 'Dân số châu Âu già đi: nhóm từ 65 tuổi trở lên tăng từ 12,6% lên 19,1%.', 80, size=13))
    return svg(720, 310, ''.join(b))


def donut(cx, cy, r, frac, col, bg='#e3e8ee', w=26):
    c = 2 * math.pi * r
    return ('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="%g"/>'
            '<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="%g" stroke-dasharray="%.1f %.1f" transform="rotate(-90 %g %g)"/>'
            % (cx, cy, r, bg, w, cx, cy, r, col, w, c * frac, c * (1 - frac), cx, cy))


def fig_eu_gdp():
    b = [T(360, 26, 'Liên minh châu Âu trong nền kinh tế thế giới', size=16, weight='bold')]
    b.append(donut(190, 160, 72, 0.179, '#4e79a7'))
    b.append(T(190, 166, '17,9%', size=22, weight='bold'))
    b.append(TX(190, 268, 'Tỉ trọng GDP của EU trong GDP toàn thế giới (GDP EU 15 192,6 tỉ USD; thế giới 84 705,4 tỉ USD)', 34, size=12))
    b.append(donut(540, 160, 72, 0.31, '#f28e2b'))
    b.append(T(540, 166, 'Trên 31%', size=20, weight='bold'))
    b.append(TX(540, 268, 'Tỉ trọng EU trong xuất khẩu hàng hoá của thế giới', 34, size=12))
    return svg(720, 310, ''.join(b))


def fig_chau_a_dan_so():
    b = [T(360, 26, 'Dân số châu Á so với thế giới (2020)', size=16, weight='bold')]
    b.append(donut(220, 170, 82, 0.595, '#e15759', w=32))
    b.append(T(220, 176, '59,5%', size=24, weight='bold'))
    b.append(TX(520, 120, 'Châu Á: 4 641,1 triệu người, chiếm 59,5% dân số thế giới.', 28, size=14, anchor='start'))
    b.append(TX(520, 190, 'Châu Á là châu lục đông dân nhất thế giới.', 28, size=14, anchor='start'))
    return svg(720, 290, ''.join(b))


def fig_chau_a_khu_vuc():
    names = [('Bắc Á', '#4e79a7'), ('Trung Á', '#f28e2b'), ('Tây Á', '#59a14f'), ('Nam Á', '#e15759'), ('Đông Á', '#76b7b2'), ('Đông Nam Á', '#b07aa1')]
    b = [T(360, 26, 'Sáu khu vực của châu Á', size=16, weight='bold')]
    for i, (nm, c) in enumerate(names):
        x = 60 + (i % 3) * 215
        y = 52 + (i // 3) * 90
        b.append(box(x, y, 190, 66, nm, fill='#ffffff', stroke=c, size=16, weight='bold', tc=c))
    b.append(T(360, 260, 'Khu vực Đông Nam Á có 11 quốc gia, trong đó có Việt Nam.', size=13))
    return svg(720, 290, ''.join(b))


def fig_chau_phi_khi_hau():
    zones = [('Hoang mạc', '#f4d58d'), ('Xavan', '#bfd88a'), ('Rừng nhiệt đới', '#4e9a51'), ('Xavan', '#bfd88a'), ('Hoang mạc', '#f4d58d'),
             ('Cận nhiệt', '#a8c9a0')]
    b = [T(360, 26, 'Các đới khí hậu châu Phi phân bố đối xứng qua Xích đạo', size=16, weight='bold')]
    ys = [60, 110, 160, 210, 260, 310]
    order = [('Cận nhiệt (Bắc)', '#a8c9a0'), ('Hoang mạc', '#f4d58d'), ('Xavan', '#bfd88a'), ('Xích đạo (rừng nhiệt đới)', '#4e9a51'),
             ('Xavan', '#bfd88a'), ('Hoang mạc', '#f4d58d'), ('Cận nhiệt (Nam)', '#a8c9a0')]
    h = 46
    for i, (nm, c) in enumerate(order):
        y = 50 + i * h
        b.append(R(160, y, 400, h, fill=c, stroke='#ffffff', sw=1))
        b.append(T(360, y + 28, nm, size=14, weight='bold' if i == 3 else 'normal'))
    b.append(L(120, 50 + 3.5 * h, 160, 50 + 3.5 * h, stroke='#c0392b', w=2, arrow=True))
    b.append(T(114, 50 + 3.5 * h + 4, 'Xích đạo', size=12, anchor='end', fill='#c0392b'))
    return svg(720, 50 + 7 * h + 24, ''.join(b))


def fig_bac_my_dia_hinh():
    b = [T(360, 26, 'Địa hình Bắc Mỹ theo chiều từ tây sang đông', size=16, weight='bold')]
    pts = [(40, 250), (80, 130), (130, 70), (190, 120), (240, 200), (290, 250), (400, 255), (520, 250), (580, 200), (620, 170), (660, 230), (690, 260)]
    b.append(POLY(pts + [(690, 280), (40, 280)], '#cfe0c8', stroke='#59a14f', sw=2))
    b.append(T(130, 60, 'Miền núi Coóc-đi-e', size=13, weight='bold'))
    b.append(T(400, 235, 'Miền đồng bằng trung tâm', size=13, weight='bold'))
    b.append(T(620, 160, 'Núi A-pa-lát', size=13, weight='bold'))
    b.append(TX(360, 310, 'Ở giữa còn có hệ thống 14 hồ lớn, mỗi hồ rộng trên 5 000 km².', 80, size=13))
    return svg(720, 330, ''.join(b))


def fig_andet_dai_thuc_vat():
    bands = [('Trên 5 300 m', 'Băng tuyết', '#e8f1f8'), ('4 000 – 5 300 m', 'Đồng cỏ núi cao', '#cfe3b8'),
             ('3 000 – 4 000 m', 'Đồng cỏ', '#b6d98b'), ('1 300 – 3 000 m', 'Rừng lá kim', '#6fa86f'),
             ('1 000 – 1 300 m', 'Rừng lá rộng', '#4f9a52'), ('0 – 1 000 m', 'Rừng nhiệt đới', '#2e7d32')]
    b = [T(360, 26, 'Các đai thực vật ở sườn đông dãy An-đét', size=16, weight='bold')]
    for i, (a, nm, c) in enumerate(bands):
        y = 50 + i * 50
        w = 260 + i * 60
        b.append(R(360 - w / 2, y, w, 50, fill=c, stroke='#ffffff', sw=1))
        b.append(T(360, y + 30, '%s: %s' % (a, nm), size=14, fill=INK if i < 4 else '#ffffff', weight='bold'))
    return svg(720, 372, ''.join(b))


def fig_amazon():
    return hbar('Diện tích rừng A-ma-dôn ở Bra-xin (triệu km²)', [('Năm 1970', 4.0), ('Năm 2019', 3.39)],
                colors=['#4e9a51', '#e15759'], note='Rừng bị thu hẹp do khai thác gỗ, đốt rừng làm nông nghiệp, chăn nuôi')


def fig_nam_cuc():
    b = [T(360, 26, 'Châu Nam Cực – lục địa băng giá', size=16, weight='bold')]
    b.append(donut(190, 160, 72, 0.98, '#8bb8d9', w=30))
    b.append(T(190, 166, '98%', size=24, weight='bold'))
    b.append(TX(190, 268, 'Diện tích được băng bao phủ', 30, size=13))
    facts = ['Chứa khoảng 60% lượng nước ngọt của Trái Đất', 'Nhiệt độ thấp nhất: −94,5 °C (năm 1967)', 'Độ cao trung bình: hơn 2 040 m',
             'Phát hiện năm 1820; ngày 14 – 12 – 1911, A-mun-sen đặt chân tới cực Nam']
    for i, t in enumerate(facts):
        b.append(C(400, 106 + i * 50, 5, fill='#8bb8d9', stroke='#8bb8d9'))
        b.append(TX(414, 110 + i * 50, t, 38, size=13, anchor='start'))
    return svg(720, 310, ''.join(b))


def fig_chau_au_vi_tri():
    b = [T(360, 26, 'Vị trí và phạm vi châu Âu', size=16, weight='bold')]
    b.append(R(60, 50, 600, 260, fill='#eaf1f8', stroke='#8aa5bd', sw=1.5, rx=8))
    for i, (lat, y) in enumerate([('71°B', 70), ('60°B', 130), ('50°B', 190), ('36°B', 280)]):
        b.append(L(60, y, 660, y, stroke='#c3d6e6', w=1, dash='3 4'))
        b.append(T(54, y + 4, lat, size=12, anchor='end'))
    b.append(POLY([(180, 100), (260, 70), (360, 90), (460, 120), (520, 170), (460, 210), (400, 260), (300, 280), (210, 250), (170, 190)], '#cfe8c3', stroke='#59a14f', sw=2))
    b.append(TX(350, 160, 'Châu Âu: phần lớn nằm ở đới ôn hoà, từ khoảng 36°B đến 71°B; diện tích trên 10 triệu km²', 26, size=13, weight='bold'))
    b.append(TX(580, 100, 'Bắc Băng Dương', 14, size=12, fill='#3d6d99'))
    b.append(TX(120, 230, 'Đại Tây Dương', 14, size=12, fill='#3d6d99'))
    b.append(TX(350, 300, 'Địa Trung Hải', 14, size=12, fill='#3d6d99'))
    return svg(720, 340, ''.join(b))


GEO_FIGS = {
    'dl-dan-so-chau-au.svg': fig_dan_so_au,
    'dl-do-thi-hoa.svg': fig_do_thi_hoa,
    'dl-eu-kinh-te.svg': fig_eu_gdp,
    'dl-dien-tich-chau-luc.svg': fig_dien_tich_chau,
    'dl-chau-a-dan-so.svg': fig_chau_a_dan_so,
    'dl-chau-a-khu-vuc.svg': fig_chau_a_khu_vuc,
    'dl-chau-phi-khi-hau.svg': fig_chau_phi_khi_hau,
    'dl-bac-my-dia-hinh.svg': fig_bac_my_dia_hinh,
    'dl-andet-dai-thuc-vat.svg': fig_andet_dai_thuc_vat,
    'dl-rung-amazon.svg': fig_amazon,
    'dl-nam-cuc.svg': fig_nam_cuc,
    'bien-dong-hoang-sa-truong-sa.svg': fig_ban_do_bien_dong,
}


def write_all(figs, folder):
    d = os.path.join(ROOT, 'content', folder, 'figures')
    os.makedirs(d, exist_ok=True)
    for name, fn in figs.items():
        with open(os.path.join(d, name), 'w', encoding='utf-8') as f:
            f.write(fn())


if __name__ == '__main__':
    write_all(LICH_SU_FIGS, 'lichsu7')
    write_all(GEO_FIGS, 'diali7')
    print('ok', len(LICH_SU_FIGS))
