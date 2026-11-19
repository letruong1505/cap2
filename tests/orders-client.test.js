const test = require('node:test');
const assert = require('node:assert');
const { makeClient } = require('../main/orders.js');

const reply = (status, data) => async () => ({ status, ok: status < 400, json: async () => data });

test('chưa cấu hình địa chỉ máy chủ thì trả offline', async () => {
  const c = makeClient({ baseUrl: () => '', machineId: () => 'AAAA-BBBB-CCCC' });
  assert.deepStrictEqual(await c.createOrder({}), { ok: false, offline: true });
});

test('gửi đơn: thêm mã máy từ tiến trình chính, bỏ trường lạ', async () => {
  let sent;
  const c = makeClient({ baseUrl: () => 'https://x.test/', machineId: () => 'AAAA-BBBB-CCCC',
    fetchFn: async (url, opt) => { sent = { url, body: JSON.parse(opt.body) }; return { status: 201, ok: true, json: async () => ({ code: 'ABCDEF' }) }; } });
  const r = await c.createOrder({ name: 'A', phone: '0912345678', ids: ['gia-su-ai'], terms: { version: '1', at: 't' }, machineId: 'GIẢ', amount: 1 });
  assert.strictEqual(r.ok, true);
  assert.strictEqual(sent.url, 'https://x.test/api/orders');
  assert.strictEqual(sent.body.machineId, 'AAAA-BBBB-CCCC');
  assert.strictEqual(sent.body.amount, undefined);
});

test('lỗi 4xx trả thông báo, lỗi 5xx và lỗi mạng trả offline', async () => {
  const mk = (fetchFn) => makeClient({ baseUrl: () => 'https://x.test', machineId: () => 'AAAA-BBBB-CCCC', fetchFn });
  assert.deepStrictEqual(await mk(reply(400, { error: 'Sai' })).createOrder({}), { ok: false, error: 'Sai' });
  assert.deepStrictEqual(await mk(reply(500, {})).createOrder({}), { ok: false, offline: true });
  assert.deepStrictEqual(await mk(async () => { throw new Error('net'); }).orderStatus('ABCDEF'), { ok: false, offline: true });
});

test('tín hiệu: gửi mã máy, mã đơn và số bản, bỏ trường lạ', async () => {
  let sent;
  const c = makeClient({ baseUrl: () => 'https://x.test', machineId: () => 'AAAA-BBBB-CCCC',
    fetchFn: async (url, opt) => { sent = { url, body: JSON.parse(opt.body) }; return { status: 200, ok: true, json: async () => ({ revoked: [] }) }; } });
  await c.ping({ ids: ['ABCDEF'], version: '1.2.9', machineId: 'GIẢ', name: 'X' });
  assert.strictEqual(sent.url, 'https://x.test/api/ping');
  assert.deepStrictEqual(sent.body, { machineId: 'AAAA-BBBB-CCCC', ids: ['ABCDEF'], version: '1.2.9' });
});

test('gửi mã đối tác lên máy chủ, đã trim và cắt độ dài', async () => {
  let sent;
  const c = makeClient({ baseUrl: () => 'https://x.test/', machineId: () => 'AAAA-BBBB-CCCC',
    fetchFn: async (url, opt) => { sent = JSON.parse(opt.body); return { status: 201, ok: true, json: async () => ({ code: 'ABCDEF' }) }; } });
  await c.createOrder({ name: 'A', phone: '0912345678', ids: ['gia-su-ai'], partnerCode: '  dt-hoai  ', terms: { version: '1', at: 't' } });
  assert.strictEqual(sent.partnerCode, 'dt-hoai');
  await c.createOrder({ name: 'A', phone: '0912345678', ids: ['gia-su-ai'], terms: { version: '1', at: 't' } });
  assert.strictEqual(sent.partnerCode, '');
});

test('tiến độ cho phụ huynh: mã máy do tiến trình chính thêm, mã máy từ giao diện bị bỏ', async () => {
  const sent = [];
  const c = makeClient({ baseUrl: () => 'https://x.test', machineId: () => 'AAAA-BBBB-CCCC',
    fetchFn: async (url, opt) => { sent.push({ url, body: JSON.parse(opt.body) }); return { status: 200, ok: true, json: async () => ({}) }; } });
  await c.progressSettings({ code: 'ABCDEF', enabled: true, machineId: 'GIẢ' });
  await c.progressPush({ code: 'ABCDEF', days: [{ day: '2026-11-17' }], machineId: 'GIẢ' });
  await c.progressView({ code: 'ABCDEF', phone: '0912345678', grade: '9', from: '2026-11-01', machineId: 'GIẢ' });
  assert.deepStrictEqual(sent.map((s) => s.url), ['https://x.test/api/progress/settings', 'https://x.test/api/progress/push', 'https://x.test/api/progress/view']);
  sent.forEach((s) => assert.strictEqual(s.body.machineId, 'AAAA-BBBB-CCCC'));
  assert.strictEqual(sent[0].body.enabled, true);
  assert.strictEqual(sent[1].body.days.length, 1);
  assert.strictEqual(sent[2].body.grade, 9);
});
