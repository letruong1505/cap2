// Lưu dữ liệu người dùng (mã PIN, câu sai, tiến độ, trò chơi...) ra file riêng trong thư mục dữ liệu cố định.
// Dùng song song với localStorage: nếu localStorage bị mất sau khi cập nhật thì khôi phục từ file này.
const fs = require('fs');
const path = require('path');

const MAX_KEY = 200;
const MAX_VALUE = 4 * 1024 * 1024;

function createStore(dir) {
  const file = path.join(dir, 'user-data.json');
  const bak = file + '.bak';
  const tmp = file + '.tmp';
  let cache = null;

  function parse(p) {
    try {
      const o = JSON.parse(fs.readFileSync(p, 'utf8'));
      return o && typeof o === 'object' && !Array.isArray(o) ? o : null;
    } catch { return null; }
  }

  function load() {
    if (cache) return cache;
    cache = parse(file) || parse(bak) || {};
    return cache;
  }

  function flush() {
    fs.mkdirSync(dir, { recursive: true });
    try { if (fs.existsSync(file) && parse(file)) fs.copyFileSync(file, bak); } catch { /* bỏ qua */ }
    fs.writeFileSync(tmp, JSON.stringify(cache), 'utf8');
    fs.renameSync(tmp, file);
  }

  return {
    file,
    all() { return { ...load() }; },
    set(key, value) {
      key = String(key);
      if (!key || key.length > MAX_KEY) return false;
      const data = load();
      if (value === null || value === undefined) {
        if (!(key in data)) return true;
        delete data[key];
      } else {
        value = String(value);
        if (value.length > MAX_VALUE) return false;
        if (data[key] === value) return true;
        data[key] = value;
      }
      try { flush(); return true; } catch { return false; }
    },
  };
}

module.exports = { createStore };
