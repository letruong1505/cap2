// Khóa "Gia sư AI": danh sách bài + màn hình học. Tổng quan, Bài 1–2 xem miễn phí; Bài 3–8 và Phụ lục mở khi mua khóa.
(function () {
  'use strict';
  const COURSE_ID = 'gia-su-ai';
  const FREE = ['tongquan', 'bai1', 'bai2'];
  const PARTS = [
    { name: 'Tổng quan', keys: ['tongquan'] },
    { name: 'Phần 1 · Nhận thức & an toàn AI', keys: ['bai1', 'bai2', 'bai3', 'bai4'] },
    { name: 'Phần 2 · Tự tìm lỗ hổng kiến thức', keys: ['bai5'] },
    { name: 'Phần 3 · Xây gia sư AI riêng', keys: ['bai6'] },
    { name: 'Phần 4 · Lộ trình cá nhân hóa', keys: ['bai7'] },
    { name: 'Tổng kết & phụ lục', keys: ['bai8', 'phuluc'] },
  ];
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
  const content = () => window.GIA_SU_AI || {};
  let ctx = { license: () => ({}), onBuy() {}, onExit() {} };
  let body;

  function canOpen(key) { return FREE.includes(key) || owned(ctx.license()); }
  function shortTitle(key) {
    const t = (content()[key] || {}).title || key;
    return t.replace(/^Bài\s*\d+\s*[·:.\-–]\s*/, '');
  }
  function no(key) { return key === 'tongquan' ? 'Mở đầu' : key === 'phuluc' ? 'Phụ lục' : 'Bài ' + key.replace(/\D/g, ''); }

  function listScreen() {
    const own = owned(ctx.license());
    const buy = () => { if (window.confirm('Bài này mở khi Anh/Chị mua khóa Gia sư AI. Mở màn hình Mua khóa học?')) ctx.onBuy(COURSE_ID); };
    const sections = PARTS.map((p) => h('section', { class: 'book' }, h('h2', { class: 'book-title' }, p.name),
      h('ul', { class: 'lesson-list' }, p.keys.filter((k) => content()[k]).map((k) => {
        const open = canOpen(k);
        const r = h('button', { class: 'lesson-row' + (open ? '' : ' locked'), type: 'button', onclick: open ? () => lessonScreen(k) : buy },
          h('span', { class: 'lesson-no' }, no(k)), h('span', { class: 'lesson-name' }, shortTitle(k)),
          FREE.includes(k) && !own ? h('span', { class: 'lesson-tag' }, 'Xem thử') : null);
        if (!open) { const l = h('span', { class: 'lesson-lock', title: 'Cần mua khóa' }); l.innerHTML = LOCK; r.append(l); r.setAttribute('aria-label', no(k) + ' ' + shortTitle(k) + ' (cần mua khóa)'); }
        return h('li', {}, r);
      }))));
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: () => ctx.onExit() }, '← Chọn khóa'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'Khóa Kỹ năng'), h('h1', {}, 'Gia sư AI'),
        h('p', { class: 'screen-sub' }, own ? 'Anh/Chị đã mua khóa này. Mở từng bài bên dưới để học.'
          : 'Học cách dùng AI như một gia sư: An toàn, biết kiểm chứng, tự tìm lỗ hổng kiến thức và xây lộ trình học riêng. Phần mở đầu, Bài 1 và Bài 2 xem miễn phí; các bài còn lại mở khi mua khóa.'),
        own ? null : h('button', { class: 'primary', type: 'button', onclick: () => ctx.onBuy(COURSE_ID) }, 'Mua khóa Gia sư AI')),
      ...sections);
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

  function lessonScreen(key) {
    const L = content()[key];
    const box = h('article', { class: 'aiw-lesson' });
    if (L && canOpen(key)) box.innerHTML = '<h2>' + L.title + '</h2>' + (L.sub ? '<p class="sub">' + L.sub + '</p>' : '') + L.html;
    else box.append(h('p', {}, L ? 'Bài này mở khi mua khóa Gia sư AI.' : 'Bài này đang được biên soạn.'));
    addCopyButtons(box);
    const keys = PARTS.flatMap((p) => p.keys).filter((k) => content()[k]);
    const i = keys.indexOf(key), prev = keys[i - 1], next = keys[i + 1];
    const nav = h('div', { class: 'aiw-nav' },
      prev ? h('button', { type: 'button', onclick: () => (canOpen(prev) ? lessonScreen(prev) : listScreen()) }, '← ' + no(prev)) : h('span'),
      next ? h('button', { type: 'button', onclick: () => (canOpen(next) ? lessonScreen(next) : listScreen()) }, no(next) + (canOpen(next) ? ' →' : ' 🔒')) : h('span'));
    body.replaceChildren(h('button', { class: 'back-link', type: 'button', onclick: listScreen }, '← Các bài của khóa Gia sư AI'), box, nav);
    window.scrollTo(0, 0);
  }

  window.GiaSuAi = {
    open(c) { ctx = Object.assign(ctx, c || {}); body = document.getElementById('giasu-body'); listScreen(); },
    _keys: PARTS.flatMap((p) => p.keys), _free: FREE,
  };
})();
