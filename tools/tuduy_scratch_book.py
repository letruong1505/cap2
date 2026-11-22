"""Chuyển cuốn "Tư duy trước, Scratch sau" (tools/data/scratch-book) thành lộ trình Scratch k811.
Nguồn: book.json.gz (pandoc AST của bản docx) + img/*.webp. Không có phụ lục B (phiếu photocopy) và C (thẻ thử thách).
Tuổi hiển thị 8–11 (sách gốc ghi 8–12). Các sửa lỗi nội dung nằm ở FIXES."""
import gzip, json, os, re, base64, html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'scratch-book')
E = html.escape

# ---------------------------------------------------------------- sửa nội dung (đã duyệt)
# (mẫu regex trên HTML đã dựng, thay bằng, số lần tối thiểu phải khớp)
FIXES = [
    # tuổi: 8–11
    (r'8–12 tuổi', '8–11 tuổi', 0),
    (r'10–12 tuổi', '10–11 tuổi', 0),
    # (1) Scratch 3 không có ≥: dùng "lớn hơn" với số nhỏ hơn 1 đơn vị
    # (2) Chương 3: 120° lặp 3 lần
    (r'thử 4 lần với góc 120°', 'thử 3 lần với góc 120°', 1),
    # (3) Chương 4: không dẫn về chương tọa độ (Chương 5 chưa học)
    (r'Làm bốn kịch bản phím mũi tên như chương tọa độ hoặc dùng một phím để tiến\.',
     'Làm kịch bản phím mũi tên như “Di chuyển mẫu” ở bên dưới (chỉ cần phím phải và phím trái), hoặc chỉ dùng một phím để tiến.', 1),
    (r'<p>Thêm khối giới hạn x của Giỏ', '<p class="tnote">Scratch 3 chỉ có ba phép so sánh: nhỏ hơn, bằng và lớn hơn. “Điểm &gt; 9” nghĩa là từ 10 điểm trở lên; “Bỏ lỡ &gt; 4” nghĩa là từ 5 lần bỏ lỡ.</p><p>Thêm khối giới hạn x của Giỏ', 1),
    (r'<b>ĐƯỜNG KHÁM PHÁ', '<b>Đường khám phá', 16),
    (r'<b>ĐƯỜNG SÁNG TẠO', '<b>Đường sáng tạo', 16),
    # (7) Chương 13: ghi kết quả khớp luật chơi (thắng ở 10 điểm, thua ở 5 lần bỏ lỡ)
    (r'ghi số điểm khi chơi một phút\.',
     'mỗi tốc độ chơi 3 ván, ghi lại số táo hứng được trước khi thua (hoặc thời gian để đủ 10 điểm).', 1),
    # (8) Chương 14: trả lời bằng số 1/2/3 cho dễ gõ, không cần dấu
    (r'giấy sạch →\s*giấy; chai nhựa sạch → nhựa; vỏ chuối → hữu cơ\.',
     'giấy sạch → 1 (giấy); chai nhựa sạch → 2 (nhựa); vỏ chuối → 3 (hữu cơ). Người chơi trả lời bằng số 1, 2 hoặc 3 cho dễ gõ.', 1),
    (r'Nếu trả lời = [“"]nhựa[”"]', 'Nếu trả lời = 2', 1),
    (r'Bấm chai và trả lời [“"]nhựa[”"]', 'Bấm chai và trả lời 2 (nhựa)', 1),
    (r'Bấm chai, trả lời [“"]giấy[”"]', 'Bấm chai, trả lời 1 (giấy)', 1),
    (r'Chai nhựa sạch: giấy, nhựa hay hữu cơ\?', 'Chai nhựa sạch: gõ 1 (giấy), 2 (nhựa) hay 3 (hữu cơ)?', 1),
    # (9) Chương 8: "còn mạng" dễ nhầm với mạng internet
    (r'chạm màu và còn mạng để tạo hệ thống mất mạng sau mỗi lần va chạm', 'chạm màu và còn lượt sống để tạo hệ thống mất một lượt sống sau mỗi lần va chạm', 1),
    # bản trong ứng dụng: khối lệnh được vẽ bằng khối màu, không phải mô tả chữ cho bản in
    (r'Các đoạn khối lệnh được viết dạng mô tả văn bản để dễ đọc và in ấn; khi thực hành',
     'Các đoạn khối lệnh trong sách được vẽ bằng khối màu giống Scratch; khi thực hành', 1),
]

# ---------------------------------------------------------------- inline / block
def txt(x):
    if isinstance(x, list): return ''.join(txt(i) for i in x)
    if isinstance(x, dict):
        t = x['t']
        if t == 'Str': return x['c']
        if t in ('Space', 'SoftBreak'): return ' '
        if t == 'LineBreak': return '\n'
        if t == 'Quoted': return '“' + txt(x['c'][1]) + '”'
        if 'c' in x: return txt(x['c'])
    return ''

def inl(x):
    if isinstance(x, list): return ''.join(inl(i) for i in x)
    t = x['t']
    if t == 'Str': return E(x['c'], quote=False)
    if t in ('Space', 'SoftBreak'): return ' '
    if t == 'LineBreak': return '<br>'
    if t == 'Strong': return '<b>' + inl(x['c']) + '</b>'
    if t == 'Emph': return '<i>' + inl(x['c']) + '</i>'
    if t == 'Quoted': return '“' + inl(x['c'][1]) + '”'
    if t == 'Code': return '<code>' + E(x['c'][1]) + '</code>'
    if t in ('Span', 'SmallCaps'): return inl(x['c'][1])
    if t == 'Link': return inl(x['c'][1])
    raise ValueError('inline chưa hỗ trợ: ' + t)

def clean(s):
    s = re.sub(r'(?:\\?_){3,}', '', s)       # gạch chân điền chỗ trống trong sách in
    s = re.sub(r'_{3,}', '', s)
    return re.sub(r'\s+(<br>|$)', r'\1', s).strip()

def has_image(b):
    return b['t'] in ('Para', 'Plain') and any(i['t'] == 'Image' for i in b['c'])

def img_name(b):
    for i in b['c']:
        if i['t'] == 'Image': return os.path.basename(i['c'][2][0])

_IMG = {}
def img_uri(name):
    if name not in _IMG:
        p = os.path.join(DATA, 'img', name.replace('.png', '.webp'))
        _IMG[name] = 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    return _IMG[name]

def figure(name, cap=None):
    c = '<figcaption>%s</figcaption>' % E(cap) if cap else ''
    return '<figure class="aiw-fig"><img src="%s" alt="%s" loading="lazy">%s</figure>' % (img_uri(name), E(cap or 'Hình minh họa'), c)

# ---------------------------------------------------------------- khối lệnh Scratch
OPEN = re.compile(r'^(nếu .* thì|lặp mãi|lặp lại .*|lặp .*)$')
def split_groups(s):
    """Dựng '<i>' lồng nhau cho ( ) [ ] < >. Trả về html."""
    out = []; stack = []   # mỗi phần tử: (ký tự mở, vị trí bắt đầu trong out)
    i = 0
    def close(kind, start):
        inner = ''.join(out[start:]); del out[start:]
        cls = ''
        raw = re.sub(r'<[^>]+>', '', inner)
        nested = '<i' in inner
        if kind == '<':
            cls = 'se bool' if re.match(r'\s*(đang )?chạm', raw) else 'op bool'
        elif kind == '(':
            if re.match(r'\s*(trả lời|vị trí [xy]|hướng)\s*$', raw): cls = 'se'
            elif nested or re.match(r'\s*(nối|lấy ngẫu nhiên)', raw) or re.search(r' [+\-*/] ', raw): cls = 'op'
        out.append('<i%s>%s</i>' % (' class="%s"' % cls if cls else '', inner))
    while i < len(s):
        c = s[i]
        prev = s[i - 1] if i else ' '
        nxt = s[i + 1] if i + 1 < len(s) else ' '
        if c in '([' or (c == '<' and nxt != ' ' and not stack_has_lt_literal(s, i)):
            stack.append((c, len(out))); i += 1; continue
        if stack and ((c == ')' and stack[-1][0] == '(') or (c == ']' and stack[-1][0] == '[') or (c == '>' and stack[-1][0] == '<' and prev != ' ')):
            k, st = stack.pop(); close(k, st); i += 1; continue
        out.append(E(c, quote=False)); i += 1
    assert not stack, s
    return ''.join(out)

def stack_has_lt_literal(s, i):
    return False

def classify(line):
    l = line.strip()
    if l.startswith('Khi '): return 'sb-ev'
    if l.startswith('phát tin'): return 'sb-ev sb-evs'
    if re.match(r'^(nếu|lặp|đợi|dừng|kết thúc)', l): return 'sb-co'
    if re.match(r'^(di chuyển|xoay|đi tới|lướt|hướng|thay đổi [xy] |đặt [xy] )', l): return 'sb-mo'
    if re.match(r'^(nói|nghĩ|hiện|ẩn|chuyển phông|thay đổi hiệu ứng|đổi trang)', l): return 'sb-lo'
    if re.match(r'^hỏi', l): return 'sb-se'
    if re.match(r'^(đặt|thay đổi) \[', l): return 'sb-va'
    return 'sb-cm'

LINE_FIXES = [   # sửa trên từng dòng khối lệnh (trước khi dựng khối)
    (r'>= \((\d+)\)', lambda m: '> (%d)' % (int(m.group(1)) - 1), 2),      # (1) Scratch 3 không có ≥
    (r'= \[nhựa\]', '= [2]', 1),                                           # (8) trả lời bằng số
]
LINE_HITS = [0] * len(LINE_FIXES)

def script_html(lines):
    # tách "Khi … → khối lệnh" thành hai dòng
    flat = []
    for l in lines:
        l = l.strip()
        if not l: continue
        for k, (pat, rep, _) in enumerate(LINE_FIXES):
            l, n = re.subn(pat, rep, l); LINE_HITS[k] += n
        if ' → ' in l and l.startswith('Khi '): flat += [p.strip() for p in l.split(' → ', 1)]
        else: flat.append(l)
    groups = []; cur = []; depth = 0
    for l in flat:
        cls = classify(l)
        if cls == 'sb-ev' and cur: groups.append(cur); cur = []; depth = 0
        if re.match(r'^kết thúc', l): depth = max(0, depth - 1); cur.append((cls + ' sb-end', l, depth)); continue
        if l == 'nếu không': cur.append((cls, l, max(0, depth - 1))); continue
        cur.append((cls, l, depth))
        if OPEN.match(l) and not l.startswith('kết thúc'): depth += 1
    if cur: groups.append(cur)
    out = []
    for g in groups:
        rows = []
        for cls, l, d in g:
            body = split_groups(l)
            rows.append('<div class="sbk %s" style="margin-left:%dpx">%s</div>' % (cls, d * 22, body))
        out.append('<div class="sb">%s</div>' % ''.join(rows))
    return ''.join(out)

# ---------------------------------------------------------------- bảng / hộp
def cells(tb):
    """-> (head_rows, body_rows); mỗi ô = danh sách block"""
    c = tb['c']
    head = [[cell[4] for cell in r[1]] for r in c[3][1]]
    body = [[cell[4] for cell in r[1]] for bd in c[4] for r in bd[3]]
    return head, body

def blocks_html(bs):
    return ''.join(block_html(b) for b in bs)

def para(b):
    return clean(inl(b['c']))

def callout(title, rest, kind='think'):
    inner = ''.join('<p>%s</p>' % p for p in rest if p)
    return '<div class="card think"><div class="lbl">%s</div>%s</div>' % (sentence(title), inner)

def sentence(t):
    t = t.strip().rstrip('.')
    return t[:1].upper() + t[1:].lower() if t.isupper() else t

def table_html(tb):
    head, body = cells(tb)
    if len(head) + len(body) == 1 and len((head or body)[0]) == 1:       # hộp một ô
        bs = (head or body)[0][0]
        first = bs[0]
        if first['t'] in ('Para', 'Plain') and first['c'] and first['c'][0]['t'] == 'Strong' and len(first['c']) == 1:
            title = txt(first['c'])
            rest = [para(b) for b in bs[1:]]
            if title.startswith('SAU CHƯƠNG NÀY'):
                items = [x.strip(' .') for x in re.split(r'\s•\s', ' '.join(rest)) if x.strip()]
                return '<div class="tsum"><div class="tsum-l">Sau chương này, em làm được</div><ul>%s</ul></div>' % ''.join('<li>%s.</li>' % x.rstrip('.') for x in items)
            return callout(title, rest)
        return ''  # hộp kịch bản được xử lý riêng
    th = ''.join('<th>%s</th>' % clean(inl(c[0]['c'])) for c in head[0]) if head else ''
    rows = ''.join('<tr>' + ''.join('<td>%s</td>' % '<br>'.join(para(b) for b in c) for c in r) + '</tr>' for r in body)
    return '<table>%s<tbody>%s</tbody></table>' % ('<thead><tr>%s</tr></thead>' % th if th else '', rows)

def script_from_table(tb):
    head, body = cells(tb)
    bs = (head or body)[0][0]
    lines = []
    for b in bs: lines += txt(b['c']).split('\n')
    return lines

def block_html(b):
    t = b['t']
    if t in ('Para', 'Plain'):
        s = para(b)
        return '<p>%s</p>' % s if s else ''
    if t == 'BulletList':
        return '<ul class="tl">' + ''.join('<li>%s</li>' % ''.join(para(x) if x['t'] in ('Para', 'Plain') else '' for x in it) for it in b['c']) + '</ul>'
    if t == 'Table': return table_html(b)
    if t == 'BlockQuote': return '<ul class="tl tchk">' + ''.join('<li>%s</li>' % re.sub(r'^□\s*', '', para(x)) for x in b['c']) + '</ul>'
    raise ValueError('block chưa hỗ trợ: ' + t)

NUM = re.compile(r'^\s*(\d+)\.\s*$')
def numbered(b):
    """Para bắt đầu bằng **n.** -> (n, html còn lại) hoặc None"""
    if b['t'] != 'Para' or not b['c'] or b['c'][0]['t'] != 'Strong': return None
    m = NUM.match(txt(b['c'][0]['c']))
    if not m: return None
    return int(m.group(1)), clean(inl(b['c'][1:]))

def step_html(n, rest, checks):
    m = re.match(r'^([^:<]{2,60}):\s+(.*)$', rest, re.S)
    body = '<b>%s:</b> %s' % (m.group(1), m.group(2)) if m else rest
    tn = ''.join('<p class="tnote">✔ %s</p>' % c for c in checks)
    return '<div class="tstep"><span class="tn s">%d</span><div class="tstep-b"><p class="tstep-c">%s</p>%s</div></div>' % (n, body, tn)

def is_script_label(b):
    return b['t'] == 'Para' and txt(b['c']).startswith('KỊCH BẢN KHỐI LỆNH')

def script_label(b):
    rest = txt(b['c']).split('·', 1)[1].strip()
    who, _, what = rest.partition(' – ')
    who = who.title()
    return 'Kịch bản khối lệnh · ' + who + (' – ' + what[:1].upper() + what[1:].lower() if what else '')

def render_section(body):
    """body: các block của một mục (không gồm tiêu đề). Gom bước đánh số thành .tsteps, ảnh thành figure."""
    out = []; i = 0; steps = []; nums = []
    def flush_steps():
        nonlocal steps, nums
        if steps: out.append('<div class="tsteps">%s</div>' % ''.join(steps)); steps = []
        if nums: out.append('<ol class="tl tol">%s</ol>' % ''.join('<li>%s</li>' % x for x in nums)); nums = []
    while i < len(body):
        b = body[i]
        if has_image(b):
            flush_steps()
            name = img_name(b)
            cap = para(body[i + 1]) if i + 1 < len(body) and body[i + 1]['t'] == 'Para' and txt(body[i + 1]['c']).startswith('Hình ') else None
            n = int(re.search(r'image(\d+)', name).group(1))
            skip = bool(cap and re.match(r'Hình \d+\.3 - Bản minh họa khối màu', cap))   # đã thay bằng khối lệnh thật
            if n == 3: skip = True                                                       # sơ đồ chương 1 lệch với lời văn: dựng lại bên dưới
            if not skip: out.append(figure(name, cap))
            if n == 3: out.append(FLOW_CH1)
            i += 2 if cap else 1
            continue
        if is_script_label(b):
            flush_steps()
            lines = script_from_table(body[i + 1])
            if all(classify(l) == 'sb-cm' for l in lines if l.strip()):      # phiếu thiết kế (chữ), không phải khối lệnh
                out.append('<p class="sbt">%s</p>' % script_label(b).replace('Kịch bản khối lệnh', 'Phiếu thiết kế'))
                out.append('<ul class="tl">%s</ul>' % ''.join('<li>%s</li>' % E(l.strip()) for l in lines if l.strip()))
            else:
                out.append('<p class="sbt">%s</p>' % script_label(b))
                out.append(script_html(lines))
            i += 2; continue
        nb = numbered(b)
        if nb:
            n, rest = nb
            if i + 1 < len(body) and body[i + 1]['t'] == 'BlockQuote':      # bước + "Tự kiểm tra"
                checks = [para(x) for x in body[i + 1]['c']]
                checks = [re.sub(r'^Tự kiểm tra:\s*', 'Tự kiểm tra: ', c) for c in checks]
                steps.append(step_html(n, rest, [c.replace('Tự kiểm tra: ', '', 1) if False else c for c in checks])); i += 2; continue
            if steps: flush_steps()
            nums.append(rest); i += 1; continue
        flush_steps()
        out.append(block_html(b)); i += 1
    flush_steps()
    return ''.join(out)

FLOW_CH1 = ('<figure class="aiw-fig"><svg class="tdfig tdnarrow" viewBox="0 0 760 150" role="img" aria-label="Sơ đồ bốn bước làm bánh mì phết mứt">'
            '<rect width="760" height="150" fill="#fff"/><g font-family="sans-serif" font-size="16">' +
            ''.join('<rect x="%d" y="26" width="154" height="70" rx="12" fill="%s" stroke="#b9c9cf"/><text x="%d" y="52" font-weight="700" fill="#0f7c86">%d</text><text x="%d" y="80" font-weight="700" fill="#1c2733">%s</text>%s' % (
                12 + k * 188, col, 28 + k * 188, k + 1, 28 + k * 188, lab, '<path d="M%d 61h24m-8-7 8 7-8 7" fill="none" stroke="#6b9a9c" stroke-width="3"/>' % (172 + k * 188) if k < 3 else '')
                for k, (lab, col) in enumerate([('Lấy bánh', '#d9eef0'), ('Mở lọ mứt', '#e8eefb'), ('Phết mứt', '#fff0dc'), ('Đặt lên đĩa', '#e0f2e5')])) +
            '<text x="12" y="128" fill="#5b6773">Tự hỏi: nếu thiếu dao phết, robot sẽ làm gì?</text></g></svg>'
            '<figcaption>Hình 1.2 - Sơ đồ suy nghĩ. Che ô bên phải và thử đoán bước tiếp theo.</figcaption></figure>')

# ---------------------------------------------------------------- dựng sách
def load():
    return json.load(gzip.open(os.path.join(DATA, 'book.json.gz'), 'rt', encoding='utf-8'))['blocks']

def card(n, title, body):
    return '<section class="tcard"><h4><span class="tn">%s</span>%s</h4>%s</section>' % (n, title, body)

def sections(bs):
    """chia danh sách block theo Header cấp 2 -> [(tiêu đề, [block])]; phần trước header đầu tiên có tiêu đề None"""
    out = [(None, [])]
    for b in bs:
        if b['t'] == 'Header' and b['c'][0] == 2: out.append((txt(b['c'][2]), []))
        else: out[-1][1].append(b)
    return out

HITS = {}
def apply_fixes(h):
    for pat, rep, need in FIXES:
        h, n = re.subn(pat, rep, h)
        HITS[pat] = HITS.get(pat, 0) + n
    return h

def check_fixes():
    for k, (pat, rep, need) in enumerate(LINE_FIXES):
        assert LINE_HITS[k] == need, 'sửa dòng lệnh %s: %d lần' % (pat, LINE_HITS[k])
    for pat, rep, need in FIXES:
        assert HITS.get(pat, 0) >= need, 'sửa lỗi không khớp: %s (%d lần)' % (pat, HITS.get(pat, 0))

def chapter(head, bs):
    """head: (số chương, tên, tagline). bs: block từ sau Header1 tới hết chương."""
    num, name, tag = head
    parts = []
    secs = sections(bs)
    for title, body in secs:
        if title is None:
            parts.append(render_section(body)); continue
        m = re.match(r'^(\d+)\.\s*(.*)$', title)
        n, tt = (m.group(1), m.group(2)) if m else ('•', title)
        parts.append(card(n, E(tt), render_section(body)))
    return {'title': 'Chương %d · %s' % (num, name), 'sub': sentence(tag), 'html': apply_fixes('\n'.join(parts))}

def build():
    bl = load()
    # mốc: Header cấp 1 của từng chương/phụ lục; phần mở đầu là các block trước chương 1
    H1 = [i for i, b in enumerate(bl) if b['t'] == 'Header' and b['c'][0] == 1]
    chap_idx = [i for i in H1 if i > 43 or True]
    lessons = {}
    # ---- Mở đầu
    first_ch = next(i for i in H1 if bl[i - 1]['t'] == 'Para' and txt(bl[i - 1]['c']).startswith('CHƯƠNG 01'))
    front = bl[:first_ch - 1]
    fs = []; cur = None
    for b in front:
        if b['t'] == 'Header': cur = [txt(b['c'][2]), []]; fs.append(cur)
        elif cur: cur[1].append(b)
    F = {t: bb for t, bb in fs}
    def sec(title, n=None, key=None):
        return card(n, E(title), render_section(F[key or title])) if n else render_section(F[key or title])
    keys = list(F)
    def find(prefix): return next(k for k in keys if k.startswith(prefix))
    t1 = ''.join([
        card('1', 'Lời gửi tới người đọc', render_section(F[find('Lời gửi')])),
        card('2', 'Cuốn sách này dành cho ai?', render_section(F[find('Cuốn sách này')])),
        card('3', 'Cách học để thực sự tiến bộ', render_section(F[find('Cách học')]) + '<p class="tnote">Những chỗ có dấu “:” để trống, em ghi vào vở nháp hoặc nhật ký của mình.</p>'),
        card('4', 'Bản đồ tư duy của nhà phát minh', render_section(F[find('Bản đồ tư duy')])),
    ])
    lessons['tongquan'] = {'title': 'Mở đầu · Lời gửi tới người đọc', 'sub': 'Em sẽ học cách nghĩ trước, rồi mới dùng Scratch để kiểm chứng', 'html': apply_fixes(t1)}
    t2 = ''.join([
        card('1', 'Làm quen giao diện Scratch bằng hình ảnh', render_section(F[find('Làm quen giao diện')])),
        card('2', 'Quy ước để đọc khối lệnh', render_section(F[find('Quy ước')])),
    ])
    lessons['giaodien'] = {'title': 'Mở đầu · Làm quen giao diện và cách đọc khối lệnh', 'sub': 'Bốn vùng của Scratch và cách đọc khối lệnh trong sách', 'html': apply_fixes(t2)}
    # ---- Chương và phụ lục
    order = []
    for k, i in enumerate(H1):
        end = H1[k + 1] - 1 if k + 1 < len(H1) else len(bl)
        # lùi qua Para "CHƯƠNG NN / …" nằm ngay trước Header kế tiếp
        j = H1[k + 1] if k + 1 < len(H1) else len(bl)
        if j < len(bl) and bl[j - 1]['t'] == 'Para' and txt(bl[j - 1]['c']).startswith('CHƯƠNG'): j -= 1
        title = txt(bl[i]['c'][2])
        body = bl[i + 1:j]
        if i >= first_ch and bl[i - 1]['t'] == 'Para' and txt(bl[i - 1]['c']).startswith('CHƯƠNG'):
            m = re.match(r'CHƯƠNG (\d+)\s*/\s*(.*)', txt(bl[i - 1]['c']))
            n = int(m.group(1)); tag = m.group(2).strip()
            lessons['c%d' % n] = chapter((n, title, tag), body)
        elif title.startswith('PHỤ LỤC'):
            letter = title.split()[2].lower()
            if letter in ('b', 'c'): continue        # phiếu photocopy và thẻ thử thách: không đưa vào phần mềm
            name = title.split('·', 1)[1].strip()
            lessons['p' + letter] = appendix(letter.upper(), name, body)
    check_fixes()
    return lessons

def appendix(letter, name, body):
    parts = []
    for title, bb in sections(body):
        if title is None: parts.append(render_section(bb)); continue
        m = re.match(r'^(\d+)\.\s*(.*)$', title)
        parts.append(card(m.group(1) if m else '•', E(m.group(2) if m else title), render_section(bb)))
    return {'title': 'Phụ lục %s · %s' % (letter, name), 'sub': name, 'html': apply_fixes('\n'.join(parts))}

PARTS = [
    ('Mở đầu', [('tongquan', 'Lời gửi tới người đọc'), ('giaodien', 'Làm quen giao diện và cách đọc khối lệnh')]),
    ('Phần I · Học cách nghĩ', [('c1', None), ('c2', None), ('c3', None), ('c4', None)]),
    ('Phần II · Dùng Scratch để kiểm chứng', [('c5', None), ('c6', None), ('c7', None), ('c8', None), ('c9', None), ('c10', None)]),
    ('Phần III · Tạo sản phẩm có ích', [('c11', None), ('c12', None), ('c13', None), ('c14', None)]),
    ('Phần IV · Tư duy độc lập và trách nhiệm số', [('c15', None), ('c16', None)]),
    ('Phụ lục', [('pa', None), ('pd', None), ('pe', None), ('pf', None), ('pg', None)]),
]

def toc(L):
    out = []
    for gt, items in PARTS:
        rows = []
        for key, name in items:
            t = L[key]['title']
            m = re.match(r'^(Chương \d+|Phụ lục [A-G])\s*·\s*(.*)$', t)
            label, title = (m.group(1), m.group(2)) if m else ('Mở đầu', name or t)
            rows.append({'key': key, 'label': label, 'title': title, 'ready': True})
        out.append({'t': gt, 'items': rows})
    return out
