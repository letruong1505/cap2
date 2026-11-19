/* Sao lưu localStorage ra file của ứng dụng và khôi phục khi localStorage bị mất (ví dụ sau khi cập nhật bản mới).
   Phải nạp trước mọi tệp khác đọc localStorage. */
(function () {
  var api = window.vungBai;
  var ls;
  try { ls = window.localStorage; } catch (e) { return; }
  if (!api || !api.storeAll || !api.storeSet || !ls) return;

  var data = {};
  try { data = api.storeAll() || {}; } catch (e) { data = {}; }

  // 1. Khôi phục: khóa có trong file mà localStorage chưa có.
  Object.keys(data).forEach(function (k) {
    try { if (ls.getItem(k) === null) ls.setItem(k, data[k]); } catch (e) { /* bỏ qua */ }
  });
  // 2. Chuyển dữ liệu cũ: khóa có trong localStorage mà file chưa có.
  try {
    for (var i = 0; i < ls.length; i++) {
      var key = ls.key(i);
      if (data[key] === undefined) api.storeSet(key, ls.getItem(key));
    }
  } catch (e) { /* bỏ qua */ }

  // 3. Từ nay mọi thay đổi được ghi song song ra file.
  var set = Storage.prototype.setItem;
  var remove = Storage.prototype.removeItem;
  var clear = Storage.prototype.clear;
  Storage.prototype.setItem = function (k, v) {
    set.call(this, k, v);
    if (this === ls) { try { api.storeSet(String(k), String(v)); } catch (e) { /* bỏ qua */ } }
  };
  Storage.prototype.removeItem = function (k) {
    remove.call(this, k);
    if (this === ls) { try { api.storeSet(String(k), null); } catch (e) { /* bỏ qua */ } }
  };
  Storage.prototype.clear = function () {
    var keys = [];
    if (this === ls) { for (var j = 0; j < ls.length; j++) keys.push(ls.key(j)); }
    clear.call(this);
    keys.forEach(function (k) { try { api.storeSet(k, null); } catch (e) { /* bỏ qua */ } });
  };
})();
