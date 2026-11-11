// Màn hình "Mua khóa học": phụ huynh nhập thông tin, chọn khóa, đồng ý điều khoản, nhận mã QR chuyển khoản.
(function () {
  'use strict';
  const CATALOG = window.NL_CATALOG.GROUPS;
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

  let timer = null;
  let polling = 0;
  const PENDING_KEY = 'nl-pending-order';
  const savePending = (o) => { try { o ? localStorage.setItem(PENDING_KEY, JSON.stringify({ code: o.code })) : localStorage.removeItem(PENDING_KEY); } catch { /* bỏ qua */ } };
  const loadPending = () => { try { return JSON.parse(localStorage.getItem(PENDING_KEY) || 'null'); } catch { return null; } };
  function stopPoll() { if (timer) clearInterval(timer); timer = null; }

  function showDone(o) {
    const P = window.NL_PAYMENT;
    const names = ALL.filter((x) => o.ids.includes(x.id)).map((x) => x.name);
    payEl.replaceChildren(
      h('h2', {}, 'Thanh toán thành công'),
      h('p', { class: 'buy-ok' }, 'Khóa học đã được kích hoạt trên máy này.'),
      h('ul', { class: 'buy-lines' }, names.map((n) => h('li', {}, h('span', {}, n)))),
      h('p', { class: 'muted' }, 'Cần hỗ trợ: Zalo ' + P.zalo + '.'),
      h('div', { class: 'buy-actions' }, h('button', { type: 'button', class: 'primary', onclick: () => document.getElementById('btn-purchase-back').click() }, 'Về màn hình chính')));
    payEl.hidden = false; summaryEl.hidden = true; createBtn.hidden = true; hint.hidden = true;
  }

  // Hỏi máy chủ xem đơn đã được thanh toán chưa; có tiền thì nhận key và tự kích hoạt.
  async function check(o, statusEl) {
    const r = await window.vungBai.orderStatus(o.code);
    if (!r.ok) { statusEl.textContent = r.offline ? 'Chưa kết nối được máy chủ. Em kiểm tra mạng rồi bấm "Kiểm tra thanh toán".' : (r.error || 'Không kiểm tra được đơn.'); return; }
    const d = r.data;
    if (d.status === 'paid' && d.key) {
      stopPoll();
      const a = await window.vungBai.activateLicense(d.key);
      if (a.status === 'ok') {
        savePending(null);
        if (ctx.onActivated) ctx.onActivated();
        showDone(o);
      } else statusEl.textContent = 'Đã nhận tiền nhưng chưa kích hoạt được khóa. Em liên hệ Zalo ' + window.NL_PAYMENT.zalo + ' kèm mã đơn NL-' + o.code + '.';
    } else if (d.status === 'paid') statusEl.textContent = 'Đã nhận tiền, đang cấp khóa...';
    else if (d.status === 'underpaid') statusEl.textContent = 'Đã nhận ' + money(d.paidAmount) + ', còn thiếu ' + money(d.amount - d.paidAmount) + '. Em chuyển thêm đúng nội dung NL ' + o.code + '.';
    else if (d.status === 'cancelled') { stopPoll(); savePending(null); statusEl.textContent = 'Đơn này đã được hủy. Em tạo đơn mới.'; }
    else statusEl.textContent = 'Đang chờ thanh toán. Phần mềm sẽ tự kích hoạt khi nhận được tiền.';
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
    const statusEl = h('p', { class: 'buy-status', 'aria-live': 'polite' }, o.online ? 'Đang chờ thanh toán. Phần mềm sẽ tự kích hoạt khi nhận được tiền.' : '');
    const actions = o.online
      ? [h('button', { type: 'button', class: 'primary', onclick: () => { statusEl.textContent = 'Đang kiểm tra...'; check(o, statusEl); } }, 'Kiểm tra thanh toán')]
      : [h('button', { type: 'button', class: 'primary', onclick: async () => {
          try { await navigator.clipboard.writeText(orderText(o)); copyMsg.textContent = 'Đã sao chép thông tin đơn.'; }
          catch { copyMsg.textContent = 'Không sao chép được. Em chụp màn hình để gửi.'; }
        } }, 'Sao chép thông tin đơn')];
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
      o.online ? statusEl
        : h('p', { class: 'buy-after' }, 'Chưa kết nối được máy chủ nên chưa tự kích hoạt được. Sau khi chuyển khoản, em gửi ảnh biên lai kèm mã đơn NL-' + o.code + ' qua Zalo ' + P.zalo + '. Nam Linh sẽ gửi khóa kích hoạt sau khi xác nhận thanh toán.'),
      h('div', { class: 'buy-actions' }, actions,
        h('button', { type: 'button', class: 'ghost', onclick: () => { stopPoll(); savePending(null); st.order = null; payEl.hidden = true; summaryEl.hidden = false; createBtn.hidden = false; hint.hidden = false; renderSummary(); } }, o.online ? 'Tạo đơn khác' : 'Sửa đơn'),
        copyMsg));
    payEl.hidden = false; summaryEl.hidden = true; createBtn.hidden = true; hint.hidden = true;
    stopPoll();
    if (o.online) {
      polling = Date.now();
      check(o, statusEl);
      timer = setInterval(() => {
        const panel = document.getElementById('purchase');
        if (!panel || panel.hidden) { stopPoll(); return; }
        if (Date.now() - polling > 30 * 60 * 1000) { stopPoll(); statusEl.textContent = 'Đã dừng tự kiểm tra. Em bấm "Kiểm tra thanh toán" sau khi chuyển khoản.'; return; }
        check(o, statusEl);
      }, 5000);
    }
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
    createBtn = h('button', { type: 'button', class: 'primary buy-create', onclick: async () => {
      if (!formOk()) return;
      createBtn.disabled = true; hint.textContent = 'Đang tạo đơn...';
      const at = new Date().toLocaleString('vi-VN');
      const base = { name: st.name.trim(), phone: normPhone(st.phone), ids: ALL.filter((x) => st.picks.has(x.id)).map((x) => x.id), at };
      const r = await window.vungBai.createOrder({ name: base.name, phone: base.phone, ids: base.ids, terms: { version: window.NL_TERMS.version, at } });
      let o;
      if (r.ok) o = { ...base, code: r.data.code, amount: r.data.amount, online: true };
      else if (r.offline) o = { ...base, code: newCode(), amount: total(), online: false };
      else { hint.textContent = r.error; createBtn.disabled = false; return; }
      st.order = o;
      if (o.online) savePending(o);
      showPay(o);
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

  // Mở lại phần mềm khi còn đơn đang chờ: hỏi máy chủ rồi hiện lại mã QR hoặc tự kích hoạt nếu đã trả tiền.
  async function resume(code) {
    const r = await window.vungBai.orderStatus(code);
    if (!r.ok || !r.data) return;
    const d = r.data;
    if (d.status === 'pending' || d.status === 'underpaid' || (d.status === 'paid' && d.key)) {
      const o = { code, amount: d.amount, ids: d.items || [], name: '', phone: '', online: true };
      st.order = o; showPay(o);
    } else savePending(null);
  }

  window.Purchase = {
    open(c) {
      ctx = c || ctx;
      root = document.getElementById('purchase-body');
      stopPoll();
      build();
      const pending = !st.order && loadPending();
      if (pending && pending.code) resume(pending.code);
      const first = document.getElementById('buy-name');
      if (first && !st.order) first.focus();
    },
  };
})();
