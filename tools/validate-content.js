// Kiểm tra gói nội dung trước khi đóng gói.
// Chạy: npm run validate
// Kiểm tra cấu trúc, và tính lại mọi đáp án số bằng core/rational.js để so với đáp án khóa.
const fs = require('fs');
const path = require('path');
const R = require('../core/rational.js');
const EN = require('../renderer/english.js');

const CONTENT_DIR = path.join(__dirname, '..', 'content');
const LEVELS = ['Biết', 'Hiểu', 'Vận dụng', 'Nâng cao'];

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

// Môn đang kiểm tra (thư mục con của content/), đặt trước khi đọc từng môn.
let currentSubject = 'toan7';

function checkFigurePath(figure, tag) {
  const rel = String(figure);
  if (rel.includes('..') || path.isAbsolute(rel)) {
    return [`${tag}: đường dẫn hình không hợp lệ (${rel})`];
  }
  if (!fs.existsSync(path.join(CONTENT_DIR, currentSubject, rel))) {
    return [`${tag}: không tìm thấy hình ${rel}`];
  }
  return [];
}

function validateReview(lesson, relPath) {
  const errs = [];
  const where = relPath;
  if (!lesson.id) errs.push('thiếu id');
  if (!Array.isArray(lesson.questions) || lesson.questions.length !== 20) {
    errs.push(`cần đúng 20 câu tự luận (hiện có ${(lesson.questions || []).length})`);
  }
  const ids = new Set();
  for (const q of lesson.questions || []) {
    const tag = `câu ${q.id}`;
    if (ids.has(q.id)) errs.push(`${tag}: trùng mã câu`);
    ids.add(q.id);
    if (!q.stem) errs.push(`${tag}: thiếu đề bài`);
    if (!Array.isArray(q.steps) || q.steps.length === 0) errs.push(`${tag}: thiếu hướng dẫn giải`);
    if (!q.answer) errs.push(`${tag}: thiếu đáp số`);
    if (q.figure) errs.push(...checkFigurePath(q.figure, tag));
  }
  return errs.map((e) => `${where}: ${e}`);
}

function validateLesson(lesson, relPath) {
  if (lesson.kind === 'review') return validateReview(lesson, relPath);
  const errs = [];
  const where = relPath;
  if (!lesson.id) errs.push('thiếu id');
  if (!Array.isArray(lesson.theory) || lesson.theory.length === 0) errs.push('thiếu lý thuyết');
  if (!Array.isArray(lesson.examples)) errs.push('thiếu ví dụ');
  if (!Array.isArray(lesson.items) || lesson.items.length === 0) errs.push('thiếu câu hỏi');

  for (const ex of lesson.examples || []) {
    if (!Array.isArray(ex.steps)) errs.push(`ví dụ "${ex.problem}": các bước giải phải là danh sách`);
    // Ví dụ chứng minh (proof: true) không có đáp án số để kiểm tra.
    if (!ex.proof) errs.push(...checkExpr(ex.expr, ex.answer, `ví dụ "${ex.problem}"`));
    if (ex.figure) errs.push(...checkFigurePath(ex.figure, `ví dụ "${ex.problem}"`));
  }
  for (const block of lesson.theory || []) {
    if (block.type === 'method') {
      const t = `cách giải "${block.title}"`;
      if (!block.title) errs.push('cách giải: thiếu tên dạng bài');
      if (!Array.isArray(block.steps) || block.steps.length < 3) errs.push(`${t}: cần ít nhất 3 bước`);
      if (!Array.isArray(block.notes) || block.notes.length < 2) errs.push(`${t}: cần ít nhất 2 lưu ý`);
      if (!block.sample || !block.sample.problem || !Array.isArray(block.sample.steps) || !block.sample.steps.length) errs.push(`${t}: thiếu ví dụ mẫu`);
      continue;
    }
    if (block.type !== 'figure') continue;
    errs.push(...checkFigurePath(block.figure, 'lý thuyết'));
    if (!block.caption) errs.push('lý thuyết: hình thiếu chú thích');
  }

  if (lesson.crossword) errs.push(...EN.validate(lesson.crossword));
  for (const v of lesson.vocab || []) if (!v.w || !v.pos || !v.vi) errs.push(`từ vựng "${v.w}": thiếu từ, loại từ hoặc nghĩa`);
  if (lesson.reading && (!lesson.reading.title || !Array.isArray(lesson.reading.paragraphs) || !lesson.reading.paragraphs.length)) errs.push('đọc hiểu: thiếu tiêu đề hoặc đoạn văn');
  const wr = lesson.writing;
  if (wr && (!wr.prompt || !Array.isArray(wr.keywords) || !Array.isArray(wr.checklist) || !wr.checklist.length || !Array.isArray(wr.sample) || !Number.isInteger(wr.minWords))) errs.push('phần viết: thiếu đề, từ khóa, bảng kiểm, bài mẫu hoặc số từ tối thiểu');

  const ids = new Set();
  for (const item of lesson.items || []) {
    const tag = `câu ${item.id}`;
    if (ids.has(item.id)) errs.push(`${tag}: trùng mã câu`);
    ids.add(item.id);
    if (!LEVELS.includes(item.level)) errs.push(`${tag}: mức độ không hợp lệ (${item.level})`);
    if (!item.explain) errs.push(`${tag}: thiếu lời giải`);
    if (item.figure) errs.push(...checkFigurePath(item.figure, tag));

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
      // Câu khái niệm (phân loại biến cố, chọn cạnh lớn nhất…): không có giá trị số để tính lại.
      // Bắt buộc có giải thích cho mọi phương án sai (đã kiểm ở trên) và các phương án không trùng nhau.
      if (item.concept === true) {
        if (item.expr) errs.push(`${tag}: câu khái niệm không được có expr`);
        if (new Set(item.choices).size !== item.choices.length) errs.push(`${tag}: có phương án trùng nhau`);
        continue;
      }
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
  // Kiểm tra mọi môn có manifest trong content/ (toan7, khtn7, ...).
  const subjects = fs.readdirSync(CONTENT_DIR).filter((d) =>
    fs.existsSync(path.join(CONTENT_DIR, d, 'manifest.json')));
  const problems = [];
  const report = [];
  let lessonTotal = 0;
  let checkedTotal = 0;
  let conceptTotal = 0;

  for (const subject of subjects) {
    currentSubject = subject;
    const manifest = JSON.parse(fs.readFileSync(path.join(CONTENT_DIR, subject, 'manifest.json'), 'utf8'));
    let lessonCount = 0;
    for (const book of manifest.books) {
      for (const chapter of book.chapters) {
        for (const lesson of chapter.lessons) {
          if (!lesson.file) continue;
          lessonCount += 1;
          const full = path.join(CONTENT_DIR, subject, lesson.file);
          if (!fs.existsSync(full)) {
            problems.push(`${subject}/${lesson.file}: không tìm thấy file`);
            continue;
          }
          const data = JSON.parse(fs.readFileSync(full, 'utf8'));
          checkedTotal += (data.items || []).filter((i) => i.expr).length;
          conceptTotal += (data.items || []).filter((i) => i.concept === true).length;
          problems.push(...validateLesson(data, `${subject}/${lesson.file}`));
        }
      }
    }
    lessonTotal += lessonCount;
    report.push(`${subject}: ${lessonCount} bài`);
  }

  if (problems.length) {
    console.error(`Có ${problems.length} lỗi:`);
    problems.forEach((p) => console.error('  - ' + p));
    process.exit(1);
  }
  console.log(`Đạt: ${lessonTotal} bài (${report.join(', ')}), ${checkedTotal} câu có đáp án đã được tính lại và khớp, `
    + `${conceptTotal} câu trắc nghiệm khái niệm có đủ giải thích cho phương án sai.`);
}

main();
