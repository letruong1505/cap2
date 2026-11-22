#!/usr/bin/env node
// Gói giao diện + nội dung thành thư mục www/ để đưa vào ứng dụng Android (Capacitor).
// Dùng: node tools/build-mobile-www.js [--out mobile/www] [--pubkey main/license/public-key.pem] [--version 1.0.0] [--commit abc] [--api https://...]
// Khóa công khai mặc định là khóa thật của sản phẩm (main/license/public-key.pem). Chỉ kiểm thử mới dùng --pubkey khác.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.join(__dirname, '..');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}

// Khóa công khai Ed25519 dạng 32 byte thô (base64), lấy từ file PEM.
function rawPublicKey(pemPath) {
  const der = crypto.createPublicKey(fs.readFileSync(pemPath, 'utf8')).export({ type: 'spki', format: 'der' });
  return Buffer.from(der.subarray(-32)).toString('base64');
}

const SCRIPTS = ['mobile/native.js', 'mobile/ota-store.js', 'mobile/vendor/nacl-fast.min.js', 'mobile/mobile-config.js', 'mobile/license.js', 'mobile/api.js', 'mobile/content.js', 'mobile/packs.js', 'mobile/heartbeat.js', 'mobile/machine.js', 'mobile/updater.js', 'mobile/bridge.js', 'mobile/boot.js'];

// Chỉnh index.html cho điện thoại: nạp cầu nối trước persist-shim.js, cho phép gọi máy chủ đơn hàng, thêm viewport, sửa đường dẫn core/.
function rewriteIndex(html, apiOrigin) {
  const tags = SCRIPTS.map((s) => `  <script src="${s}"></script>\n`).join('');
  let out = html.replace('  <script src="persist-shim.js"></script>', tags + '  <script src="persist-shim.js"></script>');
  if (out === html) throw new Error('Không tìm thấy persist-shim.js trong index.html');
  out = out.replace('src="../core/rational.js"', 'src="core/rational.js"');
  // blob: cho phép nạp gói cập nhật nội dung (OTA) đã được kiểm tra chữ ký.
  out = out.replace("default-src 'self';", "default-src 'self'; script-src 'self' blob:;");
  out = out.replace("font-src 'self'\"", `font-src 'self'; connect-src 'self' ${apiOrigin}"`);
  if (!out.includes(`connect-src 'self' ${apiOrigin}`)) throw new Error('Không sửa được Content-Security-Policy');
  if (!/name="viewport"/.test(out)) out = out.replace('<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />');
  return out;
}

// Trang khởi động (index.html): đọc gói OTA nếu có, nếu không thì chuyển sang app.html trong apk.
function launcherHtml(apiOrigin) {
  return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' blob:; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' ${apiOrigin}" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>Nam Linh Educenter</title>
  <style>html,body{margin:0;background:#14304F}</style>
</head>
<body>
  <script src="mobile/native.js"></script>
  <script src="mobile/ota-store.js"></script>
  <script src="mobile/ota-boot.js"></script>
</body>
</html>
`;
}

function build({ out, pubkey, version, commit, api, versionCode = 1, otaPublicKey }) {
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(path.join(out, 'mobile'), { recursive: true });
  fs.cpSync(path.join(ROOT, 'renderer'), out, { recursive: true });
  fs.cpSync(path.join(ROOT, 'content'), path.join(out, 'content'), { recursive: true });
  fs.mkdirSync(path.join(out, 'core'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'core', 'rational.js'), path.join(out, 'core', 'rational.js'));
  // Danh sách môn lấy từ product/nam-linh-educenter.json (bản Windows cũng được chép từ file này khi build, xem build-win.yml),
  // không lấy main/product.json vì file đó chỉ là bản sao do tools/select-product.js ghi ra và có thể cũ.
  const product = JSON.parse(fs.readFileSync(path.join(ROOT, 'product', 'nam-linh-educenter.json'), 'utf8'));
  for (const sub of product.subjects) if (!fs.existsSync(path.join(ROOT, 'content', sub, 'manifest.json'))) throw new Error('Thiếu nội dung môn: ' + sub);
  fs.writeFileSync(path.join(out, 'product.json'), JSON.stringify(product, null, 2) + '\n');
  for (const f of fs.readdirSync(path.join(ROOT, 'mobile', 'bridge'))) fs.copyFileSync(path.join(ROOT, 'mobile', 'bridge', f), path.join(out, 'mobile', f));
  fs.mkdirSync(path.join(out, 'mobile', 'vendor'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'mobile', 'vendor', 'nacl-fast.min.js'), path.join(out, 'mobile', 'vendor', 'nacl-fast.min.js'));
  fs.copyFileSync(path.join(ROOT, 'mobile', 'vendor', 'TWEETNACL-LICENSE.txt'), path.join(out, 'mobile', 'vendor', 'TWEETNACL-LICENSE.txt'));
  const config = { publicKey: rawPublicKey(pubkey), ordersBaseUrl: api, version, commit };
  fs.writeFileSync(path.join(out, 'mobile', 'mobile-config.js'), 'window.NL_MOBILE_CONFIG = ' + JSON.stringify(config) + ';\n');
  // main/content-mode.json do tools/build-packs.js --prune tạo: content/ chỉ còn mục lục và bài học thử, phần còn lại tải về theo lớp đã mua.
  const native = { code: versionCode, version, otaPublicKey, packs: fs.existsSync(path.join(ROOT, 'main', 'content-mode.json')) };
  fs.writeFileSync(path.join(out, 'mobile', 'native.js'), 'window.NL_NATIVE = ' + JSON.stringify(native) + ';\n');
  fs.writeFileSync(path.join(out, 'app.html'), rewriteIndex(fs.readFileSync(path.join(ROOT, 'renderer', 'index.html'), 'utf8'), new URL(api).origin));
  fs.writeFileSync(path.join(out, 'index.html'), launcherHtml(new URL(api).origin));
  fs.copyFileSync(path.join(ROOT, 'mobile', 'bridge', 'ota-boot.js'), path.join(out, 'mobile', 'ota-boot.js'));
  return config;
}

module.exports = { build, rewriteIndex, launcherHtml, rawPublicKey, SCRIPTS };

if (require.main === module) {
  const api = arg('api', JSON.parse(fs.readFileSync(path.join(ROOT, 'main', 'orders-api.json'), 'utf8')).baseUrl);
  const cfg = build({ out: path.resolve(arg('out', path.join(ROOT, 'mobile', 'www'))), pubkey: path.resolve(arg('pubkey', path.join(ROOT, 'main', 'license', 'public-key.pem'))), version: arg('version', JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8')).version), commit: arg('commit', 'local'), api,
    versionCode: Number(arg('version-code', '1')), otaPublicKey: fs.readFileSync(path.join(ROOT, 'mobile', 'ota-public-key.txt'), 'utf8').trim() });
  console.log('Đã tạo', arg('out', 'mobile/www'), '— bản', cfg.version, '— máy chủ', cfg.ordersBaseUrl);
}
