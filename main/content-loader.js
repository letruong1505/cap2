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
  if (!Array.isArray(lesson.items)) problems.push('thiếu danh sách câu hỏi');
  if (!Array.isArray(lesson.theory)) problems.push('thiếu lý thuyết');
  if (problems.length) {
    throw new Error(`Bài ${relPath} không hợp lệ: ${problems.join(', ')}`);
  }
  return lesson;
}

function loadManifest(product) {
  return readJson(path.join(product, 'manifest.json'));
}

function loadLesson(relPath) {
  return checkLesson(readJson(relPath), relPath);
}

module.exports = { loadManifest, loadLesson, safeResolve };
