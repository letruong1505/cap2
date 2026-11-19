// Tín hiệu định kỳ về máy chủ khi app đang mở, giống main/heartbeat.js. Chỉ gửi mã máy, mã đơn và số bản.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobileHeartbeat = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var INTERVAL_MS = 5 * 60 * 1000;
  function create(o) {
    var timer = null;
    var interval = o.intervalMs || INTERVAL_MS;
    var setIntervalFn = o.setIntervalFn || setInterval; var setTimeoutFn = o.setTimeoutFn || setTimeout;
    function beat() {
      var ids = o.lic.pingCodes();
      if (!ids.length) return Promise.resolve({ sent: false });
      return o.client.ping({ ids: ids, version: o.version }).then(function (r) {
        if (!r.ok) return { sent: true, ok: false };
        var changed = Array.isArray(r.data && r.data.revoked) ? o.lic.setRevoked(r.data.revoked, r.data.revokedItems) : false;
        if (changed) { try { (o.onChange || function () {})(); } catch (e) { /* bỏ qua */ } }
        return { sent: true, ok: true, changed: changed };
      });
    }
    function start() {
      if (timer) return;
      setTimeoutFn(function () { beat().catch(function () {}); }, 8000);
      timer = setIntervalFn(function () { beat().catch(function () {}); }, interval);
      // Quay lại app từ nền: gửi tín hiệu ngay để nhận thu hồi sớm.
      if (typeof document !== 'undefined' && document.addEventListener) document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') beat().catch(function () {}); });
    }
    return { beat: beat, start: start };
  }
  return { create: create, INTERVAL_MS: INTERVAL_MS };
});
