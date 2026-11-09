# Sinh hình minh họa Vật lí 12 (SVG) ghi ra content/ly12/figures/.
# Chạy: python3 tools/build-ly12-figures.py
import os, math, random, html
OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'ly12', 'figures')
INK, MUTED, BLUE, RED, GREEN, GREY, FILL = '#1d2733', '#5b6775', '#4e79a7', '#c0392b', '#2e8b57', '#9aa5b1', '#e8f1fa'

def svg(w, h, parts, caption):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Segoe UI, Arial, sans-serif">'
            + ''.join(parts)
            + f'<text x="{w/2}" y="{h-8}" font-size="13" text-anchor="middle" fill="{MUTED}">{caption}</text></svg>\n')

def txt(x, y, s, size=14, color=INK, bold=False, anchor='middle'):
    b = ' font-weight="bold"' if bold else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}"{b}>{html.escape(s, quote=False)}</text>'

def arrow_line(x1, y1, x2, y2, color=INK, w=1.8, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ''
    a = math.atan2(y2-y1, x2-x1); L = 10
    p1 = (x2 - L*math.cos(a-0.4), y2 - L*math.sin(a-0.4))
    p2 = (x2 - L*math.cos(a+0.4), y2 - L*math.sin(a+0.4))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"{d}/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')

# ---------- Bài 1: cấu trúc chất và chuyển thể ----------
def fig_ba_the():
    random.seed(3)
    parts = []
    # rắn: lưới đều
    x0, y0 = 40, 60
    parts.append(f'<rect x="{x0}" y="{y0}" width="100" height="100" rx="8" fill="{FILL}" stroke="{BLUE}"/>')
    for i in range(4):
        for j in range(4):
            parts.append(f'<circle cx="{x0+15+i*23}" cy="{y0+15+j*23}" r="7" fill="{BLUE}"/>')
    # lỏng: sắp xếp gần nhau, không đều
    x1 = 190
    parts.append(f'<rect x="{x1}" y="{y0}" width="100" height="100" rx="8" fill="{FILL}" stroke="{BLUE}"/>')
    for k in range(16):
        cx = x1 + 12 + random.random()*76; cy = y0 + 12 + random.random()*76
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{BLUE}"/>')
    # khí: thưa, chuyển động
    x2 = 340
    parts.append(f'<rect x="{x2}" y="{y0}" width="100" height="100" rx="8" fill="{FILL}" stroke="{BLUE}"/>')
    for k in range(6):
        cx = x2 + 12 + random.random()*76; cy = y0 + 12 + random.random()*76
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{BLUE}"/>')
        parts.append(arrow_line(cx, cy, cx + 9, cy - 6, RED, 1.4))
    parts.append(txt(x0+50, 190, 'Chất rắn', 15, bold=True))
    parts.append(txt(x1+50, 190, 'Chất lỏng', 15, bold=True))
    parts.append(txt(x2+50, 190, 'Chất khí', 15, bold=True))
    parts.append(txt(x0+50, 210, 'trật tự, dao động', 12, MUTED))
    parts.append(txt(x1+50, 210, 'gần nhau, hỗn loạn', 12, MUTED))
    parts.append(txt(x2+50, 210, 'thưa, tự do', 12, MUTED))
    return svg(490, 240, parts, 'Sắp xếp phân tử trong ba thể (minh họa)')

def fig_chuyen_the():
    parts = []
    # ba thể
    pos = {'Rắn': (110, 80), 'Lỏng': (330, 80), 'Khí': (220, 230)}
    for name, (x, y) in pos.items():
        parts.append(f'<rect x="{x-60}" y="{y-24}" width="120" height="48" rx="10" fill="{FILL}" stroke="{BLUE}" stroke-width="1.5"/>')
        parts.append(txt(x, y+6, name, 16, bold=True))
    # rắn -> lỏng: nóng chảy (trên); lỏng -> rắn: đông đặc (dưới)
    parts.append(arrow_line(172, 70, 268, 70, RED))
    parts.append(txt(220, 62, 'nóng chảy', 13, RED))
    parts.append(arrow_line(268, 92, 172, 92, BLUE))
    parts.append(txt(220, 112, 'đông đặc', 13, BLUE))
    # lỏng -> khí: hóa hơi; khí -> lỏng: ngưng tụ
    parts.append(arrow_line(340, 106, 270, 205, RED))
    parts.append(txt(290, 150, 'hóa hơi', 13, RED, anchor='end'))
    parts.append(arrow_line(296, 210, 364, 110, BLUE))
    parts.append(txt(330, 200, 'ngưng tụ', 13, BLUE, anchor='start'))
    # rắn -> khí: thăng hoa; khí -> rắn: kết tinh
    parts.append(arrow_line(120, 106, 184, 205, RED))
    parts.append(txt(118, 176, 'thăng hoa', 13, RED, anchor='end'))
    parts.append(arrow_line(190, 212, 118, 110, BLUE))
    parts.append(txt(112, 136, 'kết tinh', 13, BLUE, anchor='end'))
    parts.append(txt(430, 22, 'Đỏ: thu nhiệt', 12, RED, anchor='end'))
    parts.append(txt(430, 38, 'Xanh: toả nhiệt', 12, BLUE, anchor='end'))
    return svg(440, 280, parts, 'Sơ đồ các quá trình chuyển thể')

# ---------- Bài 2: quy ước dấu Q và A ----------
def fig_quy_uoc_dau():
    parts = []
    cx, cy = 220, 130
    parts.append(f'<rect x="{cx-70}" y="{cy-40}" width="140" height="80" rx="10" fill="{FILL}" stroke="{BLUE}" stroke-width="1.6"/>')
    parts.append(txt(cx, cy-4, 'Vật', 17, bold=True))
    parts.append(txt(cx, cy+16, '(khí, chất lỏng…)', 12, MUTED))
    # nhận: mũi tên hướng vào vật (bên trái và trên)
    parts.append(arrow_line(60, 70, cx-72, cy-14, RED, 2))
    parts.append(txt(60, 60, 'Q > 0: nhận nhiệt', 13, RED, anchor='start'))
    parts.append(arrow_line(60, 200, cx-72, cy+14, GREEN, 2))
    parts.append(txt(60, 222, 'A > 0: nhận công', 13, GREEN, anchor='start'))
    # truyền / thực hiện: mũi tên đi ra khỏi vật (bên phải)
    parts.append(arrow_line(cx+72, cy-14, 380, 70, RED, 2))
    parts.append(txt(380, 60, 'Q < 0: truyền nhiệt', 13, RED, anchor='end'))
    parts.append(arrow_line(cx+72, cy+14, 380, 200, GREEN, 2))
    parts.append(txt(380, 222, 'A < 0: thực hiện công', 13, GREEN, anchor='end'))
    return svg(440, 250, parts, 'Quy ước dấu của nhiệt lượng Q và công A đối với vật')

# ---------- Bài 3: các mốc nhiệt độ ở ba thang ----------
def fig_thang_nhiet_do():
    parts = []
    cols = ['Celsius (°C)', 'Kelvin (K)', 'Fahrenheit (°F)']
    rows = [('Độ không tuyệt đối', ['−273,15', '0', '−459,67']),
            ('Nước đóng băng', ['0', '273,15', '32']),
            ('Nước sôi (áp suất chuẩn)', ['100', '373,15', '212'])]
    x0, y0, cw, rh = 20, 30, 150, 52
    x_lab = x0
    parts.append(f'<rect x="{x0}" y="{y0}" width="{170+cw*3}" height="34" fill="{BLUE}" rx="6"/>')
    parts.append(txt(x0+85, y0+22, 'Mốc nhiệt độ', 13, '#ffffff', True))
    for j, c in enumerate(cols):
        parts.append(txt(x0+170+j*cw+cw/2, y0+22, c, 13, '#ffffff', True))
    for i, (name, vals) in enumerate(rows):
        y = y0 + 34 + i*rh
        parts.append(f'<rect x="{x0}" y="{y}" width="{170+cw*3}" height="{rh}" fill="{FILL if i%2==0 else "#ffffff"}" stroke="{GREY}" stroke-width="0.8"/>')
        parts.append(txt(x0+10, y+rh/2+5, name, 13, INK, False, 'start'))
        for j, v in enumerate(vals):
            parts.append(txt(x0+170+j*cw+cw/2, y+rh/2+6, v, 15, INK, True))
    parts.append(txt(x0, y0+34+3*rh+30, 'Công thức: T(K) = t(°C) + 273,15;   t(°F) = 32 + 1,8·t(°C)', 13, MUTED, False, 'start'))
    return svg(640, 280, parts, 'Các mốc nhiệt độ quan trọng trong ba thang đo')

def bar_chart(items, unit, w=440, h=290, title='', caption='', maxv=None, color=BLUE):
    parts = []
    L, R, T, B = 130, w-30, 20, h-50
    maxv = maxv or max(v for _, v in items) * 1.1
    n = len(items); bh = (B - T) / n
    for i, (name, v) in enumerate(items):
        y = T + i*bh + bh*0.18
        bw = (R - L) * v / maxv
        parts.append(txt(L-8, y+bh*0.42, name, 13, INK, False, 'end'))
        parts.append(f'<rect x="{L}" y="{y:.1f}" width="{bw:.1f}" height="{bh*0.62:.1f}" fill="{color}" rx="3"/>')
        parts.append(txt(L+bw+6, y+bh*0.42, f'{v:g} {unit}', 13, INK, True, 'start'))
    parts.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="{MUTED}" stroke-width="1.2"/>')
    return svg(w, h, parts, caption)

def fig_nhiet_dung_rieng():
    items = [('Nước', 4200), ('Nước đá', 2100), ('Đất', 800), ('Sắt', 440), ('Đồng', 380), ('Thuỷ ngân', 140), ('Chì', 130)]
    return bar_chart(items, 'J/(kg·K)', 460, 300, caption='Nhiệt dung riêng c của một số chất (gần đúng)', maxv=6200)

def heating_curve(points, labels, caption, w=440, h=300, xlab='Q (nhiệt lượng cung cấp)', ylab='t (°C)', ymin=None, ymax=None):
    # points: danh sách (x, y) theo thứ tự; labels: [(x, y, text, color, anchor)]
    L, R, T, B = 60, w-20, 20, h-56
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    x0, x1 = 0, max(xs)*1.05
    y0 = ymin if ymin is not None else min(ys)-10
    y1 = ymax if ymax is not None else max(ys)+15
    sx = lambda x: L + (x - x0)/(x1-x0)*(R-L)
    sy = lambda y: B - (y - y0)/(y1-y0)*(B-T)
    parts = []
    parts.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{R}" y2="{sy(0):.1f}" stroke="{GREY}" stroke-dasharray="4 3"/>')
    parts.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="{MUTED}" stroke-width="1.4"/>')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTED}" stroke-width="1.4"/>')
    pts = ' '.join(f'{sx(x):.1f},{sy(y):.1f}' for x, y in points)
    parts.append(f'<polyline points="{pts}" fill="none" stroke="{RED}" stroke-width="2.6"/>')
    parts.append(txt(L-6, T+6, ylab, 13, MUTED, False, 'end'))
    parts.append(txt(R, B+18, xlab, 13, MUTED, False, 'end'))
    for x, y, t, col, anc in labels:
        parts.append(txt(sx(x), sy(y)-10, t, 13, col, True, anc))
    return svg(w, h, parts, caption)

def fig_do_thi_nong_chay():
    # nước đá -10 °C -> 0 °C -> nóng chảy (0 °C) -> nước 0 °C -> 20 °C
    pts = [(0, -10), (60, 0), (260, 0), (300, 0), (360, 20)]
    labels = [(160, 0, 'nóng chảy: t không đổi', BLUE, 'middle'), (30, -6, 'nước đá', INK, 'start'), (330, 14, 'nước', INK, 'start')]
    return heating_curve(pts, labels, 'Đồ thị nhiệt độ theo nhiệt lượng khi đun nước đá từ −10 °C (minh họa)', ymin=-14, ymax=26, h=320)

def fig_do_thi_hoa_hoi():
    pts = [(0, 25), (75, 100), (250, 100), (265, 100), (300, 120)]
    labels = [(160, 100, 'hoá hơi: t không đổi (100 °C)', BLUE, 'middle'), (30, 40, 'nước 25 °C', INK, 'start'), (290, 128, 'hơi nước', INK, 'end')]
    return heating_curve(pts, labels, 'Đồ thị nhiệt độ theo nhiệt lượng khi đun nước từ 25 °C đến hơi (minh họa)', ymin=0, ymax=140, h=320)

def fig_can_bang_nhiet():
    parts = []
    # bình trái: nước nóng 100 °C; bình phải: nước lạnh 20 °C; giữa: hỗn hợp 40 °C
    def vessel(x, y, w, h, fill, label, sub):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{MUTED}" stroke-width="1.4"/>'
                + txt(x+w/2, y+h/2-2, label, 15, INK, True) + txt(x+w/2, y+h/2+18, sub, 13, MUTED))
    parts.append(vessel(30, 60, 120, 110, '#fbe3d6', 'Nước nóng', '100 °C, m₁'))
    parts.append(vessel(290, 60, 120, 110, '#d6ebfb', 'Nước lạnh', '20 °C, m₂'))
    parts.append(arrow_line(152, 115, 286, 115, RED, 2.2))
    parts.append(txt(219, 104, 'nhiệt truyền', 13, RED))
    parts.append(txt(219, 132, 'từ nóng sang lạnh', 12, MUTED))
    parts.append(txt(210, 200, 'Khi cân bằng nhiệt: t = 40 °C', 15, INK, True))
    parts.append(txt(210, 222, 'Q toả = Q thu  ⇒  m₁·c·(100 − 40) = m₂·c·(40 − 20)', 13, MUTED))
    return svg(440, 250, parts, 'Hai khối nước trao đổi nhiệt đến khi cân bằng nhiệt')

def fig_khi_ap_suat():
    random.seed(7)
    parts = []
    x0, y0, w, h = 50, 50, 280, 170
    parts.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{FILL}" stroke="{BLUE}" stroke-width="2.4"/>')
    # quỹ đạo phân tử ngắn: mũi tên chỉ hướng
    pts = [(120, 110, 40, -30), (210, 170, -25, -35), (260, 90, -30, 25), (150, 190, 35, -20), (230, 130, 25, 30)]
    for (cx, cy, dx, dy) in pts:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{BLUE}"/>')
        parts.append(arrow_line(cx, cy, cx+dx*0.6, cy+dy*0.6, INK, 1.4))
    # lực va chạm lên thành bên phải
    for yy in (80, 120, 160):
        parts.append(arrow_line(x0+w+26, yy, x0+w+4, yy, RED, 2))
    parts.append(txt(x0+w+30, 118, 'lực do va chạm', 13, RED, anchor='start'))
    parts.append(txt(x0+w+30, 134, 'tạo áp suất lên thành', 13, RED, anchor='start'))
    return svg(500, 270, parts, 'Mô hình: áp suất khí là do phân tử va chạm vào thành bình')

def axes_frame(L, R, T, B, xlab, ylab):
    parts = []
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R+8}" y2="{B}" stroke="{MUTED}" stroke-width="1.4"/>')
    parts.append(f'<line x1="{L}" y1="{B+6}" x2="{L}" y2="{T-8}" stroke="{MUTED}" stroke-width="1.4"/>')
    parts.append(txt(R+8, B+18, xlab, 13, MUTED, False, 'end'))
    parts.append(txt(L-8, T-10, ylab, 13, MUTED, False, 'end'))
    return parts

def fig_boyle():
    L, R, T, B = 70, 400, 30, 240
    parts = axes_frame(L, R, T, B, 'V', 'p')
    sx = lambda v: L + v/10*(R-L-20)
    sy = lambda p: B - p/10*(B-T-10)
    k1, k2 = 18, 36   # pV = k (đơn vị tuỳ ý): đẳng nhiệt T1 < T2
    for k, col, lab in [(k1, BLUE, 'T₁'), (k2, RED, 'T₂ > T₁')]:
        pts = []
        for i in range(1, 101):
            v = 0.5 + i*0.095
            pp = k / v
            if pp <= 9.6:
                pts.append(f'{sx(v):.1f},{sy(pp):.1f}')
        parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.4"/>')
        vx = 9.4; parts.append(txt(sx(vx)+6, sy(k/vx)-6, lab, 14, col, True, 'start'))
    # hai điểm cùng đường đẳng nhiệt T1
    for v in (3.0, 6.0):
        pp = k1 / v
        parts.append(f'<circle cx="{sx(v):.1f}" cy="{sy(pp):.1f}" r="4" fill="{INK}"/>')
        parts.append(f'<line x1="{sx(v):.1f}" y1="{sy(pp):.1f}" x2="{sx(v):.1f}" y2="{B}" stroke="{GREY}" stroke-dasharray="4 3"/>')
        parts.append(f'<line x1="{L}" y1="{sy(pp):.1f}" x2="{sx(v):.1f}" y2="{sy(pp):.1f}" stroke="{GREY}" stroke-dasharray="4 3"/>')
    parts.append(txt(sx(3.0)+4, B+16, 'V₁', 13, INK, True, 'start'))
    parts.append(txt(sx(6.0)+4, B+16, 'V₂', 13, INK, True, 'start'))
    parts.append(txt(L-6, sy(k1/3.0)+4, 'p₁', 13, INK, True, 'end'))
    parts.append(txt(L-6, sy(k1/6.0)+4, 'p₂', 13, INK, True, 'end'))
    return svg(440, 300, parts, 'Đường đẳng nhiệt p–V: pV không đổi; T₂ > T₁ nằm xa gốc hơn')

def fig_charles():
    L, R, T, B = 70, 400, 30, 240
    parts = axes_frame(L, R, T, B, 'T (K)', 'V')
    sx = lambda t: L + t/600*(R-L-20)
    sy = lambda v: B - v/10*(B-T-10)
    for slope, col, lab in [(1.0/60, RED, 'p₁ (nhỏ hơn)'), (1.0/120, BLUE, 'p₂ (lớn hơn)')]:
        t_end = 560
        parts.append(f'<line x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(t_end):.1f}" y2="{sy(t_end*slope):.1f}" stroke="{col}" stroke-width="2.4"/>')
        parts.append(txt(sx(t_end)-6, sy(t_end*slope)-8, lab, 13, col, True, 'end'))
    parts.append(txt(sx(0)+4, B+16, '0 K', 13, INK, False, 'start'))
    parts.append(txt(sx(300), B+16, '300', 13, MUTED))
    return svg(440, 290, parts, 'Đường đẳng áp V–T: V tỉ lệ thuận với T (K)')

def fig_duong_bien_doi():
    L, R, T, B = 70, 400, 30, 250
    parts = axes_frame(L, R, T, B, 'V', 'p')
    sx = lambda v: L + v/10*(R-L-20)
    sy = lambda p: B - p/10*(B-T-10)
    P1, P2 = (2.0, 8.0), (6.0, 3.0)   # (V, p)
    P3 = (P1[0], P2[1])               # đẳng tích 1->3 rồi đẳng áp 3->2
    P4 = (P2[0], P1[1])               # đẳng áp 1->4 rồi đẳng tích 4->2
    def line(a, b, col, dash=False):
        d = ' stroke-dasharray="6 4"' if dash else ''
        return f'<line x1="{sx(a[0]):.1f}" y1="{sy(a[1]):.1f}" x2="{sx(b[0]):.1f}" y2="{sy(b[1]):.1f}" stroke="{col}" stroke-width="2.2"{d}/>'
    parts.append(line(P1, P3, BLUE)); parts.append(line(P3, P2, BLUE))
    parts.append(line(P1, P4, RED)); parts.append(line(P4, P2, RED))
    for P, lab, anc in [(P1, '1', 'end'), (P2, '2', 'start')]:
        parts.append(f'<circle cx="{sx(P[0]):.1f}" cy="{sy(P[1]):.1f}" r="4.5" fill="{INK}"/>')
        parts.append(txt(sx(P[0])+(-8 if anc=='end' else 8), sy(P[1])-8, lab, 16, INK, True, anc))
    parts.append(txt(425, 40, 'Xanh: đẳng tích rồi đẳng áp', 12, BLUE, False, 'end'))
    parts.append(txt(425, 58, 'Đỏ: đẳng áp rồi đẳng tích', 12, RED, False, 'end'))
    return svg(440, 290, parts, 'Hai đường biến đổi khác nhau nối trạng thái 1 và 2')

def fig_maxwell():
    import math
    L, R, T, B = 70, 430, 30, 240
    sx = lambda v: L + v/900*(R-L)
    sigma = 300.0
    f = lambda v: v*v*math.exp(-v*v/(2*sigma*sigma))
    fmax = max(f(v) for v in range(1, 900))
    sy = lambda y: B - y/fmax*(B-T-20)
    parts = [f'<line x1="{L}" y1="{B}" x2="{R+6}" y2="{B}" stroke="{MUTED}" stroke-width="1.4"/>',
             f'<line x1="{L}" y1="{B+4}" x2="{L}" y2="{T-6}" stroke="{MUTED}" stroke-width="1.4"/>']
    pts = ' '.join(f'{sx(v):.1f},{sy(f(v)):.1f}' for v in range(0, 901, 5))
    parts.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
    vtb = sigma*math.sqrt(8/math.pi); vrms = sigma*math.sqrt(3)
    for v, lab, col, dy in [(vtb, 'v̄ (tốc độ trung bình)', RED, 14), (vrms, 'v_căn quân phương', GREEN, 30)]:
        parts.append(f'<line x1="{sx(v):.1f}" y1="{sy(f(v)):.1f}" x2="{sx(v):.1f}" y2="{B}" stroke="{col}" stroke-dasharray="5 4" stroke-width="1.8"/>')
        parts.append(txt(sx(v)-6 if col==RED else sx(v)+6, B-40 if col==RED else T+12, lab, 12, col, True, 'end' if col==RED else 'start'))
    parts.append(txt(R, B+18, 'tốc độ v', 13, MUTED, False, 'end'))
    parts.append(txt(L+6, T+4, 'số phân tử', 12, MUTED, False, 'start'))
    return svg(480, 280, parts, 'Phân bố tốc độ phân tử: v căn quân phương > v̄')

def fig_ba_dang_quá_trinh():
    # ba đồ thị: đẳng nhiệt (p–V), đẳng áp (V–T), đẳng tích (p–T)
    parts = []
    def frame(x0, title):
        L, R, T, B = x0+30, x0+190, 50, 200
        parts.append(txt(x0+110, 30, title, 14, INK, True))
        parts.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTED}" stroke-width="1.3"/>')
        parts.append(f'<line x1="{L}" y1="{B}" x2="{L}" y2="{T}" stroke="{MUTED}" stroke-width="1.3"/>')
        return L, R, T, B
    # đẳng nhiệt: p = k/V
    L, R, T, B = frame(0, 'Đẳng nhiệt (T không đổi)')
    pts = []
    for i in range(1, 60):
        v = 0.4 + i*0.07
        pp = 4.0 / v
        if pp < 9.5: pts.append(f'{L+ v/5*(R-L-10):.1f},{B - pp/9.5*(B-T):.1f}')
    parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
    parts.append(txt(R-4, B+18, 'V', 13, MUTED, False, 'end')); parts.append(txt(L-6, T+6, 'p', 13, MUTED, False, 'end'))
    parts.append(txt(L+40, B-30, 'pV = hằng số', 12, BLUE, True, 'start'))
    # đẳng áp: V tỉ lệ thuận với T
    L, R, T, B = frame(200, 'Đẳng áp (p không đổi)')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R-10}" y2="{T+10}" stroke="{RED}" stroke-width="2.4"/>')
    parts.append(txt(R-4, B+18, 'T', 13, MUTED, False, 'end')); parts.append(txt(L-6, T+6, 'V', 13, MUTED, False, 'end'))
    parts.append(txt(R-40, B-18, 'V/T = hằng số', 12, RED, True, 'end'))
    # đẳng tích: p tỉ lệ thuận với T
    L, R, T, B = frame(400, 'Đẳng tích (V không đổi)')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R-10}" y2="{T+10}" stroke="{GREEN}" stroke-width="2.4"/>')
    parts.append(txt(R-4, B+18, 'T', 13, MUTED, False, 'end')); parts.append(txt(L-6, T+6, 'p', 13, MUTED, False, 'end'))
    parts.append(txt(R-40, B-18, 'p/T = hằng số', 12, GREEN, True, 'end'))
    return svg(600, 260, parts, 'Tóm tắt đồ thị của ba đẳng quá trình khí lí tưởng')

def fig_suc_tu_nam_cham():
    parts = []
    parts.append(f'<rect x="150" y="120" width="70" height="40" fill="#c0392b" rx="4"/>')
    parts.append(f'<rect x="220" y="120" width="70" height="40" fill="#4e79a7" rx="4"/>')
    parts.append(txt(185, 146, 'N', 16, '#ffffff', True))
    parts.append(txt(255, 146, 'S', 16, '#ffffff', True))
    for d in ['M 150 140 C 90 0, 350 0, 290 140', 'M 150 140 C 90 280, 350 280, 290 140',
              'M 150 140 C 120 60, 320 60, 290 140', 'M 150 140 C 120 220, 320 220, 290 140']:
        parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(arrow_line(200, 36, 240, 36, RED, 1.8))
    parts.append(arrow_line(200, 244, 240, 244, BLUE, 1.8))
    return svg(440, 280, parts, 'Đường sức từ ra từ cực N, vào cực S (minh họa)')

def fig_day_dan_thang():
    parts = []
    cx, cy = 220, 150
    parts.append(f'<line x1="{cx}" y1="20" x2="{cx}" y2="290" stroke="{INK}" stroke-width="3"/>')
    parts.append(arrow_line(cx, 60, cx, 36, INK, 2.2))
    parts.append(txt(cx+12, 46, 'I', 16, INK, True, 'start'))
    for r in (45, 85, 125):
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.35:.1f}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="0"/>')
    # mũi tên chỉ chiều đường sức (ngược chiều kim đồng hồ khi nhìn từ trên, dòng hướng lên)
    for r in (45, 85, 125):
        parts.append(arrow_line(cx-r+1, cy, cx-r+1, cy-r*0.35-0.1, BLUE, 1.6))
    parts.append(txt(cx+130, cy-6, 'B', 15, BLUE, True, 'start'))
    return svg(440, 310, parts, 'Dòng điện đi lên: đường sức từ là vòng tròn đồng tâm (nắm tay phải)')

def fig_ban_tay_trai():
    parts = []
    # dây dẫn nằm ngang, dòng I sang phải; B hướng vào trang (ký hiệu ⊗); lực F hướng lên
    parts.append(f'<line x1="90" y1="170" x2="370" y2="170" stroke="{INK}" stroke-width="4"/>')
    parts.append(arrow_line(120, 170, 200, 170, INK, 2.4))
    parts.append(txt(150, 156, 'I', 16, INK, True))
    parts.append(arrow_line(230, 170, 230, 90, RED, 2.6))
    parts.append(txt(246, 96, 'F', 16, RED, True, 'start'))
    for x in range(120, 361, 60):
        parts.append(f'<circle cx="{x}" cy="{250}" r="11" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
        parts.append(f'<line x1="{x-6}" y1="244" x2="{x+6}" y2="256" stroke="{BLUE}" stroke-width="1.6"/>')
        parts.append(f'<line x1="{x+6}" y1="244" x2="{x-6}" y2="256" stroke="{BLUE}" stroke-width="1.6"/>')
    parts.append(txt(40, 254, 'B', 16, BLUE, True, 'start'))
    parts.append(txt(40, 270, '(hướng vào trang)', 12, MUTED, False, 'start'))
    parts.append(txt(30, 40, 'Quy tắc bàn tay trái: B vào lòng bàn tay, ngón cái chỉ F,', 13, MUTED, False, 'start'))
    parts.append(txt(30, 58, 'bốn ngón tay chỉ chiều I.', 13, MUTED, False, 'start'))
    return svg(440, 300, parts, 'Lực từ tác dụng lên dây dẫn: F vuông góc với dây và với B')

def fig_tu_thong():
    import math
    parts = []
    cx, cy = 230, 165
    a = math.radians(60)
    # đường sức từ B (song song, thẳng đứng)
    for x in (90, 150, 370):
        parts.append(arrow_line(x, 260, x, 60, BLUE, 1.6))
    parts.append(txt(90, 52, 'B', 16, BLUE, True))
    # mặt phẳng S (đoạn thẳng nghiêng)
    dx, dy = 85*math.cos(a), 85*math.sin(a)
    parts.append(f'<line x1="{cx-dx:.1f}" y1="{cy+dy:.1f}" x2="{cx+dx:.1f}" y2="{cy-dy:.1f}" stroke="{INK}" stroke-width="4"/>')
    parts.append(txt(cx+dx+6, cy-dy+4, 'S', 16, INK, True, 'start'))
    # pháp tuyến n
    nx, ny = 95*math.sin(a), 95*math.cos(a)
    parts.append(arrow_line(cx, cy, cx+nx, cy-ny, RED, 2.2))
    parts.append(txt(cx+nx+8, cy-ny, 'n', 16, RED, True, 'start'))
    # cung góc α giữa n và B (chiều lên)
    r = 42
    pts = [(cx + r*math.sin(math.radians(t)), cy - r*math.cos(math.radians(t))) for t in [i*60/20 for i in range(21)]]
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    parts.append(f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    parts.append(txt(cx+r*math.sin(math.radians(30))+22, cy-r*math.cos(math.radians(30))-4, 'α', 17, GREEN, True, 'start'))
    parts.append(txt(230, 285, '', 12, MUTED))
    return svg(440, 300, parts, 'Từ thông Φ = B·S·cosα, với α là góc giữa n và B')

def fig_cam_ung():
    parts = []
    cy = 150
    # trục cuộn dây
    parts.append(f'<line x1="70" y1="{cy}" x2="390" y2="{cy}" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    # nam châm: S bên trái, N bên phải (quay về phía cuộn dây)
    parts.append(f'<rect x="80" y="{cy-22}" width="85" height="44" fill="{BLUE}" rx="3"/>')
    parts.append(f'<rect x="165" y="{cy-22}" width="85" height="44" fill="{RED}" rx="3"/>')
    parts.append(txt(122, cy+6, 'S', 18, '#ffffff', True))
    parts.append(txt(207, cy+6, 'N', 18, '#ffffff', True))
    parts.append(txt(125, cy+42, 'Nam châm', 13, MUTED))
    # mũi tên chuyển động
    parts.append(arrow_line(95, cy-44, 175, cy-44, INK, 2.2))
    parts.append(txt(135, cy-52, 'v', 16, INK, True))
    # cuộn dây: các vòng dây
    for x in (300, 315, 330, 345):
        parts.append(f'<ellipse cx="{x}" cy="{cy}" rx="9" ry="52" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(306, cy+74, 'Cuộn dây', 13, MUTED))
    # dây nối tới điện kế G
    parts.append(f'<path d="M 345 {cy-52} L 345 40 L 420 40 L 420 {cy-18}" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<path d="M 345 {cy+52} L 345 250 L 420 250 L 420 {cy+18}" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<circle cx="420" cy="{cy}" r="18" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(420, cy+6, 'G', 16, INK, True))
    return svg(440, 280, parts, 'Nam châm đưa lại gần cuộn dây kín; G là điện kế')

def fig_dao_dong_dien():
    import math
    parts = []
    x0, y0, amp = 60, 160, 85
    parts.append(arrow_line(x0, 270, x0, 40, INK, 1.6))
    parts.append(arrow_line(x0-10, y0, 410, y0, INK, 1.6))
    parts.append(txt(412, y0+4, 't', 14, INK, False, 'start'))
    parts.append(txt(x0+8, 42, 'e', 14, INK, False, 'start'))
    pts = []
    for i in range(0, 121):
        u = i/120*2  # hai chu kì, đơn vị T
        x = x0 + u*150
        y = y0 - amp*math.cos(2*math.pi*u)
        pts.append((x, y))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    parts.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
    parts.append(f'<line x1="{x0}" y1="{y0-amp}" x2="{x0+150}" y2="{y0-amp}" stroke="{GREY}" stroke-dasharray="5 4"/>')
    parts.append(txt(x0-6, y0-amp+4, 'E₀', 15, RED, True, 'end'))
    parts.append(f'<line x1="{x0}" y1="{y0+amp}" x2="{x0+150}" y2="{y0+amp}" stroke="{GREY}" stroke-dasharray="5 4"/>')
    parts.append(txt(x0-6, y0+amp+4, '-E₀', 13, MUTED, False, 'end'))
    # khoảng T giữa hai đỉnh liên tiếp
    parts.append(arrow_line(x0, 262, x0+150, 262, GREEN, 1.6))
    parts.append(arrow_line(x0+150, 262, x0, 262, GREEN, 1.6))
    parts.append(txt(x0+75, 282, 'T', 15, GREEN, True))
    return svg(440, 300, parts, 'e = E₀cos(ωt): suất điện động biến thiên điều hoà theo thời gian')

def fig_may_phat_xc():
    parts = []
    # cực nam châm
    parts.append(f'<rect x="50" y="90" width="70" height="120" fill="{RED}" rx="4"/>')
    parts.append(txt(85, 158, 'N', 18, '#ffffff', True))
    parts.append(f'<rect x="320" y="90" width="70" height="120" fill="{BLUE}" rx="4"/>')
    parts.append(txt(355, 158, 'S', 18, '#ffffff', True))
    parts.append(arrow_line(125, 150, 315, 150, GREY, 1.6, True))
    parts.append(txt(150, 140, 'B', 16, INK, True))
    # khung dây quay quanh trục thẳng đứng
    parts.append(f'<path d="M 180 105 L 260 105 L 260 195 L 180 195 Z" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    parts.append(f'<line x1="220" y1="60" x2="220" y2="240" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    parts.append(arrow_line(248, 62, 194, 62, GREEN, 2.2))
    parts.append(txt(220, 52, 'ω', 16, GREEN, True))
    return svg(440, 270, parts, 'Khung dây quay đều trong từ trường đều sinh ra suất điện động xoay chiều')

def fig_may_bien_ap():
    parts = []
    # lõi thép kín
    parts.append(f'<rect x="130" y="90" width="180" height="120" fill="none" stroke="{GREY}" stroke-width="14"/>')
    # cuộn sơ cấp (trái) và thứ cấp (phải)
    for y in range(110, 196, 12):
        parts.append(f'<ellipse cx="130" cy="{y}" rx="20" ry="5" fill="none" stroke="{BLUE}" stroke-width="2"/>')
        parts.append(f'<ellipse cx="310" cy="{y}" rx="20" ry="5" fill="none" stroke="{RED}" stroke-width="2"/>')
    parts.append(txt(130, 70, 'N₁', 16, BLUE, True))
    parts.append(txt(310, 70, 'N₂', 16, RED, True))
    # nguồn xoay chiều
    parts.append(f'<circle cx="50" cy="150" r="18" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(50, 156, '~', 18, INK, True))
    parts.append(f'<path d="M 50 132 L 50 108 L 110 108 M 50 168 L 50 192 L 110 192" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(50, 210, 'nguồn', 13, MUTED))
    # tải tiêu thụ
    parts.append(f'<path d="M 330 108 L 390 108 L 390 130 M 330 192 L 390 192 L 390 170" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<rect x="380" y="130" width="20" height="40" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(410, 156, 'R', 16, INK, True, 'start'))
    parts.append(txt(410, 210, 'tải', 13, MUTED, False, 'start'))
    return svg(440, 260, parts, 'Máy biến áp: hai cuộn dây quấn trên lõi thép kín')

def fig_song_dien_tu():
    import math
    parts = []
    x0, x1, y0 = 60, 400, 150
    parts.append(arrow_line(x0-10, y0, 420, y0, GREY, 1.4, True))
    parts.append(txt(425, y0+4, 'c', 15, INK, True, 'start'))
    pe, pb = [], []
    for i in range(0, 241):
        X = x0 + i*(x1-x0)/240
        th = 2*math.pi*(X-x0)/170
        pe.append((X, y0 - 70*math.sin(th)))
        pb.append((X - 0.55*62*math.sin(th), y0 + 0.45*62*math.sin(th)))
    de = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pe)
    db = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pb)
    parts.append(f'<path d="{db}" fill="none" stroke="{RED}" stroke-width="2.4"/>')
    parts.append(f'<path d="{de}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
    parts.append(txt(x0+20, y0-78, 'E', 17, BLUE, True))
    parts.append(txt(x0+112, y0+58, 'B', 17, RED, True, 'start'))
    return svg(440, 280, parts, 'E và B đồng pha, vuông góc nhau và với phương truyền')

def fig_rutherford():
    parts = []
    parts.append(f'<rect x="200" y="40" width="12" height="225" fill="#f3d98b" stroke="{GREY}"/>')
    for y in (70, 110, 150, 190, 230):
        parts.append(f'<circle cx="206" cy="{y}" r="3" fill="{RED}"/>')
    parts.append(arrow_line(40, 60, 195, 60, BLUE, 2))
    parts.append(arrow_line(212, 60, 420, 60, BLUE, 2))
    parts.append(arrow_line(40, 105, 195, 105, BLUE, 2))
    parts.append(f'<path d="M 212 105 Q 230 104 300 80 T 420 45" fill="none" stroke="{BLUE}" stroke-width="2" marker-end="url(#ar)"/>')
    parts.append(arrow_line(40, 150, 195, 150, BLUE, 2))
    parts.append(arrow_line(212, 150, 420, 150, BLUE, 2))
    parts.append(arrow_line(40, 200, 195, 200, BLUE, 2))
    parts.append(f'<path d="M 212 200 Q 120 150 40 185" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    parts.append(arrow_line(62, 176, 40, 185, BLUE, 2))
    parts.append(txt(108, 40, 'hạt α', 14, BLUE, True))
    parts.append(txt(330, 210, 'hạt nhân nhỏ, mang điện dương', 13, RED))
    return svg(440, 290, parts, 'Tán xạ hạt α trên lá vàng mỏng')

def fig_phan_hach():
    parts = []
    parts.append(f'<circle cx="115" cy="140" r="42" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(115, 146, '²³⁵U', 16, INK, True))
    parts.append(f'<circle cx="30" cy="140" r="11" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
    parts.append(txt(30, 145, 'n', 14, INK, True))
    parts.append(arrow_line(44, 140, 70, 140, INK, 2))
    parts.append(arrow_line(152, 122, 240, 92, INK, 2))
    parts.append(arrow_line(152, 158, 240, 192, INK, 2))
    parts.append(f'<circle cx="275" cy="82" r="30" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(275, 88, 'X₁', 16, INK, True))
    parts.append(f'<circle cx="275" cy="200" r="26" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(275, 206, 'X₂', 16, INK, True))
    for (x, y) in ((385, 60), (395, 140), (385, 225)):
        parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
        parts.append(txt(x, y+5, 'n', 13, INK, True))
    parts.append(arrow_line(305, 78, 372, 62, GREY, 1.4))
    parts.append(arrow_line(301, 200, 372, 226, GREY, 1.4))
    parts.append(arrow_line(305, 130, 382, 138, GREY, 1.4))
    return svg(440, 280, parts, 'Phân hạch: hạt nhân nặng vỡ thành hai mảnh nhẹ hơn')

def fig_phan_ra_ham_mu():
    parts = []
    x0, y0, H, Tpx = 60, 250, 190, 100
    parts.append(arrow_line(x0, y0, 420, y0, INK, 1.6))
    parts.append(arrow_line(x0, y0, x0, 30, INK, 1.6))
    parts.append(txt(425, y0+4, 't', 14, INK, False, 'start'))
    parts.append(txt(x0-8, 36, 'N', 14, INK, False, 'end'))
    pts = []
    for i in range(0, 351):
        u = i/100
        pts.append((x0 + u*Tpx, y0 - H*(2**(-u))))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    parts.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
    parts.append(f'<line x1="{x0}" y1="{y0-H}" x2="{x0+Tpx*3.5:.0f}" y2="{y0-H}" stroke="{GREY}" stroke-dasharray="5 4"/>')
    parts.append(txt(x0-8, y0-H+4, 'N₀', 14, RED, True, 'end'))
    parts.append(f'<line x1="{x0}" y1="{y0-H/2:.1f}" x2="{x0+Tpx:.0f}" y2="{y0-H/2:.1f}" stroke="{GREY}" stroke-dasharray="5 4"/>')
    parts.append(f'<line x1="{x0+Tpx:.0f}" y1="{y0-H/2:.1f}" x2="{x0+Tpx:.0f}" y2="{y0}" stroke="{GREY}" stroke-dasharray="3 4"/>')
    parts.append(txt(x0-8, y0-H/2+4, 'N₀/2', 13, RED, False, 'end'))
    for k in (1, 2, 3):
        parts.append(f'<line x1="{x0+k*Tpx}" y1="{y0}" x2="{x0+k*Tpx}" y2="{y0+6}" stroke="{INK}" stroke-width="1.4"/>')
        parts.append(txt(x0+k*Tpx, y0+20, f'{k}T' if k > 1 else 'T', 14, INK, False))
    return svg(440, 290, parts, 'Số hạt nhân chưa phân rã giảm theo hàm số mũ theo thời gian')

def fig_lo_phan_ung():
    parts = []
    parts.append(f'<rect x="60" y="60" width="150" height="180" fill="{FILL}" stroke="{INK}" stroke-width="2" rx="6"/>')
    for x in (85, 110, 135, 160, 185):
        parts.append(f'<line x1="{x}" y1="90" x2="{x}" y2="220" stroke="{GREEN}" stroke-width="4"/>')
    parts.append(f'<rect x="{110-5}" y="60" width="10" height="110" fill="{GREY}"/>')
    parts.append(txt(135, 52, 'Lò phản ứng', 14, INK, True))
    parts.append(f'<path d="M 210 120 L 262 120" stroke="{INK}" stroke-width="5" fill="none"/>')
    parts.append(txt(236, 102, 'hơi nước', 12, MUTED))
    parts.append(f'<circle cx="300" cy="120" r="30" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(300, 124, 'tua bin', 12, INK, True))
    parts.append(f'<line x1="330" y1="120" x2="350" y2="120" stroke="{INK}" stroke-width="4"/>')
    parts.append(f'<rect x="350" y="92" width="62" height="56" fill="{FILL}" stroke="{INK}" stroke-width="2" rx="4"/>')
    parts.append(txt(381, 118, 'máy phát', 12, INK, True))
    parts.append(txt(381, 134, 'điện', 12, INK, True))
    return svg(440, 260, parts, 'Lò phản ứng, tua bin và máy phát điện')

FIGS = {
    'c-ly12-b1-ba-the.svg': fig_ba_the,
    'c-ly12-b1-chuyen-the.svg': fig_chuyen_the,
    'c-ly12-b2-quy-uoc-dau.svg': fig_quy_uoc_dau,
    'c-ly12-b3-thang-nhiet-do.svg': fig_thang_nhiet_do,
    'c-ly12-b4-nhiet-dung-rieng.svg': fig_nhiet_dung_rieng,
    'c-ly12-b5-do-thi-nong-chay.svg': fig_do_thi_nong_chay,
    'c-ly12-b6-do-thi-hoa-hoi.svg': fig_do_thi_hoa_hoi,
    'c-ly12-b7-can-bang-nhiet.svg': fig_can_bang_nhiet,
    'c-ly12-b8-ap-suat-khi.svg': fig_khi_ap_suat,
    'c-ly12-b9-boyle.svg': fig_boyle,
    'c-ly12-b10-charles.svg': fig_charles,
    'c-ly12-b11-duong-bien-doi.svg': fig_duong_bien_doi,
    'c-ly12-b12-maxwell.svg': fig_maxwell,
    'c-ly12-b13-tom-tat-dang-qua-trinh.svg': fig_ba_dang_quá_trinh,
    'c-ly12-b14-suc-tu-nam-cham.svg': fig_suc_tu_nam_cham,
    'c-ly12-b14-day-dan-thang.svg': fig_day_dan_thang,
    'c-ly12-b15-ban-tay-trai.svg': fig_ban_tay_trai,
    'c-ly12-b16-tu-thong.svg': fig_tu_thong,
    'c-ly12-b16-cam-ung.svg': fig_cam_ung,
    'c-ly12-b17-dao-dong-dien.svg': fig_dao_dong_dien,
    'c-ly12-b17-may-phat.svg': fig_may_phat_xc,
    'c-ly12-b18-may-bien-ap.svg': fig_may_bien_ap,
    'c-ly12-b19-song-dien-tu.svg': fig_song_dien_tu,
    'c-ly12-b21-rutherford.svg': fig_rutherford,
    'c-ly12-b22-phan-hach.svg': fig_phan_hach,
    'c-ly12-b23-phan-ra.svg': fig_phan_ra_ham_mu,
    'c-ly12-b24-lo-phan-ung.svg': fig_lo_phan_ung,
}

if __name__ == '__main__':
    for name, fn in FIGS.items():
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
            fh.write(fn())
        print('wrote', name)
