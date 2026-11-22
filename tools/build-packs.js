// Đóng gói nội dung khóa học theo lớp (mã hóa) và, nếu có --prune, bỏ nội dung đã đóng gói khỏi thư mục content/
// trước khi build exe: app chỉ giữ mục lục (manifest) và 2 bài học thử đầu của mỗi môn, phần còn lại tải về sau khi kích hoạt.
//   PACK_MASTER=... node tools/build-packs.js --out packs-out [--prune]
const fs = require('fs');
const path = require('path');
const { deriveGradeKey, encryptPack, sha256, gradeOfSubject } = require('../core/pack-format');

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

function build({ contentDir = path.join(ROOT, 'content'), outDir, master, prune = false, modeFile = path.join(ROOT, 'main', 'content-mode.json') }) {
  const subjects = fs.readdirSync(contentDir, { withFileTypes: true }).filter((e) => e.isDirectory() && /\d+$/.test(e.name)).map((e) => e.name).sort();
  const byGrade = {};
  for (const s of subjects) (byGrade[gradeOfSubject(s)] = byGrade[gradeOfSubject(s)] || []).push(s);
  fs.mkdirSync(outDir, { recursive: true });
  const index = { v: 1, builtAt: new Date().toISOString(), packs: {} };
  const removable = [];
  for (const [grade, subs] of Object.entries(byGrade)) {
    const files = {};
    for (const s of subs) {
      const keep = freeFiles(contentDir, s);
      for (const rel of walk(path.join(contentDir, s))) {
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
  const r = build({ outDir: path.resolve(outDir), master, prune: process.argv.includes('--prune') });
  for (const [g, p] of Object.entries(r.index.packs)) console.log(`Lớp ${g}: ${p.files} file, ${(p.size / 1048576).toFixed(2)} MB`);
  console.log(r.removed ? `Đã bỏ ${r.removed} file khỏi content/ (giữ mục lục và 2 bài học thử mỗi môn).` : 'Không bỏ file nào khỏi content/.');
}

module.exports = { build, freeFiles };
