import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createTrial, getOrder, approveOrder, issueKey, ping, revokeOrder, orderStatus } from '../src/orders.js';
import { packKeys } from '../src/pack.js';

const NOW = new Date('2026-11-27T15:00:00Z'); // 22:00 giờ Việt Nam ngày 27/11
const M = 'B6F5-AB86-A5A1';
const { env, publicKey } = testEnv();
const body = (key) => JSON.parse(Buffer.from(key.slice(4).split('.')[0], 'base64url').toString());
const verify = (key) => { const [b, s] = key.slice(4).split('.'); return crypto.verify(null, Buffer.from(b, 'base64url'), publicKey, Buffer.from(s, 'base64url')); };
const trial = (db, o = {}, now = NOW) => createTrial(db, env, catalog, { machineId: M, name: 'Nguyễn Văn A', phone: '0968 646 853', ...o }, now);

test('dùng thử: khóa gắn máy, toàn bộ nội dung, hết hạn sau 3 ngày theo giờ Việt Nam (28, 29, 30/11)', async () => {
  const db = fakeD1();
  const r = await trial(db);
  assert.equal(r.expires, '2026-11-30');
  assert.ok(verify(r.key));
  const p = body(r.key);
  assert.deepEqual([p.machine, p.expires, p.trial, p.id], [M, '2026-11-30', true, 'NL-' + r.code]);
  assert.deepEqual(p.grades, [6, 7, 8, 9, 10, 11, 12]);
  assert.ok(p.courses.includes('gia-su-ai') && p.courses.includes('ai-nguoi-di-lam-claude'));
  const o = await getOrder(db, r.code);
  assert.deepEqual([o.status, o.amount, o.phone, o.name], ['paid', 0, '0968646853', 'Nguyễn Văn A']);
  assert.match(o.note, /^TRIAL 2026-11-30/);
});

test('mỗi máy và mỗi số điện thoại chỉ dùng thử một lần', async () => {
  const db = fakeD1();
  await trial(db);
  await assert.rejects(trial(db), (e) => e.status === 409);
  await assert.rejects(trial(db, { machineId: 'AAAA-BBBB-CCCC' }), (e) => e.status === 409); // cùng số điện thoại
  await assert.rejects(trial(db, { phone: '0912345678' }), (e) => e.status === 409);          // cùng máy
  await trial(db, { machineId: 'AAAA-BBBB-CCCC', phone: '0912345678' });
});

test('dùng thử: kiểm tra tên, số điện thoại, mã máy', async () => {
  const db = fakeD1();
  await assert.rejects(trial(db, { name: '' }), (e) => e.status === 400);
  await assert.rejects(trial(db, { phone: '123' }), (e) => e.status === 400);
  await assert.rejects(trial(db, { machineId: 'xyz' }), (e) => e.status === 400);
});

test('đổi máy cho đơn dùng thử vẫn giữ hạn, không thành khóa vĩnh viễn; duyệt tay bị chặn', async () => {
  const db = fakeD1();
  const r = await trial(db);
  const o = await getOrder(db, r.code);
  const k2 = await issueKey(db, env, catalog, o, new Date('2026-11-28T03:00:00Z'), 'AAAA-BBBB-CCCC');
  assert.deepEqual([body(k2).expires, body(k2).trial, body(k2).machine], ['2026-11-30', true, 'AAAA-BBBB-CCCC']);
  await assert.rejects(approveOrder(db, env, catalog, r.code, 'Duyệt tay', NOW), (e) => e.status === 409);
});

test('máy chủ ngừng cấp khóa giải mã nội dung khi hết hạn hoặc bị thu hồi', async () => {
  const db = fakeD1();
  const e2 = { ...env, PACK_MASTER: 'master-secret', UPDATES_BASE: 'https://cdn.example.com' };
  const r = await trial(db);
  const got = (now) => packKeys(db, e2, catalog, { machineId: M, keys: [r.key] }, now);
  const d1 = await got(new Date('2026-11-30T10:00:00Z'));
  assert.deepEqual(Object.keys(d1.keys), ['6', '7', '8', '9', '10', '11', '12']);
  assert.deepEqual(Object.keys((await got(new Date('2026-12-01T00:30:00Z'))).keys), []);
  await revokeOrder(db, r.code, 'thu hồi sớm', NOW);
  assert.deepEqual(Object.keys((await got(new Date('2026-11-28T00:00:00Z'))).keys), []);
  assert.deepEqual((await ping(db, { machineId: M, ids: ['NL-' + r.code], version: '1' }, NOW, catalog)).revoked, [r.code]);
});

test('máy gửi tín hiệu (ping) thì admin thấy máy dùng thử; trạng thái đơn trả đúng khóa', async () => {
  const db = fakeD1();
  const r = await trial(db);
  await ping(db, { machineId: M, ids: [r.code], version: '1.2.0' }, NOW, catalog);
  assert.equal((await db.prepare('SELECT COUNT(*) AS n FROM devices WHERE code = ?1').bind(r.code).first()).n, 1);
  const st = await orderStatus(db, env, catalog, r.code, M, NOW);
  assert.equal(st.key, r.key);
  assert.ok(st.lines.every((l) => l.paid === 0));
});
