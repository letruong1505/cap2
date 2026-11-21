// Khóa "Tư duy & lập trình": 2 lộ trình (8–11 Scratch, 12–18 Python). Mở đầu và Bài 1 xem miễn phí; các bài còn lại mở khi khóa ra mắt và được mua.
(function () {
  'use strict';
  const COURSE_ID = 'tu-duy-lap-trinh';
  const FREE = ['tongquan', 'bai1'];
  const TRACKS = {
    k811: { name: 'Lộ trình 8–11 tuổi', tool: 'Scratch', sub: 'Kéo thả khối lệnh để làm nhân vật di chuyển, vẽ hình và chơi trò chơi – đồng thời tập hỏi “vì sao đúng?” và nghĩ ngược.' },
    k1218: { name: 'Lộ trình 12–18 tuổi', tool: 'Python', sub: 'Dùng Python để phân rã bài toán, kiểm thử như một nhà phản biện và giải bài bằng tư duy ngược.' },
  };
  const KEYS = ['tongquan', 'bai1', 'bai2', 'bai3', 'bai4', 'bai5', 'bai6', 'bai7', 'bai8'];
  const LOCK = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';

  function h(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') e.className = v;
      else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (v != null && v !== false) e.setAttribute(k, v);
    }
    for (const c of kids.flat()) if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c)));
    return e;
  }
  const owned = (lic) => !!(lic && lic.status === 'ok' && Array.isArray(lic.courses) && lic.courses.includes(COURSE_ID));
  const content = (t) => (window.TUDUY || {})[t] || {};
  let ctx = { license: () => ({}), onBuy() {}, onExit() {} };
  let body;

  function canOpen(key) { return FREE.includes(key) || owned(ctx.license()); }
  function shortTitle(t, key) { return ((content(t)[key] || {}).title || key).replace(/^(Bài\s*\d+|Mở đầu)\s*[·:.\-–]\s*/, ''); }
  function no(key) { return key === 'tongquan' ? 'Mở đầu' : 'Bài ' + key.replace(/\D/g, ''); }
  const soon = () => window.alert('Bài này mở khi khóa Tư duy & lập trình chính thức ra mắt. Phần mở đầu và Bài 1 đang xem thử miễn phí.');

  function trackScreen() {
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: () => ctx.onExit() }, '← Chọn khóa'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'Khóa Kỹ năng · sắp ra mắt'), h('h1', {}, 'Tư duy & lập trình'),
        h('p', { class: 'screen-sub' }, 'Lập trình chỉ là công cụ. Điều khóa học rèn là tư duy phản biện (hỏi “vì sao đúng?”) và tư duy ngược (đi từ kết quả về điều kiện ban đầu). Chọn lộ trình phù hợp với độ tuổi; phần mở đầu và Bài 1 xem miễn phí.')),
      h('ul', { class: 'lesson-list' }, Object.keys(TRACKS).map((t) => h('li', {}, h('button', { class: 'lesson-row', type: 'button', onclick: () => listScreen(t) },
        h('span', { class: 'lesson-no' }, TRACKS[t].tool), h('span', { class: 'lesson-name' }, TRACKS[t].name + ' – ' + TRACKS[t].sub))))));
    window.scrollTo(0, 0);
  }

  function listScreen(t) {
    const own = owned(ctx.license());
    const rows = KEYS.filter((k) => content(t)[k]).map((k) => {
      const open = canOpen(k);
      const r = h('button', { class: 'lesson-row' + (open ? '' : ' locked'), type: 'button', onclick: open ? () => lessonScreen(t, k) : soon },
        h('span', { class: 'lesson-no' }, no(k)), h('span', { class: 'lesson-name' }, shortTitle(t, k)),
        FREE.includes(k) && !own ? h('span', { class: 'lesson-tag' }, 'Xem thử') : null);
      if (!open) { const l = h('span', { class: 'lesson-lock', title: 'Mở khi mua khóa' }); l.innerHTML = LOCK; r.append(l); r.setAttribute('aria-label', no(k) + ' ' + shortTitle(t, k) + ' (cần mua khóa)'); }
      return h('li', {}, r);
    });
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: trackScreen }, '← Chọn lộ trình'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'Tư duy & lập trình · ' + TRACKS[t].tool), h('h1', {}, TRACKS[t].name),
        h('p', { class: 'screen-sub' }, TRACKS[t].sub)),
      h('section', { class: 'book' }, h('ul', { class: 'lesson-list' }, rows)));
    window.scrollTo(0, 0);
  }

  // Nút "Sao chép" cho prompt mẫu và dữ liệu mẫu
  function addCopyButtons(root) {
    root.querySelectorAll('pre.prompt, pre.pdata').forEach((pre) => {
      const b = h('button', { class: 'copy-btn', type: 'button' }, 'Sao chép');
      b.addEventListener('click', () => {
        const text = pre.textContent;
        const ok = () => { b.textContent = 'Đã chép'; b.classList.add('done'); setTimeout(() => { b.textContent = 'Sao chép'; b.classList.remove('done'); }, 1500); };
        const fallback = () => { const t = document.createElement('textarea'); t.value = text; t.style.position = 'fixed'; t.style.opacity = '0'; document.body.append(t); t.select(); try { document.execCommand('copy'); ok(); } catch (e) { /* bỏ qua */ } t.remove(); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fallback); else fallback();
      });
      pre.parentNode.insertBefore(b, pre);
    });
  }

  function lessonScreen(t, key) {
    const L = content(t)[key];
    const box = h('article', { class: 'aiw-lesson' });
    if (L && canOpen(key)) box.innerHTML = '<h2>' + L.title + '</h2>' + (L.sub ? '<p class="sub">' + L.sub + '</p>' : '') + L.html;
    else box.append(h('p', {}, L ? 'Bài này mở khi mua khóa.' : 'Bài này đang được biên soạn.'));
    addCopyButtons(box);
    const keys = KEYS.filter((k) => content(t)[k]);
    const i = keys.indexOf(key), prev = keys[i - 1], next = keys[i + 1];
    const nav = h('div', { class: 'aiw-nav' },
      prev ? h('button', { type: 'button', onclick: () => (canOpen(prev) ? lessonScreen(t, prev) : listScreen(t)) }, '← ' + no(prev)) : h('span'),
      next ? h('button', { type: 'button', onclick: () => (canOpen(next) ? lessonScreen(t, next) : listScreen(t)) }, no(next) + (canOpen(next) ? ' →' : ' 🔒')) : h('span'));
    body.replaceChildren(h('button', { class: 'back-link', type: 'button', onclick: () => listScreen(t) }, '← Các bài ' + TRACKS[t].name.toLowerCase()), box, nav);
    window.scrollTo(0, 0);
  }

  window.TuDuy = {
    open(c) { ctx = Object.assign(ctx, c || {}); body = document.getElementById('tuduy-body'); trackScreen(); },
    _keys: KEYS, _free: FREE, _courseId: COURSE_ID,
  };
})();
