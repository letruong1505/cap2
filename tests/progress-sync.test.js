const test = require('node:test');
const assert = require('node:assert/strict');
const S = require('../renderer/progress-sync.js');
const P = require('../renderer/progress.js');

const at = (y, m, d, h = 10) => new Date(y, m - 1, d, h).getTime();
const NOW = at(2026, 11, 18, 12);
const att = (t, o = {}) => Object.assign({ t, subject: 'toan', grade: 9, lessonId: 'l1', lesson: 'Bài 1', chapter: 'Chương 1', correct: 4, total: 5, pts: 40, seconds: 120 }, o);

test('mã đơn lấy từ id khóa NL-xxxxxx', () => {
  assert.equal(S.codeFromLicense({ id: 'NL-3KAHFK' }), '3KAHFK');
  assert.equal(S.codeFromLicense({ id: 'NL-3KAHFK, NL-BBBBBB' }), '3KAHFK');
  assert.equal(S.codeFromLicense({ id: '' }), '');
  assert.equal(S.codeFromLicense(null), '');
});

test('aggregate gom theo ngày × môn × lớp × chương, không có câu trả lời riêng lẻ', () => {
  const rows = S.aggregate([
    att(at(2026, 11, 17, 9)), att(at(2026, 11, 17, 20), { correct: 3, total: 5, seconds: 60 }),
    att(at(2026, 11, 17, 21), { chapter: 'Chương 2' }), att(at(2026, 11, 18), { subject: 'ly', grade: 12 }),
    att(at(2025, 1, 1)), // quá 120 ngày
    { t: at(2026, 11, 18), subject: '', grade: 9, chapter: 'x', correct: 1, total: 1 }, // thiếu môn
    att(at(2026, 11, 18), { chapter: '', lesson: '' }), // thiếu tên chương
  ], NOW);
  assert.equal(rowsKeys(rows).length, 3);
  const c1 = rows.find((r) => r.day === '2026-11-17' && r.chapter === 'Chương 1');
  assert.deepEqual([c1.correct, c1.total, c1.lessons, c1.seconds], [7, 10, 2, 180]);
  assert.equal(rows[0].day, '2026-11-18'); // ngày mới nhất trước
  rows.forEach((r) => assert.deepEqual(Object.keys(r).sort(), ['chapter', 'correct', 'day', 'grade', 'lessons', 'seconds', 'subject', 'total']));
});
function rowsKeys(rows) { return rows.map((r) => [r.day, r.subject, r.grade, r.chapter].join('|')); }

test('aggregate dùng tên bài khi nhật ký không có chương, và giới hạn số dòng', () => {
  const r = S.aggregate([att(at(2026, 11, 17), { chapter: undefined, lesson: 'Bài X' })], NOW);
  assert.equal(r[0].chapter, 'Bài X');
  const many = []; for (let i = 0; i < 2000; i++) many.push(att(at(2026, 11, 17), { chapter: 'C' + i }));
  assert.equal(S.aggregate(many, NOW).length, 1500);
});

test('buildReport cho kết quả giống báo cáo trên máy tính từ cùng dữ liệu', () => {
  const attempts = [
    att(at(2026, 11, 16)), att(at(2026, 11, 17), { correct: 1, total: 5 }), att(at(2026, 11, 17, 15), { correct: 1, total: 5 }),
    att(at(2026, 11, 18), { subject: 'ly', grade: 12, chapter: 'Điện', correct: 5, total: 5 }),
  ];
  const data = { attempts, notebook: [], reviews: [], goals: { daily: 5, weekly: 3 } };
  const range = { from: at(2026, 11, 12), to: at(2026, 11, 18) };
  const local = P.report(data, range, NOW);
  const remote = S.buildReport(S.aggregate(attempts, NOW), range, data.goals);
  for (const k of ['correct', 'wrong', 'total', 'pct', 'minutes', 'attempts', 'activeDays']) assert.equal(remote[k], local[k], k);
  assert.deepEqual(remote.days.map((d) => [d.t, d.correct, d.total, d.reached]), local.days.map((d) => [d.t, d.correct, d.total, d.reached]));
  assert.deepEqual(remote.subjects.map((s) => [s.subject, s.grade, s.correct, s.total]), local.subjects.map((s) => [s.subject, s.grade, s.correct, s.total]));
  assert.deepEqual(remote.weak.map((w) => [w.name, w.pct]), local.weak.map((w) => [w.name, w.pct]));
  const g12 = S.buildReport(S.aggregate(attempts, NOW), { ...range, grade: 12 }, data.goals);
  assert.deepEqual([g12.total, g12.subjects.length], [5, 1]);
  const ly = S.buildReport(S.aggregate(attempts, NOW), { ...range, subject: 'ly' }, data.goals);
  assert.equal(ly.total, 5);
});

test('buildReport với dữ liệu rỗng không lỗi', () => {
  const r = S.buildReport([], { from: at(2026, 11, 12), to: at(2026, 11, 18) }, null);
  assert.deepEqual([r.total, r.days.length, r.activeDays, r.pct], [0, 7, 0, 0]);
});
