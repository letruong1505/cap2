// Cổng đối tác (chỉ xem): đối tác mở liên kết riêng để xem số khóa/máy đang hoạt động trong kỳ, phục vụ đối soát hoa hồng.
// Liên kết dùng mã truy cập tính từ ADMIN_TOKEN (+ PARTNER_SALT nếu có) và tên đối tác nên không cần bảng dữ liệu mới.
import { listOrders } from './orders.js';

// Quy định hoa hồng: 25% trên số tiền khách thực trả cho từng khóa; tổng hoa hồng trong kỳ vượt 5 triệu thì khấu trừ 10% trên toàn bộ số đó (thuế).
export const COMMISSION_PERCENT = 25;
export const TAX_THRESHOLD = 5000000;
export const TAX_PERCENT = 10;
export const commissionOf = (paid) => Math.round(paid * COMMISSION_PERCENT / 100);
export function commissionTotal(gross) {
  const tax = gross > TAX_THRESHOLD ? Math.round(gross * TAX_PERCENT / 100) : 0;
  return { percent: COMMISSION_PERCENT, gross, taxPercent: TAX_PERCENT, taxThreshold: TAX_THRESHOLD, tax, net: gross - tax };
}

const b64url = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

export async function partnerToken(env, name) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode('partner-portal:' + env.ADMIN_TOKEN + ':' + (env.PARTNER_SALT || '')), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64url(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(String(name)))).slice(0, 32);
}

function same(a, b) {
  const x = new TextEncoder().encode(String(a)); const y = new TextEncoder().encode(String(b));
  let d = x.length ^ y.length;
  for (let i = 0; i < Math.max(x.length, y.length); i++) d |= (x[i] || 0) ^ (y[i] || 0);
  return d === 0;
}

// Danh sách liên kết để quản trị gửi cho từng đối tác.
export async function partnerLinks(db, env) {
  if (!env.ADMIN_TOKEN) return [];
  const names = (await db.prepare('SELECT DISTINCT partner FROM partner_codes ORDER BY partner').all()).results.map((r) => r.partner);
  const out = [];
  for (const partner of names) out.push({ partner, token: await partnerToken(env, partner) });
  return out;
}

export async function partnerByToken(db, env, token) {
  if (!env.ADMIN_TOKEN || typeof token !== 'string' || token.length < 20 || token.length > 64) return null;
  const names = (await db.prepare('SELECT DISTINCT partner FROM partner_codes').all()).results.map((r) => r.partner);
  let found = null;
  for (const n of names) if (same(await partnerToken(env, n), token)) found = n;
  return found;
}

const maskPhone = (p) => { const s = String(p || '').replace(/\D/g, ''); return s.length >= 4 ? '•'.repeat(s.length - 3) + s.slice(-3) : ''; };

// Tổng hợp theo đơn có mã của đối tác: "đang hoạt động" = đơn đã thanh toán, chưa thu hồi, khóa chưa bị thu hồi riêng.
export async function partnerSummary(db, catalog, partner, { from, to } = {}, now = new Date()) {
  const codes = new Set((await db.prepare('SELECT code FROM partner_codes WHERE partner = ?1').bind(partner).all()).results.map((r) => r.code));
  const orders = await listOrders(db, { partner, from, to }, now);
  let gross = 0;
  const sum = { orders: 0, items: 0, machines: 0, list: 0, paid: 0, refundedItems: 0, pendingOrders: 0 };
  const machines = new Set(); const byCourse = new Map(); const list = [];
  for (const o of orders) {
    if (o.status === 'cancelled') continue;
    const gone = new Set((o.item_revoked || []).map((r) => r.item));
    const ids = Object.keys(o.prices || {}).filter((id) => o.prices[id].partner_code && codes.has(o.prices[id].partner_code));
    if (!ids.length) continue;
    if (o.status !== 'paid') { sum.pendingOrders++; continue; }
    let active = 0; let paid = 0; let ocm = 0; const names = [];
    for (const id of ids) {
      const name = catalog.byId[id] ? catalog.byId[id].name : id;
      names.push(o.revoked || gone.has(id) ? name + ' (đã thu hồi)' : name);
      if (o.revoked || gone.has(id)) { sum.refundedItems++; continue; }
      active++; paid += o.prices[id].paid; ocm += commissionOf(o.prices[id].paid); sum.items++; sum.list += o.prices[id].list; sum.paid += o.prices[id].paid;
      const cm = commissionOf(o.prices[id].paid); gross += cm;
      const c = byCourse.get(id) || { id, name, count: 0, paid: 0, commission: 0 }; c.count++; c.paid += o.prices[id].paid; c.commission += cm; byCourse.set(id, c);
    }
    if (active) { sum.orders++; for (const s of Object.values(o.slots || {})) if (s && s.machine) machines.add(s.machine); }
    list.push({ code: 'NL-' + o.code, date: String(o.created_at).slice(0, 10), phone: maskPhone(o.phone), items: names, paid, commission: ocm, active: active > 0 });
  }
  sum.machines = machines.size;
  return { partner, from: from || '', to: to || '', summary: sum, commission: commissionTotal(gross), byCourse: [...byCourse.values()].sort((a, b) => b.count - a.count), orders: list.slice(0, 500) };
}

const PAGE = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Đối tác - Nam Linh Educenter</title>
<style nonce="__N__">
:root{--ink:#1c2733;--mut:#64748b;--line:#e2e8f0;--navy:#14304f;--bg:#f1f5f9}
*{box-sizing:border-box}body{font:15px/1.55 "Segoe UI",system-ui,sans-serif;margin:0;background:var(--bg);color:var(--ink)}
header{background:linear-gradient(135deg,#0f2a47,#1d4a7a);color:#fff;padding:14px 22px}header h1{margin:0;font-size:18px}header small{opacity:.8}
main{max-width:980px;margin:0 auto;padding:18px 18px 48px}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end;margin-bottom:10px}.bar label{display:flex;flex-direction:column;font-size:12px;font-weight:700;color:var(--mut);gap:4px}
input,button{font:inherit;padding:8px 12px;border-radius:10px;border:1px solid #cbd5e1;background:#fff}button{background:var(--navy);color:#fff;border-color:var(--navy);font-weight:600;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:12px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(15,23,42,.06)}.card b{display:block;font-size:26px;color:var(--navy)}.card span{color:var(--mut);font-size:13px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:10px 0}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;font-size:14px}th{background:#f8fafc;color:var(--mut);font-size:12px;text-transform:uppercase}
.gone{color:#94a3b8;text-decoration:line-through}h2{font-size:16px;margin:24px 0 4px}.muted{color:var(--mut);font-size:13px}#msg{color:#b42318;font-weight:600;min-height:22px}
</style></head><body>
<header><h1>Đối tác Nam Linh Educenter</h1><small id="who"></small></header>
<main><div id="msg"></div>
<div class="bar"><label>Từ ngày<input id="fd" type="date"></label><label>Đến ngày<input id="td" type="date"></label><button id="go">Xem</button></div>
<div class="muted">Chọn khoảng ngày theo ngày khách đặt đơn; hoa hồng và mức khấu trừ thuế tính theo khoảng ngày đang chọn. Chỉ tính đơn đã thanh toán và chưa bị hoàn hoặc thu hồi.</div>
<div class="grid" id="sum"></div><div id="cm"></div><h2>Theo khóa học</h2><div id="byc"></div><h2>Chi tiết đơn</h2><div id="lst"></div>
<p class="muted">Trang chỉ để xem. Số điện thoại khách được che, chỉ hiện 3 số cuối. Giữ kín liên kết của bạn; cần đổi liên kết hãy báo Nam Linh Educenter.</p></main>
<script nonce="__N__">
(function(){
var tok=decodeURIComponent((location.hash||'').replace(/^#/,'')),msg=document.getElementById('msg');
function el(t,a){var e=document.createElement(t);for(var k in(a||{}))e.setAttribute(k,a[k]);for(var i=2;i<arguments.length;i++){var c=arguments[i];if(c==null)continue;e.append(c.nodeType?c:document.createTextNode(String(c)))}return e}
function money(n){return new Intl.NumberFormat('vi-VN').format(n)+' đ'}
function table(head,rows){var t=el('table',{});t.append(el('tr',{},...head.map(function(h){return el('th',{},h)})));rows.forEach(function(r){t.append(el('tr',{},...r.map(function(c){return el('td',{},c)})))});return t}
function load(){
  msg.textContent='';
  if(!tok){msg.textContent='Thiếu mã truy cập. Hãy mở đúng liên kết Nam Linh Educenter đã gửi.';return}
  fetch('/api/partner/summary',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token:tok,from:document.getElementById('fd').value,to:document.getElementById('td').value})})
  .then(function(r){return r.json().then(function(d){if(!r.ok)throw new Error(d.error||'Lỗi');return d})}).then(function(d){
    document.getElementById('who').textContent='Đối tác: '+d.partner;var s=d.summary,g=document.getElementById('sum');g.replaceChildren();
    var cm=d.commission;
    [['Khóa đang hoạt động',s.items],['Đơn đang hoạt động',s.orders],['Máy đã kích hoạt',s.machines],['Khách thực trả',money(s.paid)],['Hoa hồng '+cm.percent+'%',money(cm.gross)],['Khóa đã hoàn/thu hồi',s.refundedItems],['Đơn chờ thanh toán',s.pendingOrders]].forEach(function(x){g.append(el('div',{class:'card'},el('b',{},x[1]),el('span',{},x[0])))});
    var ct=document.getElementById('cm');ct.replaceChildren(el('div',{class:'card'},
      el('div',{},'Hoa hồng '+cm.percent+'% trên số tiền khách thực trả của từng khóa: ',el('b',{style:'display:inline;font-size:16px'},money(cm.gross))),
      cm.tax>0?el('div',{},'Tổng hoa hồng vượt '+money(cm.taxThreshold)+' nên khấu trừ '+cm.taxPercent+'% thuế trên toàn bộ: -'+money(cm.tax)):el('div',{class:'muted'},'Tổng hoa hồng chưa vượt '+money(cm.taxThreshold)+' nên chưa khấu trừ thuế.'),
      el('div',{style:'margin-top:6px'},'Thực nhận: ',el('b',{style:'display:inline;font-size:20px'},money(cm.net)))));
    var b=document.getElementById('byc');b.replaceChildren(d.byCourse.length?table(['Khóa học','Số lượng','Khách thực trả','Hoa hồng'],d.byCourse.map(function(c){return [c.name,c.count,money(c.paid),money(c.commission)]})):el('p',{class:'muted'},'Chưa có khóa nào trong kỳ này.'));
    var l=document.getElementById('lst');l.replaceChildren(d.orders.length?table(['Mã đơn','Ngày','SĐT khách','Khóa học','Thực trả','Hoa hồng'],d.orders.map(function(o){return [o.code,o.date,o.phone,o.items.join(', '),o.active?money(o.paid):'Đã hoàn/thu hồi',o.active?money(o.commission):'—']})):el('p',{class:'muted'},'Chưa có đơn.'));
  }).catch(function(e){msg.textContent=e.message==='Failed to fetch'?'Không kết nối được máy chủ.':e.message})
}
document.getElementById('go').onclick=load;load();
})();
</script></body></html>`;

export function partnerPage() {
  const nonce = btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(16))));
  return new Response(PAGE.replaceAll('__N__', nonce), { headers: {
    'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store',
    'content-security-policy': `default-src 'none'; script-src 'nonce-${nonce}'; style-src 'nonce-${nonce}'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`,
    'x-content-type-options': 'nosniff', 'referrer-policy': 'no-referrer' } });
}
