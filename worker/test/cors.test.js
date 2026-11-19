import test from 'node:test';
import assert from 'node:assert/strict';
import { fakeD1, testEnv } from './helpers.js';
import { handle } from '../src/index.js';

const env = () => ({ ...testEnv().env, DB: fakeD1() });
const req = (method, path, origin, extra = {}) => new Request('https://w.test' + path, { method, headers: { ...(origin ? { origin } : {}), ...extra.headers }, body: extra.body });

test('ứng dụng Android (https://localhost) gọi được các đường dẫn của phần mềm khách: có CORS và preflight', async () => {
  for (const path of ['/api/orders', '/api/orders/ABCDEF/status', '/api/pin-reset', '/api/claim-device', '/api/ping']) {
    const pre = await handle(req('OPTIONS', path, 'https://localhost', { headers: { 'access-control-request-method': 'POST' } }), env());
    assert.equal(pre.status, 204, path);
    assert.equal(pre.headers.get('access-control-allow-origin'), 'https://localhost');
    assert.match(pre.headers.get('access-control-allow-headers'), /content-type/);
    const res = await handle(req('POST', path, 'https://localhost', { body: '{}', headers: { 'content-type': 'application/json' } }), env());
    assert.equal(res.headers.get('access-control-allow-origin'), 'https://localhost', path);
    assert.equal(res.headers.get('vary'), 'Origin');
  }
});

test('trang web khác không nhận CORS; trang quản trị và SePay không bao giờ mở CORS', async () => {
  const other = await handle(req('POST', '/api/ping', 'https://evil.test', { body: '{}', headers: { 'content-type': 'application/json' } }), env());
  assert.equal(other.headers.get('access-control-allow-origin'), null);
  assert.equal((await handle(req('OPTIONS', '/api/ping', 'https://evil.test'), env())).status, 403);
  for (const path of ['/api/admin/orders', '/api/sepay']) {
    const res = await handle(req('GET', path, 'https://localhost'), env());
    assert.equal(res.headers.get('access-control-allow-origin'), null, path);
    assert.equal((await handle(req('OPTIONS', path, 'https://localhost'), env())).status, 403, path);
  }
});

test('không có Origin (app Windows, SePay): phản hồi như cũ, không thêm CORS', async () => {
  const res = await handle(req('POST', '/api/ping', null, { body: '{}', headers: { 'content-type': 'application/json' } }), env());
  assert.equal(res.headers.get('access-control-allow-origin'), null);
});
