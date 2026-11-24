const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
// Dữ liệu cho phụ huynh phải trùng biến D của khóa Định hướng quốc gia.
test('dữ liệu định hướng của app Phụ huynh trùng với khóa học', () => {
  const html = fs.readFileSync(path.join(root, 'courses/dinh-huong-quoc-gia/index.html'), 'utf8');
  const m = /var D=(\{.*?\});\nvar KEY/s.exec(html);
  assert.ok(m);
  const ctx = { window: {} };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'parent/dhqg-data.js'), 'utf8'), ctx);
  assert.deepEqual(JSON.parse(JSON.stringify(ctx.window.PARENT_DHQG)), JSON.parse(m[1]));
  for (const g of Object.values(ctx.window.PARENT_DHQG)) { assert.ok(g.n && g.m.length && g.s.length && g.a.length && g.b.length); }
});

test('build app Phụ huynh có dữ liệu định hướng và nút xem', () => {
  const { build } = require('../tools/build-parent-www.js');
  const out = fs.mkdtempSync(path.join(require('node:os').tmpdir(), 'pw-'));
  build({ out, version: '1.0.0', api: 'https://x.example/api' });
  assert.ok(fs.existsSync(path.join(out, 'dhqg-data.js')));
  const html = fs.readFileSync(path.join(out, 'index.html'), 'utf8');
  assert.match(html, /id="go-orient"/); assert.match(html, /dhqg-data\.js/);
});

test('app học gửi mã hướng đã chọn lên máy chủ khi bật chia sẻ', () => {
  const s = fs.readFileSync(path.join(root, 'renderer/progress-sync.js'), 'utf8');
  assert.match(s, /nl-dhqg/); assert.match(s, /orientation: ids/);
  for (const f of ['main/orders.js', 'mobile/bridge/api.js']) assert.match(fs.readFileSync(path.join(root, f), 'utf8'), /orientation:/);
});
