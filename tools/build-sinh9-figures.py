# Sinh 9: sơ đồ minh họa lý thuyết (không phải ảnh chụp, không đo đúng tỉ lệ).
import sys, os, math, random, itertools
sys.path.insert(0, os.path.dirname(__file__))
from sinhlib import *

ATTACH = []
FIGS = {}
PURPLE, YELLOW_P, GREEN_P = '#9b59b6', '#f2c94c', '#6fbf5a'


def reg(name, fn, rel, after, cap):
    FIGS[name] = fn
    ATTACH.append((rel, after, name, cap))


def chrom(b, x, y, h=70, w=14, bands=(), fill='#e9e1f2', stroke=INK, cen=0.5, sw=2):
    """Nhiễm sắc thể dạng que đứng; bands: [(vị trí 0..1, màu)]."""
    b.append(R(x - w / 2, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=w / 2))
    for pos, col in bands:
        b.append(R(x - w / 2 + 1, y + h * pos - 3, w - 2, 7, fill=col, stroke='none', sw=0))
    b.append(L(x - w / 2, y + h * cen, x + w / 2, y + h * cen, stroke=INK, w=1))


def flower(x, y, col, r=11):
    o = []
    for a in range(0, 360, 72):
        px, py = pt(x, y, r * 0.8, a)
        o.append(C(px, py, r * 0.55, fill=col, stroke=INK, w=1.3))
    o.append(C(x, y, r * 0.35, fill='#f6d86b', stroke=INK, w=1))
    return ''.join(o)


def pea(x, y, col, wrinkled=False, r=11):
    if not wrinkled:
        return C(x, y, r, fill=col, stroke=INK, w=1.6)
    pts = []
    for k in range(60):
        th = 2 * math.pi * k / 60
        rr = r + 2.2 * math.sin(7 * th)
        pts.append((x + rr * math.cos(th), y + rr * math.sin(th)))
    return POLY(pts, fill=col, stroke=INK, sw=1.6)


# ---------- Bài 36 ----------
def fig_thuat_ngu():
    b = [title(720, 'Kí hiệu và thuật ngữ cơ bản của di truyền học')]
    rows = [('P', 'bố mẹ (thế hệ xuất phát)'), ('F₁, F₂', 'thế hệ con thứ nhất, thứ hai'), ('G', 'giao tử'), ('×', 'phép lai'), ('♀', 'cái'), ('♂', 'đực')]
    for i, (k, v) in enumerate(rows):
        y = 52 + i * 40
        b.append(R(20, y, 80, 34, fill=LBLUE, stroke=INK, sw=1.8, rx=6)); b.append(T(60, y + 24, k, size=18, weight='bold'))
        b.append(R(100, y, 220, 34, fill='white', stroke=INK, sw=1.8, rx=6)); b.append(T(210, y + 23, v, size=13))
    # allele
    b.append(T(530, 56, 'Cặp NST tương đồng và allele', size=14, weight='bold'))
    items = [('AA', 'đồng hợp (trội)', ['#c0392b', '#c0392b']), ('Aa', 'dị hợp', ['#c0392b', '#2b6cb0']), ('aa', 'đồng hợp (lặn)', ['#2b6cb0', '#2b6cb0'])]
    for i, (g, nm, cols) in enumerate(items):
        cx = 420 + i * 100
        chrom(b, cx - 12, 82, bands=[(0.4, cols[0])]); chrom(b, cx + 12, 82, bands=[(0.4, cols[1])])
        b.append(T(cx, 178, g, size=17, weight='bold')); b.append(T(cx, 197, nm, size=12))
    b.append(T(520, 222, 'Mỗi NST của cặp mang một allele ở cùng một vị trí (locus)', size=12, fill=GREY))
    b.append(R(340, 240, 360, 26, fill=LYELLOW, stroke=INK, sw=1.6, rx=6)) if False else None
    b.append(TL(360, 280, ['Kiểu gene: tổ hợp các allele (AA, Aa, aa); kiểu hình: tính trạng biểu hiện', 'Cặp tính trạng tương phản: hoa tím – hoa trắng, hạt vàng – hạt xanh, hạt trơn – hạt nhăn'], size=12.5, lh=18, fill='#3b4856'))
    return svg(720, 312, ''.join(b))


reg('c-s9-b36-thuat-ngu.svg', fig_thuat_ngu, 'sinh9/bai-36/khai-quat-di-truyen.json', 2, 'Kí hiệu, allele, đồng hợp – dị hợp (sơ đồ)')


# ---------- Bài 37 ----------
def fig_lai_mot_cap():
    b = [title(720, 'Lai một cặp tính trạng: hoa tím × hoa trắng')]
    # P -> F1
    b.append(T(30, 70, 'P', size=16, weight='bold', anchor='start'))
    b.append(R(60, 50, 110, 40, fill='#efe2f6', stroke=INK, sw=2, rx=8)); b.append(T(115, 76, 'AA (tím)', size=14, weight='bold'))
    b.append(T(190, 76, '×', size=20, weight='bold'))
    b.append(R(210, 50, 110, 40, fill='white', stroke=INK, sw=2, rx=8)); b.append(T(265, 76, 'aa (trắng)', size=14, weight='bold'))
    b.append(T(30, 116, 'G', size=16, weight='bold', anchor='start')); b.append(T(115, 118, 'A', size=15)); b.append(T(265, 118, 'a', size=15))
    b.append(L(115, 124, 190, 150, arrow=True)); b.append(L(265, 124, 215, 150, arrow=True))
    b.append(T(30, 176, 'F₁', size=16, weight='bold', anchor='start'))
    b.append(R(150, 156, 110, 40, fill='#efe2f6', stroke=INK, sw=2, rx=8)); b.append(T(205, 182, 'Aa (tím)', size=14, weight='bold'))
    b.append(T(330, 182, '100% hoa tím', size=13, anchor='start', weight='bold', fill=PURPLE))
    # F1 x F1
    b.append(T(30, 236, 'F₁ × F₁', size=15, weight='bold', anchor='start')); b.append(T(120, 236, 'Aa × Aa', size=15, weight='bold', anchor='start'))
    b.append(T(30, 264, 'G', size=16, weight='bold', anchor='start')); b.append(T(120, 264, '(A, a) × (A, a)', size=14, anchor='start'))
    # Punnett
    gx, gy = 420, 84
    for j, g in enumerate(('A', 'a')):
        b.append(T(gx + 50 + j * 80, gy - 8, g, size=16, weight='bold')); b.append(T(gx - 12, gy + 52 + j * 70 - 10 + 18, g, size=16, weight='bold'))
    cells = [['AA', 'Aa'], ['Aa', 'aa']]
    for i in range(2):
        for j in range(2):
            g = cells[i][j]
            x, y = gx + j * 80 + 10, gy + i * 70
            b.append(R(x, y, 80, 66, fill='#efe2f6' if g != 'aa' else 'white', stroke=INK, sw=1.8))
            b.append(flower(x + 40, y + 24, PURPLE if g != 'aa' else 'white', 11)); b.append(T(x + 40, y + 58, g, size=13, weight='bold'))
    b.append(T(310, 232, 'F₂', size=16, weight='bold', anchor='start'))
    b.append(TL(530, 252, ['Kiểu gene: 1 AA : 2 Aa : 1 aa', 'Kiểu hình: 3 hoa tím : 1 hoa trắng'], size=13, lh=20, weight='bold', anchor='start')) if False else None
    b.append(TL(360, 306, ['Kiểu gene F₂: 1 AA : 2 Aa : 1 aa', 'Kiểu hình F₂: 3 hoa tím : 1 hoa trắng'], size=13.5, lh=21, weight='bold'))
    return svg(720, 336, ''.join(b))


reg('c-s9-b37-lai-mot-cap.svg', fig_lai_mot_cap, 'sinh9/bai-37/quy-luat-mendel.json', 1, 'Sơ đồ lai một cặp tính trạng (Mendel)')


def fig_lai_hai_cap():
    b = [title(720, 'Lai hai cặp tính trạng: F₁ AaBb × AaBb → F₂ tỉ lệ 9 : 3 : 3 : 1')]
    gam = ['AB', 'Ab', 'aB', 'ab']
    gx, gy = 150, 72
    cw, ch = 96, 54
    for j, g in enumerate(gam):
        b.append(T(gx + j * cw + cw / 2, gy - 8, g, size=15, weight='bold'))
        b.append(T(gx - 22, gy + j * ch + ch / 2 + 6, g, size=15, weight='bold'))
    def phen(g):
        a = 'A' in g
        bb = 'B' in g
        return ((YELLOW_P if a else GREEN_P), (not bb)), ('vàng' if a else 'xanh') + (' trơn' if bb else ' nhăn')
    for i in range(4):
        for j in range(4):
            g1, g2 = gam[j], gam[i]
            geno = ''.join(sorted([g1[0], g2[0]], key=lambda c: (c.lower(), c.islower()))) + ''.join(sorted([g1[1], g2[1]], key=lambda c: (c.lower(), c.islower())))
            (col, wr), nm = phen(geno)
            x, y = gx + j * cw, gy + i * ch
            b.append(R(x, y, cw, ch, fill='#fbfbf4', stroke=INK, sw=1.4))
            b.append(pea(x + 22, y + ch / 2, col, wr, 11)); b.append(T(x + 62, y + ch / 2 + 5, geno, size=13, weight='bold'))
    # chú giải
    ly = 72
    b.append(R(560, ly, 150, 150, fill=LGREY, stroke=GREY, sw=1.4, rx=8))
    leg = [(YELLOW_P, False, 'vàng, trơn', '9'), (YELLOW_P, True, 'vàng, nhăn', '3'), (GREEN_P, False, 'xanh, trơn', '3'), (GREEN_P, True, 'xanh, nhăn', '1')]
    for k, (col, wr, nm, n) in enumerate(leg):
        y = ly + 26 + k * 34
        b.append(pea(582, y, col, wr, 10)); b.append(T(600, y + 5, nm, size=12.5, anchor='start')); b.append(T(698, y + 5, n, size=15, weight='bold', anchor='end'))
    b.append(TL(360, 318, ['Hạt vàng (A), xanh (a); hạt trơn (B), nhăn (b). Gồm 4 loại giao tử ở mỗi bên,', '16 tổ hợp; các cặp nhân tố di truyền phân li độc lập'], size=12.5, lh=18, fill='#3b4856'))
    b.append(T(30, 56, '♀ \\ ♂', size=12, fill=GREY, anchor='start')) if False else None
    return svg(720, 346, ''.join(b))


reg('c-s9-b37-lai-hai-cap.svg', fig_lai_hai_cap, 'sinh9/bai-37/quy-luat-mendel.json', 3, 'Bảng Punnett của phép lai hai cặp tính trạng (F₁ × F₁)')


def fig_lai_phan_tich():
    b = [title(720, 'Phép lai phân tích: xác định kiểu gene của cá thể mang tính trạng trội')]
    panels = [(20, 'Trường hợp 1', 'AA × aa', ['G: A  |  a', 'F: 100% Aa (đồng tính)'], [('Aa', PURPLE)] * 4, '→ cá thể trội là đồng hợp (AA)'),
              (370, 'Trường hợp 2', 'Aa × aa', ['G: A, a  |  a', 'F: 1 Aa : 1 aa (phân tính 1 : 1)'], [('Aa', PURPLE), ('aa', 'white'), ('Aa', PURPLE), ('aa', 'white')], '→ cá thể trội là dị hợp (Aa)')]
    for x, nm, cross, lines, kids, concl in panels:
        b.append(R(x, 46, 330, 250, fill='#fafafa', stroke=GREY, sw=1.4, rx=10))
        b.append(T(x + 165, 72, nm, size=14, weight='bold')); b.append(T(x + 165, 98, 'P: ' + cross, size=16, weight='bold'))
        b.append(TL(x + 165, 128, lines, size=13, lh=22))
        for k, (g, col) in enumerate(kids):
            cx = x + 70 + k * 64
            b.append(flower(cx, 200, col, 14)); b.append(T(cx, 232, g, size=13, weight='bold'))
        b.append(T(x + 165, 272, concl, size=13.5, weight='bold', fill=BLUE))
    b.append(T(360, 320, 'Cá thể lặn aa chỉ cho một loại giao tử a nên kiểu hình con phản ánh kiểu gene cá thể trội', size=12.5, fill=GREY))
    return svg(720, 336, ''.join(b))


reg('c-s9-b37-phan-tich.svg', fig_lai_phan_tich, 'sinh9/bai-37/quy-luat-mendel.json', 5, 'Phép lai phân tích (sơ đồ)')


# ---------- Bài 38 ----------
def helix(b, cx, y0, h, amp=26, turns=2, cols=('#2b6cb0', '#c0392b'), rungs=True):
    n = 80
    p1, p2 = [], []
    for k in range(n + 1):
        t = k / n
        y = y0 + h * t
        ph = 2 * math.pi * turns * t
        p1.append((cx + amp * math.sin(ph), y)); p2.append((cx - amp * math.sin(ph), y))
    if rungs:
        for k in range(0, n + 1, 4):
            b.append(L(p1[k][0], p1[k][1], p2[k][0], p2[k][1], stroke='#9aa5b1', w=2.4))
    b.append(PL(p1, stroke=cols[0], w=5)); b.append(PL(p2, stroke=cols[1], w=5))


def fig_dna():
    b = [title(720, 'Cấu trúc DNA: hai mạch xoắn kép, các nucleotide liên kết bổ sung')]
    helix(b, 120, 56, 270)
    b.append(T(120, 410, 'DNA xoắn kép', size=14, weight='bold'))
    b.append(L(168, 110, 168, 178, stroke=INK, w=1.6)); b.append(L(160, 110, 176, 110, w=1.6)); b.append(L(160, 178, 176, 178, w=1.6))
    b.append(TL(186, 138, ['mỗi chu kì xoắn', 'dài 3,4 nm,', '10 cặp nucleotide'], size=11.5, lh=15, anchor='start', fill='#3b4856'))
    # thang phẳng
    seq = [('A', 'T'), ('T', 'A'), ('G', 'C'), ('C', 'G'), ('A', 'T')]
    colr = {'A': '#e9a23b', 'T': '#4e9a8f', 'G': '#c0392b', 'C': '#4e79a7'}
    x1, x2 = 400, 560
    b.append(L(x1 - 20, 66, x1 - 20, 66 + len(seq) * 56, stroke='#2b6cb0', w=6)); b.append(L(x2 + 20, 66, x2 + 20, 66 + len(seq) * 56, stroke='#c0392b', w=6))
    for i, (l, r) in enumerate(seq):
        y = 80 + i * 56
        b.append(R(x1 - 4, y, 56, 30, fill=colr[l], stroke=INK, sw=1.6, rx=6)); b.append(T(x1 + 24, y + 22, l, size=17, weight='bold', fill='white'))
        b.append(R(x2 - 52, y, 56, 30, fill=colr[r], stroke=INK, sw=1.6, rx=6)); b.append(T(x2 - 24, y + 22, r, size=17, weight='bold', fill='white'))
        n = 2 if {l, r} == {'A', 'T'} else 3
        for k in range(n):
            yy = y + 8 + k * (14 / (n - 1) * 1.0 if n > 1 else 0)
            b.append(L(x1 + 54, y + 7 + k * 8, x2 - 54, y + 7 + k * 8, stroke=INK, w=1.6, dash='3 3'))
        b.append(T(480, y + 46 if False else y + 26, '', size=1))
        b.append(T(600, y + 20, '%d liên kết H' % n, size=12, anchor='start', fill='#3b4856'))
    b.append(TL(480, 372, ['Nguyên tắc bổ sung:', 'A liên kết T (2 liên kết hydrogen)', 'G liên kết C (3 liên kết hydrogen)'], size=12.5, lh=18, weight='bold'))
    return svg(720, 438, ''.join(b))


reg('c-s9-b38-dna.svg', fig_dna, 'sinh9/bai-38/nucleic-acid-gene.json', 1, 'Cấu trúc DNA và nguyên tắc bổ sung (sơ đồ)')


def fig_dna_rna():
    b = [title(720, 'So sánh DNA và RNA')]
    colr = {'A': '#e9a23b', 'T': '#4e9a8f', 'G': '#c0392b', 'C': '#4e79a7', 'U': '#8e6fc4'}
    seq1 = 'ATGCAT'; seq2 = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    # DNA
    b.append(T(180, 56, 'DNA: hai mạch', size=15, weight='bold'))
    for i, ch_ in enumerate(seq1):
        x = 40 + i * 52
        b.append(R(x, 80, 44, 34, fill=colr[ch_], stroke=INK, sw=1.6, rx=6)); b.append(T(x + 22, 104, ch_, size=17, weight='bold', fill='white'))
        c2 = seq2[ch_]
        b.append(R(x, 150, 44, 34, fill=colr[c2], stroke=INK, sw=1.6, rx=6)); b.append(T(x + 22, 174, c2, size=17, weight='bold', fill='white'))
        b.append(L(x + 22, 114, x + 22, 150, stroke=INK, w=1.6, dash='3 3'))
    b.append(L(36, 72, 36 + 6 * 52 - 4, 72, stroke='#2b6cb0', w=4)); b.append(L(36, 192, 36 + 6 * 52 - 4, 192, stroke='#c0392b', w=4))
    b.append(T(180, 222, 'đơn phân A, T, G, C', size=13, fill='#3b4856'))
    # RNA
    b.append(T(540, 56, 'RNA: một mạch', size=15, weight='bold'))
    rna = 'AUGCAU'
    for i, ch_ in enumerate(rna):
        x = 400 + i * 52
        b.append(R(x, 115, 44, 34, fill=colr[ch_], stroke=INK, sw=1.6, rx=6)); b.append(T(x + 22, 139, ch_, size=17, weight='bold', fill='white'))
    b.append(L(396, 107, 396 + 6 * 52 - 4, 107, stroke='#8e6fc4', w=4))
    b.append(T(540, 222, 'đơn phân A, U, G, C', size=13, fill='#3b4856'))
    b.append(TL(540, 252, ['Có ba loại RNA: mRNA, tRNA, rRNA'], size=13, lh=18))
    b.append(TL(180, 252, ['Gene: một đoạn DNA mang thông tin', 'quy định một RNA hoặc protein'], size=12.5, lh=17, fill='#3b4856'))
    return svg(720, 290, ''.join(b))


reg('c-s9-b38-dna-rna.svg', fig_dna_rna, 'sinh9/bai-38/nucleic-acid-gene.json', 4, 'So sánh cấu trúc DNA và RNA')


# ---------- Bài 39 ----------
def ladder(b, x, y, n, c1, c2, w=18, pitch=10):
    """Đoạn DNA nằm ngang gồm hai mạch: c1 (trên) và c2 (dưới)."""
    L_ = n * pitch
    b.append(L(x, y, x + L_, y, stroke=c1, w=5)); b.append(L(x, y + w, x + L_, y + w, stroke=c2, w=5))
    for k in range(n + 1):
        b.append(L(x + k * pitch, y, x + k * pitch, y + w, stroke='#9aa5b1', w=1.6))


def fig_tai_ban():
    b = [title(720, 'Tái bản DNA: nguyên tắc bổ sung và bán bảo toàn')]
    OLD1, OLD2, NEW = '#2b6cb0', '#c0392b', '#f2a33a'
    # DNA mẹ
    ladder(b, 220, 56, 28, OLD1, OLD2, 22, 10)
    b.append(T(100, 80, 'DNA mẹ', size=14, weight='bold'))
    b.append(L(360, 92, 360, 118, w=2.6, arrow=True)); b.append(T(372, 112, 'hai mạch tách nhau', size=12, anchor='start', fill='#3b4856'))
    # tách và tổng hợp
    ladder(b, 220, 126, 8, OLD1, OLD2, 22, 10)
    # nhánh tách ra
    b.append(PL([(300, 126), (330, 120), (400, 100), (500, 96)], stroke=OLD1, w=5)) if False else None
    for sgn, c, yy in ((-1, OLD1, 0), (1, OLD2, 0)):
        pass
    b.append(PL([(300, 126), (340, 112), (420, 106), (500, 106)], stroke=OLD1, w=5)); b.append(PL([(300, 148), (340, 168), (420, 176), (500, 176)], stroke=OLD2, w=5))
    b.append(L(420, 106, 420, 114, stroke=NEW, w=0.1)) if False else None
    b.append(L(340, 118, 500, 118, stroke=NEW, w=5, dash='1 0')) if False else None
    b.append(T(560, 112, 'mỗi mạch làm khuôn', size=12, anchor='start', fill='#3b4856'))
    # hai DNA con
    b.append(L(360, 190, 360, 214, w=2.6, arrow=True)); b.append(T(372, 208, 'tổng hợp mạch mới (A–T, G–C)', size=12, anchor='start', fill='#3b4856'))
    ladder(b, 140, 226, 28, OLD1, NEW, 22, 10); ladder(b, 140, 286, 28, OLD2, NEW, 22, 10)
    b.append(T(100, 252, 'DNA con 1', size=12.5, weight='bold', anchor='end')) if False else None
    b.append(T(130, 252, 'DNA con 1', size=12.5, weight='bold', anchor='end')); b.append(T(130, 312, 'DNA con 2', size=12.5, weight='bold', anchor='end'))
    for k, (c, t) in enumerate(((OLD1, 'mạch cũ (từ DNA mẹ)'), (OLD2, 'mạch cũ (từ DNA mẹ)'), (NEW, 'mạch mới tổng hợp'))):
        pass
    b.append(L(450, 244, 480, 244, stroke=OLD1, w=5)); b.append(L(450, 256, 480, 256, stroke=OLD2, w=5)); b.append(T(488, 254, 'mạch cũ của DNA mẹ', size=12, anchor='start'))
    b.append(L(450, 276, 480, 276, stroke=NEW, w=5)); b.append(T(488, 280, 'mạch mới tổng hợp', size=12, anchor='start'))
    b.append(TL(360, 350, ['Mỗi DNA con có một mạch của DNA mẹ và một mạch mới (nguyên tắc bán bảo toàn)', 'Sau k lần tái bản, từ 1 DNA tạo 2ᵏ DNA con'], size=12.5, lh=18, weight='bold', fill='#3b4856'))
    return svg(720, 380, ''.join(b))


reg('c-s9-b39-tai-ban.svg', fig_tai_ban, 'sinh9/bai-39/tai-ban-phien-ma.json', 0, 'Tái bản DNA (sơ đồ)')


def fig_phien_ma():
    b = [title(720, 'Phiên mã: tổng hợp mRNA từ mạch khuôn của gene')]
    colr = {'A': '#e9a23b', 'T': '#4e9a8f', 'G': '#c0392b', 'C': '#4e79a7', 'U': '#8e6fc4'}
    tmpl = 'TACGGTAAA'
    code = {'T': 'A', 'A': 'U', 'C': 'G', 'G': 'C'}
    gen = {'T': 'A', 'A': 'T', 'C': 'G', 'G': 'C'}
    b.append(T(40, 70, 'Mạch bổ sung', size=12.5, anchor='start', fill=GREY)); b.append(T(40, 148, 'Mạch khuôn', size=12.5, anchor='start', fill=GREY))
    b.append(T(40, 250, 'mRNA', size=14, anchor='start', weight='bold', fill='#8e6fc4'))
    for i, ch_ in enumerate(tmpl):
        x = 170 + i * 56
        b.append(R(x, 80, 48, 34, fill=colr[gen[ch_]], stroke=INK, sw=1.6, rx=6)); b.append(T(x + 24, 104, gen[ch_], size=17, weight='bold', fill='white'))
        b.append(R(x, 128, 48, 34, fill=colr[ch_], stroke=INK, sw=1.6, rx=6)); b.append(T(x + 24, 152, ch_, size=17, weight='bold', fill='white'))
        b.append(L(x + 24, 114, x + 24, 128, stroke=INK, w=1.2, dash='2 2'))
        r_ = code[ch_]
        b.append(L(x + 24, 164, x + 24, 222, stroke=GREY, w=1.4, dash='3 3', arrow=True))
        b.append(R(x, 226, 48, 34, fill=colr[r_], stroke=INK, sw=1.6, rx=6)); b.append(T(x + 24, 250, r_, size=17, weight='bold', fill='white'))
    b.append(T(360, 292, 'Nguyên tắc bổ sung: A–U, T–A, G–C, C–G (mạch khuôn → mRNA)', size=13, weight='bold', fill=BLUE))
    b.append(T(360, 314, 'Ví dụ mạch khuôn TAC GGT AAA → mRNA AUG CCA UUU', size=12.5, fill=GREY))
    return svg(720, 332, ''.join(b))


reg('c-s9-b39-phien-ma.svg', fig_phien_ma, 'sinh9/bai-39/tai-ban-phien-ma.json', 3, 'Phiên mã: tạo mRNA từ mạch khuôn (ví dụ)')


# ================= Bài 40–51 =================
def Xc(b, x, y, s=1.0, col=INK, w=5):
    b.append(L(x - 6 * s, y - 12 * s, x + 6 * s, y + 12 * s, stroke=col, w=w)); b.append(L(x + 6 * s, y - 12 * s, x - 6 * s, y + 12 * s, stroke=col, w=w))


def Ic(b, x, y, s=1.0, col=INK, w=5, h=24):
    b.append(L(x, y - h * s / 2, x, y + h * s / 2, stroke=col, w=w))


def cell(b, cx, cy, r, fill='#fdf3dc'):
    b.append(C(cx, cy, r, fill=fill, stroke=INK, w=2))


BL, RD = '#2b6cb0', '#c0392b'


def flowbox(b, x, y, w, h, text, fill=LBLUE, size=12.5):
    b.append(R(x, y, w, h, fill=fill, stroke=INK, sw=1.8, rx=8))
    ls = text.split('\n')
    b.append(TL(x + w / 2, y + h / 2 - (len(ls) - 1) * 8 + 5, ls, size=size, lh=16, weight='bold'))


# ---------- Bài 40 ----------
def fig_dich_ma():
    b = [title(720, 'Dịch mã tại ribosome: mRNA → chuỗi polypeptide')]
    cod = ['AUG', 'GCU', 'UUA', 'GAA']
    colr = ['#e9a23b', '#4e9a8f', '#c0392b', '#4e79a7']
    b.append(L(60, 210, 660, 210, stroke='#8e6fc4', w=6)); b.append(T(40, 215, '5′', size=12, anchor='end')); b.append(T(680, 215, '3′', size=12, anchor='start'))
    for i, c in enumerate(cod):
        x = 150 + i * 90
        b.append(R(x, 196, 80, 28, fill='#efe6fa', stroke='#8e6fc4', sw=1.4, rx=4)); b.append(T(x + 40, 216, c, size=14, weight='bold'))
    b.append(T(60, 246, 'mRNA (các bộ ba = codon)', size=12, anchor='start', fill='#3b4856'))
    # ribosome
    b.append(R(150, 140, 180, 56, fill='#d9d9d9', stroke=INK, sw=2, rx=28)); b.append(T(240, 172, 'ribosome', size=13, weight='bold'))
    # tRNA ở vị trí 2 (codon GCU): anticodon CGA
    b.append(R(172 + 90 - 90 + 0, 100, 0, 0, fill='none', stroke='none'))
    # tRNA 1 (AUG, anticodon UAC) tại x=150..230; tRNA 2 tại 240..320
    for i, (ac, aa) in enumerate((('UAC', 'Met'), ('CGA', 'Ala'))):
        x = 190 + i * 90
        b.append(L(x, 196, x, 124, stroke='#4e9a8f', w=4))
        b.append(R(x - 20, 80, 40, 22, fill='#4e9a8f', stroke=INK, sw=1.4, rx=11)); b.append(T(x, 96, aa, size=11.5, weight='bold', fill='white'))
        b.append(T(x, 118, ac, size=11, weight='bold', fill='#2f6f66'))
    # chuỗi polypeptide
    for k, a in enumerate(('Met', 'Ala')):
        pass
    b.append(L(210, 90, 190, 60, stroke=GREY, w=1.5)) if False else None
    for k, aa in enumerate(('Met', 'Ala', 'Leu')):
        cx = 400 + k * 44
        b.append(C(cx, 90 - k * 8, 18, fill=['#e9a23b', '#4e9a8f', '#c0392b'][k], stroke=INK, w=1.6)); b.append(T(cx, 95 - k * 8, aa, size=11, weight='bold', fill='white'))
        if k: b.append(L(cx - 26, 90 - k * 8 + 8, cx - 18, 90 - k * 8, stroke=INK, w=2))
    b.append(T(470, 40, 'chuỗi polypeptide đang dài ra', size=12, anchor='middle', fill='#3b4856'))
    b.append(L(330, 168, 345, 130, w=2, arrow=True)) if False else None
    b.append(L(560, 160, 560, 196, w=2.4, arrow=True)); b.append(T(570, 182, 'ribosome trượt về 3′', size=11.5, anchor='start', fill='#3b4856'))
    b.append(TL(360, 288, ['Anticodon của tRNA khớp codon trên mRNA theo nguyên tắc bổ sung (A–U, G–C)', 'AUG là codon mở đầu; UAA, UAG, UGA là codon kết thúc'], size=12.5, lh=18, weight='bold', fill='#3b4856'))
    return svg(720, 320, ''.join(b))


reg('c-s9-b40-dich-ma.svg', fig_dich_ma, 'sinh9/bai-40/dich-ma.json', 0, 'Dịch mã tại ribosome (sơ đồ)')


def fig_gene_tinh_trang():
    b = [title(720, 'Mối quan hệ gene → mRNA → protein → tính trạng')]
    names = [('Gene (DNA)', LBLUE), ('mRNA', '#efe6fa'), ('Protein', LYELLOW), ('Tính trạng', LGREEN)]
    steps = ['phiên mã', 'dịch mã', 'biểu hiện']
    for i, (n, f) in enumerate(names):
        x = 30 + i * 175
        b.append(R(x, 80, 125, 56, fill=f, stroke=INK, sw=2, rx=10)); b.append(T(x + 62, 114, n, size=14, weight='bold'))
        if i < 3:
            b.append(L(x + 128, 108, x + 170, 108, w=2.6, arrow=True)); b.append(T(x + 149, 98, steps[i], size=11, fill='#3b4856'))
    b.append(T(360, 190, 'Ví dụ: gene quy định hemoglobin → mRNA → hemoglobin → hồng cầu bình thường', size=12.5, fill=GREY))
    return svg(720, 215, ''.join(b))


reg('c-s9-b40-gene-tinh-trang.svg', fig_gene_tinh_trang, 'sinh9/bai-40/dich-ma.json', 3, 'Sơ đồ gene → tính trạng')


# ---------- Bài 41 ----------
def fig_dot_bien_gene():
    b = [title(720, 'Các dạng đột biến gene (ví dụ trên một đoạn mạch)')]
    colr = {'A': '#e9a23b', 'T': '#4e9a8f', 'G': '#c0392b', 'C': '#4e79a7'}

    def row(y, label, seq, hi, desc):
        b.append(T(24, y + 22, label, size=13, weight='bold', anchor='start'))
        for i, ch_ in enumerate(seq):
            x = 150 + i * 36 + (i // 3) * 10
            b.append(R(x, y, 32, 30, fill=colr[ch_], stroke=RD if i in hi else INK, sw=3.2 if i in hi else 1.4, rx=5)); b.append(T(x + 16, y + 21, ch_, size=15, weight='bold', fill='white'))
        b.append(T(600, y + 21, desc, size=12.5, anchor='start', weight='bold', fill=RD))
    row(56, 'Bình thường', 'ATGGCTAAA', [], '')
    row(116, 'Mất 1 cặp', 'ATGCTAAA', [3], 'mất G')
    row(176, 'Thêm 1 cặp', 'ATGGCCTAAA', [5], 'thêm C')
    row(236, 'Thay thế', 'ATGGATAAA', [4], 'C → A')
    b.append(T(360, 298, 'Các nucleotide từ chỗ biến đổi trở đi bị đọc lệch bộ ba (mất, thêm) hoặc chỉ đổi một bộ ba (thay thế)', size=12, fill=GREY))
    return svg(720, 316, ''.join(b))


reg('c-s9-b41-dot-bien-gene.svg', fig_dot_bien_gene, 'sinh9/bai-41/dot-bien-gene.json', 0, 'Mất, thêm, thay thế một cặp nucleotide (sơ đồ minh họa)')


# ---------- Bài 42 ----------
def fig_nst():
    b = [title(720, 'Nhiễm sắc thể: cấu trúc và bộ NST')]
    # NST kép
    cx, top = 120, 70
    for dx in (-9, 9):
        b.append(R(cx + dx - 8, top, 16, 150, fill='#e9e1f2', stroke=INK, sw=2, rx=8))
    b.append(R(cx - 18, top + 66, 36, 18, fill='#f2c94c', stroke=INK, sw=1.6, rx=6))
    b.append(lead(b, cx - 15, top + 30, 20, top + 4, '', 'start', 12, INK) if False else '')
    b.append(L(cx + 18, top + 30, 210, top + 14, stroke=GREY, w=1.2)); b.append(T(214, top + 18, 'chromatid chị em', size=12, anchor='start'))
    b.append(L(cx + 18, top + 75, 210, top + 75, stroke=GREY, w=1.2)); b.append(T(214, top + 79, 'tâm động', size=12, anchor='start'))
    b.append(T(cx, 258, 'NST kép (kì giữa)', size=13, weight='bold'))
    # 2n vs n
    def kary(x0, label, pairs, single):
        cell(b, x0 + 90, 120, 78, '#fdf3dc')
        for i in range(pairs):
            xx = x0 + 40 + i * 40
            h = 46 if i % 2 == 0 else 32
            Ic(b, xx, 120, 1, RD, 6, h)
            if not single: Ic(b, xx + 11, 120, 1, BL, 6, h)
        b.append(T(x0 + 90, 224, label, size=14, weight='bold'))
    kary(340, '2n = 6 (cặp tương đồng)', 3, False)
    kary(540, 'n = 3 (giao tử)', 3, True) if False else None
    cell(b, 640, 120, 62, '#fdf3dc')
    for i in range(3):
        Ic(b, 612 + i * 28, 120, 1, [RD, BL, RD][i], 6, 46 if i % 2 == 0 else 32)
    b.append(T(640, 224, 'n = 3', size=14, weight='bold'))
    b.append(T(420, 250, '(minh họa: 2n = 6 chỉ để dễ vẽ)', size=11.5, fill=GREY))
    b.append(T(360, 290, 'Mỗi cặp tương đồng: một NST từ bố, một NST từ mẹ (hai màu)', size=12.5, weight='bold', fill='#3b4856'))
    # bảng số NST
    b.append(R(30, 304, 660, 44, fill=LGREY, stroke=GREY, sw=1.2, rx=8))
    b.append(T(360, 332, 'Người 2n = 46   |   Ruồi giấm 2n = 8   |   Đậu Hà Lan 2n = 14   |   Lúa 2n = 24', size=13.5, weight='bold'))
    return svg(720, 366, ''.join(b))


reg('c-s9-b42-nst.svg', fig_nst, 'sinh9/bai-42/nhiem-sac-the.json', 1, 'NST kép và bộ NST 2n, n (sơ đồ)')


# ---------- Bài 43 ----------
def fig_nguyen_phan():
    b = [title(720, 'Nguyên phân: 1 tế bào (2n = 4) → 2 tế bào con (2n = 4)')]
    xs = [95, 265, 435, 605]
    names = ['Kì đầu', 'Kì giữa', 'Kì sau', 'Kì cuối']
    cols = [RD, BL, RD, BL]
    for i, x in enumerate(xs):
        b.append(T(x, 62, names[i], size=14, weight='bold'))
        if i < 3:
            cell(b, x, 140, 66)
        if i == 0:
            for (dx, dy, col) in ((-24, -16, RD), (8, -22, BL), (-10, 18, RD), (24, 10, BL)):
                Xc(b, x + dx, 140 + dy, 1.0 if dx in (-24, 8) else 0.75, col)
            b.append(C(x, 140, 66, fill='none', stroke=GREY, w=1, dash='3 3')) if False else None
        if i == 1:
            b.append(L(x - 62, 140, x + 62, 140, stroke=GREY, w=1.4, dash='4 3'))
            for k, col in enumerate(cols):
                Xc(b, x - 36 + k * 24, 140, 0.85, col)
        if i == 2:
            b.append(L(x - 62, 140, x + 62, 140, stroke=GREY, w=1, dash='4 3'))
            for k, col in enumerate(cols):
                Ic(b, x - 36 + k * 24, 108, 0.9, col, 5, 20); Ic(b, x - 36 + k * 24, 172, 0.9, col, 5, 20)
            b.append(L(x + 70, 124, x + 70, 108, w=2, arrow=True)) if False else None
        if i == 3:
            for cy in (98, 184):
                cell(b, x, cy, 38)
            for k, col in enumerate(cols):
                Ic(b, x - 27 + k * 18, 98, 0.8, col, 4.5, 20); Ic(b, x - 27 + k * 18, 184, 0.8, col, 4.5, 20)
        if i < 3:
            b.append(L(x + 70, 140, x + 98, 140, w=2.4, arrow=True))
    b.append(T(360, 250, 'NST nhân đôi (mỗi NST gồm 2 chromatid) → xếp một hàng → chromatid tách về hai cực → hai nhân mới', size=12.5, fill='#3b4856'))
    b.append(T(360, 274, 'Hai tế bào con có bộ NST giống hệt tế bào mẹ', size=13, weight='bold', fill=BLUE))
    return svg(720, 296, ''.join(b))


reg('c-s9-b43-nguyen-phan.svg', fig_nguyen_phan, 'sinh9/bai-43/nguyen-phan-giam-phan.json', 0, 'Các kì của nguyên phân (sơ đồ, 2n = 4)')


def fig_giam_phan():
    b = [title(720, 'Giảm phân: 1 tế bào (2n = 4) → 4 tế bào con (n = 2)')]
    cell(b, 360, 82, 44)
    for dx, col in ((-22, RD), (-8, BL), (8, RD), (22, BL)):
        Xc(b, 360 + dx, 82, 0.8, col, 4.5)
    b.append(TL(300, 80, ['Tế bào mẹ 2n', 'NST nhân đôi 1 lần'], size=12.5, lh=18, anchor='end', weight='bold')) if False else b.append(TL(300, 80, ['Tế bào mẹ 2n', '(NST đã nhân đôi)'], size=12.5, lh=18, weight='bold'))
    
    for cx in (220, 500):
        cell(b, cx, 196, 42)
        for dx, col in ((-12, RD if cx < 300 else BL), (12, RD if cx < 300 else BL)):
            pass
    # GP I: mỗi tế bào chứa 2 NST kép (một từ mỗi cặp)
    Xc(b, 208, 196, 0.8, RD, 4.5); Xc(b, 232, 196, 0.8, BL, 4.5)
    Xc(b, 488, 196, 0.8, BL, 4.5); Xc(b, 512, 196, 0.8, RD, 4.5)
    b.append(L(190, 128, 210, 152, w=0) ) if False else None
    b.append(L(340, 124, 240, 150, stroke=GREY, w=1.4, arrow=True)); b.append(L(380, 124, 480, 150, stroke=GREY, w=1.4, arrow=True))
    b.append(T(360, 190, 'giảm phân I', size=12, fill='#3b4856')); 
    b.append(L(220, 240, 220, 258, w=2.4, arrow=True)); b.append(L(500, 240, 500, 258, w=2.4, arrow=True)); b.append(T(360, 252, 'giảm phân II', size=12, fill='#3b4856'))
    pos = [(150, RD, BL), (290, RD, BL), (430, BL, RD), (570, BL, RD)]
    # 4 tế bào: mỗi tế bào 2 NST đơn
    kids = [(160, RD, BL), (280, RD, BL), (440, BL, RD), (560, BL, RD)]
    for cx, c1, c2 in kids:
        cell(b, cx, 312, 34)
        Ic(b, cx - 9, 312, 0.8, c1, 4.5, 22); Ic(b, cx + 9, 312, 0.8, c2, 4.5, 22)
    b.append(T(360, 372, '4 tế bào con, mỗi tế bào có bộ NST đơn bội n (một NST của mỗi cặp)', size=13, weight='bold', fill=BLUE))
    return svg(720, 392, ''.join(b))


reg('c-s9-b43-giam-phan.svg', fig_giam_phan, 'sinh9/bai-43/nguyen-phan-giam-phan.json', 2, 'Giảm phân (sơ đồ, 2n = 4)')


def fig_thu_tinh():
    b = [title(720, 'Thụ tinh khôi phục bộ NST lưỡng bội')]
    cell(b, 140, 130, 52, '#fdf3dc'); Ic(b, 126, 130, 1, RD, 6, 36); Ic(b, 154, 130, 1, RD, 6, 28)
    b.append(T(140, 206, 'trứng (n)', size=13, weight='bold'))
    cell(b, 360, 130, 52, '#fdf3dc'); Ic(b, 346, 130, 1, BL, 6, 36); Ic(b, 374, 130, 1, BL, 6, 28)
    b.append(T(360, 206, 'tinh trùng (n)', size=13, weight='bold'))
    b.append(T(250, 136, '+', size=26, weight='bold'))
    b.append(L(424, 130, 500, 130, w=2.6, arrow=True)); b.append(T(462, 118, 'thụ tinh', size=12, fill='#3b4856'))
    cell(b, 580, 130, 62, '#fff2d0')
    for dx, col, h in ((-24, RD, 36), (-8, BL, 36), (8, RD, 28), (24, BL, 28)):
        Ic(b, 580 + dx, 130, 1, col, 6, h)
    b.append(T(580, 220, 'hợp tử (2n)', size=13, weight='bold'))
    b.append(T(360, 262, 'Giảm phân tạo giao tử (n); thụ tinh tạo hợp tử (2n): bộ NST của loài ổn định qua các thế hệ', size=12.5, weight='bold', fill=BLUE))
    return svg(720, 286, ''.join(b))


reg('c-s9-b43-thu-tinh.svg', fig_thu_tinh, 'sinh9/bai-43/nguyen-phan-giam-phan.json', 4, 'Thụ tinh (sơ đồ)')


# ---------- Bài 44 ----------
def fig_gioi_tinh():
    b = [title(720, 'Cơ chế xác định giới tính ở người')]
    def person(x, y, sex, lab):
        if sex == 'f':
            b.append(C(x, y, 22, fill='#fadadd', stroke=INK, w=2))
        else:
            b.append(R(x - 22, y - 22, 44, 44, fill='#d6e6f7', stroke=INK, sw=2, rx=3))
        b.append(T(x, y + 6, lab, size=15, weight='bold'))
    b.append(T(30, 66, 'P', size=16, weight='bold', anchor='start'))
    person(200, 60, 'f', 'XX'); b.append(T(200, 98, 'mẹ', size=12)); b.append(T(360, 66, '×', size=22, weight='bold')); person(520, 60, 'm', 'XY'); b.append(T(520, 98, 'bố', size=12))
    b.append(T(30, 136, 'G', size=16, weight='bold', anchor='start'))
    b.append(T(200, 138, 'trứng: X', size=14, weight='bold')); b.append(T(520, 138, 'tinh trùng: X, Y', size=14, weight='bold'))
    b.append(T(30, 232, 'F', size=16, weight='bold', anchor='start'))
    gx, gy = 250, 170
    for j, g in enumerate(('X', 'Y')):
        b.append(T(gx + 50 + j * 100, gy - 8, g, size=15, weight='bold'))
    b.append(T(gx + 100, gy - 26, 'tinh trùng', size=11.5, fill=GREY))
    for i in range(2):
        b.append(T(gx - 14, gy + 36 + i * 64, 'X', size=15, weight='bold'))
        for j in range(2):
            x, y = gx + j * 100, gy + i * 64
            b.append(R(x, y, 100, 60, fill='#fafafa', stroke=INK, sw=1.4))
            if j == 0: b.append(C(x + 28, y + 30, 16, fill='#fadadd', stroke=INK, w=1.6))
            else: b.append(R(x + 12, y + 14, 32, 32, fill='#d6e6f7', stroke=INK, sw=1.6, rx=3))
            b.append(T(x + 72, y + 36, 'XX' if j == 0 else 'XY', size=14, weight='bold'))
    b.append(T(gx - 40, gy + 36, 'trứng', size=11.5, anchor='end', fill=GREY))
    b.append(T(600, 230, '1 gái (XX) : 1 trai (XY)', size=14, weight='bold', fill=BLUE))
    b.append(T(600, 252, 'tỉ lệ xấp xỉ 1 : 1', size=12.5, fill=GREY))
    return svg(720, 318, ''.join(b))


reg('c-s9-b44-gioi-tinh.svg', fig_gioi_tinh, 'sinh9/bai-44/nst-gioi-tinh.json', 1, 'Sơ đồ xác định giới tính ở người')


# ---------- Bài 45 ----------
def fig_morgan():
    b = [title(720, 'Thí nghiệm của Morgan: di truyền liên kết ở ruồi giấm')]
    def pair(x, y, a, c1, c2, lab):
        chrom(b, x - 12, y, 56, 12, [(0.25, c1), (0.7, c1)]); chrom(b, x + 12, y, 56, 12, [(0.25, c2), (0.7, c2)])
        b.append(T(x, y + 74, lab, size=12.5, weight='bold'))
    b.append(T(30, 50, 'P', size=16, weight='bold', anchor='start'))
    pair(130, 36, 0, RD, RD, 'BV/BV'); b.append(T(130, 124, 'xám, dài', size=11.5)); b.append(T(210, 76, '×', size=20, weight='bold'))
    pair(290, 36, 0, BL, BL, 'bv/bv'); b.append(T(290, 124, 'đen, cụt', size=11.5))
    b.append(L(210, 140, 210, 164, w=2, arrow=True)); b.append(T(30, 190, 'F₁', size=16, weight='bold', anchor='start'))
    pair(210, 166, 0, RD, BL, 'BV/bv'); b.append(T(210, 254, '100% xám, dài', size=11.5, weight='bold'))
    # lai phân tích
    b.append(T(470, 54, 'Lai phân tích: đực F₁ × cái đen, cụt', size=13.5, weight='bold'))
    b.append(T(470, 90, 'BV/bv  ×  bv/bv', size=15, weight='bold'))
    b.append(T(470, 120, 'G: BV, bv  |  bv', size=13.5))
    b.append(L(470, 130, 470, 150, w=2, arrow=True))
    b.append(R(380, 158, 100, 56, fill='#f2f2f2', stroke=INK, sw=1.6, rx=8)); b.append(TL(430, 180, ['1 BV/bv', 'xám, dài'], size=13, lh=18, weight='bold'))
    b.append(R(500, 158, 100, 56, fill='#dfe6f0', stroke=INK, sw=1.6, rx=8)); b.append(TL(550, 180, ['1 bv/bv', 'đen, cụt'], size=13, lh=18, weight='bold'))
    b.append(T(470, 244, 'Tỉ lệ 1 : 1 — hai gene cùng nằm trên một NST nên đi cùng nhau', size=12.5, fill=BLUE, weight='bold'))
    b.append(T(360, 290, 'B: thân xám, b: thân đen; V: cánh dài, v: cánh cụt (ký hiệu minh họa)', size=11.5, fill=GREY))
    return svg(720, 308, ''.join(b))


reg('c-s9-b45-morgan.svg', fig_morgan, 'sinh9/bai-45/di-truyen-lien-ket.json', 0, 'Phép lai của Morgan (sơ đồ)')


# ---------- Bài 46 ----------
def fig_dot_bien_nst():
    b = [title(720, 'Các dạng đột biến cấu trúc NST')]
    cc = {'A': '#e9a23b', 'B': '#4e9a8f', 'C': '#c0392b', 'D': '#4e79a7', 'E': '#8e6fc4', 'F': '#6fbf5a', 'G': '#d98c5f', 'M': '#7f8c8d', 'N': '#a07040', 'O': '#3c9d9b', 'P': '#c25a8a', 'Q': '#5a6ec2'}

    def row(y, label, seq, hi=(), gap=None):
        b.append(T(24, y + 21, label, size=13, weight='bold', anchor='start'))
        for i, ch_ in enumerate(seq):
            x = 150 + i * 44
            if ch_ == '_':
                b.append(R(x, y, 40, 28, fill='white', stroke=GREY, sw=1.4, rx=4)); b.append(T(x + 20, y + 20, '—', size=14, fill=GREY)); continue
            b.append(R(x, y, 40, 28, fill=cc[ch_], stroke=RD if i in hi else INK, sw=3 if i in hi else 1.4, rx=4)); b.append(T(x + 20, y + 20, ch_, size=14, weight='bold', fill='white'))
    row(50, 'Bình thường', 'ABCDEFG')
    row(94, 'Mất đoạn', 'ABC_EFG', [3])
    row(138, 'Lặp đoạn', 'ABCDDEFG', [4])
    row(182, 'Đảo đoạn', 'ABEDCFG', [2, 3, 4])
    row(262, '', 'ABOPQ', [2, 3, 4]) if False else None
    row(238, 'Chuyển đoạn', 'ABOPQ', [2, 3, 4])
    row(270, '', 'MNCDE', [2, 3, 4])
    b.append(T(560, 252, '(trao đổi đoạn giữa', size=11.5, anchor='start', fill=GREY)); b.append(T(560, 268, 'hai NST không tương đồng)', size=11.5, anchor='start', fill=GREY))
    return svg(720, 312, ''.join(b))


reg('c-s9-b46-dot-bien-cau-truc.svg', fig_dot_bien_nst, 'sinh9/bai-46/dot-bien-nst.json', 1, 'Các dạng đột biến cấu trúc NST (sơ đồ)')


def fig_so_luong():
    b = [title(720, 'Đột biến số lượng NST: lệch bội và đa bội')]
    def bars(x, y, n, col, h=44):
        for k in range(n):
            Ic(b, x + k * 16, y, 1, col, 7, h)
    def grp(x, y, lab, n, col, sub):
        cell(b, x, y, 46, '#fdf3dc')
        bars(x - (n - 1) * 8, y, n, col)
        b.append(T(x, y + 72, lab, size=13, weight='bold')); b.append(T(x, y + 90, sub, size=11.5, fill='#3b4856'))
    b.append(T(178, 50, 'Lệch bội (cặp NST số 21)', size=14, weight='bold'))
    grp(60, 130, 'Bình thường', 2, BL, '2 NST số 21'); grp(178, 130, 'Down: 2n + 1', 3, RD, '3 NST số 21 (47)'); grp(296, 130, '2n − 1', 1, RD, 'thể một nhiễm')
    b.append(T(548, 50, 'Đa bội', size=14, weight='bold'))
    grp(430, 130, '2n', 2, BL, 'lưỡng bội'); grp(548, 130, '3n', 3, RD, 'tam bội'); grp(666, 130, '4n', 4, RD, 'tứ bội')
    b.append(T(360, 250, 'Tam bội 3n ở dưa hấu: không có hạt (không tạo giao tử bình thường)', size=12.5, weight='bold', fill=BLUE))
    b.append(T(360, 272, '(minh họa số NST chỉ mang tính sơ đồ)', size=11.5, fill=GREY))
    return svg(720, 292, ''.join(b))


reg('c-s9-b46-so-luong.svg', fig_so_luong, 'sinh9/bai-46/dot-bien-nst.json', 4, 'Lệch bội và đa bội (sơ đồ)')


# ---------- Bài 47 ----------
def fig_pha_he():
    b = [title(720, 'Phả hệ bệnh do gene lặn (a): bố mẹ cùng mang gene')]
    def sym(x, y, sex, st):
        fill = {'n': 'white', 'c': '#bcd6ee', 'b': '#4a4a4a'}[st]
        if sex == 'f': b.append(C(x, y, 22, fill=fill, stroke=INK, w=2))
        else: b.append(R(x - 22, y - 22, 44, 44, fill=fill, stroke=INK, sw=2, rx=2))
    sym(250, 80, 'm', 'c'); sym(430, 80, 'f', 'c')
    b.append(L(272, 80, 408, 80, w=2)); b.append(L(340, 80, 340, 140, w=2)); b.append(L(130, 140, 580, 140, w=2))
    b.append(T(250, 124, 'Aa', size=13, weight='bold')) if False else None
    b.append(T(250, 116, 'Aa', size=13, weight='bold')); b.append(T(430, 116, 'Aa', size=13, weight='bold'))
    kids = [(130, 'f', 'n', 'AA'), (280, 'm', 'c', 'Aa'), (430, 'f', 'c', 'Aa'), (580, 'm', 'b', 'aa')]
    for x, sx, st, g in kids:
        b.append(L(x, 140, x, 168, w=2)); sym(x, 192, sx, st); b.append(T(x, 238, g, size=13, weight='bold'))
    lg = [('n', 'bình thường'), ('c', 'mang gene lặn, không bệnh'), ('b', 'mắc bệnh')]
    for i, (st, tx) in enumerate(lg):
        y = 280
        x = 100 + i * 190
        b.append(R(x, y - 10, 20, 20, fill={'n': 'white', 'c': '#bcd6ee', 'b': '#4a4a4a'}[st], stroke=INK, sw=1.6)); b.append(T(x + 28, y + 5, tx, size=12, anchor='start'))
    b.append(T(360, 316, 'Hình vuông: nam, hình tròn: nữ. Xác suất con mắc bệnh aa = 1/4 khi cả bố mẹ đều Aa', size=12.5, weight='bold', fill=BLUE))
    b.append(T(360, 338, 'Kết hôn gần làm tăng khả năng hai người cùng mang gene lặn', size=12, fill=GREY))
    return svg(720, 356, ''.join(b))


reg('c-s9-b47-pha-he.svg', fig_pha_he, 'sinh9/bai-47/di-truyen-hoc-voi-con-nguoi.json', 2, 'Phả hệ minh họa bệnh do gene lặn')


# ---------- Bài 48 ----------
def fig_chuyen_gene():
    b = [title(720, 'Chuyển gene người vào vi khuẩn để sản xuất insulin')]
    ORG = '#f2a33a'
    xs = [90, 270, 450, 630]
    heads = ['1. Chuẩn bị', '2. Tạo DNA tái tổ hợp', '3. Đưa vào vi khuẩn', '4. Nuôi cấy']
    for x, h in zip(xs, heads):
        b.append(T(x, 54, h, size=13, weight='bold'))
    # 1: plasmid + gene
    b.append(C(60, 130, 28, fill='none', stroke=BL, w=5)); b.append(T(60, 176, 'plasmid', size=11.5))
    b.append(R(104, 110, 56, 18, fill=ORG, stroke=INK, sw=1.4, rx=4)); b.append(T(132, 152, 'gene insulin', size=11.5)); b.append(T(132, 166, '(từ DNA người)', size=11))
    # 2: plasmid with gene inserted
    b.append(C(270, 130, 30, fill='none', stroke=BL, w=5)); b.append(PATH('M %.1f %.1f A 30 30 0 0 1 %.1f %.1f' % (270 - 15, 130 - 26, 270 + 15, 130 - 26), stroke=ORG, w=8) if False else '')
    b.append(R(250, 94, 40, 14, fill=ORG, stroke=INK, sw=1.4, rx=4)); b.append(T(270, 178, 'DNA tái tổ hợp', size=11.5))
    b.append(L(185, 130, 218, 130, w=2.4, arrow=True)); b.append(T(202, 120, 'enzyme', size=10.5, fill=GREY))
    # 3: vi khuẩn
    b.append(R(405, 100, 90, 56, fill='#e3f1de', stroke=INK, sw=2, rx=28)); b.append(C(450, 128, 14, fill='none', stroke=BL, w=3)); b.append(R(442, 108, 16, 7, fill=ORG, stroke=INK, sw=1, rx=2))
    b.append(L(310, 130, 400, 130, w=2.4, arrow=True)); b.append(T(450, 178, 'vi khuẩn (E. coli)', size=11.5))
    # 4: nhiều vi khuẩn + insulin
    for i, (dx, dy) in enumerate(((-26, -14), (14, -20), (-8, 18), (30, 14))):
        b.append(R(630 + dx - 20, 130 + dy - 9, 40, 18, fill='#e3f1de', stroke=INK, sw=1.4, rx=9))
    b.append(L(500, 130, 580, 130, w=2.4, arrow=True)); b.append(T(630, 178, 'sinh sản nhanh, tạo insulin', size=11.5))
    b.append(R(80, 214, 560, 40, fill=LYELLOW, stroke=INK, sw=1.6, rx=8)); b.append(T(360, 240, 'Sản phẩm: insulin chữa bệnh đái tháo đường (quy mô công nghiệp)', size=13, weight='bold'))
    return svg(720, 276, ''.join(b))


reg('c-s9-b48-chuyen-gene.svg', fig_chuyen_gene, 'sinh9/bai-48/ung-dung-cong-nghe-di-truyen.json', 0, 'Kĩ thuật chuyển gene (sơ đồ)')


# ---------- Bài 49 ----------
def fig_chon_loc():
    b = [title(720, 'Chọn lọc nhân tạo và chọn lọc tự nhiên')]
    rows = [('Chọn lọc nhân tạo', ['Biến dị ở vật nuôi,\ncây trồng', 'Con người giữ lại biến dị\ncó lợi cho mình', 'Giống vật nuôi,\ncây trồng mới'], '#e3f1de', 66),
            ('Chọn lọc tự nhiên', ['Biến dị trong\nquần thể', 'Môi trường: cá thể thích nghi\nsống sót, sinh sản nhiều', 'Đặc điểm thích nghi,\nloài mới'], '#dfe9f7', 176)]
    for name, boxes, f, y in rows:
        b.append(T(30, y - 8, name, size=14, weight='bold', anchor='start'))
        for i, t in enumerate(boxes):
            x = 30 + i * 230
            flowbox(b, x, y, 190, 56, t, f, 12)
            if i < 2: b.append(L(x + 192, y + 28, x + 226, y + 28, w=2.4, arrow=True))
    b.append(T(360, 270, 'Điểm khác: nhân tố chọn lọc là con người (nhân tạo) hay điều kiện môi trường (tự nhiên)', size=12.5, fill=GREY))
    return svg(720, 288, ''.join(b))


reg('c-s9-b49-chon-loc.svg', fig_chon_loc, 'sinh9/bai-49/khai-niem-tien-hoa-chon-loc.json', 2, 'So sánh chọn lọc nhân tạo và chọn lọc tự nhiên')


def moth(b, x, y, dark, s=1.0):
    col = '#3a3a3a' if dark else '#f0ece0'
    b.append(R(x - 11 * s, y - 4 * s, 22 * s, 8 * s, fill=col, stroke=INK, sw=1, rx=4))
    b.append(R(x - 3 * s, y - 9 * s, 6 * s, 18 * s, fill=col, stroke=INK, sw=1, rx=3))


def fig_buom():
    b = [title(720, 'Bướm sâu đo bạch dương: chọn lọc theo màu thân cây (minh họa)')]
    panels = [(30, 'Thân cây sáng (trước công nghiệp hóa)', '#e8e4d6', [(0, 1), (1, 0), (1, 0), (0, 0), (1, 0), (1, 0), (1, 0), (0, 0)], 7, 1),
              (370, 'Thân cây ám khói đen', '#4a4a48', [(0, 1), (1, 0), (0, 0), (0, 0), (0, 1), (0, 0), (0, 0), (0, 0)], 1, 6)]
    rnd = random.Random(3)
    for x, ttl, trunk, _, nl, nd in panels:
        b.append(T(x + 150, 54, ttl, size=13, weight='bold'))
        b.append(R(x, 66, 300, 190, fill=trunk, stroke=INK, sw=2, rx=6))
        for k in range(nl + nd):
            dark = k >= nl
            mx = x + 30 + (k % 4) * 70 + rnd.randint(-6, 6)
            my = 100 + (k // 4) * 80 + rnd.randint(-8, 8)
            moth(b, mx, my, dark, 1.5)
    b.append(T(180, 280, 'Nhiều bướm sáng, ít bướm đen', size=12.5, fill='#3b4856')); b.append(T(520, 280, 'Bướm đen ít bị phát hiện → tăng dần', size=12.5, fill='#3b4856'))
    b.append(T(360, 308, 'Số lượng bướm vẽ chỉ để minh họa, không phải số liệu thực', size=11.5, fill=GREY))
    return svg(720, 326, ''.join(b))


reg('c-s9-b49-buom.svg', fig_buom, 'sinh9/bai-49/khai-niem-tien-hoa-chon-loc.json', 4, 'Minh họa chọn lọc tự nhiên ở bướm sâu đo')


# ---------- Bài 50 ----------
def giraffe(b, x, y, neck, col='#e9c46a'):
    b.append(R(x - 26, y, 52, 24, fill=col, stroke=INK, sw=1.6, rx=12))
    for dx in (-18, -8, 8, 18): b.append(L(x + dx, y + 22, x + dx, y + 44, stroke=INK, w=3))
    b.append(L(x + 18, y + 4, x + 24, y - neck, stroke=col, w=9)); b.append(L(x + 18, y + 4, x + 24, y - neck, stroke=INK, w=1.2)) if False else None
    b.append(C(x + 28, y - neck - 4, 6, fill=col, stroke=INK, w=1.4))


def fig_lamarck_darwin():
    b = [title(720, 'Lamarck và Darwin giải thích sự hình thành cổ dài ở hươu cao cổ')]
    b.append(R(20, 44, 330, 250, fill='#fdf1f0', stroke=GREY, sw=1.4, rx=10)); b.append(T(185, 68, 'Lamarck', size=15, weight='bold'))
    b.append(R(370, 44, 330, 250, fill='#eef6ec', stroke=GREY, sw=1.4, rx=10)); b.append(T(535, 68, 'Darwin', size=15, weight='bold'))
    for i, (neck, tx) in enumerate(((10, 'cổ ngắn'), (30, 'vươn cổ nhiều'), (48, 'cổ dài ra'))):
        x = 70 + i * 100
        giraffe(b, x, 150 + (48 - neck) * 0.0, neck); b.append(T(x, 224, tx, size=11.5))
        if i < 2: b.append(L(x + 38, 140, x + 62, 140, w=2, arrow=True))
    b.append(T(185, 252, 'Đặc điểm do tập quán được di truyền (chưa chính xác)', size=11.5, fill='#8a3a33', weight='bold'))
    b.append(T(185, 274, 'Sinh vật chủ động biến đổi theo ngoại cảnh', size=11.5, fill=GREY))
    for i, (neck, tx) in enumerate(((10, 'cổ ngắn'), (30, 'cổ trung bình'), (48, 'cổ dài'))):
        giraffe(b, 420 + i * 70, 150, neck)
    b.append(T(535, 224, 'biến dị cá thể có sẵn trong quần thể', size=11.5))
    b.append(T(535, 246, 'thức ăn ở cao → cá thể cổ dài sống sót, sinh sản nhiều', size=11.5, weight='bold', fill='#2f6b2a'))
    b.append(T(535, 268, 'chọn lọc tự nhiên giữ lại biến dị có lợi', size=11.5, fill=GREY))
    b.append(T(360, 316, 'Hình vẽ minh họa, không đo đúng tỉ lệ', size=11, fill=GREY))
    return svg(720, 330, ''.join(b))


reg('c-s9-b50-lamarck-darwin.svg', fig_lamarck_darwin, 'sinh9/bai-50/co-che-tien-hoa.json', 1, 'So sánh quan điểm Lamarck và Darwin (minh họa)')


def fig_nhan_to_tien_hoa():
    b = [title(720, 'Các nhân tố tiến hóa tác động lên quần thể')]
    cell(b, 360, 160, 62, '#fdf3dc'); b.append(T(360, 156, 'Quần thể', size=14, weight='bold')); b.append(T(360, 176, '(đơn vị tiến hóa)', size=11.5))
    fac = ['Đột biến', 'Di – nhập gene', 'Chọn lọc tự nhiên', 'Phiêu bạt di truyền', 'Giao phối không ngẫu nhiên']
    pos = [(110, 70), (610, 70), (90, 210), (630, 210), (360, 276)]
    for (x, y), t in zip(pos, fac):
        w = 170 if len(t) > 18 else 140
        b.append(R(x - w / 2, y - 18, w, 36, fill=LBLUE, stroke=INK, sw=1.8, rx=8)); b.append(T(x, y + 5, t, size=12.5, weight='bold'))
        dx, dy = 360 - x, 160 - y
        d = math.hypot(dx, dy)
        sx, sy = x + dx / d * (w / 2 if abs(dx) > abs(dy) * 1.5 else 20), y + dy / d * (18 if abs(dx) <= abs(dy) * 1.5 else 0)
        ex, ey = 360 - dx / d * 68, 160 - dy / d * 68
        b.append(L(sx, sy, ex, ey, w=2, arrow=True))
    b.append(T(360, 318, 'Nguyên liệu tiến hóa: đột biến và biến dị tổ hợp', size=12.5, weight='bold', fill=BLUE))
    return svg(720, 336, ''.join(b))


reg('c-s9-b50-nhan-to.svg', fig_nhan_to_tien_hoa, 'sinh9/bai-50/co-che-tien-hoa.json', 3, 'Các nhân tố tiến hóa (sơ đồ)')


# ---------- Bài 51 ----------
def fig_phat_sinh_su_song():
    b = [title(720, 'Các giai đoạn phát sinh sự sống')]
    st = [('Tiến hóa hóa học', 'chất vô cơ → chất hữu cơ\n(đơn giản → phức tạp)', '#e6eef7'), ('Tiến hóa tiền sinh học', 'hình thành tế bào\nnguyên thủy', '#fdf3dc'), ('Tiến hóa sinh học', 'tế bào nguyên thủy →\ncác loài sinh vật', '#e3f1de')]
    for i, (h, d, f) in enumerate(st):
        x = 30 + i * 230
        b.append(R(x, 56, 200, 110, fill=f, stroke=INK, sw=2, rx=10)); b.append(T(x + 100, 82, h, size=13, weight='bold')); b.append(TL(x + 100, 116, d.split('\n'), size=12, lh=18))
        if i < 2: b.append(L(x + 204, 110, x + 226, 110, w=2.6, arrow=True))
    b.append(T(360, 210, 'Trái Đất hình thành khoảng 4,6 tỉ năm trước; sự sống đầu tiên xuất hiện khoảng 3,5 tỉ năm trước', size=12.5, weight='bold', fill=BLUE))
    return svg(720, 232, ''.join(b))


reg('c-s9-b51-phat-sinh.svg', fig_phat_sinh_su_song, 'sinh9/bai-51/phat-sinh-su-song.json', 0, 'Ba giai đoạn phát sinh sự sống')


def fig_dai_dia_chat():
    b = [title(720, 'Các đại trong lịch sử Trái Đất (sơ đồ, không theo tỉ lệ)')]
    dai = [('Thái cổ', '#d9c7e6'), ('Nguyên sinh', '#c5d9ee'), ('Cổ sinh', '#cde7d3'), ('Trung sinh', '#f6e3b0'), ('Tân sinh', '#f4c9b8')]
    for i, (n, f) in enumerate(dai):
        x = 24 + i * 135
        b.append(POLY([(x, 70), (x + 125, 70), (x + 135, 106), (x + 125, 142), (x, 142), (x + 10, 106)], fill=f, stroke=INK, sw=1.8))
        b.append(T(x + 67, 112, n, size=14, weight='bold'))
    b.append(T(24, 60, '4,6 tỉ năm trước', size=11.5, anchor='start', fill=GREY)); b.append(T(696, 60, 'hiện nay', size=11.5, anchor='end', fill=GREY))
    b.append(L(24, 160, 690, 160, w=2, arrow=True)) if False else None
    ev = [(0, 'Sự sống đầu tiên\n(~3,5 tỉ năm trước)'), (3, 'Bò sát khổng lồ\n(khủng long) phát triển'), (4, 'Thú, chim phát triển;\nloài người xuất hiện')]
    for i, t in ev:
        x = 24 + i * 135 + 67
        b.append(L(x, 144, x, 176, w=1.6)); b.append(R(x - 66, 176, 132, 46, fill='white', stroke=GREY, sw=1.4, rx=6)); b.append(TL(x, 196, t.split('\n'), size=11, lh=15))
    return svg(720, 244, ''.join(b))


reg('c-s9-b51-dai.svg', fig_dai_dia_chat, 'sinh9/bai-51/phat-sinh-su-song.json', 2, 'Các đại địa chất (sơ đồ không theo tỉ lệ)')


def fig_nguoi():
    b = [title(720, 'Các dạng người trong quá trình tiến hóa (sơ đồ)')]
    names = [('Người vượn', 'Australopithecus', 70), ('Người khéo léo', 'Homo habilis', 84), ('Người đứng thẳng', 'Homo erectus', 98), ('Người hiện đại', 'Homo sapiens', 112)]
    for i, (vn, la, h) in enumerate(names):
        x = 90 + i * 180
        base = 190
        top = base - h
        b.append(C(x, top - 10, 11 + i * 1.5, fill='#e5c9a8', stroke=INK, w=1.8))
        b.append(L(x, top, x, base - 36, stroke=INK, w=6)); b.append(L(x, base - 36, x - 10, base, stroke=INK, w=5)); b.append(L(x, base - 36, x + 10, base, stroke=INK, w=5))
        b.append(L(x, top + 10, x - 14, base - 50, stroke=INK, w=4)); b.append(L(x, top + 10, x + 14, base - 50, stroke=INK, w=4))
        b.append(T(x, 216, vn, size=13, weight='bold')); b.append(T(x, 235, la, size=12, fill='#3b4856'))
        if i < 3: b.append(L(x + 50, 130, x + 130, 130, w=2.4, arrow=True))
    b.append(T(360, 266, 'Hình người chỉ là biểu tượng sơ đồ, không phải tái hiện hình dạng thật', size=11.5, fill=GREY))
    return svg(720, 284, ''.join(b))


reg('c-s9-b51-nguoi.svg', fig_nguoi, 'sinh9/bai-51/phat-sinh-su-song.json', 4, 'Các dạng người trong tiến hóa (sơ đồ)')


if __name__ == '__main__':
    import glob
    write_figs('sinh9', FIGS)
    for rel, after, name, cap in ATTACH:
        subj, path = rel.split('/', 1)
        hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', path)) + glob.glob(os.path.join(ROOT, 'content', subj, '*', path))
        assert hits, rel
        attach(subj, os.path.relpath(hits[0], os.path.join(ROOT, 'content', subj)), after, name, cap)
    print('sinh9: %d hình' % len(FIGS))
