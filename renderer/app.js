// Engine giao diện bài học: lý thuyết, ví dụ, luyện tập và chấm toàn bài.
// Mọi nội dung từ file JSON được gán bằng textContent để tránh chèn mã HTML ngoài ý muốn.

// Khóa lưu tiến độ được đặt khi mở bài, theo đường dẫn bài học.
// Tiền tố v3: dữ liệu của các bản trước không được đọc lại.
let PROGRESS_KEY = null;
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

// Trạng thái bài học: đáp án đã chọn (theo nội dung), và đã nộp bài chưa.
function loadState() {
  try {
    const s = JSON.parse(localStorage.getItem(PROGRESS_KEY));
    return { answers: (s && s.answers) || {}, submitted: !!(s && s.submitted) };
  } catch {
    return { answers: {}, submitted: false };
  }
}

function saveState(state) {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(state));
  } catch {
    // Bỏ qua nếu không ghi được; bản thử vẫn chạy được.
  }
}

function renderTheory(lesson) {
  const box = document.getElementById('theory');
  box.replaceChildren();
  for (const block of lesson.theory) {
    if (block.type === 'formula') {
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
    const steps = el('ol');
    ex.steps.forEach((s) => steps.append(el('li', {}, s)));
    wrap.append(steps);
    wrap.append(el('p', {}, `Đáp số: ${ex.answer}`));
    box.append(wrap);
  });
}

function renderQuiz(lesson, state) {
  const box = document.getElementById('quiz');
  box.replaceChildren();

  lesson.items.forEach((item, idx) => {
    const q = el('div', { class: 'question', 'data-id': item.id });
    q.append(el('span', { class: 'level' }, item.level));
    q.append(el('div', { class: 'stem' }, `${idx + 1}. ${item.stem}`));

    // Chỉ lưu lựa chọn, không hiện đúng sai khi chọn.
    if (item.type === 'mcq') {
      item.choices.forEach((choice, ci) => {
        const label = el('label', { class: 'choice' });
        const input = el('input', { type: 'radio', name: item.id, value: String(ci) });
        input.addEventListener('change', () => {
          state.answers[item.id] = choice;
          saveState(state);
        });
        label.append(input, ' ', choice);
        q.append(label);
      });
    } else {
      const input = el('input', { type: 'text', 'aria-label': 'Đáp án' });
      input.addEventListener('input', () => {
        state.answers[item.id] = input.value.trim() || null;
        saveState(state);
      });
      q.append(input);
    }

    q.append(el('div', { class: 'feedback', hidden: 'hidden' }));
    box.append(q);
    restoreAnswer(item, q, state.answers[item.id]);
  });

  if (state.submitted) applySubmitted(lesson, state);
}

function readAnswer(item, q) {
  if (item.type === 'mcq') {
    const picked = q.querySelector('input[type="radio"]:checked');
    return picked ? item.choices[Number(picked.value)] : null;
  }
  const text = q.querySelector('input[type="text"]').value.trim();
  return text === '' ? null : text;
}

// Đáp án được so theo giá trị (nội dung phương án hoặc số đã nhập), không theo vị trí.
// Với câu điền, 2/4 và 1/2 là cùng một đáp án.
function isCorrect(item, value) {
  if (value === null || value === undefined || value === '') return false;
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

function restoreAnswer(item, q, value) {
  if (value === null || value === undefined || value === '') return;
  if (item.type === 'mcq') {
    const idx = item.choices.indexOf(value);
    const input = q.querySelector(`input[type="radio"][value="${idx}"]`);
    if (input) input.checked = true;
  } else {
    q.querySelector('input[type="text"]').value = value;
  }
}

function lockQuestion(q) {
  q.querySelectorAll('input').forEach((i) => { i.disabled = true; });
}

// Hiển thị kết quả của một câu sau khi nộp bài.
function showResult(item, feedback, value) {
  feedback.hidden = false;
  const explain = item.explain;

  if (value === null || value === undefined || value === '') {
    feedback.className = 'feedback bad';
    feedback.textContent = `Bạn chưa trả lời. Đáp án đúng: ${correctText(item)}. Lời giải: ${explain}`;
    return;
  }
  if (item.type === 'fill') {
    try {
      R.parse(value);
    } catch {
      feedback.className = 'feedback bad';
      feedback.textContent = `Chưa đúng định dạng a/b. Đáp án đúng: ${item.answer}. Lời giải: ${explain}`;
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
  feedback.textContent = (note ? note + ' ' : '') + 'Lời giải: ' + explain;
}

// Hiển thị kết quả toàn bài và khóa mọi câu. Dùng cho cả lần nộp vừa xong và lần mở lại.
function applySubmitted(lesson, state) {
  lesson.items.forEach((item) => {
    const q = document.querySelector(`.question[data-id="${item.id}"]`);
    if (!q) return;
    showResult(item, q.querySelector('.feedback'), state.answers[item.id]);
    lockQuestion(q);
  });
  document.getElementById('btn-submit').disabled = true;
  updateScore(lesson, state);
}

// Nộp bài: đọc đáp án hiện tại, lưu, rồi chấm toàn bộ.
function submitAll(lesson, state) {
  if (state.submitted) return;
  lesson.items.forEach((item) => {
    const q = document.querySelector(`.question[data-id="${item.id}"]`);
    state.answers[item.id] = q ? readAnswer(item, q) : null;
  });
  state.submitted = true;
  saveState(state);
  applySubmitted(lesson, state);
}

function updateScore(lesson, state) {
  const box = document.getElementById('score');
  box.replaceChildren();

  if (!state.submitted) {
    const unanswered = lesson.items.filter((i) => {
      const v = state.answers[i.id];
      return v === null || v === undefined || v === '';
    }).length;
    box.append(el('span', { class: 'meta' },
      `Còn ${unanswered} câu chưa trả lời. Bấm Kiểm tra toàn bài khi làm xong.`));
    return;
  }

  const byLevel = {};
  let total = 0;
  let correct = 0;
  for (const item of lesson.items) {
    byLevel[item.level] = byLevel[item.level] || { total: 0, correct: 0 };
    byLevel[item.level].total += 1;
    total += 1;
    if (isCorrect(item, state.answers[item.id])) {
      byLevel[item.level].correct += 1;
      correct += 1;
    }
  }
  box.append(el('strong', {}, `Đúng ${correct}/${total} câu`));
  const levels = Object.entries(byLevel)
    .map(([level, r]) => `${level} ${r.correct}/${r.total}`)
    .join('  ·  ');
  box.append(el('div', { class: 'meta' }, levels));
}

function showOnly(id) {
  for (const sec of ['home', 'lesson', 'empty']) {
    document.getElementById(sec).hidden = sec !== id;
  }
}

// Màn hình chính: danh sách chương và bài theo manifest của gói nội dung.
function renderHome(manifest) {
  const home = document.getElementById('home');
  home.replaceChildren(el('h1', {}, 'Chọn bài học'));
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
            btn.addEventListener('click', () => openLesson('toan7/' + lesson.file));
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

async function openLesson(relPath) {
  try {
    const lesson = await window.vungBai.loadLesson(relPath);
    PROGRESS_KEY = 'vungbai.v3.progress.' + relPath;
    document.getElementById('breadcrumb').textContent =
      `Lớp ${lesson.grade} › ${lesson.subject === 'toan' ? 'Toán' : lesson.subject} › ${lesson.chapter}`;
    document.getElementById('lesson-title').textContent = lesson.lesson;
    document.getElementById('lesson-meta').textContent =
      `Sách: ${lesson.bookSeries} · ${lesson.items.length} câu luyện tập`;

    const state = loadState();
    renderTheory(lesson);
    renderExamples(lesson);
    renderQuiz(lesson, state);

    const submit = document.getElementById('btn-submit');
    submit.disabled = state.submitted;
    submit.onclick = () => {
      submitAll(lesson, state);
    };
    if (!state.submitted) updateScore(lesson, state);

    showOnly('lesson');
  } catch (err) {
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được bài học: ' + err.message));
    showOnly('empty');
  }
}

async function init() {
  try {
    const info = await window.vungBai.appInfo();
    document.getElementById('build').textContent = `v${info.version} · ${info.commit}`;
  } catch {
    // Không hiện số phiên bản nếu không đọc được; không ảnh hưởng luồng chính.
  }
  try {
    const manifest = await window.vungBai.loadManifest();
    document.getElementById('breadcrumb').textContent = '';
    document.getElementById('btn-back').addEventListener('click', () => {
      document.getElementById('breadcrumb').textContent = '';
      showOnly('home');
    });
    renderHome(manifest);
  } catch (err) {
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được gói nội dung: ' + err.message));
    showOnly('empty');
  }
}

init();
