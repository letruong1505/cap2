const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const { scoreExam, TF_POINTS } = require('../renderer/exam.js');

const mcq = (id, part = 1) => ({ id, part, type: 'mcq' });
const fill = (id) => ({ id, part: 3, type: 'fill' });
const tf = (id) => ({ id, part: 2, type: 'tf', statements: [{ truth: true }, { truth: false }, { truth: true }, { truth: false }] });
const eq = (it, v) => v === 'ok';

test('điểm đúng–sai theo số ý đúng', () => {
  assert.deepStrictEqual(TF_POINTS, [0, 0.1, 0.25, 0.5, 1]);
  for (let k = 0; k <= 4; k++) {
    const a = {}; [true, false, true, false].forEach((t, i) => { a[i] = i < k ? t : !t; });
    assert.strictEqual(scoreExam([tf('t')], { t: a }, eq).p2, TF_POINTS[k]);
  }
});

test('tổng điểm ba phần và câu bỏ trống', () => {
  const items = [mcq('a'), mcq('b'), tf('t'), fill('f')];
  const r = scoreExam(items, { a: 'ok', t: { 0: true, 1: false, 2: true, 3: false }, f: 'ok' }, eq);
  assert.strictEqual(r.p1, 0.25); assert.strictEqual(r.p2, 1); assert.strictEqual(r.p3, 0.5);
  assert.strictEqual(r.total, 1.75);
  assert.strictEqual(scoreExam(items, {}, eq).total, 0);
});

test('đề thi mẫu đúng cấu trúc 12+4+6 và tối đa 10 điểm', () => {
  const dir = path.join(__dirname, '..', 'content', 'toan12', 'de-thi');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
  assert.ok(files.length >= 1);
  files.forEach((f) => {
    const e = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    const n = (p) => e.items.filter((i) => i.part === p).length;
    assert.deepStrictEqual([n(1), n(2), n(3)], [12, 4, 6]);
    assert.strictEqual(e.durationMin, 90);
    assert.strictEqual(12 * 0.25 + 4 * 1 + 6 * 0.5, 10);
  });
});
