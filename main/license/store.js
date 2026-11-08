// Lưu khoá đã kích hoạt trong thư mục dữ liệu của app, kèm ngày chạy gần nhất để phát hiện chỉnh lùi đồng hồ.
const fs = require('fs');
const path = require('path');

const file = (dir) => path.join(dir, 'license.json');

function readStore(dir) {
  try {
    const d = JSON.parse(fs.readFileSync(file(dir), 'utf8'));
    return { key: typeof d.key === 'string' ? d.key : '', lastSeen: typeof d.lastSeen === 'string' ? d.lastSeen : '' };
  } catch {
    return { key: '', lastSeen: '' };
  }
}

function writeStore(dir, data) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(file(dir), JSON.stringify(data));
}

module.exports = { readStore, writeStore };
