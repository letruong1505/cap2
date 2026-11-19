// Cập nhật Android: gói nội dung (OTA) phải được ký đúng, bị từ chối khi bị sửa hoặc ký sai khóa, và trạng thái cập nhật phải đúng.
const test = require('node:test');
const assert = require('node:assert');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const nacl = require('../mobile/vendor/nacl-fast.min.js');
const ML = require('../mobile/bridge/license.js');
const Updater = require('../mobile/bridge/updater.js');
const { createBundle, verifyBundle } = require('../tools/build-ota.js');
const { build: buildWww, rawPublicKey } = require('../tools/build-mobile-www.js');

const ROOT = path.join(__dirname, '..');
const ota = crypto.generateKeyPairSync('ed25519');
const otaPem = ota.privateKey.export({ type: 'pkcs8', format: 'pem' });
const otaPubB64 = Buffer.from(ota.publicKey.export({ type: 'spki', format: 'der' }).subarray(-32)).toString('base64');
const other = crypto.generateKeyPairSync('ed25519');

let www;
const wwwDir = () => {
  if (!www) {
    www = fs.mkdtempSync(path.join(os.tmpdir(), 'nl-ota-'));
    buildWww({ out: www, pubkey: path.join(ROOT, 'main', 'license', 'public-key.pem'), version: '1.0.7', commit: 'abc', api: 'https://api.test', versionCode: 7, otaPublicKey: otaPubB64 });
  }
  return www;
};
const bundle = (build, extra = {}) => createBundle({ www: wwwDir(), build, version: '1.0.' + build, privateKeyPem: otaPem, ...extra });

test('gói OTA: chỉ chứa mã giao diện (không có bài học, phông chữ, trang khởi động), ký đúng và nhỏ gọn', () => {
  const text = bundle(8);
  const p = verifyBundle(text, otaPubB64);
  assert.strictEqual(p.build, 8);
  assert.strictEqual(p.version, '1.0.8');
  const names = Object.keys(p.files);
  for (const need of ['app.js', 'styles.css', 'purchase.js', 'mobile/bridge.js', 'mobile/updater.js', 'mobile/boot.js', 'mobile/mobile-config.js', 'product.json']) assert.ok(names.includes(need), need);
  for (const no of names) assert.ok(!/^(content|fonts)\//.test(no) && !/ota-boot|ota-store|native\.js|LICENSE/.test(no), no);
  assert.match(p.html, /<script src="app\.js">/);
  assert.ok(text.length < 4 * 1024 * 1024, 'gói quá lớn: ' + text.length);
});

test('gói OTA: bị sửa, ký bằng khóa khác hoặc không đúng định dạng đều bị từ chối', () => {
  const text = bundle(9);
  const [p, s] = text.slice(5).split('.');
  const evil = Buffer.from(JSON.stringify({ ...JSON.parse(Buffer.from(p, 'base64url').toString()), version: 'xau' })).toString('base64url');
  assert.throws(() => verifyBundle('NLO1-' + evil + '.' + s, otaPubB64), /Chữ ký/);
  assert.throws(() => verifyBundle(text, Buffer.from(other.publicKey.export({ type: 'spki', format: 'der' }).subarray(-32)).toString('base64')), /Chữ ký/);
  assert.throws(() => verifyBundle('rac', otaPubB64), /Không phải gói/);
  assert.throws(() => verifyBundle('NLO1-abc', otaPubB64), /hỏng/);
  const forged = createBundle({ www: wwwDir(), build: 9, version: '1', privateKeyPem: other.privateKey.export({ type: 'pkcs8', format: 'pem' }) });
  assert.throws(() => verifyBundle(forged, otaPubB64), /Chữ ký/);
});

// --- bộ cập nhật trong ứng dụng ---
function setup({ code = 7, latest, bundles = {}, stored = null, bad = [], running = null, now = 1_000_000_000 } = {}) {
  const kv = new Map([['current', stored], ['bad', bad]]);
  const ls = new Map();
  const calls = []; const opened = []; let reloaded = 0;
  const fetchFn = async (url) => {
    calls.push(url);
    const route = url.replace('https://api.test', '');
    if (route === '/api/app/android/latest') return latest ? { ok: true, status: 200, json: async () => latest } : { ok: false, status: 502 };
    const m = /\/api\/app\/android\/ota\/(\d+)$/.exec(route);
    if (m && bundles[m[1]]) return { ok: true, status: 200, text: async () => bundles[m[1]] };
    return { ok: false, status: 404 };
  };
  let t = now;
  const up = Updater.create({
    fetchFn, baseUrl: () => 'https://api.test', nacl, b64uToBytes: ML.b64uToBytes, otaPublicKey: new Uint8Array(Buffer.from(otaPubB64, 'base64')),
    native: { code, version: '1.0.' + code }, runningBuild: () => running || code,
    store: { get: async (k) => (kv.has(k) ? kv.get(k) : null), set: async (k, v) => { kv.set(k, v); } },
    storage: { get: (k) => ls.get(k) || null, set: (k, v) => { ls.set(k, v); } },
    openUrl: (u) => opened.push(u), reload: () => { reloaded++; }, now: () => t,
  });
  return { up, kv, calls, opened, reloaded: () => reloaded, advance: (ms) => { t += ms; } };
}
const L = (o) => ({ version: '1.0.9', versionCode: 9, otaBuild: 9, minNative: 0, notes: 'Sửa lỗi nhận khóa', apkUrl: 'https://r2.test/a.apk', ...o });

test('có bản mới và apk cho phép OTA: tự tải, kiểm tra chữ ký, lưu lại, báo "ready"; bấm cài thì nạp lại', async () => {
  const s = setup({ latest: L(), bundles: { 9: bundle(9) } });
  const seen = []; s.up.onUpdate((x) => seen.push(x.state));
  const st = await s.up.check();
  assert.strictEqual(st.state, 'ready');
  assert.strictEqual(st.version, '1.0.9');
  assert.deepStrictEqual(seen.filter((x, i) => seen.indexOf(x) === i), ['checking', 'downloading', 'ready']);
  const cur = s.kv.get('current');
  assert.strictEqual(cur.build, 9);
  assert.strictEqual(cur.tries, 0);
  assert.ok(cur.html.includes('app.js') && typeof cur.files['app.js'] === 'string');
  assert.deepStrictEqual(s.opened, []);
  assert.strictEqual(await s.up.install(), true);
  assert.strictEqual(s.reloaded(), 1);
});

test('gói bị sửa hoặc sai số build: không lưu, báo lỗi, bản đang chạy không đổi', async () => {
  const good = bundle(9);
  const [p, sg] = good.slice(5).split('.');
  const tampered = 'NLO1-' + Buffer.from(JSON.stringify({ ...JSON.parse(Buffer.from(p, 'base64url').toString()), html: '<script>evil()</script>' })).toString('base64url') + '.' + sg;
  let s = setup({ latest: L(), bundles: { 9: tampered } });
  let st = await s.up.check();
  assert.strictEqual(st.state, 'error');
  assert.strictEqual(s.kv.get('current'), null);
  // gói cũ (build 8) bị phát lại thay cho build 9
  s = setup({ latest: L(), bundles: { 9: bundle(8) } });
  st = await s.up.check();
  assert.strictEqual(st.state, 'error');
  assert.strictEqual(s.kv.get('current'), null);
});

test('thay đổi cần apk mới (minNative cao hơn) hoặc gói từng bị hỏng: báo có bản mới và mở địa chỉ tải apk', async () => {
  let s = setup({ latest: L({ minNative: 9 }), bundles: { 9: bundle(9) } });
  let st = await s.up.check();
  assert.strictEqual(st.state, 'available');
  assert.strictEqual(st.version, '1.0.9');
  assert.strictEqual(st.notes, 'Sửa lỗi nhận khóa');
  assert.ok(!s.calls.some((u) => /\/ota\//.test(u)), 'không tải gói khi apk chưa đủ mới');
  await s.up.download();
  assert.deepStrictEqual(s.opened, ['https://r2.test/a.apk']);
  s = setup({ latest: L(), bundles: { 9: bundle(9) }, bad: [9] });
  st = await s.up.check();
  assert.strictEqual(st.state, 'available');
});

test('đã dùng bản mới nhất thì không làm gì; apk mới hơn gói OTA đã lưu thì bỏ qua gói cũ', async () => {
  let s = setup({ latest: L({ versionCode: 7, otaBuild: 7, version: '1.0.7' }) });
  assert.strictEqual((await s.up.check()).state, 'none');
  // gói đã lưu build 8 nhưng apk vừa cài là build 9 → coi như đã mới nhất
  s = setup({ code: 9, latest: L(), stored: { build: 8, version: '1.0.8', minNative: 0, html: 'x', files: {} } });
  assert.strictEqual((await s.up.check()).state, 'none');
  assert.ok(!s.calls.some((u) => /\/ota\//.test(u)));
});

test('gói đã tải trước đó nhưng chưa dùng: lần kiểm tra sau báo "ready" mà không tải lại', async () => {
  const s = setup({ latest: L(), stored: { build: 9, version: '1.0.9', minNative: 0, html: 'x', files: {} }, running: 7 });
  const st = await s.up.check();
  assert.strictEqual(st.state, 'ready');
  assert.ok(!s.calls.some((u) => /\/ota\//.test(u)));
});

test('kiểm tra ngầm: tối đa 6 giờ một lần, lỗi mạng thì im lặng', async () => {
  const s = setup({ latest: L({ versionCode: 7, otaBuild: 7 }) });
  await s.up.check({ auto: true });
  await s.up.check({ auto: true });
  assert.strictEqual(s.calls.filter((u) => /latest/.test(u)).length, 1);
  s.advance(6 * 3600 * 1000 + 1);
  await s.up.check({ auto: true });
  assert.strictEqual(s.calls.filter((u) => /latest/.test(u)).length, 2);
  const off = setup({ latest: null });
  const st = await off.up.check({ auto: true });
  assert.notStrictEqual(st.state, 'error');
  assert.strictEqual((await off.up.check()).state, 'error'); // kiểm tra thủ công thì báo lỗi
});

test('gói www: index.html chỉ là trang khởi động OTA; giao diện nằm trong app.html cùng khóa công khai OTA', () => {
  const dir = wwwDir();
  const launcher = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const app = fs.readFileSync(path.join(dir, 'app.html'), 'utf8');
  assert.match(launcher, /ota-boot\.js/);
  assert.ok(!/app\.js|purchase\.js/.test(launcher));
  assert.match(launcher, /script-src 'self' blob:/);
  assert.match(app, /script-src 'self' blob:/);
  assert.ok(app.indexOf('mobile/native.js') < app.indexOf('mobile/boot.js'));
  assert.ok(app.indexOf('mobile/ota-store.js') < app.indexOf('mobile/updater.js'));
  const native = fs.readFileSync(path.join(dir, 'mobile', 'native.js'), 'utf8');
  assert.match(native, new RegExp(otaPubB64.replace(/[+/=]/g, '\\$&')));
  assert.match(native, /"code":7/);
  assert.strictEqual(Buffer.from(fs.readFileSync(path.join(ROOT, 'mobile', 'ota-public-key.txt'), 'utf8').trim(), 'base64').length, 32);
});
