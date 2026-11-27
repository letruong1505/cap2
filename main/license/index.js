const { evaluateKey, today } = require('./verify');
const { readStore, updateStore } = require('./store');
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
  // Khóa dùng thử chỉ để mở nội dung: có khóa mua thì hạn, chủ khóa và mã hiển thị lấy theo khóa mua, không hiện "còn 3 ngày".
  const paid = ok.filter((r) => !r.trial);
  const shown = paid.length ? paid : ok;
  const dated = shown.map((r) => r.expiresOn).filter((e) => e !== 'never').sort();
  const out = { ...shown[0], status: 'ok', grades, courses, expiresOn: dated.length ? dated[0] : 'never', id: shown.map((r) => r.id).filter(Boolean).join(', '), owner: shown[0].owner };
  if (paid.length) delete out.trial; else out.trial = true;
  return out;
}

// Áp dụng thu hồi lên một khóa hợp lệ: cả đơn bị thu hồi, hoặc chỉ một số lớp/khóa học trong đơn (hoàn tiền một phần).
function applyRevocation(e, revokedCodes, revokedItems) {
  if (revokedCodes.has(e.id)) return { ...e, status: 'revoked' };
  const part = revokedItems[String(e.id).replace(/^NL-/, '')];
  if (!part || e.grades === 'all') return e;
  const dropG = new Set(part.grades || []); const dropC = new Set(part.courses || []);
  const grades = e.grades.filter((g) => !dropG.has(g));
  const courses = e.courses.filter((c) => !dropC.has(c));
  if (!grades.length && !courses.length) return { ...e, status: 'revoked' };
  return { ...e, grades, courses };
}

// Trạng thái bản quyền hiện tại. Đồng hồ bị chỉnh lùi so với lần chạy trước thì coi như hết hạn.
function currentLicense(dir, now = new Date(), pubKey) {
  const machineId = getMachineId();
  const store = readStore(dir);
  if (!store.keys.length) return { status: 'missing', machineId };
  const t = today(now);
  // Khóa của đơn bị thu hồi (máy chủ báo về) thì vô hiệu, các khóa khác vẫn dùng bình thường.
  const revoked = new Set(store.revoked.map((c) => 'NL-' + c));
  const results = store.keys.map((k) => { const e = evaluateKey(k, machineId, now, pubKey); return e.status === 'ok' ? applyRevocation(e, revoked, store.revokedItems) : e; });
  const merged = merge(results);
  const r = merged || results.find((x) => x.status === 'revoked') || results.find((x) => x.status === 'expired') || results[0];
  // Khoá vĩnh viễn không phụ thuộc ngày nên không cần chặn khi đồng hồ bị lùi.
  if (r.expiresOn !== 'never' && store.lastSeen && t < store.lastSeen) return { status: 'clock', machineId };
  if (r.status === 'ok' && t > store.lastSeen) updateStore(dir, { lastSeen: t });
  return { ...r, machineId };
}

// Kích hoạt thêm một khoá: giữ các khoá đang có, thay khoá cùng mã đơn (ví dụ khoá cấp lại khi đổi máy).
function activate(dir, key, now = new Date(), pubKey) {
  const machineId = getMachineId();
  const clean = String(key).replace(/\s+/g, '');
  const r = evaluateKey(clean, machineId, now, pubKey);
  if (r.status !== 'ok') return { ...r, machineId };
  const keep = readStore(dir).keys.filter((k) => k !== clean && evaluateKey(k, machineId, now, pubKey).id !== r.id);
  updateStore(dir, { keys: [...keep, clean], lastSeen: today(now) });
  return { ...currentLicense(dir, now, pubKey), machineId };
}

function deactivate(dir) {
  updateStore(dir, { keys: [] });
}

// Mã đơn (6 ký tự) của các khóa đang hợp lệ trên máy này, để gửi tín hiệu về máy chủ. Khóa cấp tay không thuộc đơn nào thì bỏ qua.
function pingCodes(dir, now = new Date(), pubKey) {
  const machineId = getMachineId();
  return readStore(dir).keys.map((k) => evaluateKey(k, machineId, now, pubKey)).filter((r) => r.status === 'ok' && /^NL-[A-Z0-9]{6}$/.test(r.id)).map((r) => r.id.slice(3));
}

// Khóa đang hợp lệ trên máy này có mã dạng NL-xxxxxx (khóa cấp bằng USB chưa có trong hệ thống đơn hàng sẽ được khách tự đăng ký).
function registrableKeys(dir, now = new Date(), pubKey) {
  const machineId = getMachineId();
  return readStore(dir).keys.filter((k) => { const r = evaluateKey(k, machineId, now, pubKey); return r.status === 'ok' && /^NL-[A-Z0-9]{6}$/.test(r.id); });
}

// Cập nhật danh sách mã đơn bị thu hồi từ máy chủ. Trả về true nếu có thay đổi.
function setRevoked(dir, codes, items) {
  const next = [...new Set((codes || []).filter((c) => typeof c === 'string'))].sort();
  const nextItems = {};
  for (const [code, v] of Object.entries(items && typeof items === 'object' ? items : {})) {
    nextItems[code] = { grades: (v && Array.isArray(v.grades) ? v.grades.filter(Number.isInteger) : []).sort((a, b) => a - b), courses: (v && Array.isArray(v.courses) ? v.courses.filter((c) => typeof c === 'string') : []).sort() };
  }
  const st = readStore(dir);
  if (JSON.stringify(next) === JSON.stringify([...st.revoked].sort()) && JSON.stringify(nextItems) === JSON.stringify(st.revokedItems)) return false;
  updateStore(dir, { revoked: next, revokedItems: nextItems });
  return true;
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

// Các khoá đã lưu trên máy (chuỗi NL1-...) để gửi máy chủ xin khoá giải mã gói nội dung; máy chủ tự kiểm tra chữ ký và mã máy.
function rawKeys(dir) { return readStore(dir).keys.slice(); }

// Khóa Kỹ năng đã mua: khóa bản cũ 'tu-duy-lap-trinh' (bán chung) mở cả hai lộ trình Tư duy & lập trình.
function hasCourse(license, id) {
  if (!license || license.status !== 'ok' || !Array.isArray(license.courses)) return false;
  return license.courses.includes(id) || (/^tu-duy-lap-trinh-/.test(id) && license.courses.includes('tu-duy-lap-trinh'));
}

module.exports = { hasCourse, rawKeys, currentLicense, activate, deactivate, pingCodes, registrableKeys, setRevoked, canOpen, annotateManifest, hasGrade, MAX_FREE_LESSONS };
