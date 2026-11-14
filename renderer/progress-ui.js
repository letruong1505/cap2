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

  function dueCount() { return P ? P.due(P.load(store())).length : 0; }

  /* ---------- Sổ câu sai ---------- */
  function renderReview(body) {
    body.replaceChildren();
    const data = P.load(store());
    const list = P.due(data);
    body.append(h('h1', {}, 'Sổ câu sai'));
    if (!data.notebook.length) {
      body.append(h('p', { class: 'meta' }, 'Chưa có câu sai nào. Khi làm bài và bấm "Kiểm tra toàn bài", các câu sai sẽ được lưu ở đây để ôn lại.'));
      return;
    }
    body.append(h('p', { class: 'meta' }, `Trong sổ có ${data.notebook.length} câu, ${list.length} câu đến hạn ôn hôm nay. Làm đúng ba lần cách quãng 1, 3, 7 ngày thì câu được xóa khỏi sổ.`));
    if (!list.length) {
      const next = Math.min(...data.notebook.map((n) => n.due));
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
    out.push(`Số ngày học trong 7 ngày: ${w.days}/7`);
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
    g.fillText('Báo cáo tuần – Nam Linh Educenter', 36, 52);
    g.font = '22px sans-serif';
    g.fillText(`${name ? name + ' · ' : ''}${fmtDate(w.from)} – ${fmtDate(w.to)}`, 36, 88);
    g.fillStyle = '#222'; g.font = '24px sans-serif';
    L.forEach((t, i) => g.fillText(t, 36, 160 + i * 44));
    g.fillStyle = '#888'; g.font = '18px sans-serif';
    g.fillText('Dữ liệu lưu trên máy của học sinh', 36, c.height - 24);
    return c;
  }

  function renderReport(body) {
    body.replaceChildren();
    const w = P.weekly(P.load(store()));
    body.append(h('h1', {}, 'Báo cáo tuần cho phụ huynh'));
    body.append(h('p', { class: 'meta' }, `7 ngày gần nhất: ${fmtDate(w.from)} – ${fmtDate(w.to)}`));
    const ul = h('ul', { class: 'report-list' });
    lines(w).forEach((t) => ul.append(h('li', {}, t.replace(/^\s*•\s*/, ''))));
    body.append(ul);
    const nameIn = h('input', { type: 'text', placeholder: 'Tên học sinh (không bắt buộc)', autocomplete: 'off', 'aria-label': 'Tên học sinh' });
    const btn = h('button', { type: 'button', class: 'primary' }, 'Lưu ảnh báo cáo gửi Zalo');
    const msg = h('p', { class: 'meta' });
    btn.addEventListener('click', () => {
      drawPng(w, nameIn.value.trim()).toBlob((blob) => {
        if (!blob) { msg.textContent = 'Không tạo được ảnh.'; return; }
        const a = h('a', { download: `bao-cao-tuan-${new Date().toISOString().slice(0, 10)}.png`, href: URL.createObjectURL(blob) });
        document.body.append(a); a.click(); a.remove();
        msg.textContent = 'Đã tạo ảnh báo cáo. Chọn nơi lưu rồi gửi cho phụ huynh qua Zalo.';
      }, 'image/png');
    });
    body.append(nameIn, btn, msg);
  }

  function refreshBadge() {
    const n = dueCount();
    const b = document.getElementById('open-review');
    if (b) b.textContent = n ? `Sổ câu sai (${n} câu cần ôn)` : 'Sổ câu sai';
  }

  window.VungProgressUI = { record, renderReview, renderReport, refreshBadge, dueCount };
})();
