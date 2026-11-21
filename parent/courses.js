// Giới thiệu và nội dung các khóa học cho phụ huynh xem trong app (không chứa bài học).
window.PARENT_COURSES = (function () {
  const VH = ['Toán', 'Vật lí', 'Hoá học', 'Sinh học', 'Tiếng Anh', 'Lịch sử', 'Địa lí'];
  const common = ['Bài 1: An toàn', 'Bài 2: Trách nhiệm', 'Bài 3: Kiểm chứng (3 bài này học thử miễn phí)'];
  const out = {
    'gia-su-ai': { intro: 'Biến AI thành trợ lý học tập phù hợp với mỗi cá nhân, biết khắc phục điểm yếu và khai thác điểm mạnh. Dành cho học sinh từ 12 tuổi, có hướng dẫn từng bước để các em làm chủ công nghệ chứ không phụ thuộc vào AI.', content: ['Nhận thức và an toàn AI', 'Tự tìm lỗ hổng kiến thức', 'Xây gia sư AI riêng', 'Lộ trình cá nhân hóa'] },
    'he-mien-dich-so': { intro: 'Giúp trẻ 8–11 tuổi nhận biết các tình huống không an toàn trên mạng và biết cách nói với người lớn.', content: [] },
    'lam-chu-the-gioi-so': { intro: 'Giúp học sinh 12–15 tuổi hiểu cách thông tin, mạng xã hội và công nghệ hoạt động để tự quyết định khi dùng chúng.', content: [] },
    'cong-dan-so': { intro: 'Giúp học sinh 16–18 tuổi hiểu trách nhiệm, đạo đức và pháp luật khi tham gia không gian mạng.', content: [] },
    'ranh-gioi-so': { intro: 'Dành cho học sinh THPT và tân sinh viên: tư duy phản biện và kỹ năng xử lý thông tin trước khi chia sẻ, dựng nền móng cho tuổi lập thân, lập nghiệp.', content: [] },
    'ai-nguoi-di-lam-chatgpt': { intro: 'Ứng dụng ChatGPT để tăng hiệu quả công việc văn phòng, tối ưu nguồn lực và thời gian. Giá chưa gồm phí tài khoản ChatGPT do người học tự đăng ký.', content: common.concat(['Bài 4: Vai trò của ChatGPT và thiết lập an toàn', 'Bài 5: Công thức giao việc và quy trình 6 bước', 'Bài 6: Email, Word và SOP', 'Bài 7: Excel và phân tích KPI', 'Bài 8: PowerPoint, cuộc họp và quản lý lịch', 'Bài 9: Hành chính, nhân sự và mua hàng', 'Bài 10: Dự án, nghiên cứu nguồn và tự động hóa', 'Bài 11: Năm case study và lộ trình 30 ngày', 'Bài 12: Thư viện 96 prompt và phụ lục']) },
    'ai-nguoi-di-lam-gemini': { intro: 'Ứng dụng Gemini cho công việc với Gmail, Docs, Sheets, Drive. Giá chưa gồm phí tài khoản Gemini do người học tự đăng ký.', content: common.concat(['Phần riêng của lớp Gemini đang được biên soạn']) },
    'ai-nguoi-di-lam-claude': { intro: 'Ứng dụng Claude để viết dài, đọc kỹ tài liệu và làm công cụ nhỏ, nâng năng suất làm việc. Giá chưa gồm phí tài khoản Claude do người học tự đăng ký.', content: common.concat(['Bài 4: Làm xong một việc thật ngay buổi đầu', 'Bài 5: Ra lệnh đúng một lần, sửa cho trúng', 'Bài 6: Giọng văn của Anh/Chị và trợ lý riêng', 'Bài 7: Đọc nhanh, nghĩ rõ, quyết nhanh', 'Bài 8: Biến thành sản phẩm và file', 'Bài 9: Ứng dụng theo nghề', 'Bài 10: Tự động hóa và nâng cao', 'Bài 11: Tổng kết, dự án cuối và đo năng suất']) },
  };
  for (let g = 6; g <= 12; g++) {
    out['van-hoa-' + g] = { intro: 'Bài tập và ôn luyện theo chương trình lớp ' + g + ', chạy offline trên máy tính và điện thoại, có sổ câu sai để ôn đúng lúc và báo cáo cho phụ huynh.', content: VH.concat(g >= 10 ? ['Giáo dục kinh tế và pháp luật'] : []) };
  }
  return out;
})();
