/* Thời khóa biểu của học sinh: nhập một lần, cập nhật mỗi tuần (không lưu tuần cũ).
   Tối hôm trước mỗi ngày học, app nhắc ôn bài và làm bài trước các môn của ngày hôm sau.
   Phần logic (tuần, nhắc, kế hoạch thông báo) là hàm thuần để kiểm thử trong Node; phần giao diện ở cuối. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VungTimetable = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const KEY = 'nl-timetable';
  const DAYS = [[1, 'Thứ hai'], [2, 'Thứ ba'], [3, 'Thứ tư'], [4, 'Thứ năm'], [5, 'Thứ sáu'], [6, 'Thứ bảy']];
  const DOW_NAME = ['Chủ nhật', 'Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy'];
  const HORIZON = 14; // lên lịch thông báo trước 14 ngày

  const day0 = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const addDays = (d, n) => { const x = day0(d); x.setDate(x.getDate() + n); return x; };
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

  /* Khóa tuần = ngày thứ hai của tuần. Chủ nhật tính vào tuần tới: tối Chủ nhật là lúc nhập thời khóa biểu tuần mới. */
  function weekKey(d) {
    const x = day0(d); const dow = x.getDay();
    return iso(dow === 0 ? addDays(x, 1) : addDays(x, -(dow - 1)));
  }

  const empty = () => ({ v: 1, remindOn: true, remindHour: 19, grades: {} });
  function normalize(raw) {
    const d = empty();
    if (!raw || typeof raw !== 'object') return d;
    d.remindOn = raw.remindOn !== false;
    const h = Number(raw.remindHour); d.remindHour = h >= 0 && h <= 23 ? Math.floor(h) : 19;
    Object.keys(raw.grades || {}).forEach((g) => {
      const t = raw.grades[g]; if (!t || typeof t.week !== 'string' || !t.days) return;
      const days = {};
      DAYS.forEach(([n]) => { days[n] = (Array.isArray(t.days[n]) ? t.days[n] : []).filter((s) => typeof s === 'string' && s).slice(0, 12); });
      d.grades[g] = { week: t.week, days };
    });
    return d;
  }
  function load(storage) { try { return normalize(JSON.parse(storage.getItem(KEY) || 'null')); } catch (e) { return empty(); } }
  function save(storage, data) { try { storage.setItem(KEY, JSON.stringify(data)); } catch (e) { /* bỏ qua */ } }

  /* Lưu thời khóa biểu của một lớp cho tuần chứa ngày now; thay hẳn bản cũ. */
  function setTimetable(data, grade, days, now) {
    const clean = {};
    DAYS.forEach(([n]) => { clean[n] = Array.from(new Set((days[n] || []).filter(Boolean))); });
    data.grades[grade] = { week: weekKey(now), days: clean };
    return data;
  }
  const isEmptyTT = (t) => !t || DAYS.every(([n]) => !t.days[n].length);
  /* Thời khóa biểu của lớp đã cũ (chưa nhập cho tuần này) hoặc chưa có. */
  const isStale = (data, grade, now) => { const t = data.grades[grade]; return !t || t.week !== weekKey(now); };

  /* Mục trong ngày: mã môn của app (toan, ly...) hoặc "x:Tên môn" do học sinh tự gõ. */
  const custom = (e) => e.startsWith('x:');
  const labelOf = (e, names) => (custom(e) ? e.slice(2) : (names && names[e]) || e);

  /* Nhắc cho lớp grade vào thời điểm now: từ giờ nhắc của tối hôm trước, báo các môn của ngày mai. */
  function reminderFor(data, grade, now) {
    const t = data.grades[grade];
    if (!data.remindOn || isEmptyTT(t)) return null;
    if (now.getHours() < data.remindHour) return null;
    const tomorrow = addDays(now, 1);
    const dow = tomorrow.getDay();
    const items = dow === 0 ? [] : t.days[dow];
    if (!items.length) return null;
    return { grade: Number(grade), date: tomorrow, dow, dayName: DOW_NAME[dow], items, stale: t.week !== weekKey(tomorrow) };
  }

  /* Kế hoạch thông báo điện thoại cho HORIZON ngày tới: mỗi ngày học một thông báo vào giờ nhắc của tối hôm trước. */
  function plan(data, now, names) {
    if (!data.remindOn) return [];
    const grades = Object.keys(data.grades).filter((g) => !isEmptyTT(data.grades[g]));
    const out = [];
    grades.forEach((g) => {
      const t = data.grades[g];
      for (let k = 0; k <= HORIZON; k++) {
        const D = addDays(now, k); const dow = D.getDay();
        if (dow === 0) continue;
        const items = t.days[dow]; if (!items.length) continue;
        const at = addDays(D, -1); at.setHours(data.remindHour, 0, 0, 0);
        if (at <= now) continue;
        const list = items.map((e) => labelOf(e, names)).join(', ');
        const monday = at.getDay() === 0 && t.week !== weekKey(D);
        out.push({
          id: Number(iso(D).replace(/-/g, '')) * 100 + Number(g),
          at: at.getTime(),
          title: grades.length > 1 ? `Nam Linh · Lớp ${g}` : 'Nam Linh Educenter',
          body: `Ngày mai (${DOW_NAME[dow]}) học ${list}. Ôn bài và làm bài trước nhé!` + (monday ? ' Nhớ cập nhật thời khóa biểu tuần mới.' : ''),
        });
      }
    });
    return out.sort((a, b) => a.at - b.at);
  }

  /* ---------- Giao diện ---------- */
  const store = () => { try { return window.localStorage; } catch (e) { return null; } };
  function h(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => { if (v !== false && v != null) n.setAttribute(k, v); });
    kids.forEach((k) => { if (k != null) n.append(k); });
    return n;
  }

  /* Đưa kế hoạch thông báo xuống điện thoại (chỉ Android có NLNotify). */
  function sync(names) {
    try {
      if (!window.NLNotify) return Promise.resolve(false);
      return window.NLNotify.schedule(plan(load(store()), new Date(), names || {}));
    } catch (e) { return Promise.resolve(false); }
  }

  /* Khung nhắc nhở ở đầu màn hình: opts = { grades: [số lớp], names, open(grade, môn) }. */
  function banner(slot, opts) {
    slot.replaceChildren();
    const data = load(store()); const now = new Date();
    (opts.grades || []).forEach((g) => {
      const r = reminderFor(data, g, now); if (!r) return;
      const chips = h('div', { class: 'tt-chips' });
      r.items.forEach((e) => {
        const name = labelOf(e, opts.names);
        if (custom(e) || !opts.open) { chips.append(h('span', { class: 'tt-chip' }, name)); return; }
        const b = h('button', { type: 'button', class: 'tt-chip go' }, name);
        b.addEventListener('click', () => opts.open(r.grade, e));
        chips.append(b);
      });
      slot.append(h('div', { class: 'tt-banner', role: 'status' },
        h('b', {}, `Lớp ${r.grade}: ngày mai (${r.dayName}) học ${r.items.length} môn`),
        h('p', {}, 'Tối nay ôn bài và làm bài trước các môn này:'), chips,
        r.stale ? h('p', { class: 'meta' }, 'Thời khóa biểu chưa được cập nhật cho tuần mới. Vào mục Thời khóa biểu để sửa.') : null));
    });
  }

  /* Thẻ nhập thời khóa biểu của một lớp: opts = { grade, subjects: [{id, name}], onSaved }. */
  function editor(slot, opts) {
    const g = String(opts.grade); const now = new Date();
    const data = load(store());
    const names = {}; opts.subjects.forEach((s) => { names[s.id] = s.name; });
    const cur = data.grades[g];
    const draft = {}; DAYS.forEach(([n]) => { draft[n] = cur ? cur.days[n].slice() : []; });
    const stale = isStale(data, g, now);
    const status = !cur ? 'Chưa nhập' : (stale ? 'Cần cập nhật cho tuần mới' : 'Đã cập nhật tuần này');
    const det = h('details', { class: 'tt-card' + (stale ? ' stale' : '') });
    det.append(h('summary', {}, h('span', { class: 'tt-title' }, 'Thời khóa biểu'), h('b', { class: 'tt-status' }, status)));
    const body = h('div', { class: 'tt-body' });
    body.append(h('p', { class: 'meta' }, 'Chọn các môn học mỗi ngày. Mỗi tuần nhập lại một lần, app không lưu tuần cũ. Tối hôm trước app sẽ nhắc ôn bài các môn của ngày mai.'));

    DAYS.forEach(([n, label]) => {
      const row = h('div', { class: 'tt-day' }, h('div', { class: 'tt-day-name' }, label));
      const chips = h('div', { class: 'tt-chips' });
      const draw = () => {
        chips.replaceChildren();
        opts.subjects.forEach((s) => {
          const on = draft[n].includes(s.id);
          const b = h('button', { type: 'button', class: 'tt-chip toggle' + (on ? ' on' : ''), 'aria-pressed': String(on) }, s.name);
          b.addEventListener('click', () => { draft[n] = on ? draft[n].filter((x) => x !== s.id) : draft[n].concat(s.id); draw(); });
          chips.append(b);
        });
        draft[n].filter(custom).forEach((e) => {
          const b = h('button', { type: 'button', class: 'tt-chip toggle on', title: 'Bấm để bỏ' }, labelOf(e) + ' ✕');
          b.addEventListener('click', () => { draft[n] = draft[n].filter((x) => x !== e); draw(); });
          chips.append(b);
        });
        const input = h('input', { type: 'text', class: 'tt-other', placeholder: 'Môn khác (Ngữ văn, Tin học...)', maxlength: '30', 'aria-label': `Môn khác ${label}` });
        const add = () => { const v = input.value.trim(); if (v && !draft[n].includes('x:' + v)) { draft[n] = draft[n].concat('x:' + v); draw(); } };
        input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); add(); } });
        input.addEventListener('blur', add);
        chips.append(input);
      };
      draw(); row.append(chips); body.append(row);
    });

    const remind = h('input', { type: 'checkbox', id: 'tt-remind' }); remind.checked = data.remindOn;
    const hour = h('select', { id: 'tt-hour', 'aria-label': 'Giờ nhắc' });
    for (let x = 16; x <= 22; x++) { const o = h('option', { value: String(x) }, `${x}:00`); if (x === data.remindHour) o.selected = true; hour.append(o); }
    if (![16, 17, 18, 19, 20, 21, 22].includes(data.remindHour)) hour.append(h('option', { value: String(data.remindHour), selected: 'selected' }, `${data.remindHour}:00`));
    body.append(h('div', { class: 'tt-remind-row' }, h('label', {}, remind, ' Nhắc học bài tối hôm trước lúc '), hour));
    const msg = h('div', { class: 'meta', role: 'status' });
    const saveBtn = h('button', { type: 'button', class: 'primary' }, 'Lưu thời khóa biểu tuần này');
    saveBtn.addEventListener('click', async () => {
      const d = load(store());
      d.remindOn = remind.checked; d.remindHour = Number(hour.value);
      setTimetable(d, g, draft, new Date());
      save(store(), d);
      let note = 'Đã lưu.';
      if (window.NLNotify && d.remindOn) {
        try {
          const ok = await window.NLNotify.request();
          if (ok) { await sync(names); note = 'Đã lưu. Điện thoại sẽ nhắc đúng giờ.'; } else note = 'Đã lưu. Bật quyền thông báo cho app để điện thoại nhắc đúng giờ; app vẫn nhắc khi bạn mở.';
        } catch (e) { /* bỏ qua */ }
      } else if (window.NLNotify) { await sync(names); }
      msg.textContent = note;
      det.querySelector('.tt-status').textContent = 'Đã cập nhật tuần này'; det.classList.remove('stale');
      if (opts.onSaved) opts.onSaved();
    });
    body.append(saveBtn, msg);
    det.append(body);
    slot.replaceChildren(det);
  }

  return { KEY, DAYS, weekKey, load, save, setTimetable, isStale, isEmptyTT, reminderFor, plan, labelOf, normalize, banner, editor, sync };
});
