"""Giáo trình Python 12–18 – Chương 2: Bài 2.2 Số và phép toán, Bài 2.3 Chuỗi, Tóm tắt chương 2.
Mọi kết quả chạy, thông báo lỗi lấy từ lần chạy thật."""
from tuduy_py2 import *

C = {'bl': ('#e6f1fb', '#1f6fb2'), 'gr': ('#e5f5ea', '#2a8a4a'), 'ye': ('#fff4d6', '#d9822b'), 'rd': ('#fdecea', '#c0392b'), 'pu': ('#f1e8fb', '#7b4bb3'), 'gy': ('#f3f4f6', '#9db4c9')}


def M(x, y, t, col, sz, anchor='start', bold=False):
    """Chữ code (ASCII) dùng ô đơn cách; chữ tiếng Việt dùng phông thường để không bị giãn."""
    return mono(x, y, t, col, sz, anchor, bold) if t.isascii() else txt(x, y, t, col, sz - 1, {'start': 'start', 'middle': 'middle', 'end': 'end'}[anchor], bold)


def cmp_fig(title, cols, h=190, cap=None, label=None):
    """Các cột so sánh: mỗi cột = (màu, tiêu đề, [dòng code], kết quả, ghi chú)."""
    n = len(cols); w = 700; gap = 12; bw = (w - 28 - (n - 1) * gap) / n
    s = ARR + txt(350, 26, title, '#17406b', 17, bold=True)
    for i, (c, head, lines, res, note_) in enumerate(cols):
        x = 14 + i * (bw + gap); f, st = C[c]
        s += '<rect x="%.1f" y="44" width="%.1f" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="2"/>' % (x, bw, h - 56, f, st)
        s += txt(x + bw / 2, 68, head, st, 15, bold=True)
        for k, l in enumerate(lines):
            sz = 17 if len(l) * 10 < bw else 14
            s += M(x + bw / 2, 100 + k * 26, l, '#17406b', sz, 'middle')
        y0 = 100 + len(lines) * 26
        s += arr(x + bw / 2, y0 - 12, x + bw / 2, y0 + 8, st) + M(x + bw / 2, y0 + 34, res, st, 20 if res.isascii() else 18, 'middle', True)
        if note_: s += txt(x + bw / 2, y0 + 58, note_, '#5b6773', 13)
    return svg(w, h, s, label or title)


def grid_fig(title, head, rows, colw, hl=None, label=None, rh=34):
    """Bảng dạng hình: head, rows là các chuỗi; cột đầu dạng code."""
    w = sum(colw) + 28; s = ARR + txt(w / 2, 26, title, '#17406b', 17, bold=True)
    x0 = 14; y = 44
    xs = [x0]
    for c in colw: xs.append(xs[-1] + c)
    s += '<rect x="%d" y="%d" width="%d" height="%d" fill="#17406b" rx="6"/>' % (x0, y, sum(colw), rh)
    for j, t in enumerate(head): s += txt(xs[j] + colw[j] / 2, y + rh / 2 + 5, t, '#fff', 14, bold=True)
    for i, r in enumerate(rows):
        yy = y + rh * (i + 1)
        fill = '#fff4d6' if hl is not None and i in hl else ('#f6f8fb' if i % 2 else '#fff')
        s += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#d3dce6"/>' % (x0, yy, sum(colw), rh, fill)
        for j, t in enumerate(r):
            if j == 0: s += M(xs[j] + colw[j] / 2, yy + rh / 2 + 5, t, '#17406b', 15, 'middle', True)
            else: s += txt(xs[j] + colw[j] / 2, yy + rh / 2 + 5, t, '#1c2733', 14)
    return svg(w, y + rh * (len(rows) + 1) + 14, s, label or title)


def build():
    P = {}

    # ===================================================== BÀI 2.2  SỐ VÀ PHÉP TOÁN
    ops = 'a = 7\nb = 2\nprint(a + b)\nprint(a - b)\nprint(a * b)\nprint(a / b)\nprint(a // b)\nprint(a % b)\nprint(a ** b)'
    prec = 'print(2 + 3 * 4)\nprint((2 + 3) * 4)\nprint(2 * 3 ** 2)\nprint(10 - 4 - 3)\nprint(20 / 4 / 5)'
    tm = 'phut = 135\ngio = phut // 60\ndu = phut % 60\nprint(phut, "phút =", gio, "giờ", du, "phút")'
    ft = 'print(8 / 2)\nprint(type(8 / 2))\nprint(type(8 // 2))\nprint(int(3.9))\nprint(float(5))\nprint(round(3.567, 2))'
    fe = 'print(0.1 + 0.2)\nprint(round(0.1 + 0.2, 2))\nprint(0.1 + 0.2 == 0.3)\nprint(round(0.1 + 0.2, 2) == 0.3)'
    fn = 'print(abs(-7))\nprint(max(3, 9, 4))\nprint(min(3, 9, 4))\nprint(round(2.5))\nprint(round(3.5))\nprint(int(-3.9))'
    aug = 'x = 10\nx += 5\nx -= 3\nx *= 2\nx //= 4\nprint(x)'
    shop = 'gia = 25000\nsl = 3\ntong = gia * sl\ngiam = tong * 10 // 100\nprint("Tạm tính:", tong)\nprint("Giảm 10%:", giam)\nprint("Phải trả:", tong - giam)'
    kt = 'tong = 17\nnhom = 5\nprint(tong // nhom, "nhóm đầy, dư", tong % nhom)\nprint(tong // nhom * nhom + tong % nhom == tong)'

    # --- hình
    N1 = fig(grid_fig('7 và 2: bảy phép toán cơ bản', ['Ký hiệu', 'Tên gọi', 'Ví dụ', 'Kết quả'],
        [['+', 'cộng', '7 + 2', '9'], ['-', 'trừ', '7 - 2', '5'], ['*', 'nhân', '7 * 2', '14'], ['/', 'chia (ra số thập phân)', '7 / 2', '3.5'], ['//', 'chia lấy phần nguyên', '7 // 2', '3'], ['%', 'chia lấy phần dư', '7 % 2', '1'], ['**', 'lũy thừa', '7 ** 2', '49']],
        [90, 250, 150, 130]), 'Ngoài + − × quen thuộc, Python có thêm ba phép rất hữu ích: <code>/</code>, <code>//</code>, <code>%</code>.')
    N2 = fig(cmp_fig('Ba phép chia khác nhau', [('bl', 'Chia thường  /', ['7 / 2'], '3.5', 'luôn ra số thập phân'), ('gr', 'Chia nguyên  //', ['7 // 2'], '3', 'bỏ phần lẻ'), ('ye', 'Chia dư  %', ['7 % 2'], '1', 'phần còn thừa')], 200),
        'Cùng 7 và 2 nhưng ba phép chia cho ba câu trả lời khác nhau: hãy chọn phép đúng với câu hỏi.')
    dots = ARR + txt(350, 26, '17 chia thành các nhóm 5: 3 nhóm đầy, dư 2', '#17406b', 17, bold=True)
    cols_ = ['#2a8a4a', '#1f6fb2', '#d9822b', '#c0392b']
    for k in range(17):
        g, p = divmod(k, 5); x = 40 + g * 150 + p * 26; y = 70
        dots += '<circle cx="%d" cy="%d" r="10" fill="%s"/>' % (x, y, cols_[min(g, 3)])
    for g in range(3): dots += '<rect x="%d" y="52" width="140" height="36" rx="8" fill="none" stroke="%s" stroke-width="2"/>' % (26 + g * 150, cols_[g])
    dots += '<rect x="476" y="52" width="66" height="36" rx="8" fill="none" stroke="#c0392b" stroke-width="2" stroke-dasharray="5 4"/>'
    dots += mono(40, 130, '17 // 5 = 3', '#2a8a4a', 20, 'start', True) + txt(40, 154, '(số nhóm đầy)', '#5b6773', 13, 'start') + mono(330, 130, '17 % 5 = 2', '#c0392b', 20, 'start', True) + txt(330, 154, '(số chấm còn dư)', '#5b6773', 13, 'start')
    dots += txt(350, 190, 'Kiểm chứng: 3 × 5 + 2 = 17', '#17406b', 15, bold=True)
    N3 = fig(svg(700, 204, dots, 'Chia nhóm có dư'), '<code>//</code> đếm số nhóm đầy, <code>%</code> đếm phần dư; hai kết quả ghép lại phải ra số ban đầu.')
    N4 = fig(cmp_fig('Thứ tự thực hiện: nhân trước, cộng sau', [('rd', 'Không ngoặc', ['2 + 3 * 4'], '14', '3 * 4 = 12 trước, rồi + 2'), ('gr', 'Có ngoặc', ['(2 + 3) * 4'], '20', '(2 + 3) = 5 trước, rồi * 4')], 200),
        'Ngoặc tròn ép Python tính trước. Thứ tự: <b>ngoặc</b> → <b>**</b> → <b>* / // %</b> → <b>+ −</b>.')
    N5 = fig(grid_fig('Bậc ưu tiên: càng trên càng làm trước', ['Thứ tự', 'Phép toán', 'Ví dụ', 'Kết quả'],
        [['1', '( )', '(2 + 3) * 4', '20'], ['2', '**', '2 * 3 ** 2', '18'], ['3', '* / // %', '10 - 6 / 2', '7.0'], ['4', '+ −', '10 - 4 - 3', '3']], [90, 200, 200, 130], label='Bậc ưu tiên phép toán'),
        'Cùng bậc thì làm từ trái sang phải: <code>10 - 4 - 3</code> là <code>(10 - 4) - 3 = 3</code>.')
    N6 = fig(cmp_fig('Số nguyên (int) và số thực (float)', [('bl', 'int', ['8 // 2', 'int(3.9)'], '4  ·  3', 'số nguyên, không có dấu chấm'), ('ye', 'float', ['8 / 2', 'float(5)'], '4.0  ·  5.0', 'số thập phân, có dấu chấm')], 232),
        'Phép <code>/</code> luôn cho kết quả <b>float</b>, dù chia hết (8 / 2 ra 4.0). <code>int()</code> cắt bỏ phần lẻ, không làm tròn.')
    N7 = fig(cmp_fig('Số thực có thể sai lệch rất nhỏ', [('rd', 'Dễ nhầm', ['0.1 + 0.2'], '0.30000000000000004', 'máy lưu số thực gần đúng'), ('gr', 'An toàn hơn', ['round(0.1 + 0.2, 2)'], '0.3', 'làm tròn tới 2 chữ số')], 232),
        'Máy lưu số thập phân dưới dạng nhị phân nên có sai lệch nhỏ. Vì vậy hãy <b>làm tròn</b> khi in và so sánh.')
    N8 = fig(grid_fig('Bộ hàm hỗ trợ về số', ['Hàm', 'Việc làm', 'Ví dụ', 'Kết quả'],
        [['abs(x)', 'giá trị tuyệt đối', 'abs(-7)', '7'], ['max(...)', 'số lớn nhất', 'max(3, 9, 4)', '9'], ['min(...)', 'số nhỏ nhất', 'min(3, 9, 4)', '3'], ['round(x, n)', 'làm tròn n chữ số', 'round(3.567, 2)', '3.57'], ['int(x)', 'bỏ phần lẻ', 'int(-3.9)', '-3']], [130, 220, 200, 100], label='Các hàm về số'),
        '<code>int(-3.9)</code> ra -3 (bỏ phần lẻ, hướng về 0) chứ không phải -4.')
    gh = ARR + txt(350, 26, '135 phút đổi thành giờ và phút', '#17406b', 17, bold=True)
    gh += box(14, 50, 150, 70, '#fff4d6', '#d9822b', ['phut = 135'], 17, bold=True) + arr(166, 70, 230, 56) + arr(166, 100, 230, 124)
    gh += box(232, 36, 210, 44, '#e5f5ea', '#2a8a4a', ['135 // 60 = 2 giờ'], 16, bold=True) + box(232, 102, 210, 44, '#e6f1fb', '#1f6fb2', ['135 % 60 = 15 phút'], 16, bold=True)
    gh += arr(444, 58, 500, 90) + arr(444, 124, 500, 100) + box(502, 66, 184, 54, '#fff', '#17406b', ['2 giờ 15 phút'], 18, bold=True) + txt(350, 176, '// cho phần nguyên (giờ); % cho phần còn lại (phút)', '#5b6773', 14)
    N9 = fig(svg(700, 192, gh, 'Đổi phút sang giờ'), 'Cặp <code>//</code> và <code>%</code> thường đi cùng nhau: đổi đơn vị, tách chữ số, chia nhóm.')
    N10 = flowrow(['Đọc đề,|nêu dữ liệu', 'Chọn phép|toán', 'Viết biểu|thức', 'Đoán kết|quả', 'Chạy rồi|đối chiếu'], 'Quy trình giải bài tính toán', colors=['#e6f1fb', '#e6f1fb', '#fff4d6', '#fff4d6', '#e5f5ea'])
    N11 = ptrace(shop, pick=[0, 1, 2, 3, 4], maxn=6, captions=['Tạo biến <b>gia</b> = 25000.', 'Tạo biến <b>sl</b> = 3.', '<b>tong</b> = 25000 × 3 = 75000.', '<b>giam</b> = 75000 × 10 // 100 = 7500.', 'In “Tạm tính: 75000”.'])

    cmd22 = cmdx('Phân tích các ký hiệu và hàm của bài. Phần “Nếu thiếu hoặc sai” đều là kết quả chạy thật.', [
        ['<code>+  -  *</code>', 'Cộng, trừ, nhân như trong toán.', 'Quên dấu nhân giữa hai số (viết như toán học):' + ERR('print(3 4)')],
        ['<code>/</code> chia', 'Chia ra số thập phân, kết quả luôn là float.', 'Chia cho 0 không có nghĩa:' + ERR('print(10 / 0)')],
        ['<code>//</code> chia lấy phần nguyên', 'Cho số lần “chứa trọn” (số nhóm đầy).', 'Dùng <code>//</code> với số chia 0 cũng lỗi:' + ERR('print(7 // 0)')],
        ['<code>%</code> chia lấy phần dư', 'Cho phần còn thừa; <code>n % 2</code> là 0 khi n chẵn.', 'Chia dư cho 0 cũng không được:' + ERR('print(7 % 0)')],
        ['<code>**</code> lũy thừa', '<code>a ** b</code> là a mũ b.', 'Viết <code>^</code> như trong toán: <b>không báo lỗi</b> nhưng ra kết quả khác hẳn (đó là phép khác):' + R('print(2 ^ 3)\nprint(2 ** 3)')],
        ['<code>( )</code> ngoặc tròn', 'Ép Python tính phần trong ngoặc trước.', 'Bỏ ngoặc, kết quả đổi:' + R('print(2 + 3 * 4)\nprint((2 + 3) * 4)') + 'Thiếu ngoặc đóng:' + ERR('print((2 + 3) * 4')],
        ['<code>int( )</code>', 'Đổi sang số nguyên; cắt bỏ phần lẻ.', 'Đưa chữ không phải số nguyên vào:' + ERR('print(int("3.5"))')],
        ['<code>round(x, n)</code>', 'Làm tròn x tới n chữ số thập phân; bỏ <code>n</code> thì làm tròn về số nguyên.', 'Bỏ <code>n</code>:' + R('print(round(3.14159))\nprint(round(3.14159, 2))')],
        ['dấu chấm <code>.</code> thập phân', 'Python dùng <b>dấu chấm</b> cho số thập phân (3.5).', 'Gõ dấu phẩy như kiểu Việt Nam, Python hiểu là hai thứ khác nhau (không báo lỗi!):' + R('print(3,5 + 2)')],
        ['<code>+=  -=  *=  //=</code>', 'Viết tắt: <code>x += 5</code> nghĩa là <code>x = x + 5</code>.', 'Dùng khi chưa có biến:' + ERR('y += 1')]])

    P['c2b2'] = std2('Bài 2.2 · Số và phép toán', 'Tính toán với Python: chia lấy nguyên, chia lấy dư, thứ tự phép tính và số thực.',
        ('Dùng được 7 phép toán, hiểu thứ tự thực hiện, phân biệt int với float, dùng // và % để đổi đơn vị và chia nhóm', 'Đã học biến và print (Bài 2.1); mở sẵn IDLE', 'Chương trình tính tiền có giảm giá và chương trình đổi phút sang giờ'),
        ['Mọi bài toán tính toán — tiền, điểm, thời gian, khoảng cách — đều quy về các phép toán trên số.', 'Hai phép <b>//</b> và <b>%</b> là “đặc sản” của người lập trình: đổi đơn vị, chia đều, kiểm tra chẵn lẻ.', 'Hiểu <b>thứ tự thực hiện</b> giúp em không bao giờ viết sai công thức mà không biết.', 'Số thực có sai lệch nhỏ — biết điều này giúp em không hoang mang khi thấy 0.30000000000000004.'],
        ol(['Đọc đề, <b>gạch chân dữ kiện</b> rồi đặt tên biến cho từng dữ kiện (<code>gia</code>, <code>sl</code>).', 'Hỏi: “Cần phép nào?” – tổng tiền dùng <code>*</code>; số nhóm đầy dùng <code>//</code>; phần dư dùng <code>%</code>.', 'Viết biểu thức, <b>thêm ngoặc</b> nếu cần ép thứ tự; đoán kết quả trước khi chạy.', 'Chạy và <b>kiểm chứng ngược</b>: ví dụ <code>nhóm × cỡ nhóm + dư</code> phải bằng số ban đầu.']),
        think(['<b>Phản biện:</b> kết quả máy đưa ra có hợp lý không? Ví dụ 17 kẹo chia 5 bạn mà mỗi bạn được 3.4 cái thì có hợp lý không?', '<b>Nghĩ ngược:</b> từ kết quả quay về dữ kiện để kiểm tra: 3 × 5 + 2 có bằng 17 không?', '<b>Chọn đúng công cụ:</b> cùng hai số có ba phép chia; hỏi “mình cần số nhóm, phần dư hay số thập phân?” trước khi gõ.']),
        'Ứng dụng vào Python',
        li(['Bảy phép toán với <code>a = 7</code>, <code>b = 2</code>:']) + R(ops) + 'Thứ tự thực hiện:' + R(prec) + 'Đổi phút sang giờ, phút:' + R(tm) + 'Tính tiền có giảm giá:' + R(shop) + 'Số nguyên, số thực và các hàm hỗ trợ:' + R(ft) + R(fn) + note('Chú ý: <code>round(2.5)</code> ra 2 còn <code>round(3.5)</code> ra 4 – Python làm tròn về số chẵn gần nhất khi đúng .5. Cần luật “.5 làm tròn lên” thì phải tự xử lý.') + 'Số thực và sai lệch nhỏ:' + R(fe) + 'Viết tắt phép gán:' + R(aug),
        cmd22,
        N1 + N2 + N3 + N4 + N5 + N6 + N7 + N8 + N9 + N10 + N11,
        [err('Nhầm / với //', '<code>7 / 2</code> ra 3.5 còn <code>7 // 2</code> ra 3. Đếm số bàn, số xe, số nhóm thì cần <code>//</code> (hoặc cộng 1 nếu còn dư).', 'Tự hỏi: “đáp số có thể lẻ không?” – nếu không, dùng <code>//</code>.'),
         err('Chia cho 0', 'Một biến làm số chia có thể bằng 0 mà em không để ý:' + ERR('so_nhom = 0\nprint(12 // so_nhom)'), 'Trước khi chia, nhớ nghĩ: “số chia có thể bằng 0 không?” – bài rẽ nhánh sẽ dạy cách chặn.'),
         err('Viết ^ thay cho **', 'Trong Python, <code>^</code> là phép khác nên không báo lỗi mà ra kết quả sai âm thầm:' + R('print(2 ^ 3)'), 'Lũy thừa viết <code>**</code>.'),
         err('So sánh số thực bằng ==', R('print(0.1 + 0.2 == 0.3)') + 'Hai vế gần bằng nhau nhưng không giống hệt.', 'Làm tròn trước khi so sánh: <code>round(0.1 + 0.2, 2) == 0.3</code>.'),
         err('Quên nhân ngầm', 'Trong toán, <code>2(3 + 4)</code> hiểu là nhân. Trong Python phải viết rõ:' + ERR('print(2(3 + 4))'), 'Luôn viết dấu <code>*</code>: <code>2 * (3 + 4)</code>.')],
        [eg('Ví dụ 1: chẵn hay lẻ?', R('for n in (6, 7, 10, 13):\n    print(n, "dư", n % 2)') + note('Số chẵn chia 2 dư 0; số lẻ dư 1. Dòng <code>for</code> sẽ học ở chương lặp, bây giờ em chỉ cần đọc kết quả.')),
         eg('Ví dụ 2: tách chữ số của 482', R('n = 482\nprint("Đơn vị:", n % 10)\nprint("Chục:", n // 10 % 10)\nprint("Trăm:", n // 100)')),
         eg('Ví dụ 3: chia 17 kẹo cho nhóm 5 bạn', R(kt) + note('Dòng cuối là kiểm chứng ngược: kết quả <code>True</code> chứng tỏ phép chia và phần dư khớp nhau.'))],
        [('Dự đoán rồi chạy: <code>print(15 + 4 * 3)</code> và <code>print((15 + 4) * 3)</code>. Vì sao hai kết quả khác nhau?', R('print(15 + 4 * 3)\nprint((15 + 4) * 3)') + '<p>Dòng 1: nhân trước (4 × 3 = 12), cộng sau: 27. Dòng 2: ngoặc ép cộng trước (19), rồi nhân: 57.</p>', None),
         ('Một chuyến xe dài 200 phút. Viết chương trình in ra “3 giờ 20 phút” bằng cách dùng biến, <code>//</code> và <code>%</code>.', R('phut = 200\nprint(phut // 60, "giờ", phut % 60, "phút")') + note('Kiểm chứng: 3 × 60 + 20 = 200.'), None),
         ('Mua 3 ly trà sữa giá 28000 đồng/ly, được giảm 10% trên tổng tiền. In ra tạm tính, tiền giảm và số tiền phải trả.', R('gia = 28000\nsl = 3\ntong = gia * sl\ngiam = tong * 10 // 100\nprint("Tạm tính:", tong)\nprint("Giảm:", giam)\nprint("Phải trả:", tong - giam)'), None),
         ('Cho số 2847. Chỉ dùng <code>//</code> và <code>%</code>, hãy in riêng từng chữ số: nghìn, trăm, chục, đơn vị.', R('n = 2847\nprint("Nghìn:", n // 1000)\nprint("Trăm:", n // 100 % 10)\nprint("Chục:", n // 10 % 10)\nprint("Đơn vị:", n % 10)') + note('Mẹo: chia nguyên để “dời” chữ số cần lấy về cuối, rồi lấy phần dư khi chia 10.'), None),
         ('<b>Thử thách (nghĩ ngược):</b> (a) Bây giờ là 22 giờ. Sau 30 giờ nữa là mấy giờ trên đồng hồ 24 giờ? (b) Chia 47 cái kẹo cho 6 bạn: mỗi bạn được bao nhiêu, dư bao nhiêu, cần thêm bao nhiêu cái để chia đều không dư? Hãy tự kiểm chứng kết quả.', R('# (a)\nprint((22 + 30) % 24)\n# (b)\nkeo = 47\nban = 6\nmoi = keo // ban\ndu = keo % ban\nprint("Mỗi bạn:", moi, "dư:", du)\nprint("Cần thêm:", ban - du)\nprint("Kiểm chứng:", moi * ban + du == keo)') + '<p>(a) 52 % 24 = 4: tức 4 giờ sáng hôm sau; phép <code>%</code> “quay vòng” như kim đồng hồ. (b) Mỗi bạn 7, dư 5, cần thêm 1 cái (6 − 5) để thành 48 chia đều.</p>', None)],
        '')

    # ===================================================== BÀI 2.3  CHUỖI
    s1 = 's = "Python"\nprint(len(s))\nprint(s[0])\nprint(s[5])\nprint(s[-1])\nprint(s[-6])'
    sl = 's = "Python"\nprint(s[0:2])\nprint(s[2:5])\nprint(s[:3])\nprint(s[3:])\nprint(s[::2])\nprint(s[::-1])'
    cat = 'a = "Xin"\nb = "chào"\nprint(a + " " + b)\nprint("ha" * 3)\nprint("-" * 10)'
    fs = 'ten = "Lan"\ntuoi = 13\nprint(f"Mình là {ten}, {tuoi} tuổi.")\nprint(f"Năm sau mình {tuoi + 1} tuổi.")'
    meth = 's = "  Xin Chào Python  "\nprint(s.strip())\nprint(s.upper())\nprint(s.lower())\nprint(s.replace("Python", "Lan"))\nprint(s.strip().split())'
    find = 'cau = "hôm nay học Python"\nprint(cau.find("học"))\nprint(cau.find("Java"))\nprint("Python" in cau)\nprint(cau.count("o"))\nprint(cau.startswith("hôm"))'
    jn = 'ds = ["Lan", "Minh", "Hà"]\nprint(", ".join(ds))\nprint("Lan Minh Hà".split())'
    tr = 'ten = "nguyen van an"\nho = ten[:6]\ncuoi = ten[-2:]\nprint(ho.upper(), cuoi.upper())'

    def letters(s, title, hl=(), neg=True, label=None, note_=None):
        n = len(s); bw = 56; x0 = 350 - n * bw / 2; sv = ARR + txt(350, 24, title, '#17406b', 17, bold=True)
        for i, ch in enumerate(s):
            x = x0 + i * bw; on = i in hl
            sv += '<rect x="%.1f" y="76" width="%d" height="52" rx="6" fill="%s" stroke="%s" stroke-width="2"/>' % (x, bw - 4, '#fff4d6' if on else '#e6f1fb', '#d9822b' if on else '#1f6fb2')
            sv += '<text x="%.1f" y="111" text-anchor="middle" font-size="26" font-weight="700" font-family="Consolas,Menlo,monospace" fill="#1c2733">%s</text>' % (x + (bw - 4) / 2, E(ch if ch != ' ' else '␣'))
            sv += txt(x + (bw - 4) / 2, 62, str(i), '#2a8a4a', 15, bold=True)
            if neg: sv += txt(x + (bw - 4) / 2, 150, str(i - n), '#c0392b', 14, bold=True)
        sv += txt(x0 - 14, 62, 'i', '#2a8a4a', 14, 'end', True)
        if neg: sv += txt(x0 - 14, 150, '-i', '#c0392b', 14, 'end', True)
        if note_: sv += txt(350, 184, note_, '#5b6773', 14)
        return svg(700, 198 if note_ else 168, sv, label or title)
    S1 = fig(letters('Python', 'Chuỗi là dãy ký tự, mỗi ký tự có số thứ tự (chỉ số)', note_='Chỉ số xuôi bắt đầu từ 0 (xanh); chỉ số ngược bắt đầu từ -1 (đỏ).'), 'Python đếm chỉ số từ <b>0</b>, không phải từ 1. Chỉ số âm đếm ngược từ cuối.')
    S2 = fig(letters('Xin chào', 'Dấu cách cũng là một ký tự: "Xin chào" có độ dài 8', hl=(3,), note_='len("Xin chào") = 8 vì tính cả dấu cách (ký hiệu ␣).', neg=False), '<code>len()</code> đếm mọi ký tự, kể cả dấu cách và dấu câu.')
    S3 = fig(letters('Python', 's[2:5] lấy chỉ số 2, 3, 4 (dừng TRƯỚC 5)', hl=(2, 3, 4), neg=False, note_='s[a:b] lấy từ a đến b-1: kết quả “tho”.'), 'Cắt chuỗi <code>s[a:b]</code> lấy từ chỉ số a và <b>dừng trước</b> b. Đếm số ký tự lấy được là b − a.')
    S4 = fig(cmp_fig('Các kiểu cắt thường dùng với s = "Python"', [('bl', 'Đầu chuỗi', ['s[:3]'], '"Pyt"', 'bỏ a = từ 0'), ('gr', 'Cuối chuỗi', ['s[3:]'], '"hon"', 'bỏ b = tới hết'), ('ye', 'Cách một', ['s[::2]'], '"Pto"', 'bước nhảy 2'), ('pu', 'Đảo ngược', ['s[::-1]'], '"nohtyP"', 'bước -1')], 232),
        'Có thể bỏ a hoặc b. Thêm tham số thứ ba để nhảy cách; bước -1 là đi ngược.')
    S5 = fig(cmp_fig('Ghép và lặp chuỗi', [('bl', 'Ghép bằng +', ['"Xin" + " " + "chào"'], '"Xin chào"', 'nối đầu-cuối'), ('gr', 'Lặp bằng *', ['"ha" * 3'], '"hahaha"', 'nhân bản chữ'), ('rd', 'Cộng chữ với số', ['"Tuổi: " + 13'], 'TypeError', 'phải đổi kiểu')], 232),
        'Chữ cộng chữ thì ghép; chữ nhân số thì lặp; chữ cộng số thì lỗi: dùng f-string hoặc <code>str()</code>.')
    fa = ARR + txt(350, 24, 'Giải phẫu một f-string', '#17406b', 17, bold=True) + mono(40, 112, 'f"Mình là {ten}, {tuoi} tuổi."', '#17406b', 24)
    cw = 24 * 0.6
    fa += '<rect x="%.1f" y="88" width="%.1f" height="34" rx="5" fill="none" stroke="#d9822b" stroke-width="2.5"/>' % (40, cw)
    fa += '<rect x="%.1f" y="88" width="%.1f" height="34" rx="5" fill="none" stroke="#1f6fb2" stroke-width="2.5"/>' % (40 + cw * 10, cw * 5)
    fa += '<rect x="%.1f" y="88" width="%.1f" height="34" rx="5" fill="none" stroke="#2a8a4a" stroke-width="2.5"/>' % (40 + cw * 17, cw * 6)
    fa += arr(40 + cw * 20, 62, 40 + cw * 20, 84, '#2a8a4a') + txt(40 + cw * 20 + 14, 52, '③ {tuoi + 1} tính được cả biểu thức', '#2a8a4a', 14, 'start', True)
    fa += arr(40 + cw * 12.5, 164, 40 + cw * 12.5, 128, '#1f6fb2') + txt(40 + cw * 12.5 + 8, 184, '② {ten} → giá trị của biến', '#1f6fb2', 14, 'start', True)
    fa += arr(40 + cw / 2, 210, 40 + cw / 2, 128, '#d9822b') + txt(40 + cw / 2 + 10, 226, '① chữ f đứng trước dấu nháy', '#d9822b', 14, 'start', True)
    fa += txt(560, 150, 'Kết quả:', '#5b6773', 14, 'middle', True) + txt(560, 172, 'Mình là Lan, 13 tuổi.', '#17406b', 15, 'middle', True)
    S6 = fig(svg(700, 246, fa, 'Giải phẫu f-string'), 'Chữ <b>f</b> trước dấu nháy cho phép nhét giá trị biến và cả biểu thức vào chuỗi qua cặp ngoặc nhọn.')
    S7 = fig(grid_fig('Phương thức chuỗi hay dùng', ['Phương thức', 'Việc làm', 'Ví dụ', 'Kết quả'],
        [['.upper()', 'viết HOA tất cả', '"abc".upper()', '"ABC"'], ['.lower()', 'viết thường tất cả', '"ABC".lower()', '"abc"'], ['.strip()', 'cắt khoảng trắng 2 đầu', '"  a ".strip()', '"a"'], ['.replace(a, b)', 'thay a bằng b', '"cat".replace("c", "b")', '"bat"'], ['.split()', 'tách thành danh sách', '"a b c".split()', "['a','b','c']"], ['.find(x)', 'vị trí của x (-1 nếu không có)', '"hello".find("l")', '2']], [160, 220, 230, 120], label='Các phương thức chuỗi'),
        'Phương thức gọi bằng dấu chấm sau tên chuỗi và luôn có cặp ngoặc <code>( )</code>, kể cả khi trong ngoặc không có gì.')
    S8 = fig(cmp_fig('Tìm trong chuỗi: find và in', [('bl', 'Vị trí', ['cau.find("học")'], '8', 'chỉ số xuất hiện đầu'), ('rd', 'Không có', ['cau.find("Java")'], '-1', 'không báo lỗi'), ('gr', 'Có hay không', ['"Python" in cau'], 'True', 'câu hỏi đúng/sai')], 232),
        '<code>find</code> trả về <b>vị trí</b> hoặc -1; <code>in</code> trả về <b>đúng/sai</b>. Chọn theo câu hỏi cần trả lời.')
    sj = ARR + txt(350, 24, 'split tách, join ghép: hai phép ngược nhau', '#17406b', 17, bold=True)
    sj += box(14, 48, 200, 60, '#e6f1fb', '#1f6fb2', ['"Lan Minh Hà"'], 17, bold=True) + arr(216, 70, 300, 70, '#d9822b') + txt(258, 62, '.split()', '#d9822b', 14, bold=True)
    sj += box(302, 48, 384, 60, '#e5f5ea', '#2a8a4a', ['["Lan", "Minh", "Hà"]'], 17, bold=True)
    sj += arr(494, 112, 494, 148, '#7b4bb3') + txt(540, 136, '", ".join(…)', '#7b4bb3', 14, 'start', True)
    sj += box(302, 150, 384, 50, '#f1e8fb', '#7b4bb3', ['"Lan, Minh, Hà"'], 17, bold=True) + txt(150, 180, 'tách theo dấu cách', '#5b6773', 14)
    S9 = fig(svg(700, 214, sj, 'split và join'), '<code>split</code> chuỗi → danh sách các mẩu; <code>"nối".join(danh_sách)</code> nối ngược lại bằng dấu em chọn.')
    S10 = fig(cmp_fig('Chuỗi không sửa được từng chữ', [('rd', 'Sửa tại chỗ', ['s = "Python"', 's[0] = "J"'], 'TypeError', 'chuỗi là “bất biến”'), ('gr', 'Tạo chuỗi mới', ['s = "J" + s[1:]'], '"Jython"', 'ghép phần cũ với chữ mới')], 232),
        'Muốn đổi một chữ, em tạo chuỗi mới từ những phần có sẵn rồi gán lại cho biến.')
    S11 = flowrow(['Xác định|việc cần làm', 'Chọn: cắt,|ghép hay tìm', 'Viết lệnh|đếm chỉ số', 'Đoán kết|quả', 'Chạy,|kiểm chứng'], 'Quy trình xử lý chuỗi', colors=['#e6f1fb', '#e6f1fb', '#fff4d6', '#fff4d6', '#e5f5ea'])
    S12 = ptrace(tr, pick=[0, 1, 2, 3], maxn=6, captions=['Biến <b>ten</b> = “nguyen van an”.', '<b>ho</b> = ten[:6] = “nguyen” (6 ký tự đầu).', '<b>cuoi</b> = ten[-2:] = “an” (2 ký tự cuối).', 'In hai biến viết HOA: NGUYEN AN.'])

    cmd23 = cmdx('Phân tích từng phần các câu lệnh xử lý chuỗi. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', [
        ['<code>len(s)</code>', 'Đếm số ký tự (kể cả dấu cách).', 'Quên cặp ngoặc, Python không báo lỗi mà trả về chính cái hàm:' + R('s = "Python"\nprint(len)')],
        ['<code>s[i]</code> – chỉ số', 'Lấy đúng một ký tự ở vị trí i (từ 0).', 'Chỉ số vượt độ dài (chuỗi 6 ký tự không có s[6]):' + ERR('s = "Python"\nprint(s[6])')],
        ['<code>s[-1]</code> – chỉ số âm', 'Đếm từ cuối: -1 là ký tự cuối.', 'Chỉ số âm quá xa cũng lỗi:' + ERR('s = "Python"\nprint(s[-7])')],
        ['<code>s[a:b]</code> – cắt', 'Lấy từ a đến <b>trước</b> b; cắt vượt giới hạn không báo lỗi.', 'Cắt quá dài vẫn ra chuỗi (không lỗi):' + R('s = "Python"\nprint(s[2:100])\nprint(s[10:20] == "")')],
        ['<code>s[::-1]</code>', 'Bước -1 là đi ngược nên đảo chuỗi.', 'Bỏ <code>-1</code> thì chuỗi y nguyên:' + R('s = "Python"\nprint(s[::1])\nprint(s[::-1])')],
        ['<code>+</code> ghép chuỗi', 'Nối hai chuỗi liền nhau, không tự thêm dấu cách.', 'Ghép chuỗi với số:' + ERR('print("Tuổi: " + 13)') + 'Quên dấu cách trong chuỗi:' + R('print("Xin" + "chào")')],
        ['<code>*</code> lặp chuỗi', 'Chuỗi nhân số nguyên: lặp lại số lần đó.', 'Nhân hai chuỗi với nhau:' + ERR('print("ha" * "ha")')],
        ['<code>f"…{biến}…"</code>', 'Chuỗi định dạng: <code>{ }</code> được thay bằng giá trị.', 'Quên chữ <b>f</b> trước dấu nháy, ngoặc nhọn bị in nguyên:' + R('ten = "Lan"\nprint("Mình là {ten}")')],
        ['<code>.upper()  .lower()</code>', 'Viết hoa hoặc viết thường toàn bộ.', 'Quên ngoặc <code>( )</code>:' + R('print("abc".upper)')],
        ['<code>.strip()</code>', 'Cắt khoảng trắng ở hai đầu; <b>trả về chuỗi mới</b>.', 'Gọi mà không lưu kết quả, chuỗi gốc không đổi:' + R('s = "  a  "\ns.strip()\nprint(len(s))\ns = s.strip()\nprint(len(s))')],
        ['<code>.replace(a, b)</code>', 'Thay mọi a trong chuỗi bằng b.', 'Thiếu một tham số:' + ERR('print("cat".replace("c"))')],
        ['<code>.find(x)</code>  và  <code>x in s</code>', '<code>find</code> cho vị trí hoặc -1; <code>in</code> cho đúng/sai.', 'Dùng <code>find</code> như đúng/sai là bẫy: ' + R('s = "hello"\nprint(s.find("h"))\nprint(bool(s.find("h")))') + 'Ký tự ở vị trí 0 cho kết quả 0, bị hiểu là “sai”!'],
        ['<code>.split()</code>  và  <code>sep.join(ds)</code>', 'Tách chuỗi thành danh sách; nối danh sách thành chuỗi.', 'Nối danh sách có số bên trong:' + ERR('print(", ".join([1, 2]))')]])

    P['c2b3'] = std2('Bài 2.3 · Chuỗi: cắt, ghép, tìm', 'Chuỗi là dãy ký tự: đếm vị trí, cắt từng đoạn, ghép lại và tìm trong đó.',
        ('Dùng được chỉ số, cắt chuỗi, ghép, f-string và các phương thức upper, strip, replace, find, split; tự đoán và kiểm chứng kết quả', 'Đã biết biến và phép toán (Bài 2.1, 2.2)', 'Chương trình xử lý tên người và mã số bằng cắt và ghép chuỗi'),
        ['Văn bản có mặt ở mọi nơi: tên, địa chỉ, mật khẩu, tin nhắn. Xử lý chuỗi là kỹ năng dùng hằng ngày của người lập trình.', 'Hiểu <b>chỉ số bắt đầu từ 0</b> là chìa khóa cho cả danh sách, bảng và tệp ở các chương sau.', '<b>f-string</b> giúp in thông tin gọn gàng, dễ đọc, không cần ghép từng mảnh.', 'Biết dùng các phương thức có sẵn giúp em không phải tự viết lại những việc đã có người làm.'],
        ol(['Xác định việc cần làm: lấy một phần, ghép thêm, đổi chữ hay tìm một đoạn?', 'Vẽ chuỗi thành các ô, <b>đánh số 0, 1, 2…</b> rồi tìm vị trí cần lấy.', 'Chọn công cụ: <code>s[a:b]</code> để cắt, <code>+</code>/f-string để ghép, <code>.find()</code> hoặc <code>in</code> để tìm.', 'Đoán kết quả trước, chạy, rồi kiểm chứng (ví dụ ghép lại các phần xem có ra chuỗi gốc không).']),
        think(['<b>Phản biện:</b> “Em đếm vị trí từ 0 hay từ 1?” – đa số lỗi chuỗi đến từ chỗ này.', '<b>Nghĩ ngược:</b> muốn kết quả là “Python”, từ chuỗi “Lập trình Python” em phải lấy từ vị trí nào đến đâu?', '<b>Kiểm chứng bằng cách ghép lại:</b> <code>s[:k] + s[k:] == s</code> luôn đúng với mọi k; dùng nó để thử cách cắt của mình.']),
        'Ứng dụng vào Python',
        li(['Chỉ số và độ dài:']) + R(s1) + 'Cắt chuỗi:' + R(sl) + 'Ghép và lặp:' + R(cat) + 'f-string:' + R(fs) + 'Phương thức biến đổi:' + R(meth) + 'Tìm trong chuỗi:' + R(find) + 'Tách và ghép danh sách chữ:' + R(jn),
        cmd23,
        S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8 + S9 + S10 + S11 + S12,
        [err('Đếm vị trí từ 1', 'Ký tự đầu là <code>s[0]</code>, không phải <code>s[1]</code>; chuỗi 6 ký tự có chỉ số cuối là 5:' + ERR('s = "Python"\nprint(s[len(s)]'), 'Ký tự cuối là <code>s[len(s) - 1]</code> hoặc ngắn gọn <code>s[-1]</code>.'),
         err('Nghĩ rằng s[a:b] lấy cả b', '<code>"Python"[2:5]</code> ra “tho” (3 ký tự), không có “n”.', 'Quy tắc: lấy từ a, dừng <b>trước</b> b; số ký tự lấy được là b − a.'),
         err('Cộng chữ với số', 'In tuổi mà viết <code>"Tuổi: " + 13</code> gây lỗi:' + ERR('print("Tuổi: " + 13)'), 'Dùng f-string <code>f"Tuổi: {13}"</code> hoặc đổi kiểu <code>"Tuổi: " + str(13)</code>.'),
         err('Quên gán kết quả của phương thức', '<code>s.strip()</code> không sửa s mà trả về chuỗi mới; nếu không gán lại thì mất:' + R('s = "  a  "\ns.strip()\nprint(len(s))'), 'Viết <code>s = s.strip()</code>.'),
         err('Quên chữ f trước f-string', R('ten = "Lan"\nprint("Xin chào {ten}")'), 'Thêm chữ <code>f</code> ngay trước dấu nháy mở: <code>f"Xin chào {ten}"</code>.')],
        [eg('Ví dụ 1: viết tắt tên', R('ho_ten = "Nguyễn Văn An"\nds = ho_ten.split()\nprint(ds[0][0] + ds[1][0] + ds[2][0])') + note('<code>ds[0][0]</code>: lấy mẩu đầu tiên, rồi lấy ký tự đầu của mẩu đó.')),
         eg('Ví dụ 2: kiểm tra chuỗi đối xứng', R('s = "level"\nprint(s == s[::-1])\nprint("Python" == "Python"[::-1])')),
         eg('Ví dụ 3: dọn dữ liệu nhập lộn xộn', R('raw = "   NGUYỄN văn AN  "\nprint(raw.strip().title())') + note('<code>.title()</code> viết hoa chữ cái đầu mỗi từ.'))],
        [('Cho <code>s = "Viet Nam"</code>. In ra ký tự đầu, ký tự cuối và độ dài của s.', R('s = "Viet Nam"\nprint(s[0])\nprint(s[-1])\nprint(len(s))') + note('Độ dài là 8 vì dấu cách cũng tính.'), None),
         ('Cho <code>s = "Lập trình Python"</code>. Chỉ dùng cắt chuỗi để lấy ra “Python”, “Lập” và chuỗi đảo ngược.', R('s = "Lập trình Python"\nprint(s[-6:])\nprint(s[:3])\nprint(s[::-1])'), None),
         ('Cho <code>ten = "nguyễn an"</code>. In ra tên với chữ cái đầu viết hoa: “Nguyễn an” (chỉ chữ đầu), rồi cách viết hoa chữ cái đầu mỗi từ.', R('ten = "nguyễn an"\nprint(ten[0].upper() + ten[1:])\nprint(ten.title())'), None),
         ('Kiểm tra xem “level” và “Python” có phải chuỗi đối xứng không (đọc xuôi ngược giống nhau). Rồi thử với “Madam” (chú ý hoa thường).', R('for s in ("level", "Python", "Madam"):\n    print(s, s == s[::-1], s.lower() == s.lower()[::-1])') + '<p>“Madam” đảo thành “madaM” nên so sánh trực tiếp là False; chuyển về chữ thường trước thì mới đúng.</p>', None),
         ('<b>Thử thách (nghĩ ngược):</b> Mã học sinh <code>"HS-2026-0148"</code>. Hãy tách năm (2026) và số thứ tự (148), in câu “Năm 2026, số thứ tự 148”, tính năm kế tiếp, rồi tự ghép lại từ các phần để kiểm chứng lại đúng bằng mã gốc.', R('ma = "HS-2026-0148"\nnam = ma[3:7]\nstt = ma[-4:]\nprint(f"Năm {nam}, số thứ tự {int(stt)}")\nprint(int(nam) + 1)\nprint("HS-" + nam + "-" + stt == ma)') + '<p>Cắt <code>ma[3:7]</code> lấy ký tự vị trí 3 đến 6. <code>int("0148")</code> bỏ các số 0 đầu thành 148. Dòng cuối ghép lại các phần và so với mã gốc: <code>True</code> nghĩa là cắt đúng.</p>', None)],
        '')

    # ===================================================== TÓM TẮT CHƯƠNG 2
    mm = ARR + txt(350, 24, 'Sơ đồ tóm tắt Chương 2', '#17406b', 17, bold=True) + box(260, 100, 180, 62, '#fff4d6', '#d9822b', ['Chương 2', 'Biến, số và chuỗi'], 15, bold=True)
    br = [(24, 40, 'Biến (Bài 2.1)', 'tên – giá trị – kiểu'), (24, 160, 'Số (Bài 2.2)', '+ - * / // % **, ngoặc'), (496, 40, 'Chuỗi (Bài 2.3)', 'chỉ số, cắt, ghép, tìm'), (496, 160, 'Nhập – xuất (Bài 2.4)', 'input, int, print, f-string')]
    for x, y, a, b in br:
        mm += box(x, y, 180, 60, '#e6f1fb', '#1f6fb2', [a, b], 14, bold=True)
        mm += arr(x + 182 if x < 270 else x - 2, y + 30, 258 if x < 270 else 442, 130, '#6b7785')
    M1 = fig(svg(700, 250, mm, 'Sơ đồ tóm tắt chương 2'), 'Bốn nhánh của Chương 2: biến lưu dữ liệu, số và chuỗi là hai loại dữ liệu chính, nhập – xuất nối chương trình với người dùng.')
    ba = ARR + txt(350, 24, 'Trước và sau Chương 2', '#17406b', 17, bold=True)
    ba += box(14, 44, 330, 150, '#f3f4f6', '#9db4c9', [], 14) + txt(179, 68, 'Trước chương 2', '#5b6773', 15, bold=True)
    for i, l in enumerate(['Chỉ in chữ cố định', 'Chưa biết lưu giá trị', 'Chưa tách, ghép được chữ']): ba += txt(30, 104 + i * 28, '• ' + l, '#5b6773', 14, 'start')
    ba += box(356, 44, 330, 150, '#e5f5ea', '#2a8a4a', [], 14) + txt(521, 68, 'Sau chương 2', '#2a8a4a', 15, bold=True)
    for i, l in enumerate(['Lưu dữ liệu vào biến có tên', 'Tính toán và đổi đơn vị bằng // %', 'Cắt, ghép, tìm trong chuỗi']): ba += txt(372, 104 + i * 28, '✓ ' + l, '#17406b', 14, 'start')
    M2 = fig(svg(700, 212, ba, 'Trước và sau chương 2'), 'Chương trình của em giờ biết “nhớ” và “tính”, không chỉ “nói”.')
    ck = ARR + txt(350, 24, 'Bảng tự đánh giá: tô màu ô em làm được', '#17406b', 17, bold=True)
    for i, l in enumerate(['Tạo biến và đổi giá trị', 'Phân biệt int, float, str', 'Dùng // và % đúng chỗ', 'Viết biểu thức có ngoặc', 'Cắt chuỗi s[a:b]', 'Dùng f-string để in']):
        x = 14 + (i % 2) * 345; y = 44 + (i // 2) * 52; ck += '<rect x="%d" y="%d" width="330" height="42" rx="8" fill="#fff" stroke="#9db4c9"/><rect x="%d" y="%d" width="22" height="22" rx="4" fill="#fff" stroke="#1f6fb2" stroke-width="2"/>' % (x, y, x + 12, y + 10) + txt(x + 46, y + 27, l, '#1c2733', 14, 'start')
    M3 = fig(svg(700, 206, ck, 'Bảng tự đánh giá chương 2'), 'Chưa tô được ô nào thì quay lại bài tương ứng, đừng bỏ qua.')
    proj = 'ten = input()\nso_ly = int(input())\ngia = 28000\ntong = gia * so_ly\ngiam = tong // 10\ntra = tong - giam\nprint("=" * 32)\nprint(" " * 8 + "PHIẾU THANH TOÁN")\nprint("=" * 32)\nprint(f"Khách: {ten.strip().title()}")\nprint(f"Số ly: {so_ly} x {gia}")\nprint(f"Tạm tính: {tong}")\nprint(f"Giảm 10%: -{giam}")\nprint(f"Phải trả: {tra}")\nprint("=" * 32)'
    out_ = run(proj, '  nguyễn thị lan \n3\n')
    po = ARR + txt(350, 24, 'Kết quả dự án: phiếu thanh toán', '#17406b', 17, bold=True) + box(150, 40, 400, 200, '#fff', '#6b7785', [], 14)
    for i, l in enumerate(out_.split('\n')): po += mono(166, 70 + i * 22, l, '#1c2733', 13)
    M4 = fig(svg(700, 254, po, 'Kết quả phiếu thanh toán'), 'Phiếu do dự án tạo ra với tên “  nguyễn thị lan ” và 3 ly.')
    tab = table(['Điều cần nhớ', 'Ví dụ', 'Ý nghĩa'], [['<code>//</code>  <code>%</code>', '<code>135 // 60</code>, <code>135 % 60</code>', 'Phần nguyên và phần dư'], ['Thứ tự phép toán', '<code>2 + 3 * 4</code> = 14', 'Ngoặc → ** → * / // % → + -'], ['<code>int</code> / <code>float</code>', '<code>8 // 2</code> = 4, <code>8 / 2</code> = 4.0', '<code>/</code> luôn ra float'], ['Chỉ số bắt đầu từ 0', '<code>s[0]</code>, <code>s[-1]</code>', 'Ký tự đầu, ký tự cuối'], ['Cắt chuỗi', '<code>s[2:5]</code>', 'Từ 2, dừng trước 5'], ['Ghép / lặp', '<code>"a" + "b"</code>, <code>"ha" * 3</code>', 'Nối / nhân bản'], ['f-string', '<code>f"Tuổi {t}"</code>', 'Nhét biến vào chuỗi'], ['Phương thức chuỗi', '<code>.upper() .strip() .find()</code>', 'Luôn có cặp ngoặc; trả về chuỗi mới']])
    top5 = ''.join(err(a, b, c) for a, b, c in [('Chia cho 0', 'ZeroDivisionError với <code>/</code>, <code>//</code> và <code>%</code>.', 'Nghĩ trước: số chia có thể bằng 0 không?'), ('Nhầm / với //', 'Cần số nguyên (số nhóm) mà dùng <code>/</code> sẽ ra số lẻ.', 'Hỏi: đáp số có thể lẻ không?'), ('Đếm chỉ số từ 1', 'IndexError hoặc lấy nhầm ký tự.', 'Chỉ số đầu là 0, cuối là len − 1 (hoặc -1).'), ('Cộng chữ với số', 'TypeError.', 'Dùng f-string hoặc <code>str()</code>.'), ('Quên gán kết quả phương thức', '<code>s.strip()</code> không đổi s.', 'Viết <code>s = s.strip()</code>.')])
    quiz = [('<code>17 // 5</code> và <code>17 % 5</code> bằng bao nhiêu?', 'Bằng 3 và 2: 3 × 5 + 2 = 17.'), ('<code>2 + 3 * 4</code> ra mấy, vì sao?', 'Ra 14: nhân trước (3 × 4 = 12) rồi cộng 2; muốn cộng trước thì thêm ngoặc.'), ('<code>8 / 2</code> ra kiểu gì?', 'Ra 4.0, kiểu float; dấu <code>/</code> luôn cho số thực.'), ('Với <code>s = "Python"</code>, <code>s[1:4]</code> ra gì?', 'Ra “yth” (chỉ số 1, 2, 3).'), ('Làm sao in “Mình 13 tuổi” khi tuổi nằm trong biến <code>t</code>?', 'Dùng <code>print(f"Mình {t} tuổi")</code> (hoặc <code>"Mình " + str(t) + " tuổi"</code>).'), ('Vì sao <code>s.strip()</code> đứng một mình không đổi được s?', 'Vì chuỗi không sửa tại chỗ; phương thức trả về chuỗi mới, cần gán lại <code>s = s.strip()</code>.')]
    qh = ''.join('<details class="tans"><summary>Câu %d. %s</summary><p>%s</p></details>' % (i + 1, q, a) for i, (q, a) in enumerate(quiz))
    P['c2t'] = {'title': 'Tóm tắt Chương 2 · Biến, số và chuỗi', 'sub': 'Hệ thống lại kiến thức, lỗi hay gặp và làm dự án phiếu thanh toán.',
        'html': '\n'.join([tsum('Hệ thống lại Chương 2 và tự kiểm tra; hoàn thành dự án “phiếu thanh toán quán trà sữa”', 'Đã học Bài 2.1 đến 2.4', 'Bảng ghi nhớ của em và chương trình phiếu thanh toán chạy đúng'),
            card(1, 'Sơ đồ tóm tắt chương', M1 + M2), card(2, 'Bảng ghi nhớ nhanh', tab), card(3, '5 lỗi hay gặp nhất của chương', top5),
            card('+', 'Em đã làm được gì? (tự đánh giá)', M3),
            card(4, 'Em đã học được thói quen tư duy nào?', think(['<b>Chọn đúng công cụ</b> trước khi gõ: cần số nhóm, phần dư hay số thập phân?', '<b>Kiểm chứng bằng cách làm ngược</b>: <code>nhóm × cỡ + dư == tổng</code>; <code>s[:k] + s[k:] == s</code>.', '<b>Đếm từ 0</b> và nhớ “dừng trước”.'], 'Thói quen của Chương 2')),
            chap('Dự án nhỏ cuối chương'),
            '<section class="tcard tprac"><h4><span class="tn">DA</span>Dự án: phiếu thanh toán quán trà sữa <span class="lvl">★★★☆</span></h4><p>Viết chương trình nhập <b>tên khách</b> (có thể gõ thừa dấu cách, viết thường) và <b>số ly</b>, giá cố định 28000 đồng/ly, giảm 10%% trên tổng. In ra <b>phiếu thanh toán</b> có khung, tên khách viết đúng chuẩn, số ly, tạm tính, tiền giảm và số tiền phải trả. Dùng đủ: <code>input</code>, <code>int</code>, <code>*</code>, <code>//</code>, f-string, <code>.strip()</code>, <code>.title()</code>.</p><details class="tans"><summary>Xem bài mẫu và kết quả chạy</summary>%s%s<p>Tên “  nguyễn thị lan ” được dọn gọn bằng <code>.strip().title()</code>. Tiền giảm dùng <code>// 10</code> để ra số nguyên đồng. Kiểm chứng: 84000 − 8400 = 75600.</p></details></section>' % (code('# Dự án chương 2: phiếu thanh toán\n' + proj, out_), M4),
            chap('Tự kiểm tra (6 câu)'), '<section class="tcard">%s</section>' % qh,
            card(5, 'Chương sau học gì?', li(['<b>Chương 3 – Cấu trúc rẽ nhánh:</b> máy tự quyết định làm việc này hay việc kia theo điều kiện (nếu… thì…).', 'Em đã biết cho máy <b>nhớ và tính</b>; sang chương 3 em sẽ cho máy <b>lựa chọn</b>, ví dụ báo “đủ tiền hay chưa”, “chẵn hay lẻ”.']))])}
    return P
