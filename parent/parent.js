// Điều hướng app Phụ huynh: màn hình chính, xem con học, thời khóa biểu (đồng bộ từ máy của con), liên hệ, khóa học và giá.
(function () {
  'use strict';
  const SECTIONS = ['home', 'parent-view', 'timetable', 'advice', 'purchase', 'buy', 'digest'];
  const NAMES = { toan: 'Toán', van: 'Ngữ văn', anh: 'Tiếng Anh', ly: 'Vật lí', hoa: 'Hoá học', sinh: 'Sinh học', lichsu: 'Lịch sử', diali: 'Địa lí', gdktpl: 'Giáo dục KT&PL', tin: 'Tin học' };
  const T = window.VungTimetable;
  const $ = (id) => document.getElementById(id);
  const ls = () => { try { return window.localStorage; } catch (e) { return null; } };
  const PV_KEY = 'vungbai.parentview.v1'; // mã đơn + số điện thoại do màn hình "Xem con học" lưu
  const REMIND_KEY = 'nl-parent-remind';

  function h(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) { if (k === 'class') e.className = v; else if (k.startsWith('on') && typeof v === 'function') e.addEventListener(k.slice(2), v); else if (v != null && v !== false) e.setAttribute(k, v); }
    for (const c of kids.flat()) if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c)));
    return e;
  }
  const creds = () => { try { const v = JSON.parse(ls().getItem(PV_KEY) || '{}'); return v && v.code && v.phone ? v : null; } catch (e) { return null; } };
  const remindOn = () => { try { return ls().getItem(REMIND_KEY) !== '0'; } catch (e) { return true; } };

  function show(id) { SECTIONS.forEach((s) => { $(s).hidden = s !== id; }); window.scrollTo(0, 0); }
  function gradesOf() { return T ? Object.keys(T.load(ls()).grades).map(Number).sort((a, b) => a - b) : []; }
  function home() { T.banner($('tt-banner-home'), { grades: gradesOf(), names: NAMES }); show('home'); syncTimetable(); }

  /* Lấy thời khóa biểu con đã đồng bộ lên máy chủ, gộp các lớp lại và lưu để app nhắc học. Trả về { ok, list, error }. */
  async function syncTimetable() {
    const c = creds();
    if (!c) return { ok: false, error: 'Hãy vào "Xem con học" và nhập mã đơn, số điện thoại trước.' };
    const r = await window.vungBai.progressView({ code: c.code, phone: c.phone, from: '', to: '', grade: 0 });
    if (!r.ok) return { ok: false, error: r.offline ? 'Không có mạng. Thử lại sau.' : (r.error || 'Không đọc được thời khóa biểu.') };
    const list = (r.data && r.data.timetables) || [];
    const merged = T.normalize({ remindOn: remindOn(), remindHour: (list[0] && list[0].data.remindHour) || 19, grades: Object.assign({}, ...list.map((x) => x.data.grades)) });
    if (list.length) T.save(ls(), merged); else { const cur = T.load(ls()); cur.grades = {}; T.save(ls(), cur); }
    T.banner($('tt-banner-home'), { grades: gradesOf(), names: NAMES });
    await applyReminders();
    return { ok: true, list, enabled: !!(r.data && r.data.enabled) };
  }
  async function applyReminders() {
    if (!window.NLNotify) return false;
    if (!remindOn()) return window.NLNotify.schedule([]);
    return T.sync(NAMES);
  }

  function renderTimetable(res) {
    const box = $('tt-view'); box.replaceChildren();
    if (!res.ok) { $('tt-msg').textContent = res.error; return; }
    if (!res.list.length) {
      $('tt-msg').textContent = res.enabled ? 'Con chưa nhập thời khóa biểu trên app học.' : 'Chưa có dữ liệu. Trên app học của con, vào "Báo cáo cho phụ huynh", bật "Cho phụ huynh xem", rồi nhập thời khóa biểu.';
      return;
    }
    $('tt-msg').textContent = 'Đã cập nhật lúc ' + new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }) + '.';
    const now = new Date(); const cur = T.load(ls());
    res.list.forEach((x) => Object.keys(x.data.grades).forEach((g) => {
      const t = x.data.grades[g];
      const card = h('div', { class: 'goal-box' }, h('h2', {}, 'Lớp ' + g + (res.list.length > 1 && x.label ? ' · ' + x.label : '')));
      if (T.isStale(cur, g, now)) card.append(h('p', { class: 'meta' }, 'Thời khóa biểu chưa được con cập nhật cho tuần mới.'));
      T.DAYS.forEach(([n, label]) => {
        const sang = (t.days[n] || []).map((e) => T.labelOf(e, NAMES));
        const chieu = ((t.pm && t.pm[n]) || []).map((e) => T.labelOf(e, NAMES));
        card.append(h('p', {}, h('b', {}, label + ': '), 'Sáng ' + (sang.length ? sang.join(', ') : 'nghỉ') + '. Chiều ' + (chieu.length ? chieu.join(', ') : 'nghỉ') + '.'));
      });
      box.append(card);
    }));
  }
  async function openTimetable() {
    const cb = $('tt-remind-local'); cb.checked = remindOn();
    cb.onchange = async () => {
      try { ls().setItem(REMIND_KEY, cb.checked ? '1' : '0'); } catch (e) { /* bỏ qua */ }
      if (cb.checked && window.NLNotify) { try { await window.NLNotify.request(); } catch (e) { /* bỏ qua */ } }
      await applyReminders();
    };
    show('timetable');
    $('tt-msg').textContent = 'Đang cập nhật...';
    T.banner($('tt-banner'), { grades: gradesOf(), names: NAMES });
    const res = await syncTimetable();
    if (res.ok && res.list.length && remindOn() && window.NLNotify) { try { await window.NLNotify.request(); await applyReminders(); } catch (e) { /* bỏ qua */ } }
    renderTimetable(res);
    T.banner($('tt-banner'), { grades: gradesOf(), names: NAMES });
  }

  function openBuy(preselect) {
    window.ParentBuy.open($('buy-body'), { preselect });
    show('buy');
  }

  function openCourses() {
    const box = $('price-list'); box.replaceChildren();
    const money = (n) => n.toLocaleString('vi-VN') + ' đ';
    window.NL_CATALOG.GROUPS.forEach((g) => {
      const c = h('div', { class: 'goal-box' }, h('h2', {}, g.group));
      if (g.fee) c.append(h('p', { class: 'meta' }, g.fee));
      g.items.forEach((x) => {
        const info = (window.PARENT_COURSES || {})[x.id] || { intro: '', content: [] };
        const d = h('details', { class: 'edu-note' }, h('summary', {}, x.name + ' · ' + money(x.price)));
        const body = h('div', { class: 'edu-note-body' });
        if (x.note) body.append(h('p', { class: 'meta' }, x.note));
        if (info.intro) body.append(h('p', {}, info.intro));
        if (info.content.length) { body.append(h('p', {}, h('b', {}, 'Nội dung:'))); body.append(h('ul', {}, info.content.map((t) => h('li', {}, t)))); }
        const vh = /^van-hoa-(\d+)$/.exec(x.id);
        if (vh && window.ParentDigest) body.append(h('p', {}, h('button', { type: 'button', class: 'primary', onclick: () => { window.ParentDigest.open($('digest-body'), Number(vh[1])); show('digest'); } }, 'Xem nội dung chi tiết lớp ' + vh[1])));
        body.append(h('p', {}, h('button', { type: 'button', class: 'ghost', onclick: () => openBuy(x.id) }, /^ai-nguoi-di-lam/.test(x.id) ? 'Mua khóa học' : 'Mua khóa này cho con')));
        d.append(body); c.append(d);
      });
      box.append(c);
    });
    show('purchase');
  }

  document.querySelectorAll('[data-back]').forEach((b) => b.addEventListener('click', () => { if (b.closest('#buy')) openCourses(); else home(); }));
  $('go-progress').addEventListener('click', () => { window.VungProgressUI.renderParentView($('parent-body')); show('parent-view'); });
  $('go-timetable').addEventListener('click', openTimetable);
  $('tt-refresh').addEventListener('click', openTimetable);
  $('go-advice').addEventListener('click', () => show('advice'));
  $('go-buy').addEventListener('click', openCourses);
  $('go-buy-now').addEventListener('click', () => openBuy());
  document.querySelectorAll('[data-back-courses]').forEach((b) => b.addEventListener('click', openCourses));
  const v = $('build'); if (v && window.NL_MOBILE_CONFIG) v.textContent = 'Phụ huynh ' + (window.NL_MOBILE_CONFIG.version || '');
  home();
})();
