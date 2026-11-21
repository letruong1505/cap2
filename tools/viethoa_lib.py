"""Viết hoa chữ cái đầu sau dấu chấm, hai chấm, chấm hỏi, chấm than (bỏ qua mã lệnh)."""
# ---- Viết hoa chữ đầu sau dấu "." và ":" (chỉ ở phần chữ thường, bỏ qua mã lệnh) ----
import re as _re
_LOW = 'a-zà-ỹ'
_TOK = _re.compile(r'(<[^>]*>)')
_AFTER = _re.compile(r'((?:[.:?!])\s+)([' + _LOW + r'])(\S*)')
_VN = _re.compile(r'[^\x00-\x7f]')
CAP_COUNT = [0]
def _cap_text(t, svg):
    def rep(m):
        before = t[:m.start()]
        nxt = m.group(2) + m.group(3)
        if not _VN.search(nxt) and _re.search(r'[A-Z_(/.@]|^https?', nxt[1:] if len(nxt) > 1 else '') or nxt.startswith(('http', 'www')):
            return m.group(0)
        if m.group(1)[0] == ':' or m.group(1)[0] == '.':
            w = _re.findall(r'(\S+)$', before)
            w = w[0] if w else ''
            if m.group(1)[0] == '.' and (_re.search(r'\d$', w) or len(w) <= 2 and w.islower() or w.endswith(('v.v', 'vd', 'tr'))):
                return m.group(0)
            if svg and not _VN.search(w):   # trong hình: "def: ..." là mã lệnh, giữ nguyên
                return m.group(0)
            if m.group(1)[0] == ':' and _re.search(r'[\]\)\}"\'=]$', w):
                return m.group(0)
        CAP_COUNT[0] += 1
        return m.group(1) + m.group(2).upper() + m.group(3)
    return _AFTER.sub(rep, t)
def cap_html(h):
    parts = _TOK.split(h); out = []; skip = 0; svgd = 0
    for part in parts:
        if part.startswith('<'):
            low = part.lower()
            if _re.match(r'<(pre|code|script|style)\b', low): skip += 1
            elif _re.match(r'</(pre|code|script|style)\b', low): skip = max(0, skip - 1)
            elif low.startswith('<svg'): svgd += 1
            elif low.startswith('</svg'): svgd = max(0, svgd - 1)
            out.append(part)
        else:
            out.append(part if skip else _cap_text(part, svgd > 0))
    return ''.join(out)
def cap_walk(o):
    if isinstance(o, str): return cap_html(o)
    if isinstance(o, list): return [cap_walk(x) for x in o]
    if isinstance(o, dict): return {k: cap_walk(v) for k, v in o.items()}
    return o
