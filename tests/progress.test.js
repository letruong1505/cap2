const test = require('node:test');
const assert = require('node:assert/strict');
const P = require('../renderer/progress.js');

const DAY = 86400000;
const T0 = new Date(2026, 10, 10, 9, 0, 0).getTime();
const meta = (o) => Object.assign({ subject: 'toan', grade: 7, lessonId: 'toan7/a', lesson: 'Bài A', chapter: 'Chương 1', correct: 3, total: 5, seconds: 300 }, o);
const item = (id) => ({ id, stem: 'Câu ' + id, answer: 'A', choices: ['A', 'B'], explain: 'x', secret: 1 });

test('câu sai vào sổ, hạn ngày mai, bỏ trường lạ', () => {
  const d = P.recordAttempt({ attempts: [], notebook: [] }, meta(), [item('q1')], [], T0);
  assert.equal(d.notebook.length, 1);
  assert.equal(d.notebook[0].due, T0 + DAY);
  assert.equal(d.notebook[0].item.secret, undefined);
  assert.equal(P.due(d, T0).length, 0);
  assert.equal(P.due(d, T0 + DAY).length, 1);
});

test('ôn đúng lên hộp 1 rồi 2 rồi ra khỏi sổ; sai thì về hộp 0', () => {
  const d = P.recordAttempt({ attempts: [], notebook: [] }, meta(), [item('q1')], [], T0);
  const k = d.notebook[0].key;
  P.grade(d, k, true, T0 + DAY);
  assert.equal(d.notebook[0].box, 1);
  assert.equal(d.notebook[0].due, T0 + 4 * DAY);
  P.grade(d, k, false, T0 + 4 * DAY);
  assert.equal(d.notebook[0].box, 0);
  assert.equal(d.notebook[0].misses, 2);
  P.grade(d, k, true, T0 + 5 * DAY);
  P.grade(d, k, true, T0 + 8 * DAY);
  assert.equal(d.notebook[0].box, 2);
  P.grade(d, k, true, T0 + 15 * DAY);
  assert.equal(d.notebook.length, 0);
});

test('làm lại bài mà đúng câu đang trong sổ thì nâng hộp', () => {
  const d = P.recordAttempt({ attempts: [], notebook: [] }, meta(), [item('q1')], [], T0);
  P.recordAttempt(d, meta(), [], [item('q1')], T0 + DAY);
  assert.equal(d.notebook[0].box, 1);
});

test('sai lại cùng câu không nhân đôi', () => {
  const d = P.recordAttempt({ attempts: [], notebook: [] }, meta(), [item('q1')], [], T0);
  P.recordAttempt(d, meta(), [item('q1')], [], T0 + DAY);
  assert.equal(d.notebook.length, 1);
  assert.equal(d.notebook[0].misses, 2);
});

test('báo cáo tuần: tổng, số ngày, môn, chương yếu, bỏ bài quá 7 ngày', () => {
  const d = { attempts: [], notebook: [] };
  P.recordAttempt(d, meta({ correct: 2, total: 10, seconds: 600 }), [item('q1')], [], T0);
  P.recordAttempt(d, meta({ subject: 'ly', chapter: 'Chương 2', correct: 9, total: 10, seconds: 600 }), [], [], T0 + DAY);
  P.recordAttempt(d, meta({ correct: 1, total: 10 }), [], [], T0 - 10 * DAY);
  const w = P.weekly(d, T0 + DAY);
  assert.equal(w.attempts, 2);
  assert.equal(w.days, 2);
  assert.equal(w.total, 20);
  assert.equal(w.correct, 11);
  assert.equal(w.pct, 55);
  assert.equal(w.minutes, 20);
  assert.equal(w.subjects.length, 2);
  assert.equal(w.weak.length, 1);
  assert.equal(w.weak[0].name, 'Chương 1');
  assert.equal(w.notebook, 1);
});

test('lưu và nạp qua storage, dữ liệu hỏng thì trả rỗng', () => {
  const mem = {}; const st = { getItem: (k) => mem[k] || null, setItem: (k, v) => { mem[k] = v; } };
  const d = P.recordAttempt(P.load(st), meta(), [item('q1')], [], T0);
  P.save(st, d);
  assert.equal(P.load(st).notebook.length, 1);
  mem[P.KEY] = '{hỏng';
  assert.deepEqual(P.load(st).attempts, []);
});

test('lọc theo lớp: báo cáo và hạn ôn chỉ tính lớp được chọn', () => {
  const d = { attempts: [], notebook: [] };
  P.recordAttempt(d, meta({ grade: 6, lessonId: 'toan6/a', correct: 5, total: 10 }), [item('q1')], [], T0);
  P.recordAttempt(d, meta({ grade: 7, lessonId: 'toan7/a', correct: 9, total: 10 }), [item('q2')], [], T0);
  const w7 = P.weekly(d, T0, 7);
  assert.equal(w7.total, 10);
  assert.equal(w7.pct, 90);
  assert.equal(w7.notebook, 1);
  assert.equal(w7.grade, 7);
  assert.equal(P.weekly(d, T0).total, 20);
  assert.equal(P.due(d, T0 + DAY, 6).length, 1);
  assert.equal(P.due(d, T0 + DAY).length, 2);
});

test('điểm: thang 10 và điểm thưởng', () => {
  assert.equal(P.score10(7, 9), 7.8);
  assert.equal(P.score10(0, 0), 0);
  assert.equal(P.points(9, 10), 110);
  assert.equal(P.points(4, 4), 40);
  assert.equal(P.points(3, 5), 30);
});

test('mục tiêu: tiến độ ngày/tuần, điểm ôn sổ, lọc lớp, giới hạn đặt mục tiêu', () => {
  const d = P.load(null);
  assert.deepEqual(d.goals, { daily: 20, weekly: 5 });
  P.recordAttempt(d, meta({ correct: 9, total: 10 }), [item('q1')], [], T0);
  P.recordAttempt(d, meta({ grade: 8, lessonId: 'toan8/a', correct: 5, total: 5 }), [], [], T0 + 2 * DAY);
  P.grade(d, d.notebook[0].key, true, T0 + 2 * DAY);
  let p = P.progress(d, T0 + 2 * DAY);
  assert.equal(p.todayDone, 5);
  assert.equal(p.daysDone, 2);
  assert.equal(p.todayPts, 70 + 5);
  assert.equal(p.totalPts, 110 + 70 + 5);
  p = P.progress(d, T0 + 2 * DAY, 8);
  assert.equal(p.totalPts, 70);
  P.setGoals(d, { daily: 9999, weekly: 0 });
  assert.deepEqual(d.goals, { daily: 200, weekly: 1 });
  assert.equal(P.weekly(d, T0 + 2 * DAY).prog.weekPts, 185);
});
