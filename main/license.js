// Đọc thông tin bản quyền từ file license.json đặt cạnh file chạy của phần mềm.
// Đây là bản đầu: file không có chữ ký, nên chỉ hiển thị thông tin, chưa kiểm tra tính hợp lệ của mã.
// Khi làm cơ chế kích hoạt thật, cần thay bằng khóa có chữ ký.

const fs = require('fs');
const path = require('path');

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

function loadLicense(baseDir) {
  const file = path.join(baseDir, 'license.json');
  if (!fs.existsSync(file)) return { status: 'missing' };
  try {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (typeof data.expiresOn !== 'string' || !DATE_RE.test(data.expiresOn)) {
      return { status: 'invalid' };
    }
    return {
      status: 'ok',
      owner: String(data.owner || ''),
      code: String(data.code || ''),
      scope: String(data.scope || ''),
      expiresOn: data.expiresOn,
    };
  } catch {
    return { status: 'invalid' };
  }
}

module.exports = { loadLicense };
