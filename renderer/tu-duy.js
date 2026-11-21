// "Tư duy & lập trình": hai khóa bán riêng, mỗi khóa 1.490.000 đ: Scratch (8–11) và Python (12–18). Mỗi khóa có vài bài xem thử miễn phí; các bài còn lại mở khi mua đúng khóa đó.
// Khóa bản cũ 'tu-duy-lap-trinh' (đã bán trước khi tách) vẫn mở cả hai.
(function () {
  'use strict';
  const LEGACY_ID = 'tu-duy-lap-trinh';
  const COURSE = { k811: 'tu-duy-lap-trinh-scratch', k1218: 'tu-duy-lap-trinh-python' };
  const FREE = { k811: ['tongquan', 'caidat', 'bai1'], k1218: ['tongquan', 'caidat', 'c1b2'] };
  const TRACKS = {
    k811: { name: 'Lộ trình 8–11 tuổi', tool: 'Scratch', sub: 'Kéo thả khối lệnh để làm nhân vật di chuyển, vẽ hình và chơi trò chơi – đồng thời tập hỏi “vì sao đúng?” và nghĩ ngược.' },
    k1218: { name: 'Lộ trình 12–18 tuổi', tool: 'Python', sub: 'Dùng Python để phân rã bài toán, kiểm thử như một nhà phản biện và giải bài bằng tư duy ngược.' },
  };
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
  const owned = (lic, t) => !!(lic && lic.status === 'ok' && Array.isArray(lic.courses) && (lic.courses.includes(COURSE[t]) || lic.courses.includes(LEGACY_ID)));
  const content = (t) => (window.TUDUY || {})[t] || {};
  let ctx = { license: () => ({}), onBuy() {}, onExit() {} };
  let body;

  const toc = (t) => (window.TUDUY_TOC || {})[t] || [];
  const rowsOf = (t) => toc(t).flatMap((g) => g.items);
  const info = (t, key) => rowsOf(t).find((r) => r.key === key) || { key, label: key, title: key, ready: !!content(t)[key] };
  function canOpen(t, key) { return FREE[t].includes(key) || owned(ctx.license(), t); }
  const no = (t, key) => info(t, key).label || '';
  const shortTitle = (t, key) => info(t, key).title;
  const buyTrack = (t) => { if (window.confirm('Bài này mở khi Anh/Chị mua khóa "Tư duy & lập trình · ' + TRACKS[t].tool + '". Mở màn hình Mua khóa học?')) ctx.onBuy(COURSE[t]); };

  function trackScreen() {
    const lic = ctx.license();
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: () => ctx.onExit() }, '← Chọn khóa'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'Khóa Kỹ năng'), h('h1', {}, 'Tư duy & lập trình'),
        h('p', { class: 'screen-sub' }, 'Lập trình chỉ là công cụ. Điều khóa học rèn là tư duy phản biện (hỏi “vì sao đúng?”) và tư duy ngược (đi từ kết quả về điều kiện ban đầu). Hai khóa bán riêng, mỗi khóa 1.490.000 đ, chọn khóa đúng độ tuổi của con.')),
      h('ul', { class: 'lesson-list' }, Object.keys(TRACKS).map((t) => h('li', {}, h('button', { class: 'lesson-row', type: 'button', onclick: () => listScreen(t) },
        h('span', { class: 'lesson-no' }, TRACKS[t].tool), h('span', { class: 'lesson-name' }, TRACKS[t].name + ' – ' + TRACKS[t].sub),
        owned(lic, t) ? h('span', { class: 'lesson-tag' }, 'Đã mua') : h('span', { class: 'lesson-tag' }, '1.490.000 đ'))))));
    window.scrollTo(0, 0);
  }

  function listScreen(t) {
    const own = owned(ctx.license(), t);
    const groups = toc(t).map((g) => {
      const ul = h('ul', { class: 'lesson-list' }, g.items.map((it) => {
        if (!it.ready) {
          return h('li', {}, h('button', { class: 'lesson-row soon', type: 'button', disabled: 'disabled', 'aria-label': (it.label || '') + ' ' + it.title + ' (sắp ra mắt)' },
            h('span', { class: 'lesson-no' }, it.label || ''), h('span', { class: 'lesson-name' }, it.title), h('span', { class: 'lesson-tag' }, 'Sắp ra mắt')));
        }
        const open = canOpen(t, it.key);
        const r = h('button', { class: 'lesson-row' + (open ? '' : ' locked'), type: 'button', onclick: open ? () => lessonScreen(t, it.key) : () => buyTrack(t) },
          h('span', { class: 'lesson-no' }, it.label || ''), h('span', { class: 'lesson-name' }, it.title),
          FREE[t].includes(it.key) && !own ? h('span', { class: 'lesson-tag' }, 'Xem thử') : null);
        if (!open) { const l = h('span', { class: 'lesson-lock', title: 'Mở khi mua khóa' }); l.innerHTML = LOCK; r.append(l); r.setAttribute('aria-label', (it.label || '') + ' ' + it.title + ' (cần mua khóa)'); }
        return h('li', {}, r);
      }));
      return h('section', { class: 'book' }, g.t ? h('h2', { class: 'book-title' }, g.t) : null, ul);
    });
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: trackScreen }, '← Chọn lộ trình'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'Tư duy & lập trình · ' + TRACKS[t].tool), h('h1', {}, TRACKS[t].name),
        h('p', { class: 'screen-sub' }, TRACKS[t].sub),
        own ? null : h('button', { class: 'primary', type: 'button', onclick: () => ctx.onBuy(COURSE[t]) }, 'Mua khóa Tư duy & lập trình · ' + TRACKS[t].tool + ' (1.490.000 đ)')),
      ...groups);
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
    if (L && canOpen(t, key)) box.innerHTML = '<h2>' + L.title + '</h2>' + (L.sub ? '<p class="sub">' + L.sub + '</p>' : '') + L.html;
    else box.append(h('p', {}, L ? 'Bài này mở khi mua khóa.' : 'Bài này đang được biên soạn.'));
    addCopyButtons(box);
    const keys = rowsOf(t).filter((r) => r.ready).map((r) => r.key);
    const i = keys.indexOf(key), prev = keys[i - 1], next = keys[i + 1];
    const nav = h('div', { class: 'aiw-nav' },
      prev ? h('button', { type: 'button', onclick: () => (canOpen(t, prev) ? lessonScreen(t, prev) : listScreen(t)) }, '← ' + no(t, prev)) : h('span'),
      next ? h('button', { type: 'button', onclick: () => (canOpen(t, next) ? lessonScreen(t, next) : listScreen(t)) }, no(t, next) + (canOpen(t, next) ? ' →' : ' 🔒')) : h('span'));
    body.replaceChildren(h('button', { class: 'back-link', type: 'button', onclick: () => listScreen(t) }, '← Các bài ' + TRACKS[t].name.toLowerCase()), box, nav);
    window.scrollTo(0, 0);
  }

  window.TuDuy = {
    open(c) { ctx = Object.assign(ctx, c || {}); body = document.getElementById('tuduy-body'); trackScreen(); },
    _free: FREE, _course: COURSE, _legacy: LEGACY_ID,
  };
})();
