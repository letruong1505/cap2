// Khởi động app Phụ huynh bản Windows: dựng window.vungBai tối giản (chỉ gọi máy chủ Nam Linh qua tiến trình chính) và nhắc học bài.
(function () {
  'use strict';
  var cfg = window.NL_MOBILE_CONFIG || {};
  var ls = window.localStorage;
  function deviceId() {
    var k = 'nl-parent-machine'; var v = null;
    try { v = ls.getItem(k); } catch (e) { /* bỏ qua */ }
    if (!v || !/^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/.test(v)) {
      var a = new Uint8Array(6); window.crypto.getRandomValues(a);
      var hex = ''; for (var i = 0; i < a.length; i++) hex += ('0' + a[i].toString(16)).slice(-2);
      hex = hex.toUpperCase(); v = hex.slice(0, 4) + '-' + hex.slice(4, 8) + '-' + hex.slice(8, 12);
      try { ls.setItem(k, v); } catch (e) { /* bỏ qua */ }
    }
    return v;
  }
  var id = deviceId();
  // Cuộc gọi mạng đi qua tiến trình chính (NLDesktop.fetch) nên không vướng giới hạn CORS của trang file://.
  function fetchFn(u, init) {
    if (!window.NLDesktop) return Promise.reject(new Error('offline'));
    return window.NLDesktop.fetch(u, init).then(function (r) {
      if (!r.status) throw new Error('offline');
      return { ok: r.ok, status: r.status, json: function () { try { return Promise.resolve(JSON.parse(r.body)); } catch (e) { return Promise.reject(e); } } };
    });
  }
  var client = window.NLMobileApi.makeClient({ baseUrl: function () { return cfg.ordersBaseUrl; }, fetchFn: fetchFn, machineId: function () { return id; } });
  window.vungBai = {
    version: cfg.version || 'phuhuynh', platform: 'windows', role: 'parent', machineId: id,
    createOrder: function (x) { return client.createOrder(x); },
    orderStatus: function (c) { return client.orderStatus(c); },
    familyCreate: function (x) { return client.familyCreate(x); },
    progressView: function (x) { return client.progressView(x); },
    progressSettings: function (x) { return client.progressSettings(x); },
    storeAll: function () { return {}; }, storeSet: function () {},
  };
  // Nhắc học bài: hẹn giờ trong tiến trình đang chạy (app thu nhỏ xuống khay vẫn nhắc được).
  window.NLNotify = (function () {
    if (typeof Notification === 'undefined') return null;
    var timers = [];
    return {
      request: function () { return Promise.resolve(Notification.permission === 'granted' ? true : Notification.requestPermission().then(function (p) { return p === 'granted'; })); },
      schedule: function (items) {
        timers.forEach(clearTimeout); timers = [];
        var now = Date.now();
        (items || []).forEach(function (i) {
          var ms = new Date(i.at).getTime() - now;
          if (ms > 0 && ms < 2147483000) timers.push(setTimeout(function () { try { new Notification(i.title, { body: i.body }); } catch (e) { /* bỏ qua */ } }, ms));
        });
        return Promise.resolve(true);
      },
    };
  })();
})();
