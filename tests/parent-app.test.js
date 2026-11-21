const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { build, FROM_RENDERER } = require('../tools/build-parent-www.js');

test('app Phụ huynh: gói www nhẹ, đủ tệp và không chứa bài học', () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'ph-'));
  build({ out, version: '1.0.9', api: 'https://example.workers.dev/api' });
  const html = fs.readFileSync(path.join(out, 'index.html'), 'utf8');
  assert.match(html, /connect-src 'self' https:\/\/example\.workers\.dev/);
  assert.ok(!html.includes('__API_ORIGIN__'));
  for (const m of html.matchAll(/<script src="([^"]+)"/g)) assert.ok(fs.existsSync(path.join(out, m[1])), 'thiếu ' + m[1]);
  for (const f of FROM_RENDERER) assert.ok(fs.existsSync(path.join(out, f)), f);
  assert.ok(!fs.existsSync(path.join(out, 'content')));
  const size = fs.readdirSync(out, { recursive: true }).reduce((a, f) => { const p = path.join(out, f); return a + (fs.statSync(p).isFile() ? fs.statSync(p).size : 0); }, 0);
  assert.ok(size < 6 * 1024 * 1024, 'gói quá nặng: ' + size);
  assert.match(fs.readFileSync(path.join(out, 'mobile-config.js'), 'utf8'), /1\.0\.9/);
  assert.match(fs.readFileSync(path.join(out, 'mobile-config.js'), 'utf8'), /"versionCode":1/);
  assert.match(fs.readFileSync(path.join(out, 'parent-boot.js'), 'utf8'), /XXXX-XXXX-XXXX/);
});

test('app Phụ huynh: có màn mua cho con, mã gia đình và tóm tắt nội dung Giáo trình văn hóa lớp 6–12', () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'ph-'));
  build({ out, version: '1.0.1', api: 'https://example.workers.dev/api' });
  for (const f of ['buy.js', 'digest.js', 'vietqr.js', 'payment-config.js', 'terms.js', 'vendor/qrcode.js']) assert.ok(fs.existsSync(path.join(out, f)), f);
  const html = fs.readFileSync(path.join(out, 'index.html'), 'utf8');
  for (const m of html.matchAll(/<script src="([^"]+)"/g)) assert.ok(fs.existsSync(path.join(out, m[1])), 'thiếu ' + m[1]);
  assert.ok(!/mua ngay trên app học của con: mở app/.test(html), 'không còn bắt phụ huynh mua trên máy của con');
  assert.match(html, /go-buy-now/);
  const boot = fs.readFileSync(path.join(out, 'parent-boot.js'), 'utf8');
  for (const n of ['createOrder', 'orderStatus', 'familyCreate']) assert.match(boot, new RegExp(n));
  const buy = fs.readFileSync(path.join(out, 'buy.js'), 'utf8');
  assert.match(buy, /family: fcode/);
  for (let g = 6; g <= 12; g++) {
    const w = { window: {} };
    require('vm').runInNewContext(fs.readFileSync(path.join(out, 'digest', 'van-hoa-' + g + '.js'), 'utf8'), w);
    const d = w.window.PARENT_DIGEST[g];
    assert.ok(d.subjects.length >= 6, 'lớp ' + g);
    const lessons = d.subjects.flatMap((s) => s.b.flatMap((b) => b.c.flatMap((c) => c.l)));
    assert.ok(lessons.length > 100, 'lớp ' + g);
    for (const k of ['sum', 'm', 'e']) assert.ok(lessons.filter((l) => l[k] && l[k].length).length > 5, 'lớp ' + g + ' thiếu ' + k);
    const all = JSON.stringify(d);
    assert.ok(!/\{[svck] /.test(all), 'không còn dấu màu {k ...}');
    assert.ok(!/"stem"|"choices"|"answer"/.test(all), 'không chứa câu hỏi và đáp án');
  }
});

test('khóa Tư duy & lập trình có trong danh sách khóa của app Phụ huynh', () => {
  const w = { window: {} };
  require('vm').runInNewContext(fs.readFileSync(path.join(__dirname, '..', 'parent', 'courses.js'), 'utf8'), w);
  const sc = w.window.PARENT_COURSES['tu-duy-lap-trinh-scratch'], py = w.window.PARENT_COURSES['tu-duy-lap-trinh-python'];
  assert.ok(sc.content.length >= 2 && /Scratch/.test(sc.intro));
  assert.ok(py.content.length >= 3 && /Chương 1/.test(py.content.join()) && /Python/.test(py.intro));
});

test('app Phụ huynh: nút bấm gắn bằng addEventListener (CSP chặn onclick dạng chuỗi); khóa người đi làm ghi "Mua khóa học"', () => {
  const src = fs.readFileSync(path.join(__dirname, '..', 'parent', 'parent.js'), 'utf8');
  assert.match(src, /k\.startsWith\('on'\) && typeof v === 'function'\) e\.addEventListener/);
  assert.match(src, /ai-nguoi-di-lam\/\.test\(x\.id\) \? 'Mua khóa học'/);
});
