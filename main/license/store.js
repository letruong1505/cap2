// Lưu khoá đã kích hoạt trong thư mục dữ liệu của app, kèm ngày chạy gần nhất để phát hiện chỉnh lùi đồng hồ.
const fs = require('fs');
const path = require('path');

const file = (dir) => path.join(dir, 'license.json');

function readStore(dir) {
  try {
    const d = JSON.parse(fs.readFileSync(file(dir), 'utf8'));
    // Bản cũ chỉ lưu một khoá (key); bản mới lưu nhiều khoá (keys) để gộp khoá Văn hóa và khoá Kỹ năng mua ở các đơn khác nhau.
    const keys = Array.isArray(d.keys) ? d.keys.filter((k) => typeof k === 'string' && k) : (typeof d.key === 'string' && d.key ? [d.key] : []);
    return { keys, lastSeen: typeof d.lastSeen === 'string' ? d.lastSeen : '' };
  } catch {
    return { keys: [], lastSeen: '' };
  }
}

function writeStore(dir, data) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(file(dir), JSON.stringify(data));
}

module.exports = { readStore, writeStore };
