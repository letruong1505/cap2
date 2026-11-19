// Trang phiếu xác nhận thanh toán (/hoa-don). Khách nhập mã đơn và số điện thoại đã đặt đơn để xem lại phiếu.
// Không có script trên trang. Mọi dữ liệu được escape trước khi đưa vào HTML.
import { getOrder, linePrices } from './orders.js';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const money = (n) => String(Math.round(Number(n) || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' đ';
const normPhone = (s) => String(s || '').replace(/[\s.\-]/g, '');

// Giờ Việt Nam (UTC+7) dạng hh:mm dd/mm/yyyy.
function timeVi(iso) {
  if (!iso) return '';
  const d = new Date(new Date(iso).getTime() + 7 * 3600e3);
  const p = (n) => String(n).padStart(2, '0');
  return `${p(d.getUTCHours())}:${p(d.getUTCMinutes())} ${p(d.getUTCDate())}/${p(d.getUTCMonth() + 1)}/${d.getUTCFullYear()}`;
}

const SELLER = 'Công ty TNHH Giải pháp & Ứng dụng Công nghệ Nam Linh · MST 2902274556 · Xã Hùng Châu, Nghệ An · Zalo 0968 646 853';

const CSS = `body{font:16px/1.5 system-ui,sans-serif;margin:0;background:#f4f7fb;color:#1c2733}
main{max-width:720px;margin:0 auto;padding:24px}
.card{background:#fff;border:1px solid #dbe3ec;border-radius:12px;padding:20px 24px;margin-bottom:16px}
h1{font-size:22px;margin:0 0 6px;color:#15324e}h2{font-size:17px;margin:0 0 10px;color:#15324e}
table{width:100%;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid #e3e9f0;text-align:left;font-size:15px}
td.n,th.n{text-align:right;white-space:nowrap}s{color:#8a8f96}
.muted{color:#5d6d80;font-size:14px}.err{color:#9b2b1f;font-weight:600}
input{font:inherit;padding:9px 12px;border:1px solid #c5d0dc;border-radius:8px;margin:4px 0;width:100%;box-sizing:border-box}
button{font:inherit;font-weight:700;padding:10px 18px;border:0;border-radius:8px;background:#15324e;color:#fff;cursor:pointer}
.tot{font-weight:700;font-size:17px}`;

function shell(title, body) {
  return new Response(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><style>${CSS}</style></head><body><main>${body}</main></body></html>`, {
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'no-store',
      'content-security-policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
      'x-content-type-options': 'nosniff',
      'referrer-policy': 'no-referrer',
    },
  });
}

function form(code, phone, error) {
  return `<div class="card"><h1>Xem phiếu xác nhận thanh toán</h1>
<p class="muted">Nhập mã đơn (6 ký tự, ví dụ ABC123) và số điện thoại đã dùng khi đặt mua khóa học.</p>
${error ? `<p class="err">${esc(error)}</p>` : ''}
<form method="get" action="/hoa-don">
<label>Mã đơn<input name="code" value="${esc(code)}" maxlength="10" autocomplete="off" required></label>
<label>Số điện thoại<input name="phone" value="${esc(phone)}" maxlength="15" autocomplete="off" required></label>
<p><button type="submit">Xem phiếu</button></p>
</form></div>
<p class="muted">${esc(SELLER)}</p>`;
}

function receipt(o, lines) {
  const rows = lines.map((l) => `<tr><td>${esc(l.name)}</td>
<td class="n">${l.list !== l.paid ? `<s>${esc(money(l.list))}</s>` : esc(money(l.list))}</td>
<td class="n">${esc(money(l.paid))}</td></tr>`).join('');
  const partner = lines.find((l) => l.partner);
  return `<div class="card">
<h1>Phiếu xác nhận thanh toán</h1>
<p class="muted">Mã đơn NL-${esc(o.code)} · Thanh toán lúc ${esc(timeVi(o.paidAt))}</p>
<p><b>Phụ huynh:</b> ${esc(o.name)} · <b>Số điện thoại:</b> ${esc(o.phone)}</p>
</div>
<div class="card"><h2>Khóa học đã mua</h2>
<table><tr><th>Khóa học</th><th class="n">Giá niêm yết</th><th class="n">Đã thanh toán</th></tr>${rows}
<tr><td class="tot">Tổng đã thanh toán</td><td></td><td class="n tot">${esc(money(o.paidAmount))}</td></tr></table>
${partner ? `<p class="muted">Đã áp mã đối tác ${esc(partner.partner.code)}: giảm ${esc(partner.partner.percent)}% trên giá từng khóa.</p>` : ''}
</div>
<div class="card muted">Phiếu này xác nhận khoản thanh toán cho khóa học trên phần mềm Nam Linh Educenter. Đây không phải hóa đơn giá trị gia tăng.<br>${esc(SELLER)}</div>`;
}

export async function receiptPage(db, catalog, url) {
  const code = String(url.searchParams.get('code') || '').trim().toUpperCase().replace(/^NL-?/, '');
  const phone = String(url.searchParams.get('phone') || '');
  if (!code && !phone) return shell('Phiếu xác nhận thanh toán', form('', '', ''));
  if (!/^[A-Z0-9]{6}$/.test(code)) return shell('Phiếu xác nhận thanh toán', form(code, phone, 'Mã đơn gồm 6 ký tự.'));
  const o = await getOrder(db, code);
  // Cùng một thông báo cho mọi trường hợp không khớp, để không đoán được mã đơn của người khác.
  if (!o || normPhone(o.phone) !== normPhone(phone)) {
    return shell('Phiếu xác nhận thanh toán', form(code, phone, 'Mã đơn hoặc số điện thoại không khớp.'));
  }
  if (o.status !== 'paid') {
    return shell('Phiếu xác nhận thanh toán', `<div class="card"><h1>Đơn chưa thanh toán đủ</h1>
<p>Đơn NL-${esc(o.code)} chưa có phiếu xác nhận. Nếu bạn đã chuyển khoản, vui lòng liên hệ Zalo 0968 646 853 kèm mã đơn.</p></div>`);
  }
  const items = JSON.parse(o.items);
  const lines = await linePrices(db, o.code, catalog, items);
  const view = { code: o.code, name: o.name, phone: o.phone, paidAt: o.paid_at, paidAmount: o.paid_amount || 0 };
  return shell('Phiếu xác nhận thanh toán', receipt(view, lines));
}
