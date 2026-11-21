const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

function collect(subject) {
  const out = [];
  (function walk(d) {
    for (const f of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, f.name);
      if (f.isDirectory()) { if (f.name !== 'figures') walk(p); } else if (f.name.endsWith('.json') && f.name !== 'manifest.json') out.push(p);
    }
  })(path.join(__dirname, '..', 'content', subject));
  return out.filter((p) => !p.includes('on-tap') && !p.includes('nang-cao'));
}
// minTry: số câu "Thử ngay" tối thiểu (các môn dựng tự động bằng tools/auto-cards.py chưa có câu thử)
const SUBJECTS = { toan12: [19, 25], ly12: [25, 25], hoa12: [22, 0], sinh12: [35, 0], lichsu12: [17, 0], diali12: [35, 0], gdktpl12: [16, 0],
   toan11: [33, 0], ly11: [26, 0], hoa11: [19, 0], sinh11: [29, 0], lichsu11: [13, 0], diali11: [30, 0], gdktpl11: [21, 0] };

for (const [subject, [count, minTry]] of Object.entries(SUBJECTS)) {
  const bai = collect(subject);

  test(subject + ': mọi bài học có lý thuyết dạng thẻ (tóm tắt, thẻ)', () => {
    assert.equal(bai.length, count);
    for (const p of bai) {
      const th = JSON.parse(fs.readFileSync(p, 'utf8')).theory;
      assert.equal(th[0].type, 'summary', path.basename(p) + ': khối đầu phải là tóm tắt');
      const cards = th.filter((b) => b.type === 'card');
      assert.ok(cards.length >= 1, path.basename(p) + ': cần ít nhất 1 thẻ');
      cards.forEach((c, i) => assert.equal(c.n, i + 1, path.basename(p) + ': số thẻ phải liên tục'));
      assert.ok(!th.some((b) => b.type === 'text' && b.content && b.content.length > 200 && !b.content.startsWith('Bài')), path.basename(p) + ': còn đoạn văn dài');
    }
  });

  test(subject + ': câu "Thử ngay" có đáp án hợp lệ và có giải thích', () => {
    let n = 0;
    for (const p of bai) {
      for (const c of JSON.parse(fs.readFileSync(p, 'utf8')).theory.filter((b) => b.type === 'card' && b.try)) {
        const t = c.try; n++;
        assert.ok(t.q && Array.isArray(t.options) && t.options.length >= 2, path.basename(p) + ': câu thử thiếu phương án');
        assert.ok(Number.isInteger(t.answer) && t.answer >= 0 && t.answer < t.options.length);
        assert.equal(new Set(t.options).size, t.options.length, path.basename(p) + ': phương án trùng nhau');
        assert.ok(t.explain, path.basename(p) + ': thiếu giải thích');
      }
    }
    assert.ok(n >= minTry);
  });

  test(subject + ': chạy lại công cụ dựng thẻ không làm đổi nội dung', () => {
    const before = bai.map((p) => fs.readFileSync(p, 'utf8'));
    execFileSync('python3', ['-B', path.join(__dirname, '..', 'tools', 'build-theory-cards.py')], { stdio: 'pipe' });
    bai.forEach((p, i) => assert.equal(fs.readFileSync(p, 'utf8'), before[i], path.basename(p) + ' đã bị đổi'));
  });
}
