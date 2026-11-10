# Hình lý thuyết Địa lí 7, 8, 9: biểu đồ cơ cấu, mặt cắt, sơ đồ, bảng. Chỉ dùng số liệu có trong bài; không vẽ bản đồ.
import sys, os, math, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

NAVY = '#1a56a0'
PAL = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#b07aa1', '#9aa5b1']
SOFT = ['#dbe7f3', '#fde3c4', '#dfe9d5', '#f7d4d4', '#e8dcef', '#eef1f4']


def halo(x, y, s, size=13, fill=INK, anchor='middle', weight='normal'):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s" stroke="white" '
            'stroke-width="3" paint-order="stroke">%s</text>' % (x, y, anchor, size, weight, fill, s))


def stacks(ttl, rows, note=None, W=640):
    """rows: [(nhãn hàng, [(chữ trong ô, giá trị, chỉ số màu)])]"""
    h = 56 + len(rows) * 74 + (24 if note else 0)
    b = [T(W / 2, 24, ttl, size=16, weight='bold')]
    x0, x1 = 30, W - 30
    for k, (rl, parts) in enumerate(rows):
        y = 56 + k * 74
        b.append(T(x0, y - 6, rl, size=13, anchor='start', weight='bold'))
        tot = sum(v for _, v, _ in parts)
        x = x0
        for s, v, ci in parts:
            w = (x1 - x0) * v / tot
            b.append(R(x, y, w, 38, fill=SOFT[ci], stroke=PAL[ci], sw=2))
            if '\n' in s:
                b.append(TL(x + w / 2, y + 17, s.split('\n'), size=12.5, weight='bold', fill=INK, lh=15))
            else:
                b.append(T(x + w / 2, y + 24, s, size=13, weight='bold', fill=INK))
            x += w
    if note:
        b.append(T(W / 2, h - 8, note, size=12, fill='#55606d'))
    return svg(W, h, ''.join(b))


def pie(ttl, parts, W=660, H=300):
    cx, cy, r = 160, 160, 100
    b = [T(W / 2, 24, ttl, size=16, weight='bold')]
    tot = sum(v for _, v, _ in parts)
    a = -math.pi / 2
    for k, (s, v, ci) in enumerate(parts):
        a2 = a + 2 * math.pi * v / tot
        x1, y1, x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a), cx + r * math.cos(a2), cy + r * math.sin(a2)
        big = 1 if a2 - a > math.pi else 0
        b.append(PATH('M%.1f,%.1f L%.1f,%.1f A%d,%d 0 %d 1 %.1f,%.1f Z' % (cx, cy, x1, y1, r, r, big, x2, y2), fill=PAL[ci], stroke='white', w=2))
        m = (a + a2) / 2
        if v < 8:
            b.append(T(cx + 1.2 * r * math.cos(m), cy + 1.2 * r * math.sin(m) + 5, '%g%%' % v, size=15, weight='bold', fill=INK))
        else:
            b.append(T(cx + 0.62 * r * math.cos(m), cy + 0.62 * r * math.sin(m) + 5, '%g%%' % v, size=15, weight='bold', fill='white'))
        a = a2
    for k, (s, v, ci) in enumerate(parts):
        y = 90 + k * 56
        b.append(R(330, y - 14, 20, 20, fill=PAL[ci], stroke=PAL[ci]))
        b.append(T(360, y + 2, s[0], size=14, anchor='start', weight='bold'))
        b.append(T(360, y + 20, s[1], size=12, anchor='start', fill='#55606d'))
    return svg(W, H, ''.join(b))


def vbars(ttl, data, ymax, step, unit, fmt='%g', W=420, H=290):
    ml, mb, mt = 60, 46, 64
    fy = lambda v: H - mb - v / ymax * (H - mb - mt)
    b = [T(W / 2, 24, ttl, size=15, weight='bold')]
    b.append(L(ml, H - mb, W - 20, H - mb, arrow=False)); b.append(L(ml, H - mb, ml, mt - 8, arrow=True))
    v = 0
    while v <= ymax + 1e-9:
        b.append(L(ml - 5, fy(v), ml, fy(v), w=1.5)); b.append(T(ml - 8, fy(v) + 4, fmt % v, size=12, anchor='end'))
        if v: b.append(L(ml, fy(v), W - 20, fy(v), stroke='#e6ebf0', w=1))
        v += step
    b.append(T(ml + 6, mt - 14, unit, size=13, anchor='start'))
    n = len(data); bw = 70; gap = (W - ml - 20 - n * bw) / (n + 1)
    for k, (s, val, ci) in enumerate(data):
        x = ml + gap + k * (bw + gap)
        b.append(R(x, fy(val), bw, H - mb - fy(val), fill=PAL[ci], stroke=PAL[ci]))
        b.append(T(x + bw / 2, fy(val) - 6, ('%g' % val).replace('.', ','), size=14, weight='bold'))
        b.append(T(x + bw / 2, H - mb + 20, s, size=13))
    return svg(W, H, ''.join(b))


def hbars(ttl, data, vmax, unit, W=560):
    H = 60 + len(data) * 52
    x0 = 250
    b = [T(W / 2, 24, ttl, size=15, weight='bold')]
    for k, (s, val, ci) in enumerate(data):
        y = 50 + k * 52
        w = (W - x0 - 150) * val / vmax
        b.append(T(x0 - 10, y + 24, s, size=13, anchor='end'))
        b.append(R(x0, y + 6, w, 28, fill=PAL[ci], stroke=PAL[ci]))
        b.append(T(x0 + w + 8, y + 26, ('%g' % val).replace('.', ',') + ' ' + unit, size=13, anchor='start', weight='bold'))
    return svg(W, H, ''.join(b))


def table(ttl, head, rows, widths, W=660):
    H = 56 + 34 + len(rows) * 34 + 10
    b = [T(W / 2, 24, ttl, size=16, weight='bold')]
    x = 20
    xs = []
    for w in widths:
        xs.append(x); x += w
    xr = x
    y = 44
    b.append(R(20, y, xr - 20, 34, fill=LBLUE, stroke=INK, sw=1.5))
    for xx, h in zip(xs, head):
        b.append(T(xx + 10, y + 22, h, size=14, anchor='start', weight='bold'))
    for k, row in enumerate(rows):
        yy = y + 34 + k * 34
        b.append(R(20, yy, xr - 20, 34, fill='white' if k % 2 else LGREY, stroke=GREY, sw=1))
        for xx, c in zip(xs, row):
            b.append(T(xx + 10, yy + 22, c, size=13, anchor='start'))
    for xx in xs[1:]:
        b.append(L(xx, y, xx, y + 34 + len(rows) * 34, stroke=GREY, w=1))
    return svg(W, H, ''.join(b))


# ---------- Địa 8 ----------
def toa_do():
    W, H = 600, 356
    b = [T(W / 2, 24, 'Bốn điểm cực của phần đất liền Việt Nam', size=16, weight='bold')]
    cx, cy = W / 2, 178
    b.append(C(cx, cy, 52, fill=LGREEN, stroke=GREEN, w=2))
    b.append(TL(cx, cy - 4, ['Phần đất', 'liền'], size=14, weight='bold'))
    cards = [(cx, 70, 'Cực Bắc', '23°23′B', 'Lũng Cú (Hà Giang)', cx, cy - 52, cx, 98),
             (cx, 288, 'Cực Nam', '8°34′B', 'Đất Mũi (Cà Mau)', cx, cy + 52, cx, 260),
             (100, cy, 'Cực Tây', '102°09′Đ', 'Sín Thầu (Điện Biên)', cx - 52, cy, 188, cy),
             (500, cy, 'Cực Đông', '109°28′Đ', 'Vạn Thạnh (Khánh Hoà)', cx + 52, cy, 412, cy)]
    for x, y, a, c, p, x1, y1, x2, y2 in cards:
        b.append(L(x1, y1, x2, y2, stroke=GREY, w=2))
        b.append(R(x - 88, y - 28, 176, 56, fill=LYELLOW, stroke=ORANGE, sw=2, rx=6))
        b.append(T(x, y - 8, a + ': ' + c, size=14, weight='bold', fill=NAVY))
        b.append(T(x, y + 14, p, size=12.5))
    b.append(T(W / 2, H - 6, 'Sơ đồ minh họa vị trí tương đối, không phải bản đồ', size=11, fill='#55606d'))
    return svg(W, H, ''.join(b))


def dia_hinh8():
    return stacks('Địa hình Việt Nam', [
        ('Theo diện tích', [('Đồi núi ≈ 3/4 diện tích', 75, 2), ('Đồng bằng ≈ 1/4', 25, 0)]),
        ('Theo độ cao', [('Dưới 1 000 m ≈ 85%', 85, 2), ('Từ 1 000 m\ntrở lên ≈ 15%', 15, 1)])],
        note='Trong đó núi cao trên 2 000 m chỉ chiếm khoảng 1% diện tích lãnh thổ.')


def gio_mua():
    W, H = 640, 250
    b = [T(W / 2, 24, 'Hai mùa gió chính ở nước ta theo tháng', size=16, weight='bold')]
    x0, cw = 40, 46
    for m in range(1, 13):
        x = x0 + (m - 1) * cw
        b.append(R(x, 56, cw, 28, fill=LGREY, stroke=GREY, sw=1)); b.append(T(x + cw / 2, 75, str(m), size=13, weight='bold'))
    b.append(T(x0, 50, 'Tháng', size=12, anchor='start', fill='#55606d'))
    # gió mùa Đông Bắc: tháng 11-12 và 1-4
    for rng in ((1, 4), (11, 12)):
        xa, xb = x0 + (rng[0] - 1) * cw, x0 + rng[1] * cw
        b.append(R(xa, 100, xb - xa, 34, fill='#cfe3f5', stroke=BLUE, sw=2))
    b.append(T(x0 + 2 * cw, 122, 'ĐB', size=14, weight='bold', fill=NAVY)); b.append(T(x0 + 11 * cw, 122, 'ĐB', size=14, weight='bold', fill=NAVY))
    xa, xb = x0 + 4 * cw, x0 + 10 * cw
    b.append(R(xa, 150, xb - xa, 34, fill='#fde3c4', stroke=ORANGE, sw=2)); b.append(T((xa + xb) / 2, 172, 'TN', size=14, weight='bold', fill='#a8570a'))
    b.append(TL(W / 2, 208, ['Gió mùa Đông Bắc (tháng 11 – 4): làm miền Bắc lạnh.', 'Gió mùa Tây Nam (tháng 5 – 10): gây mưa lớn cho cả nước.'], size=13, lh=20))
    return svg(W, H, ''.join(b))


def thuy_van():
    return stacks('Sông ngòi và chế độ nước ở Việt Nam', [
        ('Trong 2 360 con sông dài trên 10 km', [('Sông nhỏ, ngắn: 93%', 93, 0), ('7%', 7, 5)]),
        ('Lượng nước cả năm', [('Mùa lũ: 70%', 70, 0), ('→ 80%', 10, 1), ('Mùa cạn\n20 – 30%', 20, 5)])],
        note='Mùa lũ chiếm từ 70% đến 80% lượng nước cả năm; phần còn lại là mùa cạn.')


def tho_nhuong():
    return pie('Ba nhóm đất chính ở Việt Nam (khoảng)', [
        (('Đất feralit', 'Đồi núi thấp, chua, nghèo mùn'), 65, 0),
        (('Đất phù sa', 'Đồng bằng, màu mỡ (lúa, hoa màu)'), 24, 2),
        (('Đất mùn núi cao', 'Trên 1 600 – 1 700 m, rừng đầu nguồn'), 11, 1)])


def khoang_san():
    return table('Khoáng sản chính và nơi phân bố', ['Khoáng sản', 'Nơi phân bố'], [
        ['Than đá', 'Quảng Ninh'],
        ['Dầu mỏ, khí tự nhiên', 'Thềm lục địa phía nam (bể Cửu Long, Nam Côn Sơn)'],
        ['Bô-xít', 'Tây Nguyên'],
        ['Sắt', 'Thái Nguyên, Hà Tĩnh'],
        ['A-pa-tít', 'Lào Cai'],
        ['Đá vôi', 'Miền Bắc, Bắc Trung Bộ'],
        ['Titan', 'Ven biển miền Trung']], [200, 420])


def vung_bien():
    W, H = 740, 330
    b = [T(W / 2, 22, 'Các vùng biển của Việt Nam (mặt cắt sơ đồ)', size=16, weight='bold')]
    yS = 150
    # nước, đất, đáy biển
    b.append(R(80, yS, 620, 110, fill=LBLUE, stroke='none', sw=0))
    b.append(POLY([(10, 116), (60, 116), (80, yS), (80, 262), (10, 262)], fill=LGREEN, stroke=GREEN, sw=2))
    b.append(POLY([(80, yS), (150, 172), (300, 196), (520, 210), (570, 240), (700, 248), (700, 262), (80, 262)], fill=LYELLOW, stroke=ORANGE, sw=2))
    b.append(L(80, yS, 700, yS, stroke=BLUE, w=2.5))
    b.append(T(40, 100, 'Đất liền', size=13, weight='bold'))
    xs = {'bờ': 80, 'cơ sở': 150, '12': 270, '24': 390, '200': 650}
    for k in ('cơ sở', '12', '24', '200'):
        b.append(L(xs[k], 84, xs[k], 262, stroke=GREY, w=1.5, dash='5 4'))
    b.append(L(80, 84, 80, yS, stroke=GREY, w=1.5, dash='5 4'))
    boxes = [(80, 150, 'Nội thuỷ', ['']), (150, 270, 'Lãnh hải', ['12 hải lí']), (270, 390, 'Tiếp giáp lãnh hải', ['12 hải lí tiếp theo'])]
    for xa, xb, a, c in boxes:
        b.append(R(xa, 88, xb - xa, 44, fill=SOFT[1], stroke=ORANGE, sw=2))
        b.append(T((xa + xb) / 2, 107 if c[0] else 115, a, size=12.5, weight='bold'))
        if c[0]: b.append(T((xa + xb) / 2, 124, c[0], size=12, fill='#55606d'))
    b.append(R(150, 44, 500, 34, fill=SOFT[0], stroke=BLUE, sw=2))
    b.append(T(400, 66, 'Vùng đặc quyền kinh tế: đến 200 hải lí tính từ đường cơ sở', size=13, weight='bold'))
    b.append(halo(370, 238, 'Thềm lục địa', 14, '#8a5a00', 'middle', 'bold'))
    for k, s in (('cơ sở', 'Đường cơ sở'), ('12', '12 hải lí'), ('24', '24 hải lí'), ('200', '200 hải lí')):
        b.append(T(xs[k], 282, s, size=12.5, weight='bold'))
    b.append(T(W / 2, 318, 'Sơ đồ minh họa, không vẽ đúng tỉ lệ (khoảng cách tính từ đường cơ sở)', size=11.5, fill='#55606d'))
    return svg(W, H, ''.join(b))


# ---------- Địa 9 ----------
def dan_toc():
    return stacks('Dân tộc và cơ cấu dân số theo tuổi', [
        ('Dân tộc', [('Kinh ≈ 85%', 85, 0), ('Dân tộc khác\n≈ 15%', 15, 1)]),
        ('Nhóm tuổi', [('15 – 64 tuổi ≈ 2/3', 66.7, 2), ('Dưới 15 và từ 65 tuổi ≈ 1/3', 33.3, 5)])],
        note='Số liệu "khoảng"; phần còn lại tính bù theo tổng 100%.')


def nongthon_thanhthi():
    return stacks('Dân số nông thôn và thành thị (2023)', [
        ('Cả nước', [('Nông thôn ≈ 62%', 62, 2), ('Thành thị ≈ 38%', 38, 0)])],
        note='Tỉ lệ dân thành thị đang tăng.')


def cong_nghiep():
    return table('Một số ngành công nghiệp và địa điểm tiêu biểu', ['Ngành', 'Địa điểm'], [
        ['Khai thác than', 'Quảng Ninh'],
        ['Khai thác dầu khí', 'Bà Rịa – Vũng Tàu (thềm lục địa phía nam)'],
        ['Thuỷ điện', 'Hoà Bình, Sơn La, Lai Châu…'],
        ['Nhiệt điện', 'Phả Lại, Phú Mỹ…'],
        ['Khai thác bô-xít', 'Tây Nguyên'],
        ['Trung tâm công nghiệp lớn', 'Hà Nội, TP Hồ Chí Minh, Hải Phòng, Đà Nẵng…']], [250, 400], W=690)


def dich_vu():
    W, H = 640, 330
    b = [T(W / 2, 24, 'Cơ cấu ngành dịch vụ', size=16, weight='bold')]
    b.append(R(240, 44, 160, 40, fill=LBLUE, stroke=BLUE, sw=2, rx=6)); b.append(T(320, 70, 'Dịch vụ', size=15, weight='bold'))
    xs = [110, 320, 530]
    for x, s in zip(xs, ['Dịch vụ tiêu dùng', 'Dịch vụ sản xuất', 'Dịch vụ công']):
        b.append(PL([(320, 84), (320, 104), (x, 104), (x, 120)], stroke=GREY, w=2))
        b.append(R(x - 80, 120, 160, 40, fill=LYELLOW, stroke=ORANGE, sw=2, rx=6)); b.append(T(x, 146, s, size=13.5, weight='bold'))
    b.append(T(W / 2, 200, 'Giao thông vận tải gồm các loại đường:', size=13.5, weight='bold'))
    chips = ['Đường bộ', 'Đường sắt', 'Đường biển', 'Đường hàng không', 'Đường sông']
    ws = [92, 92, 92, 132, 92]
    gap = 12; tot = sum(ws) + gap * 4; x = (W - tot) / 2
    for s, w in zip(chips, ws):
        b.append(R(x, 214, w, 34, fill=SOFT[2], stroke=GREEN, sw=2, rx=17)); b.append(T(x + w / 2, 236, s, size=12.5)); x += w + gap
    b.append(T(W / 2, 282, 'Hà Nội và Thành phố Hồ Chí Minh là hai trung tâm dịch vụ lớn nhất cả nước.', size=13))
    return svg(W, H, ''.join(b))


def mat_cat_btb():
    W, H = 560, 250
    b = [T(W / 2, 24, 'Mặt cắt Bắc Trung Bộ từ tây sang đông (sơ đồ)', size=15, weight='bold')]
    pts = [(30, 120), (70, 70), (100, 52), (140, 80), (170, 118), (200, 140), (230, 126), (260, 144), (290, 150), (390, 158), (410, 160)]
    ground = pts + [(410, 200), (30, 200)]
    b.append(POLY([(410, 160), (530, 160), (530, 200), (410, 200)], fill=LBLUE, stroke='none', sw=0))
    b.append(POLY(ground, fill=LGREEN, stroke=GREEN, sw=2))
    b.append(POLY([(410, 160), (530, 160), (530, 200), (410, 200)], fill=LBLUE, stroke=BLUE, sw=1.5))
    b.append(L(410, 160, 530, 160, stroke=BLUE, w=2.5))
    for xa, xb, s in ((30, 170, 'Núi (Trường Sơn Bắc)'), (170, 290, 'Gò đồi'), (290, 410, 'Đồng bằng'), (410, 530, 'Biển')):
        b.append(L(xa, 206, xb, 206, stroke=GREY, w=2)); b.append(L(xa, 200, xa, 212, stroke=GREY, w=2)); b.append(L(xb, 200, xb, 212, stroke=GREY, w=2))
        b.append(T((xa + xb) / 2, 226, s, size=13, weight='bold'))
    b.append(T(30, 46, 'Tây', size=13, anchor='start', weight='bold')); b.append(T(530, 46, 'Đông', size=13, anchor='end', weight='bold'))
    return svg(W, H, ''.join(b))


def dien_tich_vung():
    return hbars('Diện tích một số vùng (nghìn km²)', [
        ('Trung du và miền núi phía Bắc', 95, 0), ('Đồng bằng sông Cửu Long', 40.9, 2),
        ('Đông Nam Bộ', 23.5, 1), ('Đồng bằng sông Hồng', 21, 3)], 100, 'nghìn km²', W=640)


# ---------- Địa 7 ----------
def uc_mat_cat():
    W, H = 600, 260
    b = [T(W / 2, 24, 'Mặt cắt địa hình lục địa Ô-xtrây-li-a (sơ đồ, tây → đông)', size=15, weight='bold')]
    pts = [(30, 110), (190, 110), (230, 150), (330, 160), (400, 150), (440, 100), (470, 70), (500, 62), (530, 72), (570, 130)]
    b.append(POLY(pts + [(570, 200), (30, 200)], fill=LYELLOW, stroke=ORANGE, sw=2))
    b.append(halo(110, 140, 'Sơn nguyên', 13, INK, 'middle', 'bold')); b.append(halo(110, 158, 'Tây Ô-xtrây-li-a', 13, INK, 'middle', 'bold'))
    b.append(halo(110, 176, '(nhiều hoang mạc)', 12, '#55606d'))
    b.append(halo(320, 186, 'Đồng bằng Trung Tâm', 13, INK, 'middle', 'bold'))
    b.append(halo(500, 150, 'Dãy Trường Sơn', 13, INK, 'middle', 'bold')); b.append(halo(500, 168, 'Ô-xtrây-li-a', 13, INK, 'middle', 'bold'))
    b.append(T(320, 226, 'Độ cao dưới 200 m', size=12.5, fill=NAVY, weight='bold'))
    b.append(T(500, 226, 'Cao 800 – 1 000 m', size=12.5, fill=NAVY, weight='bold'))
    b.append(T(30, 46, 'Tây', size=13, anchor='start', weight='bold')); b.append(T(570, 46, 'Đông', size=13, anchor='end', weight='bold'))
    b.append(T(W / 2, 250, 'Sơ đồ minh họa, chiều cao không vẽ theo tỉ lệ', size=11, fill='#55606d'))
    return svg(W, H, ''.join(b))


def amazon_ha():
    return vbars('Diện tích rừng ở Bra-xin', [('1970', 4, 2), ('2019', 3.39, 3)], 5, 1, 'triệu km²', '%g')


def a_tang():
    return vbars('Mức tăng dân số 2015 – 2020', [('Châu Á', 0.95, 0), ('Thế giới', 1.09, 5)], 1.2, 0.2, '%/năm', '%.1f')


FIGS = {
    'diali8': {'dl8-toa-do-cuc.svg': toa_do, 'dl8-dia-hinh.svg': dia_hinh8, 'dl8-gio-mua.svg': gio_mua, 'dl8-thuy-van.svg': thuy_van,
               'dl8-tho-nhuong.svg': tho_nhuong, 'dl8-khoang-san.svg': khoang_san, 'dl8-vung-bien.svg': vung_bien},
    'diali9': {'dl9-dan-toc.svg': dan_toc, 'dl9-nong-thon.svg': nongthon_thanhthi, 'dl9-cong-nghiep.svg': cong_nghiep,
               'dl9-dich-vu.svg': dich_vu, 'dl9-bac-trung-bo.svg': mat_cat_btb, 'dl9-dien-tich-vung.svg': dien_tich_vung,
               'dl9-vung-bien.svg': vung_bien},
    'diali7': {'dl7-uc-mat-cat.svg': uc_mat_cat, 'dl7-amazon-giam.svg': amazon_ha, 'dl7-a-tang-dan-so.svg': a_tang},
}

# (môn, bài, chỉ số khối lý thuyết cần chèn sau, tên hình, chú thích)
ATTACH = [
    ('diali8', 1, 1, 'dl8-toa-do-cuc.svg', 'Toạ độ bốn điểm cực phần đất liền'),
    ('diali8', 2, 0, 'dl8-dia-hinh.svg', 'Cơ cấu địa hình Việt Nam'),
    ('diali8', 3, 1, 'dl8-khoang-san.svg', 'Khoáng sản và nơi phân bố'),
    ('diali8', 4, 2, 'dl8-gio-mua.svg', 'Gió mùa theo tháng'),
    ('diali8', 6, 1, 'dl8-thuy-van.svg', 'Sông ngòi và chế độ nước'),
    ('diali8', 9, 1, 'dl8-tho-nhuong.svg', 'Ba nhóm đất chính'),
    ('diali8', 11, 1, 'dl8-vung-bien.svg', 'Các vùng biển của Việt Nam'),
    ('diali9', 1, 0, 'dl9-dan-toc.svg', 'Dân tộc và nhóm tuổi'),
    ('diali9', 2, 1, 'dl9-nong-thon.svg', 'Dân cư nông thôn – thành thị'),
    ('diali9', 8, 2, 'dl9-cong-nghiep.svg', 'Ngành công nghiệp và địa điểm'),
    ('diali9', 10, 0, 'dl9-dich-vu.svg', 'Cơ cấu ngành dịch vụ'),
    ('diali9', 14, 0, 'dl9-bac-trung-bo.svg', 'Mặt cắt Bắc Trung Bộ'),
    ('diali9', 19, 0, 'dl9-dien-tich-vung.svg', 'So sánh diện tích một số vùng (theo các bài 12, 13, 17, 19)'),
    ('diali9', 21, 0, 'dl9-vung-bien.svg', 'Các vùng biển của Việt Nam'),
    ('diali7', 17, 3, 'dl7-amazon-giam.svg', 'Diện tích rừng Bra-xin giảm'),
    ('diali7', 6, 2, 'dl7-a-tang-dan-so.svg', 'Mức tăng dân số châu Á và thế giới'),
    ('diali7', 18, 1, 'dl7-uc-mat-cat.svg', 'Mặt cắt địa hình lục địa Ô-xtrây-li-a'),
]

if __name__ == '__main__':
    for subj, figs in FIGS.items():
        write_figs(subj, figs)
    for subj, bai, after, name, cap in ATTACH:
        hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%d' % bai, '*.json'))
        assert len(hits) == 1, (subj, bai, hits)
        attach(subj, os.path.relpath(hits[0], os.path.join(ROOT, 'content', subj)), after, name, cap)
    print('diali789: %d hình' % sum(len(v) for v in FIGS.values()))
