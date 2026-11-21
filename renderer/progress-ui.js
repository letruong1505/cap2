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
  const U = window.VungUsage;
  const fmtDur = (s) => (U ? U.fmtDur(s) : '');
  /* Gắn thời gian dùng app (mở app, dùng thực, ngắt quãng) vào báo cáo và từng ngày. rows = [{day, open, active}] tính bằng giây. */
  function attachUsage(r, rows) {
    if (!U) return;
    const u = U.summarize(rows, U.isoOf(r.from), U.isoOf(r.to));
    r.usage = u;
    r.days.forEach((d) => { const x = u.byDay[U.isoOf(d.t)]; d.open = x ? x.open : 0; d.active = x ? x.active : 0; d.brk = x ? x.brk : 0; });
  }
  const usageText = (open, active) => `Mở app ${fmtDur(open)} · dùng thực ${fmtDur(active)} · ngắt quãng ${fmtDur(open - active)}`;
  function usageBox(r) {
    const u = r.usage;
    if (!u) return null;
    const tile = (label, v, cls) => h('div', { class: 'ut ' + cls }, h('small', {}, label), h('b', {}, fmtDur(v)));
    return h('div', { class: 'goal-box usage-box' }, h('h2', {}, 'Thời gian dùng app'),
      h('div', { class: 'ut-row' }, tile('Mở app', u.open, 'ut-open'), tile('Dùng thực', u.active, 'ut-act'), tile('Ngắt quãng', u.brk, 'ut-brk')),
      h('p', { class: 'meta' }, u.open ? 'Mở app: Từ lúc mở đến lúc đóng. Dùng thực: App đang hiện trên màn hình và có thao tác. Ngắt quãng: Lúc thu nhỏ, chuyển sang app khác hoặc lâu không thao tác. Chỉ là ước lượng, tính cả các môn.' : 'Chưa có dữ liệu thời gian trong khoảng này (cần cập nhật bản mới trên máy của con).'));
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
    if (window.VungProgressSync) window.VungProgressSync.schedule();
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
    box.append(h('p', {}, `Hôm nay: ${p.todayDone}/${p.todayGoal} câu${p.todayDone >= p.todayGoal ? ' – đạt mục tiêu!' : ''}`), bar(p.todayDone, p.todayGoal));
    box.append(h('p', { class: 'meta' }, 'Chất lượng hôm nay'), qualityBar(p.todayCorrect, p.todayDone, true));
    box.append(h('p', {}, `Tuần này: ${p.daysDone}/${g.weekly} ngày học${p.daysDone >= g.weekly ? ' – đạt mục tiêu!' : ''}`), bar(p.daysDone, g.weekly));
    box.append(h('p', { class: 'meta' }, `Điểm: Hôm nay ${p.todayPts} · 7 ngày ${p.weekPts} · tổng ${p.totalPts}`));
    const mk = (opts, cur, label) => {
      const sel = h('select', { 'aria-label': label });
      (opts.includes(cur) ? opts : opts.concat(cur).sort((a, b) => a - b)).forEach((o) => { const op = h('option', { value: o }, String(o)); if (o === cur) op.selected = true; sel.append(op); });
      return sel;
    };
    const d = mk([20, 30, 40, 50, 60, 80, 100], g.daily, 'Số câu mỗi ngày thường (thứ 2 đến thứ 6)');
    const we = mk([60, 80, 90, 100, 120, 150], g.weekend, 'Số câu mỗi ngày cuối tuần (thứ 7, chủ nhật)');
    const w = mk([1, 2, 3, 4, 5, 6, 7], g.weekly, 'Số ngày học mỗi tuần');
    const apply = async () => {
      const ui = window.VungPinUI;
      if (ui && !(await ui.ensureUnlocked())) { renderGoals(box, grade); return; }
      P.save(store(), P.setGoals(P.load(store()), { daily: d.value, weekend: we.value, weekly: w.value })); renderGoals(box, grade);
    };
    d.addEventListener('change', apply); we.addEventListener('change', apply); w.addEventListener('change', apply);
    box.append(h('p', { class: 'goal-set' }, 'Đặt mục tiêu: Thứ 2–6 ', d, ' câu/ngày; thứ 7, CN ', we, ' câu/ngày; ', w, ' ngày học/tuần'));

    /* Ngưỡng đạt: dưới ngưỡng thì báo "không đạt". Chung cho mọi môn, có thể đặt riêng từng môn đã học. */
    const PASS = [50, 60, 70, 75, 80, 85, 90, 95, 100];
    const mkPass = (cur, label) => {
      const sel = h('select', { 'aria-label': label });
      (PASS.includes(cur) ? PASS : PASS.concat(cur).sort((a, b) => a - b)).forEach((o) => { const op = h('option', { value: o }, o + '%'); if (o === cur) op.selected = true; sel.append(op); });
      return sel;
    };
    const savePass = async (mut) => {
      const ui = window.VungPinUI;
      if (ui && !(await ui.ensureUnlocked())) { renderGoals(box, grade); return; }
      const cur = P.load(store());
      const ng = Object.assign({}, cur.goals, { passBy: Object.assign({}, cur.goals.passBy) });
      mut(ng);
      P.save(store(), P.setGoals(cur, ng)); renderGoals(box, grade);
    };
    const pg = mkPass(g.pass, 'Ngưỡng đạt chung cho mọi môn');
    pg.addEventListener('change', () => savePass((ng) => { ng.pass = Number(pg.value); }));
    box.append(h('p', { class: 'goal-set' }, 'Ngưỡng đạt (dưới mức này báo "không đạt"): chung ', pg, ' số câu đúng'));
    /* Riêng từng môn: hiện tất cả các môn của lớp (không chỉ môn đã học), chọn xong bấm "Lưu ngưỡng". */
    const subs = Object.keys(SUBJ).filter((sj) => sj !== 'gdktpl' || !grade || grade >= 10);
    const grid = h('div', { class: 'pass-grid' });
    const sels = {};
    subs.forEach((sj) => {
      sels[sj] = mkPass(P.passFor(g, sj), 'Ngưỡng đạt môn ' + subjName(sj));
      grid.append(h('label', {}, subjName(sj) + ' ', sels[sj]));
    });
    const save = h('button', { type: 'button' }, 'Lưu ngưỡng từng môn');
    save.addEventListener('click', async () => {
      await savePass((ng) => {
        subs.forEach((sj) => { const v = Number(sels[sj].value); if (v === ng.pass) delete ng.passBy[sj]; else ng.passBy[sj] = v; }); // bằng ngưỡng chung thì không cần đặt riêng
      });
    });
    box.append(h('p', { class: 'goal-set' }, 'Riêng từng môn (chọn xong bấm Lưu):'), grid, h('p', { class: 'goal-set' }, save));
    rewardSettings(box, grade, data);
  }

  /* Phần thưởng theo tuần: học sinh không thấy nội dung; phụ huynh mở bằng mã PIN. */
  function rewardSettings(box, grade, data) {
    const wrap = h('div', { class: 'reward-set' });
    const open = h('button', { type: 'button' }, 'Phần thưởng cuối tuần (dành cho phụ huynh)');
    open.addEventListener('click', async () => {
      const ui = window.VungPinUI;
      if (ui && !(await ui.ensureUnlocked())) return;
      open.remove(); rewardForm(wrap, box, grade);
    });
    wrap.append(open); box.append(wrap);
  }
  function rewardForm(wrap, box, grade) {
    const data = P.load(store()); const R = P.cleanReward(data.reward);
    const st = P.rewardState(data);
    wrap.append(h('h3', {}, 'Phần thưởng theo tuần'), h('p', { class: 'meta' }, 'Con không nhìn thấy nội dung thưởng. Cuối tuần (hoặc khi đủ ngày) con sẽ thấy lời chúc mừng; nếu hụt sẽ thấy lời động viên.'));
    const on = h('input', { type: 'checkbox' }); on.checked = R.on;
    const days = h('input', { type: 'number', min: 1, max: 7, value: R.days, 'aria-label': 'Số ngày đạt trong tuần' });
    const pct = h('input', { type: 'number', min: 10, max: 100, value: R.pct, 'aria-label': 'Ngưỡng mỗi ngày (%)' });
    const text = h('input', { type: 'text', maxlength: 80, value: R.text, placeholder: 'Ví dụ: 30 phút chơi game vào cuối tuần', 'aria-label': 'Phần thưởng' });
    const refresh = () => renderGoals(box, grade);
    const gate = async () => { const ui = window.VungPinUI; return !ui || (await ui.ensureUnlocked()); };
    const sync = () => { if (window.VungProgressSync && window.VungProgressSync.schedule) window.VungProgressSync.schedule(); };
    const save = h('button', { type: 'button' }, 'Lưu phần thưởng');
    save.addEventListener('click', async () => {
      if (!(await gate())) return;
      const d = P.load(store()); P.save(store(), P.setReward(d, { on: on.checked, days: days.value, pct: pct.value, text: text.value })); sync(); refresh();
    });
    wrap.append(
      h('p', { class: 'goal-set' }, h('label', {}, on, ' Bật phần thưởng')),
      h('p', { class: 'goal-set' }, 'Mỗi tuần (thứ 2 đến chủ nhật) đạt ít nhất ', days, ' ngày, mỗi ngày đúng từ ', pct, '% số câu → thưởng:'),
      h('p', { class: 'goal-set' }, text), h('p', { class: 'goal-set' }, save));
    if (R.on) {
      wrap.append(h('p', { class: 'meta' }, `Tuần này: ${st.count}/${st.days} ngày đạt. Bắt đầu tính từ ${R.from.split('-').reverse().join('/')}.`));
      if (st.pending) {
        const give = h('button', { type: 'button', class: 'give-reward' }, 'Đã trao thưởng');
        give.addEventListener('click', async () => { if (!(await gate())) return; P.save(store(), P.giveReward(P.load(store()))); sync(); refresh(); });
        wrap.append(h('p', {}, h('strong', {}, `Con đạt thưởng ${st.pending} tuần, chưa trao${R.text ? ': ' + R.text : ''}. `), give));
      }
    }
    if (R.hist.length) {
      const ul = h('ul', { class: 'report-list' });
      R.hist.slice().reverse().slice(0, 6).forEach((x) => ul.append(h('li', {}, `Tuần ${x.week.split('-').reverse().join('/')}: ${x.ok ? (x.done ? 'đạt, đã trao' : 'đạt, chưa trao') : 'không đạt'} (${x.count}/${R.days} ngày)`)));
      wrap.append(h('p', { class: 'meta' }, 'Kết quả các tuần'), ul);
    }
  }

  /* Hiệu ứng báo kết quả cho học sinh: pháo giấy khi đạt, mặt buồn khi hụt. */
  let rewardShowing = false;
  function confetti(canvas) {
    const ctx = canvas.getContext('2d'); const W = (canvas.width = canvas.offsetWidth); const H = (canvas.height = canvas.offsetHeight);
    const cols = ['#f94144', '#f8961e', '#f9c74f', '#90be6d', '#43aa8b', '#577590', '#b5179e'];
    const ps = Array.from({ length: 140 }, () => ({ x: Math.random() * W, y: -Math.random() * H, r: 4 + Math.random() * 6, c: cols[(Math.random() * cols.length) | 0], vy: 2 + Math.random() * 3, vx: -1.5 + Math.random() * 3, a: Math.random() * 6, va: -0.2 + Math.random() * 0.4 }));
    let t0 = null;
    (function frame(ts) {
      if (!canvas.isConnected) return;
      if (t0 === null) t0 = ts; if (ts - t0 > 6000) { ctx.clearRect(0, 0, W, H); return; }
      ctx.clearRect(0, 0, W, H);
      ps.forEach((p) => { p.x += p.vx; p.y += p.vy; p.a += p.va; if (p.y > H) { p.y = -10; p.x = Math.random() * W; } ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.c; ctx.fillRect(-p.r, -p.r / 2, p.r * 2, p.r); ctx.restore(); });
      requestAnimationFrame(frame);
    })(0);
  }
  function showRewardNotice(x, text, next) {
    const win = x.ok;
    const ov = h('div', { class: 'reward-ov', role: 'dialog', 'aria-modal': 'true' });
    const card = h('div', { class: 'reward-card ' + (win ? 'win' : 'lose') },
      h('div', { class: 'reward-emoji', 'aria-hidden': 'true' }, win ? '🎉' : '😢'),
      h('p', { class: 'reward-msg' }, win
        ? (text ? `Chúc mừng! Bạn được ${text}.` : 'Chúc mừng! Bạn đã đạt phần thưởng tuần này.')
        : 'Rất tiếc, tuần này bạn đã đánh rơi phần thưởng. Cố gắng vào tuần sau nhé!'));
    const ok = h('button', { type: 'button' }, win ? 'Tuyệt vời!' : 'Mình sẽ cố gắng');
    ok.addEventListener('click', () => { ov.remove(); const d = P.load(store()); P.save(store(), P.markShown(d, x.week)); if (window.VungProgressSync && window.VungProgressSync.schedule) window.VungProgressSync.schedule(); next(); });
    card.append(ok); ov.append(card);
    if (win && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) { const cv = h('canvas', { class: 'reward-confetti', 'aria-hidden': 'true' }); ov.prepend(cv); document.body.append(ov); confetti(cv); } else document.body.append(ov);
    ok.focus();
  }
  function checkReward() {
    if (!P || rewardShowing || window.VungProgressUI.parentOnly) return;
    const data = P.load(store());
    const pend = P.evaluate(data, Date.now());
    P.save(store(), data);
    if (!pend.length) return;
    const text = P.cleanReward(data.reward).text;
    rewardShowing = true;
    const queue = pend.slice().sort((a, b) => a.week.localeCompare(b.week));
    const step = () => {
      const x = queue.shift();
      if (!x) { rewardShowing = false; return; }
      showRewardNotice(x, text, step);
    };
    step();
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
          (lesson.theory || []).forEach((t) => {
            if (t.type === 'formula') kids.push(h('p', { class: 'formula' }, t.content));
            // Lý thuyết dạng thẻ: lấy tóm tắt và công thức, bỏ ký hiệu tô màu {s …}.
            else if (t.type === 'summary') kids.push(h('div', { class: 'kt-line' }, String(t.content).replace(/\{[svck] ([^}]+)\}/g, '$1')));
            else if (t.type === 'card') (t.formulas || []).forEach((f) => kids.push(h('p', { class: 'formula' }, String(f).replace(/\{[svck] ([^}]+)\}/g, '$1'))));
          });
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
      if (it.figureSvg) q.append(typeof figureNode === 'function' ? figureNode(it.figureSvg, '') : h('img', { class: 'figure', alt: '', src: figureSrc(it.figureSvg) }));
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
    if (r.usage && r.usage.open) out.push('Thời gian dùng app: ' + usageText(r.usage.open, r.usage.active));
    out.push(r.total ? `Đúng ${r.correct} · Sai ${r.wrong} (${r.pct}% đúng / ${100 - r.pct}% sai, tổng ${r.total} câu)` : 'Chưa có bài nào trong khoảng này');
    r.subjects.forEach((s) => out.push(`${subjName(s.subject)} lớp ${s.grade}: Đúng ${s.correct}, sai ${s.wrong} (${s.pct}% đúng) – ${s.passed ? 'ĐẠT' : 'KHÔNG ĐẠT'} (ngưỡng ${s.need}%)`));
    if (r.weak.length) {
      out.push('Cần ôn thêm:');
      r.weak.forEach((c) => out.push(`  • ${c.name} (${subjName(c.subject)} ${c.grade}) – ${c.pct}%`));
    } else if (r.total) out.push('Chưa có chương nào dưới ngưỡng đạt.');
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
    g.fillText('Xanh: Đúng · Đỏ: Sai · Dữ liệu lưu trên máy của học sinh', 36, c.height - 24);
    return c;
  }

  /* Biểu đồ cột: mỗi ngày một cột xếp chồng (xanh = đúng, đỏ = sai), cao theo số câu, ghi % đúng phía trên.
     Chạm vào một cột thì chi tiết ngày đó hiện ra bên dưới. Dùng cùng lúc với lịch khi có từ 2 ngày. */
  function dayChart(r) {
    const max = Math.max(1, ...r.days.map((d) => d.total));
    const many = r.days.length > 14;
    const step = r.days.length <= 14 ? 1 : Math.ceil(r.days.length / 10);
    const root = h('div', { class: 'dc-root' });
    const wrap = h('div', { class: 'dchart' + (many ? ' many' : ''), role: 'group', 'aria-label': 'Biểu đồ số câu đúng và sai theo từng ngày; chạm vào cột để xem chi tiết' });
    const detail = h('div', { class: 'dc-detail', 'aria-live': 'polite' }, h('p', { class: 'meta' }, 'Chạm vào một cột để xem chi tiết ngày đó.'));
    const cols = [];
    const show = (i) => {
      const d = r.days[i];
      cols.forEach((c, j) => c.classList.toggle('sel', j === i));
      detail.replaceChildren(h('h3', {}, fmtFull(d.t)));
      if (d.open) detail.append(h('p', {}, usageText(d.open, d.active)));
      if (!d.total) { detail.append(h('p', { class: 'meta' }, 'Chưa làm bài nào trong ngày này.')); return; }
      detail.append(h('p', {}, `Đúng ${d.correct} · Sai ${d.wrong} (${d.pct}% đúng), tổng ${d.total} câu trong ${d.lessons} bài${d.reached ? ' · đạt mục tiêu' : ''}`), qualityBar(d.correct, d.total, false));
      (d.subjects || []).forEach((s) => detail.append(h('p', {}, `${subjName(s.subject)} lớp ${s.grade}: ${s.correct}/${s.total} câu (${s.pct}%) · `,
        h('strong', { class: s.passed ? 'pass-ok' : 'pass-bad' }, s.passed ? `Đạt (ngưỡng ${s.need}%)` : `Không đạt (ngưỡng ${s.need}%)`))));
    };
    r.days.forEach((d, i) => {
      const dt = new Date(d.t);
      const col = h('button', { type: 'button', class: 'dc-col', 'aria-label': d.total ? `${fmtFull(d.t)}: ${d.pct}% đúng, ${d.total} câu` : `${fmtFull(d.t)}: Chưa học` });
      col.append(h('span', { class: 'dc-n' }, d.total && !many ? `${d.pct}%` : '\u00a0'));
      const bar = h('div', { class: 'dc-bar' });
      if (d.total) {
        const hh = Math.max(4, Math.round((100 * d.total) / max));
        const stack = h('div', { class: 'dc-stack', style: `height:${hh}%` });
        if (d.wrong) stack.append(h('div', { class: 'q-bad', style: `flex:${d.wrong}` }));
        if (d.correct) stack.append(h('div', { class: 'q-ok', style: `flex:${d.correct}` }));
        bar.append(stack);
      }
      col.append(bar, h('small', {}, i % step === 0 ? dt.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' }) : '\u00a0'));
      col.addEventListener('click', () => show(i));
      cols.push(col); wrap.append(col);
    });
    root.append(wrap, detail);
    return root;
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
      if (d.active) cell.append(h('small', {}, 'Dùng ' + fmtDur(d.active)));
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
    attachUsage(r, U ? U.list() : []);
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
    const ub = usageBox(r); if (ub) body.append(ub);
    if (r.days.length > 1 || r.total) {
      body.append(h('h2', { class: 'rep-h' }, 'Biểu đồ theo ngày'), h('div', { class: 'goal-box' }, dayChart(r), h('p', { class: 'meta' }, 'Xanh: Câu đúng · Đỏ: Câu sai')), h('h2', { class: 'rep-h' }, r.days.length <= 7 ? 'Lịch tuần' : 'Lịch học'), calendar(r, today));
    }
    if (r.subjects.length) {
      const box = h('div', { class: 'goal-box' }, h('h2', {}, 'Theo môn học'));
      r.subjects.forEach((s) => box.append(h('p', {}, `${subjName(s.subject)} lớp ${s.grade}: ${s.lessons} bài · `, h('strong', { class: s.passed ? 'pass-ok' : 'pass-bad' }, s.passed ? `Đạt (${s.pct}% ≥ ${s.need}%)` : `Không đạt (${s.pct}% < ${s.need}%)`)), qualityBar(s.correct, s.total, true)));
      body.append(box);
    }
    const ul = h('ul', { class: 'report-list' });
    lines(r).forEach((t) => ul.append(h('li', {}, t.replace(/^\s*•\s*/, ''))));
    body.append(ul);
    const book = grade ? data.notebook.filter((n) => n.grade === grade) : data.notebook;
    body.append(h('p', { class: 'meta' }, `Sổ câu sai: ${book.length} câu, ${P.due(data, now, grade).length} câu đến hạn ôn`));
    body.append(h('div', { class: 'goal-box', id: 'goal-box-report' }));
    renderGoals(document.getElementById('goal-box-report') || body.lastChild, grade);
    const syncBox = h('div', { class: 'goal-box' });
    body.append(syncBox);
    if (window.VungProgressSync && !window.VungProgressUI.parentOnly) window.VungProgressSync.renderBox(syncBox, () => renderReport(body, grade));
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

  /* ---------- Phụ huynh xem trên điện thoại (dữ liệu do máy tính của học sinh gửi lên) ---------- */
  const PV_KEY = 'vungbai.parentview.v1';
  const pvLoad = () => { try { return JSON.parse(store().getItem(PV_KEY) || '{}') || {}; } catch (e) { return {}; } };
  const pvSave = (v) => { try { v ? store().setItem(PV_KEY, JSON.stringify(v)) : store().removeItem(PV_KEY); } catch (e) { /* bỏ qua */ } };
  const pvView = { period: '7', subject: '', grade: 0, from: null, to: null };

  function renderParentView(body, notice) {
    body.replaceChildren();
    const S = window.VungProgressSync;
    const saved = pvLoad();
    body.append(h('h1', {}, 'Xem con học'));
    if (!saved.code || !saved.phone) {
      body.append(h('p', { class: 'meta' }, 'Nhập mã đơn và số điện thoại đã dùng khi mua để xem kết quả học do máy tính của con gửi lên.'));
      const code = h('input', { type: 'text', maxlength: '14', placeholder: 'Mã đơn, ví dụ 3KAHFK', autocomplete: 'off', 'aria-label': 'Mã đơn' });
      const phone = h('input', { type: 'tel', maxlength: '14', placeholder: 'Số điện thoại đã mua', autocomplete: 'off', 'aria-label': 'Số điện thoại đã mua' });
      const msg = h('p', { class: 'meta', role: 'status' }, notice || '');
      const go = h('button', { type: 'button', class: 'primary' }, 'Xem kết quả');
      go.addEventListener('click', () => {
        const c = code.value.toUpperCase().replace(/[^A-Z0-9]/g, '').replace(/^NL(?=[A-Z0-9]{6}$)/, '');
        const p = phone.value.replace(/[\s.\-]/g, '');
        if (!/^[A-Z0-9]{6}$/.test(c) || !/^(0|\+84)\d{9}$/.test(p)) { msg.textContent = 'Kiểm tra lại mã đơn (6 ký tự) và số điện thoại.'; return; }
        pvSave({ code: c, phone: p }); renderParentView(body);
      });
      body.append(h('div', { class: 'license-form' }, code, phone, go), msg);
      return;
    }
    const msg = h('p', { class: 'meta', role: 'status' }, 'Đang tải...');
    body.append(msg);
    const now = Date.now(); const today = new Date(now).setHours(0, 0, 0, 0);
    const rg = rangeOf(pvView.period, now, pvView.from, pvView.to);
    window.vungBai.progressView({ code: saved.code, phone: saved.phone, from: S.isoOf(rg.from), to: S.isoOf(rg.to), grade: pvView.grade }).then((res) => {
      if (!res.ok) {
        if (res.offline) { msg.textContent = 'Không có mạng. Vui lòng thử lại.'; body.append(h('button', { type: 'button' }, 'Thử lại')); body.lastChild.addEventListener('click', () => renderParentView(body)); return; }
        pvSave(null); renderParentView(body, res.error || 'Không xem được.'); return;
      }
      const d = res.data; const rerender = () => renderParentView(body);
      msg.remove();
      body.append(h('p', { class: 'meta' }, `${d.name ? d.name + ' · ' : ''}Đơn ${d.code}${d.lastSync ? ' · cập nhật lúc ' + new Date(d.lastSync).toLocaleString('vi-VN') : ''}`));
      if (!d.enabled) {
        body.append(h('div', { class: 'goal-box' }, h('p', {}, 'Chưa có dữ liệu. Trên máy tính của con, vào "Báo cáo cho phụ huynh" và bật "Cho phụ huynh xem trên điện thoại".')));
      } else {
        const perSel = h('select', { 'aria-label': 'Khoảng thời gian' });
        PERIODS.forEach(([k, t]) => { const o = h('option', { value: k }, t); if (k === pvView.period) o.selected = true; perSel.append(o); });
        perSel.addEventListener('change', () => { pvView.period = perSel.value; if (pvView.period === 'custom' && pvView.from == null) { pvView.from = rg.from; pvView.to = rg.to; } rerender(); });
        const ctl = h('div', { class: 'rep-ctl' }, h('label', {}, 'Thời gian ', perSel));
        if (d.courses.length > 1) {
          const cs = h('select', { 'aria-label': 'Khóa học' }); cs.append(h('option', { value: '0' }, 'Tất cả các khóa'));
          d.courses.forEach((c) => { const o = h('option', { value: String(c.grade) }, c.name); if (c.grade === pvView.grade) o.selected = true; cs.append(o); });
          cs.addEventListener('change', () => { pvView.grade = Number(cs.value); rerender(); });
          ctl.append(h('label', {}, 'Khóa học ', cs));
        } else if (pvView.grade) pvView.grade = 0;
        const subs = [...new Set(d.rows.map((r) => r.subject))];
        const ss = h('select', { 'aria-label': 'Môn học' }); ss.append(h('option', { value: '' }, 'Tất cả môn'));
        subs.forEach((k) => { const o = h('option', { value: k }, subjName(k)); if (k === pvView.subject) o.selected = true; ss.append(o); });
        ss.addEventListener('change', () => { pvView.subject = ss.value; rerender(); });
        ctl.append(h('label', {}, 'Môn học ', ss));
        if (pvView.period === 'custom') {
          const f = h('input', { type: 'date', value: iso(rg.from), max: iso(today), 'aria-label': 'Từ ngày' });
          const t = h('input', { type: 'date', value: iso(rg.to), max: iso(today), 'aria-label': 'Đến ngày' });
          const onDate = () => { if (f.value && t.value) { pvView.from = fromIso(f.value); pvView.to = fromIso(t.value); rerender(); } };
          f.addEventListener('change', onDate); t.addEventListener('change', onDate);
          ctl.append(h('label', {}, 'Từ ', f), h('label', {}, 'Đến ', t));
        }
        body.append(ctl);
        const r = S.buildReport(d.rows, { from: rg.from, to: rg.to, subject: pvView.subject, grade: pvView.grade }, d.goals);
        body.append(h('p', { class: 'meta' }, `${fmtFull(r.from)} → ${fmtFull(r.to)}`));
        attachUsage(r, d.usage || []);
        /* Phần thưởng: mỗi bé (mỗi khóa/máy) một khối riêng; chọn khóa học ở trên thì chỉ hiện bé thuộc khóa đó. */
        const rws = (d.rewards || (d.reward && d.reward.on ? [d.reward] : [])).filter((x) => x.on && (!pvView.grade || !x.grades || !x.grades.length || x.grades.includes(pvView.grade)));
        rws.forEach((rw) => {
          const box = h('div', { class: 'goal-box' }, h('h2', {}, 'Phần thưởng cuối tuần' + (rws.length > 1 && rw.label ? ' · ' + rw.label : '')),
            h('p', {}, `Tuần này: ${rw.count}/${rw.need} ngày đạt ${rw.pct}%${rw.text ? ' · Thưởng: ' + rw.text : ''}`), bar(Math.min(rw.count, rw.need), rw.need));
          if (rw.pending) box.append(h('p', {}, h('strong', {}, `🎁 Con đạt thưởng ${rw.pending} tuần, chờ bố mẹ trao.`), ' Sau khi trao, bấm "Đã trao" trong báo cáo trên máy của con.'));
          const done = (rw.hist || []).slice().reverse().slice(0, 4);
          if (done.length) { const ul = h('ul', { class: 'report-list' }); done.forEach((x) => ul.append(h('li', {}, `Tuần ${x.week.split('-').reverse().join('/')}: ${x.ok ? (x.done ? 'đạt, đã trao' : 'đạt, chưa trao') : 'không đạt'} (${x.count}/${rw.need} ngày)`))); box.append(ul); }
          body.append(box);
        });
        body.append(h('div', { class: 'goal-box' }, h('h2', {}, 'Chất lượng làm bài'), qualityBar(r.correct, r.total, true)));
        const ub = usageBox(r); if (ub) body.append(ub);
        if (r.days.length > 1 || r.total) body.append(h('h2', { class: 'rep-h' }, 'Biểu đồ theo ngày'), h('div', { class: 'goal-box' }, dayChart(r), h('p', { class: 'meta' }, 'Xanh: Câu đúng · Đỏ: Câu sai')), h('h2', { class: 'rep-h' }, r.days.length <= 7 ? 'Lịch tuần' : 'Lịch học'), calendar(r, today));
        if (r.subjects.length) {
          const box = h('div', { class: 'goal-box' }, h('h2', {}, 'Theo môn học'));
          r.subjects.forEach((s) => box.append(h('p', {}, `${subjName(s.subject)} lớp ${s.grade}: ${s.lessons} bài · `, h('strong', { class: s.passed ? 'pass-ok' : 'pass-bad' }, s.passed ? `Đạt (${s.pct}% ≥ ${s.need}%)` : `Không đạt (${s.pct}% < ${s.need}%)`)), qualityBar(s.correct, s.total, true)));
          body.append(box);
        }
        const ul = h('ul', { class: 'report-list' });
        lines(r).forEach((t) => ul.append(h('li', {}, t.replace(/^\s*•\s*/, ''))));
        body.append(ul);
      }
      const out = h('button', { type: 'button' }, 'Đổi đơn khác / Thoát');
      out.addEventListener('click', () => { pvSave(null); renderParentView(body); });
      body.append(out);
    });
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
    checkReward();
  }

  window.VungProgressUI = { scope: 0, renderGoals, record, renderReview, renderReport, renderParentView, refreshBadge, dueCount, checkReward };
})();
