"""Python 12–18 – Chương 5: Bài 5.2 Tuple và set, Bài 5.3 Từ điển, Bài 5.4 Duyệt – tìm kiếm – sắp xếp, Tóm tắt chương 5."""
from tuduy_gen import *


def venn(title, cap):
    s = ARR + txt(350, 24, title, '#17406b', 17, bold=True)
    ops = [('A | B', 'hợp: có ở A hoặc B', 'u'), ('A & B', 'giao: có ở cả hai', 'i'), ('A - B', 'hiệu: chỉ có ở A', 'd'), ('A ^ B', 'chỉ ở một bên', 'x')]
    for k, (op, desc, kind) in enumerate(ops):
        cx = 100 + k * 165; cy = 100; r = 42; ax = cx - 22; bx = cx + 22
        s += '<defs><clipPath id="cb%d"><circle cx="%d" cy="%d" r="%d"/></clipPath><clipPath id="ca%d"><circle cx="%d" cy="%d" r="%d"/></clipPath></defs>' % (k, bx, cy, r, k, ax, cy, r)
        g = '#2a8a4a'
        if kind == 'u': s += '<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".45"/><circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".45"/>' % (ax, cy, r, g, bx, cy, r, g)
        elif kind == 'i': s += '<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".55" clip-path="url(#cb%d)"/>' % (ax, cy, r, g, k)
        elif kind == 'd': s += '<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".45"/><circle cx="%d" cy="%d" r="%d" fill="#fff"/>' % (ax, cy, r, g, bx, cy, r)
        else: s += '<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".45"/><circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".45"/><circle cx="%d" cy="%d" r="%d" fill="#fff" clip-path="url(#cb%d)"/>' % (ax, cy, r, g, bx, cy, r, g, ax, cy, r, k)
        s += '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#1f6fb2" stroke-width="2.5"/><circle cx="%d" cy="%d" r="%d" fill="none" stroke="#d9822b" stroke-width="2.5"/>' % (ax, cy, r, bx, cy, r)
        s += txt(ax - 14, cy - 50, 'A', '#1f6fb2', 14, bold=True) + txt(bx + 14, cy - 50, 'B', '#d9822b', 14, bold=True) + mono(cx, cy + 82, op, '#17406b', 18, 'middle', True) + txt(cx, cy + 104, desc, '#5b6773', 12)
    return fig(svg(700, 224, s, title), cap)


def build():
    P = {}
    # ====================================================== BÀI 5.2  TUPLE VÀ SET
    t1 = 'toa_do = (3, 5)\nprint(toa_do)\nprint(toa_do[0])\nprint(len(toa_do))\nx, y = toa_do\nprint(x, y)'
    t3 = 'a = (5)\nb = (5,)\nprint(type(a))\nprint(type(b))'
    t4 = 'a = 3\nb = 8\na, b = b, a\nprint(a, b)'
    t5 = 'lop = {"Lan", "Minh", "Lan", "Hà", "Minh"}\nprint(len(lop))\nprint(sorted(lop))'
    t6 = 'a = {1, 2, 3, 4}\nb = {3, 4, 5}\nprint(sorted(a | b))\nprint(sorted(a & b))\nprint(sorted(a - b))\nprint(sorted(a ^ b))'
    t7 = 'ds = [3, 1, 3, 2, 1, 3]\nso_khac = set(ds)\nprint(len(so_khac), sorted(so_khac))'
    t8 = 'hs = {"Lan"}\nhs.add("Minh")\nhs.add("Lan")\nhs.discard("Nam")\nprint(sorted(hs))'
    t9 = 'a = {}\nb = set()\nprint(type(a))\nprint(type(b))'
    cells = ARR + txt(350, 24, 'Tuple (3, 5): dãy giá trị có thứ tự và không đổi được', '#17406b', 17, bold=True)
    for i, v in enumerate(['3', '5']): cells += box(250 + i * 100, 50, 90, 56, '#e6f1fb', '#1f6fb2', [v], 24, bold=True) + txt(295 + i * 100, 130, 'toa_do[%d]' % i, '#2a8a4a', 14, bold=True)
    cells += txt(350, 170, 'Chỉ đọc được, không gán lại từng phần tử.', '#5b6773', 14)
    F = [fig(svg(700, 186, cells, 'Tuple'), 'Tuple viết bằng cặp ngoặc tròn, các phần tử có chỉ số 0, 1, … như danh sách, nhưng không sửa được.'),
         fg('Ba kiểu dữ liệu nhiều phần tử', ['Kiểu', 'Cách viết', 'Có thứ tự?', 'Sửa được?', 'Trùng nhau?'], [['list', '[1, 2, 3]', 'có', 'có', 'cho phép'], ['tuple', '(1, 2, 3)', 'có', 'không', 'cho phép'], ['set', '{1, 2, 3}', 'không', 'có', 'tự loại trùng']], [120, 150, 130, 130, 140], 'Chọn kiểu theo nhu cầu: cần sửa → list; cần cố định → tuple; cần loại trùng, kiểm tra thuộc → set.'),
         fc('Tuple không sửa được từng phần tử', [('rd', 'Gán lại phần tử', ['toa_do[0] = 9'], 'TypeError', 'tuple là bất biến'), ('gr', 'Tạo tuple mới', ['toa_do = (9, 5)'], '(9, 5)', 'thay cả tuple')], 'Muốn đổi, em tạo tuple mới và gán lại cho biến.'),
         fig(svg(700, 190, ARR + txt(350, 24, 'Giải nén tuple: x, y = toa_do', '#17406b', 17, bold=True) + box(30, 60, 180, 60, '#e6f1fb', '#1f6fb2', ['toa_do = (3, 5)'], 17, bold=True) + arr(212, 80, 300, 62) + arr(212, 100, 300, 128) + box(302, 40, 150, 46, '#e5f5ea', '#2a8a4a', ['x = 3'], 18, bold=True) + box(302, 108, 150, 46, '#fff4d6', '#d9822b', ['y = 5'], 18, bold=True) + txt(560, 100, 'số biến = số phần tử', '#5b6773', 14), 'Giải nén tuple'), 'Gán một tuple cho nhiều biến cùng lúc: phần tử thứ nhất vào biến thứ nhất, …'),
         fc('Hoán đổi hai biến chỉ bằng một dòng', [('ye', 'Trước', ['a = 3', 'b = 8'], 'a=3, b=8', ''), ('gr', 'Sau a, b = b, a', ['a, b = b, a'], 'a=8, b=3', 'vế phải tạo tuple rồi giải nén')], 'Python tính vế phải (b, a) = (8, 3) rồi mới gán, nên không cần biến tạm.'),
         fc('Single element: dấu phẩy mới tạo tuple', [('rd', '(5)', ['a = (5)'], '<class int>', 'chỉ là số 5 trong ngoặc'), ('gr', '(5,)', ['b = (5,)'], '<class tuple>', 'dấu phẩy tạo tuple')], 'Tuple một phần tử cần dấu phẩy ở cuối; ngoặc chỉ để gom nhóm.'),
         fc('Set tự loại bỏ phần tử trùng', [('bl', 'Danh sách có trùng', ['Lan Minh Lan', 'Hà Minh'], '5 phần tử', ''), ('gr', 'Sau khi chuyển set', ['{"Lan","Minh","Hà"}'], '3 phần tử', 'mỗi giá trị chỉ một lần')], 'Dùng <code>set(danh_sách)</code> để đếm số giá trị khác nhau rất gọn.'),
         venn('Bốn phép toán trên tập hợp (A = {1,2,3,4}, B = {3,4,5})', 'Phần tô xanh là kết quả: hợp, giao, hiệu và phần ở đúng một bên.'),
         fg('Kết quả bốn phép trên A và B', ['Phép', 'Ý nghĩa', 'Kết quả'], [['A | B', 'hợp', '{1, 2, 3, 4, 5}'], ['A & B', 'giao', '{3, 4}'], ['A - B', 'hiệu', '{1, 2}'], ['A ^ B', 'ở đúng một bên', '{1, 2, 5}']], [150, 250, 300], 'Kiểm chứng: số phần tử A + B = hợp + giao (4 + 3 = 5 + 2).'),
         fc('Set rỗng phải viết set()', [('rd', '{}', ['a = {}'], '<class dict>', 'cặp ngoặc nhọn rỗng là từ điển'), ('gr', 'set()', ['b = set()'], '<class set>', 'mới là tập hợp rỗng')], 'Cặp ngoặc nhọn rỗng được dành cho từ điển nên tập hợp rỗng phải viết <code>set()</code>.'),
         ff(['Cần sửa|thường xuyên?', 'Có thứ tự|quan trọng?', 'Cần loại trùng|hoặc kiểm tra in?', 'Chọn list,|tuple hay set', 'Thử với|dữ liệu nhỏ'], 'Chọn kiểu dữ liệu'),
         fp(t4, [0, 1, 2, 3], ['Gán <b>a</b> = 3.', 'Gán <b>b</b> = 8.', 'Vế phải (b, a) = (8, 3) rồi giải nén: a = 8, b = 3.', 'In 8 3.'], maxn=6)]
    cmd = [['<code>( )</code> của tuple', 'Gom các giá trị thành một nhóm không sửa được.', W('Sửa một phần tử:', 'toa_do = (3, 5)\ntoa_do[0] = 9', 'E')],
           ['dấu phẩy trong tuple một phần tử', 'Dấu phẩy mới tạo tuple, ngoặc chỉ để gom nhóm.', W('Quên dấu phẩy:', t3, 'R')],
           ['<code>x, y = toa_do</code>', 'Giải nén: số biến bên trái phải bằng số phần tử.', W('Số biến không khớp:', 'x, y, z = (3, 5)', 'E')],
           ['<code>{ }</code> của set', 'Tập hợp: không có thứ tự, tự loại trùng.', W('Truy cập bằng chỉ số:', 's = {1, 2}\nprint(s[0])', 'E')],
           ['<code>set()</code>', 'Tạo tập hợp rỗng hoặc chuyển danh sách thành tập hợp.', W('Dùng <code>{}</code> để tạo tập rỗng:', t9, 'R')],
           ['<code>.add(x)</code>', 'Thêm một phần tử (thêm trùng thì không đổi).', W('Thêm vào tuple không được:', 't = (1, 2)\nt.add(3)', 'E')],
           ['<code>.discard(x)</code> và <code>.remove(x)</code>', '<code>discard</code> bỏ nếu có, <code>remove</code> bắt buộc phải có.', W('<code>remove</code> phần tử không có:', 's = {1, 2}\ns.remove(9)', 'E') + W('<code>discard</code> thì im lặng:', 's = {1, 2}\ns.discard(9)\nprint(sorted(s))', 'R')],
           ['<code>|  &amp;  -  ^</code>', 'Hợp, giao, hiệu và phần ở đúng một bên.', W('Dùng <code>+</code> cho hai tập hợp:', 'print({1, 2} + {3})', 'E')],
           ['<code>x in tập</code>', 'Kiểm tra x có thuộc tập hợp, rất nhanh.', W('Thử kiểm tra:', 'print(3 in {1, 2, 3})\nprint(9 in {1, 2, 3})', 'R')]]
    P['c5b2'] = LS('Bài 5.2 · Tuple và set', 'Hai kiểu dữ liệu gom nhiều giá trị: một cái cố định, một cái tự loại trùng.',
        ('Dùng được tuple (bất biến, giải nén) và set (loại trùng, hợp – giao – hiệu); phân biệt list, tuple, set', 'Đã biết list (Bài 5.1) và vòng lặp', 'Chương trình hoán đổi, đếm giá trị khác nhau và so sánh hai nhóm học sinh'),
        ['Có dữ liệu nên <b>cố định</b> (tọa độ, ngày tháng): dùng tuple để khỏi sửa nhầm.', 'Set giúp loại trùng và trả lời “có hay không” rất nhanh, tránh phải duyệt cả danh sách.', 'Các phép hợp – giao – hiệu giải gọn bài toán so sánh hai nhóm: ai ở cả hai lớp, ai chỉ ở một lớp.', 'Biết chọn đúng kiểu dữ liệu giúp chương trình ngắn và ít lỗi hơn.'],
        ol(['Hỏi: dữ liệu có <b>cần sửa</b> không? Có <b>trùng</b> không? Thứ tự có quan trọng không?', 'Cố định và có thứ tự → tuple; cần loại trùng, kiểm tra thuộc → set; còn lại → list.', 'Dùng giải nén để lấy các phần tử gọn; dùng phép tập hợp để so sánh nhóm.', 'Nhớ: set không có chỉ số; muốn in có thứ tự thì dùng <code>sorted(...)</code>.']),
        think(['<b>Phản biện:</b> em đang cần sửa dữ liệu hay chỉ đọc? Chọn nhầm sẽ phải đổi cả chương trình.', '<b>Nghĩ ngược:</b> muốn biết lớp A có bao nhiêu bạn không học lớp B, nên dùng phép nào trên hai tập hợp?', '<b>Thói quen tốt:</b> kiểm chứng bằng công thức: |A| + |B| = |A ∪ B| + |A ∩ B|.']),
        [A('Tuple và giải nén:', t1), A('Hoán đổi hai biến:', t4), A('Tuple một phần tử cần dấu phẩy:', t3), A('Set loại trùng:', t5), A('Hợp, giao, hiệu:', t6), A('Đếm giá trị khác nhau trong danh sách:', t7), A('Thêm, bỏ phần tử của set:', t8)],
        'Phân tích từng phần. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', cmd, F,
        [err('Cố sửa phần tử của tuple', 'Tuple không cho gán lại từng phần tử:' + E2('t = (1, 2)\nt[0] = 9'), 'Chuyển sang list nếu cần sửa, hoặc tạo tuple mới.'),
         err('Tạo set rỗng bằng {}', R2(t9), 'Dùng <code>set()</code>.'),
         err('Truy cập set bằng chỉ số', 'Set không có thứ tự nên không có <code>s[0]</code>:' + E2('s = {1, 2}\nprint(s[0])'), 'Chuyển sang list đã sắp xếp: <code>sorted(s)[0]</code>.'),
         err('Quên dấu phẩy khi tuple có một phần tử', R2(t3), 'Viết <code>(5,)</code>.'),
         err('Mong set giữ thứ tự khi thêm', 'In trực tiếp set có thể ra thứ tự khác lúc em nghĩ.', 'Cần thứ tự thì dùng <code>sorted()</code> hoặc list.')],
        [eg('Ví dụ 1: hàm trả về nhiều giá trị bằng tuple', R2('ds = [4, 9, 2, 7]\nkq = (min(ds), max(ds))\nprint(kq)\nnho, lon = kq\nprint(nho, lon)')),
         eg('Ví dụ 2: học sinh hai lớp', R2('a = {"Lan", "Minh", "Hà"}\nb = {"Minh", "An", "Hà", "Bình"}\nprint("Cả hai lớp:", sorted(a & b))\nprint("Chỉ lớp A:", sorted(a - b))\nprint("Tất cả:", len(a | b), "bạn")')),
         eg('Ví dụ 3: kiểm chứng công thức số phần tử', R2('a = {1, 2, 3, 4}\nb = {3, 4, 5}\nprint(len(a) + len(b) == len(a | b) + len(a & b))'))],
        [('Tạo tuple <code>hoa = ("đỏ", "vàng", "tím")</code>. In phần tử đầu, phần tử cuối và độ dài; rồi giải nén vào ba biến.', R2('hoa = ("đỏ", "vàng", "tím")\nprint(hoa[0], hoa[-1], len(hoa))\na, b, c = hoa\nprint(c, b, a)'), None),
         ('Danh sách điểm <code>[7, 9, 7, 8, 9, 10, 7]</code> có bao nhiêu điểm khác nhau? Liệt kê theo thứ tự tăng dần.', R2('diem = [7, 9, 7, 8, 9, 10, 7]\nkhac = set(diem)\nprint(len(khac), sorted(khac))'), None),
         ('Lớp A học Toán và Văn, lớp B học Văn và Anh. Với hai tập môn, in môn học chung và môn chỉ có ở một lớp.', R2('a = {"Toán", "Văn"}\nb = {"Văn", "Anh"}\nprint("Chung:", sorted(a & b))\nprint("Chỉ ở một lớp:", sorted(a ^ b))'), None),
         ('Viết đoạn chương trình đưa ba số <code>a, b, c</code> vào một tuple (min, max, tổng) rồi in.', R2('a, b, c = 4, 11, 7\nkq = (min(a, b, c), max(a, b, c), a + b + c)\nprint(kq)'), None),
         ('<b>Thử thách (nghĩ ngược):</b> Loại các phần tử trùng khỏi danh sách <code>[5, 3, 5, 1, 3, 2]</code> nhưng <b>giữ nguyên thứ tự xuất hiện đầu tiên</b> (dùng một set để nhớ những số đã gặp), rồi kiểm chứng số phần tử bằng <code>len(set(...))</code>.', R2('ds = [5, 3, 5, 1, 3, 2]\nda_gap = set()\nkq = []\nfor x in ds:\n    if x not in da_gap:\n        da_gap.add(x)\n        kq.append(x)\nprint(kq)\nprint(len(kq) == len(set(ds)))') + '<p>Set chỉ dùng để “nhớ đã gặp”, còn list <code>kq</code> giữ thứ tự. Dòng cuối kiểm chứng ngược: số phần tử khớp với số giá trị khác nhau.</p>', None)])

    # ====================================================== BÀI 5.3  TỪ ĐIỂN
    d1 = 'diem = {"Toán": 8, "Văn": 7, "Anh": 9}\nprint(diem["Toán"])\nprint(len(diem))\nprint(diem)'
    d2 = 'diem = {"Toán": 8, "Văn": 7}\ndiem["Lý"] = 6\ndiem["Văn"] = 8\nprint(diem)'
    d3 = 'diem = {"Toán": 8, "Văn": 7}\nprint(diem.get("Hóa"))\nprint(diem.get("Hóa", 0))\nprint("Toán" in diem)'
    d4 = 'diem = {"Toán": 8, "Văn": 7, "Anh": 9}\nfor mon in diem:\n    print(mon, diem[mon])\nfor mon, d in diem.items():\n    print(mon, "->", d)'
    d4b = 'diem = {"Toán": 8, "Văn": 7, "Anh": 9}\nprint(list(diem.keys()))\nprint(list(diem.values()))\nprint(sum(diem.values()))'
    d5 = 'cau = "mot hai mot ba hai mot"\nbang = {}\nfor tu in cau.split():\n    bang[tu] = bang.get(tu, 0) + 1\nprint(bang)'
    d6 = 'diem = {"Toán": 8, "Văn": 7, "Anh": 9}\ndel diem["Văn"]\nprint(diem)\nso = diem.pop("Anh")\nprint(so, diem)'
    d8 = 'ds = [{"ten": "Lan", "diem": 8}, {"ten": "Minh", "diem": 6}]\nfor h in ds:\n    print(h["ten"], h["diem"])'
    F = [fg('Từ điển là bảng “khóa → giá trị”', ['Khóa (key)', 'Giá trị (value)'], [['"Toán"', '8'], ['"Văn"', '7'], ['"Anh"', '9']], [320, 320], 'Mỗi phần tử gồm một khóa và một giá trị; tra bằng khóa, không phải bằng số thứ tự.'),
         fc('Tra bằng chỉ số và tra bằng khóa', [('bl', 'list', ['ds[1]'], 'phần tử thứ 2', 'phải nhớ vị trí'), ('gr', 'dict', ['diem["Văn"]'], '7', 'chỉ cần nhớ tên')], 'Từ điển cho phép dùng tên có ý nghĩa thay vì số thứ tự khó nhớ.'),
         fc('Thêm mới và cập nhật cùng một cú pháp', [('gr', 'Khóa chưa có', ['diem["Lý"] = 6'], 'thêm mới', ''), ('ye', 'Khóa đã có', ['diem["Văn"] = 8'], 'ghi đè', 'giá trị cũ mất')], 'Cùng một lệnh gán: có khóa rồi thì đổi giá trị, chưa có thì thêm mới.'),
         fc('[ ] và get: khi khóa không tồn tại', [('rd', 'diem["Hóa"]', ['khóa không có'], 'KeyError', 'chương trình dừng'), ('gr', 'diem.get("Hóa", 0)', ['khóa không có'], '0', 'trả về giá trị mặc định')], '<code>get</code> an toàn hơn: không có khóa thì trả về <code>None</code> hoặc giá trị mặc định em chọn.'),
         fg('Ba cách duyệt từ điển', ['Cách viết', 'Lấy được', 'Ví dụ kết quả'], [['for k in d', 'khóa', 'Toán, Văn, Anh'], ['d.values()', 'giá trị', '8, 7, 9'], ['d.items()', 'cả khóa và giá trị', '("Toán", 8) …']], [190, 200, 250], 'Muốn cả hai thì dùng <code>for k, v in d.items()</code>.'),
         trace_fig('Đếm từ trong câu “mot hai mot ba hai mot”', ['Từ', 'Trước khi đếm', 'Sau khi đếm'], [('mot', '{}', '{mot: 1}'), ('hai', '{mot: 1}', '{mot: 1, hai: 1}'), ('mot', '…', '{mot: 2, hai: 1}'), ('ba', '…', '{… ba: 1}'), ('hai', '…', '{mot: 2, hai: 2, ba: 1}'), ('mot', '…', '{mot: 3, hai: 2, ba: 1}')], 'Mỗi từ: lấy số đếm cũ (mặc định 0) rồi cộng 1 – mẫu <code>bang[tu] = bang.get(tu, 0) + 1</code>.'),
         fc('Khóa phải là kiểu không đổi được', [('gr', 'Hợp lệ', ['chữ, số, tuple'], '"Toán", 5, (1, 2)', 'bất biến'), ('rd', 'Không hợp lệ', ['list, set, dict'], 'TypeError', 'sửa được nên không làm khóa')], 'Khóa phải “băm” được; kiểu sửa được như list không làm khóa.'),
         fg('Danh sách các từ điển: bảng dữ liệu', ['ten', 'diem'], [['"Lan"', '8'], ['"Minh"', '6']], [320, 320], 'Mỗi từ điển là một hàng (một học sinh); cả danh sách là cả bảng.'),
         fg('Chọn list hay dict?', ['Cần', 'Dùng', 'Ví dụ'], [['Thứ tự, vị trí', 'list', 'điểm theo lượt kiểm tra'], ['Tra theo tên', 'dict', 'điểm theo môn'], ['Đếm số lần xuất hiện', 'dict', 'đếm từ'], ['Chỉ cần loại trùng', 'set', 'danh sách tên khác nhau']], [200, 120, 320], 'Hỏi: “Mình tra theo vị trí hay theo tên?”'),
         ff(['Xác định|khóa và giá trị', 'Tạo từ điển|rỗng hoặc có sẵn', 'Duyệt hoặc|tra cứu', 'Dùng get|cho khóa lạ', 'Thử với|dữ liệu nhỏ'], 'Quy trình dùng từ điển'),
         fp(d2, [0, 1, 2, 3], ['Tạo từ điển có hai môn.', 'Thêm khóa “Lý” → 6.', 'Khóa “Văn” đã có nên ghi đè thành 8.', 'In ra từ điển đã cập nhật.'], maxn=6),
         fc('Xóa phần tử: del và pop', [('rd', 'del d["Văn"]', ['xóa theo khóa'], 'mất cả cặp', 'không trả về gì'), ('bl', 'd.pop("Anh")', ['lấy ra rồi xóa'], 'trả về 9', 'dùng khi cần giá trị')], 'Cả hai đều xóa; <code>pop</code> còn trả lại giá trị vừa xóa.')]
    cmd = [['<code>{ khóa: giá trị }</code>', 'Tạo từ điển: mỗi cặp cách nhau dấu phẩy, khóa và giá trị cách nhau dấu hai chấm.', W('Quên dấu hai chấm:', 'd = {"a" 1}', 'E')],
           ['<code>d[khóa]</code>', 'Lấy giá trị của khóa.', W('Khóa không có:', 'd = {"Toán": 8}\nprint(d["Lý"])', 'E')],
           ['<code>d[khóa] = giá_trị</code>', 'Thêm mới hoặc ghi đè.', W('Kiểm tra: gán cùng khóa hai lần chỉ còn giá trị cuối:', 'd = {}\nd["a"] = 1\nd["a"] = 2\nprint(d)', 'R')],
           ['<code>d.get(khóa, mặc_định)</code>', 'Lấy giá trị an toàn.', W('Bỏ giá trị mặc định thì ra <code>None</code>:', d3, 'R')],
           ['<code>khóa in d</code>', 'Kiểm tra khóa có trong từ điển (không kiểm tra giá trị).', W('<code>in</code> chỉ tìm trong khóa:', 'd = {"a": 1}\nprint("a" in d)\nprint(1 in d)', 'R')],
           ['<code>for k in d</code>', 'Duyệt các khóa.', W('Duyệt giá trị phải dùng <code>.values()</code>:', 'd = {"a": 1, "b": 2}\nfor x in d:\n    print(x)', 'R')],
           ['<code>d.items()</code>', 'Cho từng cặp (khóa, giá trị).', W('Giải nén sai số biến:', 'd = {"a": 1}\nfor k, v, z in d.items():\n    print(k)', 'E')],
           ['<code>del d[khóa]</code> và <code>.pop</code>', 'Xóa một cặp.', W('Xóa khóa không có:', 'd = {"a": 1}\ndel d["b"]', 'E')],
           ['khóa kiểu list', 'Khóa phải là kiểu không sửa được.', W('Dùng list làm khóa:', 'd = {[1, 2]: "a"}', 'E')]]
    P['c5b3'] = LS('Bài 5.3 · Từ điển (dict)', 'Tra cứu bằng tên thay vì số thứ tự.',
        ('Tạo, thêm, sửa, xóa và duyệt từ điển; dùng get để tránh KeyError; viết mẫu đếm số lần xuất hiện', 'Đã biết list, tuple, set (Bài 5.1, 5.2)', 'Sổ điểm theo môn và chương trình đếm từ'),
        ['Đời sống đầy những quan hệ “tên → giá trị”: môn → điểm, tên → số điện thoại, từ → nghĩa.', 'Từ điển cho phép tra rất nhanh bằng khóa mà không phải duyệt từng phần tử.', 'Mẫu đếm số lần xuất hiện bằng từ điển dùng được cho văn bản, điểm số, kết quả khảo sát.', 'Từ điển là nền cho dữ liệu dạng bảng, JSON và đối tượng ở các chương sau.'],
        ol(['Hỏi: “Cái gì là khóa (tên để tra), cái gì là giá trị?”', 'Tạo từ điển: <code>{ khóa: giá trị, … }</code>; thêm sửa bằng <code>d[khóa] = giá_trị</code>.', 'Tra cứu bằng <code>d[khóa]</code> hoặc <code>d.get(khóa, mặc_định)</code> khi khóa có thể không có.', 'Duyệt bằng <code>for k, v in d.items()</code>.']),
        think(['<b>Phản biện:</b> nếu khóa không tồn tại thì chương trình sẽ xử lý thế nào? Em đã chuẩn bị chưa?', '<b>Nghĩ ngược:</b> biết kết quả cần là “từ → số lần”, em dựng từ điển rỗng rồi cập nhật từng từ.', '<b>Thói quen tốt:</b> dùng khóa có ý nghĩa (tên môn) thay vì số thứ tự khó nhớ.']),
        [A('Tạo và tra cứu:', d1), A('Thêm mới và ghi đè:', d2), A('Tra an toàn bằng get và kiểm tra bằng in:', d3), A('Duyệt khóa và cặp:', d4), A('Khóa, giá trị và tổng điểm:', d4b), A('Đếm từ:', d5), A('Xóa phần tử:', d6), A('Danh sách các từ điển:', d8)],
        'Phân tích từng phần. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', cmd, F,
        [err('Tra khóa không tồn tại bằng [ ]', E2('d = {"Toán": 8}\nprint(d["Lý"])'), 'Dùng <code>d.get("Lý", 0)</code> hoặc kiểm tra <code>"Lý" in d</code> trước.'),
         err('Nhầm <code>in</code> kiểm tra giá trị', R2('d = {"a": 1}\nprint(1 in d)'), '<code>in</code> chỉ tìm trong khóa; muốn tìm giá trị dùng <code>1 in d.values()</code>.'),
         err('Dùng list làm khóa', E2('d = {[1, 2]: "a"}'), 'Dùng tuple <code>(1, 2)</code> làm khóa.'),
         err('Quên khởi tạo khi đếm', 'Cộng vào khóa chưa có gây lỗi:' + E2('bang = {}\nbang["a"] += 1'), 'Dùng <code>bang["a"] = bang.get("a", 0) + 1</code>.'),
         err('Ghi đè nhầm vì trùng khóa', R2('d = {"Lan": 7, "Lan": 9}\nprint(d)'), 'Hai khóa trùng thì chỉ còn giá trị cuối; chọn khóa duy nhất.')],
        [eg('Ví dụ 1: danh bạ', R2('danh_ba = {"Lan": "0901", "Minh": "0902"}\nten = "Hà"\nprint(danh_ba.get(ten, "Không có trong danh bạ"))\nprint(danh_ba.get("Minh", "Không có"))')),
         eg('Ví dụ 2: đếm chữ cái', R2('bang = {}\nfor ch in "banana":\n    bang[ch] = bang.get(ch, 0) + 1\nprint(bang)')),
         eg('Ví dụ 3: nhóm từ theo độ dài', R2('tu = ["cam", "kiwi", "nho", "xoài", "chuối"]\nnhom = {}\nfor t in tu:\n    nhom.setdefault(len(t), []).append(t)\nprint(nhom)') + note('<code>setdefault</code> tạo danh sách rỗng nếu khóa chưa có rồi trả về danh sách đó.'))],
        [('Tạo từ điển điểm các môn Toán 8, Văn 7, Anh 9; in điểm Toán và số môn.', R2('diem = {"Toán": 8, "Văn": 7, "Anh": 9}\nprint(diem["Toán"])\nprint(len(diem))'), None),
         ('Tính tổng và điểm trung bình từ các giá trị của từ điển điểm ở trên.', R2('diem = {"Toán": 8, "Văn": 7, "Anh": 9}\ntong = sum(diem.values())\nprint(tong, round(tong / len(diem), 2))'), None),
         ('Đếm số lần mỗi chữ cái xuất hiện trong từ “mississippi”.', R2('bang = {}\nfor ch in "mississippi":\n    bang[ch] = bang.get(ch, 0) + 1\nprint(bang)') + '<p>Kiểm chứng: tổng các số đếm phải bằng độ dài từ (11).</p>' + R2('bang = {"m": 1, "i": 4, "s": 4, "p": 2}\nprint(sum(bang.values()) == len("mississippi"))'), None),
         ('Danh bạ có “Lan” và “Minh”. Viết đoạn nhập tên rồi in số điện thoại; nếu không có thì in “Không tìm thấy”.', A('', 'danh_ba = {"Lan": "0901", "Minh": "0902"}\nten = input()\nprint(danh_ba.get(ten, "Không tìm thấy"))', 'Minh\n') + A('Thử với tên không có:', 'danh_ba = {"Lan": "0901", "Minh": "0902"}\nten = input()\nprint(danh_ba.get(ten, "Không tìm thấy"))', 'Hà\n'), None),
         ('<b>Thử thách (nghĩ ngược):</b> Đảo từ điển <code>{"a": 1, "b": 2, "c": 3}</code> thành <code>{1: "a", 2: "b", 3: "c"}</code>, rồi đảo lại và kiểm chứng ra từ điển ban đầu.', R2('goc = {"a": 1, "b": 2, "c": 3}\ndao = {}\nfor k, v in goc.items():\n    dao[v] = k\nprint(dao)\ndao_lai = {}\nfor k, v in dao.items():\n    dao_lai[v] = k\nprint(dao_lai == goc)') + '<p>Đảo hai lần thì trở về như cũ vì các giá trị ban đầu đều khác nhau; nếu có giá trị trùng thì phép đảo sẽ mất dữ liệu.</p>', None)])

    # ====================================================== BÀI 5.4  DUYỆT, TÌM KIẾM, SẮP XẾP
    s1 = 'ds = [5, 9, 2, 9, 7]\nfor x in ds:\n    print(x, end=" ")\nprint()\nfor i, x in enumerate(ds):\n    print(i, x)'
    s2 = 'ds = [5, 9, 2, 9, 7]\nvi_tri = -1\nfor i in range(len(ds)):\n    if ds[i] == 9:\n        vi_tri = i\n        break\nprint(vi_tri)'
    s4 = 'ds = [5, 9, 2, 9, 7]\nprint(sorted(ds))\nprint(ds)\nds.sort()\nprint(ds)\nds.sort(reverse=True)\nprint(ds)'
    s5 = 'ten = ["Minh", "an", "Lan", "bình"]\nprint(sorted(ten))\nprint(sorted(ten, key=str.lower))'
    s6 = 'tu = ["banana", "kiwi", "cam", "xoài"]\nprint(sorted(tu, key=len))'
    s7 = 'ds = [5, 2, 9, 1]\nfor i in range(len(ds) - 1):\n    for j in range(len(ds) - 1 - i):\n        if ds[j] > ds[j + 1]:\n            ds[j], ds[j + 1] = ds[j + 1], ds[j]\nprint(ds)'
    s8 = 'ds = [1, 3, 5, 7, 9, 11, 13]\nmuc = 11\ntrai = 0\nphai = len(ds) - 1\nvi_tri = -1\nwhile trai <= phai:\n    giua = (trai + phai) // 2\n    if ds[giua] == muc:\n        vi_tri = giua\n        break\n    elif ds[giua] < muc:\n        trai = giua + 1\n    else:\n        phai = giua - 1\nprint(vi_tri)'
    bub = [5, 2, 9, 1]; passes = []
    for i in range(len(bub) - 1):
        for j in range(len(bub) - 1 - i):
            if bub[j] > bub[j + 1]: bub[j], bub[j + 1] = bub[j + 1], bub[j]
        passes.append((i + 1, str(list(bub))))
    F = [fg('Hai cách duyệt danh sách', ['Cách viết', 'Lấy được', 'Dùng khi'], [['for x in ds', 'từng giá trị', 'chỉ cần giá trị'], ['for i in range(len(ds))', 'chỉ số i', 'cần vị trí'], ['for i, x in enumerate(ds)', 'cả chỉ số và giá trị', 'cần cả hai']], [250, 190, 200], 'Chọn cách duyệt theo thứ em cần: giá trị, vị trí hay cả hai.'),
         trace_fig('Tìm tuần tự số 9 trong [5, 9, 2, 9, 7]', ['i', 'ds[i]', 'có phải 9?'], [(0, 5, 'không'), (1, 9, 'đúng → vi_tri = 1, dừng!')], 'Tìm tuần tự: xét từng phần tử từ đầu; gặp là dừng (break), nếu hết dãy mà chưa gặp thì vi_tri vẫn là -1.', hl=[1]),
         fc('sorted và sort khác nhau', [('bl', 'sorted(ds)', ['trả về list mới'], 'ds không đổi', 'dùng khi cần giữ bản gốc'), ('ye', 'ds.sort()', ['sắp ngay trong ds'], 'ds đổi, trả về None', 'tiết kiệm bộ nhớ')], 'Hai cách đều sắp tăng dần; thêm <code>reverse=True</code> để sắp giảm dần.'),
         fc('Tham số key: sắp theo tiêu chí tự chọn', [('bl', 'Mặc định', ['sorted(tu)'], 'theo bảng chữ cái', ''), ('gr', 'key=len', ['sorted(tu, key=len)'], 'theo độ dài', 'ngắn trước dài sau')], '<code>key</code> nhận một hàm; mỗi phần tử được đưa qua hàm đó rồi mới so sánh.'),
         trace_fig('Sắp xếp nổi bọt [5, 2, 9, 1] qua từng lượt', ['Lượt', 'Danh sách sau lượt'], [(a, b) for a, b in passes], 'Mỗi lượt, số lớn nhất “nổi” về cuối; sau n − 1 lượt cả dãy đã tăng dần.'),
         fig(svg(700, 190, ARR + txt(350, 24, 'Một phép đổi chỗ khi ds[j] > ds[j + 1]', '#17406b', 17, bold=True) + ''.join(box(150 + i * 100, 60, 90, 56, c, st, [str(v)], 22, bold=True) for i, (v, c, st) in enumerate([(5, '#fdecea', '#c0392b'), (2, '#fdecea', '#c0392b'), (9, '#f3f4f6', '#9db4c9'), (1, '#f3f4f6', '#9db4c9')])) + txt(250, 150, '5 > 2 → đổi chỗ thành [2, 5, 9, 1]', '#c0392b', 15, bold=True) + txt(350, 176, 'ds[j], ds[j + 1] = ds[j + 1], ds[j]', '#5b6773', 14), 'Đổi chỗ'), 'Hai ô liền kề đứng sai thứ tự thì đổi chỗ bằng phép gán tuple – không cần biến tạm.'),
         fig(svg(700, 250, ARR + txt(350, 24, 'Tìm kiếm nhị phân số 11 trong [1, 3, 5, 7, 9, 11, 13]', '#17406b', 17, bold=True) + ''.join(box(70 + i * 82, 52, 76, 44, '#e6f1fb' if i not in (3, 5) else ('#fff4d6' if i == 3 else '#e5f5ea'), '#1f6fb2' if i not in (3, 5) else ('#d9822b' if i == 3 else '#2a8a4a'), [str(v)], 18, bold=True) for i, v in enumerate([1, 3, 5, 7, 9, 11, 13])) + txt(70 + 3 * 82 + 38, 118, 'giữa = 3 → 7', '#d9822b', 13, bold=True) + txt(70 + 3 * 82 + 38, 138, '7 < 11 → bỏ nửa trái', '#5b6773', 13) + txt(70 + 5 * 82 + 38, 176, 'giữa = 5 → 11 ✓', '#2a8a4a', 14, bold=True) + txt(350, 218, 'Danh sách đã sắp xếp: mỗi bước loại một nửa còn lại', '#5b6773', 14), 'Tìm nhị phân'), 'Nhị phân chỉ dùng được khi danh sách đã sắp xếp; mỗi bước loại ngay một nửa.'),
         fg('Số bước tìm trong danh sách n phần tử (xấu nhất)', ['Số phần tử n', 'Tuần tự', 'Nhị phân'], [['8', '8', '4'], ['1.000', '1.000', '10'], ['1.000.000', '1.000.000', '20']], [220, 210, 210], 'Nhị phân nhanh hơn tuần tự rất nhiều khi dữ liệu lớn, nhưng đòi hỏi dữ liệu đã sắp xếp.'),
         fg('Chọn cách tìm nào?', ['Tình huống', 'Dùng'], [['Dữ liệu chưa sắp xếp, ít phần tử', 'tìm tuần tự'], ['Chỉ cần biết có hay không', 'x in ds (hoặc set)'], ['Dữ liệu lớn và đã sắp xếp', 'tìm nhị phân'], ['Tra theo tên', 'từ điển']], [360, 280], 'Chọn cách tìm theo dữ liệu em có.'),
         ff(['Xác định|việc cần làm', 'Chọn duyệt,|tìm hay sắp xếp', 'Viết bằng|vòng lặp', 'Thử trên|danh sách nhỏ', 'Kiểm chứng|bằng sorted'], 'Quy trình xử lý danh sách'),
         fp(s2, [0, 1, 2, 3, 4], ['Gán danh sách và <b>vi_tri</b> = -1.', 'Vào vòng lặp với i = 0.', 'Kiểm tra ds[0] == 9: sai.', 'Sang i = 1; ds[1] = 9 nên đúng.', 'Gán vi_tri = 1 rồi dừng.'], maxn=8),
         fc('sort() trả về None', [('rd', 'kq = ds.sort()', ['sai ý định'], 'kq là None', 'sort sắp tại chỗ'), ('gr', 'kq = sorted(ds)', ['đúng ý định'], 'kq là list mới', 'dùng khi cần giá trị trả về')], 'Một lỗi rất hay gặp: gán kết quả của <code>.sort()</code> vào biến.')]
    cmd = [['<code>for x in ds</code>', 'Duyệt từng giá trị của danh sách.', W('Viết thiếu <code>in</code>:', 'ds = [1, 2]\nfor x ds:\n    print(x)', 'E')],
           ['<code>enumerate(ds)</code>', 'Cho từng cặp (chỉ số, giá trị).', W('Nhận sai số biến:', 'for i, x, y in enumerate([5, 6]):\n    print(i)', 'E')],
           ['<code>range(len(ds))</code>', 'Dãy các chỉ số hợp lệ 0 … len − 1.', W('Dùng <code>range(len(ds) + 1)</code> sẽ vượt cuối:', 'ds = [5, 6]\nfor i in range(len(ds) + 1):\n    print(ds[i])', 'E')],
           ['<code>break</code> khi tìm thấy', 'Dừng khi đã gặp để khỏi duyệt thừa.', 'Bỏ <code>break</code> thì <code>vi_tri</code> sẽ là vị trí <b>cuối cùng</b> của số 9 chứ không phải đầu tiên.'],
           ['<code>sorted(ds)</code>', 'Trả về danh sách mới đã sắp, giữ nguyên ds.', W('Sắp xếp danh sách trộn số và chữ:', 'print(sorted([3, "a", 1]))', 'E')],
           ['<code>ds.sort()</code>', 'Sắp xếp ngay trong ds và trả về <code>None</code>.', W('Gán kết quả vào biến:', 'ds = [3, 1, 2]\nkq = ds.sort()\nprint(kq)', 'R')],
           ['<code>reverse=True</code>', 'Sắp giảm dần.', W('Thử:', 'print(sorted([3, 1, 2], reverse=True))', 'R')],
           ['<code>key=len</code>', 'Sắp theo kết quả của hàm key.', W('Gọi hàm thay vì đưa tên hàm (<code>len()</code>):', 'print(sorted(["bb", "a"], key=len()))', 'E')],
           ['<code>(trai + phai) // 2</code>', 'Vị trí giữa của đoạn đang xét.', W('Dùng <code>/</code> thay <code>//</code> gây vị trí không nguyên:', 'ds = [1, 2, 3]\nprint(ds[(0 + 2) / 2])', 'E')]]
    P['c5b4'] = LS('Bài 5.4 · Duyệt, tìm kiếm và sắp xếp', 'Ba việc nền tảng nhất khi xử lý một danh sách dữ liệu.',
        ('Duyệt danh sách bằng for, enumerate; tìm tuần tự và nhị phân; sắp xếp bằng sorted, sort, key; hiểu thuật toán nổi bọt', 'Đã biết list, dict và vòng lặp', 'Chương trình tìm vị trí, xếp hạng điểm và tìm nhị phân'),
        ['Hầu như mọi chương trình xử lý dữ liệu đều lặp lại ba việc: <b>duyệt</b>, <b>tìm</b>, <b>sắp xếp</b>.', 'Biết thuật toán chạy bên trong giúp em hiểu vì sao có cách nhanh, cách chậm.', 'Hàm có sẵn <code>sorted</code> rất mạnh, nhưng tự viết sắp xếp nổi bọt giúp rèn tư duy thuật toán.', 'So sánh số bước tìm tuần tự và nhị phân giúp em hiểu “hiệu quả” của một thuật toán.'],
        ol(['Xác định việc: duyệt tất cả, tìm một phần tử hay sắp xếp?', 'Duyệt: chọn <code>for x in ds</code> hoặc <code>enumerate</code>; tìm: nhớ <code>break</code> khi thấy; sắp: <code>sorted</code> hoặc <code>sort</code>.', 'Thử trên danh sách <b>nhỏ</b> (4 – 5 phần tử) và theo dõi từng bước.', 'Kiểm chứng ngược: kết quả sắp xếp phải tăng dần; vị trí tìm được phải thỏa <code>ds[vi_tri] == muc</code>.']),
        think(['<b>Phản biện:</b> với dữ liệu 1 triệu phần tử, cách tìm này có còn nhanh không?', '<b>Nghĩ ngược:</b> sau khi sắp xếp, mỗi phần tử có nhỏ hơn hoặc bằng phần tử đứng sau nó không? Kiểm tra bằng vòng lặp.', '<b>Thói quen tốt:</b> dùng hàm có sẵn khi đã hiểu cách nó làm việc.']),
        [A('Duyệt bằng for và enumerate:', s1), A('Tìm tuần tự:', s2), A('sorted và sort:', s4), A('Sắp chữ có hoa thường:', s5), A('Sắp theo độ dài:', s6), A('Sắp xếp nổi bọt:', s7), A('Tìm nhị phân:', s8)],
        'Phân tích từng phần. Phần “Nếu thiếu hoặc sai” là kết quả chạy thật.', cmd, F,
        [err('Gán kết quả của sort()', R2('ds = [3, 1, 2]\nkq = ds.sort()\nprint(kq)'), 'Dùng <code>sorted(ds)</code> nếu cần giá trị trả về.'),
         err('Dùng tìm nhị phân trên dữ liệu chưa sắp xếp', R2('ds = [9, 1, 7, 3, 5]\ntrai = 0\nphai = len(ds) - 1\nmuc = 3\nvi_tri = -1\nwhile trai <= phai:\n    giua = (trai + phai) // 2\n    if ds[giua] == muc:\n        vi_tri = giua\n        break\n    elif ds[giua] < muc:\n        trai = giua + 1\n    else:\n        phai = giua - 1\nprint(vi_tri)') + 'Số 3 có trong dãy (ở vị trí 3) nhưng bị bỏ sót.', 'Chỉ dùng nhị phân khi danh sách đã sắp xếp.'),
         err('Vượt chỉ số cuối', E2('ds = [1, 2, 3]\nfor i in range(len(ds) + 1):\n    print(ds[i])'), 'Chỉ số hợp lệ từ 0 đến <code>len(ds) - 1</code>.'),
         err('Sắp xếp chữ mà quên hoa thường', R2('print(sorted(["Minh", "an", "Lan"]))'), 'Dùng <code>key=str.lower</code> để bỏ qua hoa thường.'),
         err('Quên break khi tìm', 'Chương trình vẫn đúng nhưng chạy thừa; nếu cần vị trí đầu tiên thì kết quả còn sai.', 'Thêm <code>break</code> ngay khi tìm thấy.')],
        [eg('Ví dụ 1: top 3 điểm cao nhất', R2('diem = [7.5, 9, 6, 8.5, 10, 5]\ntop = sorted(diem, reverse=True)[:3]\nprint(top)')),
         eg('Ví dụ 2: xếp hạng từ điển theo giá trị', R2('diem = {"Lan": 8.5, "Minh": 6, "Hà": 9}\nfor ten in sorted(diem, key=diem.get, reverse=True):\n    print(ten, diem[ten])') + note('<code>key=diem.get</code>: mỗi tên được đưa qua <code>diem.get</code> để lấy điểm rồi mới so sánh.')),
         eg('Ví dụ 3: kiểm chứng danh sách đã sắp', R2('ds = [2, 5, 5, 9]\nso_hop_le = True\nfor i in range(len(ds) - 1):\n    if ds[i] > ds[i + 1]:\n        so_hop_le = False\nprint(so_hop_le)'))],
        [('Tìm và in vị trí của số lớn nhất trong <code>[5, 9, 2, 9, 7]</code> (lấy vị trí đầu tiên).', R2('ds = [5, 9, 2, 9, 7]\nlon = max(ds)\nprint(ds.index(lon))'), None),
         ('Tìm <b>tất cả</b> vị trí của số 9 trong danh sách trên.', R2('ds = [5, 9, 2, 9, 7]\nfor i in range(len(ds)):\n    if ds[i] == 9:\n        print(i, end=" ")\nprint()'), None),
         ('Sắp điểm <code>[7.5, 9, 6, 8.5, 10]</code> giảm dần và in 3 điểm cao nhất.', R2('diem = [7.5, 9, 6, 8.5, 10]\ndiem.sort(reverse=True)\nprint(diem[:3])'), None),
         ('Sắp danh sách tên theo độ dài, các tên bằng độ dài xếp theo bảng chữ cái: <code>["Hà", "An", "Minh", "Lan", "Bình"]</code>.', R2('ten = ["Hà", "An", "Minh", "Lan", "Bình"]\nprint(sorted(sorted(ten), key=len))') + '<p>Sắp theo bảng chữ cái trước rồi sắp theo độ dài; Python giữ nguyên thứ tự cũ với các phần tử cùng độ dài nên kết quả đúng ý.</p>', None),
         ('<b>Thử thách (nghĩ ngược):</b> Tạo danh sách 1 đến 1000 và tìm số 777 bằng tìm tuần tự và tìm nhị phân, đếm số bước mỗi cách. Kiểm chứng vị trí tìm được thỏa <code>ds[vi_tri] == 777</code>.', R2('ds = list(range(1, 1001))\nmuc = 777\nbuoc1 = 0\nfor x in ds:\n    buoc1 += 1\n    if x == muc:\n        break\ntrai = 0\nphai = len(ds) - 1\nbuoc2 = 0\nvi_tri = -1\nwhile trai <= phai:\n    buoc2 += 1\n    giua = (trai + phai) // 2\n    if ds[giua] == muc:\n        vi_tri = giua\n        break\n    elif ds[giua] < muc:\n        trai = giua + 1\n    else:\n        phai = giua - 1\nprint("Tuần tự:", buoc1, "bước")\nprint("Nhị phân:", buoc2, "bước")\nprint(ds[vi_tri] == muc)') + '<p>Số bước thực tế do máy đếm: nhị phân chỉ cần vài bước trong khi tuần tự cần 777 bước.</p>', None)])

    # ====================================================== TÓM TẮT CHƯƠNG 5
    proj = 'diem = {"Lan": 8.5, "Minh": 6.0, "Hà": 9.0, "An": 4.5, "Bình": 7.5}\ntong = sum(diem.values())\nprint(f"Trung bình lớp: {tong / len(diem):.2f}")\nprint("Xếp hạng:")\nxep = sorted(diem, key=diem.get, reverse=True)\nfor hang, ten in enumerate(xep, start=1):\n    print(f"  {hang}. {ten}: {diem[ten]}")\nloai = {}\nfor d in diem.values():\n    if d >= 8:\n        xl = "Giỏi"\n    elif d >= 6.5:\n        xl = "Khá"\n    elif d >= 5:\n        xl = "Trung bình"\n    else:\n        xl = "Yếu"\n    loai[xl] = loai.get(xl, 0) + 1\nprint(loai)'
    P['c5t'] = SUM(5, 'Cấu trúc dữ liệu',
        [('list – tuple – set', 'chọn đúng kiểu dữ liệu'), ('Từ điển (Bài 5.3)', 'khóa → giá trị'), ('Duyệt và tìm', 'tuần tự, nhị phân'), ('Sắp xếp', 'sorted, sort, key')],
        ['Mỗi giá trị một biến riêng', 'Chưa biết tra cứu theo tên', 'Tìm kiếm bằng cách duyệt hết'], ['Chọn list, tuple, set, dict đúng việc', 'Đếm và tra cứu bằng từ điển', 'Sắp xếp và tìm nhị phân'],
        ['Phân biệt list, tuple, set', 'Dùng giải nén tuple', 'Dùng hợp – giao – hiệu', 'Tạo và duyệt từ điển', 'Sắp xếp bằng key', 'Tìm nhị phân'],
        [['list / tuple / set', '<code>[ ]  ( )  { }</code>', 'Sửa được / cố định / loại trùng'], ['giải nén', '<code>x, y = (3, 5)</code>', 'Số biến bằng số phần tử'], ['phép tập hợp', '<code>a | b</code>, <code>a &amp; b</code>', 'Hợp, giao, hiệu, phần ở đúng một bên'], ['từ điển', '<code>d[k] = v</code>', 'Thêm hoặc ghi đè'], ['<code>d.get(k, 0)</code>', 'tra an toàn', 'Không có khóa thì trả về giá trị mặc định'], ['<code>sorted(x, key=…)</code>', '<code>key=len</code>', 'Sắp theo tiêu chí tự chọn'], ['tìm nhị phân', 'trai, phai, giua', 'Chỉ dùng khi đã sắp xếp']],
        [('Sửa phần tử của tuple', 'TypeError.', 'Dùng list hoặc tạo tuple mới.'), ('Tạo set rỗng bằng {}', 'Ra từ điển.', 'Dùng <code>set()</code>.'), ('Tra khóa không có bằng [ ]', 'KeyError.', 'Dùng <code>get</code> hoặc kiểm tra <code>in</code>.'), ('Gán kết quả của sort()', 'Nhận được None.', 'Dùng <code>sorted</code>.'), ('Nhị phân trên dữ liệu chưa sắp', 'Có thể bỏ sót.', 'Sắp xếp trước khi tìm.')],
        [('Tuple khác list ở điểm nào?', 'Tuple không sửa được từng phần tử; list sửa được.'), ('Set dùng khi nào?', 'Khi cần loại trùng hoặc kiểm tra thuộc rất nhanh.'), ('<code>d.get("x", 0)</code> làm gì?', 'Lấy giá trị của khóa “x”; nếu không có thì trả về 0 thay vì báo lỗi.'), ('Viết một dòng đếm số lần từ <code>tu</code> xuất hiện trong từ điển <code>bang</code>.', '<code>bang[tu] = bang.get(tu, 0) + 1</code>.'), ('Khác nhau giữa sorted và sort?', 'sorted trả về list mới và giữ nguyên bản gốc; sort sắp ngay trong list và trả về None.'), ('Vì sao tìm nhị phân nhanh hơn?', 'Mỗi bước loại bỏ một nửa phần còn lại, nhưng chỉ dùng được khi dữ liệu đã sắp xếp.')],
        'Sổ điểm lớp học', 'Cho từ điển điểm của 5 học sinh. In điểm trung bình (làm tròn 2 chữ số), bảng xếp hạng từ cao xuống thấp có số thứ tự, và số học sinh theo từng loại (Giỏi ≥ 8, Khá ≥ 6.5, Trung bình ≥ 5, Yếu). Dùng đủ: từ điển, <code>sum</code>, <code>sorted(…, key=…)</code>, <code>enumerate</code>, đếm bằng từ điển.',
        proj, [''], 'Trong f-string, <code>{x:.2f}</code> in số x với đúng 2 chữ số thập phân. <code>enumerate(xep, start=1)</code> bắt đầu đếm từ 1 thay vì 0.',
        ['<b>Chương 6 – Hàm:</b> đặt tên cho một nhóm lệnh để dùng lại nhiều lần, chia bài toán lớn thành các việc nhỏ.', 'Em đã biết <b>chứa dữ liệu</b>; sang chương 6 em sẽ <b>đóng gói cách xử lý</b> thành các hàm tái sử dụng.'],
        ['<b>Chọn đúng kiểu dữ liệu</b> trước khi viết code.', '<b>Dùng get</b> khi khóa có thể không có.', '<b>Kiểm chứng ngược</b> sau khi sắp xếp hoặc tìm kiếm.'])
    return P
