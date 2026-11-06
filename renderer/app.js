// Engine giao diện bài học: hiển thị lý thuyết, ví dụ, luyện tập và chấm điểm.
// Mọi nội dung từ file JSON được gán bằng textContent để tránh chèn mã HTML ngoài ý muốn.

// Khóa lưu tiến độ được đặt khi mở bài, theo đường dẫn bài học.
let PROGRESS_KEY = null;

const el = (tag, attrs = {}, text) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else node.setAttribute(k, v);
  }
  if (text !== undefined) node.textContent = text;
  return node;
};

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || {};
  } catch {
    return {};
  }
}

function saveProgress(progress) {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
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

function renderQuiz(lesson, progress) {
  const box = document.getElementById('quiz');
  box.replaceChildren();

  lesson.items.forEach((item, idx) => {
    const q = el('div', { class: 'question', 'data-id': item.id });
    q.append(el('span', { class: 'level' }, item.level));
    q.append(el('div', { class: 'stem' }, `${idx + 1}. ${item.stem}`));

    const feedback = el('div', { class: 'feedback', hidden: 'hidden' });

    if (item.type === 'mcq') {
      item.choices.forEach((choice, ci) => {
        const label = el('label', { class: 'choice' });
        const input = el('input', { type: 'radio', name: item.id, value: String(ci) });
        label.append(input, ' ', choice);
        q.append(label);
      });
    } else {
      const input = el('input', { type: 'text', 'aria-label': 'Đáp án' });
      q.append(input);
    }

    const check = el('button', { class: 'primary', type: 'button' }, 'Kiểm tra');
    check.style.marginLeft = '8px';
    check.addEventListener('click', () => checkItem(item, q, feedback, progress));
    q.append(check, feedback);

    const saved = progress[item.id];
    if (saved) showFeedback(item, q, feedback, saved.chosen);

    box.append(q);
  });
}

function readAnswer(item, q) {
  if (item.type === 'mcq') {
    const picked = q.querySelector('input[type="radio"]:checked');
    return picked ? Number(picked.value) : null;
  }
  const text = q.querySelector('input[type="text"]').value.trim();
  return text === '' ? null : text;
}

function isCorrect(item, chosen) {
  if (chosen === null) return false;
  if (item.type === 'mcq') return chosen === item.answer;
  return String(chosen).replace(/\s+/g, '') === String(item.answer).replace(/\s+/g, '');
}

function checkItem(item, q, feedback, progress) {
  const chosen = readAnswer(item, q);
  if (chosen === null) {
    feedback.hidden = false;
    feedback.className = 'feedback bad';
    feedback.textContent = 'Bạn chưa chọn hoặc nhập đáp án.';
    return;
  }
  progress[item.id] = { chosen, correct: isCorrect(item, chosen) };
  saveProgress(progress);
  showFeedback(item, q, feedback, chosen);
}

function showFeedback(item, q, feedback, chosen) {
  const ok = isCorrect(item, chosen);
  feedback.hidden = false;
  feedback.className = 'feedback ' + (ok ? 'ok' : 'bad');
  if (ok) {
    feedback.textContent = 'Đúng. ' + item.explain;
  } else {
    const wrongNote = item.type === 'mcq' ? item.wrong_explain[String(chosen)] : null;
    feedback.textContent = (wrongNote ? wrongNote + ' ' : '') + 'Lời giải: ' + item.explain;
  }
}

function showScore(lesson, progress) {
  const box = document.getElementById('score');
  const byLevel = {};
  let total = 0;
  let correct = 0;
  for (const item of lesson.items) {
    const level = item.level;
    byLevel[level] = byLevel[level] || { total: 0, correct: 0 };
    byLevel[level].total += 1;
    total += 1;
    const saved = progress[item.id];
    if (saved && saved.correct) {
      byLevel[level].correct += 1;
      correct += 1;
    }
  }
  box.replaceChildren();
  box.hidden = false;
  box.append(el('strong', {}, `Đúng ${correct}/${total} câu`));
  const list = el('ul');
  for (const [level, r] of Object.entries(byLevel)) {
    list.append(el('li', {}, `${level}: ${r.correct}/${r.total}`));
  }
  box.append(list);
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
            btn.addEventListener('click', () => openLesson(lesson.file));
            li.append(btn, el('span', { class: 'meta' }, ` · trang ${lesson.bookPage}`));
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
    PROGRESS_KEY = 'vungbai.progress.' + relPath;
    document.getElementById('breadcrumb').textContent =
      `Lớp ${lesson.grade} › ${lesson.subject === 'toan' ? 'Toán' : lesson.subject} › ${lesson.chapter}`;
    document.getElementById('lesson-title').textContent = lesson.lesson;
    document.getElementById('lesson-meta').textContent =
      `Sách: ${lesson.bookSeries} · ${lesson.items.length} câu luyện tập`;
    document.getElementById('score').hidden = true;

    const progress = loadProgress();
    renderTheory(lesson);
    renderExamples(lesson);
    renderQuiz(lesson, progress);

    const btn = document.getElementById('btn-score');
    btn.replaceWith(btn.cloneNode(true));
    document.getElementById('btn-score').addEventListener('click', () => showScore(lesson, progress));

    showOnly('lesson');
  } catch (err) {
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được bài học: ' + err.message));
    showOnly('empty');
  }
}

async function init() {
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
