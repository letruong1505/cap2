import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import catalog from '../../renderer/catalog.js';
import { fakeD1 } from './helpers.js';
import { getOrder } from '../src/orders.js';
import { registerLegacy, DEFAULT_PUBLIC_KEY_PEM } from '../src/register.js';
import { handle } from '../src/index.js';

const NOW = new Date('2026-11-20T03:00:00Z');
const M = 'B6F5-AB86-A5A1';
const { privateKey, publicKey } = crypto.generateKeyPairSync('ed25519');
const env = { PUBLIC_KEY_PEM: publicKey.export({ type: 'spki', format: 'pem' }) };
const mk = (p) => { const body = Buffer.from(JSON.stringify({ v: 1, id: 'NL-43356A', owner: 'Lê Trường', grades: [9, 12], courses: [], machine: M, issued: '2026-09-01', expires: 'never', ...p })); return 'NL1-' + body.toString('base64url') + '.' + crypto.sign(null, body, privateKey).toString('base64url'); };
const reg = (db, o = {}) => registerLegacy(db, env, catalog, { key: mk(), phone: '0968 646 853', machineId: M, ...o }, NOW);

test('khóa công khai nhúng trong Worker khớp main/license/public-key.pem', () => {
  const file = fs.readFileSync(new URL('../../main/license/public-key.pem', import.meta.url), 'utf8').replace(/\s+/g, '');
  assert.equal(DEFAULT_PUBLIC_KEY_PEM.replace(/\s+/g, ''), file);
});

test('khách tự đăng ký khóa USB: tạo đơn 0 đ đã thanh toán đúng máy, lớp, số điện thoại', async () => {
  const db = fakeD1();
  const r = await reg(db);
  assert.deepEqual([r.ok, r.existed, r.code, r.items], [true, false, '43356A', ['van-hoa-9', 'van-hoa-12']]);
  const o = await getOrder(db, '43356A');
  assert.deepEqual([o.status, o.amount, o.phone, o.machine, o.name], ['paid', 0, '0968646853', M, 'Lê Trường']);
  assert.match(o.note, /tự đăng ký/);
  assert.match(o.key, /^NL1-/);
  const again = await reg(db, { phone: '0900000000' }); // đăng ký lại: không đổi số điện thoại đã có
  assert.deepEqual([again.existed, (await getOrder(db, '43356A')).phone], [true, '0968646853']);
});

test('chặn: khóa sai chữ ký, khóa của máy khác, khóa hết hạn, id không đúng dạng, mọi máy', async () => {
  const good = mk();
  const bad = [good.slice(0, -3) + 'AAA', mk({ machine: 'AAAA-BBBB-CCCC' }), mk({ expires: '2026-01-01' }), mk({ id: 'NL-0001' }), mk({ machine: '*' }), 'rac', ''];
  for (const key of bad) {
    const db = fakeD1(); // mỗi khóa một cơ sở dữ liệu mới để không chạm giới hạn 5 lần/giờ
    await assert.rejects(reg(db, { key }), (e) => e.status === 400, key.slice(0, 20));
    assert.equal(await getOrder(db, '43356A'), null);
  }
});

test('mã khóa đã thuộc máy khác: từ chối; sai quá 5 lần/giờ: khóa tạm; số điện thoại sai: từ chối', async () => {
  const db = fakeD1();
  await reg(db);
  await assert.rejects(registerLegacy(db, env, catalog, { key: mk({ machine: 'AAAA-BBBB-CCCC' }), phone: '0968646853', machineId: 'AAAA-BBBB-CCCC' }, NOW), (e) => e.status === 409);
  await assert.rejects(reg(fakeD1(), { phone: '123' }), (e) => e.status === 400);
  const db2 = fakeD1();
  for (let i = 0; i < 5; i++) await assert.rejects(reg(db2, { key: 'rac' }), (e) => e.status === 400);
  await assert.rejects(reg(db2), (e) => e.status === 429);
});

test('đường dẫn đăng ký khóa có CORS', async () => {
  const pre = await handle(new Request('https://w.test/api/register-legacy', { method: 'OPTIONS', headers: { origin: 'https://localhost', 'access-control-request-method': 'POST' } }), { DB: fakeD1() });
  assert.equal(pre.status, 204);
});
