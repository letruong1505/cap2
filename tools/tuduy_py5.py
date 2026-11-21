"""Python 12–18 – Chương 4: Bài 4.1 while, Bài 4.3 break/continue/lồng nhau, Tóm tắt chương 4."""
from tuduy_gen import *


def build():
    P = {}
    # ================================================= BÀI 4.1  WHILE
    w1 = 'dem = 1\nwhile dem <= 5:\n    print("Lần", dem)\n    dem += 1\nprint("Xong")'
    w2 = 'tong = 0\nso = 1\nwhile so <= 100:\n    tong += so\n    so += 1\nprint(tong)'
    w3 = 'tien = 1000\nnam = 0\nwhile tien < 5000:\n    tien = tien * 2\n    nam += 1\nprint(nam, tien)'
    w4 = 'tong = 0\nso = int(input())\nwhile so != 0:\n    tong += so\n    so = int(input())\nprint("Tổng:", tong)'
    w5 = 'n = 2847\nso_cs = 0\nwhile n > 0:\n    n //= 10\n    so_cs += 1\nprint(so_cs)'
    w6 = 'a = 48\nb = 18\nwhile b != 0:\n    du = a % b\n    a = b\n    b = du\nprint(a)'
    wloop = 'dem = 1\nlan = 0\nwhile dem <= 5 and lan < 6:\n    lan += 1\nprint("Đã lặp", lan, "lần mà dem vẫn bằng", dem)'
    w0 = 'dem = 10\nwhile dem <= 5:\n    print("không bao giờ in")\nprint("Vòng lặp chạy 0 lần")'
    rows1 = []; dem = 1
    while dem <= 5: rows1.append((dem, 'đúng', 'Lần %d' % dem, dem + 1)); dem += 1
    rows1.append((6, 'SAI', '(dừng)', '—'))
    rs = []; t = 0
    for s in range(1, 6): t += s; rs.append((s, t - s, t))
    gr = [(48, 18, 12)]; a, b = 48, 18
    while b: a, b = b, a % b; gr.append((a, b, a % b if b else 0))
    gcdrows = []; a, b = 48, 18
    while b != 0:
        du = a % b; gcdrows.append((a, b, du)); a, b = b, du

    F = [loop_fig('Vòng lặp while hoạt động thế nào', 'dem <= 5', ['Làm thân vòng lặp', '(thụt vào)'], cap='Máy kiểm tra điều kiện; đúng thì làm thân vòng lặp rồi quay lại kiểm tra; sai thì thoát ra chạy tiếp.'),
         trace_fig('Bảng theo dõi vòng lặp đếm 1 đến 5', ['Lần kiểm tra', 'dem lúc kiểm tra', 'Điều kiện dem <= 5', 'In ra', 'dem sau khi tăng'], [(i + 1,) + r for i, r in enumerate(rows1)], 'Vòng lặp chạy đúng 5 lần; ở lần kiểm tra thứ 6, dem = 6 làm điều kiện sai nên dừng.', hl=[5]),
         trace_fig('Cộng dồn 1 + 2 + 3 + 4 + 5', ['so', 'tong trước', 'tong sau'], rs, 'Biến <b>tong</b> giữ kết quả cộng dồn; mỗi vòng thêm số hiện tại vào.'),
         loop_fig('Chờ cho tới khi gặp số 0', 'so != 0', ['Cộng so vào tong', 'Nhập số tiếp theo'], 'in tổng', 'Dùng while khi không biết trước sẽ lặp bao nhiêu lần: lặp cho đến khi người dùng gõ 0.'),
         fc('Quên tăng biến đếm: vòng lặp không bao giờ dừng', [('rd', 'Thiếu dem += 1', ['dem luôn = 1', 'dem <= 5 luôn đúng'], 'Lặp mãi mãi', 'phải tắt chương trình'), ('gr', 'Có dem += 1', ['dem tăng 1 mỗi vòng', 'tới 6 thì sai'], 'Dừng sau 5 lần', 'đúng ý')], 'Mỗi vòng phải làm điều kiện “tiến gần” tới việc sai, nếu không chương trình chạy mãi.'),
         fc('Điều kiện sai ngay từ đầu', [('ye', 'dem = 10', ['while dem <= 5:'], '0 lần', 'thân vòng lặp không chạy lần nào'), ('gr', 'dem = 1', ['while dem <= 5:'], '5 lần', 'chạy bình thường')], 'while kiểm tra điều kiện <b>trước</b> khi làm: nếu sai ngay từ đầu thì thân vòng lặp không chạy lần nào.'),
         trace_fig('Tìm ước chung lớn nhất của 48 và 18', ['a', 'b', 'du = a % b'], gcdrows + [(6, 0, '—')], 'Lặp “thay a bằng b, b bằng số dư” cho đến khi b = 0; lúc đó a chính là ước chung lớn nhất (6).'),
         fg('Ba mẫu dùng while quen thuộc', ['Mẫu', 'Ví dụ', 'Dấu hiệu nhận ra'], [['Đếm', 'dem += 1', 'biết số lần lặp'], ['Cộng dồn', 'tong += so', 'cần kết quả tích lũy'], ['Chờ điều kiện', 'while so != 0:', 'không biết trước số lần']], [150, 250, 300], 'Gặp bài toán lặp, hỏi: đếm, cộng dồn hay chờ điều kiện?'),
         fc('while và for: chọn cái nào?', [('bl', 'for', ['for i in range(5):'], 'biết số lần', 'danh sách cho sẵn'), ('ye', 'while', ['while điều_kiện:'], 'chưa biết số lần', 'lặp đến khi hết điều kiện')], 'Biết trước số lần lặp thì dùng <code>for</code>; lặp đến khi một điều kiện thay đổi thì dùng <code>while</code>.'),
         ff(['Xác định|điều kiện lặp', 'Khởi tạo|biến', 'Viết thân|vòng lặp', 'Cập nhật|biến', 'Thử vòng|đầu và cuối'], 'Quy trình viết vòng lặp while'),
         fp(w1, [0, 1, 2, 3, 4], ['Gán <b>dem</b> = 1.', 'Kiểm tra <code>1 &lt;= 5</code>: đúng, vào vòng lặp.', 'In “Lần 1”.', 'Tăng dem lên 2.', 'Quay lại kiểm tra <code>2 &lt;= 5</code>...'], maxn=6),
         trace_fig('Đếm số chữ số của 2847', ['n', 'n sau khi n //= 10', 'so_cs'], [(2847, 284, 1), (284, 28, 2), (28, 2, 3), (2, 0, 4)], 'Mỗi lần chia nguyên cho 10 là bỏ một chữ số; đếm cho tới khi n về 0 được 4 chữ số.')]
    cmd = [['<code>while</code>', 'Từ khóa mở vòng lặp: lặp trong khi điều kiện còn đúng.', W('Viết hoa chữ <code>While</code>:', 'dem = 1\nWhile dem <= 3:\n    dem += 1', 'E')],
           ['<code>điều_kiện</code>', 'Biểu thức đúng/sai quyết định có lặp tiếp không.', W('Dùng biến chưa tạo:', 'while dem <= 3:\n    dem += 1', 'E')],
           ['<code>=</code> trong điều kiện', 'Điều kiện cần so sánh <code>==</code> hoặc <code>&lt;=</code>…, không phải gán.', W('Viết một dấu <code>=</code>:', 'dem = 1\nwhile dem = 3:\n    dem += 1', 'E')],
           ['dấu hai chấm <code>:</code>', 'Kết thúc dòng <code>while</code>, báo khối lệnh sắp bắt đầu.', W('Quên dấu hai chấm:', 'dem = 1\nwhile dem <= 3\n    dem += 1', 'E')],
           ['thân vòng lặp (thụt vào)', 'Các lệnh thụt 4 dấu cách thuộc về vòng lặp và lặp lại cùng nhau.', W('Không thụt dòng:', 'dem = 1\nwhile dem <= 3:\ndem += 1', 'E') + 'Nếu dòng <code>dem += 1</code> không thụt vào thì nó nằm ngoài vòng lặp, vòng lặp không bao giờ dừng.'],
           ['<code>dem += 1</code>', 'Cập nhật biến đếm để điều kiện cuối cùng sai và vòng lặp dừng.', W('Bỏ dòng này, vòng lặp không dừng (ở đây có rào bảo vệ để ví dụ tự dừng):', wloop, 'R')],
           ['biến khởi tạo trước vòng', 'Gán giá trị ban đầu cho biến đếm, biến tổng.', W('Quên khởi tạo <code>tong</code> trước khi cộng dồn:', 'so = 1\nwhile so <= 3:\n    tong += so\n    so += 1', 'E')],
           ['<code>!=</code> với <code>input()</code>', 'Lặp cho tới khi người dùng nhập đúng giá trị dừng (ví dụ 0).', W('Quên đổi sang số nên “0” (chữ) luôn khác số 0, vòng lặp sẽ không dừng; ở đây ta chỉ chạy thử 1 vòng:', 'x = "0"\nprint(x != 0)', 'R')]]
    P['c4b1'] = LS('Bài 4.1 · Vòng lặp while', 'Lặp lại một việc cho tới khi điều kiện không còn đúng.',
        ('Viết được vòng lặp while với biến đếm, cộng dồn và điều kiện dừng; theo dõi từng vòng bằng bảng; tránh vòng lặp vô hạn', 'Đã biết điều kiện đúng/sai và if (Chương 3)', 'Các chương trình đếm, cộng dồn, nhập đến khi gặp 0 và tìm ước chung lớn nhất'),
        ['Máy tính giỏi nhất ở việc <b>lặp lại</b> không biết mệt: lặp 1 triệu lần cũng nhanh như lặp 10 lần.', '<b>while</b> dùng khi chưa biết trước phải lặp bao nhiêu lần, chỉ biết “lặp đến khi điều kiện thay đổi”.', 'Hiểu while là nền để viết trò chơi, chương trình nhập dữ liệu, thuật toán tìm kiếm.', 'Biết cách tránh vòng lặp vô hạn là kỹ năng sống còn khi lập trình.'],
        ol(['Nói bằng lời: “lặp trong khi…” – đó chính là điều kiện.', '<b>Khởi tạo</b> biến dùng trong điều kiện trước vòng lặp.', 'Viết thân vòng lặp, <b>nhớ cập nhật biến</b> để điều kiện có ngày sai.', 'Kiểm tra bằng bảng theo dõi: vòng đầu, vòng cuối và lúc dừng.']),
        think(['<b>Phản biện:</b> điều kiện của em có thể đúng mãi không? Cái gì làm nó sai đi?', '<b>Nghĩ ngược:</b> biết kết quả cần đạt (ví dụ tổng ≥ 100), em viết điều kiện lặp là “khi chưa đạt”.', '<b>Thói quen tốt:</b> viết dòng cập nhật biến ngay sau khi viết dòng <code>while</code>, để khỏi quên.']),
        [A('Đếm từ 1 đến 5:', w1), A('Cộng dồn 1 đến 100:', w2), A('Gấp đôi số tiền cho tới khi đạt từ 5000 trở lên:', w3), A('Nhập số cho tới khi gặp 0:', w4, '5\n3\n8\n0\n'), A('Đếm chữ số của 2847:', w5), A('Ước chung lớn nhất của 48 và 18:', w6), A('Điều kiện sai ngay từ đầu:', w0)],
        'Phân tích từng phần của vòng lặp while. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', cmd, F,
        [err('Quên cập nhật biến trong vòng lặp', 'Điều kiện không bao giờ sai nên chương trình chạy mãi:' + R2(wloop), 'Mỗi vòng phải thay đổi ít nhất một biến trong điều kiện.'),
         err('Lệch một lần', R2('dem = 1\nwhile dem < 5:\n    print(dem)\n    dem += 1') + 'Muốn in đến 5 mà dùng <code>&lt;</code> nên thiếu số 5.', 'Muốn lấy cả 5 thì dùng <code>&lt;= 5</code>.'),
         err('Quên khởi tạo biến', 'Biến chưa có giá trị thì không dùng được:' + E2('while so <= 3:\n    so += 1'), 'Gán giá trị ban đầu trước <code>while</code>.'),
         err('Thụt dòng sai chỗ', 'Dòng cập nhật nằm ngoài vòng lặp nên chỉ chạy một lần sau khi vòng lặp xong.', 'Mọi lệnh cần lặp phải thụt thẳng hàng với nhau.'),
         err('Dùng while khi biết trước số lần', 'Dễ quên tăng biến đếm.', 'Biết trước số lần thì dùng <code>for ... in range(...)</code>.')],
        [eg('Ví dụ 1: số nhỏ nhất có tổng chữ số lớn hơn 10', R2('so = 1\nwhile True:\n    tong = 0\n    t = so\n    while t > 0:\n        tong += t % 10\n        t //= 10\n    if tong > 10:\n        break\n    so += 1\nprint(so)') + note('Vòng lặp trong và <code>break</code> sẽ học kỹ ở Bài 4.3; bây giờ em chỉ cần đọc để thấy while xử lý được bài toán “tìm cho đến khi gặp”.')),
         eg('Ví dụ 2: gấp đôi cho tới khi vượt 1000', R2('x = 1\nwhile x <= 1000:\n    x *= 2\nprint(x)')),
         eg('Ví dụ 3: đếm ngược', R2('n = 5\nwhile n > 0:\n    print(n)\n    n -= 1\nprint("Cất cánh!")'))],
        [('In các số từ 10 xuống 1 (giảm dần), mỗi số một dòng, rồi in “Hết”.', R2('n = 10\nwhile n >= 1:\n    print(n)\n    n -= 1\nprint("Hết")'), None),
         ('Tính tổng các số lẻ từ 1 đến 99 bằng while. Kiểm chứng: tổng n số lẻ đầu tiên bằng n × n.', R2('so = 1\ntong = 0\nwhile so <= 99:\n    tong += so\n    so += 2\nprint(tong, 50 * 50)') + '<p>Có 50 số lẻ từ 1 đến 99 nên tổng phải bằng 50 × 50 = 2500; hai số in ra khớp nhau.</p>', None),
         ('Bạn gửi 2.000.000 đồng, lãi 8% mỗi năm (lãi cộng vào gốc, làm tròn xuống đồng). Sau bao nhiêu năm số tiền đạt từ 10.000.000 đồng trở lên?', R2('tien = 2000000\nnam = 0\nwhile tien < 10000000:\n    tien = tien * 108 // 100\n    nam += 1\nprint(nam, tien)') + note('Không biết trước số năm nên dùng while.'), None),
         ('Nhập các số cho tới khi gặp 0. Sau đó in tổng, số lượng số đã nhập (không tính số 0) và trung bình cộng.', A('', 'tong = 0\nsl = 0\nso = int(input())\nwhile so != 0:\n    tong += so\n    sl += 1\n    so = int(input())\nprint("Tổng:", tong)\nprint("Số lượng:", sl)\nprint("Trung bình:", tong / sl)', '4\n6\n8\n0\n') + note('Nếu người dùng gõ 0 ngay lần đầu thì <code>sl</code> bằng 0 và phép chia gây lỗi: sẽ xử lý bằng if ở bài sau.'), None),
         ('<b>Thử thách (nghĩ ngược):</b> (a) Tìm ước chung lớn nhất của 84 và 36 bằng vòng lặp, rồi kiểm chứng ngược: kết quả phải chia hết cả hai số. (b) Chia 64 cho 2 liên tiếp cho đến khi ra 1: mất mấy lần?', R2('a = 84\nb = 36\nwhile b != 0:\n    a, b = b, a % b\nprint(a)\nprint(84 % a == 0 and 36 % a == 0)\nn = 64\nlan = 0\nwhile n > 1:\n    n //= 2\n    lan += 1\nprint(lan)') + '<p>(a) Ước chung lớn nhất là 12, cả 84 và 36 đều chia hết cho 12. (b) 64 = 2 mũ 6 nên chia 6 lần. Dòng <code>a, b = b, a % b</code> gán cùng lúc hai biến, gọn hơn cách dùng biến tạm <code>du</code> ở phần trên.</p>', None)])

    # ================================================= BÀI 4.3  BREAK / CONTINUE / LỒNG NHAU
    b1 = 'while True:\n    s = input()\n    if s == "thoat":\n        break\n    print("Bạn gõ:", s)\nprint("Tạm biệt")'
    b1in = 'xin chao\nhoc python\nthoat\n'
    b2 = 'for n in (29, 21):\n    la_nt = True\n    for i in range(2, n):\n        if n % i == 0:\n            la_nt = False\n            break\n    print(n, la_nt)'
    b3 = 'for i in range(1, 11):\n    if i % 3 == 0:\n        continue\n    print(i, end=" ")\nprint()'
    b4 = 'for i in range(1, 4):\n    for j in range(1, 4):\n        print(i * j, end=" ")\n    print()'
    b5 = 'for i in range(1, 5):\n    for j in range(i):\n        print("*", end="")\n    print()'
    b6 = 'for i in range(1, 4):\n    for j in range(1, 4):\n        if j == 2:\n            break\n        print(i, j)'
    b7 = 'for i in range(1, 11):\n    if i == 5:\n        break\n    print(i, end=" ")\nprint()'
    F = [loop_fig('break: thoát khỏi vòng lặp ngay lập tức', 'điều kiện lặp', ['Gặp break → thoát hẳn', 'khỏi vòng lặp'], 'câu lệnh sau vòng lặp', 'Gặp <code>break</code>, máy bỏ phần còn lại của vòng và nhảy ra chạy lệnh sau vòng lặp.'),
         fc('break và continue khác nhau thế nào', [('rd', 'break', ['gặp i == 5'], '1 2 3 4', 'dừng hẳn vòng lặp'), ('bl', 'continue', ['gặp i % 3 == 0'], '1 2 4 5 7 8 10', 'bỏ qua lượt này, vẫn lặp tiếp')], 'break thoát cả vòng lặp; continue chỉ bỏ qua phần còn lại của lượt hiện tại rồi sang lượt kế.'),
         fg('Bảng nhân 3 × 3 do hai vòng lặp lồng nhau tạo ra', ['i \\ j', 'j = 1', 'j = 2', 'j = 3'], [['i = 1', '1', '2', '3'], ['i = 2', '2', '4', '6'], ['i = 3', '3', '6', '9']], [120, 160, 160, 160], 'Vòng ngoài chọn hàng (i), vòng trong chạy hết các cột (j) rồi mới sang hàng kế.'),
         trace_fig('Thứ tự chạy của hai vòng for lồng nhau', ['i (ngoài)', 'j (trong)', 'In ra'], [(1, 1, 1), (1, 2, 2), (1, 3, 3), ('xuống dòng', '', ''), (2, 1, 2), (2, 2, 4)], 'Mỗi lần i đổi, vòng trong chạy lại từ đầu; tổng số lần = số lượt ngoài × số lượt trong.'),
         fc('break trong vòng lồng chỉ thoát vòng trong', [('rd', 'Khi j == 2', ['break ở vòng trong'], 'vòng ngoài vẫn chạy', 'chỉ thoát vòng đang đứng'), ('gr', 'Kết quả', ['(1,1) (2,1) (3,1)'], '3 cặp', 'mỗi i một cặp')], 'break luôn chỉ tác dụng lên vòng lặp gần nó nhất (vòng trong cùng chứa nó).'),
         fc('end=" " giữ nguyên dòng', [('rd', 'Mặc định', ['print(i)'], 'mỗi số một dòng', 'tự xuống dòng'), ('gr', 'Có end=" "', ['print(i, end=" ")'], '1 2 3 4 5', 'in cùng một dòng')], 'Tham số <code>end</code> quyết định ký tự in sau cùng; mặc định là xuống dòng, đổi thành dấu cách để in liền nhau.'),
         fg('Tam giác sao do vòng lặp lồng nhau vẽ', ['Hàng i', 'Số dấu *', 'Kết quả'], [['1', '1', '*'], ['2', '2', '**'], ['3', '3', '***'], ['4', '4', '****']], [120, 160, 260], 'Vòng ngoài là số hàng; vòng trong in i dấu *, cuối mỗi hàng dùng <code>print()</code> để xuống dòng.'),
         trace_fig('Kiểm tra 21 có phải số nguyên tố không', ['i', '21 % i', 'kết luận'], [(2, 1, 'chưa'), (3, 0, 'chia hết → dừng')], 'Gặp ước đầu tiên là có thể dừng bằng break, khỏi phải thử tiếp các số còn lại.', hl=[1]),
         fg('Chọn công cụ nào?', ['Tình huống', 'Dùng', 'Ví dụ'], [['Tìm thấy rồi, không cần lặp tiếp', 'break', 'tìm ước đầu tiên'], ['Bỏ qua một giá trị nhưng lặp tiếp', 'continue', 'bỏ qua bội của 3'], ['Việc có 2 chiều (hàng, cột)', 'vòng lặp lồng', 'bảng nhân, hình vẽ']], [270, 150, 260], 'Hỏi: “Mình muốn dừng, bỏ qua hay lặp hai tầng?”'),
         ff(['Xác định|lặp mấy tầng', 'Viết vòng|ngoài', 'Viết vòng|trong', 'Thêm break,|continue', 'Thử bảng|nhỏ trước'], 'Quy trình xử lý vòng lặp phức tạp'),
         fp(b3, [0, 1, 2, 3, 4], ['Vào vòng lặp với <b>i = 1</b>.', 'Kiểm tra <code>1 % 3 == 0</code>: sai.', 'In “1 ” cùng dòng (end=" ").', 'Sang <b>i = 2</b>, kiểm tra tiếp.', 'In “2 ”...'], maxn=8),
         fc('Thứ tự hai tầng: ngoài chậm, trong nhanh', [('bl', 'Vòng ngoài', ['for i in range(1, 4):'], 'đổi 3 lần', 'như kim giờ'), ('ye', 'Vòng trong', ['for j in range(1, 4):'], 'đổi 9 lần', 'như kim phút')], 'Giống kim giờ và kim phút: kim phút (vòng trong) quay hết một vòng thì kim giờ (vòng ngoài) mới nhích một nấc.')]
    cmd = [['<code>break</code>', 'Thoát hẳn khỏi vòng lặp gần nhất.', W('Dùng ngoài vòng lặp:', 'break', 'E')],
           ['<code>continue</code>', 'Bỏ phần còn lại của lượt này, sang lượt kế.', W('Dùng ngoài vòng lặp:', 'continue', 'E')],
           ['<code>while True:</code>', 'Vòng lặp vô hạn có chủ ý; phải có <code>break</code> bên trong để dừng.', 'Không có <code>break</code> thì chương trình không bao giờ dừng, nên luôn viết lối thoát trước.'],
           ['vòng <code>for</code> lồng nhau', 'Vòng trong nằm trong thân vòng ngoài, thụt thêm một cấp.', W('Quên thụt vòng trong:', 'for i in range(2):\nfor j in range(2):\n    print(i, j)', 'E')],
           ['<code>end=" "</code>', 'Thay cách kết thúc dòng của print bằng dấu cách (hoặc chữ khác).', W('Quên <code>end</code> thì mỗi số một dòng:', 'for i in range(1, 4):\n    print(i)', 'R')],
           ['<code>print()</code> sau vòng trong', 'In một dòng trống để xuống dòng giữa các hàng.', W('Quên dòng này thì cả bảng dính thành một hàng:', 'for i in range(1, 4):\n    for j in range(1, 4):\n        print(i * j, end=" ")', 'R')],
           ['<code>range(1, 4)</code>', 'Dãy 1, 2, 3 (dừng <b>trước</b> 4).', W('Muốn tới 3 mà viết <code>range(1, 3)</code> thì thiếu số 3:', 'for j in range(1, 3):\n    print(j)', 'R')],
           ['biến cờ (<code>la_nt</code>)', 'Biến đúng/sai ghi nhớ “đã gặp điều kiện chưa” để dùng sau vòng lặp.', W('Quên đặt lại cờ <code>True</code> cho mỗi số mới thì kết quả cũ dính sang số sau:', 'la_nt = True\nfor n in (21, 29):\n    for i in range(2, n):\n        if n % i == 0:\n            la_nt = False\n            break\n    print(n, la_nt)', 'R')]]
    P['c4b3'] = LS('Bài 4.3 · break, continue và vòng lặp lồng nhau', 'Dừng sớm, bỏ qua một lượt và lặp hai tầng.',
        ('Dùng break và continue đúng chỗ; viết vòng lặp lồng nhau để in bảng và hình; đọc thứ tự chạy của hai tầng vòng lặp', 'Đã biết for và while (Bài 4.1, 4.2)', 'Chương trình kiểm tra số nguyên tố, in bảng nhân và tam giác sao'),
        ['<b>break</b> cho phép dừng ngay khi đã tìm thấy điều cần tìm, tiết kiệm rất nhiều lần lặp thừa.', '<b>continue</b> giúp bỏ qua trường hợp không quan tâm mà không cần viết thêm khối if lồng sâu.', 'Vòng lặp lồng nhau là cách xử lý dữ liệu hai chiều: bảng, ma trận, ảnh, bàn cờ.', 'Hiểu thứ tự chạy hai tầng là nền để đọc các chương trình phức tạp hơn.'],
        ol(['Xác định việc có <b>một chiều</b> (một vòng) hay <b>hai chiều</b> (hai vòng lồng nhau).', 'Với tìm kiếm: thêm điều kiện và <code>break</code> khi tìm thấy; với lọc: thêm điều kiện và <code>continue</code> cho phần bỏ qua.', 'Vẽ bảng theo dõi nhỏ (2 – 3 hàng) để kiểm tra thứ tự chạy trước khi chạy lớn.', 'Nhớ: <code>break</code> chỉ thoát vòng trong cùng chứa nó.']),
        think(['<b>Phản biện:</b> “Em có cần lặp hết không, hay tìm thấy là dừng được?” – câu hỏi này tạo ra các chương trình nhanh.', '<b>Nghĩ ngược:</b> muốn in hình tam giác 4 hàng, nhìn kết quả để rút ra quy luật: hàng i có i dấu *.', '<b>Thói quen tốt:</b> thử vòng lồng với kích thước nhỏ (3 × 3) trước khi đổi sang 100 × 100.']),
        [A('Dừng khi người dùng gõ “thoat”:', b1, b1in), A('Kiểm tra số nguyên tố bằng break:', b2), A('Bỏ qua bội của 3 bằng continue:', b3), A('Dừng ngay khi gặp số 5:', b7), A('Bảng nhân 3 × 3 bằng hai vòng lồng nhau:', b4), A('Tam giác sao:', b5), A('break chỉ thoát vòng trong:', b6)],
        'Phân tích từng phần. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', cmd, F,
        [err('Dùng break khi chỉ muốn bỏ qua một lượt', 'Vòng lặp dừng hẳn thay vì chỉ bỏ qua giá trị đó:' + R2(b7), 'Chỉ muốn bỏ qua một lượt thì dùng <code>continue</code>.'),
         err('Quên đặt lại biến cờ cho mỗi lượt', 'Kết quả của số trước dính sang số sau.', 'Đặt <code>la_nt = True</code> ngay đầu thân vòng ngoài.'),
         err('Nhầm break thoát cả hai vòng', R2(b6) + 'Vòng ngoài vẫn chạy đủ 3 lượt dù mỗi lượt vòng trong bị cắt.', 'Muốn thoát cả hai tầng, dùng biến cờ hoặc đưa vào hàm và <code>return</code> (Chương 6).'),
         err('Quên print() cuối mỗi hàng', 'Cả bảng dính thành một hàng dài.', 'Thêm <code>print()</code> thụt cùng cấp với vòng trong.'),
         err('Lặp thừa nhiều lần do không dùng break', 'Kiểm tra số 1.000.003 mà không dừng ở ước đầu tiên thì mất hàng triệu lần thử.', 'Khi đã tìm thấy kết quả thì dừng.')],
        [eg('Ví dụ 1: số nguyên tố từ 2 đến 30', R2('for n in range(2, 31):\n    la_nt = True\n    for i in range(2, n):\n        if n % i == 0:\n            la_nt = False\n            break\n    if la_nt:\n        print(n, end=" ")\nprint()')),
         eg('Ví dụ 2: in các số không chia hết cho 2 và 3', R2('for i in range(1, 21):\n    if i % 2 == 0 or i % 3 == 0:\n        continue\n    print(i, end=" ")\nprint()')),
         eg('Ví dụ 3: bàn cờ 4 × 4 xen kẽ', R2('for i in range(4):\n    for j in range(4):\n        if (i + j) % 2 == 0:\n            print("#", end="")\n        else:\n            print(".", end="")\n    print()'))],
        [('In các số từ 1 đến 10 nhưng bỏ qua số 5 (dùng continue).', R2('for i in range(1, 11):\n    if i == 5:\n        continue\n    print(i, end=" ")\nprint()'), None),
         ('Tìm số đầu tiên lớn hơn 100 mà chia hết cho cả 7 và 5 (dùng while hoặc for với break).', R2('for n in range(101, 1000):\n    if n % 7 == 0 and n % 5 == 0:\n        print(n)\n        break') + '<p>Bội chung nhỏ nhất của 7 và 5 là 35; bội đầu tiên trên 100 là 105.</p>', None),
         ('In bảng nhân dạng lưới 5 hàng 5 cột (hàng i, cột j in tích i × j), các số cách nhau một dấu cách.', R2('for i in range(1, 6):\n    for j in range(1, 6):\n        print(i * j, end=" ")\n    print()'), None),
         ('In các số nguyên tố từ 2 đến 50 và đếm có bao nhiêu số.', R2('dem = 0\nfor n in range(2, 51):\n    la_nt = True\n    for i in range(2, n):\n        if n % i == 0:\n            la_nt = False\n            break\n    if la_nt:\n        print(n, end=" ")\n        dem += 1\nprint()\nprint("Có", dem, "số")') + '<p>Dưới 50 có 15 số nguyên tố (đối chiếu với bảng số nguyên tố quen thuộc).</p>', None),
         ('<b>Thử thách (nghĩ ngược):</b> In hình sau bằng vòng lặp lồng nhau (hàng i in các số 1 đến i), rồi kiểm chứng tổng số chữ số đã in là 1 + 2 + 3 + 4 = 10:' + code('1\n12\n123\n1234'), R2('dem = 0\nfor i in range(1, 5):\n    for j in range(1, i + 1):\n        print(j, end="")\n        dem += 1\n    print()\nprint(dem, dem == 1 + 2 + 3 + 4)') + '<p>Hàng i in các số từ 1 đến i nên vòng trong là <code>range(1, i + 1)</code>; biến <code>dem</code> đếm số lần in để kiểm chứng ngược.</p>', None)])

    # ================================================= TÓM TẮT CHƯƠNG 4
    proj = 'bi_mat = 37\nlan = 0\nwhile True:\n    doan = int(input("Đoán số: "))\n    lan += 1\n    if doan < bi_mat:\n        print("Cao hơn!")\n    elif doan > bi_mat:\n        print("Thấp hơn!")\n    else:\n        break\nprint(f"Đúng rồi! Em đoán trong {lan} lần.")'
    P['c4t'] = SUM(4, 'Cấu trúc lặp',
        [('while (Bài 4.1)', 'lặp khi điều kiện đúng'), ('for (Bài 4.2)', 'lặp qua dãy, range'), ('break – continue (4.3)', 'dừng, bỏ qua'), ('Lồng nhau & gỡ lỗi', 'bảng, hình, test')],
        ['Chạy một mạch từ trên xuống', 'Làm việc lặp bằng cách gõ lại', 'Sợ vòng lặp chạy mãi'], ['Viết while và for đúng điều kiện', 'Dừng sớm bằng break', 'In bảng bằng hai vòng lặp'],
        ['Viết vòng lặp while', 'Viết vòng lặp for với range', 'Dùng break và continue', 'Viết vòng lặp lồng nhau', 'Theo dõi bằng bảng', 'Tránh vòng lặp vô hạn'],
        [['<code>while</code>', '<code>while dem &lt;= 5:</code>', 'Lặp khi điều kiện còn đúng'], ['<code>for … in range</code>', '<code>for i in range(1, 6):</code>', 'Biết trước số lần; dừng trước số cuối'], ['<code>break</code>', 'tìm thấy thì dừng', 'Thoát vòng lặp gần nhất'], ['<code>continue</code>', 'bỏ qua bội của 3', 'Sang lượt kế'], ['vòng lồng nhau', 'bảng nhân', 'Ngoài chậm, trong nhanh'], ['biến đếm, tổng', '<code>tong += so</code>', 'Giữ kết quả tích lũy'], ['<code>end=" "</code>', '<code>print(i, end=" ")</code>', 'Giữ nguyên dòng']],
        [('Quên cập nhật biến trong while', 'Vòng lặp chạy mãi.', 'Mỗi vòng phải tiến gần đến điều kiện dừng.'), ('Lệch một lần với range', '<code>range(1, 5)</code> không có 5.', 'Số cuối phải cộng thêm 1.'), ('Dùng break khi chỉ cần continue', 'Vòng lặp dừng hẳn.', 'Bỏ qua một lượt thì dùng continue.'), ('Không đặt lại biến cờ mỗi lượt', 'Kết quả cũ dính sang lượt sau.', 'Đặt lại ở đầu thân vòng ngoài.'), ('Quên thụt dòng', 'Dòng nằm ngoài vòng lặp.', 'Thụt thẳng hàng với các lệnh cùng vòng.')],
        [('Khi nào dùng while, khi nào dùng for?', 'For khi biết trước số lần hoặc duyệt một dãy; while khi chỉ biết điều kiện dừng.'), ('<code>range(2, 6)</code> gồm những số nào?', '2, 3, 4, 5 (dừng trước 6).'), ('Khác nhau giữa break và continue?', 'break thoát hẳn vòng lặp; continue bỏ qua phần còn lại của lượt hiện tại rồi lặp tiếp.'), ('Vòng for lồng nhau 3 × 4 chạy thân vòng trong bao nhiêu lần?', '12 lần (3 lượt ngoài × 4 lượt trong).'), ('Làm sao in nhiều số trên cùng một dòng?', 'Dùng <code>print(x, end=" ")</code> và <code>print()</code> để xuống dòng khi kết thúc.'), ('Làm sao tránh vòng lặp vô hạn?', 'Bảo đảm trong thân vòng có lệnh làm điều kiện dần sai (hoặc có break).')],
        'Trò chơi đoán số', 'Máy giữ một số bí mật là 37. Chương trình cho phép nhập số đoán nhiều lần, mỗi lần báo “Cao hơn!” hoặc “Thấp hơn!”, đúng thì dừng và báo số lần đoán. Dùng đủ: <code>while</code>, <code>input</code>, <code>if</code>–<code>elif</code>–<code>else</code>, <code>break</code>, biến đếm, f-string.',
        proj, ['50\n25\n37\n', '37\n'], 'Chiến lược đoán “chia đôi” (đoán 50, rồi 25, rồi 37) đoán được số bất kỳ từ 1 đến 100 trong tối đa 7 lần; em hãy thử đổi số bí mật và tự đo.',
        ['<b>Chương 5 – Cấu trúc dữ liệu:</b> gom nhiều giá trị vào danh sách, tuple, tập hợp và từ điển để lưu và tra cứu dữ liệu.', 'Em đã biết cho máy <b>lặp lại</b>; sang chương 5 em sẽ cho máy <b>ghi nhớ nhiều thứ cùng lúc</b>.'],
        ['<b>Cập nhật biến</b> trong mỗi vòng để vòng lặp có ngày kết thúc.', '<b>Dừng sớm</b> khi đã tìm thấy, bỏ qua những lượt không cần.', '<b>Thử với bảng nhỏ</b> (3 × 3) trước khi chạy lớn.'])
    return P
