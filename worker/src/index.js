import catalog from '../../renderer/catalog.js';
import { HttpError, createOrder, orderStatus, applyPayment, listOrders, listUnmatched, approveOrder, cancelOrder, reissueOrder, attachTransaction, pinReset, claimDevice, revokeOrder, restoreOrder, revokeItem, restoreItem, ping, listPartnerCodes, createPartnerCode, setPartnerActive } from './orders.js';
import { adminPage } from './admin.js';
import { importLegacy } from './legacy.js';
import { registerLegacy } from './register.js';
import { progressSettings, progressPush, progressView } from './progress.js';
import { receiptPage } from './receipt.js';

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

const OTA_MAX_BYTES = 12 * 1024 * 1024;

function updatesBase(env) {
  const b = String(env.UPDATES_BASE || '').trim().replace(/\/+$/, '');
  if (!/^https:\/\//i.test(b)) throw new HttpError(503, 'Chưa cấu hình nơi lưu bản cập nhật.');
  return b;
}

// Thông tin bản mới nhất của ứng dụng Android (latest.json do workflow build đẩy lên R2).
async function androidLatest(env) {
  const base = updatesBase(env);
  const r = await fetch(base + '/educenter-android/latest.json', { cf: { cacheTtl: 60 } }).catch(() => null);
  if (!r || !r.ok) throw new HttpError(502, 'Chưa đọc được thông tin bản mới.');
  let j;
  try { j = await r.json(); } catch { throw new HttpError(502, 'Thông tin bản mới không hợp lệ.'); }
  const n = (v) => (Number.isInteger(v) && v >= 0 ? v : 0);
  const apk = /^[A-Za-z0-9._-]{1,80}$/.test(String(j.apk || '')) ? String(j.apk) : 'nam-linh-educenter.apk';
  return json({
    version: String(j.version || '').slice(0, 20), versionCode: n(j.versionCode), otaBuild: n(j.otaBuild), minNative: n(j.minNative),
    notes: String(j.notes || '').slice(0, 1500), apkUrl: base + '/educenter-android/' + apk,
  });
}

// Gói cập nhật nội dung (OTA) của một bản build. Gói đã được ký; ứng dụng tự kiểm tra chữ ký trước khi dùng.
async function androidOta(env, build) {
  const base = updatesBase(env);
  const r = await fetch(base + '/educenter-android/ota/' + build + '.nlo', { cf: { cacheTtl: 3600 } }).catch(() => null);
  if (!r || !r.ok) throw new HttpError(404, 'Không có gói cập nhật cho bản này.');
  const text = await r.text();
  if (text.length > OTA_MAX_BYTES) throw new HttpError(502, 'Gói cập nhật quá lớn.');
  return new Response(text, { status: 200, headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'public, max-age=3600' } });
}

async function route(req, env, now) {
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

    // Trang xem lại phiếu xác nhận thanh toán (khách nhập mã đơn và số điện thoại).
    if (req.method === 'GET' && path === '/hoa-don') {
      return receiptPage(db, catalog, url);
    }

    if (req.method === 'POST' && path === '/api/pin-reset') {
      return json(await pinReset(db, await body(req), now));
    }

    // Cập nhật bản Android: chuyển tiếp tệp công khai trên R2 để ứng dụng không cần cấu hình CORS cho R2.
    if (req.method === 'GET' && path === '/api/app/android/latest') return await androidLatest(env);
    m = /^\/api\/app\/android\/ota\/(\d{1,9})$/.exec(path);
    if (req.method === 'GET' && m) return await androidOta(env, m[1]);

    if (req.method === 'POST' && path === '/api/claim-device') {
      return json(await claimDevice(db, env, catalog, await body(req), now));
    }

    if (req.method === 'POST' && path === '/api/register-legacy') return json(await registerLegacy(db, env, catalog, await body(req), now), 201);
    if (req.method === 'POST' && path === '/api/progress/settings') return json(await progressSettings(db, await body(req), now));
    if (req.method === 'POST' && path === '/api/progress/push') return json(await progressPush(db, await body(req), now));
    if (req.method === 'POST' && path === '/api/progress/view') return json(await progressView(db, catalog, await body(req), now));

    if (req.method === 'POST' && path === '/api/ping') {
      return json(await ping(db, await body(req), now, catalog));
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
      if (req.method === 'GET' && path === '/api/admin/orders') return json({ orders: await listOrders(db, { status: url.searchParams.get('status') || '', q: url.searchParams.get('q') || '' }, now), catalog: catalog.byId });
      if (req.method === 'POST' && path === '/api/admin/import-legacy') return json(await importLegacy(db, catalog, await body(req), now), 201);
      if (req.method === 'GET' && path === '/api/admin/transactions') return json({ transactions: await listUnmatched(db) });
      if (req.method === 'GET' && path === '/api/admin/partner-codes') return json({ partners: await listPartnerCodes(db) });
      if (req.method === 'POST' && path === '/api/admin/partner-codes') return json(await createPartnerCode(db, await body(req), now), 201);
      m = /^\/api\/admin\/partner-codes\/([A-Za-z0-9-]{3,20})\/active$/.exec(path);
      if (req.method === 'POST' && m) { const b = await body(req); await setPartnerActive(db, m[1], !!b.active); return json({ ok: true }); }
      m = /^\/api\/admin\/transactions\/(\d+)\/attach$/.exec(path);
      if (req.method === 'POST' && m) { const b = await body(req); return json(await attachTransaction(db, env, catalog, Number(m[1]), b.code, now)); }
      m = /^\/api\/admin\/orders\/([A-Za-z0-9]{6})\/(approve|cancel|reissue|revoke|restore)$/.exec(path);
      if (req.method === 'POST' && m) {
        const b = await body(req);
        if (m[2] === 'approve') return json({ key: await approveOrder(db, env, catalog, m[1], b.note, now) });
        if (m[2] === 'revoke' && b.item) { await revokeItem(db, m[1], String(b.item), b.reason, now); return json({ ok: true }); }
        if (m[2] === 'restore' && b.item) { await restoreItem(db, m[1], String(b.item), now); return json({ ok: true }); }
        if (m[2] === 'revoke') { await revokeOrder(db, m[1], b.reason, now); return json({ ok: true }); }
        if (m[2] === 'restore') { await restoreOrder(db, m[1], now); return json({ ok: true }); }
        if (m[2] === 'cancel') { await cancelOrder(db, m[1], b.note); return json({ ok: true }); }
        return json({ key: await reissueOrder(db, env, catalog, m[1], b.machine, now, b.platform) });
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

// Ứng dụng Android chạy trong WebView ở địa chỉ https://localhost nên trình duyệt đòi CORS khi gọi sang máy chủ này.
// Chỉ mở cho các địa chỉ của chính ứng dụng và chỉ cho các đường dẫn của phần mềm khách; trang quản trị và SePay không mở.
export const APP_ORIGINS = ['https://localhost', 'http://localhost', 'capacitor://localhost'];
const CLIENT_PATH = /^\/api\/(orders(\/[A-Za-z0-9]{6}\/status)?|pin-reset|claim-device|register-legacy|ping|progress\/(settings|push|view)|app\/android\/(latest|ota\/\d{1,9}))$/;

export async function handle(req, env, now = new Date()) {
  const origin = req.headers.get('origin');
  const path = new URL(req.url).pathname.replace(/\/+$/, '') || '/';
  const cors = origin && APP_ORIGINS.includes(origin) && CLIENT_PATH.test(path) ? { 'access-control-allow-origin': origin, vary: 'Origin' } : null;
  if (req.method === 'OPTIONS') {
    if (!cors) return new Response(null, { status: 403 });
    return new Response(null, { status: 204, headers: { ...cors, 'access-control-allow-methods': 'GET, POST, OPTIONS', 'access-control-allow-headers': 'content-type', 'access-control-max-age': '86400' } });
  }
  const res = await route(req, env, now);
  if (!cors) return res;
  const headers = new Headers(res.headers);
  for (const [k, v] of Object.entries(cors)) headers.set(k, v);
  return new Response(res.body, { status: res.status, headers });
}

export default { fetch: (req, env) => handle(req, env) };
