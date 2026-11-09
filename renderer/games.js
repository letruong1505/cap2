// Giao diện trò chơi: menu theo môn, bốn trò chơi, và chuỗi ngày học.
// Logic chọn câu và chấm đúng/sai nằm trong games-logic.js. File này chỉ dựng giao diện.
// Toàn bộ nằm trong IIFE để không trùng tên với app.js.
(function () {
  'use strict';

  const L = window.VungGamesLogic;
  const STORE_KEY = 'vungbai.games.v1';
  const QUICK_SECONDS = 60;
  const QUICK_FEEDBACK_MS = 700;
  const QUIZ_SIZE = 10;
  const PAIRS_PER_ROUND = 6;
  const PAIR_MISS_MS = 600;
  const MIN_QUICK = 5;
  const MIN_QUIZ = 5;
  const MIN_PAIRS = 4;

  let ctx = null;          // { subject, label, kicker, manifest, onBack }
  let menuToken = 0;       // chặn kết quả tải cũ ghi đè màn hình mới
  let cleanups = [];       // hàm dọn khi rời khỏi trò chơi (dừng đồng hồ, huỷ hẹn giờ)
  const poolCache = new Map();

  const el = (tag, attrs = {}, ...children) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'class') node.className = v;
      else node.setAttribute(k, v);
    }
    for (const c of children) {
      if (c === undefined || c === null || c === false) continue;
      node.append(c instanceof Node ? c : String(c));
    }
    return node;
  };

  function show(id) {
    for (const p of document.querySelectorAll('#app > .panel')) p.hidden = p.id !== id;
  }

  function addCleanup(fn) { cleanups.push(fn); }
  function runCleanups() {
    for (const fn of cleanups) {
      try { fn(); } catch { /* bỏ qua lỗi khi dọn */ }
    }
    cleanups = [];
  }
  function addTimeout(fn, ms) {
    const id = setTimeout(fn, ms);
    addCleanup(() => clearTimeout(id));
    return id;
  }

  // Lưu cục bộ trên máy: chuỗi ngày học và điểm cao nhất. Không gửi đi đâu.
  function loadStore() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; } catch { return {}; }
  }
  function saveStore(store) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch { /* không ghi được thì bỏ qua */ }
  }
  function bestOf(gameId) {
    const bests = loadStore().bests || {};
    return bests[`${gameId}:${ctx.subject}`];
  }
  function saveBest(gameId, score) {
    const store = loadStore();
    store.bests = L.updateBest(store.bests, gameId, ctx.subject, score);
    saveStore(store);
  }

  // Gọi từ app.js khi học sinh nộp bài luyện tập: tính một ngày học.
  function recordStudy() {
    const store = loadStore();
    store.streak = L.recordStudy(store.streak, new Date());
    saveStore(store);
  }

  // Các bài đã mở khoá của môn (đúng với mục lục đã cập nhật bản quyền).
  function unlockedFiles(manifest, subject) {
    const files = [];
    for (const book of manifest.books || []) {
      for (const c of book.chapters || []) {
        for (const l of c.lessons || []) {
          if (l.file && !l.locked) files.push(subject + '/' + l.file);
        }
      }
    }
    return files;
  }

  // Nạp các bài đã mở và gom câu hợp lệ. Kết quả được cache theo danh sách bài.
  function loadPool(subject, manifest) {
    const files = unlockedFiles(manifest, subject);
    const key = files.join('|');
    if (!poolCache.has(key)) {
      const loads = files.map((p) => window.vungBai.loadLesson(p).catch(() => null));
      poolCache.set(key, Promise.all(loads).then((lessons) => L.collectPool(lessons)));
    }
    return poolCache.get(key);
  }

  function correctText(item) {
    return item.type === 'mcq' ? item.choices[item.answer] : L.viNumber(item.answer);
  }

  // Lời giải sau mỗi câu, cùng kiểu với bài học: nêu lý do nếu chọn phương án sai.
  function feedbackText(item, correct, pickedIndex) {
    const explain = item.explain || '';
    if (correct) return `Đúng. ${explain}`;
    const note = item.type === 'mcq' && pickedIndex !== undefined
      ? (item.wrong_explain || {})[String(pickedIndex)]
      : null;
    return `${note ? note + ' ' : ''}Đáp án đúng: ${correctText(item)}. Lời giải: ${explain}`;
  }

  // Một câu hỏi: trắc nghiệm (bấm chọn) hoặc điền (gõ rồi Enter). Trả về phần tử DOM.
  // onResult(correct) được gọi đúng một lần; onNext() được gọi khi học sinh bấm tiếp.
  function questionView(item, { onResult, onNext, nextLabel = 'Câu tiếp', autoNextOnCorrect = false }) {
    let done = false;
    let advanced = false;
    const advance = () => {
      if (advanced) return;
      advanced = true;
      onNext();
    };

    const wrap = el('div', { class: 'game-question' });
    wrap.append(el('div', { class: 'stem' }, item.stem));
    const feedback = el('div', { class: 'feedback', hidden: 'hidden' });

    const reveal = (correct, text) => {
      done = true;
      feedback.hidden = false;
      feedback.className = 'feedback ' + (correct ? 'ok' : 'bad');
      feedback.textContent = text;
      const nextBtn = el('button', { class: 'primary game-next', type: 'button' }, nextLabel);
      nextBtn.addEventListener('click', advance);
      wrap.append(nextBtn);
      if (autoNextOnCorrect && correct) addTimeout(advance, QUICK_FEEDBACK_MS);
    };

    if (item.type === 'mcq') {
      const grid = el('div', { class: 'quiz-choices' });
      const buttons = [];
      for (const orig of L.shuffle(item.choices.map((_, k) => k))) {
        const btn = el('button', { class: 'quiz-choice', type: 'button' }, item.choices[orig]);
        btn.addEventListener('click', () => {
          if (done) return;
          const correct = L.isChoiceCorrect(item, orig);
          for (const b of buttons) {
            b.btn.disabled = true;
            if (b.idx === item.answer) b.btn.classList.add('is-right');
            else if (b.idx === orig) b.btn.classList.add('is-wrong');
          }
          onResult(correct);
          reveal(correct, feedbackText(item, correct, orig));
        });
        buttons.push({ btn, idx: orig });
        grid.append(btn);
      }
      wrap.append(grid);
    } else {
      const input = el('input', {
        type: 'text',
        'aria-label': 'Đáp án',
        placeholder: 'Ví dụ: 3/4 hoặc 0,75',
        autocomplete: 'off',
        spellcheck: 'false',
      });
      const submit = el('button', { class: 'primary', type: 'button' }, 'Trả lời');
      const hint = el('p', { class: 'game-hint', 'aria-live': 'polite' });
      const check = () => {
        if (done) return;
        const r = L.checkFill(item, input.value);
        if (!r.valid) {
          hint.textContent = 'Nhập đúng định dạng, ví dụ 3/4 hoặc 0,75. Câu này chưa được tính.';
          input.focus();
          return;
        }
        hint.textContent = '';
        input.disabled = true;
        submit.disabled = true;
        onResult(r.correct);
        reveal(r.correct, feedbackText(item, r.correct));
      };
      submit.addEventListener('click', check);
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          check();
        }
      });
      wrap.append(el('div', { class: 'game-input-row' }, input, submit), hint);
      addTimeout(() => input.focus(), 0);
    }
    wrap.append(feedback);
    return wrap;
  }

  function backLink(label, onClick) {
    const btn = el('button', { class: 'back-link', type: 'button' }, label);
    btn.addEventListener('click', onClick);
    return btn;
  }

  // Khung một trò chơi: tiêu đề, nút quay lại menu, vùng nội dung.
  function gameScreen(title) {
    runCleanups();
    const root = document.getElementById('game');
    const body = el('div', { class: 'game-body' });
    root.replaceChildren(
      backLink('← Trò chơi', () => showMenu()),
      el('header', { class: 'screen-head' },
        el('p', { class: 'screen-kicker' }, ctx.label),
        el('h1', {}, title)),
      body,
    );
    show('game');
    window.scrollTo(0, 0);
    return body;
  }

  // ---------- Đua 60 giây ----------
  function playQuick(pool) {
    const body = gameScreen('Đua 60 giây');
    const timeLabel = el('span', { class: 'timer' }, `${QUICK_SECONDS} giây`);
    const scoreLabel = el('span', { class: 'game-score' }, 'Đúng 0');
    const stage = el('div', { class: 'game-stage' });
    body.append(el('div', { class: 'game-hud' }, timeLabel, scoreLabel), stage);

    let deck = [];
    let deckPos = 0;
    let correct = 0;
    let answered = 0;
    let endAt = 0;
    let finished = false;
    let timerId = null;

    function tick() {
      const left = Math.max(0, Math.ceil((endAt - Date.now()) / 1000));
      timeLabel.textContent = `${left} giây`;
      if (left === 0 && !finished) finish();
    }

    function nextQuestion() {
      if (finished) return;
      if (deckPos >= deck.length) {
        deck = L.shuffle(pool);
        deckPos = 0;
      }
      const item = deck[deckPos++];
      stage.replaceChildren(questionView(item, {
        autoNextOnCorrect: true,
        onResult: (ok) => {
          answered += 1;
          if (ok) correct += 1;
          scoreLabel.textContent = `Đúng ${correct}`;
        },
        onNext: () => { if (!finished) nextQuestion(); },
      }));
    }

    function begin() {
      endAt = Date.now() + QUICK_SECONDS * 1000;
      deck = L.shuffle(pool);
      deckPos = 0;
      timerId = setInterval(tick, 200);
      addCleanup(() => clearInterval(timerId));
      tick();
      nextQuestion();
    }

    function finish() {
      finished = true;
      clearInterval(timerId);
      timeLabel.textContent = '0 giây';
      saveBest('quick', correct);
      const again = el('button', { class: 'primary', type: 'button' }, 'Chơi lại');
      again.addEventListener('click', () => playQuick(pool));
      const back = el('button', { class: 'back-link', type: 'button' }, 'Về trò chơi');
      back.addEventListener('click', () => showMenu());
      stage.replaceChildren(
        el('p', { class: 'game-result' },
          'Hết giờ. Bạn trả lời đúng ', el('b', {}, `${correct}/${answered}`), ' câu.'),
        el('div', { class: 'game-actions' }, again, back),
      );
    }

    const start = el('button', { class: 'primary', type: 'button' }, 'Bắt đầu');
    start.addEventListener('click', () => {
      start.remove();
      begin();
    });
    stage.append(
      el('p', {}, `Trả lời được nhiều câu nhất trong ${QUICK_SECONDS} giây. Câu đúng được chuyển ngay sang câu tiếp.`),
      start,
    );
  }

  // ---------- Trắc nghiệm nhanh ----------
  function playQuiz(pool) {
    const mcqs = L.pickQuestions(pool.filter((i) => i.type === 'mcq'), QUIZ_SIZE);
    const body = gameScreen('Trắc nghiệm nhanh');
    const progress = el('p', { class: 'meta' });
    const stage = el('div', { class: 'game-stage' });
    body.append(progress, stage);

    let pos = 0;
    let correct = 0;
    const wrong = [];

    function showStep() {
      progress.textContent = `Câu ${pos + 1}/${mcqs.length} · Đúng ${correct}`;
      const item = mcqs[pos];
      const last = pos === mcqs.length - 1;
      stage.replaceChildren(questionView(item, {
        nextLabel: last ? 'Xem kết quả' : 'Câu tiếp',
        onResult: (ok) => {
          if (ok) correct += 1;
          else wrong.push({ stem: item.stem, answer: correctText(item) });
        },
        onNext: () => {
          pos += 1;
          if (pos < mcqs.length) showStep();
          else showResult();
        },
      }));
    }

    function showResult() {
      saveBest('quiz', correct);
      progress.textContent = `Hoàn thành ${mcqs.length} câu`;
      const again = el('button', { class: 'primary', type: 'button' }, 'Chơi lại');
      again.addEventListener('click', () => playQuiz(pool));
      const back = el('button', { class: 'back-link', type: 'button' }, 'Về trò chơi');
      back.addEventListener('click', () => showMenu());
      const children = [
        el('p', { class: 'game-result' }, 'Bạn đúng ', el('b', {}, `${correct}/${mcqs.length}`), ' câu.'),
      ];
      if (wrong.length > 0) {
        const list = el('ul', { class: 'wrong-list' });
        for (const w of wrong) list.append(el('li', {}, `${w.stem} Đáp án đúng: ${w.answer}`));
        children.push(el('p', { class: 'meta' }, 'Các câu cần xem lại:'), list);
      }
      children.push(el('div', { class: 'game-actions' }, again, back));
      stage.replaceChildren(...children);
    }

    showStep();
  }

  // ---------- Ghép phép tính ----------
  function playPairs(pool) {
    const body = gameScreen('Ghép phép tính');
    const status = el('p', { class: 'game-status', 'aria-live': 'polite' },
      'Chọn một phép tính bên trái, rồi chọn kết quả đúng bên phải.');
    const stage = el('div', { class: 'game-stage' });
    body.append(stage, status);

    let rounds = 0;

    function startRound() {
      const pairs = L.buildPairs(pool, PAIRS_PER_ROUND);
      if (pairs.length < MIN_PAIRS) {
        stage.replaceChildren(el('p', {}, 'Chưa đủ phép tính để ghép trong các bài đã mở.'));
        status.textContent = '';
        return;
      }
      let selected = null;
      let matched = 0;
      let roundMistakes = 0;
      const grid = el('div', { class: 'pair-grid' });
      const leftCol = el('div', { class: 'pair-col' }, el('p', { class: 'pair-head' }, 'Phép tính'));
      const rightCol = el('div', { class: 'pair-col' }, el('p', { class: 'pair-head' }, 'Kết quả'));

      const lefts = pairs.map((p) => ({ p, btn: el('button', { class: 'pair-btn', type: 'button', 'data-key': p.key }, p.left) }));
      const rights = L.shuffle(pairs).map((p) => ({ p, btn: el('button', { class: 'pair-btn', type: 'button', 'data-key': p.key }, p.right) }));

      const clearSelection = () => {
        if (selected) selected.btn.classList.remove('selected');
        selected = null;
      };

      for (const { p, btn } of lefts) {
        btn.addEventListener('click', () => {
          if (btn.disabled) return;
          clearSelection();
          selected = { p, btn };
          btn.classList.add('selected');
          status.textContent = `Chọn kết quả cho: ${p.left}`;
        });
        leftCol.append(btn);
      }

      for (const { p, btn } of rights) {
        btn.addEventListener('click', () => {
          if (btn.disabled) return;
          if (!selected) {
            status.textContent = 'Hãy chọn một phép tính bên trái trước.';
            return;
          }
          const pick = selected;
          if (pick.p.key === p.key) {
            pick.btn.classList.remove('selected');
            pick.btn.classList.add('matched');
            pick.btn.disabled = true;
            btn.classList.add('matched');
            btn.disabled = true;
            selected = null;
            matched += 1;
            status.textContent = `Đúng: ${p.equation}`;
            if (matched === pairs.length) finishRound();
          } else {
            roundMistakes += 1;
            btn.classList.add('miss');
            pick.btn.classList.add('miss');
            status.textContent = 'Chưa khớp. Chọn lại nhé.';
            const pickBtn = pick.btn;
            clearSelection();
            addTimeout(() => {
              btn.classList.remove('miss');
              pickBtn.classList.remove('miss');
            }, PAIR_MISS_MS);
          }
        });
        rightCol.append(btn);
      }

      grid.append(leftCol, rightCol);
      stage.replaceChildren(grid);

      function finishRound() {
        rounds += 1;
        saveBest('pairs', rounds);
        status.textContent = `Hoàn thành vòng! Số lần chọn sai trong vòng: ${roundMistakes}.`;
        const next = el('button', { class: 'primary', type: 'button' }, 'Vòng mới');
        next.addEventListener('click', startRound);
        stage.append(el('div', { class: 'game-actions' }, next));
      }
    }

    startRound();
  }

  // ---------- Chuỗi ngày học ----------
  function showStreak() {
    const body = gameScreen('Chuỗi ngày học');
    const store = loadStore();
    const streak = L.normalizeStreak(store.streak);
    const now = new Date();
    const count = L.currentStreak(store.streak, now);
    const doneToday = streak.last === L.dayKey(now);

    body.append(streakSummary(count, doneToday, streak.best));
    body.append(el('h2', {}, 'Huy hiệu'));
    const list = el('div', { class: 'badge-list' });
    for (const b of L.badgesFor(count)) {
      list.append(el('div', { class: 'badge' + (b.earned ? ' earned' : '') },
        el('b', {}, `${b.days} ngày`),
        el('span', {}, b.earned ? b.name : `${b.name} · còn ${b.days - count} ngày`)));
    }
    body.append(list);
    body.append(el('p', { class: 'meta' }, 'Chuỗi được tính khi bạn nộp bài luyện tập (nút "Kiểm tra toàn bài"). Trò chơi không tính vào chuỗi.'));
  }

  function streakSummary(count, doneToday, best) {
    return el('div', { class: 'streak-card' },
      el('div', { class: 'streak-num' }, String(count)),
      el('div', {},
        el('p', { class: 'streak-label' }, 'ngày học liên tiếp'),
        el('p', { class: 'meta' }, doneToday
          ? `Hôm nay bạn đã nộp bài luyện tập. Kỷ lục: ${best} ngày.`
          : `Hôm nay chưa có bài nào. Nộp một bài luyện tập để giữ chuỗi. Kỷ lục: ${best} ngày.`)));
  }

  // ---------- Menu trò chơi của một môn ----------
  async function showMenu() {
    runCleanups();
    const token = ++menuToken;
    const games = document.getElementById('games');
    games.replaceChildren(
      backLink('← Chọn bài học', () => ctx.onBack()),
      el('header', { class: 'screen-head' },
        el('p', { class: 'screen-kicker' }, ctx.kicker || ''),
        el('h1', {}, 'Trò chơi'),
        el('p', { class: 'screen-sub' }, `Môn ${ctx.label}. Câu hỏi lấy từ các bài bạn đã mở, nên luôn đúng với sách.`)),
      streakSummary(L.currentStreak(loadStore().streak, new Date()),
        L.normalizeStreak(loadStore().streak).last === L.dayKey(new Date()),
        L.normalizeStreak(loadStore().streak).best),
      el('p', { class: 'meta', id: 'games-loading' }, 'Đang chuẩn bị câu hỏi…'),
    );
    show('games');

    let pool = [];
    try {
      pool = await loadPool(ctx.subject, ctx.manifest);
    } catch (err) {
      console.error(err);
    }
    if (token !== menuToken) return;

    games.querySelector('#games-loading').remove();
    games.append(gameCards(pool));
  }

  function gameCards(pool) {
    const mcqCount = pool.filter((i) => i.type === 'mcq').length;
    const pairsReady = L.buildPairs(pool, PAIRS_PER_ROUND).length >= MIN_PAIRS;
    const defs = [
      {
        id: 'quick',
        name: 'Đua 60 giây',
        desc: 'Trả lời được nhiều câu nhất trong 60 giây. Mỗi câu đúng được 1 điểm.',
        ok: pool.length >= MIN_QUICK,
        need: `Cần ít nhất ${MIN_QUICK} câu từ các bài đã mở.`,
        best: (b) => `Kỷ lục: ${b} câu đúng`,
        play: () => playQuick(pool),
      },
      {
        id: 'quiz',
        name: 'Trắc nghiệm nhanh',
        desc: `${QUIZ_SIZE} câu chọn đáp án, có giải thích ngay sau mỗi câu.`,
        ok: mcqCount >= MIN_QUIZ,
        need: `Cần ít nhất ${MIN_QUIZ} câu trắc nghiệm từ các bài đã mở.`,
        best: (b) => `Kỷ lục: ${b}/${QUIZ_SIZE} câu đúng`,
        play: () => playQuiz(pool),
      },
      {
        id: 'pairs',
        name: 'Ghép phép tính',
        desc: 'Ghép mỗi phép tính với kết quả đúng. Chỉ có ở môn có phép tính.',
        ok: pairsReady,
        need: 'Môn này chưa có đủ phép tính để ghép.',
        best: (b) => `Kỷ lục: ${b} vòng hoàn thành trong một lượt`,
        play: () => playPairs(pool),
      },
      {
        id: 'streak',
        name: 'Chuỗi ngày học',
        desc: 'Xem chuỗi ngày học liên tiếp và các huy hiệu bạn đã mở.',
        ok: true,
        need: '',
        best: () => '',
        play: () => showStreak(),
      },
    ];

    const grid = el('div', { class: 'game-cards' });
    for (const d of defs) {
      const best = d.id === 'streak' ? undefined : bestOf(d.id);
      const status = !d.ok ? d.need : (best !== undefined ? d.best(best) : 'Chưa chơi');
      const card = el('button', { class: 'game-card' + (d.ok ? '' : ' unavailable'), type: 'button' },
        el('h3', {}, d.name),
        el('p', { class: 'game-desc' }, d.desc),
        el('p', { class: 'game-status-line' }, status));
      if (d.ok) card.addEventListener('click', d.play);
      else card.disabled = true;
      grid.append(card);
    }
    return grid;
  }

  // Mở menu trò chơi của một môn. options: { subject, label, kicker, manifest, onBack }.
  function open(options) {
    ctx = options;
    runCleanups();
    showMenu();
  }

  window.VungGames = { open, recordStudy };
})();
