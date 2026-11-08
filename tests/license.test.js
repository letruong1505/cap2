const test = require('node:test');
const assert = require('node:assert');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { PREFIX, b64u, evaluateKey } = require('../main/license/verify');
const lic = require('../main/license');
const { getMachineId } = require('../main/license/machine');

const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
function issue(p, priv = privateKey) {
  const body = Buffer.from(JSON.stringify({ v: 1, id: 'T1', owner: 'Test', grades: [7], machine: '*', issued: '2026-01-01', expires: '2099-01-01', ...p }));
  return PREFIX + b64u(body) + '.' + b64u(crypto.sign(null, body, priv));
}
const NOW = new Date(2026, 10, 9);

test('khoá hợp lệ', () => assert.equal(evaluateKey(issue({}), 'AAAA-AAAA-AAAA', NOW, publicKey).status, 'ok'));
test('sai chữ ký', () => {
  const other = crypto.generateKeyPairSync('ed25519').privateKey;
  assert.equal(evaluateKey(issue({}, other), 'X', NOW, publicKey).status, 'invalid');
});
test('sửa nội dung khoá bị từ chối', () => {
  const k = issue({ grades: [7] });
  const [h, s] = k.split('.');
  const body = JSON.parse(Buffer.from(h.slice(PREFIX.length), 'base64url'));
  body.grades = 'all';
  const forged = PREFIX + b64u(JSON.stringify(body)) + '.' + s;
  assert.equal(evaluateKey(forged, 'X', NOW, publicKey).status, 'invalid');
});
test('sai máy', () => assert.equal(evaluateKey(issue({ machine: 'AAAA-AAAA-AAAA' }), 'BBBB-BBBB-BBBB', NOW, publicKey).status, 'wrong-machine'));
test('hết hạn', () => assert.equal(evaluateKey(issue({ expires: '2026-11-08' }), 'X', NOW, publicKey).status, 'expired'));
test('rác', () => assert.equal(evaluateKey('abc', 'X', NOW, publicKey).status, 'invalid'));

test('phân quyền bài theo lớp', () => {
  const man = { books: [{ chapters: [{ lessons: [{ file: 'a' }, { file: 'b' }, { file: 'c' }] }] }] };
  const none = { status: 'missing' };
  assert.ok(lic.canOpen(none, 'toan7', man, 'a') && lic.canOpen(none, 'toan7', man, 'b'));
  assert.ok(!lic.canOpen(none, 'toan7', man, 'c'));
  const g7 = { status: 'ok', grades: [7] };
  assert.ok(lic.canOpen(g7, 'toan7', man, 'c'));
  assert.ok(!lic.canOpen(g7, 'toan8', man, 'c'));
  assert.ok(lic.canOpen({ status: 'ok', grades: 'all' }, 'ly8', man, 'c'));
  assert.ok(!lic.canOpen({ status: 'expired', grades: 'all' }, 'ly8', man, 'c'));
});

test('kích hoạt thật bằng khoá công khai trong repo', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lic-'));
  assert.equal(lic.currentLicense(dir).status, 'missing');
  assert.equal(lic.activate(dir, 'NL1-rac.rac').status, 'invalid');
  assert.equal(lic.currentLicense(dir).status, 'missing');
  assert.match(getMachineId(), /^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/);
});
