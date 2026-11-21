// Bản chạy trên điện thoại (mobile/bridge) phải cho kết quả giống bản Windows (main/): cùng khóa, cùng quy tắc, cùng nội dung bài học.
const test = require('node:test');
const assert = require('node:assert');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const nacl = require('../mobile/vendor/nacl-fast.min.js');
const ML = require('../mobile/bridge/license.js');
const MApi = require('../mobile/bridge/api.js');
const MContent = require('../mobile/bridge/content.js');
const MMachine = require('../mobile/bridge/machine.js');
const Bridge = require('../mobile/bridge/bridge.js');
const Heartbeat = require('../mobile/bridge/heartbeat.js');
const nodeLic = require('../main/license');
const { PREFIX, b64u, evaluateKey } = require('../main/license/verify');
const { getMachineId } = require('../main/license/machine');
const nodeContent = require('../main/content-loader');
const { makeClient } = require('../main/orders.js');
const product = require('../main/product.json');

const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
const raw = new Uint8Array(publicKey.export({ type: 'spki', format: 'der' }).subarray(-32));
const verify = (msg, sig) => sig.length === 64 && nacl.sign.detached.verify(msg, sig, raw);
const MACHINE = getMachineId();
const NOW = new Date(2026, 10, 9);

function issue(p, priv = privateKey) {
  const body = Buffer.from(JSON.stringify({ v: 1, id: 'NL-ABC234', owner: 'Test', grades: [7], courses: [], machine: MACHINE, issued: '2026-01-01', expires: 'never', ...p }));
  return PREFIX + b64u(body) + '.' + b64u(crypto.sign(null, body, priv));
}
const memStorage = () => { const m = new Map(); return { get: (k) => (m.has(k) ? m.get(k) : null), set: (k, v) => m.set(k, v) }; };
const strip = (r) => { const { machineId, ...rest } = r; return rest; };

test('chữ ký: khóa hợp lệ, sai chữ ký, bị sửa nội dung, sai định dạng — cùng kết quả với bản Windows', () => {
  const other = crypto.generateKeyPairSync('ed25519').privateKey;
  const good = issue({});
  const [h, s] = good.split('.');
  const body = JSON.parse(Buffer.from(h.slice(PREFIX.length), 'base64url')); body.grades = 'all';
  const cases = [good, issue({}, other), PREFIX + b64u(JSON.stringify(body)) + '.' + s, 'rac', 'NL1-abc', issue({ expires: '2026-11-08' }), issue({ machine: 'AAAA-AAAA-AAAA' }), issue({ machine: '*' }), issue({ grades: 'all', courses: ['gia-su-ai'] })];
  for (const k of cases) assert.deepStrictEqual(ML.evaluateKey(k, MACHINE, NOW, verify), evaluateKey(k, MACHINE, NOW, publicKey), k.slice(0, 30));
});

test('kích hoạt, gộp nhiều khóa, thay khóa cùng mã đơn, thu hồi, hết hạn, đồng hồ lùi: kết quả giống bản Windows', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mob-'));
  const lic = ML.create({ storage: memStorage(), machineId: MACHINE, verify });
  const steps = [
    ['cur'], ['act', issue({ id: 'NL-AAAAAA', grades: [7] })], ['act', issue({ id: 'NL-BBBBBB', grades: [8], courses: ['gia-su-ai'] })],
    ['act', issue({ id: 'NL-AAAAAA', grades: [9] })], ['act', 'rác'], ['act', issue({ id: 'NL-CCCCCC', machine: 'ZZZZ-ZZZZ-ZZZZ' })],
    ['act', issue({ id: 'NL-DDDDDD', grades: [6], expires: '2026-11-08' })], ['ping'],
    ['revoke', ['BBBBBB'], {}], ['cur'], ['revoke', [], { AAAAAA: { grades: [9], courses: [] } }], ['cur'], ['revoke', [], {}], ['cur'], ['clock'], ['remove'], ['cur'],
  ];
  for (const [op, a, b] of steps) {
    if (op === 'cur') assert.deepStrictEqual(strip(lic.currentLicense(NOW)), strip(nodeLic.currentLicense(dir, NOW, publicKey)), op);
    if (op === 'act') assert.deepStrictEqual(strip(lic.activate(a, NOW)), strip(nodeLic.activate(dir, a, NOW, publicKey)), 'act');
    if (op === 'ping') assert.deepStrictEqual(lic.pingCodes(NOW), nodeLic.pingCodes(dir, NOW, publicKey));
    if (op === 'revoke') assert.strictEqual(lic.setRevoked(a, b), nodeLic.setRevoked(dir, a, b));
    if (op === 'clock') assert.deepStrictEqual(strip(lic.currentLicense(new Date(2026, 10, 1))), strip(nodeLic.currentLicense(dir, new Date(2026, 10, 1), publicKey)));
    if (op === 'remove') { lic.deactivate(); nodeLic.deactivate(dir); }
  }
});

test('mã máy điện thoại: đúng dạng XXXX-XXXX-XXXX, cố định theo thiết bị, khác nhau giữa các thiết bị', () => {
  const a = MMachine.machineIdFrom('android-id-1', nacl);
  assert.match(a, /^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/);
  assert.strictEqual(a, MMachine.machineIdFrom('android-id-1', nacl));
  assert.notStrictEqual(a, MMachine.machineIdFrom('android-id-2', nacl));
});

test('gọi máy chủ: cùng đường dẫn và nội dung như bản Windows, thêm platform android và claimDevice', async () => {
  const sent = [];
  const fetchFn = async (url, opt) => { sent.push({ url, method: opt.method, body: opt.body ? JSON.parse(opt.body) : null }); return { status: 200, ok: true, json: async () => ({ ok: 1 }) }; };
  const m = MApi.makeClient({ baseUrl: () => 'https://x.test/', fetchFn, machineId: () => 'AAAA-BBBB-CCCC' });
  const n = makeClient({ baseUrl: () => 'https://x.test/', fetchFn, machineId: () => 'AAAA-BBBB-CCCC' });
  const order = { name: 'A', phone: '0912345678', ids: ['gia-su-ai'], partnerCode: ' dt-x ', terms: { version: '1.2', at: 't' }, amount: 5 };
  await m.createOrder(order); await n.createOrder(order);
  await m.pinReset({ phone: '09', code: 'AB' }); await n.pinReset({ phone: '09', code: 'AB' });
  await m.ping({ ids: ['ABCDEF'], version: '1' }); await n.ping({ ids: ['ABCDEF'], version: '1' });
  await m.orderStatus('ABCDEFG'); await n.orderStatus('ABCDEFG');
  const [mc, nc, mp, np, mg, ng, ms, ns] = sent;
  assert.deepStrictEqual({ ...mc.body, platform: undefined }, { ...nc.body, platform: undefined });
  assert.strictEqual(mc.body.platform, 'android');
  assert.deepStrictEqual([mp, mg, ms].map((x) => [x.url, x.method, x.body]), [np, ng, ns].map((x) => [x.url, x.method, x.body]));
  sent.length = 0;
  await m.claimDevice({ code: 'ABCDEF', phone: '0912345678' }); await n.claimDevice({ code: 'ABCDEF', phone: '0912345678' });
  assert.deepStrictEqual(sent[0].body, { phone: '0912345678', code: 'ABCDEF', machineId: 'AAAA-BBBB-CCCC', platform: 'android' });
  assert.deepStrictEqual(sent[1].body, { phone: '0912345678', code: 'ABCDEF', machineId: 'AAAA-BBBB-CCCC', platform: 'win' });
  assert.strictEqual(sent[0].url, 'https://x.test/api/claim-device');
});

test('gọi máy chủ: lỗi 4xx trả thông báo, 5xx và lỗi mạng trả offline, chưa cấu hình trả offline', async () => {
  const mk = (fetchFn, base = 'https://x.test') => MApi.makeClient({ baseUrl: () => base, fetchFn, machineId: () => 'AAAA-BBBB-CCCC' });
  const reply = (status, data) => async () => ({ status, ok: status < 400, json: async () => data });
  assert.deepStrictEqual(await mk(reply(400, { error: 'Sai' })).createOrder({}), { ok: false, error: 'Sai' });
  assert.deepStrictEqual(await mk(reply(500, {})).createOrder({}), { ok: false, offline: true });
  assert.deepStrictEqual(await mk(async () => { throw new Error('net'); }).orderStatus('ABCDEF'), { ok: false, offline: true });
  assert.deepStrictEqual(await mk(reply(200, {}), '').createOrder({}), { ok: false, offline: true });
});

test('nội dung bài học: mục lục và bài (kèm hình) giống hệt bản Windows', async () => {
  const fetchText = async (url) => fs.readFileSync(path.join(__dirname, '..', url), 'utf8');
  const c = MContent.create({ fetchText, subjects: product.subjects });
  const subject = 'toan7';
  const manifest = await c.loadManifest(subject);
  assert.deepStrictEqual(manifest, nodeContent.loadManifest(subject));
  const files = [];
  for (const b of manifest.books) for (const ch of b.chapters) for (const l of ch.lessons) if (l.file) files.push(subject + '/' + l.file);
  const withFigure = files.find((f) => /"figure"/.test(fs.readFileSync(path.join(__dirname, '..', 'content', f), 'utf8')));
  for (const f of [files[0], withFigure].filter(Boolean)) assert.deepStrictEqual(await c.loadLesson(f), nodeContent.loadLesson(f), f);
  await assert.rejects(c.loadLesson('toan7/../../etc/passwd'), /không hợp lệ/);
  await assert.rejects(c.loadLesson('mon-la/x.json'), /Môn học không hợp lệ/);
  await assert.rejects(c.loadManifest('../x'), /Môn học không hợp lệ/);
});

function boot(extra = {}) {
  const storage = memStorage();
  const calls = [];
  const fetchFn = async (url, opt) => { calls.push({ url, body: opt && opt.body ? JSON.parse(opt.body) : null }); return (extra.fetch || (async () => ({ status: 200, ok: true, json: async () => ({ revoked: [] }) })))(url, opt); };
  const fetchText = async (url) => fs.readFileSync(path.join(__dirname, '..', url), 'utf8');
  const b = Bridge.create({ nacl, publicKey: raw, storage, rawDeviceId: 'android-xyz', fetchFn, fetchText, product, config: { ordersBaseUrl: 'https://x.test', version: '1.0.0', commit: 'abc' }, setTimeoutFn: () => {}, setIntervalFn: () => 1 });
  return { b, storage, calls };
}

test('cầu nối: chưa có khóa thì chỉ mở 2 bài đầu, bài khóa trả LOCKED; có khóa lớp 7 thì mở', async () => {
  const { b } = boot();
  const mid = b.api.machineId;
  const manifest = await b.api.loadManifest('toan7');
  const files = []; for (const bk of manifest.books) for (const c of bk.chapters) for (const l of c.lessons) if (l.file) files.push([l.file, l.locked]);
  assert.deepStrictEqual(files.slice(0, 2).map((f) => f[1]), [false, false]);
  assert.strictEqual(files[2][1], true);
  await assert.rejects(b.api.loadLesson('toan7/' + files[2][0]), /LOCKED/);
  assert.ok((await b.api.loadLesson('toan7/' + files[0][0])).id);
  const r = await b.api.activateLicense(issue({ machine: mid, grades: [7] }));
  assert.strictEqual(r.status, 'ok');
  assert.ok((await b.api.loadLesson('toan7/' + files[2][0])).id);
  assert.strictEqual((await b.api.loadLicense()).status, 'ok');
  assert.strictEqual((await b.api.removeLicense()).status, 'missing');
});

test('cầu nối: nhận khóa từ đơn mua ở máy tính (claimDevice) rồi kích hoạt và báo máy chủ', async () => {
  let mid;
  const { b, calls } = boot({ fetch: async (url, opt) => {
    if (url.endsWith('/api/claim-device')) return { status: 200, ok: true, json: async () => ({ key: issue({ id: 'NL-ABC234', machine: mid, grades: [7] }) }) };
    return { status: 200, ok: true, json: async () => ({ revoked: [] }) };
  } });
  mid = b.api.machineId;
  const r = await b.api.claimDevice({ code: 'ABC234', phone: '0912345678' });
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.license.status, 'ok');
  assert.deepStrictEqual(r.license.grades, [7]);
  await new Promise((res) => setImmediate(res));
  assert.ok(calls.some((c) => c.url.endsWith('/api/ping') && c.body.ids.includes('ABC234')), 'phải gửi tín hiệu sau khi kích hoạt');
});

test('cầu nối: đồng bộ gia đình (familySync) nhận nhiều khóa của phụ huynh và kích hoạt hết', async () => {
  let mid; let sent;
  const { b } = boot({ fetch: async (url, opt) => {
    if (url.endsWith('/api/family/sync')) { sent = JSON.parse(opt.body); return { status: 200, ok: true, json: async () => ({ keys: [{ code: 'ABC234', key: issue({ id: 'NL-ABC234', machine: mid, grades: [], courses: ['tu-duy-lap-trinh'] }) }, { code: 'XYZ234', key: issue({ id: 'NL-XYZ234', machine: mid, grades: [7] }) }], full: 1 }) }; }
    return { status: 200, ok: true, json: async () => ({ revoked: [] }) };
  } });
  mid = b.api.machineId;
  const r = await b.api.familySync({ fcode: 'ABCD2345' });
  assert.strictEqual(r.ok, true); assert.strictEqual(r.activated, 2); assert.strictEqual(r.full, 1);
  assert.deepStrictEqual(sent, { fcode: 'ABCD2345', machineId: mid, platform: 'android' });
  const lic = await b.api.loadLicense();
  assert.deepStrictEqual(lic.grades, [7]); assert.ok(lic.courses.includes('tu-duy-lap-trinh'));
});

test('cầu nối: máy chủ báo đơn bị thu hồi thì khóa mất hiệu lực và giao diện được báo', async () => {
  let mid; let revoked = false;
  const { b } = boot({ fetch: async (url) => ({ status: 200, ok: true, json: async () => (url.endsWith('/api/ping') ? { revoked: revoked ? ['ABC234'] : [] } : {}) }) });
  mid = b.api.machineId;
  let notified = 0; b.api.onLicenseChanged(() => { notified++; });
  await b.api.activateLicense(issue({ id: 'NL-ABC234', machine: mid, grades: [7] }));
  await new Promise((res) => setTimeout(res, 20)); // chờ tín hiệu gửi nền sau khi kích hoạt xong (lúc này chưa thu hồi)
  revoked = true;
  assert.strictEqual((await b.heartbeat.beat()).changed, true);
  assert.strictEqual(notified, 1);
  assert.strictEqual((await b.api.loadLicense()).status, 'revoked');
});

test('cầu nối: cập nhật tắt, thông tin sản phẩm và bản đúng', async () => {
  const { b } = boot();
  assert.deepStrictEqual(await b.api.updateStatus(), { state: 'off' });
  assert.strictEqual(await b.api.installUpdate(), false);
  assert.strictEqual((await b.api.productInfo()).id, 'nam-linh-educenter');
  assert.deepStrictEqual(await b.api.appInfo(), { version: '1.0.0', commit: 'abc' });
});

test('bản sao dữ liệu người dùng: lưu, đọc lại, xóa; không gọi vòng khi setItem bị bọc', () => {
  const data = new Map();
  const ls = { get length() { return data.size; }, key: (i) => [...data.keys()][i] };
  const get = function (k) { return data.has(k) ? data.get(k) : null; };
  const set = function (k, v) { data.set(k, String(v)); };
  const remove = function (k) { data.delete(k); };
  const us = Bridge.mirrorUserStore(ls, get, set, remove);
  us.set('pin', '1234'); us.set('khac', 'x');
  data.set('khong-lien-quan', 'y');
  assert.deepStrictEqual(us.all(), { pin: '1234', khac: 'x' });
  us.set('pin', null);
  assert.deepStrictEqual(us.all(), { khac: 'x' });
});

test('gói www cho Android: nạp cầu nối trước persist-shim, cho phép gọi máy chủ, khóa công khai đúng 32 byte', () => {
  const { rewriteIndex, rawPublicKey, SCRIPTS } = require('../tools/build-mobile-www.js');
  const html = fs.readFileSync(path.join(__dirname, '..', 'renderer', 'index.html'), 'utf8');
  const out = rewriteIndex(html, 'https://x.test');
  const pos = (s) => out.indexOf(`src="${s}"`);
  for (const s of SCRIPTS) assert.ok(pos(s) > 0, s);
  assert.ok(pos('mobile/boot.js') < pos('persist-shim.js'), 'cầu nối phải nạp trước persist-shim.js');
  assert.ok(pos('mobile/vendor/nacl-fast.min.js') < pos('mobile/license.js'));
  assert.match(out, /connect-src 'self' https:\/\/x\.test/);
  assert.match(out, /name="viewport"/);
  assert.ok(!out.includes('../core/rational.js'));
  assert.strictEqual(Buffer.from(rawPublicKey(path.join(__dirname, '..', 'main', 'license', 'public-key.pem')), 'base64').length, 32);
});
