// Khởi động trong WebView Android (Capacitor): nối các module vào window.vungBai. Phải nạp trước persist-shim.js.
// Cần nạp trước: vendor/nacl-fast.min.js, mobile-config.js (khóa công khai, địa chỉ máy chủ, số bản), license.js, api.js, content.js, heartbeat.js, machine.js, bridge.js.
(function () {
  'use strict';
  if (window.vungBai) return; // đang chạy trong Electron (Windows): đã có cầu nối riêng
  var cfg = window.NL_MOBILE_CONFIG;
  if (!cfg || !window.nacl) return;

  var ls = window.localStorage;
  // Mã thiết bị: ưu tiên mã do Android cấp (qua plugin Device của Capacitor); không có thì dùng mã ngẫu nhiên lưu cục bộ (chạy thử trên trình duyệt).
  function rawDeviceId() {
    var dev = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.Device;
    if (dev && dev.getId) return dev.getId().then(function (r) { return r && r.identifier ? r.identifier : null; }).catch(function () { return null; });
    return Promise.resolve(null);
  }
  function fallbackId() {
    var k = 'nl-device-fallback';
    var v = null;
    try { v = ls.getItem(k); } catch (e) { /* bỏ qua */ }
    if (!v) {
      var b = window.nacl.randomBytes(16); v = '';
      for (var i = 0; i < b.length; i++) v += ('0' + b[i].toString(16)).slice(-2);
      try { ls.setItem(k, v); } catch (e) { /* bỏ qua */ }
    }
    return v;
  }
  var fetchText = function (url) { return fetch(url).then(function (r) { if (!r.ok) throw new Error('Không đọc được ' + url); return r.text(); }); };
  var keyBytes = window.NLMobileLicense.b64uToBytes(cfg.publicKey.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''));

  // Nội dung phụ thuộc mã thiết bị (async) và danh sách môn (product.json), nên dựng cầu nối sau khi có đủ hai thứ.
  var rawSet = Storage.prototype.setItem; var rawGet = Storage.prototype.getItem; var rawRemove = Storage.prototype.removeItem;
  var ready = Promise.all([rawDeviceId(), fetchText('product.json').then(JSON.parse)]).then(function (r) {
    return window.NLMobileBridge.create({
      nacl: window.nacl, publicKey: keyBytes,
      storage: { get: function (k) { return rawGet.call(ls, k); }, set: function (k, v) { rawSet.call(ls, k, v); } },
      rawDeviceId: r[0] || fallbackId(), fetchFn: function (u, i) { return fetch(u, i); }, fetchText: fetchText, product: r[1], config: cfg,
      userStore: window.NLMobileBridge.mirrorUserStore(ls, rawGet, rawSet, rawRemove),
    });
  });

  // Bản quyền dùng cho cả màn hình ngay khi mở: các hàm async của giao diện chờ cầu nối sẵn sàng, riêng storeAll/storeSet phải đồng bộ
  // nên dùng bản sao lưu trực tiếp trên localStorage ngay từ đầu.
  var mirror = window.NLMobileBridge.mirrorUserStore(ls, rawGet, rawSet, rawRemove);
  var names = ['loadManifest', 'loadLesson', 'appInfo', 'productInfo', 'loadLicense', 'activateLicense', 'removeLicense', 'createOrder', 'pinReset', 'orderStatus', 'claimDevice', 'updateStatus', 'checkUpdate', 'downloadUpdate', 'installUpdate'];
  var proxy = { version: cfg.version || 'android', platform: 'android',
    storeAll: function () { return mirror.all(); }, storeSet: function (k, v) { mirror.set(String(k), v); },
    onUpdate: function () {},
    onLicenseChanged: function (cb) { ready.then(function (b) { b.api.onLicenseChanged(cb); }); } };
  names.forEach(function (n) { proxy[n] = function () { var a = arguments; return ready.then(function (b) { return b.api[n].apply(null, a); }); }; });
  window.vungBai = proxy;
  ready.then(function (b) { b.heartbeat.start(); }).catch(function () {});
})();
