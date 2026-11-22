// Kho gói nội dung trên điện thoại (mobile/bridge/packs.js): cùng gói với bản Windows, giải mã bằng WebCrypto.
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');
const nacl = require('../mobile/vendor/nacl-fast.min.js');
const Packs = require('../mobile/bridge/packs.js');
const Bridge = require('../mobile/bridge/bridge.js');
const { deriveGradeKey, deriveCourseKey } = require('../core/pack-format');
const { build } = require('../tools/build-packs');
const { PREFIX, b64u } = require('../main/license/verify');
const product = require('../main/product.json');

const MASTER = 'q'.repeat(40);
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'nlpm-'));
const w = (f, t) => { fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, t); };
const gunzip = async (bytes) => new Uint8Array(zlib.gunzipSync(Buffer.from(bytes)));
const memKV = () => { const m = new Map(); return { get: async (k) => (m.has(k) ? m.get(k) : null), set: async (k, v) => { m.set(k, v); }, remove: async (k) => { m.delete(k); } }; };

function content() {
  const d = tmp();
  const man = { books: [{ chapters: [{ lessons: [{ file: 'tap1/b1.json' }, { file: 'tap1/b2.json' }, { file: 'tap1/b3.json' }] }] }] };
  w(path.join(d, 'toan7/manifest.json'), JSON.stringify(man));
  w(path.join(d, 'toan7/tap1/b1.json'), JSON.stringify({ id: 'b1', items: [], theory: [] }));
  w(path.join(d, 'toan7/tap1/b2.json'), JSON.stringify({ id: 'b2', items: [], theory: [] }));
  w(path.join(d, 'toan7/tap1/b3.json'), JSON.stringify({ id: 'b3', items: [], theory: [{ type: 'figure', figure: 'figures/f.svg' }] }));
  w(path.join(d, 'toan7/figures/f.svg'), '<svg>trả phí</svg>');
  return d;
}

function world({ online = true, corrupt = false } = {}) {
  const dir = content(); const out = tmp();
  const r = build({ contentDir: dir, outDir: out, master: MASTER });
  const keys = { 7: deriveGradeKey(MASTER, 7).toString('base64') };
  const calls = [];
  const client = { packKeys: async () => (online ? { ok: true, data: { base: 'b', keys } } : { ok: false, offline: true }) };
  const fetchFn = async (url) => {
    calls.push(url);
    if (!online) throw new Error('offline');
    const p = new URL(url).pathname;
    if (p === '/api/pack/index') return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(path.join(out, 'index.json'), 'utf8')) };
    const name = p.split('/').pop();
    let buf = Buffer.from(fs.readFileSync(path.join(out, name)));
    if (corrupt) buf[40] ^= 1;
    return { ok: true, status: 200, arrayBuffer: async () => buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length) };
  };
  const events = [];
  const store = memKV();
  const mk = () => Packs.create({ client, lic: { rawKeys: () => ['NL1-x'] }, baseUrl: () => 'https://x.test', fetchFn, store, subtle: crypto.webcrypto.subtle, gunzip, enabled: true, send: (s) => events.push(s.state) });
  return { packs: mk(), mk, calls, events, store, dir, r };
}

test('điện thoại: tải gói đúng lớp, lưu vào kho, đọc lại cả sau khi khởi động lại app', async () => {
  const { packs, mk, calls, events } = world();
  assert.equal(await packs.read('toan7/tap1/b3.json'), null);
  const r = await packs.sync();
  assert.equal(r.ok, true); assert.equal(r.downloaded, 1);
  assert.equal(JSON.parse(await packs.read('toan7/tap1/b3.json')).id, 'b3');
  assert.equal(await packs.read('toan7/figures/f.svg'), '<svg>trả phí</svg>');
  assert.equal(await packs.read('toan8/tap1/b3.json'), null);
  assert.ok(events.includes('downloading') && events.at(-1) === 'ready');
  assert.deepEqual((await packs.status()).grades, [7]);
  const n = calls.length;
  await packs.sync(); // đủ rồi: chỉ hỏi danh sách, không tải lại gói
  assert.equal(calls.length, n + 1);
  const again = mk(); // mô phỏng mở lại app: cùng kho, bộ nhớ trống
  assert.equal(JSON.parse(await again.read('toan7/tap1/b3.json')).id, 'b3');
});

test('điện thoại: dữ liệu gói bị mất mà state còn thì tải lại', async () => {
  const { packs, mk, store } = world();
  await packs.sync();
  await store.remove('data:g7');
  const again = mk();
  assert.equal(await again.read('toan7/tap1/b3.json'), null);
  const r = await again.sync();
  assert.equal(r.downloaded, 1);
  assert.equal(JSON.parse(await again.read('toan7/tap1/b3.json')).id, 'b3');
});

test('điện thoại: gói bị sửa thì không lưu; mất mạng thì báo offline', async () => {
  const bad = world({ corrupt: true });
  assert.equal((await bad.packs.sync()).ok, false);
  assert.equal(await bad.packs.read('toan7/tap1/b3.json'), null);
  assert.equal((await bad.packs.status()).state, 'error');
  const off = world({ online: false });
  const r = await off.packs.sync();
  assert.equal(r.offline, true);
});

test('điện thoại: không bật chế độ gói thì không làm gì', async () => {
  const p = Packs.create({ client: { packKeys: async () => { throw new Error('không được gọi'); } }, lic: { rawKeys: () => ['k'] }, enabled: false, store: memKV() });
  assert.deepEqual(await p.sync(), { ok: true, disabled: true });
  assert.equal(await p.read('toan7/x.json'), null);
});

test('cầu nối: bài trả phí không có trong apk thì đọc từ gói; chưa tải thì NOT_DOWNLOADED; có khoá mới được mở', async () => {
  const { store, dir } = world();
  // apk chỉ giữ mục lục + 2 bài đầu: bài 3 và hình không có trong thư mục "apk".
  const apk = tmp(); fs.cpSync(dir, apk, { recursive: true });
  fs.rmSync(path.join(apk, 'toan7/tap1/b3.json')); fs.rmSync(path.join(apk, 'toan7/figures'), { recursive: true });
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const raw = new Uint8Array(publicKey.export({ type: 'spki', format: 'der' }).subarray(-32));
  const issue = (machine) => { const body = Buffer.from(JSON.stringify({ v: 1, id: 'NL-ABC234', owner: 'T', grades: [7], courses: [], machine, issued: '2026-01-01', expires: 'never' })); return PREFIX + b64u(body) + '.' + b64u(crypto.sign(null, body, privateKey)); };
  const keys = { 7: deriveGradeKey(MASTER, 7).toString('base64') };
  const out2 = tmp(); const built = build({ contentDir: dir, outDir: out2, master: MASTER });
  const fetchFn = async (url) => {
    const p = new URL(url).pathname;
    if (p === '/api/pack/keys') return { ok: true, status: 200, json: async () => ({ base: 'b', keys }) };
    if (p === '/api/pack/index') return { ok: true, status: 200, json: async () => built.index };
    if (p.startsWith('/api/pack/file/')) { const b = fs.readFileSync(path.join(out2, p.split('/').pop())); return { ok: true, status: 200, arrayBuffer: async () => b.buffer.slice(b.byteOffset, b.byteOffset + b.length) }; }
    return { ok: true, status: 200, json: async () => ({ revoked: [] }) };
  };
  const fetchText = async (url) => fs.readFileSync(path.join(apk, url.replace(/^content\//, '')), 'utf8');
  const mem = new Map();
  const b = Bridge.create({ nacl, publicKey: raw, storage: { get: (k) => (mem.has(k) ? mem.get(k) : null), set: (k, v) => mem.set(k, v) }, rawDeviceId: 'android-xyz', fetchFn, fetchText, product,
    config: { ordersBaseUrl: 'https://x.test', version: '1.0.0', commit: 'abc' }, setTimeoutFn: () => {}, setIntervalFn: () => 1,
    packs: { enabled: true, store, subtle: crypto.webcrypto.subtle, gunzip } });
  assert.equal((await b.api.loadLesson('toan7/tap1/b1.json')).id, 'b1'); // bài học thử nằm trong apk
  await assert.rejects(b.api.loadLesson('toan7/tap1/b3.json'), /LOCKED/); // chưa có khoá
  b.license.activate(issue(b.api.machineId));
  await assert.rejects(b.api.loadLesson('toan7/tap1/b3.json'), /NOT_DOWNLOADED/); // có khoá nhưng chưa tải
  await b.packs.sync();
  const l = await b.api.loadLesson('toan7/tap1/b3.json');
  assert.equal(l.id, 'b3'); assert.equal(l.theory[0].figureSvg, '<svg>trả phí</svg>');
  assert.deepEqual((await b.api.packsStatus()).grades, [7]);
});

test('điện thoại: gói khóa Kỹ năng tải về, chỉ trả cho khóa đã mua; bản không tách gói thì trả rỗng', async () => {
  const rd = tmp();
  for (const f of ['tu-duy-content.js', 'tu-duy.js', 'gia-su-ai-content.js', 'gia-su-ai.js', 'ai-work-claude.js', 'ai-work-chatgpt.js', 'ai-work-gemini.js']) fs.copyFileSync(path.join(__dirname, '..', 'renderer', f), path.join(rd, f));
  const out = tmp(); const built = build({ contentDir: content(), outDir: out, master: MASTER, rendererDir: rd });
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const raw = new Uint8Array(publicKey.export({ type: 'spki', format: 'der' }).subarray(-32));
  const issue = (machine, courses) => { const body = Buffer.from(JSON.stringify({ v: 1, id: 'NL-ABC234', owner: 'T', grades: [], courses, machine, issued: '2026-01-01', expires: 'never' })); return PREFIX + b64u(body) + '.' + b64u(crypto.sign(null, body, privateKey)); };
  const cKey = (id) => deriveCourseKey(MASTER, id).toString('base64');
  const fetchFn = async (url) => {
    const p = new URL(url).pathname;
    if (p === '/api/pack/keys') return { ok: true, status: 200, json: async () => ({ base: 'b', keys: {}, courses: { 'gia-su-ai': cKey('gia-su-ai') } }) };
    if (p === '/api/pack/index') return { ok: true, status: 200, json: async () => built.index };
    if (p.startsWith('/api/pack/file/')) { const b = fs.readFileSync(path.join(out, p.split('/').pop())); return { ok: true, status: 200, arrayBuffer: async () => b.buffer.slice(b.byteOffset, b.byteOffset + b.length) }; }
    return { ok: true, status: 200, json: async () => ({ revoked: [] }) };
  };
  const mk = (enabled) => { const mem = new Map(); return Bridge.create({ nacl, publicKey: raw, storage: { get: (k) => (mem.has(k) ? mem.get(k) : null), set: (k, v) => mem.set(k, v) }, rawDeviceId: 'android-xyz', fetchFn, fetchText: async () => { throw new Error('x'); }, product,
    config: { ordersBaseUrl: 'https://x.test', version: '1.0.0', commit: 'abc' }, setTimeoutFn: () => {}, setIntervalFn: () => 1, packs: { enabled, store: memKV(), subtle: crypto.webcrypto.subtle, gunzip } }); };
  const b = mk(true);
  assert.deepEqual(await b.api.courseContent('gia-su-ai'), { ok: false, error: 'LOCKED' }); // chưa mua
  b.license.activate(issue(b.api.machineId, ['gia-su-ai']));
  assert.deepEqual(await b.api.courseContent('gia-su-ai'), { ok: false, error: 'NOT_DOWNLOADED' });
  const sres = await b.packs.sync();
  assert.equal(sres.ok, true, JSON.stringify(sres) + JSON.stringify(await b.api.packsStatus()));
  const r = await b.api.courseContent('gia-su-ai');
  assert.equal(r.ok, true, JSON.stringify(r).slice(0, 200) + JSON.stringify(sres));
  assert.ok(JSON.parse(r.files.GIA_SU_AI).bai3.html);
  assert.deepEqual(await b.api.courseContent('ai-nguoi-di-lam-claude'), { ok: false, error: 'LOCKED' });
  assert.deepEqual((await b.api.packsStatus()).courses, ['gia-su-ai']);
  // bản cũ (apk giữ đủ nội dung): đã mua thì trả rỗng, giao diện dùng nội dung có sẵn
  const old = mk(false); old.license.activate(issue(old.api.machineId, ['gia-su-ai']));
  assert.deepEqual(await old.api.courseContent('gia-su-ai'), { ok: true, files: {} });
});
