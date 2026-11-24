// Gọi máy chủ đơn hàng (Cloudflare Worker) từ tiến trình chính. Lỗi mạng hoặc chưa cấu hình thì trả offline để giao diện dùng cách gửi đơn qua Zalo.
const fs = require('fs');
const path = require('path');
const { getMachineId } = require('./license/machine');

function readBaseUrl() {
  try { return String(JSON.parse(fs.readFileSync(path.join(__dirname, 'orders-api.json'), 'utf8')).baseUrl || '').replace(/\/+$/, ''); } catch { return ''; }
}

function makeClient({ baseUrl = readBaseUrl, fetchFn = (...a) => fetch(...a), machineId = getMachineId } = {}) {
  async function call(method, route, body) {
    const base = String(baseUrl() || '').replace(/\/+$/, '');
    if (!base) return { ok: false, offline: true };
    try {
      const r = await fetchFn(base + route, { method, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(10000) });
      const data = await r.json().catch(() => ({}));
      if (r.ok) return { ok: true, data };
      if (r.status >= 500) return { ok: false, offline: true };
      return { ok: false, error: data.error || 'Không xử lý được yêu cầu.' };
    } catch {
      return { ok: false, offline: true };
    }
  }
  return {
    // Giao diện chỉ gửi thông tin phụ huynh và danh sách khóa; mã máy do tiến trình chính tự thêm.
    createOrder: (o) => call('POST', '/api/orders', {
      name: String(o && o.name || ''), phone: String(o && o.phone || ''), ids: Array.isArray(o && o.ids) ? o.ids.map(String) : [],
      partnerCode: String(o && o.partnerCode || '').trim().slice(0, 20),
      terms: { version: String(o && o.terms && o.terms.version || ''), at: String(o && o.terms && o.terms.at || '') }, machineId: machineId(),
    }),
    // Nhận khóa cho máy tính này từ đơn mua trên điện thoại: nhập mã đơn + số điện thoại đã mua.
    claimDevice: (o) => call('POST', '/api/claim-device', { phone: String(o && o.phone || ''), code: String(o && o.code || ''), machineId: machineId(), platform: 'win' }),
    // Máy tính của con nhận khóa các đơn phụ huynh mua cho gia đình (mã gia đình nhập một lần).
    familySync: (o) => call('POST', '/api/family/sync', { fcode: String(o && o.fcode || ''), machineId: machineId(), platform: 'win' }),
    pinReset: (o) => call('POST', '/api/pin-reset', { phone: String(o && o.phone || ''), code: String(o && o.code || ''), machineId: machineId() }),
    // Khách tự đăng ký khóa cũ (cấp bằng USB) vào hệ thống: gửi khóa NL1-... (do tiến trình chính đọc từ kho khóa) và số điện thoại phụ huynh.
    registerLegacy: (o) => call('POST', '/api/register-legacy', { key: String(o && o.key || ''), phone: String(o && o.phone || ''), machineId: machineId() }),
    // Phụ huynh xem kết quả học trên điện thoại: máy học sinh bật/tắt và gửi tóm tắt theo ngày (không có từng câu trả lời).
    progressSettings: (o) => call('POST', '/api/progress/settings', { code: String(o && o.code || ''), machineId: machineId(), enabled: o && typeof o.enabled === 'boolean' ? o.enabled : undefined, purge: o && o.purge === true ? true : undefined, goals: o && o.goals && typeof o.goals === 'object' ? { daily: Number(o.goals.daily), weekend: Number(o.goals.weekend), weekly: Number(o.goals.weekly), pass: Number(o.goals.pass) || undefined, passBy: o.goals.passBy && typeof o.goals.passBy === 'object' ? o.goals.passBy : undefined } : undefined, reward: o && o.reward && typeof o.reward === 'object' ? o.reward : undefined, timetable: o && o.timetable && typeof o.timetable === 'object' ? o.timetable : undefined, orientation: o && Array.isArray(o.orientation) ? o.orientation.slice(0, 3).map(String) : undefined }),
    progressPush: (o) => call('POST', '/api/progress/push', { code: String(o && o.code || ''), machineId: machineId(), days: Array.isArray(o && o.days) ? o.days : [], usage: Array.isArray(o && o.usage) ? o.usage.slice(0, 400) : [] }),
    progressView: (o) => call('POST', '/api/progress/view', { code: String(o && o.code || ''), phone: String(o && o.phone || ''), machineId: machineId(), from: String(o && o.from || ''), to: String(o && o.to || ''), grade: Number(o && o.grade) || 0 }),
    // Tín hiệu "máy này đang mở phần mềm" + nhận danh sách mã đơn bị thu hồi. Chỉ gửi mã máy, mã đơn và số bản, không gửi dữ liệu học tập.
    ping: (o) => call('POST', '/api/ping', { machineId: machineId(), ids: Array.isArray(o && o.ids) ? o.ids.map(String) : [], version: String(o && o.version || '') }),
    // Xin khoá giải mã gói nội dung các lớp đang có bản quyền: gửi các khoá NL1-... đã kích hoạt, máy chủ tự kiểm tra chữ ký, mã máy, hạn và thu hồi.
    packKeys: (o) => call('POST', '/api/pack/keys', { machineId: machineId(), keys: Array.isArray(o && o.keys) ? o.keys.slice(0, 10).map(String) : [] }),
    orderStatus: (code) => call('GET', `/api/orders/${encodeURIComponent(String(code).slice(0, 6))}/status?machine=${encodeURIComponent(machineId())}`),
  };
}

module.exports = { makeClient, ...makeClient() };
