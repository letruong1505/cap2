// Gọi máy chủ đơn hàng (Cloudflare Worker) từ điện thoại. Cùng quy tắc với main/orders.js: lỗi mạng hoặc máy chủ 5xx thì trả offline.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobileApi = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var PLATFORM = 'android';

  function makeClient(o) {
    var baseUrl = o.baseUrl; var fetchFn = o.fetchFn; var machineId = o.machineId;
    var timeoutMs = o.timeoutMs || 10000;

    function call(method, route, body) {
      var base = String(baseUrl() || '').replace(/\/+$/, '');
      if (!base) return Promise.resolve({ ok: false, offline: true });
      var ctl = typeof AbortController === 'function' ? new AbortController() : null;
      var timer = ctl ? setTimeout(function () { ctl.abort(); }, timeoutMs) : null;
      return fetchFn(base + route, { method: method, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined, signal: ctl ? ctl.signal : undefined })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (data) {
            if (r.ok) return { ok: true, data: data };
            if (r.status >= 500) return { ok: false, offline: true };
            return { ok: false, error: data.error || 'Không xử lý được yêu cầu.' };
          });
        })
        .catch(function () { return { ok: false, offline: true }; })
        .then(function (res) { if (timer) clearTimeout(timer); return res; });
    }
    var s = function (v) { return String(v == null ? '' : v); };
    return {
      createOrder: function (x) {
        x = x || {};
        return call('POST', '/api/orders', {
          name: s(x.name), phone: s(x.phone), ids: Array.isArray(x.ids) ? x.ids.map(String) : [],
          partnerCode: s(x.partnerCode).trim().slice(0, 20),
          terms: { version: s(x.terms && x.terms.version), at: s(x.terms && x.terms.at) }, machineId: machineId(), platform: PLATFORM,
        });
      },
      pinReset: function (x) { x = x || {}; return call('POST', '/api/pin-reset', { phone: s(x.phone), code: s(x.code), machineId: machineId() }); },
      // Nhận khóa cho thiết bị này từ một đơn đã mua trên thiết bị khác: nhập mã đơn + số điện thoại đã mua.
      claimDevice: function (x) { x = x || {}; return call('POST', '/api/claim-device', { phone: s(x.phone), code: s(x.code), machineId: machineId(), platform: PLATFORM }); },
      ping: function (x) { x = x || {}; return call('POST', '/api/ping', { machineId: machineId(), ids: Array.isArray(x.ids) ? x.ids.map(String) : [], version: s(x.version) }); },
      orderStatus: function (code) { return call('GET', '/api/orders/' + encodeURIComponent(s(code).slice(0, 6)) + '/status?machine=' + encodeURIComponent(machineId())); },
    };
  }
  return { makeClient: makeClient, PLATFORM: PLATFORM };
});
