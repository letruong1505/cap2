// Bản sao bền của dữ liệu app Phụ huynh (khóa "nl-…" và "vungbai.parentview.v1" = mã đơn + SĐT xem con, trong localStorage) lưu thành tệp JSON ở thư mục cố định.
// Dùng khi localStorage của trình duyệt nhúng bị mất (đổi bản, đổi thư mục dữ liệu, dọn dẹp) để phụ huynh khỏi nhập lại.
const fs = require('fs');
const path = require('path');

function createStore(file) {
  let data = {};
  try { const j = JSON.parse(fs.readFileSync(file, 'utf8')); if (j && typeof j === 'object' && !Array.isArray(j)) data = j; } catch { /* chưa có tệp */ }
  function save() {
    try {
      fs.mkdirSync(path.dirname(file), { recursive: true });
      const tmp = file + '.tmp';
      fs.writeFileSync(tmp, JSON.stringify(data));
      fs.renameSync(tmp, file);
    } catch { /* ghi lỗi thì thôi, localStorage vẫn còn */ }
  }
  return {
    all: () => ({ ...data }),
    set(k, v) {
      if (typeof k !== 'string' || !/^(nl-[\w.-]{1,80}|vungbai\.parentview\.v1)$/.test(k) || typeof v !== 'string' || v.length > 500000) return false;
      if (data[k] !== v) { data[k] = v; save(); }
      return true;
    },
    remove(k) { if (typeof k === 'string' && Object.prototype.hasOwnProperty.call(data, k)) { delete data[k]; save(); } },
  };
}

module.exports = { createStore };
