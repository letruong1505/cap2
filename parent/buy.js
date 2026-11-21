// Phụ huynh mua khóa học cho con ngay trên app Phụ huynh. Đơn không gắn với điện thoại của phụ huynh:
// máy của con (máy tính và điện thoại) nhập "mã gia đình" một lần rồi tự nhận khóa mỗi khi có mạng.
(function () {
  'use strict';
  const CATALOG = window.NL_CATALOG.GROUPS;
  const ALL = CATALOG.flatMap((c) => c.items);
  const money = (n) => n.toLocaleString('vi-VN') + ' đ';
  const FAM_KEY = 'nl-parent-family'; // { fcode, phone, name }
  const PEND_KEY = 'nl-parent-pending'; // { code }
  const ls = () => { try { return window.localStorage; } catch (e) { return null; } };
  const load = (k) => { try { return JSON.parse(ls().getItem(k) || 'null'); } catch (e) { return null; } };
  const save = (k, v) => { try { v == null ? ls().removeItem(k) : ls().setItem(k, JSON.stringify(v)); } catch (e) { /* bỏ qua */ } };

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
  function qrSvg(text) {
    const qr = window.qrcode(0, 'M'); qr.addData(text); qr.make();
    const n = qr.getModuleCount(); const quiet = 3; let d = '';
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (qr.isDark(r, c)) d += `M${c + quiet} ${r + quiet}h1v1h-1z`;
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', `0 0 ${n + quiet * 2} ${n + quiet * 2}`); svg.setAttribute('class', 'buy-qr');
    svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'Mã QR chuyển khoản'); svg.setAttribute('shape-rendering', 'crispEdges');
    const bg = document.createElementNS(ns, 'rect'); bg.setAttribute('width', '100%'); bg.setAttribute('height', '100%'); bg.setAttribute('fill', '#fff');
    const p = document.createElementNS(ns, 'path'); p.setAttribute('d', d); p.setAttribute('fill', '#000');
    svg.append(bg, p);
    return svg;
  }
  const normPhone = (s) => s.replace(/[\s.\-]/g, '');
  const phoneOk = (s) => /^(0|\+84)\d{9}$/.test(normPhone(s));

  const fam = load(FAM_KEY) || {};
  const st = { name: fam.name || '', phone: fam.phone || '', picks: new Set(), agreed: false, refundOk: false, partner: '' };
  let root; let timer = null;
  const stopPoll = () => { if (timer) clearInterval(timer); timer = null; };

  function familyCard(fcode) {
    const msg = h('span', { class: 'muted', 'aria-live': 'polite' });
    return h('div', { class: 'goal-box family-box' },
      h('h2', {}, 'Mã gia đình: ', h('b', { class: 'family-code' }, fcode)),
      h('p', {}, 'Trên máy của con (máy tính và điện thoại), mở app Nam Linh Educenter → phần bản quyền → ô ', h('b', {}, 'Phụ huynh mua cho con?'), ' → nhập mã này một lần. Từ đó khóa học bạn mua tự về máy của con mỗi khi có mạng.'),
      h('button', { type: 'button', class: 'ghost', onclick: async () => {
        try { await navigator.clipboard.writeText(fcode); msg.textContent = 'Đã sao chép mã.'; } catch (e) { msg.textContent = 'Không sao chép được, hãy chép tay.'; }
      } }, 'Sao chép mã'), ' ', msg);
  }

  function done(code, d) {
    const f = load(FAM_KEY) || {};
    const names = ALL.filter((x) => (d.items || []).includes(x.id)).map((x) => x.name);
    save(PEND_KEY, null); stopPoll();
    root.replaceChildren(
      h('h1', {}, 'Thanh toán thành công'),
      h('p', { class: 'buy-ok' }, 'Đơn NL-' + code + ' đã được ghi nhận.'),
      h('ul', { class: 'buy-lines' }, names.map((n) => h('li', {}, h('span', {}, n)))),
      f.fcode ? familyCard(f.fcode) : null,
      h('p', { class: 'muted' }, 'Mỗi đơn dùng được cho 1 máy tính và 1 điện thoại của con. Khóa về máy của con khi máy đó mở app và có mạng. Xem lại phiếu thanh toán trên web: https://nam-linh-orders.namlinh.workers.dev/hoa-don (nhập mã đơn và số điện thoại). Cần hỗ trợ: Zalo ' + window.NL_PAYMENT.zalo + '.'),
      h('button', { type: 'button', class: 'primary', onclick: () => document.querySelector('#buy [data-back]').click() }, 'Xong'));
  }

  async function check(code, statusEl) {
    const r = await window.vungBai.orderStatus(code);
    if (!r.ok) { statusEl.textContent = r.offline ? 'Chưa kết nối được máy chủ. Hãy kiểm tra mạng rồi bấm "Kiểm tra thanh toán".' : (r.error || 'Không kiểm tra được đơn.'); return; }
    const d = r.data;
    if (d.status === 'paid') done(code, d);
    else if (d.status === 'underpaid') statusEl.textContent = 'Đã nhận ' + money(d.paidAmount) + ', còn thiếu ' + money(d.amount - d.paidAmount) + '. Hãy chuyển thêm đúng nội dung NL ' + code + '.';
    else if (d.status === 'cancelled') { stopPoll(); save(PEND_KEY, null); statusEl.textContent = 'Đơn này đã được hủy. Hãy tạo đơn mới.'; }
    else statusEl.textContent = 'Đang chờ thanh toán. App sẽ tự cập nhật khi nhận được tiền.';
  }

  function showPay(o) {
    const P = window.NL_PAYMENT;
    let qr;
    if (P.bankBin && P.accountNo) {
      try { qr = qrSvg(window.VietQR.build({ bin: P.bankBin, account: P.accountNo, amount: o.amount, content: 'NL ' + o.code })); }
      catch (e) { qr = h('p', { class: 'buy-warn' }, 'Không tạo được mã QR: ' + e.message); }
    } else qr = h('p', { class: 'buy-warn' }, 'Chưa cài đặt tài khoản nhận tiền. Hãy liên hệ Zalo ' + P.zalo + '.');
    const row = (k, v, strong) => h('div', { class: 'buy-row' }, h('span', {}, k), strong ? h('b', {}, v) : h('span', {}, v));
    const statusEl = h('p', { class: 'buy-status', 'aria-live': 'polite' }, 'Đang chờ thanh toán. App sẽ tự cập nhật khi nhận được tiền.');
    const f = load(FAM_KEY) || {};
    root.replaceChildren(
      h('h1', {}, 'Quét mã để thanh toán'),
      h('div', { class: 'buy-card' }, qr,
        h('div', { class: 'buy-bank' },
          P.bankName ? row('Ngân hàng', P.bankName) : null,
          P.accountNo ? row('Số tài khoản', P.accountNo, true) : null,
          P.accountName ? row('Chủ tài khoản', P.accountName) : null,
          o.partner ? row('Mã đối tác', o.partner.code + ' (giảm ' + o.partner.percent + '%)') : null,
          row('Số tiền', money(o.amount), true), row('Nội dung', 'NL ' + o.code, true), row('Mã đơn', 'NL-' + o.code)),
        statusEl,
        h('div', { class: 'buy-actions' },
          h('button', { type: 'button', class: 'primary', onclick: () => { statusEl.textContent = 'Đang kiểm tra...'; check(o.code, statusEl); } }, 'Kiểm tra thanh toán'),
          h('button', { type: 'button', class: 'ghost', onclick: () => { stopPoll(); save(PEND_KEY, null); build(); } }, 'Hủy, chọn lại'))),
      f.fcode ? familyCard(f.fcode) : null);
    stopPoll();
    const t0 = Date.now();
    check(o.code, statusEl);
    timer = setInterval(() => {
      const panel = document.getElementById('buy');
      if (!panel || panel.hidden) { stopPoll(); return; }
      if (Date.now() - t0 > 30 * 60 * 1000) { stopPoll(); statusEl.textContent = 'Đã dừng tự kiểm tra. Bấm "Kiểm tra thanh toán" sau khi chuyển khoản.'; return; }
      check(o.code, statusEl);
    }, 5000);
  }

  function build() {
    const T = window.NL_TERMS;
    const name = h('input', { type: 'text', id: 'pbuy-name', autocomplete: 'off', placeholder: 'Nguyễn Văn A', maxlength: '60', value: st.name });
    const phone = h('input', { type: 'tel', id: 'pbuy-phone', autocomplete: 'off', placeholder: '09xx xxx xxx', maxlength: '15', inputmode: 'tel', value: st.phone });
    const partner = h('input', { type: 'text', id: 'pbuy-partner', autocomplete: 'off', placeholder: 'Nếu có mã đối tác', maxlength: '20', value: st.partner });
    const summary = h('div', { class: 'buy-card' });
    const hint = h('p', { class: 'muted buy-hint', 'aria-live': 'polite' });
    const create = h('button', { type: 'button', class: 'primary buy-create' }, 'Tạo mã QR thanh toán');
    const total = () => ALL.filter((x) => st.picks.has(x.id)).reduce((s, x) => s + x.price, 0);
    const formOk = () => st.name.trim().length >= 2 && phoneOk(st.phone) && st.picks.size > 0 && st.agreed && st.refundOk;
    function render() {
      const sel = ALL.filter((x) => st.picks.has(x.id));
      summary.replaceChildren(h('h2', {}, 'Đơn hàng'),
        sel.length ? h('ul', { class: 'buy-lines' }, sel.map((x) => h('li', {}, h('span', {}, x.name), h('b', {}, money(x.price))))) : h('p', { class: 'muted' }, 'Chưa chọn khóa học nào.'),
        h('div', { class: 'buy-total' }, h('span', {}, 'Tổng tiền'), h('b', {}, money(total()))));
      const miss = [];
      if (st.name.trim().length < 2) miss.push('họ và tên');
      if (!phoneOk(st.phone)) miss.push('số điện thoại hợp lệ');
      if (!st.picks.size) miss.push('ít nhất một khóa học');
      if (!st.agreed) miss.push('đồng ý điều khoản');
      if (!st.refundOk) miss.push('xác nhận chính sách hoàn tiền');
      create.disabled = !formOk();
      hint.textContent = miss.length ? 'Còn thiếu: ' + miss.join(', ') + '.' : '';
    }
    name.addEventListener('input', () => { st.name = name.value; render(); });
    phone.addEventListener('input', () => { st.phone = phone.value; render(); });
    partner.addEventListener('input', () => { st.partner = partner.value; });

    const groups = CATALOG.map((c) => h('fieldset', { class: 'buy-group' }, h('legend', {}, c.group), c.fee ? h('p', { class: 'buy-fee' }, c.fee) : null,
      c.items.map((x) => {
        const cb = h('input', { type: 'checkbox', checked: st.picks.has(x.id) });
        cb.addEventListener('change', () => { cb.checked ? st.picks.add(x.id) : st.picks.delete(x.id); render(); });
        return h('label', { class: 'buy-item' }, cb, h('span', { class: 'buy-iname' }, x.name, h('small', {}, x.note)),
          h('span', { class: 'buy-iprice' }, money(x.price), x.was ? h('s', {}, money(x.was)) : null));
      })));
    const terms = h('div', { class: 'buy-terms', tabindex: '0', role: 'region', 'aria-label': 'Điều khoản mua và sử dụng' },
      h('p', { class: 'muted' }, 'Điều khoản mua và sử dụng của Nam Linh Technology, phiên bản ' + T.version),
      T.sections.map(([t, ps]) => h('section', {}, h('h4', {}, t), ps.map((p) => h('p', {}, p)))));
    const agree = h('input', { type: 'checkbox', id: 'pbuy-agree' });
    agree.addEventListener('change', () => { st.agreed = agree.checked; render(); });
    const refund = h('input', { type: 'checkbox', id: 'pbuy-refund' });
    refund.addEventListener('change', () => { st.refundOk = refund.checked; render(); });
    const refundBox = h('div', { class: 'buy-refund' }, h('h3', {}, 'Chính sách hoàn tiền'),
      h('ul', {},
        h('li', {}, 'Hoàn tiền trong 07 ngày kể từ khi thanh toán thành công, chỉ khi phần mềm có lỗi kỹ thuật mà Nam Linh không khắc phục được.'),
        h('li', {}, 'Không hoàn tiền khi đổi ý sau khi đã kích hoạt. Được hỗ trợ đổi thiết bị miễn phí.'),
        h('li', {}, 'Đơn có mã đối tác: Số tiền hoàn là số tiền đã trả sau khi giảm, không phải giá niêm yết.'),
        h('li', {}, 'Có thể học thử các bài miễn phí trong app của con trước khi mua.')),
      h('label', { class: 'buy-agree', for: 'pbuy-refund' }, refund, h('span', {}, 'Tôi đã đọc và đồng ý chính sách hoàn tiền trên.')));

    create.addEventListener('click', async () => {
      if (!formOk()) return;
      create.disabled = true; hint.textContent = 'Đang tạo đơn...';
      const phoneN = normPhone(st.phone);
      const fr = await window.vungBai.familyCreate({ phone: phoneN });
      if (!fr.ok) { hint.textContent = fr.offline ? 'Cần kết nối mạng để mua. Hãy kiểm tra mạng rồi thử lại.' : fr.error; create.disabled = false; return; }
      const fcode = fr.data.fcode;
      save(FAM_KEY, { fcode, phone: phoneN, name: st.name.trim() });
      const at = new Date().toLocaleString('vi-VN');
      const r = await window.vungBai.createOrder({ name: st.name.trim(), phone: phoneN, ids: ALL.filter((x) => st.picks.has(x.id)).map((x) => x.id), partnerCode: st.partner.trim(), family: fcode, terms: { version: T.version, at } });
      if (!r.ok) { hint.textContent = r.offline ? 'Cần kết nối mạng để mua. Hãy kiểm tra mạng rồi thử lại.' : r.error; create.disabled = false; return; }
      const o = { code: r.data.code, amount: r.data.amount, partner: r.data.partner };
      save(PEND_KEY, { code: o.code });
      if (o.amount === 0) { showPay(o); return; }
      showPay(o);
    });

    const f = load(FAM_KEY);
    root.replaceChildren(
      h('h1', {}, 'Mua khóa học cho con'),
      h('p', { class: 'screen-sub' }, 'Bạn thanh toán ngay trên điện thoại này. Khóa học tự về máy tính và điện thoại của con khi con mở app học có mạng (con nhập "mã gia đình" một lần).'),
      f && f.fcode ? familyCard(f.fcode) : null,
      h('section', { class: 'buy-card' }, h('h2', {}, '1. Thông tin phụ huynh'),
        h('div', { class: 'buy-fields' }, h('label', { for: 'pbuy-name' }, 'Họ và tên', name), h('label', { for: 'pbuy-phone' }, 'Số điện thoại (Zalo)', phone))),
      h('section', { class: 'buy-card' }, h('h2', {}, '2. Chọn khóa học của con'),
        h('p', { class: 'muted' }, 'Mỗi khóa dùng vĩnh viễn trên 1 máy tính và 1 điện thoại của con.'), groups,
        h('div', { class: 'buy-partner' }, h('label', { for: 'pbuy-partner' }, 'Mã đối tác (không bắt buộc)', partner))),
      h('section', { class: 'buy-card' }, h('h2', {}, '3. Điều khoản'), terms,
        h('label', { class: 'buy-agree', for: 'pbuy-agree' }, agree, h('span', {}, 'Tôi là phụ huynh, người giám hộ hoặc người từ đủ 18 tuổi, đã đọc và đồng ý Điều khoản mua và sử dụng của Nam Linh Technology.')),
        refundBox),
      summary, hint, create);
    render();
  }

  async function resume() {
    const p = load(PEND_KEY);
    if (!p || !p.code) return false;
    const r = await window.vungBai.orderStatus(p.code);
    if (!r.ok || !r.data) return false;
    const d = r.data;
    if (d.status === 'pending' || d.status === 'underpaid') { showPay({ code: p.code, amount: d.amount, partner: d.partner || null }); return true; }
    save(PEND_KEY, null);
    return false;
  }

  window.ParentBuy = {
    open(el, opts) {
      root = el; stopPoll();
      if (opts && opts.preselect && window.NL_CATALOG.byId[opts.preselect]) st.picks.add(opts.preselect);
      build();
      resume();
    },
    familyCode() { const f = load(FAM_KEY); return f && f.fcode || ''; },
  };
})();
