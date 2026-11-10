# Lịch sử 6, 8, 9: trục thời gian dựng từ chính các mốc trong bài (không có bản đồ, không có ảnh).
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from figlib import *

NAVY = '#1a56a0'
COLS = ['#e8f1fa', '#fdf1e0']


def timeline(ttl, events, h=None):
    n = len(events)
    W = 720
    h = h or 330
    cy = h / 2 + 8
    b = [title(W, ttl)]
    b.append(L(30, cy, W - 30, cy, stroke=INK, w=3, arrow=True))
    cw = 190
    for _ in range(6):
        step = (W - cw - 16) / (n - 1) if n > 1 else 0
        cw = min(190, 2 * step - 8) if n > 1 else 220
    step = (W - cw - 16) / (n - 1) if n > 1 else 0
    for i, (yr, lines) in enumerate(events):
        x = 8 + cw / 2 + i * step if n > 1 else W / 2
        up = i % 2 == 0
        b.append(C(x, cy, 7, fill=RED, stroke=INK, w=1.6))
        ch = 22 + 16 * len(lines) + 8
        top = cy - 28 - ch if up else cy + 28
        b.append(L(x, cy + (-7 if up else 7), x, cy + (-28 if up else 28), stroke=GREY, w=1.4))
        bx = max(8, min(W - 8 - cw, x - cw / 2))
        b.append(R(bx, top, cw, ch, fill=COLS[i % 2], stroke=INK, sw=1.5, rx=8))
        b.append(T(bx + cw / 2, top + 20, yr, size=14, weight='bold', fill=RED))
        b.append(TL(bx + cw / 2, top + 38, lines, size=11.5, lh=16))
    return svg(W, int(h), ''.join(b))


SPEC = []


def reg(subj, bai, ttl, events, cap, h=None):
    SPEC.append((subj, bai, ttl, events, cap, h))


reg('lichsu6', 14, 'Nhà nước Văn Lang – Âu Lạc', [
    ('Khoảng thế kỉ VII TCN', ['Nhà nước Văn Lang', 'Hùng Vương, Phong Châu']),
    ('Năm 208 TCN', ['Thục Phán lập nước Âu Lạc,', 'đóng đô ở Phong Khê (Cổ Loa)']),
    ('Năm 179 TCN', ['Triệu Đà xâm chiếm Âu Lạc'])], 'Dòng thời gian: Văn Lang – Âu Lạc', 300)
reg('lichsu6', 16, 'Các cuộc khởi nghĩa tiêu biểu trước thế kỉ X', [
    ('Năm 40', ['Khởi nghĩa Hai Bà Trưng', '(Mê Linh); năm 43 bị đàn áp']),
    ('Năm 248', ['Khởi nghĩa Bà Triệu', '(Cửu Chân)']),
    ('Năm 542', ['Khởi nghĩa Lý Bí; năm 544', 'lên ngôi, nước Vạn Xuân']),
    ('Năm 713', ['Khởi nghĩa Mai Thúc Loan', '(Hoan Châu)']),
    ('Khoảng năm 776', ['Khởi nghĩa Phùng Hưng', '(Đường Lâm)'])], 'Dòng thời gian các cuộc khởi nghĩa', 330)
reg('lichsu6', 18, 'Bước ngoặt đầu thế kỉ X', [
    ('Năm 905', ['Khúc Thừa Dụ giành', 'quyền tự chủ']),
    ('Năm 931', ['Dương Đình Nghệ đánh', 'tan quân Nam Hán']),
    ('Năm 937', ['Kiều Công Tiễn giết', 'Dương Đình Nghệ']),
    ('Năm 938', ['Ngô Quyền thắng', 'trận Bạch Đằng']),
    ('Năm 939', ['Ngô Quyền xưng vương,', 'đóng đô Cổ Loa'])], 'Dòng thời gian đầu thế kỉ X', 330)
reg('lichsu8', 8, 'Phong trào Tây Sơn', [
    ('Năm 1771', ['Khởi nghĩa Tây Sơn']),
    ('Năm 1777', ['Lật đổ chúa Nguyễn']),
    ('Năm 1785', ['Rạch Gầm – Xoài Mút,', 'đánh tan quân Xiêm']),
    ('Năm 1786', ['Ra Bắc lật đổ', 'chính quyền chúa Trịnh']),
    ('Năm 1788', ['Nguyễn Huệ lên ngôi', 'hoàng đế (Quang Trung)']),
    ('Tết Kỷ Dậu 1789', ['Đại phá quân Thanh', '(Ngọc Hồi – Đống Đa)'])], 'Dòng thời gian phong trào Tây Sơn', 340)
reg('lichsu8', 17, 'Cuộc kháng chiến chống Pháp (1858 – 1884)', [
    ('1/9/1858', ['Pháp nổ súng', 'tấn công Đà Nẵng']),
    ('Năm 1859', ['Pháp đánh Gia Định']),
    ('Năm 1862', ['Hiệp ước Nhâm Tuất']),
    ('Năm 1867', ['Pháp chiếm ba tỉnh', 'miền Tây Nam Kì']),
    ('Năm 1873', ['Pháp đánh Bắc Kì lần 1;', 'thắng Cầu Giấy']),
    ('Năm 1882', ['Pháp đánh Bắc Kì lần 2;', 'Hà Nội thất thủ']),
    ('Năm 1883', ['Hiệp ước Hác-măng']),
    ('Năm 1884', ['Hiệp ước Pa-tơ-nốt'])], 'Dòng thời gian kháng chiến chống Pháp 1858–1884', 340)
reg('lichsu9', 4, 'Chiến tranh thế giới thứ hai (1939 – 1945)', [
    ('1/9/1939', ['Đức tấn công Ba Lan,', 'chiến tranh bùng nổ']),
    ('22/6/1941', ['Đức tấn công Liên Xô']),
    ('7/12/1941', ['Nhật tấn công Trân', 'Châu Cảng, Mỹ tham chiến']),
    ('Tháng 2/1943', ['Chiến thắng Xta-lin-grát', '(bước ngoặt)']),
    ('9/5/1945', ['Đức đầu hàng', 'không điều kiện']),
    ('6/8 và 9/8/1945', ['Mỹ ném bom nguyên tử', 'xuống Hi-rô-si-ma, Na-ga-xa-ki']),
    ('15/8/1945', ['Nhật đầu hàng,', 'chiến tranh kết thúc'])], 'Dòng thời gian Chiến tranh thế giới thứ hai', 340)
reg('lichsu9', 6, 'Hoạt động của Nguyễn Ái Quốc và thành lập Đảng', [
    ('Năm 1919', ['Gửi Bản yêu sách của', 'nhân dân An Nam']),
    ('Năm 1920', ['Đọc Luận cương của Lê-nin;', 'sáng lập Đảng Cộng sản Pháp']),
    ('Năm 1925', ['Thành lập Hội Việt Nam', 'Cách mạng Thanh niên']),
    ('Năm 1927', ['Xuất bản', 'Đường Kách mệnh']),
    ('Năm 1929', ['Ba tổ chức cộng sản', 'ra đời']),
    ('6/1 – 7/2/1930', ['Hội nghị hợp nhất,', 'thành lập Đảng Cộng sản VN'])], 'Dòng thời gian: từ 1919 đến thành lập Đảng 1930', 340)
reg('lichsu9', 8, 'Cách mạng tháng Tám năm 1945', [
    ('Tháng 5/1941', ['Thành lập', 'Mặt trận Việt Minh']),
    ('Tháng 12/1944', ['Đội Việt Nam Tuyên truyền', 'Giải phóng quân']),
    ('9/3/1945', ['Nhật đảo chính Pháp']),
    ('15/8/1945', ['Nhật đầu hàng;', 'Đảng phát động Tổng khởi nghĩa']),
    ('19/8 – 25/8', ['Hà Nội 19/8, Huế 23/8,', 'Sài Gòn 25/8']),
    ('30/8/1945', ['Vua Bảo Đại thoái vị']),
    ('2/9/1945', ['Tuyên ngôn Độc lập,', 'khai sinh nước VNDCCH'])], 'Dòng thời gian Cách mạng tháng Tám', 340)
reg('lichsu9', 9, 'Chiến tranh lạnh (1947 – 1989)', [
    ('Năm 1947', ['Học thuyết Tru-man;', 'kế hoạch Mác-san']),
    ('Năm 1949', ['Thành lập NATO;', 'Liên Xô – Đông Âu lập SEV']),
    ('Năm 1955', ['Tổ chức Hiệp ước', 'Vác-sa-va']),
    ('Tháng 12/1989', ['Man-ta: Liên Xô và Mỹ', 'tuyên bố chấm dứt Chiến tranh lạnh'])], 'Dòng thời gian Chiến tranh lạnh', 300)
reg('lichsu9', 14, 'Kháng chiến chống Pháp (1946 – 1950)', [
    ('Đêm 19/12/1946', ['Lời kêu gọi toàn quốc', 'kháng chiến']),
    ('Thu – đông 1947', ['Chiến dịch Việt Bắc,', 'phá sản kế hoạch “đánh nhanh thắng nhanh”']),
    ('Thu – đông 1950', ['Chiến dịch Biên giới,', 'khai thông đường liên lạc quốc tế'])], 'Dòng thời gian kháng chiến 1946–1950', 300)
reg('lichsu9', 15, 'Kháng chiến chống Pháp (1951 – 1954)', [
    ('Tháng 2/1951', ['Đại hội II của Đảng,', 'Đảng Lao động Việt Nam']),
    ('Năm 1953', ['Pháp đề ra kế hoạch Na-va;', 'ta tiến công Đông – Xuân']),
    ('13/3 – 7/5/1954', ['Chiến dịch Điện Biên Phủ']),
    ('21/7/1954', ['Hiệp định Giơ-ne-vơ,', 'giới tuyến vĩ tuyến 17'])], 'Dòng thời gian kháng chiến 1951–1954', 300)
reg('lichsu9', 16, 'Kháng chiến chống Mỹ (1954 – 1965)', [
    ('Sau năm 1954', ['Đất nước chia cắt', 'thành hai miền']),
    ('1959 – 1960', ['Phong trào Đồng khởi', '(Bến Tre 17/1/1960)']),
    ('20/12/1960', ['Mặt trận Dân tộc Giải', 'phóng miền Nam ra đời']),
    ('1961 – 1965', ['“Chiến tranh đặc biệt”;', 'Ấp Bắc (1/1963), Bình Giã (12/1964)'])], 'Dòng thời gian 1954–1965', 300)
reg('lichsu9', 17, 'Kháng chiến chống Mỹ (1965 – 1975)', [
    ('1965 – 1968', ['“Chiến tranh cục bộ”;', 'Vạn Tường, Tết Mậu Thân 1968']),
    ('1969 – 1973', ['“Việt Nam hoá chiến tranh”;', 'tiến công chiến lược 1972']),
    ('27/1/1973', ['Hiệp định Pa-ri,', 'Mỹ rút quân']),
    ('Mùa Xuân 1975', ['Ba chiến dịch: Tây Nguyên,', 'Huế – Đà Nẵng, Hồ Chí Minh']),
    ('30/4/1975', ['Miền Nam hoàn toàn', 'giải phóng'])], 'Dòng thời gian 1965–1975', 330)


def trucs_thoi_gian():
    b = [title(720, 'Trục thời gian: trước Công nguyên và Công nguyên')]
    cy = 130
    b.append(L(30, cy, 690, cy, stroke=INK, w=3, arrow=True))
    b.append(L(360, cy - 22, 360, cy + 22, stroke=RED, w=3))
    b.append(T(360, cy - 30, 'Năm 1 CN', size=14, weight='bold', fill=RED))
    b.append(T(200, cy - 30, 'Trước Công nguyên (TCN)', size=13, weight='bold', fill=NAVY)); b.append(T(540, cy - 30, 'Công nguyên (CN)', size=13, weight='bold', fill=NAVY))
    b.append(T(200, cy + 46, '← càng xa, năm TCN càng lớn', size=12.5, fill='#3b4856')); b.append(T(540, cy + 46, 'năm càng lớn → càng gần hiện tại', size=12.5, fill='#3b4856'))
    b.append(T(360, 210, 'Không có năm 0', size=14, weight='bold', fill=RED))
    b.append(TL(360, 240, ['Thế kỉ I: năm 1 – 100; thế kỉ XXI: năm 2001 – 2100', '1 thập kỉ = 10 năm; 1 thế kỉ = 100 năm; 1 thiên niên kỉ = 1 000 năm'], size=12.5, lh=18, fill='#3b4856'))
    return svg(720, 285, ''.join(b))


def find(subj, bai):
    hits = glob.glob(os.path.join(ROOT, 'content', subj, '*', '*', 'bai-%d' % bai, '*.json'))
    assert len(hits) == 1, (subj, bai, hits)
    return hits[0]


if __name__ == '__main__':
    FIG = {}
    plan = []
    FIG['su-lichsu6-b3-truc.svg'] = trucs_thoi_gian()
    plan.append(('lichsu6', 3, 'su-lichsu6-b3-truc.svg', 'Trục thời gian TCN – CN'))
    for subj, bai, ttl, ev, cap, h in SPEC:
        nm = 'su-%s-b%d-tl.svg' % (subj, bai)
        FIG[nm] = timeline(ttl, ev, h)
        plan.append((subj, bai, nm, cap))
    byS = {}
    for subj, bai, nm, cap in plan:
        d = os.path.join(ROOT, 'content', subj, 'figures'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf8').write(FIG[nm])
        p = find(subj, bai)
        data = json.load(open(p, encoding='utf8'))
        attach(subj, os.path.relpath(p, os.path.join(ROOT, 'content', subj)), len(data['theory']) - 1, nm, cap)
    print('su: %d hình' % len(plan))
