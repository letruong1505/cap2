"""Lộ trình 12–18 (Python): 8 bài theo khung 8 mục. Mọi kết quả chạy lấy từ lần chạy thật."""
import subprocess, sys
from tuduy_lib import *

def R(src, stdin=''): return code(src, run(src, stdin))
def runerr(src):
    r = subprocess.run([sys.executable, '-I', '-c', src], capture_output=True, text=True, timeout=10)
    assert r.returncode != 0, src
    return r.stderr.strip().split('\n')[-1]
def ERR(src): return code(src, runerr(src))

def build():
    P = {}
    # ---------------- Bài 1 ----------------
    p1 = 'ten = input()\nprint("Xin chào,", ten)\na = int(input())\nb = int(input())\nprint("Tổng:", a + b)'
    P['bai1'] = std('Bài 1 · Từ bài toán đến thuật toán', 'Nghĩ rõ trước, gõ code sau.',
        ('Chia bài toán thành các bước; viết chương trình Python với print, input, int; dự đoán trước khi chạy', 'Python 3 và IDLE (đã cài ở bài Cài đặt)', 'Chương trình nhập dữ liệu, tính toán và in kết quả'),
        ['<b>Thuật toán</b> là dãy bước hữu hạn, rõ ràng, giải được một bài toán.', 'Người giỏi lập trình dành phần lớn thời gian <b>nghĩ</b>, phần nhỏ thời gian gõ.', 'Bài này cho bạn quy trình đi từ đề bài tới code để dùng cho mọi bài sau.'],
        ol(['<b>Hiểu đề:</b> đầu vào là gì, đầu ra là gì?', '<b>Chia nhỏ</b> thành các bước viết bằng lời.', '<b>Dự đoán</b> kết quả với một ví dụ nhỏ tính tay.', '<b>Gõ code</b> theo từng bước, chạy thử, so với dự đoán.']),
        think(['<b>Phản biện:</b> kết quả máy ra có khớp với tính tay không? Nếu lệch, lỗi nằm ở code hay ở cách hiểu đề?', '<b>Ngược:</b> bắt đầu từ đầu ra mong muốn, hỏi “muốn có nó cần dữ liệu gì, tính qua những bước nào?”.'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['<code>print(...)</code> in ra màn hình; <code>input()</code> đọc một dòng người dùng nhập – luôn là <b>chữ</b>.', '<code>int(...)</code> đổi chữ thành số nguyên để tính toán.']) + R(p1, 'Lan\n12\n30\n') + note('Ví dụ trên nhập: Lan, 12, 30.'),
        flowrow(['Hiểu đề', 'Chia nhỏ|thành bước', 'Dự đoán|ví dụ nhỏ', 'Gõ code', 'Chạy & so|với dự đoán'], 'Quy trình giải một bài toán') + ptrace(p1, 'Lan\n12\n30', pick=[0, 1, 2, 3, 4], captions=['Dòng 1: <b>input()</b> nhận chữ “Lan” và gán vào biến ten.', 'Dòng 2: in lời chào.', 'Dòng 3: nhập 12, <b>int()</b> đổi sang số rồi gán vào a.', 'Dòng 4: nhập 30, gán vào b.', 'Dòng 5: in tổng a + b = 42.']),
        [err('Gõ code ngay, không nghĩ', 'Viết dở dang rồi vá liên tục, mất nhiều thời gian hơn.', 'Viết ra giấy: đầu vào – các bước – đầu ra, rồi mới gõ.'),
         err('Quên int() khi nhập số', 'input() trả về chữ nên phép “+” nối chữ thay vì cộng số:' + R('a = input()\nb = input()\nprint(a + b)', '12\n30\n'), 'Dùng <code>a = int(input())</code>.'),
         err('Thiếu ngoặc hoặc dấu nháy', 'Python báo lỗi cú pháp:' + ERR('print("Xin chào)'), 'Đọc dòng báo lỗi cuối cùng, kiểm tra mọi dấu ngoặc/nháy đã đóng đủ.'),
         err('Thụt dòng không đều', 'Thêm khoảng trắng đầu dòng bừa bãi gây lỗi:' + ERR('print("a")\n  print("b")'), 'Chỉ thụt dòng khi có khối lệnh (if, for, def).')],
        [eg('Ví dụ 1: chu vi và diện tích hình chữ nhật', R('d = int(input())\nr = int(input())\nprint("Chu vi:", 2 * (d + r))\nprint("Diện tích:", d * r)', '8\n5\n')),
         eg('Ví dụ 2: đổi phút ra giờ và phút', R('p = int(input())\nprint(p // 60, "giờ", p % 60, "phút")', '135\n') + note('<code>//</code> là chia lấy phần nguyên, <code>%</code> là lấy phần dư.'))],
        [('Viết chương trình in dòng “Mình tên là …, năm nay … tuổi” (thay bằng thông tin của bạn).', R('ten = "Lan"\ntuoi = 14\nprint("Mình tên là", ten + ", năm nay", tuoi, "tuổi")'), None),
         ('Nhập chiều dài và chiều rộng, in chu vi và diện tích. Thử với 8 và 5.', R('d = int(input())\nr = int(input())\nprint(2 * (d + r), d * r)', '8\n5\n') + note('Tính tay: chu vi 2 × (8 + 5) = 26; diện tích 8 × 5 = 40 ✓.'), None),
         ('Bữa ăn 4 người, mỗi người 45 000 đồng, thêm 10% phí phục vụ. Viết các bước bằng lời rồi viết code.', '<p>Bước: tiền ăn = 4 × 45000; phí = 10% tiền ăn; tổng = tiền ăn + phí.</p>' + R('an = 4 * 45000\nphi = an * 10 // 100\nprint(an + phi)'), None),
         ('Nhập số phút (ví dụ 135) rồi in ra “… giờ … phút”. Thử thêm 59 và 60 để kiểm tra ranh giới.', R('p = int(input())\nprint(p // 60, "giờ", p % 60, "phút")', '135\n') + R('print(59 // 60, 59 % 60)\nprint(60 // 60, 60 % 60)') + note('Ranh giới 59 và 60 cho kết quả đúng: 0 giờ 59 phút và 1 giờ 0 phút.'), None),
         ('<b>Thử thách (nghĩ ngược):</b> sau khi cộng 10% phí, hóa đơn là 198 000 đồng. Tiền ăn ban đầu là bao nhiêu? Một bạn tính 198000 × 0,9 = 178200. Bạn ấy sai ở đâu?', '<p>Đi ngược phép “nhân 1,1”: chia 1,1.</p>' + R('tong = 198000\nan = tong / 1.1\nprint(round(an))\nprint(round(an * 1.1))\nprint(198000 * 0.9)') + '<p>Kiểm tra xuôi: 180000 × 1,1 = 198000 ✓. Sai của bạn kia: bớt 10% của <b>tổng</b> không phải là ngược của việc thêm 10% của <b>tiền gốc</b>, vì hai số 10% khác nhau (19 800 so với 18 000).</p>', None)],
        'Python')

    # ---------------- Bài 2 ----------------
    p2 = 'gia = 25000\nsl = 3\ntong = gia * sl\nsl = sl + 2\nprint(tong)\nprint(gia * sl)'
    P['bai2'] = std('Bài 2 · Biến và kiểu dữ liệu', 'Theo dõi giá trị biến để kiểm chứng chương trình.',
        ('Hiểu phép gán, biến, số và chữ; lập bảng theo dõi giá trị biến để dự đoán kết quả', 'Python 3 và IDLE', 'Bảng theo dõi biến cho một đoạn code'),
        ['<b>Biến</b> là ô nhớ có tên giữ một giá trị; chương trình nào cũng cần biến.', 'Phép <code>=</code> là <b>gán</b>, khác với “bằng nhau” trong toán.', 'Số và chữ là hai kiểu dữ liệu khác nhau; nhầm kiểu là lỗi rất phổ biến.'],
        ol(['Đặt <b>tên biến rõ nghĩa</b> (gia, so_luong, tong_tien).', 'Gán giá trị đầu.', 'Cập nhật khi cần: <code>sl = sl + 2</code> hoặc <code>sl += 2</code>.', 'Khi nghi ngờ, <b>in biến ra</b> bằng print để kiểm tra.']),
        think(['<b>Phản biện:</b> nhiều bạn nghĩ sau khi đổi <code>sl</code> thì <code>tong</code> tự cập nhật. Hãy lập bảng theo dõi để kiểm chứng.', '<b>Ngược:</b> biết giá trị cuối của biến, suy ngược về giá trị đầu từ các phép gán.'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['<code>int</code> số nguyên, <code>float</code> số thập phân, <code>str</code> chữ.', 'Cộng hai số ra số; cộng hai chuỗi chữ thì <b>nối</b> lại.']) + R('print(3 + 4)\nprint("3" + "4")\nprint("Ha" * 3)\nprint(type(3), type(3.5), type("3"))'),
        ptrace(p2, pick=[0, 1, 2, 3, 4, 5], captions=['<code>gia</code> = 25000.', '<code>sl</code> = 3.', '<code>tong</code> = 25000 × 3 = 75000.', '<code>sl</code> đổi thành 5 – nhưng <code>tong</code> vẫn là 75000.', 'In <code>tong</code>: 75000 (giá trị cũ).', 'In <code>gia * sl</code>: tính lại với sl mới = 125000.']),
        [err('Nhầm “=” (gán) với “==” (so sánh)', 'Viết <code>if x = 3:</code> gây lỗi:' + ERR('x = 1\nif x = 3:\n    print(1)'), 'Dùng <code>==</code> để so sánh.'),
         err('Cộng chữ thay vì cộng số', '<code>"3" + 4</code> không cộng được:' + ERR('print("3" + 4)'), 'Đổi kiểu: <code>int("3") + 4</code>.'),
         err('Dùng biến chưa gán', 'Python không biết biến chưa tạo:' + ERR('print(tien)'), 'Gán giá trị cho biến trước khi dùng; kiểm tra chính tả tên biến.'),
         err('Tin rằng biến tự cập nhật', 'Biến <code>tong</code> được tính một lần, không đổi khi <code>sl</code> đổi.', 'Muốn có tổng mới phải tính lại: <code>tong = gia * sl</code>.')],
        [eg('Ví dụ 1: đổi chỗ hai biến', R('a = 3\nb = 8\na, b = b, a\nprint(a, b)') + note('Python cho phép đổi chỗ trong một dòng. Ở ngôn ngữ khác phải dùng biến tạm.')),
         eg('Ví dụ 2: tiền lãi', R('so_tien = 1000000\nso_tien = so_tien * 1.05\nso_tien = so_tien * 1.05\nprint(so_tien)'))],
        [('Đoán kết quả rồi chạy: <code>x = 4; y = x * 2; x = x + 1; print(x, y)</code>.', R('x = 4\ny = x * 2\nx = x + 1\nprint(x, y)') + note('y được tính khi x còn 4 nên y = 8; x sau đó thành 5.'), None),
         ('In ra <code>"5" * 3</code> và <code>5 * 3</code>. Giải thích vì sao khác nhau.', R('print("5" * 3)\nprint(5 * 3)') + '<p>“5” là chữ nên nhân với 3 là lặp chữ 3 lần; 5 là số nên nhân với 3 là phép nhân.</p>', None),
         ('Đổi chỗ hai biến a = 3, b = 8 bằng <b>biến tạm</b> (không dùng cách viết một dòng) rồi in ra.', R('a = 3\nb = 8\nt = a\na = b\nb = t\nprint(a, b)'), None),
         ('<b>Nghĩ ngược:</b> sau <code>x = x * 3 + 2</code> thì x = 29. Giá trị x trước đó là bao nhiêu? Kiểm tra bằng code.', '<p>Ngược: 29 − 2 = 27; 27 ÷ 3 = <b>9</b>.</p>' + R('x = 9\nx = x * 3 + 2\nprint(x)'), None),
         ('<b>Thử thách:</b> gửi 1 000 000 đồng, lãi 5%/năm, lãi nhập gốc. Sau 3 năm có bao nhiêu? Ngược lại, nếu sau 3 năm có 1 157 625 đồng thì số tiền gửi ban đầu là bao nhiêu?', R('tien = 1000000\ntien = tien * 1.05\ntien = tien * 1.05\ntien = tien * 1.05\nprint(round(tien))\nban_dau = 1157625 / 1.05 / 1.05 / 1.05\nprint(round(ban_dau))') + '<p>Đi ngược 3 lần: chia 1,05 ba lần. Kết quả khớp: 1 000 000.</p>', None)],
        'Python')

    # ---------------- Bài 3 ----------------
    p3 = 'd = 8\nif d >= 8:\n    xl = "Giỏi"\nelif d >= 5:\n    xl = "Khá"\nelse:\n    xl = "Yếu"\nprint(xl)'
    ham3 = 'def xep_loai(d):\n    if d >= 8:\n        return "Giỏi"\n    elif d >= 5:\n        return "Khá"\n    else:\n        return "Yếu"\n'
    P['bai3'] = std('Bài 3 · Điều kiện if và kiểm thử biên', 'Lỗi thường nằm ở ranh giới.',
        ('Viết if/elif/else; chọn bộ test gồm giá trị thường, biên và bất thường', 'Python 3 và IDLE', 'Hàm xếp loại kèm bảng test'),
        ['Chương trình hữu ích phải biết <b>chọn</b> việc làm theo tình huống.', '<code>if</code> là công cụ chọn quan trọng nhất của mọi ngôn ngữ.', 'Nó cũng là nơi dễ sai nhất, nên bài này dạy cả cách <b>kiểm thử ranh giới</b>.'],
        ol(['Viết điều kiện bằng lời, đổi thành phép so sánh.', 'Liệt kê các trường hợp: nhánh nào chạy khi nào.', 'Xếp <code>if</code> từ trường hợp <b>hẹp/cao nhất</b> xuống.', 'Lập bảng test: giá trị thường, biên, bất thường.']),
        think(['<b>Phản biện:</b> đừng thử một giá trị rồi kết luận. Hãy tìm giá trị làm chương trình sai: ranh giới 8, 7,9, 5, 4,9.', '<b>Ngược:</b> từ kết quả mong muốn (“Khá”) suy ra điều kiện <b>5 ≤ d &lt; 8</b>.'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['Sau <code>if</code>, <code>elif</code>, <code>else</code> luôn có dấu <b>hai chấm</b> và khối lệnh <b>thụt vào 4 dấu cách</b>.', 'Chỉ nhánh đầu tiên đúng được chạy.']) + R(ham3 + 'for d in [10, 8, 7.9, 5, 4.9, 0]:\n    print(d, xep_loai(d))'),
        decision_svg('d >= 8 ?', '“Giỏi”', 'xét tiếp d >= 5') + ptrace(p3, captions=['Gán <code>d = 8</code>.', 'Kiểm tra <code>d >= 8</code>: 8 ≥ 8 <b>đúng</b>.', 'Vào nhánh đầu: gán <code>xl = "Giỏi"</code>; các nhánh elif, else bị bỏ qua.', 'Nhảy tới dòng <code>print</code> và in “Giỏi”.']),
        [err('Dùng &gt; thay vì &gt;=', 'Điểm 8 bị xếp “Khá”:' + R(ham3.replace('d >= 8', 'd > 8') + 'print(xep_loai(8))'), 'Xác định số ở ranh giới thuộc nhóm nào rồi chọn <code>&gt;=</code> hay <code>&gt;</code>.'),
         err('Sắp elif sai thứ tự', 'Kiểm tra <code>d &gt;= 5</code> trước thì điểm 9 cũng thành “Khá”:' + R('def xl(d):\n    if d >= 5:\n        return "Khá"\n    elif d >= 8:\n        return "Giỏi"\nprint(xl(9))'), 'Điều kiện chặt nhất (≥ 8) phải đặt trước.'),
         err('Quên dấu hai chấm', 'Python báo lỗi:' + ERR('if 1 > 0\n    print(1)'), 'Nhớ dấu <code>:</code> cuối dòng if/elif/else.'),
         err('So sánh chữ với số', 'Chuỗi so sánh theo thứ tự chữ cái, không theo giá trị số:' + R('print("10" < "9")\nprint(10 < 9)'), 'Đổi sang số bằng <code>int()</code> trước khi so sánh.')],
        [eg('Ví dụ 1: bộ test cho xếp loại', R(ham3 + 'tests = [(10, "Giỏi"), (8, "Giỏi"), (7.9, "Khá"), (5, "Khá"), (4.9, "Yếu"), (0, "Yếu")]\nfor d, mong_doi in tests:\n    print(d, xep_loai(d) == mong_doi)')),
         eg('Ví dụ 2: năm nhuận', R('def nhuan(n):\n    return (n % 4 == 0 and n % 100 != 0) or n % 400 == 0\nfor n in [1900, 2000, 2023, 2024]:\n    print(n, nhuan(n))') + note('Năm chia hết cho 100 chỉ nhuận khi chia hết cho 400. Các năm 1900 và 2000 là test biên.'))],
        [('Viết hàm cho biết một số là <b>chẵn</b> hay <b>lẻ</b>. Thử với 0, 7, 10.', R('def chan_le(n):\n    if n % 2 == 0:\n        return "chẵn"\n    else:\n        return "lẻ"\nfor n in [0, 7, 10]:\n    print(n, chan_le(n))'), None),
         ('Viết hàm xếp loại 3 mức (≥ 8 Giỏi, ≥ 5 Khá, còn lại Yếu) và test 6 giá trị 10, 8, 7.9, 5, 4.9, 0.', R(ham3 + 'for d in [10, 8, 7.9, 5, 4.9, 0]:\n    print(d, xep_loai(d))'), None),
         ('Giá vé: dưới 6 tuổi miễn phí; 6–11 tuổi 20 000; từ 12 tuổi 40 000. Viết hàm <code>gia_ve(tuoi)</code> và tính tổng cho nhóm tuổi 5, 6, 11, 12.', R('def gia_ve(tuoi):\n    if tuoi < 6:\n        return 0\n    elif tuoi < 12:\n        return 20000\n    else:\n        return 40000\nprint(sum(gia_ve(t) for t in [5, 6, 11, 12]))') + note('Các tuổi 5, 6, 11, 12 chính là test biên của bài.'), None),
         ('<b>Nghĩ ngược:</b> điểm nào thì được xếp “Khá”? Viết khoảng, rồi chọn bộ test biên để chắc hàm đúng.', '<p>Khoảng: <b>5 ≤ d &lt; 8</b>. Test biên: 4.9 (Yếu), 5 (Khá), 7.9 (Khá), 8 (Giỏi).</p>' + R(ham3 + 'for d in [4.9, 5, 7.9, 8]:\n    print(d, xep_loai(d))'), None),
         ('<b>Thử thách:</b> viết hàm năm nhuận rồi tìm <b>năm nhuận đầu tiên sau 2025</b>. Dùng test biên 1900, 2000, 2100.', R('def nhuan(n):\n    return (n % 4 == 0 and n % 100 != 0) or n % 400 == 0\nfor n in [1900, 2000, 2100]:\n    print(n, nhuan(n))\nn = 2026\nwhile not nhuan(n):\n    n += 1\nprint("Năm nhuận tiếp theo:", n)'), None)],
        'Python')

    # ---------------- Bài 4 ----------------
    p4 = 'tong = 0\nfor i in range(1, 5):\n    tong += i\nprint(tong)'
    P['bai4'] = std('Bài 4 · Vòng lặp và lỗi lệch một', 'Làm việc lặp lại một cách chắc chắn.',
        ('Dùng for và while; hiểu range(a, b) dừng trước b; tránh lỗi lệch một', 'Python 3 và IDLE', 'Chương trình tính tổng, in bảng nhân và đếm bước lặp'),
        ['Máy tính nhàm chán thì không bao giờ mệt: <b>vòng lặp</b> cho nó làm việc hàng triệu lần.', 'Bài này dạy bạn viết vòng lặp <b>đúng số lần</b> – lỗi “lệch một” là lỗi phổ biến nhất.', 'Nó cũng giúp bạn nhận ra khi nào nên dùng công thức thay vì lặp.'],
        ol(['Xác định <b>cái gì lặp lại</b> và <b>lặp mấy lần / đến khi nào</b>.', 'Chọn <code>for</code> khi biết số lần, <code>while</code> khi lặp đến khi điều kiện sai.', 'Khởi tạo biến tích lũy <b>trước</b> vòng lặp (ví dụ <code>tong = 0</code>).', 'Thử với <b>n nhỏ</b> (0, 1, 2) để bắt lỗi lệch.']),
        think(['<b>Phản biện:</b> tính tổng 1 đến n bằng vòng lặp và bằng công thức n(n+1)/2: hai cách phải cho cùng kết quả.', '<b>Ngược:</b> thay vì hỏi “tổng 1..n là bao nhiêu”, hỏi “n nhỏ nhất để tổng vượt 1000 là bao nhiêu?”.'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['<code>range(1, 5)</code> chạy 1, 2, 3, 4 – <b>không gồm 5</b>.', '<code>tong += i</code> là viết gọn của <code>tong = tong + i</code>.']) + R(p4) + R('for i in range(1, 4):\n    print(7, "x", i, "=", 7 * i)'),
        flowrow(['tong = 0', 'lấy i tiếp|theo trong range', 'tong += i', 'hết i?|in tong'], 'Vòng lặp for: lặp lại bước giữa cho tới hết') + ptrace(p4, maxn=7),
        [err('Lỗi lệch một', 'Muốn in đến 5 mà viết <code>range(1, 5)</code>:' + R('for i in range(1, 5):\n    print(i)'), 'Muốn tới n phải viết <code>range(1, n + 1)</code>.'),
         err('Đặt tong = 0 bên trong vòng lặp', 'Mỗi vòng tổng bị đặt lại:' + R('for i in range(1, 5):\n    tong = 0\n    tong += i\nprint(tong)'), 'Khởi tạo biến tích lũy <b>trước</b> vòng lặp.'),
         err('Vòng while không bao giờ dừng', 'Quên cập nhật biến điều kiện thì chương trình chạy mãi (nhấn Ctrl+C để dừng).', 'Chắc chắn trong thân while có lệnh làm điều kiện tiến tới sai.'),
         err('Thụt dòng print vào trong vòng lặp', 'In ra kết quả ở mỗi vòng thay vì chỉ cuối cùng:' + R('tong = 0\nfor i in range(1, 4):\n    tong += i\n    print(tong)'), 'Đưa <code>print</code> ra ngang hàng với <code>for</code> nếu chỉ cần kết quả cuối.')],
        [eg('Ví dụ 1: tổng 1 đến 10 và kiểm chứng bằng công thức', R('n = 10\ntong = 0\nfor i in range(1, n + 1):\n    tong += i\nprint(tong, n * (n + 1) // 2)')),
         eg('Ví dụ 2: while đếm số lần chia đôi', R('n = 100\nso_lan = 0\nwhile n > 1:\n    n = n // 2\n    so_lan += 1\nprint(so_lan)'))],
        [('In các số từ 1 đến 5, mỗi số một dòng.', R('for i in range(1, 6):\n    print(i)'), None),
         ('Tính tổng 1 + 2 + … + 100 bằng vòng lặp và kiểm chứng bằng công thức n(n+1)/2.', R('tong = 0\nfor i in range(1, 101):\n    tong += i\nprint(tong, 100 * 101 // 2)'), None),
         ('In bảng cửu chương 9 (từ 9 × 1 đến 9 × 10).', R('for i in range(1, 11):\n    print("9 x", i, "=", 9 * i)'), None),
         ('<b>Nghĩ ngược:</b> n nhỏ nhất để 1 + 2 + … + n lớn hơn 1000 là bao nhiêu?', R('tong = 0\nn = 0\nwhile tong <= 1000:\n    n += 1\n    tong += n\nprint(n, tong)\nprint(44 * 45 // 2)') + '<p>Đáp án: <b>45</b> (tổng 1035). Với n = 44 tổng chỉ là 990, chưa vượt 1000.</p>', None),
         ('<b>Thử thách:</b> “dãy Collatz”: bắt đầu từ n; nếu n chẵn thì chia 2, nếu lẻ thì nhân 3 cộng 1; dừng khi n = 1. Bắt đầu từ n = 6 cần bao nhiêu bước? In ra cả dãy.', R('n = 6\nbuoc = 0\nday = [n]\nwhile n != 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n        n = 3 * n + 1\n    day.append(n)\n    buoc += 1\nprint(day)\nprint(buoc)') + '<p>Phản biện: có số nào chạy mãi không? Đến nay chưa ai tìm được, cũng chưa ai chứng minh – một bài toán mở nổi tiếng.</p>', None)],
        'Python')

    # ---------------- Bài 5 ----------------
    p5 = 'ds = [5, 9, 2, 9, 7, 3]\nkq = ds[0]\nfor x in ds:\n    if x > kq:\n        kq = x\nprint(kq)'
    P['bai5'] = std('Bài 5 · Danh sách và hàm', 'Gom dữ liệu lại, đóng gói việc lặp lại.',
        ('Dùng list và hàm; tìm số lớn nhất, đếm, tính trung bình; hiểu chỉ số bắt đầu từ 0', 'Python 3 và IDLE', 'Bộ hàm xử lý danh sách điểm'),
        ['<b>List</b> chứa nhiều giá trị trong một biến: danh sách điểm, giá, tên…', '<b>Hàm</b> là cỗ máy nhỏ nhận đầu vào, trả đầu ra – viết một lần, dùng nhiều lần.', 'Hai công cụ này đủ để giải rất nhiều bài toán xử lý dữ liệu thực tế.'],
        ol(['Gom dữ liệu vào list.', 'Chia việc thành các hàm nhỏ, mỗi hàm làm đúng một việc.', 'Mỗi hàm: <b>nhận gì, trả gì</b>? Viết ra trước.', 'Test mỗi hàm riêng với dữ liệu nhỏ, kể cả danh sách rỗng.']),
        think(['<b>Phản biện:</b> hàm đúng với danh sách thường, nhưng có đúng với danh sách rỗng, một phần tử, hoặc các phần tử trùng nhau?', '<b>Ngược:</b> biết trung bình và các phần tử, suy ngược phần tử còn thiếu: tổng = trung bình × số phần tử.'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['<code>ds[0]</code> là phần tử đầu; <code>ds[-1]</code> là phần tử cuối; <code>len(ds)</code> số phần tử.', '<code>def ten(tham_so):</code> định nghĩa hàm; <code>return</code> trả kết quả về.']) + R('def lon_nhat(ds):\n    kq = ds[0]\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\n\nds = [5, 9, 2, 9, 7, 3]\nprint(lon_nhat(ds))\nprint(ds.count(9))\nprint(round(sum(ds) / len(ds), 2))'),
        list_svg([5, 9, 2, 9, 7, 3]) + ptrace(p5, maxn=7),
        [err('Chỉ số vượt phạm vi', 'List 6 phần tử có chỉ số 0–5; <code>ds[6]</code> báo lỗi:' + ERR('ds = [5, 9, 2, 9, 7, 3]\nprint(ds[6])'), 'Phần tử cuối là <code>ds[len(ds) - 1]</code> hoặc <code>ds[-1]</code>.'),
         err('Danh sách rỗng', '<code>ds[0]</code> trên list rỗng báo lỗi:' + ERR('ds = []\nprint(ds[0])'), 'Kiểm tra <code>if not ds:</code> trước khi lấy phần tử.'),
         err('Quên return', 'Hàm chỉ in mà không trả về nên kết quả là None:' + R('def tong(ds):\n    s = sum(ds)\nprint(tong([1, 2, 3]))'), 'Dùng <code>return s</code> để trả giá trị cho chỗ gọi hàm.'),
         err('Khởi tạo max = 0', 'Với toàn số âm hàm trả về 0 (không có trong danh sách):' + R('def lon(ds):\n    kq = 0\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\nprint(lon([-5, -2, -9]))'), 'Khởi tạo bằng phần tử đầu: <code>kq = ds[0]</code>.')],
        [eg('Ví dụ 1: hàm trung bình có kiểm tra rỗng', R('def trung_binh(ds):\n    if not ds:\n        return 0\n    return sum(ds) / len(ds)\nprint(trung_binh([4, 6, 8]), trung_binh([]))')),
         eg('Ví dụ 2: lọc số chẵn', R('def so_chan(ds):\n    kq = []\n    for x in ds:\n        if x % 2 == 0:\n            kq.append(x)\n    return kq\nprint(so_chan([1, 2, 3, 4, 6]))'))],
        [('Cho <code>ds = [5, 9, 2, 9, 7, 3]</code>. In phần tử đầu, phần tử cuối và số phần tử.', R('ds = [5, 9, 2, 9, 7, 3]\nprint(ds[0], ds[-1], len(ds))'), None),
         ('Điểm 6 bạn là 5, 9, 2, 9, 7, 3. In điểm cao nhất, số bạn đạt điểm cao nhất, và điểm trung bình (2 số lẻ).', R('ds = [5, 9, 2, 9, 7, 3]\nprint(max(ds), ds.count(max(ds)), round(sum(ds) / len(ds), 2))'), '<pre class="pdata">5\n9\n2\n9\n7\n3</pre>'),
         ('Viết hàm <code>dem_tren_tb(ds)</code> đếm số bạn có điểm cao hơn trung bình. Thử với dữ liệu trên.', R('def dem_tren_tb(ds):\n    tb = sum(ds) / len(ds)\n    dem = 0\n    for x in ds:\n        if x > tb:\n            dem += 1\n    return dem\nprint(dem_tren_tb([5, 9, 2, 9, 7, 3]))') + note('Trung bình 5,83: các điểm 9, 9, 7 cao hơn.'), None),
         ('<b>Nghĩ ngược:</b> 5 bạn có điểm trung bình 8. Bốn bạn có điểm 6, 9, 7, 10. Bạn thứ năm được mấy điểm?', '<p>Tổng 5 bạn = 8 × 5 = 40. Bốn bạn đầu: 6 + 9 + 7 + 10 = 32. Bạn thứ năm: <b>8</b>.</p>' + R('ds = [6, 9, 7, 10, 8]\nprint(sum(ds) / len(ds))'), None),
         ('<b>Thử thách:</b> viết hàm tìm <b>số lớn thứ hai khác nhau</b> trong danh sách; test với [5, 9, 2, 9, 7, 3], [9, 9, 5], và danh sách rỗng (trả về None).', R('def lon_nhi(ds):\n    kx = sorted(set(ds))\n    if len(kx) < 2:\n        return None\n    return kx[-2]\nprint(lon_nhi([5, 9, 2, 9, 7, 3]))\nprint(lon_nhi([9, 9, 5]))\nprint(lon_nhi([]))') + '<p>Ý chính: dùng <code>set</code> để bỏ phần tử trùng, nên [9, 9, 5] ra 5, không ra 9.</p>', None)],
        'Python')

    # ---------------- Bài 6 ----------------
    p6 = 'x = 7\nx = x * 3\nx = x + 4\nx = x * 2\nprint(x)'
    P['bai6'] = std('Bài 6 · Tư duy ngược', 'Đi từ kết quả về điều kiện ban đầu.',
        ('Giải bài bằng cách đảo thứ tự và phép tính; dùng vét cạn khi khó đi ngược; kiểm chứng ngược', 'Python 3 và IDLE', 'Cặp hàm xuôi – ngược kiểm tra lẫn nhau'),
        ['Nhiều vấn đề thực tế cho biết <b>kết quả</b> và hỏi <b>nguyên nhân</b>: lỗi nằm ở đâu, cần bao nhiêu vốn, bắt đầu lúc mấy giờ.', '<b>Tư duy ngược</b> là công cụ mạnh để lập kế hoạch và tìm lỗi.', 'Khi không đi ngược được bằng toán, ta nhờ máy <b>thử mọi khả năng</b>.'],
        ol(['Viết quá trình <b>xuôi</b> bằng các phép tính.', 'Đổi mỗi phép sang <b>phép nghịch đảo</b> và <b>đảo thứ tự</b>.', 'Nếu quá khó, dùng vòng lặp thử mọi giá trị trong một khoảng.', '<b>Kiểm chứng xuôi</b> đáp án tìm được.']),
        think(['<b>Ngược:</b> “Điều kiện cuối cùng cần để có kết quả này là gì? Trước đó là gì?”', '<b>Phản biện:</b> phép ngược có thể cho <b>nhiều đáp án</b> (ví dụ phép bình phương): đề bài đã đủ để chọn một đáp án chưa?'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['Viết hàm <code>xuoi</code>, rồi hàm <code>nguoc</code>, và dùng chúng kiểm tra nhau.', '<code>nguoc(xuoi(n)) == n</code> là bài test rất đẹp.']) + R('def xuoi(n):\n    return (n * 3 + 4) * 2\n\ndef nguoc(kq):\n    return (kq // 2 - 4) // 3\n\nprint(xuoi(7))\nprint(nguoc(xuoi(7)))'),
        reverse_svg(['× 3', '+ 4', '× 2'], ['÷ 2', '− 4', '÷ 3'], '7', '50', 'Xuôi và ngược: nhân 3, cộng 4, nhân 2') + ptrace(p6, pick=[0, 1, 2, 3, 4], captions=['Bắt đầu: x = 7.', 'Nhân 3: x = 21.', 'Cộng 4: x = 25.', 'Nhân 2: x = 50.', 'In ra 50. Đi ngược từ 50 sẽ ra lại 7.']),
        [err('Không đảo thứ tự', 'Chia 3 trước rồi mới chia 2 sẽ sai:' + R('kq = 50\nprint((kq // 3 - 4) // 2)'), 'Bước làm <b>sau cùng</b> khi đi xuôi phải được hoàn tác <b>đầu tiên</b>.'),
         err('Không đổi phép tính', 'Gặp “+ 4” vẫn cộng 4 khi đi ngược.', 'Cộng ↔ trừ, nhân ↔ chia, bình phương ↔ căn bậc hai (nhớ cả dấu âm).'),
         err('Bỏ qua đáp án thứ hai', 'Bình phương làm mất thông tin dấu: (−3)² = 3² = 9.', 'Khi đi ngược qua phép bình phương, xét cả hai căn.'),
         err('Không kiểm chứng xuôi', 'Tính ngược sai mà không biết.', 'Luôn chạy <code>xuoi(dap_an)</code> xem có ra kết quả đề cho không.')],
        [eg('Ví dụ 1: tìm n bằng vét cạn', R('for n in range(1, 1000):\n    if n * n + n == 156:\n        print(n)\n        break')),
         eg('Ví dụ 2: hoàn tác chuỗi thao tác', R('def xuoi(s):\n    return s.upper()[::-1]\nprint(xuoi("tuduy"))\nprint(xuoi(xuoi("tuduy")).lower() == "tuduy")') + note('Có thao tác xuôi “đảo chữ, viết hoa”; làm lại đúng thao tác đảo chữ sẽ trở về chuỗi gốc.'))],
        [('Một số nhân 5 rồi cộng 2 được 37. Số đó là bao nhiêu? Kiểm tra bằng code.', '<p>Ngược: 37 − 2 = 35; 35 ÷ 5 = <b>7</b>.</p>' + R('x = 7\nprint(x * 5 + 2)'), None),
         ('Một số trừ 3 rồi nhân 4 được 36. Số đó là bao nhiêu?', '<p>36 ÷ 4 = 9; 9 + 3 = <b>12</b>.</p>' + R('x = 12\nprint((x - 3) * 4)'), None),
         ('Viết hàm xuôi <code>f(n) = (n * 3 + 4) * 2</code> và hàm ngược <code>g</code>, test <code>g(f(n)) == n</code> với n = 0, 1, 7, 100.', R('def f(n):\n    return (n * 3 + 4) * 2\ndef g(kq):\n    return (kq // 2 - 4) // 3\nfor n in [0, 1, 7, 100]:\n    print(n, g(f(n)) == n)'), None),
         ('Tìm <b>mọi số nguyên</b> n sao cho n² + n = 156 (kể cả số âm) bằng vòng lặp.', R('kq = []\nfor n in range(-100, 100):\n    if n * n + n == 156:\n        kq.append(n)\nprint(kq)') + '<p>Có hai nghiệm: 12 và −13. Chỉ xét n dương sẽ bỏ sót một đáp án.</p>', None),
         ('<b>Thử thách:</b> Số nào nhân 5, trừ 8, rồi bình phương cho 169? Tìm bằng cách làm ngược, sau đó kiểm tra mọi đáp án bằng code. Thêm bài kẹo: Lan cho Mai một nửa số kẹo và thêm 1 cái, rồi cho Nam một nửa số còn lại và thêm 1 cái, còn 2 cái. Ban đầu có bao nhiêu?',
          '<p>Ngược: căn 169 = ±13; cộng 8 được 21 hoặc −5; chia 5 được 4,2 hoặc −1.</p>' + R('for x in [4.2, -1]:\n    print(x, ((x * 5) - 8) ** 2)') + '<p>Cả hai đều thỏa; nếu đề yêu cầu số nguyên thì <b>x = −1</b>.</p><p>Bài kẹo đi ngược 2 lần (mỗi lần: cộng 1 rồi nhân 2):</p>' + R('con = 2\nfor _ in range(2):\n    con = (con + 1) * 2\nprint(con)\nk = 14\nfor _ in range(2):\n    k = k - (k // 2 + 1)\nprint(k)') + '<p>Ban đầu 14 cái; kiểm tra xuôi còn lại đúng 2 cái.</p>', None)],
        'Python')

    # ---------------- Bài 7 ----------------
    bug7 = 'def dem_chan(ds):\n    dem = 0\n    for x in ds:\n        if x % 2 == 1:\n            dem += 1\n    return dem\n\nassert dem_chan([1, 2, 3, 4, 6]) == 3'
    fix7 = bug7.replace('x % 2 == 1', 'x % 2 == 0')
    P['bai7'] = std('Bài 7 · Gỡ lỗi và viết test', 'Bằng chứng thay cho cảm giác.',
        ('Dùng assert để tự kiểm thử; theo quy trình tìm lỗi có hệ thống', 'Python 3 và IDLE', 'Bộ test cho một hàm và nhật ký 5 lỗi đã sửa'),
        ['Phần lớn thời gian của lập trình viên là <b>đọc, thử và sửa lỗi</b>.', 'Biết gỡ lỗi có hệ thống tiết kiệm hàng giờ mò mẫm.', '<b>Test</b> biến “tôi nghĩ nó đúng” thành “tôi có bằng chứng nó đúng”.'],
        ol(['<b>Tái hiện:</b> tìm đầu vào làm lỗi xuất hiện.', '<b>Thu hẹp:</b> in giá trị biến giữa chừng để biết sai từ dòng nào.', '<b>Giả thuyết:</b> đoán nguyên nhân, sửa <b>một chỗ</b>, chạy lại.', '<b>Chặn tái phạm:</b> thêm một <code>assert</code> cho lỗi vừa sửa.']),
        think(['<b>Phản biện:</b> “Điều gì làm cho hàm này sai?” – chủ động tìm giá trị làm hỏng nó, đừng chỉ chứng minh nó đúng.', '<b>Ngược:</b> từ kết quả sai, lần ngược theo dòng chạy tới chỗ giá trị bắt đầu lệch.'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['<code>assert điều_kiện</code>: nếu sai Python báo lỗi ngay; nếu đúng không in gì.', 'Đọc <b>dòng cuối</b> của thông báo lỗi trước: nó nói loại lỗi và gợi ý dòng sai.']) + R('def trung_binh(ds):\n    return sum(ds) / len(ds)\n\nassert trung_binh([4, 6, 8]) == 6\nassert trung_binh([5]) == 5\nassert trung_binh([0, 10]) == 5\nprint("Tất cả test đều qua")'),
        steps(('<b>Tái hiện:</b> chạy test và thấy lỗi.', code(bug7) + '<div class="code-out-l">Kết quả khi chạy</div><pre class="code out">%s</pre>' % E(runerr(bug7))),
              ('<b>Thu hẹp:</b> in ra xem hàm đếm được bao nhiêu. Máy trả 2, mong đợi 3.', R('def dem_chan(ds):\n    dem = 0\n    for x in ds:\n        if x % 2 == 1:\n            dem += 1\n    return dem\nprint(dem_chan([1, 2, 3, 4, 6]))')),
              ('<b>Giả thuyết:</b> hàm đang đếm số <b>lẻ</b> (1 và 3 → 2). Điều kiện <code>x % 2 == 1</code> sai.', '<p class="tnote">Số chẵn có phần dư 0 khi chia 2, nên điều kiện đúng là <code>x % 2 == 0</code>.</p>'),
              ('<b>Sửa và chặn tái phạm:</b> đổi thành <code>== 0</code>, giữ lại assert làm test.', code(fix7) + '<p class="tnote">Chạy lại: không in lỗi gì, test đã qua.</p>')),
        [err('Sửa nhiều chỗ cùng lúc', 'Không biết sửa chỗ nào mới có tác dụng.', 'Mỗi lần chỉ đổi một chỗ rồi chạy lại.'),
         err('Không đọc thông báo lỗi', 'Thông báo cuối nói rõ loại lỗi và số dòng:' + ERR('x = [1, 2]\nprint(x[5])'), 'Đọc từ dòng cuối: <b>IndexError</b> nghĩa là chỉ số vượt phạm vi.'),
         err('Chỉ test trường hợp dễ', 'Hàm đúng với [4, 6, 8] nhưng sập với danh sách rỗng:' + ERR('def tb(ds):\n    return sum(ds) / len(ds)\nprint(tb([]))'), 'Luôn thêm test biên: rỗng, một phần tử, giá trị âm, số lớn.'),
         err('Xóa lỗi mà không hiểu', 'Bọc try/except cho im lặng thì lỗi vẫn còn, chỉ bị giấu đi.', 'Tìm nguyên nhân thật; chỉ dùng try/except khi chủ động xử lý được.')],
        [eg('Ví dụ 1: assert bắt lỗi biên', R('def lon_nhat(ds):\n    kq = ds[0]\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\nassert lon_nhat([3, 9, 2]) == 9\nassert lon_nhat([-5, -2, -9]) == -2\nassert lon_nhat([7]) == 7\nprint("ok")')),
         eg('Ví dụ 2: in biến giữa chừng để thu hẹp', R('tong = 0\nfor i in range(1, 6):\n    tong += i\n    print("i =", i, " tong =", tong)'))],
        [('Dòng sau lỗi gì? Sửa: <code>if x &gt; 3</code> rồi <code>print("lớn")</code> thụt dòng.' + code('x = 5\nif x > 3\n    print("lớn")'), '<p>Thiếu dấu hai chấm sau điều kiện:</p>' + code('x = 5\nif x > 3\n    print("lớn")', runerr('x = 5\nif x > 3\n    print("lớn")')) + R('x = 5\nif x > 3:\n    print("lớn")'), None),
         ('Tính tổng 1 đến 10 nhưng máy ra 45 thay vì 55. Tìm lỗi.' + R('tong = 0\nfor i in range(1, 10):\n    tong += i\nprint(tong)'), '<p>Lỗi lệch một: <code>range(1, 10)</code> dừng ở 9. Sửa thành <code>range(1, 11)</code>.</p>' + R('tong = 0\nfor i in range(1, 11):\n    tong += i\nprint(tong)'), None),
         ('Hàm tìm số lớn nhất trả về 0 với danh sách [−5, −2, −9]. Tìm lỗi và viết assert chặn lỗi.' + R('def lon(ds):\n    kq = 0\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\nprint(lon([-5, -2, -9]))'), '<p>Khởi tạo <code>kq = 0</code> làm số âm không bao giờ lớn hơn. Sửa: <code>kq = ds[0]</code>.</p>' + R('def lon(ds):\n    kq = ds[0]\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\nassert lon([-5, -2, -9]) == -2\nprint("ok")'), None),
         ('<b>Nghĩ ngược:</b> hàm <code>dem_chan</code> trả 2 cho [1, 2, 3, 4, 6] trong khi mong đợi 3. Hãy suy ngược: lỗi có thể nằm ở những dòng nào? Chọn bộ test nhỏ nhất để xác định chính xác.', '<p>Chỉ có hai nghi phạm: điều kiện <code>x % 2 == ?</code> và chỗ tăng đếm. Thử với <b>[2]</b> (đáng ra 1) và <b>[1]</b> (đáng ra 0): hàm lỗi ở trên trả 0 và 1 – ngược hẳn, chứng tỏ điều kiện bị đảo.</p>' + R('def dem_chan(ds):\n    dem = 0\n    for x in ds:\n        if x % 2 == 1:\n            dem += 1\n    return dem\nprint(dem_chan([2]), dem_chan([1]))'), None),
         ('<b>Thử thách:</b> hàm trung bình sau có <b>hai lỗi</b>. Tìm cả hai, sửa, viết 4 assert (gồm trường hợp rỗng).' + R('def tb(ds):\n    return sum(ds) // len(ds)\nprint(tb([4, 5]), tb([]) if False else "(rỗng sẽ gây lỗi)")'), '<p>Lỗi 1: dùng <code>//</code> (chia nguyên) nên [4, 5] ra 4 thay vì 4.5. Lỗi 2: danh sách rỗng gây chia cho 0.</p>' + R('def tb(ds):\n    if not ds:\n        return 0\n    return sum(ds) / len(ds)\nassert tb([4, 5]) == 4.5\nassert tb([6]) == 6\nassert tb([0, 10]) == 5\nassert tb([]) == 0\nprint("Tất cả test đều qua")'), None)],
        'Python')

    # ---------------- Bài 8 ----------------
    ds8 = 'Ăn uống\t450000\nĂn uống\t380000\nHọc tập\t300000\nGiải trí\t150000\nHọc tập\t220000\nGiải trí\t90000'
    c8 = 'du_lieu = [("Ăn uống", 450000), ("Ăn uống", 380000), ("Học tập", 300000),\n           ("Giải trí", 150000), ("Học tập", 220000), ("Giải trí", 90000)]\ntong = {}\nfor muc, so_tien in du_lieu:\n    tong[muc] = tong.get(muc, 0) + so_tien\nfor muc in tong:\n    print(muc, tong[muc])\nprint("Tổng:", sum(tong.values()))'
    mini8 = 'du_lieu = [("Ăn uống", 450), ("Học tập", 300), ("Ăn uống", 380)]\ntong = {}\nfor muc, tien in du_lieu:\n    tong[muc] = tong.get(muc, 0) + tien\nprint(tong)'
    P['bai8'] = std('Bài 8 · Dự án: sổ chi tiêu có kiểm chứng', 'Ghép mọi thứ đã học vào một bài toán thật.',
        ('Hoàn thành chương trình thống kê chi tiêu; ghi rõ giả định; kiểm chứng kết quả', 'Python 3 và IDLE', 'Chương trình thống kê, 3 test và một đoạn nêu giả định'),
        ['Ghép biến, điều kiện, vòng lặp, list và hàm vào một sản phẩm có ích.', 'Bạn thực hành <b>lập kế hoạch từ đích về</b> và <b>kiểm chứng như một nhà phản biện</b>.', 'Sản phẩm này là bản mẫu cho mọi chương trình xử lý số liệu sau này.'],
        ol(['Viết <b>đích</b>: cần in ra những con số nào?', '<b>Nghĩ ngược</b> ra các phần cần có (dữ liệu, cộng theo mục, in).', 'Làm từng phần, chạy với dữ liệu nhỏ trước.', 'Viết test và danh sách giả định; kiểm chứng chéo kết quả.']),
        think(['<b>Ngược:</b> Đích “mỗi mục tiêu bao nhiêu” → cần cộng dồn theo mục → cần cấu trúc “mục → tổng” (dict) → cần danh sách các khoản chi.', '<b>Phản biện:</b> “Giả định nào đang ẩn? Tổng các mục có bằng tổng các khoản gốc không? Dữ liệu rỗng hay số âm thì sao?”'], 'Hai câu hỏi nền tảng'),
        'Ứng dụng vào Python',
        li(['<code>dict</code> lưu cặp “khóa → giá trị”: <code>tong["Ăn uống"] = 830000</code>.', '<code>tong.get(muc, 0)</code> lấy giá trị hiện có, mặc định 0 nếu chưa có.']) + R(c8),
        flowrow(['Dữ liệu|các khoản chi', 'Cộng dồn|theo mục', 'Kiểm chứng|tổng mục = tổng gốc', 'In kết quả|+ giả định'], 'Các phần của dự án') + ptrace(mini8, maxn=7),
        [err('Dữ liệu lẫn dấu cách hoặc chữ hoa/thường', '“Ăn uống” và “ăn uống ” bị tính thành hai mục.', 'Chuẩn hóa tên mục: <code>muc.strip().lower()</code> trước khi cộng.'),
         err('Quên số âm (hoàn tiền)', 'Khoản hoàn tiền ghi âm vẫn cộng bình thường nhưng ý nghĩa khác chi tiêu.', 'Quyết định và ghi rõ: tính vào tổng hay tách riêng.'),
         err('Không kiểm chứng tổng', 'Cộng thiếu một khoản mà không biết.', 'So tổng các mục với tổng trực tiếp: <code>sum(v for _, v in du_lieu)</code>.'),
         err('Chia cho 0 khi tính phần trăm', 'Dữ liệu rỗng làm tổng bằng 0:' + ERR('tong = 0\nprint(100 * 5 / tong)'), 'Kiểm tra <code>if tong == 0</code> trước khi chia.')],
        [eg('Ví dụ 1: kiểm chứng chéo', R(c8 + '\nassert sum(tong.values()) == sum(v for _, v in du_lieu)\nprint("Khớp tổng")')),
         eg('Ví dụ 2: mục chi nhiều nhất và phần trăm', R(c8 + '\ntop = max(tong, key=tong.get)\nprint(top, round(tong[top] * 100 / sum(tong.values()), 1), "%")'))],
        [('Tính <b>tổng chi</b> của 6 khoản dưới đây.', R('du_lieu = [450000, 380000, 300000, 150000, 220000, 90000]\nprint(sum(du_lieu))'), '<pre class="pdata">%s</pre>' % E(ds8)),
         ('Tính <b>tổng theo từng mục</b> (dict). Dùng dữ liệu bên dưới.', R(c8), '<pre class="pdata">%s</pre>' % E(ds8)),
         ('Tìm <b>mục chi nhiều nhất</b> và phần trăm của nó so với tổng.', R(c8 + '\ntop = max(tong, key=tong.get)\nprint(top, round(tong[top] * 100 / sum(tong.values()), 1), "%")'), '<pre class="pdata">%s</pre>' % E(ds8)),
         ('<b>Nghĩ ngược:</b> ngân sách tháng là 1 600 000 đồng. Hỏi: mục nào đã vượt <b>40%</b> ngân sách (640 000)? Còn lại bao nhiêu tiền? Viết test kiểm chứng.', R(c8 + '\nngan_sach = 1600000\nfor muc in tong:\n    if tong[muc] > ngan_sach * 40 // 100:\n        print("Vượt 40%:", muc)\nprint("Còn lại:", ngan_sach - sum(tong.values()))\nassert ngan_sach - sum(tong.values()) == 10000') + '<p>Chỉ “Ăn uống” (830 000) vượt 640 000; còn lại 10 000 đồng.</p>', '<pre class="pdata">%s</pre>' % E(ds8)),
         ('<b>Thử thách:</b> thêm hai khoản “Ăn uống −50000” (hoàn tiền) và một dòng có tên viết thường/thừa dấu cách “  ăn uống ”. Chương trình phải gộp đúng vào “Ăn uống” và in tổng. Phản biện: bạn đã tính hoàn tiền vào tổng chi như thế nào và vì sao?', R('du_lieu = [("Ăn uống", 450000), ("Ăn uống", 380000), ("Học tập", 300000),\n           ("Giải trí", 150000), ("Học tập", 220000), ("Giải trí", 90000),\n           ("Ăn uống", -50000), ("  ăn uống ", 20000)]\ntong = {}\nfor muc, so_tien in du_lieu:\n    khoa = muc.strip().lower()\n    tong[khoa] = tong.get(khoa, 0) + so_tien\nfor k in tong:\n    print(k, tong[k])\nprint("Tổng:", sum(tong.values()))') + '<p>Giả định đã chọn: hoàn tiền (số âm) <b>trừ</b> vào chi tiêu của mục đó – ghi rõ để người dùng biết. Phương án khác là tách riêng hoàn tiền; mỗi cách đều hợp lý nếu được ghi rõ.</p>', None)],
        'Python')
    return P
