# Địa lí 6, Địa lí 9, Lịch sử 7, Sinh 7 (đợt 3): sơ đồ, mặt cắt, dòng thời gian, nhóm ý.
# Chỉ dựng từ dữ kiện có trong bài học; sơ đồ minh họa, không phải ảnh hay bản đồ.
import sys, os, json, glob, math, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *


def _load(name, fn):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(__file__), fn))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


su2 = _load('su2', 'build-su2-figures.py')
dl = _load('dl789', 'build-diali789-figures.py')
groups, timeline, flow, wrap = su2.groups, su2.timeline, su2.flow, su2.wrap
HEAD, SOFT = su2.HEAD, su2.SOFT
NAVY = '#1a56a0'


def halo(x, y, s, size=13, fill=INK, anchor='middle', weight='normal'):
    return dl.halo(x, y, s, size, fill, anchor, weight)


def box(x, y, w, h, lines, ci=0, size=13, bold_first=True):
    b = [R(x, y, w, h, fill=SOFT[ci % 4], stroke=HEAD[ci % 4], sw=2, rx=8)]
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * 9 + 5
    for i, s in enumerate(lines):
        b.append(T(x + w / 2, y0 + i * 18, s, size=size, weight='bold' if (i == 0 and bold_first) else 'normal'))
    return ''.join(b)


# ================= Địa lí 6 =================
def ki_hieu():
    W, H = 720, 250
    b = [title(W, 'Ba loại kí hiệu trên bản đồ')]
    cw, gap = 220, 20
    heads = [('Kí hiệu điểm', 'Ví dụ: sân bay, nhà máy'), ('Kí hiệu đường', 'Ví dụ: đường giao thông, ranh giới, sông'),
             ('Kí hiệu diện tích', 'Ví dụ: vùng trồng lúa, rừng')]
    for k, (h, ex) in enumerate(heads):
        x = 14 + k * (cw + gap)
        b.append(R(x, 44, cw, 190, fill=SOFT[k], stroke=HEAD[k], sw=2, rx=8))
        b.append(R(x, 44, cw, 34, fill=HEAD[k], stroke=HEAD[k], sw=2, rx=8)); b.append(T(x + cw / 2, 67, h, size=14, weight='bold', fill='white'))
        cx, cy = x + cw / 2, 140
        if k == 0:
            b.append(C(cx - 50, cy, 12, fill=RED, stroke=INK, w=1.6)); b.append(R(cx + 26, cy - 12, 24, 24, fill=BLUE, stroke=INK, sw=1.6))
        elif k == 1:
            b.append(L(cx - 80, cy + 18, cx + 80, cy + 18, stroke=INK, w=3))
            b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (cx - 80, cy - 14, cx - 40, cy - 40, cx + 10, cy + 10, cx + 80, cy - 16), stroke=BLUE, w=3))
            b.append(L(cx - 80, cy + 2, cx + 80, cy + 2, stroke=GREY, w=2, dash='8 5'))
        else:
            b.append(R(cx - 70, cy - 28, 140, 56, fill='#cfe6c3', stroke=GREEN, sw=2))
            for i in range(-60, 60, 14):
                b.append(L(cx + i, cy + 28, cx + i + 20, cy - 28, stroke=GREEN, w=1.2))
        for i, s in enumerate(wrap(ex, 26)):
            b.append(T(x + cw / 2, 198 + i * 17, s, size=12.5))
    return svg(W, H, ''.join(b))


def phuong_huong():
    W, H = 640, 330
    cx, cy = 320, 175
    b = [title(W, 'Xác định phương hướng bằng Mặt Trời (nhìn từ trên xuống)')]
    b.append(L(cx - 150, cy, cx + 150, cy, stroke=INK, w=5))
    b.append(L(cx, cy + 90, cx, cy - 100, stroke=GREY, w=2, dash='6 4'))
    b.append(C(cx, cy, 20, fill=LYELLOW, stroke=INK, w=2.5)); b.append(T(cx, cy + 5, 'Em', size=12, weight='bold'))
    b.append(L(cx, cy - 22, cx, cy - 92, stroke=RED, w=3, arrow=True))
    b.append(T(cx, cy - 106, 'Trước mặt: hướng Bắc', size=14, weight='bold', fill=RED))
    b.append(T(cx, cy + 112, 'Sau lưng: hướng Nam', size=14, weight='bold', fill=NAVY))
    # Mặt Trời mọc bên phải
    sx = cx + 215
    b.append(C(sx, cy, 24, fill='#ffd34d', stroke='#d99a00', w=2))
    for a in range(0, 360, 45):
        r = math.radians(a)
        b.append(L(sx + 30 * math.cos(r), cy + 30 * math.sin(r), sx + 40 * math.cos(r), cy + 40 * math.sin(r), stroke='#d99a00', w=2))
    b.append(T(sx, cy + 62, 'Mặt Trời mọc', size=12.5, weight='bold')); b.append(T(sx, cy + 79, '(hướng Đông)', size=12.5, weight='bold', fill=RED))
    b.append(T(cx - 100, cy - 14, 'Tay trái:', size=13, weight='bold')); b.append(T(cx - 100, cy + 24, 'hướng Tây', size=13, weight='bold', fill=NAVY))
    b.append(T(cx + 100, cy - 14, 'Tay phải:', size=13, weight='bold')); b.append(T(cx + 100, cy + 24, 'chỉ hướng Đông', size=13, weight='bold', fill=RED))
    b.append(T(W / 2, H - 10, 'Đứng giang hai tay, tay phải chỉ hướng Mặt Trời mọc.', size=12.5, fill='#55606d'))
    return svg(W, H, ''.join(b))


def noi_ngoai():
    return groups('Quá trình nội sinh và ngoại sinh', [
        ('Nội sinh', ['Xảy ra trong lòng Trái Đất, do năng lượng bên trong', 'Làm di chuyển các mảng kiến tạo, uốn nếp, đứt gãy, động đất, núi lửa', 'Tạo ra các dạng địa hình lớn: núi, cao nguyên']),
        ('Ngoại sinh', ['Xảy ra trên bề mặt Trái Đất, do năng lượng Mặt Trời, gió, nước chảy, sinh vật, con người', 'Phá huỷ, san bằng địa hình: phong hoá, bóc mòn, vận chuyển, bồi tụ'])],
        note='Hai quá trình xảy ra đồng thời và có tác động trái ngược nhau.')


def dia_hinh():
    W, H = 720, 330
    ys = 215
    b = [title(W, 'Các dạng địa hình chính (mặt cắt sơ đồ)')]
    pts = [(14, ys), (100, ys), (110, ys - 6), (230, ys - 8), (270, ys - 40), (320, ys - 8), (350, ys - 16), (400, ys - 70), (440, ys - 112), (480, ys - 60), (510, ys - 34), (520, ys - 76), (690, ys - 76), (706, ys - 50), (706, ys)]
    b.append(R(14, ys, 692, 40, fill=LGREY, stroke='none', sw=0))
    b.append(R(14, ys - 8, 96, 48, fill=LBLUE, stroke='none', sw=0))
    b.append(POLY(pts + [(706, ys + 40), (14, ys + 40)], fill='#e6efd9', stroke=GREEN, sw=2.2))
    b.append(L(14, ys, 706, ys, stroke=BLUE, w=2, dash='7 5'))
    b.append(T(14, ys + 18, 'Mực nước biển (0 m)', size=12, anchor='start', fill=BLUE, weight='bold'))
    # nhãn
    labs = [(170, 'Đồng bằng', 'độ cao tuyệt đối', 'thường dưới 200 m'), (270, 'Đồi', 'độ cao tương đối', 'dưới 200 m'),
            (440, 'Núi', 'độ cao tuyệt đối', 'trên 500 m'), (600, 'Cao nguyên', 'độ cao tuyệt đối', 'trên 500 m')]
    for x, a, c, d in labs:
        b.append(T(x, 52, a, size=14, weight='bold', fill=NAVY)); b.append(T(x, 70, c, size=12)); b.append(T(x, 86, d, size=12))
    # độ cao tương đối đồi: từ chân (ys-8) lên đỉnh
    b.append(L(270, ys - 40, 270, ys - 10, stroke=RED, w=2, arrow=True))
    b.append(L(440, ys - 112, 440, ys - 2, stroke=ORANGE, w=2.5, arrow=True))
    b.append(halo(520, ys - 78, 'Độ cao tuyệt đối', 12, ORANGE, 'start', 'bold')) if False else None
    b.append(T(W / 2, H - 28, 'Độ cao tuyệt đối: tính từ mực nước biển. Độ cao tương đối: tính từ chân lên đỉnh.', size=12.5, weight='bold', fill=NAVY))
    b.append(T(W / 2, H - 8, 'Sơ đồ minh họa, chiều cao không vẽ theo tỉ lệ.', size=11, fill='#55606d'))
    return svg(W, H, ''.join(b))


def nhiet_do_do_cao():
    W, H = 640, 300
    b = [title(W, 'Nhiệt độ giảm theo độ cao (trung bình lên 100 m giảm 0,6 °C)')]
    base, top, cx = 250, 70, 250
    b.append(POLY([(cx - 200, base), (cx, top), (cx + 200, base)], fill='#e6efd9', stroke=GREEN, sw=2.2))
    for k, (h, t) in enumerate([(0, 't °C'), (100, 't − 0,6 °C'), (200, 't − 1,2 °C'), (300, 't − 1,8 °C')]):
        y = base - k * 50
        xl = cx - 200 * (1 - (base - y) / (base - top))
        xr = cx + 200 * (1 - (base - y) / (base - top))
        b.append(L(xl, y, 520, y, stroke=GREY, w=1.3, dash='5 4'))
        b.append(T(560, y + 5, t, size=14, weight='bold', fill=RED if k else NAVY, anchor='start') if False else T(528, y + 5, t, size=14, weight='bold', fill=RED if k else NAVY, anchor='start'))
        if h:
            b.append(halo(xl - 8, y + 4, 'Cao %d m' % h, 12, INK, 'end', 'bold'))
        else:
            b.append(T(cx, y + 20, 'Chân núi', size=12, weight='bold'))
    b.append(T(W / 2, H - 8, 't là nhiệt độ ở chân núi; các giá trị tính theo quy tắc 0,6 °C mỗi 100 m.', size=12, fill='#55606d'))
    return svg(W, H, ''.join(b))


def globe():
    W, H = 640, 360
    cx, cy, r = 230, 190, 130
    cid = 'gl'
    b = [title(W, 'Năm đới khí hậu trên Trái Đất'), '<defs><clipPath id="%s"><circle cx="%d" cy="%d" r="%d"/></clipPath></defs>' % (cid, cx, cy, r)]
    lats = [90, 66.5, 23.5, -23.5, -66.5, -90]
    cols = ['#d9ecf7', '#e6efd9', '#fbd9d0', '#e6efd9', '#d9ecf7']
    names = ['Đới lạnh', 'Đới ôn hoà', 'Đới nóng', 'Đới ôn hoà', 'Đới lạnh']
    g = ['<g clip-path="url(#%s)">' % cid]
    for k in range(5):
        y1 = cy - r * math.sin(math.radians(lats[k])); y2 = cy - r * math.sin(math.radians(lats[k + 1]))
        g.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s"/>' % (cx - r, y1, 2 * r, y2 - y1, cols[k]))
    g.append('</g>')
    b.append(''.join(g)); b.append(C(cx, cy, r, stroke=INK, w=2.5))
    lines = [(66.5, 'Vòng cực Bắc'), (23.5, 'Chí tuyến Bắc'), (0, 'Xích đạo'), (-23.5, 'Chí tuyến Nam'), (-66.5, 'Vòng cực Nam')]
    for lat, nm in lines:
        y = cy - r * math.sin(math.radians(lat)); dx = r * math.cos(math.radians(lat))
        b.append(L(cx - dx, y, cx + dx, y, stroke=INK if lat else RED, w=1.6, dash=None if lat == 0 else '6 4'))
        b.append(L(cx + dx, y, 392, y, stroke=GREY, w=1, dash='3 3'))
        b.append(T(398, y + 4, nm, size=12.5, anchor='start', weight='bold'))
    for k in range(5):
        y1 = cy - r * math.sin(math.radians(lats[k])); y2 = cy - r * math.sin(math.radians(lats[k + 1]))
        if k in (0, 4):
            b.append(T(cx - r - 10, (y1 + y2) / 2 + 4 + (8 if k == 0 else -8), names[k], 13, anchor='end', weight='bold'))
        else:
            b.append(halo(cx, (y1 + y2) / 2 + 4, names[k], 13, INK, 'middle', 'bold'))
    b.append(T(500, 150, '', size=1))
    b.append(T(W / 2, H - 10, '1 đới nóng (giữa hai chí tuyến), 2 đới ôn hoà, 2 đới lạnh (từ vòng cực đến cực).', size=12.5, weight='bold', fill=NAVY))
    return svg(W, H, ''.join(b))


def song_ngoi():
    W, H = 720, 320
    b = [title(W, 'Hệ thống sông và lưu vực sông (sơ đồ)')]
    b.append(PATH('M60,180 C50,100 140,60 260,66 C400,60 560,70 640,120 C690,170 660,250 560,270 C420,290 300,285 180,270 C90,255 70,230 60,180 Z', fill='#f3f8ec', stroke=GREY, w=2).replace('stroke-linejoin', 'stroke-dasharray="8 6" stroke-linejoin'))
    b.append(halo(410, 232, 'Lưu vực sông', 13, '#55606d', 'middle', 'bold'))
    main = 'M110,205 C200,190 260,185 340,180 C430,176 500,172 560,165'
    b.append(PATH(main, stroke=BLUE, w=6))
    for d, nm, lx, ly in [('M190,100 C195,140 200,170 205,193', 'Phụ lưu', 130, 130), ('M330,92 C335,125 338,150 341,180', 'Phụ lưu', 360, 120),
                          ('M300,262 C310,230 330,205 345,181', 'Phụ lưu', 262, 250), ('M470,268 C480,230 490,200 495,174', 'Phụ lưu', 520, 250)]:
        b.append(PATH(d, stroke=BLUE, w=3.5))
    b.append(halo(140, 120, 'Phụ lưu', 13, NAVY, 'middle', 'bold')); b.append(halo(380, 112, 'Phụ lưu', 13, NAVY, 'middle', 'bold'))
    b.append(halo(250, 252, 'Phụ lưu', 13, NAVY, 'middle', 'bold')); b.append(halo(530, 252, 'Phụ lưu', 13, NAVY, 'middle', 'bold'))
    b.append(halo(300, 168, 'Sông chính', 14, '#0b3d82', 'middle', 'bold'))
    # chi lưu
    b.append(PATH('M560,165 C600,150 640,130 680,118', stroke=BLUE, w=3.5)); b.append(PATH('M560,165 C610,168 650,170 690,172', stroke=BLUE, w=3.5)); b.append(PATH('M560,165 C600,185 640,205 676,224', stroke=BLUE, w=3.5))
    b.append(halo(660, 100, 'Chi lưu', 13, RED, 'middle', 'bold'))
    b.append(T(W / 2, H - 8, 'Phụ lưu đổ nước vào sông chính; chi lưu thoát nước cho sông chính; lưu vực là vùng đất cung cấp nước cho sông.', size=11.5, fill='#55606d'))
    return svg(W, H, ''.join(b))


def dat6():
    return dl.pie('Thành phần của đất (khoảng)', [
        (('Thành phần khoáng', 'Chiếm khoảng 45%'), 45, 0), (('Nước', 'Chiếm khoảng 25%'), 25, 2),
        (('Không khí', 'Chiếm khoảng 25%'), 25, 5), (('Chất hữu cơ (chất mùn)', 'Chiếm khoảng 5%'), 5, 1)])


# ================= Địa lí 9 =================
def cay_vung():
    return dl.table('Một số cây trồng chính và vùng tập trung', ['Cây trồng', 'Vùng tập trung'], [
        ['Cây lúa (lương thực chính)', 'Đồng bằng sông Cửu Long (hơn 50% sản lượng), Đồng bằng sông Hồng'],
        ['Cà phê', 'Tây Nguyên'], ['Cao su', 'Đông Nam Bộ'], ['Chè', 'Trung du và miền núi phía Bắc'],
        ['Hồ tiêu, điều…', 'Cây công nghiệp khác']], [270, 440], W=730)


def rung():
    return dl.stacks('Rừng nước ta', [
        ('Độ che phủ rừng (năm 2023)', [('Rừng ≈ 42%', 42, 2), ('Diện tích khác ≈ 58%', 58, 5)]),
        ('Ba loại rừng', [('Rừng đặc dụng', 1, 0), ('Rừng phòng hộ', 1, 1), ('Rừng sản xuất', 1, 2)])],
        note='Vùng có diện tích rừng lớn: Tây Nguyên, Bắc Trung Bộ, Trung du và miền núi phía Bắc.')


def vung(ttl, cols, note=None):
    return lambda: groups(ttl, cols, note)


# ================= Lịch sử 7 =================
def phuc_hung():
    return groups('Thành tựu Văn hoá Phục hưng', [
        ('Văn học', ['Xéc-van-tét (Đôn Ki-hô-tê)', 'Sếch-xpia (Rô-mê-ô và Giu-li-ét, Hăm-lét)']),
        ('Hội hoạ, điêu khắc', ['Lê-ô-na đơ Vanh-xi (Bữa tiệc cuối cùng, Nàng Mô-na Li-da)', 'Mi-ken-lăng-giơ (Tượng Đa-vít)']),
        ('Khoa học', ['Cô-péc-ních', 'Bru-nô', 'Ga-li-lê'])],
        note='Đề cao con người, tự do cá nhân và tinh thần khoa học.')


# ================= Sinh 7 =================
def buoc_pp():
    W, H = 880, 250
    steps = ['Đề xuất\nvấn đề', 'Đưa ra dự đoán\nkhoa học', 'Lập kế hoạch\nkiểm tra dự đoán', 'Thực hiện\nkế hoạch', 'Viết báo cáo,\nthảo luận,\ntrình bày']
    n = 5; gap = 28; bw = (W - 28 - gap * (n - 1)) / n
    b = [title(W, 'Năm bước của phương pháp tìm hiểu tự nhiên')]
    xs = []
    for k, s in enumerate(steps):
        x = 14 + k * (bw + gap); xs.append(x)
        b.append(R(x, 50, bw, 90, fill=SOFT[k % 4], stroke=HEAD[k % 4], sw=2.5, rx=10))
        b.append(T(x + 22, 74, str(k + 1), size=15, weight='bold', fill=HEAD[k % 4]))
        for i, ln in enumerate(s.split('\n')):
            b.append(T(x + bw / 2 + 8, 88 + i * 18 - (len(s.split('\n')) - 2) * 4, ln, size=13, weight='bold'))
        if k < n - 1:
            b.append(L(x + bw + 4, 95, x + bw + gap - 4, 95, w=3, arrow=True))
    # mũi tên quay lại từ bước 4 về bước 2
    x4, x2 = xs[3] + bw / 2, xs[1] + bw / 2
    b.append(PL([(x4, 142), (x4, 185), (x2, 185)], stroke=RED, w=2.5, dash='7 5'))
    b.append(L(x2, 185, x2, 144, stroke=RED, w=2.5, arrow=True))
    b.append(T((x4 + x2) / 2, 206, 'Kết quả không phù hợp với dự đoán: quay lại bước đưa ra dự đoán', size=12.5, weight='bold', fill=RED))
    return svg(W, H, ''.join(b))


def tn_tinh_bot():
    W, H = 900, 330
    steps = [('Bước 1', 'Đặt cây trong', 'bóng tối 2 ngày'), ('Bước 2', 'Che một phần lá bằng', 'giấy đen, đưa ra ánh sáng', '4 – 6 giờ'),
             ('Bước 3', 'Ngắt lá, đun trong', 'cồn 90° để tẩy', 'diệp lục'), ('Bước 4', 'Rửa trong nước ấm,', 'nhúng vào dung dịch', 'iodine')]
    n = 4; gap = 30; bw = (W - 28 - gap * (n - 1)) / n
    b = [title(W, 'Thí nghiệm chứng minh tinh bột được tạo thành trong quang hợp')]
    for k, s in enumerate(steps):
        x = 14 + k * (bw + gap)
        b.append(R(x, 48, bw, 110, fill=SOFT[k % 4], stroke=HEAD[k % 4], sw=2.5, rx=10))
        b.append(T(x + bw / 2, 72, s[0], size=14, weight='bold', fill=HEAD[k % 4]))
        for i, ln in enumerate(s[1:]):
            b.append(T(x + bw / 2, 96 + i * 18, ln, size=12.5))
        if k < n - 1:
            b.append(L(x + bw + 4, 103, x + bw + gap - 4, 103, w=3, arrow=True))
    b.append(L(W / 2, 160, W / 2, 190, w=3, arrow=True))
    b.append(R(120, 192, 300, 100, fill='#e3dcf2', stroke='#6c4aa8', sw=2.5, rx=10)); b.append(R(480, 192, 300, 100, fill='#eaf3e0', stroke=GREEN, sw=2.5, rx=10))
    b.append(T(270, 224, 'Phần lá không che', size=14, weight='bold')); b.append(T(270, 250, 'Bị nhuộm màu xanh tím', size=13)); b.append(T(270, 272, '(có tinh bột)', size=12, fill='#55606d'))
    b.append(T(630, 224, 'Phần lá bị che', size=14, weight='bold')); b.append(T(630, 250, 'Không đổi màu', size=13)); b.append(T(630, 272, '(không có tinh bột)', size=12, fill='#55606d'))
    b.append(T(W / 2, H - 14, 'Kết luận: tinh bột được tạo thành trong quang hợp ở phần lá có ánh sáng.', size=13, weight='bold', fill=NAVY))
    return svg(W, H, ''.join(b))


def ho_hap():
    W, H = 720, 280
    b = [title(W, 'Hô hấp tế bào')]
    b.append(box(14, 60, 170, 56, ['Glucose', 'C₆H₁₂O₆'], 0)); b.append(box(14, 150, 170, 56, ['Khí oxygen', 'O₂'], 1))
    b.append(L(186, 90, 262, 140, w=3, arrow=True)); b.append(L(186, 178, 262, 160, w=3, arrow=True))
    b.append('<ellipse cx="360" cy="150" rx="100" ry="70" fill="#fdf1e0" stroke="#f28e2b" stroke-width="3"/>')
    b.append(T(360, 140, 'Ti thể', size=17, weight='bold')); b.append(T(360, 164, 'hô hấp tế bào', size=13))
    b.append(L(462, 140, 536, 90, w=3, arrow=True)); b.append(L(462, 150, 536, 150, w=3, arrow=True)); b.append(L(462, 160, 536, 208, w=3, arrow=True))
    b.append(box(538, 60, 168, 52, ['Khí CO₂'], 2)); b.append(box(538, 126, 168, 52, ['Nước H₂O'], 0)); b.append(box(538, 192, 168, 52, ['Năng lượng (ATP)'], 3))
    b.append(T(W / 2, H - 14, 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + năng lượng (ATP)', size=13, weight='bold', fill=NAVY))
    return svg(W, H, ''.join(b))


def yeu_to_hh():
    return groups('Một số yếu tố ảnh hưởng đến hô hấp tế bào', [
        ('Nước', ['Là dung môi, môi trường của phản ứng hô hấp', 'Hàm lượng nước trong hạt tăng thì cường độ hô hấp tăng mạnh']),
        ('Khí oxygen', ['Là nguyên liệu của hô hấp', 'Nồng độ O₂ ngoài môi trường dưới 5% thì cường độ hô hấp giảm']),
        ('Khí CO₂', ['Nồng độ 3% đến 5% đã gây ức chế hô hấp']),
        ('Nhiệt độ', ['Quá cao hoặc quá thấp đều ảnh hưởng', 'Ở người, trên 40 °C hô hấp tế bào gặp khó khăn'])],
        note='Bảo quản nông sản: phơi/sấy khô (độ ẩm hạt khoảng 13% đến 16%), bảo quản lạnh (khoai tây 4 °C, cam 6 °C).')


def chuong_ab():
    W, H = 700, 330
    b = [title(W, 'Thí nghiệm hô hấp ở hạt nảy mầm')]
    for k, (cx, lab, seeds, col, res) in enumerate([(190, 'Chuông A', True, '#e8e8e8', 'Nước vôi trong bị vẩn đục'), (510, 'Chuông B', False, '#e8f4fb', 'Nước vôi trong vẫn trong')]):
        b.append(PATH('M%d,230 L%d,110 Q%d,60 %d,60 Q%d,60 %d,110 L%d,230' % (cx - 110, cx - 110, cx - 110, cx, cx + 110, cx + 110, cx + 110), fill='#f3f8fb', stroke=INK, w=2.5))
        b.append(R(cx - 130, 230, 260, 10, fill=LGREY, stroke=INK, sw=2))
        b.append(R(cx + 20, 200, 60, 30, fill=col, stroke=INK, sw=2)); b.append(T(cx + 50, 195, 'nước vôi trong', size=11, fill='#3b4856'))
        if seeds:
            b.append(R(cx - 90, 214, 90, 16, fill='#e5d6b4', stroke=INK, sw=1.5))
            for i in range(5):
                b.append(C(cx - 78 + i * 17, 207, 7, fill='#8fb35b', stroke=INK, w=1.2))
            b.append(T(cx - 45, 195, 'hạt nảy mầm', size=11, fill='#3b4856'))
        b.append(T(cx, 266, lab, size=15, weight='bold'))
        b.append(T(cx, 290, res, size=13, weight='bold', fill=RED if seeds else NAVY))
    b.append(T(W / 2, H - 6, 'Hạt đang nảy mầm hô hấp và thải khí carbon dioxide.', size=12.5, fill='#55606d'))
    return svg(W, H, ''.join(b))


def nuoc():
    W, H = 640, 320
    b = [title(W, 'Phân tử nước (H₂O)')]
    ox, oy = 250, 130
    a = math.radians(52)
    hx1, hy1 = ox - 110 * math.sin(a), oy + 110 * math.cos(a)
    hx2, hy2 = ox + 110 * math.sin(a), oy + 110 * math.cos(a)
    b.append(L(ox, oy, hx1, hy1, stroke=INK, w=5)); b.append(L(ox, oy, hx2, hy2, stroke=INK, w=5))
    b.append(C(ox, oy, 30, fill='#f6c3c3', stroke=RED, w=2.5)); b.append(T(ox, oy + 6, 'O', size=20, weight='bold'))
    for hx, hy in ((hx1, hy1), (hx2, hy2)):
        b.append(C(hx, hy, 20, fill='#dbe7f3', stroke=BLUE, w=2.5)); b.append(T(hx, hy + 6, 'H', size=16, weight='bold'))
    b.append(T(ox, oy - 42, 'δ−', size=16, weight='bold', fill=RED)); b.append(T(hx1 - 6, hy1 + 40, 'δ+', size=16, weight='bold', fill=BLUE)); b.append(T(hx2 + 6, hy2 + 40, 'δ+', size=16, weight='bold', fill=BLUE))
    b.append(TL(470, 100, ['Một nguyên tử oxygen liên kết', 'với hai nguyên tử hydrogen', 'bằng liên kết cộng hoá trị.'], size=13, lh=20))
    b.append(TL(470, 190, ['Cặp electron bị lệch về phía', 'oxygen nên nước có tính phân cực,', 'là dung môi hoà tan nhiều chất.'], size=13, lh=20))
    b.append(T(W / 2, H - 8, 'Sơ đồ minh họa; góc liên kết không phải số đo chính xác.', size=11, fill='#55606d'))
    return svg(W, H, ''.join(b))


def song_chu():
    return groups('Thực hành với cây cần tây', [
        ('Thí nghiệm 1', ['Cắt ngang cuống lá gần gốc, cắm vào cốc nước pha màu', 'Sau 30 – 60 phút: màu nước đã di chuyển lên cuống và lá']),
        ('Thí nghiệm 2', ['Cắt ngang phần cuống lá có màu, quan sát dưới kính lúp', 'Màu nhuộm ở các bó mạch dẫn: mạch gỗ vận chuyển nước']),
        ('Thí nghiệm 3', ['Dùng túi nylon trong suốt bao kín lá (hoặc cành)', 'Trong túi xuất hiện giọt nước đọng: lá thoát hơi nước'])])


def cam_ung():
    return groups('Thực hành cảm ứng ở sinh vật', [
        ('Tính hướng nước', ['Gieo hạt đỗ vào 2 chậu; cây có 3 – 5 lá', 'Đặt chậu nước có lỗ thủng nhỏ vào một chậu', 'Sau 3 – 5 ngày nhổ cây, quan sát hướng mọc của rễ']),
        ('Tính hướng sáng', ['Úp hộp carton (khoét lỗ bên cạnh) lên chậu cây', 'Sau 3 – 5 ngày nhấc hộp, quan sát hướng của thân']),
        ('Tính hướng tiếp xúc', ['Quan sát tranh ảnh, video về cây mướp, bầu, bí'])],
        note='Ghi kết quả vào phiếu theo mẫu và so sánh với chậu đối chứng.')


def vong_doi():
    W, H = 760, 250
    b = [title(W, 'Các giai đoạn trong vòng đời')]
    rows = [('Bướm', ['Trứng', 'Ấu trùng', 'Nhộng', 'Con trưởng thành']), ('Gà', ['Trứng', 'Gà con', 'Gà trưởng thành'])]
    for r, (nm, st) in enumerate(rows):
        y = 52 + r * 92
        b.append(T(30, y + 38, nm, size=16, weight='bold', anchor='start'))
        n = len(st); gap = 36; x0 = 110; bw = (W - x0 - 20 - gap * 3) / 4
        for k, s in enumerate(st):
            x = x0 + k * (bw + gap)
            b.append(box(x, y, bw, 56, [s], k, size=13.5))
            if k < n - 1:
                b.append(L(x + bw + 4, y + 28, x + bw + gap - 4, y + 28, w=3, arrow=True))
    return svg(W, H, ''.join(b))


def sinh_san_vt():
    return groups('Sinh sản vô tính ở sinh vật', [
        ('Sinh dưỡng ở thực vật', ['Từ rễ: khoai lang', 'Từ lá: cây lá bỏng', 'Từ thân: cây dâu tây', 'Từ thân ngầm: cây gừng']),
        ('Ở động vật', ['Nảy chồi: thuỷ tức', 'Phân mảnh: giun dẹp, sao biển', 'Trinh sản: rệp cây, ong, kiến']),
        ('Ứng dụng', ['Giâm cành, chiết cành, ghép cây', 'Nuôi cấy tế bào và mô để nhân nhanh giống, tạo giống sạch bệnh, khôi phục giống quý'])],
        note='Cơ thể con được tạo thành từ một phần của cơ thể mẹ, không có sự kết hợp của giao tử.')


def yeu_to_sinh_san():
    return groups('Yếu tố ảnh hưởng và điều khiển sinh sản', [
        ('Yếu tố bên trong', ['Đặc điểm di truyền', 'Hormone', 'Tuổi']),
        ('Yếu tố bên ngoài', ['Ánh sáng', 'Độ ẩm', 'Nhiệt độ', 'Chế độ dinh dưỡng']),
        ('Điều khiển sinh sản', ['Thực vật: hormone, nhiệt độ, chiếu sáng, dinh dưỡng, thụ phấn nhân tạo', 'Động vật: hormone, thụ tinh nhân tạo, cấy phôi'])],
        note='Ví dụ: thắp đèn cho cây thanh long ra hoa vào mùa đông; cá chép chỉ đẻ ở nhiệt độ trên 15 °C.')


def thong_nhat():
    W, H = 720, 330
    b = [title(W, 'Cơ thể sinh vật là một thể thống nhất')]
    cx, cy = 360, 180
    b.append('<ellipse cx="%d" cy="%d" rx="86" ry="42" fill="#e6f0df" stroke="#59a14f" stroke-width="3"/>' % (cx, cy))
    b.append(T(cx, cy - 2, 'Tế bào', size=15, weight='bold')); b.append(T(cx, cy + 18, 'Cơ thể', size=15, weight='bold'))
    items = [(40, 56, 'Trao đổi chất và', 'chuyển hoá năng lượng', 0), (480, 56, 'Sinh trưởng', 'và phát triển', 1), (40, 236, 'Sinh sản', '', 2), (480, 236, 'Cảm ứng', '', 3)]
    for x, y, a, c, ci in items:
        b.append(R(x, y, 200, 56, fill=SOFT[ci], stroke=HEAD[ci], sw=2.5, rx=10))
        b.append(T(x + 100, y + (24 if c else 34), a, size=13.5, weight='bold'))
        if c: b.append(T(x + 100, y + 44, c, size=13.5, weight='bold'))
        tx, ty = (x + 200, y + 28) if x < 300 else (x, y + 28)
        ex = cx - 88 if x < 300 else cx + 88
        b.append(L(tx, ty, ex, cy + (-8 if y < 150 else 8), stroke=GREY, w=2.5))
    b.append(L(240, 84, 480, 84, stroke=INK, w=2)); b.append(L(240, 264, 480, 264, stroke=INK, w=2))
    b.append(T(W / 2, H - 8, 'Các hoạt động sống có quan hệ qua lại mật thiết; hoạt động ở cấp tế bào là cơ sở cho hoạt động ở cấp cơ thể.', size=11.5, fill='#55606d'))
    return svg(W, H, ''.join(b))


FIG = []   # (môn, bài, tên file, hàm, chú thích, đường dẫn tương đối tuỳ chọn)


def add(subj, bai, tag, fn, cap, rel=None):
    FIG.append((subj, bai, 'hh-%s-b%s-%s.svg' % (subj, bai, tag), fn, cap, rel))


# Địa 6
add('diali6', 4, 'kihieu', ki_hieu, 'Ba loại kí hiệu bản đồ')
add('diali6', 9, 'huong', phuong_huong, 'Xác định phương hướng bằng Mặt Trời')
add('diali6', 11, 'noisinh', noi_ngoai, 'Nội sinh và ngoại sinh')
add('diali6', 13, 'dia-hinh', dia_hinh, 'Các dạng địa hình chính')
add('diali6', 16, 'do-cao', nhiet_do_do_cao, 'Nhiệt độ giảm theo độ cao')
add('diali6', 17, 'doi-khi-hau', globe, 'Năm đới khí hậu')
add('diali6', 20, 'song', song_ngoi, 'Hệ thống sông và lưu vực')
add('diali6', 22, 'dat', dat6, 'Thành phần của đất')
add('diali6', 25, 'doi-tn', globe, 'Các đới thiên nhiên theo vĩ độ')
# Địa 9
add('diali9', 5, 'cay', cay_vung, 'Cây trồng chính và vùng tập trung')
add('diali9', 6, 'rung', rung, 'Độ che phủ rừng và các loại rừng')
add('diali9', 12, 'vung', vung('Vùng Trung du và miền núi phía Bắc', [
    ('Thế mạnh', ['Khai thác khoáng sản (than Quảng Ninh, a-pa-tít Lào Cai)', 'Thuỷ điện trên sông Đà (Hoà Bình, Sơn La, Lai Châu)', 'Cây cận nhiệt và ôn đới (chè), dược liệu, rau quả', 'Chăn nuôi trâu, bò; du lịch; kinh tế biển Quảng Ninh']),
    ('Dân cư và khó khăn', ['Dân cư thưa, nhiều dân tộc ít người', 'Địa hình hiểm trở', 'Rét đậm, rét hại, lũ quét', 'Cơ sở hạ tầng còn hạn chế'])], 'Diện tích khoảng 95 nghìn km², lớn nhất cả nước; gồm Đông Bắc và Tây Bắc.'), 'Vùng Trung du và miền núi phía Bắc')
add('diali9', 13, 'vung', vung('Vùng Đồng bằng sông Hồng', [
    ('Điều kiện', ['Diện tích khoảng 21 nghìn km²', 'Dân số đông nhất (khoảng 23 triệu), mật độ cao nhất', 'Đất phù sa màu mỡ, mùa đông lạnh trồng cây vụ đông']),
    ('Kinh tế', ['Công nghiệp phát triển sớm (Hà Nội, Hải Phòng, Bắc Ninh…)', 'Vùng trọng điểm lúa thứ hai, năng suất lúa cao nhất', 'Dịch vụ: Hà Nội, cảng Hải Phòng']),
    ('Hạn chế', ['Dân số đông: sức ép việc làm, nhà ở, môi trường', 'Thiên tai: bão, lũ'])]), 'Vùng Đồng bằng sông Hồng')
add('diali9', 16, 'vung', vung('Duyên hải Nam Trung Bộ và Tây Nguyên', [
    ('Duyên hải Nam Trung Bộ', ['Dải đồng bằng hẹp ven biển, nhiều vũng vịnh', 'Khai thác, nuôi trồng thuỷ sản; làm muối (Sa Huỳnh, Cà Ná)', 'Du lịch biển (Nha Trang, Mũi Né)', 'Cảng biển: Đà Nẵng, Quy Nhơn, Cam Ranh']),
    ('Tây Nguyên', ['Không giáp biển, các cao nguyên xếp tầng, đất badan', 'Khí hậu cận xích đạo, một mùa khô sâu sắc', 'Cây công nghiệp: cà phê (lớn nhất cả nước), cao su, chè, hồ tiêu', 'Rừng, thuỷ điện, bô-xít; du lịch (Đà Lạt)'])]), 'Hai vùng Duyên hải Nam Trung Bộ và Tây Nguyên')
add('diali9', 17, 'vung', vung('Vùng Đông Nam Bộ', [
    ('Điều kiện', ['Diện tích khoảng 23,5 nghìn km²', 'Địa hình thoải, đất badan và đất xám', 'Thềm lục địa giàu dầu khí', 'Dân cư đông, lao động có trình độ']),
    ('Kinh tế', ['Phát triển nhất cả nước', 'Công nghiệp: dầu khí, điện, điện tử, cơ khí, hoá chất, chế biến thực phẩm', 'Cao su lớn nhất cả nước, điều, hồ tiêu', 'TP Hồ Chí Minh: trung tâm kinh tế, tài chính, thương mại lớn nhất']),
    ('Vấn đề', ['Ô nhiễm môi trường', 'Ùn tắc giao thông', 'Sức ép dân số đô thị'])]), 'Vùng Đông Nam Bộ')
# Lịch sử 7
add('lichsu7', 3, 'phuchung', phuc_hung, 'Thành tựu Văn hoá Phục hưng')
FIG.append(('lichsu7', 8, 'hh-lichsu7-b8-tl.svg', lambda: timeline('Vương quốc Cam-pu-chia', [
    ('Năm 802', ['Giay-a-vác-man II thống nhất,', 'đặt tên nước là Cam-pu-chia']),
    ('Thế kỉ IX – XV', ['Thời kì Ăng-co,', 'rực rỡ nhất']),
    ('Thế kỉ XV', ['Suy yếu; chuyển kinh đô', 'về phía nam Biển Hồ'])], 300), 'Dòng thời gian Cam-pu-chia', None))
FIG.append(('lichsu7', 10, 'hh-lichsu7-b10-tl.svg', lambda: timeline('Đại Cồ Việt thời Đinh và Tiền Lê', [
    ('Năm 968', ['Đinh Bộ Lĩnh lên ngôi,', 'đặt tên nước Đại Cồ Việt,', 'đóng đô Hoa Lư']),
    ('Cuối năm 979', ['Đinh Tiên Hoàng bị ám sát;', 'Lê Hoàn được suy tôn']),
    ('Đầu năm 981', ['Quân Tống tiến đánh,', 'bị Lê Hoàn đánh bại']),
    ('Năm 1002', ['Đổi 10 đạo thành', 'lộ, phủ, châu'])], 320), 'Dòng thời gian Đinh – Tiền Lê', None))
add('lichsu7', 13, 'tran', lambda: groups('Đại Việt thời Trần', [
    ('Chính trị', ['Củng cố quân chủ tập quyền', 'Tôn thất họ Trần giữ vị trí trọng yếu, được lập thái ấp', 'Ban hành Quốc triều hình luật']),
    ('Kinh tế – xã hội', ['Khai hoang, đắp đê, làm thuỷ lợi', 'Làng nghề, phường nghề', 'Buôn bán sôi động: cảng Vân Đồn, Hội Thống']),
    ('Văn hoá', ['Nho giáo, Phật giáo, Đạo giáo', 'Đại Việt sử kí', 'Binh thư yếu lược, Vạn Kiếp tông bí truyền thư', 'Y học: Tuệ Tĩnh'])],
    note='Tháng 1 – 1226: Lý Chiêu Hoàng nhường ngôi cho Trần Cảnh, nhà Trần thành lập.'), 'Đại Việt thời Trần')
FIG.append(('lichsu7', 'bs2', 'hh-lichsu7-bs2-tl.svg', lambda: timeline('Bảo vệ chủ quyền biển đảo', [
    ('Ngày 19 – 20 – 1974', ['Trung Quốc dùng vũ lực đánh', 'chiếm nhóm đảo phía tây Hoàng Sa']),
    ('Ngày 14 – 3 – 1988', ['Đá Gạc Ma (Trường Sa): 64 cán', 'bộ, chiến sĩ hải quân hi sinh'])], 280), 'Hai mốc bảo vệ chủ quyền biển đảo',
    'tap1/chu-quyen-bien-dao/bs-2/bao-ve-chu-quyen-bien-dao.json'))
# Sinh 7
add('sinh7', 1, 'buoc', buoc_pp, 'Năm bước tìm hiểu tự nhiên')
add('sinh7', 24, 'tn', tn_tinh_bot, 'Thí nghiệm tinh bột trong quang hợp')
add('sinh7', 25, 'hohap', ho_hap, 'Hô hấp tế bào ở ti thể')
add('sinh7', 26, 'yeuto', yeu_to_hh, 'Các yếu tố ảnh hưởng đến hô hấp tế bào')
add('sinh7', 27, 'chuong', chuong_ab, 'Thí nghiệm hô hấp ở hạt nảy mầm')
add('sinh7', 29, 'nuoc', nuoc, 'Phân tử nước')
add('sinh7', 32, 'canTay', song_chu, 'Ba thí nghiệm với cây cần tây')
add('sinh7', 35, 'camung', cam_ung, 'Thực hành cảm ứng ở sinh vật')
add('sinh7', 38, 'vongdoi', vong_doi, 'Giai đoạn trong vòng đời của bướm và gà')
add('sinh7', 39, 'vo-tinh', sinh_san_vt, 'Sinh sản vô tính')
add('sinh7', 41, 'sinhsan', yeu_to_sinh_san, 'Yếu tố ảnh hưởng, điều khiển sinh sản')
add('sinh7', 42, 'thongnhat', thong_nhat, 'Cơ thể là một thể thống nhất')


def find(subj, bai, rel):
    if rel:
        p = os.path.join(ROOT, 'content', subj, rel)
        assert os.path.exists(p), p
        return p
    hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%s' % bai, '*.json'))
    assert len(hits) == 1, (subj, bai, hits)
    return hits[0]


if __name__ == '__main__':
    for subj, bai, nm, fn, cap, rel in FIG:
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf8').write(fn())
        p = find(subj, bai, rel)
        data = json.load(open(p, encoding='utf8'))
        attach(subj, os.path.relpath(p, os.path.join(ROOT, 'content', subj)), len(data['theory']) - 1, nm, cap)
    print('hh: %d hình' % len(FIG))
