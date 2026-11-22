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
  function show(st) {
    if (!st) return;
    if (st.state === 'available') say('Có bản mới ' + st.version + (st.notes ? ': ' + st.notes : '') + '.', 'Tải về', function () { d.downloadUpdate(); });
    else if (st.state === 'downloading') say('Đang tải bản mới: ' + (st.percent | 0) + '%');
    else if (st.state === 'ready') say('Đã tải xong bản ' + st.version + '.', 'Khởi động lại để cài', function () { d.installUpdate(); });
    else if (st.state === 'error') bar.hidden = true;
    else bar.hidden = true;
  }
  d.onUpdate(show);
  d.updateStatus().then(show);
})();
