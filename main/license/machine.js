// Mã máy: băm từ định danh có sẵn của hệ điều hành, hiển thị dạng XXXX-XXXX-XXXX.
// Cài lại app không đổi mã; cài lại Windows có thể đổi mã (khi đó cần cấp lại khoá).
const crypto = require('crypto');
const fs = require('fs');
const { execFileSync } = require('child_process');
const os = require('os');

function rawMachineId() {
  try {
    if (process.platform === 'win32') {
      const out = execFileSync('reg', ['query', 'HKLM\\SOFTWARE\\Microsoft\\Cryptography', '/v', 'MachineGuid'], { encoding: 'utf8', windowsHide: true });
      const m = out.match(/MachineGuid\s+REG_SZ\s+(\S+)/);
      if (m) return m[1];
    } else if (fs.existsSync('/etc/machine-id')) {
      return fs.readFileSync('/etc/machine-id', 'utf8').trim();
    }
  } catch { /* dùng phương án dự phòng */ }
  return os.hostname() + '|' + os.cpus()[0]?.model;
}

function getMachineId() {
  const h = crypto.createHash('sha256').update('vungbai-machine-v1|' + rawMachineId()).digest('hex').slice(0, 12).toUpperCase();
  return h.match(/.{4}/g).join('-');
}

module.exports = { getMachineId };
