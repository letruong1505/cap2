const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');
const { loadManifest, loadLesson } = require('./content-loader');
const lic = require('./license');

const APP_TITLE = 'Giáo trình THCS';


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

ipcMain.handle('license:load', () => licenseNow());
ipcMain.handle('license:activate', (_event, key) => lic.activate(licenseStoreDir(), key));
ipcMain.handle('license:remove', () => { lic.deactivate(licenseStoreDir()); return licenseNow(); });

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
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
