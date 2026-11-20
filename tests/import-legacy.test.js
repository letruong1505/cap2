const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('crypto');
const { parseLines } = require('../tools/import-legacy.js');

const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
const mk = (p) => { const body = Buffer.from(JSON.stringify({ v: 1, expires: 'never', ...p })); return 'NL1-' + body.toString('base64url') + '.' + crypto.sign(null, body, privateKey).toString('base64url'); };
const M = 'B6F5-AB86-A5A1';

test('dòng hợp lệ: lấy mã khóa, tên, mã máy, lớp từ khóa; số điện thoại từ dòng', () => {
  const k = mk({ id: 'NL-SGPTWN', owner: 'Lê Trường', grades: [9, 12], machine: M, issued: '2026-09-01' });
  const [r] = parseLines(`# ghi chú\n\n${k} ; 0912 345 678\n`, publicKey);
  assert.equal(r.ok, true);
  assert.deepEqual([r.body.code, r.body.name, r.body.phone, r.body.machine, r.body.grades], ['NL-SGPTWN', 'Lê Trường', '0912 345 678', M, [9, 12]]);
});

test('dòng lỗi được báo rõ lý do, không gửi lên', () => {
  const good = { id: 'NL-SGPTWN', owner: 'A B', grades: [9], machine: M };
  const lines = [
    mk(good) + ' ; ', // thiếu số điện thoại
    mk({ ...good, id: 'NL-0001' }) + ' ; 0912345678', // id không đúng dạng
    mk({ ...good, machine: '*' }) + ' ; 0912345678', // mọi máy
    mk(good).slice(0, -3) + 'AAA ; 0912345678', // sai chữ ký
    'khong-phai-khoa ; 0912345678',
  ].join('\n');
  const r = parseLines(lines, publicKey);
  assert.equal(r.length, 5);
  assert.ok(r.every((x) => !x.ok));
  assert.match(r[0].error, /số điện thoại/); assert.match(r[1].error, /6 ký tự/); assert.match(r[2].error, /mọi máy/);
  assert.match(r[3].error, /chữ ký/); assert.match(r[4].error, /định dạng/);
});

test('dòng nhập tay không cần khóa: mã khóa ; điện thoại ; tên ; mã máy ; lớp', () => {
  const [a, b, c, d, e] = parseLines([
    'nl-43356a ; 0968 646 853 ; Lê Trường ; b6f5-ab86-a5a1 ; 9, 12',
    'NL-43356A ; 0968646853 ; Lê Trường ; B6F5-AB86-A5A1 ; all',
    'NL-43356A ; 0968646853 ; Lê Trường ; sai ; 9',
    'NL-0001 ; 0968646853 ; Lê Trường ; B6F5-AB86-A5A1 ; 9',
    'NL-43356A ; 0968646853 ; Lê Trường ; B6F5-AB86-A5A1 ; ',
  ].join('\n'), null);
  assert.equal(a.ok, true);
  assert.deepEqual([a.body.code, a.body.machine, a.body.grades, a.body.name], ['NL-43356A', 'B6F5-AB86-A5A1', [9, 12], 'Lê Trường']);
  assert.equal(b.body.grades, 'all');
  assert.match(c.error, /mã máy/); assert.match(d.error, /6 ký tự/); assert.match(e.error, /lớp/);
});
