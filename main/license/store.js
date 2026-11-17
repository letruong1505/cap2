// Lưu khoá đã kích hoạt trong thư mục dữ liệu của app, kèm ngày chạy gần nhất để phát hiện chỉnh lùi đồng hồ.
const fs = require('fs');
const path = require('path');

const file = (dir) => path.join(dir, 'license.json');

function readStore(dir) {
  try {
    const d = JSON.parse(fs.readFileSync(file(dir), 'utf8'));
    // Bản cũ chỉ lưu một khoá (key); bản mới lưu nhiều khoá (keys) để gộp khoá Văn hóa và khoá Kỹ năng mua ở các đơn khác nhau.
    const keys = Array.isArray(d.keys) ? d.keys.filter((k) => typeof k === 'string' && k) : (typeof d.key === 'string' && d.key ? [d.key] : []);
    // revoked: mã đơn bị thu hồi do máy chủ báo về, lưu lại để khóa vẫn bị vô hiệu khi mở phần mềm lúc không có mạng.
    const revoked = Array.isArray(d.revoked) ? d.revoked.filter((c) => typeof c === 'string') : [];
    return { keys, lastSeen: typeof d.lastSeen === 'string' ? d.lastSeen : '', revoked };
  } catch {
    return { keys: [], lastSeen: '', revoked: [] };
  }
}

function writeStore(dir, data) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(file(dir), JSON.stringify(data));
}

// Ghi đè một phần, giữ nguyên các trường còn lại.
function updateStore(dir, patch) {
  const cur = readStore(dir);
  writeStore(dir, { keys: cur.keys, lastSeen: cur.lastSeen, revoked: cur.revoked, ...patch });
}

module.exports = { readStore, writeStore, updateStore };
