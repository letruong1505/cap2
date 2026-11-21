// Cập nhật ứng dụng Android. Hai đường:
//  1) Gói nội dung (OTA): tải gói đã ký từ máy chủ, kiểm tra chữ ký, lưu lại; lần mở sau trang khởi động sẽ dùng gói này.
//  2) Apk mới: khi thay đổi nằm ngoài phần giao diện (hoặc gói OTA không dùng được) thì báo có bản mới và tải apk ngay trong app rồi mở hộp cài đặt của Android (không có plugin thì mở địa chỉ tải).
// Trạng thái dùng cùng giao thức với bản Windows (idle/checking/available/downloading/ready/none/error) để dùng chung thanh thông báo.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobileUpdater = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var PREFIX = 'NLO1-';
  var AUTO_EVERY_MS = 6 * 3600 * 1000;
  var MAX_CHARS = 12 * 1024 * 1024;

  function create(o) {
    var state = { state: 'idle', version: '', notes: '', percent: 0, error: '' };
    var listeners = []; var busy = false; var apkUrl = '';
    var now = o.now || function () { return Date.now(); };
    var timeoutMs = o.timeoutMs || 20000;

    function snap() { return { state: state.state, version: state.version, notes: state.notes, percent: state.percent, error: state.error }; }
    function set(p) { for (var k in p) state[k] = p[k]; var s = snap(); listeners.forEach(function (cb) { try { cb(s); } catch (e) { /* bỏ qua */ } }); return s; }
    function base() { return String(o.baseUrl() || '').replace(/\/+$/, ''); }

    function get(route, asText, ms) {
      var ctl = typeof AbortController === 'function' ? new AbortController() : null;
      var timer = ctl ? setTimeout(function () { ctl.abort(); }, ms || timeoutMs) : null;
      return o.fetchFn(base() + route, { signal: ctl ? ctl.signal : undefined }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return asText ? r.text() : r.json();
      }).then(function (x) { if (timer) clearTimeout(timer); return x; }, function (e) { if (timer) clearTimeout(timer); throw e; });
    }

    // Kiểm tra gói: đúng định dạng, đúng chữ ký OTA, đúng số build và có đủ trường cần thiết.
    function verify(text, build) {
      var s = String(text || '').trim();
      if (s.length > MAX_CHARS || s.indexOf(PREFIX) !== 0) throw new Error('Gói cập nhật không hợp lệ.');
      var parts = s.slice(PREFIX.length).split('.');
      if (parts.length !== 2 || !parts[0] || !parts[1]) throw new Error('Gói cập nhật hỏng.');
      var payload = o.b64uToBytes(parts[0]); var sig = o.b64uToBytes(parts[1]);
      if (!o.nacl.sign.detached.verify(payload, sig, o.otaPublicKey)) throw new Error('Chữ ký gói cập nhật không đúng.');
      var p = JSON.parse(new TextDecoder().decode(payload));
      if (p.v !== 1 || p.build !== build || typeof p.html !== 'string' || !p.files || typeof p.files !== 'object' || typeof p.version !== 'string' || typeof p.minNative !== 'number') throw new Error('Gói cập nhật thiếu thông tin.');
      for (var k in p.files) if (typeof p.files[k] !== 'string') throw new Error('Gói cập nhật hỏng.');
      return p;
    }

    function effectiveBuild(cur) {
      var usable = cur && cur.build > o.native.code && o.native.code >= (cur.minNative || 0);
      return { stored: usable ? cur.build : 0, effective: Math.max(o.native.code, usable ? cur.build : 0) };
    }

    function downloadOta(latest, target) {
      set({ state: 'downloading', percent: 10, error: '' });
      return get('/api/app/android/ota/' + target, true, 60000).then(function (text) {
        set({ percent: 70 });
        var p = verify(text, target);
        return o.store.set('current', { build: p.build, version: p.version, minNative: p.minNative, html: p.html, files: p.files, tries: 0 }).then(function () {
          return set({ state: 'ready', version: p.version, notes: latest.notes || '', percent: 100 });
        });
      });
    }

    function decide(latest) {
      return Promise.all([o.store.get('current'), o.store.get('bad')]).then(function (r) {
        var bad = Array.isArray(r[1]) ? r[1] : [];
        var b = effectiveBuild(r[0]);
        var running = o.runningBuild ? o.runningBuild() : o.native.code;
        var target = latest.otaBuild | 0;
        var canOta = target > b.effective && o.native.code >= (latest.minNative | 0) && bad.indexOf(target) < 0;
        if (canOta) return downloadOta(latest, target);
        if ((latest.versionCode | 0) > b.effective) {
          apkUrl = latest.apkUrl || '';
          return set({ state: 'available', version: latest.version || String(latest.versionCode), notes: latest.notes || '', error: '' });
        }
        if (b.stored > running) return set({ state: 'ready', version: r[0].version || '', notes: latest.notes || '', percent: 100, error: '' }); // đã tải trước đó, chưa dùng
        return set({ state: 'none', error: '' });
      });
    }

    return {
      status: function () { return snap(); },
      onUpdate: function (cb) { listeners.push(cb); },
      // opts.auto: kiểm tra ngầm, tối đa mỗi 6 giờ một lần, lỗi thì im lặng.
      check: function (opts) {
        var auto = !!(opts && opts.auto);
        if (busy || state.state === 'downloading') return Promise.resolve(snap());
        if (auto) {
          var last = 0;
          try { last = parseInt(o.storage.get('nl-update-last') || '0', 10) || 0; } catch (e) { /* bỏ qua */ }
          if (now() - last < AUTO_EVERY_MS) return Promise.resolve(snap());
        } else if (state.state !== 'ready') set({ state: 'checking', error: '' });
        busy = true;
        return get('/api/app/android/latest', false).then(function (latest) {
          try { o.storage.set('nl-update-last', String(now())); } catch (e) { /* bỏ qua */ }
          if (state.state === 'ready') return snap(); // đã có gói chờ dùng
          return decide(latest);
        }).catch(function (e) {
          return auto ? set({ state: state.state === 'checking' ? 'idle' : state.state }) : set({ state: 'error', error: String(e && e.message || e).slice(0, 200) });
        }).then(function (s) { busy = false; return s; });
      },
      // Với apk mới: mở địa chỉ tải; Android sẽ hỏi cài đặt như mọi ứng dụng tải ngoài CH Play.
      download: function () {
        if (state.state !== 'available' || !apkUrl) return Promise.resolve(snap());
        var url = apkUrl;
        var viaBrowser = function () { try { o.openUrl(url); } catch (e) { /* bỏ qua */ } };
        if (!o.installApk) { viaBrowser(); return Promise.resolve(snap()); }
        // Tải ngay trong app rồi mở hộp cài đặt; lỗi bất kỳ (trừ chưa cấp quyền) thì quay về cách mở trình duyệt.
        set({ state: 'downloading', percent: 0, error: '' });
        return o.installApk(url, function (p) { set({ state: 'downloading', percent: p }); }).then(function () {
          return set({ state: 'available', error: '' });
        }, function (e) {
          if (e && e.code === 'needs_permission') return set({ state: 'available', error: 'Hãy bật "Cho phép từ nguồn này" rồi quay lại app và bấm Tải về lần nữa.' });
          viaBrowser();
          return set({ state: 'available', error: '' });
        });
      },
      // Dùng ngay gói OTA đã tải: nạp lại từ trang khởi động.
      install: function () {
        if (state.state !== 'ready') return Promise.resolve(false);
        try { o.reload(); } catch (e) { return Promise.resolve(false); }
        return Promise.resolve(true);
      },
    };
  }

  return { create: create, PREFIX: PREFIX };
});
