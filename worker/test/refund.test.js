import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, revokeOrder, revokeItem, refundOpen } from '../src/orders.js';

const MACHINE = 'B6F5-AB86-A5A1';
const input = { name: 'Nguyễn Văn An', phone: '0912345678', machineId: MACHINE, ids: ['gia-su-ai', 'van-hoa-8'], terms: { version: '1.2', at: 'x' } };
const fixedRand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);
const PAID = new Date('2026-11-18T10:00:00Z');
const DAY = 86400e3;

async function paidOrder() {
  const db = fakeD1();
  const env = { ...testEnv().env, DB: db };
  const o = await createOrder(db, catalog, input, PAID, fixedRand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ' + o.code }, PAID);
  return { db, code: o.code };
}

test('cửa sổ hoàn tiền: 7 ngày tính từ lúc thanh toán', () => {
  assert.equal(refundOpen(PAID.toISOString(), new Date(PAID.getTime() + 7 * DAY)), true);
  assert.equal(refundOpen(PAID.toISOString(), new Date(PAID.getTime() + 7 * DAY + 1000)), false);
  assert.equal(refundOpen(null, PAID), false);
});

test('trong 7 ngày: thu hồi cả đơn và một khóa đều được', async () => {
  const { db, code } = await paidOrder();
  const now = new Date(PAID.getTime() + 2 * DAY);
  await revokeItem(db, code, 'van-hoa-8', 'Hoàn tiền một phần', now);
  await revokeOrder(db, code, 'Hoàn tiền', now);
});

test('quá 7 ngày: không thu hồi để hoàn tiền được nữa', async () => {
  const { db, code } = await paidOrder();
  const late = new Date(PAID.getTime() + 8 * DAY);
  await assert.rejects(revokeItem(db, code, 'van-hoa-8', 'x', late), (e) => e.status === 409);
  await assert.rejects(revokeOrder(db, code, 'x', late), (e) => e.status === 409);
  const row = await db.prepare('SELECT COUNT(*) AS n FROM item_revocations').first();
  assert.equal(row.n, 0);
});
