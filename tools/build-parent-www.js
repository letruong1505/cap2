#!/usr/bin/env node
// Gói app Phụ huynh (nhẹ, không có bài học) thành thư mục www/ để đưa vào apk riêng (Capacitor).
// Dùng: node tools/build-parent-www.js [--out mobile/www] [--version 1.0.0] [--api https://...]
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };

const FROM_RENDERER = ['styles.css', 'fonts.css', 'progress.js', 'usage.js', 'progress-sync.js', 'progress-ui.js', 'catalog.js', 'timetable.js'];

function build({ out, version, api }) {
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(path.join(out, 'vendor'), { recursive: true });
  for (const f of FROM_RENDERER) fs.copyFileSync(path.join(ROOT, 'renderer', f), path.join(out, f));
  fs.cpSync(path.join(ROOT, 'renderer', 'fonts'), path.join(out, 'fonts'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'mobile', 'bridge', 'api.js'), path.join(out, 'api.js'));
  for (const f of ['parent.js', 'parent-boot.js']) fs.copyFileSync(path.join(ROOT, 'parent', f), path.join(out, f));
  const origin = new URL(api).origin;
  fs.writeFileSync(path.join(out, 'index.html'), fs.readFileSync(path.join(ROOT, 'parent', 'index.html'), 'utf8').replace('__API_ORIGIN__', origin));
  fs.writeFileSync(path.join(out, 'mobile-config.js'), 'window.NL_MOBILE_CONFIG = ' + JSON.stringify({ ordersBaseUrl: api, version }) + ';\n');
  return out;
}
module.exports = { build, FROM_RENDERER };

if (require.main === module) {
  const api = arg('api', JSON.parse(fs.readFileSync(path.join(ROOT, 'main', 'orders-api.json'), 'utf8')).baseUrl);
  const out = path.resolve(arg('out', path.join(ROOT, 'mobile', 'www')));
  build({ out, version: arg('version', '1.0.0'), api });
  console.log('Đã tạo app Phụ huynh tại', out);
}
