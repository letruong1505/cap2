#!/usr/bin/env node
// Gói app Phụ huynh (nhẹ, không có bài học) thành thư mục www/ để đưa vào apk riêng (Capacitor).
// Dùng: node tools/build-parent-www.js [--out mobile/www] [--version 1.0.x] [--api https://...]
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };

// Không truyền --version thì lấy số bản của package.json (workflow Windows đặt 1.0.<số lần chạy> trước khi đóng gói).
const pkgVersion = () => { try { return JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8')).version || '1.0.0'; } catch (e) { return '1.0.0'; } };

const FROM_RENDERER = ['styles.css', 'fonts.css', 'progress.js', 'usage.js', 'progress-sync.js', 'progress-ui.js', 'catalog.js', 'timetable.js', 'vietqr.js', 'payment-config.js', 'terms.js'];

function build({ out, version, api, versionCode = 1, desktop = false }) {
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(path.join(out, 'vendor'), { recursive: true });
  for (const f of FROM_RENDERER) fs.copyFileSync(path.join(ROOT, 'renderer', f), path.join(out, f));
  fs.copyFileSync(path.join(ROOT, 'renderer', 'vendor', 'qrcode.js'), path.join(out, 'vendor', 'qrcode.js'));
  fs.cpSync(path.join(ROOT, 'parent', 'digest'), path.join(out, 'digest'), { recursive: true });
  fs.cpSync(path.join(ROOT, 'renderer', 'fonts'), path.join(out, 'fonts'), { recursive: true });
  fs.copyFileSync(path.join(ROOT, 'mobile', 'bridge', 'api.js'), path.join(out, 'api.js'));
  for (const f of ['parent.js', 'courses.js', 'buy.js', 'digest.js']) fs.copyFileSync(path.join(ROOT, 'parent', f), path.join(out, f));
  // Bản Windows dùng khởi động và cập nhật riêng (gọi mạng qua tiến trình chính, cập nhật bằng electron-updater), giữ nguyên tên tệp để index.html dùng chung.
  fs.copyFileSync(path.join(ROOT, 'parent', desktop ? 'parent-boot-desktop.js' : 'parent-boot.js'), path.join(out, 'parent-boot.js'));
  fs.copyFileSync(path.join(ROOT, 'parent', desktop ? 'parent-update-desktop.js' : 'parent-update.js'), path.join(out, 'parent-update.js'));
  const origin = new URL(api).origin;
  fs.writeFileSync(path.join(out, 'index.html'), fs.readFileSync(path.join(ROOT, 'parent', 'index.html'), 'utf8').replace('__API_ORIGIN__', origin));
  fs.writeFileSync(path.join(out, 'mobile-config.js'), 'window.NL_MOBILE_CONFIG = ' + JSON.stringify({ ordersBaseUrl: api, version, versionCode }) + ';\n');
  if (desktop) {
    // Bản Windows: đổi các câu nói "điện thoại này" của phụ huynh thành "máy tính này".
    const swap = [['ngay trên điện thoại này', 'ngay trên máy tính này'], ['Nhắc trên điện thoại này', 'Nhắc trên máy tính này'], ['Điện thoại sẽ nhắc', 'Máy tính sẽ nhắc'], ['để điện thoại nhắc', 'để máy tính nhắc']];
    for (const f of ['index.html', 'buy.js', 'timetable.js']) {
      const fp = path.join(out, f); let t = fs.readFileSync(fp, 'utf8');
      for (const [a, b] of swap) t = t.split(a).join(b);
      fs.writeFileSync(fp, t);
    }
  }
  return out;
}
module.exports = { build, FROM_RENDERER };

if (require.main === module) {
  const api = arg('api', JSON.parse(fs.readFileSync(path.join(ROOT, 'main', 'orders-api.json'), 'utf8')).baseUrl);
  const out = path.resolve(arg('out', path.join(ROOT, 'mobile', 'www')));
  build({ out, version: arg('version', pkgVersion()), api, versionCode: Number(arg('version-code', '1')), desktop: process.argv.includes('--desktop') });
  console.log('Đã tạo app Phụ huynh tại', out);
}
