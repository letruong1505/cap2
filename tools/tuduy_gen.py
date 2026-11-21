"""Bộ dựng nhanh bài học Python 12–18 (Chương 4 trở đi): cùng khung 8 mục + giải nghĩa câu lệnh. Mọi kết quả chạy thật."""
import os, subprocess, sys, tempfile
from tuduy_py3 import *
from tuduy_py3 import cmp_fig, grid_fig, C


def _exec(src, stdin='', files=None):
    d = tempfile.mkdtemp()
    for n, c in (files or {}).items(): open(os.path.join(d, n), 'w', encoding='utf-8').write(c)
    return subprocess.run([sys.executable, '-I', '-c', src], input=stdin, capture_output=True, text=True, cwd=d, timeout=30)


def OUT(src, stdin='', files=None):
    r = _exec(src, stdin, files); assert r.returncode == 0, r.stderr + '\n' + src
    return r.stdout.rstrip('\n')


def R2(src, stdin='', files=None, show_in=True):
    s = code(src, OUT(src, stdin, files))
    if stdin and show_in: s = s.replace('<div class="code-out-l">', '<div class="code-out-l">Nhập vào: %s · ' % E(' ⏎ '.join(stdin.strip('\n').split('\n'))) if False else '<div class="code-out-l">', 1)
    return s


def RI(src, stdin):
    """Chạy có nhập từ bàn phím: hiển thị dữ liệu nhập và kết quả."""
    return code(src, OUT(src, stdin)) .replace('<div class="code-out-l">Kết quả khi chạy</div>', '<div class="code-out-l">Em gõ vào (mỗi dòng nhấn Enter): %s</div><div class="code-out-l">Kết quả khi chạy</div>' % E('  |  '.join(stdin.strip('\n').split('\n'))), 1)


def E2(src, stdin='', files=None):
    r = _exec(src, stdin, files); assert r.returncode != 0, src
    return code(src, r.stderr.strip().split('\n')[-1])


def W(intro, src, kind='R', stdin='', files=None):
    return intro + (R2(src, stdin, files) if kind == 'R' else E2(src, stdin, files))


def A(intro, src, stdin='', kind='R', files=None):
    if stdin and kind == 'R': return intro + RI(src, stdin)
    return W(intro, src, kind, stdin, files)


def fc(title, cols, cap, h=232): return fig(cmp_fig(title, cols, h), cap)
def fg(title, head, rows, colw, cap, hl=None): return fig(grid_fig(title, head, rows, colw, hl=hl), cap)
def ff(labels, title, cap=None):
    f = flowrow(labels, title, colors=(['#e6f1fb'] * 2 + ['#fff4d6'] * 2 + ['#e5f5ea'] * 4)[:len(labels)]); return f
def fp(src, pick, caps, maxn=8, stdin=''): return ptrace(src, stdin=stdin, pick=pick, maxn=maxn, captions=caps)


def fout(title, text, cap, w=400):
    L = text.split('\n'); h = 60 + len(L) * 22
    s = ARR + txt(350, 24, title, '#17406b', 17, bold=True) + box(350 - w / 2, 40, w, h - 50, '#fff', '#6b7785', [], 14)
    for i, l in enumerate(L): s += mono(350 - w / 2 + 16, 68 + i * 22, l, '#1c2733', 13)
    return fig(svg(700, h, s, title), cap)


def loop_fig(title, cond, body, after='phần còn lại của chương trình', cap=''):
    s = ARR + txt(350, 22, title, '#17406b', 17, bold=True)
    s += '<polygon points="170,62 280,98 170,134 60,98" fill="#fff4d6" stroke="#d9822b" stroke-width="2"/>' + txt(170, 94, cond, '#17406b', 14, bold=True) + txt(170, 112, 'còn đúng?', '#5b6773', 12)
    s += arr(282, 98, 372, 98, '#2a8a4a') + txt(326, 88, 'đúng', '#2a8a4a', 13, bold=True) + box(374, 68, 250, 60, '#e5f5ea', '#2a8a4a', body, 14, bold=True)
    s += '<path d="M500,68 L500,52 L170,52 L170,60" fill="none" stroke="#6b7785" stroke-width="2.5" marker-end="url(#ah)"/>' + txt(335, 44, 'xong thân vòng lặp → quay lại kiểm tra', '#5b6773', 12)
    s += arr(170, 136, 170, 192, '#c0392b') + txt(186, 170, 'sai → thoát ra', '#c0392b', 13, 'start', True) + box(60, 194, 220, 38, '#f3f4f6', '#9db4c9', [after], 13)
    return fig(svg(700, 246, s, title), cap)


def trace_fig(title, head, rows, cap, hl=None, w=None):
    n = len(head); cw = [int(640 / n)] * n
    return fg(title, head, [[str(c) for c in r] for r in rows], cw, cap, hl)


def LS(title, sub, summ, meaning, usage, think_, apply_, cmdi, cmd, figs, errs, exs, pr):
    return std2(title, sub, summ, meaning, usage, think_, 'Ứng dụng vào Python', ''.join(apply_) if not isinstance(apply_, str) else apply_,
                cmdx(cmdi, cmd), ''.join(figs), errs, exs, pr, '')


def SUM(n, name, nodes, before, after, checks, tabrows, top5, quiz, ptitle, pdesc, psrc, pstdins, pnote, nxt, habits, stars='★★★★', pfiles=None):
    """Bài tóm tắt chương: sơ đồ, bảng nhớ, 5 lỗi, tự đánh giá, dự án (chạy thật), 6 câu tự kiểm tra."""
    mm = ARR + txt(350, 24, 'Sơ đồ tóm tắt Chương %d' % n, '#17406b', 17, bold=True) + box(260, 100, 180, 62, '#fff4d6', '#d9822b', ['Chương %d' % n, name], 15, bold=True)
    pos = [(24, 40), (24, 160), (496, 40), (496, 160)]
    for (x, y), (a, b) in zip(pos, nodes):
        mm += box(x, y, 190, 60, '#e6f1fb', '#1f6fb2', [a, b], 14, bold=True) + arr(x + 192 if x < 270 else x - 2, y + 30, 258 if x < 270 else 442, 130, '#6b7785')
    M1 = fig(svg(700, 250, mm, 'Sơ đồ tóm tắt chương %d' % n), 'Bốn nhánh kiến thức của chương và mối liên hệ giữa chúng.')
    ba = ARR + txt(350, 24, 'Trước và sau Chương %d' % n, '#17406b', 17, bold=True)
    ba += box(14, 44, 330, 150, '#f3f4f6', '#9db4c9', [], 14) + txt(179, 68, 'Trước chương %d' % n, '#5b6773', 15, bold=True)
    for i, l in enumerate(before): ba += txt(30, 104 + i * 28, '• ' + l, '#5b6773', 14, 'start')
    ba += box(356, 44, 330, 150, '#e5f5ea', '#2a8a4a', [], 14) + txt(521, 68, 'Sau chương %d' % n, '#2a8a4a', 15, bold=True)
    for i, l in enumerate(after): ba += txt(372, 104 + i * 28, '✓ ' + l, '#17406b', 14, 'start')
    M2 = fig(svg(700, 212, ba, 'Trước và sau chương %d' % n), 'Em đã tiến thêm một bước rõ rệt so với đầu chương.')
    ck = ARR + txt(350, 24, 'Bảng tự đánh giá: tô màu ô em làm được', '#17406b', 17, bold=True)
    for i, l in enumerate(checks):
        x = 14 + (i % 2) * 345; y = 44 + (i // 2) * 52
        ck += '<rect x="%d" y="%d" width="330" height="42" rx="8" fill="#fff" stroke="#9db4c9"/><rect x="%d" y="%d" width="22" height="22" rx="4" fill="#fff" stroke="#1f6fb2" stroke-width="2"/>' % (x, y, x + 12, y + 10) + txt(x + 46, y + 27, l, '#1c2733', 14, 'start')
    M3 = fig(svg(700, 206, ck, 'Bảng tự đánh giá chương %d' % n), 'Chưa tô được ô nào thì quay lại bài tương ứng, đừng bỏ qua.')
    outs = [OUT(psrc, s, pfiles) for s in pstdins]
    pj = fout('Kết quả dự án (lần chạy đầu)', outs[0], 'Kết quả thật khi chạy chương trình mẫu với dữ liệu nhập thứ nhất.')
    runs = ''.join(('<div class="code-out-l">Lần chạy %d%s</div><pre class="code out">%s</pre>' % (i + 1, (' – em gõ: ' + E('  |  '.join(s.strip('\n').split('\n')))) if s else '', E(o))) for i, (s, o) in enumerate(zip(pstdins, outs)))
    tab = table(['Điều cần nhớ', 'Ví dụ', 'Ý nghĩa'], tabrows)
    t5 = ''.join(err(a, b, c) for a, b, c in top5)
    qh = ''.join('<details class="tans"><summary>Câu %d. %s</summary><p>%s</p></details>' % (i + 1, q, a) for i, (q, a) in enumerate(quiz))
    return {'title': 'Tóm tắt Chương %d · %s' % (n, name), 'sub': 'Hệ thống lại kiến thức, lỗi hay gặp và làm dự án cuối chương.',
        'html': '\n'.join([tsum('Hệ thống lại Chương %d và tự kiểm tra; hoàn thành dự án “%s”' % (n, ptitle), 'Đã học hết các bài của Chương %d' % n, 'Bảng ghi nhớ của em và chương trình dự án chạy đúng'),
            card(1, 'Sơ đồ tóm tắt chương', M1 + M2), card(2, 'Bảng ghi nhớ nhanh', tab), card(3, '5 lỗi hay gặp nhất của chương', t5),
            card('+', 'Em đã làm được gì? (tự đánh giá)', M3),
            card(4, 'Em đã học được thói quen tư duy nào?', think(habits, 'Thói quen của Chương %d' % n)),
            chap('Dự án nhỏ cuối chương'),
            '<section class="tcard tprac"><h4><span class="tn">DA</span>Dự án: %s <span class="lvl">%s</span></h4><p>%s</p><details class="tans"><summary>Xem bài mẫu và kết quả chạy</summary>%s%s%s<p>%s</p></details></section>' % (ptitle, stars, pdesc, code('# Dự án chương %d: %s\n' % (n, ptitle) + psrc), runs, pj, pnote),
            chap('Tự kiểm tra (6 câu)'), '<section class="tcard">%s</section>' % qh,
            card(5, 'Chương sau học gì?', li(nxt))])}


def FB(name, content):
    """Khối hiển thị nội dung một tệp có sẵn."""
    return '<div class="code-out-l">Tệp %s có sẵn:</div><pre class="code out">%s</pre>' % (E(name), E(content.rstrip('\n')))


def RF(intro, src, files, stdin='', kind='R'):
    """Chạy đoạn code có tệp dữ liệu sẵn; hiển thị tệp, code và kết quả."""
    fb = ''.join(FB(n, c) for n, c in files.items())
    return intro + fb + (R2(src, stdin, files) if kind == 'R' else E2(src, stdin, files))


def fpd(src, pick, caps, files=None, maxn=8):
    """ptrace trong một thư mục tạm có sẵn tệp."""
    d = tempfile.mkdtemp()
    for n, c in (files or {}).items(): open(os.path.join(d, n), 'w', encoding='utf-8').write(c)
    old = os.getcwd(); os.chdir(d)
    try: return ptrace(src, pick=pick, maxn=maxn, captions=caps)
    finally: os.chdir(old)
