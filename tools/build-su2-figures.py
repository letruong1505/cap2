# Lịch sử 6, 8, 9 (đợt 2): dòng thời gian, sơ đồ so sánh, nhóm ý, biểu đồ thanh thời gian.
# Chỉ dựng từ các mốc và dữ kiện có trong chính bài học; không có bản đồ, không có ảnh.
import sys, os, json, glob, textwrap, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

_spec = importlib.util.spec_from_file_location('su1', os.path.join(os.path.dirname(__file__), 'build-su-figures.py'))
su1 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(su1)
timeline, find = su1.timeline, su1.find

NAVY = '#1a56a0'
HEAD = ['#4e79a7', '#f28e2b', '#59a14f', '#b07aa1']
SOFT = ['#e8f1fa', '#fdf1e0', '#e6f0df', '#efe6f3']


def wrap(s, n):
    return textwrap.wrap(s, n) or ['']


def groups(ttl, cols, note=None, W=720, size=12.5):
    """cols: [(tiêu đề, [ý, ...])]; mỗi ý được tự xuống dòng."""
    n = len(cols)
    gap = 14
    cw = (W - 28 - gap * (n - 1)) / n
    cpl = int((cw - 26) / (size * 0.52))
    blocks = []
    for head, items in cols:
        ls = []
        for it in items:
            w = wrap(it, cpl)
            ls.append(['• ' + w[0]] + ['  ' + x for x in w[1:]])
        blocks.append((head, ls))
    maxl = max(sum(len(i) for i in ls) for _, ls in blocks)
    lh = size + 5
    hh = 36
    ch = hh + 14 + maxl * lh + 10 + 4 * max(len(ls) for _, ls in blocks)
    H = 52 + ch + (36 if note else 14)
    b = [title(W, ttl)]
    for k, (head, ls) in enumerate(blocks):
        x = 14 + k * (cw + gap)
        b.append(R(x, 44, cw, ch, fill=SOFT[k % 4], stroke=HEAD[k % 4], sw=2, rx=8))
        b.append('<path d="M%.1f,%.1f h%.1f v%.1f h-%.1f z" fill="%s" opacity="0"/>' % (x, 44, 0, 0, 0, HEAD[k % 4]))
        b.append(R(x, 44, cw, hh, fill=HEAD[k % 4], stroke=HEAD[k % 4], sw=2, rx=8))
        b.append(T(x + cw / 2, 44 + 23, head, size=14, weight='bold', fill='white'))
        y = 44 + hh + 22
        for item in ls:
            for ln in item:
                b.append(T(x + 12, y, ln, size=size, anchor='start'))
                y += lh
            y += 4
    if note:
        for i, ln in enumerate(wrap(note, 96)):
            b.append(T(W / 2, 44 + ch + 24 + i * 17, ln, size=12.5, weight='bold', fill=NAVY))
        H += 17 * (len(wrap(note, 96)) - 1)
    return svg(W, int(H), ''.join(b))


def compare(ttl, head, rows, widths, W=720, size=12.5):
    xs = [14]
    for w in widths:
        xs.append(xs[-1] + w)
    b = [title(W, ttl)]
    y = 44
    for k, h in enumerate(head):
        b.append(R(xs[k], y, widths[k], 32, fill=HEAD[0] if k else '#dbe7f3', stroke=INK, sw=1.2))
        b.append(T(xs[k] + widths[k] / 2, y + 21, h, size=14, weight='bold', fill='white' if k else INK))
    y += 32
    for r, row in enumerate(rows):
        cells = [wrap(c, int((widths[k] - 16) / (size * 0.52))) for k, c in enumerate(row)]
        hh = max(len(c) for c in cells) * (size + 5) + 12
        for k, c in enumerate(cells):
            b.append(R(xs[k], y, widths[k], hh, fill=LGREY if k == 0 else ('white' if r % 2 else '#f7fafd'), stroke=GREY, sw=1))
            for i, ln in enumerate(c):
                b.append(T(xs[k] + 8, y + 18 + i * (size + 5), ln, size=size, anchor='start', weight='bold' if k == 0 else 'normal'))
        y += hh
    return svg(W, int(y + 14), ''.join(b))


def flow(ttl, boxes, note=None, W=720):
    n = len(boxes)
    gap = 44
    bw = (W - 28 - gap * (n - 1)) / n
    cpl = int((bw - 20) / 6.4)
    cells = [(h, [x for l in ls for x in wrap(l, cpl)]) for h, ls in boxes]
    bh = 40 + max(len(c[1]) for c in cells) * 18 + 14
    b = [title(W, ttl)]
    for k, (h, ls) in enumerate(cells):
        x = 14 + k * (bw + gap)
        b.append(R(x, 50, bw, bh, fill=SOFT[k % 4], stroke=HEAD[k % 4], sw=2.5, rx=10))
        b.append(T(x + bw / 2, 50 + 26, h, size=15, weight='bold', fill=INK))
        for i, ln in enumerate(ls):
            b.append(T(x + bw / 2, 50 + 50 + i * 18, ln, size=12.5, fill='#3b4856'))
        if k < n - 1:
            b.append(L(x + bw + 6, 50 + bh / 2, x + bw + gap - 6, 50 + bh / 2, stroke=INK, w=3, arrow=True))
    H = 50 + bh + (34 if note else 18)
    if note:
        b.append(T(W / 2, 50 + bh + 24, note, size=12.5, weight='bold', fill=NAVY))
    return svg(W, int(H), ''.join(b))


def pyramid(ttl, levels, note=None, W=720):
    n = len(levels)
    lh = 64
    top_w, bot_w = 300, 640
    b = [title(W, ttl)]
    for k, (h, d) in enumerate(levels):
        y = 48 + k * lh
        w1 = top_w + (bot_w - top_w) * k / n
        w2 = top_w + (bot_w - top_w) * (k + 1) / n
        pts = [(W / 2 - w1 / 2, y), (W / 2 + w1 / 2, y), (W / 2 + w2 / 2, y + lh - 4), (W / 2 - w2 / 2, y + lh - 4)]
        b.append(POLY(pts, fill=SOFT[k % 4], stroke=HEAD[k % 4], sw=2.5))
        b.append(T(W / 2, y + 26, h, size=15, weight='bold'))
        b.append(T(W / 2, y + 46, d, size=12.5, fill='#3b4856'))
    H = 48 + n * lh + (34 if note else 12)
    if note:
        b.append(T(W / 2, H - 12, note, size=12.5, weight='bold', fill=NAVY))
    return svg(W, int(H), ''.join(b))


def gantt(ttl, rows, y0, y1, step, note=None, W=720):
    lw = 190
    x0, x1 = lw + 20, W - 24
    fx = lambda y: x0 + (y - y0) / (y1 - y0) * (x1 - x0)
    n = len(rows)
    H = 52 + n * 44 + 50 + (22 if note else 0)
    b = [title(W, ttl)]
    yb = 52 + n * 44
    v = y0
    while v <= y1:
        b.append(L(fx(v), 48, fx(v), yb, stroke='#e1e7ee', w=1)); b.append(T(fx(v), yb + 18, str(v), size=12))
        v += step
    b.append(L(x0, yb, x1, yb, stroke=INK, w=2))
    for k, (lab, a, c) in enumerate(rows):
        y = 52 + k * 44
        b.append(T(lw + 8, y + 24, lab, size=12.5, anchor='end', weight='bold'))
        if a == c:
            b.append(POLY([(fx(a), y + 8), (fx(a) + 8, y + 20), (fx(a), y + 32), (fx(a) - 8, y + 20)], fill=RED, stroke=INK, sw=1.5))
            b.append(T(fx(a) + 14, y + 25, str(a), size=12, anchor='start', fill=NAVY, weight='bold'))
        else:
            b.append(R(fx(a), y + 8, fx(c) - fx(a), 24, fill=HEAD[k % 4], stroke=INK, sw=1.2, rx=4))
            b.append(T(fx(a) - 5, y + 25, str(a), size=12, anchor='end', fill=NAVY, weight='bold'))
            b.append(T(fx(c) + 5, y + 25, str(c), size=12, anchor='start', fill=NAVY, weight='bold'))
    if note:
        b.append(T(W / 2, H - 8, note, size=12, fill='#55606d'))
    return svg(W, int(H), ''.join(b))


# ====== nội dung ======
FIG = []  # (môn, bài, tên file, hàm vẽ, chú thích)


def add(subj, bai, tag, fn, cap):
    FIG.append((subj, bai, 'su2-%s-b%d-%s.svg' % (subj, bai, tag), fn, cap))


def tl(subj, bai, ttl, events, cap, h=330):
    add(subj, bai, 'tl', lambda: timeline(ttl, events, h), cap)


# ---- Lịch sử 6 ----
add('lichsu6', 2, 'nhom', lambda: groups('Các loại tư liệu lịch sử', [
    ('Tư liệu truyền miệng', ['Lời kể truyền từ đời này sang đời khác', 'Truyền thuyết, ca dao, tục ngữ']),
    ('Tư liệu hiện vật', ['Di tích, đồ vật người xưa để lại trong lòng đất hay trên mặt đất', 'Trống đồng, đồ gốm, công cụ đá']),
    ('Tư liệu chữ viết', ['Bản ghi, sách in, khắc, chép tay còn lưu lại', 'Bia đá, sắc phong, sách sử'])],
    note='Tư liệu gốc: ra đời vào thời điểm sự kiện diễn ra, là nguồn đáng tin cậy nhất.'), 'Các loại tư liệu lịch sử')
add('lichsu6', 4, 'flow', lambda: flow('Quá trình tiến hoá của loài người', [
    ('Vượn người', ['Cách đây khoảng 5 – 6 triệu năm']),
    ('Người tối cổ', ['Khoảng 4 triệu năm trước', 'Đi bằng hai chân, biết chế tạo công cụ']),
    ('Người tinh khôn', ['Khoảng 150 000 năm trước', 'Cơ thể như người ngày nay'])]), 'Vượn người → Người tối cổ → Người tinh khôn')
add('lichsu6', 5, 'flow', lambda: flow('Hai giai đoạn của xã hội nguyên thuỷ', [
    ('Bầy người nguyên thuỷ', ['Thời Người tối cổ', 'Sống theo bầy, có người đứng đầu']),
    ('Công xã thị tộc', ['Thời Người tinh khôn', 'Gồm các gia đình có quan hệ huyết thống', 'Nhiều thị tộc hợp thành bộ lạc', 'Làm chung, hưởng chung'])]),
    'Hai giai đoạn của xã hội nguyên thuỷ')
tl('lichsu6', 6, 'Kim loại và sự phân hoá xã hội', [
    ('Thiên niên kỉ IV TCN', ['Phát hiện đồng đỏ,', 'sau đó đồng thau']),
    ('Đầu thiên niên kỉ I TCN', ['Biết chế tạo đồ sắt']),
    ('Thế kỉ VII TCN – thế kỉ I', ['Văn hoá Đông Sơn', '(Việt Nam)'])], 'Dòng thời gian: các kim loại', 300)
add('lichsu6', 7, 'sosanh', lambda: compare('Ai Cập và Lưỡng Hà cổ đại', ['', 'Ai Cập', 'Lưỡng Hà'], [
    ['Vị trí', 'Đông Bắc châu Phi, có sông Nin', 'Giữa sông Ơ-phrát và sông Ti-grơ (Tây Á)'],
    ['Nhà nước', 'Khoảng năm 3200 TCN vua Mê-nét thống nhất; người đứng đầu là Pha-ra-ông', 'Người Xu-me lập các thành bang khoảng thiên niên kỉ IV TCN; đứng đầu là En-xi'],
    ['Chữ viết', 'Chữ tượng hình, viết trên giấy pa-pi-rút', 'Chữ hình nêm trên đất sét'],
    ['Thành tựu', 'Hình học, hệ đếm thập phân, kim tự tháp, ướp xác', 'Hệ đếm 60, lịch âm, vườn treo Ba-bi-lon, Bộ luật Ham-mu-ra-bi']], [110, 290, 290]),
    'So sánh Ai Cập và Lưỡng Hà')
add('lichsu6', 8, 'dang-cap', lambda: pyramid('Chế độ đẳng cấp (vác-na) ở Ấn Độ cổ đại', [
    ('Bra-man', 'Tăng lữ'), ('Ksa-tri-a', 'Quý tộc, chiến binh'),
    ('Vai-si-a', 'Nông dân, thương nhân, thợ thủ công'), ('Su-đra', 'Người lao động nghèo')],
    note='Quy định rất khắt khe giữa các đẳng cấp.'), 'Bốn đẳng cấp ở Ấn Độ cổ đại')
tl('lichsu6', 9, 'Trung Quốc từ cổ đại đến thế kỉ VII', [
    ('Ra đời sớm', ['Các nhà nước Hạ, Thương, Chu']),
    ('Năm 221 TCN', ['Nhà Tần thống nhất; Tần Thuỷ', 'Hoàng xưng hoàng đế']),
    ('Sau nhà Tần', ['Hán, Tam quốc, Tấn,', 'Nam – Bắc triều']),
    ('Đến năm 618', ['Nhà Tuỳ'])], 'Các triều đại Trung Quốc', 300)
add('lichsu6', 10, 'nhom', lambda: groups('Hy Lạp và La Mã cổ đại', [
    ('Hy Lạp', ['Tổ chức theo thành bang (A-ten, Xpác-ta)', 'A-ten: nền dân chủ chủ nô, có Đại hội nhân dân']),
    ('La Mã', ['Từ nhà nước cộng hoà chuyển sang đế chế (năm 27 TCN)', 'Đứng đầu đế chế là hoàng đế'])],
    note='Cả hai nằm ven Địa Trung Hải, thuận lợi thủ công nghiệp và thương nghiệp đường biển.'), 'Tổ chức nhà nước Hy Lạp và La Mã')
add('lichsu6', 11, 'nhom', lambda: groups('Các quốc gia sơ kì ở Đông Nam Á', [
    ('Ở Việt Nam', ['Văn Lang – Âu Lạc', 'Chăm-pa', 'Phù Nam']),
    ('Lưu vực sông Mê Nam', ['Đva-ra-va-ti']),
    ('Hải đảo', ['Ka-la-ta', 'Ma-lay-u', 'Tô-ra-ma'])],
    note='Ra đời từ những thế kỉ tiếp giáp đầu Công nguyên, nhờ sử dụng đồ sắt.'), 'Các quốc gia sơ kì')
add('lichsu6', 12, 'nhom', lambda: groups('Các vương quốc phong kiến (thế kỉ VII – X)', [
    ('Lục địa', ['Chân Lạp', 'Chăm-pa']),
    ('Hải đảo', ['Sri Vi-giay-a', 'Ka-lin-ga', 'Ma-ta-ram'])],
    note='Thế kỉ VII: Sri Vi-giay-a kiểm soát eo biển Ma-lắc-ca; Chân Lạp thôn tính Phù Nam.'), 'Các vương quốc phong kiến Đông Nam Á')
add('lichsu6', 13, 'nhom', lambda: groups('Giao lưu văn hoá ở Đông Nam Á', [
    ('Tiếp thu từ Ấn Độ', ['Tôn giáo: Hin-đu giáo, Phật giáo', 'Chữ Phạn, cải biên thành chữ viết riêng', 'Sử thi Ra-ma-y-a-na', 'Kiến trúc đền tháp']),
    ('Tiếp thu từ Trung Quốc', ['Nho giáo, chữ Hán, kĩ thuật', 'Chủ yếu ở Việt Nam']),
    ('Kết quả', ['Tiếp thu có chọn lọc, kết hợp với văn hoá bản địa', 'Ví dụ: đền tháp Chăm, khu đền Bô-rô-bu-đua'])]),
    'Giao lưu văn hoá ở Đông Nam Á')
add('lichsu6', 15, 'nhom', lambda: groups('Chính sách cai trị của phương Bắc (từ năm 179 TCN đến năm 938)', [
    ('Chính trị', ['Chia nước ta thành các quận, huyện', 'Sáp nhập vào lãnh thổ Trung Quốc']),
    ('Kinh tế', ['Bóc lột nặng nề bằng tô thuế', 'Cống nạp sản vật quý', 'Nắm độc quyền muối, sắt']),
    ('Văn hoá', ['Đưa người Hán sang ở', 'Truyền bá Nho giáo, chữ Hán', 'Truyền bá phong tục Hán nhằm đồng hoá'])]),
    'Chính sách cai trị thời Bắc thuộc')
add('lichsu6', 17, 'nhom', lambda: groups('Bảo tồn và tiếp thu văn hoá', [
    ('Giữ gìn văn hoá dân tộc', ['Tiếng nói của tổ tiên', 'Phong tục: ăn trầu, nhuộm răng, xăm mình, búi tóc', 'Tục thờ cúng tổ tiên, thờ các anh hùng; lễ hội', 'Làng xã là nơi lưu giữ, bảo tồn']),
    ('Tiếp thu có chọn lọc văn hoá Trung Hoa', ['Chữ Hán (đọc theo cách người Việt)', 'Nho giáo, Phật giáo, Đạo giáo', 'Kĩ thuật làm giấy, thuỷ tinh…'])]),
    'Bảo tồn và tiếp thu văn hoá thời Bắc thuộc')
add('lichsu6', 19, 'nhom', lambda: groups('Vương quốc Chăm-pa', [
    ('Kinh tế', ['Trồng lúa nước trên ruộng bậc thang, làm guồng nước', 'Khai thác lâm sản (trầm hương, ngà voi)', 'Đánh cá, buôn bán đường biển, làm gốm']),
    ('Văn hoá', ['Chữ viết bắt nguồn từ chữ Phạn', 'Hin-đu giáo và Phật giáo', 'Đền tháp (Mỹ Sơn, tháp Pô Na-ga)', 'Tục hoả táng người chết'])],
    note='Năm 192: Khu Liên lập nước Lâm Ấp, sau đổi là Chăm-pa.'), 'Kinh tế và văn hoá Chăm-pa')
tl('lichsu6', 20, 'Vương quốc Phù Nam', [
    ('Khoảng thế kỉ I', ['Thành lập, trên cơ sở', 'văn hoá Óc Eo']),
    ('Thế kỉ III – V', ['Phát triển mạnh']),
    ('Thế kỉ VII', ['Bị Chân Lạp thôn tính'])], 'Dòng thời gian Phù Nam', 300)

# ---- Lịch sử 8 ----
tl('lichsu8', 1, 'Cách mạng tư sản Anh và chiến tranh giành độc lập ở Bắc Mỹ', [
    ('Năm 1642', ['Bắt đầu cách mạng', 'tư sản Anh']),
    ('Năm 1649', ['Vua Sác-lơ I bị xử tử,', 'Anh thành cộng hoà']),
    ('Năm 1688', ['“Cách mạng vinh quang”,', 'quân chủ lập hiến']),
    ('Năm 1775', ['Bắt đầu chiến tranh giành', 'độc lập ở Bắc Mỹ']),
    ('4/7/1776', ['Thông qua Tuyên ngôn', 'Độc lập']),
    ('Năm 1783', ['Anh công nhận độc lập', 'của Hợp chúng quốc Mỹ'])], 'Dòng thời gian: Anh và Bắc Mỹ', 340)
tl('lichsu8', 2, 'Cách mạng tư sản Pháp', [
    ('14/7/1789', ['Tấn công pháo đài –', 'nhà tù Ba-xti']),
    ('Tháng 8/1789', ['Tuyên ngôn Nhân quyền', 'và Dân quyền']),
    ('Năm 1792', ['Nền Cộng hoà', 'thứ nhất']),
    ('1793 – 1794', ['Chuyên chính Gia-cô-banh,', 'cách mạng lên đỉnh cao'])], 'Dòng thời gian Cách mạng Pháp', 320)
tl('lichsu8', 3, 'Một số thành tựu của Cách mạng công nghiệp', [
    ('Năm 1764', ['Máy kéo sợi Gien-ni', '(Giêm Ha-gri-vơ)']),
    ('Năm 1784', ['Máy hơi nước', '(Giêm Oát)']),
    ('Năm 1785', ['Máy dệt chạy bằng sức', 'nước (Ét-mơn Các-rai)']),
    ('Năm 1807', ['Tàu thuỷ chạy bằng hơi', 'nước (Phơn-tơn)']),
    ('Năm 1814', ['Đầu máy xe lửa', '(Xti-phen-xơn)'])], 'Dòng thời gian các phát minh', 330)
tl('lichsu8', 5, 'Nam – Bắc triều và Trịnh – Nguyễn', [
    ('Năm 1527', ['Mạc Đăng Dung', 'lập nhà Mạc']),
    ('Năm 1533', ['Nguyễn Kim lập Nam triều;', 'bắt đầu Nam – Bắc triều']),
    ('Năm 1592', ['Kết thúc chiến tranh', 'Nam – Bắc triều']),
    ('Năm 1627', ['Bắt đầu chiến tranh', 'Trịnh – Nguyễn']),
    ('Năm 1672', ['Kết thúc chiến tranh', 'Trịnh – Nguyễn'])], 'Dòng thời gian xung đột Nam – Bắc triều và Trịnh – Nguyễn', 330)
tl('lichsu8', 6, 'Khai phá vùng đất phía Nam', [
    ('Năm 1558', ['Nguyễn Hoàng vào', 'trấn thủ Thuận Hoá']),
    ('Năm 1611', ['Lập phủ Phú Yên']),
    ('Năm 1653', ['Lập dinh Thái Khang', '(Khánh Hoà)']),
    ('Năm 1698', ['Nguyễn Hữu Cảnh', 'lập phủ Gia Định']),
    ('Năm 1757', ['Cơ bản xác lập chủ quyền', 'trên vùng đất Nam Bộ'])], 'Dòng thời gian khai phá phương Nam', 330)
add('lichsu8', 7, 'gantt', lambda: gantt('Các cuộc khởi nghĩa nông dân ở Đàng Ngoài', [
    ('Nguyễn Dương Hưng', 1737, 1737), ('Lê Duy Mật', 1738, 1770), ('Nguyễn Danh Phương', 1740, 1751),
    ('Nguyễn Hữu Cầu', 1741, 1751), ('Hoàng Công Chất', 1739, 1769)], 1735, 1775, 5,
    note='Mỗi thanh là thời gian diễn ra một cuộc khởi nghĩa.'), 'Thời gian các cuộc khởi nghĩa')
tl('lichsu8', 11, 'Phong trào công nhân quốc tế', [
    ('Năm 1848', ['Tuyên ngôn của', 'Đảng Cộng sản']),
    ('Năm 1864', ['Thành lập Quốc tế', 'thứ nhất']),
    ('18/3 – 28/5/1871', ['Công xã Pa-ri', '(tồn tại 72 ngày)']),
    ('1/5/1886', ['Công nhân Mỹ đình công', 'đòi ngày làm 8 giờ']),
    ('Năm 1889', ['Thành lập Quốc tế', 'thứ hai'])], 'Dòng thời gian phong trào công nhân', 330)
tl('lichsu8', 12, 'Chiến tranh thế giới thứ nhất và Cách mạng tháng Mười Nga', [
    ('Năm 1882', ['Khối Liên minh (Đức,', 'Áo – Hung, I-ta-li-a)']),
    ('Năm 1907', ['Khối Hiệp ước', '(Anh, Pháp, Nga)']),
    ('28/6/1914', ['Thái tử Áo – Hung bị', 'ám sát ở Xéc-bi']),
    ('7/11/1917', ['Cách mạng tháng Mười', 'Nga (theo lịch mới)']),
    ('Năm 1918', ['Chiến tranh kết thúc,', 'phe Liên minh thất bại'])], 'Dòng thời gian CTTG thứ nhất', 340)
tl('lichsu8', 13, 'Một số phát minh kĩ thuật', [
    ('Năm 1837', ['Điện báo', '(Moóc-xơ)']),
    ('Năm 1876', ['Điện thoại', '(Graham Bell)']),
    ('Năm 1879', ['Bóng đèn', '(Ê-đi-xơn)']),
    ('Năm 1903', ['Máy bay', '(anh em Rai-tơ)'])], 'Dòng thời gian các phát minh', 320)
tl('lichsu8', 14, 'Trung Quốc và Nhật Bản', [
    ('1840 – 1842', ['Chiến tranh thuốc phiện', '(Trung Quốc)']),
    ('Năm 1868', ['Thiên hoàng Minh Trị', 'cải cách (Nhật Bản)']),
    ('1904 – 1905', ['Chiến tranh Nga – Nhật']),
    ('Năm 1911', ['Cách mạng Tân Hợi, lật đổ', 'triều Mãn Thanh (Trung Quốc)'])], 'Dòng thời gian Trung Quốc và Nhật Bản', 320)
tl('lichsu8', 15, 'Ấn Độ và Đông Nam Á', [
    ('Năm 1885', ['Ấn Độ: thành lập', 'Đảng Quốc đại']),
    ('1896 – 1898', ['Cách mạng Phi-líp-pin,', 'thành lập Cộng hoà']),
    ('1905 – 1908', ['Ấn Độ: đấu tranh', 'chống chia cắt Ben-gan'])], 'Dòng thời gian Ấn Độ và Đông Nam Á', 300)
tl('lichsu8', 16, 'Việt Nam dưới thời Nguyễn', [
    ('Năm 1802', ['Nguyễn Ánh lên ngôi', '(Gia Long), lập nhà Nguyễn']),
    ('Năm 1804', ['Đặt quốc hiệu', 'Việt Nam']),
    ('Năm 1816', ['Đội Hoàng Sa ra', 'cắm mốc']),
    ('1831 – 1832', ['Minh Mạng chia cả nước', 'thành 30 tỉnh, phủ Thừa Thiên']),
    ('1833 – 1836', ['Dựng bia chủ quyền,', 'xây chùa, trồng cây trên đảo']),
    ('Năm 1838', ['Đổi quốc hiệu', 'thành Đại Nam'])], 'Dòng thời gian thời Nguyễn', 340)
add('lichsu8', 18, 'gantt', lambda: gantt('Phong trào chống Pháp 1885 – 1896 và khởi nghĩa Yên Thế', [
    ('Phong trào Cần vương', 1885, 1896), ('Khởi nghĩa Ba Đình', 1886, 1887), ('Khởi nghĩa Bãi Sậy', 1883, 1892),
    ('Khởi nghĩa Hương Khê', 1885, 1896), ('Khởi nghĩa Yên Thế', 1884, 1913)], 1880, 1915, 5,
    note='Mỗi thanh là thời gian diễn ra phong trào hay khởi nghĩa.'), 'Thời gian các cuộc khởi nghĩa')
tl('lichsu8', 19, 'Phong trào yêu nước đầu thế kỉ XX', [
    ('Năm 1904', ['Phan Bội Châu lập', 'Hội Duy tân']),
    ('1905 – 1908', ['Phong trào Đông du']),
    ('Năm 1906', ['Duy tân ở Trung Kì', '(Phan Châu Trinh)']),
    ('Năm 1908', ['Chống thuế ở Trung Kì']),
    ('5/6/1911', ['Nguyễn Tất Thành rời', 'bến cảng Nhà Rồng']),
    ('Năm 1912', ['Việt Nam Quang', 'phục hội']),
    ('Năm 1917', ['Người trở lại Pháp'])], 'Dòng thời gian phong trào yêu nước', 340)

# ---- Lịch sử 9 ----
tl('lichsu9', 1, 'Nước Nga và Liên Xô (1918 – 1945)', [
    ('1918 – 1920', ['Chống thù trong giặc ngoài;', 'Chính sách cộng sản thời chiến']),
    ('Năm 1921', ['Chính sách kinh tế mới', '(NEP)']),
    ('Tháng 12/1922', ['Thành lập Liên Xô']),
    ('1925 – 1941', ['Xây dựng chủ nghĩa xã hội:', 'công nghiệp hoá, tập thể hoá'])], 'Dòng thời gian Liên Xô', 320)
tl('lichsu9', 2, 'Châu Âu và nước Mỹ (1918 – 1945)', [
    ('1918 – 1923', ['Phong trào cách mạng', 'bùng nổ ở châu Âu']),
    ('Tháng 3/1919', ['Thành lập Quốc tế', 'Cộng sản']),
    ('1929 – 1933', ['Đại suy thoái kinh tế', '(bắt đầu từ Mỹ)']),
    ('Năm 1933', ['Hít-le lên nắm', 'quyền ở Đức'])], 'Dòng thời gian châu Âu và Mỹ', 320)
tl('lichsu9', 3, 'Châu Á (1918 – 1945)', [
    ('4/5/1919', ['Phong trào Ngũ tứ', '(Trung Quốc)']),
    ('Năm 1920', ['Đảng cộng sản', 'In-đô-nê-xi-a']),
    ('Năm 1921', ['Đảng Cộng sản', 'Trung Quốc thành lập']),
    ('Năm 1930', ['Đảng cộng sản', 'Việt Nam']),
    ('Năm 1931', ['Nhật xâm lược', 'Trung Quốc']),
    ('1937 – 1945', ['Trung Quốc kháng', 'chiến chống Nhật']),
    ('1940 – 1942', ['Nhật chiếm', 'Đông Nam Á'])], 'Dòng thời gian châu Á', 340)
tl('lichsu9', 5, 'Phong trào dân tộc dân chủ 1918 – 1930', [
    ('Năm 1919', ['Chấn hưng nội hoá,', 'bài trừ ngoại hoá']),
    ('Năm 1923', ['Chống độc quyền', 'cảng Sài Gòn']),
    ('Năm 1925', ['Đòi thả Phan Bội Châu']),
    ('8/1925', ['Bãi công thợ máy', 'xưởng Ba Son']),
    ('Năm 1926', ['Để tang', 'Phan Châu Trinh']),
    ('Năm 1927', ['Thành lập Việt Nam', 'Quốc dân đảng']),
    ('2/1930', ['Khởi nghĩa Yên Bái', '(thất bại)'])], 'Dòng thời gian 1918 – 1930', 340)
tl('lichsu9', 7, 'Phong trào cách mạng 1930 – 1939', [
    ('1930 – 1931', ['Phong trào cách mạng;', 'Xô viết Nghệ – Tĩnh']),
    ('Tháng 10/1930', ['Đổi tên Đảng thành Đảng Cộng', 'sản Đông Dương; Luận cương']),
    ('1936 – 1939', ['Phong trào dân chủ;', 'Mặt trận Dân chủ Đông Dương'])], 'Dòng thời gian 1930 – 1939', 300)
tl('lichsu9', 10, 'Liên Xô và Đông Âu (1945 – 1991)', [
    ('1945 – 1950', ['Liên Xô khôi phục', 'kinh tế']),
    ('Năm 1949', ['Chế tạo thành công', 'bom nguyên tử']),
    ('Năm 1957', ['Phóng vệ tinh nhân', 'tạo đầu tiên']),
    ('Năm 1961', ['Ga-ga-rin bay', 'vào vũ trụ']),
    ('Năm 1985', ['Gooc-ba-chốp', 'tiến hành cải tổ']),
    ('Năm 1989', ['Chế độ XHCN ở', 'Đông Âu sụp đổ']),
    ('25/12/1991', ['Liên Xô tan rã'])], 'Dòng thời gian Liên Xô và Đông Âu', 340)
tl('lichsu9', 11, 'Mỹ và Tây Âu (1945 – 1991)', [
    ('1945 – 1950', ['Mỹ chiếm hơn 1/2 sản lượng', 'công nghiệp thế giới']),
    ('Năm 1957', ['Thành lập Cộng đồng', 'Kinh tế châu Âu (EEC)']),
    ('Năm 1967', ['Thành lập Cộng đồng', 'châu Âu (EC)']),
    ('Năm 1993', ['Trở thành Liên minh', 'châu Âu (EU)'])], 'Dòng thời gian Mỹ và Tây Âu', 320)
tl('lichsu9', 12, 'Mỹ La-tinh và châu Á (1945 – 1991)', [
    ('15/8/1947', ['Ấn Độ giành độc lập']),
    ('1/10/1949', ['Thành lập nước Cộng hoà', 'Nhân dân Trung Hoa']),
    ('26/1/1950', ['Thành lập nước', 'Cộng hoà Ấn Độ']),
    ('1/1/1959', ['Cách mạng Cu-ba', 'thắng lợi']),
    ('8/8/1967', ['Thành lập ASEAN', '(5 thành viên)']),
    ('Năm 1978', ['Trung Quốc cải cách,', 'mở cửa'])], 'Dòng thời gian Mỹ La-tinh và châu Á', 340)
tl('lichsu9', 13, 'Việt Nam trong năm đầu sau Cách mạng tháng Tám', [
    ('8/9/1945', ['Thành lập Nha', 'Bình dân học vụ']),
    ('23/9/1945', ['Pháp gây hấn', 'ở Sài Gòn']),
    ('6/1/1946', ['Tổng tuyển cử', 'bầu Quốc hội']),
    ('6/3/1946', ['Hiệp định Sơ bộ']),
    ('14/9/1946', ['Tạm ước'])], 'Dòng thời gian 1945 – 1946', 330)
tl('lichsu9', 19, 'ASEAN mở rộng', [
    ('Năm 1995', ['Việt Nam gia nhập', 'ASEAN']),
    ('Năm 1997', ['Lào và Mi-an-ma', 'gia nhập ASEAN']),
    ('Năm 1999', ['Cam-pu-chia gia nhập;', 'ASEAN có 10 thành viên']),
    ('Năm 2015', ['Thành lập Cộng đồng ASEAN', '(ba trụ cột)'])], 'Dòng thời gian ASEAN', 320)
tl('lichsu9', 20, 'Việt Nam từ năm 1976 đến nay', [
    ('25/4/1976', ['Tổng tuyển cử bầu', 'Quốc hội chung cả nước']),
    ('Tháng 12/1986', ['Đại hội VI: đường lối', 'Đổi mới toàn diện']),
    ('Năm 1991', ['Bình thường hoá quan hệ', 'với Trung Quốc']),
    ('Năm 1995', ['Quan hệ với Mỹ;', 'gia nhập ASEAN']),
    ('Năm 1998', ['Gia nhập APEC']),
    ('Năm 2007', ['Gia nhập WTO']),
    ('Năm 2008', ['Ra khỏi nhóm nước', 'thu nhập thấp'])], 'Dòng thời gian từ 1976 đến nay', 340)
tl('lichsu9', 21, 'Cách mạng khoa học – kĩ thuật', [
    ('Những năm 1940', ['Bắt đầu cách mạng khoa học', '– kĩ thuật lần thứ hai']),
    ('Năm 1969', ['Con người đặt chân', 'lên Mặt Trăng']),
    ('Năm 2003', ['Bản đồ gen người'])], 'Dòng thời gian khoa học – kĩ thuật', 300)


if __name__ == '__main__':
    for subj, bai, nm, fn, cap in FIG:
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf8').write(fn())
        p = find(subj, bai)
        data = json.load(open(p, encoding='utf8'))
        attach(subj, os.path.relpath(p, os.path.join(ROOT, 'content', subj)), len(data['theory']) - 1, nm, cap)
    print('su2: %d hình' % len(FIG))
