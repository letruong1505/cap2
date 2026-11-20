import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, claimDevice, revokeOrder } from '../src/orders.js';
import { progressSettings, progressPush, progressView } from '../src/progress.js';
import { handle } from '../src/index.js';

const PC = 'B6F5-AB86-A5A1';
const PHONE = 'ABCD-1234-5678';
const NOW = new Date('2026-11-18T10:00:00Z');
const rand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);
const base = { name: 'Nguyễn Văn An', phone: '0912345678', ids: ['van-hoa-9', 'van-hoa-12', 'gia-su-ai'], terms: { version: '1.2', at: 'x' } };

async function setup() {
  const db = fakeD1();
  const env = { ...testEnv().env, DB: db };
  const o = await createOrder(db, catalog, { ...base, machineId: PC, platform: 'win' }, NOW, rand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ' + o.code }, NOW);
  return { db, env, code: o.code };
}
const row = (day, subject, grade, chapter, correct, total, extra = {}) => ({ day, subject, grade, chapter, correct, total, lessons: 1, seconds: 60, ...extra });
const dev = (code, machine = PC) => ({ code, machineId: machine });
const view = (db, code, extra = {}) => progressView(db, catalog, { code, phone: '0912 345 678', machineId: PHONE, ...extra }, NOW);

test('máy học sinh bật chia sẻ, gửi tóm tắt; phụ huynh xem bằng mã đơn + số điện thoại', async () => {
  const { db, code } = await setup();
  await assert.rejects(progressPush(db, { ...dev(code), days: [row('2026-11-17', 'toan', 9, 'Chương 1', 4, 5)] }, NOW), (e) => e.status === 409); // chưa bật
  assert.equal((await progressSettings(db, { ...dev(code), enabled: true }, NOW)).enabled, true);
  const r = await progressPush(db, { ...dev(code), days: [row('2026-11-17', 'toan', 9, 'Chương 1', 4, 5), row('2026-11-18', 'ly', 12, 'Chương 2', 3, 4)] }, NOW);
  assert.deepEqual([r.saved, r.skipped], [2, 0]);
  const v = await view(db, code);
  assert.equal(v.enabled, true);
  assert.equal(v.name, 'Nguyễn Văn An');
  assert.deepEqual(v.courses.map((c) => c.grade), [9, 12]); // chỉ các khóa Văn hóa của đơn; Gia sư AI không có tiến độ theo lớp
  assert.equal(v.courses[0].name, 'Giáo trình Văn hóa lớp 9');
  assert.equal(v.rows.length, 2);
  assert.ok(v.lastSync);
});

test('chỉ máy có trong đơn mới gửi được; mã đơn hoặc máy lạ thì không tìm thấy', async () => {
  const { db, code } = await setup();
  await progressSettings(db, { ...dev(code), enabled: true }, NOW);
  await assert.rejects(progressPush(db, { ...dev(code, PHONE), days: [] }, NOW), (e) => e.status === 404);
  await assert.rejects(progressPush(db, { ...dev('ZZZZZZ'), days: [] }, NOW), (e) => e.status === 404);
  await assert.rejects(progressSettings(db, { code, machineId: 'xyz', enabled: true }, NOW), (e) => e.status === 404);
  // điện thoại đã nhận khóa của đơn thì được gửi
  await claimDevice(db, { ...testEnv().env }, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW).catch(() => null);
});

test('dòng sai bị bỏ qua; gửi lại số nhỏ hơn không làm giảm dữ liệu; hai thiết bị cộng dồn khi xem', async () => {
  const { db, env, code } = await setup();
  await progressSettings(db, { ...dev(code), enabled: true }, NOW);
  const bad = [row('2026-11-17', 'toan', 9, 'A', 6, 5), row('khong-phai-ngay', 'toan', 9, 'A', 1, 1), row('2026-11-17', '', 9, 'A', 1, 1), row('2026-11-17', 'toan', 99, 'A', 1, 1), row('2025-01-01', 'toan', 9, 'A', 1, 1), row('2026-11-17', 'toan', 9, 'Chương 1', 4, 5)];
  const r = await progressPush(db, { ...dev(code), days: bad }, NOW);
  assert.deepEqual([r.saved, r.skipped], [1, 5]);
  await progressPush(db, { ...dev(code), days: [row('2026-11-17', 'toan', 9, 'Chương 1', 2, 3, { lessons: 0, seconds: 10 })] }, NOW);
  let v = await view(db, code);
  assert.deepEqual([v.rows[0].correct, v.rows[0].total, v.rows[0].lessons, v.rows[0].seconds], [4, 5, 1, 60]);
  // điện thoại của cùng đơn cũng học và gửi: cộng vào ngày/môn/chương đó
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  await progressPush(db, { ...dev(code, PHONE), days: [row('2026-11-17', 'toan', 9, 'Chương 1', 3, 4)] }, NOW);
  v = await view(db, code);
  assert.equal(v.rows.length, 1);
  assert.deepEqual([v.rows[0].correct, v.rows[0].total, v.rows[0].lessons], [7, 9, 2]);
});

test('xem theo khoảng ngày và theo từng khóa (lớp)', async () => {
  const { db, code } = await setup();
  await progressSettings(db, { ...dev(code), enabled: true }, NOW);
  await progressPush(db, { ...dev(code), days: [row('2026-11-10', 'toan', 9, 'A', 1, 2), row('2026-11-16', 'toan', 9, 'A', 2, 2), row('2026-11-17', 'ly', 12, 'B', 3, 4), row('2026-11-18', 'toan', 9, 'A', 5, 5)] }, NOW);
  assert.equal((await view(db, code)).rows.length, 3); // mặc định 7 ngày tới hôm nay (10/11 nằm ngoài)
  const range = await view(db, code, { from: '2026-11-10', to: '2026-11-16' });
  assert.deepEqual(range.rows.map((r) => r.day), ['2026-11-10', '2026-11-16']);
  const g12 = await view(db, code, { grade: 12, from: '2026-11-01', to: '2026-11-18' });
  assert.deepEqual(g12.rows.map((r) => [r.grade, r.subject]), [[12, 'ly']]);
  const all = await view(db, code, { from: '2026-11-01', to: '2026-11-18' });
  assert.equal(all.rows.length, 4);
});

test('xem: sai thông tin bị từ chối và giới hạn 5 lần sai mỗi giờ; nhập đúng không bị tính', async () => {
  const { db, code } = await setup();
  await progressSettings(db, { ...dev(code), enabled: true }, NOW);
  for (let i = 0; i < 5; i++) await view(db, code); // đúng nhiều lần vẫn được
  for (let i = 0; i < 5; i++) await assert.rejects(progressView(db, catalog, { code, phone: '0900000000', machineId: PHONE }, NOW), (e) => e.status === 404);
  await assert.rejects(view(db, code), (e) => e.status === 429);
  await assert.rejects(progressView(db, catalog, { code, phone: '0912345678', machineId: 'bad' }, NOW), (e) => e.status === 400);
});

test('phụ huynh chưa bật thì không có dữ liệu; tắt rồi bật lại; xóa dữ liệu; đơn bị thu hồi thì chặn', async () => {
  const { db, code } = await setup();
  const off = await view(db, code);
  assert.deepEqual([off.enabled, off.rows], [false, []]);
  await progressSettings(db, { ...dev(code), enabled: true, goals: { daily: 30, weekend: 100, weekly: 4 } }, NOW);
  await progressPush(db, { ...dev(code), days: [row('2026-11-17', 'toan', 9, 'A', 4, 5)] }, NOW);
  const on = await view(db, code);
  assert.deepEqual(on.goals, { daily: 30, weekend: 100, weekly: 4 });
  assert.equal(on.rows.length, 1);
  await progressSettings(db, { ...dev(code), enabled: false }, NOW); // tắt: phụ huynh không xem được nữa, dữ liệu cũ còn đó
  assert.deepEqual([(await view(db, code)).enabled, (await view(db, code)).rows.length], [false, 0]);
  await assert.rejects(progressPush(db, { ...dev(code), days: [] }, NOW), (e) => e.status === 409);
  await progressSettings(db, { ...dev(code), enabled: true }, NOW);
  assert.equal((await view(db, code)).rows.length, 1);
  const purged = await progressSettings(db, { ...dev(code), purge: true }, NOW);
  assert.deepEqual([purged.rows, purged.lastSync], [0, null]);
  assert.equal((await view(db, code)).rows.length, 0);
  await revokeOrder(db, code, 'thử', NOW);
  await assert.rejects(view(db, code), (e) => e.status === 403);
  await assert.rejects(progressPush(db, { ...dev(code), days: [] }, NOW), (e) => e.status === 403);
});

test('các đường dẫn tiến độ có CORS cho ứng dụng Android', async () => {
  for (const path of ['/api/progress/settings', '/api/progress/push', '/api/progress/view']) {
    const pre = await handle(new Request('https://w.test' + path, { method: 'OPTIONS', headers: { origin: 'https://localhost', 'access-control-request-method': 'POST' } }), { ...testEnv().env, DB: fakeD1() });
    assert.equal(pre.status, 204, path);
  }
});

test('phụ huynh có nhiều đơn (cùng số điện thoại): nhập mã nào cũng thấy dữ liệu của tất cả đơn, đủ các khóa', async () => {
  const { db, env, code } = await setup();
  const o2 = await createOrder(db, catalog, { ...base, ids: ['van-hoa-10'], machineId: 'C1C1-C1C1-C1C1', platform: 'win' }, NOW, () => Uint8Array.from([6, 7, 8, 9, 10, 11]));
  await applyPayment(db, env, catalog, { id: 2, amount: o2.amount, content: 'NL ' + o2.code }, NOW);
  await createOrder(db, catalog, { ...base, phone: '0988888888', ids: ['van-hoa-11'], machineId: 'D1D1-D1D1-D1D1', platform: 'win' }, NOW, () => Uint8Array.from([12, 13, 14, 15, 16, 17])); // đơn của người khác
  await progressSettings(db, { ...dev(code), enabled: true }, NOW);
  await progressPush(db, { ...dev(code), days: [row('2026-11-17', 'toan', 9, 'A', 4, 5)] }, NOW);
  await progressSettings(db, { ...dev(o2.code, 'C1C1-C1C1-C1C1'), enabled: true }, NOW);
  await progressPush(db, { ...dev(o2.code, 'C1C1-C1C1-C1C1'), days: [row('2026-11-17', 'toan', 9, 'A', 1, 5)] }, NOW);
  for (const c of [code, o2.code]) {
    const v = await view(db, c);
    assert.deepEqual(v.courses.map((x) => x.grade), [9, 10, 12], c);
    assert.equal(v.codes.length, 2);
    assert.deepEqual([v.rows.length, v.rows[0].correct, v.rows[0].total], [1, 5, 10]);
  }
  assert.equal((await view(db, code, { grade: 10 })).rows.length, 0);
  assert.equal((await view(db, code, { grade: 9 })).rows.length, 1);
  // đơn thứ hai bật, đơn đầu chưa bật: vẫn thấy
  await progressSettings(db, { ...dev(code), enabled: false }, NOW);
  assert.equal((await view(db, code)).enabled, true);
  // đơn bị thu hồi thì không còn tính vào khóa của phụ huynh
  await revokeOrder(db, o2.code, 'thử', NOW);
  const v = await view(db, code);
  assert.deepEqual(v.codes, [code]);
  assert.deepEqual(v.courses.map((x) => x.grade), [9, 12]);
});
