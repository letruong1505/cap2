// Phụ huynh xem tóm tắt nội dung Giáo trình văn hóa theo lớp và môn: kiến thức cần nhớ, dạng bài, các bước giải, lỗi dễ mắc.
// Dữ liệu nằm ở digest/van-hoa-<lớp>.js (tạo bởi tools/build-parent-digest.py), chỉ tải khi phụ huynh mở lớp đó.
(function () {
  'use strict';
  function h(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) { if (k === 'class') e.className = v; else if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else if (v != null && v !== false) e.setAttribute(k, v); }
    for (const c of kids.flat()) if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c)));
    return e;
  }
  const loaded = {};
  function load(grade) {
    const store = (window.PARENT_DIGEST = window.PARENT_DIGEST || {});
    if (store[grade]) return Promise.resolve(store[grade]);
    if (!loaded[grade]) {
      loaded[grade] = new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = 'digest/van-hoa-' + grade + '.js';
        s.onload = () => (store[grade] ? resolve(store[grade]) : reject(new Error('empty')));
        s.onerror = () => { loaded[grade] = null; reject(new Error('load')); };
        document.head.append(s);
      });
    }
    return loaded[grade];
  }

  const list = (title, items, cls) => items && items.length ? h('div', { class: 'dg-block ' + (cls || '') }, h('h4', {}, title), h('ul', {}, items.map((t) => h('li', {}, t)))) : null;

  function lessonView(l) {
    const body = h('div', { class: 'dg-lesson' },
      list('Yêu cầu cần đạt', l.req),
      list('Kiến thức cần nhớ', l.sum),
      list('Dạng bài thường gặp', l.d));
    (l.m || []).forEach((m) => {
      body.append(h('div', { class: 'dg-block dg-method' }, h('h4', {}, 'Cách giải: ' + m.t),
        m.w ? h('p', { class: 'meta' }, 'Khi nào dùng: ' + m.w) : null,
        m.s && m.s.length ? h('ol', {}, m.s.map((t) => h('li', {}, t))) : null));
    });
    body.append(list('Lỗi dễ mắc phải', l.e, 'dg-err'));
    if (l.q) {
      const lv = Object.entries(l.q.lv || {}).map(([k, v]) => k + ' ' + v).join(' · ');
      body.append(h('p', { class: 'meta' }, 'Bài luyện trong app của con: ' + l.q.n + ' câu' + (lv ? ' (' + lv + ')' : '') + ', có giải thích từng đáp án.'));
    }
    return h('details', { class: 'edu-note dg-l' }, h('summary', {}, l.t), body);
  }

  function render(root, data, sid, grade) {
    const subs = data.subjects;
    const cur = subs.find((s) => s.id === sid) || subs[0];
    const tabs = h('div', { class: 'dg-tabs' }, subs.map((s) => h('button', { type: 'button', class: s === cur ? 'primary' : 'ghost', onclick: () => render(root, data, s.id, grade) }, s.name)));
    const body = h('div', {});
    cur.b.forEach((b) => {
      if (cur.b.length > 1) body.append(h('h3', {}, b.t));
      b.c.forEach((c) => {
        const d = h('details', { class: 'goal-box dg-chapter' }, h('summary', {}, h('b', {}, c.t), h('span', { class: 'meta' }, ' · ' + c.l.length + ' bài')));
        c.l.forEach((l) => d.append(lessonView(l)));
        body.append(d);
      });
    });
    root.replaceChildren(
      h('h1', {}, 'Nội dung lớp ' + grade),
      h('p', { class: 'screen-sub' }, 'Tóm tắt từng bài: kiến thức cần nhớ, dạng bài, các bước giải và lỗi dễ mắc, để phụ huynh biết con đang học gì và kèm con đúng chỗ. Bài tập và đáp án chi tiết nằm trong app học của con.'),
      tabs, body);
  }

  window.ParentDigest = {
    open(root, grade) {
      root.replaceChildren(h('h1', {}, 'Nội dung lớp ' + grade), h('p', { class: 'meta' }, 'Đang tải...'));
      return load(grade).then((data) => render(root, data, '', grade))
        .catch(() => root.replaceChildren(h('h1', {}, 'Nội dung lớp ' + grade), h('p', { class: 'buy-warn' }, 'Không tải được nội dung. Hãy thử lại.')));
    },
  };
})();
