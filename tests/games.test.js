// Kiểm thử logic trò chơi và kiểm tra toàn bộ nội dung: mọi câu đưa vào trò chơi phải đúng.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const G = require('../renderer/games-logic.js');
const R = require('../core/rational.js');
const { SUBJECTS } = require('../main/content-loader.js');

const CONTENT = path.join(__dirname, '..', 'content');

// Dãy số đơn giản để kết quả chọn ngẫu nhiên lặp lại được.
function seeded(seed) {
  let s = seed;
  return () => {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    return s / 0x80000000;
  };
}

const mcq = (over = {}) => ({
  id: 'm1', type: 'mcq', level: 'Biết', stem: 'Mỗi góc của tam giác đều?',
  expr: '60', choices: ['60', '45', '90', '120'], answer: 0, explain: 'Vì 180/3 = 60.',
  wrong_explain: { 1: 'a', 2: 'b', 3: 'c' }, ...over,
});
const fill = (over = {}) => ({
  id: 'f1', type: 'fill', level: 'Biết', stem: 'Tính (180 - 50)/2.',
  expr: '(180 - 50)/2', answer: '65', explain: 'Vì 130/2 = 65.', ...over,
});

test('câu có hình minh họa không đưa vào trò chơi', () => {
  assert.equal(G.isGameItem(mcq({ figure: 'figures/a.svg' })), false);
  assert.equal(G.isGameItem(fill({ figureSvg: '<svg/>' })), false);
  assert.equal(G.isGameItem(mcq()), true);
});

test('mcq: đáp án phải khớp biểu thức, không có phương án trùng', () => {
  assert.equal(G.isGameItem(mcq({ answer: 1 })), false, 'đáp án chỉ số 1 không khớp expr 60');
  assert.equal(G.isGameItem(mcq({ choices: ['60', '60', '90', '120'] })), false, 'phương án trùng');
  assert.equal(G.isGameItem(mcq({ choices: ['60', '45', '', '120'] })), false, 'phương án rỗng');
  assert.equal(G.isGameItem(mcq({ answer: 9 })), false, 'chỉ số ngoài phạm vi');
  // Hai phương án cùng bằng biểu thức (60 và 120/2) là mơ hồ.
  assert.equal(G.isGameItem(mcq({ choices: ['60', '120/2', '90', '120'] })), false);
});

test('mcq không có expr vẫn hợp lệ nếu chỉ số đáp án đúng', () => {
  assert.equal(G.isGameItem({ id: 'c', type: 'mcq', stem: 'Thủ đô?', choices: ['Hà Nội', 'Huế'], answer: 0, explain: 'x' }), true);
});

test('fill: phải có expr và đáp án khớp expr', () => {
  assert.equal(G.isGameItem(fill()), true);
  assert.equal(G.isGameItem(fill({ answer: '64' })), false);
  assert.equal(G.isGameItem(fill({ expr: undefined })), false);
  assert.equal(G.isGameItem(fill({ expr: '1/0' })), false, 'chia cho 0 không được đưa vào');
});

test('checkFill: so theo giá trị, nhập sai định dạng không tính là trả lời', () => {
  const item = fill({ answer: '1/2', expr: '1/2' });
  assert.deepEqual(G.checkFill(item, '2/4'), { valid: true, correct: true });
  assert.deepEqual(G.checkFill(item, '0,5'), { valid: true, correct: true });
  assert.deepEqual(G.checkFill(item, ' 1/3 '), { valid: true, correct: false });
  assert.deepEqual(G.checkFill(item, 'abc'), { valid: false, correct: false });
  assert.deepEqual(G.checkFill(item, ''), { valid: false, correct: false });
  assert.deepEqual(G.checkFill(item, null), { valid: false, correct: false });
});

test('isChoiceCorrect so theo chỉ số phương án gốc', () => {
  const item = mcq({ answer: 2 });
  assert.equal(G.isChoiceCorrect(item, 2), true);
  assert.equal(G.isChoiceCorrect(item, 0), false);
});

test('collectPool bỏ bài tự luận và câu không hợp lệ', () => {
  const pool = G.collectPool([
    { id: 'a', items: [mcq(), fill({ id: 'f2', figure: 'x.svg' })] },
    { id: 'b', kind: 'review', questions: [{ id: 'r1' }] },
    null,
  ]);
  assert.equal(pool.length, 1);
  assert.equal(pool[0].lessonId, 'a');
});

test('buildPairs: mỗi kết quả chỉ xuất hiện một lần, cặp đúng giá trị', () => {
  const pool = [
    fill({ id: 'p1', expr: '1/2', answer: '1/2' }),
    fill({ id: 'p2', expr: '2/4', answer: '2/4' }), // cùng giá trị với p1
    fill({ id: 'p3', expr: '3*4', answer: '12' }),
    fill({ id: 'p4', expr: '0.5*2', answer: '1' }),
    mcq(), // mcq không vào ghép cặp
  ];
  const pairs = G.buildPairs(pool, 10, seeded(7));
  const keys = pairs.map((p) => p.key);
  assert.equal(new Set(keys).size, keys.length, 'không trùng kết quả');
  assert.equal(pairs.length, 3);
  for (const p of pairs) {
    assert.ok(R.sameValue(p.left.replace(/×/g, '*'), p.right.replace(',', '.')), `${p.left} phải bằng ${p.right}`);
    assert.equal(p.equation, `${p.left} = ${p.right}`);
  }
});

test('viNumber đổi dấu chấm thành dấu phẩy cho số thập phân', () => {
  assert.equal(G.viNumber('4.5'), '4,5');
  assert.equal(G.viNumber('12'), '12');
  assert.equal(G.viNumber('-3/4'), '-3/4');
});

test('chuỗi ngày học: cùng ngày không đếm lại, ngày liên tiếp tăng, đứt chuỗi thì về 1', () => {
  let s = G.recordStudy(undefined, new Date(2026, 10, 9, 8));
  assert.equal(s.count, 1);
  s = G.recordStudy(s, new Date(2026, 10, 9, 21));
  assert.equal(s.count, 1, 'cùng ngày');
  s = G.recordStudy(s, new Date(2026, 10, 10, 7));
  assert.equal(s.count, 2, 'ngày kế tiếp');
  s = G.recordStudy(s, new Date(2026, 10, 12, 7));
  assert.equal(s.count, 1, 'bỏ một ngày thì đứt chuỗi');
  assert.equal(s.best, 2, 'kỷ lục giữ nguyên');
});

test('chuỗi ngày học qua cuối tháng và cuối năm', () => {
  let s = G.recordStudy(undefined, new Date(2026, 11, 31, 22));
  s = G.recordStudy(s, new Date(2027, 0, 1, 6));
  assert.equal(s.count, 2);
  assert.equal(G.dayKey(new Date(2027, 0, 1)), '2027-01-01');
});

test('currentStreak trả về 0 khi đã bỏ qua hôm qua', () => {
  const s = G.recordStudy(undefined, new Date(2026, 10, 9));
  assert.equal(G.currentStreak(s, new Date(2026, 10, 9, 23)), 1);
  assert.equal(G.currentStreak(s, new Date(2026, 10, 10)), 1, 'hôm qua còn giữ chuỗi');
  assert.equal(G.currentStreak(s, new Date(2026, 10, 11)), 0);
  assert.equal(G.currentStreak(undefined, new Date(2026, 10, 11)), 0);
});

test('huy hiệu mở theo số ngày', () => {
  const earned = (n) => G.badgesFor(n).filter((b) => b.earned).map((b) => b.days);
  assert.deepEqual(earned(2), []);
  assert.deepEqual(earned(3), [3]);
  assert.deepEqual(earned(14), [3, 7, 14]);
});

test('updateBest chỉ ghi khi điểm cao hơn và không sửa đối tượng cũ', () => {
  const a = { 'quick:toan7': 5 };
  const b = G.updateBest(a, 'quick', 'toan7', 3);
  assert.equal(b['quick:toan7'], 5);
  assert.equal(a['quick:toan7'], 5);
  assert.equal(G.updateBest(b, 'quick', 'toan7', 9)['quick:toan7'], 9);
  assert.equal(G.updateBest(undefined, 'pairs', 'toan7', 1)['pairs:toan7'], 1);
});

// Kiểm tra toàn bộ nội dung thật: mọi câu trong trò chơi phải có đáp án đúng.
test('toàn bộ nội dung: câu trong trò chơi đều đúng, không trùng kết quả trong ghép cặp', () => {
  let total = 0;
  let excluded = 0;
  for (const subject of SUBJECTS) {
    const manifest = JSON.parse(fs.readFileSync(path.join(CONTENT, subject, 'manifest.json'), 'utf8'));
    const lessons = [];
    for (const book of manifest.books) for (const c of book.chapters) for (const l of c.lessons) {
      if (!l.file) continue;
      lessons.push(JSON.parse(fs.readFileSync(path.join(CONTENT, subject, l.file), 'utf8')));
    }
    const allItems = lessons.filter((l) => l.kind !== 'review').flatMap((l) => l.items || []);
    const pool = G.collectPool(lessons);
    total += allItems.length;
    excluded += allItems.length - pool.length;

    for (const item of pool) {
      if (item.type === 'mcq') {
        assert.ok(item.answer >= 0 && item.answer < item.choices.length, `${subject} ${item.id}: chỉ số đáp án`);
        if (item.expr) assert.ok(R.sameValue(item.expr, item.choices[item.answer]), `${subject} ${item.id}: expr ≠ đáp án`);
      } else {
        assert.ok(R.sameValue(item.expr, item.answer), `${subject} ${item.id}: "${item.expr}" ≠ "${item.answer}"`);
      }
    }

    const pairs = G.buildPairs(pool, 1000, seeded(1));
    const keys = pairs.map((p) => p.key);
    assert.equal(new Set(keys).size, keys.length, `${subject}: ghép cặp trùng kết quả`);
    for (const p of pairs) {
      assert.ok(R.sameValue(p.left.replace(/×/g, '*'), p.right.replace(',', '.')), `${subject}: cặp sai ${p.equation}`);
    }
  }
  assert.ok(total > 1000, 'phải kiểm tra đủ số câu');
  console.log(`  Kiểm tra ${total} câu, đưa vào trò chơi ${total - excluded} câu (loại ${excluded} câu có hình hoặc không kiểm được đáp án).`);
});
