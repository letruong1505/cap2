#!/usr/bin/env python3
"""Sinh renderer/tu-duy-content.js: giáo trình Tư duy & lập trình (2 lộ trình). Kết quả code Python lấy từ lần chạy thật."""
import json, html, subprocess, sys, os

def run(code, stdin=''):
    r = subprocess.run([sys.executable, '-I', '-c', code], input=stdin, capture_output=True, text=True, timeout=10)
    assert r.returncode == 0, r.stderr
    return r.stdout.rstrip('\n')

E = html.escape
def li(items): return '<ul class="tl">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def card(n, title, body): return '<section class="tcard"><h4><span class="tn">%s</span>%s</h4>%s</section>' % (n, title, body)
def tsum(goal, prep, prod):
    return '<div class="tsum"><div class="tsum-l">Tóm tắt bài</div><ul><li><b>Mục tiêu:</b> %s</li><li><b>Chuẩn bị:</b> %s</li><li><b>Sản phẩm:</b> %s</li></ul></div>' % (goal, prep, prod)
def think(items): return '<div class="card think"><div class="lbl">Khai mở tư duy</div>%s</div>' % li(items)
def note(t): return '<p class="tnote">%s</p>' % t
def code(src, out=None):
    s = '<pre class="code">%s</pre>' % E(src.strip('\n'))
    if out is not None: s += '<div class="code-out-l">Kết quả khi chạy</div><pre class="code out">%s</pre>' % E(out)
    return s
def blocks(src): return '<pre class="scratch">%s</pre>' % E(src.strip('\n'))
def ex(bad, good): return '<div class="ex"><div class="ex-row ex-bad"><b>Chưa tốt:</b> %s</div><div class="ex-row ex-good"><b>Tốt hơn:</b> %s</div></div>' % (bad, good)
def prac(n, title, task, data=None, ans=''):
    s = '<section class="tcard tprac"><h4><span class="tn">%s</span>Thực hành: %s</h4><p>%s</p>' % (n, title, task)
    if data: s += data
    s += '<details class="tans"><summary>Xem đáp án</summary>%s</details></section>' % ans
    return s
def lesson(title, sub, *parts): return {'title': title, 'sub': sub, 'html': '\n'.join(parts)}
def chap(t): return '<div class="tchap">%s</div>' % t

THINK2 = ('<b>Hai thói quen của khóa học:</b> (1) <b>Hỏi “vì sao đúng?”</b> – không tin ngay kết quả, luôn tìm bằng chứng và thử thêm trường hợp khác; '
          '(2) <b>Nghĩ ngược</b> – bắt đầu từ kết quả mong muốn rồi lần ngược về các bước cần làm.')

# ====================== LỘ TRÌNH 8–11 (SCRATCH) ======================
def sq_trace(n):  # mô phỏng
    return n
K1 = {}
K1['tongquan'] = lesson('Mở đầu · Lập trình để học cách nghĩ', 'Lộ trình 8–11 tuổi · dùng Scratch.',
  tsum('Hiểu khóa học dạy em cách <b>nghĩ</b>, không chỉ cách gõ lệnh', 'Máy tính hoặc điện thoại; vào <b>scratch.mit.edu</b> (làm cùng người lớn nếu cần); giấy bút', 'Tờ “2 câu hỏi vàng” dán trước bàn học'),
  card(1, 'Khóa học này dạy gì?', li(['Em sẽ làm nhân vật di chuyển, vẽ hình, chơi trò chơi bằng <b>khối lệnh Scratch</b> – kéo thả, không cần gõ chữ.', 'Nhưng mục tiêu lớn hơn: <b>học cách giải quyết vấn đề</b>. Scratch chỉ là đồ chơi để em thử suy nghĩ của mình.', 'Học xong, em sẽ chia được việc khó thành bước nhỏ, tự tìm ra lỗi và biết “nghĩ ngược”.'])),
  card(2, 'Hai câu hỏi vàng', li(['<b>Câu 1 – Vì sao đúng?</b> Chương trình chạy ra kết quả chưa chắc là đúng. Em hãy thử thêm một trường hợp khác để kiểm tra.', '<b>Câu 2 – Muốn có kết quả này, trước đó phải làm gì?</b> Đó là <b>nghĩ ngược</b>: đi từ đích về điểm xuất phát.']) +
    think(['Muốn lên tầng 3 của ngôi nhà, em phải đi qua gì trước? (Tầng 2, rồi cầu thang.)', 'Chuyện này chính là nghĩ ngược: từ đích, hỏi “trước đó cần gì?”'])),
  card(3, 'Cách học mỗi bài', li(['<b>Thẻ tóm tắt</b> cho biết hôm nay học gì.', '<b>Thẻ số</b> giải thích từng ý, có ví dụ.', '<b>Thẻ thực hành</b> màu cam: em tự làm rồi mới bấm “Xem đáp án”.', 'Gặp lỗi là bình thường – nhà lập trình giỏi cũng sửa lỗi cả ngày!'])),
  prac(4, 'Tìm việc “nghĩ ngược” quanh em', 'Kể ra 3 việc trong ngày mà em phải <b>nghĩ ngược</b> mới làm được (ví dụ: biết giờ ra khỏi nhà thì phải dậy lúc mấy giờ).', None,
       '<p>Gợi ý: (1) Muốn đến trường lúc 7h, đi mất 15 phút → phải ra khỏi nhà lúc 6h45. (2) Muốn bài tập xong trước bữa tối → phải bắt đầu sớm. (3) Muốn có điểm tốt bài kiểm tra → phải ôn trước. Đúng rồi nếu em đi từ <b>đích</b> ngược về <b>việc cần làm trước đó</b>.</p>'))

K1['bai1'] = lesson('Bài 1 · Máy chỉ làm đúng điều em bảo', 'Thuật toán là dãy bước rõ ràng.',
  tsum('Viết được dãy bước đủ rõ để “người máy” làm theo; tìm được bước bị thiếu', 'Giấy bút; Scratch (nếu có)', 'Bản hướng dẫn “pha mì tôm cho người máy”'),
  card(1, 'Máy không tự đoán ý em', li(['Người máy làm <b>đúng từng chữ</b> em bảo, không hơn không kém.', 'Nếu em nói “cho mì vào tô”, nó có thể cho mì <b>chưa nấu</b> vào tô!', 'Dãy bước rõ ràng, theo thứ tự gọi là <b>thuật toán</b>.']) +
    think(['Hãy hướng dẫn một bạn nhắm mắt đi từ ghế đến cửa lớp, bạn chỉ làm theo lời em.', 'Em sẽ thấy cần nói rất rõ: “đi 5 bước”, “rẽ phải”…'])),
  card(2, 'Ví dụ: pha mì tôm', ex('1. Nấu mì. 2. Ăn.', '1. Đun sôi nước. 2. Cho mì vào nồi. 3. Đợi 3 phút. 4. Tắt bếp. 5. Cho mì vào tô. 6. Cho gia vị.') + note('Bản bên trái thiếu bước nên người máy “bó tay”. <b>Câu hỏi vàng 1:</b> hỏi “làm đúng chưa?” bằng cách thử tưởng tượng từng bước.')),
  card(3, 'Trong Scratch', li(['Mỗi <b>khối lệnh</b> là một bước. Các khối xếp chồng lên nhau sẽ chạy từ trên xuống dưới.', 'Khối “khi bấm cờ xanh” là nút bắt đầu.', 'Khối “tiến 10 bước” cho nhân vật đi về phía trước.']) + blocks('khi bấm cờ xanh\n  tiến 50 bước\n  nói "Xin chào!" trong 2 giây')),
  prac(4, 'Tìm bước thiếu', 'Dãy bước <b>“đánh răng”</b> sau thiếu 2 bước. Em tìm ra chúng: 1) Cầm bàn chải. 2) Đánh răng 2 phút. 3) Nhổ bọt. 4) Cất bàn chải.', None,
       '<p>Thiếu: <b>bóp kem đánh răng</b> (trước khi đánh) và <b>súc miệng</b> (sau khi nhổ bọt). Em có thể tìm thêm “mở nước”, “lau miệng”.</p>'))

# --- Bài 2: hình vuông (mô phỏng tổng góc quay) ---
K1['bai2'] = lesson('Bài 2 · Dãy lệnh & bắt lỗi', 'Xếp lệnh đúng thứ tự và sửa lỗi.',
  tsum('Vẽ được hình vuông bằng khối lệnh; biết thứ tự lệnh quyết định kết quả', 'Scratch; thêm phần mở rộng “Bút vẽ”', 'Chương trình vẽ hình vuông'),
  card(1, 'Vẽ một cạnh rồi quay', li(['Muốn vẽ hình, em cần <b>hạ bút</b>, rồi <b>tiến</b> và <b>quay</b>.', 'Hình vuông có 4 cạnh bằng nhau và 4 góc vuông (90°).']) + blocks('khi bấm cờ xanh\n  hạ bút\n  tiến 100 bước\n  quay phải 90 độ\n  tiến 100 bước\n  quay phải 90 độ\n  tiến 100 bước\n  quay phải 90 độ\n  tiến 100 bước\n  quay phải 90 độ')),
  card(2, 'Thứ tự rất quan trọng', ex('quay phải 90 → tiến 100 → hạ bút', 'hạ bút → tiến 100 → quay phải 90') + note('Nếu <b>hạ bút sau</b> khi đã đi, cạnh đầu tiên sẽ không được vẽ!')),
  card(3, 'Nghĩ ngược để kiểm tra', li(['Muốn nhân vật <b>về đúng chỗ xuất phát</b>, tổng các lần quay phải đủ <b>một vòng 360°</b>.', 'Hình vuông: 4 lần × 90° = 360°. Đúng!']) + think(['Nếu em chỉ quay 3 lần 90°, nhân vật có về đúng chỗ cũ không? (Không: 270° chưa đủ một vòng.)'])),
  prac(4, 'Chương trình có lỗi', 'Chương trình sau muốn vẽ hình vuông cạnh 80 nhưng chỉ ra hình chữ L. Em tìm lỗi:' + blocks('khi bấm cờ xanh\n  hạ bút\n  tiến 80 bước\n  quay phải 90 độ\n  tiến 80 bước\n  quay phải 90 độ\n  tiến 80 bước'), None,
       '<p>Lỗi: chỉ có <b>3 cạnh</b>, thiếu một lần quay và một lần tiến. Thêm: <i>quay phải 90 độ</i>, <i>tiến 80 bước</i>. Kiểm tra bằng câu hỏi vàng: tổng góc quay = 4 × 90 = 360° → đủ vòng.</p>'))

K1['bai3'] = lesson('Bài 3 · Lặp lại cho gọn', 'Khối “lặp” thay cho việc chép lệnh.',
  tsum('Dùng khối lặp để vẽ hình vuông, tam giác, ngũ giác; tính được góc quay', 'Scratch', 'Chương trình vẽ nhiều hình bằng khối lặp'),
  card(1, 'Chép đi chép lại là dấu hiệu cần lặp', li(['Chương trình vẽ hình vuông chép đi chép lại 2 lệnh, <b>4 lần</b>.', 'Khối <b>lặp 4 lần</b> làm việc đó gọn hơn nhiều.']) + blocks('khi bấm cờ xanh\n  hạ bút\n  lặp 4 lần\n    tiến 100 bước\n    quay phải 90 độ')),
  card(2, 'Công thức góc quay', li(['Một vòng quay đầy đủ là 360°.', 'Hình có <b>n cạnh</b> thì mỗi lần quay <b>360 ÷ n</b> độ.', 'Tam giác đều: 360 ÷ 3 = <b>120°</b>. Ngũ giác đều: 360 ÷ 5 = <b>72°</b>. Lục giác đều: 360 ÷ 6 = <b>60°</b>.']) + think(['Em dùng công thức này <b>nghĩ ngược</b>: biết góc quay 60°, hỏi số cạnh? (360 ÷ 60 = 6 cạnh.)'])),
  card(3, 'Ví dụ: tam giác đều', blocks('khi bấm cờ xanh\n  hạ bút\n  lặp 3 lần\n    tiến 100 bước\n    quay phải 120 độ')),
  prac(4, 'Nghĩ ngược từ góc quay', 'Điền bảng: biết góc quay, tìm số lần lặp. (a) quay 90° (b) quay 45° (c) quay 36°.', None,
       '<p>(a) 360 ÷ 90 = <b>4</b> lần (hình vuông). (b) 360 ÷ 45 = <b>8</b> lần (bát giác). (c) 360 ÷ 36 = <b>%d</b> lần (thập giác). Em thử vẽ trong Scratch để kiểm tra nhé!</p>' % (360 // 36)))

# --- Bài 4: biến (trace) ---
def var_trace():
    d = 5; steps = [('đặt điểm = 5', d)]
    d += 3; steps.append(('thêm 3 vào điểm', d))
    d *= 2; steps.append(('đặt điểm = điểm × 2', d))
    d -= 4; steps.append(('thêm -4 vào điểm', d))
    return steps, d
VT, VF = var_trace()
K1['bai4'] = lesson('Bài 4 · Biến – chiếc hộp nhớ', 'Biến lưu số, thay đổi được.',
  tsum('Hiểu biến như chiếc hộp có tên; theo dõi giá trị biến sau từng lệnh', 'Giấy bút; Scratch', 'Bảng theo dõi giá trị biến'),
  card(1, 'Biến là gì?', li(['<b>Biến</b> là chiếc hộp có <b>tên</b> để chứa một giá trị, ví dụ <b>điểm</b> hoặc <b>mạng</b>.', 'Giá trị trong hộp có thể thay đổi khi chương trình chạy.', 'Trong Scratch: tạo biến “điểm”, rồi dùng khối “đặt điểm = 0” và “thêm 1 vào điểm”.'])),
  card(2, 'Ví dụ: trò chơi bắt sao', blocks('khi bấm cờ xanh\n  đặt điểm = 0\n  lặp liên tục\n    nếu chạm ngôi sao thì\n      thêm 1 vào điểm') + note('Mỗi lần chạm sao, điểm tăng 1. Nếu em quên “đặt điểm = 0” ở đầu, ván sau sẽ <b>cộng dồn</b> điểm cũ!')),
  card(3, 'Bảng theo dõi', li(['Để biết chương trình làm gì, em lập bảng ghi giá trị biến sau <b>từng lệnh</b>.', 'Đây là cách <b>kiểm tra “vì sao đúng”</b> mà không cần chạy máy.'])),
  prac(4, 'Theo dõi biến', 'Chương trình: ' + blocks('đặt điểm = 5\nthêm 3 vào điểm\nđặt điểm = điểm × 2\nthêm -4 vào điểm') + 'Sau mỗi lệnh, điểm bằng bao nhiêu? Cuối cùng điểm là bao nhiêu?', None,
       '<p>' + ' → '.join('%s: <b>%d</b>' % (a, b) for a, b in VT) + '.</p><p>Cuối cùng <b>điểm = %d</b>.</p>' % VF))

K1['bai5'] = lesson('Bài 5 · Nếu… thì…', 'Cho chương trình biết cách chọn.',
  tsum('Dùng khối “nếu – thì – nếu không” để chương trình tự chọn', 'Scratch', 'Chương trình phân loại điểm'),
  card(1, 'Chương trình biết chọn', li(['Đời thường: “<b>Nếu</b> trời mưa <b>thì</b> mang ô”.', 'Khối <b>nếu … thì … nếu không …</b> giúp chương trình chọn theo điều kiện.']) + blocks('nếu điểm ≥ 5 thì\n  nói "Đạt"\nnếu không\n  nói "Cố lên"')),
  card(2, 'Thử cả trường hợp biên', li(['Câu hỏi vàng 1: em chỉ thử điểm 9 thì chưa đủ.', 'Hãy thử cả <b>điểm 5</b> (sát ranh giới) và <b>điểm 4</b>. Lỗi hay nằm ở ranh giới!', 'Dấu <b>≥</b> khác dấu <b>&gt;</b>: điểm 5 “Đạt” với ≥ nhưng “Cố lên” với &gt;.'])),
  card(3, 'Nghĩ ngược', li(['Muốn nhân vật nói “Đạt” thì điểm phải thế nào? Đáp: điểm ≥ 5.', 'Từ <b>kết quả</b>, em suy ra <b>điều kiện</b>.'])),
  prac(4, 'Đoán kết quả', 'Chương trình: ' + blocks('nếu điểm ≥ 8 thì\n  nói "Giỏi"\nnếu không, nếu điểm ≥ 5 thì\n  nói "Khá"\nnếu không\n  nói "Cố lên"') + 'Điểm 8, 7, 5, 4 thì nhân vật nói gì?', None,
       '<p>' + ', '.join('điểm %d: <b>%s</b>' % (d, 'Giỏi' if d >= 8 else 'Khá' if d >= 5 else 'Cố lên') for d in (8, 7, 5, 4)) + '. Chú ý điểm <b>8</b> và <b>5</b> nằm đúng ranh giới.</p>'))

def rev(n, add, mul):  # nghĩ một số, nhân mul, cộng add
    return None
K1['bai6'] = lesson('Bài 6 · Nghĩ ngược', 'Từ kết quả, lần ngược về lúc đầu.',
  tsum('Giải bài toán bằng cách đi ngược các bước; tự viết chương trình “đảo ngược”', 'Giấy bút; Scratch', 'Chương trình đoán số em đã nghĩ'),
  card(1, 'Trò chơi đoán số', li(['Em nghĩ một số. Nhân với 2, rồi cộng 6, được <b>20</b>. Số ban đầu là gì?', 'Đi <b>ngược</b>: trừ 6 trước → 20 − 6 = 14; rồi chia 2 → <b>7</b>.', 'Kiểm tra lại <b>xuôi</b>: 7 × 2 = 14; 14 + 6 = 20. Đúng!']) + think(['Phép ngược của <b>cộng</b> là <b>trừ</b>; của <b>nhân</b> là <b>chia</b>.', 'Làm ngược phải <b>đảo thứ tự</b> các bước.'])),
  card(2, 'Viết trong Scratch', blocks('hỏi "Kết quả em có là gì?" và đợi\nđặt kq = câu trả lời\nđặt số = (kq - 6) / 2\nnói (kết hợp "Số em nghĩ là " số)')),
  card(3, 'Nghĩ ngược trong mê cung', li(['Tìm đường ra mê cung khó? Thử <b>đi từ lối ra ngược về lối vào</b>.', 'Nhiều đường ngõ cụt khi đi xuôi lại không xuất hiện khi đi ngược.'])),
  prac(4, 'Giải ngược', 'Em nghĩ một số, <b>nhân 3</b>, rồi <b>trừ 4</b>, được <b>%d</b>. Số ban đầu là gì? Hãy làm ngược rồi kiểm tra xuôi.' % (3 * 9 - 4), None,
       '<p>Ngược: %d + 4 = %d; %d ÷ 3 = <b>%d</b>. Kiểm tra xuôi: %d × 3 = %d; %d − 4 = %d. Đúng!</p>' % (23, 27, 27, 9, 9, 27, 27, 23)))

K1['bai7'] = lesson('Bài 7 · Thám tử bắt lỗi', 'Gỡ lỗi là kỹ năng quan trọng nhất.',
  tsum('Tìm và sửa lỗi bằng cách thử, quan sát, chia nhỏ', 'Scratch; giấy bút', 'Nhật ký “thám tử bắt lỗi”'),
  card(1, '3 bước bắt lỗi', li(['<b>1. Quan sát:</b> chương trình làm gì khác ý em?', '<b>2. Chia nhỏ:</b> chạy từng đoạn ngắn để thấy đoạn nào sai.', '<b>3. Sửa một chỗ rồi thử lại</b> – đừng sửa nhiều chỗ cùng lúc.'])),
  card(2, 'Ví dụ lỗi thường gặp', li(['Quên <b>đặt lại biến</b> ở đầu chương trình.', 'Sai <b>thứ tự</b> các khối.', 'Sai <b>con số</b>, ví dụ quay 80° thay vì 90°.', 'Quên khối <b>hạ bút</b>.'])),
  card(3, 'Câu hỏi vàng 1', think(['Chương trình chạy ra không lỗi nhưng kết quả có <b>đúng ý</b> không?', 'Hãy thử ít nhất 3 trường hợp: bình thường, sát ranh giới, và bất thường.'])),
  prac(4, 'Bắt lỗi trò chơi', 'Trò chơi “điểm” luôn bắt đầu từ điểm của ván trước thay vì 0. Chương trình:' + blocks('khi bấm cờ xanh\n  lặp liên tục\n    nếu chạm ngôi sao thì\n      thêm 1 vào điểm') + 'Em tìm lỗi và nêu cách sửa.', None,
       '<p>Lỗi: chưa có lệnh <b>đặt điểm = 0</b> lúc bắt đầu. Sửa: thêm khối “đặt điểm = 0” ngay dưới “khi bấm cờ xanh”. Thử lại ván 2 để kiểm tra điểm bắt đầu từ 0.</p>'))

K1['bai8'] = lesson('Bài 8 · Dự án: trò chơi bắt sao', 'Tự lên kế hoạch ngược và làm trọn một sản phẩm.',
  tsum('Hoàn thành một trò chơi nhỏ, dùng đủ lặp, biến, điều kiện; lập kế hoạch bằng cách nghĩ ngược', 'Scratch; giấy bút', 'Trò chơi bắt sao của riêng em'),
  card(1, 'Nghĩ ngược để lập kế hoạch', li(['<b>Đích:</b> ván chơi có điểm, kết thúc sau 30 giây.', 'Muốn có điểm → cần <b>biến điểm</b>.', 'Muốn tăng điểm → cần <b>nếu chạm sao thì thêm 1</b>.', 'Muốn sao xuất hiện liên tục → cần <b>lặp</b> và <b>vị trí ngẫu nhiên</b>.'])),
  card(2, 'Khung chương trình', blocks('khi bấm cờ xanh\n  đặt điểm = 0\n  đặt thời gian = 30\n  lặp 30 lần\n    chờ 1 giây\n    thêm -1 vào thời gian\n  nói "Hết giờ!"') + blocks('(nhân vật Sao)\nkhi bấm cờ xanh\n  lặp liên tục\n    đến vị trí ngẫu nhiên\n    nếu chạm chuột thì\n      thêm 1 vào điểm')),
  card(3, 'Tự kiểm tra và nâng cấp', li(['Thử 3 ván: điểm có về 0 mỗi lần? Hết 30 giây thì dừng chưa?', 'Nâng cấp: thêm ngôi sao vàng cho 5 điểm; thêm nhạc nền.'])),
  prac(4, 'Tính điểm tối đa', 'Mỗi giây sao hiện một lần và em bắt được ngay. Ván 30 giây, sao thường 1 điểm, cứ 5 giây có thêm 1 sao vàng 5 điểm (thay sao thường ở giây đó). Điểm tối đa là bao nhiêu?', None,
       '<p>Số giây có sao vàng: 30 ÷ 5 = %d. Số giây sao thường: 30 − %d = %d → %d điểm. Sao vàng: %d × 5 = %d điểm. <b>Tổng = %d điểm.</b></p>' % (6, 6, 24, 24, 6, 30, 54)))

# ====================== LỘ TRÌNH 12–18 (PYTHON) ======================
P = {}
P['tongquan'] = lesson('Mở đầu · Lập trình để rèn tư duy', 'Lộ trình 12–18 tuổi · dùng Python.',
  tsum('Hiểu mục tiêu: dùng Python như phòng thí nghiệm để luyện tư duy phản biện và tư duy ngược', 'Máy tính có <b>Python 3</b> (python.org) hoặc trình chạy online như Replit/Colab; một trình soạn thảo bất kỳ', 'Bảng “2 câu hỏi nền tảng” dán cạnh máy'),
  card(1, 'Khóa học này khác gì “học gõ code”?', li(['Bạn sẽ học Python <b>vừa đủ</b> để giải bài toán thật. Ngôn ngữ chỉ là công cụ.', 'Điểm cốt lõi là <b>cách nghĩ</b>: phân rã bài toán, nghi ngờ kết quả, và đi ngược từ đích.', 'Trong thời đại AI, ai biết <b>đặt câu hỏi và kiểm chứng</b> sẽ làm chủ được công cụ.'])),
  card(2, 'Hai câu hỏi nền tảng', li(['<b>Phản biện:</b> “Điều này đúng ở mọi trường hợp chưa? Bằng chứng nào? Giả định nào đang ẩn?”', '<b>Nghĩ ngược:</b> “Muốn có kết quả này, điều kiện cuối cùng cần là gì? Trước đó là gì?”']) + think(['Một chương trình in đúng ví dụ mẫu có thật sự đúng không?', 'Có thể không: nó mới đúng <b>một</b> trường hợp. Bạn sẽ học cách tìm trường hợp làm nó sai.'])),
  card(3, 'Cách học', li(['<b>Thẻ số:</b> khái niệm và ví dụ. Mọi đoạn code đều có <b>kết quả chạy thật</b> bên dưới.', '<b>Thẻ thực hành (cam):</b> tự làm rồi mở đáp án.', 'Bấm <b>Sao chép</b> ở khối dữ liệu để dán vào trình chạy.', 'Gõ lại code bằng tay thay vì chỉ đọc – bạn sẽ nhớ lâu hơn.'])),
  prac(4, 'Đoán trước khi chạy', 'Đoạn code sau in ra gì? Hãy dự đoán rồi mới chạy:' + code('print(2 + 3 * 4)'), None,
       '<p>Kết quả là <b>%s</b> vì nhân trước, cộng sau (2 + 12). Thói quen tốt: <b>dự đoán trước, chạy sau, rồi hỏi “vì sao khác?”</b> nếu lệch.</p>' % run('print(2 + 3 * 4)')))

c = 'name = "Lan"\nprint("Xin chào,", name)\nprint("Bình phương của 7 là", 7 * 7)'
P['bai1'] = lesson('Bài 1 · Từ bài toán đến thuật toán', 'Phân rã vấn đề rồi mới viết code.',
  tsum('Chia một bài toán thành các bước; viết chương trình Python đầu tiên với print và input', 'Python 3 hoặc trình chạy online', 'Chương trình chào và tính toán đơn giản'),
  card(1, 'Nghĩ trước, gõ sau', li(['<b>Thuật toán</b> là dãy bước hữu hạn, rõ ràng để giải một bài toán.', 'Quy trình: <b>hiểu đề → chia nhỏ → viết các bước bằng lời → mới gõ code</b>.', 'Người giỏi dành nhiều thời gian nghĩ hơn gõ.']) + ex('Mở máy và gõ ngay cho đến khi chạy được.', 'Viết ra: đầu vào là gì, đầu ra là gì, các bước ở giữa là gì.')),
  card(2, 'Chương trình đầu tiên', code(c, run(c))),
  card(3, 'Nhập dữ liệu với input()', li(['<code>input()</code> luôn trả về <b>chữ</b>. Muốn tính toán phải đổi sang số bằng <code>int()</code>.']) + code('a = int(input())\nb = int(input())\nprint("Tổng:", a + b)', run('a = int(input())\nb = int(input())\nprint("Tổng:", a + b)', '12\n30\n')) + note('Ví dụ trên nhập 12 và 30.')),
  prac(4, 'Chia nhỏ bài toán', 'Bài: “Tính tiền một bữa ăn 4 người, mỗi người 45 000 đồng, thêm 10% phí phục vụ.” Hãy (a) liệt kê các bước bằng lời, (b) viết code, rồi chạy.', None,
       '<p>Các bước: tính tiền ăn = 4 × 45000; tính phí = 10%% của tiền ăn; cộng lại.</p>' + code('an = 4 * 45000\nphi = an * 10 // 100\nprint(an + phi)', run('an = 4 * 45000\nphi = an * 10 // 100\nprint(an + phi)'))))

c2 = 'gia = 25000\nsl = 3\ntong = gia * sl\nsl = sl + 2\nprint(tong)\nprint(gia * sl)'
P['bai2'] = lesson('Bài 2 · Biến và kiểu dữ liệu', 'Theo dõi giá trị biến để kiểm chứng chương trình.',
  tsum('Hiểu biến, số và chữ; biết lập bảng theo dõi để dự đoán kết quả', 'Python 3', 'Bảng theo dõi biến cho một đoạn code'),
  card(1, 'Biến là ô nhớ có tên', li(['<code>gia = 25000</code> nghĩa là: lưu số 25000 vào ô tên <b>gia</b>.', 'Dấu <code>=</code> trong lập trình là <b>gán</b>, không phải “bằng nhau” như toán học.', '<code>sl = sl + 2</code> nghĩa là lấy giá trị cũ cộng 2 rồi lưu lại.'])),
  card(2, 'Số và chữ khác nhau', code('print(3 + 4)\nprint("3" + "4")\nprint("Ha" * 3)', run('print(3 + 4)\nprint("3" + "4")\nprint("Ha" * 3)')) + note('Cộng hai số ra số; cộng hai chuỗi chữ thì <b>nối</b> lại. Đây là lỗi hay gặp khi quên <code>int()</code>.')),
  card(3, 'Phản biện kết quả', think(['Có người nói: sau khi tăng <code>sl</code>, biến <code>tong</code> tự cập nhật. Đúng không?', 'Không! <code>tong</code> được tính <b>một lần</b> lúc đó. Hãy thử chạy để kiểm chứng.'])),
  prac(4, 'Dự đoán rồi chạy', 'Đoạn code dưới in ra hai số. Lập bảng theo dõi <code>gia</code>, <code>sl</code>, <code>tong</code> sau từng dòng, dự đoán kết quả.' + code(c2), None,
       '<p>Bảng: gia=25000; sl=3; tong=75000; sl=5. In ra tong → <b>75000</b>; in gia×sl → <b>125000</b>.</p>' + code(c2, run(c2)) + note('Vì tong không tự cập nhật theo sl.')))

c3 = 'def xep_loai(d):\n    if d >= 8:\n        return "Giỏi"\n    elif d >= 5:\n        return "Khá"\n    else:\n        return "Yếu"\nfor d in [10, 8, 7.9, 5, 4.9, 0]:\n    print(d, xep_loai(d))'
P['bai3'] = lesson('Bài 3 · Điều kiện if và kiểm thử biên', 'Lỗi thường nằm ở ranh giới.',
  tsum('Viết được if/elif/else; chọn bộ test gồm giá trị thường, biên và bất thường', 'Python 3', 'Hàm xếp loại kèm bảng test'),
  card(1, 'Rẽ nhánh', li(['<code>if</code> kiểm tra điều kiện; nếu sai thì thử <code>elif</code>, cuối cùng là <code>else</code>.', 'Thụt đầu dòng 4 dấu cách là <b>bắt buộc</b> trong Python.']) + code(c3, run(c3))),
  card(2, 'Chọn test như một nhà phản biện', li(['Test “bình thường”: 7.', 'Test <b>biên</b>: 8, 7.9, 5, 4.9 – nơi điều kiện đổi kết quả.', 'Test <b>bất thường</b>: 0, 10 (hoặc điểm âm, điểm trên 10 nếu chương trình cho phép).']) + ex('Chỉ thử điểm 9 thấy ra “Giỏi” rồi kết luận đúng.', 'Thử 8 và 7.9 để chắc dấu <code>&gt;=</code> đặt đúng chỗ.')),
  card(3, 'Nghĩ ngược về điều kiện', li(['Muốn nhận “Khá”, điểm phải nằm trong khoảng nào? Đáp: <b>5 ≤ d &lt; 8</b>.', 'Từ <b>kết quả mong muốn</b>, bạn suy ra <b>điều kiện</b> cần viết.'])),
  prac(4, 'Tìm test làm chương trình sai', 'Một bạn viết <code>if d &gt; 8</code> thay vì <code>&gt;= 8</code>. Chọn <b>một test</b> để lộ lỗi và nói kết quả mong đợi so với kết quả thực.', None,
       '<p>Test <b>d = 8</b>: mong đợi “Giỏi” nhưng code sai in “Khá”. Bằng chứng là một giá trị cụ thể, không phải cảm giác.</p>'))

c4 = 'tong = 0\nfor i in range(1, 11):\n    tong += i\nprint(tong)'
c4b = 'for i in range(1, 6):\n    print(i)'
c4c = 'print(sum(range(1, 100)))'
P['bai4'] = lesson('Bài 4 · Vòng lặp và lỗi lệch một', 'Làm việc lặp lại một cách chắc chắn.',
  tsum('Dùng for/while; hiểu range(a, b) dừng trước b; tránh lỗi lệch 1', 'Python 3', 'Chương trình tính tổng và bảng nhân'),
  card(1, 'for lặp đúng số lần', code(c4, run(c4)) + li(['<code>range(1, 11)</code> chạy 1, 2, …, <b>10</b> (không gồm 11).', '<code>tong += i</code> là viết gọn của <code>tong = tong + i</code>.'])),
  card(2, 'Lỗi lệch một (off-by-one)', code(c4b, run(c4b)) + note('Muốn in đến 5 phải viết <code>range(1, 6)</code>. Hãy luôn <b>thử với n nhỏ</b> (n = 1, 2) để bắt lỗi lệch.')),
  card(3, 'Phản biện bằng công thức', li(['Tổng 1 đến n bằng <b>n(n+1)/2</b>. Với n = 10: 10 × 11 ÷ 2 = %d, khớp với kết quả chạy!' % (10 * 11 // 2), 'Hai cách khác nhau cho cùng kết quả → bạn tin kết quả hơn. Đó là <b>kiểm chứng chéo</b>.'])),
  prac(4, 'Tổng 1 đến 99', 'Dự đoán tổng 1 + 2 + … + 99 bằng công thức rồi chạy kiểm tra. Nếu ai đó viết <code>range(1, 99)</code> thì thiếu số nào?', None,
       '<p>Công thức: 99 × 100 ÷ 2 = <b>%d</b>.</p>' % (99 * 100 // 2) + code(c4c, run(c4c)) + note('<code>range(1, 99)</code> thiếu số <b>99</b>, tổng sẽ là %d.' % sum(range(1, 99)))))

dl = '5\n9\n2\n9\n7\n3\n'
c5 = 'def lon_nhat(ds):\n    kq = ds[0]\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\n\nds = [5, 9, 2, 9, 7, 3]\nprint(lon_nhat(ds))\nprint(ds.count(9))\nprint(sum(ds) / len(ds))'
P['bai5'] = lesson('Bài 5 · Danh sách và hàm', 'Gom dữ liệu, đóng gói việc lặp lại.',
  tsum('Dùng list và hàm; tìm số lớn nhất, đếm, tính trung bình', 'Python 3', 'Hàm tìm số lớn nhất tự viết'),
  card(1, 'List chứa nhiều giá trị', li(['<code>ds = [5, 9, 2]</code> là danh sách 3 phần tử; <code>ds[0]</code> là phần tử đầu (đếm từ 0).', '<code>len(ds)</code> là số phần tử, <code>sum(ds)</code> là tổng.'])),
  card(2, 'Hàm là cỗ máy nhỏ', code(c5, run(c5)) + note('Hàm nhận đầu vào, trả đầu ra bằng <code>return</code>. Viết một lần, dùng nhiều lần.')),
  card(3, 'Nghi ngờ hàm của chính mình', li(['Hàm <code>lon_nhat</code> sai với danh sách <b>rỗng</b> (<code>ds[0]</code> lỗi).', 'Nó có đúng khi có hai số lớn nhất bằng nhau (như hai số 9)? Kết quả cho thấy: vẫn đúng.', 'Phản biện tốt là <b>đi tìm trường hợp làm hàm sai</b> chứ không chỉ chứng minh nó đúng.'])),
  prac(4, 'Dữ liệu điểm', 'Điểm 6 bạn: dán dữ liệu vào code, tìm điểm cao nhất, số bạn đạt điểm cao nhất, và điểm trung bình (làm tròn 2 số lẻ).', '<pre class="pdata">5\n9\n2\n9\n7\n3</pre>',
       '<p>Cao nhất <b>9</b>; có <b>2</b> bạn; trung bình = 35 ÷ 6 = <b>%.2f</b>.</p>' % (35 / 6) + code('ds = [5, 9, 2, 9, 7, 3]\nprint(max(ds), ds.count(max(ds)), round(sum(ds) / len(ds), 2))', run('ds = [5, 9, 2, 9, 7, 3]\nprint(max(ds), ds.count(max(ds)), round(sum(ds) / len(ds), 2))'))))

c6 = 'def xuoi(n):\n    return (n * 3 + 4) * 2\n\ndef nguoc(kq):\n    return (kq // 2 - 4) // 3\n\nprint(xuoi(7))\nprint(nguoc(xuoi(7)))'
c6b = 'ket_qua = 0\nfor n in range(1, 1000):\n    if n * n + n == 156:\n        ket_qua = n\n        break\nprint(ket_qua)'
c6c = 'n = 156\nx = 12\nprint(x * (x + 1) == n)'
c6d = 'ds = "tuduy"\nprint(ds[::-1])'
P['bai6'] = lesson('Bài 6 · Tư duy ngược', 'Đi từ kết quả về điều kiện ban đầu.',
  tsum('Giải bài bằng cách đảo thứ tự và phép tính; dùng code kiểm tra đáp án suy ngược', 'Python 3', 'Hàm xuôi và hàm ngược kiểm tra lẫn nhau'),
  card(1, 'Đảo ngược các bước', li(['Quy trình xuôi: <b>nhân 3, cộng 4, nhân 2</b>. Muốn tìm đầu vào từ kết quả, làm ngược: <b>chia 2, trừ 4, chia 3</b>.', 'Nguyên tắc: <b>đảo thứ tự</b> và <b>đổi phép tính thành phép nghịch đảo</b>.']) + code(c6, run(c6)) + note('Hàm ngược lấy lại đúng 7 → chương trình nhất quán.')),
  card(2, 'Khi khó đi ngược: thử hết khả năng', code(c6b, run(c6b)) + li(['Bài: tìm n sao cho n² + n = 156.', 'Nếu chưa biết giải phương trình, ta <b>thử lần lượt</b> – thuật toán “vét cạn”.', 'Máy tính làm việc thử này rất nhanh; việc của bạn là <b>chọn khoảng thử hợp lý</b>.'])),
  card(3, 'Kiểm chứng ngược', code(c6c, run(c6c)) + note('Thay đáp án vào đề bài để kiểm tra. Đây là bước nhiều người bỏ qua nhưng quan trọng nhất của tư duy phản biện.')),
  prac(4, 'Giải ngược bài toán', 'Một số được nhân 5, trừ 8, rồi bình phương, kết quả 169. Hãy tìm số ban đầu (có thể có 2 đáp án) bằng cách làm ngược, rồi dùng code kiểm tra.', None,
       '<p>Ngược: căn bậc hai 169 = 13 hoặc −13; cộng 8: 21 hoặc −5; chia 5: <b>4,2</b> hoặc <b>−1</b>. Số nguyên: <b>−1</b>.</p>' + code('x = -1\nprint(((x * 5) - 8) ** 2)', run('x = -1\nprint(((x * 5) - 8) ** 2)')) + note('Chú ý: bình phương làm mất thông tin dấu nên khi đi ngược có <b>hai</b> khả năng. Phản biện: đề bài đã đủ để chọn một đáp án chưa?')))

c7 = 'def trung_binh(ds):\n    return sum(ds) / len(ds)\n\nprint(trung_binh([4, 6, 8]))'
c7b = 'def trung_binh(ds):\n    return sum(ds) / len(ds)\n\nassert trung_binh([4, 6, 8]) == 6\nassert trung_binh([5]) == 5\nassert trung_binh([0, 10]) == 5\nprint("Tất cả test đều qua")'
c7c = 'def so_chan(ds):\n    dem = 0\n    for x in ds:\n        if x % 2 == 0:\n            dem += 1\n    return dem\nprint(so_chan([1, 2, 3, 4, 6]))'
P['bai7'] = lesson('Bài 7 · Gỡ lỗi và viết test', 'Bằng chứng thay cho cảm giác.',
  tsum('Dùng assert để tự kiểm thử; quy trình tìm lỗi có hệ thống', 'Python 3', 'Bộ test cho một hàm'),
  card(1, 'Quy trình gỡ lỗi', li(['<b>Tái hiện:</b> tìm đầu vào làm lỗi xuất hiện.', '<b>Thu hẹp:</b> in giá trị biến giữa chừng để biết sai từ dòng nào.', '<b>Giả thuyết:</b> đoán nguyên nhân, sửa một chỗ, chạy lại.', '<b>Chặn tái phạm:</b> thêm test cho lỗi vừa sửa.'])),
  card(2, 'assert – tự động kiểm tra', code(c7b, run(c7b)) + note('<code>assert điều_kiện</code> báo lỗi ngay nếu điều kiện sai. Test tốt gồm cả giá trị thường, biên và bất thường.')),
  card(3, 'Ví dụ: đếm số chẵn', code(c7c, run(c7c)) + note('Kết quả đúng là 3 (2, 4, 6). Dùng <code>x % 2 == 0</code> để kiểm tra số chẵn; <code>%</code> là phép lấy dư.')),
  prac(4, 'Tìm test làm sập hàm', 'Hàm <code>trung_binh([])</code> chạy sẽ ra gì? Đề xuất cách sửa hợp lý và viết test.', None,
       '<p>Với danh sách rỗng, <code>len(ds)</code> bằng 0 nên chia cho 0 gây lỗi <b>ZeroDivisionError</b>.</p>' + code('def trung_binh(ds):\n    if not ds:\n        return 0\n    return sum(ds) / len(ds)\nassert trung_binh([]) == 0\nprint("ok")', run('def trung_binh(ds):\n    if not ds:\n        return 0\n    return sum(ds) / len(ds)\nassert trung_binh([]) == 0\nprint("ok")')) + note('Phản biện thêm: trả về 0 có hợp lý không? Có thể nên báo lỗi rõ ràng. Quyết định phụ thuộc bài toán – và là <b>giả định</b> cần ghi rõ.')))

ds8 = 'Ăn uống\t450000\nĂn uống\t380000\nHọc tập\t300000\nGiải trí\t150000\nHọc tập\t220000\nGiải trí\t90000'
c8 = 'du_lieu = [("Ăn uống", 450000), ("Ăn uống", 380000), ("Học tập", 300000),\n           ("Giải trí", 150000), ("Học tập", 220000), ("Giải trí", 90000)]\ntong = {}\nfor muc, so_tien in du_lieu:\n    tong[muc] = tong.get(muc, 0) + so_tien\nfor muc in tong:\n    print(muc, tong[muc])\nprint("Tổng:", sum(tong.values()))'
P['bai8'] = lesson('Bài 8 · Dự án: sổ chi tiêu có kiểm chứng', 'Ghép mọi thứ đã học vào một bài toán thật.',
  tsum('Hoàn thành chương trình thống kê chi tiêu; ghi rõ giả định; kiểm chứng kết quả', 'Python 3', 'Chương trình thống kê + 3 test + 1 đoạn nêu giả định'),
  card(1, 'Nghĩ ngược để lập kế hoạch', li(['<b>Đích:</b> biết mỗi mục (ăn uống, học tập…) tiêu bao nhiêu và tổng cộng.', 'Muốn thế → cần <b>cộng dồn theo mục</b> → cần cấu trúc lưu “mục → tổng” (từ điển <code>dict</code>).', 'Muốn có dữ liệu → cần danh sách các khoản chi.'])),
  card(2, 'Chương trình mẫu', code(c8, run(c8)) + note('<code>tong.get(muc, 0)</code> lấy tổng hiện có của mục, mặc định 0 nếu chưa có.')),
  card(3, 'Phản biện dự án', li(['<b>Giả định ẩn:</b> mọi khoản đều ghi đúng mục? Có khoản nào bị ghi trùng không?', '<b>Kiểm chứng chéo:</b> tổng các mục có bằng tổng các khoản gốc? (Ở ví dụ: %d.)' % sum(int(l.split('\t')[1]) for l in ds8.split('\n')), '<b>Trường hợp biên:</b> danh sách rỗng? số tiền âm (hoàn tiền)?'])),
  prac(4, 'Tự làm: mục nào tốn nhất?', 'Dán dữ liệu (mục, tiền) và mở rộng chương trình để in ra <b>mục chi nhiều nhất</b> và <b>tỉ lệ phần trăm</b> của mục đó so với tổng.', '<pre class="pdata">%s</pre>' % E(ds8),
       '<p>Gợi ý: dùng <code>max(tong, key=tong.get)</code>.</p>' + code(c8 + '\ntop = max(tong, key=tong.get)\nprint(top, round(tong[top] * 100 / sum(tong.values()), 1), "%")', run(c8 + '\ntop = max(tong, key=tong.get)\nprint(top, round(tong[top] * 100 / sum(tong.values()), 1), "%")'))))

OUT = {'k811': K1, 'k1218': P}
js = '// Sinh bởi tools/build-tu-duy.py – đừng sửa tay.\nwindow.TUDUY = ' + json.dumps(OUT, ensure_ascii=False, indent=1) + ';\n'
open(os.path.join(os.path.dirname(__file__), '..', 'renderer', 'tu-duy-content.js'), 'w', encoding='utf-8').write(js)
print('ok', {k: len(v) for k, v in OUT.items()})
