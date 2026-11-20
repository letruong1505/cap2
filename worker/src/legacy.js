import { HttpError, MACHINE_RE, getOrder } from './orders.js';

// Nhập khóa cũ cấp bằng USB (không có trong hệ thống): tạo đơn "đã thanh toán" 0 đ để máy gửi tín hiệu, gửi kết quả học và hỗ trợ sau bán hàng.
// Chữ ký của khóa do công cụ nhập (tools/import-legacy.js) kiểm tra trên máy quản trị; ở đây chỉ kiểm tra dữ liệu.
export async function importLegacy(db, catalog, input, now = new Date()) {
  const code = String(input.code || '').toUpperCase().replace(/^NL-/, '');
  const name = String(input.name || '').trim().replace(/\s+/g, ' ');
  const phone = String(input.phone || '').replace(/[\s.\-]/g, '');
  const machine = String(input.machine || '').trim().toUpperCase();
  const key = String(input.key || '').replace(/\s+/g, '').slice(0, 2000);
  if (!/^[ABCDEFGHJKMNPQRSTUVWXYZ2-9]{6}$/.test(code)) throw new HttpError(400, 'Mã khóa phải có dạng NL- và 6 ký tự (chữ in hoa, số).');
  if (name.length < 2 || name.length > 80) throw new HttpError(400, 'Họ và tên không hợp lệ.');
  if (!/^(0|\+84)\d{9}$/.test(phone)) throw new HttpError(400, 'Số điện thoại không hợp lệ.');
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Mã máy không hợp lệ (khóa dùng cho mọi máy thì không nhập được).');
  const vh = catalog.ALL.map((x) => x.id).filter((id) => /^van-hoa-\d+$/.test(id));
  const grades = input.grades === 'all' ? vh : (Array.isArray(input.grades) ? input.grades.map((g) => `van-hoa-${Number(g)}`) : []);
  const courses = Array.isArray(input.courses) ? input.courses.map(String) : [];
  const items = [...new Set([...grades, ...courses])];
  if (!items.length || items.some((id) => !catalog.byId[id])) throw new HttpError(400, 'Khóa có lớp hoặc khóa học không có trong danh mục.');
  if (await getOrder(db, code)) throw new HttpError(409, 'Mã này đã có trong hệ thống.');
  const issued = /^\d{4}-\d{2}-\d{2}$/.test(String(input.issued || '')) ? `${input.issued}T00:00:00.000Z` : now.toISOString();
  await db.batch([
    db.prepare("INSERT INTO orders (code, name, phone, machine, items, amount, status, paid_amount, key, terms_version, created_at, paid_at, note) VALUES (?1,?2,?3,?4,?5,0,'paid',0,?6,'usb-cũ',?7,?7,?8)")
      .bind(code, name, phone, machine, JSON.stringify(items), key || null, issued, String(input.note || 'Khóa cũ cấp bằng USB, nhập vào hệ thống').slice(0, 200)),
    db.prepare("INSERT INTO order_devices (code, platform, machine, key, issued_at) VALUES (?1,'win',?2,?3,?4)").bind(code, machine, key || null, issued),
    ...items.map((id) => db.prepare('INSERT INTO order_prices (code, item, list_price, paid_price) VALUES (?1,?2,?3,0)').bind(code, id, catalog.byId[id].price || 0)),
  ]);
  return { ok: true, code, items };
}
