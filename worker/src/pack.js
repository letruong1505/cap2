// Cấp khoá giải mã gói nội dung khóa học theo lớp cho máy có bản quyền hợp lệ.
// Khoá lớp = HMAC-SHA256(PACK_MASTER, "nl-pack-v1:lop<N>") (khớp core/pack-format.js). Gói mã hóa nằm công khai trên R2;
// không có khoá lớp thì không đọc được. Máy gửi các khoá NL1-... đang dùng; máy chủ kiểm tra chữ ký, mã máy, hạn, thu hồi.
import { HttpError, MACHINE_RE } from './orders.js';

const enc = new TextEncoder();
const GRADES = [6, 7, 8, 9, 10, 11, 12];

function b64uToBytes(s) {
  const b = atob(String(s).replace(/-/g, '+').replace(/_/g, '/'));
  return Uint8Array.from(b, (c) => c.charCodeAt(0));
}
const b64 = (bytes) => { let s = ''; for (const x of bytes) s += String.fromCharCode(x); return btoa(s); };

function pemToDer(pem) {
  return Uint8Array.from(atob(String(pem).replace(/-----[A-Z ]+-----/g, '').replace(/\s+/g, '')), (c) => c.charCodeAt(0));
}

// Khoá công khai Ed25519 lấy từ khoá ký (JWK của khoá riêng có trường x là khoá công khai).
let pubCache = { pem: null, key: null };
async function publicKey(pem) {
  if (pubCache.pem === pem && pubCache.key) return pubCache.key;
  const priv = await crypto.subtle.importKey('pkcs8', pemToDer(pem), { name: 'Ed25519' }, true, ['sign']);
  const jwk = await crypto.subtle.exportKey('jwk', priv);
  const key = await crypto.subtle.importKey('jwk', { kty: jwk.kty, crv: jwk.crv, x: jwk.x }, { name: 'Ed25519' }, false, ['verify']);
  pubCache = { pem, key };
  return key;
}

async function derive(master, label) {
  const k = await crypto.subtle.importKey('raw', enc.encode(String(master)), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64(new Uint8Array(await crypto.subtle.sign('HMAC', k, enc.encode(label))));
}
export const gradeKey = (master, grade) => derive(master, `nl-pack-v1:lop${grade}`);
export const courseKey = (master, id) => derive(master, `nl-pack-v1:course:${id}`);

// Các khóa Kỹ năng có gói nội dung. Khóa bản cũ 'tu-duy-lap-trinh' (đã bán chung) mở cả hai lộ trình.
export const PACKED_COURSES = ['tu-duy-lap-trinh-scratch', 'tu-duy-lap-trinh-python', 'gia-su-ai', 'ai-nguoi-di-lam-claude', 'ai-nguoi-di-lam-chatgpt', 'ai-nguoi-di-lam-gemini'];
const LEGACY_COURSE = { 'tu-duy-lap-trinh': ['tu-duy-lap-trinh-scratch', 'tu-duy-lap-trinh-python'] };

async function parseKey(pem, text) {
  const t = String(text || '').replace(/\s+/g, '');
  if (!t.startsWith('NL1-') || t.indexOf('.') < 0) return null;
  const [body, sig] = t.slice(4).split('.');
  try {
    const bodyBytes = b64uToBytes(body);
    if (!(await crypto.subtle.verify('Ed25519', await publicKey(pem), b64uToBytes(sig), bodyBytes))) return null;
    const p = JSON.parse(new TextDecoder().decode(bodyBytes));
    return p && p.v === 1 ? p : null;
  } catch { return null; }
}

export async function packKeys(db, env, catalog, input, now = new Date()) {
  if (!env.PACK_MASTER || !env.SIGNING_KEY_PEM) throw new HttpError(503, 'Chưa cấu hình tải nội dung khóa học.');
  const machine = String(input && input.machineId || '').trim().toUpperCase();
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Mã máy không hợp lệ.');
  const keys = (Array.isArray(input.keys) ? input.keys : []).slice(0, 10);
  const today = now.toISOString().slice(0, 10);
  const granted = new Set();
  const grantedCourses = new Set();
  for (const k of keys) {
    const p = await parseKey(env.SIGNING_KEY_PEM, k);
    if (!p) continue;
    if (p.machine !== '*' && String(p.machine).toUpperCase() !== machine) continue;
    if (p.expires !== 'never' && !(typeof p.expires === 'string' && today <= p.expires)) continue;
    let courses = (Array.isArray(p.courses) ? p.courses : []).flatMap((c) => LEGACY_COURSE[c] || [c]).filter((c) => PACKED_COURSES.includes(c));
    let grades = p.grades === 'all' ? GRADES.slice() : (Array.isArray(p.grades) ? p.grades.filter((g) => GRADES.includes(g)) : []);
    const code = String(p.id || '').replace(/^NL-/, '');
    if (/^[A-Z0-9]{6}$/.test(code)) {
      if (await db.prepare('SELECT 1 AS x FROM revocations WHERE code = ?1 AND restored_at IS NULL').bind(code).first()) continue;
      const gone = (await db.prepare('SELECT item FROM item_revocations WHERE code = ?1 AND restored_at IS NULL').bind(code).all()).results.map((r) => r.item);
      const dropped = new Set(gone.map((id) => catalog.byId[id]?.grade).filter((g) => Number.isInteger(g)));
      if (p.grades !== 'all') {
        grades = grades.filter((g) => !dropped.has(g));
        const droppedC = new Set(gone.flatMap((id) => LEGACY_COURSE[id] || [id]));
        courses = courses.filter((c) => !droppedC.has(c));
      }
    }
    grades.forEach((g) => granted.add(g));
    courses.forEach((c) => grantedCourses.add(c));
  }
  const out = {};
  for (const g of [...granted].sort((a, b) => a - b)) out[g] = await gradeKey(env.PACK_MASTER, g);
  const outCourses = {};
  for (const c of [...grantedCourses].sort()) outCourses[c] = await courseKey(env.PACK_MASTER, c);
  const base = String(env.UPDATES_BASE || '').trim().replace(/\/+$/, '');
  if (!/^https:\/\//i.test(base)) throw new HttpError(503, 'Chưa cấu hình nơi lưu nội dung.');
  return { base: base + '/educenter-content', keys: out, courses: outCourses };
}

// Chuyển tiếp tệp công khai trên R2 cho ứng dụng Android (WebView không gọi thẳng R2 được vì CORS). Gói đã mã hóa nên không cần kiểm tra bản quyền ở đây.
function packBase(env) {
  const b = String(env.UPDATES_BASE || '').trim().replace(/\/+$/, '');
  if (!/^https:\/\//i.test(b)) throw new HttpError(503, 'Chưa cấu hình nơi lưu nội dung.');
  return b + '/educenter-content';
}

export async function packIndex(env) {
  const r = await fetch(packBase(env) + '/index.json', { cf: { cacheTtl: 60 } }).catch(() => null);
  if (!r || !r.ok) throw new HttpError(502, 'Chưa đọc được danh sách gói nội dung.');
  const text = await r.text();
  if (text.length > 20000) throw new HttpError(502, 'Danh sách gói nội dung không hợp lệ.');
  return new Response(text, { status: 200, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
}

export const PACK_FILE_RE = /^(lop\d{1,2}|course-[a-z0-9-]{1,60})-[0-9a-f]{10}\.nlp$/;
export async function packFile(env, name) {
  if (!PACK_FILE_RE.test(String(name))) throw new HttpError(404, 'Không tìm thấy.');
  const r = await fetch(packBase(env) + '/' + name, { cf: { cacheTtl: 86400 } }).catch(() => null);
  if (!r || !r.ok) throw new HttpError(404, 'Không có gói nội dung này.');
  const buf = await r.arrayBuffer();
  if (buf.byteLength > 40 * 1024 * 1024) throw new HttpError(502, 'Gói nội dung quá lớn.');
  return new Response(buf, { status: 200, headers: { 'content-type': 'application/octet-stream', 'cache-control': 'public, max-age=31536000, immutable' } });
}
