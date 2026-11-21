// Mua cho con từ app Phụ huynh. Phụ huynh có một "mã gia đình"; máy của con nhập mã này một lần,
// sau đó tự nhận khóa của mọi đơn phụ huynh mua cho gia đình mỗi lần có mạng.
import { HttpError, MACHINE_RE, PLATFORM_NAME, getOrder, getSlots, issueSlotKey } from './orders.js';

const PHONE_RE = /^(0|\+84)\d{9}$/;
const ABC = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
const nowIso = (now) => now.toISOString();
const cleanF = (v) => String(v || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
const platformOf = (v) => (String(v || '').toLowerCase() === 'android' ? 'android' : 'win');

function newFamilyCode(rand = (n) => crypto.getRandomValues(new Uint8Array(n))) {
  return Array.from(rand(8), (x) => ABC[x % ABC.length]).join('');
}

// Máy phụ huynh xin mã gia đình (mỗi máy + số điện thoại chỉ có một mã, xin lại trả về mã cũ).
export async function createFamily(db, input, now = new Date(), rand) {
  const machine = String(input.machineId || '').trim().toUpperCase();
  const phone = String(input.phone || '').replace(/[\s.\-]/g, '');
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy.');
  if (!PHONE_RE.test(phone)) throw new HttpError(400, 'Số điện thoại không hợp lệ.');
  const cur = await db.prepare('SELECT fcode FROM families WHERE parent_machine = ?1 AND phone = ?2').bind(machine, phone).first();
  if (cur) return { fcode: cur.fcode };
  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM families WHERE (parent_machine = ?1 OR phone = ?2) AND created_at > ?3').bind(machine, phone, since).first();
  if (recent.n >= 5) throw new HttpError(429, 'Tạo mã quá nhiều lần. Vui lòng thử lại sau.');
  for (let i = 0; i < 5; i++) {
    const fcode = newFamilyCode(rand);
    try {
      await db.prepare('INSERT INTO families (fcode, phone, parent_machine, created_at) VALUES (?1,?2,?3,?4)').bind(fcode, phone, machine, nowIso(now)).run();
      return { fcode };
    } catch (e) {
      if (!/UNIQUE|constraint/i.test(String(e.message))) throw e;
    }
  }
  throw new HttpError(500, 'Không tạo được mã gia đình, vui lòng thử lại.');
}

// Máy của con (win hoặc android) gọi: nhận khóa của mọi đơn gia đình còn chỗ cho loại máy này.
export async function syncFamily(db, env, catalog, input, now = new Date()) {
  const machine = String(input.machineId || '').trim().toUpperCase();
  const fcode = cleanF(input.fcode);
  const platform = platformOf(input.platform);
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy.');
  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM pin_attempts WHERE machine = ?1 AND ok = 0 AND at > ?2').bind(machine, since).first();
  if (recent.n >= 5) throw new HttpError(429, 'Thử quá nhiều lần. Vui lòng thử lại sau 1 giờ hoặc liên hệ hỗ trợ.');
  const fam = /^[A-Z0-9]{8}$/.test(fcode) ? await db.prepare('SELECT fcode FROM families WHERE fcode = ?1').bind(fcode).first() : null;
  await db.prepare('INSERT INTO pin_attempts (machine, at, ok) VALUES (?1, ?2, ?3)').bind(machine, nowIso(now), fam ? 1 : 0).run();
  if (!fam) throw new HttpError(404, 'Mã gia đình không đúng.');
  await db.prepare('INSERT INTO family_links (fcode, machine, platform, linked_at) VALUES (?1,?2,?3,?4) ON CONFLICT(fcode, machine) DO UPDATE SET platform = ?3').bind(fcode, machine, platform, nowIso(now)).run();
  const rows = (await db.prepare('SELECT code FROM family_orders WHERE fcode = ?1 ORDER BY created_at').bind(fcode).all()).results;
  const keys = []; let full = 0;
  for (const { code } of rows) {
    const o = await getOrder(db, code);
    if (!o || o.status !== 'paid') continue;
    if (await db.prepare('SELECT 1 AS x FROM revocations WHERE code = ?1 AND restored_at IS NULL').bind(code).first()) continue;
    const cur = (await getSlots(db, o))[platform];
    if (cur && cur.machine !== machine) { full++; continue; }
    const key = cur && cur.key ? cur.key : await issueSlotKey(db, env, catalog, o, platform, machine, now);
    keys.push({ code, key, items: JSON.parse(o.items) });
  }
  return { keys, full, platform: PLATFORM_NAME[platform] };
}
