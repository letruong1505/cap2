import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, orderStatus, findCode, approveOrder, cancelOrder, reissueOrder, HttpError } from '../src/orders.js';
import { handle } from '../src/index.js';

const require = createRequire(import.meta.url);
const { parseKey, evaluateKey } = require('../../main/license/verify.js');

const MACHINE = 'B6F5-AB86-A5A1';
const input = (over = {}) => ({ name: 'Nguyễn Văn An', phone: '0912 345 678', machineId: MACHINE, ids: ['gia-su-ai', 'van-hoa-8'], terms: { version: '1.0', at: 'x' }, ...over });
const fixedRand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);

test('tạo đơn: tiền tính ở máy chủ, chuẩn hóa dữ liệu', async () => {
  const db = fakeD1();
  const o = await createOrder(db, catalog, input({ amount: 1 }), new Date(), fixedRand);
  assert.equal(o.amount, 999000 + 399000);
  assert.equal(o.code, 'ABCDEF');
  assert.equal(o.content, 'NL ABCDEF');
  const row = await db.prepare('SELECT * FROM orders').first();
  assert.equal(row.phone, '0912345678');
  assert.equal(row.status, 'pending');
});

test('tạo đơn: từ chối dữ liệu sai', async () => {
  const db = fakeD1();
  for (const bad of [{ name: '' }, { phone: '123' }, { machineId: 'abc' }, { ids: [] }, { ids: ['khong-co'] }, { terms: null }]) {
    await assert.rejects(createOrder(db, catalog, input(bad)), HttpError);
  }
});

test('tạo đơn: giới hạn 10 đơn mỗi giờ cho một máy', async () => {
  const db = fakeD1();
  let n = 0;
  const rand = () => Uint8Array.from([n++, 7, 8, 9, 10, 11]);
  for (let i = 0; i < 10; i++) await createOrder(db, catalog, input(), new Date(), rand);
  await assert.rejects(createOrder(db, catalog, input(), new Date(), rand), (e) => e.status === 429);
});

test('findCode: nhận nhiều kiểu nội dung ngân hàng', () => {
  assert.equal(findCode('NL ABCDEF chuyen tien'), 'ABCDEF');
  assert.equal(findCode('nlabcdef'), 'ABCDEF');
  assert.equal(findCode('NGUYEN VAN A NL-ABCDEF FT2411'), 'ABCDEF');
  assert.equal(findCode('', 'NLABCDEF'), 'ABCDEF');
  assert.equal(findCode('chuyen tien hoc phi'), null);
  assert.equal(findCode('ANL ABCDEF'), null);
});

test('thanh toán đủ: cấp key hợp lệ, đúng mã máy, đúng lớp và khóa', async () => {
  const db = fakeD1(); const { env, publicKey } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  const res = await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ABCDEF chuyen tien' });
  assert.equal(res, 'paid');
  const st = await orderStatus(db, env, catalog, 'ABCDEF', MACHINE);
  assert.equal(st.status, 'paid');
  const parsed = parseKey(st.key, publicKey);
  assert.ok(parsed.ok);
  assert.deepEqual(parsed.payload.grades, [8]);
  assert.deepEqual(parsed.payload.courses, ['gia-su-ai']);
  assert.equal(parsed.payload.machine, MACHINE);
  assert.equal(parsed.payload.expires, 'never');
  assert.equal(evaluateKey(st.key, MACHINE, new Date(), publicKey).status, 'ok');
  assert.equal(evaluateKey(st.key, 'AAAA-BBBB-CCCC', new Date(), publicKey).status, 'wrong-machine');
});

test('webhook gửi lại cùng giao dịch: không xử lý hai lần', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  const tx = { id: 7, amount: o.amount, content: 'NL ABCDEF' };
  assert.equal(await applyPayment(db, env, catalog, tx), 'paid');
  assert.equal(await applyPayment(db, env, catalog, tx), 'duplicate');
});

test('chuyển thiếu rồi bù thêm: đủ thì mới cấp key', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  assert.equal(await applyPayment(db, env, catalog, { id: 1, amount: 500000, content: 'NL ABCDEF' }), 'underpaid');
  assert.equal((await orderStatus(db, env, catalog, 'ABCDEF', MACHINE)).key, undefined);
  assert.equal(await applyPayment(db, env, catalog, { id: 2, amount: o.amount - 500000, content: 'NL ABCDEF' }), 'paid');
  assert.ok((await orderStatus(db, env, catalog, 'ABCDEF', MACHINE)).key);
});

test('chuyển thừa vẫn cấp key và ghi nhận; sai nội dung thì không khớp', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  assert.equal(await applyPayment(db, env, catalog, { id: 1, amount: 100000, content: 'hoc phi' }), 'unmatched');
  assert.equal(await applyPayment(db, env, catalog, { id: 2, amount: o.amount + 1000, content: 'NL ABCDEF' }), 'paid-overpaid');
});

test('tra trạng thái: sai mã máy thì không lộ key', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ABCDEF' });
  await assert.rejects(orderStatus(db, env, catalog, 'ABCDEF', 'AAAA-BBBB-CCCC'), (e) => e.status === 404);
  await assert.rejects(orderStatus(db, env, catalog, 'ZZZZZZ', MACHINE), (e) => e.status === 404);
});

test('thiếu khóa ký: thu tiền vẫn ghi nhận, key cấp bù khi có khóa', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  const res = await applyPayment(db, { ...env, SIGNING_KEY_PEM: '' }, catalog, { id: 1, amount: o.amount, content: 'NL ABCDEF' });
  assert.equal(res, 'paid-nokey');
  assert.ok((await orderStatus(db, env, catalog, 'ABCDEF', MACHINE)).key);
});

test('duyệt tay, hủy, đổi máy', async () => {
  const db = fakeD1(); const { env, publicKey } = testEnv();
  await createOrder(db, catalog, input(), new Date(), fixedRand);
  const key = await approveOrder(db, env, catalog, 'ABCDEF', 'nhận tiền mặt');
  assert.ok(parseKey(key, publicKey).ok);
  await assert.rejects(cancelOrder(db, 'ABCDEF'), (e) => e.status === 409);
  const k2 = await reissueOrder(db, env, catalog, 'ABCDEF', 'aaaa-bbbb-cccc');
  assert.equal(parseKey(k2, publicKey).payload.machine, 'AAAA-BBBB-CCCC');
  assert.equal((await db.prepare('SELECT reissues FROM orders').first()).reissues, 1);
  await assert.rejects(reissueOrder(db, env, catalog, 'ABCDEF', 'sai'), (e) => e.status === 400);
});

test('đơn đã hủy thì tiền về không cấp key', async () => {
  const db = fakeD1(); const { env } = testEnv();
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  await cancelOrder(db, 'ABCDEF');
  assert.equal(await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ABCDEF' }), 'order-cancelled');
});

test('HTTP: webhook cần đúng API Key; quản trị cần đúng mật khẩu', async () => {
  const db = fakeD1(); const { env } = testEnv(); env.DB = db;
  const o = await createOrder(db, catalog, input(), new Date(), fixedRand);
  const hook = (key, body) => handle(new Request('https://x/api/sepay', { method: 'POST', headers: key ? { authorization: 'Apikey ' + key } : {}, body: JSON.stringify(body) }), env);
  const payload = { id: 99, transferType: 'in', transferAmount: o.amount, content: 'NL ABCDEF', referenceCode: 'FT1' };
  assert.equal((await hook(null, payload)).status, 401);
  assert.equal((await hook('sai', payload)).status, 401);
  const ok = await hook('sepay-secret', payload);
  assert.equal(ok.status, 200);
  assert.equal((await ok.json()).result, 'paid');
  assert.equal((await hook('sepay-secret', { ...payload, id: 100, transferType: 'out' })).status, 200);
  assert.equal((await handle(new Request('https://x/api/admin/orders'), env)).status, 401);
  const list = await handle(new Request('https://x/api/admin/orders', { headers: { authorization: 'Bearer admin-secret' } }), env);
  assert.equal((await list.json()).orders.length, 1);
  const st = await handle(new Request(`https://x/api/orders/ABCDEF/status?machine=${MACHINE}`), env);
  assert.ok((await st.json()).key.startsWith('NL1-'));
  const page = await handle(new Request('https://x/admin'), env);
  assert.match(page.headers.get('content-security-policy'), /default-src 'none'/);
});

test('ký bằng WebCrypto khớp chữ ký của công cụ keygen (Node crypto)', async () => {
  const crypto = await import('node:crypto');
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  const pem = privateKey.export({ type: 'pkcs8', format: 'pem' });
  const { signKey } = await import('../src/keys.js');
  const payload = { v: 1, id: 'NL-T', owner: 'A', grades: [6], machine: '*', issued: '2026-11-11', expires: 'never' };
  const mine = await signKey(pem, payload);
  const body = Buffer.from(JSON.stringify(payload));
  const theirs = 'NL1-' + body.toString('base64url') + '.' + Buffer.from(crypto.sign(null, body, privateKey)).toString('base64url');
  assert.equal(mine, theirs);
});
