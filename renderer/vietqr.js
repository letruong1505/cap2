// Tạo chuỗi VietQR (chuẩn EMVCo/NAPAS) để mã QR chuyển khoản có sẵn số tiền và nội dung.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VietQR = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  function crc16(str) {
    let crc = 0xFFFF;
    for (let i = 0; i < str.length; i++) {
      crc ^= str.charCodeAt(i) << 8;
      for (let b = 0; b < 8; b++) crc = (crc & 0x8000) ? ((crc << 1) ^ 0x1021) & 0xFFFF : (crc << 1) & 0xFFFF;
    }
    return crc.toString(16).toUpperCase().padStart(4, '0');
  }
  const tlv = (id, value) => id + String(value.length).padStart(2, '0') + value;

  // Bỏ dấu tiếng Việt, chỉ giữ chữ, số, khoảng trắng; tối đa 25 ký tự (giới hạn nội dung chuyển khoản).
  function cleanContent(text) {
    return String(text).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D')
      .replace(/[^A-Za-z0-9 ]/g, '').replace(/\s+/g, ' ').trim().slice(0, 25).trim();
  }

  function build({ bin, account, amount, content }) {
    if (!/^\d{6}$/.test(String(bin))) throw new Error('Mã ngân hàng (BIN) phải gồm 6 chữ số');
    if (!/^[0-9A-Za-z]{4,19}$/.test(String(account))) throw new Error('Số tài khoản không hợp lệ');
    const money = Math.round(Number(amount));
    if (!(money > 0)) throw new Error('Số tiền phải lớn hơn 0');
    const member = tlv('00', String(bin)) + tlv('01', String(account));
    const merchant = tlv('00', 'A000000727') + tlv('01', member) + tlv('02', 'QRIBFTTA');
    const body = tlv('00', '01') + tlv('01', '12') + tlv('38', merchant) + tlv('53', '704') + tlv('54', String(money)) +
      tlv('58', 'VN') + tlv('62', tlv('08', cleanContent(content))) + '6304';
    return body + crc16(body);
  }
  return { build, crc16, cleanContent };
});
