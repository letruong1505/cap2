// Ôn thi THPT Quốc gia: chọn 2 môn tự chọn, xem khối thi tương ứng, rồi các bước ôn tập.
// Đang ở mức khung: bài học, đề và báo cáo chưa có nội dung. Chạy offline, mọi chữ gán bằng textContent.

(function () {
  const D = window.THPT_EXAM_DATA;
  const KEY = 'nl-thpt-chon';

  const h = (tag, attrs, ...children) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === undefined || v === null || v === false) continue;
      if (k === 'class') n.className = v;
      else if (k.startsWith('on') && typeof v === 'function') n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v === true ? '' : v);
    }
    for (const c of children.flat()) {
      if (c === undefined || c === null || c === false) continue;
      n.append(c instanceof Node ? c : String(c));
    }
    return n;
  };

  const TABS = [
    ['chon', 'Chọn tổ hợp'],
    ['mon', 'Môn ôn'],
    ['bai', 'Bài học'],
    ['de', 'Luyện đề'],
    ['bao-cao', 'Báo cáo'],
  ];

  const state = { tab: 'chon', picked: loadPicked() };
  let root = null;

  function loadPicked() {
    try {
      const v = JSON.parse(localStorage.getItem(KEY) || '[]');
      const ids = D.ELECTIVES.map((e) => e.id);
      return Array.isArray(v) ? v.filter((id) => ids.includes(id)).slice(0, 2) : [];
    } catch (_) {
      return [];
    }
  }
  function savePicked() {
    try { localStorage.setItem(KEY, JSON.stringify(state.picked)); } catch (_) { /* bỏ qua nếu không lưu được */ }
  }
  const nameOf = (id) => (D.ELECTIVES.find((e) => e.id === id) || {}).name || id;

  function togglePick(id) {
    const i = state.picked.indexOf(id);
    if (i >= 0) state.picked.splice(i, 1);
    else if (state.picked.length < 2) state.picked.push(id);
    else { state.picked.shift(); state.picked.push(id); }
    savePicked();
    render();
  }

  function tabBar() {
    return h('nav', { class: 'thpt-tabs', 'aria-label': 'Các bước ôn thi' },
      TABS.map(([id, label]) => h('button', {
        type: 'button',
        class: state.tab === id ? 'thpt-tab active' : 'thpt-tab',
        'aria-pressed': state.tab === id ? 'true' : 'false',
        onclick: () => { state.tab = id; render(); },
      }, label)));
  }

  function panelChon() {
    const picked = state.picked;
    const khoi = D.khoiFor(picked);
    const summary = picked.length < 2
      ? h('p', { class: 'muted' }, `Đã chọn ${picked.length}/2 môn. Chọn đủ 2 môn để xem khối thi.`)
      : h('div', {},
          h('p', { class: 'thpt-combo' }, `Toán + Ngữ văn + ${picked.map(nameOf).join(' + ')}`),
          khoi
            ? h('div', { class: 'nat-chips' }, khoi.map((k) => h('span', {}, `Khối ${k}`)))
            : h('p', { class: 'muted' }, 'Tổ hợp này chưa có trong bảng khối của khung. Sẽ bổ sung khi đối chiếu đủ 36 tổ hợp.'));
    return h('div', {},
      h('section', { class: 'thpt-card' },
        h('h2', {}, 'Cấu trúc kỳ thi qua các năm'),
        h('ul', { class: 'nat-list' }, D.YEARS.map((y) => h('li', {}, h('b', {}, `${y.years}: `), y.text)))),
      h('section', { class: 'thpt-card' },
        h('h2', {}, 'Chọn 2 môn tự chọn'),
        h('p', { class: 'muted' }, 'Ngữ văn và Toán là 2 môn bắt buộc. Chọn 2 trong 9 môn tự chọn.'),
        h('div', { class: 'thpt-grid', role: 'group', 'aria-label': 'Môn tự chọn' },
          D.ELECTIVES.map((e) => h('button', {
            type: 'button',
            class: state.picked.includes(e.id) ? 'thpt-pick sel' : 'thpt-pick',
            'aria-pressed': state.picked.includes(e.id) ? 'true' : 'false',
            onclick: () => togglePick(e.id),
          }, e.name)))),
      h('section', { class: 'thpt-card' },
        h('h2', {}, 'Tổ hợp đã chọn'),
        summary));
  }

  function panelMon() {
    if (state.picked.length < 2) {
      return h('section', { class: 'thpt-card' }, h('p', { class: 'muted' }, 'Hãy chọn 2 môn tự chọn ở bước "Chọn tổ hợp".'));
    }
    const list = ['Toán', 'Ngữ văn', ...state.picked.map(nameOf)];
    return h('div', { class: 'thpt-grid' }, list.map((n) => h('div', { class: 'thpt-subject' },
      h('div', { class: 'thpt-subject-name' }, n),
      h('div', { class: 'muted' }, '0 / 0 bài đã học · đang biên soạn'),
      h('div', { class: 'thpt-bar' }, h('span', { style: 'width:0' })))));
  }

  function placeholder(text) {
    return h('section', { class: 'thpt-card thpt-placeholder' }, h('p', {}, text));
  }

  function body() {
    if (state.tab === 'chon') return panelChon();
    if (state.tab === 'mon') return panelMon();
    if (state.tab === 'bai') return placeholder('Bài học theo môn đang được biên soạn. Mỗi bài sẽ có tóm tắt kiến thức, ví dụ mẫu và bài tập ngắn.');
    if (state.tab === 'de') return placeholder('Đề luyện đang được biên soạn: đề theo môn và đề tổng hợp theo tổ hợp, có chế độ làm bài tính giờ.');
    return placeholder('Báo cáo điểm luyện đề theo thời gian và theo môn đang được hoàn thiện.');
  }

  function render() {
    if (!root) return;
    root.replaceChildren(
      h('header', { class: 'screen-head' },
        h('p', { class: 'screen-kicker' }, 'Lớp 12 · Kỳ thi THPT Quốc gia'),
        h('h1', {}, 'Ôn thi THPT Quốc gia'),
        h('p', { class: 'screen-sub' }, 'Chọn tổ hợp để biết khối thi tương ứng, rồi ôn theo từng môn. Nội dung bài học và đề đang được biên soạn.')),
      tabBar(),
      body());
  }

  window.ThptExam = {
    open() {
      root = document.getElementById('thpt-body');
      state.tab = 'chon';
      state.picked = loadPicked();
      render();
    },
  };
})();
