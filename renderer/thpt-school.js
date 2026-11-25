// Tab "Chọn trường" trong Ôn thi THPT: nhập điểm 4 môn, xem điểm xét tuyển theo từng khối, rồi gợi ý ngành theo điểm chuẩn
// 2026 của các trường, chia 3 miền Bắc - Trung - Nam. Chỉ để tham khảo. Mọi chữ gán bằng textContent, chạy offline.
(function () {
  const L = window.THPT_SCHOOL_LOGIC;
  const KEY = 'nl-thpt-diem';
  const REGIONS = [['bac', 'Miền Bắc'], ['trung', 'Miền Trung'], ['nam', 'Miền Nam']];
  const SHOW = 12;

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
  const fmt = (x) => (Math.round(x * 100) / 100).toString().replace('.', ',');
  const dateVi = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || ''); return m ? `${m[3]}/${m[2]}/${m[1]}` : ''; };

  function load() {
    try {
      const v = JSON.parse(localStorage.getItem(KEY) || '{}');
      return {
        s: v && typeof v.s === 'object' && v.s ? v.s : {},
        kv: L.KV[v.kv] !== undefined ? v.kv : 'KV3',
        dt: L.DT[v.dt] !== undefined ? v.dt : 'none',
        regions: Array.isArray(v.regions) ? v.regions.filter((r) => REGIONS.some((x) => x[0] === r)) : [],
      };
    } catch (_) { return { s: {}, kv: 'KV3', dt: 'none', regions: [] }; }
  }
  function save(st) {
    try { localStorage.setItem(KEY, JSON.stringify({ s: st.s, kv: st.kv, dt: st.dt, regions: st.regions })); } catch (_) { /* bỏ qua nếu không lưu được */ }
  }

  // Dựng tab. picked: 2 mã môn tự chọn; nameOf: mã môn -> tên hiển thị.
  function panel(picked, nameOf) {
    const st = load();
    st.query = ''; st.open = {};
    const wrap = h('div', {});
    const data = window.THPT_SCHOOL_DATA || {};

    function render() {
      save(st);
      const subjects = ['TO', 'VA', ...picked];
      const label = (m) => (m === 'TO' ? 'Toán' : m === 'VA' ? 'Ngữ văn' : nameOf(m));
      const ks = L.khoiScores(st.s, picked, st.kv, st.dt);
      const groups = L.suggest(data, ks, { regions: st.regions, query: st.query });
      const filled = Object.keys(ks).length > 0;

      wrap.replaceChildren(
        h('section', { class: 'thpt-card' },
          h('h2', {}, 'Điểm thi của em'),
          h('p', { class: 'muted' }, 'Nhập điểm 4 môn (thang 10). Dùng điểm thi thử hoặc điểm dự kiến. Kết quả chỉ để tham khảo.'),
          h('div', { class: 'sch-inputs' }, subjects.map((m) => h('label', { class: 'sch-field' },
            h('span', {}, label(m)),
            h('input', {
              type: 'text', inputmode: 'decimal', autocomplete: 'off', 'aria-label': `Điểm ${label(m)}`, value: st.s[m] === undefined ? '' : String(st.s[m]),
              onchange: (e) => { const v = e.target.value.trim(); if (v === '') delete st.s[m]; else st.s[m] = v; render(); },
            })))),
          h('div', { class: 'sch-inputs' },
            h('label', { class: 'sch-field' }, h('span', {}, 'Khu vực ưu tiên'),
              h('select', { 'aria-label': 'Khu vực ưu tiên', onchange: (e) => { st.kv = e.target.value; render(); } },
                Object.keys(L.KV).map((k) => h('option', { value: k, selected: st.kv === k }, L.KV_LABEL[k])))),
            h('label', { class: 'sch-field' }, h('span', {}, 'Đối tượng ưu tiên'),
              h('select', { 'aria-label': 'Đối tượng ưu tiên', onchange: (e) => { st.dt = e.target.value; render(); } },
                Object.keys(L.DT).map((k) => h('option', { value: k, selected: st.dt === k }, L.DT_LABEL[k])))))),

        h('section', { class: 'thpt-card' },
          h('h2', {}, 'Điểm xét tuyển theo từng khối'),
          filled
            ? h('div', { class: 'nat-chips' }, Object.entries(ks).sort((a, b) => b[1].score - a[1].score).map(([k, v]) =>
                h('span', {}, `Khối ${k}: ${fmt(v.score)}${v.bonus ? ` (gồm ưu tiên ${fmt(v.bonus)})` : ''}`)))
            : h('p', { class: 'muted' }, 'Nhập đủ điểm các môn của một khối để xem điểm xét tuyển.'),
          h('p', { class: 'muted' }, 'Điểm ưu tiên: dưới 22,5 điểm được cộng đủ; từ 22,5 điểm trở lên giảm dần theo công thức của Bộ GD&ĐT (Thông tư 06/2026/TT-BGDĐT).')),

        h('section', { class: 'thpt-card' },
          h('h2', {}, 'Gợi ý ngành theo điểm chuẩn 2026'),
          h('div', { class: 'nat-chips sch-regions', role: 'group', 'aria-label': 'Chọn miền' },
            [['', 'Cả nước'], ...REGIONS].map(([id, name]) => {
              const on = id === '' ? st.regions.length === 0 : st.regions.includes(id);
              return h('button', {
                type: 'button', class: on ? 'thpt-tab active' : 'thpt-tab', 'aria-pressed': on ? 'true' : 'false',
                onclick: () => {
                  if (id === '') st.regions = [];
                  else st.regions = st.regions.includes(id) ? st.regions.filter((r) => r !== id) : [...st.regions, id];
                  render();
                },
              }, name);
            })),
          h('ul', { class: 'nat-list sch-meta' }, REGIONS.map(([id, name]) => {
            const d = data[id];
            return h('li', {}, h('b', {}, `${name}: `), d && d.schools.length
              ? `${d.schools.length} trường (${d.schools.map((s) => s.short).join(', ')}). Cập nhật ${dateVi(d.updated)}.`
              : 'chưa có dữ liệu.');
          })),
          h('label', { class: 'sch-field' }, h('span', {}, 'Tìm ngành hoặc trường'),
            h('input', { type: 'search', 'aria-label': 'Tìm ngành hoặc trường', value: st.query, autocomplete: 'off',
              onchange: (e) => { st.query = e.target.value; render(); } })),
          !filled ? h('p', { class: 'muted' }, 'Nhập điểm ở trên để xem gợi ý.') : L.BANDS.map((b) => band(b, groups[b.id]))),

        h('section', { class: 'thpt-card' },
          h('h2', {}, 'Lưu ý khi dùng'),
          h('ul', { class: 'nat-list' },
            h('li', {}, 'Chỉ dùng điểm chuẩn xét điểm thi tốt nghiệp THPT năm 2026. Điểm chuẩn mỗi năm thay đổi theo đề thi và số thí sinh đăng ký.'),
            h('li', {}, 'Phần mềm chưa có đủ mọi trường và mọi ngành. Chưa tính xét học bạ, đánh giá năng lực, ngành năng khiếu, chứng chỉ ngoại ngữ và điểm cộng của từng trường.'),
            h('li', {}, 'Một số trường quy định độ lệch điểm giữa các tổ hợp. Hãy đối chiếu đề án tuyển sinh chính thức của trường trước khi đăng ký nguyện vọng.'))));
    }

    function band(b, list) {
      const open = !!st.open[b.id];
      const shown = open ? list : list.slice(0, SHOW);
      return h('div', { class: `sch-band sch-${b.id}` },
        h('h3', {}, `${b.label} (${list.length})`),
        h('p', { class: 'muted' }, b.hint),
        list.length === 0 ? h('p', { class: 'muted' }, 'Chưa có ngành nào trong nhóm này.') : h('div', { class: 'sch-table', role: 'table' },
          shown.map((x) => h('div', { class: 'sch-row', role: 'row' },
            h('div', { class: 'sch-main' }, h('b', {}, x.name), h('span', { class: 'muted' }, x.school)),
            h('div', { class: 'sch-nums' }, `Khối ${x.khoi} · chuẩn ${fmt(x.cut)} · em ${fmt(x.mine)} (${x.diff >= 0 ? '+' : ''}${fmt(x.diff)})`)))),
        list.length > SHOW ? h('button', { type: 'button', class: 'ghost', onclick: () => { st.open[b.id] = !open; render(); } }, open ? 'Thu gọn' : `Xem thêm ${list.length - SHOW} ngành`) : null);
    }

    render();
    return wrap;
  }

  window.ThptSchool = { panel };
})();
