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
    if (st.state === 'available') say('Có bản mới ' + st.version + (st.notes ? ': ' + st.notes : '') + '.', 'Tải về', function () { d.downloadUpdate(); });
    else if (st.state === 'downloading') say('Đang tải bản mới: ' + (st.percent | 0) + '%');
    else if (st.state === 'ready') say('Đã tải xong bản ' + st.version + '.', 'Khởi động lại để cài', function () { d.installUpdate(); });
    else if (manual && st.state === 'none') say('Bạn đang dùng bản mới nhất.');
    else if (manual && st.state === 'error') say('Không kiểm tra được bản mới: ' + (st.error || 'lỗi không rõ') + '. Thử lại sau hoặc báo Nam Linh.');
    else if (manual && st.state === 'off') say('Bản này chưa bật tự cập nhật. Hãy cài lại từ file cài đặt mới nhất.');
    else if (!manual || st.state === 'idle' || st.state === 'checking') bar.hidden = true;
  }
  d.onUpdate(show);
  d.updateStatus().then(show);
  // Hiện đúng số bản đang cài (lấy từ hệ thống) và nút kiểm tra bản mới thủ công.
  var label = document.getElementById('build');
  if (label && d.version) d.version().then(function (v) {
    var s = document.createElement('span'); s.textContent = 'Phụ huynh ' + v;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'ghost'; b.textContent = 'Kiểm tra bản mới';
    b.addEventListener('click', function () { manual = true; say('Đang kiểm tra bản mới…'); d.checkUpdate().then(show); });
    label.replaceChildren(s, ' ', b);
  });
})();
