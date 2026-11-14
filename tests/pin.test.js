const test = require('node:test');
const assert = require('node:assert/strict');
const PIN = require('../renderer/pin.js');

const mem = () => { const m = {}; return { getItem: (k) => (k in m ? m[k] : null), setItem: (k, v) => { m[k] = String(v); }, removeItem: (k) => { delete m[k]; }, raw: m }; };

test('đặt PIN: chỉ nhận 4–6 chữ số, không lưu PIN dạng thô', async () => {
  const st = mem();
  await assert.rejects(PIN.setPin(st, '12'), /4 đến 6/);
  await assert.rejects(PIN.setPin(st, 'abcd'), /4 đến 6/);
  assert.equal(PIN.isSet(st), false);
  const rec = await PIN.setPin(st, '2468');
  assert.match(rec, /^[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{4}$/);
  assert.equal(PIN.isSet(st), true);
  const raw = st.getItem(PIN.KEY);
  assert.ok(!raw.includes('2468'));
  assert.ok(!raw.replace(/-/g, '').includes(rec.replace(/-/g, '')));
});

test('xác nhận PIN: đúng và sai', async () => {
  const st = mem(); await PIN.setPin(st, '2468');
  assert.equal((await PIN.verify(st, '2468')).ok, true);
  const bad = await PIN.verify(st, '1111');
  assert.equal(bad.ok, false);
  assert.equal(bad.left, 4);
});

test('nhập sai 5 lần thì khóa 5 phút, hết giờ nhập lại được', async () => {
  const st = mem(); await PIN.setPin(st, '2468');
  const t0 = 1_000_000;
  let r;
  for (let i = 0; i < 5; i++) r = await PIN.verify(st, '0000', t0);
  assert.equal(r.locked, true);
  assert.equal((await PIN.verify(st, '2468', t0 + 1000)).locked, true);
  assert.equal((await PIN.verify(st, '2468', t0 + PIN.LOCK_MS + 1)).ok, true);
});

test('mã khôi phục: đặt PIN mới, mã cũ hết hiệu lực, mã mới cấp lại', async () => {
  const st = mem(); const rec = await PIN.setPin(st, '2468');
  const wrong = await PIN.recover(st, 'AAAA-AAAA-AAAA', '1357');
  assert.equal(wrong.ok, false);
  assert.equal((await PIN.verify(st, '2468')).ok, true);
  const r = await PIN.recover(st, rec.toLowerCase().replace(/-/g, ' '), '1357');
  assert.equal(r.ok, true);
  assert.notEqual(r.recovery, rec);
  assert.equal((await PIN.verify(st, '1357')).ok, true);
  assert.equal((await PIN.verify(st, '2468')).ok, false);
  assert.equal((await PIN.recover(st, rec, '9999')).ok, false);
});

test('đặt lại sau khi máy chủ xác nhận, và tắt PIN', async () => {
  const st = mem(); await PIN.setPin(st, '2468');
  const r = await PIN.resetVerified(st, '7777');
  assert.equal(r.ok, true);
  assert.equal((await PIN.verify(st, '7777')).ok, true);
  PIN.clear(st);
  assert.equal(PIN.isSet(st), false);
  assert.equal((await PIN.verify(st, 'x')).ok, true);
});
