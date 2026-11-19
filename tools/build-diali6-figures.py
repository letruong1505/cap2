# Địa lí 6: sơ đồ minh họa lý thuyết (không theo tỉ lệ thật).
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *
from figlib2 import H, pt

NAVY = '#1a56a0'
ATTACH, FIGS = [], {}


def reg(name, fn, rel, after, cap):
    FIGS[name] = fn
    ATTACH.append((rel, after, name, cap))


def ELLARC(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


# ---- Bài 1 ----
def f_kinh_vi():
    b = [title(720, 'Kinh tuyến, vĩ tuyến và các bán cầu trên quả Địa Cầu')]
    cx, cy, r = 220, 190, 120
    b.append(C(cx, cy, r, fill='#e8f1fa', stroke=INK, w=2.4))
    for lat in (-60, -30, 0, 30, 60):
        y = cy - r * math.sin(math.radians(lat)); rx = r * math.cos(math.radians(lat))
        b.append(PL(ELLARC(cx, y, rx, rx * 0.22, 0, 180), stroke=RED if lat == 0 else GREY, w=2.4 if lat == 0 else 1.2))
        b.append(PL(ELLARC(cx, y, rx, rx * 0.22, 180, 360), stroke=RED if lat == 0 else '#cbd2d9', w=2.4 if lat == 0 else 1, dash=None if lat == 0 else '3 3'))
    for lon in (-60, -30, 0, 30, 60):
        rx = abs(r * math.sin(math.radians(lon)))
        if lon == 0:
            b.append(L(cx, cy - r, cx, cy + r, stroke=BLUE, w=2.6))
        else:
            b.append(PL(ELLARC(cx, cy, rx, r, -90, 90) if lon > 0 else ELLARC(cx, cy, rx, r, 90, 270), stroke=GREY, w=1.2))
    b.append(dot(cx, cy - r, 4)); b.append(dot(cx, cy + r, 4))
    b.append(T(cx, cy - r - 10, 'Cực Bắc', size=13, weight='bold')); b.append(T(cx, cy + r + 20, 'Cực Nam', size=13, weight='bold'))
    b.append(L(cx + r + 10, cy + 4, cx + r + 60, cy + 4, stroke=RED, w=1.4)); b.append(T(cx + r + 66, cy + 9, 'Xích đạo (vĩ tuyến gốc 0°)', size=13, anchor='start', fill=RED, weight='bold'))
    b.append(L(cx + 2, cy - 90, cx + r + 10, cy - 100, stroke=BLUE, w=1.4)); b.append(T(cx + r + 16, cy - 96, 'Kinh tuyến gốc 0°', size=13, anchor='start', fill=BLUE, weight='bold'))
    b.append(TL(cx + r + 66, cy + 50, ['Bán cầu Bắc ↑ , bán cầu Nam ↓ (chia bởi Xích đạo)', 'Bán cầu Đông và bán cầu Tây', '(chia bởi kinh tuyến 0° và 180°)'], size=12.5, lh=18, anchor='start', fill='#3b4856'))
    b.append(T(cx + r + 66, 340, 'Kinh độ + vĩ độ = toạ độ địa lí', size=13, anchor='start', weight='bold', fill=NAVY))
    return svg(720, 372, ''.join(b))


reg('d6-b1-kinh-vi.svg', f_kinh_vi, 'diali6/bai-1/kinh-vi-tuyen-toa-do.json', 1, 'Kinh tuyến, vĩ tuyến, Xích đạo (sơ đồ)')


# ---- Bài 2: la bàn ----
def f_la_ban():
    b = [title(720, 'Tám hướng chính trên bản đồ')]
    cx, cy, r = 360, 190, 100
    b.append(C(cx, cy, r + 20, fill='#f6f9fc', stroke=GREY, w=1.5))
    dirs = [('Bắc', 0), ('Đông Bắc', 45), ('Đông', 90), ('Đông Nam', 135), ('Nam', 180), ('Tây Nam', 225), ('Tây', 270), ('Tây Bắc', 315)]
    for nm, a in dirs:
        ar = math.radians(a - 90)
        x2, y2 = cx + r * math.cos(ar), cy + r * math.sin(ar)
        main = a % 90 == 0
        b.append(L(cx, cy, x2, y2, stroke=RED if a == 0 else INK, w=3 if main else 1.8, arrow=main))
        tx, ty = cx + (r + 38) * math.cos(ar), cy + (r + 38) * math.sin(ar)
        b.append(T(tx, ty + 5, nm, size=14 if main else 12.5, weight='bold' if main else 'normal', fill=RED if a == 0 else INK))
    b.append(dot(cx, cy, 5))
    b.append(T(360, 360, 'Trên bản đồ có lưới: đầu trên kinh tuyến chỉ hướng bắc, bên phải vĩ tuyến là hướng đông', size=12.5, fill='#3b4856'))
    return svg(720, 380, ''.join(b))


reg('d6-b2-tam-huong.svg', f_la_ban, 'diali6/bai-2/ban-do-phuong-huong.json', 3, 'Tám hướng chính')


# ---- Bài 3: thước tỉ lệ ----
def f_ti_le():
    b = [title(720, 'Tỉ lệ bản đồ 1 : 100 000')]
    x0, y0, u = 120, 100, 160
    for i in range(2):
        b.append(R(x0 + i * u, y0, u, 20, fill='white' if i % 2 else '#444', stroke=INK, sw=1.8))
    for i, t in enumerate(('0', '1 cm', '2 cm')):
        b.append(L(x0 + i * u, y0 + 20, x0 + i * u, y0 + 30, w=1.6)); b.append(T(x0 + i * u, y0 + 48, t, size=13, weight='bold'))
    b.append(T(360, 74, 'Trên bản đồ', size=13, fill=GREY))
    b.append(L(x0, 200, x0 + 2 * u, 200, w=2, stroke=NAVY))
    for i, t in enumerate(('0', '1 km', '2 km')):
        b.append(L(x0 + i * u, 194, x0 + i * u, 206, w=2, stroke=NAVY)); b.append(T(x0 + i * u, 226, t, size=13, weight='bold', fill=NAVY))
    b.append(T(360, 176, 'Ngoài thực tế', size=13, fill=GREY))
    b.append(T(360, 266, '1 cm trên bản đồ ứng với 100 000 cm = 1 km ngoài thực tế', size=14, weight='bold', fill=NAVY))
    b.append(T(360, 290, 'Khoảng cách thực tế = khoảng cách trên bản đồ × mẫu số tỉ lệ', size=12.5, fill='#3b4856'))
    return svg(720, 312, ''.join(b))


reg('d6-b3-ti-le.svg', f_ti_le, 'diali6/bai-3/ti-le-ban-do.json', 1, 'Thước tỉ lệ 1 : 100 000')


# ---- Bài 6: Hệ Mặt Trời ----
def f_he_mat_troi():
    b = [title(720, 'Hệ Mặt Trời: tám hành tinh theo thứ tự xa dần Mặt Trời')]
    b.append(C(-10, 150, 80, fill='#f6c445', stroke='#d9a100', w=2)); b.append(T(46, 255, 'Mặt Trời', size=12, weight='bold'))
    pl = [('Thuỷ tinh', 8, '#9a9a9a'), ('Kim tinh', 13, '#e5c07b'), ('Trái Đất', 14, '#3b82c4'), ('Hoả tinh', 10, '#c8553d'), ('Mộc tinh', 34, '#d9a066'), ('Thổ tinh', 29, '#e1c68c'), ('Thiên Vương tinh', 20, '#9fd3d8'), ('Hải Vương tinh', 20, '#4a6fd1')]
    for i, (nm, r, col) in enumerate(pl):
        x = 120 + i * 80
        b.append(C(x, 150, r, fill=col, stroke=INK, w=1.6))
        if nm == 'Thổ tinh': b.append(PL(ELLARC(x, 150, r + 12, 6, 0, 360), stroke=INK, w=1.2))
        b.append(T(x, 150 + 46 if r < 25 else 150 + 52, str(i + 1), size=15, weight='bold', fill=RED if nm == 'Trái Đất' else INK))
        b.append(TL(x, 150 + 70, nm.replace(' tinh', '\ntinh').split('\n') if len(nm) > 9 else [nm], size=11, lh=13, weight='bold' if nm == 'Trái Đất' else 'normal'))
    b.append(T(360, 290, 'Trái Đất là hành tinh thứ ba, cách Mặt Trời khoảng 150 triệu km', size=13, weight='bold', fill=NAVY))
    b.append(T(360, 312, '(kích thước và khoảng cách không theo tỉ lệ)', size=11.5, fill=GREY))
    return svg(720, 330, ''.join(b))


reg('d6-b6-he-mat-troi.svg', f_he_mat_troi, 'diali6/bai-6/trai-dat-trong-he-mat-troi.json', 0, 'Hệ Mặt Trời (sơ đồ không theo tỉ lệ)')


# ---- Bài 7: tự quay ----
def f_tu_quay():
    b = [title(720, 'Trái Đất tự quay quanh trục: ngày và đêm')]
    cx, cy, r = 400, 170, 100
    for k in range(5):
        b.append(L(60, 90 + k * 40, cx - r - 20, 90 + k * 40, stroke='#f0b400', w=2.4, arrow=True))
    b.append(C(60, 170, 0.1)); b.append(T(120, 70, 'Ánh sáng Mặt Trời', size=13, weight='bold', fill='#b07d00'))
    b.append(C(cx, cy, r, fill='#2f3b52', stroke=INK, w=2.4))
    b.append(PATH('M %.1f %.1f A %d %d 0 0 0 %.1f %.1f Z' % (cx, cy - r, r, r, cx, cy + r), fill='#cfe6fb', stroke=INK, w=2.4))
    t = math.radians(23.5)
    b.append(L(cx + 135 * math.sin(t) * 1.0 * -1 + 0, cy - 135 * math.cos(t), cx - 135 * math.sin(t) * -1, cy + 135 * math.cos(t), stroke=RED, w=3) if False else '')
    ax, ay = 140 * math.sin(t), 140 * math.cos(t)
    b.append(L(cx - ax, cy + ay, cx + ax, cy - ay, stroke=RED, w=3))
    b.append(T(cx + ax + 14, cy - ay - 4, 'Bắc', size=13, weight='bold', fill=RED)); b.append(T(cx - ax - 4, cy + ay + 18, 'Nam', size=13, weight='bold', fill=RED))
    b.append(T(cx - 50, cy + 6, 'NGÀY', size=15, weight='bold')); b.append(T(cx + 50, cy + 6, 'ĐÊM', size=15, weight='bold', fill='white'))
    b.append(PATH('M %.1f %.1f A 130 40 0 0 1 %.1f %.1f' % (cx - 100, cy + 108, cx + 100, cy + 108), stroke=NAVY, w=2.4))
    b.append(T(cx, cy + 176, 'quay từ tây sang đông, 24 giờ một vòng', size=12.5, fill=NAVY, weight='bold'))
    b.append(TL(545, 110, ['Trục nghiêng 66°33′', 'so với mặt phẳng', 'quỹ đạo'], size=12.5, lh=18, anchor='start', fill=RED, weight='bold'))
    b.append(TL(545, 200, ['24 khu vực giờ,', 'mỗi khu vực rộng 15°', 'kinh tuyến;', 'Việt Nam thuộc', 'khu vực giờ số 7'], size=12.5, lh=18, anchor='start', fill='#3b4856'))
    return svg(720, 366, ''.join(b))


reg('d6-b7-tu-quay.svg', f_tu_quay, 'diali6/bai-7/tu-quay-quanh-truc.json', 1, 'Trái Đất tự quay, ngày đêm (sơ đồ)')


# ---- Bài 8: các mùa ----
def f_bon_mua():
    b = [title(720, 'Trái Đất quay quanh Mặt Trời: trục nghiêng không đổi hướng')]
    cx, cy = 360, 180
    b.append(C(cx, cy, 36, fill='#f6c445', stroke='#d9a100', w=2)); b.append(T(cx, cy + 5, 'Mặt Trời', size=12, weight='bold'))
    b.append(PL(ELLARC(cx, cy, 250, 110, 0, 360), stroke=GREY, w=1.6, dash='5 4'))
    pos = [(cx - 250, cy, '22/6', 'Hạ chí', 'Bắc bán cầu ngả về Mặt Trời: mùa nóng'), (cx, cy + 110, '23/9', 'Thu phân', ''), (cx + 250, cy, '22/12', 'Đông chí', 'Bắc bán cầu xa Mặt Trời: mùa lạnh'), (cx, cy - 110, '21/3', 'Xuân phân', '')]
    t = math.radians(23.5)
    for x, y, d, nm, note in pos:
        b.append(C(x, y, 20, fill='#8fc1ee', stroke=INK, w=2))
        ax, ay = 34 * math.sin(t), 34 * math.cos(t)
        b.append(L(x - ax, y + ay, x + ax, y - ay, stroke=RED, w=2.4))
        b.append(T(x + ax + 4, y - ay - 2, 'B', size=11, weight='bold', fill=RED, anchor='start'))
    b.append(TL(cx - 250, cy + 50, ['22/6 – Hạ chí', 'Bắc bán cầu: mùa nóng'], size=12, lh=16, weight='bold')); b.append(TL(cx + 250, cy + 50, ['22/12 – Đông chí', 'Bắc bán cầu: mùa lạnh'], size=12, lh=16, weight='bold'))
    b.append(TL(cx + 70, cy + 128, ['23/9 – Thu phân'], size=12.5, lh=16, weight='bold')); b.append(TL(cx + 70, cy - 98, ['21/3 – Xuân phân'], size=12.5, lh=16, weight='bold'))
    b.append(T(360, 340, 'Quỹ đạo hình elip gần tròn, từ tây sang đông, 365 ngày 6 giờ; trục nghiêng 66°33′ luôn giữ nguyên hướng', size=12, fill='#3b4856'))
    return svg(720, 358, ''.join(b))


reg('d6-b8-bon-mua.svg', f_bon_mua, 'diali6/bai-8/quanh-mat-troi.json', 1, 'Trái Đất trên quỹ đạo và các mùa (sơ đồ, Bắc bán cầu)')


# ---- Bài 10: cấu tạo Trái Đất ----
def f_cau_tao():
    b = [title(720, 'Cấu tạo bên trong của Trái Đất (không theo tỉ lệ)')]
    cx, cy = 190, 180
    layers = [(140, '#c9a27a'), (125, '#e98a3c'), (80, '#f2c14e'), (38, '#f7e08a')]
    for r, col in layers:
        b.append(C(cx, cy, r, fill=col, stroke=INK, w=1.8))
    leads = [('Vỏ Trái Đất: dày 5–70 km, rắn chắc', cx + 90, cy - 96, 390, 90), ('Man-ti: dày khoảng 2 900 km, quánh dẻo đến rắn', cx + 70, cy - 70, 390, 140), ('Nhân ngoài: lỏng', cx + 60, cy - 8, 390, 190), ('Nhân trong: rắn, khoảng 5 000 °C', cx + 25, cy + 8, 390, 240)]
    for txt, x, y, tx, ty in leads:
        b.append(L(x, y, tx - 8, ty, stroke=GREY, w=1.3)); b.append(dot(x, y, 3)); b.append(T(tx, ty + 5, txt, size=12.5, anchor='start', weight='bold'))
    b.append(T(390, 290, 'Nhân (cả hai lớp) dày khoảng 3 400 km', size=12.5, anchor='start', fill=NAVY))
    return svg(720, 340, ''.join(b))


reg('d6-b10-cau-tao.svg', f_cau_tao, 'diali6/bai-10/cau-tao-trai-dat.json', 0, 'Cấu tạo bên trong Trái Đất (không theo tỉ lệ)')


# ---- Bài 12: núi lửa ----
def f_nui_lua():
    b = [title(720, 'Cấu tạo núi lửa')]
    b.append(R(40, 250, 640, 80, fill='#b98a5e', stroke=INK, sw=1.5))
    b.append(POLY([(160, 250), (300, 110), (420, 110), (560, 250)], fill='#a77a52', stroke=INK, sw=2.2))
    b.append(POLY([(305, 110), (330, 100), (390, 100), (415, 110), (400, 116), (320, 116)], fill='#e0452b', stroke=INK, sw=1.8))
    b.append(POLY([(335, 116), (385, 116), (395, 250), (325, 250)], fill='#f08a2a', stroke=INK, sw=1))
    b.append(PATH('M 260 280 Q 360 240 470 280 Q 460 330 360 330 Q 260 330 260 280 Z', fill='#e0452b', stroke=INK, w=2))
    for x, y in ((345, 88), (365, 70), (385, 90), (370, 52)):
        b.append(C(x, y, 14, fill='#bdbdbd', stroke='none'))
    for tx, ty, x, y, txt in ((560, 70, 405, 104, 'Miệng núi lửa'), (560, 160, 365, 190, 'Ống phun'), (560, 290, 440, 290, 'Lò mac-ma')):
        b.append(L(x, y, tx - 6, ty, stroke=GREY, w=1.3)); b.append(dot(x, y, 3)); b.append(T(tx, ty + 5, txt, size=14, anchor='start', weight='bold'))
    return svg(720, 350, ''.join(b))


reg('d6-b12-nui-lua.svg', f_nui_lua, 'diali6/bai-12/nui-lua-dong-dat.json', 0, 'Cấu tạo núi lửa (sơ đồ)')


# ---- Bài 15: khí quyển ----
def f_khi_quyen():
    b = [title(720, 'Các tầng khí quyển và thành phần không khí')]
    b.append(R(60, 50, 180, 70, fill='#1d2a44', stroke=INK, sw=1.6)); b.append(T(150, 90, 'Các tầng cao', size=13, weight='bold', fill='white'))
    b.append(R(60, 120, 180, 110, fill='#6e92c7', stroke=INK, sw=1.6)); b.append(TL(150, 168, ['Tầng bình lưu', '16–80 km', '(có lớp ô-dôn)'], size=12.5, lh=18, fill='white', weight='bold'))
    b.append(R(60, 230, 180, 56, fill='#cfe6fb', stroke=INK, sw=1.6)); b.append(TL(150, 252, ['Tầng đối lưu', '0–16 km'], size=12.5, lh=18, weight='bold'))
    b.append(T(300, 262, '← tập trung khoảng 90% không khí,', size=12.5, anchor='start', fill='#3b4856')); b.append(T(300, 282, 'nơi sinh ra các hiện tượng thời tiết', size=12.5, anchor='start', fill='#3b4856'))
    # thành phần
    x0, y0, w = 330, 90, 340
    segs = [(78, '#4e79a7', 'Nitơ 78%'), (21, '#e9a23b', 'Oxy 21%'), (1, '#8e6fc4', '')]
    x = x0
    for v, col, t in segs:
        ww = w * v / 100
        b.append(R(x, y0, ww, 30, fill=col, stroke=INK, sw=1.4))
        if t: b.append(T(x + ww / 2, y0 + 21, t, size=13, weight='bold', fill='white'))
        x += ww
    b.append(L(x0 + w - 1, y0 + 30, x0 + w - 1, y0 + 56, stroke=GREY, w=1.2)); b.append(T(x0 + w, y0 + 70, 'Hơi nước và khí khác 1%', size=12.5, anchor='end', weight='bold'))
    b.append(T(x0 + w / 2, y0 - 12, 'Thành phần không khí', size=13, weight='bold'))
    return svg(720, 310, ''.join(b))


reg('d6-b15-khi-quyen.svg', f_khi_quyen, 'diali6/bai-15/vo-khi-khi-ap-gio.json', 0, 'Tầng khí quyển và thành phần không khí')


# ---- Bài 19 ----
def f_thuy_quyen():
    b = [title(720, 'Thuỷ quyển: nước mặn và nước ngọt')]
    def bar(y, parts, lab):
        b.append(T(30, y - 10, lab, size=13, weight='bold', anchor='start'))
        x = 30; W_ = 660
        for v, col, t in parts:
            ww = W_ * v / 100
            b.append(R(x, y, ww, 34, fill=col, stroke=INK, sw=1.4))
            if ww > 120: b.append(T(x + ww / 2, y + 22, t, size=13, weight='bold', fill='white'))
            x += ww
    bar(70, [(97.5, '#3b82c4', 'Nước biển và đại dương ≈ 97,5%'), (2.5, '#e9a23b', '')], 'Toàn bộ nước trên Trái Đất')
    b.append(T(690, 126, '≈ 2,5% nước ngọt', size=12.5, anchor='end', fill='#b07d00', weight='bold'))
    bar(180, [(68.7, '#8fc1ee', 'Băng ≈ 68,7%'), (30.1, '#4a8f5f', 'Nước ngầm ≈ 30,1%'), (1.2, '#c8553d', '')], 'Trong nước ngọt')
    b.append(T(690, 236, 'Nước mặt và nước khác ≈ 1,2%', size=12.5, anchor='end', fill='#c8553d', weight='bold'))
    return svg(720, 260, ''.join(b))


reg('d6-b19-thuy-quyen.svg', f_thuy_quyen, 'diali6/bai-19/thuy-quyen-tuan-hoan-nuoc.json', 1, 'Tỉ lệ nước mặn, nước ngọt (sơ đồ)')


def f_tuan_hoan():
    b = [title(720, 'Vòng tuần hoàn lớn của nước')]
    b.append(R(20, 260, 300, 70, fill='#3b82c4', stroke=INK, sw=1.6)); b.append(T(170, 300, 'Biển, đại dương', size=14, weight='bold', fill='white'))
    b.append(POLY([(320, 260), (420, 130), (500, 130), (560, 260)], fill='#9b8062', stroke=INK, sw=1.8))
    b.append(R(320, 260, 380, 70, fill='#b98a5e', stroke=INK, sw=1.4)); b.append(T(560, 300, 'Đất liền (nước ngầm)', size=13, weight='bold', fill='white'))
    for (x, y) in ((400, 60), (440, 50), (480, 60), (440, 72)):
        b.append(C(x, y, 22, fill='#e6eef5', stroke=GREY, w=1.4))
    b.append(L(110, 255, 110, 140, stroke=ORANGE, w=2.6, arrow=True)); b.append(T(66, 200, 'Bốc hơi', size=13, weight='bold', fill=ORANGE, anchor='middle'))
    b.append(L(130, 130, 380, 90, stroke=GREY, w=2.4, arrow=True)); b.append(T(255, 98, 'Gió đưa hơi nước vào đất liền', size=12, fill='#3b4856'))
    b.append(L(450, 90, 450, 150, stroke=BLUE, w=2.6, arrow=True)); b.append(T(520, 126, 'Ngưng tụ, gây mưa', size=13, weight='bold', fill=BLUE, anchor='start'))
    b.append(L(470, 170, 400, 255, stroke=BLUE, w=2.4, arrow=True)); b.append(T(350, 206, 'Dòng chảy mặt', size=12.5, anchor='end', fill=BLUE, weight='bold'))
    b.append(L(540, 262, 540, 300, stroke=BLUE, w=2, arrow=True)) if False else None
    b.append(L(400, 268, 330, 268, stroke=BLUE, w=2.4, arrow=True)); b.append(T(560, 245, 'Nước ngầm (ngấm xuống)', size=12, fill=BLUE, anchor='start'))
    b.append(T(360, 352, 'Nước đổ về biển, tiếp tục chu trình', size=12.5, fill='#3b4856', weight='bold'))
    return svg(720, 372, ''.join(b))


reg('d6-b19-tuan-hoan.svg', f_tuan_hoan, 'diali6/bai-19/thuy-quyen-tuan-hoan-nuoc.json', 3, 'Vòng tuần hoàn lớn của nước (sơ đồ)')


if __name__ == '__main__':
    import glob
    write_figs('diali6', FIGS)
    for rel, after, name, cap in ATTACH:
        subj, path = rel.split('/', 1)
        hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', path))
        assert hits, rel
        attach(subj, os.path.relpath(hits[0], os.path.join(ROOT, 'content', subj)), after, name, cap)
    print('diali6: %d hình' % len(FIGS))
