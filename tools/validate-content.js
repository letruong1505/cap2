// Kiểm tra gói nội dung trước khi đóng gói.
// Chạy: npm run validate
const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '..', 'content');
const LEVELS = ['Biết', 'Hiểu', 'Vận dụng'];

function validateLesson(lesson, relPath) {
  const errs = [];
  const where = relPath;
  if (!lesson.id) errs.push('thiếu id');
  if (!Array.isArray(lesson.theory) || lesson.theory.length === 0) errs.push('thiếu lý thuyết');
  if (!Array.isArray(lesson.examples)) errs.push('thiếu ví dụ');
  if (!Array.isArray(lesson.items) || lesson.items.length === 0) errs.push('thiếu câu hỏi');

  const ids = new Set();
  for (const item of lesson.items || []) {
    const tag = `câu ${item.id}`;
    if (ids.has(item.id)) errs.push(`${tag}: trùng mã câu`);
    ids.add(item.id);
    if (!LEVELS.includes(item.level)) errs.push(`${tag}: mức độ không hợp lệ (${item.level})`);
    if (item.type === 'mcq') {
      if (!Array.isArray(item.choices) || item.choices.length < 2) {
        errs.push(`${tag}: thiếu phương án`);
        continue;
      }
      if (!Number.isInteger(item.answer) || item.answer < 0 || item.answer >= item.choices.length) {
        errs.push(`${tag}: chỉ số đáp án đúng nằm ngoài danh sách phương án`);
        continue;
      }
      item.choices.forEach((_, ci) => {
        if (ci === item.answer) return;
        const note = item.wrong_explain && item.wrong_explain[String(ci)];
        if (!note) errs.push(`${tag}: thiếu giải thích cho phương án ${ci}`);
      });
    } else if (item.type === 'fill') {
      if (item.answer === undefined || item.answer === '') errs.push(`${tag}: thiếu đáp án`);
    } else {
      errs.push(`${tag}: loại câu không được hỗ trợ (${item.type})`);
    }
    if (!item.explain) errs.push(`${tag}: thiếu lời giải`);
  }
  return errs.map((e) => `${where}: ${e}`);
}

function main() {
  const manifestPath = path.join(CONTENT_DIR, 'toan7', 'manifest.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const problems = [];
  let lessonCount = 0;

  for (const book of manifest.books) {
    for (const chapter of book.chapters) {
      for (const lesson of chapter.lessons) {
        if (!lesson.file) continue;
        lessonCount += 1;
        const full = path.join(CONTENT_DIR, 'toan7', lesson.file);
        if (!fs.existsSync(full)) {
          problems.push(`${lesson.file}: không tìm thấy file`);
          continue;
        }
        const data = JSON.parse(fs.readFileSync(full, 'utf8'));
        problems.push(...validateLesson(data, lesson.file));
      }
    }
  }

  if (problems.length) {
    console.error(`Có ${problems.length} lỗi:`);
    problems.forEach((p) => console.error('  - ' + p));
    process.exit(1);
  }
  console.log(`Đạt: ${lessonCount} bài kiểm tra không lỗi.`);
}

main();
