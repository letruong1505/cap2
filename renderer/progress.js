/* Tiến độ học tập: nhật ký làm bài, sổ câu sai (ôn cách quãng 1/3/7 ngày), báo cáo tuần.
   Logic thuần, không phụ thuộc DOM; lưu trữ qua localStorage nếu có. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VungProgress = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const KEY = 'vungbai.progress.v1';
  const DAY = 86400000;
  const INTERVALS = [1, 3, 7]; // ngày cho các hộp 0,1,2; qua hộp 2 là thuộc
  const MAX_ATTEMPTS = 1000;
  const MAX_NOTEBOOK = 300;

  const DEFAULT_PASS = 80; // ngưỡng đạt mặc định: dưới 80% câu đúng thì báo không đạt
  const DEFAULT_GOALS = { daily: 50, weekend: 80, weekly: 5, pass: DEFAULT_PASS, passBy: {} }; // T2–T6: 50 câu/ngày; T7, CN: 80 câu/ngày; 5 ngày học/tuần
  function empty() { return { attempts: [], notebook: [], reviews: [], goals: Object.assign({}, DEFAULT_GOALS, { passBy: {} }), reward: cleanReward({}) }; }

  /* Điểm thang 10 của một bài (làm tròn 1 chữ số). */
  function score10(correct, total) { return total ? Math.round((correct / total) * 100) / 10 : 0; }
  /* Điểm thưởng: 10/câu đúng, thêm 20 nếu bài từ 5 câu đạt từ 90%. Ôn sổ câu sai: 5/câu đúng. */
  function points(correct, total) { return correct * 10 + (total >= 5 && correct / total >= 0.9 ? 20 : 0); }
  const REVIEW_PTS = 5;
  function clampInt(v, lo, hi, d) { v = Math.round(Number(v)); return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : d; }
  function setGoals(data, g) {
    const old = data.goals || {};
    g = Object.assign({}, { pass: old.pass, passBy: old.passBy }, g); // không nhắc tới ngưỡng đạt thì giữ nguyên
    data.goals = {
      daily: clampInt(g.daily, 5, 200, DEFAULT_GOALS.daily),
      weekend: clampInt(g.weekend, 5, 200, DEFAULT_GOALS.weekend),
      weekly: clampInt(g.weekly, 1, 7, DEFAULT_GOALS.weekly),
      pass: clampInt(g.pass, 10, 100, DEFAULT_PASS),
      passBy: cleanPassBy(g.passBy),
    };
    return data;
  }
  /* Phần thưởng theo tuần (Chủ nhật đến thứ Bảy): đạt ít nhất `days` ngày trong tuần, mỗi ngày đúng từ `pct`% số câu thì được `text`.
     Học sinh KHÔNG thấy nội dung thưởng; chỉ thấy lời chúc mừng khi đạt hoặc lời tiếc khi hụt.
     from = Chủ nhật đầu tiên được tính (tuần sau khi bật). hist = kết quả từng tuần: { week, ok, count, shown, done }. */
  const DAY_RE = /^\d{4}-\d{2}-\d{2}$/;
  function cleanReward(r) {
    r = r && typeof r === 'object' ? r : {};
    return {
      on: r.on === true,
      days: clampInt(r.days, 1, 7, 7),
      pct: clampInt(r.pct, 10, 100, 70),
      text: String(r.text || '').replace(/\s+/g, ' ').trim().slice(0, 80),
      from: DAY_RE.test(String(r.from || '')) ? String(r.from) : '',
      hist: (Array.isArray(r.hist) ? r.hist : []).filter((x) => x && DAY_RE.test(String(x.week))).slice(-30)
        .map((x) => ({ week: String(x.week), ok: x.ok === true, count: clampInt(x.count, 0, 7, 0), shown: x.shown === true, done: x.done === true })),
    };
  }
  function isoLocal(t) { const d = new Date(t); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function weekStart(t) { const d = new Date(t); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - d.getDay()); return d.getTime(); }  /* tuần từ Chủ nhật đến thứ Bảy */
  function addDays(t, n) { const d = new Date(t); d.setDate(d.getDate() + n); return d.getTime(); }
  /* Bật lần đầu thì bắt đầu tính từ Chủ nhật tuần sau; tắt thì xóa mốc. */
  function setReward(data, r) {
    const old = cleanReward(data.reward); const n = cleanReward(Object.assign({}, old, r));
    if (!n.on) n.from = '';
    else if (!old.on || !n.from) n.from = isoLocal(addDays(weekStart(Date.now()), 7));
    data.reward = n;
    return data;
  }
  /* Số ngày đạt trong tuần bắt đầu ngày weekStartMs. Ngày đạt: có làm bài và tổng số câu đúng ≥ pct% (gộp mọi môn, mọi lớp). */
  function weekCount(data, wStart) {
    const r = cleanReward(data.reward); const byDay = {};
    (data.attempts || []).forEach((a) => { const k = isoLocal(a.t); const x = byDay[k] || (byDay[k] = { c: 0, n: 0 }); x.c += a.correct; x.n += a.total; });
    let n = 0;
    for (let i = 0; i < 7; i++) { const x = byDay[isoLocal(addDays(wStart, i))]; if (x && x.n > 0 && (100 * x.c) / x.n >= r.pct) n++; }
    return n;
  }
  /* Chốt kết quả các tuần đã tính: tuần đã qua thì đạt/hụt; tuần hiện tại đạt đủ số ngày thì thắng ngay. Trả về các kết quả chưa báo cho học sinh. */
  function evaluate(data, now) {
    now = now || Date.now();
    const r = cleanReward(data.reward);
    if (!r.on || !r.from) { data.reward = r; return []; }
    const cur = weekStart(now);
    const have = new Set(r.hist.map((x) => x.week));
    /* mốc cũ (thứ Hai) thì dời sang Chủ nhật kế tiếp để khớp tuần CN–T7 */
    const f0 = new Date(r.from + 'T00:00:00').getTime(); const f1 = weekStart(f0) === f0 ? f0 : addDays(weekStart(f0), 7);
    for (let w = f1, i = 0; w <= cur && i < 60; w = addDays(w, 7), i++) {
      const k = isoLocal(w); if (have.has(k)) continue;
      const count = weekCount(data, w); const ok = count >= r.days;
      if (ok || w < cur) r.hist.push({ week: k, ok, count, shown: false, done: false });
    }
    r.hist = r.hist.slice(-30);
    data.reward = r;
    return r.hist.filter((x) => !x.shown);
  }
  function markShown(data, week) { const r = cleanReward(data.reward); r.hist.forEach((x) => { if (x.week === week) x.shown = true; }); data.reward = r; return data; }
  /* Phụ huynh bấm "Đã trao" cho các tuần thắng chưa trao. */
  function giveReward(data) { const r = cleanReward(data.reward); r.hist.forEach((x) => { if (x.ok) x.done = true; }); data.reward = r; return data; }
  /* Tóm tắt cho phụ huynh/Worker: số ngày đạt tuần này, số tuần thắng chờ trao. */
  function rewardState(data, now) {
    now = now || Date.now();
    const r = cleanReward(data.reward);
    return { on: r.on, days: r.days, pct: r.pct, text: r.text, from: r.from, count: r.on ? weekCount(data, weekStart(now)) : 0, pending: r.hist.filter((x) => x.ok && !x.done).length, hist: r.hist.slice(-12) };
  }

  /* Ngưỡng riêng từng môn: { mã môn: % }, chỉ giữ giá trị hợp lệ. */
  function cleanPassBy(o) {
    const out = {};
    if (o && typeof o === 'object') Object.keys(o).slice(0, 60).forEach((k) => { const v = Math.round(Number(o[k])); if (/^[a-z0-9_-]{1,30}$/i.test(k) && Number.isFinite(v) && v >= 10 && v <= 100) out[k] = v; });
    return out;
  }
  /* Ngưỡng đạt (%) của một môn: riêng của môn nếu có, không thì ngưỡng chung. */
  function passFor(goals, subject) {
    const g = goals || DEFAULT_GOALS;
    const own = g.passBy && g.passBy[subject];
    return own || g.pass || DEFAULT_PASS;
  }
  /* Gắn ngưỡng và kết quả đạt/không đạt vào từng dòng môn (cần ít nhất 1 câu). */
  function markPass(list, goals) {
    list.forEach((x) => { x.need = passFor(goals, x.subject); x.passed = x.total > 0 && x.pct >= x.need; });
    return list;
  }
  /* Mục tiêu số câu của một ngày: T7, CN dùng mục tiêu cuối tuần, còn lại dùng mục tiêu ngày thường. */
  function goalFor(goals, t) {
    const g = goals || DEFAULT_GOALS; const wd = new Date(t).getDay();
    return wd === 0 || wd === 6 ? (g.weekend || DEFAULT_GOALS.weekend) : (g.daily || DEFAULT_GOALS.daily);
  }

  /* Bài cần làm lại: lần làm gần nhất của bài đó chưa đạt ngưỡng của môn (mới nhất trước, tối đa 12). grade: 0 là mọi lớp. */
  function redoList(data, grade) {
    const last = {};
    (data.attempts || []).forEach((a) => {
      if (grade && a.grade !== grade) return;
      if (!a.total) return;
      if (!last[a.lessonId] || a.t >= last[a.lessonId].t) last[a.lessonId] = a;
    });
    return Object.values(last).map((a) => ({
      lessonId: a.lessonId, subject: a.subject, grade: a.grade, lesson: a.lesson, chapter: a.chapter || '', t: a.t,
      pct: Math.round((100 * a.correct) / a.total), need: passFor(data.goals, a.subject),
    })).filter((x) => x.pct < x.need).sort((a, b) => b.t - a.t).slice(0, 12);
  }

  /* Tóm tắt để phụ huynh biết: bài đang cần ôn lại (lần làm gần nhất chưa đạt) và các lần con làm lại bài đã không đạt trước đó
     (trong 30 ngày, mới nhất trước, tối đa 12), kèm % trước và sau để thấy con có tiến bộ không. */
  function redoSummary(data, now) {
    now = now == null ? Date.now() : now;
    const pct = (a) => Math.round((100 * a.correct) / a.total);
    const byLesson = {};
    (data.attempts || []).filter((a) => a.total > 0 && a.lessonId).sort((a, b) => a.t - b.t).forEach((a) => { (byLesson[a.lessonId] = byLesson[a.lessonId] || []).push(a); });
    const done = [];
    Object.values(byLesson).forEach((list) => {
      for (let i = 1; i < list.length; i++) {
        const prev = list[i - 1]; const a = list[i];
        if (pct(prev) >= passFor(data.goals, prev.subject) || a.t < now - 30 * DAY) continue;
        done.push({ subject: a.subject, grade: a.grade, lesson: a.lesson, chapter: a.chapter || '', from: pct(prev), to: pct(a), passed: pct(a) >= passFor(data.goals, a.subject), t: a.t });
      }
    });
    done.sort((x, y) => y.t - x.t);
    const pending = redoList(data, 0).map((x) => ({ subject: x.subject, grade: x.grade, lesson: x.lesson, chapter: x.chapter, pct: x.pct, need: x.need, t: x.t }));
    return { pending, done: done.slice(0, 12) };
  }

  function load(storage) {
    try {
      const raw = storage && storage.getItem(KEY);
      if (!raw) return empty();
      const d = JSON.parse(raw);
      return {
        attempts: Array.isArray(d.attempts) ? d.attempts : [],
        notebook: Array.isArray(d.notebook) ? d.notebook : [],
        reviews: Array.isArray(d.reviews) ? d.reviews : [],
        goals: setGoals({}, d.goals || {}).goals,
        reward: cleanReward(d.reward),
      };
    } catch (e) { return empty(); }
  }

  function save(storage, data) {
    try { if (storage) storage.setItem(KEY, JSON.stringify(data)); } catch (e) { /* bỏ qua */ }
  }

  function slimItem(item) {
    const o = {};
    ['id', 'level', 'type', 'stem', 'answer', 'explain', 'wrong_explain', 'choices', 'concept', 'expr', 'figure', 'reading'].forEach((k) => {
      if (item[k] !== undefined) o[k] = item[k];
    });
    return o;
  }

  /* meta: {subject, grade, lessonId, lesson, chapter, correct, total, seconds}
     wrong: mảng item làm sai; right: mảng item làm đúng (để nâng hộp nếu đang trong sổ) */
  function recordAttempt(data, meta, wrong, right, now) {
    now = now || Date.now();
    data.attempts.push({
      t: now, subject: meta.subject, grade: meta.grade, lessonId: meta.lessonId,
      lesson: meta.lesson, chapter: meta.chapter || '',
      correct: meta.correct, total: meta.total, pts: points(meta.correct, meta.total), seconds: Math.max(0, Math.round(meta.seconds || 0)),
    });
    if (data.attempts.length > MAX_ATTEMPTS) data.attempts.splice(0, data.attempts.length - MAX_ATTEMPTS);

    const key = (it) => meta.lessonId + '#' + it.id;
    // Đáp án em đã nhập hoặc chọn ở lần làm sai gần nhất (null nếu bỏ trống).
    const given = meta.given || {};
    const givenOf = (it) => (given[it.id] === undefined || given[it.id] === null || given[it.id] === '' ? null : String(given[it.id]));
    (wrong || []).forEach((it) => {
      const k = key(it);
      const found = data.notebook.find((n) => n.key === k);
      if (found) { found.box = 0; found.due = now + DAY; found.misses = (found.misses || 1) + 1; found.item = slimItem(it); found.given = givenOf(it); }
      else data.notebook.push({
        key: k, subject: meta.subject, grade: meta.grade, lessonId: meta.lessonId, lesson: meta.lesson,
        chapter: meta.chapter || '', box: 0, due: now + DAY, misses: 1, added: now, item: slimItem(it), given: givenOf(it),
      });
    });
    (right || []).forEach((it) => {
      const found = data.notebook.find((n) => n.key === key(it));
      if (found) grade(data, found.key, true, now);
    });
    if (data.notebook.length > MAX_NOTEBOOK) {
      data.notebook.sort((a, b) => b.added - a.added);
      data.notebook.length = MAX_NOTEBOOK;
    }
    return data;
  }

  /* Trả lời đúng: lên hộp sau; qua hộp cuối thì xóa khỏi sổ. Sai: về hộp 0, hạn ngày mai. */
  function grade(data, key, ok, now) {
    now = now || Date.now();
    const i = data.notebook.findIndex((n) => n.key === key);
    if (i < 0) return;
    const n = data.notebook[i];
    if (ok) { (data.reviews = data.reviews || []).push({ t: now, grade: n.grade }); if (data.reviews.length > MAX_ATTEMPTS) data.reviews.shift(); }
    if (!ok) { n.box = 0; n.due = now + DAY; n.misses = (n.misses || 1) + 1; return; }
    n.box += 1;
    if (n.box >= INTERVALS.length) data.notebook.splice(i, 1);
    else n.due = now + INTERVALS[n.box] * DAY;
  }

  function due(data, now, grade) {
    now = now || Date.now();
    return data.notebook.filter((n) => n.due <= now && (!grade || n.grade === grade)).sort((a, b) => a.due - b.due);
  }

  function startOfDay(t) { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); }

  /* Tiến độ mục tiêu: hôm nay (số câu đã làm) và 7 ngày (số ngày học), cùng tổng điểm. */
  function progress(data, now, grade) {
    now = now || Date.now();
    const ok = (x) => !grade || x.grade === grade;
    const t0 = startOfDay(now); const from = t0 - 6 * DAY;
    const goals = data.goals || DEFAULT_GOALS;
    const at = (data.attempts || []).filter(ok);
    const rv = (data.reviews || []).filter(ok);
    const sum = (arr, a, b) => arr.filter((x) => x.t >= a && x.t < b);
    const today = sum(at, t0, t0 + DAY);
    const week = sum(at, from, t0 + DAY);
    const weekRv = sum(rv, from, t0 + DAY);
    const days = new Set(week.map((a) => startOfDay(a.t)).concat(weekRv.map((r) => startOfDay(r.t))));
    return {
      goals, todayGoal: goalFor(goals, now), todayDone: today.reduce((n, a) => n + a.total, 0), todayCorrect: today.reduce((n, a) => n + a.correct, 0), daysDone: days.size,
      todayPts: today.reduce((n, a) => n + (a.pts || 0), 0) + sum(rv, t0, t0 + DAY).length * REVIEW_PTS,
      weekPts: week.reduce((n, a) => n + (a.pts || 0), 0) + weekRv.length * REVIEW_PTS,
      totalPts: at.reduce((n, a) => n + (a.pts || 0), 0) + rv.length * REVIEW_PTS,
    };
  }

  /* Báo cáo 7 ngày gần nhất (tính cả hôm nay). */
  function weekly(data, now, grade) {
    now = now || Date.now();
    const from = startOfDay(now) - 6 * DAY;
    const list = data.attempts.filter((a) => a.t >= from && a.t <= now + DAY && (!grade || a.grade === grade));
    const book = grade ? data.notebook.filter((n) => n.grade === grade) : data.notebook;
    const days = new Set(list.map((a) => startOfDay(a.t)));
    const subj = {}, chap = {};
    let correct = 0, total = 0, seconds = 0;
    list.forEach((a) => {
      correct += a.correct; total += a.total; seconds += a.seconds;
      const sk = a.subject + '|' + a.grade;
      const s = subj[sk] || (subj[sk] = { subject: a.subject, grade: a.grade, correct: 0, total: 0, lessons: 0 });
      s.correct += a.correct; s.total += a.total; s.lessons += 1;
      const ck = sk + '|' + (a.chapter || a.lesson);
      const c = chap[ck] || (chap[ck] = { subject: a.subject, grade: a.grade, name: a.chapter || a.lesson, correct: 0, total: 0 });
      c.correct += a.correct; c.total += a.total;
    });
    const pct = (x) => (x.total ? Math.round((100 * x.correct) / x.total) : 0);
    const subjects = Object.values(subj).map((s) => Object.assign(s, { pct: pct(s) })).sort((a, b) => b.total - a.total);
    markPass(subjects, data.goals);
    const weak = Object.values(chap).filter((c) => c.total >= 5).map((c) => Object.assign(c, { pct: pct(c) }))
      .filter((c) => c.pct < passFor(data.goals, c.subject)).sort((a, b) => a.pct - b.pct).slice(0, 5);
    return {
      from, to: startOfDay(now), attempts: list.length, days: days.size,
      minutes: Math.round(seconds / 60), correct, total, pct: pct({ correct, total }),
      subjects, weak, prog: progress(data, now, grade), notebook: book.length, dueCount: due(data, now, grade).length, grade: grade || 0,
    };
  }

  /* Báo cáo theo khoảng ngày tùy chọn. from/to là mốc đầu ngày (to tính cả ngày đó); subject, grade lọc nếu có.
     Trả về từng ngày (số câu đúng/sai) để vẽ lịch, tổng, theo môn và các chương yếu. */
  function report(data, opts, now) {
    now = now || Date.now();
    opts = opts || {};
    const from = startOfDay(opts.from != null ? opts.from : now - 6 * DAY);
    const to = startOfDay(opts.to != null ? opts.to : now);
    const subject = opts.subject || ''; const grade = opts.grade || 0;
    const goals = data.goals || DEFAULT_GOALS;
    const list = (data.attempts || []).filter((a) => a.t >= from && a.t < to + DAY && (!grade || a.grade === grade) && (!subject || a.subject === subject));
    const pct = (x) => (x.total ? Math.round((100 * x.correct) / x.total) : 0);
    const days = [];
    for (let t = from; t <= to && days.length < 366; t += DAY) {
      const d = new Date(t); d.setHours(0, 0, 0, 0);
      const day = { t: d.getTime(), correct: 0, total: 0, lessons: 0 };
      const ds = {};
      list.forEach((a) => {
        if (a.t >= day.t && a.t < day.t + DAY) {
          day.correct += a.correct; day.total += a.total; day.lessons += 1;
          const k = a.subject + '|' + a.grade;
          const x = ds[k] || (ds[k] = { subject: a.subject, grade: a.grade, correct: 0, total: 0, lessons: 0 });
          x.correct += a.correct; x.total += a.total; x.lessons += 1;
        }
      });
      day.wrong = day.total - day.correct; day.pct = pct(day);
      day.subjects = markPass(Object.values(ds).map((x) => Object.assign(x, { wrong: x.total - x.correct, pct: pct(x) })).sort((a, b) => b.total - a.total), goals);
      day.reached = !subject && day.total >= goalFor(goals, day.t);
      days.push(day);
    }
    const subj = {}, chap = {};
    let correct = 0, total = 0, seconds = 0;
    list.forEach((a) => {
      correct += a.correct; total += a.total; seconds += a.seconds || 0;
      const sk = a.subject + '|' + a.grade;
      const s = subj[sk] || (subj[sk] = { subject: a.subject, grade: a.grade, correct: 0, total: 0, lessons: 0 });
      s.correct += a.correct; s.total += a.total; s.lessons += 1;
      const ck = sk + '|' + (a.chapter || a.lesson);
      const c = chap[ck] || (chap[ck] = { subject: a.subject, grade: a.grade, name: a.chapter || a.lesson, correct: 0, total: 0 });
      c.correct += a.correct; c.total += a.total;
    });
    const subjects = Object.values(subj).map((x) => Object.assign(x, { wrong: x.total - x.correct, pct: pct(x) })).sort((a, b) => b.total - a.total);
    markPass(subjects, goals);
    const weak = Object.values(chap).filter((c) => c.total >= 5).map((c) => Object.assign(c, { pct: pct(c) }))
      .filter((c) => c.pct < passFor(goals, c.subject)).sort((a, b) => a.pct - b.pct).slice(0, 5);
    return {
      from, to, days, goals, subject, grade, correct, wrong: total - correct, total, pct: pct({ correct, total }),
      minutes: Math.round(seconds / 60), attempts: list.length, activeDays: days.filter((d) => d.total > 0).length,
      subjects, weak,
    };
  }

  return { redoSummary, redoList, KEY, INTERVALS, DEFAULT_GOALS, DEFAULT_PASS, goalFor, passFor, markPass, cleanPassBy, score10, points, setGoals, cleanReward, setReward, weekStart, weekCount, evaluate, markShown, giveReward, rewardState, progress, report, load, save, recordAttempt, grade, due, weekly, slimItem };
});
