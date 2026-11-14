// Nghiệp vụ đơn hàng: tạo đơn, tra trạng thái, nhận thanh toán, cấp key. Không phụ thuộc Cloudflare ngoài giao diện D1.
import { payloadFor, signKey } from './keys.js';

const CODE_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
export const MACHINE_RE = /^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/;
const PHONE_RE = /^(0|\+84)\d{9}$/;
export const CODE_RE = /(?:^|[^A-Z0-9])NL[\s\-]*([ABCDEFGHJKMNPQRSTUVWXYZ2-9]{6})/;

export class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

export function newCode(rand = (n) => crypto.getRandomValues(new Uint8Array(n))) {
  return Array.from(rand(6), (x) => CODE_ALPHABET[x % CODE_ALPHABET.length]).join('');
}

// Tìm mã đơn trong nội dung chuyển khoản (ngân hàng có thể bỏ khoảng trắng hoặc đổi chữ hoa/thường).
export function findCode(...texts) {
  for (const t of texts) {
    const m = CODE_RE.exec(String(t || '').toUpperCase());
    if (m) return m[1];
  }
  return null;
}

const nowIso = (now) => now.toISOString();

export async function createOrder(db, catalog, input, now = new Date(), rand) {
  const name = String(input.name || '').trim().replace(/\s+/g, ' ');
  const phone = String(input.phone || '').replace(/[\s.\-]/g, '');
  const machine = String(input.machineId || '').trim().toUpperCase();
  const ids = Array.isArray(input.ids) ? [...new Set(input.ids.map(String))] : [];
  if (name.length < 2 || name.length > 80) throw new HttpError(400, 'Họ và tên không hợp lệ.');
  if (!PHONE_RE.test(phone)) throw new HttpError(400, 'Số điện thoại không hợp lệ.');
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy. Em mở lại phần mềm rồi thử lại.');
  if (!ids.length || ids.some((id) => !catalog.byId[id])) throw new HttpError(400, 'Danh sách khóa học không hợp lệ.');
  if (!input.terms || !input.terms.version) throw new HttpError(400, 'Cần đồng ý điều khoản.');
  const amount = ids.reduce((s, id) => s + catalog.byId[id].price, 0);

  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM orders WHERE (machine = ?1 OR phone = ?2) AND created_at > ?3').bind(machine, phone, since).first();
  if (recent.n >= 10) throw new HttpError(429, 'Tạo quá nhiều đơn trong một giờ. Em vui lòng thử lại sau.');

  for (let i = 0; i < 5; i++) {
    const code = newCode(rand);
    try {
      await db.prepare('INSERT INTO orders (code, name, phone, machine, items, amount, status, terms_version, terms_at, created_at) VALUES (?1,?2,?3,?4,?5,?6,\'pending\',?7,?8,?9)')
        .bind(code, name, phone, machine, JSON.stringify(ids), amount, String(input.terms.version).slice(0, 40), String(input.terms.at || '').slice(0, 40), nowIso(now)).run();
      return { code, amount, content: 'NL ' + code, status: 'pending' };
    } catch (e) {
      if (!/UNIQUE|constraint/i.test(String(e.message))) throw e;
    }
  }
  throw new HttpError(500, 'Không tạo được mã đơn, vui lòng thử lại.');
}

// Cấp key cho đơn đã thanh toán (hoặc đổi sang máy khác nếu truyền machine).
export async function issueKey(db, env, catalog, order, now = new Date(), machine) {
  const o = machine ? { ...order, machine } : order;
  const key = await signKey(env.SIGNING_KEY_PEM, payloadFor(o, catalog, now));
  await db.prepare('UPDATE orders SET key = ?1, machine = ?2 WHERE code = ?3').bind(key, o.machine, order.code).run();
  return key;
}

export async function getOrder(db, code) {
  return db.prepare('SELECT * FROM orders WHERE code = ?1').bind(String(code || '').toUpperCase()).first();
}

// Phần mềm hỏi trạng thái đơn. Chỉ trả key khi đúng mã đơn VÀ đúng mã máy đã đăng ký trong đơn.
export async function orderStatus(db, env, catalog, code, machine, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o || o.machine !== String(machine || '').toUpperCase()) throw new HttpError(404, 'Không tìm thấy đơn.');
  const out = { code: o.code, status: o.status, amount: o.amount, paidAmount: o.paid_amount || 0, items: JSON.parse(o.items) };
  if (o.status === 'paid') {
    out.key = o.key || await issueKey(db, env, catalog, o, now).catch(() => null);
  }
  return out;
}

// Xử lý một giao dịch tiền vào từ SePay. Trả về chuỗi kết quả để lưu log.
export async function applyPayment(db, env, catalog, tx, now = new Date()) {
  const ins = await db.prepare('INSERT OR IGNORE INTO transactions (id, reference, amount, content, raw, created_at) VALUES (?1,?2,?3,?4,?5,?6)')
    .bind(tx.id, tx.reference || '', tx.amount, tx.content || '', tx.raw || '', nowIso(now)).run();
  if (!ins.meta.changes) return 'duplicate';

  const finish = async (result, orderCode) => {
    await db.prepare('UPDATE transactions SET result = ?1, order_code = ?2 WHERE id = ?3').bind(result, orderCode || null, tx.id).run();
    return result;
  };
  const code = findCode(tx.code, tx.content);
  const order = code ? await getOrder(db, code) : null;
  if (!order) return finish('unmatched', null);
  if (order.status === 'cancelled') return finish('order-cancelled', order.code);
  if (order.status === 'paid') return finish('extra-payment', order.code);

  const paid = (order.paid_amount || 0) + tx.amount;
  if (paid < order.amount) {
    await db.prepare('UPDATE orders SET status = \'underpaid\', paid_amount = ?1 WHERE code = ?2').bind(paid, order.code).run();
    return finish('underpaid', order.code);
  }
  await db.prepare('UPDATE orders SET status = \'paid\', paid_amount = ?1, paid_at = ?2, tx_id = ?3 WHERE code = ?4').bind(paid, nowIso(now), tx.id, order.code).run();
  try {
    await issueKey(db, env, catalog, { ...order }, now);
  } catch (e) {
    return finish('paid-nokey', order.code); // đã thu tiền; key sẽ được cấp khi phần mềm hỏi hoặc khi admin cấp lại
  }
  return finish(paid > order.amount ? 'paid-overpaid' : 'paid', order.code);
}

export async function listOrders(db, { status, q } = {}) {
  let sql = 'SELECT code, name, phone, machine, items, amount, status, paid_amount, paid_at, created_at, reissues, note, CASE WHEN key IS NULL THEN 0 ELSE 1 END AS has_key FROM orders';
  const where = []; const args = [];
  if (status) { args.push(status); where.push('status = ?' + args.length); }
  if (q) { args.push('%' + String(q).slice(0, 40) + '%'); where.push(`(name LIKE ?${args.length} OR phone LIKE ?${args.length} OR code LIKE ?${args.length} OR machine LIKE ?${args.length})`); }
  if (where.length) sql += ' WHERE ' + where.join(' AND ');
  sql += ' ORDER BY created_at DESC LIMIT 200';
  return (await db.prepare(sql).bind(...args).all()).results;
}

export async function listUnmatched(db) {
  return (await db.prepare('SELECT id, reference, amount, content, result, order_code, created_at FROM transactions WHERE result != \'paid\' ORDER BY created_at DESC LIMIT 100').all()).results;
}

// Duyệt tay: dùng khi chuyển thiếu/thừa, SePay chậm, hoặc nhận tiền ngoài hệ thống.
export async function approveOrder(db, env, catalog, code, note, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o) throw new HttpError(404, 'Không tìm thấy đơn.');
  if (o.status === 'cancelled') throw new HttpError(409, 'Đơn đã hủy.');
  await db.prepare('UPDATE orders SET status = \'paid\', paid_at = COALESCE(paid_at, ?1), note = ?2 WHERE code = ?3').bind(nowIso(now), String(note || 'Duyệt tay').slice(0, 200), o.code).run();
  return issueKey(db, env, catalog, o, now);
}

export async function cancelOrder(db, code, note) {
  const o = await getOrder(db, code);
  if (!o) throw new HttpError(404, 'Không tìm thấy đơn.');
  if (o.status === 'paid') throw new HttpError(409, 'Đơn đã thanh toán, không hủy được. Cần hoàn tiền thì xử lý ngoài hệ thống rồi ghi chú.');
  await db.prepare('UPDATE orders SET status = \'cancelled\', note = ?1 WHERE code = ?2').bind(String(note || 'Hủy').slice(0, 200), o.code).run();
}

// Đổi máy: cấp lại key cho mã máy mới.
export async function reissueOrder(db, env, catalog, code, machine, now = new Date()) {
  const o = await getOrder(db, code);
  const m = String(machine || '').trim().toUpperCase();
  if (!o || o.status !== 'paid') throw new HttpError(404, 'Chỉ cấp lại cho đơn đã thanh toán.');
  if (!MACHINE_RE.test(m)) throw new HttpError(400, 'Mã máy phải có dạng XXXX-XXXX-XXXX.');
  const key = await issueKey(db, env, catalog, o, now, m);
  await db.prepare('UPDATE orders SET reissues = reissues + 1 WHERE code = ?1').bind(o.code).run();
  return key;
}

// Gắn giao dịch tiền vào (đã lưu nhưng chưa khớp đơn) vào một đơn có thật, rồi cấp key nếu đủ tiền.
export async function attachTransaction(db, env, catalog, txId, code, now = new Date()) {
  const tx = await db.prepare('SELECT id, amount, result, order_code FROM transactions WHERE id = ?1').bind(txId).first();
  if (!tx) throw new HttpError(404, 'Không tìm thấy giao dịch.');
  if (tx.order_code) throw new HttpError(409, 'Giao dịch này đã gắn vào đơn ' + tx.order_code + '.');
  const order = await getOrder(db, String(code || '').toUpperCase());
  if (!order) throw new HttpError(404, 'Không tìm thấy đơn.');
  if (order.status === 'cancelled') throw new HttpError(409, 'Đơn đã hủy.');
  const paid = (order.paid_amount || 0) + tx.amount;
  const full = paid >= order.amount;
  await db.prepare('UPDATE orders SET status = ?1, paid_amount = ?2, paid_at = CASE WHEN ?1 = \'paid\' THEN COALESCE(paid_at, ?3) ELSE paid_at END, tx_id = ?4, note = ?5 WHERE code = ?6')
    .bind(full ? 'paid' : 'underpaid', paid, nowIso(now), tx.id, 'Gắn giao dịch ' + tx.id, order.code).run();
  let key = null;
  if (full) key = await issueKey(db, env, catalog, { ...order }, now).catch(() => null);
  await db.prepare('UPDATE transactions SET result = ?1, order_code = ?2 WHERE id = ?3').bind(full ? 'paid-manual' : 'underpaid', order.code, tx.id).run();
  return { key, status: full ? 'paid' : 'underpaid' };
}

// Khôi phục mã PIN phụ huynh: đúng khi số điện thoại, mã đơn và mã máy cùng khớp một đơn đã thanh toán.
// Giới hạn 5 lần thử mỗi giờ cho mỗi mã máy. Máy chủ không biết mã PIN, chỉ xác nhận quyền đặt lại.
export async function pinReset(db, input, now = new Date()) {
  const machine = String(input.machineId || '').trim().toUpperCase();
  const phone = String(input.phone || '').replace(/[\s.\-]/g, '');
  const code = String(input.code || '').toUpperCase().replace(/[^A-Z0-9]/g, '').replace(/^NL(?=[A-Z0-9]{6}$)/, '');
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy.');
  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM pin_attempts WHERE machine = ?1 AND at > ?2').bind(machine, since).first();
  if (recent.n >= 5) throw new HttpError(429, 'Thử quá nhiều lần. Vui lòng thử lại sau 1 giờ hoặc liên hệ hỗ trợ.');
  const o = /^[A-Z0-9]{6}$/.test(code) && PHONE_RE.test(phone) ? await getOrder(db, code) : null;
  const ok = !!o && o.status === 'paid' && o.machine === machine && o.phone === phone;
  await db.prepare('INSERT INTO pin_attempts (machine, at, ok) VALUES (?1, ?2, ?3)').bind(machine, nowIso(now), ok ? 1 : 0).run();
  if (!ok) throw new HttpError(404, 'Thông tin không khớp với đơn đã mua trên máy này.');
  return { ok: true };
}
