import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, pinReset, HttpError } from '../src/orders.js';
import { handle } from '../src/index.js';

const MACHINE = 'B6F5-AB86-A5A1';
const rand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);

async function paidOrder(db, env) {
  const o = await createOrder(db, catalog, { name: 'Nguyễn Văn An', phone: '0912345678', machineId: MACHINE, ids: ['van-hoa-8'], terms: { version: '1.0', at: 'x' } }, new Date(), rand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: o.content, raw: '' });
  return o;
}

test('khôi phục PIN: đúng số điện thoại, mã đơn, mã máy', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await paidOrder(db, env);
  assert.deepEqual(await pinReset(db, { phone: '0912 345 678', code: 'nl ' + o.code, machineId: MACHINE }), { ok: true });
  assert.deepEqual(await pinReset(db, { phone: '0912345678', code: o.code, machineId: MACHINE }), { ok: true });
});

test('khôi phục PIN: sai điện thoại, sai máy hoặc đơn chưa thanh toán đều bị từ chối', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await paidOrder(db, env);
  await assert.rejects(pinReset(db, { phone: '0999999999', code: o.code, machineId: MACHINE }), (e) => e.status === 404);
  await assert.rejects(pinReset(db, { phone: '0912345678', code: o.code, machineId: 'AAAA-BBBB-CCCC' }), (e) => e.status === 404);
  await assert.rejects(pinReset(db, { phone: '0912345678', code: 'ZZZZZZ', machineId: MACHINE }), (e) => e.status === 404);
  await assert.rejects(pinReset(db, { phone: '0912345678', code: o.code, machineId: 'xx' }), (e) => e.status === 400);
  const db2 = fakeD1();
  const p = await createOrder(db2, catalog, { name: 'Nguyễn Văn An', phone: '0912345678', machineId: MACHINE, ids: ['van-hoa-8'], terms: { version: '1.0', at: 'x' } }, new Date(), rand);
  await assert.rejects(pinReset(db2, { phone: '0912345678', code: p.code, machineId: MACHINE }), (e) => e.status === 404);
});

test('khôi phục PIN: giới hạn 5 lần mỗi giờ cho một mã máy, hết giờ thử lại được', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await paidOrder(db, env);
  const t0 = new Date();
  for (let i = 0; i < 5; i++) await assert.rejects(pinReset(db, { phone: '0900000000', code: o.code, machineId: MACHINE }, t0), (e) => e.status === 404);
  await assert.rejects(pinReset(db, { phone: '0912345678', code: o.code, machineId: MACHINE }, t0), (e) => e.status === 429);
  const later = new Date(t0.getTime() + 3700_000);
  assert.deepEqual(await pinReset(db, { phone: '0912345678', code: o.code, machineId: MACHINE }, later), { ok: true });
});

test('khôi phục PIN: qua đường dẫn /api/pin-reset', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await paidOrder(db, env);
  const call = (b) => handle(new Request('https://x/api/pin-reset', { method: 'POST', body: JSON.stringify(b) }), { ...env, DB: db });
  assert.equal((await call({ phone: '0912345678', code: o.code, machineId: MACHINE })).status, 200);
  assert.equal((await call({ phone: '0911111111', code: o.code, machineId: MACHINE })).status, 404);
});
