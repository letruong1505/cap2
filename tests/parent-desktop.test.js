const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');
const { build } = require('../tools/build-parent-www.js');

test('app Phụ huynh bản Windows: gói www dùng khởi động riêng, gọi mạng qua tiến trình chính, đủ tệp', () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'phw-'));
  build({ out, version: '1.0.3', api: 'https://example.workers.dev/api', desktop: true });
  const html = fs.readFileSync(path.join(out, 'index.html'), 'utf8');
  for (const m of html.matchAll(/<script src="([^"]+)"/g)) assert.ok(fs.existsSync(path.join(out, m[1])), 'thiếu ' + m[1]);
  const boot = fs.readFileSync(path.join(out, 'parent-boot.js'), 'utf8');
  assert.match(boot, /NLDesktop\.fetch/);
  assert.match(boot, /platform: 'windows'/);
  assert.match(fs.readFileSync(path.join(out, 'parent-update.js'), 'utf8'), /NLDesktop/);
  assert.ok(!/ngay trên điện thoại này/.test(fs.readFileSync(path.join(out, 'buy.js'), 'utf8')));
  assert.ok(!/Nhắc trên điện thoại này/.test(html));
  // Bản Android không bị ảnh hưởng.
  const out2 = fs.mkdtempSync(path.join(os.tmpdir(), 'pha-'));
  build({ out: out2, version: '1.0.3', api: 'https://example.workers.dev/api' });
  assert.match(fs.readFileSync(path.join(out2, 'parent-boot.js'), 'utf8'), /Capacitor/);
});

test('app Phụ huynh bản Windows: tiến trình chính đúng cú pháp, cấu hình đóng gói và nguồn cập nhật riêng', () => {
  const root = path.join(__dirname, '..');
  for (const f of ['main-parent/main.js', 'main-parent/preload.js', 'main-parent/store.js', 'parent/parent-boot-desktop.js', 'parent/parent-update-desktop.js']) {
    cp.execFileSync(process.execPath, ['--check', path.join(root, f)]);
  }
  const b = JSON.parse(fs.readFileSync(path.join(root, 'build-parent-win.json'), 'utf8'));
  assert.strictEqual(b.extraMetadata.main, 'main-parent/main.js');
  assert.notStrictEqual(b.appId, 'vn.namlinh.educenter');
  assert.ok(!b.files.some((f) => /content|renderer/.test(f)), 'không đóng gói bài học');
  const u = JSON.parse(fs.readFileSync(path.join(root, 'main-parent/update-config.json'), 'utf8'));
  assert.match(u.url, /\/phuhuynh-windows$/);
  assert.match(JSON.parse(fs.readFileSync(path.join(root, 'main-parent/orders-api.json'), 'utf8')).baseUrl, /^https:\/\//);
  // Tiến trình chính chỉ cho gọi tới máy chủ đơn hàng.
  assert.match(fs.readFileSync(path.join(root, 'main-parent/main.js'), 'utf8'), /url\.startsWith\(base \+ '\/'\)/);
});

test('app Phụ huynh bản Windows: bản sao dữ liệu ra tệp giữ lại sau khi mở lại và chỉ nhận khóa nl-', () => {
  const { createStore } = require('../main-parent/store.js');
  const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'phs-')), 'sub', 'store.json');
  const a = createStore(f);
  assert.ok(a.set('nl-parent-family', '{"fcode":"F1","phone":"09"}'));
  assert.ok(!a.set('khac', 'x') && !a.set('nl-x', 5));
  a.set('nl-parent-pending', '{"code":"C"}'); a.remove('nl-parent-pending');
  const b = createStore(f); // mở lại như sau khi cập nhật
  assert.deepStrictEqual(b.all(), { 'nl-parent-family': '{"fcode":"F1","phone":"09"}' });
  fs.writeFileSync(f, 'hỏng'); assert.deepStrictEqual(createStore(f).all(), {});
});
