// Kho gói nội dung khóa học trên điện thoại: tải theo lớp đã có bản quyền, lưu trong IndexedDB, đọc offline.
// Cùng định dạng và cùng quy tắc với main/pack-store.js (Windows); giải mã bằng WebCrypto (AES-256-GCM) và giải nén gzip.
// Gói lấy qua máy chủ đơn hàng (Worker chuyển tiếp từ R2) để WebView không vướng CORS.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobilePacks = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var MAX_PACK_BYTES = 40 * 1024 * 1024;
  var MAGIC = [0x4e, 0x4c, 0x50, 0x31]; // "NLP1"

  function b64ToBytes(b64) {
    var bin = atob(String(b64));
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); }
  var gradeOf = function (rel) { var m = String(rel).split('/')[0].match(/(\d+)$/); return m ? Number(m[1]) : NaN; };

  // IndexedDB của WebView: kho khóa-giá trị riêng cho gói (khác kho OTA).
  function idbStore(indexedDB) {
    var DB = 'nl-packs'; var STORE = 'kv';
    function open() {
      return new Promise(function (resolve, reject) {
        if (!indexedDB) { reject(new Error('Không có IndexedDB')); return; }
        var req = indexedDB.open(DB, 1);
        req.onupgradeneeded = function () { req.result.createObjectStore(STORE); };
        req.onsuccess = function () { resolve(req.result); };
        req.onerror = function () { reject(req.error || new Error('Không mở được kho')); };
      });
    }
    function run(mode, fn) {
      return open().then(function (db) {
        return new Promise(function (resolve, reject) {
          var tx = db.transaction(STORE, mode); var out;
          tx.oncomplete = function () { db.close(); resolve(out); };
          tx.onerror = tx.onabort = function () { db.close(); reject(tx.error || new Error('Lỗi kho')); };
          fn(tx.objectStore(STORE), function (v) { out = v; });
        });
      });
    }
    return {
      get: function (k) { return run('readonly', function (s, ret) { var r = s.get(k); r.onsuccess = function () { ret(r.result === undefined ? null : r.result); }; }); },
      set: function (k, v) { return run('readwrite', function (s) { s.put(v, k); }); },
      remove: function (k) { return run('readwrite', function (s) { s.delete(k); }); },
    };
  }

  function gunzipBrowser(bytes) {
    var stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
    return new Response(stream).arrayBuffer().then(function (b) { return new Uint8Array(b); });
  }

  // o: { client, lic, baseUrl(), fetchFn, store:{get,set,remove}, subtle, gunzip(bytes)->Promise<Uint8Array>, enabled, send(status) }
  function create(o) {
    var enabled = !!o.enabled;
    var subtle = o.subtle; var gunzip = o.gunzip || gunzipBrowser; var fetchFn = o.fetchFn; var store = o.store;
    var send = o.send || function () {};
    var cache = {}; // lớp -> { sha, files }
    var have = []; // các lớp đã có gói trên máy
    var status = { state: 'idle', grades: [], enabled: enabled };
    var busy = null;
    var loaded = enabled ? store.get('state').then(function (st) { have = Object.keys((st && st.grades) || {}).map(Number).sort(function (a, b) { return a - b; }); status.grades = have.slice(); }).catch(function () {}) : Promise.resolve();

    function setStatus(patch) {
      Object.keys(patch).forEach(function (k) { status[k] = patch[k]; });
      status.enabled = enabled; status.grades = have.slice();
      try { send(JSON.parse(JSON.stringify(status))); } catch (e) { /* bỏ qua */ }
    }

    function decrypt(bytes, keyB64) {
      if (bytes.length < 33 || MAGIC.some(function (m, i) { return bytes[i] !== m; })) return Promise.reject(new Error('Gói nội dung không hợp lệ'));
      var iv = bytes.subarray(4, 16); var tag = bytes.subarray(16, 32); var ct = bytes.subarray(32);
      var joined = new Uint8Array(ct.length + tag.length); joined.set(ct, 0); joined.set(tag, ct.length); // WebCrypto đặt tag sau dữ liệu
      return subtle.importKey('raw', b64ToBytes(keyB64), 'AES-GCM', false, ['decrypt'])
        .then(function (k) { return subtle.decrypt({ name: 'AES-GCM', iv: iv }, k, joined); })
        .then(function (plain) { return gunzip(new Uint8Array(plain)); })
        .then(function (raw) {
          var j = JSON.parse(new TextDecoder().decode(raw));
          if (!j || j.v !== 1 || typeof j.files !== 'object') throw new Error('Gói nội dung không hợp lệ');
          return j.files;
        });
    }

    function loadGrade(grade) {
      return store.get('state').then(function (st) {
        var ent = st && st.grades && st.grades[grade];
        if (!ent) return null;
        if (cache[grade] && cache[grade].sha === ent.sha256) return cache[grade].files;
        return store.get('data:' + grade).then(function (data) {
          if (!data) return null;
          return decrypt(new Uint8Array(data), ent.key).then(function (files) { cache[grade] = { sha: ent.sha256, files: files }; return files; });
        });
      }).catch(function () { return null; });
    }

    // Đọc một file nội dung dạng "<môn>/<đường dẫn>"; null nếu chưa tải.
    function read(rel) {
      if (!enabled) return Promise.resolve(null);
      return loaded.then(function () { return loadGrade(gradeOf(rel)); }).then(function (files) { return files && typeof files[rel] === 'string' ? files[rel] : null; });
    }

    function getBytes(url) {
      return fetchFn(url).then(function (r) {
        if (!r.ok) throw new Error('http ' + r.status);
        return r.arrayBuffer();
      }).then(function (b) { if (b.byteLength > MAX_PACK_BYTES) throw new Error('gói quá lớn'); return new Uint8Array(b); });
    }

    function run() {
      var keys = o.lic.rawKeys();
      if (!keys.length) { setStatus({ state: 'idle', error: '' }); return Promise.resolve({ ok: true, downloaded: 0 }); }
      var base = String(o.baseUrl() || '').replace(/\/+$/, '');
      return o.client.packKeys({ keys: keys }).then(function (kr) {
        if (!kr.ok) { setStatus({ state: kr.offline ? 'offline' : 'error', error: kr.error || '' }); return { ok: false, offline: !!kr.offline, error: kr.error }; }
        var granted = kr.data.keys || {};
        var grades = Object.keys(granted).map(Number).sort(function (a, b) { return a - b; });
        return fetchFn(base + '/api/pack/index').then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); }).then(function (idx) {
          return store.get('state').then(function (st) {
            st = st && st.grades ? st : { grades: {} };
            var todo = grades.filter(function (g) { var p = idx.packs && idx.packs[g]; return p && (!st.grades[g] || st.grades[g].sha256 !== p.sha256 || st.grades[g].key !== granted[g]); });
            var downloaded = 0;
            var chain = Promise.resolve({ ok: true });
            todo.forEach(function (g, i) {
              chain = chain.then(function (prev) {
                if (!prev.ok) return prev;
                var p = idx.packs[g];
                if (!/^lop\d{1,2}-[0-9a-f]{10}\.nlp$/.test(String(p.file))) return prev;
                setStatus({ state: 'downloading', grade: g, done: i, total: todo.length, error: '' });
                return getBytes(base + '/api/pack/file/' + p.file).then(function (bytes) {
                  return subtle.digest('SHA-256', bytes).then(function (d) {
                    if (hex(d) !== p.sha256) throw new Error('sai mã kiểm tra');
                    return decrypt(bytes, granted[g]); // kiểm tra giải mã được trước khi lưu
                  }).then(function (files) {
                    return store.set('data:' + g, bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)).then(function () {
                      return store.get('state');
                    }).then(function (cur) {
                      cur = cur && cur.grades ? cur : { grades: {} };
                      cur.grades[g] = { file: p.file, sha256: p.sha256, key: granted[g] };
                      return store.set('state', cur);
                    }).then(function () {
                      cache[g] = { sha: p.sha256, files: files };
                      if (have.indexOf(g) < 0) have.push(g);
                      have.sort(function (a, b) { return a - b; });
                      downloaded++;
                      return { ok: true };
                    });
                  });
                }).catch(function (e) {
                  setStatus({ state: 'error', grade: g, error: 'Không tải được nội dung lớp ' + g + '. Kiểm tra mạng rồi thử lại.' });
                  return { ok: false, downloaded: downloaded, error: String(e && e.message) };
                });
              });
            });
            return chain.then(function (res) {
              if (!res.ok) return res;
              setStatus({ state: 'ready', done: todo.length, total: todo.length, grade: 0, error: '' });
              return { ok: true, downloaded: downloaded, grades: grades };
            });
          });
        }, function () { setStatus({ state: 'offline', error: '' }); return { ok: false, offline: true }; });
      });
    }

    function sync() {
      if (!enabled) return Promise.resolve({ ok: true, disabled: true });
      if (busy) return busy;
      busy = loaded.then(run).catch(function (e) { setStatus({ state: 'error', error: 'Lỗi tải nội dung: ' + String(e && e.message) }); return { ok: false, error: String(e && e.message) }; })
        .then(function (r) { busy = null; return r; });
      return busy;
    }

    // Mở app: tải bù các lớp đã có bản quyền mà chưa có nội dung, rồi kiểm tra lại mỗi 6 giờ.
    function start(setTimeoutFn, setIntervalFn) {
      if (!enabled) return;
      (setTimeoutFn || setTimeout)(function () { sync(); }, 4000);
      (setIntervalFn || setInterval)(function () { sync(); }, 6 * 60 * 60 * 1000);
    }

    return { read: read, sync: sync, start: start, enabled: enabled, status: function () { return loaded.then(function () { return JSON.parse(JSON.stringify(Object.assign({}, status, { enabled: enabled, grades: have.slice() }))); }); } };
  }

  return { create: create, idbStore: idbStore, gunzipBrowser: gunzipBrowser };
});
