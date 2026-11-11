// Danh mục khóa học và giá niêm yết. Dùng chung cho phần mềm (màn hình Mua khóa học) và Worker Cloudflare (tính tiền, cấp key).
// Sửa giá ở đây rồi build lại phần mềm và deploy lại Worker.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NL_CATALOG = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const GROUPS = [
    { group: 'Khóa Kỹ năng', items: [
      { id: 'gia-su-ai', name: 'Gia sư AI', note: 'Học sinh từ 12 tuổi trở lên', price: 999000, was: 1600000 },
      { id: 'he-mien-dich-so', name: 'Hệ miễn dịch số', note: 'Học sinh 8 - 11 tuổi', price: 2090000 },
      { id: 'lam-chu-the-gioi-so', name: 'Làm chủ thế giới số', note: 'Học sinh 12 - 15 tuổi', price: 2590000 },
      { id: 'cong-dan-so', name: 'Công dân số', note: 'Học sinh 16 - 18 tuổi', price: 2990000 },
      { id: 'ranh-gioi-so', name: 'Ranh giới số', note: 'Học sinh THPT & tân sinh viên', price: 1590000 },
    ] },
    { group: 'Giáo trình Văn hóa', items: [6, 7, 8, 9, 12].map((g) => ({
      id: 'van-hoa-' + g, name: 'Giáo trình Văn hóa lớp ' + g, note: g === 12 ? '2 môn học' : '6 môn học', price: g === 12 ? 499000 : 399000, grade: g })) },
  ];
  const ALL = GROUPS.flatMap((c) => c.items);
  const byId = Object.fromEntries(ALL.map((x) => [x.id, x]));
  return { GROUPS, ALL, byId };
});
