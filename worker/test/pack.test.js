import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, revokeOrder, revokeItem } from '../src/orders.js';
import { packKeys, gradeKey } from '../src/pack.js';

const require = createRequire(import.meta.url);
const { deriveGradeKey } = require('../../core/pack-format.js');

const PC = 'B6F5-AB86-A5A1';
const OTHER = 'B6F5-AB86-0000';
const NOW = new Date('2026-11-22T10:00:00Z');
const rand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);
const T = { version: '1.2', at: 'x' };
const MASTER = 'm'.repeat(40);
let txn = 500;

const gradeIds = (grades) => grades.map((g) => Object.values(catalog.byId).find((c) => c.grade === g && !c.bundle)?.id).filter(Boolean);

async function setup(ids) {
  const db = fakeD1();
  const env = { ...testEnv().env, DB: db, PACK_MASTER: MASTER, UPDATES_BASE: 'https://r2.example.com' };
  const o = await createOrder(db, catalog, { name: 'An', phone: '0912345678', ids, terms: T, machineId: PC }, NOW, rand);
  const r = await applyPayment(db, env, catalog, { id: ++txn, amount: o.amount, content: 'NL ' + o.code }, NOW);
  const row = await db.prepare('SELECT key FROM orders WHERE code = ?1').bind(o.code).first();
  return { db, env, key: row.key, code: o.code, r };
}

test('khoá lớp của Worker khớp khoá của công cụ đóng gói', async () => {
  for (const g of [6, 9, 12]) assert.equal(await gradeKey(MASTER, g), deriveGradeKey(MASTER, g).toString('base64'));
});

test('máy có khoá lớp nào thì nhận khoá giải mã đúng lớp đó', async () => {
  const ids = gradeIds([7, 9]);
  assert.equal(ids.length, 2);
  const { db, env, key } = await setup(ids);
  const r = await packKeys(db, env, catalog, { machineId: PC, keys: [key] }, NOW);
  assert.deepEqual(Object.keys(r.keys), ['7', '9']);
  assert.equal(r.base, 'https://r2.example.com/educenter-content');
  assert.equal(r.keys['7'], deriveGradeKey(MASTER, 7).toString('base64'));
});

test('máy khác, khoá giả, khoá hết hạn hoặc không có khoá thì không nhận được gì', async () => {
  const { db, env, key } = await setup(gradeIds([7]));
  assert.deepEqual((await packKeys(db, env, catalog, { machineId: OTHER, keys: [key] }, NOW)).keys, {});
  assert.deepEqual((await packKeys(db, env, catalog, { machineId: PC, keys: [key.slice(0, -6) + 'AAAAAA', 'rac', ''] }, NOW)).keys, {});
  assert.deepEqual((await packKeys(db, env, catalog, { machineId: PC, keys: [] }, NOW)).keys, {});
});

test('đơn bị thu hồi hoặc bị thu hồi riêng một lớp thì mất khoá giải mã lớp đó', async () => {
  const ids = gradeIds([7, 9]);
  const a = await setup(ids);
  await revokeItem(a.db, a.code, ids[1], 'hoàn tiền', NOW);
  assert.deepEqual(Object.keys((await packKeys(a.db, a.env, catalog, { machineId: PC, keys: [a.key] }, NOW)).keys), ['7']);
  const b = await setup(ids);
  await revokeOrder(b.db, b.code, 'hoàn tiền', NOW);
  assert.deepEqual((await packKeys(b.db, b.env, catalog, { machineId: PC, keys: [b.key] }, NOW)).keys, {});
});

test('chưa cấu hình PACK_MASTER thì báo 503, mã máy sai thì báo 400', async () => {
  const { db, env, key } = await setup(gradeIds([7]));
  await assert.rejects(packKeys(db, { ...env, PACK_MASTER: '' }, catalog, { machineId: PC, keys: [key] }, NOW), (e) => e.status === 503);
  await assert.rejects(packKeys(db, env, catalog, { machineId: 'x', keys: [key] }, NOW), (e) => e.status === 400);
});
