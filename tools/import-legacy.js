#!/usr/bin/env node
// Công cụ của CHỦ SẢN PHẨM: nhập các khóa cũ cấp bằng USB vào hệ thống đơn hàng (Worker), để máy gửi tín hiệu,
// gửi kết quả học cho phụ huynh và trang quản lý có đủ đơn. Khóa đã nhập là đơn "đã thanh toán" 0 đ, ghi chú "Khóa cũ cấp bằng USB".
//   ADMIN_TOKEN=... node tools/import-legacy.js khoa-cu.txt [--dry-run] [--api https://...]
// Mỗi dòng trong file: <khóa NL1-...> ; <số điện thoại phụ huynh>      (dòng trống hoặc bắt đầu bằng # bị bỏ qua)
// Khóa được kiểm tra chữ ký bằng khóa công khai của sản phẩm trước khi gửi; mã khóa (id) phải có dạng NL- + 6 ký tự.
const fs = require('fs');
const path = require('path');
const { parseKey } = require('../main/license/verify');

const argv = process.argv.slice(2);
const flag = (n) => argv.includes('--' + n);
const opt = (n, d) => { const i = argv.indexOf('--' + n); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };
const file = argv.find((a) => !a.startsWith('--') && a !== opt('api'));

// Đọc và kiểm tra từng dòng; trả về danh sách {line, ok, error, body}. Tách riêng để kiểm thử.
function parseLines(text, pubKey) {
  return text.split(/\r?\n/).map((raw, i) => ({ raw: raw.trim(), n: i + 1 })).filter((l) => l.raw && !l.raw.startsWith('#')).map(({ raw, n }) => {
    const [k, phone = ''] = raw.split(/[;\t|]/).map((s) => s.trim());
    const r = parseKey(k, pubKey);
    if (!r.ok) return { n, ok: false, error: r.reason === 'signature' ? 'chữ ký khóa không hợp lệ' : 'khóa không đúng định dạng' };
    const p = r.payload;
    if (!/^NL-[A-Z0-9]{6}$/.test(p.id || '')) return { n, ok: false, error: `mã khóa "${p.id || ''}" không có dạng NL- + 6 ký tự (cần cấp lại khóa mới cho khách)` };
    if (!p.machine || p.machine === '*') return { n, ok: false, error: 'khóa dùng cho mọi máy, không gắn được vào một máy' };
    if (!/^(0|\+84)\d{9}$/.test(phone.replace(/[\s.\-]/g, ''))) return { n, ok: false, error: 'thiếu hoặc sai số điện thoại phụ huynh (sau dấu ;)' };
    return { n, ok: true, body: { code: p.id, name: p.owner || '', phone, machine: p.machine, grades: p.grades, courses: p.courses || [], issued: p.issued, key: k } };
  });
}

async function main() {
  if (!file) { console.error('Dùng: ADMIN_TOKEN=... node tools/import-legacy.js <file> [--dry-run] [--api URL]'); process.exit(1); }
  const items = parseLines(fs.readFileSync(path.resolve(file), 'utf8'));
  const api = opt('api', process.env.NL_API || require('../main/orders-api.json').baseUrl || '').replace(/\/$/, '');
  const token = process.env.ADMIN_TOKEN;
  let fail = 0;
  for (const it of items) {
    if (!it.ok) { console.log(`Dòng ${it.n}: BỎ QUA - ${it.error}`); fail++; continue; }
    const b = it.body;
    const what = `${b.code} · ${b.name} · ${b.phone} · máy ${b.machine} · ${b.grades === 'all' ? 'tất cả lớp' : 'lớp ' + b.grades.join(',')}`;
    if (flag('dry-run')) { console.log(`Dòng ${it.n}: SẼ NHẬP ${what}`); continue; }
    if (!token || !api) { console.error('Thiếu ADMIN_TOKEN hoặc địa chỉ máy chủ (--api).'); process.exit(1); }
    const r = await fetch(api + '/api/admin/import-legacy', { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + token }, body: JSON.stringify(b) });
    const d = await r.json().catch(() => ({}));
    if (r.ok) console.log(`Dòng ${it.n}: ĐÃ NHẬP ${what}`);
    else { console.log(`Dòng ${it.n}: LỖI - ${d.error || r.status} (${b.code})`); fail++; }
  }
  console.log(fail ? `Xong, ${fail} dòng không nhập được.` : 'Xong.');
  process.exit(fail ? 1 : 0);
}

if (require.main === module) main().catch((e) => { console.error(e.message); process.exit(1); });
module.exports = { parseLines };
