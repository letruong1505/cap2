const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { deriveGradeKey, encryptPack, decryptPack, sha256 } = require('../core/pack-format');
const { build, freeFiles } = require('../tools/build-packs');
const { createPackStore } = require('../main/pack-store');

const MASTER = 'k'.repeat(40);
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'nlpack-'));
const w = (f, t) => { fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, t); };

function fakeContent() {
  const d = tmp();
  for (const s of ['toan7', 'ly7', 'toan8']) {
    const man = { books: [{ chapters: [{ lessons: [{ file: 'tap1/b1.json' }, { file: 'tap1/b2.json' }, { file: 'tap1/b3.json' }] }] }] };
    w(path.join(d, s, 'manifest.json'), JSON.stringify(man));
    w(path.join(d, s, 'tap1/b1.json'), JSON.stringify({ id: 'b1', items: [{ figure: 'figures/f1.svg' }] }));
    w(path.join(d, s, 'tap1/b2.json'), JSON.stringify({ id: 'b2', theory: [{ type: 'figure', figure: 'figures/f2.svg' }] }));
    w(path.join(d, s, 'tap1/b3.json'), JSON.stringify({ id: 'b3', secret: 'nội dung trả phí ' + s }));
    for (const f of ['f1', 'f2', 'f3']) w(path.join(d, s, `figures/${f}.svg`), `<svg>${f}</svg>`);
  }
  return d;
}

test('gói mã hóa: giải mã đúng khoá, sai khoá hoặc bị sửa thì từ chối', () => {
  const key = deriveGradeKey(MASTER, 7);
  const blob = encryptPack({ 'toan7/a.json': 'xin chào' }, key);
  assert.deepEqual(decryptPack(blob, key), { 'toan7/a.json': 'xin chào' });
  assert.throws(() => decryptPack(blob, deriveGradeKey(MASTER, 8)));
  const bad = Buffer.from(blob); bad[bad.length - 1] ^= 1;
  assert.throws(() => decryptPack(bad, key));
  assert.throws(() => decryptPack(Buffer.from('rac'), key));
  assert.ok(!blob.toString('utf8').includes('xin chào'));
});

test('đóng gói: mỗi lớp một gói, giữ lại mục lục, 2 bài học thử và hình của chúng', () => {
  const dir = fakeContent(); const out = tmp(); const mode = path.join(tmp(), 'm.json');
  assert.deepEqual([...freeFiles(dir, 'toan7')].sort(), ['figures/f1.svg', 'figures/f2.svg', 'manifest.json', 'tap1/b1.json', 'tap1/b2.json']);
  const r = build({ contentDir: dir, outDir: out, master: MASTER, prune: true, modeFile: mode });
  assert.deepEqual(Object.keys(r.index.packs), ['7', '8']);
  assert.equal(JSON.parse(fs.readFileSync(mode, 'utf8')).mode, 'packs');
  assert.ok(fs.existsSync(path.join(dir, 'toan7/tap1/b1.json')));
  assert.ok(!fs.existsSync(path.join(dir, 'toan7/tap1/b3.json')));
  assert.ok(!fs.existsSync(path.join(dir, 'toan7/figures/f3.svg')));
  const p7 = path.join(out, r.index.packs[7].file);
  const files = decryptPack(fs.readFileSync(p7), deriveGradeKey(MASTER, 7));
  assert.ok(files['toan7/tap1/b3.json'].includes('trả phí toan7') && files['ly7/tap1/b3.json'] && !files['toan8/tap1/b3.json']);
  assert.equal(sha256(fs.readFileSync(p7)), r.index.packs[7].sha256);
});

// --- Kho gói trên máy ---
function world({ grades = [7], online = true, corrupt = false } = {}) {
  const content = fakeContent(); const out = tmp();
  const r = build({ contentDir: content, outDir: out, master: MASTER, prune: false });
  const keys = {}; for (const g of grades) keys[g] = deriveGradeKey(MASTER, g).toString('base64');
  const calls = { keys: 0, fetch: [] };
  const client = { packKeys: async () => { calls.keys++; return online ? { ok: true, data: { base: 'https://r2.test/educenter-content', keys } } : { ok: false, offline: true }; } };
  const fetchFn = async (url) => {
    calls.fetch.push(url);
    if (!online) throw new Error('offline');
    const name = url.split('/').pop();
    const file = name === 'index.json' ? path.join(out, 'index.json') : path.join(out, name);
    if (!fs.existsSync(file)) return { ok: false, status: 404 };
    let buf = fs.readFileSync(file); if (corrupt && name !== 'index.json') { buf = Buffer.from(buf); buf[40] ^= 1; }
    return { ok: true, status: 200, json: async () => JSON.parse(buf.toString()), arrayBuffer: async () => buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length) };
  };
  const dir = tmp();
  const events = [];
  const store = createPackStore({ dir, licenseDir: dir, client, lic: { rawKeys: () => ['NL1-x'] }, fetchFn, send: (s) => events.push(s.state) });
  return { store, calls, events, dir, r, setOnline: (v) => { online = v; } };
}

test('kho gói: tải đúng lớp có bản quyền, lưu máy và đọc lại được', async () => {
  const { store, calls, events } = world({ grades: [7] });
  assert.equal(store.read('toan7/tap1/b3.json'), null); // chưa tải
  const r = await store.sync();
  assert.equal(r.ok, true); assert.equal(r.downloaded, 1);
  assert.deepEqual(store.have(), [7]);
  assert.ok(JSON.parse(store.read('toan7/tap1/b3.json')).secret.includes('toan7'));
  assert.equal(store.read('toan8/tap1/b3.json'), null); // lớp 8 chưa mua
  assert.ok(events.includes('downloading') && events.at(-1) === 'ready');
  const before = calls.fetch.length;
  await store.sync(); // đã đủ thì chỉ hỏi index, không tải lại gói
  assert.equal(calls.fetch.length, before + 1);
});

test('kho gói: file gói bị xóa mà state.json còn thì tải lại và have() không tính gói thiếu', async () => {
  const { store, dir } = world({ grades: [7] });
  await store.sync();
  for (const f of fs.readdirSync(path.join(dir, 'packs'))) if (f.endsWith('.nlp')) fs.unlinkSync(path.join(dir, 'packs', f));
  assert.deepEqual(store.have(), []);
  assert.equal(store.read('toan7/tap1/b3.json'), null);
  const r = await store.sync();
  assert.equal(r.downloaded, 1);
  assert.deepEqual(store.have(), [7]);
  assert.ok(store.read('toan7/tap1/b3.json'));
});

test('kho gói: mất mạng thì báo offline và không làm hỏng gói đã có; có mạng lại thì tải tiếp', async () => {
  const w1 = world({ grades: [7], online: false });
  const r = await w1.store.sync();
  assert.equal(r.ok, false); assert.equal(r.offline, true);
  assert.equal(w1.store.status().state, 'offline');
  w1.setOnline(true);
  assert.equal((await w1.store.sync()).downloaded, 1);
});

test('kho gói: gói bị sửa trên đường tải (sai mã kiểm tra) thì không lưu', async () => {
  const { store } = world({ grades: [7], corrupt: true });
  const r = await store.sync();
  assert.equal(r.ok, false);
  assert.deepEqual(store.have(), []);
  assert.equal(store.status().state, 'error');
});

test('kho gói: bản build đầy đủ (không bật chế độ gói) thì không tải gì', async () => {
  const dir = tmp();
  const s = createPackStore({ dir, licenseDir: dir, enabled: false, client: { packKeys: async () => { throw new Error('không được gọi'); } }, lic: { rawKeys: () => ['k'] } });
  assert.deepEqual(await s.sync(), { ok: true, disabled: true });
});

test('bộ nạp nội dung: bài không có trong content/ thì đọc từ gói, chưa tải thì NOT_DOWNLOADED', () => {
  const loader = require('../main/content-loader');
  const rel = 'toan7/tap1/chuong-9/gia-lap-chua-co.json';
  loader.setPackReader(() => null);
  assert.throws(() => loader.loadLesson(rel), /NOT_DOWNLOADED/);
  loader.setPackReader((r) => (r === rel ? JSON.stringify({ id: 'x', items: [], theory: [] }) : null));
  assert.equal(loader.loadLesson(rel).id, 'x');
  loader.setPackReader(null);
});

test('gói mã hóa tất định: cùng nội dung thì cùng file, đổi nội dung thì khác', () => {
  const key = deriveGradeKey(MASTER, 9);
  const a = encryptPack({ 'a.json': '1', 'b.json': '2' }, key);
  assert.ok(a.equals(encryptPack({ 'a.json': '1', 'b.json': '2' }, key)));
  assert.ok(!a.equals(encryptPack({ 'a.json': '1', 'b.json': '3' }, key)));
  const dir = fakeContent();
  const r1 = build({ contentDir: dir, outDir: tmp(), master: MASTER });
  const r2 = build({ contentDir: dir, outDir: tmp(), master: MASTER });
  assert.equal(r1.index.packs[7].sha256, r2.index.packs[7].sha256);
});

// --- Khóa Kỹ năng (nội dung nằm trong file JS của giao diện) ---
const vm = require('vm');
const { COURSES, freeKeys } = require('../tools/build-packs');
const { deriveCourseKey } = require('../core/pack-format');
const REAL = path.join(__dirname, '..', 'renderer');
const evalFile = (f) => { const w = {}; vm.runInNewContext(fs.readFileSync(f, 'utf8'), { window: w }); return JSON.parse(JSON.stringify(w)); };
function rendererCopy() {
  const d = tmp();
  for (const f of new Set([...COURSES.map((c) => c.file), 'tu-duy.js', 'gia-su-ai.js'])) fs.copyFileSync(path.join(REAL, f), path.join(d, f));
  return d;
}

test('khóa Kỹ năng: danh sách bài xem thử khớp module giao diện (không lệch khi sửa FREE)', () => {
  const free = Object.fromEntries(COURSES.map((c) => [c.id, freeKeys(REAL, c)]));
  assert.deepEqual(free['tu-duy-lap-trinh-scratch'], ['tongquan', 'caidat', 'bai1']);
  assert.deepEqual(free['tu-duy-lap-trinh-python'], ['tongquan', 'caidat', 'c1b2']);
  assert.deepEqual(free['gia-su-ai'], ['tongquan', 'bai1', 'bai2']);
  assert.deepEqual(free['ai-nguoi-di-lam-claude'], []);
});

test('khóa Kỹ năng: cắt nội dung trả phí khỏi giao diện, gói giải mã và nạp lại đúng như bản đầy đủ', () => {
  const rd = rendererCopy(); const out = tmp(); const content = fakeContent(); const mode = path.join(tmp(), 'm.json');
  const before = evalFile(path.join(rd, 'tu-duy-content.js'));
  const gsBefore = evalFile(path.join(rd, 'gia-su-ai-content.js'));
  const sizeBefore = fs.statSync(path.join(rd, 'tu-duy-content.js')).size;
  const r = build({ contentDir: content, outDir: out, master: MASTER, prune: true, modeFile: mode, rendererDir: rd });
  assert.deepEqual(Object.keys(r.index.courses).sort(), COURSES.map((c) => c.id).sort());
  const after = evalFile(path.join(rd, 'tu-duy-content.js'));
  assert.ok(fs.statSync(path.join(rd, 'tu-duy-content.js')).size < sizeBefore / 5);
  // bài xem thử còn đủ; bài trả phí chỉ còn tiêu đề; mục lục giữ nguyên
  assert.ok(after.TUDUY.k1218.c1b2.html && after.TUDUY.k1218.tongquan.html);
  const paid = Object.keys(before.TUDUY.k1218).find((k) => !['tongquan', 'caidat', 'c1b2'].includes(k));
  assert.equal(after.TUDUY.k1218[paid].html, undefined);
  assert.equal(after.TUDUY.k1218[paid].title, before.TUDUY.k1218[paid].title);
  assert.deepEqual(after.TUDUY_TOC, before.TUDUY_TOC);
  assert.equal(evalFile(path.join(rd, 'ai-work-claude.js')).AI_WORK_CLAUDE.bai4.html, undefined);
  // giải mã gói rồi nạp bằng NLCourse.merge: ra đúng như bản đầy đủ
  const win = { ...after, JSON };
  const code = fs.readFileSync(path.join(REAL, 'course-loader.js'), 'utf8');
  vm.runInNewContext(code, { window: win });
  for (const id of ['tu-duy-lap-trinh-python', 'tu-duy-lap-trinh-scratch']) win.NLCourse.merge(decryptPack(fs.readFileSync(path.join(out, r.index.courses[id].file)), deriveCourseKey(MASTER, id)));
  assert.deepEqual(JSON.parse(JSON.stringify(win.TUDUY)), before.TUDUY);
  const gs = { ...evalFile(path.join(rd, 'gia-su-ai-content.js')), JSON };
  vm.runInNewContext(code, { window: gs });
  gs.NLCourse.merge(decryptPack(fs.readFileSync(path.join(out, r.index.courses['gia-su-ai'].file)), deriveCourseKey(MASTER, 'gia-su-ai')));
  assert.deepEqual(JSON.parse(JSON.stringify(gs.GIA_SU_AI)), gsBefore.GIA_SU_AI);
  // sai khoá thì không đọc được
  assert.throws(() => decryptPack(fs.readFileSync(path.join(out, r.index.courses['gia-su-ai'].file)), deriveCourseKey(MASTER, 'cong-dan-so')));
});

test('kho gói: tải cả gói khóa Kỹ năng, chỉ trả cho đúng khóa đã có', async () => {
  const rd = rendererCopy(); const out = tmp();
  const r = build({ contentDir: fakeContent(), outDir: out, master: MASTER, prune: false, rendererDir: rd });
  const keys = { 7: deriveGradeKey(MASTER, 7).toString('base64') };
  const courses = { 'gia-su-ai': deriveCourseKey(MASTER, 'gia-su-ai').toString('base64') };
  const fetchFn = async (url) => {
    const name = url.split('/').pop(); const f = path.join(out, name);
    if (!fs.existsSync(f)) return { ok: false, status: 404 };
    const b = fs.readFileSync(f);
    return { ok: true, status: 200, json: async () => JSON.parse(b.toString()), arrayBuffer: async () => b.buffer.slice(b.byteOffset, b.byteOffset + b.length) };
  };
  const dir = tmp();
  const store = createPackStore({ dir, licenseDir: dir, client: { packKeys: async () => ({ ok: true, data: { base: 'https://r2.test/c', keys, courses } }) }, lic: { rawKeys: () => ['k'] }, fetchFn });
  assert.equal(store.readCourse('gia-su-ai'), null);
  const res = await store.sync();
  assert.equal(res.ok, true); assert.equal(res.downloaded, 2);
  assert.ok(store.readCourse('gia-su-ai')['GIA_SU_AI']);
  assert.equal(store.readCourse('tu-duy-lap-trinh-python'), null); // chưa mua
  assert.deepEqual(store.status().courses, ['gia-su-ai']);
  assert.ok(r.index.courses['gia-su-ai'].file.startsWith('course-gia-su-ai-'));
});

test('hasCourse: khóa bản cũ tu-duy-lap-trinh mở cả hai lộ trình; khóa khác không', () => {
  const lic = require('../main/license');
  const ok = (courses) => ({ status: 'ok', courses });
  assert.ok(lic.hasCourse(ok(['gia-su-ai']), 'gia-su-ai'));
  assert.ok(!lic.hasCourse(ok(['gia-su-ai']), 'ai-nguoi-di-lam-claude'));
  assert.ok(lic.hasCourse(ok(['tu-duy-lap-trinh']), 'tu-duy-lap-trinh-python') && lic.hasCourse(ok(['tu-duy-lap-trinh']), 'tu-duy-lap-trinh-scratch'));
  assert.ok(!lic.hasCourse(ok(['tu-duy-lap-trinh']), 'gia-su-ai'));
  assert.ok(!lic.hasCourse({ status: 'expired', courses: ['gia-su-ai'] }, 'gia-su-ai'));
});
