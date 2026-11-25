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
const lastOrders = {};
function newAttempt(lesson) {
  // Làm lại bài thì thứ tự câu và vị trí đáp án khác lượt trước (thử tối đa 8 lần nếu bài đủ dài để khác được).
  const key = lesson.items.map((i) => i.id).join('|');
  let questions; let order;
  for (let t = 0; t < 8; t++) {
    questions = orderedQuestionIndexes(lesson);
    order = {};
    for (const item of lesson.items) {
      if (item.type === 'mcq') order[item.id] = shuffle(item.choices.map((_, i) => i));
    }
    if (lesson.items.length < 3 || JSON.stringify({ questions, order }) !== lastOrders[key]) break;
  }
  lastOrders[key] = JSON.stringify({ questions, order });
  return { questions, order, answers: {}, submitted: false, started: Date.now(), meta: null };
}

function figureSrc(svg) {
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
}

// Hình không gian có kèm mô hình 3D thì dựng bản xoay được 360°; còn lại (hoặc nếu lỗi) dùng ảnh tĩnh.
function figureNode(svg, alt) {
  const S = window.NL_SOLID3D;
  const model = S ? S.extractModel(svg) : null;
  if (model) {
    try {
      const host = el('div', { class: 'solid3d-host' });
      S.mount(host, model, { alt: alt || '' });
      return host;
    } catch (e) { /* dùng ảnh tĩnh */ }
  }
  return el('img', { class: 'figure', alt: alt || '', src: figureSrc(svg) });
}

function figureBlock(svg, caption) {
  const fig = el('figure', { class: 'theory-figure' });
  fig.append(figureNode(svg, caption || ''));
  if (caption) fig.append(el('figcaption', {}, caption));
  return fig;
}

function methodBlock(m) {
  // Khung "Cách giải" cho một dạng bài: nhận dạng, các bước, lưu ý và ví dụ mẫu.
  const wrap = el('div', { class: 'method' });
  wrap.append(el('p', { class: 'method-title' }, 'Cách giải: ', m.title));
  if (m.when) wrap.append(el('p', { class: 'method-when' }, el('b', {}, 'Nhận dạng: '), m.when));
  const steps = el('ol', { class: 'method-steps' });
  m.steps.forEach((t, i) => steps.append(el('li', {}, el('b', {}, `Bước ${i + 1}. `), t)));
  wrap.append(steps);
  if (Array.isArray(m.notes) && m.notes.length) {
    const notes = el('div', { class: 'method-notes' }, el('p', { class: 'method-notes-title' }, 'Lưu ý'));
    const ul = el('ul');
    m.notes.forEach((t) => ul.append(el('li', {}, t)));
    notes.append(ul);
    wrap.append(notes);
  }
  if (m.sample) {
    const sm = el('div', { class: 'method-sample' }, el('p', { class: 'method-sample-label' }, 'Ví dụ mẫu'), el('p', { class: 'method-sample-problem' }, m.sample.problem));
    const ol = el('ol');
    m.sample.steps.forEach((t) => ol.append(el('li', {}, t)));
    sm.append(ol);
    if (m.sample.answer) sm.append(el('p', { class: 'example-answer' }, 'Kết quả: ', el('b', {}, m.sample.answer)));
    wrap.append(sm);
  }
  return wrap;
}

// Lý thuyết dạng thẻ (ngữ pháp, tiếng Anh): tóm tắt một dòng, mỗi ý một thẻ có công thức tô màu, bảng, ví dụ có phiên âm đọc, lỗi hay gặp và câu hỏi thử nhanh.
// Chữ trong thẻ có thể đánh dấu màu: {s Teenagers} = chủ ngữ, {v face} = động từ, {c so} = liên từ, {k nội dung} = từ khóa.
function richText(str) {
  const frag = document.createDocumentFragment();
  const re = /\{([svck]) ([^}]+)\}/g;
  let last = 0; let m;
  const text = String(str);
  while ((m = re.exec(text))) {
    if (m.index > last) appendLimits(frag, text.slice(last, m.index));
    const sp = el('span', { class: 'rt rt-' + m[1] });
    appendLimits(sp, m[2]);
    frag.append(sp);
    last = m.index + m[0].length;
  }
  if (last < text.length) appendLimits(frag, text.slice(last));
  return frag;
}

// Tích phân có cận: viết ∫_a^b hoặc |_a^b (cận một kí tự) thì hiện cận dưới, cận trên xếp chồng cạnh dấu.
// Chỉ số dưới: x_A, y_CĐ, Q_r, a_{p+1} hiện thành chỉ số nhỏ ở dưới.
function appendLimits(parent, text) {
  const re = /(∫|\|)_([A-Za-z0-9])\^([A-Za-z0-9])/g;
  let last = 0; let m;
  while ((m = re.exec(text))) {
    if (m.index > last) appendSubs(parent, text.slice(last, m.index));
    parent.append(m[1], el('span', { class: 'lim' }, el('span', {}, m[3]), el('span', {}, m[2])));
    last = m.index + m[0].length;
  }
  if (last < text.length) appendSubs(parent, text.slice(last));
}

function appendSubs(parent, text) {
  const re = /_(\{[^}]+\}|[A-Za-z0-9ĐĐ]+)/g;
  let last = 0; let m;
  while ((m = re.exec(text))) {
    if (m.index > last) parent.append(text.slice(last, m.index));
    const sub = m[1].startsWith('{') ? m[1].slice(1, -1) : m[1];
    parent.append(el('sub', {}, sub));
    last = m.index + m[0].length;
  }
  if (last < text.length) parent.append(text.slice(last));
}

function plainText(str) { return String(str).replace(/\{[svck] ([^}]+)\}/g, '$1'); }

function speakEnglish(text) {
  if (window.vungBai && typeof window.vungBai.speak === 'function') { window.vungBai.speak(text); return; }
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text); u.lang = 'en-US'; u.rate = 0.9;
  const v = window.speechSynthesis.getVoices().find((x) => /^en[-_]/i.test(x.lang));
  if (v) u.voice = v;
  window.speechSynthesis.speak(u);
}

function tryBlock(t) {
  const box = el('div', { class: 'g-try' }, el('p', { class: 'g-try-label' }, 'Thử ngay'), el('p', { class: 'g-try-q' }, richText(t.q)));
  const res = el('p', { class: 'g-try-res', 'aria-live': 'polite' });
  const row = el('div', { class: 'g-try-opts' });
  t.options.forEach((o, i) => {
    const b = el('button', { type: 'button', class: 'g-try-opt' }, richText(o));
    b.addEventListener('click', () => {
      row.querySelectorAll('button').forEach((x) => { x.classList.remove('ok', 'no'); });
      b.classList.add(i === t.answer ? 'ok' : 'no');
      res.textContent = i === t.answer ? '✓ Đúng! ' + (t.explain || '') : '✗ Chưa đúng, thử lại nhé.' ;
      res.className = 'g-try-res ' + (i === t.answer ? 'ok' : 'no');
    });
    row.append(b);
  });
  box.append(row, res);
  return box;
}

function grammarCard(c) {
  const card = el('section', { class: 'g-card' });
  card.append(el('h3', { class: 'g-title' }, c.n ? el('span', { class: 'g-n' }, String(c.n)) : '', c.title));
  if (c.text) card.append(el('p', { class: 'g-text' }, richText(c.text)));
  (c.formulas || []).forEach((f) => card.append(el('div', { class: 'g-formula' }, richText(f))));
  if (c.points && c.points.length) {
    const ul = el('ul', { class: 'g-points' });
    c.points.forEach((x) => ul.append(el('li', {}, richText(x))));
    card.append(ul);
  }
  if (c.timeline && c.timeline.length) {
    const ol = el('ol', { class: 'g-timeline' });
    c.timeline.forEach((r) => ol.append(el('li', {}, el('span', { class: 'g-tl-when' }, richText(r[0])), el('span', { class: 'g-tl-what' }, richText(r[1])))));
    card.append(ol);
  }
  if (c.table) {
    const tb = el('table', { class: 'g-table' });
    tb.append(el('tr', {}, ...c.table.head.map((x) => el('th', {}, x))));
    c.table.rows.forEach((r) => tb.append(el('tr', {}, ...r.map((x, i) => el('td', {}, i === 0 ? el('b', {}, richText(x)) : richText(x))))));
    card.append(el('div', { class: 'g-table-wrap' }, tb));
  }
  if (c.examples && c.examples.length) {
    const ul = el('ul', { class: 'g-ex' });
    c.examples.forEach((ex) => {
      const sp = el('button', { type: 'button', class: 'g-speak', 'aria-label': 'Nghe câu', title: 'Nghe' }, '🔊');
      sp.addEventListener('click', () => speakEnglish(plainText(ex.en)));
      ul.append(el('li', {}, el('div', { class: 'g-en' }, sp, el('span', { class: 'g-en-t' }, richText(ex.en))), ex.vi ? el('div', { class: 'g-vi' }, ex.vi) : ''));
    });
    card.append(el('p', { class: 'g-sub' }, 'Ví dụ'), ul);
  }
  if (c.wrong) {
    card.append(el('div', { class: 'g-pitfall' }, el('p', { class: 'g-pit-title' }, c.pitTitle || 'Lỗi hay gặp'),
      el('p', { class: 'g-wrong' }, el('b', {}, c.wrongLabel || '✗ Sai: '), richText(c.wrong)),
      el('p', { class: 'g-right' }, el('b', {}, c.rightLabel || '✓ Đúng: '), richText(c.right)),
      c.why ? el('p', { class: 'g-why' }, c.why) : ''));
  }
  if (c.tip) card.append(el('p', { class: 'g-tip' }, el('b', {}, 'Mẹo nhớ: '), richText(c.tip)));
  if (c.try) card.append(tryBlock(c.try));
  if (c.collapse) {
    const d = el('details', { class: 'g-more' }, el('summary', {}, c.collapse));
    d.append(card);
    return d;
  }
  return card;
}

function renderTheory(lesson) {
  const box = document.getElementById('theory');
  box.replaceChildren();
  for (const block of lesson.theory) {
    if (block.type === 'figure') {
      box.append(figureBlock(block.figureSvg, block.caption));
    } else if (block.type === 'formula') {
      box.append(el('p', { class: 'formula' }, block.content));
    } else if (block.type === 'method') {
      box.append(methodBlock(block));
    } else if (block.type === 'summary') {
      box.append(el('div', { class: 'g-summary' }, el('p', { class: 'g-sum-label' }, block.label || 'Tóm tắt'), el('p', { class: 'g-sum-text' }, richText(block.content))));
    } else if (block.type === 'card') {
      box.append(grammarCard(block));
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
      wrap.append(figureNode(ex.figureSvg, `Hình minh họa ví dụ ${i + 1}`));
    }
    const steps = el('ol');
    ex.steps.forEach((s) => steps.append(el('li', {}, s)));
    wrap.append(steps);
    // Ví dụ chứng minh hoặc lập luận không có đáp số riêng: các bước đã kết thúc bằng kết luận.
    if (ex.answer !== undefined) {
      wrap.append(el('p', { class: 'example-answer' }, 'Đáp số: ', el('b', {}, viNumber(ex.answer))));
    }
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
    if (item.figureSvg) q.append(figureNode(item.figureSvg, `Hình minh họa câu ${idx + 1}`));

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
  // Nộp bài luyện tập được tính là một ngày học (chuỗi ngày học).
  if (window.VungGames) window.VungGames.recordStudy();
  if (window.VungProgressUI) { window.VungProgressUI.record(lesson, attempt, attempt.meta); window.VungProgressUI.refreshBadge(); }
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
  if (window.VungProgress) {
    const P = window.VungProgress;
    box.append(el('p', { class: 'score-total' }, 'Điểm: ', el('b', {}, `${P.score10(correct, total)}/10`), ` · +${P.points(correct, total)} điểm thưởng`));
  }
  if (wrong.length > 0) {
    const list = el('ul', { class: 'wrong-list' });
    for (const w of wrong) {
      list.append(el('li', {}, `Câu ${w.no}: Đáp án đúng là ${w.answer}`));
    }
    box.append(list);
  }
}

function showOnly(id) {
  for (const sec of ['launch', 'subjects', 'home', 'lesson', 'exam', 'games', 'game', 'national', 'aiwork', 'giasu', 'tuduy', 'examprep', 'thpt', 'purchase', 'review', 'report', 'parent-view', 'empty']) {
    document.getElementById(sec).hidden = sec !== id;
  }
}

// Biểu tượng ổ khoá cho bài cần bản quyền.
const LOCK_SVG = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';

// Tách "Bài 12. Tên bài" thành số bài và tên bài để hiển thị theo cột.
function splitLessonTitle(title) {
  const m = /^(Bài|Unit) (\d+)\.\s*(.*)$/.exec(title);
  return m ? { no: `${m[1]} ${m[2]}`, name: m[3] } : { no: '', name: title };
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
  // Trò chơi chỉ dành cho bản đã kích hoạt; bản dùng thử thì hiện ổ khoá.
  const gamesBtn = el('button', { class: 'games-entry', type: 'button' }, 'Trò chơi');
  const gamesOpen = subjectLicensed(lastLicense, subject);
  if (!gamesOpen) {
    gamesBtn.classList.add('locked');
    const lock = el('span', { class: 'games-lock', 'aria-hidden': 'true' });
    lock.innerHTML = LOCK_SVG;
    gamesBtn.append(lock);
    gamesBtn.setAttribute('aria-label', 'Trò chơi (cần bản quyền)');
  }
  gamesBtn.addEventListener('click', () => {
    if (!subjectLicensed(lastLicense, subject)) {
      window.alert(lastLicense.status === 'ok'
        ? 'Khoá hiện tại không bao gồm môn/lớp này. Trò chơi của môn này cần khoá riêng.'
        : 'Trò chơi cần kích hoạt bản quyền. Bản dùng thử chỉ có bài học.\nVề màn hình chọn lớp để nhập khoá kích hoạt.');
      return;
    }
    window.VungGames.open({
      subject,
      label: SUBJECT_LABELS[subject] || '',
      kicker: `Lớp ${currentGrade}`,
      manifest: manifestCache[subject],
      onBack: () => renderHome(manifestCache[subject], subject),
    });
  });
  head.append(gamesBtn);
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
  if (!practice) { document.getElementById('sec-english-top').hidden = true; document.getElementById('sec-english-bottom').hidden = true; }
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
    if (q.figureSvg) card.append(figureNode(q.figureSvg, `Hình minh họa câu ${idx + 1}`));
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
      `Lớp ${lesson.grade} › ${{ anh: 'Tiếng Anh', toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', gdktpl: 'Giáo dục KT&PL', 'lich-su': 'Lịch sử', 'dia-li': 'Địa lí' }[lesson.subject] || lesson.subject} › ${lesson.chapter}`;

    if (lesson.kind === 'exam' && window.VungExam) {
      window.VungExam.open(lesson, relPath, () => { document.getElementById('breadcrumb').textContent = ''; showOnly('home'); });
      return;
    }

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
    attempt.meta = { subject: lesson.subject, grade: lesson.grade, lessonId: relPath, lesson: lesson.lesson, chapter: lesson.chapter };
    renderTheory(lesson);
    if (window.NL_ENGLISH && window.NL_ENGLISH.render) {
      window.NL_ENGLISH.render(lesson, { top: document.getElementById('sec-english-top'), bottom: document.getElementById('sec-english-bottom') });
    }
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
    if (err && String(err.message || err).includes('NOT_DOWNLOADED')) {
      // Khóa đã có bản quyền nhưng nội dung chưa về máy: thử tải ngay và báo khách chờ.
      if (window.vungBai.packsSync) window.vungBai.packsSync().catch(() => {});
      document.getElementById('empty').replaceChildren(el('p', {}, 'Nội dung khóa học này chưa được tải về máy. Phần mềm đang tải; hãy giữ kết nối mạng, đợi tải xong rồi mở lại bài.'));
      showOnly('empty');
      return;
    }
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không mở được bài học này. Hãy quay lại và thử lại; nếu vẫn lỗi, hãy cài lại phần mềm.'));
    showOnly('empty');
  }
}

// Màn hình khởi động: chọn lớp, thông tin bản quyền và khu vực quảng cáo.
// Lớp và môn lấy từ cấu hình sản phẩm (THCS hoặc THPT), nạp khi mở app.
let GRADES = [];
const SUBJECT_BASE = { anh: 'Tiếng Anh', toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', gdktpl: 'Giáo dục KT&PL', lichsu: 'Lịch sử', diali: 'Địa lí' };
const GRADE_SUBJECTS = {};
// Giá bản quyền theo lớp, hiển thị dưới mỗi ô lớp.
const GIFT_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 7h-2.2A3 3 0 0 0 12 4.6 3 3 0 0 0 6.2 7H4a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1ZM15 5a1 1 0 1 1 0 2h-2.2A2.99 2.99 0 0 1 15 5ZM9 5a1 1 0 0 1 2.2 2H9a1 1 0 0 1 0-2Zm2 15H6v-7h5v7Zm0-9H5V9h6v2Zm2 9v-7h5v7h-5Zm6-9h-6V9h6v2Z"/></svg>';
function giftBadge() { const b = el('span', { class: 'gift-badge', title: 'Tặng kèm', 'aria-label': 'Tặng kèm' }); b.innerHTML = GIFT_SVG; return b; }
const GRADE_PRICE = { 6: '399.000 đ', 7: '399.000 đ', 8: '399.000 đ', 9: '399.000 đ', 10: '449.000 đ', 11: '449.000 đ', 12: '499.000 đ' };
const SUBJECT_LABELS = {};
function applyProduct(product) {
  for (const g of product.grades) GRADE_SUBJECTS[g] = [];
  for (const subject of product.subjects) {
    const grade = Number(subject.match(/(\d+)$/)[1]);
    const base = subject.slice(0, -String(grade).length);
    GRADE_SUBJECTS[grade].push(subject);
    SUBJECT_LABELS[subject] = SUBJECT_BASE[base] || base;
  }
  // Lớp chưa có môn nào hiển thị trước nhưng đánh dấu "Đang biên soạn".
  GRADES = product.grades.map((g) => ({ grade: g, available: GRADE_SUBJECTS[g].length > 0 }));
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
  'wrong-machine': 'Khoá này được cấp cho thiết bị khác. Nếu bạn đã mua, hãy nhập mã đơn và số điện thoại ở mục "Đã mua ở thiết bị khác" bên dưới để nhận khóa cho thiết bị này.',
  revoked: 'Khóa này đã bị thu hồi. Liên hệ Zalo 0968 646 853 để được hỗ trợ.',
  expired: 'Khoá đã hết hạn. Liên hệ Nam Linh Educenter để gia hạn.',
  clock: 'Đồng hồ máy bị chỉnh lùi. Hãy chỉnh lại đúng ngày giờ.',
};

let lastLicense = { status: 'missing' };

// Khoá chỉ mở môn của đúng các lớp trong khoá (grades = 'all' hoặc danh sách lớp), giống main/license/index.js.
function subjectLicensed(license, subject) {
  if (!license || license.status !== 'ok') return false;
  if (license.grades === 'all') return true;
  const grade = Number(String(subject).match(/(\d+)$/)?.[1]);
  return Array.isArray(license.grades) && license.grades.includes(grade);
}

function gradesText(grades) {
  return grades === 'all' ? 'Tất cả các lớp' : 'Lớp ' + grades.join(', ');
}

function showLockedNotice() {
  window.alert('Bài này cần bản quyền. Bản dùng thử chỉ mở 2 bài đầu của mỗi môn.\nVề màn hình chọn lớp để nhập khoá kích hoạt.');
}

// Tải nội dung khóa học về máy sau khi kích hoạt: báo tiến độ ở màn hình chọn lớp. Khóa đã tải xong thì học offline được.
let packWasBusy = false;
let packDoneShown = false;
function renderPackStatus(st) {
  const box = document.getElementById('pack-status');
  if (!box || !st || !st.enabled) return;
  const lic = lastLicense && lastLicense.status === 'ok' ? lastLicense : null;
  const owned = lic ? (lic.grades === 'all' ? GRADES.map((g) => g.grade || g) : (lic.grades || [])) : [];
  const lc = lic && Array.isArray(lic.courses) ? lic.courses : [];
  const ownedCourses = (window.NLCourse ? window.NLCourse.PACKED : []).filter((id) => lc.includes(id) || (/^tu-duy-lap-trinh-/.test(id) && lc.includes('tu-duy-lap-trinh')));
  const missing = owned.filter((g) => !(st.grades || []).includes(g)).concat(ownedCourses.filter((id) => !(st.courses || []).includes(id)));
  const retry = el('button', { type: 'button' }, 'Tải lại');
  retry.addEventListener('click', () => { if (window.vungBai.packsSync) window.vungBai.packsSync().catch(() => {}); });
  let msg = null;
  if (st.state === 'downloading') {
    packWasBusy = true; packDoneShown = false; const pc = Math.max(0, Math.min(99, Number(st.percent) || 0));
    const bar = el('div', { class: 'pack-bar' }, el('div', { class: 'pack-bar-fill', style: `width:${pc}%` }));
    msg = [el('b', {}, `Đang tải nội dung khóa học: ${pc}%`), ` (phần ${(st.done || 0) + 1}/${st.total || 1}). Vui lòng giữ kết nối mạng.`, bar];
  } else if (st.state === 'ready' && !packDoneShown && (packWasBusy || st.fresh)) {
    packWasBusy = false; packDoneShown = true; const close = el('button', { type: 'button' }, 'Đóng'); close.addEventListener('click', () => { box.hidden = true; });
    msg = [el('b', {}, 'Đã tải xong nội dung khóa học (100%).'), ' Từ giờ học được cả khi không có mạng. ', close];
  }
  else if ((st.state === 'offline' || st.state === 'error') && missing.length) msg = [el('b', {}, st.state === 'offline' ? 'Chưa tải được nội dung khóa học vì không có mạng.' : (st.error || 'Chưa tải được nội dung khóa học.')), ' Có mạng, phần mềm sẽ tự tải. ', retry];
  if (!msg) { if (st.state !== 'ready' || !packWasBusy) box.hidden = true; return; }
  box.replaceChildren(...msg); box.hidden = false;
}
if (window.vungBai && window.vungBai.onPacks) {
  window.vungBai.onPacks(renderPackStatus);
  window.vungBai.packsStatus().then(renderPackStatus).catch(() => {});
}

// Máy chủ báo khóa bị thu hồi hoặc khôi phục: tải lại để mục lục và các khóa Kỹ năng đổi theo ngay.
if (window.vungBai && window.vungBai.onLicenseChanged) {
  window.vungBai.onLicenseChanged(() => {
    window.alert('Bản quyền trên máy này vừa được cập nhật. Phần mềm sẽ tải lại.');
    window.location.reload();
  });
}

async function refreshLicense() {
  try {
    lastLicense = await window.vungBai.loadLicense();
  } catch {
    lastLicense = { status: 'missing' };
  }
  renderLicense(lastLicense);
  if (window.vungBai.packsStatus) window.vungBai.packsStatus().then(renderPackStatus).catch(() => {});
  // Mục lục có thể đã đổi trạng thái khoá.
  for (const subject of Object.keys(manifestCache)) manifestCache[subject] = await window.vungBai.loadManifest(subject);
}

function renderLicense(license) {
  const info = document.getElementById('license-info');
  const status = document.getElementById('license-status');
  const children = [];
  const courses = [];
  let termBig;
  let termSmall;
  if (license.status === 'ok') {
    children.push(
      el('div', {}, `Cấp cho: ${license.owner || '—'}`),
      el('div', { class: 'muted' }, `Mã khoá: ${license.id || '—'}`),
    );
    if (license.grades === 'all' || (license.grades || []).length) courses.push(`Giáo trình Văn hóa · ${gradesText(license.grades)}`);
    for (const id of license.courses || []) courses.push(window.NL_CATALOG.byId[id]?.name || id);
    if (license.expiresOn === 'never') {
      termBig = 'Vĩnh viễn';
      termSmall = 'Không giới hạn thời gian trên thiết bị này';
    } else {
      const left = licenseDaysLeft(license.expiresOn);
      termBig = `${left} ngày`;
      termSmall = `Hết hạn ngày ${license.expiresOn.split('-').reverse().join('/')}`;
    }
  } else {
    children.push(el('div', { class: 'muted' }, LICENSE_MESSAGES[license.status] || 'Chưa kích hoạt bản quyền. Đang dùng thử: Mở 2 bài đầu của mỗi môn.'));
    termBig = '—';
    termSmall = 'Chưa có bản quyền trả phí';
  }
  courses.push('Định hướng công nghệ quốc gia · Miễn phí');
  if (license.machineId) children.push(el('div', { class: 'muted' }, `Mã máy: ${license.machineId} (gửi mã này khi mua khoá)`));
  // Thu gọn như "Lời nhắn từ Nam Linh": dòng tiêu đề luôn thấy thời hạn, bấm mới xổ danh sách khóa học.
  const wasOpen = !!status.querySelector('details[open]');
  const det = el('details', { class: 'license-fold' },
    el('summary', {}, el('span', { class: 'license-fold-title' }, 'Thời hạn bản quyền & khóa học'), el('b', { class: 'license-fold-term' }, termBig)),
    el('div', { class: 'license-fold-body' },
      el('div', { class: 'muted' }, termSmall),
      el('div', { class: 'license-courses-label' }, 'Khóa học đã đăng ký'),
      el('ul', { class: 'license-courses' }, ...courses.map((c) => el('li', {}, c)))));
  if (wasOpen) det.open = true;
  status.replaceChildren(det);

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
  if (window.vungBai.familySync) children.push(familyBox());
  if (window.vungBai.claimDevice) children.push(claimDeviceBox());
  // Thu gọn phần kích hoạt như hộp thời hạn: dòng tiêu đề cho biết trạng thái, bấm mới xổ ra khoá, mã máy, mã gia đình.
  const infoWasOpen = !!info.querySelector('details[open]');
  const infoDet = el('details', { class: 'license-fold' },
    el('summary', {}, el('span', { class: 'license-fold-title' }, 'Kích hoạt & mã máy'), el('b', { class: 'license-fold-term' }, license.status === 'ok' ? 'Đã kích hoạt' : 'Chưa kích hoạt')),
    el('div', { class: 'license-fold-body' }, ...children));
  if (infoWasOpen) infoDet.open = true;
  info.replaceChildren(infoDet);
}

// Mã gia đình: phụ huynh mua trên app Phụ huynh, máy của con nhập mã một lần rồi tự nhận khóa mỗi khi có mạng.
const FAMILY_KEY = 'nl-family-code';
const cleanFamily = (v) => String(v || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8);
const getFamily = () => { try { return localStorage.getItem(FAMILY_KEY) || ''; } catch { return ''; } };
let familyBusy = false;
async function syncFamilyNow() {
  const fcode = getFamily();
  if (!fcode || familyBusy || !window.vungBai || !window.vungBai.familySync) return null;
  familyBusy = true;
  try {
    const r = await window.vungBai.familySync({ fcode });
    if (r && r.ok && r.activated) await refreshLicense();
    return r;
  } catch { return null; } finally { familyBusy = false; }
}
function startFamilySync() {
  if (!window.vungBai || !window.vungBai.familySync) return;
  setTimeout(syncFamilyNow, 3000);
  setInterval(syncFamilyNow, 10 * 60 * 1000);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') syncFamilyNow(); });
}
function familyBox() {
  const code = el('input', { type: 'text', id: 'family-code', placeholder: 'Mã gia đình (8 ký tự)', maxlength: '12', autocomplete: 'off', spellcheck: 'false', value: getFamily() });
  const btn = el('button', { type: 'button', class: 'primary' }, 'Lưu và đồng bộ');
  const msg = el('div', { class: 'muted', id: 'family-msg', role: 'status' }, getFamily() ? 'Đã liên kết gia đình. Khóa phụ huynh mua sẽ tự về máy này khi có mạng.' : '');
  btn.addEventListener('click', async () => {
    const v = cleanFamily(code.value);
    if (v.length !== 8) { msg.textContent = 'Mã gia đình gồm 8 ký tự, xem trong app Nam Linh Educenter cho phụ huynh.'; return; }
    btn.disabled = true; msg.textContent = 'Đang đồng bộ...';
    try {
      const r = await window.vungBai.familySync({ fcode: v });
      if (!r.ok) { msg.textContent = r.offline ? 'Cần kết nối mạng. Hãy kiểm tra mạng rồi thử lại.' : (r.error || 'Không đồng bộ được.'); return; }
      try { localStorage.setItem(FAMILY_KEY, v); } catch { /* bỏ qua */ }
      msg.textContent = r.total ? (r.activated ? `Đã nhận ${r.activated} khóa từ phụ huynh.` : 'Đã có khóa này trên máy.') : 'Đã liên kết. Khi phụ huynh mua khóa học và thanh toán xong, khóa sẽ tự về máy này.';
      if (r.full) msg.textContent += ` (${r.full} đơn đã dùng hết chỗ cho loại máy này.)`;
      if (r.activated) await refreshLicense();
    } catch { msg.textContent = 'Không đồng bộ được. Hãy thử lại.'; } finally { btn.disabled = false; }
  });
  return el('div', { class: 'license-claim' },
    el('h3', {}, 'Phụ huynh mua cho con?'),
    el('div', { class: 'muted' }, 'Nhập mã gia đình trong app Nam Linh Educenter cho phụ huynh một lần. Sau đó khóa học phụ huynh mua sẽ tự về máy này mỗi khi có mạng.'),
    el('div', { class: 'license-form' }, code, btn),
    msg,
  );
}

// Một đơn dùng được cho 1 máy tính và 1 điện thoại: nhập mã đơn + số điện thoại đã mua để nhận khóa cho thiết bị này.
function claimDeviceBox() {
  const code = el('input', { type: 'text', id: 'claim-code', placeholder: 'Mã đơn, ví dụ 3KAHFK', maxlength: '14', autocomplete: 'off', spellcheck: 'false' });
  const phone = el('input', { type: 'tel', id: 'claim-phone', placeholder: 'Số điện thoại đã mua', maxlength: '15', autocomplete: 'off' });
  const btn = el('button', { type: 'button', class: 'primary' }, 'Nhận khóa');
  const msg = el('div', { class: 'muted', id: 'claim-msg', role: 'status' });
  btn.addEventListener('click', async () => {
    msg.textContent = '';
    if (!code.value.trim() || !phone.value.trim()) { msg.textContent = 'Nhập đủ mã đơn và số điện thoại đã dùng khi mua.'; return; }
    btn.disabled = true;
    try {
      const r = await window.vungBai.claimDevice({ code: code.value.toUpperCase().replace(/[^A-Z0-9]/g, '').replace(/^NL(?=[A-Z0-9]{6}$)/, ''), phone: phone.value.replace(/[\s.\-]/g, '') });
      if (r.ok && r.license && r.license.status === 'ok') {
        code.value = ''; phone.value = '';
        await refreshLicense();
        document.getElementById('license-msg').textContent = 'Đã nhận khóa cho thiết bị này.';
      } else if (r.ok) {
        msg.textContent = LICENSE_MESSAGES[r.license && r.license.status] || 'Không kích hoạt được khóa nhận về. Liên hệ Zalo 0968 646 853.';
      } else {
        msg.textContent = r.offline ? 'Cần kết nối mạng để nhận khóa. Hãy kiểm tra mạng rồi thử lại.' : (r.error || 'Không nhận được khóa.');
      }
    } catch {
      msg.textContent = 'Không nhận được khóa. Hãy thử lại.';
    } finally {
      btn.disabled = false;
    }
  });
  return el('div', { class: 'license-claim' },
    el('h3', {}, 'Đã mua ở thiết bị khác?'),
    el('div', { class: 'muted' }, 'Mỗi đơn dùng được cho 1 máy tính và 1 điện thoại. Nhập mã đơn và số điện thoại đã mua để nhận khóa cho thiết bị này (cần có mạng).'),
    el('div', { class: 'license-form' }, code, phone, btn),
    msg,
  );
}

function renderGrades() {
  const box = document.getElementById('grades');
  box.replaceChildren();
  for (const g of GRADES) {
    const btn = el('button', { class: 'grade-tile', type: 'button', 'aria-label': `Lớp ${g.grade}` });
    btn.append(
      el('span', { class: 'grade-word' }, 'Lớp'),
      el('span', { class: 'grade-num' }, String(g.grade)),
      el('span', { class: 'grade-note' }, `${g.available ? `${(GRADE_SUBJECTS[g.grade] || []).length} môn học` : 'Đang biên soạn'} · ${GRADE_PRICE[g.grade] || ''}`),
    );
    if (g.grade === 9) {
      btn.classList.add('grade-gift');
      btn.append(giftBadge(), el('span', { class: 'gift-note' }, 'Tặng bộ đề ôn thi chuyển cấp'));
    }
    if (g.available) btn.addEventListener('click', () => showSubjects(g.grade));
    else btn.disabled = true;
    box.append(btn);
  }
  // Ôn thi THPT: màn hình khung (chọn tổ hợp, khối thi); bài học và đề đang được biên soạn.
  const thpt = el('button', { class: 'grade-tile', type: 'button', 'aria-label': 'Ôn thi THPT' });
  thpt.append(
    el('span', { class: 'grade-word' }, 'Ôn thi'),
    el('span', { class: 'grade-num long' }, 'THPT'),
    el('span', { class: 'grade-note' }, 'Đang biên soạn · 555.000 đ'),
  );
  thpt.addEventListener('click', () => showThpt());
  box.append(thpt);
}

function showThpt() {
  document.getElementById('breadcrumb').textContent = '';
  window.ThptExam.open();
  showOnly('thpt');
  window.scrollTo(0, 0);
}

// Ôn thi và luyện đề (tặng kèm Lớp 9): chọn môn rồi làm đề thử vào lớp 10. Đề đang được biên soạn.
const EXAM_PREP_GRADE = 9;
const EXAM_PREP = [
  { name: 'Toán', note: 'Đang biên soạn' },
  { name: 'Ngữ văn', note: 'Đang biên soạn' },
  { name: 'Tiếng Anh', note: 'Đang biên soạn' },
  { name: 'Đề tổng hợp', note: 'Giống đề thi thật · đang biên soạn' },
];
function showExamPrep() {
  const box = document.getElementById('examprep-body');
  box.replaceChildren(
    el('button', { class: 'back-link', type: 'button' }, '← Chọn môn học'),
    el('header', { class: 'screen-head' },
      el('p', { class: 'screen-kicker' }, `Lớp ${EXAM_PREP_GRADE} · Tặng kèm`),
      el('h1', {}, 'Ôn thi và luyện đề'),
      el('p', { class: 'screen-sub' }, 'Bộ đề ôn thi chuyển cấp vào lớp 10. Chọn môn rồi làm đề; điểm và câu sai được lưu vào Sổ câu sai như các bài khác. Các đề đang được biên soạn và sẽ có trong phần mềm khi hoàn thành.')),
    el('div', { class: 'grades' }, ...EXAM_PREP.map((x) => {
      const b = el('button', { class: 'grade subject-btn', type: 'button', disabled: true }, x.name, el('small', {}, x.note));
      return b;
    })));
  box.querySelector('.back-link').addEventListener('click', () => showSubjects(EXAM_PREP_GRADE));
  showOnly('examprep');
  window.scrollTo(0, 0);
}

function showPurchase(preselect) {
  document.getElementById('breadcrumb').textContent = '';
  window.Purchase.open({ machineId: (lastLicense && lastLicense.machineId) || '', onActivated: () => refreshLicense(), preselect });
  showOnly('purchase');
}

function showAiWork() {
  document.getElementById('breadcrumb').textContent = '';
  window.AiWork.open({
    license: () => lastLicense,
    onBuy: (id) => { showPurchase(id); },
    onExit: () => showLaunch(),
  });
  showOnly('aiwork');
}

function showGiaSu() {
  document.getElementById('breadcrumb').textContent = '';
  window.GiaSuAi.open({
    license: () => lastLicense,
    onBuy: (id) => { showPurchase(id); },
    onExit: () => showLaunch(),
  });
  showOnly('giasu');
}

function showTuDuy() {
  document.getElementById('breadcrumb').textContent = '';
  window.TuDuy.open({
    license: () => lastLicense,
    onBuy: (id) => { showPurchase(id); },
    onExit: () => showLaunch(),
  });
  showOnly('tuduy');
}

function showNational() {
  document.getElementById('breadcrumb').textContent = '';
  window.National.open();
  showOnly('national');
  window.scrollTo(0, 0);
}

/* Thời khóa biểu: khung nhắc học bài và thẻ nhập thời khóa biểu theo lớp. */
function ttOpen(grade, base) {
  const subject = (GRADE_SUBJECTS[grade] || []).find((x) => x.replace(/\d+$/, '') === base);
  if (subject) { currentGrade = grade; renderHome(manifestCache[subject], subject); }
}
function ttBanner(slotId, grades) {
  const T = window.VungTimetable; const slot = document.getElementById(slotId);
  if (!T || !slot) return;
  T.banner(slot, { grades, names: SUBJECT_BASE, open: ttOpen });
}
function ttSyncNotifications() { if (window.VungTimetable) window.VungTimetable.sync(SUBJECT_BASE); }

function showLaunch() {
  ttBanner('tt-banner-launch', GRADES.map((g) => g.grade));
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
  if (window.VungProgressUI) {
    window.VungProgressUI.scope = grade;
    document.getElementById('open-report-grade').textContent = `Báo cáo lớp ${grade}`;
    window.VungProgressUI.refreshBadge();
  }
  document.getElementById('breadcrumb').textContent = '';
  ttBanner('tt-banner', [grade]);
  if (window.VungTimetable) {
    window.VungTimetable.editor(document.getElementById('tt-card'), {
      grade,
      subjects: (GRADE_SUBJECTS[grade] || []).map((x) => ({ id: x.replace(/\d+$/, ''), name: SUBJECT_LABELS[x] })),
      onSaved: () => ttBanner('tt-banner', [grade]),
    });
  }
  const box = document.getElementById('subject-list');
  box.replaceChildren();
  for (const subject of GRADE_SUBJECTS[grade] || []) {
    const btn = el('button', { class: 'grade subject-btn', type: 'button' }, SUBJECT_LABELS[subject]);
    btn.addEventListener('click', () => renderHome(manifestCache[subject], subject));
    box.append(btn);
  }
  if (grade === EXAM_PREP_GRADE) {
    const ex = el('button', { class: 'exam-entry', type: 'button' },
      el('span', { class: 'exam-title' }, 'Ôn thi và luyện đề'),
      el('span', { class: 'exam-sub' }, 'Bộ đề ôn thi chuyển cấp vào lớp 10'),
      giftBadge());
    ex.addEventListener('click', () => showExamPrep());
    box.append(ex);
  }
  showOnly('subjects');
}

// Thanh thông báo cập nhật: luôn hỏi trước khi tải và trước khi cài.
function setupUpdateBar() {
  const bar = document.getElementById('update-bar');
  if (!bar || !window.vungBai.onUpdate) return;
  let dismissed = '';
  let manual = false;
  /* Android: gói giao diện mới tải xong thì tự khởi động lại, nhưng chỉ khi con không đang làm bài (đang ở màn hình chính/chọn môn). */
  const auto = window.vungBai.platform === 'android';
  const safe = () => ['launch', 'subjects', 'home'].some((id) => { const e = document.getElementById(id); return e && !e.hidden; });
  let autoOff = ''; let autoTimer = null; let waitTimer = null;
  const btn = (label, fn, cls) => {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = label; if (cls) b.className = cls; b.addEventListener('click', fn);
    return b;
  };
  const render = (st) => {
    bar.replaceChildren();
    const msg = document.createElement('span');
    let acts = [];
    let notes = null;
    if (st.state === 'available' && dismissed !== st.version) {
      msg.textContent = `Có phiên bản mới ${st.version}.${st.error ? ' ' + st.error : ''}`;
      acts = [btn('Tải về', () => window.vungBai.downloadUpdate()), btn('Để sau', () => { dismissed = st.version; render({ state: 'none' }); }, 'ghost')];
      if (st.notes) {
        const ul = document.createElement('ul'); ul.className = 'update-notes';
        for (const line of st.notes.split('\n')) { const t = line.replace(/^\s*[-*•]\s*/, '').trim(); if (t) { const li = document.createElement('li'); li.textContent = t; ul.append(li); } }
        notes = ul;
      }
    } else if (st.state === 'checking' && manual) {
      msg.textContent = 'Đang kiểm tra bản mới…';
    } else if ((st.state === 'none' || st.state === 'error') && manual) {
      // Giữ thông báo cho đến khi bấm Đóng: trên Android trạng thái được báo hai lần liên tiếp (sự kiện rồi kết quả), nếu xóa cờ ngay thì thông báo biến mất tức thì.
      msg.textContent = st.state === 'none' ? 'Bạn đang dùng phiên bản mới nhất.' : 'Chưa kiểm tra được (không có mạng?).';
      acts = [btn('Đóng', () => { manual = false; bar.hidden = true; }, 'ghost')];
    } else if (st.state === 'downloading') {
      manual = false;
      msg.textContent = `Đang tải bản mới… ${st.percent || 0}%`;
    } else if (st.state === 'ready' && auto && autoOff !== st.version && safe()) {
      clearTimeout(autoTimer); clearInterval(waitTimer);
      msg.textContent = `Đã có giao diện mới ${st.version}. Đang tự khởi động lại…`;
      acts = [btn('Để sau', () => { autoOff = st.version; clearTimeout(autoTimer); bar.hidden = true; }, 'ghost')];
      autoTimer = setTimeout(() => { if (autoOff !== st.version && safe()) window.vungBai.installUpdate(); else render(st); }, 3000);
    } else if (st.state === 'ready') {
      msg.textContent = `Đã tải xong phiên bản ${st.version}.`;
      if (auto && autoOff !== st.version) { clearInterval(waitTimer); waitTimer = setInterval(() => { if (safe()) { clearInterval(waitTimer); render(st); } }, 4000); } // đang làm bài: chờ con về màn hình chính rồi mới tự cài
      acts = [btn('Khởi động lại để cài', () => window.vungBai.installUpdate()), btn('Để sau', () => { bar.hidden = true; }, 'ghost')];
    } else { bar.hidden = true; return; }
    const head = document.createElement('div'); head.className = 'update-head'; head.append(msg, ...acts);
    bar.append(head); if (notes) bar.append(notes);
    bar.hidden = false;
  };
  window.vungBai.onUpdate(render);
  window.vungBai.updateStatus().then(render).catch(() => {});
  // Bấm vào dòng phiên bản ở góc màn hình để kiểm tra ngay.
  const ver = document.getElementById('build');
  if (ver) {
    ver.title = 'Bấm để kiểm tra bản mới';
    ver.addEventListener('click', () => { manual = true; dismissed = ''; render({ state: 'checking' }); window.vungBai.checkUpdate().then(render).catch(() => {}); });
  }
}

async function init() {
  try { setupUpdateBar(); } catch { /* cập nhật là phụ, không chặn app */ }
  try {
    const info = await window.vungBai.appInfo();
    document.getElementById('build').textContent = `Phiên bản ${info.version}`;
  } catch {
    // Không hiện số phiên bản nếu không đọc được; không ảnh hưởng luồng chính.
  }
  try {
    const product = await window.vungBai.productInfo();
    applyProduct(product);
    document.title = product.title;
    document.getElementById('brand').textContent = product.title;
    currentGrade = GRADES[0].grade;
    for (const subject of Object.keys(SUBJECT_LABELS)) {
      manifestCache[subject] = await window.vungBai.loadManifest(subject);
    }
    document.getElementById('btn-back').addEventListener('click', () => {
      document.getElementById('breadcrumb').textContent = '';
      showOnly('home');
    });
    document.getElementById('btn-grades').addEventListener('click', () => showLaunch());
    document.getElementById('btn-national-back').addEventListener('click', () => showLaunch());
    document.getElementById('btn-thpt-back').addEventListener('click', () => showLaunch());
    document.getElementById('open-national').addEventListener('click', () => showNational());
    document.getElementById('open-aiwork').addEventListener('click', () => showAiWork());
    document.getElementById('open-giasu').addEventListener('click', () => showGiaSu());
    document.getElementById('open-tuduy').addEventListener('click', () => showTuDuy());
    const openProg = async (kind, grade) => {
      const ui = window.VungProgressUI;
      if (kind === 'report' && window.VungPinUI && !(await window.VungPinUI.ensureUnlocked())) return;
      ui.scope = grade;
      if (kind === 'review') ui.renderReview(document.getElementById('review-body'), grade);
      else ui.renderReport(document.getElementById('report-body'), grade);
      showOnly(kind);
    };
    const backProg = () => (window.VungProgressUI.scope ? showSubjects(window.VungProgressUI.scope) : showLaunch());
    document.getElementById('open-review').addEventListener('click', () => openProg('review', 0));
    document.getElementById('open-report').addEventListener('click', () => openProg('report', 0));
    document.getElementById('open-review-grade').addEventListener('click', () => openProg('review', currentGrade));
    document.getElementById('open-report-grade').addEventListener('click', () => openProg('report', currentGrade));
    // Màn hình phụ huynh xem kết quả học do máy tính gửi lên (chỉ có trên điện thoại).
    const openParent = document.getElementById('open-parent-view');
    if (window.vungBai.platform === 'android' && window.vungBai.progressView) {
      openParent.hidden = false;
      openParent.addEventListener('click', async () => {
        if (window.VungPinUI && !(await window.VungPinUI.ensureUnlocked())) return;
        window.VungProgressUI.renderParentView(document.getElementById('parent-body'));
        showOnly('parent-view');
      });
      document.getElementById('btn-parent-back').addEventListener('click', () => showLaunch());
    }
    document.getElementById('btn-review-back').addEventListener('click', backProg);
    document.getElementById('btn-report-back').addEventListener('click', backProg);
    document.getElementById('open-purchase').addEventListener('click', () => showPurchase());
    document.getElementById('btn-purchase-back').addEventListener('click', () => showLaunch());
    renderGrades();
    if (window.VungProgressUI) window.VungProgressUI.refreshBadge();
    await refreshLicense();
    startFamilySync();
    try { ttSyncNotifications(); } catch { /* nhắc trên điện thoại là phụ */ }
    showLaunch();
  } catch (err) {
    console.error(err);
    document.getElementById('empty').replaceChildren(el('p', {}, 'Không tải được nội dung bài học. Hãy cài lại phần mềm hoặc liên hệ Nam Linh: 0968 646 853.'));
    showOnly('empty');
  }
}

init();
