"""Giáo trình Python 12–18 – Chương 3: Bài 3.1 Biểu thức lô-gíc, Bài 3.3 Kiểm thử giá trị biên, Tóm tắt chương 3.
Mọi kết quả chạy, thông báo lỗi lấy từ lần chạy thật."""
from tuduy_py3 import *
from tuduy_py3 import cmp_fig, grid_fig


def build():
    P = {}

    # ===================================================== BÀI 3.1  BIỂU THỨC LÔ-GÍC
    cmpc = 'a = 7\nb = 5\nprint(a > b)\nprint(a == b)\nprint(a != b)\nprint(a <= 7)\nprint(type(a > b))'
    logic = 'tuoi = 13\nprint(tuoi >= 12 and tuoi <= 18)\nprint(tuoi < 12 or tuoi > 18)\nprint(not tuoi >= 12)'
    chain = 'x = 15\nprint(10 <= x <= 20)\nprint(10 <= x and x <= 20)\nprint(x % 2 == 0)'
    strc = 'print("a" == "a")\nprint("a" == "A")\nprint("10" < "9")\nprint(10 < 9)\nprint("Lan" in "Lan Anh")'
    truthy = 'print(bool(0))\nprint(bool(0.0))\nprint(bool(""))\nprint(bool(5))\nprint(bool("a"))\nprint(bool(" "))'
    prec = 'print(True or False and False)\nprint((True or False) and False)\nprint(not True or True)'
    pt1 = 'tuoi = 13\nhop_le = tuoi >= 12 and tuoi <= 18\nprint(hop_le)'

    B1 = fig(cmp_fig('Kiểu bool chỉ có hai giá trị', [('gr', 'True (đúng)', ['3 > 2'], 'True', 'điều kiện thỏa'), ('rd', 'False (sai)', ['3 < 2'], 'False', 'điều kiện không thỏa'), ('rd', 'Hoa thường khác nhau', ['"ba" == "Ba"'], 'False', 'chữ hoa khác chữ thường')], 232),
        'Mỗi phép so sánh cho đúng một trong hai giá trị: <b>True</b> hoặc <b>False</b>. Viết hoa chữ cái đầu, không có dấu nháy.')
    B2 = fig(grid_fig('Sáu phép so sánh (a = 7, b = 5)', ['Ký hiệu', 'Ý nghĩa', 'Ví dụ', 'Kết quả'],
        [['==', 'bằng nhau', 'a == b', 'False'], ['!=', 'khác nhau', 'a != b', 'True'], ['>', 'lớn hơn', 'a > b', 'True'], ['<', 'nhỏ hơn', 'a < b', 'False'], ['>=', 'lớn hơn hoặc bằng', 'a >= 7', 'True'], ['<=', 'nhỏ hơn hoặc bằng', 'a <= b', 'False']], [90, 260, 170, 120], label='Các phép so sánh'),
        'Chú ý: “bằng” là <b>hai</b> dấu <code>==</code>; một dấu <code>=</code> dành cho phép gán.')
    B3 = fig(cmp_fig('Một dấu = và hai dấu ==', [('ye', 'x = 5', ['x = 5'], 'x thành 5', 'GÁN giá trị cho biến'), ('gr', 'x == 5', ['x == 5'], 'True hoặc False', 'SO SÁNH, được câu trả lời'), ('rd', 'Nhầm trong print', ['print(x = 5)'], 'TypeError', 'Python hiểu là đặt tham số')], 232),
        '<code>=</code> bảo máy “đặt giá trị”, <code>==</code> hỏi máy “có bằng nhau không?”. Hai việc khác hẳn nhau.')
    t_and = [['True', 'True', 'True'], ['True', 'False', 'False'], ['False', 'True', 'False'], ['False', 'False', 'False']]
    B4 = fig(grid_fig('Bảng chân trị của and: cả hai cùng đúng mới đúng', ['A', 'B', 'A and B'], t_and, [200, 200, 220], hl=[0], label='Bảng and'), 'Giống câu “đạt cả Toán <b>và</b> Văn”: chỉ cần một môn trượt là cả câu sai.')
    t_or = [['True', 'True', 'True'], ['True', 'False', 'True'], ['False', 'True', 'True'], ['False', 'False', 'False']]
    B5 = fig(grid_fig('Bảng chân trị của or: chỉ cần một bên đúng là đúng', ['A', 'B', 'A or B'], t_or, [200, 200, 220], hl=[3], label='Bảng or'), 'Giống câu “được thưởng nếu đạt Toán <b>hoặc</b> Văn”: chỉ khi trượt cả hai mới không được.')
    B6 = fig(cmp_fig('not đảo ngược đúng – sai', [('gr', 'not True', ['not True'], 'False', 'đảo ngược'), ('rd', 'not False', ['not False'], 'True', 'đảo ngược'), ('bl', 'not với so sánh', ['not 3 > 5'], 'True', 'not (3 > 5) = not False')], 232),
        '<code>not</code> đặt trước một giá trị đúng/sai để đảo nó; nó tính sau phép so sánh.')
    # trục số
    nl = ARR + txt(350, 24, 'Khoảng 10 <= x <= 20 trên trục số', '#17406b', 17, bold=True)
    def X(v): return 40 + v * 20.6
    nl += '<rect x="%.1f" y="100" width="%.1f" height="26" fill="#e5f5ea" stroke="#2a8a4a" stroke-width="2"/>' % (X(10), X(20) - X(10)) + '<line x1="40" y1="113" x2="660" y2="113" stroke="#6b7785" stroke-width="2.5"/>'
    for v in range(0, 31, 5): nl += '<line x1="%.1f" y1="106" x2="%.1f" y2="120" stroke="#6b7785" stroke-width="2"/>' % (X(v), X(v)) + txt(X(v), 142, str(v), '#5b6773', 14)
    for v, ok in [(8, 0), (10, 1), (15, 1), (20, 1), (23, 0)]:
        c = '#2a8a4a' if ok else '#c0392b'; nl += '<circle cx="%.1f" cy="113" r="7" fill="%s"/>' % (X(v), c) + txt(X(v), 84, 'x = %d' % v, c, 14, bold=True) + txt(X(v), 66, 'True' if ok else 'False', c, 13, bold=True)
    nl += txt(350, 180, 'Hai đầu 10 và 20 đều thuộc khoảng vì dùng <= (có dấu bằng).', '#5b6773', 14)
    B7 = fig(svg(700, 196, nl, 'Trục số và điều kiện'), 'Viết <code>10 &lt;= x &lt;= 20</code> như trong toán: Python hiểu đúng là “x nằm giữa 10 và 20 (kể cả hai đầu)”.')
    B8 = fig(grid_fig('Thứ tự thực hiện: so sánh → not → and → or', ['Bậc', 'Phép', 'Ví dụ', 'Kết quả'],
        [['1', 'so sánh  == != < > <= >=', '3 > 2', 'True'], ['2', 'not', 'not False', 'True'], ['3', 'and', 'True or False and False', 'True'], ['4', 'or', '(True or False) and False', 'False']], [70, 270, 250, 100], label='Bậc ưu tiên lô-gíc'),
        '<code>and</code> được tính trước <code>or</code> (giống nhân trước cộng). Nghi ngờ thì thêm ngoặc cho rõ.')
    B9 = fig(cmp_fig('So sánh chữ và so sánh số', [('gr', 'Số', ['10 < 9'], 'False', 'so theo giá trị'), ('rd', 'Chữ (từng ký tự)', ['"10" < "9"'], 'True', '"1" đứng trước "9"'), ('bl', 'Chữ có trong chữ', ['"Lan" in "Lan Anh"'], 'True', 'kiểm tra chứa')], 232),
        'Chữ so sánh từng ký tự từ trái sang, nên <code>"10" &lt; "9"</code> là True. Muốn so sánh số thì phải đổi sang số bằng <code>int()</code>.')
    B10 = fig(grid_fig('Mọi giá trị đều “đúng” hoặc “sai” khi đặt vào điều kiện', ['Giá trị', 'bool(...)', 'Giá trị', 'bool(...)'],
        [['0', 'False', '5', 'True'], ['0.0', 'False', '-3', 'True'], ['""  (chữ rỗng)', 'False', '"a"', 'True'], ['""  (chữ rỗng)', 'False', '" " (dấu cách)', 'True']], [180, 130, 190, 130], label='Giá trị đúng sai'),
        '“Rỗng” và số 0 tính là sai; mọi thứ còn lại tính là đúng. Dấu cách vẫn là một ký tự nên <code>" "</code> tính là đúng.')
    B11 = flowrow(['Nói điều|kiện bằng lời', 'Chia thành|các ý nhỏ', 'Dịch sang|so sánh', 'Nối bằng|and / or', 'Thử với|giá trị biên'], 'Cách viết một điều kiện', colors=['#e6f1fb', '#e6f1fb', '#fff4d6', '#fff4d6', '#e5f5ea'])
    B12 = ptrace(pt1, pick=[0, 1, 2], maxn=6, captions=['Gán <b>tuoi</b> = 13.', '<b>hop_le</b> = (13 >= 12) and (13 <= 18) = True and True = True.', 'In giá trị True.'])

    cmd31 = cmdx('Phân tích các ký hiệu của bài. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', [
        ['<code>==</code> (bằng)', 'So sánh hai giá trị, cho True hoặc False.', 'Dùng một dấu <code>=</code> trong điều kiện:' + ERR('x = 5\nprint(x = 5)')],
        ['<code>!=</code> (khác)', 'True khi hai giá trị khác nhau.', 'Viết kiểu toán học <code>≠</code> không có trong Python:' + ERR('print(3 ≠ 4)')],
        ['<code>&gt;  &lt;  &gt;=  &lt;=</code>', 'Lớn hơn, nhỏ hơn, và các dạng có dấu bằng.', 'Đặt dấu bằng sai thứ tự (<code>=&lt;</code>):' + ERR('print(3 =< 4)')],
        ['so sánh số với chữ', 'Chỉ so sánh được cùng loại (số với số, chữ với chữ), trừ <code>==</code>.', 'Số lớn hơn chữ:' + ERR('print(5 < "7")') + '<code>==</code> giữa số và chữ không lỗi mà cho False:' + R('print(5 == "5")')],
        ['<code>and</code>', 'Đúng khi <b>cả hai</b> vế đúng.', 'Viết thiếu vế trái ở vế sau:' + ERR('x = 5\nprint(x > 1 and < 10)')],
        ['<code>or</code>', 'Đúng khi <b>ít nhất một</b> vế đúng.', 'Viết <code>x == 1 or 2</code> như lời nói: không báo lỗi nhưng luôn “đúng” vì 2 tính là đúng:' + R('x = 5\nprint(x == 1 or 2)\nprint(x == 1 or x == 2)')],
        ['<code>not</code>', 'Đảo ngược đúng – sai.', 'Thiếu ngoặc khi muốn đảo cả điều kiện kép: <code>not a and b</code> chỉ đảo <code>a</code>:' + R('print(not True and False)\nprint(not (True and False))')],
        ['<code>10 &lt;= x &lt;= 20</code>', 'So sánh liên tiếp: x nằm trong khoảng (kể cả hai đầu).', 'Viết sai theo kiểu nói: <code>x == 10 or 20</code> luôn đúng (xem hàng <code>or</code>); đúng phải là <code>x == 10 or x == 20</code>.'],
        ['<code>True</code> / <code>False</code>', 'Hai giá trị đúng – sai, viết hoa chữ đầu.', 'Viết thường:' + ERR('print(true)')],
        ['<code>x in s</code>', 'Kiểm tra chữ x có nằm trong chuỗi s không.', 'Đảo chỗ hai vế:' + R('print("Lan" in "Lan Anh")\nprint("Lan Anh" in "Lan")')]])

    P['c3b1'] = std2('Bài 3.1 · Biểu thức lô-gíc (Boolean)', 'Máy chỉ hiểu hai câu trả lời: đúng hoặc sai. Biết viết điều kiện là biết cách bảo máy quyết định.',
        ('Viết được phép so sánh và điều kiện kép bằng and, or, not; hiểu bảng chân trị; đoán đúng kết quả True hoặc False', 'Đã biết biến, số và chuỗi (Chương 2)', 'Bảng chân trị của riêng em và các điều kiện kiểm tra tuổi, điểm, năm nhuận'),
        ['Mọi quyết định của máy — “đủ tiền chưa?”, “mật khẩu đúng không?” — đều quy về một điều kiện đúng hoặc sai.', 'Bài này là nền cho <b>if</b> và <b>while</b>: không biết viết điều kiện thì không điều khiển được chương trình.', 'Học <b>and, or, not</b> giúp em ghép nhiều điều kiện đơn thành một điều kiện phức tạp mà vẫn chính xác.', 'Điều kiện viết sai thường không báo lỗi mà cho kết quả sai âm thầm — nên phải biết suy luận chắc chắn.'],
        ol(['Nói điều kiện bằng <b>lời</b> thật rõ (“tuổi từ 12 đến 18”).', 'Tách thành các ý nhỏ, mỗi ý là <b>một phép so sánh</b> (<code>tuoi &gt;= 12</code>, <code>tuoi &lt;= 18</code>).', 'Nối bằng <b>and</b> (cùng đúng) hoặc <b>or</b> (một trong hai); thêm ngoặc khi nghi ngờ thứ tự.', 'Thử với giá trị <b>ở biên</b> (12, 18) và <b>ngoài biên</b> (11, 19) rồi mới tin.']),
        think(['<b>Phản biện:</b> “và” trong lời nói và <code>and</code> trong code có luôn giống nhau không? Câu “Lan hoặc Minh” có thể là cả hai cùng đến không?', '<b>Nghĩ ngược:</b> muốn kết quả là True với đúng ba số 10, 15, 20, em phải viết điều kiện thế nào? Thử xem có chặn được 9 và 21 không.', '<b>Thói quen tốt:</b> luôn thử điều kiện với <i>hai giá trị ở hai phía</i> của biên.']),
        'Ứng dụng vào Python',
        li(['So sánh hai số:']) + R(cmpc) + 'Điều kiện kép về tuổi:' + R(logic) + 'So sánh liên tiếp và chẵn lẻ:' + R(chain) + 'So sánh chữ:' + R(strc) + 'Đúng – sai của các giá trị thường:' + R(truthy) + 'Thứ tự and, or, not:' + R(prec),
        cmd31,
        B1 + B2 + B3 + B4 + B5 + B6 + B7 + B8 + B9 + B10 + B11 + B12,
        [err('Dùng = thay cho ==', 'Một dấu <code>=</code> là gán, không phải so sánh:' + ERR('x = 5\nprint(x = 5)'), 'Hỏi “có bằng không?” thì dùng <code>==</code>.'),
         err('Viết điều kiện như lời nói: x == 1 or 2', R('x = 5\nprint(x == 1 or 2)') + 'Máy hiểu <code>(x == 1) or 2</code>, mà số 2 luôn tính là đúng.', 'Viết đủ cả hai vế: <code>x == 1 or x == 2</code>.'),
         err('So sánh số viết dạng chữ', R('print("10" < "9")') + 'Chữ so sánh từng ký tự nên “10” lại “nhỏ hơn” “9”.', 'Đổi sang số trước: <code>int("10") &lt; int("9")</code>.'),
         err('Thứ tự and – or', R('print(True or False and False)') + 'Tưởng là False vì “cả hai vế cuối đều sai”, nhưng <code>and</code> làm trước nên kết quả True.', 'Dùng ngoặc cho điều kiện kép nhiều vế.'),
         err('Dùng not mà quên ngoặc', R('print(not True and False)') + '<code>not</code> chỉ đảo giá trị ngay sau nó.', 'Muốn đảo cả điều kiện: <code>not (A and B)</code>.')],
        [eg('Ví dụ 1: đủ tuổi vào lớp 12–18?', R('for tuoi in (11, 12, 15, 18, 19):\n    print(tuoi, 12 <= tuoi <= 18)') + note('Dòng <code>for</code> sẽ học kỹ ở chương lặp; bây giờ em chỉ cần đọc kết quả cho từng tuổi.')),
         eg('Ví dụ 2: kiểm tra số chia hết cho cả 3 và 5', R('for n in (15, 9, 10, 30):\n    print(n, n % 3 == 0 and n % 5 == 0)')),
         eg('Ví dụ 3: quy tắc De Morgan – kiểm chứng bằng máy', R('for a in (True, False):\n    for b in (True, False):\n        print(a, b, (not (a and b)) == ((not a) or (not b)))') + note('Với mọi cặp A, B, “không phải cả hai” luôn bằng “một trong hai là sai”: máy kiểm chứng cả 4 trường hợp đều True.'))],
        [('Cho <code>a = 15</code> và <code>b = 9</code>. Đoán rồi chạy kết quả của <code>a &gt; b</code>, <code>a == b</code>, <code>a != b</code>, <code>a % b == 6</code>.', R('a = 15\nb = 9\nprint(a > b)\nprint(a == b)\nprint(a != b)\nprint(a % b == 6)') + '<p>15 chia 9 dư 6 nên dòng cuối True.</p>', None),
         ('Viết điều kiện kiểm tra tuổi từ 12 đến 18 (kể cả hai đầu) và thử với tuổi 13, 11, 18.', R('for tuoi in (13, 11, 18):\n    print(tuoi, 12 <= tuoi <= 18)'), None),
         ('Điều kiện “đạt” là điểm Toán &gt;= 5 <b>và</b> điểm Văn &gt;= 5. Kiểm tra cho các cặp (7, 4), (5, 5), (3, 9).', R('for toan, van in ((7, 4), (5, 5), (3, 9)):\n    print(toan, van, toan >= 5 and van >= 5)') + '<p>Chỉ cặp (5, 5) đạt, vì cả hai vế cùng đúng.</p>', None),
         ('Viết điều kiện kiểm tra một số là bội của 3 <b>hoặc</b> bội của 5 (nhưng không phải cả hai). Thử với 15, 9, 10, 7.', R('for n in (15, 9, 10, 7):\n    b3 = n % 3 == 0\n    b5 = n % 5 == 0\n    print(n, (b3 or b5) and not (b3 and b5))') + '<p>15 là bội của cả hai nên bị loại; 9 và 10 mỗi số chỉ một; 7 không thuộc cả hai.</p>', None),
         ('<b>Thử thách (nghĩ ngược):</b> Viết biểu thức đúng với năm nhuận: chia hết cho 4 và không chia hết cho 100, <b>hoặc</b> chia hết cho 400. Kiểm tra với 1900, 2000, 2023, 2024. Rồi tự giải thích vì sao 1900 không nhuận còn 2000 thì nhuận.', R('for n in (1900, 2000, 2023, 2024):\n    print(n, (n % 4 == 0 and n % 100 != 0) or n % 400 == 0)') + '<p>1900 chia hết cho 4 và cho 100 nhưng không chia hết cho 400 nên không nhuận. 2000 chia hết cho 400 nên nhuận. 2023 không chia hết cho 4. 2024 chia hết cho 4 mà không chia hết cho 100 nên nhuận.</p>', None)],
        '')

    # ===================================================== BÀI 3.3  KIỂM THỬ GIÁ TRỊ BIÊN
    ve = 'for tuoi, mong in [(5, 0), (6, 20000), (17, 20000), (18, 40000), (59, 40000), (60, 20000)]:\n    if tuoi < 6:\n        gia = 0\n    elif tuoi < 18:\n        gia = 20000\n    elif tuoi < 60:\n        gia = 40000\n    else:\n        gia = 20000\n    if gia == mong:\n        print(tuoi, gia, "ĐẠT")\n    else:\n        print(tuoi, gia, "SAI, mong đợi", mong)'
    ve_loi = 'for tuoi, mong in [(5, 0), (6, 20000), (17, 20000), (18, 40000), (59, 40000), (60, 20000)]:\n    if tuoi <= 6:\n        gia = 0\n    elif tuoi < 18:\n        gia = 20000\n    elif tuoi < 60:\n        gia = 40000\n    else:\n        gia = 20000\n    if gia == mong:\n        print(tuoi, gia, "ĐẠT")\n    else:\n        print(tuoi, gia, "SAI, mong đợi", mong)'
    ve_thutu = 'for tuoi, mong in [(5, 0), (6, 20000), (17, 20000), (18, 40000)]:\n    if tuoi < 6:\n        gia = 0\n    elif tuoi < 60:\n        gia = 40000\n    elif tuoi < 18:\n        gia = 20000\n    else:\n        gia = 20000\n    if gia == mong:\n        print(tuoi, gia, "ĐẠT")\n    else:\n        print(tuoi, gia, "SAI, mong đợi", mong)'
    ve1 = 'tuoi = 17\nif tuoi < 6:\n    gia = 0\nelif tuoi < 18:\n    gia = 20000\nelif tuoi < 60:\n    gia = 40000\nelse:\n    gia = 20000\nprint(gia)'
    asr = 'gia = 20000\nassert gia == 20000\nprint("qua test 1")\nassert gia == 40000, "sai ở tuổi 18"\nprint("không tới được dòng này")'

    def vline(title, pts, zones, note_=None, label=None):
        nl = ARR + txt(350, 24, title, '#17406b', 17, bold=True)
        def X(v): return 30 + v * 9.3
        for (a, b, c, t) in zones:
            f, st = C[c]; nl += '<rect x="%.1f" y="70" width="%.1f" height="36" fill="%s" stroke="%s" stroke-width="2"/>' % (X(a), X(b) - X(a), f, st) + txt((X(a) + X(b)) / 2, 93, t, st, 13, bold=True)
        for v in range(0, 71, 10): nl += txt(X(v), 128, str(v), '#5b6773', 13)
        for v, c, t in pts:
            col = C[c][1]; left = v in (5, 17, 59); nl += '<line x1="%.1f" y1="%d" x2="%.1f" y2="108" stroke="%s" stroke-width="2.5"/>' % (X(v), 54, X(v), col) + '<circle cx="%.1f" cy="54" r="5" fill="%s"/>' % (X(v), col) + txt(X(v) + (-7 if left else 7), 50, t, col, 14, 'end' if left else 'start', True)
        if note_: nl += txt(350, 160, note_, '#5b6773', 14)
        return svg(700, 176 if note_ else 144, nl, label or title)
    V1 = fig(vline('Giá vé theo tuổi: bốn đoạn', [], [(0, 6, 'gr', '0 đ'), (6, 18, 'ye', '6–17: 20.000'), (18, 60, 'bl', '18–59: 40.000'), (60, 70, 'ye', '60+')], 'Chỗ các đoạn tiếp giáp nhau chính là “biên” – nơi chương trình hay sai nhất.'), 'Giá vé chia theo bốn đoạn tuổi. Mỗi chỗ nối giữa hai đoạn là một biên cần kiểm tra.')
    V2 = fig(vline('Sáu giá trị biên cần thử: sát hai phía của mỗi biên', [(5, 'gr', '5'), (6, 'ye', '6'), (17, 'ye', '17'), (18, 'bl', '18'), (59, 'bl', '59'), (60, 'ye', '60')], [(0, 6, 'gr', '0 đ'), (6, 18, 'ye', '20.000'), (18, 60, 'bl', '40.000'), (60, 70, 'ye', '20.000')], 'Mỗi biên thử 2 giá trị: giá trị cuối của đoạn trước và giá trị đầu của đoạn sau.'), 'Với biên 6: thử 5 và 6; biên 18: thử 17 và 18; biên 60: thử 59 và 60.')
    V3 = fig(grid_fig('Bốn loại giá trị nên đưa vào bộ test', ['Loại', 'Ví dụ (vé theo tuổi)', 'Mục đích'],
        [['Giá trị biên', '6, 18, 60', 'bắt lỗi dùng sai < hay <='], ['Sát biên', '5, 17, 59', 'xác nhận phía bên kia của biên'], ['Điển hình', '10, 30, 70', 'bảo đảm trường hợp thường vẫn đúng'], ['Không hợp lệ', '-1, 200', 'xem chương trình xử lý thế nào']], [150, 250, 300], label='Bốn loại test'),
        'Bộ test tốt không cần nhiều, chỉ cần đủ bốn loại này, nhất là hai loại đầu.')
    V4 = fig(cmp_fig('Lỗi lệch một ở biên: < và <=', [('gr', 'Đúng: tuoi < 6', ['tuoi = 6', 'tuoi < 6'], 'False → vé 20.000', 'tuổi 6 phải trả tiền'), ('rd', 'Sai: tuoi <= 6', ['tuoi = 6', 'tuoi <= 6'], 'True → vé miễn phí', 'tuổi 6 lại được miễn phí!')], 232),
        'Chỉ khác nhau đúng một dấu <b>=</b> nhưng sai đúng ở giá trị biên 6. Giá trị giữa như 3 hoặc 10 không bao giờ lộ ra lỗi này.')
    ch = ARR + txt(350, 24, 'Chuỗi điều kiện: máy kiểm tra từ trên xuống, dừng ở nhánh đúng đầu tiên', '#17406b', 16, bold=True)
    rows_ = [('if tuoi < 6:', 'gia = 0', 'gr'), ('elif tuoi < 18:', 'gia = 20000', 'ye'), ('elif tuoi < 60:', 'gia = 40000', 'bl'), ('else:', 'gia = 20000', 'ye')]
    for i, (a, b, c) in enumerate(rows_):
        y = 44 + i * 64; f, st = C[c]
        ch += '<rect x="30" y="%d" width="300" height="40" rx="8" fill="%s" stroke="%s" stroke-width="2"/>' % (y, f, st) + mono(46, y + 27, a, '#17406b', 18, 'start', True) + arr(332, y + 20, 392, y + 20, st) + box(394, y, 220, 40, f, st, [b], 16, bold=True)
        if i < 3: ch += arr(180, y + 42, 180, y + 62, '#c0392b') + txt(196, y + 57, 'sai → xuống tiếp', '#c0392b', 12, 'start')
    V5 = fig(svg(700, 290, ch, 'Chuỗi điều kiện'), 'Vì máy dừng ở nhánh đúng đầu tiên, thứ tự các điều kiện quyết định kết quả.')
    pt_ok = ve
    out_ok = run(ve); out_bad = run(ve_loi)
    tg = ARR + txt(350, 24, 'Bảng kết quả kiểm thử (bản có lỗi tuoi <= 6)', '#17406b', 17, bold=True)
    for i, l in enumerate(out_bad.split('\n')):
        y = 44 + i * 34; bad = 'SAI' in l
        tg += '<rect x="30" y="%d" width="640" height="30" rx="6" fill="%s" stroke="%s"/>' % (y, '#fdecea' if bad else '#e5f5ea', '#c0392b' if bad else '#2a8a4a') + mono(46, y + 21, l, '#7b1d12' if bad else '#17406b', 15, 'start', bad)
    V6 = fig(svg(700, 44 + 34 * len(out_bad.split('\n')) + 14, tg, 'Kết quả kiểm thử'), 'Đúng một dòng báo SAI: đó là giá trị biên 6. Nhờ test ở biên mà tìm ra lỗi chỉ trong một lần chạy.')
    V7 = flowrow(['Xác định|các đoạn', 'Tìm các|biên', 'Chọn test|sát biên', 'Ghi mong|đợi trước', 'Chạy,|sửa nếu SAI'], 'Quy trình kiểm thử giá trị biên', colors=['#e6f1fb', '#e6f1fb', '#fff4d6', '#fff4d6', '#e5f5ea'])
    V8 = fig(cmp_fig('assert: tự động báo khi kết quả không như mong đợi', [('gr', 'Khớp', ['assert gia == 20000'], 'chạy tiếp, im lặng', 'không in gì'), ('rd', 'Lệch', ['assert gia == 40000,', '"sai ở tuổi 18"'], 'AssertionError', 'dừng và nêu thông báo')], 240),
        '<code>assert điều_kiện</code> im lặng khi điều kiện đúng và báo lỗi ngay khi sai: rất tiện để viết test.')
    V9 = fig(grid_fig('Mẫu bảng test: ghi trước, chạy sau', ['Tuổi', 'Mong đợi', 'Thực tế', 'Kết luận'],
        [['5', '0', '0', 'ĐẠT'], ['6', '20000', '0', 'SAI'], ['17', '20000', '20000', 'ĐẠT'], ['18', '40000', '40000', 'ĐẠT']], [100, 160, 160, 160], hl=[1], label='Mẫu bảng test'),
        'Cột “Mong đợi” phải điền <b>trước khi chạy</b>, từ đề bài; nếu điền sau khi thấy kết quả thì test không còn ý nghĩa.')
    V10 = ptrace(ve1, pick=[0, 1, 2, 3, 4], maxn=6, captions=['Gán <b>tuoi</b> = 17.', 'Kiểm tra <code>17 &lt; 6</code>: sai, bỏ nhánh này.', 'Kiểm tra <code>17 &lt; 18</code>: đúng → vào nhánh này.', '<b>gia</b> = 20000; các nhánh sau bị bỏ qua.', 'In 20000.'])
    cv = ARR + txt(350, 24, 'Độ phủ: mỗi nhánh phải được test ít nhất một lần', '#17406b', 17, bold=True)
    for i, (a, t, c) in enumerate([('tuoi < 6', 'test 5', 'gr'), ('elif tuoi < 18', 'test 6, 17', 'ye'), ('elif tuoi < 60', 'test 18, 59', 'bl'), ('else', 'test 60', 'ye')]):
        x = 14 + i * 172; f, st = C[c]; cv += box(x, 44, 162, 70, f, st, [a, ''], 14, bold=True) + '<text x="%d" y="100" text-anchor="middle" font-size="13" fill="#2a8a4a" font-weight="700">✓ %s</text>' % (x + 81, t)
    cv += txt(350, 150, 'Nhánh nào không có test chạy qua thì lỗi trong nhánh đó sẽ không bao giờ bị phát hiện.', '#5b6773', 14)
    V11 = fig(svg(700, 168, cv, 'Độ phủ nhánh'), 'Bộ test sáu giá trị ở trên chạy qua đủ cả bốn nhánh, nên phủ hết các trường hợp.')

    cmd33 = cmdx('Phân tích các phần của chương trình và bộ test. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', [
        ['<code>if điều_kiện:</code>', 'Làm khối lệnh bên dưới <b>nếu</b> điều kiện đúng.', 'Quên dấu hai chấm <code>:</code>:' + ERR('if 5 > 3\n    print(1)')],
        ['khối lệnh thụt vào', 'Các lệnh thụt vào (4 dấu cách) thuộc về <code>if</code> ngay phía trên.', 'Quên thụt dòng:' + ERR('if 5 > 3:\nprint(1)')],
        ['<code>elif điều_kiện:</code>', 'Kiểm tra thêm khi điều kiện trước sai.', 'Đảo thứ tự sai: khoảng rộng đặt trước khoảng hẹp làm khoảng hẹp không bao giờ chạy tới:' + R(ve_thutu)],
        ['<code>else:</code>', 'Làm khi mọi điều kiện phía trên đều sai.', 'Quên <code>else</code>: giá trị không được gán ở trường hợp còn lại:' + ERR('tuoi = 70\nif tuoi < 18:\n    gia = 20000\nprint(gia)')],
        ['<code>&lt;</code> so với <code>&lt;=</code> ở biên', 'Quyết định giá trị biên thuộc đoạn nào.', 'Dùng <code>&lt;=</code> thay vì <code>&lt;</code> tại biên 6:' + R(ve_loi)],
        ['<code>(tuoi, mong)</code> trong danh sách test', 'Mỗi cặp là một test: đầu vào và kết quả mong đợi.', 'Đảo hai giá trị trong cặp làm toàn bộ test báo SAI:' + R('for tuoi, mong in [(20000, 6)]:\n    gia = 20000 if tuoi >= 6 else 0\n    print(tuoi, gia, "ĐẠT" if gia == mong else "SAI")')],
        ['<code>gia == mong</code>', 'So sánh kết quả thực tế với kết quả mong đợi.', 'Viết một dấu <code>=</code> thành phép gán, Python báo lỗi cú pháp:' + ERR('gia = 0\nmong = 0\nif gia = mong:\n    print("ĐẠT")')],
        ['<code>assert điều_kiện</code>', 'Dừng chương trình nếu điều kiện sai; im lặng nếu đúng.', 'Khi điều kiện sai:' + ERR('assert 2 + 2 == 5')],
        ['<code>assert …, "thông báo"</code>', 'Thêm câu giải thích hiện ra khi test sai.', 'Có thông báo giúp biết test nào sai:' + ERR(asr)]])

    P['c3b3'] = std2('Bài 3.3 · Kiểm thử giá trị biên', 'Chọn đúng vài giá trị để bắt gọn lỗi: sát hai phía của mỗi biên.',
        ('Xác định biên của một bài toán, lập bảng test, ghi kết quả mong đợi, chạy và tìm lỗi lệch một; dùng assert để tự kiểm tra', 'Đã biết if – elif – else (Bài 3.2) và điều kiện (Bài 3.1)', 'Bộ test giá trị biên cho chương trình tính giá vé'),
        ['Lỗi trong điều kiện hiếm khi nằm giữa đoạn; chúng nằm <b>ở biên</b>, nơi hai trường hợp gặp nhau.', 'Chỉ thử 5 – 6 giá trị chọn khéo là đủ phát hiện lỗi mà không cần thử hàng trăm số.', 'Kiểm thử biến việc “có vẻ đúng” thành “đã chứng minh đúng với các trường hợp khó nhất”.', 'Đây là nền tảng của việc viết test tự động ở các chương sau.'],
        ol(['Chia bài toán thành các <b>đoạn</b> (miễn phí, nửa giá, giá đủ…).', 'Tìm các <b>biên</b> giữa hai đoạn rồi chọn giá trị biên và giá trị sát biên mỗi phía.', 'Lập bảng <b>mong đợi</b> từ đề bài <i>trước khi chạy</i>.', 'Chạy, so sánh; dòng nào SAI thì sửa điều kiện ở đúng biên đó rồi chạy lại toàn bộ test.']),
        think(['<b>Phản biện:</b> “Em chỉ thử 3 số, thấy đúng — vậy chương trình chắc đúng chưa?” Ba số đó có nằm ở biên không?', '<b>Nghĩ ngược:</b> biết đáp án mong đợi, em phải viết điều kiện như thế nào để đúng ở cả hai phía của biên?', '<b>Thói quen tốt:</b> viết test <i>trước hoặc song song</i> với code, không viết sau khi đã thấy kết quả.']),
        'Ứng dụng vào Python',
        li(['Bài toán: vé tham quan — dưới 6 tuổi miễn phí; 6–17 tuổi 20.000 đ; 18–59 tuổi 40.000 đ; từ 60 tuổi 20.000 đ. Một lần tính giá cho tuổi 17:']) + R(ve1) + 'Bộ test giá trị biên chạy với chương trình đúng:' + R(ve) + 'Cùng bộ test với chương trình bị lỗi <code>tuoi &lt;= 6</code>:' + R(ve_loi) + note('Chương trình có lỗi vẫn chạy bình thường, không báo lỗi gì; chỉ bộ test mới cho thấy dòng SAI.') + 'Tự động hóa bằng assert:' + ERR(asr),
        cmd33,
        V1 + V2 + V3 + V4 + V5 + V6 + V7 + V8 + V9 + V10 + V11,
        [err('Chỉ thử giá trị ở giữa', 'Thử tuổi 3, 10, 30, 70 đều đúng dù chương trình có lỗi ở biên:' + R(ve_loi.replace('[(5, 0), (6, 20000), (17, 20000), (18, 40000), (59, 40000), (60, 20000)]', '[(3, 0), (10, 20000), (30, 40000), (70, 20000)]')), 'Luôn thử biên và sát biên.'),
         err('Nhầm < với <= ở biên', 'Tuổi 6 trả vé miễn phí trong khi đề bảo phải trả 20.000.', 'Đọc kỹ đề: “dưới 6” là <code>&lt; 6</code>; “từ 6” là <code>&gt;= 6</code>.'),
         err('Điều kiện rộng đặt trước điều kiện hẹp', 'Với <code>elif tuoi &lt; 60</code> đặt trước <code>elif tuoi &lt; 18</code> thì tuổi 17 không bao giờ vào nhánh dành cho trẻ em.', 'Sắp xếp từ <b>hẹp đến rộng</b> hoặc theo thứ tự tăng dần.'),
         err('Điền kết quả mong đợi sau khi thấy kết quả chạy', 'Khi đó bảng test luôn “đạt” dù chương trình sai.', 'Điền cột mong đợi từ đề bài trước khi chạy.'),
         err('Quên test giá trị không hợp lệ', 'Tuổi -1 hoặc 200 vẫn được tính giá vé như bình thường vì không có điều kiện chặn.', 'Thêm điều kiện kiểm tra miền hợp lệ trước (<code>if tuoi &lt; 0 or tuoi &gt; 120</code>).')],
        [eg('Ví dụ 1: kiểm tra điểm hợp lệ 0–10', R('for d in (-0.1, 0, 5, 10, 10.1):\n    print(d, 0 <= d <= 10)') + note('Test đủ hai biên (0, 10) và hai giá trị ngay ngoài biên (-0.1, 10.1).')),
         eg('Ví dụ 2: xếp loại và các biên', R('for d in (4.9, 5, 6.4, 6.5, 7.9, 8):\n    if d >= 8:\n        xl = "Giỏi"\n    elif d >= 6.5:\n        xl = "Khá"\n    elif d >= 5:\n        xl = "TB"\n    else:\n        xl = "Yếu"\n    print(d, xl)') + note('Cặp (4.9; 5), (6.4; 6.5), (7.9; 8) là hai phía của ba biên 5, 6.5, 8.')),
         eg('Ví dụ 3: assert một loạt test', R('for tuoi, mong in [(5, 0), (6, 20000), (18, 40000)]:\n    if tuoi < 6:\n        gia = 0\n    elif tuoi < 18:\n        gia = 20000\n    else:\n        gia = 40000\n    assert gia == mong, f"sai ở tuổi {tuoi}"\nprint("Tất cả test đạt")'))],
        [('Với bài toán vé theo tuổi (miễn phí dưới 6; 20.000 từ 6–17; 40.000 từ 18–59; 20.000 từ 60), hãy liệt kê các giá trị biên và sát biên cần test.', '<p>Biên 6: thử 5 và 6. Biên 18: thử 17 và 18. Biên 60: thử 59 và 60. Tổng 6 giá trị.</p>' + R('for tuoi in (5, 6, 17, 18, 59, 60):\n    print(tuoi)'), None),
         ('Chạy bộ test với chương trình bị lỗi <code>tuoi &lt;= 6</code> (ở phần Ứng dụng), chỉ ra tuổi nào SAI và vì sao.', R(ve_loi) + '<p>Tuổi 6 báo SAI: chương trình cho vé 0 vì <code>6 &lt;= 6</code> đúng, trong khi đề yêu cầu trả 20.000. Sửa thành <code>tuoi &lt; 6</code>.</p>', None),
         ('Xếp loại: Giỏi ≥ 8; Khá ≥ 6.5; Trung bình ≥ 5; còn lại Yếu. Viết bộ test 8 giá trị có đủ biên và sát biên, ghi mong đợi trước, rồi chạy xem cái nào đạt.', R('tests = [(10, "Giỏi"), (8, "Giỏi"), (7.9, "Khá"), (6.5, "Khá"), (6.4, "TB"), (5, "TB"), (4.9, "Yếu"), (0, "Yếu")]\nfor d, mong in tests:\n    if d >= 8:\n        xl = "Giỏi"\n    elif d >= 6.5:\n        xl = "Khá"\n    elif d >= 5:\n        xl = "TB"\n    else:\n        xl = "Yếu"\n    print(d, xl, "ĐẠT" if xl == mong else "SAI")') + '<p>Tám giá trị phủ cả ba biên 8, 6.5, 5 (mỗi biên hai phía) cùng hai giá trị ở hai đầu.</p>', None),
         ('Chương trình nhận điểm từ 0 đến 10; ngoài khoảng đó phải in “Không hợp lệ”. Chọn các giá trị test và chạy.', R('for d in (-0.1, 0, 10, 10.1):\n    if 0 <= d <= 10:\n        print(d, "Hợp lệ")\n    else:\n        print(d, "Không hợp lệ")') + '<p>Hai biên 0 và 10 hợp lệ; hai giá trị ngay ngoài biên không hợp lệ.</p>', None),
         ('<b>Thử thách (nghĩ ngược):</b> Chương trình dưới có <b>hai lỗi</b> (một lỗi ở biên, một lỗi thứ tự điều kiện). Chạy bộ test, nhận ra dòng SAI, sửa cả hai lỗi rồi chạy lại cho đến khi tất cả đạt.' + code('for tuoi, mong in [(5, 0), (6, 20000), (17, 20000), (18, 40000), (59, 40000), (60, 20000)]:\n    if tuoi <= 6:\n        gia = 0\n    elif tuoi < 60:\n        gia = 40000\n    elif tuoi < 18:\n        gia = 20000\n    else:\n        gia = 20000\n    print(tuoi, gia, "ĐẠT" if gia == mong else "SAI")'), '<p>Chạy bản lỗi:</p>' + R('for tuoi, mong in [(5, 0), (6, 20000), (17, 20000), (18, 40000), (59, 40000), (60, 20000)]:\n    if tuoi <= 6:\n        gia = 0\n    elif tuoi < 60:\n        gia = 40000\n    elif tuoi < 18:\n        gia = 20000\n    else:\n        gia = 20000\n    print(tuoi, gia, "ĐẠT" if gia == mong else "SAI")') + '<p>Lỗi 1: <code>tuoi &lt;= 6</code> làm tuổi 6 miễn phí → đổi thành <code>tuoi &lt; 6</code>. Lỗi 2: <code>tuoi &lt; 60</code> đặt trước <code>tuoi &lt; 18</code> nên tuổi 6–17 rơi vào nhánh 40.000 → đặt <code>tuoi &lt; 18</code> lên trước. Bản đúng:</p>' + R(ve), None)],
        '')

    # ===================================================== TÓM TẮT CHƯƠNG 3
    mm = ARR + txt(350, 24, 'Sơ đồ tóm tắt Chương 3', '#17406b', 17, bold=True) + box(260, 100, 180, 62, '#fff4d6', '#d9822b', ['Chương 3', 'Rẽ nhánh'], 15, bold=True)
    br = [(24, 40, 'Điều kiện (Bài 3.1)', '== != < > and or not'), (24, 160, 'if – elif – else (3.2)', 'máy chọn một nhánh'), (496, 40, 'Giá trị biên (3.3)', 'test sát hai phía'), (496, 160, 'assert & bảng test', 'mong đợi viết trước')]
    for x, y, a, b in br:
        mm += box(x, y, 190, 60, '#e6f1fb', '#1f6fb2', [a, b], 14, bold=True)
        mm += arr(x + 192 if x < 270 else x - 2, y + 30, 258 if x < 270 else 442, 130, '#6b7785')
    M1 = fig(svg(700, 250, mm, 'Sơ đồ tóm tắt chương 3'), 'Điều kiện đúng/sai là gốc; if – elif – else dùng nó để chọn nhánh; kiểm thử biên bảo đảm nhánh nào cũng đúng.')
    ba = ARR + txt(350, 24, 'Trước và sau Chương 3', '#17406b', 17, bold=True)
    ba += box(14, 44, 330, 150, '#f3f4f6', '#9db4c9', [], 14) + txt(179, 68, 'Trước chương 3', '#5b6773', 15, bold=True)
    for i, l in enumerate(['Chương trình chạy một mạch', 'Chưa biết cho máy lựa chọn', 'Thử vài số rồi tin là đúng']): ba += txt(30, 104 + i * 28, '• ' + l, '#5b6773', 14, 'start')
    ba += box(356, 44, 330, 150, '#e5f5ea', '#2a8a4a', [], 14) + txt(521, 68, 'Sau chương 3', '#2a8a4a', 15, bold=True)
    for i, l in enumerate(['Viết điều kiện đúng/sai chính xác', 'Dùng if – elif – else để rẽ nhánh', 'Test giá trị biên để bắt lỗi']): ba += txt(372, 104 + i * 28, '✓ ' + l, '#17406b', 14, 'start')
    M2 = fig(svg(700, 212, ba, 'Trước và sau chương 3'), 'Chương trình của em đã biết “quyết định” và em biết cách kiểm tra quyết định đó có đúng không.')
    ck = ARR + txt(350, 24, 'Bảng tự đánh giá: tô màu ô em làm được', '#17406b', 17, bold=True)
    for i, l in enumerate(['Phân biệt = và ==', 'Viết điều kiện kép and/or', 'Đoán True/False đúng', 'Viết if – elif – else', 'Chọn giá trị biên để test', 'Dùng assert']):
        x = 14 + (i % 2) * 345; y = 44 + (i // 2) * 52; ck += '<rect x="%d" y="%d" width="330" height="42" rx="8" fill="#fff" stroke="#9db4c9"/><rect x="%d" y="%d" width="22" height="22" rx="4" fill="#fff" stroke="#1f6fb2" stroke-width="2"/>' % (x, y, x + 12, y + 10) + txt(x + 46, y + 27, l, '#1c2733', 14, 'start')
    M3 = fig(svg(700, 206, ck, 'Bảng tự đánh giá chương 3'), 'Chưa tô được ô nào thì quay lại bài tương ứng, đừng bỏ qua.')
    proj = 'tuoi = int(input())\nso_ve = int(input())\nif tuoi < 0 or tuoi > 120:\n    print("Tuổi không hợp lệ")\nelse:\n    if tuoi < 6:\n        gia = 0\n    elif tuoi < 18:\n        gia = 20000\n    elif tuoi < 60:\n        gia = 40000\n    else:\n        gia = 20000\n    tong = gia * so_ve\n    print("=" * 28)\n    print(f"Tuổi {tuoi}: giá {gia} đ/vé")\n    print(f"Số vé: {so_ve}")\n    print(f"Thành tiền: {tong} đ")\n    print("=" * 28)'
    out1 = run(proj, '17\n3\n'); out2 = run(proj, '130\n1\n')
    po = ARR + txt(350, 24, 'Kết quả dự án: máy bán vé', '#17406b', 17, bold=True) + box(60, 40, 280, 130, '#fff', '#6b7785', [], 14) + box(360, 40, 280, 130, '#fff', '#6b7785', [], 14)
    po += txt(200, 60, 'Nhập 17 và 3', '#5b6773', 13, bold=True) + txt(500, 60, 'Nhập 130 và 1', '#5b6773', 13, bold=True)
    for i, l in enumerate(out1.split('\n')): po += mono(74, 88 + i * 20, l, '#1c2733', 12)
    for i, l in enumerate(out2.split('\n')): po += mono(374, 88 + i * 20, l, '#c0392b', 13, 'start', True)
    M4 = fig(svg(700, 190, po, 'Kết quả máy bán vé'), 'Hai lần chạy: một vé hợp lệ in phiếu, một tuổi ngoài khoảng bị từ chối.')
    tab = table(['Điều cần nhớ', 'Ví dụ', 'Ý nghĩa'], [['<code>==</code> khác <code>=</code>', '<code>x == 5</code>', 'So sánh; một dấu <code>=</code> là gán'], ['and / or / not', '<code>12 &lt;= t and t &lt;= 18</code>', 'Cùng đúng / một trong hai / đảo ngược'], ['So sánh liên tiếp', '<code>10 &lt;= x &lt;= 20</code>', 'x thuộc khoảng, kể cả hai đầu'], ['if – elif – else', '<code>if t &lt; 6: … elif t &lt; 18: …</code>', 'Máy dừng ở nhánh đúng đầu tiên'], ['Giá trị biên', '5, 6 / 17, 18 / 59, 60', 'Thử sát hai phía của mỗi biên'], ['Mong đợi viết trước', 'bảng (đầu vào, mong đợi)', 'Điền từ đề bài, rồi mới chạy'], ['<code>assert</code>', '<code>assert gia == mong</code>', 'Im lặng nếu đúng, báo lỗi nếu sai']])
    top5 = ''.join(err(a, b, c) for a, b, c in [('Dùng = thay cho ==', 'Gây lỗi cú pháp hoặc gán nhầm.', 'So sánh dùng <code>==</code>.'), ('Viết x == 1 or 2', 'Luôn đúng vì 2 tính là đúng.', 'Viết đủ <code>x == 1 or x == 2</code>.'), ('Nhầm < với <= ở biên', 'Sai đúng ở giá trị biên.', 'Đọc kỹ “dưới”, “từ”, “không quá”.'), ('Điều kiện rộng đứng trước điều kiện hẹp', 'Nhánh hẹp không bao giờ chạy tới.', 'Sắp xếp theo thứ tự tăng dần.'), ('Chỉ thử giá trị ở giữa', 'Lỗi biên lọt qua test.', 'Luôn thử biên và sát biên.')])
    quiz = [('<code>=</code> và <code>==</code> khác nhau thế nào?', '<code>=</code> gán giá trị cho biến; <code>==</code> so sánh hai giá trị và cho True hoặc False.'), ('<code>True or False and False</code> ra gì, vì sao?', 'Ra True: <code>and</code> được tính trước <code>or</code>, nên là <code>True or (False and False)</code> = True or False = True.'), ('Viết điều kiện “tuổi từ 12 đến 18 (kể cả hai đầu)”.', '<code>12 &lt;= tuoi &lt;= 18</code> hoặc <code>tuoi &gt;= 12 and tuoi &lt;= 18</code>.'), ('Với vé: dưới 6 miễn phí, tuổi 6 trả tiền. Điều kiện cho nhánh miễn phí là gì?', '<code>tuoi &lt; 6</code> (không có dấu bằng), vì tuổi 6 không được miễn phí.'), ('Vì sao phải thử cả 17 và 18 khi biên là 18?', 'Để kiểm tra hai phía của biên: 17 thuộc đoạn trước, 18 thuộc đoạn sau; lỗi lệch một chỉ lộ ra ở hai giá trị này.'), ('Cột “mong đợi” của bảng test nên điền khi nào?', 'Điền từ đề bài <i>trước khi chạy</i>, nếu không bảng test sẽ không phát hiện được lỗi.')]
    qh = ''.join('<details class="tans"><summary>Câu %d. %s</summary><p>%s</p></details>' % (i + 1, q, a) for i, (q, a) in enumerate(quiz))
    P['c3t'] = {'title': 'Tóm tắt Chương 3 · Cấu trúc rẽ nhánh', 'sub': 'Hệ thống lại kiến thức, lỗi hay gặp và làm dự án máy bán vé có kiểm thử.',
        'html': '\n'.join([tsum('Hệ thống lại Chương 3 và tự kiểm tra; hoàn thành dự án “máy bán vé tham quan”', 'Đã học Bài 3.1 đến 3.3', 'Bảng ghi nhớ của em và chương trình máy bán vé chạy đúng với bộ test biên'),
            card(1, 'Sơ đồ tóm tắt chương', M1 + M2), card(2, 'Bảng ghi nhớ nhanh', tab), card(3, '5 lỗi hay gặp nhất của chương', top5),
            card('+', 'Em đã làm được gì? (tự đánh giá)', M3),
            card(4, 'Em đã học được thói quen tư duy nào?', think(['<b>Nói điều kiện bằng lời trước</b>, rồi mới dịch sang code.', '<b>Thử sát hai phía của biên</b>: lỗi thường ẩn ở đó.', '<b>Viết kết quả mong đợi trước khi chạy</b> để test có ý nghĩa.'], 'Thói quen của Chương 3')),
            chap('Dự án nhỏ cuối chương'),
            '<section class="tcard tprac"><h4><span class="tn">DA</span>Dự án: máy bán vé tham quan <span class="lvl">★★★★</span></h4><p>Viết chương trình nhập <b>tuổi</b> và <b>số vé</b>, tính tiền theo bảng giá (dưới 6: miễn phí; 6–17: 20.000; 18–59: 40.000; từ 60: 20.000), in phiếu có khung. Tuổi ngoài khoảng 0–120 phải in “Tuổi không hợp lệ”. Sau đó lập <b>bảng test</b> gồm các giá trị biên và chạy thử với tuổi 17 và 130.</p><details class="tans"><summary>Xem bài mẫu và kết quả chạy</summary>%s%s%s<p>Bảng test giá trị biên cho chương trình này gồm: 5, 6, 17, 18, 59, 60 (biên giữa các đoạn) và -1, 0, 120, 121 (biên của miền hợp lệ). Em hãy tự chạy lần lượt từng giá trị để kiểm tra.</p></details></section>' % (code('# Dự án chương 3: máy bán vé\n' + proj, out1), '<div class="code-out-l">Nhập tuổi 130, số vé 1</div><pre class="code out">%s</pre>' % E(out2), M4),
            chap('Tự kiểm tra (6 câu)'), '<section class="tcard">%s</section>' % qh,
            card(5, 'Chương sau học gì?', li(['<b>Chương 4 – Cấu trúc lặp:</b> bảo máy lặp lại một việc nhiều lần bằng <code>while</code> và <code>for</code>, kể cả vòng lặp lồng nhau.', 'Em đã biết cho máy <b>lựa chọn</b>; sang chương 4 em sẽ cho máy <b>lặp lại</b> để làm những việc nhàm chán thay em.']))])}
    return P
