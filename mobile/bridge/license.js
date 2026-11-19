// Bản quyền trên Android: cùng quy tắc với main/license (Windows) nhưng chạy trong WebView, không dùng Node.
// Khóa NL1-... ký Ed25519 bằng khóa riêng của chủ sản phẩm; app chỉ giữ khóa công khai nên không tự tạo được khóa.
// Mọi hàm đồng bộ; lưu trữ và mã máy được truyền vào để kiểm thử bằng Node và chạy bằng localStorage trên điện thoại.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobileLicense = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var PREFIX = 'NL1-';
  var NEVER = 'never';
  var DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
  var MAX_FREE_LESSONS = 2; // chưa mua: chỉ mở 2 bài đầu của mỗi môn
  var STORE_KEY = 'nl-license';

  function b64uToBytes(s) {
    var b = String(s).replace(/-/g, '+').replace(/_/g, '/');
    while (b.length % 4) b += '=';
    var bin = atob(b);
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function utf8(bytes) { return new TextDecoder('utf-8').decode(bytes); }

  // Tách và kiểm tra chữ ký. verify(msgBytes, sigBytes) -> boolean.
  function parseKey(key, verify) {
    var text = String(key || '').replace(/\s+/g, '');
    if (text.indexOf(PREFIX) !== 0 || text.indexOf('.') < 0) return { ok: false, reason: 'format' };
    var parts = text.slice(PREFIX.length).split('.');
    var payload;
    try {
      var body = b64uToBytes(parts[0]);
      if (!verify(body, b64uToBytes(parts[1]))) return { ok: false, reason: 'signature' };
      payload = JSON.parse(utf8(body));
    } catch (e) {
      return { ok: false, reason: 'format' };
    }
    var gradesOk = payload.grades === 'all' || (Array.isArray(payload.grades) && payload.grades.every(Number.isInteger));
    if (payload.v !== 1 || !gradesOk || !(payload.expires === NEVER || DATE_RE.test(payload.expires || ''))) return { ok: false, reason: 'format' };
    return { ok: true, payload: payload };
  }

  function today(now) {
    now = now || new Date();
    var p = function (n) { return String(n).padStart(2, '0'); };
    return now.getFullYear() + '-' + p(now.getMonth() + 1) + '-' + p(now.getDate());
  }

  function evaluateKey(key, machineId, now, verify) {
    var r = parseKey(key, verify);
    if (!r.ok) return { status: 'invalid', reason: r.reason };
    var p = r.payload;
    var info = { owner: p.owner || '', id: p.id || '', grades: p.grades, courses: Array.isArray(p.courses) ? p.courses.filter(function (c) { return typeof c === 'string'; }) : [], expiresOn: p.expires };
    if (p.machine !== '*' && p.machine !== machineId) return Object.assign({ status: 'wrong-machine' }, info);
    if (p.expires !== NEVER && today(now) > p.expires) return Object.assign({ status: 'expired' }, info);
    return Object.assign({ status: 'ok' }, info);
  }

  function uniq(a) { return Array.from(new Set(a)); }
  function flat(a) { return [].concat.apply([], a); }

  function merge(results) {
    var ok = results.filter(function (r) { return r.status === 'ok'; });
    if (!ok.length) return null;
    var all = ok.some(function (r) { return r.grades === 'all'; });
    var grades = all ? 'all' : uniq(flat(ok.map(function (r) { return r.grades; }))).sort(function (a, b) { return a - b; });
    var courses = uniq(flat(ok.map(function (r) { return r.courses || []; })));
    var dated = ok.map(function (r) { return r.expiresOn; }).filter(function (e) { return e !== NEVER; }).sort();
    return Object.assign({}, ok[0], { status: 'ok', grades: grades, courses: courses, expiresOn: dated.length ? dated[0] : NEVER, id: ok.map(function (r) { return r.id; }).filter(Boolean).join(', '), owner: ok[0].owner });
  }

  function applyRevocation(e, revokedCodes, revokedItems) {
    if (revokedCodes.has(e.id)) return Object.assign({}, e, { status: 'revoked' });
    var part = revokedItems[String(e.id).replace(/^NL-/, '')];
    if (!part || e.grades === 'all') return e;
    var dropG = new Set(part.grades || []); var dropC = new Set(part.courses || []);
    var grades = e.grades.filter(function (g) { return !dropG.has(g); });
    var courses = e.courses.filter(function (c) { return !dropC.has(c); });
    if (!grades.length && !courses.length) return Object.assign({}, e, { status: 'revoked' });
    return Object.assign({}, e, { grades: grades, courses: courses });
  }

  // storage: { get(key) -> string|null, set(key, string) }. machineId: chuỗi XXXX-XXXX-XXXX. verify: (msg, sig) -> boolean.
  function create(opts) {
    var storage = opts.storage; var machineId = opts.machineId; var verify = opts.verify;

    function read() {
      var d = {};
      try { d = JSON.parse(storage.get(STORE_KEY) || '{}') || {}; } catch (e) { d = {}; }
      var keys = Array.isArray(d.keys) ? d.keys.filter(function (k) { return typeof k === 'string' && k; }) : [];
      var revoked = Array.isArray(d.revoked) ? d.revoked.filter(function (c) { return typeof c === 'string'; }) : [];
      var revokedItems = d.revokedItems && typeof d.revokedItems === 'object' && !Array.isArray(d.revokedItems) ? d.revokedItems : {};
      return { keys: keys, lastSeen: typeof d.lastSeen === 'string' ? d.lastSeen : '', revoked: revoked, revokedItems: revokedItems };
    }
    function update(patch) {
      var cur = read();
      storage.set(STORE_KEY, JSON.stringify(Object.assign({ keys: cur.keys, lastSeen: cur.lastSeen, revoked: cur.revoked, revokedItems: cur.revokedItems }, patch)));
    }
    var evalKey = function (k, now) { return evaluateKey(k, machineId, now, verify); };

    function currentLicense(now) {
      now = now || new Date();
      var store = read();
      if (!store.keys.length) return { status: 'missing', machineId: machineId };
      var t = today(now);
      var revoked = new Set(store.revoked.map(function (c) { return 'NL-' + c; }));
      var results = store.keys.map(function (k) { var e = evalKey(k, now); return e.status === 'ok' ? applyRevocation(e, revoked, store.revokedItems) : e; });
      var merged = merge(results);
      var r = merged || results.find(function (x) { return x.status === 'revoked'; }) || results.find(function (x) { return x.status === 'expired'; }) || results[0];
      // Khóa vĩnh viễn không phụ thuộc ngày nên không cần chặn khi đồng hồ bị lùi.
      if (r.expiresOn !== NEVER && store.lastSeen && t < store.lastSeen) return { status: 'clock', machineId: machineId };
      if (r.status === 'ok' && t > store.lastSeen) update({ lastSeen: t });
      return Object.assign({}, r, { machineId: machineId });
    }

    function activate(key, now) {
      now = now || new Date();
      var clean = String(key).replace(/\s+/g, '');
      var r = evalKey(clean, now);
      if (r.status !== 'ok') return Object.assign({}, r, { machineId: machineId });
      var keep = read().keys.filter(function (k) { return k !== clean && evalKey(k, now).id !== r.id; });
      update({ keys: keep.concat([clean]), lastSeen: today(now) });
      return Object.assign({}, currentLicense(now), { machineId: machineId });
    }

    function deactivate() { update({ keys: [] }); }

    function pingCodes(now) {
      return read().keys.map(function (k) { return evalKey(k, now || new Date()); })
        .filter(function (r) { return r.status === 'ok' && /^NL-[A-Z0-9]{6}$/.test(r.id); })
        .map(function (r) { return r.id.slice(3); });
    }

    function setRevoked(codes, items) {
      var next = uniq((codes || []).filter(function (c) { return typeof c === 'string'; })).sort();
      var nextItems = {};
      var src = items && typeof items === 'object' ? items : {};
      Object.keys(src).forEach(function (code) {
        var v = src[code];
        nextItems[code] = {
          grades: (v && Array.isArray(v.grades) ? v.grades.filter(Number.isInteger) : []).sort(function (a, b) { return a - b; }),
          courses: (v && Array.isArray(v.courses) ? v.courses.filter(function (c) { return typeof c === 'string'; }) : []).sort(),
        };
      });
      var st = read();
      if (JSON.stringify(next) === JSON.stringify(st.revoked.slice().sort()) && JSON.stringify(nextItems) === JSON.stringify(st.revokedItems)) return false;
      update({ revoked: next, revokedItems: nextItems });
      return true;
    }

    var gradeOf = function (subject) { var m = String(subject).match(/(\d+)$/); return m ? Number(m[1]) : NaN; };
    function hasGrade(license, subject) {
      if (license.status !== 'ok') return false;
      return license.grades === 'all' || license.grades.indexOf(gradeOf(subject)) >= 0;
    }
    function allowedFiles(manifest) {
      var files = [];
      manifest.books.forEach(function (b) { b.chapters.forEach(function (c) { c.lessons.forEach(function (l) { if (l.file) files.push(l.file); }); }); });
      return new Set(files.slice(0, MAX_FREE_LESSONS));
    }
    function canOpen(license, subject, manifest, file) { return hasGrade(license, subject) || allowedFiles(manifest).has(file); }
    function annotateManifest(license, subject, manifest) {
      var unlocked = hasGrade(license, subject);
      var free = allowedFiles(manifest);
      var out = JSON.parse(JSON.stringify(manifest));
      out.books.forEach(function (b) { b.chapters.forEach(function (c) { c.lessons.forEach(function (l) { if (l.file) l.locked = !(unlocked || free.has(l.file)); }); }); });
      return out;
    }

    return { currentLicense: currentLicense, activate: activate, deactivate: deactivate, pingCodes: pingCodes, setRevoked: setRevoked, canOpen: canOpen, annotateManifest: annotateManifest, hasGrade: hasGrade };
  }

  return { PREFIX: PREFIX, MAX_FREE_LESSONS: MAX_FREE_LESSONS, parseKey: parseKey, evaluateKey: evaluateKey, today: today, create: create, b64uToBytes: b64uToBytes };
});
