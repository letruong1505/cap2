// Dữ liệu khung "Ôn thi THPT Quốc gia": môn tự chọn và tổ hợp → khối thi.
// Kỳ thi từ 2025: thi bắt buộc Ngữ văn, Toán và 2 môn tự chọn trong 9 môn (Thông tư 24/2024/TT-BGDĐT).
// Bảng khối dưới đây chỉ có một phần 36 tổ hợp (đối chiếu từ các nguồn công bố). Cần bổ sung đủ trước khi bán.
// Khóa tổ hợp: mã môn tự chọn sắp theo thứ tự chữ cái, nối bằng "|".
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.THPT_EXAM_DATA = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const ELECTIVES = [
    { id: 'EN', name: 'Tiếng Anh' },
    { id: 'LI', name: 'Lịch sử' },
    { id: 'DI', name: 'Địa lý' },
    { id: 'GDKT', name: 'Giáo dục KT & PL' },
    { id: 'PH', name: 'Vật lý' },
    { id: 'CH', name: 'Hóa học' },
    { id: 'BI', name: 'Sinh học' },
    { id: 'IT', name: 'Tin học' },
    { id: 'TECH', name: 'Công nghệ' },
  ];

  const COMBO_KHOI = {
    'CH|PH': ['A00', 'C01', 'C02', 'C05'],
    'EN|PH': ['A01', 'D01', 'D10', 'C01'],
    'BI|CH': ['B00', 'B03', 'C02', 'C08'],
    'DI|LI': ['C00', 'A07', 'C03', 'C04'],
    'EN|LI': ['D01', 'C03', 'D09', 'D14'],
    'CH|EN': ['D01', 'C02', 'D07', 'D12'],
    'BI|EN': ['D01', 'B03', 'D08', 'B08', 'D13'],
    'DI|EN': ['D01', 'C04', 'D10', 'D15'],
    'LI|PH': ['C03', 'C01', 'A03', 'C07'],
    'BI|DI': ['B03', 'C04', 'B02', 'C13'],
  };

  // Cấu trúc kỳ thi qua các năm (để hiển thị ở bước 1).
  const YEARS = [
    { years: '2022 – 2024', text: '5 bài thi: Toán, Ngữ văn, Ngoại ngữ và 1 trong 2 tổ hợp: KHTN (Vật lý, Hóa học, Sinh học) hoặc KHXH (Lịch sử, Địa lý, GDCD).' },
    { years: '2025 – 2026', text: 'Ngữ văn và Toán bắt buộc, cộng 2 môn tự chọn trong 9 môn. Tạo thành 36 tổ hợp thi.' },
  ];

  // Chuẩn hóa khóa tổ hợp từ danh sách mã môn tự chọn.
  function comboKey(ids) {
    return [...ids].sort().join('|');
  }

  function khoiFor(ids) {
    if (!ids || ids.length !== 2) return null;
    return COMBO_KHOI[comboKey(ids)] || null;
  }

  return { ELECTIVES, COMBO_KHOI, YEARS, comboKey, khoiFor };
});
