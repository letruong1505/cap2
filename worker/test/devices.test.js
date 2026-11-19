import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, claimDevice, reissueOrder, getOrder, getSlots, listOrders, ping, pinReset, revokeOrder, createPartnerCode, HttpError } from '../src/orders.js';

const PC = 'B6F5-AB86-A5A1';
const PHONE = 'ABCD-1234-5678';
const PHONE2 = 'ABCD-1234-9999';
const NOW = new Date('2026-11-18T10:00:00Z');
const rand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);
const base = { name: 'Nguyễn Văn An', phone: '0912345678', ids: ['gia-su-ai'], terms: { version: '1.2', at: 'x' } };

async function paid(platform, machine) {
  const db = fakeD1();
  const env = { ...testEnv().env, DB: db };
  const o = await createOrder(db, catalog, { ...base, machineId: machine, platform }, NOW, rand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ' + o.code }, NOW);
  return { db, env, code: o.code };
}
const machineOf = (key) => JSON.parse(Buffer.from(key.slice(4).split('.')[0], 'base64url').toString()).machine;

test('mua trên máy tính rồi nhận khóa điện thoại bằng mã đơn + số điện thoại', async () => {
  const { db, env, code } = await paid('win', PC);
  const r = await claimDevice(db, env, catalog, { code, phone: '0912 345 678', machineId: PHONE, platform: 'android' }, NOW);
  assert.equal(r.platform, 'android');
  assert.equal(machineOf(r.key), PHONE);
  assert.equal(machineOf((await getOrder(db, code)).key), PC); // khóa máy tính không đổi
  // gọi lại trên cùng điện thoại: trả đúng khóa cũ
  assert.equal((await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW)).key, r.key);
});

test('điện thoại thứ hai bị từ chối, sai số điện thoại hoặc đơn chưa trả tiền cũng bị từ chối', async () => {
  const { db, env, code } = await paid('win', PC);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  await assert.rejects(claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE2, platform: 'android' }, NOW), (e) => e.status === 409);
  await assert.rejects(claimDevice(db, env, catalog, { code, phone: '0999999999', machineId: PHONE2, platform: 'android' }, NOW), (e) => e.status === 404);
  const db2 = fakeD1(); const o = await createOrder(db2, catalog, { ...base, machineId: PC }, NOW, rand);
  await assert.rejects(claimDevice(db2, { ...testEnv().env, DB: db2 }, catalog, { code: o.code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW), (e) => e.status === 404);
});

test('mua trên điện thoại trước: khóa gắn máy điện thoại, nhận thêm khóa máy tính sau', async () => {
  const { db, env, code } = await paid('android', PHONE);
  assert.equal(machineOf((await getOrder(db, code)).key), PHONE);
  const slots = await getSlots(db, await getOrder(db, code));
  assert.equal(slots.android.machine, PHONE); assert.equal(slots.win, null);
  const r = await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PC, platform: 'win' }, NOW);
  assert.equal(machineOf(r.key), PC);
  assert.equal(machineOf((await getOrder(db, code)).key), PHONE);
});

test('đơn cũ (chưa có dòng chỗ thiết bị) vẫn coi máy đặt đơn là máy tính và nhận được điện thoại', async () => {
  const { db, env, code } = await paid('win', PC);
  await db.prepare('DELETE FROM order_devices WHERE code = ?1').bind(code).run();
  const slots = await getSlots(db, await getOrder(db, code));
  assert.equal(slots.win.machine, PC);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  const after = await getSlots(db, await getOrder(db, code));
  assert.equal(after.win.machine, PC); assert.equal(after.android.machine, PHONE);
});

test('đổi thiết bị theo từng chỗ: đổi điện thoại không đụng khóa máy tính và ngược lại', async () => {
  const { db, env, code } = await paid('win', PC);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  const k1 = await reissueOrder(db, env, catalog, code, PHONE2, NOW, 'android');
  assert.equal(machineOf(k1), PHONE2);
  const NEWPC = 'FFFF-0000-1111';
  const k2 = await reissueOrder(db, env, catalog, code, NEWPC, NOW, 'win');
  assert.equal(machineOf(k2), NEWPC);
  const o = await getOrder(db, code);
  assert.equal(o.machine, NEWPC); assert.equal(machineOf(o.key), NEWPC);
  const s = await getSlots(db, o);
  assert.equal(s.android.machine, PHONE2); assert.equal(s.win.machine, NEWPC);
});

test('khóa cấp cho điện thoại có đủ nội dung khóa bản quyền của đơn', async () => {
  const { db, env, code } = await paid('win', PC);
  const r = await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  const p = JSON.parse(Buffer.from(r.key.slice(4).split('.')[0], 'base64url').toString());
  assert.equal(p.v, 1); assert.equal(p.id, 'NL-' + code); assert.deepEqual(p.courses, ['gia-su-ai']); assert.equal(p.expires, 'never');
  assert.ok(r.key.startsWith('NL1-'));
});

test('quản trị: hiện 2 chỗ và đánh dấu máy lạ khi máy không thuộc chỗ nào', async () => {
  const { db, env, code } = await paid('win', PC);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  await ping(db, { machineId: PC, ids: [code], version: '1.2.23' }, NOW, catalog);
  await ping(db, { machineId: PHONE, ids: [code], version: '1.0.0' }, NOW, catalog);
  await ping(db, { machineId: 'DEAD-BEEF-0000', ids: [code], version: '1.0.0' }, NOW, catalog);
  const o = (await listOrders(db, {}, NOW))[0];
  assert.equal(o.slots.win.machine, PC); assert.equal(o.slots.android.machine, PHONE);
  const by = Object.fromEntries(o.devices.map((d) => [d.machine, d]));
  assert.equal(by[PC].stranger, false); assert.equal(by[PC].platform, 'win');
  assert.equal(by[PHONE].stranger, false); assert.equal(by[PHONE].platform, 'android');
  assert.equal(by['DEAD-BEEF-0000'].stranger, true);
});

test('thu hồi đơn khóa cả hai thiết bị; đơn bị thu hồi không nhận được khóa mới', async () => {
  const { db, env, code } = await paid('win', PC);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  await revokeOrder(db, code, 'hoàn tiền', NOW);
  assert.deepEqual((await ping(db, { machineId: PHONE, ids: [code] }, NOW, catalog)).revoked, [code]);
  assert.deepEqual((await ping(db, { machineId: PC, ids: [code] }, NOW, catalog)).revoked, [code]);
  await assert.rejects(claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: 'AAAA-AAAA-AAAA', platform: 'win' }, NOW), (e) => e.status === 403);
});

test('đặt lại PIN dùng được trên cả điện thoại đã nhận khóa', async () => {
  const { db, env, code } = await paid('win', PC);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  assert.deepEqual(await pinReset(db, { code, phone: '0912345678', machineId: PHONE }, NOW), { ok: true });
  await assert.rejects(pinReset(db, { code, phone: '0912345678', machineId: PHONE2 }, NOW), HttpError);
});

test('giới hạn máy của mã đối tác đếm cả điện thoại', async () => {
  const db = fakeD1(); const env = { ...testEnv().env, DB: db };
  await createPartnerCode(db, { code: 'DT-X', partner: 'Đối tác X', percent: 20, maxMachines: 2 }, NOW);
  const o = await createOrder(db, catalog, { ...base, machineId: PC, partnerCode: 'DT-X' }, NOW, rand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ' + o.code }, NOW);
  await claimDevice(db, env, catalog, { code: o.code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  await assert.rejects(createOrder(db, catalog, { ...base, machineId: PHONE2, partnerCode: 'DT-X' }, NOW, () => Uint8Array.from([9, 1, 2, 3, 4, 5])), (e) => e.status === 403);
});

test('giới hạn thử: 5 lần nhập sai thì chặn, nhận khóa thành công không bị tính vào giới hạn', async () => {
  const { db, env, code } = await paid('win', PC);
  for (let i = 0; i < 4; i++) await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW);
  await claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW); // lần thứ 5 vẫn được
  for (let i = 0; i < 5; i++) await assert.rejects(claimDevice(db, env, catalog, { code, phone: '0900000000', machineId: PHONE, platform: 'android' }, NOW), (e) => e.status === 404);
  await assert.rejects(claimDevice(db, env, catalog, { code, phone: '0912345678', machineId: PHONE, platform: 'android' }, NOW), (e) => e.status === 429);
});
