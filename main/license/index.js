const { evaluateKey, today } = require('./verify');
const { readStore, writeStore } = require('./store');
const { getMachineId } = require('./machine');

const MAX_FREE_LESSONS = 2; // chưa mua: chỉ mở 2 bài đầu của mỗi môn

// Gộp nhiều khoá hợp lệ trên máy này thành một bản quyền: hợp các lớp và các khóa Kỹ năng.
// Khoá hết hạn bị bỏ riêng, không ảnh hưởng khoá còn hạn. Ngày hết hạn hiển thị là ngày gần nhất trong các khoá còn hạn.
function merge(results) {
  const ok = results.filter((r) => r.status === 'ok');
  if (!ok.length) return null;
  const all = ok.some((r) => r.grades === 'all');
  const grades = all ? 'all' : [...new Set(ok.flatMap((r) => r.grades))].sort((a, b) => a - b);
  const courses = [...new Set(ok.flatMap((r) => r.courses || []))];
  const dated = ok.map((r) => r.expiresOn).filter((e) => e !== 'never').sort();
  return { ...ok[0], status: 'ok', grades, courses, expiresOn: dated.length ? dated[0] : 'never', id: ok.map((r) => r.id).filter(Boolean).join(', '), owner: ok[0].owner };
}

// Trạng thái bản quyền hiện tại. Đồng hồ bị chỉnh lùi so với lần chạy trước thì coi như hết hạn.
function currentLicense(dir, now = new Date(), pubKey) {
  const machineId = getMachineId();
  const store = readStore(dir);
  if (!store.keys.length) return { status: 'missing', machineId };
  const t = today(now);
  const results = store.keys.map((k) => evaluateKey(k, machineId, now, pubKey));
  const merged = merge(results);
  const r = merged || results.find((x) => x.status === 'expired') || results[0];
  // Khoá vĩnh viễn không phụ thuộc ngày nên không cần chặn khi đồng hồ bị lùi.
  if (r.expiresOn !== 'never' && store.lastSeen && t < store.lastSeen) return { status: 'clock', machineId };
  if (r.status === 'ok' && t > store.lastSeen) writeStore(dir, { keys: store.keys, lastSeen: t });
  return { ...r, machineId };
}

// Kích hoạt thêm một khoá: giữ các khoá đang có, thay khoá cùng mã đơn (ví dụ khoá cấp lại khi đổi máy).
function activate(dir, key, now = new Date(), pubKey) {
  const machineId = getMachineId();
  const clean = String(key).replace(/\s+/g, '');
  const r = evaluateKey(clean, machineId, now, pubKey);
  if (r.status !== 'ok') return { ...r, machineId };
  const keep = readStore(dir).keys.filter((k) => k !== clean && evaluateKey(k, machineId, now, pubKey).id !== r.id);
  writeStore(dir, { keys: [...keep, clean], lastSeen: today(now) });
  return { ...currentLicense(dir, now, pubKey), machineId };
}

function deactivate(dir) {
  writeStore(dir, { keys: [], lastSeen: readStore(dir).lastSeen });
}

const gradeOf = (subject) => Number(String(subject).match(/(\d+)$/)?.[1]);

function hasGrade(license, subject) {
  if (license.status !== 'ok') return false;
  return license.grades === 'all' || license.grades.includes(gradeOf(subject));
}

// Bài được mở: có khoá cho lớp đó, hoặc nằm trong 2 bài đầu của môn.
function allowedFiles(manifest) {
  const files = [];
  for (const b of manifest.books) for (const c of b.chapters) for (const l of c.lessons) if (l.file) files.push(l.file);
  return new Set(files.slice(0, MAX_FREE_LESSONS));
}

function canOpen(license, subject, manifest, file) {
  return hasGrade(license, subject) || allowedFiles(manifest).has(file);
}

// Đánh dấu locked cho từng bài trong mục lục để giao diện hiển thị.
function annotateManifest(license, subject, manifest) {
  const unlocked = hasGrade(license, subject);
  const free = allowedFiles(manifest);
  const out = JSON.parse(JSON.stringify(manifest));
  for (const b of out.books) for (const c of b.chapters) for (const l of c.lessons) {
    if (l.file) l.locked = !(unlocked || free.has(l.file));
  }
  return out;
}

module.exports = { currentLicense, activate, deactivate, canOpen, annotateManifest, hasGrade, MAX_FREE_LESSONS };
