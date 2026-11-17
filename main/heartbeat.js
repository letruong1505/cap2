// Tín hiệu định kỳ về máy chủ khi phần mềm đang mở: để chủ sản phẩm thấy máy nào đang dùng khóa nào, và nhận danh sách khóa bị thu hồi.
// Không có mạng hoặc máy chủ lỗi thì bỏ qua, phần mềm vẫn học bình thường (khóa đã bị thu hồi từ trước vẫn bị vô hiệu vì đã lưu trên máy).
const INTERVAL_MS = 5 * 60 * 1000;

function createHeartbeat({ dir, client, lic, version, intervalMs = INTERVAL_MS, setIntervalFn = setInterval, setTimeoutFn = setTimeout }) {
  let timer = null;
  async function beat() {
    const ids = lic.pingCodes(dir);
    if (!ids.length) return { sent: false };
    const r = await client.ping({ ids, version });
    if (!r.ok) return { sent: true, ok: false };
    const changed = Array.isArray(r.data && r.data.revoked) ? lic.setRevoked(dir, r.data.revoked) : false;
    return { sent: true, ok: true, changed };
  }
  function start() {
    if (timer) return;
    setTimeoutFn(() => { beat().catch(() => {}); }, 8000);
    timer = setIntervalFn(() => { beat().catch(() => {}); }, intervalMs);
    if (timer && timer.unref) timer.unref();
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  return { beat, start, stop };
}

module.exports = { createHeartbeat, INTERVAL_MS };
