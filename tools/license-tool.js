#!/usr/bin/env node
// Công cụ của CHỦ SẢN PHẨM (không đưa vào bản cài): tạo cặp khoá, cấp khoá bản quyền, xem khoá.
//   node tools/license-tool.js init
//   node tools/license-tool.js issue --owner "Tên" --grades 7,8 --machine XXXX-XXXX-XXXX --expires 2027-06-30 [--id NL-0001]
//   node tools/license-tool.js issue --owner "Tên" --grades all --any-machine --expires 2027-06-30
//   node tools/license-tool.js issue --owner "Tên" --grades 6,7,8,9 --machine XXXX-XXXX-XXXX --permanent
//   node tools/license-tool.js inspect <khoá>
// Khoá riêng nằm ở ~/.vungbai-license/private.pem (hoặc biến VUNGBAI_PRIVATE_KEY). KHÔNG đưa vào git.
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { PREFIX, b64u, parseKey } = require('../main/license/verify');

const PRIVATE = process.env.VUNGBAI_PRIVATE_KEY || path.join(os.homedir(), '.vungbai-license', 'private.pem');
const PUBLIC = path.join(__dirname, '..', 'main', 'license', 'public-key.pem');

function args(list) {
  const o = {};
  for (let i = 0; i < list.length; i++) {
    if (!list[i].startsWith('--')) continue;
    const k = list[i].slice(2);
    o[k] = list[i + 1] && !list[i + 1].startsWith('--') ? list[++i] : true;
  }
  return o;
}

function die(msg) { console.error(msg); process.exit(1); }

const [cmd, ...rest] = process.argv.slice(2);
if (cmd === 'init') {
  if (fs.existsSync(PRIVATE)) die('Đã có khoá riêng tại ' + PRIVATE + '. Tạo lại sẽ làm mọi khoá đã cấp mất hiệu lực, nên công cụ không ghi đè.');
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  fs.mkdirSync(path.dirname(PRIVATE), { recursive: true });
  fs.writeFileSync(PRIVATE, privateKey.export({ type: 'pkcs8', format: 'pem' }), { mode: 0o600 });
  fs.writeFileSync(PUBLIC, publicKey.export({ type: 'spki', format: 'pem' }));
  console.log('Đã tạo khoá riêng: ' + PRIVATE + ' (hãy sao lưu an toàn)\nĐã ghi khoá công khai: ' + PUBLIC + ' (commit file này, rồi build lại app)');
} else if (cmd === 'issue') {
  const a = args(rest);
  if (!fs.existsSync(PRIVATE)) die('Chưa có khoá riêng. Chạy: node tools/license-tool.js init');
  if (!a.owner || a.owner === true) die('Thiếu --owner');
  if (!a.permanent && !/^\d{4}-\d{2}-\d{2}$/.test(a.expires || '')) die('Thiếu --permanent hoặc --expires (YYYY-MM-DD)');
  const expires = a.permanent ? 'never' : a.expires;
  let grades;
  if (a.grades === 'all') grades = 'all';
  else {
    grades = String(a.grades || '').split(',').map((s) => parseInt(s, 10));
    if (!grades.length || grades.some((g) => !Number.isInteger(g))) die('--grades là danh sách lớp (7,8) hoặc all');
  }
  let machine;
  if (a['any-machine']) machine = '*';
  else if (/^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/.test(String(a.machine || '').toUpperCase())) machine = a.machine.toUpperCase();
  else die('Cần --machine XXXX-XXXX-XXXX (mã máy hiện trong app) hoặc --any-machine');
  const id = a.id && a.id !== true ? a.id : 'NL-' + crypto.randomBytes(3).toString('hex').toUpperCase();
  const payload = Buffer.from(JSON.stringify({ v: 1, id, owner: a.owner, grades, machine, issued: new Date().toISOString().slice(0, 10), expires }));
  const sig = crypto.sign(null, payload, crypto.createPrivateKey(fs.readFileSync(PRIVATE, 'utf8')));
  console.log(PREFIX + b64u(payload) + '.' + b64u(sig));
} else if (cmd === 'inspect') {
  const r = parseKey(rest.join(''));
  console.log(r.ok ? JSON.stringify(r.payload, null, 2) : 'Khoá không hợp lệ (' + r.reason + ')');
} else {
  die('Lệnh: init | issue | inspect');
}
