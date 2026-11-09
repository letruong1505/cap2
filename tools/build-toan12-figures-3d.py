# Sinh hình minh họa không gian (phép chiếu xiên) cho Toán 12, ghi ra content/toan12/figures/.
# Chạy: python3 tools/build-toan12-figures-3d.py
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'toan12', 'figures')
INK, DASH, CURVE, MUTED = '#1d2733', '#9aa5b1', '#4e79a7', '#5b6775'
W, H = 380, 330
# Chiếu: (x,y,z) -> màn hình. Ox sang phải, Oy chéo xuống-trái, Oz thẳng đứng.
OX, OY, OZ = (66.0, 0.0), (-36.0, 26.0), (0.0, -62.0)
ORIG = (120.0, 232.0)

def P(x, y, z):
    return (ORIG[0] + x*OX[0] + y*OY[0] + z*OZ[0], ORIG[1] + x*OX[1] + y*OY[1] + z*OZ[1])

def seg(p, q, dashed=False, color=INK, w=1.6):
    a, b = P(*p), P(*q)
    d = ' stroke-dasharray="5 4"' if dashed else ''
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{w}"{d}/>'

def arrow(p, q, color=INK):
    a, b = P(*p), P(*q)
    import math
    ang = math.atan2(b[1]-a[1], b[0]-a[0]); L = 9
    l = (b[0]-L*math.cos(ang-0.4), b[1]-L*math.sin(ang-0.4))
    r = (b[0]-L*math.cos(ang+0.4), b[1]-L*math.sin(ang+0.4))
    return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="1.8"/>'
            f'<polygon points="{b[0]:.1f},{b[1]:.1f} {l[0]:.1f},{l[1]:.1f} {r[0]:.1f},{r[1]:.1f}" fill="{color}"/>')

def label(p, text, dx=0, dy=0, size=15, bold=True, color=INK):
    x, y = P(*p)
    weight = ' font-weight="bold"' if bold else ''
    return f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="{size}"{weight} fill="{color}">{text}</text>'

def build_oxyz():
    M = (2.0, 1.5, 2.0)            # điểm minh họa, không ghi tọa độ lên hình
    x, y, z = M
    parts = []
    # trục và mũi tên
    parts.append(arrow((0,0,0), (3.2,0,0)))
    parts.append(arrow((0,0,0), (0,2.7,0)))
    parts.append(arrow((0,0,0), (0,0,2.9)))
    # hình chiếu của M lên các trục / mặt phẳng: hộp nét đứt
    parts.append(seg((x,y,z),(x,y,0),True,DASH))
    parts.append(seg((x,y,z),(x,0,z),True,DASH))
    parts.append(seg((x,y,z),(0,y,z),True,DASH))
    parts.append(seg((x,0,0),(x,y,0),True,DASH))
    parts.append(seg((0,y,0),(x,y,0),True,DASH))
    parts.append(seg((0,0,z),(x,0,z),True,DASH))
    parts.append(seg((0,y,0),(0,y,z),True,DASH))
    parts.append(seg((x,0,0),(x,0,z),True,DASH))
    parts.append(seg((0,0,z),(0,y,z),True,DASH))
    # vectơ OM
    parts.append(arrow((0,0,0), M, CURVE))
    # nhãn trục
    parts.append(label((3.45,0,0), 'x', size=16))
    parts.append(label((0,2.95,0), 'y', size=16))
    parts.append(label((0,0,3.15), 'z', size=16))
    parts.append(label((0,0,0), 'O', dx=-14, dy=14, size=15))
    # đơn vị i, j, k
    parts.append(label((1,0,0), 'i', dx=-2, dy=18, size=14, bold=False, color=MUTED))
    parts.append(label((0,1,0), 'j', dx=-14, dy=6, size=14, bold=False, color=MUTED))
    parts.append(label((0,0,1), 'k', dx=8, dy=-6, size=14, bold=False, color=MUTED))
    parts.append(label(M, 'M', dx=8, dy=-8, size=15))
    parts.append(f'<text x="190" y="322" font-size="13" text-anchor="middle" fill="{MUTED}">Hệ toạ độ Oxyz: OM = xi + yj + zk</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 330" font-family="Segoe UI, Arial, sans-serif">'
            + ''.join(parts) + '</svg>\n')

def _wrap(parts, caption):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 330" font-family="Segoe UI, Arial, sans-serif">'
            + ''.join(parts)
            + f'<text x="190" y="322" font-size="13" text-anchor="middle" fill="{MUTED}">{caption}</text></svg>\n')

def build_duong_thang():
    # Đường thẳng Δ đi qua M0 với vectơ chỉ phương u (không ghi tọa độ lên hình)
    M0 = (1.0, 0.6, 0.8)
    u = (0.9, 0.5, 0.7)
    A = tuple(M0[i] - 0.7*u[i] for i in range(3))
    B = tuple(M0[i] + 1.45*u[i] for i in range(3))
    C = tuple(M0[i] + u[i] for i in range(3))
    parts = []
    parts.append(arrow((0,0,0), (3.2,0,0), DASH))
    parts.append(arrow((0,0,0), (0,2.7,0), DASH))
    parts.append(arrow((0,0,0), (0,0,2.9), DASH))
    parts.append(seg(A, B, False, CURVE, 2.2))
    parts.append(seg(M0, (M0[0],M0[1],0), True, DASH))
    parts.append(arrow(M0, C, INK))
    parts.append(label(B, 'Δ', dx=6, dy=-6, size=16, color=CURVE))
    parts.append(label(M0, 'M₀', dx=-26, dy=-8, size=15))
    parts.append(label(C, 'u', dx=6, dy=4, size=15))
    parts.append(label((0,0,0), 'O', dx=-14, dy=14, size=14, bold=False, color=MUTED))
    return _wrap(parts, 'Δ đi qua M₀, vectơ chỉ phương u')

def build_hai_duong_cheo():
    # Hai đường thẳng chéo nhau: không song song, không cắt nhau (khác mức)
    parts = []
    parts.append(arrow((0,0,0), (3.2,0,0), DASH))
    parts.append(arrow((0,0,0), (0,2.7,0), DASH))
    parts.append(arrow((0,0,0), (0,0,2.9), DASH))
    d1a, d1b = (0.0, 0.8, 1.6), (2.8, 0.8, 1.6)      # Δ₁ song song Ox, ở độ cao z = 1,6
    d2a, d2b = (1.6, 0.0, 0.0), (1.6, 2.2, 0.0)      # Δ₂ song song Oy, nằm trên mặt Oxy
    parts.append(seg(d1a, d1b, False, CURVE, 2.2))
    parts.append(seg(d2a, d2b, False, INK, 2.2))
    parts.append(seg((1.6,0.8,1.6), (1.6,0.8,0.0), True, DASH))
    parts.append(label(d1b, 'Δ₁', dx=6, dy=-6, size=16, color=CURVE))
    parts.append(label(d2b, 'Δ₂', dx=-30, dy=14, size=16))
    parts.append(label((0,0,0), 'O', dx=-14, dy=14, size=14, bold=False, color=MUTED))
    return _wrap(parts, 'Hai đường thẳng chéo nhau: không cùng mặt phẳng')


def build_goc_duong_mat():
    # Góc giữa đường thẳng Δ và mặt phẳng (P) (ở đây là mặt z = 0): góc giữa Δ và hình chiếu của nó
    I = (1.0, 0.7, 0.0)
    u = (0.9, 0.6, 1.3)
    M = tuple(I[i] + u[i] for i in range(3))
    H = (I[0] + u[0], I[1] + u[1], 0.0)
    parts = []
    poly = [(0.0,0.0,0.0), (2.4,0.0,0.0), (2.9,1.8,0.0), (0.5,1.8,0.0)]
    pts = ' '.join(f'{P(*q)[0]:.1f},{P(*q)[1]:.1f}' for q in poly)
    parts.append(f'<polygon points="{pts}" fill="#cfe3f5" stroke="{CURVE}" stroke-width="1.2"/>')
    parts.append(label((2.55,1.2,0), '(P)', dx=8, dy=0, size=15, color=CURVE))
    parts.append(arrow((0,0,0), (3.2,0,0), DASH))
    parts.append(arrow((0,0,0), (0,2.7,0), DASH))
    parts.append(arrow((0,0,0), (0,0,2.9), DASH))
    parts.append(seg(I, M, False, INK, 2.2))
    parts.append(seg(I, H, True, DASH))
    parts.append(seg(M, H, True, DASH))
    # cung góc φ tại I (vẽ bằng đoạn ngắn, không ghi giá trị)
    a = P(*I); b = P(*(I[0]+0.45, I[1]+0.0, 0)); 
    c = P(*(I[0]+0.45*u[0]/ (u[0]**2+u[1]**2+u[2]**2)**0.5, I[1]+0.45*u[1]/(u[0]**2+u[1]**2+u[2]**2)**0.5, 0.45*u[2]/(u[0]**2+u[1]**2+u[2]**2)**0.5))
    parts.append(f'<path d="M {b[0]:.1f} {b[1]:.1f} Q {(a[0]+b[0])/2+4:.1f} {(a[1]+b[1])/2-6:.1f} {c[0]:.1f} {c[1]:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    parts.append(label(I, 'I', dx=-14, dy=16, size=15))
    parts.append(label(M, 'Δ', dx=6, dy=-6, size=16, color=CURVE))
    parts.append(label(H, 'H', dx=6, dy=14, size=15))
    parts.append(label(I, 'φ', dx=20, dy=-14, size=15, bold=False))
    return _wrap(parts, 'Góc φ giữa Δ và mặt phẳng (P) là góc giữa Δ và hình chiếu IH')

def build_mat_cau():
    # Mặt cầu tâm I bán kính R: đường tròn biên, đường xích đạo nét đứt, bán kính IN
    cx, cy, r = 190.0, 165.0, 100.0
    parts = []
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e8f1fa" stroke="{CURVE}" stroke-width="2"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.28:.1f}" fill="none" stroke="{DASH}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+r*0.7:.1f}" y2="{cy-r*0.7:.1f}" stroke="{INK}" stroke-width="1.8"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{INK}"/>')
    parts.append(f'<text x="{cx-12}" y="{cy+20}" font-size="15" font-weight="bold" fill="{INK}">I</text>')
    parts.append(f'<text x="{cx+r*0.35:.1f}" y="{cy-r*0.35-8:.1f}" font-size="15" font-weight="bold" fill="{INK}">R</text>')
    parts.append(f'<circle cx="{cx+r*0.7:.1f}" cy="{cy-r*0.7:.1f}" r="3.5" fill="{CURVE}"/>')
    parts.append(f'<text x="{cx+r*0.7+6:.1f}" y="{cy-r*0.7-4:.1f}" font-size="15" font-weight="bold" fill="{CURVE}">N</text>')
    parts.append(f'<text x="{cx}" y="{cy+r+4}" font-size="0" fill="none"></text>')
    parts.append(f'<text x="{cx+120:.1f}" y="{cy-100:.1f}" font-size="14" fill="{MUTED}">(S)</text>')
    return _wrap(parts, 'Mặt cầu (S): tập các điểm cách I một khoảng R')

def build_mat_phang_chan():
    # Mặt phẳng cắt Ox, Oy, Oz tại A, B, C (phương trình đoạn chắn); không ghi tọa độ lên hình
    A, B, C = (2.6, 0, 0), (0, 2.2, 0), (0, 0, 2.4)
    parts = []
    parts.append(arrow((0,0,0), (3.2,0,0), DASH))
    parts.append(arrow((0,0,0), (0,2.7,0), DASH))
    parts.append(arrow((0,0,0), (0,0,2.9), DASH))
    poly = [A, B, C]
    pts = ' '.join(f'{P(*q)[0]:.1f},{P(*q)[1]:.1f}' for q in poly)
    parts.append(f'<polygon points="{pts}" fill="#cfe3f5" fill-opacity="0.75" stroke="{CURVE}" stroke-width="1.4"/>')
    parts.append(seg((0,0,0), A, True, DASH)); parts.append(seg((0,0,0), B, True, DASH)); parts.append(seg((0,0,0), C, True, DASH))
    parts.append(label(A, 'A', dx=6, dy=16, size=15))
    parts.append(label(B, 'B', dx=-16, dy=18, size=15))
    parts.append(label(C, 'C', dx=10, dy=-4, size=15))
    parts.append(label((0,0,0), 'O', dx=-14, dy=14, size=14, bold=False, color=MUTED))
    return _wrap(parts, 'Mặt phẳng cắt các trục Ox, Oy, Oz tại A, B, C')

if __name__ == '__main__':
    path = os.path.join(OUT, 'c2-7-he-truc-oxyz.svg')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(build_oxyz())
    print('wrote', path)
    for name, fn in [('c2-7-duong-thang-u.svg', build_duong_thang), ('c2-7-hai-duong-cheo.svg', build_hai_duong_cheo), ('c5-16-goc-duong-mat.svg', build_goc_duong_mat), ('c5-17-mat-cau.svg', build_mat_cau), ('c5-14-mat-phang-chan.svg', build_mat_phang_chan)]:
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
            fh.write(fn())
        print('wrote', name)
