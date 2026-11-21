"""Bài tổng kết cho lớp Gemini (Bài 12) và lớp ChatGPT (Bài 13) của khóa AI cho người đi làm. Dạng thẻ, có dự án cuối bằng dữ liệu giả lập kèm đáp án."""
import html
e = html.escape

def ul(items): return '<ul class="tl">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def table(head, rows): return '<div class="tbl-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (''.join('<th>%s</th>' % h for h in head), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows))
def prompt(t, x): return '<div class="ptitle">%s</div><pre class="prompt">%s</pre>' % (t, e(x))
def data(t, x): return '<div class="ptitle">%s</div><pre class="pdata">%s</pre>' % (t, e(x))

def lesson(kind):
    g = kind == 'gemini'
    name = 'Gemini' if g else 'ChatGPT'
    no = 12 if g else 13
    parts, n = [], [0]
    def card(t, body, cls=''):
        n[0] += 1; parts.append('<section class="tcard%s"><h4><span class="tn">%d</span>%s</h4>%s</section>' % (cls, n[0], t, body))
    parts.append('<div class="tsum"><div class="tsum-l">Tóm tắt bài</div><ul><li><b>Học xong bài này:</b> Nhìn lại cả lớp %s, tự đánh giá năng lực theo 4 mức và hoàn thành một gói hồ sơ cuối bằng dữ liệu giả lập</li><li><b>Chuẩn bị:</b> Nhật ký sử dụng AI và các câu lệnh Anh/Chị đã lưu từ các bài trước</li><li><b>Sản phẩm:</b> Phiếu tự đánh giá, gói hồ sơ cuối, kế hoạch 30 ngày tiếp theo</li></ul></div>' % name)
    parts.append('<h3 class="tchap">Tổng kết lớp %s</h3>' % name)
    if g:
        takeaways = ['<b>Bài 4:</b> AI làm tốt tóm tắt, soạn nháp, viết công thức; không tự đảm bảo tính toán bằng lời, số hiệu pháp luật mới, quyết định có trách nhiệm. Quy trình 4 bước: đầu vào sạch, giao việc có cấu trúc, kiểm tra chéo, lưu thành mẫu.',
            '<b>Bài 5:</b> Câu lệnh R-C-T-F (vai trò, bối cảnh, nhiệm vụ, định dạng); thêm mẫu, chia nhỏ việc, cho AI hỏi lại tối đa 3 câu.',
            '<b>Bài 6:</b> Văn phòng: tóm tắt chuỗi email, thư xin gia hạn, biên bản và bảng giao việc, ưu tiên đầu việc.',
            '<b>Bài 7:</b> Kế toán: công thức SUMIFS/QUERY, đối chiếu, rà bất thường; mọi kết quả phải kiểm tra trên chứng từ gốc.',
            '<b>Bài 8:</b> Hành chính: văn bản đúng thể thức, SOP, so sánh báo giá, checklist sự kiện.',
            '<b>Bài 9:</b> Hệ sinh thái Google: Side Panel, lệnh @, NotebookLM có trích dẫn nguồn.',
            '<b>Bài 10:</b> Quy tắc 3 không, ẩn danh trước khi dán, kiểm duyệt đầu ra 3 bước.',
            '<b>Bài 11:</b> Lộ trình 4 tuần, nhật ký, thư viện 16 câu lệnh.']
    else:
        takeaways = ['<b>Bài 4:</b> Vai trò của ChatGPT là trợ lý soạn nháp và phân tích; việc cần trách nhiệm do người làm. Thiết lập an toàn trước khi dán dữ liệu.',
            '<b>Bài 5:</b> Khung BRIEF-7 và quy trình 6 bước: giao việc, soạn, so, sửa, duyệt, lưu.',
            '<b>Bài 6:</b> Email theo mục đích hành động, báo cáo một trang, SOP.',
            '<b>Bài 7:</b> Excel: làm sạch bảng, giải thích công thức, đối chiếu, báo cáo KPI có kiểm chứng.',
            '<b>Bài 8:</b> Dàn ý PowerPoint, họp từ chuẩn bị đến theo dõi hành động, quản lý lịch.',
            '<b>Bài 9:</b> Hành chính, nhân sự, mua hàng: hồ sơ, quy trình, so sánh báo giá.',
            '<b>Bài 10:</b> Dự án, nghiên cứu nguồn, kiểm chứng tài liệu quy định, tệp đính kèm và Projects.',
            '<b>Bài 11:</b> Năm case study và lộ trình 30 ngày.',
            '<b>Bài 12:</b> Thư viện 96 prompt, checklist, phiếu giao việc, nhật ký dùng AI.']
    card('Những điều cần nhớ sau cả lớp', ul(takeaways))
    card('Ba nguyên tắc không bao giờ bỏ', ul(['<b>Đầu vào sạch:</b> ẩn danh, chỉ đưa phần dữ liệu cần thiết, không đưa CCCD, số tài khoản, bảng lương, mật khẩu.', '<b>Giao việc rõ:</b> ' + ('R-C-T-F' if g else 'BRIEF-7') + ', có điều kiện nghiệm thu, cho phép AI ghi [CẦN BỔ SUNG] thay vì bịa.', '<b>Người ký chịu trách nhiệm:</b> kiểm dữ kiện và con số, kiểm nghiệp vụ và pháp lý, chỉnh giọng văn trước khi gửi.']))
    rows = [['An toàn dữ liệu', 'Tự ẩn danh trước khi dán, nhận ra dữ liệu không được đưa vào AI', 'Lập quy tắc và nhắc người khác trong nhóm'],
            ['Giao việc có cấu trúc', 'Câu lệnh đủ ' + ('R-C-T-F' if g else '7 trường BRIEF-7') + ' và tiêu chí nghiệm thu', 'Có mẫu giao việc dùng chung cho cả phòng'],
            ['Kiểm chứng và phản biện', 'Đối chiếu mọi con số, ngày, tên riêng với nguồn gốc', 'Có checklist kiểm duyệt và dạy lại được cho người khác'],
            ['Email và văn bản', 'Bản AI soạn chỉ cần sửa nhỏ, không có thông tin bịa', 'Giữ được giọng văn riêng qua văn bản mẫu'],
            ['Bảng tính và số liệu', 'Công thức AI viết chạy đúng, kết quả khớp tính tay', 'Tự phát hiện bất thường và nêu câu hỏi kiểm tra chứng từ gốc'],
            ['Họp và đầu việc', 'Tách quyết định, việc cần làm, ý kiến chưa chốt, điều chưa rõ', 'Có bảng theo dõi chạy đều hằng tuần'],
            ['Dùng lại và chia sẻ', 'Lưu được 5 câu lệnh tốt nhất', 'Thư viện chung cả phòng, được cập nhật định kỳ']]
    if g: rows.insert(6, ['Hệ sinh thái Google', 'Dùng Side Panel và lệnh @ với phạm vi rõ ràng', 'Dựng kho tra cứu NotebookLM và kiểm tra trích dẫn gốc'])
    else: rows.insert(6, ['Dự án và nghiên cứu nguồn', 'Kiểm chứng nguồn, dùng tệp đính kèm có kiểm soát', 'Dựng Projects riêng cho từng mảng việc'])
    card('Phiếu tự đánh giá năng lực (thang 1–4)', '<p>Chấm từng dòng: <b>1</b> mới biết · <b>2</b> làm được khi có hướng dẫn · <b>3</b> tự làm tốt (cột giữa) · <b>4</b> hướng dẫn được người khác (cột phải). Ghi bằng chứng: một sản phẩm cụ thể Anh/Chị đã làm.</p>' + table(['Năng lực', 'Dấu hiệu đạt mức 3', 'Dấu hiệu đạt mức 4'], rows)
         + '<div class="ttry"><span class="ttry-l">Thử ngay</span><p>Chép bảng vào sổ tay, chấm điểm và ghi bằng chứng. Mục nào dưới 3 thì chọn đúng một bài để làm lại trong tuần này.</p></div>')
    if g:
        notes = 'GHI CHÚ TUẦN (Phòng Kho – Vận chuyển)\n- Hoàn thành: nhập 120 đơn hàng (kế hoạch 150); kiểm kê kho khu A và B.\n- Vướng mắc: khu C chưa kiểm kê vì anh Tuấn nghỉ phép 2 ngày.\n- Tuần tới: kiểm kê khu C trước 25/11 (Tuấn); gửi 3 báo giá vận chuyển trước 24/11 (Mai).'
        cost = 'Khoản mục\tTuần này (đ)\tTuần trước (đ)\nVận chuyển\t4200000\t3900000\nVăn phòng phẩm\t600000\t650000\nTiếp khách\t1800000\t900000'
        p1 = 'Bạn là chuyên viên điều phối. Từ ghi chú tuần và bảng chi phí dưới đây (đã ẩn danh), hãy: (1) lập báo cáo tuần 1 trang gồm Việc đã hoàn thành, Việc vướng mắc cần hỗ trợ, Kế hoạch tuần tới; (2) tính tỷ lệ hoàn thành đơn hàng và tổng chi phí hai tuần, mức tăng giảm từng khoản; (3) soạn email dưới 120 từ gửi trưởng phòng kèm báo cáo. Không tự nêu nguyên nhân hay ngày không có trong dữ liệu; thiếu thì ghi [CẦN BỔ SUNG]. Nếu thiếu thông tin, hỏi lại tôi tối đa 3 câu trước khi làm.\n\n[dán ghi chú và bảng]'
        ans = ul(['<b>Tỷ lệ hoàn thành đơn:</b> 120/150 = 80%.', '<b>Chi phí:</b> tuần này 4.200.000 + 600.000 + 1.800.000 = 6.600.000; tuần trước 3.900.000 + 650.000 + 900.000 = 5.450.000; tăng 1.150.000 (21,10%). Tiếp khách +100% (900.000 → 1.800.000); vận chuyển +7,69%; văn phòng phẩm −7,69%.', '<b>Việc cần có trong báo cáo:</b> hoàn thành (120/150 đơn, kiểm kê A và B), vướng mắc (khu C chưa kiểm kê do Tuấn nghỉ phép 2 ngày), tuần tới (Tuấn – khu C – 25/11; Mai – 3 báo giá – 24/11).', '<b>Email:</b> dưới 120 từ, nêu đính kèm báo cáo, nhấn mạnh 2 điểm: đơn hàng đạt 80% kế hoạch và chi tiếp khách tăng gấp đôi; không tự giải thích nguyên nhân tăng chi.', '<b>Lỗi hay gặp:</b> AI tự thêm lý do “do dịp cuối năm” hoặc làm tròn 21,10% thành 20%.'])
    else:
        notes = 'GHI CHÚ HỌP RÀ KPI, 20/11/2026\n- Hành chính đề xuất thêm 1 nhân sự, chưa ai quyết.\n- Trưởng phòng quyết định: kiểm tra toàn bộ các việc trễ trong tuần tới.\n- Chị Hà gửi danh sách việc trễ trước 25/11.\n- Chưa rõ ngân sách cho nhân sự mới.'
        cost = 'Chỉ số\tTháng 10\tTháng 11\nYêu cầu nhận\t120\t130\nHoàn tất\t108\t117\nĐúng hạn (trong số hoàn tất)\t99\t105'
        p1 = 'Hãy đóng vai chuyên viên phân tích nội bộ. Dùng đúng dữ liệu KPI hai tháng và ghi chú họp dưới đây. Trước tiên lập từ điển 3 KPI (việc chưa hoàn tất = nhận – hoàn tất; tỷ lệ hoàn tất = hoàn tất/nhận; tỷ lệ đúng hạn = đúng hạn/hoàn tất) rồi tính từng tháng. Sau đó tạo báo cáo 1 trang: Tóm tắt điều hành – Bảng KPI – 3 nhận xét có bằng chứng – Điều chưa xác minh; biên bản tách [Ý KIẾN] – [QUYẾT ĐỊNH] – [HÀNH ĐỘNG]; và email gửi trưởng phòng dưới 120 từ. Không tự nêu nguyên nhân trễ, không tự thêm ngày. Cuối cùng cho bảng tự kiểm: yêu cầu – đạt/chưa – bằng chứng.\n\n[dán dữ liệu và ghi chú]'
        ans = ul(['<b>Tháng 10:</b> chưa hoàn tất 12; hoàn tất 108/120 = 90%; đúng hạn 99/108 = 91,67%.', '<b>Tháng 11:</b> chưa hoàn tất 13; hoàn tất 117/130 = 90%; đúng hạn 105/117 = 89,74%. Tỷ lệ đúng hạn giảm khoảng 1,9 điểm phần trăm dù số lượng tăng.', '<b>Biên bản:</b> Quyết định: kiểm tra toàn bộ việc trễ trong tuần tới. Hành động: Hà – gửi danh sách việc trễ – 25/11. Ý kiến chưa quyết: thêm 1 nhân sự. Điều chưa rõ: ngân sách nhân sự mới, ai chịu trách nhiệm kiểm tra việc trễ → [CẦN XÁC MINH].', '<b>Lỗi hay gặp:</b> viết “hiệu suất tăng” vì số lượng tăng; tự thêm nguyên nhân trễ; biến đề xuất thêm nhân sự thành quyết định.'])
    card('Dự án cuối: một gói hồ sơ hoàn chỉnh', '<p>Làm trọn một gói gồm báo cáo, tính toán và email bằng dữ liệu giả lập dưới đây. Tự làm phần tính trước, sau đó nhờ ' + name + ' và đối chiếu từng chỗ với đáp án.</p>'
         + data('DỮ LIỆU MẪU – ghi chú' + (' tuần' if g else ' họp'), notes) + data('DỮ LIỆU MẪU – ' + ('chi phí hai tuần' if g else 'KPI hai tháng'), cost) + prompt('PROMPT GỢI Ý', p1)
         + '<ol class="tl"><li>Tự tính các con số và phân loại ghi chú trên giấy.</li><li>Gửi prompt cho ' + name + ', đọc kết quả.</li><li>Chấm bằng bảng tự kiểm: có dòng nào AI tự thêm, có số nào lệch đáp án không? Yêu cầu sửa đúng chỗ rồi kiểm lại.</li></ol>'
         + '<details class="tans"><summary>Đáp án để tự đối chiếu (làm xong rồi hãy mở)</summary>' + ans + '</details><p class="tnote">Toàn bộ dữ liệu trong thẻ này là giả lập, dùng được an toàn với AI.</p>', ' tprac')
    card('Checklist 60 giây trước khi gửi', ul(['Mọi số tiền, ngày, tên riêng, mã hợp đồng đã đối chiếu với nguồn gốc?', 'Không còn thông tin bịa hay chỗ trống [CẦN BỔ SUNG] chưa xử lý?', 'Đúng người nhận, đúng thẩm quyền phê duyệt, đúng quy chế?', 'Không có dữ liệu nhạy cảm không cần thiết trong tệp đính kèm?', 'Giọng văn đúng phong cách của mình, bỏ câu mở đầu sáo rỗng?']))
    card('Kế hoạch 30 ngày tiếp theo', ul(['<b>Tuần 1:</b> chọn 3 việc lặp lại nhiều nhất, làm lại bằng câu lệnh chuẩn, ghi phút tiết kiệm.', '<b>Tuần 2:</b> làm một việc có số liệu và kiểm tra bằng tay; ghi lỗi AI mắc.', '<b>Tuần 3:</b> hướng dẫn một đồng nghiệp dùng một câu lệnh trong thư viện.', '<b>Tuần 4:</b> cập nhật thư viện: bỏ câu lệnh ít dùng, thêm câu lệnh mới; tự chấm lại phiếu đánh giá.', 'Giữ nhật ký 3 phút mỗi ngày. Nếu cột lỗi luôn trống, hãy kiểm tra kỹ hơn thay vì tin AI không sai.']))
    card('Lời kết', '<p>AI không thay thế sự cẩn trọng và trách nhiệm của Anh/Chị. Nó giải phóng thời gian khỏi thao tác lặp lại để dành cho phần việc cần tư duy và kết nối con người. Hãy bắt đầu từ một việc nhỏ, kiểm soát độ chính xác và bảo mật, rồi mở rộng dần.</p>')
    return {'title': 'Bài %d · Tổng kết lớp %s và dự án cuối' % (no, name), 'sub': 'Ôn lại điều cốt lõi, tự đánh giá năng lực, hoàn thành gói hồ sơ cuối và lập kế hoạch 30 ngày tiếp theo.', 'html': ''.join(parts)}
