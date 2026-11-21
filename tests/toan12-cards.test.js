const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const BASE = path.join(__dirname, '..', 'content', 'toan12');
const lessons = [];
(function walk(d) {
  for (const f of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, f.name);
    if (f.isDirectory()) { if (f.name !== 'figures') walk(p); } else if (f.name.endsWith('.json') && f.name !== 'manifest.json') lessons.push(p);
  }
})(BASE);
const bai = lessons.filter((p) => !p.includes('on-tap'));

test('Toán 12: mọi bài học có lý thuyết dạng thẻ (tóm tắt, thẻ, cách giải)', () => {
  assert.equal(bai.length, 19);
  for (const p of bai) {
    const d = JSON.parse(fs.readFileSync(p, 'utf8'));
    const th = d.theory;
    assert.equal(th[0].type, 'summary', path.basename(p) + ': khối đầu phải là tóm tắt');
    const cards = th.filter((b) => b.type === 'card');
    assert.ok(cards.length >= 3, path.basename(p) + ': cần ít nhất 3 thẻ');
    cards.forEach((c, i) => assert.equal(c.n, i + 1, path.basename(p) + ': số thẻ phải liên tục'));
    assert.ok(!th.some((b) => b.type === 'text' && b.content && b.content.length > 200 && !b.content.startsWith('Bài')), path.basename(p) + ': còn đoạn văn dài chưa chuyển thành thẻ');
  }
});

test('Toán 12: câu "Thử ngay" có đáp án hợp lệ và có giải thích', () => {
  let n = 0;
  for (const p of bai) {
    const d = JSON.parse(fs.readFileSync(p, 'utf8'));
    for (const c of d.theory.filter((b) => b.type === 'card' && b.try)) {
      const t = c.try; n++;
      assert.ok(t.q && Array.isArray(t.options) && t.options.length >= 2, path.basename(p) + ': câu thử thiếu phương án');
      assert.ok(Number.isInteger(t.answer) && t.answer >= 0 && t.answer < t.options.length);
      assert.equal(new Set(t.options).size, t.options.length, path.basename(p) + ': phương án trùng nhau');
      assert.ok(t.explain, path.basename(p) + ': thiếu giải thích');
    }
  }
  assert.ok(n >= 25);
});

test('Toán 12: chạy lại công cụ dựng thẻ không làm đổi nội dung (không bị ghi đè)', () => {
  const before = bai.map((p) => fs.readFileSync(p, 'utf8'));
  execFileSync('python3', [path.join(__dirname, '..', 'tools', 'build-toan12-cards.py')], { stdio: 'pipe' });
  bai.forEach((p, i) => assert.equal(fs.readFileSync(p, 'utf8'), before[i], path.basename(p) + ' đã bị đổi: chạy lại build-toan12-cards.py'));
});
