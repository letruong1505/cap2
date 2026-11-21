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


def fig(svg, cap): return '<figure class="aiw-fig">%s<figcaption>%s <span class="tdhint">Trên điện thoại: vuốt ngang để xem hết hình.</span></figcaption></figure>' % (svg, cap)
def svg(w, h, inner, label):
    return '<svg class="tdfig" viewBox="0 0 %d %d" role="img" aria-label="%s"><rect width="%d" height="%d" fill="#fff"/><g font-family="sans-serif" font-size="16">%s</g></svg>' % (w, h, E(label), w, h, inner)
def step(x, y, n): return '<circle cx="%d" cy="%d" r="13" fill="#d9822b"/><text x="%d" y="%d" text-anchor="middle" font-weight="700" fill="#fff">%s</text>' % (x, y, x, y + 5, n)
def browser(url, extra=''):
    return ('<rect x="10" y="10" width="680" height="250" rx="10" fill="#f6f8fb" stroke="#9db4c9"/><rect x="10" y="10" width="680" height="34" rx="10" fill="#dfe7ef"/>'
            '<circle cx="28" cy="27" r="5" fill="#e06c5c"/><circle cx="46" cy="27" r="5" fill="#e6b23a"/><circle cx="64" cy="27" r="5" fill="#5bb26a"/>'
            '<rect x="90" y="17" width="450" height="20" rx="10" fill="#fff" stroke="#9db4c9"/><text x="105" y="32" fill="#1c2733">%s</text>%s' % (url, extra))

# ---- hình Scratch ----
SC_FIG1 = svg(700, 270, browser('scratch.mit.edu',
  '<rect x="10" y="44" width="680" height="40" fill="#4d97ff"/><text x="30" y="70" fill="#fff" font-weight="700" font-size="18">SCRATCH</text>'
  '<rect x="150" y="52" width="90" height="26" rx="6" fill="#ffbf00" stroke="#a87c00" stroke-width="3"/><text x="195" y="70" text-anchor="middle" font-weight="700" fill="#1c2733">Tạo</text>'
  '<text x="270" y="70" fill="#fff">Khám phá</text><text x="350" y="70" fill="#fff">Ý tưởng</text><text x="425" y="70" fill="#fff">Giới thiệu</text>'
  '<rect x="60" y="120" width="560" height="110" rx="10" fill="#fff" stroke="#c9d6e2"/><text x="350" y="165" text-anchor="middle" font-size="20" fill="#17406b" font-weight="700">Trang chủ Scratch</text>'
  '<text x="350" y="195" text-anchor="middle" fill="#5b6773">Không cần tài khoản vẫn bấm “Tạo” để bắt đầu lập trình</text>'
  + step(195, 105, 2) + step(565, 27, 1)), 'Vào scratch.mit.edu và bấm nút Tạo')
SC_FIG2 = svg(700, 330, '<rect x="10" y="10" width="680" height="310" rx="10" fill="#f6f8fb" stroke="#9db4c9"/>'
  '<rect x="10" y="10" width="680" height="34" rx="10" fill="#4d97ff"/><text x="28" y="33" fill="#fff" font-weight="700">Tập tin ▾    Chỉnh sửa ▾    Hướng dẫn</text>'
  '<rect x="22" y="56" width="70" height="26" rx="4" fill="#d6e6ff"/><text x="57" y="74" text-anchor="middle">Khối lệnh</text><rect x="22" y="86" width="170" height="224" fill="#fff" stroke="#c9d6e2"/>'
  '<rect x="34" y="98" width="110" height="26" rx="5" fill="#4c97ff"/><text x="42" y="116" fill="#fff">tiến 10 bước</text><rect x="34" y="132" width="130" height="26" rx="5" fill="#4c97ff"/><text x="42" y="150" fill="#fff">quay phải 15 độ</text>'
  '<rect x="34" y="166" width="120" height="26" rx="5" fill="#ffab19"/><text x="42" y="184" fill="#fff">lặp 10 lần</text>'
  '<rect x="200" y="56" width="250" height="254" fill="#fbfdff" stroke="#c9d6e2"/><text x="325" y="82" text-anchor="middle" fill="#5b6773">Vùng ghép khối (kéo khối vào đây)</text>'
  '<rect x="240" y="110" width="110" height="26" rx="5" fill="#ffbf00"/><text x="248" y="128">khi bấm cờ xanh</text><rect x="240" y="138" width="110" height="26" rx="5" fill="#4c97ff"/><text x="248" y="156" fill="#fff">tiến 10 bước</text>'
  '<rect x="462" y="56" width="216" height="162" fill="#fff" stroke="#9db4c9"/><text x="570" y="82" text-anchor="middle" fill="#5b6773">Sân khấu</text><circle cx="570" cy="140" r="22" fill="#f4a261"/><text x="570" y="146" text-anchor="middle" font-size="12">mèo</text>'
  '<polygon points="474,70 488,64 488,76" fill="#2a8a4a"/><rect x="494" y="64" width="12" height="12" fill="#c0392b"/>'
  '<rect x="462" y="226" width="216" height="84" fill="#fff" stroke="#c9d6e2"/><text x="570" y="262" text-anchor="middle" fill="#5b6773">Danh sách nhân vật</text>'
  + step(110, 70, 1) + step(210, 70, 2) + step(560, 70, 3) + step(482, 86, 4) + step(560, 236, 5), 'Giao diện trình soạn Scratch gồm 5 vùng')
SC_FIG3 = svg(700, 250, '<rect x="10" y="10" width="680" height="230" rx="10" fill="#f6f8fb" stroke="#9db4c9"/><rect x="10" y="10" width="680" height="34" rx="10" fill="#4d97ff"/><text x="28" y="33" fill="#fff" font-weight="700">Tập tin ▾</text>'
  '<rect x="20" y="46" width="270" height="130" fill="#fff" stroke="#9db4c9"/><text x="34" y="74">Mới</text><text x="34" y="102">Tải lên từ máy tính của bạn</text>'
  '<rect x="24" y="112" width="262" height="30" rx="4" fill="#ffe9a8" stroke="#d9a400" stroke-width="2"/><text x="34" y="132" font-weight="700">Lưu vào máy tính của bạn</text>'
  '<text x="34" y="160" fill="#5b6773">(Save to your computer)</text>'
  '<text x="330" y="132" fill="#1c2733">→ tệp <tspan font-weight="700">.sb3</tspan> được lưu vào thư mục Tải xuống (Downloads)</text>'
  '<text x="330" y="156" fill="#5b6773">Muốn mở lại: Tập tin → Tải lên từ máy tính của bạn → chọn tệp .sb3</text>' + step(300, 127, 1), 'Lưu và mở lại dự án Scratch trên máy tính')

# ---- hình Python ----
PY_FIG1 = svg(700, 270, browser('python.org/downloads',
  '<rect x="10" y="44" width="680" height="40" fill="#306998"/><text x="30" y="70" fill="#fff" font-weight="700" font-size="18">python</text><text x="270" y="70" fill="#fff">Downloads</text>'
  '<rect x="60" y="110" width="560" height="120" rx="10" fill="#fff" stroke="#c9d6e2"/><text x="340" y="146" text-anchor="middle" font-size="18" fill="#17406b" font-weight="700">Download the latest version for Windows</text>'
  '<rect x="220" y="162" width="260" height="42" rx="8" fill="#ffd43b" stroke="#a88a00" stroke-width="3"/><text x="350" y="189" text-anchor="middle" font-weight="700" fill="#1c2733">Download Python 3.x.x</text>'
  + step(500, 183, 2) + step(565, 27, 1)), 'Trang tải Python trên python.org')
PY_FIG2 = svg(700, 300, '<rect x="130" y="10" width="440" height="280" rx="8" fill="#f0f0f0" stroke="#6b7785"/><rect x="130" y="10" width="440" height="30" rx="8" fill="#306998"/><text x="146" y="31" fill="#fff" font-weight="700">Python 3.x.x (64-bit) Setup</text>'
  '<text x="350" y="78" text-anchor="middle" font-size="18" font-weight="700" fill="#1c2733">Install Python</text>'
  '<rect x="200" y="100" width="300" height="46" rx="6" fill="#fff" stroke="#9db4c9"/><text x="350" y="129" text-anchor="middle">Install Now</text>'
  '<rect x="200" y="160" width="300" height="34" rx="6" fill="#fff" stroke="#9db4c9"/><text x="350" y="182" text-anchor="middle" fill="#5b6773">Customize installation</text>'
  '<rect x="150" y="214" width="400" height="60" rx="6" fill="#fff4d6" stroke="#d9822b" stroke-width="2"/>'
  '<rect x="164" y="224" width="16" height="16" fill="#fff" stroke="#1c2733"/><path d="M167 232 l4 5 l8 -10" stroke="#2a8a4a" stroke-width="3" fill="none"/><text x="190" y="237" font-weight="700">Add python.exe to PATH</text>'
  '<rect x="164" y="248" width="16" height="16" fill="#fff" stroke="#1c2733"/><path d="M167 256 l4 5 l8 -10" stroke="#2a8a4a" stroke-width="3" fill="none"/><text x="190" y="261" fill="#5b6773">Use admin privileges when installing py.exe</text>'
  + step(166, 217, 1) + step(205, 100, 2), 'Màn hình cài đặt: tích ô PATH rồi bấm Install Now').replace('viewBox="0 0 700 300"', 'viewBox="120 0 460 300"').replace('class="tdfig"', 'class="tdfig tdnarrow"')
PY_FIG3 = svg(700, 320, '<rect x="10" y="10" width="330" height="300" rx="8" fill="#fff" stroke="#6b7785"/><rect x="10" y="10" width="330" height="26" rx="8" fill="#dfe7ef"/><text x="22" y="28">IDLE Shell   File  Edit  Shell  Run</text>'
  '<text x="24" y="62" font-family="monospace" font-size="12" fill="#1c2733">Python 3.x.x ... on win32</text><text x="24" y="84" font-family="monospace" fill="#1c2733">&gt;&gt;&gt; print("Xin chào")</text><text x="24" y="106" font-family="monospace" fill="#2a8a4a">Xin chào</text><text x="24" y="128" font-family="monospace" fill="#1c2733">&gt;&gt;&gt; _</text>'
  '<text x="24" y="170" fill="#5b6773">Gõ trực tiếp sau dấu &gt;&gt;&gt; để thử nhanh</text><text x="24" y="190" fill="#5b6773">một lệnh.</text>'
  '<rect x="360" y="10" width="330" height="300" rx="8" fill="#fff" stroke="#6b7785"/><rect x="360" y="10" width="330" height="26" rx="8" fill="#dfe7ef"/><text x="372" y="28">bai1.py   File  Edit  Format  Run</text>'
  '<text x="376" y="62" font-family="monospace" fill="#1c2733">name = "Lan"</text><text x="376" y="84" font-family="monospace" fill="#1c2733">print("Xin chào,", name)</text>'
  '<rect x="376" y="130" width="300" height="40" rx="6" fill="#ffe9a8" stroke="#d9a400" stroke-width="2"/><text x="388" y="156" font-weight="700">Run → Run Module   (phím F5)</text>'
  '<text x="376" y="200" fill="#5b6773">Chương trình nhiều dòng: File → New File,</text><text x="376" y="220" fill="#5b6773">gõ code, lưu (Ctrl+S) rồi bấm F5.</text>'
  + step(30, 62, 1) + step(374, 130, 2), 'IDLE: cửa sổ Shell (trái) và cửa sổ soạn code (phải)')
PY_FIG4 = svg(700, 260, browser('colab.research.google.com',
  '<rect x="40" y="60" width="620" height="180" fill="#fff" stroke="#c9d6e2"/><rect x="60" y="80" width="40" height="40" rx="20" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/><polygon points="74,89 74,111 92,100" fill="#1a73e8"/>'
  '<rect x="112" y="80" width="520" height="40" fill="#f6f8fb" stroke="#c9d6e2"/><text x="124" y="105" font-family="monospace">print("Xin chào")</text><text x="112" y="150" font-family="monospace" fill="#2a8a4a">Xin chào</text>'
  '<text x="112" y="190" fill="#5b6773">Mở “Sổ tay mới”, gõ code vào ô, bấm nút ▶ bên trái ô để chạy.</text>' + step(80, 70, 1) + step(620, 100, 2)), 'Chạy Python trên trình duyệt với Google Colab (cần tài khoản Google)')

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


K1['caidat'] = lesson('Cài đặt · Chuẩn bị Scratch', 'Hai cách dùng Scratch: trên trình duyệt hoặc cài ứng dụng.',
  tsum('Mở được trình soạn Scratch, nhận biết 5 vùng giao diện, biết lưu và mở lại dự án', 'Máy tính (Windows hoặc macOS) có mạng; trình duyệt Chrome, Edge hoặc Firefox. Phụ huynh hỗ trợ nếu cần', 'Một dự án Scratch đã lưu thành tệp .sb3'),
  card(1, 'Chọn cách dùng', li(['<b>Cách 1 (nhanh nhất): dùng trên trình duyệt.</b> Không cần cài gì và không cần tài khoản để bắt đầu. Cần có mạng.', '<b>Cách 2: cài Scratch Desktop</b> (ứng dụng offline) từ trang <b>scratch.mit.edu/download</b>, dùng được khi không có mạng. Trên Windows có thể cài từ Microsoft Store.', 'Khuyên dùng cách 1 để bắt đầu; muốn học không cần mạng thì cài thêm cách 2.']) + note('Chỉ tải phần mềm từ trang chính thức <b>scratch.mit.edu</b>. Không tải Scratch từ trang lạ vì có thể kèm phần mềm độc hại.')),
  card(2, 'Mở trình soạn Scratch', li(['<b>Bước 1:</b> mở trình duyệt, gõ <b>scratch.mit.edu</b> lên thanh địa chỉ.', '<b>Bước 2:</b> bấm nút <b>Tạo</b> (Create) trên thanh màu xanh. Trình soạn Scratch sẽ mở ra.', 'Nếu giao diện đang bằng tiếng Anh, bấm hình quả địa cầu ở góc trên và chọn <b>Tiếng Việt</b>.']) + fig(SC_FIG1, 'Hình 1. Vào scratch.mit.edu và bấm nút Tạo. (Hình minh họa; giao diện thật có thể khác đôi chút.)')),
  card(3, 'Làm quen 5 vùng giao diện', li(['<b>1. Khối lệnh:</b> kho các khối màu để em kéo ra dùng.', '<b>2. Vùng ghép khối:</b> nơi xếp các khối thành chương trình.', '<b>3. Sân khấu:</b> nơi nhân vật chạy và vẽ.', '<b>4. Nút cờ xanh và nút dừng đỏ:</b> bấm cờ xanh để chạy, nút đỏ để dừng.', '<b>5. Danh sách nhân vật:</b> chọn, thêm hoặc xóa nhân vật.']) + fig(SC_FIG2, 'Hình 2. Năm vùng của trình soạn Scratch.')),
  card(4, 'Lưu và mở lại dự án', li(['Chọn <b>Tập tin → Lưu vào máy tính của bạn</b>. Tệp có đuôi <b>.sb3</b> sẽ nằm trong thư mục <b>Tải xuống</b>.', 'Muốn mở lại: <b>Tập tin → Tải lên từ máy tính của bạn</b> rồi chọn tệp .sb3.', 'Nên đặt tên có ý nghĩa, ví dụ <b>bai2-hinh-vuong.sb3</b>.']) + fig(SC_FIG3, 'Hình 3. Lưu và mở lại dự án.')),
  prac(5, 'Chương trình đầu tiên', 'Làm trong Scratch: kéo khối <b>khi bấm cờ xanh</b> và khối <b>tiến 10 bước</b> vào vùng ghép khối, ghép chúng lại rồi bấm cờ xanh. Sau đó lưu dự án với tên <b>cai-dat.sb3</b>.' + blocks('khi bấm cờ xanh\n  tiến 10 bước'), None,
       '<p>Nếu làm đúng, chú mèo nhích sang phải một đoạn nhỏ mỗi lần em bấm cờ xanh. Nếu không thấy gì: kiểm tra hai khối đã <b>dính vào nhau</b> chưa (khối dưới phải khớp sát khối trên). Mẹo: bấm cờ xanh nhiều lần để thấy mèo đi xa dần.</p>'))


# --- Bài 2: hình vuông (mô phỏng tổng góc quay) ---


# --- Bài 4: biến (trace) ---
def var_trace():
    d = 5; steps = [('đặt điểm = 5', d)]
    d += 3; steps.append(('thêm 3 vào điểm', d))
    d *= 2; steps.append(('đặt điểm = điểm × 2', d))
    d -= 4; steps.append(('thêm -4 vào điểm', d))
    return steps, d
VT, VF = var_trace()


def rev(n, add, mul):  # nghĩ một số, nhân mul, cộng add
    return None



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

P['caidat'] = lesson('Cài đặt · Chuẩn bị Python', 'Cài Python và chạy chương trình đầu tiên.',
  tsum('Cài được Python 3, mở IDLE, chạy được lệnh print; biết một cách dự phòng chạy Python trên trình duyệt', 'Máy tính Windows có mạng, quyền cài phần mềm (nhờ phụ huynh nếu máy không phải của bạn)', 'Một tệp <code>bai1.py</code> chạy được'),
  card(1, 'Python và IDLE', li(['<b>Python</b> là ngôn ngữ lập trình miễn phí.', '<b>IDLE</b> là chương trình soạn và chạy code đi kèm sẵn khi cài Python – đủ dùng cho toàn bộ khóa học.', 'Chỉ tải Python từ trang chính thức <b>python.org</b>.'])),
  card(2, 'Tải trình cài đặt', li(['<b>Bước 1:</b> mở trình duyệt, vào <b>python.org/downloads</b>.', '<b>Bước 2:</b> bấm nút vàng <b>Download Python 3.x.x</b> (số phiên bản có thể khác). Một tệp có đuôi <b>.exe</b> sẽ được tải về.']) + fig(PY_FIG1, 'Hình 1. Trang tải Python. (Hình minh họa; giao diện thật có thể khác đôi chút.)')),
  card(3, 'Cài đặt – chú ý ô PATH', li(['Bấm đúp vào tệp .exe vừa tải.', '<b>Tích ô “Add python.exe to PATH”</b> ở cuối cửa sổ <b>trước</b> khi bấm gì khác. Ô này giúp máy tìm thấy Python từ cửa sổ lệnh.', 'Bấm <b>Install Now</b> và đợi đến khi báo cài xong, rồi bấm Close.']) + fig(PY_FIG2, 'Hình 2. Tích ô PATH rồi bấm Install Now.') + note('Một số phiên bản mới có màn hình cài hơi khác hoặc không có ô PATH. Không sao: em vẫn dùng IDLE ở bước sau bình thường, không cần PATH.')),
  card(4, 'Mở IDLE và chạy thử', li(['Bấm nút Start của Windows, gõ <b>IDLE</b> rồi mở chương trình “IDLE (Python 3.x)”.', 'Cửa sổ <b>Shell</b> hiện ra với dấu <code>&gt;&gt;&gt;</code>. Gõ <code>print("Xin chào")</code> rồi Enter: nếu thấy chữ Xin chào là cài thành công.', 'Viết nhiều dòng: <b>File → New File</b>, gõ code, lưu thành <b>bai1.py</b> (Ctrl+S), rồi <b>Run → Run Module</b> hoặc bấm phím <b>F5</b>.']) + fig(PY_FIG3, 'Hình 3. IDLE: Shell bên trái, cửa sổ soạn code bên phải.') + code('print("Xin chào")', run('print("Xin chào")'))),
  card(5, 'Dự phòng: chạy trên trình duyệt', li(['Nếu không cài được Python, em có thể dùng <b>Google Colab</b> (colab.research.google.com), cần tài khoản Google.', 'Mở sổ tay mới, gõ code vào ô, bấm nút <b>▶</b> bên trái ô để chạy.', 'Cách này cần mạng và các dự án lưu trên tài khoản Google.']) + fig(PY_FIG4, 'Hình 4. Chạy Python trên Google Colab.')),
  card(6, 'Gỡ rối thường gặp', li(['<b>Không thấy IDLE:</b> khởi động lại máy rồi tìm lại; nếu vẫn không có, cài lại Python.', '<b>Báo lỗi SyntaxError:</b> kiểm tra dấu ngoặc và dấu nháy đã đóng đủ chưa.', '<b>Chữ có dấu bị lỗi hiển thị:</b> lưu tệp ở dạng UTF-8 (mặc định của IDLE đã là UTF-8).'])),
  prac(7, 'Chương trình đầu tiên', 'Tạo tệp <code>bai1.py</code> in ra dòng chào có <b>tên của em</b> và dòng thứ hai in kết quả 12 × 12, rồi chạy bằng F5.', None,
       '<p>Ví dụ (thay tên của em):</p>' + code('print("Xin chào, mình là Lan")\nprint(12 * 12)', run('print("Xin chào, mình là Lan")\nprint(12 * 12)')) + note('Kết quả dòng thứ hai là 144. Nếu có lỗi, đọc dòng báo lỗi cuối cùng: nó cho biết dòng nào sai.')))


c2 = 'gia = 25000\nsl = 3\ntong = gia * sl\nsl = sl + 2\nprint(tong)\nprint(gia * sl)'

c3 = 'def xep_loai(d):\n    if d >= 8:\n        return "Giỏi"\n    elif d >= 5:\n        return "Khá"\n    else:\n        return "Yếu"\nfor d in [10, 8, 7.9, 5, 4.9, 0]:\n    print(d, xep_loai(d))'

c4 = 'tong = 0\nfor i in range(1, 11):\n    tong += i\nprint(tong)'
c4b = 'for i in range(1, 6):\n    print(i)'
c4c = 'print(sum(range(1, 100)))'

dl = '5\n9\n2\n9\n7\n3\n'
c5 = 'def lon_nhat(ds):\n    kq = ds[0]\n    for x in ds:\n        if x > kq:\n            kq = x\n    return kq\n\nds = [5, 9, 2, 9, 7, 3]\nprint(lon_nhat(ds))\nprint(ds.count(9))\nprint(sum(ds) / len(ds))'

c6 = 'def xuoi(n):\n    return (n * 3 + 4) * 2\n\ndef nguoc(kq):\n    return (kq // 2 - 4) // 3\n\nprint(xuoi(7))\nprint(nguoc(xuoi(7)))'
c6b = 'ket_qua = 0\nfor n in range(1, 1000):\n    if n * n + n == 156:\n        ket_qua = n\n        break\nprint(ket_qua)'
c6c = 'n = 156\nx = 12\nprint(x * (x + 1) == n)'
c6d = 'ds = "tuduy"\nprint(ds[::-1])'

c7 = 'def trung_binh(ds):\n    return sum(ds) / len(ds)\n\nprint(trung_binh([4, 6, 8]))'
c7b = 'def trung_binh(ds):\n    return sum(ds) / len(ds)\n\nassert trung_binh([4, 6, 8]) == 6\nassert trung_binh([5]) == 5\nassert trung_binh([0, 10]) == 5\nprint("Tất cả test đều qua")'
c7c = 'def so_chan(ds):\n    dem = 0\n    for x in ds:\n        if x % 2 == 0:\n            dem += 1\n    return dem\nprint(so_chan([1, 2, 3, 4, 6]))'

ds8 = 'Ăn uống\t450000\nĂn uống\t380000\nHọc tập\t300000\nGiải trí\t150000\nHọc tập\t220000\nGiải trí\t90000'
c8 = 'du_lieu = [("Ăn uống", 450000), ("Ăn uống", 380000), ("Học tập", 300000),\n           ("Giải trí", 150000), ("Học tập", 220000), ("Giải trí", 90000)]\ntong = {}\nfor muc, so_tien in du_lieu:\n    tong[muc] = tong.get(muc, 0) + so_tien\nfor muc in tong:\n    print(muc, tong[muc])\nprint("Tổng:", sum(tong.values()))'

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tuduy_k811, tuduy_py
K1.update(tuduy_k811.build())
P.update(tuduy_py.build())
ORDER = ['tongquan', 'caidat', 'bai1', 'bai2', 'bai3', 'bai4', 'bai5', 'bai6', 'bai7', 'bai8']
OUT = {'k811': {k: K1[k] for k in ORDER}, 'k1218': {k: P[k] for k in ORDER}}
js = '// Sinh bởi tools/build-tu-duy.py – đừng sửa tay.\nwindow.TUDUY = ' + json.dumps(OUT, ensure_ascii=False, indent=1) + ';\n'
open(os.path.join(os.path.dirname(__file__), '..', 'renderer', 'tu-duy-content.js'), 'w', encoding='utf-8').write(js)
print('ok', {k: len(v) for k, v in OUT.items()})
