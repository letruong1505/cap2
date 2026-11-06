// Kiểm tra gói nội dung trước khi đóng gói.
// Chạy: npm run validate
// Kiểm tra cấu trúc, và tính lại mọi đáp án số bằng core/rational.js để so với đáp án khóa.
const fs = require('fs');
const path = require('path');
const R = require('../core/rational.js');

const CONTENT_DIR = path.join(__dirname, '..', 'content');
const LEVELS = ['Biết', 'Hiểu', 'Vận dụng'];

function checkExpr(expr, answer, tag) {
  // Trả về danh sách lỗi cho một cặp biểu thức và đáp án.
  if (!expr) return [`${tag}: thiếu biểu thức gốc (expr) để kiểm tra đáp án`];
  let value;
  try {
    value = R.evaluate(expr);
  } catch (e) {
    return [`${tag}: không tính được biểu thức "${expr}" (${e.message})`];
  }
  if (!R.sameValue(answer, expr)) {
    return [`${tag}: đáp án khóa "${answer}" không bằng giá trị của "${expr}"`];
  }
  return [];
}

function validateLesson(lesson, relPath) {
  const errs = [];
  const where = relPath;
  if (!lesson.id) errs.push('thiếu id');
  if (!Array.isArray(lesson.theory) || lesson.theory.length === 0) errs.push('thiếu lý thuyết');
  if (!Array.isArray(lesson.examples)) errs.push('thiếu ví dụ');
  if (!Array.isArray(lesson.items) || lesson.items.length === 0) errs.push('thiếu câu hỏi');

  for (const ex of lesson.examples || []) {
    errs.push(...checkExpr(ex.expr, ex.answer, `ví dụ "${ex.problem}"`));
  }

  const ids = new Set();
  for (const item of lesson.items || []) {
    const tag = `câu ${item.id}`;
    if (ids.has(item.id)) errs.push(`${tag}: trùng mã câu`);
    ids.add(item.id);
    if (!LEVELS.includes(item.level)) errs.push(`${tag}: mức độ không hợp lệ (${item.level})`);
    if (!item.explain) errs.push(`${tag}: thiếu lời giải`);
    if (item.figure) {
      const rel = String(item.figure);
      if (rel.includes('..') || path.isAbsolute(rel)) {
        errs.push(`${tag}: đường dẫn hình không hợp lệ (${rel})`);
      } else if (!fs.existsSync(path.join(CONTENT_DIR, 'toan7', rel))) {
        errs.push(`${tag}: không tìm thấy hình ${rel}`);
      }
    }

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
      // Đáp án khóa phải đúng theo tính toán, và không phương án nhiễu nào trùng giá trị đúng.
      const before = errs.length;
      errs.push(...checkExpr(item.expr, item.choices[item.answer], tag));
      if (errs.length === before && item.expr) {
        item.choices.forEach((c, ci) => {
          if (ci !== item.answer && R.sameValue(c, item.expr)) {
            errs.push(`${tag}: phương án ${ci} "${c}" cũng đúng, câu có nhiều đáp án`);
          }
        });
      }
    } else if (item.type === 'fill') {
      if (item.answer === undefined || item.answer === '') {
        errs.push(`${tag}: thiếu đáp án`);
      } else {
        errs.push(...checkExpr(item.expr, item.answer, tag));
      }
    } else {
      errs.push(`${tag}: loại câu không được hỗ trợ (${item.type})`);
    }
  }
  return errs.map((e) => `${where}: ${e}`);
}

function main() {
  const manifestPath = path.join(CONTENT_DIR, 'toan7', 'manifest.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const problems = [];
  let lessonCount = 0;
  let checkedCount = 0;

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
        checkedCount += (data.items || []).filter((i) => i.expr).length;
        problems.push(...validateLesson(data, lesson.file));
      }
    }
  }

  if (problems.length) {
    console.error(`Có ${problems.length} lỗi:`);
    problems.forEach((p) => console.error('  - ' + p));
    process.exit(1);
  }
  console.log(`Đạt: ${lessonCount} bài, ${checkedCount} câu có đáp án đã được tính lại và khớp.`);
}

main();
