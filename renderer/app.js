// Engine giao diện bài học: lý thuyết, ví dụ, luyện tập và chấm toàn bài.
// Mỗi lần mở bài là một lượt làm mới: thứ tự phương án được xáo trộn, không lưu kết quả cũ.
// Mọi nội dung từ file JSON được gán bằng textContent để tránh chèn mã HTML ngoài ý muốn.

const R = window.Rational;

const el = (tag, attrs = {}, text) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else node.setAttribute(k, v);
  }
  if (text !== undefined) node.textContent = text;
  return node;
};

// Xáo trộn Fisher–Yates, trả về mảng mới.
function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Thứ tự hiển thị theo mức độ: Biết, Hiểu, Vận dụng; trong mỗi mức, thứ tự câu được xáo trộn.
const LEVEL_ORDER = ['Biết', 'Hiểu', 'Vận dụng', 'Nâng cao'];

function orderedQuestionIndexes(lesson) {
  const groups = {};
  lesson.items.forEach((item, i) => {
    (groups[item.level] = groups[item.level] || []).push(i);
  });
  const levels = [...LEVEL_ORDER.filter((l) => groups[l]),
    ...Object.keys(groups).filter((l) => !LEVEL_ORDER.includes(l))];
  return levels.flatMap((l) => shuffle(groups[l]));
}

// Một lượt làm bài: thứ tự câu hỏi và thứ tự phương án mới, đáp án đang chọn, và trạng thái đã nộp.
function newAttempt(lesson) {
  const questions = orderedQuestionIndexes(lesson);
  const order = {};
  for (const item of lesson.items) {
    if (item.type === 'mcq') {
      order[item.id] = shuffle(item.choices.map((_, i) => i));
    }
  }
  return { questions, order, answers: {}, submitted: false };
}

function figureSrc(svg) {
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
}

function figureBlock(svg, caption) {
  const fig = el('figure', { class: 'theory-figure' });
  fig.append(el('img', { class: 'figure', alt: caption || '', src: figureSrc(svg) }));
  if (caption) fig.append(el('figcaption', {}, caption));
  return fig;
}

function renderTheory(lesson) {
  const box = document.getElementById('theory');
  box.replaceChildren();
  for (const block of lesson.theory) {
    if (block.type === 'figure') {
      box.append(figureBlock(block.figureSvg, block.caption));
    } else if (block.type === 'formula') {
      box.append(el('p', { class: 'formula' }, block.content));
    } else {
      box.append(el('p', {}, block.content));
    }
  }
}

function renderExamples(lesson) {
  const box = document.getElementById('examples');
  box.replaceChildren();
  lesson.examples.forEach((ex, i) => {
    const wrap = el('div', { class: 'example' });
    wrap.append(el('strong', {}, `Ví dụ ${i + 1}: ${ex.problem}`));
    if (ex.figureSvg) {
      wrap.append(el('img', { class: 'figure', alt: `Hình minh họa ví dụ ${i + 1}`, src: figureSrc(ex.figureSvg) }));
    }
    const steps = el('ol');
    ex.steps.forEach((s) => steps.append(el('li', {}, s)));
    wrap.append(steps);
    wrap.append(el('p', {}, `Đáp số: ${ex.answer}`));
    box.append(wrap);
  });
  // Bài không có ví dụ tính toán (Lịch sử, Địa lí) thì ẩn cả mục "Ví dụ".
  document.getElementById('sec-examples').hidden = lesson.examples.length === 0;
}

function renderQuiz(lesson, attempt) {
  const box = document.getElementById('quiz');
  box.replaceChildren();

  let currentLevel = null;
  attempt.questions.forEach((itemIndex, idx) => {
    const item = lesson.items[itemIndex];
    if (item.level !== currentLevel) {
      currentLevel = item.level;
      box.append(el('h3', { class: 'level-heading' }, currentLevel === 'Nâng cao' ? 'Phần nâng cao' : `Mức ${currentLevel}`));
    }
    const q = el('div', { class: 'question', 'data-id': item.id });
    q.append(el('div', { class: 'stem' }, `${idx + 1}. ${item.stem}`));
    if (item.figureSvg) {
      q.append(el('img', {
        class: 'figure',
        alt: `Hình minh họa câu ${idx + 1}`,
        src: 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(item.figureSvg),
      }));
    }

    // Chỉ ghi nhận lựa chọn, không hiện đúng sai khi chọn.
    if (item.type === 'mcq') {
      attempt.order[item.id].forEach((origIndex) => {
        const choice = item.choices[origIndex];
        const label = el('label', { class: 'choice' });
        const input = el('input', { type: 'radio', name: item.id });
        input.addEventListener('change', () => {
          attempt.answers[item.id] = choice;
        });
        label.append(input, ' ', choice);
        q.append(label);
      });
    } else {
      const input = el('input', {
        type: 'text',
        'aria-label': 'Đáp án',
        placeholder: 'Ví dụ: 3/4 hoặc 0,75',
        autocomplete: 'off',
      });
      input.addEventListener('input', () => {
        attempt.answers[item.id] = input.value.trim() || null;
      });
      q.append(input);
    }

    q.append(el('div', { class: 'feedback', hidden: 'hidden' }));
    box.append(q);
  });
}

function isEmpty(value) {
  return value === null || value === undefined || value === '';
}

// Đáp án được so theo giá trị (nội dung phương án hoặc số đã nhập), không theo vị trí.
// Với câu điền, 2/4 và 1/2 là cùng một đáp án.
function isCorrect(item, value) {
  if (isEmpty(value)) return false;
  if (item.type === 'mcq') return value === item.choices[item.answer];
  try {
    return R.sameValue(value, item.answer);
  } catch {
    return false;
  }
}

function correctText(item) {
  return item.type === 'mcq' ? item.choices[item.answer] : item.answer;
}

// Hiển thị kết quả của một câu sau khi nộp bài.
function showResult(item, feedback, value) {
  feedback.hidden = false;
  const explain = item.explain;

  if (isEmpty(value)) {
    feedback.className = 'feedback bad';
    feedback.textContent = `Chưa trả lời, tính là sai. Đáp án đúng: ${correctText(item)}. Lời giải: ${explain}`;
    return;
  }
  if (item.type === 'fill') {
    try {
      R.parse(value);
    } catch {
      feedback.className = 'feedback bad';
      feedback.textContent = `Chưa đúng định dạng (nhập số như 3/4 hoặc 0,75). Đáp án đúng: ${correctText(item)}. Lời giải: ${explain}`;
      return;
    }
  }
  if (isCorrect(item, value)) {
    feedback.className = 'feedback ok';
    feedback.textContent = 'Đúng. ' + explain;
    return;
  }
  feedback.className = 'feedback bad';
  const idx = item.type === 'mcq' ? item.choices.indexOf(value) : -1;
  const note = idx >= 0 ? item.wrong_explain[String(idx)] : null;
  feedback.textContent = (note ? note + ' ' : '') +
    `Đáp án đúng: ${correctText(item)}. Lời giải: ${explain}`;
}

// Chấm toàn bài: hiện kết quả từng câu, khóa mọi ô nhập, cập nhật điểm.
function submitAll(lesson, attempt) {
  if (attempt.submitted) return;
  attempt.submitted = true;

  lesson.items.forEach((item) => {
    const q = document.querySelector(`.question[data-id="${item.id}"]`);
    if (!q) return;
    showResult(item, q.querySelector('.feedback'), attempt.answers[item.id]);
    q.querySelectorAll('input').forEach((i) => { i.disabled = true; });
  });
  document.getElementById('btn-submit').disabled = true;
  updateScore(lesson, attempt);
}

function updateScore(lesson, attempt) {
  const box = document.getElementById('score');
  box.replaceChildren();

  if (!attempt.submitted) {
    const unanswered = lesson.items.filter((i) => isEmpty(attempt.answers[i.id])).length;
    box.append(el('span', { class: 'meta' },
      `Còn ${unanswered} câu chưa trả lời. Câu chưa làm sẽ tính là sai khi nộp bài.`));
    return;
  }

  let total = 0;
  let correct = 0;
  const wrong = [];
  attempt.questions.forEach((itemIndex, idx) => {
    const item = lesson.items[itemIndex];
    total += 1;
    if (isCorrect(item, attempt.answers[item.id])) {
      correct += 1;
    } else {
      wrong.push({ no: idx + 1, answer: correctText(item) });
    }
  });
  box.append(el('strong', {}, `Đúng ${correct}/${total} câu`));
  if (wrong.length > 0) {
    const list = el('ul', { class: 'wrong-list' });
    for (const w of wrong) {
      list.append(el('li', {}, `Câu ${w.no}: đáp án đúng là ${w.answer}`));
    }
    box.append(list);
  }
}

function showOnly(id) {
  for (const sec of ['launch', 'subjects', 'home', 'lesson', 'empty']) {
    document.getElementById(sec).hidden = sec !== id;
  }
}

// Màn hình chính: danh sách chương và bài theo manifest của gói nội dung.
function renderHome(manifest, subject) {
  const home = document.getElementById('home');
  const back = el('button', { class: 'link', type: 'button' }, '← Chọn môn');
  back.addEventListener('click', () => showSubjects(currentGrade));
  home.replaceChildren(back, el('h1', {}, 'Chọn bài học'));
  home.append(el('p', { class: 'meta' }, `Gói: ${manifest.bookSeries} · phiên bản ${manifest.version}`));

  for (const book of manifest.books) {
    home.append(el('h2', {}, book.title));
    for (const chapter of book.chapters) {
      const block = el('div', { class: 'chapter' });
      block.append(el('h3', {}, chapter.title));
      if (chapter.lessons.length === 0) {
        block.append(el('p', { class: 'meta' }, 'Đang biên soạn'));
      } else {
        const list = el('ul', { class: 'lesson-list' });
        for (const lesson of chapter.lessons) {
          const li = el('li');
          if (lesson.file) {
            const btn = el('button', { class: 'link', type: 'button' }, lesson.title);
            // Đường dẫn trong manifest tính từ thư mục sản phẩm, còn bộ nạp tính từ content/.
            btn.addEventListener('click', () => openLesson(subject + '/' + lesson.file, lesson.mode || 'practice'));
            li.append(btn);
          } else {
            li.append(el('span', { class: 'meta' }, `${lesson.title} · đang biên soạn`));
          }
          list.append(li);
        }
        block.append(list);
      }
      home.append(block);
    }
  }
  showOnly('home');
}

// Chế độ hiển thị: luyện tập (có lý thuyết và chấm điểm), ôn tập tự luận, hoặc hướng dẫn giải.
function setSections(mode) {
  const practice = mode === 'practice';
  document.getElementById('sec-theory').hidden = !practice;
  document.getElementById('sec-examples').hidden = !practice;
  document.getElementById('score').hidden = !practice;
  document.getElementById('sec-actions').hidden = !practice;
  document.getElementById('quiz-heading').textContent = {
    practice: 'Luyện tập',
    review: 'Câu hỏi ôn tập tự luận',
    solutions: 'Hướng dẫn giải',
  }[mode];
}

// Ôn tập tự luận: chỉ hiện đề; ở chế độ hướng dẫn giải thì hiện thêm các bước và đáp số.
function renderEssays(lesson, mode) {
  const box = document.getElementById('quiz');
  box.replaceChildren();
  lesson.questions.forEach((q, idx) => {
    const card = el('div', { class: 'question essay', 'data-id': q.id });
    card.append(el('div', { class: 'stem' }, `${idx + 1}. ${q.stem}`));
    if (q.figureSvg) {
      card.append(el('img', {
        class: 'figure',
        alt: `Hình minh họa câu ${idx + 1}`,
        src: figureSrc(q.figureSvg),
      }));
    }
    if (mode === 'solutions') {
      const steps = el('ol');
      q.steps.forEach((s) => steps.append(el('li', {}, s)));
      card.append(steps);
      card.append(el('p', { class: 'answer' }, `Đáp số: ${q.answer}`));
    }
    box.append(card);
  });
}

// Mỗi lần mở bài là một lượt làm mới (không khôi phục kết quả cũ).
async function openLesson(relPath, mode = 'practice') {
  try {
    const lesson = await window.vungBai.loadLesson(relPath);
    document.getElementById('breadcrumb').textContent =
      `Lớp ${lesson.grade} › ${{ toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', 'lich-su': 'Lịch sử', 'dia-li': 'Địa lí' }[lesson.subject] || lesson.subject} › ${lesson.chapter}`;

    if (lesson.kind === 'review') {
      const view = mode === 'solutions' ? 'solutions' : 'review';
      document.getElementById('lesson-title').textContent = lesson.title;
      document.getElementById('lesson-meta').textContent =
        view === 'solutions'
          ? `Hướng dẫn giải · ${lesson.questions.length} câu tự luận`
          : `Sách: ${lesson.bookSeries} · ${lesson.questions.length} câu tự luận (không chấm điểm)`;
      setSections(view);
      document.getElementById('theory').replaceChildren();
      document.getElementById('examples').replaceChildren();
      renderEssays(lesson, view);
      showOnly('lesson');
      return;
    }

    document.getElementById('lesson-title').textContent = lesson.lesson;
    document.getElementById('lesson-meta').textContent =
      `Sách: ${lesson.bookSeries} · ${lesson.items.length} câu luyện tập`;

    setSections('practice');
    const attempt = newAttempt(lesson);
    renderTheory(lesson);
    renderExamples(lesson);
    renderQuiz(lesson, attempt);

    const submit = document.getElementById('btn-submit');
    submit.disabled = false;
    submit.onclick = () => submitAll(lesson, attempt);
    updateScore(lesson, attempt);

    showOnly('lesson');
  } catch (err) {
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được bài học: ' + err.message));
    showOnly('empty');
  }
}

// Màn hình khởi động: chọn lớp, thông tin bản quyền và khu vực quảng cáo.
const GRADES = [
  { grade: 6, available: false },
  { grade: 7, available: true },
  { grade: 8, available: true },
  { grade: 9, available: false },
];
// Mục lục của từng môn, nạp một lần khi mở app.
const SUBJECT_LABELS = { toan7: 'Toán', ly7: 'Vật lí', hoa7: 'Hoá học', sinh7: 'Sinh học', lichsu7: 'Lịch sử', diali7: 'Địa lí', toan8: 'Toán' };
// Môn học đã có nội dung của từng lớp.
const GRADE_SUBJECTS = { 7: ['toan7', 'ly7', 'hoa7', 'sinh7', 'lichsu7', 'diali7'], 8: ['toan8'] };
const manifestCache = {};

function licenseDaysLeft(expiresOn) {
  // Hết hạn vào cuối ngày ghi trong file.
  const [y, m, d] = expiresOn.split('-').map(Number);
  const end = new Date(y, m - 1, d, 23, 59, 59);
  return Math.ceil((end - new Date()) / 86400000);
}

function renderLicense(license) {
  const info = document.getElementById('license-info');
  const days = document.getElementById('license-days');
  if (license.status === 'ok') {
    info.replaceChildren(
      el('div', {}, `Đơn vị cấp: ${license.owner || '—'}`),
      el('div', { class: 'muted' }, `Mã khóa: ${license.code || '—'} · Phạm vi: ${license.scope || '—'}`),
    );
    const left = licenseDaysLeft(license.expiresOn);
    if (left >= 0) {
      days.replaceChildren(
        el('div', { class: 'days' }, `${left} ngày`),
        el('div', { class: 'muted' }, `Hết hạn ngày ${license.expiresOn.split('-').reverse().join('/')}`),
      );
    } else {
      days.replaceChildren(el('div', { class: 'days' }, 'Đã hết hạn'), el('div', { class: 'muted' }, 'Liên hệ Nam Linh Educenter để gia hạn.'));
    }
  } else {
    info.replaceChildren(el('div', { class: 'muted' }, 'Chưa kích hoạt bản quyền.'));
    days.replaceChildren(el('div', { class: 'muted' }, '—'));
  }
}

function renderGrades() {
  const box = document.getElementById('grades');
  box.replaceChildren();
  for (const g of GRADES) {
    const btn = el('button', { class: 'grade', type: 'button' }, `Lớp ${g.grade}`);
    if (g.available) {
      btn.addEventListener('click', () => showSubjects(g.grade));
    } else {
      btn.disabled = true;
      btn.append(el('small', {}, 'Đang biên soạn'));
    }
    box.append(btn);
  }
}

function showLaunch() {
  document.getElementById('breadcrumb').textContent = '';
  showOnly('launch');
}

// Chọn môn sau khi đã chọn lớp.
let currentGrade = 7;
function showSubjects(grade) {
  currentGrade = grade || currentGrade;
  grade = currentGrade;
  const title = document.querySelector('#subjects h1');
  if (title) title.textContent = `Chọn môn học · Lớp ${grade}`;
  document.getElementById('breadcrumb').textContent = '';
  const box = document.getElementById('subject-list');
  box.replaceChildren();
  for (const subject of GRADE_SUBJECTS[grade] || []) {
    const btn = el('button', { class: 'grade subject-btn', type: 'button' }, SUBJECT_LABELS[subject]);
    btn.addEventListener('click', () => renderHome(manifestCache[subject], subject));
    box.append(btn);
  }
  showOnly('subjects');
}

async function init() {
  try {
    const info = await window.vungBai.appInfo();
    document.getElementById('build').textContent = `v${info.version} · ${info.commit}`;
  } catch {
    // Không hiện số phiên bản nếu không đọc được; không ảnh hưởng luồng chính.
  }
  try {
    for (const subject of Object.keys(SUBJECT_LABELS)) {
      manifestCache[subject] = await window.vungBai.loadManifest(subject);
    }
    document.getElementById('btn-back').addEventListener('click', () => {
      document.getElementById('breadcrumb').textContent = '';
      showOnly('home');
    });
    document.getElementById('btn-grades').addEventListener('click', () => showLaunch());
    renderGrades();
    let license;
    try {
      license = await window.vungBai.loadLicense();
    } catch {
      license = { status: 'missing' };
    }
    renderLicense(license);
    showLaunch();
  } catch (err) {
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được gói nội dung: ' + err.message));
    showOnly('empty');
  }
}

init();
