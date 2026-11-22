// Đóng gói nội dung khóa học theo lớp (mã hóa) và, nếu có --prune, bỏ nội dung đã đóng gói khỏi thư mục content/
// trước khi build exe: app chỉ giữ mục lục (manifest) và 2 bài học thử đầu của mỗi môn, phần còn lại tải về sau khi kích hoạt.
//   PACK_MASTER=... node tools/build-packs.js --out packs-out [--prune]
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { deriveGradeKey, deriveCourseKey, encryptPack, sha256, gradeOfSubject } = require('../core/pack-format');

const ROOT = path.join(__dirname, '..');
const MAX_FREE_LESSONS = 2; // khớp main/license/index.js

function walk(dir, base = dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, base, out); else out.push(path.relative(base, p).split(path.sep).join('/'));
  }
  return out;
}

// Tên file hình (figure) nằm lồng trong bài học; hình luôn tính từ thư mục môn.
function figuresOf(node, out = new Set()) {
  if (Array.isArray(node)) node.forEach((x) => figuresOf(x, out));
  else if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (k === 'figure' && typeof v === 'string') out.add(v); else figuresOf(v, out);
    }
  }
  return out;
}

function freeFiles(contentDir, subject) {
  const m = JSON.parse(fs.readFileSync(path.join(contentDir, subject, 'manifest.json'), 'utf8'));
  const lessons = [];
  for (const b of m.books) for (const c of b.chapters) for (const l of c.lessons) if (l.file) lessons.push(l.file);
  const keep = new Set(['manifest.json']);
  for (const f of lessons.slice(0, MAX_FREE_LESSONS)) {
    keep.add(f);
    const j = JSON.parse(fs.readFileSync(path.join(contentDir, subject, f), 'utf8'));
    for (const fig of figuresOf(j)) keep.add(fig);
  }
  return keep;
}

// Các khóa Kỹ năng có nội dung trả phí nằm trong file JS của giao diện (window.<GLOBAL>). Bài xem thử (free) giữ nguyên trong app,
// bài trả phí chỉ còn tiêu đề (để mục lục vẫn hiện) và phần nội dung nằm trong gói của khóa. FREE phải khớp renderer/tu-duy.js, gia-su-ai.js.
const COURSES = [
  { id: 'tu-duy-lap-trinh-scratch', file: 'tu-duy-content.js', global: 'TUDUY', sub: 'k811', freeFrom: 'tu-duy.js' },
  { id: 'tu-duy-lap-trinh-python', file: 'tu-duy-content.js', global: 'TUDUY', sub: 'k1218', freeFrom: 'tu-duy.js' },
  { id: 'gia-su-ai', file: 'gia-su-ai-content.js', global: 'GIA_SU_AI', freeFrom: 'gia-su-ai.js' },
  { id: 'ai-nguoi-di-lam-claude', file: 'ai-work-claude.js', global: 'AI_WORK_CLAUDE', free: [] },
  { id: 'ai-nguoi-di-lam-chatgpt', file: 'ai-work-chatgpt.js', global: 'AI_WORK_CHATGPT', free: [] },
  { id: 'ai-nguoi-di-lam-gemini', file: 'ai-work-gemini.js', global: 'AI_WORK_GEMINI', free: [] },
];

// Danh sách bài xem thử lấy từ chính module giao diện để không lệch: tu-duy.js có FREE = { k811: [...], k1218: [...] }, gia-su-ai.js có FREE = [...].
function freeKeys(rendererDir, c) {
  if (c.free) return c.free;
  const src = fs.readFileSync(path.join(rendererDir, c.freeFrom), 'utf8');
  const m = src.match(/const FREE = (\{[^;]*\}|\[[^;]*\]);/);
  if (!m) throw new Error('Không đọc được danh sách bài xem thử trong ' + c.freeFrom);
  const v = JSON.parse(JSON.stringify(vm.runInNewContext('(' + m[1] + ')'))); // sao chép ra khỏi vùng chạy riêng
  return c.sub ? v[c.sub] : v;
}

function loadGlobals(file) {
  const w = {};
  vm.runInNewContext(fs.readFileSync(file, 'utf8'), { window: w });
  return w;
}

function buildCourses({ rendererDir, outDir, master, prune, index }) {
  const byFile = {};
  for (const c of COURSES) (byFile[c.file] = byFile[c.file] || []).push(c);
  for (const [file, list] of Object.entries(byFile)) {
    const full = path.join(rendererDir, file);
    const W = loadGlobals(full);
    for (const c of list) {
      const target = c.sub ? W[c.global][c.sub] : W[c.global];
      if (!target || typeof target !== 'object') throw new Error('Thiếu nội dung ' + c.global + (c.sub ? '.' + c.sub : '') + ' trong ' + file);
      const free = new Set(freeKeys(rendererDir, c));
      const paid = {};
      for (const [k, v] of Object.entries(target)) if (!free.has(k)) paid[k] = v;
      const blob = encryptPack({ [c.global + (c.sub ? '.' + c.sub : '')]: JSON.stringify(paid) }, deriveCourseKey(master, c.id));
      const name = `course-${c.id}-${sha256(blob).slice(0, 10)}.nlp`;
      fs.writeFileSync(path.join(outDir, name), blob);
      index.courses[c.id] = { file: name, size: blob.length, sha256: sha256(blob), lessons: Object.keys(paid).length };
      if (prune) for (const k of Object.keys(paid)) target[k] = { title: paid[k].title, sub: paid[k].sub }; // chỉ giữ tiêu đề cho mục lục
    }
    if (prune) fs.writeFileSync(full, '// Đã tách nội dung bài trả phí khỏi file này (tools/build-packs.js); phần đó tải về theo khóa đã mua.\n' + Object.entries(W).map(([k, v]) => `window.${k} = ${JSON.stringify(v)};\n`).join(''));
  }
}

function build({ contentDir = path.join(ROOT, 'content'), outDir, master, prune = false, modeFile = path.join(ROOT, 'main', 'content-mode.json'), rendererDir = null }) {
  const subjects = fs.readdirSync(contentDir, { withFileTypes: true }).filter((e) => e.isDirectory() && /\d+$/.test(e.name)).map((e) => e.name).sort();
  const byGrade = {};
  for (const s of subjects) (byGrade[gradeOfSubject(s)] = byGrade[gradeOfSubject(s)] || []).push(s);
  fs.mkdirSync(outDir, { recursive: true });
  const index = { v: 2, builtAt: new Date().toISOString(), packs: {}, courses: {} };
  const removable = [];
  for (const [grade, subs] of Object.entries(byGrade)) {
    subs.sort();
    const files = {};
    for (const s of subs) {
      const keep = freeFiles(contentDir, s);
      for (const rel of walk(path.join(contentDir, s)).sort()) {
        if (rel === 'manifest.json') continue;
        files[`${s}/${rel}`] = fs.readFileSync(path.join(contentDir, s, rel), 'utf8');
        if (!keep.has(rel)) removable.push(path.join(contentDir, s, rel));
      }
    }
    const blob = encryptPack(files, deriveGradeKey(master, grade));
    const name = `lop${grade}-${sha256(blob).slice(0, 10)}.nlp`;
    fs.writeFileSync(path.join(outDir, name), blob);
    index.packs[grade] = { file: name, size: blob.length, sha256: sha256(blob), files: Object.keys(files).length };
  }
  // Chỉ đóng gói (và cắt) file giao diện khi người gọi chỉ rõ thư mục; kiểm thử không được tự chạm vào renderer/ thật.
  if (rendererDir) buildCourses({ rendererDir, outDir, master, prune, index });
  fs.writeFileSync(path.join(outDir, 'index.json'), JSON.stringify(index, null, 1));
  if (prune) {
    for (const f of removable) fs.unlinkSync(f);
    // Dọn thư mục rỗng.
    const clean = (d) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) if (e.isDirectory()) { clean(path.join(d, e.name)); if (!fs.readdirSync(path.join(d, e.name)).length) fs.rmdirSync(path.join(d, e.name)); } };
    clean(contentDir);
    fs.writeFileSync(modeFile, JSON.stringify({ mode: 'packs' }) + '\n');
  }
  return { index, removed: prune ? removable.length : 0 };
}

if (require.main === module) {
  const arg = (n) => { const i = process.argv.indexOf(n); return i >= 0 ? process.argv[i + 1] : ''; };
  const master = process.env.PACK_MASTER || '';
  const outDir = arg('--out');
  if (!outDir || !master) { console.error('Dùng: PACK_MASTER=... node tools/build-packs.js --out <thư mục> [--prune]'); process.exit(1); }
  const r = build({ outDir: path.resolve(outDir), master, prune: process.argv.includes('--prune'), rendererDir: path.join(ROOT, 'renderer') });
  for (const [g, p] of Object.entries(r.index.packs)) console.log(`Lớp ${g}: ${p.files} file, ${(p.size / 1048576).toFixed(2)} MB`);
  for (const [id, p] of Object.entries(r.index.courses)) console.log(`Khóa ${id}: ${p.lessons} bài, ${(p.size / 1024).toFixed(0)} KB`);
  console.log(r.removed ? `Đã bỏ ${r.removed} file khỏi content/ (giữ mục lục và 2 bài học thử mỗi môn).` : 'Không bỏ file nào khỏi content/.');
}

module.exports = { build, freeFiles, COURSES, freeKeys };
