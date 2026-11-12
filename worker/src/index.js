import catalog from '../../renderer/catalog.js';
import { HttpError, createOrder, orderStatus, applyPayment, listOrders, listUnmatched, approveOrder, cancelOrder, reissueOrder, attachTransaction } from './orders.js';
import { adminPage } from './admin.js';

const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

// So sánh chuỗi bí mật theo thời gian không đổi.
function safeEqual(a, b) {
  const x = new TextEncoder().encode(String(a)); const y = new TextEncoder().encode(String(b));
  let d = x.length ^ y.length;
  for (let i = 0; i < Math.max(x.length, y.length); i++) d |= (x[i] || 0) ^ (y[i] || 0);
  return d === 0;
}

const bearer = (req) => (req.headers.get('authorization') || '').replace(/^Bearer\s+/i, '');
const sepayKey = (req) => (req.headers.get('authorization') || '').replace(/^Apikey\s+/i, '');

async function body(req) {
  try { return await req.json(); } catch { throw new HttpError(400, 'Dữ liệu gửi lên không hợp lệ.'); }
}

export async function handle(req, env, now = new Date()) {
  const url = new URL(req.url);
  const path = url.pathname.replace(/\/+$/, '') || '/';
  const db = env.DB;
  try {
    // --- Phần mềm khách ---
    if (req.method === 'POST' && path === '/api/orders') {
      return json(await createOrder(db, catalog, await body(req), now), 201);
    }
    let m = /^\/api\/orders\/([A-Za-z0-9]{6})\/status$/.exec(path);
    if (req.method === 'GET' && m) {
      return json(await orderStatus(db, env, catalog, m[1], url.searchParams.get('machine'), now));
    }

    // --- SePay gọi vào khi có tiền về ---
    if (req.method === 'POST' && path === '/api/sepay') {
      if (!env.SEPAY_API_KEY || !safeEqual(sepayKey(req), env.SEPAY_API_KEY)) return json({ success: false }, 401);
      const raw = await req.text();
      let d; try { d = JSON.parse(raw); } catch { return json({ success: false }, 400); }
      if (d.transferType !== 'in' || !Number.isInteger(d.id) || !(d.transferAmount > 0)) return json({ success: true, ignored: true });
      const result = await applyPayment(db, env, catalog, { id: d.id, reference: d.referenceCode, amount: Math.round(d.transferAmount), content: d.content, code: d.code, raw: raw.slice(0, 2000) }, now);
      return json({ success: true, result });
    }

    // --- Quản trị ---
    if (req.method === 'GET' && path === '/admin') return adminPage();
    if (path.startsWith('/api/admin/')) {
      if (!env.ADMIN_TOKEN || !safeEqual(bearer(req), env.ADMIN_TOKEN)) return json({ error: 'Sai mật khẩu quản trị.' }, 401);
      if (req.method === 'GET' && path === '/api/admin/orders') return json({ orders: await listOrders(db, { status: url.searchParams.get('status') || '', q: url.searchParams.get('q') || '' }), catalog: catalog.byId });
      if (req.method === 'GET' && path === '/api/admin/transactions') return json({ transactions: await listUnmatched(db) });
      m = /^\/api\/admin\/transactions\/(\d+)\/attach$/.exec(path);
      if (req.method === 'POST' && m) { const b = await body(req); return json(await attachTransaction(db, env, catalog, Number(m[1]), b.code, now)); }
      m = /^\/api\/admin\/orders\/([A-Za-z0-9]{6})\/(approve|cancel|reissue)$/.exec(path);
      if (req.method === 'POST' && m) {
        const b = await body(req);
        if (m[2] === 'approve') return json({ key: await approveOrder(db, env, catalog, m[1], b.note, now) });
        if (m[2] === 'cancel') { await cancelOrder(db, m[1], b.note); return json({ ok: true }); }
        return json({ key: await reissueOrder(db, env, catalog, m[1], b.machine, now) });
      }
    }
    if (path === '/') return new Response('Nam Linh Educenter orders API', { status: 200 });
    return json({ error: 'Không tìm thấy.' }, 404);
  } catch (e) {
    if (e instanceof HttpError) return json({ error: e.message }, e.status);
    console.error('lỗi', e && e.stack || e);
    return json({ error: 'Lỗi máy chủ.' }, 500);
  }
}

export default { fetch: (req, env) => handle(req, env) };
