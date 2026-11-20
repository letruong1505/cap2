import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1 } from './helpers.js';
import { getOrder, getSlots } from '../src/orders.js';
import { importLegacy } from '../src/legacy.js';
import { progressSettings, progressPush, progressView } from '../src/progress.js';

const NOW = new Date('2026-11-20T03:00:00Z');
const PC = 'B6F5-AB86-A5A1';
const base = { code: 'NL-SGPTWN', name: 'Lê Trường', phone: '0912 345 678', machine: PC, grades: [9, 12], courses: [], issued: '2026-09-01', key: 'NL1-abc.def' };

test('nhập khóa cũ: tạo đơn đã thanh toán 0 đ, chỗ máy tính đúng mã máy', async () => {
  const db = fakeD1();
  const r = await importLegacy(db, catalog, base, NOW);
  assert.deepEqual(r.items, ['van-hoa-9', 'van-hoa-12']);
  const o = await getOrder(db, 'SGPTWN');
  assert.deepEqual([o.status, o.amount, o.paid_amount, o.phone, o.machine, o.terms_version], ['paid', 0, 0, '0912345678', PC, 'usb-cũ']);
  assert.match(o.note, /USB/);
  const slots = await getSlots(db, o);
  assert.equal(slots.win.machine, PC);
  assert.equal((await db.prepare('SELECT COUNT(*) AS n FROM order_prices WHERE code = ?1 AND paid_price = 0').bind('SGPTWN').first()).n, 2);
  await assert.rejects(importLegacy(db, catalog, base, NOW), (e) => e.status === 409); // nhập lại: không trùng
});

test('khóa mọi lớp (grades all) và khóa học Kỹ năng; dữ liệu sai bị từ chối', async () => {
  const db = fakeD1();
  const all = await importLegacy(db, catalog, { ...base, grades: 'all' }, NOW);
  assert.ok(all.items.length >= 7 && all.items.every((id) => /^van-hoa-\d+$/.test(id)));
  const bad = [{ code: 'NL-0001' }, { name: 'A' }, { phone: '123' }, { machine: '*' }, { grades: [99] }, { grades: [], courses: [] }];
  for (const b of bad) await assert.rejects(importLegacy(fakeD1(), catalog, { ...base, ...b }, NOW), (e) => e.status === 400, JSON.stringify(b));
});

test('sau khi nhập: máy gửi được kết quả học và phụ huynh xem được bằng mã đơn + số điện thoại', async () => {
  const db = fakeD1();
  await importLegacy(db, catalog, base, NOW);
  await progressSettings(db, { code: 'SGPTWN', machineId: PC, enabled: true }, NOW);
  await progressPush(db, { code: 'SGPTWN', machineId: PC, days: [{ day: '2026-11-19', subject: 'toan', grade: 9, chapter: 'A', correct: 4, total: 5, lessons: 1, seconds: 60 }] }, NOW);
  const v = await progressView(db, catalog, { code: 'sgptwn', phone: '0912345678', machineId: 'ABCD-1234-5678' }, NOW);
  assert.deepEqual([v.enabled, v.rows.length, v.courses.map((c) => c.grade)], [true, 1, [9, 12]]);
});
