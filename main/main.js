const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');
const { loadManifest, loadLesson } = require('./content-loader');

const PRODUCT_DIR = 'toan7';

// build-info.json do workflow tạo khi build (số phiên bản và mã commit). Chạy dev thì không có file này.
function readBuildInfo() {
  try {
    return JSON.parse(fs.readFileSync(path.join(__dirname, 'build-info.json'), 'utf8'));
  } catch {
    return { version: 'dev', commit: 'local' };
  }
}

ipcMain.handle('manifest:load', () => loadManifest(PRODUCT_DIR));
ipcMain.handle('lesson:load', (_event, relPath) => loadLesson(relPath));
ipcMain.handle('app:info', () => readBuildInfo());

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: 'Vững Bài',
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
