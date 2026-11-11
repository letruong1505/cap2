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
      terms: { version: String(o && o.terms && o.terms.version || ''), at: String(o && o.terms && o.terms.at || '') }, machineId: machineId(),
    }),
    orderStatus: (code) => call('GET', `/api/orders/${encodeURIComponent(String(code).slice(0, 6))}/status?machine=${encodeURIComponent(machineId())}`),
  };
}

module.exports = { makeClient, ...makeClient() };
