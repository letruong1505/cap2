import test from 'node:test';
import assert from 'node:assert/strict';
import catalog from '../../renderer/catalog.js';
import { fakeD1, testEnv } from './helpers.js';
import { createOrder, applyPayment, createPartnerCode, revokeItem, revokeOrder } from '../src/orders.js';
import { handle } from '../src/index.js';
import { partnerToken, partnerByToken, partnerSummary, commissionOf, commissionTotal } from '../src/partner-portal.js';

const NOW = new Date('2026-11-18T10:00:00Z');
const rnd = (n) => () => Uint8Array.from([n, 1, 2, 3, 4, 5]);
const mk = (phone, machine, ids, partnerCode) => ({ name: 'Khách', phone, machineId: machine, ids, partnerCode, terms: { version: '1.1', at: 'x' } });

async function setup() {
  const { env } = testEnv(); const db = fakeD1(); const e = { ...env, DB: db };
  await createPartnerCode(db, { code: 'DT-HOAI', partner: 'Đối tác Hoài', percent: 20 }, NOW);
  await createPartnerCode(db, { code: 'DT-KHAC', partner: 'Đối tác Khác', percent: 10 }, NOW);
  const pay = async (o) => applyPayment(db, e, catalog, { id: Math.floor(Math.random() * 1e9), reference: 'r', amount: o.amount, content: 'NL' + o.code, code: o.code, raw: '' }, NOW);
  const a = await createOrder(db, catalog, mk('0912345678', 'AAAA-AAAA-AAAA', ['gia-su-ai', 'van-hoa-8'], 'DT-HOAI'), NOW, rnd(10)); await pay(a);
  const b = await createOrder(db, catalog, mk('0988000111', 'BBBB-BBBB-BBBB', ['gia-su-ai'], 'DT-HOAI'), NOW, rnd(20)); await pay(b);
  const c = await createOrder(db, catalog, mk('0977000222', 'CCCC-CCCC-CCCC', ['gia-su-ai'], 'DT-KHAC'), NOW, rnd(30)); await pay(c);
  await createOrder(db, catalog, mk('0966000333', 'DDDD-DDDD-DDDD', ['van-hoa-8'], 'DT-HOAI'), NOW, rnd(40)); // chưa trả tiền
  return { db, e, a, b, c };
}

test('mã truy cập đối tác: ổn định, khác nhau theo tên, đổi theo muối, chỉ khớp đối tác thật', async () => {
  const { db, e } = await setup();
  const t = await partnerToken(e, 'Đối tác Hoài');
  assert.equal(t, await partnerToken(e, 'Đối tác Hoài'));
  assert.notEqual(t, await partnerToken(e, 'Đối tác Khác'));
  assert.notEqual(t, await partnerToken({ ...e, PARTNER_SALT: 'x' }, 'Đối tác Hoài'));
  assert.equal(await partnerByToken(db, e, t), 'Đối tác Hoài');
  assert.equal(await partnerByToken(db, e, t.slice(0, -1) + (t.endsWith('a') ? 'b' : 'a')), null);
  assert.equal(await partnerByToken(db, e, ''), null);
  assert.equal(await partnerByToken(db, { ...e, ADMIN_TOKEN: '' }, t), null);
});

test('tổng hợp: chỉ tính khóa của đối tác, đã thanh toán, chưa thu hồi; che số điện thoại', async () => {
  const { db, a } = await setup();
  let r = await partnerSummary(db, catalog, 'Đối tác Hoài', {}, NOW);
  assert.equal(r.summary.orders, 2); assert.equal(r.summary.items, 3); assert.equal(r.summary.machines, 2);
  assert.equal(r.summary.pendingOrders, 1); assert.equal(r.summary.refundedItems, 0);
  assert.ok(r.orders.every((o) => /^•+\d{3}$/.test(o.phone)));
  assert.ok(!JSON.stringify(r).includes('0912345678'));
  await revokeItem(db, a.code, 'gia-su-ai', 'hoàn tiền', NOW);
  r = await partnerSummary(db, catalog, 'Đối tác Hoài', {}, NOW);
  assert.equal(r.summary.items, 2); assert.equal(r.summary.refundedItems, 1); assert.equal(r.summary.orders, 2);
  await revokeOrder(db, a.code, 'hoàn tiền', NOW);
  r = await partnerSummary(db, catalog, 'Đối tác Hoài', {}, NOW);
  assert.equal(r.summary.orders, 1); assert.equal(r.summary.machines, 1); assert.equal(r.summary.refundedItems, 2);
  const other = await partnerSummary(db, catalog, 'Đối tác Khác', {}, NOW);
  assert.equal(other.summary.items, 1);
  const none = await partnerSummary(db, catalog, 'Đối tác Hoài', { from: '2030-01-01' }, NOW);
  assert.equal(none.summary.items, 0);
});

test('đường dẫn: sai mã bị từ chối, đúng mã xem được, liên kết chỉ cho quản trị, trang không cần mật khẩu', async () => {
  const { e } = await setup();
  const post = (path, body, h = {}) => handle(new Request('https://x.test' + path, { method: 'POST', headers: { 'content-type': 'application/json', ...h }, body: JSON.stringify(body) }), e, NOW);
  assert.equal((await post('/api/partner/summary', { token: 'sai' })).status, 401);
  const t = await partnerToken(e, 'Đối tác Hoài');
  const ok = await post('/api/partner/summary', { token: t });
  assert.equal(ok.status, 200); assert.equal((await ok.json()).summary.items, 3);
  assert.equal((await handle(new Request('https://x.test/api/admin/partner-links'), e, NOW)).status, 401);
  const links = await (await handle(new Request('https://x.test/api/admin/partner-links', { headers: { authorization: 'Bearer admin-secret' } }), e, NOW)).json();
  assert.deepEqual(links.links.map((x) => x.partner).sort(), ['Đối tác Hoài', 'Đối tác Khác']);
  assert.equal(links.links.find((x) => x.partner === 'Đối tác Hoài').token, t);
  const page = await handle(new Request('https://x.test/doi-tac'), e, NOW);
  assert.equal(page.status, 200); assert.match(await page.text(), /Đối tác Nam Linh Educenter/);
});

test('hoa hồng 25% mỗi khóa; tổng trên 5 triệu thì khấu trừ 10% toàn bộ', async () => {
  assert.equal(commissionOf(799200), 199800);
  assert.deepEqual(commissionTotal(5000000), { percent: 25, gross: 5000000, taxPercent: 10, taxThreshold: 5000000, tax: 0, net: 5000000 });
  assert.deepEqual(commissionTotal(6000000), { percent: 25, gross: 6000000, taxPercent: 10, taxThreshold: 5000000, tax: 600000, net: 5400000 });
  const { db, a } = await setup();
  const r = await partnerSummary(db, catalog, 'Đối tác Hoài', {}, NOW);
  const sumC = r.byCourse.reduce((x, c) => x + c.commission, 0);
  assert.equal(r.commission.gross, sumC);
  assert.equal(r.orders.reduce((x, o) => x + (o.active ? o.commission : 0), 0), sumC);
  assert.equal(r.commission.tax, 0); assert.equal(r.commission.net, sumC);
  await revokeItem(db, a.code, 'gia-su-ai', 'hoàn tiền', NOW);
  const r2 = await partnerSummary(db, catalog, 'Đối tác Hoài', {}, NOW);
  assert.ok(r2.commission.gross < r.commission.gross);
});
