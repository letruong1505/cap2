// Nghiệp vụ đơn hàng: tạo đơn, tra trạng thái, nhận thanh toán, cấp key. Không phụ thuộc Cloudflare ngoài giao diện D1.
import { payloadFor, signKey } from './keys.js';

const CODE_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
export const MACHINE_RE = /^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/;
const PHONE_RE = /^(0|\+84)\d{9}$/;
export const CODE_RE = /(?:^|[^A-Z0-9])NL[\s\-]*([ABCDEFGHJKMNPQRSTUVWXYZ2-9]{6})/;

// Máy được coi là đang online nếu có tín hiệu trong 10 phút (phần mềm gửi mỗi 5 phút khi đang mở).
export const ONLINE_MS = 10 * 60 * 1000;

export const PLATFORMS = ['win', 'android'];
export const PLATFORM_NAME = { win: 'máy tính', android: 'điện thoại' };
const platformOf = (v) => (String(v || '').toLowerCase() === 'android' ? 'android' : 'win');

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

// Hoàn tiền chỉ trong 7 ngày kể từ lúc thanh toán thành công.
export const REFUND_DAYS = 7;
export function refundOpen(paidAt, now = new Date()) {
  if (!paidAt) return false;
  return now.getTime() - new Date(paidAt).getTime() <= REFUND_DAYS * 86400e3;
}
const REFUND_CLOSED = 'Đã quá 7 ngày kể từ khi thanh toán thành công, không thu hồi để hoàn tiền được nữa.';

// Mã đối tác: chữ, số và dấu gạch ngang, 3 đến 20 ký tự.
export const PARTNER_RE = /^[A-Z0-9-]{3,20}$/;

// Giá sau giảm của một khóa, làm tròn đến đồng. Dùng chung cho máy chủ và (nếu cần) giao diện.
export function discountPrice(list, percent) {
  return Math.round(list * (100 - percent) / 100);
}

// Tìm mã đối tác đang bật. Mã sai hoặc đã tắt đều báo lỗi cho khách.
export async function findPartner(db, raw) {
  const code = String(raw || '').trim().toUpperCase();
  if (!code) return null;
  if (!PARTNER_RE.test(code)) throw new HttpError(400, 'Mã đối tác không đúng định dạng.');
  const p = await db.prepare('SELECT p.code, p.partner, p.percent, l.max_machines FROM partner_codes p LEFT JOIN partner_limits l ON l.code = p.code WHERE p.code = ?1 AND p.active = 1').bind(code).first();
  if (!p) throw new HttpError(400, 'Mã đối tác không đúng hoặc đã ngừng dùng.');
  return p;
}

export async function createOrder(db, catalog, input, now = new Date(), rand) {
  const name = String(input.name || '').trim().replace(/\s+/g, ' ');
  const phone = String(input.phone || '').replace(/[\s.\-]/g, '');
  const machine = String(input.machineId || '').trim().toUpperCase();
  const platform = platformOf(input.platform);
  const ids = Array.isArray(input.ids) ? [...new Set(input.ids.map(String))] : [];
  if (name.length < 2 || name.length > 80) throw new HttpError(400, 'Họ và tên không hợp lệ.');
  if (!PHONE_RE.test(phone)) throw new HttpError(400, 'Số điện thoại không hợp lệ.');
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy. Em mở lại phần mềm rồi thử lại.');
  if (!ids.length || ids.some((id) => !catalog.byId[id])) throw new HttpError(400, 'Danh sách khóa học không hợp lệ.');
  if (!input.terms || !input.terms.version) throw new HttpError(400, 'Cần đồng ý điều khoản.');

  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM orders WHERE (machine = ?1 OR phone = ?2) AND created_at > ?3').bind(machine, phone, since).first();
  if (recent.n >= 10) throw new HttpError(429, 'Tạo quá nhiều đơn trong một giờ. Em vui lòng thử lại sau.');

  const partner = await findPartner(db, input.partnerCode);
  // Mỗi mã đối tác chỉ dùng được trên một số máy nhất định (đếm máy khác nhau trong các đơn chưa hủy), tránh lạm dụng mã.
  if (partner && partner.max_machines) {
    const used = (await db.prepare('SELECT o.machine AS machine FROM orders o WHERE o.status != \'cancelled\' AND o.code IN (SELECT code FROM order_prices WHERE partner_code = ?1) UNION SELECT d.machine FROM order_devices d JOIN orders o ON o.code = d.code WHERE o.status != \'cancelled\' AND d.code IN (SELECT code FROM order_prices WHERE partner_code = ?1)').bind(partner.code).all()).results.map((r) => r.machine);
    if (!used.includes(machine) && used.length >= partner.max_machines) throw new HttpError(403, 'Mã đối tác đã dùng hết số máy được phép. Em liên hệ đối tác hoặc Nam Linh Educenter để được hỗ trợ.');
  }
  const lines = ids.map((id) => {
    const list = catalog.byId[id].price;
    return { id, list, paid: partner ? discountPrice(list, partner.percent) : list };
  });
  const amount = lines.reduce((s, l) => s + l.paid, 0);

  for (let i = 0; i < 5; i++) {
    const code = newCode(rand);
    try {
      // Đơn và giá từng khóa ghi cùng lúc, để hoàn tiền và phiếu xác nhận luôn đúng số đã thu.
      await db.batch([
        db.prepare('INSERT INTO orders (code, name, phone, machine, items, amount, status, terms_version, terms_at, created_at) VALUES (?1,?2,?3,?4,?5,?6,\'pending\',?7,?8,?9)')
          .bind(code, name, phone, machine, JSON.stringify(ids), amount, String(input.terms.version).slice(0, 40), String(input.terms.at || '').slice(0, 40), nowIso(now)),
        db.prepare('INSERT INTO order_devices (code, platform, machine, key, issued_at) VALUES (?1,?2,?3,NULL,NULL)').bind(code, platform, machine),
        ...lines.map((l) => db.prepare('INSERT INTO order_prices (code, item, list_price, paid_price, partner_code, percent) VALUES (?1,?2,?3,?4,?5,?6)')
          .bind(code, l.id, l.list, l.paid, partner ? partner.code : null, partner ? partner.percent : null)),
      ]);
      return {
        code, amount, content: 'NL ' + code, status: 'pending',
        partner: partner ? { code: partner.code, percent: partner.percent } : null,
        items: lines,
      };
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
  // Chỗ thiết bị của máy đặt đơn dùng chung khóa này (máy cũ trước khi đổi là order.machine).
  await db.prepare('UPDATE order_devices SET key = ?1, machine = ?2, issued_at = ?3 WHERE code = ?4 AND machine = ?5').bind(key, o.machine, nowIso(now), order.code, order.machine).run();
  return key;
}

// Các chỗ thiết bị của đơn. Đơn cũ chưa có dòng nào thì chỗ máy tính là máy đặt đơn.
export async function getSlots(db, o) {
  const rows = (await db.prepare('SELECT platform, machine, key, issued_at FROM order_devices WHERE code = ?1').bind(o.code).all()).results;
  const slots = { win: null, android: null };
  for (const r of rows) slots[r.platform] = { machine: r.machine, key: r.key, issued_at: r.issued_at };
  if (!rows.length) slots.win = { machine: o.machine, key: o.key || null, issued_at: null };
  return slots;
}

// Khóa cho một chỗ thiết bị của đơn đã thanh toán; chỗ của máy đặt đơn dùng đường issueKey có sẵn.
async function issueSlotKey(db, env, catalog, o, platform, machine, now) {
  const slots = await getSlots(db, o);
  const cur = slots[platform];
  if (cur && cur.machine === o.machine) return issueKey(db, env, catalog, o, now, machine);
  const key = await signKey(env.SIGNING_KEY_PEM, payloadFor({ ...o, machine }, catalog, now));
  await db.prepare('INSERT INTO order_devices (code, platform, machine, key, issued_at) VALUES (?1,?2,?3,?4,?5) ON CONFLICT(code, platform) DO UPDATE SET machine = ?3, key = ?4, issued_at = ?5').bind(o.code, platform, machine, key, nowIso(now)).run();
  return key;
}

// Khách nhập mã đơn + số điện thoại trên thiết bị còn lại để nhận khóa cho chỗ máy tính hoặc điện thoại của đơn.
export async function claimDevice(db, env, catalog, input, now = new Date()) {
  const machine = String(input.machineId || '').trim().toUpperCase();
  const phone = String(input.phone || '').replace(/[\s.\-]/g, '');
  const code = String(input.code || '').toUpperCase().replace(/[^A-Z0-9]/g, '').replace(/^NL(?=[A-Z0-9]{6}$)/, '');
  const platform = platformOf(input.platform);
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy.');
  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM pin_attempts WHERE machine = ?1 AND ok = 0 AND at > ?2').bind(machine, since).first();
  if (recent.n >= 5) throw new HttpError(429, 'Thử quá nhiều lần. Vui lòng thử lại sau 1 giờ hoặc liên hệ hỗ trợ.');
  const o = /^[A-Z0-9]{6}$/.test(code) && PHONE_RE.test(phone) ? await getOrder(db, code) : null;
  const ok = !!o && o.status === 'paid' && o.phone === phone;
  await db.prepare('INSERT INTO pin_attempts (machine, at, ok) VALUES (?1, ?2, ?3)').bind(machine, nowIso(now), ok ? 1 : 0).run();
  if (!ok) throw new HttpError(404, 'Thông tin không khớp với đơn đã mua.');
  if (await db.prepare('SELECT 1 AS x FROM revocations WHERE code = ?1 AND restored_at IS NULL').bind(o.code).first()) throw new HttpError(403, 'Đơn này đã bị thu hồi bản quyền.');
  const slots = await getSlots(db, o);
  const cur = slots[platform];
  if (cur && cur.machine !== machine) throw new HttpError(409, 'Đơn này đã dùng chỗ ' + PLATFORM_NAME[platform] + ' cho thiết bị khác. Liên hệ Nam Linh Educenter để đổi thiết bị.');
  if (!cur && slots.win && slots.win.machine === machine) throw new HttpError(409, 'Mã máy này đã thuộc chỗ khác của đơn.');
  // Đơn cũ chưa có dòng nào: ghi lại chỗ máy tính hiện có trước khi thêm chỗ mới.
  if (!(await db.prepare('SELECT 1 AS x FROM order_devices WHERE code = ?1').bind(o.code).first())) {
    await db.prepare('INSERT INTO order_devices (code, platform, machine, key, issued_at) VALUES (?1,\'win\',?2,?3,NULL)').bind(o.code, o.machine, o.key || null).run();
  }
  const key = cur && cur.key ? cur.key : await issueSlotKey(db, env, catalog, o, platform, machine, now);
  return { key, platform, code: o.code, items: JSON.parse(o.items) };
}

export async function getOrder(db, code) {
  return db.prepare('SELECT * FROM orders WHERE code = ?1').bind(String(code || '').toUpperCase()).first();
}

// Phần mềm hỏi trạng thái đơn. Chỉ trả key khi đúng mã đơn VÀ đúng mã máy đã đăng ký trong đơn.
export async function orderStatus(db, env, catalog, code, machine, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o || o.machine !== String(machine || '').toUpperCase()) throw new HttpError(404, 'Không tìm thấy đơn.');
  const out = { code: o.code, status: o.status, amount: o.amount, paidAmount: o.paid_amount || 0, items: JSON.parse(o.items) };
  // Thông tin dùng cho phiếu xác nhận thanh toán (chính khách hàng, trên đúng máy đã đặt đơn).
  out.name = o.name;
  out.phone = o.phone;
  out.paidAt = o.paid_at || null;
  out.lines = await linePrices(db, o.code, catalog, out.items);
  const withPartner = out.lines.find((l) => l.partner);
  out.partner = withPartner ? withPartner.partner : null;
  if (o.status === 'paid') {
    out.key = o.key || await issueKey(db, env, catalog, o, now).catch(() => null);
  }
  return out;
}

// Giá từng khóa của đơn. Đơn cũ (trước khi có bảng giá) dùng giá niêm yết, không giảm.
export async function linePrices(db, code, catalog, items) {
  const rows = (await db.prepare('SELECT item, list_price, paid_price, partner_code, percent FROM order_prices WHERE code = ?1').bind(code).all()).results;
  const byItem = new Map(rows.map((r) => [r.item, r]));
  return items.map((id) => {
    const r = byItem.get(id);
    const list = r ? r.list_price : (catalog.byId[id] ? catalog.byId[id].price : 0);
    const paid = r ? r.paid_price : list;
    const partner = r && r.partner_code ? { code: r.partner_code, percent: r.percent } : null;
    return { id, name: catalog.byId[id] ? catalog.byId[id].name : id, list, paid, partner };
  });
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

export async function listOrders(db, { status, q } = {}, now = new Date()) {
  let sql = 'SELECT code, name, phone, machine, items, amount, status, paid_amount, paid_at, created_at, reissues, note, CASE WHEN key IS NULL THEN 0 ELSE 1 END AS has_key FROM orders';
  const where = []; const args = [];
  if (status) { args.push(status); where.push('status = ?' + args.length); }
  if (q) { args.push('%' + String(q).slice(0, 40) + '%'); where.push(`(name LIKE ?${args.length} OR phone LIKE ?${args.length} OR code LIKE ?${args.length} OR machine LIKE ?${args.length})`); }
  if (where.length) sql += ' WHERE ' + where.join(' AND ');
  sql += ' ORDER BY created_at DESC LIMIT 200';
  const orders = (await db.prepare(sql).bind(...args).all()).results;
  // Gắn máy đã mở phần mềm và trạng thái thu hồi (hai truy vấn riêng, tránh giới hạn số tham số của D1).
  const devs = (await db.prepare('SELECT code, machine, version, first_seen, last_seen FROM devices ORDER BY last_seen DESC LIMIT 3000').all()).results;
  const revs = (await db.prepare('SELECT code, reason, revoked_at FROM revocations WHERE restored_at IS NULL').all()).results;
  const byDev = new Map(); for (const d of devs) { if (!byDev.has(d.code)) byDev.set(d.code, []); byDev.get(d.code).push({ machine: d.machine, version: d.version, first_seen: d.first_seen, last_seen: d.last_seen, online: now - new Date(d.last_seen) < ONLINE_MS }); }
  const byRev = new Map(revs.map((r) => [r.code, { reason: r.reason, at: r.revoked_at }]));
  const slotRows = (await db.prepare('SELECT code, platform, machine, issued_at FROM order_devices').all()).results;
  const bySlot = new Map(); for (const r of slotRows) { if (!bySlot.has(r.code)) bySlot.set(r.code, {}); bySlot.get(r.code)[r.platform] = { machine: r.machine, issued_at: r.issued_at }; }
  const itemRevs = (await db.prepare('SELECT code, item, reason, revoked_at FROM item_revocations WHERE restored_at IS NULL').all()).results;
  const byItem = new Map(); for (const r of itemRevs) { if (!byItem.has(r.code)) byItem.set(r.code, []); byItem.get(r.code).push({ item: r.item, reason: r.reason, at: r.revoked_at }); }
  // Giá từng khóa và mã đối tác của các đơn đang hiển thị (để biết số tiền hoàn cho từng khóa).
  const priceRows = (await db.prepare('SELECT code, item, list_price, paid_price, partner_code, percent FROM order_prices WHERE code IN (SELECT code FROM orders ORDER BY created_at DESC LIMIT 200)').all()).results;
  const byPrice = new Map();
  for (const r of priceRows) {
    if (!byPrice.has(r.code)) byPrice.set(r.code, { prices: {}, partner: null });
    const e = byPrice.get(r.code);
    e.prices[r.item] = { list: r.list_price, paid: r.paid_price };
    if (r.partner_code) e.partner = { code: r.partner_code, percent: r.percent };
  }
  return orders.map((o) => {
    const pr = byPrice.get(o.code) || { prices: {}, partner: null };
    // Đơn cũ chưa có dòng chỗ thiết bị: chỗ máy tính là máy đặt đơn.
    const slots = bySlot.get(o.code) || { win: { machine: o.machine, issued_at: null } };
    const known = new Set(Object.values(slots).map((x) => x.machine));
    const devices = (byDev.get(o.code) || []).map((d) => ({ ...d, platform: Object.keys(slots).find((k) => slots[k].machine === d.machine) || null, stranger: !known.has(d.machine) }));
    return { ...o, slots, devices, revoked: byRev.get(o.code) || null, item_revoked: byItem.get(o.code) || [], prices: pr.prices, partner: pr.partner };
  });
}

// Mã đối tác: danh sách (kèm số đơn đã dùng), tạo mới, bật/tắt.
export async function listPartnerCodes(db) {
  return (await db.prepare('SELECT p.code, p.partner, p.percent, p.active, p.created_at, (SELECT COUNT(DISTINCT op.code) FROM order_prices op WHERE op.partner_code = p.code) AS used, l.max_machines, (SELECT COUNT(*) FROM (SELECT o.machine AS m FROM orders o WHERE o.status != \'cancelled\' AND o.code IN (SELECT code FROM order_prices WHERE partner_code = p.code) UNION SELECT d.machine FROM order_devices d JOIN orders o ON o.code = d.code WHERE o.status != \'cancelled\' AND d.code IN (SELECT code FROM order_prices WHERE partner_code = p.code))) AS machines FROM partner_codes p LEFT JOIN partner_limits l ON l.code = p.code ORDER BY p.created_at DESC').all()).results;
}

export async function createPartnerCode(db, input, now = new Date()) {
  const code = String(input.code || '').trim().toUpperCase();
  const partner = String(input.partner || '').trim().replace(/\s+/g, ' ');
  const percent = Number(input.percent === undefined || input.percent === '' ? 20 : input.percent);
  if (!PARTNER_RE.test(code)) throw new HttpError(400, 'Mã phải gồm chữ, số hoặc dấu gạch ngang, dài 3 đến 20 ký tự.');
  if (partner.length < 2 || partner.length > 60) throw new HttpError(400, 'Tên đối tác phải từ 2 đến 60 ký tự.');
  if (!Number.isInteger(percent) || percent < 1 || percent > 99) throw new HttpError(400, 'Tỉ lệ giảm phải là số nguyên từ 1 đến 99.');
  const maxMachines = Number(input.maxMachines === undefined || input.maxMachines === '' ? 10 : input.maxMachines);
  if (!Number.isInteger(maxMachines) || maxMachines < 1 || maxMachines > 1000) throw new HttpError(400, 'Số máy tối đa phải là số nguyên từ 1 đến 1000.');
  try {
    await db.batch([
      db.prepare('INSERT INTO partner_codes (code, partner, percent, active, created_at) VALUES (?1, ?2, ?3, 1, ?4)').bind(code, partner, percent, nowIso(now)),
      db.prepare('INSERT INTO partner_limits (code, max_machines) VALUES (?1, ?2)').bind(code, maxMachines),
    ]);
  } catch (e) {
    if (/UNIQUE|constraint/i.test(String(e.message))) throw new HttpError(409, 'Mã này đã tồn tại.');
    throw e;
  }
  return { code, partner, percent, maxMachines };
}

export async function setPartnerActive(db, code, active) {
  const r = await db.prepare('UPDATE partner_codes SET active = ?1 WHERE code = ?2').bind(active ? 1 : 0, String(code || '').toUpperCase()).run();
  if (!r.meta.changes) throw new HttpError(404, 'Không tìm thấy mã đối tác.');
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
export async function reissueOrder(db, env, catalog, code, machine, now = new Date(), platform) {
  const o = await getOrder(db, code);
  const m = String(machine || '').trim().toUpperCase();
  if (!o || o.status !== 'paid') throw new HttpError(404, 'Chỉ cấp lại cho đơn đã thanh toán.');
  if (!MACHINE_RE.test(m)) throw new HttpError(400, 'Mã máy phải có dạng XXXX-XXXX-XXXX.');
  const slots = await getSlots(db, o);
  // Không nói rõ chỗ nào: giữ cách cũ, cấp lại cho chỗ của máy đặt đơn.
  const want = platform ? platformOf(platform) : (Object.keys(slots).find((k) => slots[k] && slots[k].machine === o.machine) || 'win');
  if (!(await db.prepare('SELECT 1 AS x FROM order_devices WHERE code = ?1').bind(o.code).first())) {
    await db.prepare('INSERT INTO order_devices (code, platform, machine, key, issued_at) VALUES (?1,\'win\',?2,?3,NULL)').bind(o.code, o.machine, o.key || null).run();
  }
  const key = await issueSlotKey(db, env, catalog, o, want, m, now);
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
  const onSlot = !!o && (o.machine === machine || !!(await db.prepare('SELECT 1 AS x FROM order_devices WHERE code = ?1 AND machine = ?2').bind(o.code, machine).first()));
  const ok = !!o && o.status === 'paid' && onSlot && o.phone === phone;
  await db.prepare('INSERT INTO pin_attempts (machine, at, ok) VALUES (?1, ?2, ?3)').bind(machine, nowIso(now), ok ? 1 : 0).run();
  if (!ok) throw new HttpError(404, 'Thông tin không khớp với đơn đã mua trên máy này.');
  return { ok: true };
}

// Thu hồi khóa theo mã đơn. Chỉ đánh dấu; khóa trên máy khách bị vô hiệu ở lần phần mềm gửi tín hiệu kế tiếp. Khôi phục bằng restoreOrder.
export async function revokeOrder(db, code, reason, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o || o.status !== 'paid') throw new HttpError(404, 'Chỉ thu hồi được đơn đã thanh toán.');
  if (!refundOpen(o.paid_at, now)) throw new HttpError(409, REFUND_CLOSED);
  await db.prepare('INSERT INTO revocations (code, reason, revoked_at, restored_at) VALUES (?1, ?2, ?3, NULL) ON CONFLICT(code) DO UPDATE SET reason = ?2, revoked_at = ?3, restored_at = NULL')
    .bind(o.code, String(reason || 'Thu hồi').slice(0, 200), nowIso(now)).run();
}

export async function restoreOrder(db, code, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o) throw new HttpError(404, 'Không tìm thấy đơn.');
  const r = await db.prepare('UPDATE revocations SET restored_at = ?1 WHERE code = ?2 AND restored_at IS NULL').bind(nowIso(now), o.code).run();
  if (!r.meta.changes) throw new HttpError(409, 'Đơn này không đang bị thu hồi.');
}

// Phần mềm gửi tín hiệu: ghi nhận máy đang mở phần mềm với các khóa của đơn, trả về những mã đơn đang bị thu hồi.
// Thu hồi / khôi phục riêng một khóa học trong đơn (hoàn tiền một phần). Các khóa còn lại của đơn vẫn dùng bình thường.
export async function revokeItem(db, code, item, reason, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o || o.status !== 'paid') throw new HttpError(404, 'Chỉ thu hồi được đơn đã thanh toán.');
  if (!JSON.parse(o.items).includes(item)) throw new HttpError(400, 'Khóa học này không thuộc đơn.');
  if (!refundOpen(o.paid_at, now)) throw new HttpError(409, REFUND_CLOSED);
  await db.prepare('INSERT INTO item_revocations (code, item, reason, revoked_at, restored_at) VALUES (?1, ?2, ?3, ?4, NULL) ON CONFLICT(code, item) DO UPDATE SET reason = ?3, revoked_at = ?4, restored_at = NULL')
    .bind(o.code, item, String(reason || 'Hoàn tiền một phần').slice(0, 200), nowIso(now)).run();
}

export async function restoreItem(db, code, item, now = new Date()) {
  const o = await getOrder(db, code);
  if (!o) throw new HttpError(404, 'Không tìm thấy đơn.');
  const r = await db.prepare('UPDATE item_revocations SET restored_at = ?1 WHERE code = ?2 AND item = ?3 AND restored_at IS NULL').bind(nowIso(now), o.code, String(item)).run();
  if (!r.meta.changes) throw new HttpError(409, 'Khóa học này không đang bị thu hồi.');
}

export async function ping(db, input, now = new Date(), catalog) {
  const machine = String(input && input.machineId || '').trim().toUpperCase();
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Mã máy không hợp lệ.');
  const ids = [...new Set((Array.isArray(input.ids) ? input.ids : []).slice(0, 20).map((x) => String(x).toUpperCase().replace(/^NL-/, '')).filter((x) => /^[A-Z0-9]{6}$/.test(x)))];
  const version = String(input.version || '').slice(0, 20);
  const revoked = []; const revokedItems = {};
  for (const code of ids) {
    const o = await getOrder(db, code);
    if (!o || o.status !== 'paid') continue;
    await db.prepare('INSERT INTO devices (code, machine, version, first_seen, last_seen) VALUES (?1, ?2, ?3, ?4, ?4) ON CONFLICT(code, machine) DO UPDATE SET version = ?3, last_seen = ?4')
      .bind(o.code, machine, version, nowIso(now)).run();
    if (await db.prepare('SELECT 1 AS x FROM revocations WHERE code = ?1 AND restored_at IS NULL').bind(o.code).first()) revoked.push(o.code);
    // Khóa học bị thu hồi riêng, đổi sang cách ghi trong khóa: lớp Văn hóa (grades) và khóa Kỹ năng (courses).
    const gone = (await db.prepare('SELECT item FROM item_revocations WHERE code = ?1 AND restored_at IS NULL').bind(o.code).all()).results.map((r) => r.item);
    if (gone.length && catalog) {
      const grades = gone.map((id) => catalog.byId[id]?.grade).filter((g) => Number.isInteger(g)).sort((a, b) => a - b);
      const courses = gone.filter((id) => catalog.byId[id] && !catalog.byId[id].grade);
      revokedItems[o.code] = { grades, courses };
    }
  }
  return { revoked, revokedItems };
}
