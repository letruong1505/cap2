// Đọc và kiểm tra gói nội dung.
// Chỉ đọc file nằm trong thư mục content/, không đọc đường dẫn tùy ý.

const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '..', 'content');

function safeResolve(relPath) {
  if (typeof relPath !== 'string' || relPath.includes('..') || path.isAbsolute(relPath)) {
    throw new Error('Đường dẫn nội dung không hợp lệ');
  }
  const full = path.resolve(CONTENT_DIR, relPath);
  if (!full.startsWith(CONTENT_DIR + path.sep)) {
    throw new Error('Đường dẫn nằm ngoài thư mục nội dung');
  }
  return full;
}

function readJson(relPath) {
  return JSON.parse(fs.readFileSync(safeResolve(relPath), 'utf8'));
}

// Kiểm tra tối thiểu khi nạp một bài. Bộ kiểm tra đầy đủ nằm ở tools/validate-content.js.
function checkLesson(lesson, relPath) {
  const problems = [];
  if (!lesson.id) problems.push('thiếu id');
  if (lesson.kind === 'review') {
    if (!Array.isArray(lesson.questions)) problems.push('thiếu danh sách câu tự luận');
  } else {
    if (!Array.isArray(lesson.items)) problems.push('thiếu danh sách câu hỏi');
    if (!Array.isArray(lesson.theory)) problems.push('thiếu lý thuyết');
  }
  if (problems.length) {
    throw new Error(`Bài ${relPath} không hợp lệ: ${problems.join(', ')}`);
  }
  return lesson;
}

function loadManifest(subject) {
  return readJson(path.join(assertSubject(subject), 'manifest.json'));
}

// Các môn được phép đọc. Mỗi môn là một thư mục con của content/.
const SUBJECTS = ['toan7', 'ly7', 'hoa7', 'sinh7', 'lichsu7', 'diali7', 'toan8', 'ly8', 'hoa8', 'sinh8'];

function assertSubject(subject) {
  if (!SUBJECTS.includes(subject)) throw new Error('Môn học không hợp lệ');
  return subject;
}

// Đọc nội dung SVG của hình minh họa và gắn vào câu hỏi (figureSvg), để giao diện không cần quyền đọc file.
function readFigure(base, rel) {
  return fs.readFileSync(safeResolve(path.join(base, rel)), 'utf8');
}

function attachFigures(lesson, base) {
  for (const item of lesson.items || []) {
    if (item.figure) item.figureSvg = readFigure(base, item.figure);
  }
  for (const q of lesson.questions || []) {
    if (q.figure) q.figureSvg = readFigure(base, q.figure);
  }
  for (const block of lesson.theory || []) {
    if (block.type === 'figure') block.figureSvg = readFigure(base, block.figure);
  }
  for (const ex of lesson.examples || []) {
    if (ex.figure) ex.figureSvg = readFigure(base, ex.figure);
  }
  return lesson;
}

// Đường dẫn bài học có dạng "<môn>/<file>", ví dụ "toan7/tap1/chuong-1/bai-1/tap-hop.json".
function loadLesson(relPath) {
  const base = assertSubject(String(relPath).split('/')[0]);
  return attachFigures(checkLesson(readJson(relPath), relPath), base);
}

module.exports = { loadManifest, loadLesson, safeResolve, SUBJECTS };
