const { evaluateKey, today } = require('./verify');
const { readStore, writeStore } = require('./store');
const { getMachineId } = require('./machine');

const MAX_FREE_LESSONS = 2; // chưa mua: chỉ mở 2 bài đầu của mỗi môn

// Trạng thái bản quyền hiện tại. Đồng hồ bị chỉnh lùi so với lần chạy trước thì coi như hết hạn.
function currentLicense(dir, now = new Date()) {
  const machineId = getMachineId();
  const store = readStore(dir);
  if (!store.key) return { status: 'missing', machineId };
  let when = now;
  const t = today(now);
  if (store.lastSeen && t < store.lastSeen) return { status: 'clock', machineId };
  const r = evaluateKey(store.key, machineId, when);
  if (r.status === 'ok' && t > store.lastSeen) writeStore(dir, { key: store.key, lastSeen: t });
  return { ...r, machineId };
}

function activate(dir, key, now = new Date()) {
  const machineId = getMachineId();
  const r = evaluateKey(key, machineId, now);
  if (r.status !== 'ok') return { ...r, machineId };
  writeStore(dir, { key: String(key).replace(/\s+/g, ''), lastSeen: today(now) });
  return { ...r, machineId };
}

function deactivate(dir) {
  writeStore(dir, { key: '', lastSeen: readStore(dir).lastSeen });
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
