const test = require('node:test');
const assert = require('node:assert');
const Q = require('../renderer/vietqr.js');

test('CRC16-CCITT đúng với vector chuẩn', () => {
  assert.strictEqual(Q.crc16('123456789'), '29B1');
});

test('chuỗi VietQR có đủ trường và CRC khớp', () => {
  const s = Q.build({ bin: '970436', account: '0011001234567', amount: 999000, content: 'NL ABC123 Nguyễn Văn A' });
  assert.ok(s.startsWith('000201010212'));
  assert.ok(s.includes('0010A000000727'));
  assert.ok(s.includes('0006970436'));
  assert.ok(s.includes('QRIBFTTA'));
  assert.ok(s.includes('5406999000'));
  assert.ok(s.includes('5802VN'));
  assert.strictEqual(s.slice(-4), Q.crc16(s.slice(0, -4)));
});

test('nội dung được bỏ dấu và giới hạn 25 ký tự', () => {
  assert.strictEqual(Q.cleanContent('Nguyễn Đức Hiếu mua khoá học Gia sư AI rất dài'), 'Nguyen Duc Hieu mua khoa');
  assert.ok(Q.cleanContent('x'.repeat(40)).length <= 25);
});

test('từ chối dữ liệu sai', () => {
  assert.throws(() => Q.build({ bin: '12', account: '123456', amount: 1, content: 'a' }));
  assert.throws(() => Q.build({ bin: '970436', account: '123456', amount: 0, content: 'a' }));
});
