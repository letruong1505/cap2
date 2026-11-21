// Khởi động app Phụ huynh: dựng window.vungBai tối giản (chỉ gọi máy chủ Nam Linh) và thông báo nhắc học bài.
(function () {
  'use strict';
  var cfg = window.NL_MOBILE_CONFIG || {};
  var ls = window.localStorage;
  // Mã máy dạng XXXX-XXXX-XXXX (máy chủ chỉ nhận dạng này), sinh ngẫu nhiên một lần rồi lưu lại.
  function deviceId() {
    var k = 'nl-parent-machine'; var v = null;
    try { v = ls.getItem(k); } catch (e) { /* bỏ qua */ }
    if (!v || !/^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/.test(v)) {
      var a = new Uint8Array(6);
      (window.crypto || { getRandomValues: function (x) { for (var i = 0; i < x.length; i++) x[i] = Math.floor(Math.random() * 256); } }).getRandomValues(a);
      var hex = ''; for (var i = 0; i < a.length; i++) hex += ('0' + a[i].toString(16)).slice(-2);
      hex = hex.toUpperCase(); v = hex.slice(0, 4) + '-' + hex.slice(4, 8) + '-' + hex.slice(8, 12);
      try { ls.setItem(k, v); } catch (e) { /* bỏ qua */ }
    }
    return v;
  }
  var id = deviceId();
  var client = window.NLMobileApi.makeClient({ baseUrl: function () { return cfg.ordersBaseUrl; }, fetchFn: function (u, i) { return fetch(u, i); }, machineId: function () { return id; } });
  window.vungBai = {
    version: cfg.version || 'phuhuynh', platform: 'android', role: 'parent', machineId: id,
    progressView: function (x) { return client.progressView(x); },
    progressSettings: function (x) { return client.progressSettings(x); },
    storeAll: function () { return {}; }, storeSet: function () {},
  };
  window.NLNotify = (function () {
    var cap = window.Capacitor; var LN = null;
    try { LN = cap && cap.Plugins && cap.Plugins.LocalNotifications; } catch (e) { LN = null; }
    if (!LN) return null;
    return {
      request: function () { return LN.requestPermissions().then(function (r) { return r.display === 'granted'; }); },
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
})();
