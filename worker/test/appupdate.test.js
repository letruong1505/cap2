import test from 'node:test';
import assert from 'node:assert/strict';
import { fakeD1, testEnv } from './helpers.js';
import { handle } from '../src/index.js';

const env = (extra = {}) => ({ ...testEnv().env, DB: fakeD1(), UPDATES_BASE: 'https://r2.test', ...extra });
const get = (path, origin = 'https://localhost') => new Request('https://w.test' + path, { headers: { origin } });

function withFetch(map, fn) {
  const real = globalThis.fetch; const seen = [];
  globalThis.fetch = async (u) => { seen.push(String(u)); const r = map[String(u)]; return r ? new Response(r.body, { status: r.status || 200 }) : new Response('', { status: 404 }); };
  return fn(seen).finally(() => { globalThis.fetch = real; });
}

test('latest: chuyển tiếp latest.json, chỉ giữ trường cần thiết và thêm địa chỉ tải apk', () => withFetch({
  'https://r2.test/educenter-android/latest.json': { body: JSON.stringify({ version: '1.0.9', versionCode: 9, otaBuild: 9, minNative: 3, notes: 'Sửa lỗi', apk: 'nam-linh-educenter.apk', secret: 'x' }) },
}, async () => {
  const res = await handle(get('/api/app/android/latest'), env());
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('access-control-allow-origin'), 'https://localhost');
  assert.deepEqual(await res.json(), { version: '1.0.9', versionCode: 9, otaBuild: 9, minNative: 3, notes: 'Sửa lỗi', apkUrl: 'https://r2.test/educenter-android/nam-linh-educenter.apk' });
}));

test('latest: tên apk lạ bị thay bằng tên mặc định; chưa cấu hình hoặc R2 lỗi thì báo lỗi rõ ràng', () => withFetch({
  'https://r2.test/educenter-android/latest.json': { body: JSON.stringify({ versionCode: 1, apk: '../../x' }) },
}, async () => {
  const ok = await (await handle(get('/api/app/android/latest'), env())).json();
  assert.equal(ok.apkUrl, 'https://r2.test/educenter-android/nam-linh-educenter.apk');
  assert.equal((await handle(get('/api/app/android/latest'), env({ UPDATES_BASE: '' }))).status, 503);
  assert.equal((await handle(get('/api/app/android/latest'), env({ UPDATES_BASE: 'https://khac.test' }))).status, 502);
}));

test('ota: trả đúng gói của bản build, chỉ nhận số, thiếu gói thì 404', () => withFetch({
  'https://r2.test/educenter-android/ota/12.nlo': { body: 'NLO1-abc.def' },
}, async (seen) => {
  const res = await handle(get('/api/app/android/ota/12'), env());
  assert.equal(res.status, 200);
  assert.equal(await res.text(), 'NLO1-abc.def');
  assert.equal(res.headers.get('access-control-allow-origin'), 'https://localhost');
  assert.equal((await handle(get('/api/app/android/ota/13'), env())).status, 404);
  for (const bad of ['/api/app/android/ota/12.nlo', '/api/app/android/ota/..%2Fx', '/api/app/android/ota/1234567890']) assert.equal((await handle(get(bad), env())).status, 404, bad);
  assert.ok(!seen.some((u) => u.includes('..')));
}));

test('ota/latest: trang web khác không nhận CORS', () => withFetch({ 'https://r2.test/educenter-android/ota/1.nlo': { body: 'x' } }, async () => {
  const res = await handle(get('/api/app/android/ota/1', 'https://evil.test'), env());
  assert.equal(res.headers.get('access-control-allow-origin'), null);
}));
