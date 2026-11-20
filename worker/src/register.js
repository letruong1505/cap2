// Khách tự đăng ký khóa cũ (cấp bằng USB) từ phần mềm: máy gửi khóa NL1-... và số điện thoại phụ huynh.
// Chữ ký khóa được kiểm tra bằng khóa công khai của sản phẩm; khóa phải gắn đúng mã máy đang gửi. Đơn tạo ra là 0 đ.
import { HttpError, MACHINE_RE, getOrder } from './orders.js';
import { importLegacy } from './legacy.js';

// Khớp main/license/public-key.pem (có test kiểm tra); biến môi trường PUBLIC_KEY_PEM dùng để ghi đè khi thử.
const PUBLIC_KEY_PEM = '-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAcvUyv2YivMYNyctksF6J190DaDtQZaUcOSQDr0LnozQ=\n-----END PUBLIC KEY-----';
export const DEFAULT_PUBLIC_KEY_PEM = PUBLIC_KEY_PEM;
const unb64u = (s) => { const t = String(s).replace(/-/g, '+').replace(/_/g, '/'); return Uint8Array.from(atob(t + '='.repeat((4 - (t.length % 4)) % 4)), (c) => c.charCodeAt(0)); };
const pemToDer = (pem) => Uint8Array.from(atob(String(pem).replace(/-----[A-Z ]+-----/g, '').replace(/\s+/g, '')), (c) => c.charCodeAt(0));

async function parseKey(env, key) {
  const text = String(key || '').replace(/\s+/g, '');
  if (!text.startsWith('NL1-') || text.indexOf('.') < 0 || text.length > 2000) return null;
  try {
    const [body, sig] = text.slice(4).split('.');
    const pub = await crypto.subtle.importKey('spki', pemToDer(env.PUBLIC_KEY_PEM || PUBLIC_KEY_PEM), { name: 'Ed25519' }, false, ['verify']);
    const bytes = unb64u(body);
    if (!(await crypto.subtle.verify('Ed25519', pub, unb64u(sig), bytes))) return null;
    const p = JSON.parse(new TextDecoder().decode(bytes));
    return p && p.v === 1 ? p : null;
  } catch { return null; }
}

export async function registerLegacy(db, env, catalog, input, now = new Date()) {
  const machine = String(input.machineId || '').trim().toUpperCase();
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy.');
  const since = new Date(now.getTime() - 3600_000).toISOString();
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM pin_attempts WHERE machine = ?1 AND ok = 0 AND at > ?2').bind(machine, since).first();
  if (recent.n >= 5) throw new HttpError(429, 'Thử quá nhiều lần. Vui lòng thử lại sau 1 giờ hoặc liên hệ hỗ trợ.');
  const p = await parseKey(env, input.key);
  const code = p && /^NL-[A-Z0-9]{6}$/.test(p.id || '') ? p.id.slice(3) : '';
  const valid = !!p && !!code && p.machine === machine && (p.expires === 'never' || String(p.expires) >= now.toISOString().slice(0, 10));
  await db.prepare('INSERT INTO pin_attempts (machine, at, ok) VALUES (?1, ?2, ?3)').bind(machine, now.toISOString(), valid ? 1 : 0).run();
  if (!valid) throw new HttpError(400, 'Khóa không hợp lệ hoặc không dùng cho máy này.');
  const o = await getOrder(db, code);
  if (o) {
    if (o.machine !== machine) throw new HttpError(409, 'Mã khóa này đã đăng ký cho máy khác. Vui lòng liên hệ hỗ trợ.');
    return { ok: true, existed: true, code };
  }
  const r = await importLegacy(db, catalog, {
    code, name: String(p.owner || '').trim().length >= 2 ? p.owner : 'Khách dùng khóa USB', phone: input.phone, machine,
    grades: p.grades, courses: Array.isArray(p.courses) ? p.courses.filter((c) => typeof c === 'string') : [],
    issued: p.issued, key: String(input.key), note: 'Khóa cũ cấp bằng USB, khách tự đăng ký từ phần mềm',
  }, now);
  return { ok: true, existed: false, code, items: r.items };
}
