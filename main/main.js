const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');
const { loadManifest, loadLesson, productInfo } = require('./content-loader');
const lic = require('./license');
const orders = require('./orders');
const { createUpdater } = require('./updater');
const { createStore } = require('./persist');
const { createHeartbeat } = require('./heartbeat');

const APP_TITLE = productInfo().title;


// build-info.json do workflow tạo khi build (số phiên bản và mã commit). Chạy dev thì không có file này.
function readBuildInfo() {
  try {
    return JSON.parse(fs.readFileSync(path.join(__dirname, 'build-info.json'), 'utf8'));
  } catch {
    return { version: 'dev', commit: 'local' };
  }
}

// Khoá bản quyền lưu trong thư mục dữ liệu của app (không nằm cạnh file exe).
const licenseStoreDir = () => app.getPath('userData');
const licenseNow = () => lic.currentLicense(licenseStoreDir());

ipcMain.handle('manifest:load', (_event, subject) => lic.annotateManifest(licenseNow(), subject, loadManifest(subject)));
ipcMain.handle('lesson:load', (_event, relPath) => {
  // Chặn ở tiến trình chính: bài bị khoá thì không trả nội dung dù giao diện bị chỉnh sửa.
  const [subject, ...parts] = String(relPath).split('/');
  if (!lic.canOpen(licenseNow(), subject, loadManifest(subject), parts.join('/'))) {
    throw new Error('LOCKED');
  }
  return loadLesson(relPath);
});
ipcMain.handle('app:info', () => readBuildInfo());
ipcMain.handle('product:info', () => productInfo());


// Dữ liệu người dùng (PIN, câu sai, tiến độ...) lưu ra file trong thư mục cố định, không phụ thuộc tên ứng dụng hay bản cài.
let userStore = null;
const getUserStore = () => userStore || (userStore = createStore(path.join(app.getPath('appData'), 'Nam Linh Educenter')));
ipcMain.on('store:all', (event) => { try { event.returnValue = getUserStore().all(); } catch { event.returnValue = {}; } });
ipcMain.on('store:set', (_event, key, value) => { try { getUserStore().set(key, value); } catch { /* bỏ qua */ } });

ipcMain.handle('license:load', () => licenseNow());
let heartbeat = null;
ipcMain.handle('license:activate', (_event, key) => {
  const r = lic.activate(licenseStoreDir(), key);
  if (heartbeat) heartbeat.beat().catch(() => {}); // báo ngay cho máy chủ biết máy đã kích hoạt
  return r;
});
ipcMain.handle('order:create', (_event, order) => orders.createOrder(order));
// Nhận khóa cho máy tính này từ đơn mua trên điện thoại, kích hoạt luôn và báo máy chủ.
ipcMain.handle('device:claim', async (_event, o) => {
  const r = await orders.claimDevice(o);
  if (r.ok && r.data && r.data.key) {
    r.license = lic.activate(licenseStoreDir(), r.data.key);
    if (heartbeat) heartbeat.beat().catch(() => {});
  }
  return r;
});
ipcMain.handle('pin:reset', (_event, o) => orders.pinReset(o));
ipcMain.handle('order:status', (_event, code) => orders.orderStatus(code));
ipcMain.handle('license:remove', () => { lic.deactivate(licenseStoreDir()); return licenseNow(); });

let updater = null;
function setupUpdater(win) {
  let url = '';
  try { url = JSON.parse(fs.readFileSync(path.join(__dirname, 'update-config.json'), 'utf8')).url; } catch { /* không có cấu hình thì tắt cập nhật */ }
  let autoUpdater = null;
  if (app.isPackaged && productInfo().id === 'nam-linh-educenter') {
    try { ({ autoUpdater } = require('electron-updater')); } catch { autoUpdater = null; }
  }
  updater = createUpdater({
    autoUpdater,
    enabled: !!autoUpdater,
    url,
    send: (st) => { if (!win.isDestroyed()) win.webContents.send('update:status', st); },
  });
  // Kiểm tra sau khi mở 8 giây, rồi lặp lại mỗi 2 giờ khi phần mềm vẫn đang mở.
  if (updater.active) {
    setTimeout(() => updater.check(), 8000);
    setInterval(() => updater.check(), 2 * 60 * 60 * 1000);
  }
}
ipcMain.handle('update:status', () => (updater ? updater.status() : { state: 'off' }));
ipcMain.handle('update:check', () => (updater ? updater.check() : { state: 'off' }));
ipcMain.handle('update:download', () => (updater ? updater.download() : { state: 'off' }));
ipcMain.handle('update:install', () => (updater ? updater.install() : false));

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: APP_TITLE,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.setMenuBarVisibility(false);
  win.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'));
  setupUpdater(win);
}

app.whenReady().then(() => {
  createWindow();
  heartbeat = createHeartbeat({ dir: licenseStoreDir(), client: orders, lic, version: readBuildInfo().version,
    onChange: () => BrowserWindow.getAllWindows().forEach((w) => w.webContents.send('license:changed')) });
  heartbeat.start();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
