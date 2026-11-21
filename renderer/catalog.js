// Danh mục khóa học và giá niêm yết. Dùng chung cho phần mềm (màn hình Mua khóa học) và Worker Cloudflare (tính tiền, cấp key).
// Sửa giá ở đây rồi build lại phần mềm và deploy lại Worker.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NL_CATALOG = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const GROUPS = [
    { group: 'Khóa Kỹ năng', items: [
      { id: 'gia-su-ai', name: 'Gia sư AI', note: 'Học sinh từ 12 tuổi trở lên · chưa gồm phí bản quyền AI', price: 999000, was: 1600000 },
      { id: 'he-mien-dich-so', name: 'Hệ miễn dịch số', note: 'Học sinh 8 - 11 tuổi', price: 990000 },
      { id: 'lam-chu-the-gioi-so', name: 'Làm chủ thế giới số', note: 'Học sinh 12 - 15 tuổi', price: 1490000 },
      { id: 'cong-dan-so', name: 'Công dân số', note: 'Học sinh 16 - 18 tuổi', price: 1990000 },
      { id: 'tu-duy-lap-trinh', name: 'Tư duy & lập trình', note: 'Học sinh 8 - 18 tuổi · 2 lộ trình: Scratch (8–11), Python (12–18)', price: 1490000 },
      { id: 'ranh-gioi-so', name: 'Ranh giới số', note: 'Học sinh THPT & tân sinh viên', price: 1490000 },
    ] },
    { group: 'AI cho người đi làm', ai: true, fee: 'Giá khóa học chưa bao gồm phí bản quyền AI (tài khoản ChatGPT, Gemini hoặc Claude do người học tự đăng ký và chi trả).', items: [
      { id: 'ai-nguoi-di-lam-chatgpt', name: 'AI cho người đi làm · ChatGPT', note: 'Lớp học trên ChatGPT', price: 1990000, ai: 'chatgpt' },
      { id: 'ai-nguoi-di-lam-gemini', name: 'AI cho người đi làm · Gemini', note: 'Lớp học trên Gemini', price: 1990000, ai: 'gemini' },
      { id: 'ai-nguoi-di-lam-claude', name: 'AI cho người đi làm · Claude', note: 'Lớp học trên Claude', price: 1990000, ai: 'claude' },
    ] },
    { group: 'Giáo trình Văn hóa', items: [6, 7, 8, 9, 10, 11, 12].map((g) => ({
      id: 'van-hoa-' + g, name: 'Giáo trình Văn hóa lớp ' + g, note: g >= 10 ? '8 môn học' : '7 môn học', price: g === 12 ? 499000 : g >= 10 ? 449000 : 399000, grade: g })) },
  ];
  const ALL = GROUPS.flatMap((c) => c.items);
  const byId = Object.fromEntries(ALL.map((x) => [x.id, x]));
  return { GROUPS, ALL, byId };
});
