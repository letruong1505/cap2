const test = require('node:test');
const assert = require('node:assert');
const T = require('../renderer/timetable.js');

const d = (s, h = 12) => { const [y, m, x] = s.split('-').map(Number); return new Date(y, m - 1, x, h, 0, 0); };
const mk = (week, days) => ({ v: 1, remindOn: true, remindHour: 19, grades: { 12: { week, days: Object.assign({ 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] }, days) } } });

test('khóa tuần: Chủ nhật tính vào tuần tới', () => {
  assert.strictEqual(T.weekKey(d('2026-11-23')), '2026-11-23'); // thứ hai
  assert.strictEqual(T.weekKey(d('2026-11-28')), '2026-11-23'); // thứ bảy
  assert.strictEqual(T.weekKey(d('2026-11-29')), '2026-11-30'); // chủ nhật
});

test('lưu thay hẳn bản cũ và loại trùng', () => {
  const data = T.normalize(null);
  T.setTimetable(data, 12, { 1: ['toan', 'toan', 'ly'] }, d('2026-11-22'));
  T.setTimetable(data, 12, { 2: ['hoa'] }, d('2026-11-23'));
  assert.deepStrictEqual(data.grades[12].days[1], []);
  assert.deepStrictEqual(data.grades[12].days[2], ['hoa']);
  assert.strictEqual(data.grades[12].week, '2026-11-23');
});

test('nhắc tối hôm trước: chỉ từ giờ nhắc và chỉ ngày có môn', () => {
  const data = mk('2026-11-23', { 1: ['toan', 'x:Ngữ văn'], 3: ['ly'] });
  assert.strictEqual(T.reminderFor(data, 12, d('2026-11-22', 18)), null); // chưa đến 19:00
  const r = T.reminderFor(data, 12, d('2026-11-22', 19)); // chủ nhật tối, mai thứ hai
  assert.deepStrictEqual(r.items, ['toan', 'x:Ngữ văn']); assert.strictEqual(r.dayName, 'Thứ hai');
  assert.strictEqual(T.reminderFor(data, 12, d('2026-11-23', 20)), null); // mai thứ ba không có môn
  assert.strictEqual(T.reminderFor(data, 12, d('2026-11-27', 20)), null); // mai thứ bảy trống
  assert.strictEqual(T.reminderFor(data, 12, d('2026-11-28', 20)), null); // mai chủ nhật
  data.remindOn = false;
  assert.strictEqual(T.reminderFor(data, 12, d('2026-11-22', 19)), null);
});

test('cờ cũ khi chưa nhập cho tuần mới', () => {
  const data = mk('2026-11-23', { 1: ['toan'] });
  assert.strictEqual(T.isStale(data, 12, d('2026-11-25')), false);
  assert.strictEqual(T.isStale(data, 12, d('2026-11-29')), true); // chủ nhật: sang tuần mới
  assert.strictEqual(T.reminderFor(data, 12, d('2026-11-29', 19)).stale, true);
  assert.strictEqual(T.isStale(data, 11, d('2026-11-25')), true);
});

test('kế hoạch thông báo: đúng giờ, bỏ giờ đã qua, id không trùng', () => {
  const data = mk('2026-11-23', { 1: ['toan', 'ly'], 2: ['hoa'] });
  const p = T.plan(data, d('2026-11-22', 12), { toan: 'Toán', ly: 'Vật lí', hoa: 'Hoá học' });
  assert.ok(p.length > 0);
  assert.ok(p.every((x) => x.at > d('2026-11-22', 12).getTime()));
  assert.strictEqual(T.plan(data, d('2026-11-22', 20), {})[0].body.includes('Thứ ba'), true); // 19:00 chủ nhật đã qua
  assert.strictEqual(new Set(p.map((x) => x.id)).size, p.length);
  const first = p[0]; assert.strictEqual(new Date(first.at).getHours(), 19);
  assert.match(first.body, /Toán, Vật lí/);
  assert.ok(p.every((x) => x.id < 2147483647));
  assert.deepStrictEqual(T.plan(Object.assign(data, { remindOn: false }), d('2026-11-22', 20), {}), []);
});

test('nhắc chủ nhật dặn cập nhật thời khóa biểu tuần mới', () => {
  const data = mk('2026-11-23', { 1: ['toan'] });
  const p = T.plan(data, d('2026-11-28', 8), { toan: 'Toán' }); // thông báo tối chủ nhật 29/11 cho thứ hai 30/11
  assert.match(p[0].body, /cập nhật thời khóa biểu/);
});

test('thời khóa biểu sáng/chiều: buổi không có môn được báo nghỉ trong nhắc và thông báo', () => {
  const data = mk('2026-11-23', { 2: ['toan', 'ly'] });
  data.grades[12].pm = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] };
  const r = T.reminderFor(data, 12, d('2026-11-23', 20)); // tối thứ hai, nhắc ngày thứ ba
  assert.deepStrictEqual(r.sang, ['toan', 'ly']);
  assert.deepStrictEqual(r.chieu, []);
  const p = T.plan(data, d('2026-11-23', 8), { toan: 'Toán', ly: 'Vật lí' });
  const tue = p.find((x) => x.body.includes('Thứ ba'));
  assert.ok(tue.body.includes('Sáng: Toán, Vật lí.'));
  assert.ok(tue.body.includes('Chiều nghỉ.'));
});

test('thời khóa biểu sáng/chiều: lưu cả hai buổi, chỉ có chiều thì sáng báo nghỉ, dữ liệu cũ vẫn đọc được', () => {
  const data = T.normalize(null);
  T.setTimetable(data, 12, { 3: ['toan'] }, d('2026-11-24'), { 3: ['anh'], 4: ['hoa'] });
  const t = data.grades[12];
  assert.deepStrictEqual(T.sessionsOf(t, 3), { s: ['toan'], c: ['anh'] });
  assert.strictEqual(T.sessionText(T.sessionsOf(t, 4), {}), 'Sáng nghỉ. Chiều: hoa.');
  assert.strictEqual(T.sessionText(T.sessionsOf(t, 5), {}), 'Sáng nghỉ. Chiều nghỉ.');
  assert.strictEqual(T.isEmptyTT(t), false);
  const old = T.normalize({ grades: { 12: { week: '2026-11-23', days: { 1: ['toan'] } } } });
  assert.deepStrictEqual(old.grades[12].pm[1], []);
  assert.strictEqual(T.isEmptyTT({ days: { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] }, pm: { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] } }), true);
});
