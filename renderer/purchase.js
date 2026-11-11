// Màn hình "Mua khóa học": phụ huynh nhập thông tin, chọn khóa, đồng ý điều khoản, nhận mã QR chuyển khoản.
(function () {
  'use strict';
  const CATALOG = [
    { group: 'Khóa Kỹ năng', items: [
      { id: 'gia-su-ai', name: 'Gia sư AI', note: 'Học sinh từ 12 tuổi trở lên', price: 999000, was: 1600000 },
      { id: 'he-mien-dich-so', name: 'Hệ miễn dịch số', note: 'Học sinh 8 - 11 tuổi', price: 2090000 },
      { id: 'lam-chu-the-gioi-so', name: 'Làm chủ thế giới số', note: 'Học sinh 12 - 15 tuổi', price: 2590000 },
      { id: 'cong-dan-so', name: 'Công dân số', note: 'Học sinh 16 - 18 tuổi', price: 2990000 },
      { id: 'ranh-gioi-so', name: 'Ranh giới số', note: 'Học sinh THPT & tân sinh viên', price: 1590000 },
    ] },
    { group: 'Giáo trình Văn hóa', items: [6, 7, 8, 9, 12].map((g) => ({
      id: 'van-hoa-' + g, name: 'Giáo trình Văn hóa lớp ' + g, note: g === 12 ? '2 môn học' : '6 môn học', price: g === 12 ? 499000 : 399000 })) },
  ];
  const ALL = CATALOG.flatMap((c) => c.items);
  const money = (n) => n.toLocaleString('vi-VN') + ' đ';

  function h(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') e.className = v;
      else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (v === true) e.setAttribute(k, '');
      else if (v !== false && v != null) e.setAttribute(k, v);
    }
    for (const c of kids.flat()) if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c)));
    return e;
  }

  function newCode() {
    const abc = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
    const a = new Uint8Array(6);
    (window.crypto || { getRandomValues: (x) => x.map(() => Math.floor(Math.random() * 256)) }).getRandomValues(a);
    return Array.from(a, (x) => abc[x % abc.length]).join('');
  }

  function qrSvg(text) {
    const qr = window.qrcode(0, 'M');
    qr.addData(text);
    qr.make();
    const n = qr.getModuleCount();
    const quiet = 3;
    let d = '';
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (qr.isDark(r, c)) d += `M${c + quiet} ${r + quiet}h1v1h-1z`;
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', `0 0 ${n + quiet * 2} ${n + quiet * 2}`);
    svg.setAttribute('class', 'buy-qr');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Mã QR chuyển khoản');
    svg.setAttribute('shape-rendering', 'crispEdges');
    const bg = document.createElementNS(ns, 'rect');
    bg.setAttribute('width', '100%'); bg.setAttribute('height', '100%'); bg.setAttribute('fill', '#fff');
    const p = document.createElementNS(ns, 'path');
    p.setAttribute('d', d); p.setAttribute('fill', '#000');
    svg.append(bg, p);
    return svg;
  }

  const normPhone = (s) => s.replace(/[\s.\-]/g, '');
  const phoneOk = (s) => /^(0|\+84)\d{9}$/.test(normPhone(s));

  let ctx = { machineId: '' };
  const st = { name: '', phone: '', picks: new Set(), agreed: false, order: null };

  function total() { return ALL.filter((x) => st.picks.has(x.id)).reduce((s, x) => s + x.price, 0); }
  function formOk() { return st.name.trim().length >= 2 && phoneOk(st.phone) && st.picks.size > 0 && st.agreed; }

  function orderText(o) {
    const P = window.NL_PAYMENT;
    const lines = ALL.filter((x) => o.ids.includes(x.id)).map((x) => `- ${x.name}: ${money(x.price)}`);
    return [
      'ĐƠN MUA KHÓA HỌC NAM LINH EDUCENTER',
      `Mã đơn: NL-${o.code}`,
      `Phụ huynh: ${o.name}`,
      `Số điện thoại: ${o.phone}`,
      ctx.machineId ? `Mã máy: ${ctx.machineId}` : '',
      'Khóa học:', ...lines,
      `Tổng tiền: ${money(o.amount)}`,
      `Nội dung chuyển khoản: NL ${o.code}`,
      `Đã đồng ý Điều khoản ${window.NL_TERMS.version} lúc ${o.at}`,
      `Gửi ảnh biên lai kèm mã đơn qua Zalo ${P.zalo}`,
    ].filter(Boolean).join('\n');
  }

  let root, summaryEl, payEl, createBtn, hint;

  function renderSummary() {
    const sel = ALL.filter((x) => st.picks.has(x.id));
    summaryEl.replaceChildren(
      h('h2', {}, 'Đơn hàng'),
      sel.length ? h('ul', { class: 'buy-lines' }, sel.map((x) => h('li', {}, h('span', {}, x.name), h('b', {}, money(x.price)))))
        : h('p', { class: 'muted' }, 'Chưa chọn khóa học nào.'),
      h('div', { class: 'buy-total' }, h('span', {}, 'Tổng tiền'), h('b', {}, money(total()))));
    const miss = [];
    if (st.name.trim().length < 2) miss.push('họ và tên');
    if (!phoneOk(st.phone)) miss.push('số điện thoại hợp lệ');
    if (!st.picks.size) miss.push('ít nhất một khóa học');
    if (!st.agreed) miss.push('đồng ý điều khoản');
    createBtn.disabled = !formOk();
    hint.textContent = miss.length ? 'Còn thiếu: ' + miss.join(', ') + '.' : '';
  }

  function showPay(o) {
    const P = window.NL_PAYMENT;
    let qr;
    if (P.bankBin && P.accountNo) {
      try { qr = qrSvg(window.VietQR.build({ bin: P.bankBin, account: P.accountNo, amount: o.amount, content: 'NL ' + o.code })); }
      catch (e) { qr = h('p', { class: 'buy-warn' }, 'Không tạo được mã QR: ' + e.message); }
    } else qr = h('p', { class: 'buy-warn' }, 'Chưa cài đặt tài khoản nhận tiền. Em liên hệ Zalo ' + P.zalo + ' để được hướng dẫn chuyển khoản.');
    const row = (k, v, strong) => h('div', { class: 'buy-row' }, h('span', {}, k), strong ? h('b', {}, v) : h('span', {}, v));
    const copyMsg = h('span', { class: 'muted', 'aria-live': 'polite' }, '');
    payEl.replaceChildren(
      h('h2', {}, 'Quét mã để thanh toán'),
      qr,
      h('div', { class: 'buy-bank' },
        P.bankName ? row('Ngân hàng', P.bankName) : null,
        P.accountNo ? row('Số tài khoản', P.accountNo, true) : null,
        P.accountName ? row('Chủ tài khoản', P.accountName) : null,
        row('Số tiền', money(o.amount), true),
        row('Nội dung', 'NL ' + o.code, true),
        row('Mã đơn', 'NL-' + o.code)),
      h('p', { class: 'buy-after' }, 'Sau khi chuyển khoản, em gửi ảnh biên lai kèm mã đơn NL-' + o.code + ' qua Zalo ' + P.zalo + '. Nam Linh sẽ gửi khóa kích hoạt sau khi xác nhận thanh toán.'),
      h('div', { class: 'buy-actions' },
        h('button', { type: 'button', class: 'primary', onclick: async () => {
          try { await navigator.clipboard.writeText(orderText(o)); copyMsg.textContent = 'Đã sao chép thông tin đơn.'; }
          catch { copyMsg.textContent = 'Không sao chép được. Em chụp màn hình để gửi.'; }
        } }, 'Sao chép thông tin đơn'),
        h('button', { type: 'button', class: 'ghost', onclick: () => { st.order = null; payEl.hidden = true; summaryEl.hidden = false; createBtn.hidden = false; hint.hidden = false; } }, 'Sửa đơn'),
        copyMsg));
    payEl.hidden = false; summaryEl.hidden = true; createBtn.hidden = true; hint.hidden = true;
  }

  function build() {
    const T = window.NL_TERMS;
    const name = h('input', { type: 'text', id: 'buy-name', autocomplete: 'off', placeholder: 'Nguyễn Văn A', maxlength: '60' });
    const phone = h('input', { type: 'tel', id: 'buy-phone', autocomplete: 'off', placeholder: '09xx xxx xxx', maxlength: '15', inputmode: 'tel' });
    name.addEventListener('input', () => { st.name = name.value; renderSummary(); });
    phone.addEventListener('input', () => { st.phone = phone.value; renderSummary(); });
    name.value = st.name; phone.value = st.phone;

    const groups = CATALOG.map((c) => h('fieldset', { class: 'buy-group' }, h('legend', {}, c.group),
      c.items.map((x) => {
        const cb = h('input', { type: 'checkbox', checked: st.picks.has(x.id) });
        cb.addEventListener('change', () => { cb.checked ? st.picks.add(x.id) : st.picks.delete(x.id); renderSummary(); });
        return h('label', { class: 'buy-item' }, cb,
          h('span', { class: 'buy-iname' }, x.name, h('small', {}, x.note)),
          h('span', { class: 'buy-iprice' }, money(x.price), x.was ? h('s', {}, money(x.was)) : null));
      })));

    const terms = h('div', { class: 'buy-terms', tabindex: '0', role: 'region', 'aria-label': 'Điều khoản mua và sử dụng' },
      h('p', { class: 'muted' }, 'Điều khoản mua và sử dụng của Nam Linh Technology, phiên bản ' + T.version),
      T.sections.map(([t, ps]) => h('section', {}, h('h4', {}, t), ps.map((p) => h('p', {}, p)))));
    const agree = h('input', { type: 'checkbox', id: 'buy-agree', checked: st.agreed });
    agree.addEventListener('change', () => { st.agreed = agree.checked; renderSummary(); });

    summaryEl = h('section', { class: 'buy-card buy-summary' });
    payEl = h('section', { class: 'buy-card buy-pay', hidden: true });
    hint = h('p', { class: 'muted buy-hint', 'aria-live': 'polite' });
    createBtn = h('button', { type: 'button', class: 'primary buy-create', onclick: () => {
      if (!formOk()) return;
      const now = new Date();
      const o = { code: newCode(), name: st.name.trim(), phone: normPhone(st.phone), ids: ALL.filter((x) => st.picks.has(x.id)).map((x) => x.id), amount: total(),
        at: now.toLocaleString('vi-VN') };
      st.order = o; showPay(o);
    } }, 'Tạo mã QR thanh toán');

    root.replaceChildren(
      h('h1', {}, 'Mua khóa học'),
      h('p', { class: 'screen-sub' }, 'Dành cho phụ huynh. Nhập thông tin, chọn khóa học của con, đồng ý điều khoản rồi quét mã QR để thanh toán.'),
      h('div', { class: 'buy-layout' },
        h('div', { class: 'buy-main' },
          h('section', { class: 'buy-card' }, h('h2', {}, h('span', { class: 'buy-n' }, '1'), 'Thông tin phụ huynh'),
            h('div', { class: 'buy-fields' },
              h('label', { for: 'buy-name' }, 'Họ và tên', name),
              h('label', { for: 'buy-phone' }, 'Số điện thoại (Zalo)', phone))),
          h('section', { class: 'buy-card' }, h('h2', {}, h('span', { class: 'buy-n' }, '2'), 'Chọn khóa học của con'),
            h('p', { class: 'muted' }, 'Chọn một hoặc nhiều khóa. Mỗi khóa dùng vĩnh viễn trên 1 máy.'), groups),
          h('section', { class: 'buy-card' }, h('h2', {}, h('span', { class: 'buy-n' }, '3'), 'Điều khoản'), terms,
            h('label', { class: 'buy-agree', for: 'buy-agree' }, agree,
              h('span', {}, 'Tôi là phụ huynh, người giám hộ hoặc người từ đủ 18 tuổi, đã đọc và đồng ý Điều khoản mua và sử dụng của Nam Linh Technology.')))),
        h('aside', { class: 'buy-side' }, summaryEl, payEl, hint, createBtn)));
    renderSummary();
    if (st.order) showPay(st.order);
  }

  window.Purchase = {
    open(c) {
      ctx = c || ctx;
      root = document.getElementById('purchase-body');
      build();
      const first = document.getElementById('buy-name');
      if (first) first.focus();
    },
  };
})();
