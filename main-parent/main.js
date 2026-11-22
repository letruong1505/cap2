// App Phụ huynh cho Windows: bọc lại giao diện app Phụ huynh (parent-www) trong Electron.
// Mọi cuộc gọi mạng đi qua tiến trình chính, chỉ tới máy chủ đơn hàng của Nam Linh.
const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage, shell } = require('electron');
const fs = require('fs');
const path = require('path');
const { createUpdater } = require('../main/updater');

const APP_TITLE = 'Nam Linh Educenter cho phụ huynh';
app.setAppUserModelId('vn.namlinh.phuhuynh.win');

const readJson = (p, d) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return d; } };
const baseUrl = () => String(readJson(path.join(__dirname, 'orders-api.json'), {}).baseUrl || '').replace(/\/+$/, '');

if (!app.requestSingleInstanceLock()) { app.quit(); }

ipcMain.handle('net:fetch', async (_e, url, init) => {
  const base = baseUrl();
  if (!base || typeof url !== 'string' || !url.startsWith(base + '/')) return { ok: false, status: 0, body: '' };
  const i = init && typeof init === 'object' ? init : {};
  try {
    const r = await fetch(url, { method: i.method === 'POST' ? 'POST' : 'GET', headers: { 'content-type': 'application/json' }, body: typeof i.body === 'string' ? i.body : undefined, signal: AbortSignal.timeout(10000) });
    return { ok: r.ok, status: r.status, body: await r.text() };
  } catch { return { ok: false, status: 0, body: '' }; }
});

let win = null; let updater = null; let tray = null; let quitting = false;

function setupUpdater() {
  const cfg = readJson(path.join(__dirname, 'update-config.json'), {});
  let autoUpdater = null;
  if (app.isPackaged) { try { ({ autoUpdater } = require('electron-updater')); } catch { autoUpdater = null; } }
  updater = createUpdater({ autoUpdater, enabled: !!autoUpdater, url: cfg.url, send: (st) => { if (win && !win.isDestroyed()) win.webContents.send('update:status', st); } });
  if (updater.active) { setTimeout(() => updater.check(), 8000); setInterval(() => updater.check(), 2 * 60 * 60 * 1000); }
}
ipcMain.handle('update:status', () => (updater ? updater.status() : { state: 'off' }));
ipcMain.handle('update:check', () => (updater ? updater.check() : { state: 'off' }));
ipcMain.handle('update:download', () => (updater ? updater.download() : { state: 'off' }));
ipcMain.handle('update:install', () => { quitting = true; return updater ? updater.install() : false; });
ipcMain.handle('app:version', () => app.getVersion());

function showWindow() { if (!win) return; if (win.isMinimized()) win.restore(); win.show(); win.focus(); }

function createWindow() {
  win = new BrowserWindow({
    width: 1100, height: 780, minWidth: 700, minHeight: 560, title: APP_TITLE,
    icon: path.join(__dirname, '..', 'build', 'icon.png'),
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false },
  });
  win.setMenuBarVisibility(false);
  win.loadFile(path.join(__dirname, '..', 'parent-www', 'index.html'));
  // Liên kết ra ngoài (Zalo, trang web) mở bằng trình duyệt, không mở trong cửa sổ app.
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^https:\/\//i.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('file:')) { e.preventDefault(); if (/^https:\/\//i.test(url)) shell.openExternal(url); } });
  // Đóng cửa sổ thì thu nhỏ xuống khay hệ thống để vẫn nhắc giờ học; thoát hẳn từ menu của biểu tượng ở khay.
  win.on('close', (e) => {
    if (quitting) return;
    e.preventDefault(); win.hide();
    if (tray && !createWindow.told) { createWindow.told = true; tray.displayBalloon({ title: APP_TITLE, content: 'Phần mềm vẫn chạy ngầm để nhắc giờ học. Bấm chuột phải vào biểu tượng ở khay để thoát.' }); }
  });
  setupUpdater();
}

app.whenReady().then(() => {
  createWindow();
  try {
    tray = new Tray(nativeImage.createFromPath(path.join(__dirname, '..', 'build', 'icon.png')).resize({ width: 16, height: 16 }));
    tray.setToolTip(APP_TITLE);
    tray.setContextMenu(Menu.buildFromTemplate([{ label: 'Mở ứng dụng', click: showWindow }, { label: 'Thoát', click: () => { quitting = true; app.quit(); } }]));
    tray.on('click', showWindow);
  } catch { tray = null; }
  app.on('second-instance', showWindow);
  app.on('activate', showWindow);
});
app.on('before-quit', () => { quitting = true; });
app.on('window-all-closed', () => { if (quitting) app.quit(); });
