/* Mã PIN phụ huynh: lưu băm PBKDF2 trên máy, khóa tạm khi nhập sai, mã khôi phục dùng một lần.
   Logic thuần (nhận storage và crypto từ ngoài) để kiểm thử được. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VungPin = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const KEY = 'vungbai.pin.v1';
  const ITER = 120000;
  const MAX_FAILS = 5;
  const LOCK_MS = 5 * 60 * 1000;
  const ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  const PIN_RE = /^\d{4,6}$/;

  const hex = (buf) => Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('');
  const rnd = (c, n) => c.getRandomValues(new Uint8Array(n));

  async function hash(c, secret, saltHex) {
    const salt = Uint8Array.from(saltHex.match(/../g), (h) => parseInt(h, 16));
    const k = await c.subtle.importKey('raw', new TextEncoder().encode(secret), 'PBKDF2', false, ['deriveBits']);
    return hex(await c.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations: ITER }, k, 256));
  }

  const normCode = (s) => String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  const fmtCode = (s) => s.match(/.{4}/g).join('-');
  function newRecoveryCode(c) { return fmtCode(Array.from(rnd(c, 12), (x) => ALPHABET[x % ALPHABET.length]).join('')); }

  function read(st) { try { return JSON.parse(st.getItem(KEY)) || null; } catch (e) { return null; } }
  function write(st, d) { try { if (d) st.setItem(KEY, JSON.stringify(d)); else st.removeItem(KEY); } catch (e) { /* bỏ qua */ } }

  const isSet = (st) => { const d = read(st); return !!(d && d.hash); };
  const validPin = (pin) => PIN_RE.test(String(pin || ''));

  /* Đặt hoặc đổi PIN; trả về mã khôi phục mới (chỉ hiện một lần). */
  async function setPin(st, pin, c = globalThis.crypto) {
    if (!validPin(pin)) throw new Error('Mã PIN gồm 4 đến 6 chữ số.');
    const salt = hex(rnd(c, 16)); const rsalt = hex(rnd(c, 16));
    const recovery = newRecoveryCode(c);
    write(st, { salt, hash: await hash(c, String(pin), salt), rsalt, rhash: await hash(c, normCode(recovery), rsalt), fails: 0, lockUntil: 0 });
    return recovery;
  }

  /* Ghi nhận một lần nhập sai; khóa tạm sau MAX_FAILS lần. */
  function fail(st, d, now) {
    d.fails = (d.fails || 0) + 1;
    if (d.fails >= MAX_FAILS) { d.fails = 0; d.lockUntil = now + LOCK_MS; }
    write(st, d);
    return { ok: false, locked: d.lockUntil > now, remainMs: Math.max(0, d.lockUntil - now), left: MAX_FAILS - d.fails };
  }
  const lockedNow = (d, now) => (d.lockUntil > now ? { ok: false, locked: true, remainMs: d.lockUntil - now, left: 0 } : null);

  async function verify(st, pin, now = Date.now(), c = globalThis.crypto) {
    const d = read(st);
    if (!d) return { ok: true };
    const l = lockedNow(d, now); if (l) return l;
    if (d.hash === await hash(c, String(pin || ''), d.salt)) { d.fails = 0; write(st, d); return { ok: true }; }
    return fail(st, d, now);
  }

  /* Quên PIN, có mã khôi phục: đặt PIN mới và cấp mã khôi phục mới. */
  async function recover(st, code, newPin, now = Date.now(), c = globalThis.crypto) {
    const d = read(st);
    if (!d) return { ok: false, error: 'Chưa đặt mã PIN.' };
    if (!validPin(newPin)) return { ok: false, error: 'Mã PIN gồm 4 đến 6 chữ số.' };
    const l = lockedNow(d, now); if (l) return l;
    if (d.rhash !== await hash(c, normCode(code), d.rsalt)) return fail(st, d, now);
    return { ok: true, recovery: await setPin(st, newPin, c) };
  }

  /* Sau khi máy chủ xác nhận đơn hàng: đặt PIN mới mà không cần mã cũ. */
  async function resetVerified(st, newPin, c = globalThis.crypto) {
    return { ok: true, recovery: await setPin(st, newPin, c) };
  }

  function clear(st) { write(st, null); }

  return { KEY, MAX_FAILS, LOCK_MS, isSet, validPin, setPin, verify, recover, resetVerified, clear, normCode };
});
