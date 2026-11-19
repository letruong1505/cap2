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

const SCRIPTS = ['mobile/vendor/nacl-fast.min.js', 'mobile/mobile-config.js', 'mobile/license.js', 'mobile/api.js', 'mobile/content.js', 'mobile/heartbeat.js', 'mobile/machine.js', 'mobile/bridge.js', 'mobile/boot.js'];

// Chỉnh index.html cho điện thoại: nạp cầu nối trước persist-shim.js, cho phép gọi máy chủ đơn hàng, thêm viewport, sửa đường dẫn core/.
function rewriteIndex(html, apiOrigin) {
  const tags = SCRIPTS.map((s) => `  <script src="${s}"></script>\n`).join('');
  let out = html.replace('  <script src="persist-shim.js"></script>', tags + '  <script src="persist-shim.js"></script>');
  if (out === html) throw new Error('Không tìm thấy persist-shim.js trong index.html');
  out = out.replace('src="../core/rational.js"', 'src="core/rational.js"');
  out = out.replace("font-src 'self'\"", `font-src 'self'; connect-src 'self' ${apiOrigin}"`);
  if (!out.includes(`connect-src 'self' ${apiOrigin}`)) throw new Error('Không sửa được Content-Security-Policy');
  if (!/name="viewport"/.test(out)) out = out.replace('<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />');
  return out;
}

function build({ out, pubkey, version, commit, api }) {
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(path.join(out, 'mobile'), { recursive: true });
  fs.cpSync(path.join(ROOT, 'renderer'), out, { recursive: true });
  fs.cpSync(path.join(ROOT, 'content'), path.join(out, 'content'), { recursive: true });
  fs.mkdirSync(path.join(out, 'core'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'core', 'rational.js'), path.join(out, 'core', 'rational.js'));
  fs.copyFileSync(path.join(ROOT, 'main', 'product.json'), path.join(out, 'product.json'));
  for (const f of fs.readdirSync(path.join(ROOT, 'mobile', 'bridge'))) fs.copyFileSync(path.join(ROOT, 'mobile', 'bridge', f), path.join(out, 'mobile', f));
  fs.mkdirSync(path.join(out, 'mobile', 'vendor'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'mobile', 'vendor', 'nacl-fast.min.js'), path.join(out, 'mobile', 'vendor', 'nacl-fast.min.js'));
  fs.copyFileSync(path.join(ROOT, 'mobile', 'vendor', 'TWEETNACL-LICENSE.txt'), path.join(out, 'mobile', 'vendor', 'TWEETNACL-LICENSE.txt'));
  const config = { publicKey: rawPublicKey(pubkey), ordersBaseUrl: api, version, commit };
  fs.writeFileSync(path.join(out, 'mobile', 'mobile-config.js'), 'window.NL_MOBILE_CONFIG = ' + JSON.stringify(config) + ';\n');
  fs.writeFileSync(path.join(out, 'index.html'), rewriteIndex(fs.readFileSync(path.join(ROOT, 'renderer', 'index.html'), 'utf8'), new URL(api).origin));
  return config;
}

module.exports = { build, rewriteIndex, rawPublicKey, SCRIPTS };

if (require.main === module) {
  const api = arg('api', JSON.parse(fs.readFileSync(path.join(ROOT, 'main', 'orders-api.json'), 'utf8')).baseUrl);
  const cfg = build({ out: path.resolve(arg('out', path.join(ROOT, 'mobile', 'www'))), pubkey: path.resolve(arg('pubkey', path.join(ROOT, 'main', 'license', 'public-key.pem'))), version: arg('version', JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8')).version), commit: arg('commit', 'local'), api });
  console.log('Đã tạo', arg('out', 'mobile/www'), '— bản', cfg.version, '— máy chủ', cfg.ordersBaseUrl);
}
