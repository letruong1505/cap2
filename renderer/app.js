// Engine giao diện bài học: lý thuyết, ví dụ, luyện tập và chấm toàn bài.
// Mỗi lần mở bài là một lượt làm mới: thứ tự phương án được xáo trộn, không lưu kết quả cũ.
// Mọi nội dung từ file JSON được gán bằng textContent để tránh chèn mã HTML ngoài ý muốn.

const R = window.Rational;

// Tạo phần tử; các tham số sau attrs có thể là chữ hoặc phần tử con.
const el = (tag, attrs = {}, ...children) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c === undefined || c === null) continue;
    node.append(c instanceof Node ? c : String(c));
  }
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
    wrap.append(el('p', { class: 'example-label' }, `Ví dụ ${i + 1}`), el('p', { class: 'example-problem' }, ex.problem));
    if (ex.figureSvg) {
      wrap.append(el('img', { class: 'figure', alt: `Hình minh họa ví dụ ${i + 1}`, src: figureSrc(ex.figureSvg) }));
    }
    const steps = el('ol');
    ex.steps.forEach((s) => steps.append(el('li', {}, s)));
    wrap.append(steps);
    wrap.append(el('p', { class: 'example-answer' }, 'Đáp số: ', el('b', {}, viNumber(ex.answer))));
    box.append(wrap);
  });
  // Bài không có ví dụ tính toán (Lịch sử, Địa lí) thì ẩn cả mục "Ví dụ".
  document.getElementById('sec-examples').hidden = lesson.examples.length === 0;
}

function renderQuiz(lesson, attempt) {
  const box = document.getElementById('quiz');
  box.replaceChildren();

  const advBox = document.getElementById('quiz-adv');
  advBox.replaceChildren();
  const advCount = lesson.items.filter((it) => it.level === 'Nâng cao').length;
  document.getElementById('sec-advanced').hidden = advCount === 0;
  // Bài chỉ gồm câu nâng cao: không cần tiêu đề phụ "Bài tập nâng cao" thứ hai.
  document.getElementById('sec-advanced').classList.toggle('only', advCount === lesson.items.length);
  document.getElementById('theory-heading').textContent = lesson.book === 'Bài tập nâng cao' ? 'Hướng dẫn' : 'Lý thuyết';

  let currentLevel = null;
  attempt.questions.forEach((itemIndex, idx) => {
    const item = lesson.items[itemIndex];
    const target = item.level === 'Nâng cao' ? advBox : box;
    if (item.level !== currentLevel) {
      currentLevel = item.level;
      if (item.level !== 'Nâng cao') {
        target.append(el('h3', { class: 'level-heading' }, `Mức ${currentLevel}`));
      }
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
        label.append(input, el('span', {}, choice));
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
    target.append(q);
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

// Số thập phân hiển thị theo kiểu Việt Nam: 4,5 thay cho 4.5.
function viNumber(v) {
  const t = String(v);
  return /^-?\d+\.\d+$/.test(t) ? t.replace('.', ',') : t;
}

function correctText(item) {
  return item.type === 'mcq' ? item.choices[item.answer] : viNumber(item.answer);
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
    // Tô phương án đúng và phương án đã chọn sai.
    if (item.type === 'mcq') {
      q.querySelectorAll('.choice').forEach((label) => {
        const text = label.querySelector('span').textContent;
        if (text === item.choices[item.answer]) label.classList.add('is-right');
        else if (label.querySelector('input').checked) label.classList.add('is-wrong');
      });
    }
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
  box.append(el('p', { class: 'score-total' }, el('b', {}, `${correct}/${total}`), ' câu đúng'));
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

// Biểu tượng ổ khoá cho bài cần bản quyền.
const LOCK_SVG = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';

// Tách "Bài 12. Tên bài" thành số bài và tên bài để hiển thị theo cột.
function splitLessonTitle(title) {
  const m = /^Bài (\d+)\.\s*(.*)$/.exec(title);
  return m ? { no: `Bài ${m[1]}`, name: m[2] } : { no: '', name: title };
}

// Màn hình chính: danh sách chương và bài theo mục lục của môn.
function renderHome(manifest, subject) {
  const home = document.getElementById('home');
  const back = el('button', { class: 'back-link', type: 'button' }, '← Chọn môn');
  back.addEventListener('click', () => showSubjects(currentGrade));

  let total = 0;
  let locked = 0;
  for (const book of manifest.books) for (const c of book.chapters) for (const l of c.lessons) {
    if (!l.file) continue;
    total += 1;
    if (l.locked) locked += 1;
  }
  const head = el('header', { class: 'screen-head' });
  head.append(
    el('p', { class: 'screen-kicker' }, `Lớp ${currentGrade}`),
    el('h1', {}, SUBJECT_LABELS[subject] || 'Chọn bài học'),
    el('p', { class: 'screen-sub' }, locked > 0
      ? `${total} bài. Bạn đang dùng thử: 2 bài đầu mở sẵn, các bài có ổ khoá cần kích hoạt bản quyền.`
      : `${total} bài. Chọn một bài để học lý thuyết và luyện tập.`),
  );
  home.replaceChildren(back, head);

  for (const book of manifest.books) {
    const advanced = book.title === 'Bài tập nâng cao';
    const part = el('section', { class: 'book' + (advanced ? ' book-advanced' : '') });
    part.append(el('h2', { class: 'book-title' }, book.title));
    if (advanced) part.append(el('p', { class: 'screen-sub' }, 'Các câu khó gom theo chương, dành cho bạn muốn thử sức thêm.'));
    for (const chapter of book.chapters) {
      const block = el('div', { class: 'chapter' });
      if (!advanced) block.append(el('h3', {}, chapter.title));
      if (chapter.lessons.length === 0) {
        block.append(el('p', { class: 'meta' }, 'Đang biên soạn'));
        part.append(block);
        continue;
      }
      const list = el('ul', { class: 'lesson-list' });
      for (const lesson of chapter.lessons) {
        const li = el('li');
        const { no, name } = splitLessonTitle(lesson.title);
        if (lesson.file) {
          const btn = el('button', { class: 'lesson-row' + (lesson.locked ? ' locked' : ''), type: 'button' });
          btn.append(el('span', { class: 'lesson-no' }, no), el('span', { class: 'lesson-name' }, name));
          if (lesson.locked) {
            const lock = el('span', { class: 'lesson-lock', title: 'Cần bản quyền' });
            lock.innerHTML = LOCK_SVG;
            btn.append(lock);
            btn.setAttribute('aria-label', `${lesson.title} (cần bản quyền)`);
          }
          // Đường dẫn trong mục lục tính từ thư mục môn, còn bộ nạp tính từ content/.
          btn.addEventListener('click', () => (lesson.locked ? showLockedNotice() : openLesson(subject + '/' + lesson.file, lesson.mode || 'practice')));
          li.append(btn);
        } else {
          const row = el('span', { class: 'lesson-row pending' });
          row.append(el('span', { class: 'lesson-no' }, no), el('span', { class: 'lesson-name' }, name), el('span', { class: 'lesson-tag' }, 'Đang biên soạn'));
          li.append(row);
        }
        list.append(li);
      }
      block.append(list);
      part.append(block);
    }
    home.append(part);
  }
  showOnly('home');
  window.scrollTo(0, 0);
}

// Chế độ hiển thị: luyện tập (có lý thuyết và chấm điểm), ôn tập tự luận, hoặc hướng dẫn giải.
function setSections(mode) {
  const practice = mode === 'practice';
  document.getElementById('sec-theory').hidden = !practice;
  if (!practice) document.getElementById('sec-advanced').hidden = true;
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
      document.getElementById('lesson-kicker').textContent = lesson.chapter || '';
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

    document.getElementById('lesson-kicker').textContent = lesson.book === 'Bài tập nâng cao' ? '' : (lesson.chapter || '');
    document.getElementById('lesson-title').textContent = lesson.lesson;
    document.getElementById('lesson-meta').textContent =
      `Sách ${lesson.bookSeries}. ${lesson.items.length} câu luyện tập, làm xong bấm "Kiểm tra toàn bài" để xem kết quả.`;

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
    window.scrollTo(0, 0);
  } catch (err) {
    console.error(err);
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không mở được bài học này. Hãy quay lại và thử lại; nếu vẫn lỗi, hãy cài lại phần mềm.'));
    showOnly('empty');
  }
}

// Màn hình khởi động: chọn lớp, thông tin bản quyền và khu vực quảng cáo.
const GRADES = [
  { grade: 6, available: true },
  { grade: 7, available: true },
  { grade: 8, available: true },
  { grade: 9, available: true },
];
// Các môn của từng lớp.
const SUBJECT_BASE = { toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', lichsu: 'Lịch sử', diali: 'Địa lí' };
const GRADE_SUBJECTS = {};
const SUBJECT_LABELS = {};
for (const g of [6, 7, 8, 9]) {
  GRADE_SUBJECTS[g] = Object.keys(SUBJECT_BASE).map((k) => k + g);
  for (const k of Object.keys(SUBJECT_BASE)) SUBJECT_LABELS[k + g] = SUBJECT_BASE[k];
}
// Mục lục của từng môn, nạp một lần khi mở app.
const manifestCache = {};

function licenseDaysLeft(expiresOn) {
  // Hết hạn vào cuối ngày ghi trong khoá.
  const [y, m, d] = expiresOn.split('-').map(Number);
  const end = new Date(y, m - 1, d, 23, 59, 59);
  return Math.ceil((end - new Date()) / 86400000);
}

const LICENSE_MESSAGES = {
  invalid: 'Khoá không hợp lệ. Hãy kiểm tra lại và dán đủ toàn bộ khoá.',
  'wrong-machine': 'Khoá này được cấp cho máy khác.',
  expired: 'Khoá đã hết hạn. Liên hệ Nam Linh Educenter để gia hạn.',
  clock: 'Đồng hồ máy bị chỉnh lùi. Hãy chỉnh lại đúng ngày giờ.',
};

let lastLicense = { status: 'missing' };

function gradesText(grades) {
  return grades === 'all' ? 'Tất cả các lớp' : 'Lớp ' + grades.join(', ');
}

function showLockedNotice() {
  window.alert('Bài này cần bản quyền. Bản dùng thử chỉ mở 2 bài đầu của mỗi môn.\nVề màn hình chọn lớp để nhập khoá kích hoạt.');
}

async function refreshLicense() {
  try {
    lastLicense = await window.vungBai.loadLicense();
  } catch {
    lastLicense = { status: 'missing' };
  }
  renderLicense(lastLicense);
  // Mục lục có thể đã đổi trạng thái khoá.
  for (const subject of Object.keys(manifestCache)) manifestCache[subject] = await window.vungBai.loadManifest(subject);
}

function renderLicense(license) {
  const info = document.getElementById('license-info');
  const days = document.getElementById('license-days');
  const children = [];
  if (license.status === 'ok') {
    children.push(
      el('div', {}, `Đơn vị cấp: ${license.owner || '—'}`),
      el('div', { class: 'muted' }, `Mã khoá: ${license.id || '—'} · Phạm vi: ${gradesText(license.grades)}`),
    );
    const left = licenseDaysLeft(license.expiresOn);
    days.replaceChildren(
      el('div', { class: 'days' }, `${left} ngày`),
      el('div', { class: 'muted' }, `Hết hạn ngày ${license.expiresOn.split('-').reverse().join('/')}`),
    );
  } else {
    children.push(el('div', { class: 'muted' }, LICENSE_MESSAGES[license.status] || 'Chưa kích hoạt bản quyền. Đang dùng thử: mở 2 bài đầu của mỗi môn.'));
    days.replaceChildren(el('div', { class: 'muted' }, '—'));
  }
  if (license.machineId) children.push(el('div', { class: 'muted' }, `Mã máy: ${license.machineId} (gửi mã này khi mua khoá)`));

  const input = el('input', { type: 'text', id: 'license-key', placeholder: 'Dán khoá kích hoạt (NL1-...)', autocomplete: 'off', spellcheck: 'false' });
  const btn = el('button', { type: 'button', class: 'primary' }, license.status === 'ok' ? 'Đổi khoá' : 'Kích hoạt');
  const msg = el('div', { class: 'muted', id: 'license-msg' });
  btn.addEventListener('click', async () => {
    const r = await window.vungBai.activateLicense(input.value);
    if (r.status === 'ok') {
      input.value = '';
      await refreshLicense();
    } else {
      msg.textContent = LICENSE_MESSAGES[r.status] || 'Không kích hoạt được.';
    }
  });
  children.push(el('div', { class: 'license-form' }, input, btn), msg);
  info.replaceChildren(...children);
}

function renderGrades() {
  const box = document.getElementById('grades');
  box.replaceChildren();
  for (const g of GRADES) {
    const btn = el('button', { class: 'grade-tile', type: 'button', 'aria-label': `Lớp ${g.grade}` });
    btn.append(
      el('span', { class: 'grade-word' }, 'Lớp'),
      el('span', { class: 'grade-num' }, String(g.grade)),
      el('span', { class: 'grade-note' }, g.available ? `${(GRADE_SUBJECTS[g.grade] || []).length} môn học` : 'Đang biên soạn'),
    );
    if (g.available) btn.addEventListener('click', () => showSubjects(g.grade));
    else btn.disabled = true;
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
  if (title) title.textContent = 'Chọn môn học';
  document.getElementById('subjects-kicker').textContent = `Lớp ${grade}`;
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
    document.getElementById('build').textContent = `Phiên bản ${info.version}`;
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
    await refreshLicense();
    showLaunch();
  } catch (err) {
    console.error(err);
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được nội dung bài học. Hãy cài lại phần mềm hoặc liên hệ Nam Linh: 0968 646 853.'));
    showOnly('empty');
  }
}

init();
