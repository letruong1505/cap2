import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, getSlots, getOrder } from '../src/orders.js';
import { createFamily, syncFamily } from '../src/family.js';

const PARENT = 'AAAA-1111-2222';
const PC = 'B6F5-AB86-A5A1';
const PC2 = 'B6F5-AB86-0000';
const PHONE = 'ABCD-1234-5678';
const NOW = new Date('2026-11-22T10:00:00Z');
const rand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);
let txn = 100;
const T = { version: '1.2', at: 'x' };
const machineOf = (key) => JSON.parse(Buffer.from(key.slice(4).split('.')[0], 'base64url').toString()).machine;
const coursesOf = (key) => JSON.parse(Buffer.from(key.slice(4).split('.')[0], 'base64url').toString()).courses;

async function setup() {
  const db = fakeD1();
  const env = { ...testEnv().env, DB: db };
  const { fcode } = await createFamily(db, { machineId: PARENT, phone: '0912 345 678' }, NOW);
  return { db, env, fcode };
}
async function buy(db, env, fcode, ids = ['tu-duy-lap-trinh']) {
  const o = await createOrder(db, catalog, { name: 'Phụ huynh', phone: '0912345678', ids, terms: T, machineId: PARENT, family: fcode }, NOW, rand);
  await applyPayment(db, env, catalog, { id: ++txn, amount: o.amount, content: 'NL ' + o.code }, NOW);
  return o.code;
}

test('mã gia đình: xin lại trả về mã cũ, số điện thoại sai bị từ chối', async () => {
  const { db, fcode } = await setup();
  assert.match(fcode, /^[A-Z0-9]{8}$/);
  assert.equal((await createFamily(db, { machineId: PARENT, phone: '0912345678' }, NOW)).fcode, fcode);
  await assert.rejects(createFamily(db, { machineId: PARENT, phone: '123' }, NOW), (e) => e.status === 400);
});

test('đơn gia đình không chiếm chỗ máy của phụ huynh; con nhận khóa máy tính và điện thoại', async () => {
  const { db, env, fcode } = await setup();
  const code = await buy(db, env, fcode);
  const slots = await getSlots(db, await getOrder(db, code));
  assert.equal(slots.win, null); assert.equal(slots.android, null);
  const pc = await syncFamily(db, env, catalog, { fcode, machineId: PC, platform: 'win' }, NOW);
  assert.equal(pc.keys.length, 1);
  assert.equal(machineOf(pc.keys[0].key), PC);
  assert.ok(coursesOf(pc.keys[0].key).includes('tu-duy-lap-trinh'));
  const ph = await syncFamily(db, env, catalog, { fcode, machineId: PHONE, platform: 'android' }, NOW);
  assert.equal(machineOf(ph.keys[0].key), PHONE);
  // đồng bộ lại: cùng khóa
  assert.equal((await syncFamily(db, env, catalog, { fcode, machineId: PC, platform: 'win' }, NOW)).keys[0].key, pc.keys[0].key);
});

test('máy tính thứ hai không nhận được đơn đã đủ chỗ; đơn mới thì nhận', async () => {
  const { db, env, fcode } = await setup();
  await buy(db, env, fcode);
  await syncFamily(db, env, catalog, { fcode, machineId: PC, platform: 'win' }, NOW);
  const r = await syncFamily(db, env, catalog, { fcode, machineId: PC2, platform: 'win' }, NOW);
  assert.equal(r.keys.length, 0); assert.equal(r.full, 1);
  await buy(db, env, fcode, ['gia-su-ai']).catch(() => {});
});

test('máy của con tự nhận thêm khóa của đơn mua sau', async () => {
  const { db, env, fcode } = await setup();
  await buy(db, env, fcode);
  assert.equal((await syncFamily(db, env, catalog, { fcode, machineId: PC, platform: 'win' }, NOW)).keys.length, 1);
  const o2 = await createOrder(db, catalog, { name: 'Phụ huynh', phone: '0912345678', ids: ['gia-su-ai'], terms: T, machineId: PARENT, family: fcode }, NOW, () => Uint8Array.from([9, 8, 7, 6, 5, 4]));
  await applyPayment(db, env, catalog, { id: 99, amount: o2.amount, content: 'NL ' + o2.code }, NOW);
  assert.equal((await syncFamily(db, env, catalog, { fcode, machineId: PC, platform: 'win' }, NOW)).keys.length, 2);
});

test('đơn chưa thanh toán không có khóa; mã gia đình sai bị chặn và giới hạn thử', async () => {
  const { db, env, fcode } = await setup();
  await createOrder(db, catalog, { name: 'Phụ huynh', phone: '0912345678', ids: ['tu-duy-lap-trinh'], terms: T, machineId: PARENT, family: fcode }, NOW, rand);
  assert.equal((await syncFamily(db, env, catalog, { fcode, machineId: PC, platform: 'win' }, NOW)).keys.length, 0);
  for (let i = 0; i < 5; i++) await assert.rejects(syncFamily(db, env, catalog, { fcode: 'ZZZZZZZZ', machineId: PC2, platform: 'win' }, NOW), (e) => e.status === 404);
  await assert.rejects(syncFamily(db, env, catalog, { fcode, machineId: PC2, platform: 'win' }, NOW), (e) => e.status === 429);
});

test('mã gia đình của người khác (máy hoặc số điện thoại không khớp) không tạo được đơn', async () => {
  const { db, fcode } = await setup();
  await assert.rejects(createOrder(db, catalog, { name: 'Kẻ lạ', phone: '0999999999', ids: ['tu-duy-lap-trinh'], terms: T, machineId: PARENT, family: fcode }, NOW, rand), (e) => e.status === 404);
  await assert.rejects(createOrder(db, catalog, { name: 'Kẻ lạ', phone: '0912345678', ids: ['tu-duy-lap-trinh'], terms: T, machineId: 'CCCC-1111-2222', family: fcode }, NOW, rand), (e) => e.status === 404);
});
