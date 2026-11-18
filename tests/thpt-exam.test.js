// Kiểm thử bảng tổ hợp → khối của khung Ôn thi THPT.
const test = require('node:test');
const assert = require('node:assert/strict');
const D = require('../renderer/thpt-exam-data.js');

const IDS = D.ELECTIVES.map((e) => e.id);

test('có đúng 9 môn tự chọn, mã không trùng', () => {
  assert.equal(D.ELECTIVES.length, 9);
  assert.equal(new Set(IDS).size, 9);
});

test('mỗi khóa tổ hợp gồm 2 môn có thật, sắp theo thứ tự chữ cái', () => {
  for (const key of Object.keys(D.COMBO_KHOI)) {
    const parts = key.split('|');
    assert.equal(parts.length, 2, key);
    for (const p of parts) assert.ok(IDS.includes(p), `${key}: ${p} không có trong danh sách`);
    assert.deepEqual(parts, [...parts].sort(), `${key} chưa sắp xếp`);
  }
});

test('mỗi khối có mã dạng chữ + 2 số và không trùng trong cùng tổ hợp', () => {
  for (const [key, khoi] of Object.entries(D.COMBO_KHOI)) {
    assert.ok(khoi.length >= 2, key);
    assert.equal(new Set(khoi).size, khoi.length, key);
    for (const k of khoi) assert.match(k, /^[A-D]\d{2}$/, `${key}: ${k}`);
  }
});

test('khoiFor không phụ thuộc thứ tự chọn và trả null khi chưa đủ 2 môn', () => {
  assert.deepEqual(D.khoiFor(['PH', 'CH']), D.khoiFor(['CH', 'PH']));
  assert.deepEqual(D.khoiFor(['CH', 'PH']), ['A00', 'C01', 'C02', 'C05']);
  assert.equal(D.khoiFor(['PH']), null);
  assert.equal(D.khoiFor(['PH', 'TECH']), null);
});

test('có 2 mốc cấu trúc kỳ thi', () => {
  assert.equal(D.YEARS.length, 2);
});
