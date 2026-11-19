# Thư viện vẽ SVG dùng chung cho các script sinh hình minh họa (sơ đồ mô phỏng, không phải ảnh chụp).
import json
import math
import os
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INK = '#1d2733'
GREY = '#9aa5b1'
BLUE = '#4e79a7'
ORANGE = '#f28e2b'
RED = '#e15759'
GREEN = '#59a14f'
LGREEN = '#dfe9d5'
LBLUE = '#dbe7f3'
LYELLOW = '#fbf0c9'
LGREY = '#eef1f4'
DEFS = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % INK)


def svg(w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Segoe UI, Arial, sans-serif">'
            % (w, h)) + DEFS + body + '</svg>'


def T(x, y, s, size=15, anchor='middle', weight='normal', fill=INK):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%d" font-weight="%s" fill="%s">%s</text>'
            % (x, y, anchor, size, weight, fill, escape(s)))


def TL(x, y, lines, size=14, anchor='middle', weight='normal', fill=INK, lh=None):
    lh = lh or size + 4
    return ''.join(T(x, y + i * lh, s, size, anchor, weight, fill) for i, s in enumerate(lines))


def L(x1, y1, x2, y2, stroke=INK, w=2, dash=None, arrow=False):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    m = ' marker-end="url(#ar)"' if arrow else ''
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>'
            % (x1, y1, x2, y2, stroke, w, d, m))


def C(cx, cy, r, fill='none', stroke=INK, w=2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (cx, cy, r, fill, stroke, w, d))


def R(x, y, w, h, fill='none', stroke=INK, sw=2, rx=0):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, rx, fill, stroke, sw))


def POLY(pts, fill='none', stroke=INK, sw=2):
    p = ' '.join('%.1f,%.1f' % q for q in pts)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (p, fill, stroke, sw)


def PL(pts, stroke=INK, w=2, fill='none', dash=None):
    p = ' '.join('%.1f,%.1f' % q for q in pts)
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>' % (p, fill, stroke, w, d)


def PATH(d, fill='none', stroke=INK, w=2):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (d, fill, stroke, w)


def title(w, s):
    return T(w / 2, 24, s, size=17, weight='bold')


def write_figs(subject, figs):
    d = os.path.join(ROOT, 'content', subject, 'figures')
    os.makedirs(d, exist_ok=True)
    for name, fn in figs.items():
        with open(os.path.join(d, name), 'w', encoding='utf8') as f:
            f.write(fn())


def attach(subject, relpath, after, fig, caption):
    """Chèn khối hình vào lý thuyết sau khối số `after` (bỏ qua nếu hình đã có)."""
    p = os.path.join(ROOT, 'content', subject, relpath)
    with open(p, encoding='utf8') as f:
        data = json.load(f)
    key = 'figures/' + fig
    if any(b.get('type') == 'figure' and b.get('figure') == key for b in data['theory']):
        return
    data['theory'].insert(after + 1, {'type': 'figure', 'figure': key, 'caption': caption})
    with open(p, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


# ---- dụng cụ thí nghiệm dùng chung ----
def tube(x, y, w=26, h=110, liquid=None, level=0.55, tilt=0):
    """Ống nghiệm thẳng đứng: (x, y) là tâm miệng ống. Trả về SVG (đáy bo tròn)."""
    r = w / 2
    body = 'M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f' % (
        x - r, y, x - r, y + h - r, x - r, y + h - r, r, r, x + r, y + h - r, x + r, y)
    out = []
    if liquid:
        top = y + h - r - (h - r) * level
        out.append('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f Z" fill="%s"/>' % (
            x - r + 1, top, x - r + 1, y + h - r, r - 1, r - 1, x + r - 1, y + h - r, x + r - 1, top, liquid))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % (body, INK))
    out.append(L(x - r - 3, y, x + r + 3, y, w=2.5))
    return ''.join(out)


def beaker(x, y, w=90, h=100, liquid=None, level=0.6):
    """Cốc thuỷ tinh: (x, y) là góc trên trái."""
    out = []
    if liquid:
        top = y + h * (1 - level)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x + 1.5, top, w - 3, y + h - top - 1.5, liquid))
    out.append(PL([(x - 4, y - 4), (x, y), (x, y + h), (x + w, y + h), (x + w, y), (x + w + 4, y - 4)], w=2.5))
    return ''.join(out)


def flame(x, y, s=1.0, col='#f28e2b'):
    d = ('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z'
         % (x, y - 34 * s, x + 6 * s, y - 20 * s, x + 20 * s, y - 14 * s, x + 14 * s, y,
            x + 10 * s, y + 8 * s, x - 10 * s, y + 8 * s, x - 14 * s, y,
            x - 18 * s, y - 10 * s, x - 6 * s, y - 20 * s, x, y - 34 * s))
    return PATH(d, fill=col, stroke='#c9701a', w=1.5)


def lamp(x, y):
    """Đèn cồn: (x, y) là tâm đáy; cao khoảng 60; ngọn lửa phía trên."""
    return (R(x - 24, y - 36, 48, 36, fill='#e0e6ec', rx=6) + R(x - 7, y - 50, 14, 14, fill='#e0e6ec')
            + flame(x, y - 54, 0.6))


def card(x, y, w, h, head, lines, fill=LGREY, hsize=15, size=13, lh=18):
    return (R(x, y, w, h, fill=fill, rx=8) + T(x + w / 2, y + 26, head, size=hsize, weight='bold')
            + TL(x + w / 2, y + 52, lines, size=size, lh=lh))


def struct(atoms, bonds, ox=0, oy=0, fs=17):
    """Công thức cấu tạo: atoms = {tên: (x, y, nhãn)}, bonds = [(a, b, bậc)]. Toạ độ cộng thêm (ox, oy)."""
    out = []
    for a, b, order in bonds:
        x1, y1 = atoms[a][0] + ox, atoms[a][1] + oy
        x2, y2 = atoms[b][0] + ox, atoms[b][1] + oy
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        offs = {1: [0], 2: [-3.2, 3.2], 3: [-5, 0, 5]}[order]
        for o in offs:
            out.append(L(x1 + nx * o, y1 + ny * o, x2 + nx * o, y2 + ny * o, w=2))
    for k, (x, y, lab) in atoms.items():
        w = 12 + 9 * len(lab.replace('₂', '2').replace('₃', '3').replace('₄', '4'))
        out.append(R(x + ox - w / 2, y + oy - 12, w, 24, fill='#ffffff', stroke='none', sw=0))
        out.append(T(x + ox, y + oy + 6, lab, size=fs, weight='bold'))
    return ''.join(out)


def mol_center(atoms):
    xs = [v[0] for v in atoms.values()]
    ys = [v[1] for v in atoms.values()]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2


# ---- hình học ----
def unit(x1, y1, x2, y2):
    d = math.hypot(x2 - x1, y2 - y1) or 1
    return (x2 - x1) / d, (y2 - y1) / d


def tick(x1, y1, x2, y2, n=1, size=7, color=INK):
    """Dấu gạch đánh dấu hai đoạn thẳng bằng nhau (n gạch) ở trung điểm đoạn (x1,y1)-(x2,y2)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ux, uy = unit(x1, y1, x2, y2)
    nx, ny = -uy, ux
    out = []
    for k in range(n):
        off = (k - (n - 1) / 2) * 5
        cx, cy = mx + ux * off, my + uy * off
        out.append(L(cx - nx * size, cy - ny * size, cx + nx * size, cy + ny * size, w=2, stroke=color))
    return ''.join(out)


def right_angle(vx, vy, ax, ay, bx, by, s=11):
    """Kí hiệu góc vuông tại đỉnh V với hai cạnh hướng về A và B."""
    u1 = unit(vx, vy, ax, ay)
    u2 = unit(vx, vy, bx, by)
    p1 = (vx + u1[0] * s, vy + u1[1] * s)
    p2 = (vx + u1[0] * s + u2[0] * s, vy + u1[1] * s + u2[1] * s)
    p3 = (vx + u2[0] * s, vy + u2[1] * s)
    return PL([p1, p2, p3], w=1.5)


def angle_arc(vx, vy, ax, ay, bx, by, r=22, color=INK, w=1.5):
    """Cung góc tại V từ tia VA đến tia VB (cung nhỏ)."""
    a1 = math.atan2(ay - vy, ax - vx)
    a2 = math.atan2(by - vy, bx - vx)
    d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    sweep = 1 if d > 0 else 0
    x1, y1 = vx + r * math.cos(a1), vy + r * math.sin(a1)
    x2, y2 = vx + r * math.cos(a1 + d), vy + r * math.sin(a1 + d)
    return PATH('M%.1f,%.1f A%d,%d 0 0 %d %.1f,%.1f' % (x1, y1, r, r, sweep, x2, y2), stroke=color, w=w)


def regpoly(cx, cy, r, n, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 360 * k / n)), cy + r * math.sin(math.radians(rot + 360 * k / n)))
            for k in range(n)]


def dot(x, y, r=3.5, fill=INK):
    return C(x, y, r, fill=fill, stroke=fill, w=1)
