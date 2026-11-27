// Ký khóa bản quyền NL1-... giống hệt công cụ cấp khóa (keygen) và khớp main/license/verify.js của phần mềm.
const enc = new TextEncoder();

function b64uFromBytes(bytes) {
  let s = '';
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function pemToDer(pem) {
  const b64 = String(pem).replace(/-----[A-Z ]+-----/g, '').replace(/\s+/g, '');
  const bin = atob(b64);
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

let cached = { pem: null, key: null };
async function privateKey(pem) {
  if (cached.pem === pem && cached.key) return cached.key;
  const key = await crypto.subtle.importKey('pkcs8', pemToDer(pem), { name: 'Ed25519' }, false, ['sign']);
  cached = { pem, key };
  return key;
}

export const TRIAL_RE = /^TRIAL (\d{4}-\d{2}-\d{2})/;
const dateOf = (now) => now.toISOString().slice(0, 10);

// Dựng nội dung khóa từ đơn hàng. grades: các lớp Văn hóa đã mua; courses: các khóa Kỹ năng đã mua.
export function payloadFor(order, catalog, now = new Date()) {
  const items = JSON.parse(order.items);
  const grades = items.map((id) => catalog.byId[id]?.grade).filter((g) => Number.isInteger(g)).sort((a, b) => a - b);
  const courses = items.filter((id) => !catalog.byId[id]?.grade);
  const payload = { v: 1, id: 'NL-' + order.code, owner: order.name, grades, courses, machine: order.machine, issued: dateOf(now), expires: 'never' };
  // Đơn dùng thử ghi hạn trong ghi chú (TRIAL yyyy-mm-dd): cấp lại khóa (đổi máy) vẫn giữ nguyên hạn, không thành khóa vĩnh viễn.
  const t = TRIAL_RE.exec(String(order.note || ''));
  if (t) { payload.expires = t[1]; payload.trial = true; }
  return payload;
}

export async function signKey(pem, payload) {
  const body = enc.encode(JSON.stringify(payload));
  const sig = new Uint8Array(await crypto.subtle.sign('Ed25519', await privateKey(pem), body));
  return 'NL1-' + b64uFromBytes(body) + '.' + b64uFromBytes(sig);
}
