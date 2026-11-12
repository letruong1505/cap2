// Cập nhật phần mềm qua mạng. Chỉ chạy khi: app đã cài (không phải chế độ dev), có địa chỉ máy chủ
// cập nhật, và sản phẩm là Nam Linh Educenter. Người dùng luôn được hỏi trước khi tải và trước khi cài.
// Phần lõi nhận autoUpdater và hàm gửi tin vào dạng tham số để kiểm thử không cần Electron.
function createUpdater({ autoUpdater, send, url, enabled = true, version = '' }) {
  const feed = String(url || '').trim().replace(/\/+$/, '');
  const active = !!(enabled && /^https:\/\//i.test(feed));
  let state = { state: active ? 'idle' : 'off', version: '', percent: 0, error: '' };

  const set = (patch) => { state = { ...state, ...patch }; send(state); return state; };

  if (active) {
    autoUpdater.autoDownload = false;
    autoUpdater.autoInstallOnAppQuit = false;
    autoUpdater.allowPrerelease = false;
    autoUpdater.setFeedURL({ provider: 'generic', url: feed });
    autoUpdater.on('checking-for-update', () => set({ state: 'checking', error: '' }));
    autoUpdater.on('update-available', (i) => set({ state: 'available', version: String(i && i.version || '') }));
    autoUpdater.on('update-not-available', () => set({ state: 'none' }));
    autoUpdater.on('download-progress', (p) => set({ state: 'downloading', percent: Math.round(p && p.percent || 0) }));
    autoUpdater.on('update-downloaded', (i) => set({ state: 'ready', percent: 100, version: String(i && i.version || state.version) }));
    autoUpdater.on('error', (e) => set({ state: 'error', error: String(e && e.message || e).slice(0, 200) }));
  }

  return {
    active,
    status: () => state,
    // Kiểm tra bản mới. Lỗi mạng chỉ ghi vào trạng thái, không làm hỏng app đang chạy offline.
    async check() {
      if (!active || state.state === 'downloading' || state.state === 'ready') return state;
      try { await autoUpdater.checkForUpdates(); } catch (e) { set({ state: 'error', error: String(e && e.message || e).slice(0, 200) }); }
      return state;
    },
    async download() {
      if (!active || state.state !== 'available') return state;
      set({ state: 'downloading', percent: 0 });
      try { await autoUpdater.downloadUpdate(); } catch (e) { set({ state: 'error', error: String(e && e.message || e).slice(0, 200) }); }
      return state;
    },
    install() {
      if (!active || state.state !== 'ready') return false;
      autoUpdater.quitAndInstall(false, true);
      return true;
    },
  };
}

module.exports = { createUpdater };
