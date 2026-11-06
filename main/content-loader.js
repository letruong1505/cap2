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

function loadManifest(product) {
  return readJson(path.join(product, 'manifest.json'));
}

// Đọc nội dung SVG của hình minh họa và gắn vào câu hỏi (figureSvg), để giao diện không cần quyền đọc file.
function readFigure(rel) {
  return fs.readFileSync(safeResolve(path.join('toan7', rel)), 'utf8');
}

function attachFigures(lesson) {
  for (const item of lesson.items || []) {
    if (item.figure) item.figureSvg = readFigure(item.figure);
  }
  for (const q of lesson.questions || []) {
    if (q.figure) q.figureSvg = readFigure(q.figure);
  }
  for (const block of lesson.theory || []) {
    if (block.type === 'figure') block.figureSvg = readFigure(block.figure);
  }
  for (const ex of lesson.examples || []) {
    if (ex.figure) ex.figureSvg = readFigure(ex.figure);
  }
  return lesson;
}

function loadLesson(relPath) {
  return attachFigures(checkLesson(readJson(relPath), relPath));
}

module.exports = { loadManifest, loadLesson, safeResolve };
