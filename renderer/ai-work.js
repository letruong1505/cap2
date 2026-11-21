// Khóa "AI cho người đi làm": chọn một trong 3 lớp, xem danh sách bài. 3 bài đầu (phần chung) mở sẵn,
// các bài còn lại chỉ mở khi đã mua lớp tương ứng (giống các lớp Văn hóa).
(function () {
  'use strict';
  const COURSES = [
    { id: 'ai-nguoi-di-lam-chatgpt', ai: 'chatgpt', label: 'ChatGPT', mark: 'GPT', color: '#d9822b',
      strong: ['Việc nhỏ đa dạng mỗi ngày', 'Tạo ảnh, giọng nói', 'Tự dựng trợ lý riêng'], fit: 'Hợp: Bán hàng, truyền thông, quản lý nhỏ',
      own: [
        ['Bài 4', 'Vai trò của ChatGPT và thiết lập an toàn'], ['Bài 5', 'Công thức giao việc và quy trình 6 bước'], ['Bài 6', 'Email, Word và SOP'],
        ['Bài 7', 'Excel và phân tích KPI'], ['Bài 8', 'PowerPoint, cuộc họp và quản lý lịch'], ['Bài 9', 'Hành chính, nhân sự và mua hàng'],
        ['Bài 10', 'Dự án, nghiên cứu nguồn và tự động hóa'], ['Bài 11', 'Năm case study và lộ trình 30 ngày'], ['Bài 12', 'Thư viện 96 prompt và phụ lục'], ['Bài 13', 'Tổng kết lớp ChatGPT và dự án cuối'],
      ] },
    { id: 'ai-nguoi-di-lam-gemini', ai: 'gemini', label: 'Gemini', mark: 'G', color: '#1f6fb2',
      strong: ['Gmail, Docs, Sheets, Drive', 'Tìm thông tin, tài liệu lớn', 'Ảnh và video'], fit: 'Hợp: Văn phòng, kế toán, hành chính',
      own: [
        ['Bài 4', 'Gemini và bản đồ công cụ cho khối văn phòng'], ['Bài 5', 'Viết câu lệnh chuẩn bằng công thức R-C-T-F'], ['Bài 6', 'Email, họp, báo cáo cho nhân viên văn phòng'],
        ['Bài 7', 'Bảng tính, đối chiếu, thuyết minh cho kế toán'], ['Bài 8', 'Văn bản, SOP, báo giá, sự kiện cho hành chính'], ['Bài 9', 'Gemini trong hệ sinh thái Google và NotebookLM'],
        ['Bài 10', 'Bảo mật dữ liệu và kiểm duyệt đầu ra'], ['Bài 11', 'Lộ trình 4 tuần và thư viện câu lệnh'], ['Bài 12', 'Tổng kết lớp Gemini và dự án cuối'],
      ] },
    { id: 'ai-nguoi-di-lam-claude', ai: 'claude', label: 'Claude', mark: 'C', color: '#2a8a4a',
      strong: ['Viết dài, giọng văn tự nhiên', 'Đọc kỹ tài liệu, hợp đồng', 'Lập trình, làm công cụ'], fit: 'Hợp: Giáo viên, tư vấn, kỹ thuật, quản lý',
      own: [
        ['Bài 4', 'Làm xong một việc thật ngay buổi đầu'], ['Bài 5', 'Ra lệnh đúng một lần, sửa cho trúng'], ['Bài 6', 'Giọng văn của Anh/Chị và trợ lý riêng'],
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
        h('p', { class: 'screen-sub' }, 'Chọn AI Anh/Chị muốn học. Mỗi AI là một lớp riêng. 3 bài đầu (phần chung) xem miễn phí, các bài còn lại mở khi mua lớp.')),
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

  function ownSet(c) { return c.ai === 'claude' ? window.AI_WORK_CLAUDE : c.ai === 'chatgpt' ? window.AI_WORK_CHATGPT : c.ai === 'gemini' ? window.AI_WORK_GEMINI : null; }

  function courseScreen(c) {
    const own = owned(ctx.license(), c.id);
    const buy = () => {
      if (window.confirm('Bài này mở khi Anh/Chị mua lớp ' + c.label + '. Mở màn hình Mua khóa học?')) ctx.onBuy(c.id);
    };
    const common = h('ul', { class: 'lesson-list' }, COMMON.map(([no, name, key]) => h('li', {}, row(no, name, 'open', () => lessonScreen(c, key)))));
    const ownList = h('ul', { class: 'lesson-list' });
    if (c.own.length) for (const [no, name] of c.own) {
      const key = 'bai' + no.replace(/\D/g, '');
      const has = !!(ownSet(c) && ownSet(c)[key]);
      ownList.append(h('li', {}, !own ? row(no, name, 'locked', buy) : has ? row(no, name, 'open', () => lessonScreen(c, key)) : row(no, name, 'pending')));
    }
    else ownList.append(h('li', {}, row('Phần riêng', c.label, 'pending')));
    body.replaceChildren(
      h('button', { class: 'back-link', type: 'button', onclick: listScreen }, '← Chọn AI'),
      h('header', { class: 'screen-head' }, h('p', { class: 'screen-kicker' }, 'AI cho người đi làm'), h('h1', {}, 'Lớp học trên ' + c.label),
        h('p', { class: 'screen-sub' }, own ? (c.own.length && ownSet(c) ? 'Anh/Chị đã mua lớp này. Mở từng bài bên dưới để học.' : 'Anh/Chị đã mua lớp này. Phần riêng đang được biên soạn, sẽ có trong phần mềm khi hoàn thành.') : 'Phần chung xem miễn phí. Phần riêng mở khi mua lớp (1.990.000 đ).'),
        own ? null : h('button', { class: 'primary', type: 'button', onclick: () => ctx.onBuy(c.id) }, 'Mua lớp ' + c.label)),
      h('section', { class: 'book' }, h('h2', { class: 'book-title' }, 'Phần chung · Ai học cũng có'), common),
      h('section', { class: 'book' }, h('h2', { class: 'book-title' }, 'Phần riêng · Đi sâu vào ' + c.label), ownList));
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

  function lessonScreen(c, key) {
    const L = (window.AI_WORK_LESSONS || {})[key] || (owned(ctx.license(), c.id) ? (ownSet(c) || {})[key] : null);
    const box = h('article', { class: 'aiw-lesson' });
    if (L) { box.innerHTML = '<h2>' + L.title + '</h2><p class="sub">' + L.sub + '</p>' + L.html; }
    else box.append(h('p', {}, 'Bài này đang được biên soạn.'));
    addCopyButtons(box);
    body.replaceChildren(h('button', { class: 'back-link', type: 'button', onclick: () => courseScreen(c) }, '← Các bài của lớp ' + c.label), box);
    window.scrollTo(0, 0);
  }

  window.AiWork = {
    open(c) { ctx = Object.assign(ctx, c || {}); body = document.getElementById('aiwork-body'); listScreen(); },
  };
})();
