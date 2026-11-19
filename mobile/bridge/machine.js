// Mã máy cho điện thoại: băm từ mã thiết bị Android, hiển thị dạng XXXX-XXXX-XXXX (cùng dạng với mã máy tính).
// Dùng SHA-512 của tweetnacl để chạy đồng bộ, không phụ thuộc WebCrypto. Khôi phục cài đặt gốc có thể đổi mã (khi đó cần cấp lại khóa).
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NLMobileMachine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  function machineIdFrom(rawId, nacl) {
    var bytes = nacl.hash(new TextEncoder().encode('vungbai-android-v1|' + String(rawId)));
    var hex = '';
    for (var i = 0; i < 6; i++) hex += ('0' + bytes[i].toString(16)).slice(-2);
    hex = hex.toUpperCase();
    return hex.slice(0, 4) + '-' + hex.slice(4, 8) + '-' + hex.slice(8, 12);
  }
  return { machineIdFrom: machineIdFrom };
});
