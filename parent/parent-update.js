// Tự kiểm tra bản mới của app Phụ huynh (lúc mở và mỗi 2 giờ), tải apk ngay trong app rồi mở hộp cài đặt.
(function () {
  'use strict';
  var cfg = window.NL_MOBILE_CONFIG || {};
  var bar = document.getElementById('update-bar');
  if (!bar || !cfg.ordersBaseUrl) return;
  var base = String(cfg.ordersBaseUrl).replace(/\/+$/, '');
  var busy = false;

  function plugin() {
    try { return window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.ApkInstaller; } catch (e) { return null; }
  }
  function say(text, btnText, onClick) {
    bar.replaceChildren();
    var s = document.createElement('span'); s.textContent = text; bar.append(s);
    if (btnText) { var b = document.createElement('button'); b.type = 'button'; b.textContent = btnText; b.addEventListener('click', onClick); bar.append(' ', b); }
    bar.hidden = false;
  }
  function install(latest) {
    var plug = plugin();
    if (!plug) { window.open(latest.apkUrl, '_blank'); return; }
    if (busy) return; busy = true;
    say('Đang tải bản ' + latest.version + ': 0%');
    var sub = plug.addListener('progress', function (e) { say('Đang tải bản ' + latest.version + ': ' + ((e && e.percent) | 0) + '%'); });
    plug.install({ url: latest.apkUrl }).then(function () { busy = false; offer(latest); }, function (e) {
      busy = false;
      if (e && e.code === 'needs_permission') say('Hãy bật "Cho phép từ nguồn này" rồi quay lại app và bấm Tải về lần nữa.', 'Tải về', function () { install(latest); });
      else { window.open(latest.apkUrl, '_blank'); say('Tải trong app lỗi, đã mở trình duyệt để tải.', 'Thử lại', function () { install(latest); }); }
    }).then(function () { Promise.resolve(sub).then(function (h) { if (h && h.remove) h.remove(); }, function () {}); });
  }
  function offer(latest) { say('Có bản mới ' + latest.version + (latest.notes ? ': ' + latest.notes : '') + '.', 'Tải về và cài', function () { install(latest); }); }

  function check() {
    if (busy) return;
    fetch(base + '/api/app/parent/latest', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (j && j.apkUrl && (j.versionCode | 0) > (cfg.versionCode | 0)) offer(j);
    }).catch(function () { /* không có mạng thì thôi */ });
  }
  check();
  setInterval(check, 2 * 3600 * 1000);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) check(); });
})();
