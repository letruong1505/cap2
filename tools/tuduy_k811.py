"""Lộ trình 8–11 (Scratch): 8 bài theo khung 8 mục."""
from tuduy_lib import *

def sim(cmds, x=0, y=0, ang=90):
    """Mô phỏng robot: f n, b n, r d, l d. Trả (x, y, hướng)."""
    import math
    for c, v in cmds:
        if c in 'fb':
            k = v if c == 'f' else -v
            x += k * math.cos(math.radians(ang)); y += k * math.sin(math.radians(ang))
        elif c == 'r': ang -= v
        elif c == 'l': ang += v
    return round(x), round(y), round(ang) % 360

def vsteps(prog, init=None, caps=None):
    """prog: [(khối, hàm(state))]. Hiện khối được làm nổi bật và giá trị biến sau từng khối."""
    st = dict(init or {}); src = '\n'.join(b for b, _ in prog); res = []
    for i, (b, f) in enumerate(prog):
        f(st)
        chips = ''.join('<span class="pv"><b>%s</b> = %s</span>' % (k, v) for k, v in st.items())
        res.append((caps[i] if caps else 'Chạy khối <b>%s</b>.' % E(b.strip()), '<div class="ptr">' + sblocks(src, hl=(i,)) + '<div class="pvars">' + (chips or '<span class="pv none">(chưa có biến)</span>') + '</div></div>'))
    return steps(*res)

def build():
    K = {}
    # ---------------- Bài 1 ----------------
    assert sim([('f', 3), ('r', 90), ('f', 2), ('l', 90), ('f', 1)]) == (2, 4, 90)
    assert sim([('b', 1), ('r', 90), ('b', 2), ('l', 90), ('b', 3)], 2, 4, 90) == (0, 0, 90)
    K['bai1'] = std('Bài 1 · Máy chỉ làm đúng điều em bảo', 'Thuật toán là dãy bước rõ ràng, đúng thứ tự.',
        ('Viết được dãy bước đủ rõ để “người máy” làm theo; tìm được bước bị thiếu hoặc sai thứ tự', 'Giấy bút; Scratch (trên trình duyệt hoặc ứng dụng)', 'Bản hướng dẫn cho người máy và chương trình Scratch đầu tiên'),
        ['<b>Thuật toán</b> là dãy bước rõ ràng, sắp đúng thứ tự để làm xong một việc.', 'Máy tính rất nhanh nhưng <b>không tự đoán ý</b>: nó làm đúng từng chữ em bảo.', 'Học bài này, em sẽ biết cách “nói chuyện” với máy: đủ bước, đủ rõ, đúng thứ tự.'],
        ol(['<b>Nghĩ đích:</b> việc cuối cùng cần xong là gì?', '<b>Viết các bước ngắn</b>, mỗi dòng một việc.', '<b>Đọc lại như người máy:</b> nếu chỉ làm đúng chữ, có chỗ nào bí không?', '<b>Đổi thành khối lệnh</b> Scratch, mỗi bước một khối.']) + note('Dùng bài này mỗi khi em muốn dạy ai đó (hoặc máy) làm việc gì: pha mì, xếp cặp, vẽ một hình.'),
        think(['<b>Tư duy phản biện:</b> “Người máy làm theo bản này có ra đúng kết quả không?” Em tự đóng vai người máy để thử.', '<b>Tư duy ngược:</b> bắt đầu từ việc cuối cùng, hỏi “trước đó phải làm gì?” để không bỏ sót bước.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['Mỗi <b>khối lệnh</b> là một bước. Khối xếp chồng chạy từ trên xuống dưới.', 'Khối vàng <b>khi bấm cờ xanh</b> là nút bắt đầu; không có nó chương trình không tự chạy.']) + sblocks('khi bấm cờ xanh\n  tiến 50 bước\n  nói "Xin chào!" trong 2 giây') + note('Mèo đi tới 50 bước rồi nói “Xin chào!” trong 2 giây. Đảo hai khối cho nhau thì mèo nói trước rồi mới đi.'),
        steps(('Kéo khối mở đầu từ nhóm <b>Sự kiện</b> (màu vàng) vào vùng ghép khối.', sblocks('khi bấm cờ xanh', hl=(0,))),
              ('Kéo khối <b>tiến 50 bước</b> (nhóm Chuyển động, màu xanh dương) và thả sát dưới khối vàng cho chúng dính vào nhau.', sblocks('khi bấm cờ xanh\n  tiến 50 bước', hl=(1,))),
              ('Kéo khối <b>nói … trong 2 giây</b> (nhóm Ngoại hình, màu tím) xuống dưới cùng, sửa chữ thành “Xin chào!”.', sblocks('khi bấm cờ xanh\n  tiến 50 bước\n  nói "Xin chào!" trong 2 giây', hl=(2,))),
              ('Bấm <b>cờ xanh</b> trên sân khấu. Nếu mèo đi tới và nói, chương trình đã đúng.', '<p class="tnote">Không thấy gì? Kiểm tra các khối đã <b>dính liền</b> nhau chưa.</p>')),
        [err('Thiếu bước', 'Viết “nấu mì rồi ăn” – người máy không biết phải đun nước, cho mì vào nồi…', 'Chia nhỏ: đun nước → cho mì → đợi 3 phút → tắt bếp → cho ra tô.'),
         err('Bước mơ hồ', '“Đi một chút” là bao nhiêu? Người máy không biết.', 'Nói rõ con số: “đi 5 bước”, “đợi 3 phút”.'),
         err('Sai thứ tự', 'Cho gia vị vào tô <b>trước</b> khi có mì thì mì sẽ không được trộn gia vị.', 'Đọc lại từng bước và hỏi “bước này cần gì có sẵn trước đó?”.'),
         err('Quên khối bắt đầu', 'Chỉ có khối “tiến 50 bước” nằm một mình: bấm cờ xanh nhưng mèo đứng yên.', 'Luôn đặt khối vàng “khi bấm cờ xanh” ở trên cùng.')],
        [eg('Ví dụ 1: pha mì tôm', flowrow(['Đun sôi|nước', 'Cho mì|vào nồi', 'Đợi|3 phút', 'Tắt bếp', 'Cho ra tô|thêm gia vị']) + note('Năm bước, bước sau cần bước trước làm xong. Đảo “tắt bếp” lên trước “đợi 3 phút” là sai.')),
         eg('Ví dụ 2: hướng dẫn người máy đi trong sân', li(['Người máy đứng ở góc sân, mặt hướng lên trên.', '<b>Tiến 3 bước → quay phải → tiến 2 bước.</b>', 'Kết quả: người máy ở cách góc 2 bước sang phải và 3 bước lên trên.']))],
        [('Dãy bước <b>“đánh răng”</b> dưới đây thiếu 2 bước. Tìm chúng: 1) Cầm bàn chải. 2) Đánh răng 2 phút. 3) Nhổ bọt. 4) Cất bàn chải.',
          '<p>Thiếu <b>bóp kem đánh răng</b> (trước khi đánh) và <b>súc miệng</b> (sau khi nhổ bọt). Bạn nào thêm “mở nước”, “lau miệng” cũng đúng.</p>', None),
         ('Sắp xếp lại cho đúng thứ tự: <i>buộc dây giày – đi tất – xỏ chân vào giày – lấy giày ra khỏi tủ</i>.', '<p>Đúng: <b>lấy giày ra khỏi tủ → đi tất → xỏ chân vào giày → buộc dây giày</b>. Bước nào cần trước? Tất phải đi trước khi xỏ giày.</p>', None),
         ('Người máy đứng ở một điểm, mặt hướng lên trên. Chạy dãy lệnh: <b>tiến 3, quay phải 90°, tiến 2, quay trái 90°, tiến 1</b>. Em đặt điểm đứng đầu là (0, 0), sang phải là x tăng, lên trên là y tăng. Người máy dừng ở đâu và mặt hướng nào?',
          '<p>Tiến 3 → (0, 3). Quay phải: mặt sang phải. Tiến 2 → (2, 3). Quay trái: mặt lại lên trên. Tiến 1 → <b>(2, 4)</b>, mặt hướng <b>lên trên</b>.</p>' + note('Em vẽ ra giấy theo từng lệnh để kiểm tra nhé.'), None),
         ('<b>Nghĩ ngược:</b> người máy đang ở (2, 4), mặt hướng lên trên. Viết dãy lệnh đưa nó <b>về lại (0, 0)</b> bằng cách làm ngược lại các bước ở T3 (được dùng lệnh “lùi”).',
          '<p>Đảo thứ tự và đổi từng lệnh: <b>lùi 1, quay phải 90°, lùi 2, quay trái 90°, lùi 3</b>.</p><p>Kiểm tra: lùi 1 → (2, 3); quay phải; lùi 2 → (0, 3); quay trái; lùi 3 → <b>(0, 0)</b>, mặt lên trên. Đúng!</p>' + note('“Quay phải” của lúc đi xuôi trở thành “quay phải” hay “quay trái” khi làm ngược? Ở đây vì đã đảo cả thứ tự nên mỗi cú quay đảo chiều: quay trái lúc xuôi → quay phải lúc ngược.'), None),
         ('<b>Thử thách:</b> ba bạn viết cách pha nước chanh. <i>An:</i> vắt chanh – cho đường – rót nước. <i>Bình:</i> rót nước vào cốc – cho đường – khuấy – vắt chanh – khuấy. <i>Chi:</i> pha nước chanh. Bản nào “người máy” làm được? Bản nào tốt nhất? Rồi tự viết bản của em có ít nhất 6 bước.',
          '<p><b>Chi</b> không dùng được (không có bước nào). <b>An</b> thiếu cốc, nước chưa có chỗ chứa và không khuấy. <b>Bình</b> rõ ràng và đúng thứ tự nhất.</p><p>Bản của em ví dụ: 1) lấy cốc; 2) vắt nửa quả chanh vào cốc; 3) cho 2 thìa đường; 4) rót 200 ml nước; 5) khuấy 10 vòng; 6) nếm thử và thêm đường nếu cần.</p>', None)],
        'Scratch')

    # ---------------- Bài 2 ----------------
    sq = [('f', 100), ('r', 90)] * 4
    K['bai2'] = std('Bài 2 · Dãy lệnh & bắt lỗi', 'Thứ tự lệnh quyết định kết quả.',
        ('Vẽ được hình vuông bằng khối lệnh; hiểu thứ tự lệnh làm thay đổi kết quả; biết sửa chương trình sai', 'Scratch; thêm phần mở rộng “Bút vẽ” (nút xanh ở góc dưới bên trái)', 'Chương trình vẽ hình vuông và chữ L'),
        ['Một dãy lệnh đúng cho ra hình đúng; <b>sai một lệnh là hình sai</b>.', 'Em học cách <b>đoán trước</b> máy sẽ vẽ gì và <b>sửa lỗi</b> khi hình không như ý.', 'Đây là nền tảng để vẽ mọi hình sau này.'],
        ol(['Vẽ hình ra giấy, đếm số cạnh và góc.', 'Viết dãy: hạ bút → (tiến, quay) cho từng cạnh.', 'Ghép khối, bấm cờ xanh, so với hình trên giấy.', 'Lệch chỗ nào thì sửa đúng chỗ đó rồi thử lại.']),
        think(['<b>Phản biện:</b> “Hình có khép kín không? Các cạnh có bằng nhau không?” Đừng chỉ nhìn thoáng qua.', '<b>Ngược:</b> nhân vật muốn về đúng chỗ xuất phát thì tổng các lần quay phải là <b>một vòng 360°</b>. Hình vuông: 4 × 90° = 360°.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['<b>Hạ bút</b> làm nhân vật vẽ khi di chuyển; <b>nhấc bút</b> thì không vẽ.', '<b>Tiến n bước</b> vẽ một cạnh; <b>quay phải d độ</b> chuẩn bị cho cạnh sau.']) + sblocks('khi bấm cờ xanh\n  hạ bút\n  tiến 100 bước\n  quay phải 90 độ\n  tiến 100 bước\n  quay phải 90 độ\n  tiến 100 bước\n  quay phải 90 độ\n  tiến 100 bước\n  quay phải 90 độ'),
        steps(*[('Cạnh thứ %d xong.' % (k + 1), sblocks('hạ bút\ntiến 100 bước\nquay phải 90 độ', hl=(1, 2)) + turtle_svg(sq[:2 * (k + 1)] if k < 3 else sq)) for k in range(4)]),
        [err('Hạ bút sau khi đã đi', 'Cạnh đầu tiên đi lúc chưa hạ bút nên <b>không được vẽ</b>.', 'Đặt “hạ bút” ngay dưới khối “khi bấm cờ xanh”.'),
         err('Quên một lần quay hoặc một cạnh', 'Hình chỉ có 3 cạnh, giống chữ U hoặc chữ L.', 'Đếm: hình vuông cần 4 lần “tiến” và 4 lần “quay”.'),
         err('Góc quay sai', 'Quay 80° thay vì 90° khiến hình không khép kín.', 'Kiểm tra tổng góc: cần 360° sau khi vẽ xong.'),
         err('Chạy hai lần liền, hình chồng lên nhau', 'Bấm cờ xanh nhiều lần, nhân vật không về chỗ cũ nên vẽ nhiều hình.', 'Thêm khối “xóa hết” và “đến x: 0 y: 0” ở đầu chương trình.')],
        [eg('Ví dụ 1: hình chữ nhật 100 × 50', sblocks('hạ bút\ntiến 100 bước\nquay phải 90 độ\ntiến 50 bước\nquay phải 90 độ\ntiến 100 bước\nquay phải 90 độ\ntiến 50 bước\nquay phải 90 độ') + turtle_svg([('f', 100), ('r', 90), ('f', 50), ('r', 90)] * 2)),
         eg('Ví dụ 2: chữ L', sblocks('hạ bút\ntiến 100 bước\nquay phải 90 độ\ntiến 50 bước') + turtle_svg([('f', 100), ('r', 90), ('f', 50)]) + note('Chữ L chỉ cần 2 cạnh và 1 lần quay, không cần khép kín.'))],
        [('Viết chương trình vẽ <b>hình vuông cạnh 60</b>.', '<p>Dùng bản mẫu ở thẻ 4, đổi mọi “tiến 100 bước” thành <b>tiến 60 bước</b>.</p>' + sblocks('hạ bút\ntiến 60 bước\nquay phải 90 độ\ntiến 60 bước\nquay phải 90 độ\ntiến 60 bước\nquay phải 90 độ\ntiến 60 bước\nquay phải 90 độ'), None),
         ('Chương trình dưới muốn vẽ hình vuông cạnh 80 nhưng chỉ ra hình chữ U. Tìm lỗi và sửa.' + sblocks('hạ bút\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước'),
          '<p>Chỉ có <b>3 cạnh</b>: thiếu một lần quay và một lần tiến cuối. Thêm <i>quay phải 90 độ</i> và <i>tiến 80 bước</i>. Kiểm tra: 4 lần quay × 90° = 360° ✓.</p>' + turtle_svg(sq[:5]) + note('Hình trên là hình chương trình sai vẽ ra.'), None),
         ('Viết chương trình vẽ <b>hình chữ nhật dài 120, rộng 60</b>. Kiểm tra tổng góc quay.', '<p>Hai cạnh dài 120, hai cạnh ngắn 60, mỗi góc 90°.</p>' + sblocks('hạ bút\ntiến 120 bước\nquay phải 90 độ\ntiến 60 bước\nquay phải 90 độ\ntiến 120 bước\nquay phải 90 độ\ntiến 60 bước\nquay phải 90 độ') + note('Tổng góc quay: 4 × 90° = 360° ✓.'), None),
         ('Vẽ <b>cầu thang 3 bậc</b>: mỗi bậc đi lên 40 rồi sang phải 40. Hãy viết dãy lệnh, biết nhân vật bắt đầu hướng sang phải.',
          '<p>Mỗi bậc: <i>quay trái 90 độ, tiến 40, quay phải 90 độ, tiến 40</i>. Lặp 3 lần (viết đủ 12 khối).</p>' + sblocks('hạ bút\nquay trái 90 độ\ntiến 40 bước\nquay phải 90 độ\ntiến 40 bước\nquay trái 90 độ\ntiến 40 bước\nquay phải 90 độ\ntiến 40 bước\nquay trái 90 độ\ntiến 40 bước\nquay phải 90 độ\ntiến 40 bước') + note('Lưu ý: thứ tự “quay – tiến – quay – tiến” lặp lại. Bài sau em sẽ học khối lặp để viết gọn.'), None),
         ('<b>Thử thách:</b> một chương trình lặp “tiến 50, quay phải 90” đúng <b>6 lần</b>, nhân vật bắt đầu mặt hướng lên trên ở (0, 0). Cuối cùng nhân vật ở đâu? Giải thích bằng cách nghĩ ngược về tổng góc quay.',
          '<p>Sau 4 lần, nhân vật về lại (0, 0), mặt lên trên (4 × 90° = 360°). Hai lần còn lại: lên 50 → (0, 50); sang phải 50 → <b>(50, 50)</b>.</p><p>Cách nhanh: chỉ cần tính <b>6 − 4 = 2</b> lần dư.</p>', None)],
        'Scratch')
    assert sim([('f', 50), ('r', 90)] * 6)[:2] == (50, 50)

    # ---------------- Bài 3 ----------------
    K['bai3'] = std('Bài 3 · Lặp lại cho gọn', 'Một khối “lặp” thay cho cả chục khối chép đi chép lại.',
        ('Dùng khối lặp vẽ hình vuông, tam giác, ngũ giác, ngôi sao; tính được góc quay bằng công thức 360 ÷ số cạnh', 'Scratch + phần mở rộng “Bút vẽ”', 'Chương trình vẽ nhiều hình bằng khối lặp'),
        ['Máy tính giỏi nhất ở việc <b>làm một việc lặp đi lặp lại</b> mà không mệt.', 'Khối lặp giúp chương trình <b>ngắn hơn, dễ đọc, dễ sửa</b>: muốn đổi số cạnh chỉ sửa một con số.', 'Em học cách <b>nhận ra quy luật lặp</b> trong mọi việc.'],
        ol(['Nhìn chương trình dài: có <b>nhóm khối nào lặp lại</b> không?', 'Đếm nhóm đó lặp mấy lần.', 'Bọc nhóm khối vào khối <b>lặp n lần</b>.', 'Chạy lại, so kết quả với bản dài: phải giống hệt.']),
        think(['<b>Tìm quy luật:</b> “Cái gì lặp lại? Cái gì thay đổi?”', '<b>Nghĩ ngược:</b> biết mỗi lần quay bao nhiêu độ, tính ngược ra số cạnh: 360 ÷ góc.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['Khối <b>lặp 4 lần</b> (nhóm Điều khiển, màu cam) bọc các khối bên trong.', 'Hình có <b>n cạnh đều</b> thì mỗi lần quay <b>360 ÷ n</b> độ.', 'Tam giác đều: 360 ÷ 3 = <b>120°</b>; ngũ giác: 360 ÷ 5 = <b>72°</b>; lục giác: 360 ÷ 6 = <b>60°</b>.']) + sblocks('khi bấm cờ xanh\n  hạ bút\n  lặp 4 lần\n    tiến 100 bước\n    quay phải 90 độ'),
        steps(('Bản dài: đoạn <b>tiến 100 – quay 90</b> bị chép 4 lần. Đây là dấu hiệu cần lặp.', sblocks('tiến 100 bước\nquay phải 90 độ\ntiến 100 bước\nquay phải 90 độ\ntiến 100 bước\nquay phải 90 độ\ntiến 100 bước\nquay phải 90 độ', hl=(0, 1))),
              ('Bọc đoạn lặp vào khối <b>lặp 4 lần</b>, chỉ giữ lại một bản của đoạn đó.', sblocks('lặp 4 lần\n  tiến 100 bước\n  quay phải 90 độ', hl=(0,))),
              ('Kết quả giống hệt bản dài: hình vuông.', turtle_svg(sq)),
              ('Đổi số: lặp <b>3</b> lần, quay <b>120°</b> được tam giác đều.', sblocks('lặp 3 lần\n  tiến 100 bước\n  quay phải 120 độ', hl=(0, 2)) + turtle_svg([('f', 100), ('r', 120)] * 3))),
        [err('Đếm sai số lần lặp', 'Lặp 3 lần với góc 90° chỉ ra 3 cạnh – hình chưa khép.', 'Số lần lặp = số cạnh của hình.'),
         err('Góc không bằng 360 ÷ n', 'Ngũ giác mà quay 90° thì thành hình xoắn lạ.', 'Tính góc: 360 ÷ 5 = 72°.'),
         err('Đặt “hạ bút” trong khối lặp', 'Không sai nhưng làm thừa, mỗi vòng đều hạ bút lại.', 'Hạ bút một lần ở trước khối lặp.'),
         err('Để “quay” bên ngoài khối lặp', 'Chỉ có “tiến” lặp nên nhân vật đi thẳng một đường dài.', 'Cả “tiến” và “quay” phải nằm <b>bên trong</b> khối lặp.')],
        [eg('Ví dụ 1: lục giác', sblocks('lặp 6 lần\n  tiến 60 bước\n  quay phải 60 độ') + turtle_svg([('f', 60), ('r', 60)] * 6)),
         eg('Ví dụ 2: ngôi sao 5 cánh', sblocks('lặp 5 lần\n  tiến 100 bước\n  quay phải 144 độ') + turtle_svg([('f', 100), ('r', 144)] * 5) + note('Ngôi sao quay 144° (= 2 × 72°) mỗi lần: nhân vật đi qua hai đỉnh của ngũ giác rồi mới quay.'))],
        [('Dùng khối lặp viết lại chương trình vẽ hình vuông cạnh 80.', '<p>' + sblocks('hạ bút\nlặp 4 lần\n  tiến 80 bước\n  quay phải 90 độ') + '</p>', None),
         ('Điền bảng: hình có số cạnh đều dưới đây thì mỗi lần quay bao nhiêu độ? Tam giác (3), hình vuông (4), ngũ giác (5), lục giác (6), bát giác (8), thập giác (10).',
          '<p>' + ' · '.join('%d cạnh: <b>%d°</b>' % (n, 360 // n) for n in (3, 4, 5, 6, 8, 10)) + '.</p>', None),
         ('Vẽ <b>hình bát giác đều</b> cạnh 40 bằng khối lặp. Em tự tính góc quay.', '<p>360 ÷ 8 = 45°.</p>' + sblocks('hạ bút\nlặp 8 lần\n  tiến 40 bước\n  quay phải 45 độ') + turtle_svg([('f', 40), ('r', 45)] * 8), None),
         ('<b>Nghĩ ngược:</b> một chương trình quay <b>24°</b> mỗi lần và vẽ được hình khép kín. Phải lặp bao nhiêu lần? Và khối lặp bên ngoài “bông hoa” sau cần mấy lần: <i>lặp ? lần { lặp 4 lần {tiến 50, quay phải 90}; quay phải 30 }</i>?',
          '<p>360 ÷ 24 = <b>15</b> lần. Bông hoa vuông: mỗi lần xoay thêm 30°, phải xoay đủ 360° nên 360 ÷ 30 = <b>12</b> lần.</p>' + sblocks('hạ bút\nlặp 12 lần\n  lặp 4 lần\n    tiến 50 bước\n    quay phải 90 độ\n  quay phải 30 độ'), None),
         ('<b>Thử thách:</b> ngôi sao 5 cánh dùng góc quay 144°. Vì sao 144? Hãy kiểm tra: lặp 5 lần, tổng góc quay là bao nhiêu độ, tức là nhân vật quay bao nhiêu vòng đầy đủ?',
          '<p>5 × 144° = <b>720°</b> = <b>2 vòng</b> đầy đủ. Nhân vật phải quay một số nguyên vòng mới về đúng chỗ xuất phát. Với 1 vòng là 360°: 360 ÷ 5 = 72° ra ngũ giác; với 2 vòng: 720 ÷ 5 = 144° ra ngôi sao.</p>' + note('Em thử góc 216° (= 3 vòng ÷ 5) trong Scratch xem hình có gì lạ!'), None)],
        'Scratch')
    assert (5 * 144) % 360 == 0 and 360 // 24 == 15

    # ---------------- Bài 4 ----------------
    prog4 = [('đặt điểm = 5', lambda s: s.update(điểm=5)), ('thêm 3 vào điểm', lambda s: s.update(điểm=s['điểm'] + 3)),
             ('đặt điểm = điểm × 2', lambda s: s.update(điểm=s['điểm'] * 2)), ('thêm -4 vào điểm', lambda s: s.update(điểm=s['điểm'] - 4))]
    assert (5 + 3) * 2 - 4 == 12
    prog4b = [('đặt a = 3', lambda s: s.update(a=3)), ('đặt b = 8', lambda s: s.update(b=8)), ('đặt t = a', lambda s: s.update(t=s['a'])),
              ('đặt a = b', lambda s: s.update(a=s['b'])), ('đặt b = t', lambda s: s.update(b=s['t']))]
    K['bai4'] = std('Bài 4 · Biến – chiếc hộp nhớ', 'Biến giúp chương trình nhớ số và thay đổi nó.',
        ('Hiểu biến như chiếc hộp có tên; theo dõi giá trị biến sau từng khối', 'Giấy bút; Scratch (nhóm khối Biến, màu cam đậm)', 'Bảng theo dõi giá trị biến và trò chơi có điểm'),
        ['<b>Biến</b> là chiếc hộp có <b>tên</b> chứa một giá trị, ví dụ <b>điểm</b>, <b>mạng</b>, <b>thời gian</b>.', 'Không có biến, trò chơi không nhớ được điểm của em.', 'Biến cho phép chương trình <b>thay đổi theo thời gian</b>.'],
        ol(['Hỏi: chương trình cần <b>nhớ</b> con số nào?', '<b>Đặt tên</b> rõ nghĩa (điểm, mạng…).', '<b>Đặt giá trị đầu</b> (đặt điểm = 0) ở đầu chương trình.', '<b>Cập nhật</b> khi có chuyện xảy ra (thêm 1 vào điểm).']),
        think(['<b>Phản biện:</b> “Sau mỗi khối, giá trị biến bây giờ là bao nhiêu?” Lập bảng theo dõi, đừng đoán.', '<b>Ngược:</b> biết kết quả cuối, suy ngược xem giá trị đầu là bao nhiêu.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['Vào nhóm <b>Biến</b> → bấm <b>Tạo một biến</b> → đặt tên “điểm”.', '<b>đặt điểm = 0</b>: ghi giá trị mới. <b>thêm 1 vào điểm</b>: cộng thêm.']) + sblocks('khi bấm cờ xanh\n  đặt điểm = 0\n  lặp liên tục\n    nếu chạm ngôi sao thì\n      thêm 1 vào điểm'),
        vsteps(prog4) + '<p class="tnote">Chương trình: đặt 5 → thêm 3 → nhân 2 → thêm −4. Biến đổi giá trị theo từng khối: 5 → 8 → 16 → 12.</p>',
        [err('Quên đặt giá trị đầu', 'Ván sau điểm cộng dồn từ ván trước vì biến còn nhớ giá trị cũ.', 'Luôn <b>đặt điểm = 0</b> ngay dưới khối “khi bấm cờ xanh”.'),
         err('Nhầm “đặt” và “thêm”', 'Dùng “đặt điểm = 1” mỗi lần chạm sao thì điểm mãi là 1.', 'Muốn cộng dồn dùng “thêm 1 vào điểm”.'),
         err('Cập nhật nhầm biến', 'Có hai biến “điểm” và “mạng”, em lại trừ vào “điểm”.', 'Đọc tên biến trong khối trước khi thả.'),
         err('Đặt tên khó hiểu', 'Biến tên “a1”, “x2” khiến sau vài ngày em không nhớ nó là gì.', 'Đặt tên có nghĩa: điểm, mạng, thời_gian.')],
        [eg('Ví dụ 1: đếm bước chân', sblocks('đặt bước = 0\nlặp 10 lần\n  tiến 10 bước\n  thêm 1 vào bước\nnói bước') + note('Sau vòng lặp, biến <b>bước</b> bằng 10.')),
         eg('Ví dụ 2: 3 mạng', sblocks('đặt mạng = 3\nnếu chạm quái thì\n  thêm -1 vào mạng') + note('Mỗi lần chạm quái trừ 1 mạng; mạng bằng 0 thì hết trò chơi.'))],
        [('Biến <b>s</b> bắt đầu bằng 0. Chương trình: <i>lặp 5 lần { thêm 2 vào s }</i>. Cuối cùng s bằng bao nhiêu?', '<p>Mỗi vòng cộng 2, 5 vòng: 2 × 5 = <b>10</b>.</p>', None),
         ('Lập bảng theo dõi: <i>đặt điểm = 5, thêm 3 vào điểm, đặt điểm = điểm × 2, thêm −4 vào điểm</i>.', '<p>5 → <b>8</b> → <b>16</b> → <b>12</b>. Cuối cùng điểm = <b>12</b>.</p>', None),
         ('<i>đặt điểm = 0; lặp 4 lần { thêm 3 vào điểm }; đặt điểm = điểm × 2; thêm −5 vào điểm</i>. Điểm cuối cùng là bao nhiêu?', '<p>Sau vòng lặp: 4 × 3 = 12. Nhân 2: 24. Trừ 5: <b>19</b>.</p>', None),
         ('<b>Nghĩ ngược:</b> <i>đặt a = ?; thêm 4 vào a; đặt a = a × 3; thêm −2 vào a</i>, cuối cùng a = 25. Giá trị ban đầu là bao nhiêu?', '<p>Đi ngược: 25 + 2 = 27; 27 ÷ 3 = 9; 9 − 4 = <b>5</b>. Kiểm tra xuôi: 5 + 4 = 9; 9 × 3 = 27; 27 − 2 = 25 ✓.</p>', None),
         ('<b>Thử thách – đổi chỗ hai biến:</b> a = 3, b = 8. Dùng thêm biến t để đổi chỗ để a = 8 và b = 3. Giải thích vì sao <i>đặt a = b; đặt b = a</i> sai.',
          '<p>Cách đúng: <i>đặt t = a; đặt a = b; đặt b = t</i>.</p>' + vsteps(prog4b) + '<p>Cách sai: sau <i>đặt a = b</i>, a đã thành 8 – giá trị 3 bị mất; rồi <i>đặt b = a</i> cũng ra 8. Hai biến cùng bằng 8.</p>', None)],
        'Scratch')

    # ---------------- Bài 5 ----------------
    K['bai5'] = std('Bài 5 · Nếu… thì…', 'Cho chương trình biết cách chọn.',
        ('Dùng khối “nếu – thì – nếu không” để chương trình tự chọn; biết thử cả giá trị ở ranh giới', 'Scratch (nhóm Điều khiển và nhóm Phép toán)', 'Chương trình phân loại điểm có nhiều mức'),
        ['Đời thường ta chọn việc theo hoàn cảnh: “nếu trời mưa thì mang ô”.', 'Khối <b>nếu</b> giúp chương trình <b>tự chọn</b> việc làm theo điều kiện.', 'Trò chơi, ứng dụng nào cũng dùng nó để phản ứng với người chơi.'],
        ol(['Viết điều kiện bằng lời: “nếu … thì …”.', 'Đổi điều kiện thành phép so sánh (&gt;, &lt;, =).', 'Quyết định việc làm khi <b>đúng</b> và khi <b>sai</b>.', '<b>Thử cả ranh giới:</b> giá trị sát điểm đổi hướng.']),
        think(['<b>Phản biện:</b> thử mỗi nhánh ít nhất một lần, đặc biệt các giá trị sát ranh giới như 5, 8.', '<b>Ngược:</b> muốn nhân vật nói “Giỏi” thì điểm phải thế nào? Từ kết quả, suy ra điều kiện.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['<b>nếu … thì … nếu không …</b> có hai nhánh.', 'Muốn nhiều mức, đặt <b>nếu</b> trong <b>nếu không</b>.', 'Điều kiện đặt trong ô hình lục giác lấy từ nhóm Phép toán: <b>điểm ≥ 5</b>.']) + sblocks('nếu điểm ≥ 8 thì\n  nói "Giỏi"\nnếu không\n  nếu điểm ≥ 5 thì\n    nói "Khá"\n  nếu không\n    nói "Cố lên"'),
        steps(('Sơ đồ rẽ nhánh với điều kiện <b>điểm ≥ 5</b>.', decision_svg('điểm ≥ 5 ?', 'nói “Đạt”', 'nói “Cố lên”')),
              ('Thử <b>điểm 9</b>: 9 ≥ 8 đúng → nói “Giỏi”.', sblocks('nếu điểm ≥ 8 thì\n  nói "Giỏi"\nnếu không\n  nếu điểm ≥ 5 thì\n    nói "Khá"\n  nếu không\n    nói "Cố lên"', hl=(0, 1))),
              ('Thử <b>điểm 5</b> (sát ranh giới): 5 ≥ 8 sai; 5 ≥ 5 đúng → nói “Khá”.', sblocks('nếu điểm ≥ 8 thì\n  nói "Giỏi"\nnếu không\n  nếu điểm ≥ 5 thì\n    nói "Khá"\n  nếu không\n    nói "Cố lên"', hl=(2, 3, 4))),
              ('Thử <b>điểm 4</b>: cả hai điều kiện đều sai → nói “Cố lên”.', sblocks('nếu điểm ≥ 8 thì\n  nói "Giỏi"\nnếu không\n  nếu điểm ≥ 5 thì\n    nói "Khá"\n  nếu không\n    nói "Cố lên"', hl=(2, 5, 6)))),
        [err('Dùng &gt; thay cho ≥', 'Điểm 5 “Cố lên” trong khi bạn mong “Đạt”.', 'Hỏi: số ở ranh giới thuộc nhóm nào? Chọn ≥ hoặc &gt; cho đúng.'),
         err('Quên “nếu không”', 'Khi điều kiện sai thì chương trình không làm gì cả.', 'Thêm nhánh “nếu không” cho trường hợp còn lại.'),
         err('Kiểm tra sai thứ tự', 'Kiểm tra “điểm ≥ 5” trước “điểm ≥ 8” thì điểm 9 cũng bị xếp “Khá”.', 'Kiểm tra mức <b>cao nhất</b> trước, thấp dần xuống.'),
         err('Điều kiện không bao hết trường hợp', 'Chỉ viết “nếu điểm &lt; 5” và “nếu điểm &gt; 5” thì điểm 5 không có nhánh nào.', 'Dùng ≥ hoặc ≤ ở một phía để không bỏ sót.')],
        [eg('Ví dụ 1: phân loại điểm 3 mức', sblocks('nếu điểm ≥ 8 thì\n  nói "Giỏi"\nnếu không\n  nếu điểm ≥ 5 thì\n    nói "Khá"\n  nếu không\n    nói "Cố lên"') + note('Điểm 8 → Giỏi, 7 → Khá, 5 → Khá, 4 → Cố lên.')),
         eg('Ví dụ 2: cổng vào trò chơi', sblocks('nếu tuổi ≥ 8 thì\n  nói "Mời em vào!"\nnếu không\n  nói "Em cần lớn thêm một chút."') + note('Tuổi 8 được vào (≥), tuổi 7 không.'))],
        [('Chương trình: <i>nếu điểm ≥ 8 → Giỏi; nếu không, nếu điểm ≥ 5 → Khá; nếu không → Cố lên</i>. Điểm 8, 7, 5, 4 thì nói gì?', '<p>' + ', '.join('điểm %d: <b>%s</b>' % (d, 'Giỏi' if d >= 8 else 'Khá' if d >= 5 else 'Cố lên') for d in (8, 7, 5, 4)) + '. Chú ý điểm 8 và 5 nằm đúng ranh giới.</p>', None),
         ('Viết khối để nhân vật nói “Chạm rồi!” khi <b>chạm</b> vào ngôi sao, nếu không thì nói “Chưa chạm”.', '<p>' + sblocks('nếu chạm ngôi sao thì\n  nói "Chạm rồi!"\nnếu không\n  nói "Chưa chạm"') + '</p>', None),
         ('Tìm lỗi: ' + sblocks('nếu điểm ≥ 5 thì\n  nói "Khá"\nnếu không\n  nếu điểm ≥ 8 thì\n    nói "Giỏi"') + 'Điểm 9 nói gì? Sửa thế nào?', '<p>9 ≥ 5 đúng nên nói “Khá” – sai ý muốn. Sửa: kiểm tra <b>≥ 8 trước</b>, rồi mới tới ≥ 5.</p>', None),
         ('<b>Nghĩ ngược:</b> muốn bảng điểm có 4 mức: Xuất sắc (≥ 9), Giỏi (≥ 8), Khá (≥ 5), Cố lên. Cần mấy khối “nếu”? Viết ra, rồi cho biết điểm 9, 8,5, 6, 3 được mức nào.', '<p>Cần <b>3 khối “nếu”</b> lồng nhau (số mức − 1).</p>' + sblocks('nếu điểm ≥ 9 thì\n  nói "Xuất sắc"\nnếu không\n  nếu điểm ≥ 8 thì\n    nói "Giỏi"\n  nếu không\n    nếu điểm ≥ 5 thì\n      nói "Khá"\n    nếu không\n      nói "Cố lên"') + '<p>9 → Xuất sắc; 8,5 → Giỏi; 6 → Khá; 3 → Cố lên.</p>', None),
         ('<b>Thử thách:</b> vé tham quan: dưới 6 tuổi miễn phí; từ 6 đến 11 tuổi 20 000 đ; từ 12 tuổi trở lên 40 000 đ. Nhóm 4 bạn tuổi 5, 6, 11, 12 phải trả bao nhiêu? Viết điều kiện cho biến <b>tuổi</b> và <b>giá</b>.',
          '<p>' + sblocks('nếu tuổi < 6 thì\n  đặt giá = 0\nnếu không\n  nếu tuổi < 12 thì\n    đặt giá = 20000\n  nếu không\n    đặt giá = 40000') + '</p><p>5 tuổi: 0; 6 tuổi: 20 000; 11 tuổi: 20 000; 12 tuổi: 40 000. Tổng = <b>80 000 đ</b>. Chú ý ranh giới 6 và 12.</p>', None)],
        'Scratch')
    assert 0 + 20000 + 20000 + 40000 == 80000

    # ---------------- Bài 6 ----------------
    K['bai6'] = std('Bài 6 · Nghĩ ngược', 'Từ kết quả, lần ngược về lúc đầu.',
        ('Giải bài toán bằng cách đi ngược các bước; viết chương trình “đảo ngược”', 'Giấy bút; Scratch', 'Chương trình đoán số em đã nghĩ'),
        ['Có những bài biết <b>kết quả cuối</b> mà cần tìm <b>lúc đầu</b>.', 'Cách giải đẹp nhất là <b>đi ngược lại</b> từng bước.', 'Nghĩ ngược giúp em lập kế hoạch, tìm lỗi và giải câu đố nhanh hơn.'],
        ol(['Viết các bước <b>xuôi</b> theo thứ tự.', 'Với mỗi bước, tìm <b>phép ngược</b>: cộng ↔ trừ, nhân ↔ chia.', '<b>Đảo thứ tự</b> các bước.', 'Tính ngược từ kết quả, rồi <b>kiểm tra xuôi</b> xem có ra đúng kết quả không.']),
        think(['<b>Ngược:</b> “Muốn có kết quả này, trước đó cần có gì?”', '<b>Phản biện:</b> luôn thử lại bằng cách đi xuôi. Đáp án đúng phải ra đúng kết quả cho trước.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['Em có thể bắt Scratch giải ngược giúp: <b>hỏi</b> kết quả, rồi tính ngược bằng khối phép toán.']) + sblocks('hỏi "Kết quả em có là gì?" và đợi\nđặt kq = câu trả lời\nđặt số = (kq - 6) / 2\nnói số') + note('Câu đố: “nhân 2 rồi cộng 6 được kq”. Chương trình tính ngược: trừ 6 trước, rồi chia 2.'),
        reverse_svg(['× 2', '+ 6'], ['− 6', '÷ 2'], '7', '20', 'Nhân 2 rồi cộng 6: đi xuôi và đi ngược') + steps(
            ('Viết phép xuôi: <b>nhân 2</b>, rồi <b>cộng 6</b>, được 20.', '<p>? × 2 + 6 = 20</p>'),
            ('Đổi thành phép ngược và <b>đảo thứ tự</b>: trừ 6 trước, chia 2 sau.', '<p>20 − 6 = 14 → 14 ÷ 2 = <b>7</b></p>'),
            ('Kiểm tra xuôi: 7 × 2 = 14; 14 + 6 = 20 ✓.', '<p class="tnote">Đúng kết quả nên 7 chắc chắn là đáp án.</p>')),
        [err('Không đảo thứ tự', 'Chia 2 trước rồi trừ 6 cho ra số khác: (20 ÷ 2) − 6 = 4.', 'Bước làm sau cùng khi đi xuôi phải được làm <b>đầu tiên</b> khi đi ngược.'),
         err('Không đổi phép tính', 'Gặp “cộng 6” lại tiếp tục cộng 6.', 'Phép ngược của cộng là trừ, của nhân là chia.'),
         err('Quên kiểm tra xuôi', 'Tính nhầm mà không biết.', 'Luôn thay đáp án vào đề bài đi xuôi một lần.'),
         err('Chia ra số lẻ không hợp lý', 'Chia số kẹo cho ra 2,5 cái là vô lý.', 'Nếu đáp án vô lý, rà lại từng bước tính ngược.')],
        [eg('Ví dụ 1: số em đã nghĩ', '<p>Nghĩ một số, <b>nhân 3 rồi trừ 4</b> được 23. Ngược: 23 + 4 = 27; 27 ÷ 3 = <b>9</b>. Kiểm tra: 9 × 3 = 27; 27 − 4 = 23 ✓.</p>'),
         eg('Ví dụ 2: giờ dậy', '<p>Muốn đến trường lúc 7 giờ, đi mất 15 phút, chuẩn bị 30 phút. Ngược: 7 giờ − 15 phút = 6 giờ 45 (ra khỏi nhà); − 30 phút = <b>6 giờ 15</b> phải dậy.</p>')],
        [('Em nghĩ một số, <b>nhân 2 rồi cộng 6</b> được 30. Số đó là gì?', '<p>30 − 6 = 24; 24 ÷ 2 = <b>12</b>. Kiểm tra: 12 × 2 + 6 = 30 ✓.</p>', None),
         ('Em nghĩ một số, <b>trừ 5 rồi nhân 3</b> được 21. Số đó là gì?', '<p>21 ÷ 3 = 7; 7 + 5 = <b>12</b>. Kiểm tra: (12 − 5) × 3 = 21 ✓.</p>', None),
         ('Em nghĩ một số, <b>cộng 7, nhân 4, rồi trừ 10</b> được 54. Số đó là gì? Viết khối Scratch tính ngược.', '<p>54 + 10 = 64; 64 ÷ 4 = 16; 16 − 7 = <b>9</b>.</p>' + sblocks('hỏi "Kết quả?" và đợi\nđặt kq = câu trả lời\nđặt số = (kq + 10) / 4 - 7\nnói số') + '<p>Kiểm tra: (9 + 7) × 4 − 10 = 54 ✓.</p>', None),
         ('Em có một số kẹo. Cho bạn <b>một nửa</b>, rồi ăn thêm <b>1 cái</b>, còn <b>3 cái</b>. Lúc đầu có bao nhiêu kẹo?', '<p>Đi ngược: còn 3, trước khi ăn có 3 + 1 = 4; trước khi cho bạn một nửa có 4 × 2 = <b>8</b>. Kiểm tra: 8 → cho 4, còn 4 → ăn 1, còn 3 ✓.</p>', None),
         ('<b>Thử thách:</b> Lan có một số kẹo. Cho Mai <b>một nửa và thêm 1 cái</b>. Rồi cho Nam <b>một nửa số còn lại và thêm 1 cái</b>. Lan còn <b>2 cái</b>. Lúc đầu Lan có bao nhiêu?',
          '<p>Ngược từ cuối: sau Nam còn 2. Trước khi cho Nam, gọi là N: N − (N ÷ 2 + 1) = 2 → N ÷ 2 = 3 → <b>N = 6</b>. Trước khi cho Mai, gọi là M: M ÷ 2 − 1 = 6 → M ÷ 2 = 7 → <b>M = 14</b>.</p><p>Kiểm tra: 14 cho Mai 7 + 1 = 8, còn 6. Cho Nam 3 + 1 = 4, còn <b>2</b> ✓.</p>', None)],
        'Scratch')
    assert (30 - 6) // 2 == 12 and ((21 // 3) + 5) == 12 and ((54 + 10) // 4 - 7) == 9 and 14 - 8 == 6 and 6 - 4 == 2

    # ---------------- Bài 7 ----------------
    K['bai7'] = std('Bài 7 · Thám tử bắt lỗi', 'Gỡ lỗi (debug) là kỹ năng quan trọng nhất của người lập trình.',
        ('Tìm và sửa lỗi bằng cách quan sát, chia nhỏ, thử lại; biết thử nhiều trường hợp', 'Scratch; giấy bút để ghi “nhật ký bắt lỗi”', 'Nhật ký thám tử với 5 lỗi đã sửa'),
        ['Chương trình đầu tiên hầu như <b>luôn có lỗi</b> – điều đó rất bình thường.', 'Người giỏi không phải người không sai, mà là người <b>tìm ra lỗi nhanh</b>.', 'Kỹ năng bắt lỗi dùng được cả ngoài lập trình: làm toán, sửa đồ, viết văn.'],
        ol(['<b>Quan sát:</b> chương trình làm gì, khác ý em ở chỗ nào?', '<b>Đoán nguyên nhân</b> và chia nhỏ: chạy từng đoạn ngắn (bấm vào một cụm khối).', '<b>Sửa một chỗ</b> rồi chạy lại.', '<b>Ghi lại</b> lỗi đã gặp để lần sau không sai lại.']),
        think(['<b>Phản biện:</b> “Chương trình chạy không báo lỗi thì có đúng ý chưa?” Phải thử ít nhất 3 trường hợp: bình thường, sát ranh giới, bất thường.', '<b>Ngược:</b> từ kết quả sai, lần ngược về khối nào có thể gây ra nó.'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['<b>Bấm vào một cụm khối</b> để chạy riêng đoạn đó.', 'Dùng khối <b>nói (tên biến)</b> để xem giá trị biến giữa chừng.', 'Tắt bớt khối nghi ngờ (kéo ra) rồi chạy lại để so sánh.']) + sblocks('khi bấm cờ xanh\n  đặt điểm = 0\n  nói điểm trong 1 giây'),
        steps(('Quan sát: ý định là hình vuông nhưng máy vẽ <b>chữ U</b>.', turtle_svg(sq[:5])),
              ('Chia nhỏ: bấm từng khối, đếm. Chỉ có 3 lần “tiến” và 2 lần “quay”.', sblocks('hạ bút\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước', hl=(5,))),
              ('Sửa một chỗ: thêm “quay phải 90” và “tiến 80” ở cuối.', sblocks('hạ bút\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước\nquay phải 90 độ\ntiến 80 bước', hl=(6, 7))),
              ('Thử lại: hình vuông khép kín. Ghi vào nhật ký: “thiếu một cạnh”.', turtle_svg([('f', 80), ('r', 90)] * 4))),
        [err('Sửa nhiều chỗ cùng lúc', 'Không biết chỗ nào mới là lỗi thật.', 'Mỗi lần chỉ sửa một chỗ rồi chạy lại.'),
         err('Không thử lại sau khi sửa', 'Cứ tưởng đã đúng.', 'Chạy lại và so với kết quả mong muốn.'),
         err('Đổ lỗi cho máy', '“Máy hỏng rồi”. Hầu hết lỗi là do chương trình.', 'Giả sử máy luôn đúng, tìm lỗi trong khối lệnh của em.'),
         err('Chỉ thử một trường hợp', 'Chương trình đúng với điểm 9 nhưng sai với điểm 8.', 'Thử thêm giá trị ở ranh giới và giá trị lạ.')],
        [eg('Ví dụ 1: điểm không bắt đầu từ 0', sblocks('khi bấm cờ xanh\n  lặp liên tục\n    nếu chạm ngôi sao thì\n      thêm 1 vào điểm') + note('Lỗi: không có <b>đặt điểm = 0</b>. Ván sau điểm cộng dồn từ ván trước.')),
         eg('Ví dụ 2: hình không khép kín', sblocks('lặp 4 lần\n  tiến 100 bước\n  quay phải 80 độ') + turtle_svg([('f', 100), ('r', 80)] * 4) + note('Góc 80° thay vì 90° nên hình không về điểm xuất phát.'))],
        [('Chương trình vẽ hình vuông nhưng <b>không vẽ gì</b> lên sân khấu: ' + sblocks('lặp 4 lần\n  tiến 100 bước\n  quay phải 90 độ') + 'Thiếu gì?', '<p>Thiếu <b>hạ bút</b> (và phần mở rộng Bút vẽ). Thêm <i>hạ bút</i> trước khối lặp.</p>', None),
         ('Chương trình muốn vẽ hình vuông: ' + sblocks('hạ bút\nlặp 4 lần\n  tiến 100 bước\n  quay phải 80 độ') + 'Hình ra sao? Sửa thế nào?', '<p>Không khép kín vì quay 80° (4 × 80° = 320° chưa đủ 360°). Sửa thành <b>quay phải 90 độ</b>.</p>' + turtle_svg([('f', 100), ('r', 80)] * 4), None),
         ('Trò chơi: điểm ≥ 5 thì nói “Đạt”. Điểm đúng bằng 5 lại nói “Cố lên”. Chương trình: ' + sblocks('nếu điểm > 5 thì\n  nói "Đạt"\nnếu không\n  nói "Cố lên"') + 'Tìm lỗi.', '<p>Dùng <b>&gt;</b> nên điểm 5 sai nhánh. Sửa thành <b>điểm ≥ 5</b>. Lỗi nằm ở ranh giới, nên em phải thử điểm 5.</p>', None),
         ('Nhân vật nên đi 10 bước mỗi lần bấm phím, nhưng cứ <b>đi mãi không dừng</b>: ' + sblocks('khi bấm phím mũi tên phải\n  lặp liên tục\n    tiến 10 bước') + 'Tìm lỗi và sửa.', '<p>“Lặp liên tục” làm nhân vật đi mãi. Bỏ khối lặp liên tục, chỉ để <b>tiến 10 bước</b> cho mỗi lần bấm phím.</p>' + sblocks('khi bấm phím mũi tên phải\n  tiến 10 bước'), None),
         ('<b>Thử thách:</b> chương trình có <b>hai lỗi</b>: ' + sblocks('khi bấm cờ xanh\n  lặp liên tục\n    nếu chạm ngôi sao thì\n      thêm 1 vào điểm\n    nếu điểm = 10 thì\n      nói "Thắng!"') + 'Điểm không về 0 ở ván sau; và nếu điểm nhảy qua 10 trong một lần thì không bao giờ thắng. Sửa cả hai.',
          '<p>Lỗi 1: thiếu <b>đặt điểm = 0</b> ở đầu. Lỗi 2: dùng “=” nên chỉ thắng khi đúng 10; dùng <b>điểm ≥ 10</b> để chắc chắn.</p>' + sblocks('khi bấm cờ xanh\n  đặt điểm = 0\n  lặp liên tục\n    nếu chạm ngôi sao thì\n      thêm 1 vào điểm\n    nếu điểm ≥ 10 thì\n      nói "Thắng!"\n      dừng tất cả'), None)],
        'Scratch')

    # ---------------- Bài 8 ----------------
    K['bai8'] = std('Bài 8 · Dự án: trò chơi bắt sao', 'Tự lập kế hoạch ngược và làm trọn một sản phẩm.',
        ('Hoàn thành một trò chơi nhỏ dùng đủ lặp, biến, điều kiện; lập kế hoạch bằng cách nghĩ ngược', 'Scratch; giấy bút', 'Trò chơi bắt sao của riêng em và bản kế hoạch kiểm thử'),
        ['Ghép các kỹ năng đã học thành một sản phẩm hoàn chỉnh.', 'Em học cách <b>lập kế hoạch từ đích trở về</b> thay vì mò mẫm.', 'Có sản phẩm của riêng mình để khoe với bạn bè và gia đình.'],
        ol(['Viết <b>đích</b>: trò chơi trông thế nào khi hoàn thành?', '<b>Nghĩ ngược:</b> để có điều đó cần những phần nào?', 'Làm từng phần nhỏ, <b>thử ngay</b> sau mỗi phần.', 'Viết bảng kiểm thử và thử như một thám tử.']),
        think(['<b>Ngược:</b> Đích → cần điểm → cần biến điểm → cần “nếu chạm thì thêm 1”.', '<b>Phản biện:</b> nghĩ ra 5 cách người chơi có thể làm trò chơi hỏng (không chạm gì, chạm liên tục…).'], 'Hai thói quen của bài'),
        'Ứng dụng vào Scratch',
        li(['Nhân vật <b>Sao</b> nhảy đến chỗ ngẫu nhiên; người chơi bấm vào để ghi điểm.', 'Một nhân vật khác (hoặc phần nền) đếm giờ.']) + sblocks('(nhân vật Sao)\nkhi bấm cờ xanh\n  đặt điểm = 0\n  lặp 30 lần\n    đến vị trí ngẫu nhiên\n    chờ 1 giây') + sblocks('(cũng nhân vật Sao)\nkhi bấm vào nhân vật này\n  thêm 1 vào điểm'),
        steps(('Phần 1 – biến điểm: tạo biến và đặt về 0 khi bắt đầu.', sblocks('khi bấm cờ xanh\n  đặt điểm = 0', hl=(1,))),
              ('Phần 2 – sao di chuyển: lặp 30 lần, mỗi giây nhảy đến chỗ ngẫu nhiên.', sblocks('khi bấm cờ xanh\n  đặt điểm = 0\n  lặp 30 lần\n    đến vị trí ngẫu nhiên\n    chờ 1 giây', hl=(2, 3, 4))),
              ('Phần 3 – ghi điểm: bấm vào sao thì thêm 1 điểm.', sblocks('khi bấm vào nhân vật này\n  thêm 1 vào điểm', hl=(1,))),
              ('Phần 4 – kết thúc: hết 30 lần thì nói điểm cuối.', sblocks('khi bấm cờ xanh\n  đặt điểm = 0\n  lặp 30 lần\n    đến vị trí ngẫu nhiên\n    chờ 1 giây\n  nói điểm', hl=(5,)))),
        [err('Không đặt điểm = 0', 'Ván sau điểm cộng dồn.', 'Đặt giá trị đầu ngay khi bắt đầu.'),
         err('Làm hết rồi mới thử', 'Có lỗi mà không biết ở phần nào.', 'Làm xong mỗi phần là bấm cờ xanh thử ngay.'),
         err('Sao di chuyển quá nhanh', 'Không có khối chờ nên người chơi không kịp bấm.', 'Thêm “chờ 1 giây” (hoặc 0,8 giây cho khó hơn).'),
         err('Quên kết thúc trò chơi', 'Vòng lặp liên tục nên trò chơi không bao giờ dừng.', 'Dùng “lặp 30 lần” hoặc kiểm tra biến thời gian.')],
        [eg('Ví dụ 1: đố vui nhân', sblocks('đặt điểm = 0\nhỏi "3 × 4 = ?" và đợi\nnếu câu trả lời = 12 thì\n  thêm 1 vào điểm\n  nói "Đúng!"\nnếu không\n  nói "Sai rồi"') + note('Mỗi câu đúng được 1 điểm. Thêm nhiều câu bằng cách chép cụm hỏi.')),
         eg('Ví dụ 2: trò chơi tránh vật cản', sblocks('đặt mạng = 3\nlặp liên tục\n  nếu chạm vật cản thì\n    thêm -1 vào mạng\n    đến x: 0 y: 0\n  nếu mạng = 0 thì\n    nói "Hết mạng!"\n    dừng tất cả'))],
        [('Mỗi giây sao hiện một lần và em bấm trúng mọi lần. Ván 30 giây, sao thường 1 điểm. Điểm tối đa là bao nhiêu? Nếu cứ 5 giây có thêm một sao vàng 5 điểm thay cho sao thường ở giây đó thì sao?',
          '<p>Chỉ sao thường: <b>30 điểm</b>. Có sao vàng: 30 ÷ 5 = 6 giây có sao vàng → 6 × 5 = 30 điểm; 24 giây sao thường → 24 điểm; tổng <b>54 điểm</b>.</p>', None),
         ('Thêm <b>3 mạng</b>: mỗi lần bấm trượt (không trúng sao) mất 1 mạng. Viết các khối cần thêm.', '<p>' + sblocks('khi bấm cờ xanh\n  đặt mạng = 3\nkhi bấm vào nền\n  thêm -1 vào mạng\n  nếu mạng = 0 thì\n    nói "Hết mạng!"\n    dừng tất cả') + '</p>', None),
         ('Trò đố vui có 3 câu, mỗi câu đúng 2 điểm, sai trừ 1 điểm, bắt đầu từ 0. Em trả lời đúng, sai, đúng. Điểm cuối là bao nhiêu? Biến điểm có thể xuống dưới 0 không?', '<p>2 − 1 + 2 = <b>3</b>. Nếu sai hết 3 câu: −3, tức có thể âm; muốn không âm phải thêm điều kiện “nếu điểm &lt; 0 thì đặt điểm = 0”.</p>', None),
         ('<b>Nghĩ ngược – lập kế hoạch:</b> trò chơi “chạy né vật cản”: nhân vật nhảy qua vật cản bằng phím cách; chạm vật cản thì thua. Hãy viết kế hoạch từ đích về: cần những phần nào?', '<p>Đích: người chơi thắng nếu sống 30 giây. Ngược lại: cần <b>đếm giờ</b> → cần <b>kiểm tra chạm vật cản</b> → cần <b>vật cản chạy đến</b> → cần <b>nhân vật nhảy</b> khi bấm phím cách. Làm theo thứ tự ngược lại: nhảy → vật cản → chạm → giờ.</p>', None),
         ('<b>Thử thách:</b> viết <b>bảng kiểm thử</b> cho trò chơi bắt sao gồm 5 tình huống (ghi điều em làm và kết quả mong đợi). Ví dụ một hàng: “Không bấm gì suốt ván → điểm cuối bằng 0”.',
          '<p>Gợi ý: (1) Không bấm gì → điểm 0. (2) Bấm trúng cả 30 lần → điểm 30. (3) Bấm vào nền (trượt) → điểm không đổi. (4) Chơi 2 ván liền → ván 2 bắt đầu từ 0. (5) Bấm cực nhanh nhiều lần cùng một vị trí → mỗi lần sao đổi chỗ chỉ được 1 điểm (nếu máy cộng nhiều, cần sửa).</p>', None)],
        'Scratch')
    return K
