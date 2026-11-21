#!/usr/bin/env python3
"""Chuyển bản nháp courses/gia-su-ai/index.html (giáo án lên lớp) thành bài học tự học trong app.
Ghi renderer/gia-su-ai-content.js (window.GIA_SU_AI). Chạy: python3 tools/build-gia-su-ai.py"""
import re, json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'courses/gia-su-ai/index.html').read_text(encoding='utf8')
secs = dict(re.findall(r'<section id="([^"]+)"[^>]*>(.*?)</section>', src, flags=re.S))
ORDER = [('tong-quan', 'tongquan'), ('buoi1', 'bai1'), ('buoi2', 'bai2'), ('buoi3', 'bai3'), ('buoi4', 'bai4'),
         ('buoi5', 'bai5'), ('buoi6', 'bai6'), ('buoi7', 'bai7'), ('buoi8', 'bai8'), ('phu-luc', 'phuluc')]

# Mỗi cặp (cũ, mới) phải khớp đúng; chuyển từ giáo án lớp học sang tự học trên phần mềm.
PATCH = {
 'tong-quan': [
  ('<b>Ví dụ dùng trong buổi học</b>', '<b>Ví dụ dùng trong bài học</b>'),
  ('Mỗi bài có khung <b>“Theo độ tuổi”</b> ghi rõ phần dành cho từng nhóm. Giáo viên linh hoạt: các em 12–15 làm phần cơ bản, các em 16–18 làm thêm phần nâng cao.',
   'Mỗi bài có khung <b>“Theo độ tuổi”</b> ghi rõ phần dành cho từng nhóm tuổi. Em 12–15 tuổi làm phần cơ bản, em 16–18 tuổi làm thêm phần nâng cao.'),
  ('Giáo viên chọn một công cụ chat AI mà cơ sở đã kiểm tra, đồng thời cho học sinh biết mỗi công cụ có quy định riêng về độ tuổi.',
   'Em chọn một công cụ chat AI phù hợp với độ tuổi của mình, cùng người lớn; mỗi công cụ có quy định riêng về độ tuổi.'),
  ('<div class="lbl">Lưu ý cho trung tâm</div><p>Quy định độ tuổi, tính năng và giá của công cụ AI thay đổi thường xuyên. Trước mỗi khóa, giáo viên kiểm tra lại trang trợ giúp chính thức của công cụ. Nếu em dưới độ tuổi tối thiểu, em chỉ xem giáo viên trình diễn hoặc dùng cùng phụ huynh trên tài khoản của phụ huynh, theo đúng điều khoản. Nếu cơ sở không có mạng cho mọi em, vẫn dạy được bằng cách giáo viên trình chiếu và các em làm trên phiếu giấy.</p>',
   '<div class="lbl">Lưu ý về công cụ AI</div><p>Quy định độ tuổi, tính năng và giá của công cụ AI thay đổi thường xuyên. Trước khi bắt đầu, em và người lớn đọc lại trang trợ giúp chính thức của công cụ. Nếu em dưới độ tuổi tối thiểu, em chỉ dùng cùng phụ huynh trên tài khoản của phụ huynh, theo đúng điều khoản. Khi chưa có mạng hoặc chưa có tài khoản, em vẫn học được các phần lý thuyết và làm các bài tập ghi vào vở.</p>'),
 ],
 'buoi1': [
  ('Giáo viên đọc nửa câu: “Hôm nay trời mưa nên em phải mang…”. Cả lớp đoán từ tiếp theo. Hầu hết đều nói “ô” hoặc “áo mưa”. Hỏi:',
   'Đọc nửa câu này và đoán từ tiếp theo: “Hôm nay trời mưa nên em phải mang…”. Hầu hết mọi người đều nghĩ ngay “ô” hoặc “áo mưa”. Hãy tự hỏi:'),
  ('<i>Để tiết kiệm thời gian lớp, nên giao Phần A làm ở nhà cùng phụ huynh trước buổi học (hoặc làm trong 10 phút nếu đã có tài khoản). Dành phần lớn 40 phút thực hành cho Phần B.</i>',
   '<i>Phần A chỉ làm một lần, cùng phụ huynh. Nếu đã có tài khoản, em chuyển thẳng sang Phần B.</i>'),
  ('dùng chung với phụ huynh hoặc xem trình diễn của giáo viên.', 'chỉ dùng chung với phụ huynh, trên tài khoản của phụ huynh.'),
  ('hoặc giáo viên chiếu ảnh chụp một trường hợp AI bịa đã lưu sẵn từ trước buổi học. Giáo viên nên chạy thử bước này trước vì mỗi AI phản ứng khác nhau.',
   'hoặc tìm trên mạng một ví dụ “AI bịa” đã được báo chí nói đến để xem. Mỗi AI phản ứng khác nhau nên kết quả của em có thể khác.'),
 ],
 'buoi2': [
  ('<div><b>Chuẩn bị</b>Phiếu tình huống (trong bài này), bút màu xanh, vàng, đỏ</div>', '<div><b>Chuẩn bị</b>Tình huống ngay trong bài này; bút màu xanh, vàng, đỏ</div>'),
  ('Khai mở tư duy · Thảo luận nhóm</div><p>Chia nhóm, mỗi nhóm bốc một tình huống thực tế (ví dụ: “Bạn nhờ cậu gửi đáp án bài toán đã hỏi AI”). Nhóm tô màu xanh / vàng / đỏ và phải <b>giải thích lý do bằng một câu có chữ “vì”</b>. Nhóm khác phản biện.</p>',
   'Khai mở tư duy · Tự phân loại</div><p>Đọc một tình huống thực tế (ví dụ: “Bạn nhờ cậu gửi đáp án bài toán đã hỏi AI”). Tô màu xanh / vàng / đỏ và <b>giải thích lý do bằng một câu có chữ “vì”</b>. Sau đó kể tình huống cho một người nhà và hỏi họ có đồng ý không.</p>'),
  ('Giáo viên đưa 6 thẻ, ví dụ: mật khẩu,', 'Em tự viết ra 6 thẻ thông tin, ví dụ: mật khẩu,'),
  ('Mỗi em tô xanh, vàng hoặc đỏ rồi đổi phiếu với bạn để đối chiếu.', 'Tô xanh, vàng hoặc đỏ cho từng thẻ rồi đối chiếu với bảng ở trên.'),
  ('Làm theo cặp: một em đóng người lạ gọi “mẹ nhờ chuyển tiền gấp”, một em áp dụng 4 bước DỪNG – GÁC MÁY – HỎI RIÊNG – BÁO NGƯỜI LỚN. Đổi vai.',
   'Nhờ một người nhà (hoặc một bạn) đóng người lạ gọi “mẹ nhờ chuyển tiền gấp”, em áp dụng 4 bước DỪNG – GÁC MÁY – HỎI RIÊNG – BÁO NGƯỜI LỚN. Sau đó đổi vai.'),
  ('<b>Bốc thăm tình huống (20 phút).</b> Nhóm tô màu xanh / vàng / đỏ và giải thích bằng một câu có chữ “vì”. Nhóm khác phản biện.',
   '<b>Phân loại tình huống.</b> Đọc từng tình huống trong phần thảo luận, tô xanh / vàng / đỏ và giải thích bằng một câu có chữ “vì”. Đổi ý kiến với một người nhà nếu có thể.'),
  ('nhấn mạnh phần dữ liệu cá nhân, lừa đảo và nhờ người lớn. Đóng vai tình huống ngắn. 16–18: thêm thảo luận về', 'nhấn mạnh phần dữ liệu cá nhân, lừa đảo và nhờ người lớn. Đóng vai tình huống ngắn. 16–18: thêm phần tìm hiểu về'),
 ],
 'buoi4': [
  ('<b>Trình bày 2 phút</b> với bạn: AI nói gì, em kiểm chứng ra sao, em kết luận gì.', '<b>Kể lại</b> cho một người nhà: AI nói gì, em kiểm chứng ra sao, em kết luận gì.'),
  ('<b>Trình bày 2 phút</b> với bạn: AI nói gì, em kiểm ra sao, kết luận gì.', '<b>Kể lại</b> cho một người nhà: AI nói gì, em kiểm ra sao, kết luận gì.'),
 ],
 'buoi6': [
  ('(nếu cơ sở có hai công cụ)', '(nếu em có hai công cụ)'),
 ],
 'buoi7': [
  ('Nhật ký lỗi ghi hôm nay là đầu vào của buổi học ngày mai', 'Nhật ký lỗi ghi hôm nay là đầu vào của lần học ngày mai'),
  ('để trống ít nhất một buổi.', 'để trống ít nhất một ngày.'),
  ('Để trống ít nhất một buổi.', 'Để trống ít nhất một ngày.'),
  ('<b>Xếp mỗi lỗ hổng vào 2–3 buổi ngắn</b> (25–45 phút)', '<b>Xếp mỗi lỗ hổng vào 2–3 lần học ngắn</b> (25–45 phút)'),
  ('<b>Xếp mỗi lỗ hổng vào 2–3 buổi ngắn</b> theo chu trình', '<b>Xếp mỗi lỗ hổng vào 2–3 lần học ngắn</b> theo chu trình'),
  ('buổi học 25–30 phút, có người lớn xem lại', 'mỗi lần học 25–30 phút, có người lớn xem lại'),
 ],
 'buoi8': [
  ('1. Bài trình bày 3 phút của mỗi học sinh', '1. Bài trình bày 3 phút của em'),
  ('Giáo viên đưa một câu trả lời của AI có chứa một lỗi cài sẵn (sai số, nguồn không có thật hoặc kết luận quá chắc). Em tìm lỗi, nêu cách kiểm chứng và sửa.',
   'Nhờ một người nhà sửa kín một lỗi vào câu trả lời của AI (đổi một con số, thêm một nguồn không có thật hoặc viết kết luận quá chắc) rồi đưa lại cho em. Em tìm lỗi, nêu cách kiểm chứng và sửa.'),
  ('Ghi lại và kể cho thầy cô nghe ở buổi gặp sau.', 'Ghi lại và kể cho thầy cô hoặc người nhà nghe.'),
 ],
}
# Xóa các khối chỉ dành cho lớp học / giáo viên
CUT = {
 'tong-quan': [r'<h3>Cách tổ chức</h3>\s*<div class="meta">(?:\s*<div>.*?</div>)+\s*</div>'],
 'phu-luc': [r'<h3>C\. Gợi ý dành cho giáo viên / trung tâm</h3>\s*<ul>.*?</ul>'],
}
PHULUC_PATCH = [
  ('<h3>D. Nguồn tham khảo', '<h3>C. Nguồn tham khảo'),
  ('<div class="lbl">Cần xác minh trước khi dạy</div><p>Các quy định pháp luật, độ tuổi và tính năng công cụ trong tài liệu này được tổng hợp tại thời điểm biên soạn (tháng 11/2026) và có thể đã thay đổi. Trung tâm nên đối chiếu văn bản gốc, nhất là các điều khoản về trẻ em và dữ liệu cá nhân, trước khi đưa vào giảng dạy chính thức.</p>',
   '<div class="lbl">Cần xác minh</div><p>Các quy định pháp luật, độ tuổi và tính năng công cụ trong tài liệu này được tổng hợp tại thời điểm biên soạn (tháng 11/2026) và có thể đã thay đổi. Em và người lớn nên đối chiếu văn bản gốc, nhất là các điều khoản về trẻ em và dữ liệu cá nhân.</p>'),
]
PATCH['phu-luc'] = PHULUC_PATCH

def process(sid, h):
    t = re.search(r'<h2>(.*?)</h2>', h, flags=re.S).group(1).strip()
    sub = re.search(r'<p class="sub">(.*?)</p>', h, flags=re.S)
    sub = sub.group(1).strip() if sub else ''
    body = re.sub(r'\s*<h2>.*?</h2>', '', h, count=1, flags=re.S)
    body = re.sub(r'\s*<p class="sub">.*?</p>', '', body, count=1, flags=re.S)
    # bỏ ô "Thời gian" (thời lượng lên lớp)
    body = re.sub(r'\s*<div><b>Thời gian</b>.*?</div>', '', body, flags=re.S)
    for pat in CUT.get(sid, []):
        body, n = re.subn(pat, '', body, flags=re.S)
        assert n == 1, ('CUT', sid, pat)
    for old, new in PATCH.get(sid, []):
        assert old in body, ('PATCH', sid, old[:60])
        body = body.replace(old, new)
    # bỏ thời lượng trong ngoặc: (5 phút) / (15 phút, không dùng AI)
    body = re.sub(r'\s*\(\d+ phút\)', '', body)
    body = re.sub(r'\((\d+) phút, ', '(', body)
    body = re.sub(r'<figure>', '<figure class="aiw-fig">', body)
    body = re.sub(r'\bbạn\b(?! bè| thân| cùng| nhờ| học)', 'em', body)
    return t, sub, body.strip()

out = {}
for sid, key in ORDER:
    t, sub, body = process(sid, secs[sid])
    out[key] = {'title': t, 'sub': sub, 'html': body}
text = ' '.join(re.sub(r'<[^>]+>', ' ', v['html']) for v in out.values())
for bad in ['Giáo viên', 'giáo viên', 'Cả lớp', 'cả lớp', 'buổi', 'Chia nhóm', 'trung tâm', 'cơ sở', 'phiếu giấy']:
    if bad in text: print('CÒN:', bad, re.findall(r'.{40}' + bad + r'.{40}', text)[:3])
js = '// Giáo trình Gia sư AI (8 bài + tổng quan + phụ lục), tự học trên phần mềm.\n// Sinh bởi tools/build-gia-su-ai.py từ courses/gia-su-ai/index.html; đừng sửa tay.\nwindow.GIA_SU_AI = ' + json.dumps(out, ensure_ascii=False, indent=1) + ';\n'
(ROOT / 'renderer/gia-su-ai-content.js').write_text(js, encoding='utf8')
print({k: len(v['html']) for k, v in out.items()})
