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
          partnerCode: s(x.partnerCode).trim().slice(0, 20), family: x.family ? s(x.family).slice(0, 12) : undefined,
          terms: { version: s(x.terms && x.terms.version), at: s(x.terms && x.terms.at) }, machineId: machineId(), platform: PLATFORM,
        });
      },
      // Phụ huynh xin mã gia đình (app Phụ huynh); máy của con gọi familySync để nhận khóa các đơn phụ huynh mua cho gia đình.
      familyCreate: function (x) { x = x || {}; return call('POST', '/api/family/create', { phone: s(x.phone), machineId: machineId() }); },
      familySync: function (x) { x = x || {}; return call('POST', '/api/family/sync', { fcode: s(x.fcode), machineId: machineId(), platform: PLATFORM }); },
      pinReset: function (x) { x = x || {}; return call('POST', '/api/pin-reset', { phone: s(x.phone), code: s(x.code), machineId: machineId() }); },
      // Nhận khóa cho thiết bị này từ một đơn đã mua trên thiết bị khác: nhập mã đơn + số điện thoại đã mua.
      claimDevice: function (x) { x = x || {}; return call('POST', '/api/claim-device', { phone: s(x.phone), code: s(x.code), machineId: machineId(), platform: PLATFORM }); },
      progressSettings: function (x) { x = x || {}; return call('POST', '/api/progress/settings', { code: s(x.code), machineId: machineId(), enabled: typeof x.enabled === 'boolean' ? x.enabled : undefined, purge: x.purge === true ? true : undefined, goals: x.goals && typeof x.goals === 'object' ? { daily: Number(x.goals.daily), weekend: Number(x.goals.weekend), weekly: Number(x.goals.weekly), pass: Number(x.goals.pass) || undefined, passBy: x.goals.passBy && typeof x.goals.passBy === 'object' ? x.goals.passBy : undefined } : undefined, reward: x && x.reward && typeof x.reward === 'object' ? x.reward : undefined, timetable: x && x.timetable && typeof x.timetable === 'object' ? x.timetable : undefined, orientation: x && Array.isArray(x.orientation) ? x.orientation.slice(0, 3).map(String) : undefined, quiz: x && Array.isArray(x.quiz) ? x.quiz.slice(0, 5).map((q) => ({ id: String(q && q.id), p: Number(q && q.p) })) : undefined }); },
      progressPush: function (x) { x = x || {}; return call('POST', '/api/progress/push', { code: s(x.code), machineId: machineId(), days: Array.isArray(x.days) ? x.days : [], usage: Array.isArray(x.usage) ? x.usage.slice(0, 400) : [] }); },
      progressView: function (x) { x = x || {}; return call('POST', '/api/progress/view', { code: s(x.code), phone: s(x.phone), machineId: machineId(), from: s(x.from), to: s(x.to), grade: Number(x.grade) || 0 }); },
      // Xin khoá giải mã gói nội dung các lớp đang có bản quyền (khớp main/orders.js).
      packKeys: function (x) { x = x || {}; return call('POST', '/api/pack/keys', { machineId: machineId(), keys: Array.isArray(x.keys) ? x.keys.slice(0, 10).map(String) : [] }); },
      ping: function (x) { x = x || {}; return call('POST', '/api/ping', { machineId: machineId(), ids: Array.isArray(x.ids) ? x.ids.map(String) : [], version: s(x.version) }); },
      orderStatus: function (code) { return call('GET', '/api/orders/' + encodeURIComponent(s(code).slice(0, 6)) + '/status?machine=' + encodeURIComponent(machineId())); },
    };
  }
  return { makeClient: makeClient, PLATFORM: PLATFORM };
});
