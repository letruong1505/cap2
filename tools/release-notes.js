// Đọc CHANGELOG.md (mục đầu tiên) và ghi vào releaseInfo.releaseNotes của các file cấu hình build,
// để latest.yml mang theo nội dung cập nhật cho phần mềm hiển thị trước khi người dùng tải.
const fs = require('fs');
const path = require('path');

function firstSection(md) {
  const parts = String(md || '').split(/^## .*$/m);
  return (parts[1] || '').trim();
}

function apply(root) {
  let notes = '';
  try { notes = firstSection(fs.readFileSync(path.join(root, 'CHANGELOG.md'), 'utf8')); } catch { /* không có thì bỏ qua */ }
  if (!notes) return '';
  for (const f of ['build-nam-linh.json', 'build-thpt.json']) {
    const p = path.join(root, f);
    if (!fs.existsSync(p)) continue;
    const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
    cfg.releaseInfo = Object.assign({}, cfg.releaseInfo, { releaseNotes: notes });
    fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
  }
  return notes;
}

module.exports = { firstSection, apply };
if (require.main === module) console.log(apply(path.join(__dirname, '..')) || '(không có ghi chú)');
