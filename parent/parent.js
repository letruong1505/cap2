// Điều hướng app Phụ huynh: màn hình chính, xem con học, thời khóa biểu, tư vấn, mua khóa học.
(function () {
  'use strict';
  const SECTIONS = ['home', 'parent-view', 'timetable', 'advice', 'purchase'];
  const SUBJECTS = [['toan', 'Toán'], ['van', 'Ngữ văn'], ['anh', 'Tiếng Anh'], ['ly', 'Vật lí'], ['hoa', 'Hoá học'], ['sinh', 'Sinh học'], ['lichsu', 'Lịch sử'], ['diali', 'Địa lí'], ['gdktpl', 'Giáo dục KT&PL'], ['tin', 'Tin học']];
  const NAMES = {}; SUBJECTS.forEach(([id, n]) => { NAMES[id] = n; });
  const $ = (id) => document.getElementById(id);
  let grade = 6;
  try { grade = Number(localStorage.getItem('nl-parent-grade')) || 6; } catch (e) { /* bỏ qua */ }

  function show(id) { SECTIONS.forEach((s) => { $(s).hidden = s !== id; }); window.scrollTo(0, 0); }
  function home() {
    const T = window.VungTimetable;
    if (T) T.banner($('tt-banner-home'), { grades: [grade], names: NAMES });
    show('home');
  }
  function timetable() {
    const T = window.VungTimetable;
    const sel = $('tt-grade');
    if (!sel.options.length) for (let g = 1; g <= 12; g++) sel.append(new Option('Lớp ' + g, String(g)));
    sel.value = String(grade);
    const draw = () => {
      T.banner($('tt-banner'), { grades: [grade], names: NAMES });
      T.editor($('tt-card'), { grade, subjects: SUBJECTS.map(([id, name]) => ({ id, name })), onSaved: () => { T.banner($('tt-banner'), { grades: [grade], names: NAMES }); } });
    };
    sel.onchange = () => { grade = Number(sel.value); try { localStorage.setItem('nl-parent-grade', String(grade)); } catch (e) { /* bỏ qua */ } draw(); };
    draw(); show('timetable');
  }

  document.querySelectorAll('[data-back]').forEach((b) => b.addEventListener('click', home));
  $('go-progress').addEventListener('click', () => { window.VungProgressUI.renderParentView($('parent-body')); show('parent-view'); });
  $('go-timetable').addEventListener('click', timetable);
  $('go-advice').addEventListener('click', () => show('advice'));
  $('go-buy').addEventListener('click', () => {
    const box = $('price-list'); box.replaceChildren();
    const money = (n) => n.toLocaleString('vi-VN') + ' đ';
    window.NL_CATALOG.GROUPS.forEach((g) => {
      const c = document.createElement('div'); c.className = 'goal-box';
      const t = document.createElement('h2'); t.textContent = g.group; c.append(t);
      const ul = document.createElement('ul'); ul.className = 'report-list';
      g.items.forEach((x) => { const li = document.createElement('li'); li.textContent = x.name + ' · ' + money(x.price) + (x.note ? ' (' + x.note + ')' : ''); ul.append(li); });
      c.append(ul); box.append(c);
    });
    show('purchase');
  });
  const v = $('build'); if (v && window.NL_MOBILE_CONFIG) v.textContent = 'Phụ huynh ' + (window.NL_MOBILE_CONFIG.version || '');
  if (window.VungTimetable) window.VungTimetable.sync(NAMES);
  home();
})();
