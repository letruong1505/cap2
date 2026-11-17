// Khóa "AI cho người đi làm": chọn một trong 3 lớp, xem danh sách bài. 3 bài đầu (phần chung) mở sẵn,
// các bài còn lại chỉ mở khi đã mua lớp tương ứng (giống các lớp Văn hóa).
(function () {
  'use strict';
  const COURSES = [
    { id: 'ai-nguoi-di-lam-chatgpt', ai: 'chatgpt', label: 'ChatGPT', mark: 'GPT', color: '#d9822b',
      strong: ['Việc nhỏ đa dạng mỗi ngày', 'Tạo ảnh, giọng nói', 'Tự dựng trợ lý riêng'], fit: 'Hợp: bán hàng, truyền thông, quản lý nhỏ', own: [] },
    { id: 'ai-nguoi-di-lam-gemini', ai: 'gemini', label: 'Gemini', mark: 'G', color: '#1f6fb2',
      strong: ['Gmail, Docs, Sheets, Drive', 'Tìm thông tin, tài liệu lớn', 'Ảnh và video'], fit: 'Hợp: văn phòng, kế toán, hành chính', own: [] },
    { id: 'ai-nguoi-di-lam-claude', ai: 'claude', label: 'Claude', mark: 'C', color: '#2a8a4a',
      strong: ['Viết dài, giọng văn tự nhiên', 'Đọc kỹ tài liệu, hợp đồng', 'Lập trình, làm công cụ'], fit: 'Hợp: giáo viên, tư vấn, kỹ thuật, quản lý',
      own: [
        ['Bài 4', 'Làm xong một việc thật ngay buổi đầu'], ['Bài 5', 'Ra lệnh đúng một lần, sửa cho trúng'], ['Bài 6', 'Giọng văn của bạn và trợ lý riêng'],
        ['Bài 7', 'Đọc nhanh, nghĩ rõ, quyết nhanh'], ['Bài 8', 'Biến thành sản phẩm và file'], ['Bài 9', 'Ứng dụng theo nghề (Giáo dục · Kinh doanh – truyền thông · Dữ liệu)'],
        ['Bài 10', 'Tự động hóa và nâng cao'], ['Bài 11', 'Tổng kết, dự án cuối và đo năng suất'],
      ] },
  ];
  const COMMON = [['Bài 1', 'An toàn', 'bai1'], ['Bài 2', 'Trách nhiệm', 'bai2'], ['Bài 3', 'Kiểm chứng', 'bai3']];
  const LOCK = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';

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
  const owned = (lic, id) => !!(lic && lic.status === 'ok' && Array.isArray(lic.courses) && lic.courses.includes(id));

  let ctx = { license: () => ({}), onBuy() {}, onExit() {} };
  let body;

  function listScreen() {
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: () => ctx.onExit() }, '← Chọn lớp'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'Khóa Kỹ năng'), h('h1', {}, 'AI cho người đi làm'),
        h('p', { class: 'screen-sub' }, 'Chọn AI bạn muốn học. Mỗi AI là một lớp riêng. 3 bài đầu (phần chung) xem miễn phí, các bài còn lại mở khi mua lớp.')),
      h('div', { class: 'aiw-cards' }, COURSES.map((c) => {
        const own = owned(ctx.license(), c.id);
        return h('button', { class: 'aiw-card', type: 'button', onclick: () => courseScreen(c) },
          h('span', { class: 'ai-logo', style: 'background:' + c.color }, c.mark),
          h('span', { class: 'ai-name' }, c.label),
          own ? h('span', { class: 'aiw-own' }, 'Đã mua') : null,
          h('span', { class: 'ai-k' }, 'MẠNH NHẤT Ở'), h('ul', {}, c.strong.map((t) => h('li', {}, t))),
          h('span', { class: 'ai-fit' }, c.fit),
          h('span', { class: 'aiw-go' }, 'Xem các bài →'));
      })));
    window.scrollTo(0, 0);
  }

  function row(no, name, kind, onclick) {
    const r = h(kind === 'pending' ? 'span' : 'button', { class: 'lesson-row' + (kind === 'locked' ? ' locked' : '') + (kind === 'pending' ? ' pending' : ''), type: kind === 'pending' ? null : 'button', onclick },
      h('span', { class: 'lesson-no' }, no), h('span', { class: 'lesson-name' }, name),
      kind === 'pending' ? h('span', { class: 'lesson-tag' }, 'Đang biên soạn') : null);
    if (kind === 'locked') { const l = h('span', { class: 'lesson-lock', title: 'Cần mua lớp' }); l.innerHTML = LOCK; r.append(l); r.setAttribute('aria-label', no + ' ' + name + ' (cần mua lớp)'); }
    return r;
  }

  function courseScreen(c) {
    const own = owned(ctx.license(), c.id);
    const buy = () => {
      if (window.confirm('Bài này mở khi bạn mua lớp ' + c.label + '. Mở màn hình Mua khóa học?')) ctx.onBuy(c.id);
    };
    const common = h('ul', { class: 'lesson-list' }, COMMON.map(([no, name, key]) => h('li', {}, row(no, name, 'open', () => lessonScreen(c, key)))));
    const ownList = h('ul', { class: 'lesson-list' });
    if (c.own.length) for (const [no, name] of c.own) ownList.append(h('li', {}, own ? row(no, name, 'pending') : row(no, name, 'locked', buy)));
    else ownList.append(h('li', {}, row('Phần riêng', c.label, 'pending')));
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: listScreen }, '← Chọn AI'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'AI cho người đi làm'), h('h1', {}, 'Lớp học trên ' + c.label),
        h('p', { class: 'screen-sub' }, own ? 'Bạn đã mua lớp này. Phần riêng đang được biên soạn, sẽ có trong phần mềm khi hoàn thành.' : 'Phần chung xem miễn phí. Phần riêng mở khi mua lớp (1.990.000 đ).'),
        own ? null : h('button', { class: 'primary', type: 'button', onclick: () => ctx.onBuy(c.id) }, 'Mua lớp ' + c.label)),
      h('section', { class: 'book' }, h('h2', { class: 'book-title' }, 'Phần chung · Ai học cũng có'), common),
      h('section', { class: 'book' }, h('h2', { class: 'book-title' }, 'Phần riêng · Đi sâu vào ' + c.label), ownList));
    window.scrollTo(0, 0);
  }

  function lessonScreen(c, key) {
    const L = (window.AI_WORK_LESSONS || {})[key];
    const box = h('article', { class: 'aiw-lesson' });
    if (L) { box.innerHTML = '<h2>' + L.title + '</h2><p class="sub">' + L.sub + '</p>' + L.html; }
    else box.append(h('p', {}, 'Bài này đang được biên soạn.'));
    body.replaceChildren(h('button', { class: 'back-link', type: 'button', onclick: () => courseScreen(c) }, '← Các bài của lớp ' + c.label), box);
    window.scrollTo(0, 0);
  }

  window.AiWork = {
    open(c) { ctx = Object.assign(ctx, c || {}); body = document.getElementById('aiwork-body'); listScreen(); },
  };
})();
