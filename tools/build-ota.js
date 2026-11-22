#!/usr/bin/env node
// Đóng gói cập nhật nội dung (OTA) cho ứng dụng Android từ thư mục www đã build.
// Gói chứa mã giao diện và cầu nối (chỉ tệp văn bản); nội dung bài học, phông chữ và phần Android gốc nằm trong apk.
// Gói được ký Ed25519 bằng khóa riêng OTA (không phải khóa bản quyền); ứng dụng kiểm tra chữ ký bằng khóa công khai
// đã nhúng trong apk (mobile/ota-public-key.txt) trước khi dùng.
// Dùng: OTA_PRIVATE_KEY_BASE64=... node tools/build-ota.js --www mobile/www --out ota.nlo --build 12 --version 1.0.12 [--min-native 0]
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PREFIX = 'NLO1-';
const TEXT_EXT = new Set(['.js', '.css', '.json', '.txt']);
const MAX_BYTES = 8 * 1024 * 1024;
// Không đưa vào gói: nội dung bài học, trang khởi động và phần phải nằm trong apk.
const SKIP = (rel) => rel.startsWith('content/') || rel.startsWith('fonts/') || rel === 'index.html' || rel === 'app.html'
  || rel === 'mobile/native.js' || rel === 'mobile/ota-boot.js' || rel === 'mobile/ota-store.js' || rel.endsWith('LICENSE.txt');

// Bản build tách gói (main/content-mode.json): file nội dung khóa Kỹ năng đã bị cắt bớt nên không đưa vào gói OTA. Máy cài apk cũ (nội dung
// đầy đủ trong apk) khi nhận OTA vẫn nạp file đầy đủ của apk; máy cài apk mới nhận nội dung qua gói tải về. Xem tools/build-packs.js.
const PRUNED = fs.existsSync(path.join(__dirname, '..', 'main', 'content-mode.json'));
const PRUNED_FILES = new Set(['tu-duy-content.js', 'gia-su-ai-content.js', 'ai-work-claude.js', 'ai-work-chatgpt.js', 'ai-work-gemini.js']);
const skipPruned = (rel) => PRUNED && PRUNED_FILES.has(rel);

const b64u = (buf) => Buffer.from(buf).toString('base64url');

function collect(dir, base = dir, out = {}) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) { collect(full, base, out); continue; }
    const rel = path.relative(base, full).split(path.sep).join('/');
    if (SKIP(rel) || skipPruned(rel) || !TEXT_EXT.has(path.extname(rel).toLowerCase())) continue;
    out[rel] = fs.readFileSync(full, 'utf8');
  }
  return out;
}

function createBundle({ www, build, version, minNative = 0, privateKeyPem }) {
  if (!Number.isInteger(build) || build < 1) throw new Error('Số build không hợp lệ.');
  const html = fs.readFileSync(path.join(www, 'app.html'), 'utf8');
  const files = collect(www);
  // Chỉ giữ tệp mà app.html thật sự gọi (script, css) để gói nhỏ và không kéo theo tệp lạ.
  const wanted = new Set();
  for (const m of html.matchAll(/<script\s+src="([^"]+)"/g)) wanted.add(m[1]);
  for (const m of html.matchAll(/<link\s+rel="stylesheet"\s+href="([^"]+)"/g)) wanted.add(m[1]);
  wanted.add('product.json');
  const picked = {};
  for (const rel of wanted) if (files[rel] != null) picked[rel] = files[rel];
  const payload = Buffer.from(JSON.stringify({ v: 1, build, version: String(version), minNative, createdAt: new Date().toISOString(), html, files: picked }));
  if (payload.length > MAX_BYTES) throw new Error('Gói cập nhật quá lớn (' + payload.length + ' byte).');
  const key = crypto.createPrivateKey(privateKeyPem);
  const sig = crypto.sign(null, payload, key);
  return PREFIX + b64u(payload) + '.' + b64u(sig);
}

// Kiểm tra gói bằng khóa công khai (base64 thô 32 byte). Trả về nội dung nếu hợp lệ, ngược lại ném lỗi.
function verifyBundle(text, publicKeyB64) {
  const s = String(text || '').trim();
  if (!s.startsWith(PREFIX)) throw new Error('Không phải gói cập nhật.');
  const [p, sg] = s.slice(PREFIX.length).split('.');
  if (!p || !sg) throw new Error('Gói cập nhật hỏng.');
  const raw = Buffer.from(publicKeyB64, 'base64');
  const spki = Buffer.concat([Buffer.from('302a300506032b6570032100', 'hex'), raw]);
  const pub = crypto.createPublicKey({ key: spki, format: 'der', type: 'spki' });
  const payload = Buffer.from(p, 'base64url');
  if (!crypto.verify(null, payload, pub, Buffer.from(sg, 'base64url'))) throw new Error('Chữ ký gói cập nhật không hợp lệ.');
  return JSON.parse(payload.toString('utf8'));
}

module.exports = { createBundle, verifyBundle, collect, PREFIX };

if (require.main === module) {
  const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
  const b64 = process.env.OTA_PRIVATE_KEY_BASE64;
  if (!b64) { console.error('Thiếu OTA_PRIVATE_KEY_BASE64: bỏ qua đóng gói OTA.'); process.exit(3); }
  const root = path.join(__dirname, '..');
  const text = createBundle({
    www: path.resolve(arg('www', path.join(root, 'mobile', 'www'))), build: Number(arg('build', '0')), version: arg('version', '0'),
    minNative: Number(arg('min-native', fs.readFileSync(path.join(root, 'mobile', 'ota-min-native.txt'), 'utf8').trim() || '0')),
    privateKeyPem: Buffer.from(b64, 'base64').toString('utf8'),
  });
  const pub = fs.readFileSync(path.join(root, 'mobile', 'ota-public-key.txt'), 'utf8').trim();
  const info = verifyBundle(text, pub); // tự kiểm tra: khóa riêng phải khớp khóa công khai trong apk
  fs.writeFileSync(path.resolve(arg('out', 'ota.nlo')), text);
  console.log('Gói OTA build', info.build, '—', Object.keys(info.files).length, 'tệp —', Math.round(text.length / 1024), 'KB');
}
