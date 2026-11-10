# Toán 6: hình minh họa cho các bài lý thuyết còn thiếu (số liệu lấy đúng từ bài).
import sys, os, math, glob
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

NAVY = '#1a56a0'
ATTACH, FIGS = [], {}


def reg(name, fn, rel, after, cap):
    FIGS[name] = fn
    ATTACH.append((rel, after, name, cap))


def numline(b, x0, x1, y, lo, hi, step=1, ticks=None, lab=True):
    b.append(L(x0 - 10, y, x1 + 10, y, w=2.2, arrow=True))
    sc = (x1 - x0) / (hi - lo)
    for v in range(lo, hi + 1, step):
        x = x0 + (v - lo) * sc
        b.append(L(x, y - 5, x, y + 5, w=1.6))
        if lab: b.append(T(x, y + 22, str(v), size=12.5))
    return lambda v: x0 + (v - lo) * sc


# ---- b2: hàng, lớp và số La Mã ----
def f_b2():
    b = [title(720, 'Hàng và lớp của số tự nhiên: ví dụ số 4 305 062')]
    heads = [('Lớp triệu', 3), ('Lớp nghìn', 3), ('Lớp đơn vị', 3)]
    digs = ['', '', '4', '3', '0', '5', '0', '6', '2']
    hn = ['Trăm', 'Chục', 'Đơn vị'] * 3
    x0, cw = 90, 60
    cols = ['#fdecec', '#e8f1fa', '#eaf5e4']
    for k, (h, n) in enumerate(heads):
        b.append(R(x0 + k * 3 * cw, 50, 3 * cw, 28, fill=cols[k], stroke=INK, sw=1.6)); b.append(T(x0 + k * 3 * cw + 1.5 * cw, 70, h, size=13, weight='bold'))
    for i in range(9):
        x = x0 + i * cw
        b.append(R(x, 78, cw, 26, fill=cols[i // 3], stroke=INK, sw=1.2)); b.append(T(x + cw / 2, 96, hn[i], size=11.5))
        b.append(R(x, 104, cw, 40, fill='white', stroke=INK, sw=1.2)); b.append(T(x + cw / 2, 132, digs[i], size=22, weight='bold'))
    b.append(T(360, 172, '4 305 062 = 4 triệu + 3 trăm nghìn + 5 chục nghìn... (mỗi chữ số có giá trị theo vị trí)', size=12.5, fill='#3b4856')) if False else b.append(T(360, 172, 'Mỗi lớp có ba hàng; chữ số 0 giữ chỗ ở hàng không có đơn vị', size=12.5, fill='#3b4856'))
    b.append(T(360, 214, 'Số La Mã', size=14, weight='bold'))
    items = [('I', '1'), ('V', '5'), ('X', '10'), ('IV', '4'), ('IX', '9'), ('XIV', '14'), ('XXIX', '29')]
    for i, (r, v) in enumerate(items):
        x = 60 + i * 90
        b.append(R(x, 226, 80, 60, fill=LYELLOW, stroke=INK, sw=1.4, rx=8)); b.append(T(x + 40, 254, r, size=20, weight='bold')); b.append(T(x + 40, 276, '= ' + v, size=14))
    return svg(720, 306, ''.join(b))


reg('t6-b2-hang-lop.svg', f_b2, 'toan6/bai-2/cach-ghi-so-tu-nhien.json', 2, 'Hàng, lớp và số La Mã')


# ---- b4: tia số cộng trừ ----
def f_b4():
    b = [title(720, 'Phép cộng và phép trừ trên tia số: 7 + 5 = 12 và 12 − 5 = 7')]
    f = numline(b, 60, 660, 160, 0, 14)
    b.append(PATH('M %.1f 150 Q %.1f 100 %.1f 150' % (f(7), (f(7) + f(12)) / 2, f(12)), stroke=BLUE, w=2.6)); b.append(T((f(7) + f(12)) / 2, 108, '+ 5', size=15, weight='bold', fill=BLUE))
    b.append(PATH('M %.1f 196 Q %.1f 246 %.1f 196' % (f(12), (f(7) + f(12)) / 2, f(7)), stroke=RED, w=2.6)); b.append(T((f(7) + f(12)) / 2, 252, '− 5', size=15, weight='bold', fill=RED))
    b.append(T(360, 292, 'a + b = c thì a = c − b và b = c − a', size=13, weight='bold', fill=NAVY))
    return svg(720, 312, ''.join(b))


reg('t6-b4-tia-so.svg', f_b4, 'toan6/bai-4/cong-tru-so-tu-nhien.json', 1, 'Cộng và trừ trên tia số')


# ---- b5: mảng nhân, chia có dư ----
def f_b5():
    b = [title(720, 'Phép nhân và phép chia có dư')]
    b.append(T(180, 56, '3 × 4 = 12', size=15, weight='bold'))
    for r in range(3):
        for c in range(4):
            b.append(C(90 + c * 34, 90 + r * 34, 12, fill='#8fc1ee', stroke=INK, w=1.4))
    b.append(T(180, 206, '3 hàng, mỗi hàng 4 chấm', size=12.5, fill='#3b4856'))
    b.append(T(500, 56, '14 = 4 · 3 + 2  (14 chia 4 được 3, dư 2)', size=14, weight='bold'))
    for g in range(3):
        b.append(R(370 + g * 76, 76, 68, 68, fill='#f6f9fc', stroke=GREY, sw=1.4, rx=6))
        for k in range(4):
            b.append(C(386 + g * 76 + (k % 2) * 36, 94 + (k // 2) * 30, 11, fill='#8fc1ee', stroke=INK, w=1.3))
    for k in range(2):
        b.append(C(610 + k * 34, 110, 11, fill='#f2a33a', stroke=INK, w=1.3))
    b.append(T(446 + 38, 170, '3 nhóm, mỗi nhóm 4 chấm', size=12.5, fill='#3b4856')); b.append(T(626, 150, 'dư 2', size=13, weight='bold', fill=ORANGE))
    b.append(T(360, 250, 'Số dư luôn nhỏ hơn số chia (2 < 4)', size=13, weight='bold', fill=NAVY))
    return svg(720, 272, ''.join(b))


reg('t6-b5-nhan-chia.svg', f_b5, 'toan6/bai-5/nhan-chia-so-tu-nhien.json', 2, 'Phép nhân và phép chia có dư')


# ---- b6: luỹ thừa ----
def f_b6():
    b = [title(720, 'Luỹ thừa: bình phương và lập phương')]
    b.append(T(180, 58, '3² = 3 · 3 = 9', size=15, weight='bold'))
    for r in range(3):
        for c in range(3):
            b.append(R(120 + c * 36, 78 + r * 36, 32, 32, fill='#8fc1ee', stroke=INK, sw=1.4))
    b.append(T(180, 205, 'hình vuông cạnh 3 có 9 ô', size=12.5, fill='#3b4856'))
    b.append(T(500, 58, '2³ = 2 · 2 · 2 = 8', size=15, weight='bold'))
    for layer in range(2):
        for r in range(2):
            for c in range(2):
                b.append(R(430 + layer * 96 + c * 30, 100 + r * 30, 28, 28, fill=['#8fc1ee', '#f2a33a'][layer], stroke=INK, sw=1.4))
    b.append(T(517, 128, '+', size=22, weight='bold'))
    b.append(T(520, 205, 'khối lập phương cạnh 2: 2 lớp, mỗi lớp 4 khối = 8', size=12.5, fill='#3b4856'))
    b.append(TL(360, 244, ['aⁿ = a · a · … · a (n thừa số a);  a là cơ số, n là số mũ'], size=13, weight='bold', fill=NAVY))
    return svg(720, 264, ''.join(b))


reg('t6-b6-luy-thua.svg', f_b6, 'toan6/bai-6/luy-thua.json', 0, 'Bình phương và lập phương (sơ đồ)')


# ---- b7: thứ tự phép tính ----
def f_b7():
    b = [title(720, 'Thứ tự thực hiện các phép tính')]
    steps = [('1', 'Luỹ thừa', '#fdecec'), ('2', 'Nhân, chia', '#fdf1e0'), ('3', 'Cộng, trừ', '#e8f1fa')]
    for i, (n, t, f) in enumerate(steps):
        x = 40 + i * 220
        b.append(R(x, 56, 180, 54, fill=f, stroke=INK, sw=1.8, rx=10)); b.append(T(x + 90, 90, n + '. ' + t, size=15, weight='bold'))
        if i < 2: b.append(L(x + 184, 83, x + 214, 83, w=2.4, arrow=True))
    b.append(T(360, 146, 'Có dấu ngoặc: trong ngoặc trước', size=13.5, weight='bold'))
    br = ['( )  tròn', '[ ]  vuông', '{ }  nhọn']
    for i, t in enumerate(br):
        x = 90 + i * 210
        b.append(R(x, 160, 150, 44, fill=LYELLOW, stroke=INK, sw=1.6, rx=8)); b.append(T(x + 75, 188, t, size=15, weight='bold'))
        if i < 2: b.append(L(x + 154, 182, x + 204, 182, w=2.4, arrow=True))
    b.append(T(360, 236, 'Ví dụ: 2 + 3 · 4² = 2 + 3 · 16 = 2 + 48 = 50', size=13, fill='#3b4856'))
    return svg(720, 258, ''.join(b))


reg('t6-b7-thu-tu.svg', f_b7, 'toan6/bai-7/thu-tu-phep-tinh.json', 2, 'Thứ tự thực hiện phép tính')


# ---- b8: ước của 12 ----
def f_b8():
    b = [title(720, 'Ước của 12: các cách xếp 12 ô thành hình chữ nhật')]
    for k, (r, c) in enumerate(((1, 12), (2, 6), (3, 4))):
        y = 56 + k * 82
        cs = 18
        for i in range(r):
            for j in range(c):
                b.append(R(60 + j * cs, y + i * cs, cs - 2, cs - 2, fill='#8fc1ee', stroke=INK, sw=1))
        b.append(T(360 + 60, y + 22, '12 = %d × %d' % (r, c), size=15, weight='bold'))
    b.append(T(360, 306, 'Ư(12) = {1; 2; 3; 4; 6; 12};  B(3) = {0; 3; 6; 9; 12; …}', size=13.5, weight='bold', fill=NAVY))
    return svg(720, 328, ''.join(b))


reg('t6-b8-uoc.svg', f_b8, 'toan6/bai-8/quan-he-chia-het.json', 1, 'Các ước của 12 (sơ đồ ô vuông)')


# ---- b9: dấu hiệu chia hết ----
def f_b9():
    b = [title(720, 'Dấu hiệu chia hết cho 2, 5, 3, 9 (ví dụ 135 và 246)')]
    rows = [('Chia hết cho 2', 'chữ số tận cùng chẵn (0, 2, 4, 6, 8)', '246 ✓   135 ✗'),
            ('Chia hết cho 5', 'chữ số tận cùng là 0 hoặc 5', '135 ✓   246 ✗'),
            ('Chia hết cho 3', 'tổng các chữ số chia hết cho 3', '135: 1+3+5 = 9 ✓; 246: 2+4+6 = 12 ✓'),
            ('Chia hết cho 9', 'tổng các chữ số chia hết cho 9', '135: 9 ✓;  246: 12 ✗')]
    for i, (a, bb, c) in enumerate(rows):
        y = 52 + i * 62
        b.append(R(30, y, 150, 50, fill='#e8f1fa', stroke=INK, sw=1.6, rx=8)); b.append(T(105, y + 31, a, size=14, weight='bold'))
        b.append(R(186, y, 250, 50, fill='white', stroke=INK, sw=1.4, rx=8)); b.append(T(311, y + 30, bb, size=12))
        b.append(R(442, y, 250, 50, fill=LYELLOW, stroke=INK, sw=1.4, rx=8)); b.append(T(567, y + 30, c, size=12, weight='bold'))
    b.append(T(360, 312, 'Số chia hết cho 9 thì chia hết cho 3 (ngược lại không đúng)', size=12.5, fill=GREY))
    return svg(720, 332, ''.join(b))


reg('t6-b9-dau-hieu.svg', f_b9, 'toan6/bai-9/dau-hieu-chia-het.json', 1, 'Bảng dấu hiệu chia hết')


# ---- b10: số nguyên tố và cây phân tích ----
def f_b10():
    b = [title(720, 'Các số nguyên tố nhỏ hơn 20')]
    pr = {2, 3, 5, 7, 11, 13, 17, 19}
    for n in range(1, 20):
        r, c = (n - 1) // 10, (n - 1) % 10
        x, y = 90 + c * 54, 56 + r * 54
        b.append(R(x, y, 48, 48, fill='#cde7d3' if n in pr else ('#eeeeee' if n == 1 else 'white'), stroke=INK, sw=1.4, rx=6))
        b.append(T(x + 24, y + 32, str(n), size=18, weight='bold' if n in pr else 'normal'))
    b.append(T(630, 150, 'xanh: số nguyên tố', size=12, fill='#2f6b2a', weight='bold'))
    b.append(T(360, 188, 'Phân tích 60 ra thừa số nguyên tố (sơ đồ cây)', size=14, weight='bold'))
    def node(x, y, t, prime=False):
        b.append(C(x, y, 20, fill='#cde7d3' if prime else '#fdf1e0', stroke=INK, w=1.6)); b.append(T(x, y + 6, t, size=15, weight='bold'))
    node(360, 224, '60'); node(300, 280, '2', True); node(420, 280, '30')
    node(380, 336, '2', True); node(460, 336, '15'); node(430, 392, '3', True); node(490, 392, '5', True)
    for a, c in (((360, 224), (300, 280)), ((360, 224), (420, 280)), ((420, 280), (380, 336)), ((420, 280), (460, 336)), ((460, 336), (430, 392)), ((460, 336), (490, 392))):
        b.append(L(a[0], a[1] + 20, c[0], c[1] - 20, w=1.6))
    b.append(T(600, 330, '60 = 2² · 3 · 5', size=16, weight='bold', fill=NAVY))
    return svg(720, 424, ''.join(b))


reg('t6-b10-nguyen-to.svg', f_b10, 'toan6/bai-10/so-nguyen-to.json', 1, 'Số nguyên tố nhỏ hơn 20 và sơ đồ cây phân tích 60')


# ---- b15: dấu ngoặc ----
def f_b15():
    b = [title(720, 'Quy tắc dấu ngoặc')]
    b.append(R(30, 56, 320, 150, fill='#eaf5e4', stroke=INK, sw=1.6, rx=10)); b.append(T(190, 82, 'Dấu "+" đứng trước: giữ nguyên dấu', size=13, weight='bold'))
    b.append(T(190, 124, 'a + (b − c) = a + b − c', size=16, weight='bold')); b.append(T(190, 166, '10 + (3 − 1) = 10 + 3 − 1 = 12', size=13.5, fill='#3b4856'))
    b.append(R(370, 56, 320, 150, fill='#fdecec', stroke=INK, sw=1.6, rx=10)); b.append(T(530, 82, 'Dấu "−" đứng trước: đổi dấu tất cả', size=13, weight='bold'))
    b.append(T(530, 124, 'a − (b − c) = a − b + c', size=16, weight='bold')); b.append(T(530, 166, '10 − (3 − 1) = 10 − 3 + 1 = 8', size=13.5, fill='#3b4856'))
    return svg(720, 228, ''.join(b))


reg('t6-b15-dau-ngoac.svg', f_b15, 'toan6/bai-15/quy-tac-dau-ngoac.json', 1, 'Quy tắc dấu ngoặc (ví dụ số)')


# ---- b16: bảng dấu ----
def f_b16():
    b = [title(720, 'Quy tắc dấu khi nhân hai số nguyên')]
    hdr = ['×', '+', '−']
    cells = [['+', '−'], ['−', '+']]
    for i in range(3):
        b.append(R(200 + i * 100, 50, 100, 46, fill='#e8f1fa', stroke=INK, sw=1.6)); b.append(T(250 + i * 100, 82, hdr[i], size=20, weight='bold'))
    for r in range(2):
        b.append(R(200, 96 + r * 56, 100, 56, fill='#e8f1fa', stroke=INK, sw=1.6)); b.append(T(250, 132 + r * 56, hdr[r + 1], size=20, weight='bold'))
        for c in range(2):
            v = cells[r][c]
            b.append(R(300 + c * 100, 96 + r * 56, 100, 56, fill='#cde7d3' if v == '+' else '#f8d7d4', stroke=INK, sw=1.6)); b.append(T(350 + c * 100, 132 + r * 56, v, size=26, weight='bold'))
    b.append(T(360, 236, 'Cùng dấu → tích dương;  khác dấu → tích âm;  nhân với 0 → bằng 0', size=13, weight='bold', fill=NAVY))
    b.append(T(360, 260, 'Ví dụ: (−3) · (−4) = 12;  (−3) · 4 = −12', size=12.5, fill=GREY))
    return svg(720, 282, ''.join(b))


reg('t6-b16-bang-dau.svg', f_b16, 'toan6/bai-16/nhan-so-nguyen.json', 1, 'Bảng dấu của tích')


# ---- b17: ước của 6 trên trục số ----
def f_b17():
    b = [title(720, 'Các ước của 6 trên trục số')]
    f = numline(b, 70, 650, 130, -6, 6)
    for v in (-6, -3, -2, -1, 1, 2, 3, 6):
        b.append(C(f(v), 130, 8, fill=RED, stroke=INK, w=1.6))
    b.append(C(f(0), 130, 5, fill='white', stroke=INK, w=1.6))
    b.append(T(360, 200, 'Ư(6) = {±1; ±2; ±3; ±6}: tám ước', size=14, weight='bold', fill=NAVY))
    b.append(T(360, 226, 'Nếu b là ước của a thì −b cũng là ước của a', size=12.5, fill=GREY))
    return svg(720, 246, ''.join(b))


reg('t6-b17-uoc-so-nguyen.svg', f_b17, 'toan6/bai-17/chia-het-so-nguyen.json', 2, 'Các ước của 6 trên trục số')


# ---- b25: cộng phân số ----
def fracbar(b, x, y, w, n, k, col='#8fc1ee', h=30):
    for i in range(n):
        b.append(R(x + i * w / n, y, w / n, h, fill=col if i < k else 'white', stroke=INK, sw=1.4))


def f_b25():
    b = [title(720, 'Cộng phân số bằng băng phân số')]
    b.append(T(180, 56, '1/4 + 2/4 = 3/4', size=15, weight='bold'))
    fracbar(b, 60, 70, 240, 4, 1, '#8fc1ee'); fracbar(b, 60, 110, 240, 4, 2, '#f2a33a'); fracbar(b, 60, 150, 240, 4, 3, '#6fbf5a')
    b.append(T(180, 206, 'cùng mẫu: cộng tử, giữ nguyên mẫu', size=12.5, fill='#3b4856'))
    b.append(T(530, 56, '1/2 + 1/3 = 3/6 + 2/6 = 5/6', size=15, weight='bold'))
    fracbar(b, 400, 70, 240, 2, 1, '#8fc1ee'); fracbar(b, 400, 110, 240, 3, 1, '#f2a33a'); fracbar(b, 400, 150, 240, 6, 5, '#6fbf5a')
    b.append(T(530, 206, 'khác mẫu: quy đồng rồi cộng', size=12.5, fill='#3b4856'))
    return svg(720, 228, ''.join(b))


reg('t6-b25-cong-phan-so.svg', f_b25, 'toan6/bai-25/cong-tru-phan-so.json', 1, 'Cộng phân số (băng phân số)')


# ---- b26: nhân phân số ----
def f_b26():
    b = [title(720, 'Nhân phân số: 2/3 · 3/4 = 6/12 = 1/2')]
    x0, y0, cw, ch = 220, 56, 60, 40
    for r in range(3):
        for c in range(4):
            col = '#f2a33a' if (r < 2 and c < 3) else ('#8fc1ee' if (r < 2 or c < 3) else 'white')
            if r < 2 and c < 3: col = '#6fbf5a'
            elif r < 2: col = '#cfe3f5'
            elif c < 3: col = '#fbe3c0'
            else: col = 'white'
            b.append(R(x0 + c * cw, y0 + r * ch, cw, ch, fill=col, stroke=INK, sw=1.4))
    b.append(T(x0 + 120, y0 + 3 * ch + 20, '3/4 chiều rộng', size=12.5, fill='#3b4856'))
    b.append(T(x0 - 14, y0 + 40, '2/3', size=13, weight='bold', anchor='end'))
    b.append(T(500, 120, 'Phần xanh lá: 6 ô trong 12 ô', size=13, weight='bold', anchor='start', fill='#2f6b2a'))
    b.append(T(500, 146, '= 6/12 = 1/2', size=15, weight='bold', anchor='start', fill=NAVY))
    b.append(T(360, 236, 'Nhân tử với tử, mẫu với mẫu: (2·3)/(3·4)', size=12.5, fill='#3b4856'))
    return svg(720, 258, ''.join(b))


reg('t6-b26-nhan-phan-so.svg', f_b26, 'toan6/bai-26/nhan-chia-phan-so.json', 1, 'Nhân phân số (mô hình diện tích)')


# ---- b27: m/n của a ----
def f_b27():
    b = [title(720, '3/5 của 20 là 12  —  và ngược lại, 3/5 của số nào là 12?')]
    fracbar(b, 60, 70, 600, 5, 3, '#6fbf5a', 44)
    for i in range(5):
        b.append(T(60 + 600 / 5 * (i + .5), 98, '4', size=16, weight='bold'))
    b.append(T(360, 62, 'Cả thanh = 20 (chia 5 phần, mỗi phần 4)', size=12.5, fill='#3b4856'))
    b.append(T(60 + 600 * 0.3, 140, '3 phần = 12', size=14, weight='bold', fill='#2f6b2a'))
    b.append(T(360, 190, '20 · 3/5 = 12   (tìm m/n của số a: a · m/n)', size=14, weight='bold', fill=NAVY))
    b.append(T(360, 218, '12 : 3/5 = 20   (biết m/n của số đó bằng b: b : m/n)', size=14, weight='bold', fill=NAVY))
    return svg(720, 240, ''.join(b))


reg('t6-b27-hai-bai-toan.svg', f_b27, 'toan6/bai-27/hai-bai-toan-phan-so.json', 1, 'Hai bài toán về phân số (thanh 20 chia 5 phần)')


# ---- b29: dịch dấu phẩy ----
def f_b29():
    b = [title(720, 'Nhân với 10, 100, … : dịch dấu phẩy sang phải')]
    rows = [('3,45', '× 10', '34,5', '1 chữ số'), ('3,45', '× 100', '345', '2 chữ số'), ('3,45', '× 0,1', '0,345', 'sang trái 1 chữ số')]
    for i, (a, op, r, n) in enumerate(rows):
        y = 56 + i * 70
        b.append(R(60, y, 140, 50, fill='#e8f1fa', stroke=INK, sw=1.6, rx=8)); b.append(T(130, y + 34, a, size=20, weight='bold'))
        b.append(L(204, y + 25, 290, y + 25, w=2.4, arrow=True)); b.append(T(247, y + 16, op, size=14, weight='bold', fill=BLUE))
        b.append(R(296, y, 140, 50, fill='#eaf5e4', stroke=INK, sw=1.6, rx=8)); b.append(T(366, y + 34, r, size=20, weight='bold'))
        b.append(T(450, y + 31, 'dịch ' + n if not n.startswith('sang') else n, size=13, anchor='start', fill='#3b4856'))
    return svg(720, 270, ''.join(b))


reg('t6-b29-dich-dau-phay.svg', f_b29, 'toan6/bai-29/tinh-toan-so-thap-phan.json', 1, 'Dịch dấu phẩy khi nhân với 10, 100, 0,1')


# ---- b30: làm tròn ----
def f_b30():
    b = [title(720, 'Làm tròn 3,46 đến hàng phần mười')]
    y = 130
    x0, x1 = 90, 630
    b.append(L(x0 - 20, y, x1 + 20, y, w=2.2, arrow=True))
    f = lambda v: x0 + (v - 3.4) / 0.2 * (x1 - x0)
    for v, t in ((3.4, '3,4'), (3.5, '3,5'), (3.6, '3,6')):
        b.append(L(f(v), y - 7, f(v), y + 7, w=2)); b.append(T(f(v), y + 28, t, size=14, weight='bold'))
    b.append(C(f(3.46), y, 8, fill=RED, stroke=INK, w=1.6)); b.append(T(f(3.46), y - 22, '3,46', size=15, weight='bold', fill=RED))
    b.append(L(f(3.46), y - 8, f(3.5), y - 8, stroke=GREEN, w=0.1)) if False else None
    b.append(T(f(3.5) + 70, y - 46, 'gần 3,5 hơn → 3,5', size=13, weight='bold', fill='#2f6b2a'))
    b.append(T(360, 210, 'Chữ số bị bỏ đi đầu tiên là 6 (≥ 5) nên cộng thêm 1: 3,4 → 3,5', size=13, weight='bold', fill=NAVY))
    return svg(720, 232, ''.join(b))


reg('t6-b30-lam-tron.svg', f_b30, 'toan6/bai-30/lam-tron-uoc-luong.json', 0, 'Làm tròn 3,46 trên tia số')


# ---- b38: phân loại dữ liệu ----
def f_b38():
    b = [title(720, 'Dữ liệu và cách thu thập')]
    b.append(R(280, 46, 160, 40, fill='#e8f1fa', stroke=INK, sw=1.8, rx=8)); b.append(T(360, 72, 'Dữ liệu', size=16, weight='bold'))
    for x, t, ex, f in ((130, 'Số liệu (dữ liệu là số)', ['chiều cao', 'điểm số'], '#eaf5e4'), (590, 'Dữ liệu không phải số', ['tên', 'màu sắc', 'môn thể thao yêu thích'], '#fdf1e0')):
        b.append(L(360, 86, x, 112, w=1.8, arrow=True))
        b.append(R(x - 110, 112, 220, 92, fill=f, stroke=INK, sw=1.6, rx=8)); b.append(T(x, 136, t, size=13, weight='bold')); b.append(TL(x, 160, ex, size=12.5, lh=17, fill='#3b4856'))
    b.append(T(360, 234, 'Cách thu thập dữ liệu', size=14, weight='bold'))
    ways = ['Quan sát', 'Làm thí nghiệm', 'Lập phiếu hỏi', 'Phỏng vấn', 'Nguồn có sẵn']
    for i, w in enumerate(ways):
        x = 30 + i * 136
        b.append(R(x, 248, 128, 36, fill=LYELLOW, stroke=INK, sw=1.4, rx=8)); b.append(T(x + 64, 271, w, size=12.5, weight='bold'))
    return svg(720, 304, ''.join(b))


reg('t6-b38-du-lieu.svg', f_b38, 'toan6/bai-38/du-lieu-thu-thap.json', 2, 'Phân loại dữ liệu và cách thu thập')


if __name__ == '__main__':
    write_figs('toan6', FIGS)
    for rel, after, name, cap in ATTACH:
        subj, path = rel.split('/', 1)
        hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', path))
        assert hits, rel
        attach(subj, os.path.relpath(hits[0], os.path.join(ROOT, 'content', subj)), after, name, cap)
    print('toan6b: %d hình' % len(FIGS))
