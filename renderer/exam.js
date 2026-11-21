/* Đề thi thử theo cấu trúc thi tốt nghiệp THPT: 90 phút, ba phần (trắc nghiệm, đúng–sai, trả lời ngắn), điểm thang 10.
   Dùng các hàm chung của app.js (el, figureNode, isCorrect, showResult, shuffle, showOnly) tại thời điểm gọi.
   Phần chấm điểm (scoreExam) là logic thuần để kiểm thử trong Node. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VungExam = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const TF_POINTS = [0, 0.1, 0.25, 0.5, 1]; // đúng 0,1,2,3,4 ý của một câu đúng–sai
  const P1_EACH = 0.25; const P3_EACH = 0.5;
  const HIST_KEY = 'nl-exam-history';

  const r2 = (v) => Math.round(v * 100) / 100;
  const fmt = (v) => String(r2(v)).replace('.', ',');

  /* Chấm đề. answers: { mã câu: đáp án đã chọn/nhập } với câu tf là { chỉ số ý: true|false }.
     eq(item, value) báo câu trắc nghiệm hoặc trả lời ngắn đúng hay không. Trả về điểm từng phần và từng câu. */
  function scoreExam(items, answers, eq) {
    const out = { p1: 0, p2: 0, p3: 0, total: 0, per: {}, right: { p1: 0, p2: 0, p3: 0 } };
    items.forEach((it) => {
      const a = answers[it.id];
      if (it.type === 'tf') {
        const k = it.statements.filter((s, i) => a && typeof a[i] === 'boolean' && a[i] === s.truth).length;
        out.per[it.id] = { ok: k === 4, k, pts: TF_POINTS[k] };
        out.p2 += TF_POINTS[k]; if (k === 4) out.right.p2 += 1;
      } else {
        const ok = !!eq(it, a);
        const pts = ok ? (it.part === 3 ? P3_EACH : P1_EACH) : 0;
        out.per[it.id] = { ok, pts };
        if (it.part === 3) { out.p3 += pts; if (ok) out.right.p3 += 1; } else { out.p1 += pts; if (ok) out.right.p1 += 1; }
      }
    });
    out.p1 = r2(out.p1); out.p2 = r2(out.p2); out.p3 = r2(out.p3); out.total = r2(out.p1 + out.p2 + out.p3);
    return out;
  }

  const store = () => { try { return window.localStorage; } catch (e) { return null; } };
  const readHist = () => { try { return JSON.parse(store().getItem(HIST_KEY) || '{}') || {}; } catch (e) { return {}; } };
  const saveHist = (id, row) => { try { const h = readHist(); h[id] = (h[id] || []).concat(row).slice(-10); store().setItem(HIST_KEY, JSON.stringify(h)); } catch (e) { /* bỏ qua */ } };

  let timer = null;
  const stop = () => { if (timer) { clearInterval(timer); timer = null; } };

  function open(lesson, relPath, onBack) {
    stop();
    const box = document.getElementById('exam');
    const items = lesson.items;
    const meta = { subject: lesson.subject, grade: lesson.grade, lessonId: relPath, lesson: lesson.lesson, chapter: lesson.chapter };
    const hist = (readHist()[lesson.id] || []).slice(-1)[0];

    const back = el('button', { class: 'back-link', type: 'button' }, '← Danh mục bài học');
    back.addEventListener('click', () => {
      if (timer && !window.confirm('Thoát bây giờ sẽ mất bài đang làm. Bạn muốn thoát?')) return;
      stop(); onBack();
    });

    function intro() {
      box.replaceChildren(...[back,
        el('header', { class: 'screen-head' }, el('p', { class: 'screen-kicker' }, lesson.chapter), el('h1', {}, lesson.title),
          el('p', { class: 'screen-sub' }, `Đề ${lesson.durationMin} phút, 22 câu, thang điểm 10, theo cấu trúc đề thi tốt nghiệp THPT.`)),
        el('table', { class: 'exam-struct' },
          el('tr', {}, el('th', {}, 'Phần'), el('th', {}, 'Dạng câu'), el('th', {}, 'Số câu'), el('th', {}, 'Điểm')),
          el('tr', {}, el('td', {}, 'I'), el('td', {}, 'Trắc nghiệm 4 phương án'), el('td', {}, '12'), el('td', {}, '0,25 điểm/câu')),
          el('tr', {}, el('td', {}, 'II'), el('td', {}, 'Đúng–sai (mỗi câu 4 ý)'), el('td', {}, '4'), el('td', {}, 'đúng 1/2/3/4 ý: 0,1/0,25/0,5/1 điểm')),
          el('tr', {}, el('td', {}, 'III'), el('td', {}, 'Trả lời ngắn'), el('td', {}, '6'), el('td', {}, '0,5 điểm/câu'))),
        el('p', { class: 'meta' }, 'Trong lúc làm bài không hiện đúng sai. Hết giờ bài tự nộp. Câu trả lời ngắn nhập số, ví dụ 3/4 hoặc 0,75.'),
        hist ? el('p', { class: 'meta' }, `Lần làm gần nhất: ${fmt(hist.score)}/10.`) : null].filter(Boolean));
      const go = el('button', { type: 'button', class: 'exam-go' }, 'Bắt đầu làm bài');
      go.addEventListener('click', start);
      box.append(go);
    }

    function start() {
      const st = { started: Date.now(), left: lesson.durationMin * 60, answers: {}, order: {}, done: false };
      items.forEach((it) => { if (it.type === 'mcq') st.order[it.id] = shuffle(it.choices.map((_, i) => i)); });
      const bar = el('div', { class: 'exam-bar' });
      const clock = el('span', { class: 'exam-clock', role: 'timer' });
      const submit = el('button', { type: 'button' }, 'Nộp bài');
      bar.append(clock, submit);
      const body = el('div', { class: 'exam-body' });
      box.replaceChildren(back, bar, body);

      const tick = () => {
        const m = Math.floor(st.left / 60); const s = st.left % 60;
        clock.textContent = `Còn ${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        clock.classList.toggle('warn', st.left <= 300);
      };
      const parts = [[1, 'Phần I. Trắc nghiệm nhiều phương án chọn một (12 câu)'], [2, 'Phần II. Trắc nghiệm đúng–sai (4 câu)'], [3, 'Phần III. Trắc nghiệm trả lời ngắn (6 câu)']];
      const nodes = {};
      parts.forEach(([p, title]) => {
        body.append(el('h2', { class: 'exam-part' }, title));
        items.filter((it) => it.part === p).forEach((it, k) => {
          const q = el('div', { class: 'question', 'data-id': it.id });
          q.append(el('div', { class: 'stem' }, `Câu ${k + 1}. ${it.stem}`));
          if (it.figureSvg) q.append(figureNode(it.figureSvg, `Hình câu ${k + 1}`));
          if (it.type === 'mcq') {
            st.order[it.id].forEach((oi) => {
              const label = el('label', { class: 'choice' });
              const input = el('input', { type: 'radio', name: it.id });
              input.addEventListener('change', () => { st.answers[it.id] = it.choices[oi]; });
              label.append(input, el('span', {}, it.choices[oi]));
              q.append(label);
            });
          } else if (it.type === 'tf') {
            q.append(el('p', { class: 'meta' }, 'Với câu hỏi trên, mỗi phương án sau đúng hay sai?'));
            it.statements.forEach((s, i) => {
              const row = el('div', { class: 'tf-row' }, el('span', { class: 'tf-text' }, `${'abcd'[i]}) ${s.text}`));
              ['Đúng', 'Sai'].forEach((lab, v) => {
                const l = el('label', { class: 'tf-opt' });
                const input = el('input', { type: 'radio', name: `${it.id}-${i}` });
                input.addEventListener('change', () => { st.answers[it.id] = Object.assign({}, st.answers[it.id], { [i]: v === 0 }); });
                l.append(input, lab); row.append(l);
              });
              q.append(row);
            });
          } else {
            const input = el('input', { type: 'text', 'aria-label': 'Đáp án', placeholder: 'Ví dụ: 3/4 hoặc 0,75', autocomplete: 'off' });
            input.addEventListener('input', () => { st.answers[it.id] = input.value.trim() || null; });
            q.append(input);
          }
          q.append(el('div', { class: 'feedback', hidden: 'hidden' }));
          body.append(q); nodes[it.id] = q;
        });
      });

      function finish(auto) {
        if (st.done) return;
        st.done = true; stop();
        const res = scoreExam(items, st.answers, (it, v) => isCorrect(it, v));
        bar.remove();
        const head = el('div', { class: 'exam-result' },
          el('h2', {}, `Điểm: ${fmt(res.total)}/10`),
          el('p', {}, auto ? 'Hết giờ, bài đã tự nộp.' : `Thời gian làm bài: ${Math.max(1, Math.round((Date.now() - st.started) / 60000))} phút.`),
          el('ul', { class: 'wrong-list' },
            el('li', {}, `Phần I: ${res.right.p1}/12 câu đúng, ${fmt(res.p1)}/3 điểm`),
            el('li', {}, `Phần II: ${res.right.p2}/4 câu đúng hết 4 ý, ${fmt(res.p2)}/4 điểm`),
            el('li', {}, `Phần III: ${res.right.p3}/6 câu đúng, ${fmt(res.p3)}/3 điểm`)));
        box.insertBefore(head, body);
        items.forEach((it) => {
          const q = nodes[it.id]; const fb = q.querySelector('.feedback');
          q.querySelectorAll('input').forEach((i) => { i.disabled = true; });
          if (it.type === 'tf') {
            const a = st.answers[it.id] || {};
            const rows = q.querySelectorAll('.tf-row');
            it.statements.forEach((s, i) => {
              const given = typeof a[i] === 'boolean' ? a[i] : null;
              const ok = given === s.truth;
              rows[i].classList.add(ok ? 'is-right' : 'is-wrong');
              rows[i].append(el('div', { class: 'tf-note' }, `${ok ? 'Đúng' : given === null ? 'Chưa trả lời' : 'Sai'}. Ý này ${s.truth ? 'đúng' : 'sai'}. ${s.explain}`));
            });
            fb.hidden = false; fb.className = 'feedback ' + (res.per[it.id].ok ? 'ok' : 'bad');
            fb.textContent = `Đúng ${res.per[it.id].k}/4 ý: ${fmt(res.per[it.id].pts)} điểm.`;
          } else {
            showResult(it, fb, st.answers[it.id]);
            if (it.type === 'mcq') {
              q.querySelectorAll('.choice').forEach((label) => {
                const text = label.querySelector('span').textContent;
                if (text === it.choices[it.answer]) label.classList.add('is-right');
                else if (label.querySelector('input').checked) label.classList.add('is-wrong');
              });
            }
          }
        });
        saveHist(lesson.id, { t: Date.now(), score: res.total });
        // Ghi vào báo cáo và sổ câu sai: các câu trắc nghiệm và trả lời ngắn (câu đúng–sai chưa vào sổ câu sai).
        if (window.VungGames && window.VungGames.recordStudy) window.VungGames.recordStudy();
        if (window.VungProgressUI) {
          const practice = items.filter((it) => it.type !== 'tf');
          const attempt = { questions: practice.map((_, i) => i), answers: st.answers, started: st.started };
          window.VungProgressUI.record({ items: practice }, attempt, meta);
          window.VungProgressUI.refreshBadge();
        }
        window.scrollTo(0, 0);
      }
      submit.addEventListener('click', () => {
        const blank = items.filter((it) => it.type === 'tf' ? !st.answers[it.id] : (st.answers[it.id] === undefined || st.answers[it.id] === null || st.answers[it.id] === '')).length;
        if (blank && !window.confirm(`Còn ${blank} câu chưa trả lời. Câu bỏ trống tính là sai. Nộp bài luôn?`)) return;
        finish(false);
      });
      tick();
      timer = setInterval(() => { st.left -= 1; tick(); if (st.left <= 0) finish(true); }, 1000);
      window.scrollTo(0, 0);
    }

    intro();
    showOnly('exam');
    window.scrollTo(0, 0);
  }

  return { open, scoreExam, TF_POINTS };
});
