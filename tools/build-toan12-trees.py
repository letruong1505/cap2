# Sinh sơ đồ cây xác suất (2 tầng) cho Toán 12, ghi ra content/toan12/figures/.
# Chạy: python3 tools/build-toan12-trees.py
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'toan12', 'figures')
INK, CURVE, MUTED, FILL = '#1d2733', '#4e79a7', '#5b6775', '#e8f1fa'

def node(x, y, text, color=INK):
    return (f'<rect x="{x-38}" y="{y-13}" width="76" height="26" rx="6" fill="{FILL}" stroke="{CURVE}" stroke-width="1.2"/>'
            f'<text x="{x}" y="{y+5}" font-size="13" text-anchor="middle" fill="{color}">{text}</text>')

def edge(x1, y1, x2, y2, label, lx, ly):
    return (f'<line x1="{x1+38}" y1="{y1}" x2="{x2-38}" y2="{y2}" stroke="{INK}" stroke-width="1.3"/>'
            f'<text x="{lx}" y="{ly}" font-size="13" font-weight="bold" fill="{CURVE}">{label}</text>')

def leaf(x, y, text):
    return f'<text x="{x}" y="{y+5}" font-size="13" fill="{INK}">{text}</text>'

def build_cay_nhan():
    # Ví dụ 4: 7 xanh, 5 đen; Sơn lấy trước (không trả lại), Tùng lấy sau
    r = (48, 165); a1 = (150, 90); a2 = (150, 240)
    b11 = (262, 40); b12 = (262, 130); b21 = (262, 210); b22 = (262, 290)
    parts = []
    parts.append(node(*r, 'Bắt đầu'))
    parts.append(edge(*r, *a1, '5/12', 100, 118))
    parts.append(edge(*r, *a2, '7/12', 100, 222))
    parts.append(node(*a1, 'Sơn: đen', CURVE))
    parts.append(node(*a2, 'Sơn: xanh', CURVE))
    parts.append(edge(*a1, *b11, '7/11', 196, 56))
    parts.append(edge(*a1, *b12, '4/11', 196, 118))
    parts.append(edge(*a2, *b21, '6/11', 196, 200))
    parts.append(edge(*a2, *b22, '5/11', 196, 282))
    parts.append(node(*b11, 'Tùng: xanh'))
    parts.append(node(*b12, 'Tùng: đen'))
    parts.append(node(*b21, 'Tùng: xanh'))
    parts.append(node(*b22, 'Tùng: đen'))
    parts.append(leaf(326, 40, 'P = 35/132'))
    parts.append(leaf(326, 130, 'P = 5/33'))
    parts.append(leaf(326, 210, 'P = 7/22'))
    parts.append(leaf(326, 290, 'P = 35/132'))
    parts = [p for p in parts]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 330" font-family="Segoe UI, Arial, sans-serif">'
            + ''.join(parts)
            + f'<text x="215" y="324" font-size="13" text-anchor="middle" fill="{MUTED}">Sơ đồ cây: Sơn lấy trước, Tùng lấy sau (không trả lại)</text></svg>\n')

def build_cay_toan_phan():
    # Ví dụ 2 (Bayes): 80% chọn A00; đỗ với xác suất 0,6 (A00) và 0,7 (không chọn A00)
    r = (48, 165); a1 = (150, 90); a2 = (150, 240)
    b11 = (262, 40); b12 = (262, 130); b21 = (262, 210); b22 = (262, 290)
    parts = []
    parts.append(node(*r, 'Học sinh'))
    parts.append(edge(*r, *a1, '0,8', 100, 118))
    parts.append(edge(*r, *a2, '0,2', 100, 222))
    parts.append(node(*a1, 'Chọn A00', CURVE))
    parts.append(node(*a2, 'Không A00', CURVE))
    parts.append(edge(*a1, *b11, '0,6', 200, 52))
    parts.append(edge(*a1, *b12, '0,4', 200, 120))
    parts.append(edge(*a2, *b21, '0,7', 200, 204))
    parts.append(edge(*a2, *b22, '0,3', 200, 284))
    parts.append(node(*b11, 'Đỗ'))
    parts.append(node(*b12, 'Trượt'))
    parts.append(node(*b21, 'Đỗ'))
    parts.append(node(*b22, 'Trượt'))
    parts.append(leaf(306, 40, 'P = 0,48'))
    parts.append(leaf(306, 130, 'P = 0,32'))
    parts.append(leaf(306, 210, 'P = 0,14'))
    parts.append(leaf(306, 290, 'P = 0,06'))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 330" font-family="Segoe UI, Arial, sans-serif">'
            + ''.join(parts)
            + f'<text x="215" y="324" font-size="13" text-anchor="middle" fill="{MUTED}">P(đỗ) = 0,48 + 0,14 = 0,62; P(A00 | đỗ) = 0,48 / 0,62</text></svg>\n')

if __name__ == '__main__':
    with open(os.path.join(OUT, 'c6-18-cay-nhan.svg'), 'w', encoding='utf-8') as fh:
        fh.write(build_cay_nhan())
    with open(os.path.join(OUT, 'c6-19-cay-toan-phan.svg'), 'w', encoding='utf-8') as fh:
        fh.write(build_cay_toan_phan())
    print('wrote trees')
