"""Áp dụng quy tắc viết hoa sau dấu . : ? ! cho các chuỗi chữ trong mã nguồn giao diện.
Chỉ sửa trong chuỗi ký tự ('…', "…", `…`) có chữ tiếng Việt; bỏ qua mã, <pre>, <code>, phần ${…}."""
import re, sys, glob, os
sys.path.insert(0, os.path.dirname(__file__))
from viethoa_lib import cap_html
import viethoa_lib

VN = re.compile(r'[^\x00-\x7f]')
STR = re.compile(r"'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\"|`(?:[^`\\]|\\.)*`")

def fix_literal(lit):
    q = lit[0]; body = lit[1:-1]
    if not VN.search(body) or len(body) < 6: return lit
    if q == '`':
        parts = re.split(r'(\$\{[^}]*\})', body)
        body = ''.join(p if p.startswith('${') else cap_html(p) for p in parts)
    else:
        body = cap_html(body)
    return q + body + q

def fix_js(src):
    out = []
    for line in src.split('\n'):
        st = line.lstrip()
        if st.startswith(('//', '*', '/*')): out.append(line); continue
        # bỏ phần chú thích cuối dòng nếu có "// " ngoài chuỗi (thô): xử lý chuỗi trước, chú thích giữ nguyên
        out.append(STR.sub(lambda m: fix_literal(m.group(0)), line))
    return '\n'.join(out)

def fix_html(src):
    return cap_html(src)

if __name__ == '__main__':
    root = os.path.join(os.path.dirname(__file__), '..')
    files = [f for pat in ('renderer/*.js', 'parent/*.js', 'mobile/*.js') for f in glob.glob(os.path.join(root, pat))]
    files = [f for f in files if 'tu-duy-content' not in f]
    htmls = [os.path.join(root, f) for f in ('renderer/index.html', 'parent/index.html')]
    for f in files + htmls:
        s = open(f, encoding='utf-8').read()
        before = viethoa_lib.CAP_COUNT[0]
        n = fix_html(s) if f.endswith('.html') else fix_js(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n)
            print(os.path.relpath(f, root), viethoa_lib.CAP_COUNT[0] - before)
