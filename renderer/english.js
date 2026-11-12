// Tiếng Anh: từ vựng có phát âm, ô chữ kiểu "Đường lên đỉnh Olympia" và phần viết tự kiểm tra (không dùng AI).
// Phần logic thuần (layout, keyword, rowScore, validate) dùng chung cho kiểm thử và bộ kiểm tra nội dung.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NL_ENGLISH = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const norm = (s) => String(s == null ? '' : s).toLowerCase().replace(/[^a-z]/g, '');

  // Xếp các từ sao cho chữ cái thứ keyIndex của mỗi từ nằm cùng một cột (cột từ khóa).
  function layout(words) {
    const maxKey = Math.max(...words.map((w) => w.keyIndex));
    const rows = words.map((w) => {
      const letters = norm(w.answer).split('');
      return { letters, offset: maxKey - w.keyIndex, keyIndex: w.keyIndex };
    });
    return { rows, keyCol: maxKey, width: Math.max(...rows.map((r) => r.offset + r.letters.length)) };
  }
  const keyword = (words) => words.map((w) => norm(w.answer)[w.keyIndex]).join('');
  // Mỗi hàng 10 điểm; mỗi gợi ý trừ 3, mỗi lần trả lời sai trừ 1; tối thiểu 2 điểm.
  const rowScore = ({ hints = 0, wrong = 0 }) => Math.max(2, 10 - 3 * hints - wrong);

  function validate(cw) {
    const errs = [];
    if (!cw || !Array.isArray(cw.words) || cw.words.length < 4) return ['ô chữ cần ít nhất 4 từ'];
    const ids = new Set();
    cw.words.forEach((w, i) => {
      const t = `ô chữ, từ ${i + 1}`;
      const a = norm(w.answer);
      if (!a) errs.push(`${t}: thiếu đáp án`);
      if (ids.has(a)) errs.push(`${t}: trùng từ "${a}"`);
      ids.add(a);
      if (!Number.isInteger(w.keyIndex) || w.keyIndex < 0 || w.keyIndex >= a.length) errs.push(`${t}: keyIndex nằm ngoài từ`);
      if (!w.clueVi) errs.push(`${t}: thiếu gợi ý tiếng Việt`);
      if (!w.clueEn) errs.push(`${t}: thiếu gợi ý tiếng Anh`);
    });
    if (!errs.length && keyword(cw.words) !== norm(cw.keyword)) errs.push(`ô chữ: các ô tô màu ghép thành "${keyword(cw.words)}", không khớp từ khóa "${cw.keyword}"`);
    return errs;
  }

  if (typeof document === 'undefined') return { norm, layout, keyword, rowScore, validate };

  // ---- Phần giao diện ----
  function h(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') n.className = v;
      else if (v === true) n.setAttribute(k, '');
      else if (v !== false && v != null) n.setAttribute(k, v);
    }
    for (const k of kids) n.append(k);
    return n;
  }

  function speak(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US';
    u.rate = 0.85;
    const v = window.speechSynthesis.getVoices().find((x) => /^en[-_]/i.test(x.lang));
    if (v) u.voice = v;
    window.speechSynthesis.speak(u);
  }

  function renderVocab(box, vocab) {
    box.replaceChildren(h('h2', {}, 'Từ vựng'));
    const canSpeak = 'speechSynthesis' in window;
    box.append(h('p', { class: 'screen-sub' }, canSpeak ? 'Bấm vào loa để nghe phát âm.' : 'Máy này chưa có giọng đọc tiếng Anh nên chưa nghe được phát âm.'));
    const grid = h('div', { class: 'vocab-grid' });
    for (const v of vocab) {
      const card = h('div', { class: 'vocab-card' });
      const top = h('div', { class: 'vocab-top' }, h('b', {}, v.w), h('span', { class: 'vocab-pos' }, `(${v.pos})`));
      if (canSpeak) {
        const b = h('button', { type: 'button', class: 'vocab-speak', 'aria-label': `Nghe từ ${v.w}`, title: 'Nghe' }, '🔊');
        b.addEventListener('click', () => speak(v.w));
        top.append(b);
      }
      card.append(top, h('div', { class: 'vocab-vi' }, v.vi));
      grid.append(card);
    }
    box.append(grid);
  }

  function renderReading(box, reading) {
    box.replaceChildren(h('h2', {}, 'Đọc hiểu'), h('h3', { class: 'reading-title' }, reading.title));
    for (const p of reading.paragraphs) box.append(h('p', { class: 'reading-text', lang: 'en' }, p));
    box.append(h('p', { class: 'screen-sub' }, 'Đọc xong, trả lời các câu hỏi đọc hiểu trong phần Luyện tập bên dưới.'));
  }

  let timerId = null;

  function mountCrossword(box, cw) {
    if (timerId) { clearInterval(timerId); timerId = null; }
    const L = layout(cw.words);
    const secs = cw.seconds || 240;
    const st = {
      started: false, over: false, left: secs, active: 0, score: 0, msg: '',
      rows: cw.words.map(() => ({ open: false, hints: 0, wrong: 0, firstLetter: false })),
    };
    const stop = () => { if (timerId) { clearInterval(timerId); timerId = null; } };
    const finish = (why) => { st.over = true; stop(); st.msg = why; draw(); };

    function draw() {
      box.replaceChildren(h('h2', {}, 'Ô chữ từ vựng'));
      box.append(h('p', { class: 'screen-sub' },
        `Mỗi hàng là một từ chủ đề “${cw.theme}”. Các ô đỏ ở cột dọc ghép lại thành một từ khóa. Gợi ý càng nhiều thì điểm càng ít.`));
      const bar = h('div', { class: 'cw-bar' });
      bar.append(h('span', {}, `Điểm: ${st.score}`), h('span', { class: 'cw-time' }, st.started && !st.over ? `Còn ${st.left} giây` : `${secs} giây`));
      box.append(bar);

      if (!st.started) {
        const go = h('button', { type: 'button', class: 'primary' }, 'Bắt đầu chơi');
        go.addEventListener('click', () => {
          st.started = true;
          timerId = setInterval(() => {
            if (!box.isConnected) { stop(); return; }
            st.left -= 1;
            const t = box.querySelector('.cw-time');
            if (t) t.textContent = `Còn ${st.left} giây`;
            if (st.left <= 0) { st.rows.forEach((r) => { r.open = true; }); finish('Hết giờ! Các từ còn lại đã được mở.'); }
          }, 1000);
          draw();
        });
        box.append(go);
        return;
      }

      const grid = h('div', { class: 'cw-grid' });
      L.rows.forEach((r, i) => {
        const line = h('div', { class: 'cw-line' + (i === st.active && !st.over ? ' active' : '') });
        const no = h('button', { type: 'button', class: 'cw-no', disabled: st.over || st.rows[i].open }, String(i + 1));
        no.addEventListener('click', () => { st.active = i; draw(); });
        line.append(no);
        for (let c = 0; c < L.width; c += 1) {
          const k = c - r.offset;
          if (k < 0 || k >= r.letters.length) { line.append(h('span', { class: 'cw-gap' })); continue; }
          const show = st.rows[i].open || (st.rows[i].firstLetter && k === 0);
          line.append(h('span', { class: 'cw-cell' + (k === r.keyIndex ? ' cw-key' : '') + (show ? ' on' : '') }, show ? r.letters[k].toUpperCase() : ''));
        }
        grid.append(line);
      });
      box.append(grid);

      if (st.msg) box.append(h('p', { class: 'cw-msg' }, st.msg));

      if (!st.over) {
        const i = st.active;
        const w = cw.words[i];
        const row = st.rows[i];
        if (row.open) {
          const next = st.rows.findIndex((x) => !x.open);
          if (next >= 0) st.active = next;
        }
        const panel = h('div', { class: 'cw-panel' });
        panel.append(h('p', { class: 'cw-clue' }, `Hàng ${st.active + 1} (${L.rows[st.active].letters.length} chữ cái): ${cw.words[st.active].clueVi}`));
        const cur = st.rows[st.active];
        if (cur.hints >= 1) panel.append(h('p', { class: 'cw-hint', lang: 'en' }, cw.words[st.active].clueEn));
        if (!st.rows.every((x) => x.open)) {
          const btns = h('div', { class: 'cw-btns' });
          const h1 = h('button', { type: 'button', class: 'ghost', disabled: cur.hints >= 1 }, 'Gợi ý tiếng Anh (−3 điểm)');
          h1.addEventListener('click', () => { cur.hints = Math.max(cur.hints, 1); draw(); });
          const h2 = h('button', { type: 'button', class: 'ghost', disabled: cur.firstLetter }, 'Cho chữ cái đầu (−3 điểm)');
          h2.addEventListener('click', () => { cur.firstLetter = true; cur.hints += 1; draw(); });
          btns.append(h1, h2);
          const inp = h('input', { type: 'text', 'aria-label': 'Đáp án hàng ngang', placeholder: 'Gõ từ tiếng Anh', autocomplete: 'off', spellcheck: 'false' });
          const ok = h('button', { type: 'button', class: 'primary' }, 'Trả lời');
          const submit = () => {
            const a = norm(inp.value);
            if (!a) return;
            if (a === norm(cw.words[st.active].answer)) {
              const gain = rowScore(cur);
              cur.open = true; st.score += gain;
              st.msg = `Đúng rồi! +${gain} điểm.`;
              if (st.rows.every((x) => x.open)) st.msg += ' Đã mở hết các hàng, hãy đoán từ khóa dọc.';
            } else { cur.wrong += 1; st.msg = 'Chưa đúng, thử lại nhé.'; }
            draw();
          };
          ok.addEventListener('click', submit);
          inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') submit(); });
          panel.append(btns, h('div', { class: 'cw-answer' }, inp, ok));
          setTimeout(() => inp.focus(), 0);
        }
        box.append(panel);

        const kw = h('div', { class: 'cw-keyword' }, h('p', {}, `Từ khóa dọc có ${cw.keyword.length} chữ cái. Đoán đúng được +10 điểm cho mỗi hàng chưa mở; đoán sai −5 điểm.`));
        const kin = h('input', { type: 'text', 'aria-label': 'Từ khóa dọc', placeholder: 'Từ khóa dọc', autocomplete: 'off', spellcheck: 'false' });
        const kok = h('button', { type: 'button', class: 'primary' }, 'Đoán từ khóa');
        kok.addEventListener('click', () => {
          const a = norm(kin.value);
          if (!a) return;
          if (a === norm(cw.keyword)) {
            const closed = st.rows.filter((x) => !x.open).length;
            st.score += 10 * closed;
            st.rows.forEach((x) => { x.open = true; });
            finish(`Chính xác! Từ khóa là “${cw.keyword.toUpperCase()}”. Thưởng +${10 * closed} điểm.`);
          } else { st.score = Math.max(0, st.score - 5); st.msg = 'Từ khóa chưa đúng (−5 điểm).'; draw(); }
        });
        kw.append(h('div', { class: 'cw-answer' }, kin, kok));
        box.append(kw);
      } else {
        const again = h('button', { type: 'button', class: 'primary' }, 'Chơi lại');
        again.addEventListener('click', () => mountCrossword(box, cw));
        box.append(h('p', { class: 'cw-final' }, `Kết thúc. Tổng điểm: ${st.score}`), again);
      }
    }
    draw();
  }

  function mountWriting(box, w) {
    box.replaceChildren(h('h2', {}, 'Viết'), h('p', { class: 'writing-prompt' }, w.prompt));
    box.append(h('p', { class: 'screen-sub' }, 'Bài viết chỉ nằm trên máy này, không gửi đi đâu. Hãy tự đối chiếu với bảng kiểm bên dưới.'));
    const ta = h('textarea', { class: 'writing-area', rows: '7', lang: 'en', 'aria-label': 'Bài viết', spellcheck: 'false' });
    const stat = h('p', { class: 'writing-stat' });
    const chips = h('div', { class: 'writing-chips' });
    const update = () => {
      const words = (ta.value.match(/[A-Za-z']+/g) || []);
      const lower = words.map((x) => x.toLowerCase());
      stat.textContent = `${words.length} từ (nên viết ít nhất ${w.minWords} từ)`;
      stat.classList.toggle('ok', words.length >= w.minWords);
      chips.replaceChildren(...w.keywords.map((k) => h('span', { class: 'chip' + (lower.includes(k) ? ' ok' : '') }, k)));
    };
    ta.addEventListener('input', update);
    box.append(ta, stat, h('p', { class: 'screen-sub' }, 'Từ nên dùng:'), chips);
    const list = h('div', { class: 'writing-check' }, h('p', {}, 'Bảng tự kiểm tra:'));
    w.checklist.forEach((c, i) => {
      list.append(h('label', { class: 'choice' }, h('input', { type: 'checkbox', name: 'wc' + i }), h('span', {}, c)));
    });
    box.append(list);
    const sample = h('div', { class: 'writing-sample', hidden: true });
    sample.append(h('p', { class: 'screen-sub' }, 'Bài mẫu để tham khảo (không chép lại, hãy viết bằng ý của em):'));
    for (const p of w.sample) sample.append(h('p', { class: 'reading-text', lang: 'en' }, p));
    const toggle = h('button', { type: 'button', class: 'ghost' }, 'Xem bài mẫu');
    toggle.addEventListener('click', () => { sample.hidden = !sample.hidden; toggle.textContent = sample.hidden ? 'Xem bài mẫu' : 'Ẩn bài mẫu'; });
    box.append(toggle, sample);
    update();
  }

  // Dựng các phần riêng của bài Tiếng Anh. Phần nào bài không có thì ẩn.
  function render(lesson, els) {
    const top = els.top; const bottom = els.bottom;
    top.replaceChildren(); bottom.replaceChildren();
    const parts = [];
    const add = (host, cls, fn, data) => {
      if (!data) return;
      const sec = h('section', { class: 'en-sec ' + cls });
      fn(sec, data);
      host.append(sec); parts.push(cls);
    };
    add(top, 'en-vocab', renderVocab, lesson.vocab);
    add(top, 'en-crossword', mountCrossword, lesson.crossword);
    add(top, 'en-reading', renderReading, lesson.reading);
    add(bottom, 'en-writing', mountWriting, lesson.writing);
    top.hidden = !top.children.length; bottom.hidden = !bottom.children.length;
  }

  return { norm, layout, keyword, rowScore, validate, render };
});
