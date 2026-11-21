"""Giáo trình Python 12–18 (bản mở rộng, từng chương): Bài 0 giới thiệu và Chương 1. Mọi kết quả chạy, thông báo lỗi lấy từ lần chạy thật.
Khung mỗi bài: 8 mục + mục "Giải nghĩa từng phần của câu lệnh" (mỗi phần là gì, nếu thiếu hoặc sai thì sao, kèm kết quả chạy thật)."""
import os, subprocess, sys, tempfile
import tuduy_lib
from tuduy_lib import *
lvl_prac = tuduy_lib.prac
from tuduy_py import R, ERR, runerr

def tb(src, name='bai1.py'):
    """Chạy tệp thật và trả về toàn bộ thông báo lỗi (Traceback) như Python in ra."""
    d = tempfile.mkdtemp()
    p = os.path.join(d, name); open(p, 'w', encoding='utf-8').write(src.strip('\n') + '\n')
    r = subprocess.run([sys.executable, '-I', name], cwd=d, capture_output=True, text=True, timeout=10)
    assert r.returncode != 0, src
    return r.stderr.strip().replace(p, name)
def TB(src, name='bai1.py'): return code(src, tb(src, name))

def lesson(title, sub, *parts): return {'title': title, 'sub': sub, 'html': '\n'.join(parts)}
def prac(n, title, task, data, ans):
    s = '<section class="tcard tprac"><h4><span class="tn">%s</span>Thực hành: %s</h4><p>%s</p>' % (n, title, task)
    if data: s += data
    return s + '<details class="tans"><summary>Xem đáp án</summary>%s</details></section>' % ans

def table(head, rows):
    return '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (''.join('<th>%s</th>' % h for h in head), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows))
def cmdx(intro, rows):
    """Bảng giải nghĩa: phần của câu lệnh | ý nghĩa | nếu thiếu/sai thì sao (kèm kết quả thật)."""
    return '<p>%s</p>' % intro + table(['Phần của lệnh', 'Ý nghĩa', 'Nếu thiếu hoặc viết sai thì sao?'], rows)

def std2(title, sub, summary, meaning, usage, thinking, apply_title, apply_html, cmd_html, figs, errors, examples, practice, last=''):
    assert len(practice) == 5, title
    parts = [tsum(*summary),
        card(1, 'Ý nghĩa của bài học', li(meaning)),
        card(2, 'Dùng bài học này như thế nào', usage),
        card(3, 'Tư duy bài học mang đến', thinking),
        card(4, apply_title, apply_html),
        card(5, 'Giải nghĩa từng phần của câu lệnh', cmd_html),
        card(6, 'Hình minh họa từng bước', figs),
        card(7, 'Lỗi sai hay gặp', ''.join(errors)),
        card(8, 'Ví dụ minh họa', ''.join(examples)),
        chap('Bài thực hành · 5 mức tăng dần để nâng cấp tư duy')]
    parts += [lvl_prac(i, t, a, d) for i, (t, a, d) in enumerate(practice)]
    if last: parts.append(last)
    return {'title': title, 'sub': sub, 'html': '\n'.join(parts)}

# ---------------------------------------------------------------- hình dùng chung
def box(x, y, w, h, fill, stroke, lines, sz=15, col='#1c2733', bold=False):
    s = '<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, w, h, fill, stroke)
    n = len(lines)
    for i, t in enumerate(lines):
        s += '<text x="%s" y="%s" text-anchor="middle" font-size="%d" fill="%s"%s>%s</text>' % (x + w / 2, y + h / 2 + 5 + (i - (n - 1) / 2) * (sz + 5), sz, col, ' font-weight="700"' if bold and i == 0 else '', E(t))
    return s
def mono(x, y, t, col='#17406b', sz=20, anchor='start', bold=False):
    """Chữ đơn cách: mỗi ký tự đặt vào một ô cố định nên khung vẽ quanh luôn khớp trên mọi máy và mọi phông."""
    cw = 0.6 * sz; n = len(t)
    x0 = x if anchor == 'start' else (x - n * cw / 2 if anchor == 'middle' else x - n * cw)
    out = ''
    for i, ch in enumerate(t):
        if ch == ' ': continue
        out += '<text x="%.1f" y="%s" text-anchor="middle" fill="%s" font-size="%d" font-family="Consolas,Menlo,monospace"%s>%s</text>' % (x0 + (i + 0.5) * cw, y, col, sz, ' font-weight="700"' if bold else '', E(ch))
    return '<g>%s</g>' % out
def txt(x, y, t, col='#1c2733', sz=15, anchor='middle', bold=False):
    return '<text x="%s" y="%s" text-anchor="%s" fill="%s" font-size="%d"%s>%s</text>' % (x, y, anchor, col, sz, ' font-weight="700"' if bold else '', E(t))
ARR = '<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#6b7785"/></marker></defs>'
def arr(x1, y1, x2, y2, col='#6b7785'): return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2.5" marker-end="url(#ah)"/>' % (x1, y1, x2, y2, col)

def build():
    P = {}

    # ======================================================= BÀI 0
    roadmap = ARR + txt(350, 24, 'Lộ trình 8 chương – mỗi chương một thói quen tư duy', '#17406b', 17, bold=True)
    chs = [('1', 'Bắt đầu', 'làm đúng điều bảo'), ('2', 'Biến, số, chuỗi', 'gọi tên dữ liệu'), ('3', 'Rẽ nhánh', 'ra quyết định'), ('4', 'Lặp', 'việc lớn thành việc nhỏ'),
           ('5', 'Dữ liệu', 'sắp xếp cho gọn'), ('6', 'Hàm', 'đặt tên cho việc'), ('7', 'Tệp', 'dữ liệu không mất'), ('8', 'Đối tượng', 'mô hình thế giới thật')]
    cols = ['#e6f1fb', '#e5f5ea', '#fff4d6', '#fdf0e1', '#f1e8fb', '#e6f1fb', '#e5f5ea', '#fdecea']
    for i, (n, t, s) in enumerate(chs):
        x = 14 + (i % 4) * 171; y = 44 + (i // 4) * 120
        roadmap += box(x, y, 160, 100, cols[i], '#1f6fb2', ['Chương ' + n, t, s], 14, bold=True)
    roadmap += txt(350, 288, '→ Cuối mỗi chương có 1 bài tóm tắt và 1 dự án nhỏ', '#d9822b', 15, bold=True)
    F0a = fig(svg(700, 300, roadmap, 'Lộ trình 8 chương'), 'Lộ trình khóa Python: đi từ in ra lời chào đến mô hình hóa một thư viện sách.')

    cmp_ = ARR + txt(350, 24, 'Cùng một việc: in lời chào ra màn hình', '#17406b', 17, bold=True)
    cmp_ += box(14, 44, 216, 190, '#fff4d6', '#d9822b', [], 14) + txt(122, 68, 'Scratch', '#d9822b', 16, bold=True)
    cmp_ += '<rect x="34" y="90" width="176" height="34" rx="6" fill="#ffbf00"/>' + txt(122, 112, 'khi bấm cờ xanh', '#1c2733', 14) + '<rect x="34" y="124" width="176" height="34" rx="6" fill="#9966ff"/>' + txt(122, 146, 'nói Xin chào!', '#fff', 14) + txt(122, 190, '2 khối, kéo thả', '#5b6773', 14)
    cmp_ += box(242, 44, 216, 190, '#e5f5ea', '#2a8a4a', [], 14) + txt(350, 68, 'Python', '#2a8a4a', 16, bold=True) + mono(262, 130, 'print("Xin chào!")', '#17406b', 17) + txt(350, 190, '1 dòng, gõ chữ', '#5b6773', 14) + txt(350, 212, 'gần với tiếng Anh', '#5b6773', 14)
    cmp_ += box(470, 44, 216, 190, '#fdecea', '#c0392b', [], 14) + txt(578, 68, 'Ngôn ngữ khác (ví dụ C++)', '#c0392b', 14, bold=True)
    for i, l in enumerate(['#include <iostream>', 'int main() {', '  std::cout << "Xin chào!";', '  return 0;', '}']): cmp_ += mono(482, 100 + i * 24, l, '#7b1d12', 12)
    cmp_ += txt(578, 224, '5 dòng, nhiều ký hiệu phải nhớ', '#5b6773', 14)
    F0b = fig(svg(700, 250, cmp_, 'So sánh in lời chào'), 'Python ngắn gọn, đọc gần như tiếng Anh nên người mới học tập trung vào cách nghĩ thay vì cách viết.')

    uses = txt(350, 24, 'Python được dùng ở đâu?', '#17406b', 17, bold=True)
    items = [('Trí tuệ nhân tạo', 'và phân tích dữ liệu'), ('Trang web', 'và ứng dụng'), ('Tự động hóa', 'việc lặp lại'), ('Trò chơi', 'và mô phỏng'), ('Khoa học', 'xử lý số liệu thí nghiệm'), ('Robot', 'và thiết bị thông minh')]
    for i, (a, b) in enumerate(items):
        x = 14 + (i % 3) * 229; y = 44 + (i // 3) * 92
        uses += box(x, y, 218, 78, ['#e6f1fb', '#e5f5ea', '#fff4d6'][i % 3], '#1f6fb2', [a, b], 15, bold=True)
    F0c = fig(svg(700, 232, uses, 'Python dùng ở đâu'), 'Một ngôn ngữ, nhiều lĩnh vực: học một lần, dùng được cho nhiều mục đích sau này.')

    flow = flowrow(['Ý nghĩa', 'Dùng thế|nào', 'Tư duy', 'Ứng dụng|Python', 'Giải nghĩa|câu lệnh', 'Hình từng|bước', 'Lỗi hay|gặp', 'Ví dụ +|5 bài tập'], 'Mỗi bài học đi qua 8 chặng', w=900)
    F0d = flow

    p0 = 'print(2 + 3 * 4)'
    P['tongquan'] = lesson('Mở đầu · Giới thiệu khóa học và vì sao chọn Python', 'Lộ trình 12–18 tuổi · dùng Python.',
        tsum('Biết khóa học dạy gì, học thế nào và vì sao Python là ngôn ngữ đầu tiên hợp với lứa 12–18', 'Máy tính (chưa cần cài gì ở bài này); giấy bút để ghi câu trả lời cho phần thực hành', 'Một bản kế hoạch học của riêng em và dự đoán đầu tiên cho một đoạn code'),
        card(1, 'Khóa học này dạy gì?', li(['Em sẽ học Python <b>vừa đủ</b> để tự giải bài toán thật: tính toán, ra quyết định, lặp việc, lưu dữ liệu, tổ chức chương trình.', 'Nhưng điều khóa rèn nhất là <b>cách nghĩ</b>: chia bài toán nhỏ, dự đoán trước khi chạy, kiểm tra bằng chứng và đi ngược từ kết quả về nguyên nhân.', 'Học hết khóa em sẽ tự viết được những ứng dụng nhỏ: tính tiền, trò chơi đoán số, sổ điểm, sổ chi tiêu, quản lý thư viện mini.']) + F0a),
        card(2, 'Vì sao chọn Python?', li(['<b>Dễ đọc:</b> cú pháp gần tiếng Anh, ít ký hiệu phải nhớ, nên em mất ít thời gian “học cách viết” và nhiều thời gian “học cách nghĩ”.', '<b>Miễn phí và chạy trên mọi máy:</b> Windows, macOS, Linux; còn chạy được ngay trên trình duyệt khi chưa cài.', '<b>Dùng được lâu dài:</b> từ bài tập ở trường đến phân tích dữ liệu, trí tuệ nhân tạo, tự động hóa công việc.', '<b>Báo lỗi dễ hiểu:</b> Python nói rõ lỗi ở dòng nào, loại gì – rất hợp để rèn thói quen đọc lỗi và sửa lỗi.', '<b>Nối tiếp Scratch:</b> nếu em từng kéo thả khối lệnh, mỗi khối nay trở thành một dòng chữ; tư duy vẫn là một.']) + F0b + F0c),
        card(3, 'Học như thế nào?', li(['Mỗi bài có <b>8 mục</b> và một mục <b>giải nghĩa từng phần của câu lệnh</b>: lệnh đó là gì, <i>nếu thiếu hoặc viết sai thì sao</i> (kèm kết quả chạy thật).', 'Mỗi bài có <b>10–12 hình</b> và <b>5 bài thực hành tăng dần</b> có lời giải; hãy tự làm trước rồi mới xem lời giải.', 'Cuối mỗi chương có <b>bài tóm tắt</b> và <b>dự án nhỏ</b> để ghép các lệnh vừa học.', 'Mọi kết quả trong sách đều <b>chạy thật</b>; em nên gõ lại và chạy trên máy mình, đừng chỉ đọc.']) + F0d),
        card(4, 'Ba thói quen của một người lập trình giỏi', think(['<b>Dự đoán trước, chạy sau:</b> đoán kết quả rồi mới chạy; nếu lệch, hỏi “vì sao khác?”.', '<b>Kiểm chứng:</b> chạy đúng một lần chưa chắc đúng mọi trường hợp; thử thêm trường hợp biên.', '<b>Nghĩ ngược:</b> bắt đầu từ kết quả mong muốn rồi lần ngược về các bước cần làm.'], 'Khai mở tư duy')),
        card(5, 'Lộ trình và cách tính thời gian', li(['Khoảng <b>2 bài mỗi tuần</b>, mỗi bài 45–60 phút, hết khóa trong khoảng 4–5 tháng; em có thể học nhanh hơn hoặc chậm hơn tùy ý.', 'Bài <b>Mở đầu</b>, <b>Bài 1.1 (Cài đặt)</b> và <b>Bài 1.2 (Chương trình đầu tiên)</b> xem miễn phí để em thử trước khi mua.', 'Nên học theo thứ tự: mỗi chương dùng lại những gì chương trước đã học.'])),
        prac(4, 'Đoán trước khi chạy', 'Em chưa cần cài Python. Hãy <b>đoán</b> đoạn code sau in ra gì, viết đáp án ra giấy:' + code(p0) + 'Sau đó viết thêm 2 mục tiêu em muốn đạt khi học xong khóa này (ví dụ: làm trò chơi, tự động hóa việc nhà).', None,
             '<p>Kết quả là <b>%s</b> vì Python nhân trước, cộng sau (2 + 12). Nếu em đoán 20, em đã cộng trước – đây chính là lúc nên hỏi “vì sao khác?” và học lại thứ tự phép tính.</p>' % run(p0) + R(p0)))

    # ======================================================= BÀI 1.1  (bổ sung phần "Python là gì" vào bài Cài đặt có sẵn)
    P['_pre_caidat'] = (chap('Python là gì?') + li(['<b>Lập trình</b> là viết cho máy tính một dãy lệnh rõ ràng để nó làm việc thay em.', '<b>Python</b> là một ngôn ngữ lập trình: bộ từ vựng và quy tắc để em nói chuyện với máy.', 'Máy chỉ làm <b>đúng điều em viết</b>, không đoán ý. Viết đúng thì chạy đúng, viết sai thì máy báo lỗi.']) +
        fig(svg(700, 200, ARR + box(14, 50, 150, 90, '#e6f1fb', '#1f6fb2', ['Em viết', 'chương trình', '(file .py)'], 15, bold=True) + arr(166, 95, 214, 95) +
                box(216, 50, 150, 90, '#fff4d6', '#d9822b', ['Python', 'đọc từng dòng', 'và thực hiện'], 15, bold=True) + arr(368, 95, 416, 95) +
                box(418, 50, 150, 90, '#e5f5ea', '#2a8a4a', ['Máy tính', 'làm việc'], 15, bold=True) + arr(570, 95, 618, 95) +
                box(620, 50, 70, 90, '#f3f4f6', '#9db4c9', ['Kết', 'quả'], 15, bold=True) + txt(350, 180, 'Em → viết lệnh · Python → dịch cho máy · Máy → làm việc và trả kết quả', '#5b6773', 14), 'Vai trò của Python'),
            'Python là người phiên dịch giữa em và máy tính.'))

    # ======================================================= BÀI 1.2
    h1 = 'print("Xin chào")\nprint("Mình học Python")\nprint("Bắt đầu thôi!")'
    h2 = 'print("Mình là Lan")\nprint("Mình 13 tuổi")\nprint(2 + 3)\nprint("2 + 3")\nprint("Ha", "ha", "ha")\nprint("Dòng 1\\nDòng 2")\nprint()\nprint("Hết")'
    anat = ARR + mono(60, 80, 'print("Xin chào")', '#17406b', 34)
    anat += '<rect x="58" y="50" width="106" height="40" rx="6" fill="none" stroke="#d9822b" stroke-width="2.5"/><rect x="162" y="50" width="23" height="40" rx="6" fill="none" stroke="#1f6fb2" stroke-width="2.5"/><rect x="185" y="50" width="204" height="40" rx="6" fill="none" stroke="#2a8a4a" stroke-width="2.5"/><rect x="389" y="50" width="23" height="40" rx="6" fill="none" stroke="#1f6fb2" stroke-width="2.5"/>'
    anat += arr(111, 150, 111, 96, '#d9822b') + txt(111, 172, '① tên lệnh', '#d9822b', 15, bold=True) + txt(111, 192, 'print = “in ra”', '#5b6773', 13)
    anat += arr(173, 128, 173, 96, '#1f6fb2') + txt(182, 146, '② ngoặc mở', '#1f6fb2', 13, 'start', True)
    anat += arr(287, 150, 287, 96, '#2a8a4a') + txt(287, 172, '③ chữ cần in', '#2a8a4a', 15, bold=True) + txt(287, 192, 'nằm trong dấu nháy', '#5b6773', 13)
    anat += arr(400, 128, 400, 96, '#1f6fb2') + txt(470, 146, '④ ngoặc đóng', '#1f6fb2', 14, bold=True)
    G1 = fig(svg(700, 215, anat, 'Giải phẫu lệnh print'), '4 phần của một câu lệnh print: thiếu hoặc sai một phần là Python báo lỗi.')
    qv = ARR + txt(350, 26, 'Có dấu nháy hay không – khác nhau hoàn toàn', '#17406b', 17, bold=True)
    qv += box(14, 46, 330, 130, '#e5f5ea', '#2a8a4a', [], 14) + mono(30, 86, 'print("2 + 3")', '#17406b', 22) + txt(179, 114, 'Có dấu nháy → là CHỮ', '#2a8a4a', 15, bold=True) + arr(179, 122, 179, 146, '#2a8a4a') + mono(179, 170, '2 + 3', '#2a8a4a', 22, 'middle', True)
    qv += box(356, 46, 330, 130, '#e6f1fb', '#1f6fb2', [], 14) + mono(372, 86, 'print(2 + 3)', '#17406b', 22) + txt(521, 114, 'Không nháy → là PHÉP TÍNH', '#1f6fb2', 15, bold=True) + arr(521, 122, 521, 146, '#1f6fb2') + mono(521, 168, '5', '#1f6fb2', 22, 'middle', True)
    G2 = fig(svg(700, 196, qv, 'Chữ và phép tính'), 'Dấu nháy cho Python biết “đây là chữ, cứ in nguyên văn”. Không có dấu nháy, Python hiểu là phép tính hoặc tên.')
    ide = ARR + box(14, 20, 330, 190, '#fff', '#6b7785', [], 14) + txt(179, 44, 'Cửa sổ soạn code (bai1.py)', '#5b6773', 14, bold=True)
    for i, l in enumerate(['print("Xin chào")', 'print("Mình học Python")']): ide += mono(30, 84 + i * 30, l, '#17406b', 16)
    ide += '<rect x="26" y="150" width="200" height="34" rx="6" fill="#ffe9a8" stroke="#d9a400" stroke-width="2"/>' + txt(126, 172, 'Run → Run Module (F5)', '#1c2733', 14, bold=True)
    ide += arr(346, 115, 396, 115, '#d9822b') + box(398, 20, 288, 190, '#f6f8fb', '#6b7785', [], 14) + txt(542, 44, 'Cửa sổ Shell (kết quả)', '#5b6773', 14, bold=True) + mono(414, 84, 'Xin chào', '#1c2733', 16) + mono(414, 114, 'Mình học Python', '#1c2733', 16)
    G3 = fig(svg(700, 230, ide, 'Viết ở một cửa sổ, kết quả ở cửa sổ kia'), 'Em viết lệnh ở cửa sổ soạn code, bấm F5, kết quả hiện ở cửa sổ Shell.')
    sp = ARR + txt(350, 26, 'print("Ha", "ha", "ha") – dấu phẩy tự thêm dấu cách', '#17406b', 17, bold=True)
    for i, w in enumerate(['"Ha"', '"ha"', '"ha"']): sp += box(30 + i * 110, 60, 90, 44, '#e6f1fb', '#1f6fb2', [w], 18, bold=True) + (txt(125 + i * 110, 88, ',', '#d9822b', 22, bold=True) if i < 2 else '')
    sp += arr(190, 112, 190, 148) + box(30, 150, 320, 44, '#e5f5ea', '#2a8a4a', ['Ha ha ha'], 20, bold=True) + txt(520, 90, 'dấu phẩy: nối nhiều thứ,', '#5b6773', 15) + txt(520, 112, 'in cách nhau một dấu cách', '#5b6773', 15)
    G4 = fig(svg(700, 210, sp, 'Dấu phẩy trong print'), 'Có thể đặt nhiều thứ trong một lệnh print, cách nhau bởi dấu phẩy.')
    err1 = ARR + txt(350, 26, 'Đọc một thông báo lỗi: print("Xin chào)', '#17406b', 17, bold=True)
    err1 += box(14, 44, 672, 60, '#fdecea', '#c0392b', [], 14) + mono(30, 82, 'SyntaxError: unterminated string literal (detected at line 1)', '#7b1d12', 16)
    err1 += arr(110, 150, 110, 112, '#c0392b') + txt(110, 172, 'Loại lỗi: SyntaxError', '#c0392b', 14, bold=True) + txt(110, 192, '= viết sai cú pháp', '#5b6773', 13)
    err1 += arr(420, 150, 420, 112, '#d9822b') + txt(450, 172, 'Ý nghĩa: “chuỗi chữ chưa đóng dấu nháy”', '#d9822b', 14, bold=True) + txt(450, 192, '→ thiếu dấu " ở cuối', '#5b6773', 13)
    G5 = fig(svg(700, 210, err1, 'Đọc thông báo lỗi'), 'Thông báo lỗi nói gần như đúng điều cần sửa: hãy đọc nó trước khi làm gì khác.')
    flowx = flowrow(['Gõ lệnh', 'Lưu tệp|(Ctrl+S)', 'Bấm F5', 'Xem kết quả|ở Shell', 'Sai? Đọc lỗi|rồi sửa'], 'Vòng làm việc quen thuộc', colors=['#e6f1fb', '#e6f1fb', '#fff4d6', '#e5f5ea', '#fdecea'])
    G6 = flowx
    od = ARR + txt(350, 26, 'Đổi thứ tự dòng thì kết quả đổi theo', '#17406b', 17, bold=True)
    for k, (title_, ls_, outs, col) in enumerate([('Thứ tự A', ['print("Chào")', 'print("Tạm biệt")'], ['Chào', 'Tạm biệt'], '#e5f5ea'), ('Thứ tự B (đổi chỗ)', ['print("Tạm biệt")', 'print("Chào")'], ['Tạm biệt', 'Chào'], '#fdf0e1')]):
        x = 14 + k * 345
        od += box(x, 44, 330, 170, col, '#6b7785', [], 14) + txt(x + 165, 68, title_, '#17406b', 15, bold=True)
        for i, l in enumerate(ls_): od += mono(x + 20, 100 + i * 26, l, '#17406b', 16)
        od += arr(x + 165, 150, x + 165, 172) + txt(x + 165, 198, ' → '.join(outs), '#2a8a4a', 15, bold=True)
    G7 = fig(svg(700, 232, od, 'Đổi thứ tự dòng'), 'Máy không đảo thứ tự: dòng nào viết trước, chạy trước.')
    nl = ARR + txt(350, 26, r'Ký hiệu \n = xuống dòng', '#17406b', 17, bold=True) + mono(30, 76, 'print("Dòng 1\\nDòng 2")', '#17406b', 22)
    nl += arr(180, 92, 180, 128) + box(30, 130, 300, 70, '#e5f5ea', '#2a8a4a', ['Dòng 1', 'Dòng 2'], 18, bold=True) + txt(520, 120, r'\n là HAI ký tự khi gõ,', '#5b6773', 15) + txt(520, 142, 'nhưng máy hiểu là MỘT lần xuống dòng', '#5b6773', 15) + txt(520, 176, r'Gõ /n hay n\ thì không được!', '#c0392b', 15, bold=True)
    G8 = fig(svg(700, 218, nl, 'Ký hiệu xuống dòng'), 'Dấu gạch chéo ngược <b>\\</b> kết hợp với n thành ký hiệu xuống dòng.')
    cmd12 = cmdx('Phân tích câu lệnh <code>print("Xin chào")</code> từng phần. Phần “Nếu thiếu” đều là kết quả chạy thật (tùy phiên bản Python, câu chữ lỗi có thể hơi khác).', [
        ['<code>print</code>', 'Tên lệnh: bảo Python <b>in ra màn hình</b> thứ nằm trong ngoặc.', 'Viết <code>Print</code> (hoa) – Python phân biệt hoa thường:' + ERR('Print("Xin chào")')],
        ['<code>( )</code> – cặp ngoặc tròn', 'Bao quanh thứ cần in. Ngoặc mở và ngoặc đóng phải đi đôi.', 'Quên ngoặc đóng:' + ERR('print("Xin chào"')],
        ['<code>" "</code> – cặp dấu nháy', 'Báo cho Python biết bên trong là <b>chữ</b> (chuỗi), in nguyên văn. Dùng dấu nháy đơn <code>\' \'</code> cũng được.', 'Bỏ dấu nháy, Python tưởng là một cái tên:' + ERR('print(Xin chào)')],
        ['<code>Xin chào</code> – nội dung', 'Phần chữ em muốn hiện ra, gõ tiếng Việt có dấu thoải mái.', 'Quên nháy ở một đầu:' + ERR('print("Xin chào)')],
        ['<code>,</code> – dấu phẩy giữa các phần', 'In nhiều thứ trong một lệnh, tự chèn một dấu cách.', 'Viết thiếu dấu phẩy giữa hai chữ:' + ERR('print("Ha" "ha" 3)')],
        ['<code>\\n</code> trong chữ', 'Ký hiệu “xuống dòng”: máy hiểu là sang dòng mới.', 'Nếu viết <code>/n</code> thay vì <code>\\n</code>, máy in nguyên <code>/n</code>:' + R('print("Dòng 1/nDòng 2")')],
        ['<code>print()</code> để trống', 'In một <b>dòng trống</b> để ngăn cách.', 'Không có lỗi; chỉ là nếu bỏ lệnh này thì các dòng dính liền nhau.']])
    P['c1b2'] = std2('Bài 1.2 · Chương trình đầu tiên: Hello World và cấu trúc chương trình', 'Một dòng lệnh, bốn phần, và cách máy đọc chương trình từ trên xuống.',
        ('Viết và chạy được chương trình có nhiều lệnh print; hiểu từng phần của câu lệnh; biết máy chạy từ trên xuống dưới, từng dòng', 'Python và IDLE đã cài (Bài 1.1); mở sẵn cửa sổ soạn code (File → New File)', 'Một chương trình in ra phần giới thiệu về em, chạy đúng khi bấm F5'),
        ['Lệnh <b>print</b> là cầu nối đầu tiên giữa em và máy: nhờ nó em nhìn thấy máy đang “nghĩ” gì.', 'Chương trình <b>“Hello World”</b> (in lời chào) là truyền thống đầu tiên của mọi người học lập trình ở bất kỳ ngôn ngữ nào.', 'Biết máy đọc <b>từ trên xuống dưới, mỗi lần một dòng</b> là nền tảng để sau này đoán đúng kết quả mọi chương trình.', 'Hiểu từng phần của câu lệnh giúp em <b>tự sửa lỗi</b> thay vì chép và mong may mắn.'],
        ol(['Mở cửa sổ soạn code: <b>File → New File</b>, lưu thành <code>bai1.py</code>.', 'Mỗi lệnh gõ trên <b>một dòng riêng</b>, bắt đầu từ sát lề trái, không thụt dòng.', 'Bấm <b>F5</b>; kết quả hiện ở cửa sổ Shell, theo đúng thứ tự dòng em viết.', 'Có lỗi: đọc dòng cuối của thông báo, đối chiếu với “4 phần của lệnh print” rồi sửa.']),
        think(['<b>Phản biện:</b> em đoán máy in gì trước khi bấm F5. Nếu kết quả khác dự đoán, lỗi ở em (hiểu sai) hay ở code (gõ sai)?', '<b>Nghĩ ngược:</b> muốn màn hình hiện đúng 3 dòng như ý, em phải viết bao nhiêu lệnh print và theo thứ tự nào? Đi từ kết quả muốn có về code.', '<b>Trình tự:</b> máy không bỏ qua, không đảo thứ tự: đổi chỗ hai dòng là kết quả đổi theo.']),
        'Ứng dụng vào Python',
        li(['Cấu trúc chương trình Python đơn giản nhất: <b>một dãy lệnh, mỗi lệnh một dòng, chạy từ trên xuống</b>.']) + R(h1) + note('Ba lệnh, ba dòng kết quả, đúng thứ tự.') + 'Thử thêm các kiểu in khác:' + R(h2) + G1,
        cmd12,
        G2 + G3 + ptrace(h1, pick=[0, 1, 2], captions=['Máy chạy <b>dòng 1</b>: in “Xin chào”.', 'Chạy tiếp <b>dòng 2</b>: in thêm “Mình học Python” ở dòng dưới.', 'Chạy <b>dòng 3</b>: hết chương trình, tổng cộng 3 dòng kết quả.']) + G4 + G5 + G6 + G7 + G8,
        [err('Viết hoa chữ print', 'Python phân biệt chữ hoa và chữ thường:' + ERR('Print("Xin chào")'), 'Luôn viết thường: <code>print</code>.'),
         err('Thiếu hoặc thừa dấu nháy, dấu ngoặc', 'Mỗi dấu mở phải có dấu đóng:' + ERR('print("Xin chào"'), 'Đếm: số ngoặc mở = số ngoặc đóng; dấu nháy luôn đi đôi.'),
         err('Thụt dòng đầu dòng', 'Thêm dấu cách đầu dòng khi chưa cần gây lỗi:' + ERR('print("a")\n  print("b")'), 'Lệnh bình thường bắt đầu sát lề trái.'),
         err('Dùng dấu nháy kiểu “ ” của Word', 'Dấu nháy cong copy từ văn bản không phải dấu nháy của Python:' + ERR('print(“Xin chào”)'), 'Gõ lại bằng phím <code>"</code> trên bàn phím trong trình soạn code.')],
        [eg('Ví dụ 1: thiệp chào bằng chữ', R('print("*" * 20)\nprint("  Chào mừng em!")\nprint("*" * 20)') + note('Phép <code>"*" * 20</code> lặp dấu * 20 lần – sẽ học kỹ ở chương 2.')),
         eg('Ví dụ 2: giới thiệu bản thân', R('print("Tên:", "Lan")\nprint("Lớp:", 8)\nprint("Sở thích:", "vẽ", "và", "lập trình")'))],
        [('Viết chương trình in đúng 3 dòng: “Xin chào”, “Mình là …” (tên của em), “Rất vui được học Python”.', R('print("Xin chào")\nprint("Mình là Lan")\nprint("Rất vui được học Python")'), None),
         ('Đoán rồi chạy: <code>print(10 - 4)</code> và <code>print("10 - 4")</code>. Hai dòng in ra khác nhau thế nào, vì sao?', R('print(10 - 4)\nprint("10 - 4")') + '<p>Không có nháy thì Python tính: 6. Có nháy là chữ: in nguyên “10 - 4”.</p>', None),
         ('Chương trình dưới có 2 lỗi. Tìm và sửa:' + code('Print("Xin chào)\nprint("Python")'), '<p>Lỗi 1: <code>Print</code> viết hoa → <code>print</code>. Lỗi 2: thiếu dấu <code>"</code> đóng sau chữ Xin chào.</p>' + R('print("Xin chào")\nprint("Python")') + note('Mẹo: sửa từng lỗi một rồi chạy lại; Python chỉ báo lỗi đầu tiên nó gặp.'), None),
         ('In hình chữ nhật rỗng 3 dòng bằng dấu * và dấu cách (dòng 1: 8 dấu *, dòng 2: * rồi 6 dấu cách rồi *, dòng 3: 8 dấu *).', R('print("*" * 8)\nprint("*" + " " * 6 + "*")\nprint("*" * 8)') + note('Đếm: dòng giữa có 1 + 6 + 1 = 8 ký tự, cùng độ rộng hai dòng kia ✓.'), None),
         ('<b>Thử thách (nghĩ ngược):</b> muốn màn hình hiện ra đúng như sau, hãy viết code (không được chép tay từng dấu *):' + code('*\n**\n***\n****'), '<p>Nhìn kết quả: dòng i có i dấu *. Chưa có vòng lặp, nên viết 4 lệnh print với <code>"*" * 1</code>, … <code>"*" * 4</code>:</p>' + R('print("*" * 1)\nprint("*" * 2)\nprint("*" * 3)\nprint("*" * 4)') + note('Bài này lặp lại cùng một mẫu – chính là lý do chương 4 dạy vòng lặp.'), None)],
        '')

    # ======================================================= BÀI 1.3
    cm1 = '# Chương trình chào hỏi\nprint("Xin chào")   # in lời chào\n# print("Dòng này bị tắt")\nprint("Tạm biệt")'
    cm2 = '"""\nBài 1.3\nTác giả: Lan\n"""\nprint("Xong")'
    e_syn = 'print("Xin chào"'
    e_name = 'print(ten)'
    e_type = 'print("5" + 3)'
    e_zero = 'print(10 / 0)'
    e_ind = 'print("a")\n  print("b")'
    tbsrc = 'print("Bắt đầu")\nprint(10 / 0)\nprint("Không bao giờ tới đây")'
    tbtxt = tb(tbsrc)
    tba = ARR + txt(350, 26, 'Đọc Traceback từ dưới lên', '#17406b', 17, bold=True)
    L = tbtxt.split('\n')
    tba += box(14, 44, 672, 112, '#f6f8fb', '#9db4c9', [], 14)
    for i, l in enumerate(L[:4]): tba += mono(28, 72 + i * 24, l[:70], '#17406b' if i < 3 else '#7b1d12', 14, bold=(i == 3))
    tba += '<rect x="22" y="130" width="640" height="24" rx="5" fill="#fdecea" fill-opacity=".8" stroke="#c0392b"/>' + mono(28, 148, L[-1][:70], '#7b1d12', 14, bold=True)
    tba += arr(110, 206, 110, 162, '#c0392b') + txt(110, 228, '① Đọc dòng CUỐI trước', '#c0392b', 14, bold=True) + txt(110, 246, 'loại lỗi và lý do', '#5b6773', 13)
    tba += arr(350, 206, 350, 96, '#1f6fb2') + txt(350, 228, '② Tìm số dòng', '#1f6fb2', 14, bold=True) + txt(350, 246, '(line 2)', '#5b6773', 13)
    tba += arr(560, 206, 560, 118, '#2a8a4a') + txt(560, 228, '③ Mở đúng dòng đó', '#2a8a4a', 14, bold=True) + txt(560, 246, 'và sửa', '#5b6773', 13)
    H1 = fig(svg(700, 260, tba, 'Cách đọc Traceback'), 'Python in từ trên xuống nhưng nên đọc từ dưới lên: dòng cuối cho biết lỗi gì, dòng giữa chỉ ra ở đâu.')
    cmt = ARR + txt(350, 26, 'Dòng bắt đầu bằng # bị Python bỏ qua', '#17406b', 17, bold=True)
    lines_ = [('# Chương trình chào hỏi', 'ghi chú', '#6b7785', '#f3f4f6'), ('print("Xin chào")   # in lời chào', 'chạy (phần sau # bỏ qua)', '#17406b', '#e5f5ea'), ('# print("Dòng này bị tắt")', 'bị tắt', '#6b7785', '#f3f4f6'), ('print("Tạm biệt")', 'chạy', '#17406b', '#e5f5ea')]
    for i, (c_, lbl, col, bg) in enumerate(lines_):
        y = 44 + i * 46; cmt += '<rect x="14" y="%d" width="400" height="38" rx="8" fill="%s" stroke="#9db4c9"/>' % (y, bg) + mono(26, y + 26, c_, col, 15) + txt(550, y + 25, lbl, '#2a8a4a' if bg == '#e5f5ea' else '#6b7785', 14, bold=True)
    cmt += txt(350, 244, 'Dùng # để ghi chú và để tạm tắt một dòng khi thử nghiệm', '#d9822b', 15, bold=True)
    H2 = fig(svg(700, 262, cmt, 'Ghi chú và tắt dòng'), 'Ghi chú là lời nhắn cho người đọc; máy không chạy chúng.')
    types = [('SyntaxError', 'Viết sai cú pháp', e_syn), ('NameError', 'Dùng tên chưa có', e_name), ('TypeError', 'Trộn kiểu không hợp', e_type), ('ZeroDivisionError', 'Chia cho 0', e_zero), ('IndentationError', 'Thụt dòng sai', e_ind)]
    tt = txt(350, 24, '5 loại lỗi em sẽ gặp nhiều nhất', '#17406b', 17, bold=True)
    for i, (n, d, s) in enumerate(types):
        y = 40 + i * 44; tt += '<rect x="14" y="%d" width="672" height="38" rx="8" fill="%s" stroke="#9db4c9"/>' % (y, ['#fdecea', '#fff4d6', '#e6f1fb', '#e5f5ea', '#f1e8fb'][i]) + mono(26, y + 25, n, '#7b1d12', 15, bold=True) + txt(260, y + 25, d, '#1c2733', 15, 'start')
    H3 = fig(svg(700, 266, tt, 'Năm loại lỗi thường gặp'), 'Nhận ra tên lỗi giúp em đoán ngay nguyên nhân.')
    pv = ARR + txt(350, 26, 'Lỗi thật có thể nằm ở dòng TRƯỚC dòng được báo', '#17406b', 17, bold=True)
    pv += box(14, 44, 420, 118, '#f6f8fb', '#9db4c9', [], 14)
    pv += '<rect x="22" y="56" width="404" height="26" rx="5" fill="#fdecea" stroke="#c0392b"/><rect x="22" y="86" width="404" height="26" rx="5" fill="#fff4d6" stroke="#d9822b"/>'
    pv += mono(30, 75, '1  print("Xin chào"', '#7b1d12', 16, bold=True) + mono(30, 105, '2  print("Tạm biệt")', '#17406b', 16) + mono(30, 135, '3  print("Hết")', '#17406b', 16)
    pv += txt(492, 76, 'Thủ phạm: thiếu ) ở dòng 1', '#c0392b', 14, 'start', True) + txt(492, 106, 'Python báo lỗi ở dòng 2', '#d9822b', 14, 'start', True) + arr(486, 106, 438, 106, '#d9822b') + arr(486, 76, 438, 76, '#c0392b')
    pv += txt(350, 196, 'Dòng được báo trông đúng? Hãy xem ngay dòng phía trên.', '#d9822b', 15, bold=True)
    H4 = fig(svg(700, 214, pv, 'Lỗi ở dòng trước'), 'Quên đóng ngoặc ở dòng 1 làm Python “hụt hơi” và báo lỗi ở dòng 2.')
    bis = ARR + txt(350, 26, 'Tắt từng dòng để tìm thủ phạm', '#17406b', 17, bold=True)
    for i, (l, on) in enumerate([('print("Bước 1")', True), ('print("Bước 2")', False), ('print(10 / 0)', True), ('print("Bước 4")', True)]):
        y = 44 + i * 40; bis += '<rect x="14" y="%d" width="330" height="34" rx="8" fill="%s" stroke="#9db4c9"/>' % (y, '#e5f5ea' if on else '#f3f4f6') + mono(26, y + 23, l if on else '# ' + l, '#17406b' if on else '#6b7785', 15) + txt(360, y + 23, 'bật' if on else 'tắt thử', '#2a8a4a' if on else '#6b7785', 14, 'start', True)
    bis += txt(450, 112, 'Chạy mà vẫn lỗi ở dòng 3?', '#c0392b', 14, 'start', True) + txt(450, 136, 'Vậy thủ phạm không phải dòng 2.', '#5b6773', 13, 'start')
    H5 = fig(svg(700, 214, bis, 'Tắt từng dòng'), 'Cách “chia để trị”: tắt bớt dòng, chạy lại, thu hẹp dần vùng nghi ngờ.')
    ntr = ARR + txt(350, 26, 'Ba cách viết ghi chú', '#17406b', 17, bold=True)
    for i, (a, b, c_) in enumerate([('# một dòng', 'ghi chú ngắn, hoặc tắt một dòng', '#e6f1fb'), ('lệnh  # sau lệnh', 'giải thích ngay cạnh lệnh', '#e5f5ea'), ('""" nhiều dòng """', 'tên bài, tác giả, mô tả ở đầu tệp', '#fff4d6')]):
        ntr += box(14 + i * 229, 44, 218, 110, c_, '#1f6fb2', [], 14) + mono(123 + i * 229, 84, a, '#17406b', 15, 'middle', True) + txt(123 + i * 229, 120, b, '#5b6773', 13)
    H6 = fig(svg(700, 172, ntr, 'Ba cách ghi chú'), 'Chọn cách ghi chú phù hợp với độ dài điều cần nói.')
    lp = ARR + txt(350, 26, 'Ghi chú tốt và chưa tốt', '#17406b', 17, bold=True)
    lp += box(14, 44, 330, 110, '#fdecea', '#c0392b', [], 14) + txt(179, 68, 'Chưa tốt: chép lại lệnh', '#c0392b', 14, bold=True) + mono(28, 102, '# in ra Xin chào', '#7b1d12', 15) + mono(28, 126, 'print("Xin chào")', '#7b1d12', 15)
    lp += box(356, 44, 330, 110, '#e5f5ea', '#2a8a4a', [], 14) + txt(521, 68, 'Tốt hơn: nói vì sao', '#2a8a4a', 14, bold=True) + mono(370, 102, '# chào để người dùng biết', '#17406b', 15) + mono(370, 126, 'print("Xin chào")', '#17406b', 15)
    H7 = fig(svg(700, 172, lp, 'Ghi chú tốt'), 'Ghi chú nên trả lời “vì sao”, đừng lặp lại điều code đã nói.')
    cmd13 = cmdx('Phân tích các “ký hiệu đặc biệt” trong bài. Phần “Nếu thiếu” là kết quả chạy thật.', [
        ['<code>#</code> đầu dòng', 'Biến cả dòng thành <b>ghi chú</b>: Python bỏ qua. Dùng để giải thích hoặc tạm tắt dòng.', 'Quên <code>#</code> trước câu ghi chú, Python cố hiểu như code:' + ERR('Chương trình chào hỏi\nprint("Xin chào")')],
        ['<code># …</code> sau một lệnh', 'Ghi chú ở cuối dòng; phần lệnh phía trước vẫn chạy.', 'Nếu dấu <code>#</code> nằm <b>trong dấu nháy</b> thì nó chỉ là chữ, không là ghi chú:' + R('print("Số # 1")')],
        ['<code>""" … """</code> ba dấu nháy', 'Ghi chú nhiều dòng (thường đặt đầu tệp để ghi tên bài, tác giả).', 'Mở mà quên đóng ba dấu nháy:' + ERR('"""\nBài 1.3\nprint("Xong")')],
        ['dòng cuối của <b>Traceback</b>', 'Cho biết <b>loại lỗi</b> và lý do ngắn gọn.', 'Bỏ qua dòng này, chỉ nhìn các dòng phía trên, em sẽ không biết lỗi gì để sửa.'],
        ['<code>line 2</code> trong Traceback', 'Số dòng trong tệp nơi Python phát hiện lỗi.', 'Lỗi thật đôi khi nằm ở dòng <b>ngay trước</b> dòng được báo (ví dụ quên đóng ngoặc ở dòng trên).']])
    P['c1b3'] = std2('Bài 1.3 · Ghi chú và đọc thông báo lỗi', 'Lỗi không phải thất bại: đó là thông tin giúp em sửa nhanh.',
        ('Viết ghi chú bằng #, tạm tắt dòng lệnh; đọc được Traceback và nhận ra 5 loại lỗi thường gặp', 'Đã chạy được chương trình print (Bài 1.2)', 'Một chương trình có ghi chú rõ ràng, và bảng “lỗi – nguyên nhân – cách sửa” của riêng em'),
        ['<b>Ghi chú</b> giúp em và người khác hiểu code sau vài tuần mà không phải đoán.', 'Biết <b>đọc lỗi</b> là kỹ năng quan trọng bậc nhất: người giỏi không ít lỗi hơn, họ chỉ sửa lỗi nhanh hơn.', 'Gặp lỗi mà đọc ngay dòng cuối sẽ tiết kiệm hàng giờ so với việc đoán mò.', 'Tạm tắt dòng bằng <code>#</code> là cách thử từng phần để tìm đúng chỗ gây lỗi.'],
        ol(['Muốn giải thích: gõ <code>#</code> rồi viết ghi chú ngắn, nêu <b>vì sao</b> làm vậy, không chép lại code.', 'Muốn thử bỏ một dòng: thêm <code>#</code> đầu dòng đó, chạy lại; hết lỗi nghĩa là dòng đó gây lỗi.', 'Gặp lỗi: <b>đọc dòng cuối</b> (loại lỗi) → <b>xem số dòng</b> → <b>mở đúng dòng</b> và đối chiếu.']),
        think(['<b>Phản biện:</b> “lỗi” là một bằng chứng. Em thử đoán nguyên nhân rồi kiểm chứng, đừng sửa lung tung nhiều chỗ cùng lúc.', '<b>Nghĩ ngược:</b> từ thông báo lỗi lần ngược về nguyên nhân: loại lỗi nào, dòng nào, em đã gõ gì ở đó.', '<b>Thói quen tốt:</b> sửa một chỗ, chạy lại, rồi mới sửa chỗ khác.']),
        'Ứng dụng vào Python',
        li(['Chương trình có ghi chú và dòng bị tắt:']) + R(cm1) + 'Ghi chú nhiều dòng ở đầu tệp:' + R(cm2) + 'Một lỗi thật, với đầy đủ Traceback:' + TB(tbsrc) + H1,
        cmd13,
        H2 + ptrace(cm1, pick=[0, 1], captions=['Dòng 1 (ghi chú) máy bỏ qua; <b>dòng 2</b> chạy: in “Xin chào”, phần sau # bị bỏ qua.', 'Dòng 3 bị tắt nên máy bỏ qua; <b>dòng 4</b> chạy: in “Tạm biệt”.']) + H3 + H4 + H5 + H6 + H7 + flowrow(['Đọc dòng|cuối', 'Biết loại|lỗi', 'Mở đúng|dòng', 'Sửa một|chỗ', 'Chạy lại'], 'Quy trình sửa lỗi', colors=['#fdecea', '#fff4d6', '#e6f1fb', '#e5f5ea', '#e5f5ea']),
        [err('Bỏ qua thông báo lỗi', 'Nhiều bạn thấy chữ đỏ là hoảng và sửa bừa. Thực ra thông báo nói rõ điều cần sửa:' + ERR(e_name), 'Đọc dòng cuối: <code>NameError</code> nghĩa là tên <code>ten</code> chưa được tạo.'),
         err('Ghi chú chép lại code', '<code># in lời chào</code> ngay trên <code>print("Xin chào")</code> chẳng thêm gì.', 'Ghi chú nên nói <b>vì sao</b> hoặc <b>ý định</b>, không lặp lại lệnh.'),
         err('Sửa nhiều chỗ cùng lúc', 'Khi sửa 5 chỗ rồi chạy mà vẫn lỗi, em không biết chỗ nào đúng, chỗ nào sai.', 'Sửa một chỗ, chạy lại, rồi mới sửa tiếp.'),
         err('Cho rằng lỗi luôn nằm đúng dòng được báo', 'Quên đóng ngoặc ở dòng trên có thể làm Python báo lỗi ở dòng dưới.', 'Khi dòng được báo trông đúng, hãy xem dòng phía trên nó.')],
        [eg('Ví dụ 1: bốn loại lỗi, bốn tên', ''.join('<p><b>%s</b></p>%s' % (n, ERR(s)) for n, d, s in types[:4])),
         eg('Ví dụ 2: thử từng phần bằng cách tắt dòng', R('print("Bước 1")\n# print("Bước 2 – đang nghi ngờ dòng này")\nprint("Bước 3")') + note('Tắt dòng nghi ngờ, nếu chương trình chạy bình thường thì thủ phạm nằm ở đó.'))],
        [('Thêm một dòng ghi chú ở đầu chương trình Bài 1.2 của em, ghi tên em và ngày làm bài.', R('# Lan - bài 1.3\nprint("Xin chào")'), None),
         ('Chạy <code>print(ten)</code> (chưa gán <code>ten</code>), đọc lỗi và cho biết: loại lỗi là gì, nên sửa thế nào?', ERR(e_name) + '<p>Đây là <code>NameError</code>: Python chưa biết <code>ten</code>. Sửa bằng cách tạo tên trước (<code>ten = "Lan"</code>) hoặc đặt dấu nháy nếu muốn in chữ.</p>' + R('ten = "Lan"\nprint(ten)'), None),
         ('Chương trình có 3 lỗi, mỗi lần chạy báo một lỗi. Sửa lần lượt:' + code('print("Xin chào"\nprint(5 + "3")\nprint(10 / 0)'), '<p>Lần 1: thiếu <code>)</code> ở dòng 1 (SyntaxError). Lần 2: không cộng được số với chữ → viết <code>5 + 3</code> (TypeError). Lần 3: chia cho 0 không có nghĩa → đổi số chia khác 0 (ZeroDivisionError).</p>' + R('print("Xin chào")\nprint(5 + 3)\nprint(10 / 2)') + note('Dù có 3 lỗi, mỗi lần Python chỉ nêu lỗi đầu tiên – nên phải chạy lại sau mỗi lần sửa.'), None),
         ('Bạn Nam nói “code của mình đúng, máy lỗi”. Chạy <code>print("Xin chào"</code> và viết 2 câu giải thích bạn đọc lỗi thế nào để thấy code chưa đúng.', ERR(e_syn) + '<p>Dòng cuối cho biết ngoặc <code>(</code> chưa được đóng. Bằng chứng nằm ngay trong thông báo, không phải lỗi của máy.</p>', None),
         ('<b>Thử thách:</b> tự lập bảng “lỗi – nguyên nhân – cách sửa” cho 5 loại lỗi trong bài (mỗi loại một ví dụ code lỗi do em tự viết và kết quả chạy).', '<p>Ví dụ mẫu (em làm theo cách của mình):</p>' + table(['Loại lỗi', 'Code lỗi', 'Nguyên nhân', 'Cách sửa'], [['SyntaxError', '<code>print("a"</code>', 'thiếu ngoặc đóng', 'thêm <code>)</code>'], ['NameError', '<code>print(ten)</code>', 'chưa có tên', 'gán <code>ten</code> trước'], ['TypeError', '<code>"5" + 3</code>', 'trộn chữ và số', 'đổi cùng kiểu'], ['ZeroDivisionError', '<code>10 / 0</code>', 'chia cho 0', 'đổi số chia'], ['IndentationError', 'thụt dòng bừa', 'thụt không cần thiết', 'bỏ dấu cách đầu dòng']]), None)],
        '')

    # ======================================================= BÀI TÓM TẮT CHƯƠNG 1
    mm = ARR + txt(350, 24, 'Sơ đồ tóm tắt Chương 1', '#17406b', 17, bold=True) + box(270, 100, 160, 60, '#fff4d6', '#d9822b', ['Chương 1', 'Bắt đầu với Python'], 15, bold=True)
    br = [(30, 40, 'Python là gì', 'cài đặt, IDLE, F5'), (30, 160, 'Lệnh print', '4 phần, nháy, dấu phẩy'), (490, 40, 'Máy chạy', 'từ trên xuống, từng dòng'), (490, 160, 'Ghi chú # & lỗi', 'đọc Traceback từ dưới lên')]
    for x, y, a, b in br:
        mm += box(x, y, 180, 60, '#e6f1fb', '#1f6fb2', [a, b], 14, bold=True)
        mm += arr(x + 182 if x < 270 else x - 2, y + 30, 262 if x < 270 else 438, 130, '#6b7785')
    M1 = fig(svg(700, 250, mm, 'Sơ đồ tóm tắt chương 1'), 'Bốn nhánh kiến thức của Chương 1 xoay quanh một mục tiêu: để máy làm đúng điều em bảo.')
    ba = ARR + txt(350, 24, 'Trước và sau Chương 1', '#17406b', 17, bold=True)
    ba += box(14, 44, 330, 150, '#f3f4f6', '#9db4c9', [], 14) + txt(179, 68, 'Trước chương 1', '#5b6773', 15, bold=True)
    for i, l in enumerate(['Chưa biết máy đọc lệnh thế nào', 'Thấy chữ đỏ là hoảng', 'Chưa phân biệt chữ và phép tính']): ba += txt(30, 104 + i * 28, '• ' + l, '#5b6773', 14, 'start')
    ba += box(356, 44, 330, 150, '#e5f5ea', '#2a8a4a', [], 14) + txt(521, 68, 'Sau chương 1', '#2a8a4a', 15, bold=True)
    for i, l in enumerate(['Viết và chạy được chương trình print', 'Đọc lỗi từ dòng cuối lên', 'Biết dùng # ghi chú và tắt dòng']): ba += txt(372, 104 + i * 28, '✓ ' + l, '#17406b', 14, 'start')
    M2 = fig(svg(700, 212, ba, 'Trước và sau chương 1'), 'Em đã đi được một bước nhỏ nhưng vững: máy nói được, và em hiểu máy nói gì khi gặp lỗi.')
    ck = ARR + txt(350, 24, 'Bảng tự đánh giá: tô màu ô em làm được', '#17406b', 17, bold=True)
    for i, l in enumerate(['In 3 dòng bằng print', 'Phân biệt "2+3" và 2+3', 'Dùng , và \\n trong print', 'Viết ghi chú #', 'Đọc dòng cuối của lỗi', 'Sửa 3 lỗi cú pháp thường gặp']):
        x = 14 + (i % 2) * 345; y = 44 + (i // 2) * 52; ck += '<rect x="%d" y="%d" width="330" height="42" rx="8" fill="#fff" stroke="#9db4c9"/><rect x="%d" y="%d" width="22" height="22" rx="4" fill="#fff" stroke="#1f6fb2" stroke-width="2"/>' % (x, y, x + 12, y + 10) + txt(x + 46, y + 27, l, '#1c2733', 14, 'start')
    M3 = fig(svg(700, 206, ck, 'Bảng tự đánh giá'), 'Chưa tô được ô nào thì quay lại bài tương ứng, đừng bỏ qua.')
    card_out = ARR + txt(350, 24, 'Kết quả của dự án: tấm thiệp trên màn hình', '#17406b', 17, bold=True) + box(150, 40, 400, 170, '#fff', '#6b7785', [], 14)
    for i, l in enumerate(['==============================', '       THIỆP CHÀO MỪNG', '==============================', '', 'Chào bạn mới của lớp Python!']): card_out += mono(170, 70 + i * 22, l, '#1c2733', 13)
    M4 = fig(svg(700, 224, card_out, 'Kết quả dự án thiệp'), 'Phần đầu của tấm thiệp do dự án tạo ra (xem đầy đủ ở lời giải).')
    tab = table(['Điều cần nhớ', 'Ví dụ', 'Ý nghĩa'], [['<code>print(...)</code>', '<code>print("Xin chào")</code>', 'In ra màn hình'], ['Dấu nháy <code>" "</code>', '<code>"2 + 3"</code> khác <code>2 + 3</code>', 'Có nháy là chữ; không nháy là phép tính'], ['Dấu phẩy trong print', '<code>print("a", "b")</code>', 'In nhiều thứ, cách nhau một dấu cách'], ['<code>\\n</code>', '<code>"Dòng 1\\nDòng 2"</code>', 'Xuống dòng'], ['<code>#</code>', '<code># ghi chú</code>', 'Ghi chú, Python bỏ qua'], ['F5', 'Run Module', 'Chạy chương trình trong IDLE'], ['Traceback', 'đọc từ dưới lên', 'Dòng cuối: loại lỗi; số dòng: chỗ cần sửa']])
    top5 = ''.join(err(a, b, c) for a, b, c in [('Viết Print thay vì print', 'Python phân biệt hoa thường.', 'Luôn viết thường.'), ('Thiếu dấu nháy hoặc ngoặc', 'SyntaxError cho biết chuỗi hoặc ngoặc chưa đóng.', 'Đếm cặp mở – đóng.'), ('Thụt dòng đầu dòng', 'IndentationError.', 'Lệnh thường bắt đầu sát lề trái.'), ('Dùng dấu nháy cong của Word', 'Ký tự lạ làm lỗi cú pháp.', 'Gõ lại dấu <code>"</code> trong trình soạn code.'), ('Bỏ qua thông báo lỗi', 'Sửa bừa mất thời gian.', 'Đọc dòng cuối trước.')])
    proj = 'print("=" * 30)\nprint("      THIỆP CHÀO MỪNG")\nprint("=" * 30)\nprint()\nprint("Chào bạn mới của lớp Python!")\nprint("Hôm nay ta bắt đầu hành trình")\nprint("\\"lập trình để biết cách nghĩ\\".")\nprint()\nprint("Chúc em học vui!")\nprint("=" * 30)'
    quiz = [('Lệnh nào in ra màn hình?', '<code>print</code>.'), ('<code>print("2 + 3")</code> và <code>print(2 + 3)</code> in ra gì?', 'Câu đầu in <code>2 + 3</code> (là chữ), câu sau in <code>5</code> (là phép tính).'), ('Máy chạy các dòng theo thứ tự nào?', 'Từ trên xuống dưới, mỗi lần một dòng; đổi chỗ hai dòng thì kết quả đổi theo.'), ('Dấu <code>#</code> dùng để làm gì?', 'Ghi chú hoặc tạm tắt một dòng; Python bỏ qua phần sau <code>#</code>.'), ('Gặp lỗi, em đọc phần nào trước?', 'Dòng cuối của thông báo (loại lỗi và lý do), rồi tới số dòng.'), ('<code>NameError</code> thường do đâu?', 'Dùng một tên chưa được tạo hoặc viết sai chính tả tên.')]
    qh = ''.join('<details class="tans"><summary>Câu %d. %s</summary><p>%s</p></details>' % (i + 1, q, a) for i, (q, a) in enumerate(quiz))
    P['c1t'] = {'title': 'Tóm tắt Chương 1 · Bắt đầu với Python', 'sub': 'Hệ thống lại kiến thức, lỗi hay gặp và làm dự án nhỏ cuối chương.',
        'html': '\n'.join([tsum('Hệ thống lại Chương 1 và tự kiểm tra; hoàn thành dự án “thiệp chào mừng”', 'Đã học Bài 1.1 đến 1.3', 'Bảng ghi nhớ của em và chương trình thiệp chào mừng chạy đúng'),
            card(1, 'Sơ đồ tóm tắt chương', M1 + M2), card(2, 'Bảng ghi nhớ nhanh', tab), card(3, '5 lỗi hay gặp nhất của chương', top5),
            card('+', 'Em đã làm được gì? (tự đánh giá)', M3),
            card(4, 'Em đã học được thói quen tư duy nào?', think(['<b>Dự đoán trước, chạy sau.</b>', '<b>Đọc lỗi như đọc bằng chứng:</b> từ dòng cuối lần ngược về nguyên nhân.', '<b>Sửa từng chỗ một</b> để biết điều gì có tác dụng.'], 'Thói quen của Chương 1')),
            chap('Dự án nhỏ cuối chương'),
            '<section class="tcard tprac"><h4><span class="tn">DA</span>Dự án: thiệp chào mừng tự động <span class="lvl">★★★☆</span></h4><p>Viết chương trình in một <b>tấm thiệp chào mừng</b> gồm: khung viền, tiêu đề, một đoạn lời chào 3 dòng (trong đó có một câu có dấu ngoặc kép), và dòng chúc. Dùng đủ: <code>print</code>, dấu <code>"*"</code> hoặc <code>"="</code> lặp, dòng trống, ghi chú <code>#</code> ở đầu.</p><details class="tans"><summary>Xem bài mẫu và kết quả chạy</summary>%s<p>Chú ý: để in dấu ngoặc kép bên trong chữ, em viết <code>\\"</code>; hoặc bao chữ bằng dấu nháy đơn.</p></details></section>' % (code('# Dự án chương 1: thiệp chào mừng\n' + proj, run(proj)) + M4),
            chap('Tự kiểm tra (6 câu)'), '<section class="tcard">%s</section>' % qh,
            card(5, 'Chương sau học gì?', li(['<b>Chương 2 – Biến, số và chuỗi:</b> lưu thông tin vào “chiếc hộp có tên”, làm phép tính, cắt ghép chữ, nhập dữ liệu từ bàn phím.', 'Em đã biết cho máy <b>nói</b>; sang chương 2 em sẽ cho máy <b>nhớ và tính toán</b>.']))])}
    return P
