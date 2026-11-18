/* Giao diện sổ câu sai và báo cáo tuần cho phụ huynh. Dùng VungProgress (progress.js)
   và các hàm dùng chung của app.js (isCorrect, showResult, figureSrc) tại thời điểm gọi. */
(function () {
  const P = window.VungProgress;
  const SUBJ = { anh: 'Tiếng Anh', toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', gdktpl: 'Giáo dục KT&PL', 'lich-su': 'Lịch sử', 'dia-li': 'Địa lí' };
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
      given: Object.assign({}, attempt.answers),
      correct: right.length, total: right.length + wrong.length,
      seconds: (Date.now() - (attempt.started || Date.now())) / 1000,
    }), wrong, right);
    P.save(store(), data);
  }

  const DOW = ['Chủ nhật', 'Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy'];
  const fmtFull = (t) => { const d = new Date(t); return `${DOW[d.getDay()]}, ${d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })}`; };
  const iso = (t) => { const d = new Date(t); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  const fromIso = (v) => { const [y, m, d] = String(v).split('-').map(Number); return new Date(y, m - 1, d).getTime(); };

  /* Thanh chất lượng: xanh = đúng, đỏ = sai, kèm số câu và tỉ lệ %. */
  function qualityBar(correct, total, withText) {
    const wrong = total - correct;
    const pc = total ? Math.round((100 * correct) / total) : 0;
    const box = h('div', { class: 'q-wrap' });
    const bar = h('div', { class: 'q-bar', role: 'img', 'aria-label': total ? `Đúng ${correct}, sai ${wrong} trên ${total} câu` : 'Chưa làm câu nào' });
    if (total) {
      bar.append(h('div', { class: 'q-ok', style: `width:${100 - (100 - pc)}%` }), h('div', { class: 'q-bad', style: `width:${100 - pc}%` }));
    }
    box.append(bar);
    if (withText) box.append(h('p', { class: 'q-text' }, total
      ? `Đúng ${correct} · Sai ${wrong} (${pc}% đúng / ${100 - pc}% sai, tổng ${total} câu)`
      : 'Chưa làm câu nào'));
    return box;
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
    box.append(h('p', { class: 'meta' }, fmtFull(Date.now())));
    box.append(h('p', {}, `Hôm nay: ${p.todayDone}/${g.daily} câu${p.todayDone >= g.daily ? ' – đạt mục tiêu!' : ''}`), bar(p.todayDone, g.daily));
    box.append(h('p', { class: 'meta' }, 'Chất lượng hôm nay'), qualityBar(p.todayCorrect, p.todayDone, true));
    box.append(h('p', {}, `Tuần này: ${p.daysDone}/${g.weekly} ngày học${p.daysDone >= g.weekly ? ' – đạt mục tiêu!' : ''}`), bar(p.daysDone, g.weekly));
    box.append(h('p', { class: 'meta' }, `Điểm: hôm nay ${p.todayPts} · 7 ngày ${p.weekPts} · tổng ${p.totalPts}`));
    const mk = (opts, cur, label) => {
      const sel = h('select', { 'aria-label': label });
      opts.forEach((o) => { const op = h('option', { value: o }, String(o)); if (o === cur) op.selected = true; sel.append(op); });
      return sel;
    };
    const d = mk([10, 15, 20, 30, 40, 50, 80, 100], g.daily, 'Số câu mỗi ngày');
    const w = mk([1, 2, 3, 4, 5, 6, 7], g.weekly, 'Số ngày học mỗi tuần');
    const apply = async () => {
      const ui = window.VungPinUI;
      if (ui && !(await ui.ensureUnlocked())) { renderGoals(box, grade); return; }
      P.save(store(), P.setGoals(P.load(store()), { daily: d.value, weekly: w.value })); renderGoals(box, grade);
    };
    d.addEventListener('change', apply); w.addEventListener('change', apply);
    box.append(h('p', { class: 'goal-set' }, 'Đặt mục tiêu: ', d, ' câu/ngày, ', w, ' ngày/tuần'));
  }

  function dueCount(grade) { return P ? P.due(P.load(store()), Date.now(), grade).length : 0; }

  /* Toàn bộ câu sai trong sổ (không chỉ câu đến hạn), nhóm theo bài, kèm kiến thức cần nắm. */
  function appendAllWrong(body, all) {
    const sec = h('section', { class: 'all-wrong' });
    sec.append(h('h2', {}, `Toàn bộ câu sai (${all.length})`));
    const groups = new Map();
    all.slice().sort((a, b) => (a.subject + a.grade + a.lessonId).localeCompare(b.subject + b.grade + b.lessonId) || a.added - b.added)
      .forEach((n) => {
        if (!groups.has(n.lessonId)) groups.set(n.lessonId, { meta: n, items: [] });
        groups.get(n.lessonId).items.push(n);
      });
    groups.forEach((g, lessonId) => {
      const box = h('div', { class: 'wrong-group' });
      box.append(h('h3', {}, `${subjName(g.meta.subject)} lớp ${g.meta.grade} · ${g.meta.lesson}`));
      const know = h('div', { class: 'kt-box' }, h('div', { class: 'meta' }, 'Đang tải kiến thức cần nắm…'));
      box.append(know);
      g.items.forEach((n, idx) => {
        const it = n.item;
        const q = h('div', { class: 'question wrong-card' });
        q.append(h('div', { class: 'stem' }, `${idx + 1}. ${it.stem}`));
        if (it.expr) q.append(h('div', { class: 'meta' }, `Phép tính: ${it.expr}`));
        if (it.type === 'mcq') {
          it.choices.forEach((c, i) => {
            const ok = i === it.answer;
            const mine = !ok && n.given === c;
            q.append(h('div', { class: ok ? 'choice-correct' : mine ? 'choice-wrong' : 'choice-plain' },
              (ok ? '✓ ' : mine ? '✗ Em đã chọn: ' : '• ') + c));
          });
          if (n.given === null) q.append(h('div', { class: 'choice-wrong' }, 'Em chưa chọn đáp án nào.'));
        } else {
          if (Object.prototype.hasOwnProperty.call(n, 'given')) {
            q.append(h('div', { class: 'choice-wrong' }, n.given === null ? 'Em chưa trả lời.' : '✗ Em trả lời: ' + n.given));
          }
          q.append(h('div', { class: 'choice-correct' }, '✓ Đáp án đúng: ' + viNumber(it.answer)));
        }
        q.append(h('div', { class: 'feedback ok' }, 'Lời giải: ' + it.explain));
        box.append(q);
      });
      sec.append(box);
      if (window.vungBai && window.vungBai.loadLesson) {
        window.vungBai.loadLesson(lessonId).then((lesson) => {
          const kids = [h('div', { class: 'meta' }, 'Kiến thức cần nắm')];
          (lesson.requirements || []).forEach((r) => kids.push(h('div', { class: 'kt-line' }, '• ' + r)));
          (lesson.theory || []).filter((t) => t.type === 'formula').forEach((t) => kids.push(h('p', { class: 'formula' }, t.content)));
          know.replaceChildren(...kids);
        }).catch(() => know.replaceChildren(h('div', { class: 'meta' }, 'Không tải được phần kiến thức của bài này.')));
      } else {
        know.replaceChildren(h('div', { class: 'meta' }, 'Kiến thức cần nắm chưa khả dụng.'));
      }
    });
    body.append(sec);
  }

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
    appendAllWrong(body, all);
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

  /* ---------- Báo cáo cho phụ huynh ---------- */
  const PERIODS = [['today', 'Hôm nay'], ['week', 'Tuần này (từ thứ hai)'], ['7', '7 ngày gần nhất'], ['month', 'Tháng này'], ['30', '30 ngày gần nhất'], ['custom', 'Chọn khoảng ngày']];

  function rangeOf(kind, now, customFrom, customTo) {
    const t0 = new Date(now); t0.setHours(0, 0, 0, 0);
    const day = 86400000; const today = t0.getTime();
    if (kind === 'today') return { from: today, to: today };
    if (kind === 'week') { const dow = (t0.getDay() + 6) % 7; return { from: today - dow * day, to: today - dow * day + 6 * day }; }
    if (kind === '30') return { from: today - 29 * day, to: today };
    if (kind === 'month') { const a = new Date(t0.getFullYear(), t0.getMonth(), 1); const b = new Date(t0.getFullYear(), t0.getMonth() + 1, 0); return { from: a.getTime(), to: b.getTime() }; }
    if (kind === 'custom') { const a = customFrom || today; const b = customTo || today; return a <= b ? { from: a, to: b } : { from: b, to: a }; }
    return { from: today - 6 * day, to: today };
  }

  function lines(r) {
    const out = [];
    if (r.grade) out.push(`Lớp ${r.grade}`);
    if (r.subject) out.push(`Môn: ${subjName(r.subject)}`);
    out.push(`Số ngày có học: ${r.activeDays}/${r.days.length}`);
    out.push(`Số bài đã nộp: ${r.attempts}, thời gian làm: ${r.minutes} phút`);
    out.push(r.total ? `Đúng ${r.correct} · Sai ${r.wrong} (${r.pct}% đúng / ${100 - r.pct}% sai, tổng ${r.total} câu)` : 'Chưa có bài nào trong khoảng này');
    r.subjects.forEach((s) => out.push(`${subjName(s.subject)} lớp ${s.grade}: đúng ${s.correct}, sai ${s.wrong} (${s.pct}% đúng)`));
    if (r.weak.length) {
      out.push('Cần ôn thêm:');
      r.weak.forEach((c) => out.push(`  • ${c.name} (${subjName(c.subject)} ${c.grade}) – ${c.pct}%`));
    } else if (r.total) out.push('Chưa có chương nào dưới 70%.');
    return out;
  }

  function drawPng(r, name) {
    const days = r.days.length <= 14 ? r.days : [];
    const c = document.createElement('canvas');
    c.width = 900;
    // Ngắt dòng theo chiều rộng khung vẽ để không bị cắt chữ (tên chương dài)
    const mg = c.getContext('2d');
    mg.font = '24px sans-serif';
    const L = [];
    lines(r).forEach((t) => {
      const lead = (t.match(/^\s*•?\s*/) || [''])[0];
      const indent = lead.includes('•') ? '    ' : '';
      let cur = '';
      t.split(' ').forEach((w) => {
        const next = cur ? cur + ' ' + w : w;
        if (cur && mg.measureText(next).width > 828) { L.push(cur); cur = indent + w; } else cur = next;
      });
      L.push(cur);
    });
    c.height = 230 + L.length * 44 + (days.length ? 170 : 0);
    const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
    g.fillStyle = '#1f6f8b'; g.fillRect(0, 0, c.width, 110);
    g.fillStyle = '#fff'; g.font = 'bold 34px sans-serif';
    g.fillText(r.grade ? `Báo cáo học tập Lớp ${r.grade} – Nam Linh Educenter` : 'Báo cáo học tập – Nam Linh Educenter', 36, 52);
    g.font = '22px sans-serif';
    g.fillText(`${name ? name + ' · ' : ''}${fmtDate(r.from)} – ${fmtDate(r.to)}`, 36, 88);
    g.fillStyle = '#222'; g.font = '24px sans-serif';
    L.forEach((t, i) => g.fillText(t, 36, 160 + i * 44));
    let y = 170 + L.length * 44;
    if (days.length) {
      const w = Math.floor(828 / days.length);
      days.forEach((d, i) => {
        const x = 36 + i * w;
        g.fillStyle = '#222'; g.font = '16px sans-serif';
        g.fillText(fmtDate(d.t), x, y + 16);
        g.fillStyle = '#e3ebf0'; g.fillRect(x, y + 26, w - 8, 70);
        if (d.total) {
          const h1 = Math.round(70 * d.correct / d.total);
          g.fillStyle = '#d64545'; g.fillRect(x, y + 26, w - 8, 70);
          g.fillStyle = '#2e7d4f'; g.fillRect(x, y + 26 + 70 - h1, w - 8, h1);
        }
        g.fillStyle = '#222'; g.fillText(d.total ? `${d.correct}/${d.total}` : '–', x, y + 118);
      });
    }
    g.fillStyle = '#888'; g.font = '18px sans-serif';
    g.fillText('Xanh: đúng · Đỏ: sai · Dữ liệu lưu trên máy của học sinh', 36, c.height - 24);
    return c;
  }

  function calendar(r, today) {
    const wrap = h('div', { class: 'cal' });
    ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'].forEach((n) => wrap.append(h('div', { class: 'cal-h' }, n)));
    const first = new Date(r.days[0].t); const lead = (first.getDay() + 6) % 7;
    for (let i = 0; i < lead; i++) wrap.append(h('div', { class: 'cal-pad' }));
    r.days.forEach((d) => {
      const cell = h('div', { class: 'cal-d' + (d.t === today ? ' today' : '') + (d.total ? '' : ' none') });
      cell.append(h('b', {}, new Date(d.t).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' })));
      if (d.total) {
        cell.append(h('span', {}, `${d.correct}/${d.total} câu`), qualityBar(d.correct, d.total, false), h('small', {}, `${d.pct}% đúng${d.reached ? ' · đạt mục tiêu' : ''}`));
      } else cell.append(h('small', {}, 'Chưa học'));
      wrap.append(cell);
    });
    return wrap;
  }

  const view = { period: '7', subject: '', from: null, to: null };

  function renderReport(body, grade) {
    body.replaceChildren();
    const now = Date.now();
    const today = new Date(now).setHours(0, 0, 0, 0);
    const data = P.load(store());
    const rg = rangeOf(view.period, now, view.from, view.to);
    const r = P.report(data, { from: rg.from, to: rg.to, subject: view.subject, grade }, now);
    body.append(h('h1', {}, grade ? `Báo cáo cho phụ huynh · Lớp ${grade}` : 'Báo cáo cho phụ huynh'));
    body.append(h('p', { class: 'meta' }, `Hôm nay: ${fmtFull(now)} (theo ngày của máy tính)`));

    const rerender = () => renderReport(body, grade);
    const perSel = h('select', { 'aria-label': 'Khoảng thời gian' });
    PERIODS.forEach(([k, t]) => { const o = h('option', { value: k }, t); if (k === view.period) o.selected = true; perSel.append(o); });
    perSel.addEventListener('change', () => { view.period = perSel.value; if (view.period === 'custom' && view.from == null) { view.from = rg.from; view.to = rg.to; } rerender(); });
    const subSel = h('select', { 'aria-label': 'Môn học' });
    const allOpt = h('option', { value: '' }, 'Tất cả môn'); subSel.append(allOpt);
    Object.keys(SUBJ).forEach((k) => { const o = h('option', { value: k }, SUBJ[k]); if (k === view.subject) o.selected = true; subSel.append(o); });
    subSel.addEventListener('change', () => { view.subject = subSel.value; rerender(); });
    const ctl = h('div', { class: 'rep-ctl' }, h('label', {}, 'Thời gian ', perSel), h('label', {}, 'Môn học ', subSel));
    if (view.period === 'custom') {
      const f = h('input', { type: 'date', value: iso(rg.from), max: iso(today), 'aria-label': 'Từ ngày' });
      const t = h('input', { type: 'date', value: iso(rg.to), max: iso(today), 'aria-label': 'Đến ngày' });
      const onDate = () => { if (f.value && t.value) { view.from = fromIso(f.value); view.to = fromIso(t.value); rerender(); } };
      f.addEventListener('change', onDate); t.addEventListener('change', onDate);
      ctl.append(h('label', {}, 'Từ ', f), h('label', {}, 'Đến ', t));
    }
    body.append(ctl);
    body.append(h('p', { class: 'meta' }, `${fmtFull(r.from)} → ${fmtFull(r.to)}${view.subject ? ' · ' + subjName(view.subject) : ''}`));

    body.append(h('div', { class: 'goal-box' }, h('h2', {}, 'Chất lượng làm bài'), qualityBar(r.correct, r.total, true)));
    if (r.days.length > 1 || r.total) {
      body.append(h('h2', { class: 'rep-h' }, r.days.length <= 7 ? 'Lịch tuần' : 'Lịch học'), calendar(r, today));
    }
    if (r.subjects.length) {
      const box = h('div', { class: 'goal-box' }, h('h2', {}, 'Theo môn học'));
      r.subjects.forEach((s) => box.append(h('p', {}, `${subjName(s.subject)} lớp ${s.grade}: ${s.lessons} bài`), qualityBar(s.correct, s.total, true)));
      body.append(box);
    }
    const ul = h('ul', { class: 'report-list' });
    lines(r).forEach((t) => ul.append(h('li', {}, t.replace(/^\s*•\s*/, ''))));
    body.append(ul);
    const book = grade ? data.notebook.filter((n) => n.grade === grade) : data.notebook;
    body.append(h('p', { class: 'meta' }, `Sổ câu sai: ${book.length} câu, ${P.due(data, now, grade).length} câu đến hạn ôn`));
    body.append(h('div', { class: 'goal-box', id: 'goal-box-report' }));
    renderGoals(document.getElementById('goal-box-report') || body.lastChild, grade);
    const pinBox = h('div', { class: 'goal-box' });
    body.append(pinBox);
    if (window.VungPinUI) window.VungPinUI.renderSettings(pinBox, () => renderReport(body, grade));
    const nameIn = h('input', { type: 'text', placeholder: 'Tên học sinh (không bắt buộc)', autocomplete: 'off', 'aria-label': 'Tên học sinh' });
    const btn = h('button', { type: 'button', class: 'primary' }, 'Lưu ảnh báo cáo gửi Zalo');
    const msg = h('p', { class: 'meta' });
    btn.addEventListener('click', () => {
      drawPng(r, nameIn.value.trim()).toBlob((blob) => {
        if (!blob) { msg.textContent = 'Không tạo được ảnh.'; return; }
        const a = h('a', { download: `bao-cao${grade ? '-lop' + grade : ''}-${iso(now)}.png`, href: URL.createObjectURL(blob) });
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
