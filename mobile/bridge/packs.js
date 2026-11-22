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
    var cache = {}; // 'g7' | 'c:gia-su-ai' -> { sha, files }
    var have = []; // các lớp đã có gói trên máy
    var haveCourses = []; // các khóa Kỹ năng đã có gói
    var status = { state: 'idle', grades: [], courses: [], enabled: enabled };
    var busy = null;
    var loaded = enabled ? store.get('state').then(function (st) { have = Object.keys((st && st.grades) || {}).map(Number).sort(function (a, b) { return a - b; }); haveCourses = Object.keys((st && st.courses) || {}).sort(); status.grades = have.slice(); status.courses = haveCourses.slice(); }).catch(function () {}) : Promise.resolve();

    function setStatus(patch) {
      Object.keys(patch).forEach(function (k) { status[k] = patch[k]; });
      status.enabled = enabled; status.grades = have.slice(); status.courses = haveCourses.slice();
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

    // kind: 'grades' (gói theo lớp) hoặc 'courses' (gói khóa Kỹ năng); id là số lớp hoặc mã khóa.
    function loadUnit(kind, id) {
      return store.get('state').then(function (st) {
        var ent = st && st[kind] && st[kind][id];
        if (!ent) return null;
        var ck = (kind === 'grades' ? 'g' : 'c:') + id;
        if (cache[ck] && cache[ck].sha === ent.sha256) return cache[ck].files;
        return store.get('data:' + ck).then(function (data) {
          if (!data) return null;
          return decrypt(new Uint8Array(data), ent.key).then(function (files) { cache[ck] = { sha: ent.sha256, files: files }; return files; });
        });
      }).catch(function () { return null; });
    }

    // Đọc một file nội dung dạng "<môn>/<đường dẫn>"; null nếu chưa tải.
    function read(rel) {
      if (!enabled) return Promise.resolve(null);
      return loaded.then(function () { return loadUnit('grades', gradeOf(rel)); }).then(function (files) { return files && typeof files[rel] === 'string' ? files[rel] : null; });
    }

    // Nội dung khóa Kỹ năng: { "TUDUY.k1218": "<json các bài>", ... }; null nếu chưa tải.
    function readCourse(id) {
      if (!enabled) return Promise.resolve(null);
      return loaded.then(function () { return loadUnit('courses', String(id)); });
    }

    function getBytes(url, onBytes) {
      return fetchFn(url).then(function (r) {
        if (!r.ok) throw new Error('http ' + r.status);
        if (onBytes && r.body && typeof r.body.getReader === 'function') {
          var rd = r.body.getReader(); var parts = []; var n = 0;
          var pump = function () {
            return rd.read().then(function (x) {
              if (x.done) return;
              parts.push(x.value); n += x.value.length;
              if (n > MAX_PACK_BYTES) throw new Error('gói quá lớn');
              onBytes(n); return pump();
            });
          };
          return pump().then(function () { var out = new Uint8Array(n); var at = 0; parts.forEach(function (c) { out.set(c, at); at += c.length; }); return out.buffer; });
        }
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
        var grantedCourses = kr.data.courses || {};
        var units = Object.keys(granted).map(Number).sort(function (a, b) { return a - b; }).map(function (g) { return { kind: 'grades', id: g, key: granted[g], label: 'lớp ' + g }; })
          .concat(Object.keys(grantedCourses).sort().map(function (c) { return { kind: 'courses', id: c, key: grantedCourses[c], label: 'khóa ' + c }; }));
        return fetchFn(base + '/api/pack/index').then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); }).then(function (idx) {
          return store.get('state').then(function (st) {
            st = st || {}; st.grades = st.grades || {}; st.courses = st.courses || {};
            var pOf = function (u) { return u.kind === 'grades' ? (idx.packs && idx.packs[u.id]) : (idx.courses && idx.courses[u.id]); };
            var todo = units.filter(function (u) { var p = pOf(u); return p && (!st[u.kind][u.id] || st[u.kind][u.id].sha256 !== p.sha256 || st[u.kind][u.id].key !== u.key); });
            var downloaded = 0;
            var bytesTotal = todo.reduce(function (a, u) { return a + (Number(pOf(u).size) || 0); }, 0) || 1;
            var bytesBefore = 0; var lastEmit = 0;
            var pct = function (extra) { return Math.min(99, Math.floor(((bytesBefore + extra) / bytesTotal) * 100)); };
            var chain = Promise.resolve({ ok: true });
            todo.forEach(function (u, i) {
              chain = chain.then(function (prev) {
                if (!prev.ok) return prev;
                var p = pOf(u); var ck = (u.kind === 'grades' ? 'g' : 'c:') + u.id;
                if (!/^(lop\d{1,2}|course-[a-z0-9-]{1,60})-[0-9a-f]{10}\.nlp$/.test(String(p.file))) return prev;
                setStatus({ state: 'downloading', grade: u.kind === 'grades' ? u.id : 0, course: u.kind === 'courses' ? u.id : '', done: i, total: todo.length, percent: pct(0), error: '' });
                return getBytes(base + '/api/pack/file/' + p.file, function (n) { var t = Date.now(); if (t - lastEmit > 150) { lastEmit = t; setStatus({ percent: pct(n) }); } }).then(function (bytes) {
                  bytesBefore += Number(p.size) || bytes.length;
                  return subtle.digest('SHA-256', bytes).then(function (d) {
                    if (hex(d) !== p.sha256) throw new Error('sai mã kiểm tra');
                    return decrypt(bytes, u.key); // kiểm tra giải mã được trước khi lưu
                  }).then(function (files) {
                    return store.set('data:' + ck, bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)).then(function () {
                      return store.get('state');
                    }).then(function (cur) {
                      cur = cur || {}; cur.grades = cur.grades || {}; cur.courses = cur.courses || {};
                      cur[u.kind][u.id] = { file: p.file, sha256: p.sha256, key: u.key };
                      return store.set('state', cur);
                    }).then(function () {
                      cache[ck] = { sha: p.sha256, files: files };
                      if (u.kind === 'grades') { if (have.indexOf(u.id) < 0) have.push(u.id); have.sort(function (a, b) { return a - b; }); }
                      else { if (haveCourses.indexOf(u.id) < 0) haveCourses.push(u.id); haveCourses.sort(); }
                      downloaded++;
                      return { ok: true };
                    });
                  });
                }).catch(function (e) {
                  setStatus({ state: 'error', grade: u.kind === 'grades' ? u.id : 0, course: u.kind === 'courses' ? u.id : '', error: 'Không tải được nội dung ' + u.label + '. Kiểm tra mạng rồi thử lại.' });
                  return { ok: false, downloaded: downloaded, error: String(e && e.message) };
                });
              });
            });
            return chain.then(function (res) {
              if (!res.ok) return res;
              setStatus({ state: 'ready', done: todo.length, total: todo.length, percent: 100, fresh: downloaded, grade: 0, course: '', error: '' });
              return { ok: true, downloaded: downloaded, grades: Object.keys(granted).map(Number) };
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

    return { read: read, readCourse: readCourse, sync: sync, start: start, enabled: enabled, status: function () { return loaded.then(function () { return JSON.parse(JSON.stringify(Object.assign({}, status, { enabled: enabled, grades: have.slice(), courses: haveCourses.slice() }))); }); } };
  }

  return { create: create, idbStore: idbStore, gunzipBrowser: gunzipBrowser };
});
