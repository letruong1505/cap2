#!/usr/bin/env python3
"""Thêm thẻ "Thực hành với dữ liệu mẫu" (dữ liệu giả lập + prompt có nút Sao chép + đáp án để tự đối chiếu) vào Bài 4–9 lớp ChatGPT.
Chạy lặp lại an toàn (bỏ qua bài đã có). Chạy: python3 tools/add-practice-chatgpt.py"""
import json, subprocess, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / 'renderer/ai-work-chatgpt.js'
data = json.loads(subprocess.check_output(['node', '-e', "global.window={};require('%s');console.log(JSON.stringify(window.AI_WORK_CHATGPT))" % F]))
head = F.read_text(encoding='utf8').split('\n', 1)[0]
e = html.escape

def card(title, intro, sample_label, sample, prompt, steps, answer_html):
    return ('<section class="tcard tprac"><h4><span class="tn">★</span>Thực hành: %s</h4>'
            '<p>%s</p>'
            '<div class="ptitle">%s</div><pre class="pdata">%s</pre>'
            '<div class="ptitle">PROMPT GỢI Ý</div><pre class="prompt">%s</pre>'
            '<ol class="tl">%s</ol>'
            '<details class="tans"><summary>Đáp án để tự đối chiếu (làm xong rồi hãy mở)</summary>%s</details>'
            '<p class="tnote">Toàn bộ dữ liệu trong thẻ này là giả lập, dùng được an toàn với ChatGPT.</p></section>'
            ) % (title, intro, sample_label, e(sample), e(prompt), ''.join('<li>%s</li>' % s for s in steps), answer_html)

P = {}
P['bai4'] = card('ẩn danh trước khi dán',
  'Trước khi nhờ ChatGPT xử lý một đoạn văn bản thật, em phải gỡ thông tin định danh. Hãy tự gạch chân những chỗ cần che, rồi mới nhờ AI kiểm tra lại.',
  'DỮ LIỆU MẪU – đoạn cần xử lý',
  'Chị Lê Thu Hà (0912 345 678, ha.le@congty-mau.vn) phòng Kế toán đề nghị hoàn ứng 12.500.000 đồng cho đơn HD-2026-0457 của khách Nguyễn Văn Nam, CCCD 038 090 123 456. Hạn xử lý trước 27/11/2026.',
  'Hãy liệt kê mọi thông tin cá nhân hoặc nhạy cảm trong đoạn sau, phân loại theo mức (không được đưa vào AI / nên che / có thể giữ), rồi viết lại bản đã ẩn danh bằng ký hiệu [TÊN-1], [SĐT]... Không thêm thông tin mới.\n\n[dán đoạn mẫu]',
  ['Tự gạch chân trên giấy các chỗ cần che, ghi lý do cho từng chỗ.', 'Sao chép prompt, dán đoạn mẫu rồi gửi.', 'So kết quả của ChatGPT với bản của em và với đáp án bên dưới. Chỗ nào ChatGPT bỏ sót?'],
  '<ul class="tl"><li><b>Không bao giờ đưa vào AI:</b> số CCCD (038 090 123 456).</li><li><b>Nên che:</b> tên hai người (Lê Thu Hà, Nguyễn Văn Nam), số điện thoại, email, mã đơn HD-2026-0457.</li><li><b>Có thể giữ:</b> số tiền 12.500.000 đồng và hạn 27/11/2026 nếu việc cần tính toán hoặc nhắc hạn, vì không định danh được ai khi đã che tên và mã.</li><li>Bản ẩn danh mẫu: “[TÊN-1] ([SĐT], [EMAIL]) phòng Kế toán đề nghị hoàn ứng 12.500.000 đồng cho đơn [MÃ-ĐƠN] của khách [TÊN-2]. Hạn xử lý trước 27/11/2026.”</li><li>Nếu em và ChatGPT khác nhau, hãy theo kết quả <b>thận trọng hơn</b>.</li></ul>')
P['bai5'] = card('viết prompt BRIEF-7 từ dữ kiện có sẵn',
  'Em có các dữ kiện bên dưới. Hãy tự viết prompt đủ 7 trường BRIEF-7 trước, sau đó mới so với prompt gợi ý và đáp án.',
  'DỮ LIỆU MẪU – dữ kiện công việc',
  'Việc: nhắc 5 trưởng nhóm nộp “Bảng số liệu tháng 11”.\nHạn: 16:00 thứ Sáu, 27/11/2026.\nGửi về: baocao@congty-mau.vn\nGiọng: lịch sự, không trách móc, không nhắc chế tài.\nĐộ dài: 120–150 từ.\nĐã nộp rồi: nhóm 2 và nhóm 4 (không cần nhắc).',
  'Bối cảnh: [...]. Người nhận: [...]. Mục tiêu: [...]. Đầu vào được phép dùng: [dán dữ kiện]. Giới hạn: không thêm chính sách hay chế tài; không tự bịa tên. Đầu ra: [...]. Kiểm tra: cuối cùng lập bảng tự kiểm: yêu cầu – đạt/chưa – bằng chứng.',
  ['Điền 7 trường vào vở bằng lời của em, không nhìn gợi ý.', 'Gửi prompt của em cho ChatGPT và xem email nhận được.', 'Dùng bảng tự kiểm để chấm email: có đúng hạn, đúng người nhận, đúng độ dài, không thêm chế tài, không nhắc nhóm 2 và 4 không?'],
  '<ul class="tl"><li><b>Bối cảnh:</b> cuối tháng 11, cần tổng hợp số liệu. <b>Người nhận:</b> trưởng nhóm 1, 3, 5.</li><li><b>Mục tiêu:</b> họ nộp bảng số liệu đúng hạn. <b>Đầu vào:</b> chỉ dùng các dữ kiện đã cho.</li><li><b>Giới hạn:</b> không chế tài, không bịa số liệu. <b>Đầu ra:</b> email 120–150 từ, có tiêu đề, hạn chót, nơi gửi.</li><li><b>Kiểm tra:</b> email chứa “16:00”, “27/11/2026”, địa chỉ baocao@congty-mau.vn; <b>chỉ</b> gửi nhóm 1, 3, 5.</li><li>Lỗi hay gặp: AI vẫn nhắc cả 5 nhóm, hoặc tự thêm câu “sẽ bị trừ thi đua”. Hãy yêu cầu sửa.</li></ul>')
P['bai6'] = card('email xin lỗi khách từ ghi chú thô',
  'Biến ghi chú rời rạc thành email gửi khách. Quy tắc: email chỉ được chứa những gì có trong ghi chú.',
  'DỮ LIỆU MẪU – ghi chú nội bộ',
  'Khách: Trần Minh Anh (mã đơn DH-1021).\nHẹn giao: 20/11. Giao thực tế: 23/11.\nNguyên nhân: kho thiếu hàng 2 ngày.\nĐã duyệt bồi thường: voucher 50.000 đồng cho đơn sau.\nLiên hệ: cskh@congty-mau.vn.\nChưa biết: mã vận đơn.',
  'Viết email xin lỗi khách từ ghi chú sau, 100–130 từ, giọng chân thành, ngắn gọn. Chỉ dùng thông tin trong ghi chú. Thông tin nào chưa có, ghi [CẦN BỔ SUNG] thay vì tự điền.\n\n[dán ghi chú]',
  ['Tự viết dòng mở đầu của email (một câu xin lỗi thật) trước khi hỏi AI.', 'Gửi prompt và đọc email nhận được.', 'Chấm bằng đáp án bên dưới. Có chỗ nào AI hứa thêm hay tự bịa không?'],
  '<ul class="tl"><li>Email <b>phải có:</b> xin lỗi một lần rõ ràng; nguyên nhân thật (kho thiếu hàng 2 ngày); ngày giao thực tế 23/11 so với hẹn 20/11; voucher 50.000 đồng cho đơn sau; kênh liên hệ cskh@congty-mau.vn.</li><li><b>Không được có:</b> mã vận đơn tự bịa (phải để [CẦN BỔ SUNG] hoặc bỏ), bồi thường khác, cam kết “không bao giờ chậm nữa”.</li><li>Độ dài trong khoảng 100–130 từ.</li></ul>')
P['bai7'] = card('Excel: tính thành tiền và tổng đã duyệt',
  'Bấm “Sao chép” ở khối dữ liệu rồi dán vào ô A1 của Excel (các cột sẽ tự tách). Tính bằng Excel trước, sau đó nhờ ChatGPT giải thích công thức.',
  'DỮ LIỆU MẪU – theo dõi yêu cầu mua sắm (cột A–E)',
  'Mã\tPhòng\tSố lượng\tĐơn giá (đ)\tTrạng thái\nM01\tHành chính\t10\t120000\tĐã duyệt\nM02\tNhân sự\t3\t350000\tChờ duyệt\nM03\tHành chính\t5\t180000\tĐã duyệt\nM04\tKỹ thuật\t2\t900000\tTừ chối\nM05\tNhân sự\t4\t275000\tĐã duyệt',
  'Tôi có bảng Excel cột A=Mã, B=Phòng, C=Số lượng, D=Đơn giá, E=Trạng thái, dữ liệu từ dòng 2 đến 6. Hãy hướng dẫn: (1) tạo cột F=Thành tiền; (2) tính tổng thành tiền đã duyệt; (3) tính tổng đã duyệt theo từng phòng. Giải thích từng công thức bằng lời, không tự đoán dữ liệu.',
  ['Dán dữ liệu vào Excel. Tự tính cột F và tổng đã duyệt bằng tay hoặc máy tính.', 'Gửi prompt cho ChatGPT, áp dụng công thức nó đưa ra vào Excel.', 'So kết quả Excel với đáp án. Sai lệch ở đâu thì tìm nguyên nhân, đừng sửa số cho khớp.'],
  '<div class="tbl-wrap"><table><thead><tr><th>Mã</th><th>Thành tiền (F)</th></tr></thead><tbody><tr><td>M01</td><td>1.200.000</td></tr><tr><td>M02</td><td>1.050.000</td></tr><tr><td>M03</td><td>900.000</td></tr><tr><td>M04</td><td>1.800.000</td></tr><tr><td>M05</td><td>1.100.000</td></tr></tbody></table></div><ul class="tl"><li>Công thức F2: <code>=C2*D2</code>, kéo xuống F6.</li><li>Tổng đã duyệt: <code>=SUMIF(E2:E6,"Đã duyệt",F2:F6)</code> = <b>3.200.000</b>. Tổng đề nghị cả bảng (đừng nhầm): 6.050.000.</li><li>Theo phòng (đã duyệt): Hành chính 2.100.000; Nhân sự 1.100.000; Kỹ thuật 0. Công thức: <code>=SUMIFS(F2:F6,B2:B6,"Hành chính",E2:E6,"Đã duyệt")</code>.</li></ul>')
P['bai8'] = card('biên bản họp và bảng theo dõi việc',
  'Tách riêng quyết định, việc cần làm, ý kiến chưa chốt và điều chưa rõ. Đây là chỗ AI dễ gộp lẫn nhất.',
  'DỮ LIỆU MẪU – ghi chú họp thô',
  'Họp dự án kho, 20/11/2026.\nAnh Tuấn báo kiểm kê xong 80%, còn khu C.\nChị Mai đề xuất đổi nhà vận chuyển, chưa ai quyết.\nThống nhất: kiểm kê xong khu C trước 25/11 (Tuấn).\nMai gửi 3 báo giá vận chuyển trước 24/11.\nCó người hỏi ai sẽ chốt nhà vận chuyển, chưa ai trả lời.',
  'Từ ghi chú họp sau, lập bảng gồm: Quyết định, Việc cần làm (việc – người phụ trách – hạn), Ý kiến chưa quyết, Điều chưa rõ. Chỉ dùng thông tin trong ghi chú; không suy ra người hay hạn không có; thiếu thì ghi [CẦN XÁC MINH].\n\n[dán ghi chú]',
  ['Tự phân loại 6 dòng ghi chú vào 4 nhóm trước.', 'Gửi prompt, so bảng của ChatGPT với bảng của em.', 'Kiểm tra: có việc nào bị biến thành “quyết định”, có hạn hay người nào AI tự thêm không?'],
  '<ul class="tl"><li><b>Quyết định:</b> kiểm kê xong khu C trước 25/11.</li><li><b>Việc cần làm:</b> Tuấn – kiểm kê khu C – 25/11; Mai – gửi 3 báo giá vận chuyển – 24/11.</li><li><b>Ý kiến chưa quyết:</b> đổi nhà vận chuyển (Mai đề xuất).</li><li><b>Điều chưa rõ:</b> ai chốt nhà vận chuyển, hạn chốt → [CẦN XÁC MINH]. Dòng “kiểm kê xong 80%” chỉ là báo cáo tiến độ, không phải việc mới.</li></ul>')
P['bai9'] = card('so sánh báo giá nhà cung cấp',
  'AI giúp so sánh và nêu rủi ro, nhưng tiêu chí chọn do em đặt. Hãy tự tính tổng chi phí trước.',
  'DỮ LIỆU MẪU – ba báo giá cho cùng một thiết bị',
  'Nhà cung cấp\tĐơn giá (đ)\tVận chuyển (đ)\tGiao hàng\tBảo hành\nA\t1150000\t60000\t3 ngày\t12 tháng\nB\t1050000\t100000\t7 ngày\t6 tháng\nC\t1200000\t0 (đã gồm)\t2 ngày\t12 tháng',
  'So sánh ba báo giá sau theo: tổng chi phí (đơn giá + vận chuyển), thời gian giao, bảo hành. Lập bảng, nêu ưu nhược điểm từng bên và rủi ro cần hỏi thêm. Chưa đưa kết luận chọn ai; cuối cùng hỏi tôi tiêu chí ưu tiên.\n\n[dán bảng]',
  ['Tự tính tổng chi phí của A, B, C.', 'Gửi prompt, kiểm tra số trong bảng của ChatGPT.', 'Đặt tiêu chí của em (ví dụ cần gấp trong 3 ngày) rồi hỏi tiếp để chọn.'],
  '<ul class="tl"><li>Tổng chi phí: A = 1.210.000; B = 1.150.000; C = 1.200.000.</li><li>B rẻ nhất nhưng giao chậm nhất (7 ngày) và bảo hành ngắn nhất (6 tháng). C chỉ đắt hơn B 50.000 đồng, giao nhanh nhất; C còn rẻ hơn A mà giao nhanh hơn.</li><li>Cần gấp trong 3 ngày: loại B; còn A và C, C tổng thấp hơn. Nhưng vẫn cần hỏi thêm: báo giá còn hiệu lực đến khi nào, có hóa đơn đỏ không.</li><li>Nếu ChatGPT kết luận “chọn A” khi em chưa nêu tiêu chí, đó là tự quyết thay em.</li></ul>')

for k, c in P.items():
    if 'tprac' in data[k]['html']: continue
    data[k]['html'] += c

# ---- Bài 11: bộ dữ liệu mẫu cho Case 1–5 (chèn trước Chương 19) ----
def block(label, text):
    return '<div class="ptitle">%s</div><pre class="pdata">%s</pre>' % (label, e(text))
FILES = ['Mau_don_xin_nghi_final.docx','Mau_don_xin_nghi_final2.docx','Mau_don_xin_nghi_final_moi.docx','Bien_ban_hop_mau.docx','Bien_ban_hop_mau_v2.docx',
 'De_nghi_mua_sam.xlsx','De_nghi_mua_sam_final.xlsx','Phieu_giao_viec_HC.docx','Phieu_giao_viec_HC (1).docx','Bao_cao_tuan_mau.xlsx','Bao_cao_tuan_mau_ketoan.xlsx',
 'Quy_trinh_ban_giao_HC_v1.docx','Quy_trinh_ban_giao_HC_v1_sua.docx','Thong_bao_nghi_le.docx','Thong_bao_nghi_le_2026.docx','Danh_sach_tai_san_NV.xlsx',
 'Cong_van_mau_final.docx','Cong_van_mau_final_final.docx','Giay_uy_quyen_mau.docx','Hop_dong_mau_KT.docx','Hop_dong_mau_KT_ban_cu.docx',
 'Checklist_onboarding.docx','Checklist_onboarding_moi.docx','Mau_tam_ung.xlsx']
B11 = ('<section class="tcard tprac"><h4><span class="tn">★</span>Thực hành: bộ dữ liệu mẫu cho các case</h4>'
  '<p>Bấm “Sao chép” rồi dán vào chỗ [bảng], [danh sách], [dữ liệu] hoặc [nội dung] trong prompt của từng case ở trên. Toàn bộ là dữ liệu giả lập. '
  'Hãy tự làm phần tính toán trước, sau đó mới so với ChatGPT và phần “nghiệm thu” của case.</p>'
  + block('CASE 1 – bảng yêu cầu hai tháng; “Đúng hạn” là số đúng hạn trong các việc đã hoàn tất (dán vào [bảng])', 'Chỉ số\tTháng 9\tTháng 10\nYêu cầu nhận\t100\t120\nHoàn tất\t90\t108\nĐúng hạn\t84\t99')
  + block('CASE 2 – danh sách tên tệp giả lập (dán vào [danh sách])', '\n'.join(FILES))
  + block('CASE 3 – ba báo giá cho 10 thiết bị (dán vào [dữ liệu])', 'Nhà cung cấp\tĐơn giá (đ)\tSố lượng\tVận chuyển (đ)\nA\t2000000\t10\t300000\nB\t1950000\t10\t800000\nC\t2050000\t10\t0 (miễn phí)')
  + block('CASE 4 – ghi chú cuộc họp (dán vào [nội dung])', 'Họp tổng hợp báo cáo quý.\nPhòng Kế toán sẽ gửi dữ liệu đã khóa vào thứ Sáu (chưa chốt ngày).\nNhân sự đề nghị dùng mẫu cũ.\nTrưởng phòng quyết định dùng mẫu báo cáo mới.\nHành chính chịu trách nhiệm tổng hợp; hạn hoàn thành chưa được nêu.\nCần thống nhất định nghĩa KPI.')
  + '<p><b>Case 5</b> không cần dán dữ liệu: prompt đã có đủ bối cảnh (nhân viên hành chính mới, 30 phút mỗi ngày, 30 ngày). Em chỉ cần kiểm tra khung ChatGPT đưa ra có đúng tinh thần “chưa phải quy định chính thức” không.</p>'
  '<details class="tans"><summary>Đáp án số liệu để tự đối chiếu</summary><ul class="tl">'
  '<li><b>Case 1:</b> chưa hoàn tất tháng 9 = 10, tháng 10 = 12; tỷ lệ hoàn tất 90% và 90%; đúng hạn trên việc hoàn tất 84/90 = 93,33% và 99/108 = 91,67%. Số lượng tăng (100 → 120) nhưng tỷ lệ đúng hạn giảm, không được viết là “chất lượng tăng”.</li>'
  '<li><b>Case 2:</b> 24 tệp, trong đó 21 tệp thuộc 10 nhóm có nhiều phiên bản (Mau_don_xin_nghi có 3, các nhóm còn lại 2) và 3 tệp đơn lẻ. Cần hỏi người phụ trách bản nào đang có hiệu lực; “Bao_cao_tuan_mau_ketoan” có thể là biến thể của Kế toán chứ không phải phiên bản cũ nên ghi [CẦN CHỐT]. Không xóa hay đổi tên tệp ở giai đoạn kiểm kê.</li>'
  '<li><b>Case 3:</b> A = 20.000.000 + 300.000 = 20.300.000; B = 19.500.000 + 800.000 = 20.300.000; C = 20.500.000. A và B bằng nhau trước khi xác minh thuế, bảo hành, giao hàng; chưa được kết luận chọn bên nào.</li>'
  '<li><b>Case 4:</b> Ý kiến: dùng mẫu cũ. Quyết định: dùng mẫu báo cáo mới. Hành động: Kế toán gửi dữ liệu đã khóa (thiếu ngày; “thứ Sáu” chưa có mốc tuần nên không đổi thành ngày cụ thể), Hành chính tổng hợp (thiếu hạn). Điều chưa rõ: ai sở hữu định nghĩa KPI.</li>'
  '</ul></details></section>')
h = data['bai11']['html']
if 'bộ dữ liệu mẫu cho các case' not in h:
    mark = '<h3 class="tchap">Chương 19.'
    assert mark in h
    data['bai11']['html'] = h.replace(mark, B11 + mark, 1)

import sys; sys.path.insert(0, str(ROOT / 'tools'))
from summary_common import lesson as _summary
if 'bai13' not in data: data['bai13'] = _summary('chatgpt')
F.write_text(head + '\nwindow.AI_WORK_CHATGPT = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n', encoding='utf8')
print([k for k in P], 'bai11')
