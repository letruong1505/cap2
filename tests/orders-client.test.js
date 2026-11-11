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
