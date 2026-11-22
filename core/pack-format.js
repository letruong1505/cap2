// Định dạng gói nội dung khóa học theo lớp: gzip rồi mã hóa AES-256-GCM.
// File gói: "NLP1" + iv (12 byte) + tag (16 byte) + dữ liệu mã hóa. Khoá của từng lớp sinh từ bí mật PACK_MASTER
// (HMAC-SHA256), chỉ máy chủ giữ bí mật này và chỉ cấp khoá lớp cho máy có bản quyền hợp lệ.
const crypto = require('crypto');
const zlib = require('zlib');

const MAGIC = Buffer.from('NLP1');
const KEY_LABEL = (grade) => `nl-pack-v1:lop${Number(grade)}`;

function deriveGradeKey(master, grade) {
  if (!master || String(master).length < 16) throw new Error('PACK_MASTER quá ngắn');
  return crypto.createHmac('sha256', String(master)).update(KEY_LABEL(grade)).digest();
}

// files: { "toan7/tap1/...json": "nội dung văn bản", ... }
function encryptPack(files, key) {
  const raw = zlib.gzipSync(Buffer.from(JSON.stringify({ v: 1, files }), 'utf8'), { level: 9 });
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv('aes-256-gcm', key, iv);
  const enc = Buffer.concat([c.update(raw), c.final()]);
  return Buffer.concat([MAGIC, iv, c.getAuthTag(), enc]);
}

function decryptPack(buf, key) {
  if (!Buffer.isBuffer(buf) || buf.length < 4 + 12 + 16 + 1 || !buf.subarray(0, 4).equals(MAGIC)) throw new Error('Gói nội dung không hợp lệ');
  const d = crypto.createDecipheriv('aes-256-gcm', key, buf.subarray(4, 16));
  d.setAuthTag(buf.subarray(16, 32));
  let raw;
  try { raw = Buffer.concat([d.update(buf.subarray(32)), d.final()]); } catch { throw new Error('Không giải mã được gói nội dung'); }
  const j = JSON.parse(zlib.gunzipSync(raw).toString('utf8'));
  if (!j || j.v !== 1 || typeof j.files !== 'object') throw new Error('Gói nội dung không hợp lệ');
  return j.files;
}

const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
const gradeOfSubject = (s) => Number(String(s).match(/(\d+)$/)?.[1]);

module.exports = { deriveGradeKey, encryptPack, decryptPack, sha256, gradeOfSubject, KEY_LABEL };
