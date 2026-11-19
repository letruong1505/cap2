// Trang khởi động của ứng dụng Android (index.html chỉ nạp tệp này). Nếu đã tải được gói cập nhật nội dung (OTA) hợp lệ,
// mới hơn apk và đã chạy ổn thì dựng giao diện từ gói đó; ngược lại (hoặc có bất kỳ lỗi nào) chuyển sang bản gốc trong apk (app.html).
// An toàn: gói lỗi khi khởi động hai lần liên tiếp, hoặc gây lỗi script trong vài giây đầu, bị đánh dấu hỏng và không dùng lại.
(function () {
  'use strict';
  var native = window.NL_NATIVE || { code: 0 };
  var HEALTHY_MS = 6000;
  var store = window.NLOtaStore;

  function fallback() { location.replace('app.html'); }
  if (!store) { fallback(); return; }

  var settled = false;
  var guard = setTimeout(function () { if (!settled) { settled = true; fallback(); } }, 5000); // kho không phản hồi

  function markBad(build) {
    return store.get('bad').catch(function () { return null; }).then(function (bad) {
      bad = Array.isArray(bad) ? bad : [];
      if (bad.indexOf(build) < 0) bad.push(build);
      return store.set('bad', bad.slice(-20));
    }).catch(function () {});
  }

  function render(rec) {
    var urls = [];
    var blob = function (text) { var u = URL.createObjectURL(new Blob([text], { type: 'text/javascript' })); urls.push(u); return u; };
    var html = rec.html
      .replace(/<script\s+src="([^"]+)"\s*><\/script>/g, function (m, src) {
        return typeof rec.files[src] === 'string' ? '<script src="' + blob(rec.files[src]) + '"></script>' : m;
      })
      .replace(/<link\s+rel="stylesheet"\s+href="([^"]+)"\s*\/?>/g, function (m, href) {
        return typeof rec.files[href] === 'string' ? '<style>' + rec.files[href].replace(/<\/style/gi, '<\\/style') + '</style>' : m;
      });
    window.NL_OTA_RUNNING = rec.build;
    document.open(); document.write(html); document.close();

    var ended = false;
    function rollback() {
      if (ended) return; ended = true;
      markBad(rec.build).then(fallback);
    }
    window.addEventListener('error', function (ev) { if (!ended) rollback(ev); }, true);
    setTimeout(function () {
      if (ended) return; ended = true;
      rec.tries = 0;
      store.set('current', rec).catch(function () {});
    }, HEALTHY_MS);
  }

  Promise.all([store.get('current'), store.get('bad')]).then(function (r) {
    if (settled) return; settled = true; clearTimeout(guard);
    var rec = r[0]; var bad = Array.isArray(r[1]) ? r[1] : [];
    var usable = rec && typeof rec.html === 'string' && rec.files && typeof rec.files === 'object' && rec.build > native.code
      && native.code >= (rec.minNative || 0) && bad.indexOf(rec.build) < 0;
    if (!usable) return fallback();
    if ((rec.tries || 0) >= 2) return markBad(rec.build).then(fallback); // đã khởi động hai lần mà chưa chạy ổn
    rec.tries = (rec.tries || 0) + 1;
    return store.set('current', rec).then(function () { render(rec); });
  }).catch(function () { if (!settled) { settled = true; clearTimeout(guard); } fallback(); });
})();
