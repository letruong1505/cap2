"""Thư viện dựng bài học Tư duy & lập trình: khung 8 mục, hình khối Scratch, bảng theo dõi Python, sơ đồ SVG."""
import html, io, re, subprocess, sys, math

E = html.escape

def run(code, stdin=''):
    r = subprocess.run([sys.executable, '-I', '-c', code], input=stdin, capture_output=True, text=True, timeout=10)
    assert r.returncode == 0, r.stderr + '\n' + code
    return r.stdout.rstrip('\n')

# ---------- thành phần cơ bản ----------
def li(items): return '<ul class="tl">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def ol(items): return '<ol class="tl tol">' + ''.join('<li>%s</li>' % i for i in items) + '</ol>'
def card(n, title, body): return '<section class="tcard"><h4><span class="tn">%s</span>%s</h4>%s</section>' % (n, title, body)
def tsum(goal, prep, prod):
    return '<div class="tsum"><div class="tsum-l">Tóm tắt bài</div><ul><li><b>Mục tiêu:</b> %s</li><li><b>Chuẩn bị:</b> %s</li><li><b>Sản phẩm:</b> %s</li></ul></div>' % (goal, prep, prod)
def think(items, lbl='Khai mở tư duy'): return '<div class="card think"><div class="lbl">%s</div>%s</div>' % (lbl, li(items))
def note(t): return '<p class="tnote">%s</p>' % t
def chap(t): return '<div class="tchap">%s</div>' % t
def ex(bad, good): return '<div class="ex"><div class="ex-row ex-bad"><b>Chưa tốt:</b> %s</div><div class="ex-row ex-good"><b>Tốt hơn:</b> %s</div></div>' % (bad, good)
def code(src, out=None):
    s = '<pre class="code">%s</pre>' % E(src.strip('\n'))
    if out is not None: s += '<div class="code-out-l">Kết quả khi chạy</div><pre class="code out">%s</pre>' % E(out)
    return s
def fig(inner, cap): return '<figure class="aiw-fig">%s<figcaption>%s</figcaption></figure>' % (inner, cap)
def svg(w, h, inner, label, cls='tdfig'):
    return '<svg class="%s" viewBox="0 0 %d %d" role="img" aria-label="%s"><rect width="%d" height="%d" fill="#fff"/><g font-family="sans-serif" font-size="16">%s</g></svg>' % (cls, w, h, E(label), w, h, inner)

# ---------- khối Scratch dạng HTML ----------
CATS = [
    (r'^khi ', 'ev'), (r'^(tiến|lùi|quay|đến|đi tới|đặt x|đặt y|thay đổi x|thay đổi y|hướng|nảy)', 'mo'),
    (r'^(nói|nghĩ|hiện|ẩn|đổi|chuyển)', 'lo'), (r'^(lặp|nếu|chờ|dừng|mãi)', 'co'), (r'^hỏi', 'se'),
    (r'^(hạ bút|nhấc bút|xóa hết|đặt màu|đặt độ dày|đóng dấu)', 'pe'), (r'^(đặt|thêm|hiện biến)', 'va'), (r'^\(', 'cm'),
]
def _cat(t):
    for rx, c in CATS:
        if re.match(rx, t): return c
    return 'va'
def _pill(t):
    t = E(t)
    t = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)', r'<i>\1</i>', t)
    t = re.sub(r'(?<![\w>])(\d+(?:[.,]\d+)?)(?![\w;])', r'<i>\1</i>', t)
    return t
def sblocks(src, hl=()):
    """Vẽ chồng khối Scratch từ văn bản thụt lề 2 dấu cách. hl: chỉ số dòng cần làm nổi bật."""
    out = ['<div class="sb">']
    for i, ln in enumerate(src.strip('\n').split('\n')):
        ind = (len(ln) - len(ln.lstrip(' '))) // 2
        t = ln.strip()
        c = _cat(t)
        out.append('<div class="sbk sb-%s%s" style="margin-left:%dpx">%s</div>' % (c, ' hl' if i in hl else '', ind * 22, _pill(t)))
    out.append('</div>')
    return ''.join(out)

def turtle_pts(moves):
    x = y = 0.0; ang = 90.0; pts = [(0.0, 0.0)]
    for m, v in moves:
        if m == 'f':
            x += v * math.cos(math.radians(ang)); y += v * math.sin(math.radians(ang)); pts.append((x, y))
        elif m == 'r': ang -= v
        elif m == 'l': ang += v
    return pts
def turtle_svg(moves, size=140, label='Hình nhân vật vẽ ra'):
    pts = turtle_pts(moves)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    w = max(max(xs) - min(xs), 1); h = max(max(ys) - min(ys), 1); sc = (size - 30) / max(w, h)
    P = [((p[0] - min(xs)) * sc + 15, size - ((p[1] - min(ys)) * sc + 15)) for p in pts]
    d = ' '.join('%.1f,%.1f' % p for p in P)
    inner = ('<rect x="1" y="1" width="%d" height="%d" rx="8" fill="#f7fbff" stroke="#9db4c9"/><polyline points="%s" fill="none" stroke="#e8590c" stroke-width="3" stroke-linejoin="round"/>'
             '<circle cx="%.1f" cy="%.1f" r="5" fill="#2a8a4a"/><circle cx="%.1f" cy="%.1f" r="4" fill="#1f6fb2"/>') % (size - 2, size - 2, d, P[0][0], P[0][1], P[-1][0], P[-1][1])
    return '<svg class="tstage" viewBox="0 0 %d %d" role="img" aria-label="%s"><g>%s</g></svg>' % (size, size, E(label), inner)

# ---------- các bước minh họa ----------
def step(n, caption, body): return '<div class="tstep"><span class="tn s">%s</span><div class="tstep-b"><p class="tstep-c">%s</p>%s</div></div>' % (n, caption, body)
def steps(*items): return '<div class="tsteps">' + ''.join(step(i + 1, c, b) for i, (c, b) in enumerate(items)) + '</div>'

def _snap(d):
    out = []
    for k, v in d.items():
        if k.startswith('__') or callable(v) or type(v).__name__ == 'module': continue
        out.append((k, v))
    return out
def _fmt(v):
    if isinstance(v, str): return '"%s"' % v
    if isinstance(v, float): return ('%.4f' % v).rstrip('0').rstrip('.')
    return repr(v)
def ptrace(src, stdin='', pick=None, maxn=6, captions=None):
    """Chạy thật và dựng các bước: dòng vừa chạy, giá trị biến, kết quả in ra."""
    src = src.strip('\n'); lines = src.split('\n')
    inp = iter(stdin.split('\n') if stdin else [])
    out = io.StringIO(); events = []
    def _print(*a, sep=' ', end='\n'): out.write(sep.join(str(x) for x in a) + end)
    g = {'print': _print, 'input': lambda p='': next(inp), '__name__': '__main__'}
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != '<study>': return None
        if frame.f_code.co_name != '<module>': return None
        if event == 'line': events.append((frame.f_lineno, out.getvalue()))
        return tracer
    sys.settrace(tracer)
    try: exec(compile(src, '<study>', 'exec'), g)
    finally: sys.settrace(None)
    # trạng thái SAU mỗi dòng: chạy lại từng bước nhỏ sẽ tốn; lấy bằng cách theo dõi lần 2
    states = []
    out2 = io.StringIO(); inp2 = iter(stdin.split('\n') if stdin else [])
    def _print2(*a, sep=' ', end='\n'): out2.write(sep.join(str(x) for x in a) + end)
    g2 = {'print': _print2, 'input': lambda p='': next(inp2), '__name__': '__main__'}
    cnt = [0]
    def tracer2(frame, event, arg):
        if frame.f_code.co_filename != '<study>' or frame.f_code.co_name != '<module>': return None
        if event == 'line':
            if cnt[0] > 0: states.append((_snap(frame.f_globals), out2.getvalue()))
            cnt[0] += 1
        return tracer2
    sys.settrace(tracer2)
    try: exec(compile(src, '<study>', 'exec'), g2)
    finally: sys.settrace(None)
    states.append((_snap(g2), out2.getvalue()))
    n = len(events); assert len(states) == n
    idx = pick if pick is not None else sorted(set(round(i * (n - 1) / (maxn - 1)) for i in range(maxn))) if n > maxn else list(range(n))
    res = []
    for j, i in enumerate(idx):
        ln, _ = events[i]; vars_, o = states[i]
        code_html = ''.join('<div class="pl%s"><span class="pn">%d</span>%s</div>' % (' cur' if k + 1 == ln else '', k + 1, E(t) or '&nbsp;') for k, t in enumerate(lines))
        v = ''.join('<span class="pv"><b>%s</b> = %s</span>' % (E(k), E(_fmt(x))) for k, x in vars_) or '<span class="pv none">(chưa có biến)</span>'
        o_html = '<div class="po"><b>In ra:</b> <pre>%s</pre></div>' % E(o.rstrip('\n')) if o.strip() else ''
        cap = (captions[j] if captions and j < len(captions) else 'Vừa chạy xong <b>dòng %d</b>.' % ln)
        res.append((cap, '<div class="ptr"><div class="pcode">%s</div><div class="pvars">%s</div>%s</div>' % (code_html, v, o_html)))
    return steps(*res)

# ---------- sơ đồ SVG ----------
def _fw(x): return '<figure class="aiw-fig">%s<figcaption><span class="tdhint">Trên điện thoại: vuốt ngang để xem hết hình.</span></figcaption></figure>' % x
def _arrow(x1, y1, x2, y2, col='#9db4c9'):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="3"/><polygon points="%s,%s %s,%s %s,%s" fill="%s"/>' % (x1, y1, x2 - 8 if x2 > x1 else x2 + 8, y2, col, x2, y2, x2 - 10 if x2 > x1 else x2 + 10, y2 - 6, x2 - 10 if x2 > x1 else x2 + 10, y2 + 6, col)
def flowrow(labels, title='', colors=None, back=False, w=700):
    n = len(labels); bw = (w - 20 - (n - 1) * 34) / n; inner = ''
    if title: inner += '<text x="%d" y="24" text-anchor="middle" font-weight="700" fill="#17406b">%s</text>' % (w // 2, E(title))
    for i, t in enumerate(labels):
        x = 10 + i * (bw + 34); col = (colors or ['#e6f1fb'] * n)[i]
        inner += '<rect x="%.1f" y="46" width="%.1f" height="70" rx="10" fill="%s" stroke="#1f6fb2"/>' % (x, bw, col)
        parts = t.split('|')
        for k, p in enumerate(parts):
            inner += '<text x="%.1f" y="%d" text-anchor="middle" fill="#1c2733" font-size="%d">%s</text>' % (x + bw / 2, 76 + k * 20 - (len(parts) - 1) * 8, 15 if len(parts) > 1 else 16, E(p))
        if i < n - 1:
            xa = x + bw + 4
            inner += _arrow(xa + 26, 81, xa, 81) if back else _arrow(xa, 81, xa + 26, 81)
    return _fw(svg(w, 132, inner, title or 'Sơ đồ các bước'))
def reverse_svg(fwd, bwd, start, end, title='Đi xuôi rồi đi ngược', w=700):
    """fwd: các phép xuôi theo thứ tự; bwd: các phép ngược theo thứ tự ÁP DỤNG (đảo ngược fwd)."""
    n = len(fwd); gap = 30; bw = (w - 20 - (n + 1) * gap) / (n + 2)
    xs = [10 + i * (bw + gap) for i in range(n + 2)]
    inner = '<text x="%d" y="24" text-anchor="middle" font-weight="700" fill="#17406b">%s</text>' % (w // 2, E(title))
    inner += '<text x="10" y="50" fill="#d9822b" font-weight="700">XUÔI →</text>'
    top = [start] + fwd + [end]
    for i, t in enumerate(top):
        inner += '<rect x="%.1f" y="58" width="%.1f" height="44" rx="9" fill="%s" stroke="#6b7785"/><text x="%.1f" y="85" text-anchor="middle" fill="#1c2733">%s</text>' % (xs[i], bw, '#fdf0e1' if 0 < i < n + 1 else '#fff', xs[i] + bw / 2, E(t))
        if i < n + 1: inner += _arrow(xs[i] + bw + 3, 80, xs[i] + bw + gap - 3, 80, '#d9822b')
    inner += '<text x="10" y="132" fill="#2a8a4a" font-weight="700">← NGƯỢC</text>'
    bot = ['?'] + [bwd[n - i] for i in range(1, n + 1)] + [end]
    for i, t in enumerate(bot):
        inner += '<rect x="%.1f" y="140" width="%.1f" height="44" rx="9" fill="%s" stroke="#6b7785"/><text x="%.1f" y="167" text-anchor="middle" fill="#1c2733">%s</text>' % (xs[i], bw, '#e6f6ea' if 0 < i < n + 1 else '#fff', xs[i] + bw / 2, E(t))
        if i < n + 1: inner += _arrow(xs[i] + bw + gap - 3, 162, xs[i] + bw + 3, 162, '#2a8a4a')
    return _fw(svg(w, 200, inner, title))
def decision_svg(q, yes, no, title='Rẽ nhánh', w=700):
    inner = ('<polygon points="350,20 470,70 350,120 230,70" fill="#fff4d6" stroke="#d9822b" stroke-width="2"/><text x="350" y="76" text-anchor="middle" font-weight="700">%s</text>'
             '<line x1="230" y1="70" x2="120" y2="70" stroke="#2a8a4a" stroke-width="3"/><line x1="120" y1="70" x2="120" y2="150" stroke="#2a8a4a" stroke-width="3"/><text x="170" y="60" fill="#2a8a4a" font-weight="700">ĐÚNG</text>'
            '<line x1="470" y1="70" x2="580" y2="70" stroke="#c0392b" stroke-width="3"/><line x1="580" y1="70" x2="580" y2="150" stroke="#c0392b" stroke-width="3"/><text x="500" y="60" fill="#c0392b" font-weight="700">SAI</text>'
            '<rect x="30" y="150" width="180" height="50" rx="10" fill="#e6f6ea" stroke="#2a8a4a"/><text x="120" y="181" text-anchor="middle">%s</text>'
            '<rect x="490" y="150" width="180" height="50" rx="10" fill="#fdecea" stroke="#c0392b"/><text x="580" y="181" text-anchor="middle">%s</text>') % (E(q), E(yes), E(no))
    return _fw(svg(w, 212, inner, title))
def list_svg(vals, title='Danh sách và vị trí (chỉ số)', w=700):
    n = len(vals); bw = min(80, (w - 40) / n); x0 = (w - bw * n) / 2
    inner = '<text x="%d" y="24" text-anchor="middle" font-weight="700" fill="#17406b">%s</text>' % (w // 2, E(title))
    for i, v in enumerate(vals):
        x = x0 + i * bw
        inner += '<rect x="%.1f" y="46" width="%.1f" height="50" fill="#e6f1fb" stroke="#1f6fb2"/><text x="%.1f" y="78" text-anchor="middle" font-size="18" fill="#1c2733">%s</text><text x="%.1f" y="118" text-anchor="middle" fill="#d9822b" font-weight="700">%d</text>' % (x, bw, x + bw / 2, E(str(v)), x + bw / 2, i)
    inner += '<text x="%d" y="146" text-anchor="middle" fill="#5b6773">số cam bên dưới là chỉ số (đếm từ 0)</text>' % (w // 2)
    return _fw(svg(w, 160, inner, title))

# ---------- khung bài chuẩn 8 mục ----------
def err(bad, why, fix):
    return '<div class="terr"><div class="terr-t">⚠ %s</div><p>%s</p><p class="terr-f">✔ %s</p></div>' % (bad, why, fix)
def eg(title, body): return '<div class="tex"><h5>%s</h5>%s</div>' % (title, body)
LEVELS = ['Mức 1 · Khởi động', 'Mức 2 · Làm quen', 'Mức 3 · Vận dụng', 'Mức 4 · Nâng cao', 'Mức 5 · Thử thách']
def prac(i, task, ans, data=None):
    s = '<section class="tcard tprac"><h4><span class="tn">T%d</span>%s <span class="lvl">%s</span></h4><p>%s</p>' % (i + 1, LEVELS[i], '★' * (i + 1) + '☆' * (4 - i), task)
    if data: s += data
    s += '<details class="tans"><summary>Xem lời giải</summary>%s</details></section>' % ans
    return s
def std(title, sub, summary, meaning, usage, thinking, apply_title, apply_html, figs, errors, examples, practice, apply_lang):
    assert len(practice) == 5, title
    parts = [tsum(*summary),
        card(1, 'Ý nghĩa của bài học', li(meaning)),
        card(2, 'Dùng bài học này như thế nào', usage),
        card(3, 'Tư duy bài học mang đến', thinking),
        card(4, apply_title, apply_html),
        card(5, 'Hình minh họa từng bước', figs),
        card(6, 'Lỗi sai hay gặp', ''.join(errors)),
        card(7, 'Ví dụ minh họa', ''.join(examples)),
        chap('Bài thực hành · 5 mức tăng dần để nâng cấp tư duy')]
    parts += [prac(i, t, a, d) for i, (t, a, d) in enumerate(practice)]
    return {'title': title, 'sub': sub, 'html': '\n'.join(parts)}
