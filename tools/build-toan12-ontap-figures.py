# Sinh hình đồ thị cho đề cương cuối năm Toán 12, ghi ra content/toan12/figures/.
# Chạy: python3 tools/build-toan12-ontap-figures.py
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'toan12', 'figures')
INK, CURVE, MUTED, DASH = '#1d2733', '#4e79a7', '#5b6775', '#9aa5b1'

def build_do_thi_bac_ba():
    # Đồ thị y = x³ − 3x² + 3 trên [−1; 3.2]; khung 380×330, không ghi công thức lên hình
    x0, x1, y0, y1 = -1.0, 3.2, -2.0, 4.5
    W, H, L, T, R, B = 380, 330, 50, 20, 360, 290
    sx = lambda x: L + (x - x0) / (x1 - x0) * (R - L)
    sy = lambda y: B - (y - y0) / (y1 - y0) * (B - T)
    f = lambda x: x**3 - 3*x**2 + 3
    parts = []
    parts.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{R+8}" y2="{sy(0):.1f}" stroke="{MUTED}" stroke-width="1.4"/>')
    parts.append(f'<line x1="{sx(0):.1f}" y1="{T-6}" x2="{sx(0):.1f}" y2="{B+6}" stroke="{MUTED}" stroke-width="1.4"/>')
    parts.append(f'<text x="{R+10}" y="{sy(0)+5:.1f}" font-size="14" fill="{MUTED}">x</text>')
    parts.append(f'<text x="{sx(0)+6:.1f}" y="{T-2}" font-size="14" fill="{MUTED}">y</text>')
    pts = []
    n = 200
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append(f'{sx(x):.1f},{sy(f(x)):.1f}')
    parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CURVE}" stroke-width="2.4"/>')
    for x in (0, 1, 2, 3):
        parts.append(f'<circle cx="{sx(x):.1f}" cy="{sy(0):.1f}" r="2.5" fill="{MUTED}"/>')
    parts.append(f'<text x="{sx(0)-16:.1f}" y="{sy(0)+18:.1f}" font-size="13" fill="{MUTED}">O</text>')
    parts.append(f'<text x="{sx(2)-4:.1f}" y="{sy(0)+18:.1f}" font-size="13" fill="{MUTED}">2</text>')
    parts.append(f'<text x="{sx(1)-4:.1f}" y="{sy(0)+18:.1f}" font-size="13" fill="{MUTED}">1</text>')
    parts.append(f'<text x="{sx(3)-4:.1f}" y="{sy(0)+18:.1f}" font-size="13" fill="{MUTED}">3</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">'
            + ''.join(parts)
            + f'<text x="190" y="322" font-size="13" text-anchor="middle" fill="{MUTED}">Đồ thị hàm số bậc ba (câu 4)</text></svg>\n')

if __name__ == '__main__':
    path = os.path.join(OUT, 'ocn-q04-do-thi-bac-ba.svg')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(build_do_thi_bac_ba())
    print('wrote', path)
