import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, createPartnerCode, setPartnerActive, listOrders, discountPrice, HttpError } from '../src/orders.js';
import { handle } from '../src/index.js';

const MACHINE = 'B6F5-AB86-A5A1';
const input = (over = {}) => ({ name: 'Nguyễn Văn An', phone: '0912 345 678', machineId: MACHINE, ids: ['gia-su-ai', 'van-hoa-8'], terms: { version: '1.1', at: 'x' }, ...over });
const fixedRand = () => Uint8Array.from([0, 1, 2, 3, 4, 5]);
const NOW = new Date('2026-11-18T10:00:00Z');
// Môi trường thử nghiệm có khóa ký và cơ sở dữ liệu giả lập.
const withDb = (db) => ({ ...testEnv().env, DB: db });

async function partnerDb(percent = 20, code = 'DT-HOAI') {
  const db = fakeD1();
  await createPartnerCode(db, { code, partner: 'Đối tác Hoài', percent }, NOW);
  return db;
}

test('giảm theo tỉ lệ trên từng khóa, làm tròn đến đồng', () => {
  assert.equal(discountPrice(999000, 20), 799200);
  assert.equal(discountPrice(449000, 20), 359200);
  assert.equal(discountPrice(1001, 20), 801);
});

test('tạo đơn có mã đối tác: tiền sau giảm, lưu giá từng khóa', async () => {
  const db = await partnerDb();
  const o = await createOrder(db, catalog, input({ partnerCode: ' dt-hoai ' }), NOW, fixedRand);
  const expected = discountPrice(catalog.byId['gia-su-ai'].price, 20) + discountPrice(catalog.byId['van-hoa-8'].price, 20);
  assert.equal(o.amount, expected);
  assert.deepEqual(o.partner, { code: 'DT-HOAI', percent: 20 });
  assert.equal(o.items.length, 2);
  const rows = (await db.prepare('SELECT item, list_price, paid_price, partner_code FROM order_prices WHERE code = ?1 ORDER BY item').bind(o.code).all()).results;
  assert.equal(rows.length, 2);
  assert.ok(rows.every((r) => r.partner_code === 'DT-HOAI'));
});

test('đơn không có mã giữ nguyên giá niêm yết', async () => {
  const db = fakeD1();
  const o = await createOrder(db, catalog, input(), NOW, fixedRand);
  assert.equal(o.amount, catalog.byId['gia-su-ai'].price + catalog.byId['van-hoa-8'].price);
  assert.equal(o.partner, null);
});

test('mã sai, mã đã tắt hoặc sai định dạng bị từ chối', async () => {
  const db = await partnerDb();
  await assert.rejects(createOrder(db, catalog, input({ partnerCode: 'KHONG-CO' }), NOW, fixedRand), (e) => e instanceof HttpError && e.status === 400);
  await assert.rejects(createOrder(db, catalog, input({ partnerCode: 'a b' }), NOW, fixedRand), (e) => e instanceof HttpError && e.status === 400);
  await setPartnerActive(db, 'DT-HOAI', false);
  await assert.rejects(createOrder(db, catalog, input({ partnerCode: 'DT-HOAI' }), NOW, fixedRand), (e) => e.status === 400);
  // Không có đơn nào được tạo khi mã lỗi.
  assert.equal((await db.prepare('SELECT COUNT(*) AS n FROM orders').first()).n, 0);
});

test('tỉ lệ giảm phải là số nguyên từ 1 đến 100; mã trùng bị báo', async () => {
  const db = fakeD1();
  await assert.rejects(createPartnerCode(db, { code: 'X-1', partner: 'Ab', percent: 0 }, NOW), HttpError);
  await assert.rejects(createPartnerCode(db, { code: 'X-1', partner: 'Ab', percent: 101 }, NOW), HttpError);
  await createPartnerCode(db, { code: 'X-1', partner: 'Ab' }, NOW);
  await assert.rejects(createPartnerCode(db, { code: 'x-1', partner: 'Cd' }, NOW), (e) => e.status === 409);
});

test('sau khi thanh toán: trạng thái đơn có giá từng khóa và thời điểm thanh toán', async () => {
  const db = await partnerDb();
  const env = withDb(db);
  const o = await createOrder(db, catalog, input({ partnerCode: 'DT-HOAI' }), NOW, fixedRand);
  await applyPayment(db, env, catalog, { id: 1, amount: o.amount, content: 'NL ' + o.code }, NOW);
  const st = await handle(new Request(`https://x/api/orders/${o.code}/status?machine=${MACHINE}`), env, NOW);
  const body = await st.json();
  assert.equal(body.status, 'paid');
  assert.equal(body.amount, o.amount);
  assert.equal(body.phone, '0912345678');
  assert.ok(body.paidAt);
  assert.equal(body.lines.length, 2);
  assert.equal(body.partner.code, 'DT-HOAI');
  const giaSu = body.lines.find((l) => l.id === 'gia-su-ai');
  assert.equal(giaSu.list, 999000);
  assert.equal(giaSu.paid, 799200);
});

test('phiếu xác nhận: đúng mã và số điện thoại mới hiện; sai thì báo chung; chưa trả đủ thì không hiện phiếu', async () => {
  const db = await partnerDb();
  const env = withDb(db);
  const o = await createOrder(db, catalog, input({ name: 'Phụ huynh <b>X</b>', partnerCode: 'DT-HOAI' }), NOW, fixedRand);
  const page = (q) => handle(new Request('https://x/hoa-don?' + new URLSearchParams(q)), env, NOW).then((r) => r.text());

  const pending = await page({ code: o.code, phone: '0912345678' });
  assert.match(pending, /chưa thanh toán đủ/);

  await applyPayment(db, env, catalog, { id: 2, amount: o.amount, content: 'NL ' + o.code }, NOW);
  const ok = await page({ code: 'NL-' + o.code, phone: '0912 345 678' });
  assert.match(ok, /Phiếu xác nhận thanh toán/);
  assert.match(ok, /DT-HOAI/);
  assert.match(ok, /giảm 20%/);
  assert.match(ok, /799\.200 đ/);
  assert.doesNotMatch(ok, /<b>X<\/b>/); // tên được escape
  assert.match(ok, /&lt;b&gt;X&lt;\/b&gt;/);

  const wrong = await page({ code: o.code, phone: '0999999999' });
  assert.match(wrong, /không khớp/);
  assert.doesNotMatch(wrong, /Phiếu xác nhận thanh toán<\/h1>/);
  const none = await page({ code: 'ZZZZZZ', phone: '0912345678' });
  assert.match(none, /không khớp/);
});

test('trang phiếu không chạy script và có CSP chặn', async () => {
  const db = fakeD1();
  const env = withDb(db);
  const r = await handle(new Request('https://x/hoa-don'), env, NOW);
  assert.equal(r.status, 200);
  assert.match(r.headers.get('content-security-policy'), /default-src 'none'/);
  assert.doesNotMatch(await r.text(), /<script/i);
});

test('admin: mã đối tác cần mật khẩu; tạo, liệt kê, tắt được', async () => {
  const { env } = testEnv();
  const auth = { authorization: 'Bearer admin-secret', 'content-type': 'application/json' };
  assert.equal((await handle(new Request('https://x/api/admin/partner-codes'), env)).status, 401);
  const db = fakeD1();
  // handle dùng env.DB, nên gắn cơ sở dữ liệu giả vào môi trường thử nghiệm.
  const e2 = { ...env, DB: db };
  const created = await handle(new Request('https://x/api/admin/partner-codes', { method: 'POST', headers: auth, body: JSON.stringify({ code: 'DT-LAN', partner: 'Đối tác Lan', percent: 20 }) }), e2, NOW);
  assert.equal(created.status, 201);
  const off = await handle(new Request('https://x/api/admin/partner-codes/DT-LAN/active', { method: 'POST', headers: auth, body: JSON.stringify({ active: false }) }), e2, NOW);
  assert.equal(off.status, 200);
  const list = await (await handle(new Request('https://x/api/admin/partner-codes', { headers: auth }), e2, NOW)).json();
  assert.equal(list.partners[0].active, 0);
  assert.equal(list.partners[0].used, 0);
});

test('danh sách đơn của admin kèm mã đối tác và giá từng khóa', async () => {
  const db = await partnerDb();
  const o = await createOrder(db, catalog, input({ partnerCode: 'DT-HOAI' }), NOW, fixedRand);
  const orders = await listOrders(db, {}, NOW);
  const mine = orders.find((x) => x.code === o.code);
  assert.equal(mine.partner.code, 'DT-HOAI');
  assert.equal(mine.prices['gia-su-ai'].paid, 799200);
  assert.equal(mine.prices['gia-su-ai'].list, 999000);
});

test('mã đối tác giới hạn số máy: máy mới vượt giới hạn bị từ chối, máy đã dùng vẫn mua thêm được', async () => {
  const db = fakeD1();
  await createPartnerCode(db, { code: 'DT-LIM', partner: 'Đối tác giới hạn', percent: 20, maxMachines: 2 }, NOW);
  const rnd = (n) => () => Uint8Array.from([n, 1, 2, 3, 4, 5]);
  await createOrder(db, catalog, input({ partnerCode: 'DT-LIM', machineId: 'AAAA-AAAA-AAAA' }), NOW, rnd(0));
  await createOrder(db, catalog, input({ partnerCode: 'DT-LIM', machineId: 'BBBB-BBBB-BBBB' }), NOW, rnd(1));
  await assert.rejects(createOrder(db, catalog, input({ partnerCode: 'DT-LIM', machineId: 'CCCC-CCCC-CCCC' }), NOW, rnd(2)), (e) => e.status === 403);
  // máy đã dùng mã vẫn được mua thêm khóa khác
  await createOrder(db, catalog, input({ partnerCode: 'DT-LIM', machineId: 'AAAA-AAAA-AAAA' }), NOW, rnd(3));
  // không dùng mã thì máy nào cũng mua được
  await createOrder(db, catalog, input({ machineId: 'CCCC-CCCC-CCCC' }), NOW, rnd(4));
});

test('số máy tối đa mặc định 10 và phải là số nguyên từ 1 đến 1000', async () => {
  const db = fakeD1();
  assert.equal((await createPartnerCode(db, { code: 'M-1', partner: 'Ab' }, NOW)).maxMachines, 10);
  await assert.rejects(createPartnerCode(db, { code: 'M-2', partner: 'Ab', maxMachines: 0 }, NOW), HttpError);
  await assert.rejects(createPartnerCode(db, { code: 'M-3', partner: 'Ab', maxMachines: 1001 }, NOW), HttpError);
});

test('mã giảm 100%: bắt buộc chọn khóa áp dụng; đơn 0 đồng tự duyệt và cấp khóa', async () => {
  const db = fakeD1();
  await assert.rejects(createPartnerCode(db, { code: 'FREE-1', partner: 'Tặng', percent: 100 }, NOW, catalog), /ít nhất một khóa/);
  await assert.rejects(createPartnerCode(db, { code: 'FREE-1', partner: 'Tặng', percent: 101, items: ['van-hoa-8'] }, NOW, catalog), /1 đến 100/);
  await assert.rejects(createPartnerCode(db, { code: 'FREE-1', partner: 'Tặng', percent: 100, items: ['khong-co'] }, NOW, catalog), /không hợp lệ/);
  const made = await createPartnerCode(db, { code: 'FREE-1', partner: 'Tặng', percent: 100, items: ['van-hoa-8'], maxMachines: 2 }, NOW, catalog);
  assert.deepEqual(made.items, ['van-hoa-8']);
  const { createOrderAuto } = await import('../src/orders.js');
  const env = withDb(db);
  const o = await createOrderAuto(db, env, catalog, input({ ids: ['van-hoa-8'], partnerCode: 'free-1' }), NOW, fixedRand);
  assert.equal(o.amount, 0);
  assert.equal(o.status, 'paid');
  const row = await db.prepare('SELECT status, key FROM orders WHERE code = ?1').bind(o.code).first();
  assert.equal(row.status, 'paid');
  assert.match(row.key, /^NL1-/);
  // cùng máy dùng lại mã cho cùng khóa: bị chặn
  await assert.rejects(createOrderAuto(db, env, catalog, input({ ids: ['van-hoa-8'], partnerCode: 'FREE-1' }), NOW), (e) => e instanceof HttpError && e.status === 409);
});

test('mã chỉ áp dụng cho khóa được chọn: khóa khác tính giá niêm yết; không có khóa nào hợp thì báo lỗi', async () => {
  const db = fakeD1();
  await createPartnerCode(db, { code: 'FREE-2', partner: 'Tặng', percent: 100, items: ['van-hoa-8'], maxMachines: 5 }, NOW, catalog);
  const mixed = await createOrder(db, catalog, input({ ids: ['van-hoa-8', 'gia-su-ai'], partnerCode: 'FREE-2' }), NOW, fixedRand);
  assert.equal(mixed.amount, catalog.byId['gia-su-ai'].price); // chỉ phải trả khóa không thuộc mã
  assert.equal(mixed.status, 'pending');
  const rows = (await db.prepare('SELECT item, paid_price, partner_code FROM order_prices WHERE code = ?1 ORDER BY item').bind(mixed.code).all()).results;
  assert.deepEqual(rows.map((r) => [r.item, r.paid_price, r.partner_code]), [['gia-su-ai', catalog.byId['gia-su-ai'].price, null], ['van-hoa-8', 0, 'FREE-2']]);
  await assert.rejects(createOrder(db, catalog, input({ machineId: 'AAAA-BBBB-CCCC', phone: '0911111111', ids: ['gia-su-ai'], partnerCode: 'FREE-2' }), NOW), /không áp dụng/);
});
