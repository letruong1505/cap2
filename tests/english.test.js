const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('../renderer/english.js');
const lesson = require('../content/anh7/tap1/unit-1/unit-1.json');

test('ô chữ: các chữ ở cột dọc ghép thành từ khóa', () => {
  assert.equal(E.keyword(lesson.crossword.words), E.norm(lesson.crossword.keyword));
  assert.deepEqual(E.validate(lesson.crossword), []);
});

test('ô chữ: mọi hàng thẳng cột từ khóa', () => {
  const L = E.layout(lesson.crossword.words);
  for (const r of L.rows) assert.equal(r.offset + r.keyIndex, L.keyCol);
  assert.ok(L.width >= Math.max(...L.rows.map((r) => r.letters.length)));
});

test('ô chữ: bắt lỗi từ khóa sai và keyIndex ngoài từ', () => {
  const bad = JSON.parse(JSON.stringify(lesson.crossword));
  bad.keyword = 'hobbyx';
  assert.ok(E.validate(bad).some((e) => /không khớp/.test(e)));
  bad.keyword = lesson.crossword.keyword;
  bad.words[0].keyIndex = 99;
  assert.ok(E.validate(bad).some((e) => /ngoài từ/.test(e)));
});

test('điểm mỗi hàng: trừ gợi ý và lần sai, tối thiểu 2', () => {
  assert.equal(E.rowScore({}), 10);
  assert.equal(E.rowScore({ hints: 1, wrong: 1 }), 6);
  assert.equal(E.rowScore({ hints: 2, wrong: 9 }), 2);
});

test('chuẩn hóa đáp án bỏ khoảng trắng và dấu câu', () => {
  assert.equal(E.norm(' Horse-Riding '), 'horseriding');
});
