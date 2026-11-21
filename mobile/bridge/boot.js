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
  // Thông báo nhắc học bài (thời khóa biểu): dùng plugin LocalNotifications nếu apk có; không có thì app chỉ nhắc khi mở.
  window.NLNotify = (function () {
    var cap = window.Capacitor; var ok = false;
    try { ok = !!(cap && cap.registerPlugin && cap.isPluginAvailable && cap.isPluginAvailable('LocalNotifications')); } catch (e) { ok = false; }
    if (!ok) return null;
    var LN = cap.registerPlugin('LocalNotifications');
    return {
      request: function () { return LN.requestPermissions().then(function (r) { return r.display === 'granted'; }); },
      // Thay toàn bộ lịch cũ bằng danh sách mới [{id, at (ms), title, body}].
      schedule: function (items) {
        return LN.checkPermissions().then(function (p) {
          if (p.display !== 'granted') return false;
          return LN.getPending().then(function (pe) {
            var old = (pe.notifications || []).map(function (n) { return { id: n.id }; });
            return old.length ? LN.cancel({ notifications: old }) : null;
          }).then(function () {
            if (!items.length) return true;
            return LN.schedule({ notifications: items.map(function (i) { return { id: i.id, title: i.title, body: i.body, schedule: { at: new Date(i.at), allowWhileIdle: true } }; }) }).then(function () { return true; });
          });
        });
      },
    };
  })();
  var fetchText = function (url) { return fetch(url).then(function (r) { if (!r.ok) throw new Error('Không đọc được ' + url); return r.text(); }); };
  var keyBytes = window.NLMobileLicense.b64uToBytes(cfg.publicKey.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''));

  // Nội dung phụ thuộc mã thiết bị (async) và danh sách môn (product.json), nên dựng cầu nối sau khi có đủ hai thứ.
  var rawSet = Storage.prototype.setItem; var rawGet = Storage.prototype.getItem; var rawRemove = Storage.prototype.removeItem;
  // Cập nhật ứng dụng: chỉ bật khi chạy trong apk có trang khởi động OTA (NL_NATIVE) và kho gói (NLOtaStore).
  var updater = null;
  if (window.NL_NATIVE && window.NLOtaStore && window.NLMobileUpdater && window.NL_NATIVE.otaPublicKey) {
    updater = window.NLMobileUpdater.create({
      fetchFn: function (u, i) { return fetch(u, i); }, baseUrl: function () { return cfg.ordersBaseUrl; }, nacl: window.nacl,
      b64uToBytes: window.NLMobileLicense.b64uToBytes, otaPublicKey: window.NLMobileLicense.b64uToBytes(window.NL_NATIVE.otaPublicKey.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')),
      native: window.NL_NATIVE, runningBuild: function () { return window.NL_OTA_RUNNING || window.NL_NATIVE.code; },
      store: window.NLOtaStore, storage: { get: function (k) { return rawGet.call(ls, k); }, set: function (k, v) { rawSet.call(ls, k, v); } },
      openUrl: function (u) { window.open(u, '_blank'); },
      // Tải apk ngay trong app rồi mở hộp cài đặt của Android (apk cũ chưa có plugin này thì null: dùng openUrl như trước).
      installApk: (function () {
        var cap = window.Capacitor;
        var ok = false; try { ok = !!(cap && cap.registerPlugin && cap.isPluginAvailable && cap.isPluginAvailable('ApkInstaller')); } catch (e) { ok = false; }
        if (!ok) return null;
        var plug = cap.registerPlugin('ApkInstaller');
        return function (url, onProgress) {
          var sub = plug.addListener('progress', function (e) { try { onProgress(e && e.percent | 0); } catch (x) { /* bỏ qua */ } });
          var off = function () { Promise.resolve(sub).then(function (h) { if (h && h.remove) h.remove(); }, function () {}); };
          return plug.install({ url: url }).then(function (r) { off(); return r; }, function (e) { off(); throw e; });
        };
      })(), reload: function () { location.href = 'index.html'; },
    });
  }

  var ready = Promise.all([rawDeviceId(), fetchText('product.json').then(JSON.parse)]).then(function (r) {
    return window.NLMobileBridge.create({
      nacl: window.nacl, publicKey: keyBytes,
      storage: { get: function (k) { return rawGet.call(ls, k); }, set: function (k, v) { rawSet.call(ls, k, v); } },
      rawDeviceId: r[0] || fallbackId(), fetchFn: function (u, i) { return fetch(u, i); }, fetchText: fetchText, product: r[1], config: cfg,
      userStore: window.NLMobileBridge.mirrorUserStore(ls, rawGet, rawSet, rawRemove), updater: updater,
    });
  });

  // Bản quyền dùng cho cả màn hình ngay khi mở: các hàm async của giao diện chờ cầu nối sẵn sàng, riêng storeAll/storeSet phải đồng bộ
  // nên dùng bản sao lưu trực tiếp trên localStorage ngay từ đầu.
  var mirror = window.NLMobileBridge.mirrorUserStore(ls, rawGet, rawSet, rawRemove);
  var names = ['loadManifest', 'loadLesson', 'appInfo', 'productInfo', 'loadLicense', 'activateLicense', 'removeLicense', 'createOrder', 'pinReset', 'orderStatus', 'claimDevice', 'progressSettings', 'progressPush', 'progressView', 'updateStatus', 'checkUpdate', 'downloadUpdate', 'installUpdate'];
  var proxy = { version: cfg.version || 'android', platform: 'android',
    storeAll: function () { return mirror.all(); }, storeSet: function (k, v) { mirror.set(String(k), v); },
    onUpdate: function (cb) { ready.then(function (b) { b.api.onUpdate(cb); }); },
    onLicenseChanged: function (cb) { ready.then(function (b) { b.api.onLicenseChanged(cb); }); } };
  names.forEach(function (n) { proxy[n] = function () { var a = arguments; return ready.then(function (b) { return b.api[n].apply(null, a); }); }; });
  // Đọc phát âm tiếng Anh bằng giọng đọc của Android (plugin TextToSpeech). WebView không có speechSynthesis.
  // Chỉ bật khi apk có plugin; apk cũ không có thì giao diện giữ thông báo cũ.
  var tts = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.TextToSpeech;
  if (tts && tts.speak) {
    proxy.speak = function (text) {
      return Promise.resolve(tts.stop ? tts.stop() : null).catch(function () {}).then(function () {
        return tts.speak({ text: String(text).slice(0, 200), lang: 'en-US', rate: 0.85, pitch: 1, volume: 1, category: 'ambient' });
      }).then(function () { return { ok: true }; }, function (e) { return { ok: false, error: String(e && e.message || e) }; });
    };
  }
  window.vungBai = proxy;
  ready.then(function (b) { b.heartbeat.start(); }).catch(function () {});
  // Kiểm tra bản mới ngầm sau khi mở app vài giây (tối đa mỗi 6 giờ một lần).
  if (updater) setTimeout(function () { updater.check({ auto: true }); }, 4000);
})();
