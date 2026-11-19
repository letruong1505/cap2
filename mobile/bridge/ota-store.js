// Kho lưu gói cập nhật nội dung (OTA) trong IndexedDB của WebView. Nằm trong apk (không nằm trong gói OTA)
// vì trang khởi động cần đọc nó trước khi biết có gói nào dùng được.
(function (root) {
  'use strict';
  var DB = 'nl-ota'; var STORE = 'kv';
  function open() {
    return new Promise(function (resolve, reject) {
      if (!root.indexedDB) { reject(new Error('Không có IndexedDB')); return; }
      var req = root.indexedDB.open(DB, 1);
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
  root.NLOtaStore = {
    get: function (k) { return run('readonly', function (s, ret) { var r = s.get(k); r.onsuccess = function () { ret(r.result === undefined ? null : r.result); }; }); },
    set: function (k, v) { return run('readwrite', function (s) { s.put(v, k); }); },
    remove: function (k) { return run('readwrite', function (s) { s.delete(k); }); },
  };
})(typeof self !== 'undefined' ? self : this);
