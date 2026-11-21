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
  return out.filter((p) => !p.includes('on-tap') && !p.includes('nang-cao') && !p.includes('de-thi'));
}
// minTry: số câu "Thử ngay" tối thiểu (các môn dựng tự động bằng tools/auto-cards.py chưa có câu thử)
const SUBJECTS = { toan12: [19, 25], ly12: [25, 25], hoa12: [22, 11], sinh12: [35, 17], lichsu12: [17, 8], diali12: [35, 17], gdktpl12: [16, 8],
   toan11: [33, 16], ly11: [26, 13], hoa11: [19, 9], sinh11: [29, 14], lichsu11: [13, 6], diali11: [30, 15], gdktpl11: [21, 10],
  toan10: [27, 13], ly10: [34, 17], hoa10: [16, 8], sinh10: [26, 13], lichsu10: [14, 7], diali10: [40, 20], gdktpl10: [23, 11], toan9: [32, 16], ly9: [16, 8], hoa9: [18, 9], sinh9: [16, 8], lichsu9: [22, 11], diali9: [15, 7], toan8: [39, 19], ly8: [17, 8], hoa8: [12, 6], sinh8: [18, 9], lichsu8: [20, 10], diali8: [12, 6], toan7: [37, 3], ly7: [14, 7], hoa7: [7, 3], sinh7: [23, 11], lichsu7: [22, 11], diali7: [20, 10], toan6: [43, 21], ly6: [21, 10], hoa6: [9, 4], sinh6: [17, 8], lichsu6: [20, 10], diali6: [26, 13] };

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
