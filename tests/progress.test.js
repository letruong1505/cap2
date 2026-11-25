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

test('phần thưởng theo tuần: đếm ngày đạt thứ 2–CN, chốt thắng/hụt, chỉ báo một lần, trao thưởng', () => {
  const day = (iso, correct, total) => ({ t: new Date(iso + 'T10:00:00').getTime(), subject: 'toan', grade: 9, correct, total, lessons: 1 });
  const sat = new Date('2026-11-21T20:00:00').getTime(); // thứ Bảy; tuần này bắt đầu 2026-11-16
  const data = { attempts: [], reward: { on: true, days: 3, pct: 70, text: 'Game 30 phút', from: '2026-11-09' } };
  // tuần 09–15/11: 3 ngày đạt (ngày 11/11 dưới ngưỡng) → chỉ 2 ngày đạt: hụt
  data.attempts.push(day('2026-11-09', 8, 10), day('2026-11-10', 7, 10), day('2026-11-11', 5, 10));
  // tuần 16–22/11: 3 ngày đạt → thắng ngay khi đủ, không cần chờ hết tuần
  data.attempts.push(day('2026-11-16', 9, 10), day('2026-11-18', 7, 10));
  let pend = P.evaluate(data, sat);
  assert.deepEqual(pend.map((x) => [x.week, x.ok, x.count]), [['2026-11-09', false, 2]]); // tuần hiện tại mới 2 ngày: chưa chốt
  data.attempts.push(day('2026-11-20', 7, 10));
  pend = P.evaluate(data, sat);
  assert.deepEqual(pend.map((x) => [x.week, x.ok, x.count]), [['2026-11-09', false, 2], ['2026-11-16', true, 3]]);
  P.markShown(data, '2026-11-09'); P.markShown(data, '2026-11-16');
  assert.equal(P.evaluate(data, sat).length, 0); // đã báo thì không báo lại
  assert.equal(P.rewardState(data, sat).pending, 1);
  P.giveReward(data);
  assert.equal(P.rewardState(data, sat).pending, 0);
  // bật thưởng: bắt đầu tính từ thứ Hai tuần sau, tắt thì xóa mốc
  const d2 = { attempts: [] }; P.setReward(d2, { on: true, days: 4 });
  assert.ok(d2.reward.from > '2026-01-01');
  assert.equal(new Date(d2.reward.from + 'T00:00:00').getDay(), 1);
  assert.equal(P.setReward(d2, { on: false }).reward.from, '');
  assert.equal(P.cleanReward({ days: 99, pct: 5, text: 'x'.repeat(200) }).days, 7);
});

test('bài cần làm lại: chỉ lần làm gần nhất chưa đạt ngưỡng, theo ngưỡng riêng từng môn', () => {
  const P = require('../renderer/progress.js');
  const data = P.load(null);
  const at = (lessonId, subject, grade, correct, total, t) => data.attempts.push({ t, subject, grade, lessonId, lesson: lessonId, chapter: '', correct, total });
  at('toan/a', 'toan', 8, 6, 10, 1);   // 60% chưa đạt
  at('toan/b', 'toan', 8, 6, 10, 2);   // 60%, rồi làm lại đạt
  at('toan/b', 'toan', 8, 9, 10, 3);   // 90% đạt => không còn trong danh sách
  at('sinh/c', 'sinh', 8, 7, 10, 4);   // 70% chưa đạt với ngưỡng 80
  at('van/d', 'van', 9, 5, 10, 5);     // lớp khác
  at('ly/e', 'ly', 8, 0, 0, 6);        // chưa có câu
  let l = P.redoList(data, 8);
  assert.deepEqual(l.map((x) => x.lessonId), ['sinh/c', 'toan/a']);
  assert.equal(l[0].pct, 70); assert.equal(l[0].need, 80);
  assert.equal(P.redoList(data, 0).length, 3);
  data.goals.passBy = { sinh: 70 };      // ngưỡng riêng 70% => sinh/c đạt
  l = P.redoList(data, 8);
  assert.deepEqual(l.map((x) => x.lessonId), ['toan/a']);
});

test('làm lại bài: thứ tự câu hỏi và vị trí đáp án khác lượt trước', () => {
  const fs = require('node:fs'); const vm = require('node:vm');
  const src = fs.readFileSync(require('node:path').join(__dirname, '../renderer/app.js'), 'utf8');
  const grab = (re) => re.exec(src)[0];
  const code = [grab(/function shuffle\(arr\) \{[\s\S]*?\n\}\n/), grab(/const LEVEL_ORDER[^\n]*\n/), grab(/function orderedQuestionIndexes\(lesson\) \{[\s\S]*?\n\}\n/), grab(/const lastOrders = \{\};\nfunction newAttempt\(lesson\) \{[\s\S]*?\n\}\n/)].join('\n');
  const ctx = {}; vm.runInNewContext(code + '; this.newAttempt = newAttempt;', ctx);
  const items = Array.from({ length: 6 }, (_, i) => ({ id: 'q' + i, level: 'Hiểu', type: 'mcq', choices: ['A', 'B', 'C', 'D'] }));
  const lesson = { items };
  let prev = JSON.stringify(ctx.newAttempt(lesson).questions) + 'x';
  const seen = new Set();
  for (let i = 0; i < 30; i++) {
    const a = ctx.newAttempt(lesson);
    const sig = JSON.stringify({ q: a.questions, o: a.order });
    assert.notEqual(sig, prev); prev = sig; seen.add(sig);
    items.forEach((it) => assert.deepEqual([...a.order[it.id]].sort(), [0, 1, 2, 3]));
  }
  assert.ok(seen.size > 20);
});

test('tóm tắt ôn lại cho phụ huynh: bài đang cần ôn, và lần làm lại bài trước đó không đạt (kèm % trước và sau)', () => {
  const P2 = require('../renderer/progress.js');
  const now = new Date(2026, 10, 25, 10, 0, 0).getTime();
  const data = P2.load(null);
  const at = (lessonId, subject, correct, total, t) => data.attempts.push({ t, subject, grade: 8, lessonId, lesson: lessonId, chapter: 'C', correct, total });
  at('toan/a', 'toan', 5, 10, now - 3 * DAY);   // 50% chưa đạt
  at('toan/a', 'toan', 9, 10, now - 1 * DAY + 3600000); // làm lại 90% đạt, muộn hơn sinh/b
  at('sinh/b', 'sinh', 6, 10, now - 2 * DAY);   // 60% chưa đạt
  at('sinh/b', 'sinh', 7, 10, now - 1 * DAY);   // làm lại 70% vẫn chưa đạt
  at('ly/c', 'ly', 9, 10, now - 1 * DAY);       // đạt ngay, không phải ôn
  at('hoa/d', 'hoa', 3, 10, now - 40 * DAY);    // quá 30 ngày
  at('hoa/d', 'hoa', 8, 10, now - 39 * DAY);
  const r = P2.redoSummary(data, now);
  assert.deepEqual(r.pending.map((x) => x.lesson), ['sinh/b', 'hoa/d'].filter((x) => x === 'sinh/b'));
  assert.equal(r.pending[0].pct, 70);
  assert.deepEqual(r.done.map((x) => [x.lesson, x.from, x.to, x.passed]), [['toan/a', 50, 90, true], ['sinh/b', 60, 70, false]]);
});

test('máy con gửi tóm tắt ôn lại, bridge exe và apk cho phép, app Phụ huynh có màn hình xem', () => {
  const fs = require('node:fs'); const path = require('node:path');
  const rd = (f) => fs.readFileSync(path.join(__dirname, '..', f), 'utf8');
  assert.match(rd('renderer/progress-sync.js'), /redoSummary/);
  for (const f of ['main/orders.js', 'mobile/bridge/api.js']) assert.match(rd(f), /redo:/);
  assert.match(rd('parent/index.html'), /id="go-redo"/); assert.match(rd('parent/index.html'), /id="redo"/);
  assert.match(rd('parent/parent.js'), /'redo'/);
});

test('mở bài từ "Bài cần làm lại": Quay lại về đúng màn hình đã bấm, không về danh sách bài của môn chưa mở', () => {
  const fs = require('node:fs'); const path = require('node:path'); const vm = require('node:vm');
  const rd = (f) => fs.readFileSync(path.join(__dirname, '..', f), 'utf8');
  const app = rd('renderer/app.js');
  assert.match(app, /btn-back'\)\.addEventListener\('click', leaveLesson\)/);
  assert.match(app, /async function openLesson\(relPath, mode = 'practice', back = null\)/);
  assert.match(rd('renderer/progress-ui.js'), /openLesson\(x\.lessonId, 'practice', \(\) =>/);
  // Chạy thật leaveLesson với các màn hình giả
  const grab = (re) => re.exec(app)[0];
  const code = grab(/let lessonBack = null;\nfunction leaveLesson\(\) \{[\s\S]*?\n\}\n/);
  const calls = []; const crumb = { textContent: 'x' };
  const ctx = { document: { getElementById: () => crumb }, showOnly: (id) => calls.push('only:' + id), showLaunch: () => calls.push('launch') };
  vm.runInNewContext(code + '; this.set = (f) => { lessonBack = f; }; this.leave = leaveLesson;', ctx);
  ctx.leave(); assert.deepEqual(calls, ['only:home']);                       // mở từ danh sách môn: như cũ
  calls.length = 0; ctx.set(() => calls.push('custom')); ctx.leave(); ctx.leave();
  assert.deepEqual(calls, ['custom', 'only:home']);                           // dùng một lần rồi trả về mặc định
  calls.length = 0; ctx.set(() => { throw new Error('x'); }); ctx.leave();
  assert.deepEqual(calls, ['launch']);                                        // lỗi thì vẫn về màn hình chính
  assert.equal(crumb.textContent, '');
});
