// Kiểm tra khoá bản quyền offline: khoá = dữ liệu JSON + chữ ký Ed25519 của chủ sản phẩm.
// App chỉ giữ khoá công khai (public-key.pem) nên không thể tự tạo khoá mới.
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const PREFIX = 'NL1-';
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const PUBLIC_KEY_FILE = path.join(__dirname, 'public-key.pem');

const b64u = (buf) => Buffer.from(buf).toString('base64url');

function publicKey() {
  return crypto.createPublicKey(fs.readFileSync(PUBLIC_KEY_FILE, 'utf8'));
}

// Tách và kiểm tra chữ ký. Trả về { ok, payload } hoặc { ok:false, reason }.
function parseKey(key, pubKey = publicKey()) {
  const text = String(key || '').replace(/\s+/g, '');
  if (!text.startsWith(PREFIX) || text.indexOf('.') < 0) return { ok: false, reason: 'format' };
  const [body, sig] = text.slice(PREFIX.length).split('.');
  let payload;
  try {
    const okSig = crypto.verify(null, Buffer.from(body, 'base64url'), pubKey, Buffer.from(sig, 'base64url'));
    if (!okSig) return { ok: false, reason: 'signature' };
    payload = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
  } catch {
    return { ok: false, reason: 'format' };
  }
  const gradesOk = payload.grades === 'all' || (Array.isArray(payload.grades) && payload.grades.every((g) => Number.isInteger(g)));
  if (payload.v !== 1 || !gradesOk || !DATE_RE.test(payload.expires || '')) return { ok: false, reason: 'format' };
  return { ok: true, payload };
}

// Ngày hiện tại dạng YYYY-MM-DD theo giờ máy.
function today(now = new Date()) {
  const p = (n) => String(n).padStart(2, '0');
  return `${now.getFullYear()}-${p(now.getMonth() + 1)}-${p(now.getDate())}`;
}

// Đánh giá khoá trên máy hiện tại. Trạng thái: ok | invalid | wrong-machine | expired.
function evaluateKey(key, machineId, now = new Date(), pubKey) {
  const r = parseKey(key, pubKey);
  if (!r.ok) return { status: 'invalid', reason: r.reason };
  const p = r.payload;
  const info = { owner: p.owner || '', id: p.id || '', grades: p.grades, expiresOn: p.expires };
  if (p.machine !== '*' && p.machine !== machineId) return { status: 'wrong-machine', ...info };
  if (today(now) > p.expires) return { status: 'expired', ...info };
  return { status: 'ok', ...info };
}

module.exports = { PREFIX, b64u, parseKey, evaluateKey, today };
