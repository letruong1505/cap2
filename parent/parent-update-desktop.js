// Thanh báo cập nhật của app Phụ huynh bản Windows: hỏi trước khi tải và trước khi cài.
(function () {
  'use strict';
  var bar = document.getElementById('update-bar');
  var d = window.NLDesktop;
  if (!bar || !d) return;
  function say(text, btnText, onClick) {
    bar.replaceChildren();
    var s = document.createElement('span'); s.textContent = text; bar.append(s);
    if (btnText) { var b = document.createElement('button'); b.type = 'button'; b.textContent = btnText; b.addEventListener('click', onClick); bar.append(' ', b); }
    bar.hidden = false;
  }
  var manual = false;
  function show(st) {
    if (!st) return;
    if (st.state === 'available') say('Có bản mới ' + st.version + (st.notes ? ': ' + st.notes : '') + '.', 'Tải về', function () {
      // Bấm tải: báo ngay đang bắt đầu, và từ đây mọi lỗi đều hiện ra (không giấu thanh thông báo).
      manual = true; say('Đang bắt đầu tải bản mới…');
      d.downloadUpdate().then(show, function (e) { show({ state: 'error', error: String((e && e.message) || e) }); });
    });
    else if (st.state === 'downloading') say('Đang tải bản mới: ' + (st.percent | 0) + '%. Vui lòng chờ, đừng tắt app.');
    else if (st.state === 'ready') say('Đã tải xong bản ' + st.version + '.', 'Khởi động lại để cài', function () { d.installUpdate(); });
    else if (manual && st.state === 'none') say('Bạn đang dùng bản mới nhất.');
    else if (manual && st.state === 'error') say('Không kiểm tra được bản mới: ' + (st.error || 'lỗi không rõ') + '. Thử lại sau hoặc báo Nam Linh.');
    else if (manual && st.state === 'off') say('Bản này chưa bật tự cập nhật. Hãy cài lại từ file cài đặt mới nhất.');
    else if (!manual || st.state === 'idle' || st.state === 'checking') bar.hidden = true;
  }
  d.onUpdate(show);
  d.updateStatus().then(show);
  // Nhãn số bản + nút kiểm tra thủ công: dựng ngay bằng số bản đóng gói sẵn, rồi thay bằng số bản thật do Windows báo.
  var label = document.getElementById('build');
  if (label) {
    var cfg = window.NL_MOBILE_CONFIG || {};
    var vs = document.createElement('span'); vs.textContent = 'Phụ huynh ' + (cfg.version || '');
    var vb = document.createElement('button'); vb.type = 'button'; vb.className = 'ghost'; vb.textContent = 'Kiểm tra bản mới';
    vb.addEventListener('click', function () { manual = true; say('Đang kiểm tra bản mới…'); d.checkUpdate().then(show, function (e) { show({ state: 'error', error: String((e && e.message) || e) }); }); });
    label.replaceChildren(vs, ' ', vb);
    if (d.version) d.version().then(function (v) { if (v) vs.textContent = 'Phụ huynh ' + v; }, function () { /* giữ số bản đóng gói */ });
  }
})();
