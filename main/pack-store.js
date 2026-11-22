// Kho gói nội dung khóa học trên máy: tải theo lớp đã có bản quyền, lưu vào thư mục dữ liệu của app, đọc offline.
// Gói mã hóa (core/pack-format.js); khoá giải mã của từng lớp do máy chủ cấp sau khi kiểm tra bản quyền và được nhớ trên máy
// để học offline. Quyền mở bài vẫn do main/license quyết định ở mỗi lần mở.
const fs = require('fs');
const path = require('path');
const { decryptPack, sha256, gradeOfSubject } = require('../core/pack-format');

const MAX_PACK_BYTES = 40 * 1024 * 1024;

function createPackStore({ dir, client, lic, licenseDir, enabled = true, fetchFn = (...a) => fetch(...a), send = () => {}, readFile = fs.readFileSync }) {
  const packDir = path.join(dir, 'packs');
  const stateFile = path.join(packDir, 'state.json');
  const cache = new Map(); // 'g7' | 'c:gia-su-ai' -> { sha, files }
  let status = { state: 'idle', grades: [] };
  let busy = null;

  const readState = () => { try { const j = JSON.parse(fs.readFileSync(stateFile, 'utf8')); return { grades: j.grades || {}, courses: j.courses || {} }; } catch { return { grades: {}, courses: {} }; } };
  const writeState = (st) => { fs.mkdirSync(packDir, { recursive: true }); const tmp = stateFile + '.tmp'; fs.writeFileSync(tmp, JSON.stringify(st)); fs.renameSync(tmp, stateFile); };
  const setStatus = (s) => { status = { ...status, ...s }; try { send(status); } catch { /* bỏ qua */ } };

  // kind: 'grades' (gói theo lớp) hoặc 'courses' (gói khóa Kỹ năng); id là số lớp hoặc mã khóa.
  function loadUnit(kind, id) {
    const ent = readState()[kind][id];
    if (!ent) return null;
    const ck = (kind === 'grades' ? 'g' : 'c:') + id;
    if (cache.has(ck) && cache.get(ck).sha === ent.sha256) return cache.get(ck).files;
    try {
      const files = decryptPack(readFile(path.join(packDir, ent.file)), Buffer.from(ent.key, 'base64'));
      cache.set(ck, { sha: ent.sha256, files });
      return files;
    } catch { return null; }
  }

  // Đọc một file nội dung dạng "<môn>/<đường dẫn>"; null nếu chưa tải.
  function read(rel) {
    const files = loadUnit('grades', gradeOfSubject(String(rel).split('/')[0]));
    return files && typeof files[rel] === 'string' ? files[rel] : null;
  }

  // Nội dung khóa Kỹ năng: { "TUDUY.k1218": "<json các bài>", ... }; null nếu chưa tải.
  function readCourse(id) { return loadUnit('courses', String(id)); }

  const onDisk = (e) => { try { return fs.statSync(path.join(packDir, e.file)).isFile(); } catch { return false; } };
  const haveOf = (kind) => { const m = readState()[kind]; return Object.keys(m).filter((k) => onDisk(m[k])); };
  const have = () => haveOf('grades').map(Number).sort((a, b) => a - b);
  const haveCourses = () => haveOf('courses').sort();

  async function download(url, expectSha, onBytes) {
    const r = await fetchFn(url, { signal: AbortSignal.timeout(120000) });
    if (!r.ok) throw new Error('http ' + r.status);
    let buf;
    if (onBytes && r.body && typeof r.body.getReader === 'function') {
      const rd = r.body.getReader(); const parts = []; let n = 0;
      for (;;) { const { done, value } = await rd.read(); if (done) break; parts.push(Buffer.from(value)); n += value.length; if (n > MAX_PACK_BYTES) throw new Error('gói quá lớn'); onBytes(n); }
      buf = Buffer.concat(parts);
    } else buf = Buffer.from(await r.arrayBuffer());
    if (buf.length > MAX_PACK_BYTES) throw new Error('gói quá lớn');
    if (sha256(buf) !== expectSha) throw new Error('sai mã kiểm tra');
    return buf;
  }

  async function run() {
    const keys = lic.rawKeys(licenseDir);
    if (!keys.length) { setStatus({ state: 'idle', grades: [], error: '' }); return { ok: true, downloaded: 0, grades: [] }; }
    const kr = await client.packKeys({ keys });
    if (!kr.ok) { setStatus({ state: kr.offline ? 'offline' : 'error', error: kr.error || '' }); return { ok: false, offline: !!kr.offline, error: kr.error }; }
    const base = String(kr.data.base || '').replace(/\/+$/, '');
    const granted = kr.data.keys || {};
    const grantedCourses = kr.data.courses || {};
    if (!/^https:\/\//i.test(base)) { setStatus({ state: 'error', error: 'Chưa cấu hình nơi lưu nội dung.' }); return { ok: false, error: 'base' }; }
    let idx;
    try {
      const ir = await fetchFn(base + '/index.json', { signal: AbortSignal.timeout(20000) });
      if (!ir.ok) throw new Error('http ' + ir.status);
      idx = await ir.json();
    } catch { setStatus({ state: 'offline', error: '' }); return { ok: false, offline: true }; }
    const st = readState();
    const units = [
      ...Object.keys(granted).map(Number).sort((a, b) => a - b).map((g) => ({ kind: 'grades', id: g, p: idx.packs && idx.packs[g], key: granted[g], label: 'lớp ' + g })),
      ...Object.keys(grantedCourses).sort().map((c) => ({ kind: 'courses', id: c, p: idx.courses && idx.courses[c], key: grantedCourses[c], label: 'khóa ' + c })),
    ];
    // file đã bị xóa thì tải lại dù state.json còn ghi
    const fileOk = onDisk;
    const todo = units.filter((u) => u.p && (!st[u.kind][u.id] || st[u.kind][u.id].sha256 !== u.p.sha256 || st[u.kind][u.id].key !== u.key || !fileOk(st[u.kind][u.id])));
    let downloaded = 0;
    const bytesTotal = todo.reduce((a, u) => a + (Number(u.p.size) || 0), 0) || 1;
    let bytesBefore = 0; let lastEmit = 0;
    const pct = (extra) => Math.min(99, Math.floor(((bytesBefore + extra) / bytesTotal) * 100));
    for (let i = 0; i < todo.length; i++) {
      const u = todo[i]; const p = u.p;
      if (!/^[A-Za-z0-9._-]{1,80}$/.test(String(p.file))) continue;
      setStatus({ state: 'downloading', grade: u.kind === 'grades' ? u.id : 0, course: u.kind === 'courses' ? u.id : '', done: i, total: todo.length, percent: pct(0), error: '' });
      try {
        const buf = await download(base + '/' + p.file, p.sha256, (n) => { const t = Date.now(); if (t - lastEmit > 150) { lastEmit = t; setStatus({ percent: pct(n) }); } });
        bytesBefore += Number(p.size) || buf.length;
        decryptPack(buf, Buffer.from(u.key, 'base64')); // kiểm tra giải mã được trước khi lưu
        fs.mkdirSync(packDir, { recursive: true });
        const tmp = path.join(packDir, p.file + '.tmp');
        fs.writeFileSync(tmp, buf); fs.renameSync(tmp, path.join(packDir, p.file));
        const cur = readState(); const old = cur[u.kind][u.id];
        cur[u.kind][u.id] = { file: p.file, sha256: p.sha256, key: u.key };
        writeState(cur); cache.delete((u.kind === 'grades' ? 'g' : 'c:') + u.id);
        if (old && old.file !== p.file) { try { fs.unlinkSync(path.join(packDir, old.file)); } catch { /* bỏ qua */ } }
        downloaded++;
      } catch (e) {
        setStatus({ state: 'error', grade: u.kind === 'grades' ? u.id : 0, course: u.kind === 'courses' ? u.id : '', error: 'Không tải được nội dung ' + u.label + '. Kiểm tra mạng rồi thử lại.' });
        return { ok: false, downloaded, error: String(e && e.message) };
      }
    }
    // Khóa không còn bản quyền (thu hồi, hết hạn) thì giữ file nhưng quyền mở do license chặn; không xóa để khách mua lại không phải tải lại.
    setStatus({ state: 'ready', grades: have(), courses: haveCourses(), done: todo.length, total: todo.length, percent: 100, fresh: downloaded, grade: 0, course: '', error: '' });
    return { ok: true, downloaded, grades: Object.keys(granted).map(Number) };
  }

  function sync() {
    if (!enabled) return Promise.resolve({ ok: true, disabled: true });
    if (busy) return busy;
    busy = run().catch((e) => { setStatus({ state: 'error', error: 'Lỗi tải nội dung: ' + String(e && e.message) }); return { ok: false, error: String(e && e.message) }; }).finally(() => { busy = null; });
    return busy;
  }

  return { read, readCourse, sync, have, status: () => ({ ...status, enabled, grades: have(), courses: haveCourses() }), enabled };
}

module.exports = { createPackStore };
