// Dựng đối tượng window.vungBai cho điện thoại, cùng các hàm với main/preload.js (Windows).
// Mọi phụ thuộc (lưu trữ, mạng, thư viện chữ ký, mã thiết bị) được truyền vào để kiểm thử bằng Node.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./license.js'), require('./api.js'), require('./content.js'), require('./heartbeat.js'), require('./machine.js'), require('./packs.js'));
  else root.NLMobileBridge = factory(root.NLMobileLicense, root.NLMobileApi, root.NLMobileContent, root.NLMobileHeartbeat, root.NLMobileMachine, root.NLMobilePacks);
})(typeof self !== 'undefined' ? self : this, function (License, Api, Content, Heartbeat, Machine, Packs) {
  'use strict';
  var USER_PREFIX = 'nl-userstore:';

  // o: { nacl, publicKey: Uint8Array(32), storage:{get,set}, rawDeviceId, fetchFn, fetchText, product, config:{ordersBaseUrl,version,commit}, userStore?:{all,set}, setTimeoutFn?, setIntervalFn? }
  function create(o) {
    var machineId = Machine.machineIdFrom(o.rawDeviceId, o.nacl);
    var verify = function (msg, sig) { return sig.length === 64 && o.nacl.sign.detached.verify(msg, sig, o.publicKey); };
    var lic = License.create({ storage: o.storage, machineId: machineId, verify: verify });
    var client = Api.makeClient({ baseUrl: function () { return o.config.ordersBaseUrl; }, fetchFn: o.fetchFn, machineId: function () { return machineId; } });
    var listeners = [];
    var packListeners = [];
    // Bản build mới chỉ giữ mục lục và 2 bài học thử trong apk; bài còn lại đọc từ gói đã tải (o.packs: { enabled, store, subtle, gunzip }).
    var packsCfg = o.packs || {};
    var packs = Packs.create({ client: client, lic: lic, baseUrl: function () { return o.config.ordersBaseUrl; }, fetchFn: o.fetchFn, store: packsCfg.store, subtle: packsCfg.subtle, gunzip: packsCfg.gunzip, enabled: !!packsCfg.enabled,
      send: function (st) { packListeners.slice().forEach(function (cb) { try { cb(st); } catch (e) { /* bỏ qua */ } }); } });
    var contentBase = o.contentBase || 'content/';
    var fetchContent = function (url) {
      return o.fetchText(url).catch(function (err) {
        if (!packs.enabled || url.indexOf(contentBase) !== 0) throw err;
        return packs.read(url.slice(contentBase.length)).then(function (t) { if (typeof t === 'string') return t; throw new Error('NOT_DOWNLOADED'); });
      });
    };
    var content = Content.create({ fetchText: fetchContent, subjects: o.product.subjects, base: contentBase });
    var heartbeat = Heartbeat.create({ lic: lic, client: client, version: o.config.version, intervalMs: o.intervalMs, setTimeoutFn: o.setTimeoutFn, setIntervalFn: o.setIntervalFn,
      onChange: function () { listeners.slice().forEach(function (cb) { try { cb(); } catch (e) { /* bỏ qua */ } }); } });
    var off = { state: 'off' };
    var up = o.updater || null;
    var userStore = o.userStore || { all: function () { return {}; }, set: function () {} };

    function afterActivate(license) {
      heartbeat.beat().catch(function () {});
      if (license && license.status === 'ok') packs.sync(); // tự tải nội dung các lớp vừa kích hoạt
      return license;
    }

    var api = {
      version: o.config.version || 'android',
      platform: 'android',
      machineId: machineId,
      loadManifest: function (subject) {
        return content.loadManifest(subject).then(function (m) { return lic.annotateManifest(lic.currentLicense(), subject, m); });
      },
      loadLesson: function (relPath) {
        var parts = String(relPath).split('/');
        var subject = parts[0];
        // Chặn ở lớp cầu nối: bài bị khóa thì không trả nội dung dù giao diện bị chỉnh sửa.
        return content.loadManifest(subject).then(function (m) {
          if (!lic.canOpen(lic.currentLicense(), subject, m, parts.slice(1).join('/'))) throw new Error('LOCKED');
          return content.loadLesson(relPath);
        });
      },
      appInfo: function () { return Promise.resolve({ version: o.config.version || 'dev', commit: o.config.commit || 'local' }); },
      productInfo: function () { return Promise.resolve({ id: o.product.id, title: o.product.title, grades: o.product.grades, subjects: o.product.subjects }); },
      loadLicense: function () { return Promise.resolve(lic.currentLicense()); },
      activateLicense: function (key) { return Promise.resolve(afterActivate(lic.activate(key))); },
      removeLicense: function () { lic.deactivate(); return Promise.resolve(lic.currentLicense()); },
      createOrder: function (order) { return client.createOrder(order); },
      pinReset: function (x) { return client.pinReset(x); },
      orderStatus: function (code) { return client.orderStatus(code); },
      progressSettings: function (x) { return client.progressSettings(x); },
      progressPush: function (x) { return client.progressPush(x); },
      progressView: function (x) { return client.progressView(x); },
      // Nhận khóa cho điện thoại này từ đơn mua ở thiết bị khác (mã đơn + số điện thoại), rồi kích hoạt luôn.
      claimDevice: function (x) {
        return client.claimDevice(x).then(function (r) {
          if (r.ok && r.data && r.data.key) r.license = afterActivate(lic.activate(r.data.key));
          return r;
        });
      },
      // Nhận khóa các đơn phụ huynh mua cho gia đình (mã gia đình nhập một lần) và kích hoạt từng khóa.
      familySync: function (x) {
        return client.familySync(x).then(function (r) {
          if (!r.ok) return r;
          var keys = Array.isArray(r.data && r.data.keys) ? r.data.keys : [];
          var activated = 0;
          keys.forEach(function (k) { if (k && afterActivate(lic.activate(k.key)).status === 'ok') activated++; });
          return { ok: true, activated: activated, total: keys.length, full: (r.data && r.data.full) || 0 };
        });
      },
      // Cập nhật: o.updater (mobile/bridge/updater.js) lo gói nội dung và apk mới; không có thì tắt (chạy thử trên trình duyệt).
      updateStatus: function () { return Promise.resolve(up ? up.status() : off); },
      checkUpdate: function () { return up ? up.check() : Promise.resolve(off); },
      downloadUpdate: function () { return up ? up.download() : Promise.resolve(off); },
      installUpdate: function () { return up ? up.install() : Promise.resolve(false); },
      onUpdate: function (cb) { if (up) up.onUpdate(cb); },
      onLicenseChanged: function (cb) { listeners.push(cb); },
      packsStatus: function () { return packs.status(); },
      packsSync: function () { return packs.sync(); },
      onPacks: function (cb) { packListeners.push(cb); },
      storeAll: function () { try { return userStore.all() || {}; } catch (e) { return {}; } },
      storeSet: function (k, v) { try { userStore.set(String(k), v); } catch (e) { /* bỏ qua */ } },
    };
    return { api: api, heartbeat: heartbeat, license: lic, client: client, updater: up, packs: packs };
  }

  // Bản sao dữ liệu người dùng (PIN, tiến độ...) lưu song song với localStorage, để khôi phục khi localStorage bị xóa.
  // setRaw/getRaw phải là hàm gốc của Storage (không phải hàm đã bị persist-shim.js bọc) để không gọi vòng lại.
  function mirrorUserStore(ls, getRaw, setRaw, removeRaw) {
    return {
      all: function () {
        var out = {};
        for (var i = 0; i < ls.length; i++) {
          var k = ls.key(i);
          if (k && k.indexOf(USER_PREFIX) === 0) out[k.slice(USER_PREFIX.length)] = getRaw.call(ls, k);
        }
        return out;
      },
      set: function (k, v) {
        if (!k || k.length > 200) return;
        if (v === null || v === undefined) removeRaw.call(ls, USER_PREFIX + k);
        else if (String(v).length <= 4 * 1024 * 1024) setRaw.call(ls, USER_PREFIX + k, String(v));
      },
    };
  }

  return { create: create, mirrorUserStore: mirrorUserStore, USER_PREFIX: USER_PREFIX };
});
