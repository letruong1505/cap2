/* Giao diện sổ câu sai và báo cáo tuần cho phụ huynh. Dùng VungProgress (progress.js)
   và các hàm dùng chung của app.js (isCorrect, showResult, figureSrc) tại thời điểm gọi. */
(function () {
  const P = window.VungProgress;
  const SUBJ = { anh: 'Tiếng Anh', toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', 'lich-su': 'Lịch sử', 'dia-li': 'Địa lí' };
  const subjName = (s) => SUBJ[s] || s;
  const store = () => { try { return window.localStorage; } catch (e) { return null; } };

  function h(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => { if (v !== false && v != null) n.setAttribute(k, v); });
    kids.forEach((k) => n.append(k));
    return n;
  }
  const fmtDate = (t) => new Date(t).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' });

  /* Ghi nhận một lượt nộp bài. */
  function record(lesson, attempt, meta) {
    if (!P || !meta) return;
    const wrong = []; const right = [];
    attempt.questions.forEach((i) => {
      const it = lesson.items[i];
      (isCorrect(it, attempt.answers[it.id]) ? right : wrong).push(it);
    });
    const data = P.load(store());
    P.recordAttempt(data, Object.assign({}, meta, {
      correct: right.length, total: right.length + wrong.length,
      seconds: (Date.now() - (attempt.started || Date.now())) / 1000,
    }), wrong, right);
    P.save(store(), data);
  }

  const bar = (v, max) => {
    const pct = Math.min(100, Math.round((100 * v) / max));
    return h('div', { class: 'goal-bar', role: 'progressbar', 'aria-valuenow': v, 'aria-valuemax': max },
      h('div', { class: 'goal-fill' + (v >= max ? ' done' : ''), style: `width:${pct}%` }));
  };

  /* Khối mục tiêu ngày/tuần và điểm; grade = 0 là tất cả các lớp. */
  function renderGoals(box, grade) {
    if (!box || !P) return;
    box.replaceChildren();
    const data = P.load(store());
    const p = P.progress(data, Date.now(), grade);
    const g = p.goals;
    box.append(h('h2', {}, grade ? `Mục tiêu · Lớp ${grade}` : 'Mục tiêu học tập'));
    box.append(h('p', {}, `Hôm nay: ${p.todayDone}/${g.daily} câu${p.todayDone >= g.daily ? ' – đạt mục tiêu!' : ''}`), bar(p.todayDone, g.daily));
    box.append(h('p', {}, `Tuần này: ${p.daysDone}/${g.weekly} ngày học${p.daysDone >= g.weekly ? ' – đạt mục tiêu!' : ''}`), bar(p.daysDone, g.weekly));
    box.append(h('p', { class: 'meta' }, `Điểm: hôm nay ${p.todayPts} · 7 ngày ${p.weekPts} · tổng ${p.totalPts}`));
    const mk = (opts, cur, label) => {
      const sel = h('select', { 'aria-label': label });
      opts.forEach((o) => { const op = h('option', { value: o }, String(o)); if (o === cur) op.selected = true; sel.append(op); });
      return sel;
    };
    const d = mk([10, 15, 20, 30, 40, 50, 80, 100], g.daily, 'Số câu mỗi ngày');
    const w = mk([1, 2, 3, 4, 5, 6, 7], g.weekly, 'Số ngày học mỗi tuần');
    const apply = () => { P.save(store(), P.setGoals(P.load(store()), { daily: d.value, weekly: w.value })); renderGoals(box, grade); };
    d.addEventListener('change', apply); w.addEventListener('change', apply);
    box.append(h('p', { class: 'goal-set' }, 'Đặt mục tiêu: ', d, ' câu/ngày, ', w, ' ngày/tuần'));
  }

  function dueCount(grade) { return P ? P.due(P.load(store()), Date.now(), grade).length : 0; }

  /* ---------- Sổ câu sai ---------- */
  function renderReview(body, grade) {
    body.replaceChildren();
    const data = P.load(store());
    const all = grade ? data.notebook.filter((n) => n.grade === grade) : data.notebook;
    const list = P.due(data, Date.now(), grade);
    body.append(h('h1', {}, grade ? `Sổ câu sai · Lớp ${grade}` : 'Sổ câu sai'));
    if (!all.length) {
      body.append(h('p', { class: 'meta' }, 'Chưa có câu sai nào. Khi làm bài và bấm "Kiểm tra toàn bài", các câu sai sẽ được lưu ở đây để ôn lại.'));
      return;
    }
    body.append(h('p', { class: 'meta' }, `Trong sổ có ${all.length} câu, ${list.length} câu đến hạn ôn hôm nay. Làm đúng ba lần cách quãng 1, 3, 7 ngày thì câu được xóa khỏi sổ.`));
    if (!list.length) {
      const next = Math.min(...all.map((n) => n.due));
      body.append(h('p', {}, `Hôm nay chưa có câu cần ôn. Lượt ôn tiếp theo: ${fmtDate(next)}.`));
      return;
    }
    const batch = list.slice(0, 10);
    const answers = {};
    const order = {};
    batch.forEach((n, idx) => {
      const it = n.item;
      const q = h('div', { class: 'question', 'data-id': it.id });
      q.append(h('div', { class: 'meta' }, `${subjName(n.subject)} lớp ${n.grade} · ${n.lesson}`));
      q.append(h('div', { class: 'stem' }, `${idx + 1}. ${it.stem}`));
      if (it.figureSvg) q.append(h('img', { class: 'figure', alt: '', src: figureSrc(it.figureSvg) }));
      if (it.type === 'mcq') {
        order[it.id] = it.choices.map((_, i) => i).sort(() => Math.random() - 0.5);
        order[it.id].forEach((oi) => {
          const label = h('label', { class: 'choice' });
          const input = h('input', { type: 'radio', name: 'rv-' + n.key });
          input.addEventListener('change', () => { answers[n.key] = it.choices[oi]; });
          label.append(input, h('span', {}, it.choices[oi]));
          q.append(label);
        });
      } else {
        const input = h('input', { type: 'text', 'aria-label': 'Đáp án', autocomplete: 'off' });
        input.addEventListener('input', () => { answers[n.key] = input.value.trim() || null; });
        q.append(input);
      }
      q.append(h('div', { class: 'feedback', hidden: 'hidden' }));
      body.append(q);
    });
    const done = h('button', { type: 'button', class: 'primary' }, 'Kiểm tra');
    const result = h('p', { class: 'meta' });
    done.addEventListener('click', () => {
      done.disabled = true;
      let ok = 0;
      const now = Date.now();
      batch.forEach((n, idx) => {
        const it = n.item;
        const q = body.querySelectorAll('.question')[idx];
        showResult(it, q.querySelector('.feedback'), answers[n.key]);
        q.querySelectorAll('input').forEach((i) => { i.disabled = true; });
        const good = isCorrect(it, answers[n.key]);
        if (good) ok += 1;
        P.grade(data, n.key, good, now);
      });
      P.save(store(), data);
      result.textContent = `Đúng ${ok}/${batch.length} câu. Câu đúng sẽ hẹn ôn lại sau; câu sai ôn lại vào ngày mai.`;
      refreshBadge();
    });
    body.append(done, result);
  }

  /* ---------- Báo cáo tuần ---------- */
  function lines(w) {
    const out = [];
    if (w.grade) out.push(`Lớp ${w.grade}`);
    out.push(`Số ngày học trong 7 ngày: ${w.days}/7 (mục tiêu ${w.prog.goals.weekly} ngày)`);
    out.push(`Điểm 7 ngày: ${w.prog.weekPts}, tổng điểm: ${w.prog.totalPts}`);
    out.push(`Số bài đã nộp: ${w.attempts}, thời gian làm: ${w.minutes} phút`);
    out.push(w.total ? `Tỉ lệ đúng chung: ${w.pct}% (${w.correct}/${w.total} câu)` : 'Chưa có bài nào trong tuần này');
    w.subjects.forEach((s) => out.push(`${subjName(s.subject)} lớp ${s.grade}: ${s.pct}% (${s.lessons} bài)`));
    if (w.weak.length) {
      out.push('Cần ôn thêm:');
      w.weak.forEach((c) => out.push(`  • ${c.name} (${subjName(c.subject)} ${c.grade}) – ${c.pct}%`));
    } else if (w.total) out.push('Chưa có chương nào dưới 70%.');
    out.push(`Sổ câu sai: ${w.notebook} câu, ${w.dueCount} câu đến hạn ôn`);
    return out;
  }

  function drawPng(w, name) {
    const L = lines(w);
    const c = document.createElement('canvas');
    c.width = 900; c.height = 220 + L.length * 44;
    const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
    g.fillStyle = '#1f6f8b'; g.fillRect(0, 0, c.width, 110);
    g.fillStyle = '#fff'; g.font = 'bold 34px sans-serif';
    g.fillText(w.grade ? `Báo cáo tuần Lớp ${w.grade} – Nam Linh Educenter` : 'Báo cáo tuần – Nam Linh Educenter', 36, 52);
    g.font = '22px sans-serif';
    g.fillText(`${name ? name + ' · ' : ''}${fmtDate(w.from)} – ${fmtDate(w.to)}`, 36, 88);
    g.fillStyle = '#222'; g.font = '24px sans-serif';
    L.forEach((t, i) => g.fillText(t, 36, 160 + i * 44));
    g.fillStyle = '#888'; g.font = '18px sans-serif';
    g.fillText('Dữ liệu lưu trên máy của học sinh', 36, c.height - 24);
    return c;
  }

  function renderReport(body, grade) {
    body.replaceChildren();
    const w = P.weekly(P.load(store()), Date.now(), grade);
    body.append(h('h1', {}, grade ? `Báo cáo tuần cho phụ huynh · Lớp ${grade}` : 'Báo cáo tuần cho phụ huynh'));
    body.append(h('p', { class: 'meta' }, `7 ngày gần nhất: ${fmtDate(w.from)} – ${fmtDate(w.to)}`));
    const ul = h('ul', { class: 'report-list' });
    lines(w).forEach((t) => ul.append(h('li', {}, t.replace(/^\s*•\s*/, ''))));
    body.append(ul);
    body.append(h('div', { class: 'goal-box', id: 'goal-box-report' }));
    renderGoals(document.getElementById('goal-box-report') || body.lastChild, grade);
    const nameIn = h('input', { type: 'text', placeholder: 'Tên học sinh (không bắt buộc)', autocomplete: 'off', 'aria-label': 'Tên học sinh' });
    const btn = h('button', { type: 'button', class: 'primary' }, 'Lưu ảnh báo cáo gửi Zalo');
    const msg = h('p', { class: 'meta' });
    btn.addEventListener('click', () => {
      drawPng(w, nameIn.value.trim()).toBlob((blob) => {
        if (!blob) { msg.textContent = 'Không tạo được ảnh.'; return; }
        const a = h('a', { download: `bao-cao-tuan${grade ? '-lop' + grade : ''}-${new Date().toISOString().slice(0, 10)}.png`, href: URL.createObjectURL(blob) });
        document.body.append(a); a.click(); a.remove();
        msg.textContent = 'Đã tạo ảnh báo cáo. Chọn nơi lưu rồi gửi cho phụ huynh qua Zalo.';
      }, 'image/png');
    });
    body.append(nameIn, btn, msg);
  }

  function refreshBadge() {
    const set = (id, label, n) => {
      const b = document.getElementById(id);
      if (b) b.textContent = n ? `${label} (${n} câu cần ôn)` : label;
    };
    set('open-review', 'Sổ câu sai', dueCount());
    renderGoals(document.getElementById('goal-box'), 0);
    const g = window.VungProgressUI && window.VungProgressUI.scope;
    renderGoals(document.getElementById('goal-box-grade'), g || 0);
    if (g) set('open-review-grade', `Sổ câu sai lớp ${g}`, dueCount(g));
  }

  window.VungProgressUI = { scope: 0, renderGoals, record, renderReview, renderReport, refreshBadge, dueCount };
})();
