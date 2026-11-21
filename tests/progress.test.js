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
  assert.deepEqual(d.goals, { daily: 50, weekend: 80, weekly: 5, pass: 80, passBy: {} });
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
  assert.deepEqual(d.goals, { daily: 200, weekend: 80, weekly: 1, pass: 80, passBy: {} });
  assert.equal(P.weekly(d, T0 + 2 * DAY).prog.weekPts, 185);
});

test('lưu đáp án em đã nhập khi làm sai, null nếu bỏ trống, cập nhật ở lần sai sau', () => {
  const m = Object.assign(meta(), { given: { q1: '1500', q2: null } });
  const d = P.recordAttempt({ attempts: [], notebook: [] }, m, [item('q1'), item('q2')], [], T0);
  assert.equal(d.notebook.find((n) => n.key.endsWith('#q1')).given, '1500');
  assert.equal(d.notebook.find((n) => n.key.endsWith('#q2')).given, null);
  P.recordAttempt(d, Object.assign(meta(), { given: { q1: '150' } }), [item('q1')], [], T0 + 1000);
  assert.equal(d.notebook.find((n) => n.key.endsWith('#q1')).given, '150');
});

test('không truyền given thì vẫn ghi được, given là null', () => {
  const d = P.recordAttempt({ attempts: [], notebook: [] }, meta(), [item('q1')], [], T0);
  assert.equal(d.notebook[0].given, null);
});

test('report: theo khoảng ngày, lọc môn, đếm đúng/sai từng ngày', () => {
  const d = P.load(null);
  const T = new Date(2026, 10, 17, 10).getTime();
  P.recordAttempt(d, { subject: 'toan', grade: 8, lessonId: 'a', lesson: 'A', chapter: 'C1', correct: 7, total: 10, seconds: 60 }, [], [], T);
  P.recordAttempt(d, { subject: 'anh', grade: 8, lessonId: 'b', lesson: 'B', chapter: 'C2', correct: 3, total: 5, seconds: 60 }, [], [], T - 86400000);
  const r = P.report(d, { from: T - 6 * 86400000, to: T }, T);
  assert.equal(r.days.length, 7);
  assert.equal(r.total, 15); assert.equal(r.correct, 10); assert.equal(r.wrong, 5); assert.equal(r.pct, 67);
  assert.equal(r.days[6].total, 10); assert.equal(r.days[5].correct, 3); assert.equal(r.activeDays, 2);
  const m = P.report(d, { from: T, to: T, subject: 'toan' }, T);
  assert.equal(m.days.length, 1); assert.equal(m.total, 10); assert.equal(m.subjects.length, 1);
  assert.equal(P.report(d, { from: T, to: T, subject: 'anh' }, T).total, 0);
  assert.equal(P.progress(d, T).todayCorrect, 7);
});

test('mục tiêu theo ngày: T2–T6 dùng mục tiêu ngày thường, T7 và CN dùng mục tiêu cuối tuần', () => {
  const sat = new Date(2026, 10, 21, 10).getTime(); // thứ 7
  const fri = sat - DAY; const sun = sat + DAY; const mon = sun + DAY;
  const d = P.load(null);
  P.setGoals(d, { daily: 50, weekend: 80, weekly: 5 });
  assert.deepEqual([fri, sat, sun, mon].map((t) => P.goalFor(d.goals, t)), [50, 80, 80, 50]);
  P.recordAttempt(d, meta({ correct: 50, total: 50 }), [], [], fri);
  P.recordAttempt(d, meta({ correct: 60, total: 60 }), [], [], sat);
  const r = P.report(d, { from: fri, to: sat }, sat);
  assert.deepEqual(r.days.map((x) => x.reached), [true, false]); // T6 đủ 50; T7 mới 60/80
  assert.equal(P.progress(d, sat).todayGoal, 80);
  assert.equal(P.progress(d, fri).todayGoal, 50);
  // dữ liệu cũ chưa có mục tiêu cuối tuần: dùng mặc định 80
  const old = P.setGoals({}, { daily: 20, weekly: 5 });
  assert.deepEqual(old.goals, { daily: 20, weekend: 80, weekly: 5, pass: 80, passBy: {} });
});

test('ngưỡng đạt: mặc định 80%, riêng từng môn, chương yếu theo ngưỡng', () => {
  assert.equal(P.passFor(P.load(null).goals, 'toan'), 80);
  let d = P.recordAttempt({ attempts: [], notebook: [] }, meta({ subject: 'toan', correct: 4, total: 5 }), [], [], T0);
  d = P.recordAttempt(d, meta({ subject: 'anh', grade: 7, lessonId: 'anh7/a', correct: 3, total: 5, chapter: 'Unit 1' }), [], [], T0);
  d = P.setGoals(d, { daily: 50, weekend: 80, weekly: 5, pass: 80, passBy: { anh: 60, toan: 5, 'x y': 90 } });
  assert.deepEqual(d.goals.passBy, { anh: 60 }); // giá trị <10 hoặc mã sai bị bỏ
  const r = P.report(d, { from: T0 - DAY, to: T0 });
  const by = Object.fromEntries(r.subjects.map((s) => [s.subject, s]));
  assert.equal(by.toan.passed, true); assert.equal(by.toan.need, 80); // 80% >= 80%
  assert.equal(by.anh.passed, true); assert.equal(by.anh.need, 60); // 60% >= 60%
  d = P.setGoals(d, { pass: 90 }); // không nhắc tới passBy thì giữ nguyên
  assert.deepEqual(d.goals.passBy, { anh: 60 });
  const r2 = P.report(d, { from: T0 - DAY, to: T0 });
  assert.equal(r2.subjects.find((s) => s.subject === 'toan').passed, false);
  assert.ok(r2.weak.some((c) => c.subject === 'toan')); // 80% < 90% nên chương Toán thành chương yếu
  assert.ok(!r2.weak.some((c) => c.subject === 'anh'));
});

test('báo cáo từng ngày có chi tiết theo môn và đạt/không đạt (để chạm vào cột xem)', () => {
  let d = P.recordAttempt({ attempts: [], notebook: [] }, meta({ subject: 'toan', correct: 4, total: 5 }), [], [], T0);
  d = P.recordAttempt(d, meta({ subject: 'anh', grade: 7, lessonId: 'anh7/a', correct: 2, total: 5, chapter: 'U1' }), [], [], T0);
  const r = P.report(d, { from: T0, to: T0 }, T0);
  const day = r.days[0];
  assert.equal(day.subjects.length, 2);
  const by = Object.fromEntries(day.subjects.map((s) => [s.subject, s]));
  assert.deepEqual([by.toan.passed, by.anh.passed, by.anh.pct], [true, false, 40]);
});

test('phần thưởng chuỗi ngày: đếm ngày đạt liên tiếp, hôm nay chưa đạt không làm đứt, trao thưởng thì tính lại', () => {
  const day = (iso, correct, total) => ({ t: new Date(iso + 'T10:00:00').getTime(), subject: 'toan', grade: 9, correct, total, lessons: 1 });
  const now = new Date('2026-11-21T20:00:00').getTime();
  const data = { attempts: [day('2026-11-17', 8, 10), day('2026-11-18', 7, 10), day('2026-11-19', 9, 10), day('2026-11-20', 7, 10)], reward: { on: true, days: 4, pct: 70, text: 'Game 30 phút' } };
  let s = P.streak(data, now);
  assert.deepEqual([s.count, s.achieved, s.todayOk], [4, true, false]);
  data.attempts.push(day('2026-11-21', 3, 10)); // hôm nay làm nhưng dưới ngưỡng: chưa tính hôm nay, chưa đứt chuỗi
  assert.equal(P.streak(data, now).count, 4);
  data.attempts.pop();
  data.attempts[1] = day('2026-11-18', 6, 10); // ngày giữa chuỗi dưới 70% thì đứt
  assert.equal(P.streak(data, now).count, 2);
  data.attempts[1] = day('2026-11-18', 7, 10);
  P.giveReward(data, now);
  assert.equal(P.streak(data, now).count, 0);
  assert.equal(data.reward.given.length, 1);
  data.attempts.push(day('2026-11-21', 9, 10));
  assert.equal(P.streak(data, now).count, 0); // ngày trao thưởng không tính vào chuỗi mới
  assert.equal(P.streak({ attempts: data.attempts, reward: { on: false } }, now).achieved, false);
  assert.equal(P.cleanReward({ days: 999, pct: 5, text: 'x'.repeat(200) }).days, 60);
});
