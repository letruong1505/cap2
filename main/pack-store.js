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
  const cache = new Map(); // grade -> { sha, files }
  let status = { state: 'idle', grades: [] };
  let busy = null;

  const readState = () => { try { return JSON.parse(fs.readFileSync(stateFile, 'utf8')); } catch { return { grades: {} }; } };
  const writeState = (st) => { fs.mkdirSync(packDir, { recursive: true }); const tmp = stateFile + '.tmp'; fs.writeFileSync(tmp, JSON.stringify(st)); fs.renameSync(tmp, stateFile); };
  const setStatus = (s) => { status = { ...status, ...s }; try { send(status); } catch { /* bỏ qua */ } };

  function loadGrade(grade) {
    const ent = readState().grades[grade];
    if (!ent) return null;
    if (cache.has(grade) && cache.get(grade).sha === ent.sha256) return cache.get(grade).files;
    try {
      const files = decryptPack(readFile(path.join(packDir, ent.file)), Buffer.from(ent.key, 'base64'));
      cache.set(grade, { sha: ent.sha256, files });
      return files;
    } catch { return null; }
  }

  // Đọc một file nội dung dạng "<môn>/<đường dẫn>"; null nếu chưa tải.
  function read(rel) {
    const files = loadGrade(gradeOfSubject(String(rel).split('/')[0]));
    return files && typeof files[rel] === 'string' ? files[rel] : null;
  }

  const have = () => Object.keys(readState().grades).map(Number).sort((a, b) => a - b);

  async function download(url, expectSha) {
    const r = await fetchFn(url, { signal: AbortSignal.timeout(120000) });
    if (!r.ok) throw new Error('http ' + r.status);
    const buf = Buffer.from(await r.arrayBuffer());
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
    const grades = Object.keys(granted).map(Number).sort((a, b) => a - b);
    if (!/^https:\/\//i.test(base)) { setStatus({ state: 'error', error: 'Chưa cấu hình nơi lưu nội dung.' }); return { ok: false, error: 'base' }; }
    let idx;
    try {
      const ir = await fetchFn(base + '/index.json', { signal: AbortSignal.timeout(20000) });
      if (!ir.ok) throw new Error('http ' + ir.status);
      idx = await ir.json();
    } catch { setStatus({ state: 'offline', error: '' }); return { ok: false, offline: true }; }
    const st = readState();
    const todo = grades.filter((g) => idx.packs && idx.packs[g] && (!st.grades[g] || st.grades[g].sha256 !== idx.packs[g].sha256 || st.grades[g].key !== granted[g]));
    let downloaded = 0;
    for (let i = 0; i < todo.length; i++) {
      const g = todo[i]; const p = idx.packs[g];
      if (!/^[A-Za-z0-9._-]{1,80}$/.test(String(p.file))) continue;
      setStatus({ state: 'downloading', grade: g, done: i, total: todo.length, error: '' });
      try {
        const buf = await download(base + '/' + p.file, p.sha256);
        decryptPack(buf, Buffer.from(granted[g], 'base64')); // kiểm tra giải mã được trước khi lưu
        fs.mkdirSync(packDir, { recursive: true });
        const tmp = path.join(packDir, p.file + '.tmp');
        fs.writeFileSync(tmp, buf); fs.renameSync(tmp, path.join(packDir, p.file));
        const cur = readState(); const old = cur.grades[g];
        cur.grades[g] = { file: p.file, sha256: p.sha256, key: granted[g] };
        writeState(cur); cache.delete(g);
        if (old && old.file !== p.file) { try { fs.unlinkSync(path.join(packDir, old.file)); } catch { /* bỏ qua */ } }
        downloaded++;
      } catch (e) {
        setStatus({ state: 'error', grade: g, error: 'Không tải được nội dung lớp ' + g + '. Kiểm tra mạng rồi thử lại.' });
        return { ok: false, downloaded, error: String(e && e.message) };
      }
    }
    // Lớp không còn bản quyền (thu hồi, hết hạn) thì giữ file nhưng quyền mở bài do license chặn; không xóa để khách mua lại không phải tải lại.
    setStatus({ state: 'ready', grades: have(), done: todo.length, total: todo.length, grade: 0, error: '' });
    return { ok: true, downloaded, grades };
  }

  function sync() {
    if (!enabled) return Promise.resolve({ ok: true, disabled: true });
    if (busy) return busy;
    busy = run().catch((e) => { setStatus({ state: 'error', error: 'Lỗi tải nội dung: ' + String(e && e.message) }); return { ok: false, error: String(e && e.message) }; }).finally(() => { busy = null; });
    return busy;
  }

  return { read, sync, have, status: () => ({ ...status, enabled, grades: have() }), enabled };
}

module.exports = { createPackStore };
