/* Đếm thời gian dùng app theo ngày, trên máy của học sinh (Windows và Android).
   - open: thời gian mở app (từ lúc mở đến lúc đóng, kể cả lúc thu nhỏ hoặc để nền).
   - active: thời gian dùng thực: app đang hiện trên màn hình, đang được chọn, và có thao tác gần đây.
   - ngắt quãng = open - active (thu nhỏ, chuyển sang app khác, lâu không thao tác).
   Đang làm một câu hỏi thì cho phép im lặng lâu hơn (học sinh có thể tính trên giấy) so với lúc đọc lý thuyết.
   Chỉ là ước lượng; không dùng camera và không biết học sinh làm gì ngoài app. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VungUsage = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  const KEY = 'vungbai.usage.v1';
  const MAX_DAYS = 130;
  const TICK_MS = 5000;
  const IDLE_READ_MS = 2 * 60000; // đang đọc: sau 2 phút không thao tác thì dừng tính dùng thực
  const IDLE_QUESTION_MS = 5 * 60000; // đang làm câu hỏi: cho phép 5 phút (tính trên giấy)
  const VISIBLE_GAP_CAP = 30000; // khoảng trống dài hơn khi đang hiện: máy ngủ, không tính
  const HIDDEN_GAP_CAP = 30 * 60000; // quay lại app sau khi để nền: tối đa 30 phút tính là ngắt quãng

  const isoOf = (t) => { const d = new Date(t); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };

  /* o: { storage, now(), visible() => bool, mode() => 'read' | 'question' } */
  function create(o) {
    const now = o.now || Date.now;
    const days = {};
    try {
      const raw = o.storage && o.storage.getItem(KEY);
      const d = raw ? JSON.parse(raw) : null;
      if (d && d.days) Object.keys(d.days).forEach((k) => { const v = d.days[k]; if (/^\d{4}-\d{2}-\d{2}$/.test(k) && v) days[k] = { open: Math.max(0, +v.open || 0), active: Math.max(0, +v.active || 0) }; });
    } catch (e) { /* bỏ qua */ }
    let last = null; let lastAct = null; let wasVisible = true;

    function persist() {
      const keys = Object.keys(days).sort();
      while (keys.length > MAX_DAYS) delete days[keys.shift()];
      try { if (o.storage) o.storage.setItem(KEY, JSON.stringify({ days })); } catch (e) { /* bỏ qua */ }
    }

    function tick() {
      const t = now(); const vis = !!o.visible();
      if (last == null) { last = t; lastAct = t; wasVisible = vis; return; }
      const gap = Math.max(0, t - last);
      const d = Math.min(gap, wasVisible ? VISIBLE_GAP_CAP : HIDDEN_GAP_CAP);
      if (d > 0) {
        const k = isoOf(t);
        const day = days[k] || (days[k] = { open: 0, active: 0 });
        day.open += d / 1000;
        if (wasVisible && vis) {
          const idle = (o.mode && o.mode() === 'question') ? IDLE_QUESTION_MS : IDLE_READ_MS;
          const span = Math.max(0, Math.min(d, lastAct + idle - last));
          day.active += span / 1000;
        }
        persist();
      }
      last = t; wasVisible = vis;
    }
    /* Có thao tác của học sinh (chạm, gõ phím, cuộn). */
    function touch() { tick(); lastAct = now(); }
    function list() {
      return Object.keys(days).sort().map((k) => ({ day: k, open: Math.round(days[k].open), active: Math.round(Math.min(days[k].active, days[k].open)) }));
    }
    return { tick, touch, list };
  }

  /* Tổng hợp theo khoảng ngày (iso): rows = [{day, open, active}] (giây). */
  function summarize(rows, fromIso, toIso) {
    const byDay = {}; let open = 0; let active = 0;
    (rows || []).forEach((r) => {
      if (!r || r.day < fromIso || r.day > toIso) return;
      const o = Math.max(0, Math.round(+r.open || 0)); const a = Math.min(o, Math.max(0, Math.round(+r.active || 0)));
      const x = byDay[r.day] || (byDay[r.day] = { open: 0, active: 0, brk: 0 });
      x.open += o; x.active += a; x.brk = x.open - x.active;
      open += o; active += a;
    });
    return { open, active, brk: open - active, byDay };
  }

  /* 3720 giây -> "1 giờ 2 phút". */
  function fmtDur(sec) {
    sec = Math.max(0, Math.round(sec || 0));
    if (sec < 30) return sec ? 'dưới 1 phút' : '0 phút';
    const m = Math.round(sec / 60);
    if (m < 60) return `${m} phút`;
    const h = Math.floor(m / 60); const r = m % 60;
    return r ? `${h} giờ ${r} phút` : `${h} giờ`;
  }

  const api = { KEY, TICK_MS, IDLE_READ_MS, IDLE_QUESTION_MS, isoOf, create, summarize, fmtDur };
  if (typeof window === 'undefined' || !window.document) return api;

  /* ---------- Chạy trên máy ---------- */
  const store = () => { try { return window.localStorage; } catch (e) { return null; } };
  const android = () => !!(window.vungBai && window.vungBai.platform === 'android');
  const tracker = create({
    storage: store(),
    visible: () => document.visibilityState !== 'hidden' && (android() || typeof document.hasFocus !== 'function' || document.hasFocus()),
    mode: () => (document.querySelector('.question') ? 'question' : 'read'),
  });
  let lastTouch = 0;
  const onAct = () => { const t = Date.now(); if (t - lastTouch > 1000) { lastTouch = t; tracker.touch(); } };
  ['pointerdown', 'keydown', 'touchstart', 'wheel', 'input'].forEach((ev) => window.addEventListener(ev, onAct, { capture: true, passive: true }));
  window.addEventListener('scroll', onAct, { capture: true, passive: true });
  ['visibilitychange', 'focus', 'blur', 'pagehide'].forEach((ev) => window.addEventListener(ev, () => tracker.tick()));
  document.addEventListener('visibilitychange', () => tracker.tick());
  tracker.tick();
  setInterval(() => tracker.tick(), TICK_MS);
  return Object.assign(api, { list: () => { tracker.tick(); return tracker.list(); } });
});
