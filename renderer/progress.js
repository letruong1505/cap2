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

  const DEFAULT_GOALS = { daily: 20, weekly: 5 }; // 20 câu/ngày, 5 ngày học/tuần
  function empty() { return { attempts: [], notebook: [], reviews: [], goals: Object.assign({}, DEFAULT_GOALS) }; }

  /* Điểm thang 10 của một bài (làm tròn 1 chữ số). */
  function score10(correct, total) { return total ? Math.round((correct / total) * 100) / 10 : 0; }
  /* Điểm thưởng: 10/câu đúng, thêm 20 nếu bài từ 5 câu đạt từ 90%. Ôn sổ câu sai: 5/câu đúng. */
  function points(correct, total) { return correct * 10 + (total >= 5 && correct / total >= 0.9 ? 20 : 0); }
  const REVIEW_PTS = 5;
  function clampInt(v, lo, hi, d) { v = Math.round(Number(v)); return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : d; }
  function setGoals(data, g) {
    data.goals = { daily: clampInt(g.daily, 5, 200, DEFAULT_GOALS.daily), weekly: clampInt(g.weekly, 1, 7, DEFAULT_GOALS.weekly) };
    return data;
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
    (wrong || []).forEach((it) => {
      const k = key(it);
      const found = data.notebook.find((n) => n.key === k);
      if (found) { found.box = 0; found.due = now + DAY; found.misses = (found.misses || 1) + 1; found.item = slimItem(it); }
      else data.notebook.push({
        key: k, subject: meta.subject, grade: meta.grade, lessonId: meta.lessonId, lesson: meta.lesson,
        chapter: meta.chapter || '', box: 0, due: now + DAY, misses: 1, added: now, item: slimItem(it),
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
      goals, todayDone: today.reduce((n, a) => n + a.total, 0), daysDone: days.size,
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
    const weak = Object.values(chap).filter((c) => c.total >= 5).map((c) => Object.assign(c, { pct: pct(c) }))
      .filter((c) => c.pct < 70).sort((a, b) => a.pct - b.pct).slice(0, 5);
    return {
      from, to: startOfDay(now), attempts: list.length, days: days.size,
      minutes: Math.round(seconds / 60), correct, total, pct: pct({ correct, total }),
      subjects, weak, prog: progress(data, now, grade), notebook: book.length, dueCount: due(data, now, grade).length, grade: grade || 0,
    };
  }

  return { KEY, INTERVALS, DEFAULT_GOALS, score10, points, setGoals, progress, load, save, recordAttempt, grade, due, weekly, slimItem };
});
