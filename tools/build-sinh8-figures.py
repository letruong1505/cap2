# Sinh 8: sơ đồ minh họa lý thuyết (không phải ảnh chụp, không đo đúng tỉ lệ).
import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from sinhlib import *

ATTACH = []
FIGS = {}


def reg(name, fn, rel, after, cap):
    FIGS[name] = fn
    ATTACH.append((rel, after, name, cap))


# ---------- Bài 30 ----------
def fig_he_co_quan():
    b = [title(720, 'Tám hệ cơ quan của cơ thể người')]
    items = [('Hệ vận động', 'định hình cơ thể, cử động, di chuyển'), ('Hệ tuần hoàn', 'vận chuyển chất dinh dưỡng, khí'),
             ('Hệ hô hấp', 'lấy O₂, thải CO₂'), ('Hệ tiêu hoá', 'biến đổi thức ăn thành chất dinh dưỡng'),
             ('Hệ bài tiết', 'lọc, thải chất thải có hại'), ('Hệ thần kinh và giác quan', 'thu nhận kích thích, điều khiển'),
             ('Hệ nội tiết', 'tiết hormone điều hoà hoạt động'), ('Hệ sinh dục', 'sinh sản, duy trì nòi giống')]
    cols = ['#f9d9d6', '#fbe3c8', '#f7f0c4', '#dcebc9', '#cfe6e0', '#d3e1f3', '#e2d6f0', '#f3d3e4']
    b.append(ELL(360, 175, 78, 56, fill=LYELLOW, stroke=INK, w=2.6)); b.append(TL(360, 170, ['Cơ thể', 'người'], size=17, lh=22, weight='bold'))
    for i, (n, f) in enumerate(items):
        left = i < 4
        x = 10 if left else 520
        y = 46 + (i % 4) * 72
        b.append(R(x, y, 190, 58, fill=cols[i], stroke=INK, sw=1.8, rx=8))
        b.append(T(x + 95, y + 23, n, size=13.5, weight='bold'))
        parts = f if len(f) < 28 else None
        if len(f) < 29:
            b.append(T(x + 95, y + 43, f, size=11, fill='#3b4856'))
        else:
            b.append(TL(x + 95, y + 40, [f[:f.rfind(' ', 0, 28)], f[f.rfind(' ', 0, 28) + 1:]], size=11, lh=13, fill='#3b4856'))
        px = x + 190 if left else x
        qx = 360 + (-78 if left else 78) * 0.8
        b.append(L(px, y + 29, qx, 175 + (y + 29 - 175) * 0.3, stroke=GREY, w=1.4))
    return svg(720, 346, ''.join(b))


reg('c-s8-b30-he-co-quan.svg', fig_he_co_quan, 'sinh8/bai-30/khai-quat-co-the-nguoi.json', 1, 'Tám hệ cơ quan và chức năng chính')


# ---------- Bài 31 ----------
def fig_bo_xuong():
    b = [title(720, 'Bộ xương người (sơ đồ nhìn thẳng)')]
    cx = 240
    HEAD, TRUNK, LIMB = '#f6c28b', '#a9c8e8', '#b8dba6'
    b.append(ELL(cx, 66, 26, 30, fill=HEAD, stroke=INK, w=2.4))
    b.append(PATH('M%d,%d Q%d,%d %d,%d' % (cx - 20, 82, cx, 108, cx + 20, 82), fill=HEAD, stroke=INK, w=2.2))
    b.append(L(cx, 100, cx, 250, stroke=INK, w=13)); b.append(L(cx, 100, cx, 250, stroke=TRUNK, w=9))
    for yy in range(104, 250, 8):
        b.append(L(cx - 5, yy, cx + 5, yy, stroke=INK, w=1))
    for k in range(7):
        yy = 122 + k * 13
        wd = 52 - abs(k - 2) * 5 if k < 3 else 52 - (k - 2) * 7
        wd = 46 + (k if k < 3 else 6 - k) * 4
        for s in (-1, 1):
            b.append(PATH('M%d,%d Q%d,%d %d,%d' % (cx + s * 4, yy, cx + s * wd, yy - 4, cx + s * (wd - 4), yy + 24), stroke=INK, w=3.2))
            b.append(PATH('M%d,%d Q%d,%d %d,%d' % (cx + s * 4, yy, cx + s * wd, yy - 4, cx + s * (wd - 4), yy + 24), stroke=TRUNK, w=1.6))
    b.append(R(cx - 5, 118, 10, 58, fill=TRUNK, stroke=INK, sw=1.6, rx=3))
    b.append(POLY([(cx - 4, 248), (cx - 52, 236), (cx - 62, 270), (cx - 30, 296), (cx - 5, 276), (cx + 5, 276), (cx + 30, 296), (cx + 62, 270), (cx + 52, 236), (cx + 4, 248)], fill=TRUNK, stroke=INK, sw=2.2))
    for s in (-1, 1):
        b.append(bone(cx + s * 4, 108, cx + s * 44, 112, w=7, fill=LIMB))
        b.append(bone(cx + s * 44, 112, cx + s * 58, 190, w=10, fill=LIMB))
        b.append(C(cx + s * 59, 192, 7, fill='#e8e0c8', stroke=INK, w=1.8))
        b.append(bone(cx + s * 60, 196, cx + s * 66, 262, w=7, fill=LIMB)); b.append(bone(cx + s * 56, 196, cx + s * 58, 262, w=6, fill=LIMB))
        b.append(bone(cx + s * 28, 284, cx + s * 40, 378, w=12, fill=LIMB))
        b.append(C(cx + s * 41, 383, 8, fill='#e8e0c8', stroke=INK, w=1.8))
        b.append(bone(cx + s * 42, 390, cx + s * 44, 466, w=9, fill=LIMB))
        b.append(PL([(cx + s * 38, 470), (cx + s * 62, 470)], stroke=INK, w=5))
    # chú thích
    lead(b, cx + 24, 62, 400, 70, 'xương sọ, xương mặt', anchor='start')
    lead(b, cx + 1, 218, 400, 208, 'cột sống', anchor='start')
    lead(b, cx + 52, 142, 400, 128, 'xương sườn', anchor='start')
    lead(b, cx + 5, 150, 400, 168, 'xương ức', anchor='start')
    lead(b, cx + 56, 272, 400, 262, 'xương chậu', anchor='start')
    lead(b, cx + 22, 110, 400, 100, 'xương đòn', anchor='start') if False else None
    lead(b, cx - 58, 150, 70, 150, 'xương cánh tay', anchor='end') if False else lead(b, cx - 52, 150, 160, 150, 'xương cánh tay', anchor='end')
    lead(b, cx - 62, 230, 160, 230, 'xương cẳng tay', anchor='end')
    lead(b, cx - 36, 332, 160, 332, 'xương đùi', anchor='end')
    lead(b, cx - 42, 430, 160, 430, 'xương cẳng chân', anchor='end')
    lead(b, cx - 41, 383, 160, 380, 'khớp gối', anchor='end')
    lead(b, cx - 59, 192, 160, 190, 'khớp khuỷu', anchor='end')
    for k, (col, t) in enumerate(((HEAD, 'xương đầu'), (TRUNK, 'xương thân'), (LIMB, 'xương chi'))):
        b.append(R(520, 300 + k * 30, 22, 18, fill=col, stroke=INK, sw=1.6, rx=3)); b.append(T(550, 314 + k * 30, t, size=14, weight='bold', anchor='start'))
    b.append(T(520, 280, 'Ba phần của bộ xương', size=13, fill=GREY, anchor='start'))
    return svg(720, 490, ''.join(b))


reg('c-s8-b31-bo-xuong.svg', fig_bo_xuong, 'sinh8/bai-31/he-van-dong-o-nguoi.json', 0, 'Bộ xương người và ba phần chính (sơ đồ)')


def arm(b, sx, sy, theta, bic_contract, label):
    """Cánh tay nhìn nghiêng; phía trước là bên phải. theta: góc gập của cẳng tay (0 = duỗi thẳng)."""
    ex, ey = sx, sy + 90
    L2 = 90
    fx, fy = ex + L2 * math.sin(math.radians(theta)), ey + L2 * math.cos(math.radians(theta))
    # cơ nhị đầu (phía trước), tam đầu (phía sau)
    def muscle(x1, y1, x2, y2, bulge, col):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        ln = math.hypot(x2 - x1, y2 - y1)
        return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f %.1f %.1f)" fill="%s" stroke="%s" stroke-width="2.2"/>' % (mx, my, ln / 2 * 0.8, bulge, ang, mx, my, col, INK)
    ix, iy = ex + 18 * math.sin(math.radians(theta)) + 9 * math.cos(math.radians(theta)), ey + 18 * math.cos(math.radians(theta)) - 9 * math.sin(math.radians(theta))
    px, py = ex - 10 * math.cos(math.radians(theta)), ey + 10 * math.sin(math.radians(theta))
    # xương
    b.append(bone(sx, sy, ex, ey, w=12))
    b.append(bone(ex, ey, fx, fy, w=10))
    b.append(C(ex, ey, 9, fill='#e8e0c8', stroke=INK, w=2)); b.append(C(sx, sy, 10, fill='#e8e0c8', stroke=INK, w=2))
    # cơ nhị đầu: nối vai (sx+16, sy+8) -> điểm bám cẳng tay (ix, iy)
    b1 = (sx + 14, sy + 10)
    if bic_contract:
        b.append(muscle(b1[0], b1[1], b1[0], b1[1] + 44, 14, '#e8787a'))
        b.append(L(b1[0], b1[1] + 44, ix, iy, stroke='#c9b27c', w=3.5))
    else:
        b.append(muscle(b1[0], b1[1], b1[0], b1[1] + 62, 7, '#f2c4c4'))
        b.append(L(b1[0], b1[1] + 62, ix, iy, stroke='#c9b27c', w=3.5))
    # cơ tam đầu: nối vai (sx-14, sy+10) -> mỏm khuỷu (px, py)
    t1 = (sx - 14, sy + 10)
    if bic_contract:
        b.append(muscle(t1[0], t1[1], t1[0], t1[1] + 62, 7, '#cfd9e8'))
        b.append(L(t1[0], t1[1] + 62, px, py, stroke='#c9b27c', w=3.5))
    else:
        b.append(muscle(t1[0], t1[1], t1[0], t1[1] + 44, 14, '#6f8fbf'))
        b.append(L(t1[0], t1[1] + 44, px, py, stroke='#c9b27c', w=3.5))
        return (sx, sy, ex, ey, fx, fy)


def fig_co_xuong():
    b = [title(720, 'Cơ co, dãn làm xương cử động (sơ đồ cánh tay nhìn nghiêng)')]
    for sx_, th_, bc_, lab_ in ((170, 0, False, 'Duỗi tay'), (470, 120, True, 'Co tay (gập khuỷu)')):
        tmp = []
        arm(tmp, sx_, 56, th_, bc_, '')
        b.append('<g transform="translate(%d,56) scale(1.5) translate(%d,-56)">' % (sx_, -sx_) + ''.join(tmp) + '</g>')
        b.append(T(sx_, 366, lab_, size=14, weight='bold'))
    lead(b, 168, 123, 120, 123, 'xương cánh tay', anchor='end')
    lead(b, 172, 191, 120, 191, 'khớp khuỷu', anchor='end')
    lead(b, 170, 262, 120, 262, 'xương cẳng tay', anchor='end')
    lead(b, 162, 106, 64, 70, 'cơ tam đầu', anchor='end') if False else None
    b.append(T(170, 386, 'cơ nhị đầu dãn, cơ tam đầu co', size=13, fill=GREY))
    b.append(T(470, 386, 'cơ nhị đầu co, cơ tam đầu dãn', size=13, fill=GREY))
    lead(b, 168, 120, 60, 120, 'xương cánh tay', anchor='end') if False else lead(b, 156, 150, 60, 150, 'xương cánh tay', anchor='end') if False else None
    b.append(L(320, 50, 320, 390, stroke=GREY, w=1.2, dash='4 4'))
    b.append(T(360, 416, 'Cơ bám vào xương nhờ gân; cơ co làm xương chuyển động quanh khớp', size=13, fill=GREY))
    b.append(R(560, 72, 12, 12, fill='#e8787a', stroke=INK, sw=1.2)); b.append(T(578, 83, 'cơ nhị đầu (trước)', size=12, anchor='start'))
    b.append(R(560, 92, 12, 12, fill='#6f8fbf', stroke=INK, sw=1.2)); b.append(T(578, 103, 'cơ tam đầu (sau)', size=12, anchor='start'))
    return svg(720, 432, ''.join(b))


reg('c-s8-b31-co-xuong.svg', fig_co_xuong, 'sinh8/bai-31/he-van-dong-o-nguoi.json', 2, 'Cơ co dãn làm xương cử động')


def fig_so_cuu_gay_xuong():
    b = [title(720, 'Sơ cứu gãy xương cẳng tay bằng nẹp')]
    ex, wx, y = 120, 560, 130
    b.append(C(ex, y, 26, fill='#fbe3d0', stroke=INK, w=2.4)); b.append(T(ex, y + 48, 'khuỷu tay', size=13, weight='bold'))
    b.append(R(ex, y - 20, wx - ex, 40, fill='#fbe3d0', stroke=INK, sw=2.4, rx=6))
    b.append(R(wx, y - 14, 70, 28, fill='#fbe3d0', stroke=INK, sw=2.4, rx=10)); b.append(T(wx + 35, y + 48, 'bàn tay', size=13, weight='bold'))
    b.append(L(wx, y - 22, wx, y + 22, stroke=GREY, w=1.4, dash='4 3')); b.append(T(wx - 6, y + 48, 'cổ tay', size=13, weight='bold', anchor='end'))
    b.append(PATH('M370,%d l14,-6 l-8,10 l14,-4 l-10,8 z' % (y - 4), fill=RED, stroke=RED, w=1.4))
    b.append(T(380, y + 48, 'chỗ gãy', size=13, weight='bold', fill=RED))
    for dy, nm in ((-34, 'nẹp'), (22, 'nẹp')):
        b.append(R(ex - 10, y + dy, wx - ex + 24, 12, fill='#d9b27c', stroke=INK, sw=2, rx=2))
    for k, x in enumerate((ex + 60, 290, 470)):
        b.append(R(x, y - 36, 16, 74, fill='none', stroke=BLUE, sw=4, rx=3))
    b.append(L(ex - 10, 82, wx + 14, 82, w=1.6)); b.append(L(ex - 10, 76, ex - 10, 88, w=1.6)); b.append(L(wx + 14, 76, wx + 14, 88, w=1.6))
    b.append(T((ex + wx) / 2, 72, 'nẹp dài từ khuỷu đến cổ tay (khoảng 30–40 cm)', size=13, weight='bold'))
    b.append(TL(130, 220, ['1. Đặt tay gãy sát thân nạn nhân', '2. Đặt hai nẹp ở hai phía cẳng tay, lót bông/gạc'], size=13, anchor='start', lh=20))
    b.append(TL(420, 220, ['3. Buộc cố định nẹp (dây buộc xanh)', '4. Đưa nạn nhân đến cơ sở y tế'], size=13, anchor='start', lh=20))
    return svg(720, 262, ''.join(b))


reg('c-s8-b31-so-cuu-nep.svg', fig_so_cuu_gay_xuong, 'sinh8/bai-31/he-van-dong-o-nguoi.json', 6, 'Sơ cứu gãy xương cẳng tay (sơ đồ)')


# ---------- Bài 32: tiêu hoá ----------
def fig_he_tieu_hoa():
    b = [title(720, 'Hệ tiêu hoá ở người (sơ đồ)')]
    cx = 330
    pink, tube = '#f3b8b0', '#d98c82'
    # ống tiêu hoá
    b.append(ELL(cx, 56, 30, 14, fill='#f2a3a0', stroke=INK, w=2.4)); b.append(L(cx - 14, 56, cx + 14, 56, stroke=INK, w=2))
    for dx in (-52, 52):
        b.append(ELL(cx + dx, 66, 14, 9, fill='#e9d28c', stroke=INK, w=2))
    b.append(L(cx, 72, cx, 160, stroke=INK, w=15)); b.append(L(cx, 72, cx, 160, stroke=pink, w=11))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (
        cx - 6, 156, cx - 14, 190, cx - 4, 240, cx + 40, 246, cx + 82, 250, cx + 92, 206, cx + 56, 192,
        cx + 34, 184, cx + 20, 170, cx + 8, 156), fill='#f2a58f', stroke=INK, w=2.6))
    # gan, túi mật
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx - 104, 168, cx - 70, 150, cx - 20, 158, cx - 6, 176,
                                                                    cx - 20, 208, cx - 80, 222, cx - 110, 200), fill='#a2522f', stroke=INK, w=2.4))
    b.append(ELL(cx - 36, 214, 8, 12, fill='#7fbf6a', stroke=INK, w=1.8))
    # tuỵ
    b.append(ELL(cx + 12, 262, 52, 9, fill='#f0d98a', stroke=INK, w=2))
    # ruột non
    pts = []
    for k in range(7):
        y = 280 + k * 12
        pts += [(cx - 36, y), (cx + 36, y)] if k % 2 == 0 else [(cx + 36, y), (cx - 36, y)]
    b.append(PL(pts, stroke=INK, w=13)); b.append(PL(pts, stroke='#f4a9b0', w=9))
    # ruột già
    big = [(cx + 66, 380), (cx + 66, 270), (cx - 66, 270), (cx - 66, 372), (cx - 30, 386), (cx - 4, 396)]
    b.append(PL(big, stroke=INK, w=19)); b.append(PL(big, stroke='#d9b98a', w=14))
    b.append(C(cx - 4, 400, 6, fill='#7d5a3a', stroke=INK, w=1.6))
    b.append(C(cx + 66, 388, 11, fill='#d9b98a', stroke=INK, w=2))
    # chú thích
    lead(b, cx - 30, 52, 110, 40, 'miệng', anchor='end') if False else lead(b, cx - 30, 54, 150, 42, 'miệng', anchor='end')
    lead(b, cx - 52, 68, 150, 66, 'tuyến nước bọt', anchor='end')
    lead(b, cx - 6, 86, 150, 90, 'hầu', anchor='end')
    lead(b, cx - 6, 134, 150, 124, 'thực quản', anchor='end')
    lead(b, cx - 80, 180, 150, 168, 'gan', anchor='end')
    lead(b, cx - 36, 218, 150, 206, 'túi mật', anchor='end')
    lead(b, cx + 80, 230, 540, 214, 'dạ dày', anchor='start')
    lead(b, cx + 40, 262, 540, 258, 'tuỵ', anchor='start')
    lead(b, cx + 30, 320, 540, 318, 'ruột non', anchor='start')
    lead(b, cx + 66, 350, 540, 356, 'ruột già', anchor='start')
    lead(b, cx - 4, 400, 540, 404, 'hậu môn', anchor='start')
    return svg(720, 424, ''.join(b))


reg('c-s8-b32-he-tieu-hoa.svg', fig_he_tieu_hoa, 'sinh8/bai-32/dinh-duong-va-tieu-hoa.json', 1, 'Ống tiêu hoá và các tuyến tiêu hoá (sơ đồ)')


def fig_tieu_hoa_tung_doan():
    b = [title(720, 'Biến đổi thức ăn ở từng đoạn của ống tiêu hoá')]
    cols = ['#f9d9d6', '#fbe3c8', '#dcebc9', '#e2d6f0']
    heads = ['Miệng', 'Dạ dày', 'Ruột non', 'Ruột già']
    bodies = [['Cơ học: nhai, nghiền,', 'đảo trộn thức ăn', 'Hoá học: enzyme amylase', 'biến đổi một phần', 'tinh bột chín'],
              ['Co bóp dạ dày', 'Dịch vị: hydrochloric', 'acid, pepsin, lipase', 'biến đổi một phần', 'protein'],
              ['Dịch tuỵ, dịch mật,', 'dịch ruột biến đổi', 'chất dinh dưỡng thành', 'chất đơn giản', 'Hấp thụ chủ yếu ở đây'],
              ['Hấp thụ lại nước', 'Tạo phân', '', '', '']]
    for i in range(4):
        x = 10 + i * 178
        b.append(R(x, 50, 166, 200, fill=cols[i], stroke=INK, sw=2, rx=10))
        b.append(T(x + 83, 78, heads[i], size=16, weight='bold'))
        b.append(L(x + 14, 90, x + 152, 90, stroke=INK, w=1))
        b.append(TL(x + 83, 114, [t for t in bodies[i] if t], size=12.5, lh=21))
        if i < 3:
            b.append(L(x + 168, 150, x + 176, 150, stroke=INK, w=2.4, arrow=True))
    b.append(T(360, 278, 'Thức ăn đi theo ống tiêu hoá từ miệng đến hậu môn', size=13, fill=GREY))
    return svg(720, 296, ''.join(b))


reg('c-s8-b32-tung-doan.svg', fig_tieu_hoa_tung_doan, 'sinh8/bai-32/dinh-duong-va-tieu-hoa.json', 4, 'Biến đổi thức ăn ở miệng, dạ dày, ruột non, ruột già')


# ---------- Bài 33: máu và tuần hoàn ----------
def rbc(x, y, r=11):
    return C(x, y, r, fill='#e15759', stroke=INK, w=1.6) + C(x, y, r * 0.38, fill='#f1a3a4', stroke='none', w=0)


def wbc(x, y, r=14):
    return C(x, y, r, fill='#f4f1ff', stroke=INK, w=1.6) + PATH('M%.1f,%.1f q-6,-8 4,-9 q10,0 6,9 q-4,6 -10,0 z' % (x - 3, y + 1), fill='#8e6fc4', stroke=INK, w=1)


def plt(x, y):
    return POLY([(x, y - 5), (x + 6, y - 1), (x + 3, y + 5), (x - 4, y + 4), (x - 6, y - 2)], fill='#e8a33a', stroke=INK, sw=1.2)


def fig_thanh_phan_mau():
    b = [title(720, 'Thành phần của máu')]
    b.append(PATH('M110,60 L110,260 A30,30 0 0 0 170,260 L170,60', stroke=INK, w=3))
    b.append(R(112, 100, 56, 118, fill='#fbe7a0', stroke='none', sw=0)); b.append(R(112, 100, 56, 118, fill='#fbe7a0', stroke='none', sw=0))
    b.append('<path d="M112,218 L112,260 A28,28 0 0 0 168,260 L168,218 Z" fill="#c0383c"/>')
    b.append(L(110, 218, 170, 218, stroke=INK, w=1.6, dash='4 3'))
    b.append(T(140, 160, '55%', size=15, weight='bold')); b.append(T(140, 266, '45%', size=15, weight='bold', fill='white'))
    b.append(L(176, 160, 250, 130, stroke=GREY, w=1.4)); b.append(L(176, 255, 250, 255, stroke=GREY, w=1.4))
    b.append(T(256, 120, 'Huyết tương', size=16, weight='bold', anchor='start'))
    b.append(T(256, 140, 'chủ yếu là nước: giúp máu lỏng,', size=12.5, anchor='start')); b.append(T(256, 157, 'vận chuyển các chất', size=12.5, anchor='start'))
    b.append(T(256, 236, 'Tế bào máu', size=16, weight='bold', anchor='start'))
    items = [(rbc, 'Hồng cầu', 'vận chuyển O₂ và CO₂'), (wbc, 'Bạch cầu', 'bảo vệ cơ thể'), (plt, 'Tiểu cầu', 'tham gia làm đông máu')]
    for k, (fn, nm, f) in enumerate(items):
        y = 268 + k * 34
        b.append(fn(276, y))
        b.append(T(300, y - 1, nm, size=14, weight='bold', anchor='start')); b.append(T(390, y - 1, f, size=12.5, anchor='start', fill='#3b4856'))
    b.append(T(110, 30, '', size=10))
    return svg(720, 360, ''.join(b))


reg('c-s8-b33-thanh-phan-mau.svg', fig_thanh_phan_mau, 'sinh8/bai-33/mau-va-he-tuan-hoan.json', 0, 'Thành phần của máu (tỉ lệ gần đúng)')


def antibody_panel(b, x0, match):
    cx = x0 + 160
    ty, sp = 168, 30
    col = '#4e79a7'
    # thân và hai nhánh chữ Y
    b.append(L(cx, 262, cx, 206, stroke=col, w=9))
    for sgn in (-1, 1):
        b.append(L(cx, 206, cx + sgn * sp, ty + 4, stroke=col, w=9))
        tx = cx + sgn * sp
        b.append(PATH('M%d,%d L%d,%d L%d,%d L%d,%d L%d,%d L%d,%d L%d,%d Z' % (tx - 14, ty + 6, tx - 14, ty - 12, tx - 6, ty - 12, tx, ty - 2, tx + 6, ty - 12, tx + 14, ty - 12, tx + 14, ty + 6), fill=col, stroke=INK, w=1.6))
    # mầm bệnh và kháng nguyên
    top = ty - 12 if match else ty - 30
    b.append(R(cx - 74, top - 40, 148, 36 if match else 40, fill='#e9c6d5', stroke=INK, sw=2.2, rx=16)) if False else None
    b.append(R(cx - 74, ty - 58 if match else ty - 76, 148, 46 if match else 46, fill='#e9c6d5', stroke=INK, sw=2.2, rx=16))
    b.append(T(cx, (ty - 30) if match else (ty - 48), 'mầm bệnh', size=12.5, weight='bold'))
    for sgn in (-1, 1):
        tx = cx + sgn * sp
        if match:
            b.append(POLY([(tx - 8, ty - 12), (tx + 8, ty - 12), (tx, ty - 2)], fill=RED, stroke=INK, sw=1.6))
        else:
            b.append(R(tx - 8, ty - 28, 16, 14, fill='#8e6fc4', stroke=INK, sw=1.6))
    b.append(T(cx, 286, 'Kháng nguyên vừa khít với kháng thể' if match else 'Kháng nguyên không khớp với kháng thể', size=13, weight='bold', fill=GREEN if match else RED))
    b.append(T(cx, 304, '→ có liên kết, tiêu diệt mầm bệnh' if match else '→ không liên kết được', size=12.5, fill='#3b4856'))
    b.append(T(cx + 56, 236, 'kháng thể', size=13, weight='bold', fill=col, anchor='start'))
    if match:
        b.append(T(cx + 56, ty - 74 + 0, 'kháng nguyên', size=13, weight='bold', fill=RED, anchor='start')) if False else b.append(T(cx + 86, 128, 'kháng nguyên', size=12.5, weight='bold', fill=RED, anchor='start')) if False else None
    return


def fig_khang_nguyen_khang_the():
    b = [title(720, 'Kháng nguyên – kháng thể: cơ chế chìa khoá – ổ khoá')]
    antibody_panel(b, 20, True)
    antibody_panel(b, 380, False)
    b.append(L(360, 50, 360, 312, stroke=GREY, w=1.2, dash='4 4'))
    b.append(TL(360, 334, ['Kháng thể (protein do tế bào lympho B tạo ra) chỉ liên kết với kháng nguyên tương ứng', 'Tế bào lympho B nhớ giúp cơ thể đáp ứng nhanh khi mầm bệnh xâm nhập lại'], size=12.5, lh=18, fill=GREY))
    return svg(720, 376, ''.join(b))


reg('c-s8-b33-khang-the.svg', fig_khang_nguyen_khang_the, 'sinh8/bai-33/mau-va-he-tuan-hoan.json', 2, 'Kháng thể liên kết với kháng nguyên theo cơ chế chìa khoá – ổ khoá (sơ đồ)')


def fig_nhom_mau():
    b = [title(720, 'Hệ nhóm máu ABO và nguyên tắc truyền máu')]
    # bảng trái
    x0, y0 = 10, 52
    cw = [70, 130, 120]
    heads = ['Nhóm máu', 'Kháng nguyên', 'Kháng thể']
    x = x0
    for w, h in zip(cw, heads):
        b.append(R(x, y0, w, 34, fill=LBLUE, stroke=INK, sw=1.6)); b.append(T(x + w / 2, y0 + 22, h, size=12.5, weight='bold')); x += w
    rows = [('A', 'A', 'β', '#f8d7d4'), ('B', 'B', 'α', '#d9e7f5'), ('AB', 'A và B', 'không có', '#e7dcf0'), ('O', 'không có', 'α và β', '#f6efc9')]
    for i, (g, a, k, col) in enumerate(rows):
        y = y0 + 34 + i * 40
        x = x0
        for w, t in zip(cw, (g, a, k)):
            b.append(R(x, y, w, 40, fill=col, stroke=INK, sw=1.6)); b.append(T(x + w / 2, y + 25, t, size=14 if t == g else 13, weight='bold' if t == g else 'normal')); x += w
    b.append(T(165, 270, 'Kháng nguyên trên hồng cầu; kháng thể trong huyết tương', size=11.5, fill=GREY))
    # ma trận truyền máu
    gx, gy = 400, 80
    groups = ['A', 'B', 'AB', 'O']
    b.append(T(gx + 130, 60, 'Người nhận', size=13, weight='bold'))
    b.append(R(gx - 58, gy - 10, 54, 30, fill='white', stroke=INK, sw=1.6)); b.append(T(gx - 31, gy + 4, 'Cho ↓', size=10.5, weight='bold')); b.append(T(gx - 31, gy + 16, 'Nhận →', size=10.5, weight='bold'))
    for j, g in enumerate(groups):
        b.append(R(gx + j * 58, gy - 10, 54, 30, fill=LBLUE, stroke=INK, sw=1.6)); b.append(T(gx + j * 58 + 27, gy + 11, g, size=14, weight='bold'))
    ok = {'A': {'A', 'AB'}, 'B': {'B', 'AB'}, 'AB': {'AB'}, 'O': {'A', 'B', 'AB', 'O'}}
    for i, d in enumerate(groups):
        b.append(R(gx - 58, gy + 24 + i * 40, 54, 36, fill=LBLUE, stroke=INK, sw=1.6)); b.append(T(gx - 31, gy + 48 + i * 40, d, size=14, weight='bold'))
        for j, r in enumerate(groups):
            good = r in ok[d]
            b.append(R(gx + j * 58, gy + 24 + i * 40, 54, 36, fill='#d6e8cb' if good else '#fadcdc', stroke=INK, sw=1.4))
            b.append(T(gx + j * 58 + 27, gy + 48 + i * 40, '✓' if good else '✗', size=18, weight='bold', fill=GREEN if good else RED))
    b.append(T(gx + 116, 282, '✓ truyền được (không bị kết dính); ✗ không truyền', size=11.5, fill=GREY))
    b.append(T(360, 312, 'Nên truyền máu cùng nhóm; nếu khác nhóm thì kháng thể của người nhận', size=12.5, fill='#3b4856'))
    b.append(T(360, 330, 'không được gây kết dính kháng nguyên của máu người cho', size=12.5, fill='#3b4856'))
    return svg(720, 348, ''.join(b))


reg('c-s8-b33-nhom-mau.svg', fig_nhom_mau, 'sinh8/bai-33/mau-va-he-tuan-hoan.json', 4, 'Nhóm máu ABO và các trường hợp truyền máu')


def fig_tuan_hoan():
    b = [title(720, 'Vòng tuần hoàn lớn và vòng tuần hoàn nhỏ')]
    BL, RD = '#3f6fb5', '#d4393d'
    # tim
    hx, hy = 300, 120
    for (dx, dy, col, nm) in ((0, 0, BL, 'nhĩ phải'), (60, 0, RD, 'nhĩ trái'), (0, 56, BL, 'thất phải'), (60, 56, RD, 'thất trái')):
        b.append(R(hx + dx, hy + dy, 60, 56, fill=col, stroke=INK, sw=2.4, rx=6)); b.append(TL(hx + dx + 30, hy + dy + 26, nm.split(), size=12.5, lh=15, fill='white', weight='bold'))
    # phổi (trái) và cơ thể (phải)
    b.append(R(30, 100, 130, 60, fill='#cfe9f1', stroke=INK, sw=2.2, rx=10)); b.append(TL(95, 126, ['Mao mạch phổi', '(trao đổi khí)'], size=13, lh=17, weight='bold'))
    b.append(R(560, 100, 140, 60, fill='#f9d9d6', stroke=INK, sw=2.2, rx=10)); b.append(TL(630, 126, ['Mao mạch', 'các cơ quan'], size=13, lh=17, weight='bold'))
    # tuần hoàn nhỏ: thất phải -> phổi (xanh) ; phổi -> nhĩ trái (đỏ)
    b.append(PLA([(hx, hy + 84), (95, hy + 84), (95, 162)], stroke=BL, w=3.4))
    b.append(PLA([(95, 98), (95, 60), (hx + 90, 60), (hx + 90, hy)], stroke=RD, w=3.4))
    # tuần hoàn lớn: thất trái -> cơ quan (đỏ); cơ quan -> nhĩ phải (xanh)
    b.append(PLA([(hx + 120, hy + 84), (630, hy + 84), (630, 162)], stroke=RD, w=3.4))
    b.append(PLA([(630, 98), (630, 44), (hx + 30, 44), (hx + 30, hy)], stroke=BL, w=3.4)) if False else None
    b.append(PLA([(630, 98), (630, 52), (hx + 16, 52), (hx + 16, hy)], stroke=BL, w=3.4))
    b.append(H(120, 190, 'Động mạch phổi', size=12, fill=BL, anchor='start'))
    b.append(H(110, 52, 'Tĩnh mạch phổi', size=12, fill=RD, anchor='start')) if False else None
    b.append(H(190, 78, 'Tĩnh mạch phổi', size=12, fill=RD, anchor='start')) if False else None
    b.append(T(190, 54, 'Tĩnh mạch phổi', size=12, fill=RD, anchor='start'))
    b.append(T(520, 74, 'Tĩnh mạch chủ', size=12, fill=BL, anchor='end')) if False else b.append(T(430, 46, 'Tĩnh mạch chủ', size=12, fill=BL, anchor='start'))
    b.append(T(500, 218, 'Động mạch chủ', size=12, fill=RD, anchor='start'))
    b.append(T(95, 236, 'Tuần hoàn nhỏ: thất phải → phổi → nhĩ trái', size=13, weight='bold', fill=BLUE)) if False else None
    b.append(T(180, 256, 'Vòng tuần hoàn nhỏ: tâm thất phải → phổi → tâm nhĩ trái', size=13, weight='bold', anchor='start'))
    b.append(T(180, 276, 'Vòng tuần hoàn lớn: tâm thất trái → cơ quan → tâm nhĩ phải', size=13, weight='bold', anchor='start'))
    b.append(R(120, 292, 12, 12, fill=RD, stroke=INK, sw=1)); b.append(T(138, 303, 'máu giàu O₂', size=12, anchor='start'))
    b.append(R(250, 292, 12, 12, fill=BL, stroke=INK, sw=1)); b.append(T(268, 303, 'máu giàu CO₂', size=12, anchor='start'))
    return svg(720, 320, ''.join(b))


reg('c-s8-b33-tuan-hoan.svg', fig_tuan_hoan, 'sinh8/bai-33/mau-va-he-tuan-hoan.json', 6, 'Sơ đồ hai vòng tuần hoàn')


# ---------- Bài 34: hô hấp ----------
def fig_he_ho_hap():
    b = [title(720, 'Hệ hô hấp ở người (sơ đồ)')]
    cx = 300
    # mũi + khoang mũi
    b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d' % (cx - 30, 78, cx - 12, 40, cx + 14, 52, cx + 46, 56, cx + 40, 84), fill='#f6d7c3', stroke=INK, w=2.4))
    b.append(L(cx, 66, cx, 100, stroke=INK, w=13)); b.append(L(cx, 66, cx, 100, stroke='#f3b8b0', w=9))
    # họng, thanh quản, khí quản
    b.append(R(cx - 14, 100, 28, 26, fill='#f3b8b0', stroke=INK, sw=2, rx=6))
    b.append(R(cx - 11, 126, 22, 20, fill='#e9d28c', stroke=INK, sw=2, rx=4))
    b.append(L(cx, 146, cx, 214, stroke=INK, w=17)); b.append(L(cx, 146, cx, 214, stroke='#cfe0f0', w=13))
    for yy in range(150, 214, 8):
        b.append(L(cx - 7, yy, cx + 7, yy, stroke=INK, w=1.2))
    # phổi
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx - 16, 214, cx - 70, 200, cx - 132, 226, cx - 128, 290,
                                                                                      cx - 126, 350, cx - 80, 372, cx - 44, 366, cx - 12, 362, cx - 8, 300, cx - 16, 214), fill='#f4c6c6', stroke=INK, w=2.6))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx + 16, 214, cx + 70, 200, cx + 130, 226, cx + 124, 290,
                                                                                      cx + 122, 346, cx + 80, 368, cx + 50, 362, cx + 38, 330, cx + 12, 330, cx + 8, 290), fill='#f4c6c6', stroke=INK, w=2.6)) if False else None
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d L%d,%d C%d,%d %d,%d %d,%d Z' % (cx + 16, 214, cx + 70, 200, cx + 128, 226, cx + 124, 290,
                                                                                                cx + 122, 346, cx + 82, 372, cx + 46, 366, cx + 38, 330, cx + 10, 322, cx + 10, 300, cx + 8, 290), fill='#f4c6c6', stroke=INK, w=2.6)) if False else None
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx + 16, 214, cx + 70, 200, cx + 128, 226, cx + 124, 290,
                                                                                      cx + 122, 350, cx + 80, 372, cx + 44, 366, cx + 12, 362, cx + 8, 300, cx + 16, 214), fill='#f4c6c6', stroke=INK, w=2.6))
    # phế quản
    for sgn in (-1, 1):
        b.append(PL([(cx, 214), (cx + sgn * 34, 238), (cx + sgn * 62, 272)], stroke=INK, w=10)); b.append(PL([(cx, 214), (cx + sgn * 34, 238), (cx + sgn * 62, 272)], stroke='#cfe0f0', w=6))
        b.append(PL([(cx + sgn * 34, 238), (cx + sgn * 78, 236), (cx + sgn * 100, 250)], stroke=INK, w=6)); b.append(PL([(cx + sgn * 34, 238), (cx + sgn * 78, 236), (cx + sgn * 100, 250)], stroke='#cfe0f0', w=3))
        b.append(PL([(cx + sgn * 62, 272), (cx + sgn * 66, 312), (cx + sgn * 80, 330)], stroke=INK, w=5)); b.append(PL([(cx + sgn * 62, 272), (cx + sgn * 66, 312), (cx + sgn * 80, 330)], stroke='#cfe0f0', w=2.4))
    lead(b, cx + 40, 62, 470, 56, 'mũi', anchor='start')
    lead(b, cx + 14, 112, 470, 104, 'họng', anchor='start')
    lead(b, cx + 11, 136, 470, 146, 'thanh quản', anchor='start')
    lead(b, cx + 8, 176, 470, 190, 'khí quản', anchor='start')
    lead(b, cx + 50, 255, 470, 250, 'phế quản', anchor='start')
    lead(b, cx + 100, 310, 470, 318, 'phổi (phải và trái)', anchor='start')
    b.append(T(cx - 160, 130, 'Đường dẫn khí', size=14, weight='bold', fill=BLUE, anchor='end'))
    b.append(PATH('M%d,%d L%d,%d L%d,%d' % (cx - 150, 54, cx - 142, 54, cx - 142, 232), stroke=BLUE, w=2)) if False else None
    b.append(T(cx - 160, 150, '(mũi, họng, thanh quản,', size=12, fill='#3b4856', anchor='end')); b.append(T(cx - 160, 166, 'khí quản, phế quản)', size=12, fill='#3b4856', anchor='end'))
    return svg(720, 392, ''.join(b))


reg('c-s8-b34-he-ho-hap.svg', fig_he_ho_hap, 'sinh8/bai-34/he-ho-hap-o-nguoi.json', 0, 'Các cơ quan của hệ hô hấp (sơ đồ)')


def fig_thong_khi():
    b = [title(720, 'Cử động hô hấp làm thay đổi thể tích lồng ngực')]
    for k, (cx, name, inhale) in enumerate(((190, 'Hít vào', True), (530, 'Thở ra', False))):
        w = 130 if inhale else 104
        h = 130 if inhale else 108
        top, left = 70, cx - w / 2
        b.append(R(left, top, w, h, fill='#fbf0c9', stroke=INK, sw=3, rx=24))
        b.append(R(left + 10, top + 8, w - 20, h - 26 if inhale else h - 30, fill='#f4c6c6', stroke=INK, sw=2, rx=18))
        # cơ hoành
        yb = top + h
        if inhale:
            b.append(PATH('M%d,%d Q%d,%d %d,%d' % (left - 4, yb - 4, cx, yb + 8, left + w + 4, yb - 4), stroke='#8a5a2b', w=5))
        else:
            b.append(PATH('M%d,%d Q%d,%d %d,%d' % (left - 4, yb + 4, cx, yb - 26, left + w + 4, yb + 4), stroke='#8a5a2b', w=5))
        # mũi tên không khí
        if inhale:
            b.append(L(cx, 36, cx, top + 18, stroke=BLUE, w=3.2, arrow=True))
            b.append(L(left - 10, top + h / 2, left - 40, top + h / 2, stroke=ORANGE, w=3, arrow=True))
            b.append(L(left + w + 10, top + h / 2, left + w + 40, top + h / 2, stroke=ORANGE, w=3, arrow=True))
            b.append(L(cx, yb + 14, cx, yb + 50, stroke=ORANGE, w=3, arrow=True))
        else:
            b.append(L(cx, top + 18, cx, 36, stroke=RED, w=3.2, arrow=True))
            b.append(L(left - 40, top + h / 2, left - 10, top + h / 2, stroke=ORANGE, w=3, arrow=True))
            b.append(L(left + w + 40, top + h / 2, left + w + 10, top + h / 2, stroke=ORANGE, w=3, arrow=True))
            b.append(L(cx, yb + 50, cx, yb + 12, stroke=ORANGE, w=3, arrow=True))
        b.append(T(cx, top + h / 2 + 4, 'phổi', size=14, weight='bold'))
        b.append(T(cx, 250, name, size=16, weight='bold'))
    b.append(TL(190, 276, ['Cơ liên sườn co: xương sườn nâng lên;', 'cơ hoành co: hạ xuống → thể tích lồng ngực tăng,', 'không khí vào phổi'], size=12.5, lh=18))
    b.append(TL(530, 276, ['Cơ liên sườn dãn: xương sườn hạ xuống;', 'cơ hoành dãn: vòm lên → thể tích lồng ngực giảm,', 'không khí ra khỏi phổi'], size=12.5, lh=18))
    b.append(T(190, 358 - 8, '↑ mũi tên cam: chiều thay đổi kích thước lồng ngực', size=11.5, fill=GREY)) if False else None
    b.append(T(20, 70, '', size=1))
    b.append(H(190 + 66, 66 + 0, '', size=1)) if False else None
    b.append(T(190, 340, 'Đường nâu: cơ hoành; mũi tên cam: lồng ngực nở ra / thu lại', size=12, fill=GREY)) if False else None
    b.append(T(360, 344, 'Đường nâu ở đáy: cơ hoành. Mũi tên cam: lồng ngực nở rộng (hít vào) hoặc thu hẹp (thở ra)', size=12, fill=GREY))
    return svg(720, 362, ''.join(b))


reg('c-s8-b34-thong-khi.svg', fig_thong_khi, 'sinh8/bai-34/he-ho-hap-o-nguoi.json', 2, 'Thay đổi thể tích lồng ngực khi hít vào và thở ra (sơ đồ)')


def fig_trao_doi_khi():
    b = [title(720, 'Trao đổi khí ở phổi và ở tế bào (khuếch tán)')]
    BL, RD = '#3f6fb5', '#d4393d'
    # phổi: phế nang + mao mạch
    b.append(T(180, 56, 'Ở phổi', size=15, weight='bold'))
    b.append(C(180, 134, 58, fill='#fdeaea', stroke=INK, w=3))
    b.append(T(180, 138, 'phế nang', size=13, weight='bold'))
    b.append(PATH('M60,220 C100,240 140,214 180,224 C220,234 260,214 300,230', stroke=INK, w=22)); b.append(PATH('M60,220 C100,240 140,214 180,224 C220,234 260,214 300,230', stroke='#e6b4b4', w=17))
    b.append(T(180, 276, 'mao mạch máu quanh phế nang', size=12.5, fill='#3b4856'))
    b.append(L(146, 198, 146, 226, stroke=ORANGE, w=3.2, arrow=True)); b.append(T(136, 216, 'O₂', size=14, weight='bold', fill=ORANGE, anchor='end'))
    b.append(L(214, 226, 214, 198, stroke=BLUE, w=3.2, arrow=True)); b.append(T(224, 216, 'CO₂', size=14, weight='bold', fill=BLUE, anchor='start'))
    # tế bào
    b.append(T(540, 56, 'Ở tế bào', size=15, weight='bold'))
    b.append(R(450, 90, 180, 100, fill=CELL, stroke=INK, sw=2.6, rx=20)); b.append(T(540, 136, 'tế bào cơ thể', size=13, weight='bold'))
    b.append(PATH('M430,226 C470,206 510,240 550,224 C590,208 630,238 660,224', stroke=INK, w=22)); b.append(PATH('M430,226 C470,206 510,240 550,224 C590,208 630,238 660,224', stroke='#e6b4b4', w=17))
    b.append(T(540, 276, 'mao mạch máu', size=12.5, fill='#3b4856'))
    b.append(L(500, 220, 500, 194, stroke=ORANGE, w=3.2, arrow=True)); b.append(T(490, 212, 'O₂', size=14, weight='bold', fill=ORANGE, anchor='end'))
    b.append(L(580, 194, 580, 220, stroke=BLUE, w=3.2, arrow=True)); b.append(T(590, 212, 'CO₂', size=14, weight='bold', fill=BLUE, anchor='start'))
    b.append(T(180, 306, 'O₂: phế nang → máu; CO₂: máu → phế nang', size=12.5, weight='bold'))
    b.append(T(540, 306, 'O₂: máu → tế bào; CO₂: tế bào → máu', size=12.5, weight='bold'))
    return svg(720, 324, ''.join(b))


reg('c-s8-b34-trao-doi-khi.svg', fig_trao_doi_khi, 'sinh8/bai-34/he-ho-hap-o-nguoi.json', 4, 'Trao đổi khí theo cơ chế khuếch tán')


# ---------- Bài 35: bài tiết ----------
def fig_he_bai_tiet():
    b = [title(720, 'Hệ bài tiết nước tiểu (sơ đồ)')]
    cx = 300
    for sgn in (-1, 1):
        x = cx + sgn * 66
        b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (
            x + sgn * 8, 60, x + sgn * 40, 56, x + sgn * 38, 110, x + sgn * 10, 130, x - sgn * 4, 134, x - sgn * 8, 108, x - sgn * 4, 100,
            x - sgn * 14, 92, x - sgn * 8, 66, x + sgn * 8, 60), fill='#c9625f', stroke=INK, w=2.6))
        b.append(PL([(x - sgn * 4, 104), (cx + sgn * 18, 140), (cx + sgn * 18, 220), (cx + sgn * 8, 236)], stroke=INK, w=7)); b.append(PL([(x - sgn * 4, 104), (cx + sgn * 18, 140), (cx + sgn * 18, 220), (cx + sgn * 8, 236)], stroke='#f0d58a', w=4))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx - 34, 238, cx - 40, 296, cx + 40, 296, cx + 34, 238, cx + 20, 228, cx - 20, 228, cx - 34, 238), fill='#f2e3a0', stroke=INK, w=2.6))
    b.append(L(cx, 292, cx, 350, stroke=INK, w=9)); b.append(L(cx, 292, cx, 350, stroke='#f0d58a', w=5))
    lead(b, cx + 100, 90, 470, 80, 'thận (hai quả)', anchor='start')
    lead(b, cx + 18, 180, 470, 170, 'ống dẫn nước tiểu', anchor='start')
    lead(b, cx + 30, 260, 470, 260, 'bóng đái', anchor='start')
    lead(b, cx, 330, 470, 340, 'ống đái', anchor='start')
    b.append(T(130, 190, 'Nước tiểu được tạo ở thận,', size=12.5, anchor='middle')) if False else None
    b.append(TL(130, 160, ['Nước tiểu hình thành ở thận,', 'theo ống dẫn xuống bóng đái,', 'rồi thải ra ngoài qua ống đái'], size=12.5, lh=18))
    return svg(720, 372, ''.join(b))


reg('c-s8-b35-he-bai-tiet.svg', fig_he_bai_tiet, 'sinh8/bai-35/he-bai-tiet-o-nguoi.json', 1, 'Hệ bài tiết nước tiểu (sơ đồ)')


def fig_don_vi_than():
    b = [title(720, 'Một đơn vị chức năng của thận (sơ đồ)')]
    cx, cy = 150, 150
    b.append(C(cx, cy, 52, fill='#e9f4fb', stroke=INK, w=3))
    # cầu thận: búi mao mạch
    for k in range(5):
        b.append(PATH('M%d,%d c20,-%d 40,%d 0,%d' % (cx - 20, cy + 14 - k * 6, 14 + k, 12 + k, 10 + k), stroke='#c0383c', w=3)) if False else None
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d' % (cx - 22, cy - 18, cx + 6, cy - 34, cx + 28, cy - 10, cx + 8, cy + 2, cx - 20, cy + 14, cx + 18, cy + 28, cx + 20, cy + 18, cx + 30, cy + 8, cx - 4, cy - 8, cx - 22, cy - 6), stroke='#c0383c', w=4))
    # mạch đến/đi
    b.append(PLA([(40, 100), (cx - 30, 120)], stroke='#c0383c', w=4)) if False else None
    b.append(PLA([(30, 112), (cx - 30, 136)], stroke='#c0383c', w=4))
    b.append(L(cx - 30, 168, 30, 196, stroke='#c0383c', w=4)) if False else b.append(PLA([(cx - 18, 168), (30, 200)], stroke='#c0383c', w=4))
    # ống thận
    pts = [(cx + 52, cy)]
    tube = 'M%d,%d C%d,%d %d,%d %d,%d S%d,%d %d,%d S%d,%d %d,%d' % (cx + 52, cy, 260, cy - 40, 270, cy + 60, 340, cy + 20, 330, cy - 50, 420, cy - 20, 440, cy + 60, 520, cy + 50)
    b.append(PATH(tube, stroke=INK, w=16)); b.append(PATH(tube, stroke='#f6e3a8', w=11))
    b.append(PLA([(520, 200), (600, 200)], stroke='#c9a02e', w=4)) if False else None
    b.append(PATH('M520,%d L640,%d' % (cy + 50, cy + 50), stroke=INK, w=16)); b.append(PATH('M520,%d L640,%d' % (cy + 50, cy + 50), stroke='#f6e3a8', w=11))
    b.append(PLA([(640, cy + 50), (690, cy + 50)], stroke='#c9a02e', w=4))
    b.append(T(676, cy + 78, 'nước tiểu', size=12.5, weight='bold', fill='#9b7a1e'))
    lead(b, cx + 30, cy - 6, 40, 250, 'cầu thận (búi mao mạch)', anchor='start') if False else lead(b, cx + 10, cy - 20, 175, 66, 'cầu thận (búi mao mạch)', anchor='start')
    lead(b, cx + 44, cy - 34, 60, 60, 'nang cầu thận', anchor='end') if False else lead(b, cx - 44, cy - 30, 100, 56, 'nang cầu thận', anchor='end')
    lead(b, 340, cy + 20, 360, 232, 'ống thận', anchor='start')
    b.append(T(75, 130, 'máu vào', size=12, fill='#c0383c', anchor='middle')) if False else b.append(T(60, 104, 'máu vào', size=12, weight='bold', fill='#c0383c'))
    b.append(T(54, 222, 'máu ra', size=12, weight='bold', fill='#c0383c'))
    b.append(TL(520, 70, ['Máu qua cầu thận: nước và các chất', 'nhỏ lọt qua màng lọc vào nang cầu thận', '(màng lọc có lỗ nhỏ 30–40 Å)'], size=12, lh=17, fill='#3b4856')) if False else None
    b.append(TL(380, 300, ['Máu qua cầu thận, màng lọc có lỗ nhỏ (30–40 Å) giữ lại các phần tử lớn;', 'phần được lọc vào nang cầu thận, chảy qua ống thận tạo thành nước tiểu'], size=12.5, lh=18, fill='#3b4856'))
    return svg(720, 330, ''.join(b))


reg('c-s8-b35-don-vi-than.svg', fig_don_vi_than, 'sinh8/bai-35/he-bai-tiet-o-nguoi.json', 2, 'Đơn vị chức năng của thận (sơ đồ)')


# ---------- Bài 36: môi trường trong ----------
def fig_moi_truong_trong():
    b = [title(720, 'Môi trường trong của cơ thể: máu, nước mô và bạch huyết')]
    b.append(R(20, 120, 680, 120, fill='#e4f1f7', stroke='none', sw=0, rx=14))
    b.append(T(28, 140, 'Nước mô', size=14, weight='bold', fill=BLUE, anchor='start'))
    # mao mạch máu (trên)
    b.append(R(20, 52, 680, 46, fill='#f2b5b5', stroke=INK, sw=2.4, rx=23)); b.append(T(360, 82, 'Máu (trong mao mạch máu)', size=14, weight='bold'))
    # tế bào (dưới)
    for k, x in enumerate((120, 250, 380)):
        b.append(ELL(x, 215, 46, 26, fill=CELL, stroke=INK, w=2.2)); b.append(ELL(x, 215, 12, 9, fill=NUC, stroke=INK, w=1.4))
    b.append(T(250, 262, 'tế bào', size=13, weight='bold'))
    # mao mạch bạch huyết
    b.append(R(480, 180, 220, 40, fill='#cfe6c4', stroke=INK, sw=2.2, rx=20)); b.append(T(590, 205, 'Bạch huyết', size=14, weight='bold'))
    # mũi tên
    b.append(L(150, 98, 150, 168, stroke=ORANGE, w=3, arrow=True)); b.append(T(160, 126, 'chất dinh dưỡng, O₂', size=12, anchor='start', fill='#9a5d10'))
    b.append(L(330, 168, 330, 98, stroke=BLUE, w=3, arrow=True)); b.append(T(340, 126, 'chất thải, CO₂', size=12, anchor='start', fill=BLUE))
    b.append(L(130, 168, 130, 190, stroke=ORANGE, w=3, arrow=True)) if False else None
    b.append(L(440, 180, 478, 195, stroke=GREEN, w=3, arrow=True)); b.append(T(560, 160, 'nước mô thấm vào', size=12, fill='#2f6b2a')) if False else None
    b.append(T(560, 156, 'nước mô → bạch huyết', size=12, fill='#2f6b2a'))
    b.append(TL(360, 290, ['Các chất trao đổi giữa máu và tế bào qua nước mô;', 'môi trường trong liên hệ với môi trường ngoài qua tiêu hoá, hô hấp, bài tiết, tuần hoàn'], size=12.5, lh=18, fill='#3b4856'))
    return svg(720, 330, ''.join(b))


reg('c-s8-b36-moi-truong-trong.svg', fig_moi_truong_trong, 'sinh8/bai-36/dieu-hoa-moi-truong-trong.json', 0, 'Các thành phần của môi trường trong (sơ đồ)')


def fig_dieu_hoa_muoi():
    b = [title(720, 'Điều hoà nồng độ muối trong máu sau khi ăn mặn')]
    steps = [('Ăn mặn', '#f9d9d6'), ('Nồng độ muối trong máu tăng', '#fbe3c8'), ('Cảm giác khát, uống nhiều nước', '#d3e1f3'), ('Muối được pha loãng; thận thải bớt muối', '#dcebc9'), ('Nồng độ muối trở lại bình thường', '#d6e8cb')]
    pos = [(20, 60), (260, 60), (500, 60), (500, 170), (260, 170)]
    pos = [(20, 60), (260, 60), (500, 60), (500, 180), (260, 180)]
    for (x, y), (t, col) in zip(pos, steps):
        b.append(R(x, y, 200, 70, fill=col, stroke=INK, sw=2, rx=10))
        words = t.split(' ')
        line = ''
        lines = []
        for w in words:
            if len(line + ' ' + w) > 22 and line:
                lines.append(line); line = w
            else:
                line = (line + ' ' + w).strip()
        lines.append(line)
        b.append(TL(x + 100, y + 35 - (len(lines) - 1) * 9 + 4, lines, size=13.5, lh=18, weight='bold'))
    b.append(L(222, 95, 258, 95, w=2.6, arrow=True)); b.append(L(462, 95, 498, 95, w=2.6, arrow=True))
    b.append(L(600, 132, 600, 178, w=2.6, arrow=True)); b.append(L(498, 215, 462, 215, w=2.6, arrow=True))
    b.append(TL(130, 190, ['Cân bằng môi trường trong', 'được duy trì ổn định nhờ các', 'cơ chế điều hoà này'], size=13, lh=19, weight='bold', fill=BLUE))
    return svg(720, 276, ''.join(b))


reg('c-s8-b36-dieu-hoa-muoi.svg', fig_dieu_hoa_muoi, 'sinh8/bai-36/dieu-hoa-moi-truong-trong.json', 5, 'Cơ chế điều hoà nồng độ muối trong máu')


# ---------- Bài 37: thần kinh và giác quan ----------
def fig_he_than_kinh():
    b = [title(720, 'Các bộ phận của hệ thần kinh')]
    b.append(R(250, 44, 220, 44, fill=LYELLOW, stroke=INK, sw=2.4, rx=10)); b.append(T(360, 72, 'Hệ thần kinh', size=16, weight='bold'))
    b.append(PL([(360, 88), (360, 108), (170, 108), (170, 128)], stroke=INK, w=2)); b.append(PL([(360, 108), (550, 108), (550, 128)], stroke=INK, w=2))
    b.append(R(40, 128, 260, 52, fill='#f6d9c2', stroke=INK, sw=2.2, rx=10)); b.append(TL(170, 150, ['Bộ phận trung ương', '(giữ vai trò chủ đạo)'], size=13.5, lh=18, weight='bold'))
    b.append(R(420, 128, 260, 52, fill='#d6e8cb', stroke=INK, sw=2.2, rx=10)); b.append(TL(550, 150, ['Bộ phận ngoại biên'], size=14, lh=18, weight='bold'))
    b.append(PL([(110, 180), (110, 204)], stroke=INK, w=2)); b.append(PL([(230, 180), (230, 204)], stroke=INK, w=2))
    b.append(PL([(480, 180), (480, 204)], stroke=INK, w=2)); b.append(PL([(620, 180), (620, 204)], stroke=INK, w=2))
    for x, y, t, col in ((50, 204, 'Não', '#fbeadc'), (170, 204, 'Tuỷ sống', '#fbeadc'), (420, 204, 'Dây thần kinh', '#e7f1df'), (560, 204, 'Hạch thần kinh', '#e7f1df')):
        b.append(R(x, y, 120, 40, fill=col, stroke=INK, sw=1.8, rx=8)); b.append(T(x + 60, y + 25, t, size=13.5, weight='bold'))
    b.append(T(360, 280, 'Điều khiển, điều hoà và phối hợp hoạt động của các cơ quan thành một thể thống nhất', size=12.5, fill=GREY))
    return svg(720, 298, ''.join(b))


reg('c-s8-b37-he-than-kinh.svg', fig_he_than_kinh, 'sinh8/bai-37/he-than-kinh-va-giac-quan.json', 0, 'Sơ đồ các bộ phận của hệ thần kinh')


def eye_body(b, ex, ey, rx=70, ry=52):
    b.append(ELL(ex, ey, rx, ry, fill='#ffffff', stroke=INK, w=2.6))
    # màng lưới (cung phải)
    b.append(ARC(ex, ey, ry - 4, -50, 50, stroke='#c0383c', w=4)) if False else None
    b.append(PATH('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f' % (ex + rx * 0.56, ey - ry * 0.82, rx, ry, ex + rx * 0.56, ey + ry * 0.82), stroke='#c0383c', w=4))


def fig_mat():
    b = [title(720, 'Cấu tạo của mắt và đường đi của ánh sáng (sơ đồ)')]
    ex, ey = 330, 160
    b.append(ELL(ex, ey, 100, 74, fill='#fdfdfd', stroke=INK, w=3))
    # giác mạc: phần lồi phía trước (trái)
    b.append(PATH('M%d,%d Q%d,%d %d,%d' % (ex - 92, ey - 30, ex - 130, ey, ex - 92, ey + 30), fill='#e4f1f7', stroke=INK, w=3))
    # mống mắt + đồng tử
    b.append(L(ex - 80, ey - 36, ex - 80, ey - 12, stroke='#6b4a2a', w=6)); b.append(L(ex - 80, ey + 12, ex - 80, ey + 36, stroke='#6b4a2a', w=6))
    # thể thuỷ tinh
    b.append(ELL(ex - 60, ey, 16, 32, fill='#cfe6f7', stroke=INK, w=2.4))
    # màng lưới
    b.append(PATH('M%d,%d A100,74 0 0 1 %d,%d' % (ex + 56, ey - 62, ex + 56, ey + 62), stroke='#c0383c', w=5))
    # dây thần kinh thị giác
    b.append(L(ex + 98, ey + 24, ex + 150, ey + 40, stroke='#e9c46a', w=10)); b.append(L(ex + 98, ey + 24, ex + 150, ey + 40, stroke=INK, w=1.2))
    # tia sáng
    for dy in (-20, 0, 20):
        b.append(PL([(ex - 190, ey + dy), (ex - 112, ey + dy), (ex - 60, ey + dy * 0.7), (ex + 52, ey)], stroke=ORANGE, w=2.2))
    b.append(T(ex - 190, ey + 44, 'ánh sáng từ vật', size=12.5, fill='#9a5d10', anchor='start'))
    lead(b, ex - 122, ey - 12, 170, 58, 'giác mạc', anchor='end')
    lead(b, ex - 80, ey - 26, 70, 100, 'đồng tử (lỗ giữa mống mắt)', anchor='start') if False else lead(b, ex - 80, ey - 34, 170, 92, 'mống mắt, đồng tử', anchor='end')
    lead(b, ex - 56, ey + 22, 150, 270, 'thể thuỷ tinh', anchor='end') if False else lead(b, ex - 56, ey + 26, 190, 258, 'thể thuỷ tinh', anchor='end')
    lead(b, ex + 62, ey - 42, 520, 70, 'màng lưới', anchor='start')
    lead(b, ex + 128, ey + 34, 520, 250, 'dây thần kinh thị giác', anchor='start')
    b.append(TL(560, 130, ['Màng lưới có tế bào thụ cảm;', 'xung thần kinh theo dây thị giác', 'về não'], size=12, lh=16, fill='#3b4856')) if False else None
    b.append(T(360, 304, 'Ánh sáng khúc xạ qua giác mạc và thể thuỷ tinh, hội tụ trên màng lưới', size=12.5, fill=GREY))
    return svg(720, 322, ''.join(b))


reg('c-s8-b37-mat.svg', fig_mat, 'sinh8/bai-37/he-than-kinh-va-giac-quan.json', 3, 'Cấu tạo của mắt (sơ đồ)')


def eye_rays(b, ex, ey, f_len, glass=None):
    """Mắt đơn giản: thể thuỷ tinh tại ex-40, màng lưới tại ex+60. f_len: tiêu cự mắt (tính từ thể thuỷ tinh)."""
    lx, rx_ = ex - 40, ex + 60
    b.append(ELL(ex, ey, 78, 50, fill='#ffffff', stroke=INK, w=2.4))
    b.append(ELL(lx, ey, 7, 26, fill='#cfe6f7', stroke=INK, w=2))
    b.append(PATH('M%d,%d Q%d,%d %d,%d' % (rx_ - 4, ey - 34, rx_ + 14, ey, rx_ - 4, ey + 34), stroke='#c0383c', w=4.5))
    h0 = 18
    for sgn in (-1, 0, 1):
        if glass is None:
            start_h, h = sgn * h0, sgn * h0
            pts = [(ex - 104, ey - start_h), (lx, ey - h)]
        else:
            gx, kind = glass
            k_ = (1 / 70 - 1 / 100) if kind == 'phan' else (1 / 135 - 1 / 100)
            s_in = k_ * h0 / (1 - k_ * (lx - gx))
            h = h0 + (lx - gx) * s_in
            hh = sgn * h if sgn else 0
            sl = sgn * s_in if sgn else 0
            pts = [(ex - 104, ey - sgn * h0), (gx, ey - sgn * h0), (lx, ey - hh)]
        h_l = pts[-1][1] - ey
        h_l = -h_l
        # tiêu điểm
        fx = lx + f_len
        # sau thể thuỷ tinh: đường thẳng tới tiêu điểm (cho tia ngoài trục có độ cao hl; với kính: tính bằng cầu nối)
        hl_h = ey - pts[-1][1]  # độ cao trên trục (dương = phía trên)
        if glass is None:
            f_ = f_len
            end_x = rx_ if f_len <= 100 else rx_
            if sgn == 0:
                pts.append((rx_ + 6, ey))
            else:
                t = (rx_ - lx) / f_
                y_end = ey - hl_h * (1 - t)
                if f_ > 100:
                    pts.append((rx_, y_end))
                else:
                    pts.append((lx + f_, ey))
                    pts.append((rx_, ey + (-hl_h) * ((rx_ - lx - f_) / f_)))
        else:
            if sgn == 0:
                pts.append((rx_ + 6, ey))
            else:
                pts.append((rx_, ey))
        b.append(PL(pts, stroke=ORANGE, w=2))
        if glass is None and f_len > 100 and sgn != 0:
            # kéo dài (nét đứt) tới tiêu điểm phía sau màng lưới
            f_ = f_len
            b.append(L(pts[-1][0], pts[-1][1], lx + f_, ey, stroke=ORANGE, w=1.6, dash='3 3'))
    if glass is not None:
        gx, kind = glass
        if kind == 'phan':
            b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d Z' % (gx - 4, ey - 34, gx + 2, ey, gx - 4, ey + 34, gx - 10, ey, gx - 4, ey - 34), fill='#cfe6f7', stroke=INK, w=2)) if False else None
            b.append(PATH('M%d,%d L%d,%d Q%d,%d %d,%d L%d,%d Q%d,%d %d,%d Z' % (gx - 6, ey - 34, gx + 6, ey - 34, gx + 1, ey, gx + 6, ey + 34, gx - 6, ey + 34, gx - 1, ey, gx - 6, ey - 34), fill='#cfe6f7', stroke=INK, w=2))
        else:
            b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d Z' % (gx - 4, ey - 34, gx - 14, ey, gx - 4, ey + 34, gx - 2, ey, gx - 4, ey - 34), fill='#cfe6f7', stroke=INK, w=2)) if False else None
            b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d Z' % (gx, ey - 34, gx + 13, ey, gx, ey + 34, gx - 13, ey, gx, ey - 34), fill='#cfe6f7', stroke=INK, w=2))


def fig_can_vien():
    b = [title(720, 'Cận thị và viễn thị: ảnh của vật xa (sơ đồ)')]
    cols = [130, 370, 610]
    ey1, ey2 = 110, 270
    # hàng 1: không đeo kính
    eye_rays(b, cols[0], ey1, 100)      # bình thường: tiêu điểm tại màng lưới (cách thể thuỷ tinh 100)
    eye_rays(b, cols[1], ey1, 70)       # cận
    eye_rays(b, cols[2], ey1, 135)      # viễn
    for x, nm, sub in ((cols[0], 'Mắt bình thường', 'ảnh rơi đúng màng lưới'), (cols[1], 'Cận thị', 'ảnh ở trước màng lưới'), (cols[2], 'Viễn thị', 'ảnh ở sau màng lưới')):
        b.append(T(x, 188, nm, size=14, weight='bold')); b.append(T(x, 205, sub, size=12, fill=GREY))
    # hàng 2: đeo kính
    b.append(TL(cols[0], ey2 - 6, ['Mắt bình thường', 'không cần đeo kính'], size=13, lh=18, fill='#3b4856'))
    eye_rays(b, cols[1], ey2, 70, glass=(cols[1] - 84, 'phan'))
    eye_rays(b, cols[2], ey2, 135, glass=(cols[2] - 84, 'hoi'))
    for x, nm in ((cols[1], 'Đeo kính phân kì'), (cols[2], 'Đeo kính hội tụ (kính lão)')):
        b.append(T(x, 346, nm, size=13, weight='bold', fill=GREEN)); b.append(T(x, 364, 'ảnh rơi đúng màng lưới', size=12, fill=GREEN))
    b.append(T(cols[1] - 95 + 14, ey2 - 44, 'kính', size=11.5, fill=GREY, anchor='start')) if False else None
    return svg(720, 382, ''.join(b))


reg('c-s8-b37-can-vien.svg', fig_can_vien, 'sinh8/bai-37/he-than-kinh-va-giac-quan.json', 5, 'Cận thị, viễn thị và cách khắc phục (sơ đồ)')


def fig_tai():
    b = [title(720, 'Cấu tạo của tai (sơ đồ)')]
    y = 150
    # tai ngoài
    b.append(PATH('M110,%d C70,%d 60,%d 78,%d C60,%d 90,%d 110,%d' % (y + 20, y - 40, y - 90, y - 100, y + 60, y + 90, y + 40), fill='#f6d7c3', stroke=INK, w=2.6)) if False else None
    b.append(PATH('M130,%d C80,%d 74,%d 100,%d C96,%d 126,%d 138,%d' % (y - 60, y - 80, y + 30, y + 70, y + 100, y + 56, y + 20), fill='#f6d7c3', stroke=INK, w=2.6))
    b.append(L(130, y, 300, y, stroke=INK, w=22)); b.append(L(130, y, 300, y, stroke='#f6d7c3', w=18))
    b.append(L(300, y - 24, 300, y + 24, stroke=INK, w=3.4))  # màng nhĩ
    # tai giữa: chuỗi xương
    b.append(R(306, y - 34, 90, 68, fill='#fdf6e3', stroke=INK, sw=2.2, rx=10))
    b.append(L(304, y - 6, 322, y - 6, stroke='#8a7a55', w=5)); b.append(L(322, y - 6, 350, y - 14, stroke='#8a7a55', w=5)); b.append(L(350, y - 14, 376, y - 2, stroke='#8a7a55', w=5))
    b.append(L(340, y + 34, 360, y + 96, stroke=INK, w=7)); b.append(L(340, y + 34, 360, y + 96, stroke='#f3b8b0', w=4))
    # tai trong: ốc tai
    for k in range(6):
        t = k / 5
        b.append(ARC(450, y - 2, 34 - k * 5, 0 + k * 40, 220 + k * 40, stroke=INK, w=2.4))
    b.append(C(450, y - 2, 4, fill='#c9625f', stroke=INK, w=1))
    b.append(L(484, y + 6, 560, y + 30, stroke='#e9c46a', w=7))
    # sóng âm
    for k in range(3):
        b.append(ARC(40, y, 20 + k * 16, -50, 50, stroke=BLUE, w=2.4))
    b.append(L(0, y, 20, y, stroke=BLUE, w=0.1)) if False else None
    b.append(T(50, y + 70, 'sóng âm', size=12.5, fill=BLUE))
    lead(b, 100, y - 66, 60, 56, 'vành tai', anchor='start') if False else lead(b, 96, y - 50, 40, 60, 'vành tai', anchor='start')
    lead(b, 200, y, 150, 244, 'ống tai', anchor='end') if False else lead(b, 220, y + 12, 220, 258, 'ống tai', anchor='middle')
    lead(b, 300, y - 20, 300, 78, 'màng nhĩ', anchor='middle')
    lead(b, 350, y - 12, 400, 80, 'chuỗi xương tai', anchor='start')
    lead(b, 360, y + 90, 400, 262, 'vòi tai', anchor='start')
    lead(b, 458, y - 30, 480, 100, 'ốc tai', anchor='start')
    lead(b, 540, y + 24, 590, 232, 'dây thần kinh thính giác', anchor='start') if False else lead(b, 540, y + 24, 520, 232, 'dây thần kinh thính giác', anchor='start')
    for x0, x1, nm, col in ((110, 300, 'Tai ngoài', '#f6d7c3'), (300, 400, 'Tai giữa', '#fdf6e3'), (410, 520, 'Tai trong', '#d6e8cb')):
        b.append(R(x0, 290, x1 - x0 - 4, 24, fill=col, stroke=INK, sw=1.6, rx=6)); b.append(T((x0 + x1 - 4) / 2, 307, nm, size=13, weight='bold'))
    return svg(720, 330, ''.join(b))


reg('c-s8-b37-tai.svg', fig_tai, 'sinh8/bai-37/he-than-kinh-va-giac-quan.json', 7, 'Cấu tạo của tai (sơ đồ)')


# ---------- Bài 38: nội tiết ----------
def fig_tuyen_noi_tiet():
    b = [title(720, 'Vị trí các tuyến nội tiết chính (sơ đồ)')]
    cx = 260
    SK = '#f3dccb'
    b.append(ELL(cx, 84, 28, 34, fill=SK, stroke=INK, w=2.4))
    b.append(R(cx - 8, 116, 16, 18, fill=SK, stroke=INK, sw=2))
    b.append(PATH('M%d,%d Q%d,%d %d,%d L%d,%d L%d,%d Q%d,%d %d,%d Z' % (cx - 54, 142, cx - 34, 132, cx, 132, cx + 54, 142, cx + 46, 308, cx, 316, cx - 46, 308), fill=SK, stroke=INK, w=2.4)) if False else None
    b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d L%d,%d L%d,%d Q%d,%d %d,%d L%d,%d Z' % (cx - 8, 134, cx - 50, 136, cx - 62, 156, cx + 50, 136, cx + 62, 156, cx + 56, 330, cx + 40, 330, cx, 336, cx - 40, 330, cx - 56, 330), fill=SK, stroke=INK, w=2.4)) if False else None
    b.append(POLY([(cx - 8, 134), (cx - 62, 146), (cx - 66, 200), (cx - 54, 318), (cx - 40, 340), (cx + 40, 340), (cx + 54, 318), (cx + 66, 200), (cx + 62, 146), (cx + 8, 134)], fill=SK, stroke=INK, sw=2.4))
    # tay, chân (gợi hình)
    b.append(L(cx - 66, 150, cx - 96, 250, stroke=INK, w=14)); b.append(L(cx - 66, 150, cx - 96, 250, stroke=SK, w=10))
    b.append(L(cx + 66, 150, cx + 96, 250, stroke=INK, w=14)); b.append(L(cx + 66, 150, cx + 96, 250, stroke=SK, w=10))
    b.append(L(cx - 24, 340, cx - 30, 420, stroke=INK, w=18)); b.append(L(cx - 24, 340, cx - 30, 420, stroke=SK, w=14))
    b.append(L(cx + 24, 340, cx + 30, 420, stroke=INK, w=18)); b.append(L(cx + 24, 340, cx + 30, 420, stroke=SK, w=14))
    # các tuyến
    b.append(C(cx, 76, 5, fill=RED, stroke=INK, w=1.2))                           # tuyến yên (trong đầu)
    b.append(PATH('M%d,%d q-12,-6 0,-10 q12,4 0,10 z' % (cx, 128), fill='#e08a3c', stroke=INK, w=1.4)); b.append(ELL(cx - 7, 126, 6, 5, fill='#e08a3c', stroke=INK, w=1.2)); b.append(ELL(cx + 7, 126, 6, 5, fill='#e08a3c', stroke=INK, w=1.2))  # giáp
    b.append(ELL(cx + 22, 214, 9, 12, fill='#d4a24a', stroke=INK, w=1.2)) if False else None
    b.append(ELL(cx - 24, 214, 8, 11, fill='#c9a02e', stroke=INK, w=1.4)); b.append(ELL(cx + 24, 214, 8, 11, fill='#c9a02e', stroke=INK, w=1.4))   # trên thận
    b.append(ELL(cx, 208, 26, 7, fill='#f0d98a', stroke=INK, w=1.4))                # tuỵ
    b.append(ELL(cx - 14, 282, 9, 7, fill='#8e6fc4', stroke=INK, w=1.4)); b.append(ELL(cx + 14, 282, 9, 7, fill='#8e6fc4', stroke=INK, w=1.4))     # tuyến sinh dục
    lead(b, cx + 4, 76, 430, 60, 'tuyến yên', anchor='start')
    lead(b, cx + 12, 126, 430, 112, 'tuyến giáp', anchor='start')
    lead(b, cx + 24, 208, 430, 188, 'tuyến trên thận', anchor='start')
    lead(b, cx + 14, 208, 430, 222, 'tuyến tuỵ', anchor='start') if False else lead(b, cx + 20, 205, 430, 154, 'tuyến tuỵ', anchor='start') if False else lead(b, cx + 10, 206, 430, 240, 'tuyến tuỵ', anchor='start')
    lead(b, cx + 18, 284, 430, 290, 'tuyến sinh dục', anchor='start')
    b.append(TL(430, 320, ['(tinh hoàn ở nam, buồng', 'trứng ở nữ; vị trí vẽ minh hoạ)'], size=11.5, lh=15, anchor='start', fill=GREY))
    return svg(720, 444, ''.join(b))


reg('c-s8-b38-tuyen-noi-tiet.svg', fig_tuyen_noi_tiet, 'sinh8/bai-38/he-noi-tiet-o-nguoi.json', 1, 'Vị trí các tuyến nội tiết chính (sơ đồ minh hoạ)')


def fig_insulin_glucagon():
    b = [title(720, 'Điều hoà đường huyết nhờ insulin và glucagon')]
    # trục giữa
    b.append(R(250, 120, 220, 50, fill=LYELLOW, stroke=INK, sw=2.4, rx=10)); b.append(T(360, 150, 'Glucose trong máu', size=15, weight='bold'))
    # trên: tăng
    b.append(R(20, 46, 200, 50, fill='#fbe3c8', stroke=INK, sw=2, rx=10)); b.append(T(120, 76, 'Glucose máu tăng', size=14, weight='bold'))
    b.append(R(250, 38, 220, 50, fill='#f6d7c3', stroke=INK, sw=2, rx=10)); b.append(TL(360, 60, ['Tuyến tuỵ tiết', 'insulin'], size=13.5, lh=17, weight='bold'))
    b.append(R(500, 46, 200, 50, fill='#dcebc9', stroke=INK, sw=2, rx=10)); b.append(TL(600, 66, ['Glucose máu giảm,', 'trở lại bình thường'], size=13, lh=17, weight='bold'))
    b.append(L(222, 71, 248, 66, w=2.4, arrow=True)); b.append(L(472, 66, 498, 71, w=2.4, arrow=True))
    # dưới: giảm
    b.append(R(20, 196, 200, 50, fill='#cfe0f0', stroke=INK, sw=2, rx=10)); b.append(T(120, 226, 'Glucose máu giảm', size=14, weight='bold'))
    b.append(R(250, 204, 220, 50, fill='#e2d6f0', stroke=INK, sw=2, rx=10)); b.append(TL(360, 226, ['Tuyến tuỵ tiết', 'glucagon'], size=13.5, lh=17, weight='bold'))
    b.append(R(500, 196, 200, 50, fill='#dcebc9', stroke=INK, sw=2, rx=10)); b.append(TL(600, 216, ['Glucose máu tăng,', 'trở lại bình thường'], size=13, lh=17, weight='bold'))
    b.append(L(222, 221, 248, 226, w=2.4, arrow=True)); b.append(L(472, 226, 498, 221, w=2.4, arrow=True))
    b.append(T(360, 284, 'Insulin làm giảm đường huyết; glucagon làm tăng đường huyết', size=13, fill=GREY))
    return svg(720, 302, ''.join(b))


reg('c-s8-b38-insulin.svg', fig_insulin_glucagon, 'sinh8/bai-38/he-noi-tiet-o-nguoi.json', 3, 'Insulin và glucagon điều hoà glucose máu')


# ---------- Bài 39: da và thân nhiệt ----------
def fig_cau_tao_da():
    b = [title(720, 'Cấu tạo của da (lát cắt sơ đồ)')]
    x0, x1 = 60, 440
    b.append(R(x0, 70, x1 - x0, 36, fill='#f6c9a6', stroke=INK, sw=2.2))
    b.append(R(x0, 106, x1 - x0, 110, fill='#f4a99a', stroke=INK, sw=2.2))
    b.append(R(x0, 216, x1 - x0, 80, fill='#fbe49b', stroke=INK, sw=2.2))
    for k in range(12):
        b.append(ELL(x0 + 24 + k * 30, 262 + (k % 2) * 8, 11, 9, fill='#f8d56b', stroke='#d9b43c', w=1))
    # lông, cơ dựng lông, tuyến mồ hôi, mạch máu, thụ quan
    b.append(L(200, 100, 200, 60, stroke=INK, w=4)); b.append(L(200, 100, 190, 140, stroke='#5b3a1e', w=6)) if False else None
    b.append(PL([(200, 58), (200, 112), (196, 170)], stroke='#5b3a1e', w=5))
    b.append(ELL(196, 180, 14, 12, fill='#8a5a2b', stroke=INK, w=1.6))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d' % (300, 106, 316, 126, 284, 150, 300, 170, 316, 190, 284, 206, 300, 220), stroke='#2b6cb0', w=3))
    b.append(C(300, 226, 14, fill='#9ec3e8', stroke=INK, w=1.8))
    b.append(PL([(340, 100), (340, 150)], stroke=INK, w=1)) if False else None
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (120, 224, 140, 190, 100, 170, 130, 140), stroke='#c0383c', w=4)); b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (130, 224, 150, 190, 110, 170, 140, 140), stroke='#2b6cb0', w=4)) if False else None
    b.append(C(380, 150, 8, fill='#f9d5a0', stroke=INK, w=1.8))
    lead(b, 440, 88, 480, 70, 'lớp biểu bì', anchor='start') if False else lead(b, 438, 88, 470, 88, 'lớp biểu bì', anchor='start')
    lead(b, 438, 160, 470, 160, 'lớp bì', anchor='start')
    lead(b, 438, 256, 470, 256, 'lớp mỡ dưới da', anchor='start')
    lead(b, 200, 90, 130, 46, 'lông', anchor='end') if False else lead(b, 200, 70, 150, 52, 'lông', anchor='end')
    lead(b, 300, 175, 340, 316, 'tuyến mồ hôi', anchor='middle') if False else lead(b, 300, 226, 330, 318, 'tuyến mồ hôi', anchor='middle')
    lead(b, 126, 190, 60, 318, 'mạch máu', anchor='middle') if False else lead(b, 118, 200, 94, 318, 'mạch máu', anchor='middle')
    lead(b, 380, 150, 370, 318, 'thụ quan', anchor='middle') if False else lead(b, 380, 158, 410, 318, 'thụ quan', anchor='middle')
    b.append(T(360, 346, 'Da: bảo vệ, chống thấm nước, điều hoà thân nhiệt, nhận kích thích, bài tiết mồ hôi', size=12.5, fill=GREY))
    return svg(720, 362, ''.join(b))


reg('c-s8-b39-cau-tao-da.svg', fig_cau_tao_da, 'sinh8/bai-39/da-va-dieu-hoa-than-nhiet.json', 0, 'Cấu tạo của da (sơ đồ)')


def fig_than_nhiet():
    b = [title(720, 'Điều hoà thân nhiệt (bình thường khoảng 37 °C)')]
    cols = [('Khi trời nóng', '#fbe3c8', ORANGE, ['Mạch máu dưới da dãn', 'Tăng tiết mồ hôi', 'Tăng toả nhiệt'], 'Thân nhiệt giảm về mức bình thường'),
            ('Khi trời lạnh', '#d6e4f3', BLUE, ['Mạch máu dưới da co', 'Giảm tiết mồ hôi, cơ run', 'Tăng phân giải chất để sinh nhiệt'], 'Thân nhiệt tăng về mức bình thường')]
    for i, (t, col, lc, items, res) in enumerate(cols):
        x = 20 + i * 350
        b.append(R(x, 46, 320, 52, fill=col, stroke=INK, sw=2.2, rx=10)); b.append(T(x + 160, 78, t, size=16, weight='bold'))
        for k, it in enumerate(items):
            y = 122 + k * 56
            b.append(L(x + 160, y - 22 if k else 98, x + 160, y, stroke=lc, w=2.6, arrow=True))
            b.append(R(x + 20, y, 280, 38, fill='white', stroke=lc, sw=2, rx=8)); b.append(T(x + 160, y + 25, it, size=13.5, weight='bold'))
        b.append(L(x + 160, 122 + 2 * 56 + 38, x + 160, 292, stroke=lc, w=2.6, arrow=True))
        b.append(R(x + 20, 292, 280, 38, fill='#e7f1df', stroke=GREEN, sw=2, rx=8)); b.append(T(x + 160, 317, res, size=12.5, weight='bold'))
    b.append(T(360, 356, 'Da có vai trò quan trọng nhất; hệ thần kinh giữ vai trò chủ đạo (phản xạ)', size=12.5, fill=GREY))
    return svg(720, 374, ''.join(b))


reg('c-s8-b39-than-nhiet.svg', fig_than_nhiet, 'sinh8/bai-39/da-va-dieu-hoa-than-nhiet.json', 3, 'Cơ chế điều hoà thân nhiệt khi nóng và khi lạnh')


# ---------- Bài 40: sinh sản ----------
def fig_sinh_san_nu():
    b = [title(720, 'Hệ sinh dục nữ và quá trình thụ tinh, làm tổ (sơ đồ)')]
    cx, cy = 330, 150
    SK = '#f4c6c6'
    # tử cung
    b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d L%d,%d L%d,%d Z' % (cx - 56, cy - 40, cx, cy - 70, cx + 56, cy - 40, cx + 40, cy + 40, cx + 16, cy + 74, cx - 16, cy + 74, cx - 40, cy + 40), fill=SK, stroke=INK, w=2.8))
    b.append(PATH('M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d L%d,%d L%d,%d Z' % (cx - 44, cy - 34, cx, cy - 56, cx + 44, cy - 34, cx + 30, cy + 36, cx + 10, cy + 64, cx - 10, cy + 64, cx - 30, cy + 36), fill='#e98d8d', stroke='none', w=0))
    # âm đạo
    b.append(R(cx - 14, cy + 74, 28, 56, fill='#f0b4a8', stroke=INK, sw=2.4, rx=8))
    # ống dẫn trứng + buồng trứng
    for sgn in (-1, 1):
        pts = [(cx + sgn * 52, cy - 40), (cx + sgn * 110, cy - 76), (cx + sgn * 160, cy - 50), (cx + sgn * 170, cy - 10)]
        b.append(PL(pts, stroke=INK, w=10)); b.append(PL(pts, stroke='#f0b4a8', w=6))
        b.append(ELL(cx + sgn * 176, cy + 12, 20, 14, fill='#f3d98a', stroke=INK, w=2.4))
        b.append(C(cx + sgn * 176, cy + 12, 5, fill='white', stroke=INK, w=1.4))
    # thụ tinh & làm tổ
    b.append(C(cx - 118, cy - 70, 8, fill='#ffffff', stroke=INK, w=1.8)); b.append(C(cx - 110, cy - 76, 3, fill=BLUE, stroke='none', w=0))
    b.append(C(cx - 20, cy - 26, 8, fill='#ffffff', stroke=INK, w=1.8)); b.append(C(cx - 20, cy - 26, 3, fill=BLUE, stroke='none', w=0))
    lead(b, cx - 176, cy + 6, 90, 120, 'buồng trứng (sản sinh trứng)', anchor='start') if False else lead(b, cx - 190, cy + 16, 8, 210, 'buồng trứng', anchor='start')
    lead(b, cx - 120, cy - 70, 20, 56, 'ống dẫn trứng', anchor='start')
    lead(b, cx + 20, cy, 520, 96, 'tử cung (nuôi dưỡng thai)', anchor='start')
    lead(b, cx + 14, cy + 104, 520, 270, 'âm đạo', anchor='start')
    b.append(TL(520, 140, ['Thụ tinh: tinh trùng + trứng', '→ hợp tử, ở ống dẫn trứng', '', 'Phôi di chuyển tới tử cung,', 'làm tổ ở niêm mạc tử cung'], size=12, lh=17, anchor='start', fill='#3b4856'))
    b.append(L(cx - 112, cy - 66, cx - 28, cy - 30, stroke=RED, w=2, dash='4 3', arrow=True))
    return svg(720, 308, ''.join(b))


reg('c-s8-b40-sinh-san-nu.svg', fig_sinh_san_nu, 'sinh8/bai-40/sinh-san-o-nguoi.json', 1, 'Hệ sinh dục nữ, thụ tinh và làm tổ (sơ đồ)')


def fig_sinh_san_nam():
    b = [title(720, 'Hệ sinh dục nam (sơ đồ nhìn nghiêng)')]
    SK = '#f4c6c6'
    # dương vật + ống đái
    b.append(R(270, 152, 140, 40, fill=SK, stroke=INK, sw=2.4, rx=16))
    b.append(L(276, 172, 404, 172, stroke='#f0d58a', w=5))
    b.append(T(500, 296, 'Tinh hoàn sản sinh tinh trùng', size=12.5, fill=GREY, anchor='middle'))
    # bìu + tinh hoàn + mào tinh
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (230, 190, 200, 240, 280, 290, 330, 260, 350, 240, 330, 200, 300, 190), fill='#f0b4a8', stroke=INK, w=2.4))
    b.append(ELL(268, 240, 22, 28, fill='#8e6fc4', stroke=INK, w=2.2))
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (250, 218, 236, 240, 250, 266, 276, 272), stroke='#e9c46a', w=9)) if False else None
    b.append(PATH('M%d,%d C%d,%d %d,%d %d,%d' % (258, 214, 236, 226, 238, 262, 262, 270), stroke='#e9c46a', w=7))
    # ống dẫn tinh đi lên, túi tinh, bóng đái
    b.append(PL([(254, 214), (244, 170), (260, 120), (300, 126), (306, 160), (290, 170)], stroke=INK, w=8)); b.append(PL([(254, 214), (244, 170), (260, 120), (300, 126), (306, 160), (290, 170)], stroke='#e9c46a', w=4))
    b.append(ELL(262, 100, 36, 26, fill='#f3d98a', stroke=INK, w=2))
    b.append(ELL(318, 118, 16, 10, fill='#c9a02e', stroke=INK, w=1.8))
    lead(b, 270, 245, 120, 300, 'tinh hoàn', anchor='end') if False else lead(b, 262, 250, 150, 296, 'tinh hoàn', anchor='end')
    lead(b, 240, 262, 150, 262, 'mào tinh', anchor='end') if False else None
    lead(b, 244, 230, 150, 232, 'mào tinh', anchor='end')
    lead(b, 246, 160, 150, 160, 'ống dẫn tinh', anchor='end')
    lead(b, 318, 118, 470, 100, 'túi tinh', anchor='start') if False else lead(b, 326, 118, 470, 112, 'túi tinh', anchor='start')
    lead(b, 270, 96, 150, 80, 'bóng đái', anchor='end') if False else lead(b, 262, 94, 150, 86, 'bóng đái', anchor='end')
    lead(b, 340, 172, 470, 176, 'ống đái, dương vật', anchor='start')
    lead(b, 300, 250, 470, 250, 'bìu', anchor='start')
    return svg(720, 330, ''.join(b))


reg('c-s8-b40-sinh-san-nam.svg', fig_sinh_san_nam, 'sinh8/bai-40/sinh-san-o-nguoi.json', 0, 'Hệ sinh dục nam (sơ đồ)')


# ---------- Bài 41: môi trường và nhân tố sinh thái ----------
def fig_nhan_to_sinh_thai():
    b = [title(720, 'Môi trường sống và nhân tố sinh thái')]
    envs = [('Môi trường', 'trên cạn', '#e7f1df'), ('Môi trường', 'dưới nước', '#d3e8f3'), ('Môi trường', 'trong đất', '#e6d3bb'), ('Môi trường', 'sinh vật', '#f3d8e3')]
    for i, (a, c, col) in enumerate(envs):
        x = 10 + i * 178
        b.append(R(x, 46, 166, 54, fill=col, stroke=INK, sw=2, rx=10)); b.append(T(x + 83, 70, a, size=12.5)); b.append(T(x + 83, 90, c, size=14.5, weight='bold'))
    b.append(T(360, 128, 'Nhân tố sinh thái: các nhân tố trong môi trường ảnh hưởng đến sinh vật', size=14, weight='bold'))
    b.append(PL([(360, 134), (360, 150), (190, 150), (190, 166)], stroke=INK, w=2)); b.append(PL([(360, 150), (530, 150), (530, 166)], stroke=INK, w=2))
    b.append(R(40, 166, 300, 46, fill='#fbf0c9', stroke=INK, sw=2.2, rx=10)); b.append(T(190, 195, 'Nhân tố vô sinh', size=15, weight='bold'))
    b.append(R(380, 166, 300, 46, fill='#dcebc9', stroke=INK, sw=2.2, rx=10)); b.append(T(530, 195, 'Nhân tố hữu sinh', size=15, weight='bold'))
    b.append(TL(190, 240, ['ánh sáng, nhiệt độ,', 'độ ẩm, nước, đất,…'], size=13, lh=18))
    b.append(TL(530, 240, ['các sinh vật khác và con người', '(con người ảnh hưởng lớn nhất)'], size=13, lh=18))
    b.append(T(360, 290, 'Các sinh vật có quan hệ hỗ trợ hoặc cạnh tranh', size=12.5, fill=GREY))
    return svg(720, 308, ''.join(b))


reg('c-s8-b41-nhan-to.svg', fig_nhan_to_sinh_thai, 'sinh8/bai-41/moi-truong-va-nhan-to-sinh-thai.json', 2, 'Các loại môi trường sống và nhóm nhân tố sinh thái')


def fig_gioi_han_sinh_thai():
    b = [title(720, 'Giới hạn sinh thái của cá rô phi về nhiệt độ')]
    ox, oy = 80, 250
    x0, x1 = 5.6, 42
    sx = lambda t: ox + (t - 0) * 13.6
    b.append(L(ox, oy, 670, oy, w=1.8, arrow=True)); b.append(L(ox, oy, ox, 70, w=1.8, arrow=True))
    b.append(T(360, oy + 62, 'Nhiệt độ (°C)', size=13, weight='bold')); b.append(T(ox + 8, 84, 'Mức độ sinh trưởng', size=13, weight='bold', anchor='start'))
    for t in (0, 10, 20, 30, 40):
        b.append(L(sx(t), oy - 4, sx(t), oy + 4, w=1.5)); b.append(T(sx(t), oy + 20, str(t), size=12))
    # đường cong dạng chuông lệch: thấp ở 5,6 và 42, cực đại 30
    def val(t):
        if t <= 30:
            u = (t - x0) / (30 - x0)
            return max(0, math.sin(u * math.pi / 2)) ** 1.4
        u = (42 - t) / (42 - 30)
        return max(0, math.sin(u * math.pi / 2)) ** 1.4
    pts = [(sx(t), oy - 150 * val(t)) for t in [x0 + i * (x1 - x0) / 120 for i in range(121)]]
    b.append(PL(pts, stroke=BLUE, w=3.4))
    b.append(POLY([(sx(x0), oy)] + pts + [(sx(x1), oy)], fill='#cfe0f0', stroke='none', sw=0)) if False else None
    for t, nm, col in ((x0, '5,6 °C', RED), (30, '30 °C', GREEN), (42, '42 °C', RED)):
        b.append(L(sx(t), oy, sx(t), oy - (150 * val(t) if t == 30 else 40), stroke=col, w=1.6, dash='4 3'))
        b.append(T(sx(t), oy + 38, nm, size=13, weight='bold', fill=col))
    b.append(L(sx(x0), 64, sx(x1), 64, stroke=INK, w=1.8)); b.append(L(sx(x0), 58, sx(x0), 70, w=1.8)); b.append(L(sx(x1), 58, sx(x1), 70, w=1.8))
    b.append(T((sx(x0) + sx(x1)) / 2, 54, 'giới hạn sinh thái (5,6 – 42 °C)', size=13, weight='bold'))
    b.append(T(sx(30), oy - 158, 'điểm cực thuận', size=12.5, weight='bold', fill=GREEN))
    b.append(T(sx(x0), oy - 48, 'giới hạn dưới', size=12, fill=RED))
    b.append(T(sx(x1), oy - 48, 'giới hạn trên', size=12, fill=RED))
    b.append(T(360, 336, 'Đường cong minh hoạ dạng chung, không phải số liệu đo', size=11.5, fill=GREY))
    return svg(720, 348, ''.join(b))


reg('c-s8-b41-gioi-han.svg', fig_gioi_han_sinh_thai, 'sinh8/bai-41/moi-truong-va-nhan-to-sinh-thai.json', 5, 'Giới hạn sinh thái về nhiệt độ của cá rô phi (đường cong minh hoạ)')


# ---------- Bài 42: quần thể ----------
def fig_phan_bo_quan_the():
    b = [title(720, 'Ba kiểu phân bố cá thể trong quần thể')]
    rnd = random.Random(11)
    panels = [(20, 'Phân bố đều', 'điều kiện sống đồng đều,', 'cạnh tranh gay gắt'), (260, 'Phân bố theo nhóm', 'điều kiện sống không đều,', 'sống bầy đàn'), (500, 'Phân bố ngẫu nhiên', 'điều kiện tương đối đồng đều,', 'không cạnh tranh gay gắt')]
    for i, (x, nm, l1, l2) in enumerate(panels):
        b.append(R(x, 44, 200, 150, fill='#f4f9f2', stroke=INK, sw=2, rx=8))
        pts = []
        if i == 0:
            pts = [(x + 25 + c * 30, 64 + r * 28) for r in range(4) for c in range(6)]
        elif i == 1:
            for (gx, gy) in ((x + 55, 90), (x + 140, 80), (x + 100, 160)):
                for _ in range(8):
                    pts.append((gx + rnd.uniform(-22, 22), gy + rnd.uniform(-18, 18)))
        else:
            for _ in range(24):
                pts.append((x + rnd.uniform(12, 188), rnd.uniform(58, 182)))
        for (px, py) in pts:
            b.append(C(px, py, 5, fill=BLUE, stroke=INK, w=1.2))
        b.append(T(x + 100, 220, nm, size=14, weight='bold')); b.append(T(x + 100, 240, l1, size=12, fill='#3b4856')); b.append(T(x + 100, 256, l2, size=12, fill='#3b4856'))
    return svg(720, 274, ''.join(b))


reg('c-s8-b42-phan-bo.svg', fig_phan_bo_quan_the, 'sinh8/bai-42/quan-the-sinh-vat.json', 2, 'Ba kiểu phân bố cá thể (sơ đồ minh hoạ)')


# ---------- Bài 43: quần xã ----------
def fig_quan_xa():
    b = [title(720, 'Quần xã sinh vật: nhiều quần thể của các loài khác nhau (ví dụ ruộng lúa)')]
    b.append(ELL(360, 172, 340, 126, fill='#f4f9f2', stroke=INK, w=3))
    groups = [(160, 120, 'Quần thể lúa', '#9acb7e', 9), (360, 100, 'Quần thể châu chấu', '#e9c46a', 6), (560, 130, 'Quần thể ếch', '#7fb77e', 5), (240, 214, 'Quần thể cỏ', '#cfe6c4', 7), (470, 214, 'Quần thể rắn', '#c9a27c', 4)]
    rnd = random.Random(3)
    for (x, y, nm, col, n) in groups:
        b.append(ELL(x, y, 78, 40, fill='none', stroke=GREY, w=1.6, dash='5 4'))
        for _ in range(n):
            b.append(C(x + rnd.uniform(-58, 58), y + rnd.uniform(-22, 22), 6, fill=col, stroke=INK, w=1.2))
        b.append(T(x, y + 56, nm, size=12.5, weight='bold'))
    b.append(TL(360, 330, ['Loài ưu thế: số lượng cá thể nhiều, hoạt động mạnh (ví dụ: lúa ở ruộng lúa)', 'Loài đặc trưng: chỉ có ở một quần xã (ví dụ: voọc Cát Bà ở rừng Cát Bà)'], size=12.5, lh=18, fill='#3b4856'))
    return svg(720, 366, ''.join(b))


reg('c-s8-b43-quan-xa.svg', fig_quan_xa, 'sinh8/bai-43/quan-xa-sinh-vat.json', 0, 'Quần xã gồm nhiều quần thể (sơ đồ minh hoạ)')


# ---------- Bài 44: hệ sinh thái ----------
def fig_thanh_phan_hst():
    b = [title(720, 'Thành phần của hệ sinh thái và dòng năng lượng')]
    # Mặt Trời
    b.append(C(80, 90, 30, fill='#ffd966', stroke=INK, w=2.4)); b.append(T(80, 140, 'Ánh sáng', size=13, weight='bold')); b.append(T(80, 156, 'Mặt Trời', size=13, weight='bold'))
    for a in range(0, 360, 45):
        x1, y1 = pt(80, 90, 34, a); x2, y2 = pt(80, 90, 46, a)
        b.append(L(x1, y1, x2, y2, stroke='#e8a317', w=2.4))
    boxes = [(190, 'Sinh vật sản xuất', 'thực vật, tảo', '#d6e8cb'), (360, 'Sinh vật tiêu thụ', 'động vật', '#fbe3c8'), (530, 'Sinh vật phân giải', 'nấm, vi khuẩn', '#e6d3bb')]
    for x, t, e, col in boxes:
        b.append(R(x - 70, 160, 140, 64, fill=col, stroke=INK, sw=2.2, rx=10)); b.append(T(x, 186, t, size=13.5, weight='bold')); b.append(T(x, 206, e, size=12.5, fill='#3b4856'))
    b.append(L(110, 110, 175, 156, stroke='#e8a317', w=3, arrow=True))
    b.append(L(262, 192, 288, 192, w=2.6, arrow=True)); b.append(L(432, 192, 458, 192, w=2.6, arrow=True))
    b.append(R(150, 272, 430, 50, fill='#f6efc9', stroke=INK, sw=2.2, rx=10)); b.append(TL(365, 292, ['Thành phần vô sinh: ánh sáng, nhiệt độ, nước,', 'không khí, đất, chất vô cơ,…'], size=12.5, lh=17))
    # trả lại chất vô cơ
    b.append(PLA([(530, 226), (530, 262), (440, 262), (440, 270)], stroke=GREEN, w=2.4)) if False else None
    b.append(L(530, 226, 530, 270, stroke=GREEN, w=2.4, arrow=True)); b.append(T(536, 252, 'trả lại chất vô cơ', size=11.5, fill='#2f6b2a', anchor='start'))
    b.append(L(190, 270, 190, 228, stroke=GREEN, w=2.4, arrow=True)); b.append(T(196, 252, 'hấp thụ chất vô cơ', size=11.5, fill='#2f6b2a', anchor='start')) if False else b.append(T(184, 252, 'hấp thụ chất vô cơ', size=11.5, fill='#2f6b2a', anchor='end'))
    b.append(TL(640, 90, ['Năng lượng truyền một chiều', 'qua các bậc dinh dưỡng,', 'giảm dần (toả nhiệt)'], size=12, lh=16, fill='#9a5d10')) if False else None
    b.append(TL(630, 96, ['Năng lượng: truyền', 'một chiều, giảm dần', 'qua các bậc dinh dưỡng', '(toả nhiệt ra môi trường)'], size=12, lh=17, fill='#9a5d10'))
    return svg(720, 340, ''.join(b))


reg('c-s8-b44-thanh-phan.svg', fig_thanh_phan_hst, 'sinh8/bai-44/he-sinh-thai.json', 0, 'Thành phần của hệ sinh thái')


def fig_chuoi_thuc_an():
    b = [title(720, 'Chuỗi thức ăn và tháp năng lượng')]
    names = [('Cỏ', 'sinh vật sản xuất', '#9acb7e'), ('Châu chấu', 'tiêu thụ bậc 1', '#e9c46a'), ('Ếch', 'tiêu thụ bậc 2', '#7fb77e'), ('Rắn', 'tiêu thụ bậc 3', '#c9a27c'), ('Đại bàng', 'tiêu thụ bậc 4', '#b8c4d6')]
    for i, (n, r_, col) in enumerate(names):
        x = 12 + i * 142
        b.append(R(x, 52, 120, 54, fill=col, stroke=INK, sw=2.2, rx=10)); b.append(T(x + 60, 76, n, size=15, weight='bold')); b.append(T(x + 60, 95, r_, size=11, fill='#3b4856'))
        if i < 4:
            b.append(L(x + 122, 79, x + 140, 79, w=2.6, arrow=True))
    # tháp năng lượng (bậc thấp rộng, trên hẹp)
    cx = 360
    levels = ['Đại bàng', 'Rắn', 'Ếch', 'Châu chấu', 'Cỏ']
    for k, nm in enumerate(levels):
        w = 60 + k * 50
        y = 140 + k * 36
        b.append(R(cx - w / 2, y, w, 32, fill=names[4 - k][2], stroke=INK, sw=1.8, rx=3)); b.append(T(cx, y + 21, nm, size=13, weight='bold'))
    b.append(L(cx + 190, 300, cx + 190, 150, stroke=ORANGE, w=3, arrow=True)); b.append(T(cx + 200, 230, 'năng lượng giảm dần', size=12.5, weight='bold', fill='#9a5d10', anchor='start'))
    b.append(T(360, 340, 'Tháp năng lượng: bậc dinh dưỡng càng cao, năng lượng càng ít (sơ đồ minh hoạ, không theo số liệu)', size=11.5, fill=GREY))
    return svg(720, 358, ''.join(b))


reg('c-s8-b44-chuoi-thuc-an.svg', fig_chuoi_thuc_an, 'sinh8/bai-44/he-sinh-thai.json', 3, 'Chuỗi thức ăn và tháp năng lượng (sơ đồ minh hoạ)')


def fig_luoi_thuc_an():
    b = [title(720, 'Lưới thức ăn: nhiều chuỗi thức ăn có mắt xích chung')]
    nodes = {'cỏ': (100, 250, '#9acb7e'), 'châu chấu': (260, 170, '#e9c46a'), 'chuột': (260, 310, '#c9b27c'), 'ếch': (440, 110, '#7fb77e'), 'rắn': (500, 250, '#c9a27c'), 'đại bàng': (650, 180, '#b8c4d6')}
    edges = [('cỏ', 'châu chấu'), ('cỏ', 'chuột'), ('châu chấu', 'ếch'), ('châu chấu', 'rắn'), ('chuột', 'rắn'), ('ếch', 'rắn'), ('rắn', 'đại bàng')]
    for a, c in edges:
        x1, y1, _ = nodes[a]; x2, y2, _ = nodes[c]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        b.append(L(x1 + dx / d * 38, y1 + dy / d * 22, x2 - dx / d * 40, y2 - dy / d * 24, stroke=INK, w=2, arrow=True))
    for n, (x, y, col) in nodes.items():
        b.append(R(x - 38, y - 20, 76, 40, fill=col, stroke=INK, sw=2, rx=10)); b.append(T(x, y + 5, n, size=13.5, weight='bold'))
    b.append(T(360, 340, 'Mũi tên chỉ chiều chuyển hoá: sinh vật bị ăn → sinh vật ăn nó', size=12.5, fill=GREY))
    return svg(720, 358, ''.join(b))


reg('c-s8-b44-luoi-thuc-an.svg', fig_luoi_thuc_an, 'sinh8/bai-44/he-sinh-thai.json', 5, 'Ví dụ về lưới thức ăn (sơ đồ minh hoạ)')


# ---------- Bài 45: sinh quyển ----------
def fig_sinh_quyen():
    b = [title(720, 'Sinh quyển: gồm các lớp đất, nước và không khí có sinh vật sống')]
    b.append(R(40, 50, 640, 70, fill='#e6f2fb', stroke=INK, sw=2.2, rx=10)); b.append(T(360, 82, 'Khí quyển (lớp không khí)', size=15, weight='bold')); b.append(T(360, 104, 'sinh vật sống ở lớp thấp: chim, côn trùng, vi sinh vật,…', size=12, fill='#3b4856'))
    b.append(R(40, 124, 320, 90, fill='#e6d3bb', stroke=INK, sw=2.2, rx=10)); b.append(T(200, 160, 'Thạch quyển (lớp đất)', size=15, weight='bold')); b.append(T(200, 184, 'sinh vật sống trên và trong đất', size=12, fill='#3b4856'))
    b.append(R(364, 124, 316, 90, fill='#cfe6f1', stroke=INK, sw=2.2, rx=10)); b.append(T(522, 160, 'Thuỷ quyển (lớp nước đại dương)', size=15, weight='bold')); b.append(T(522, 184, 'sinh vật sống trong nước', size=12, fill='#3b4856'))
    b.append(T(360, 250, 'Sinh quyển = toàn bộ sinh vật + các nhân tố vô sinh của môi trường', size=13, weight='bold', fill=BLUE))
    b.append(T(360, 272, 'Là hệ sinh thái khổng lồ trên Trái Đất', size=12.5, fill=GREY))
    return svg(720, 290, ''.join(b))


reg('c-s8-b45-sinh-quyen.svg', fig_sinh_quyen, 'sinh8/bai-45/sinh-quyen.json', 0, 'Các lớp của sinh quyển')


def fig_khu_sinh_hoc():
    b = [title(720, 'Các khu sinh học trên cạn (từ cực đến vùng nhiệt đới)')]
    items = [('Đồng rêu', 'hàn đới', '#dfe9ef'), ('Rừng lá kim', 'phương bắc', '#b7d6b0'), ('Rừng ôn đới', '', '#9acb7e'), ('Rừng mưa', 'nhiệt đới', '#5fa65a')]
    for i, (n, s_, col) in enumerate(items):
        x = 20 + i * 172
        b.append(R(x, 70, 160, 100, fill=col, stroke=INK, sw=2.2, rx=10))
        b.append(T(x + 80, 118 if s_ else 126, n, size=15, weight='bold'))
        if s_:
            b.append(T(x + 80, 140, s_, size=13))
        if i < 3:
            b.append(L(x + 162, 120, x + 170, 120, w=2.4, arrow=True))
    b.append(L(40, 196, 680, 196, stroke=BLUE, w=2.4, arrow=True))
    b.append(T(40, 218, 'gần cực (lạnh)', size=13, anchor='start', fill=BLUE)); b.append(T(680, 218, 'gần xích đạo (nóng ẩm)', size=13, anchor='end', fill=BLUE))
    b.append(T(360, 254, 'Khu sinh học nước ngọt: nước đứng (ao, hồ), nước chảy (sông, suối)', size=12.5, fill='#3b4856'))
    b.append(T(360, 274, 'Khu sinh học biển: phân tầng theo độ sâu và theo chiều ngang (ven bờ, khơi)', size=12.5, fill='#3b4856'))
    return svg(720, 292, ''.join(b))


reg('c-s8-b45-khu-sinh-hoc.svg', fig_khu_sinh_hoc, 'sinh8/bai-45/sinh-quyen.json', 3, 'Các khu sinh học trên cạn và các khu sinh học khác')


# ---------- Bài 46: cân bằng tự nhiên ----------
def fig_khong_che_sinh_hoc():
    b = [title(720, 'Khống chế sinh học: thỏ tuyết và linh miêu (đường cong minh hoạ)')]
    ox, oy = 80, 250
    b.append(L(ox, oy, 680, oy, w=1.8, arrow=True)); b.append(L(ox, oy, ox, 60, w=1.8, arrow=True))
    b.append(T(680, oy + 22, 'Thời gian', size=13, weight='bold', anchor='end')); b.append(T(ox + 8, 66, 'Số lượng cá thể', size=13, weight='bold', anchor='start'))
    prey = [(ox + t * 5.6, oy - 100 - 70 * math.sin(2 * math.pi * t / 60)) for t in range(0, 106)]
    pred = [(ox + t * 5.6, oy - 80 - 40 * math.sin(2 * math.pi * (t - 8) / 60)) for t in range(0, 106)]
    b.append(PL(prey, stroke=BLUE, w=3.4)); b.append(PL(pred, stroke=RED, w=3.4))
    b.append(R(150, 292, 12, 12, fill=BLUE, stroke=INK, sw=1)); b.append(T(168, 303, 'thỏ tuyết (con mồi)', size=12.5, anchor='start'))
    b.append(R(380, 292, 12, 12, fill=RED, stroke=INK, sw=1)); b.append(T(398, 303, 'linh miêu (vật ăn thịt)', size=12.5, anchor='start'))
    b.append(TL(380, 330, ['Con mồi tăng → vật ăn thịt tăng theo (chậm hơn) → con mồi giảm → vật ăn thịt giảm;', 'số lượng mỗi quần thể bị khống chế ở mức nhất định'], size=12.5, lh=18, fill='#3b4856'))
    return svg(720, 368, ''.join(b))


reg('c-s8-b46-khong-che.svg', fig_khong_che_sinh_hoc, 'sinh8/bai-46/can-bang-tu-nhien.json', 2, 'Khống chế sinh học (đường cong minh hoạ dạng chung, không phải số liệu đo)')


# ---------- Bài 47: bảo vệ môi trường ----------
def fig_tac_dong_thoi_ky():
    b = [title(720, 'Tác động của con người đến môi trường qua các thời kì')]
    items = [('Nguyên thuỷ', ['hái lượm, săn bắn,', 'dùng lửa'], '#dcebc9'), ('Xã hội nông nghiệp', ['trồng trọt, chăn nuôi,', 'định cư, thuỷ lợi'], '#f6efc9'), ('Công nghiệp và', ['cơ giới hoá, khai thác', 'khoáng sản, khí thải tăng'], '#f9d9d6'), ('Hậu công nghiệp', ['công nghệ thông tin', 'giúp tiết kiệm tài nguyên'], '#d6e4f3')]
    items[2] = ('Công nghiệp', items[2][1], items[2][2])
    b.append(L(40, 70, 680, 70, stroke=INK, w=3, arrow=True))
    for i, (n, ls, col) in enumerate(items):
        x = 20 + i * 176
        b.append(C(x + 80, 70, 8, fill=BLUE, stroke=INK, w=1.8))
        b.append(R(x, 96, 160, 112, fill=col, stroke=INK, sw=2, rx=10))
        b.append(T(x + 80, 122, n, size=14, weight='bold')); b.append(L(x + 14, 132, x + 146, 132, stroke=INK, w=1))
        b.append(TL(x + 80, 156, ls, size=12, lh=18))
    b.append(T(360, 236, 'Mức tác động đến môi trường thay đổi theo từng thời kì phát triển của xã hội', size=12.5, fill=GREY))
    return svg(720, 254, ''.join(b))


reg('c-s8-b47-thoi-ky.svg', fig_tac_dong_thoi_ky, 'sinh8/bai-47/bao-ve-moi-truong.json', 0, 'Tác động của con người đến môi trường qua các thời kì')


def fig_hieu_ung_nha_kinh():
    b = [title(720, 'Khí nhà kính giữ nhiệt làm Trái Đất nóng lên (sơ đồ)')]
    # Mặt Trời
    b.append(C(90, 80, 34, fill='#ffd966', stroke=INK, w=2.4))
    for a in range(0, 360, 45):
        x1, y1 = pt(90, 80, 38, a); x2, y2 = pt(90, 80, 50, a)
        b.append(L(x1, y1, x2, y2, stroke='#e8a317', w=2.4))
    # khí quyển
    b.append(R(250, 60, 440, 62, fill='#e6f2fb', stroke=INK, sw=2, rx=10, )); b.append(T(470, 86, 'Khí quyển có khí nhà kính (CO₂,…)', size=13.5, weight='bold'))
    b.append(R(250, 250, 440, 46, fill='#a9c79a', stroke=INK, sw=2.2, rx=6)); b.append(T(470, 279, 'Bề mặt Trái Đất', size=14, weight='bold'))
    # ánh sáng tới
    b.append(L(130, 104, 330, 248, stroke='#e8a317', w=3.2, arrow=True))
    b.append(T(120, 190, 'ánh sáng', size=12.5, fill='#9a5d10', anchor='start')); b.append(T(120, 206, 'Mặt Trời', size=12.5, fill='#9a5d10', anchor='start'))
    # nhiệt bức xạ lên và bị giữ lại
    b.append(L(430, 248, 430, 126, stroke=RED, w=3, arrow=True)); b.append(T(420, 196, 'nhiệt bức xạ', size=12.5, fill=RED, anchor='end'))
    b.append(L(570, 126, 570, 248, stroke=RED, w=3, dash='6 4', arrow=True))
    b.append(T(582, 178, 'một phần nhiệt bị', size=12, fill=RED, anchor='start')); b.append(T(582, 194, 'khí nhà kính giữ lại,', size=12, fill=RED, anchor='start')); b.append(T(582, 210, 'trả về mặt đất', size=12, fill=RED, anchor='start'))
    b.append(T(360, 326, 'Khí nhà kính tăng → nhiệt bị giữ lại nhiều hơn → biến đổi khí hậu', size=13, weight='bold', fill=BLUE))
    return svg(720, 344, ''.join(b))


reg('c-s8-b47-nha-kinh.svg', fig_hieu_ung_nha_kinh, 'sinh8/bai-47/bao-ve-moi-truong.json', 3, 'Hiệu ứng nhà kính (sơ đồ)')


if __name__ == '__main__':
    import glob
    write_figs('sinh8', FIGS)
    for rel, after, name, cap in ATTACH:
        subj, path = rel.split('/', 1)
        hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', path)) + glob.glob(os.path.join(ROOT, 'content', subj, '*', path))
        assert hits, rel
        attach(subj, os.path.relpath(hits[0], os.path.join(ROOT, 'content', subj)), after, name, cap)
    print('sinh8: %d hình' % len(FIGS))
