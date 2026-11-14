// Cầu nối an toàn giữa giao diện và tiến trình chính.
// Giao diện chỉ gọi được các hàm được liệt kê ở đây.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('vungBai', {
  version: '0.1.0-dev',
  loadManifest: (subject) => ipcRenderer.invoke('manifest:load', subject),
  loadLesson: (relPath) => ipcRenderer.invoke('lesson:load', relPath),
  appInfo: () => ipcRenderer.invoke('app:info'),
  productInfo: () => ipcRenderer.invoke('product:info'),
  loadLicense: () => ipcRenderer.invoke('license:load'),
  activateLicense: (key) => ipcRenderer.invoke('license:activate', key),
  createOrder: (order) => ipcRenderer.invoke('order:create', order),
  pinReset: (o) => ipcRenderer.invoke('pin:reset', o),
  orderStatus: (code) => ipcRenderer.invoke('order:status', code),
  updateStatus: () => ipcRenderer.invoke('update:status'),
  checkUpdate: () => ipcRenderer.invoke('update:check'),
  downloadUpdate: () => ipcRenderer.invoke('update:download'),
  installUpdate: () => ipcRenderer.invoke('update:install'),
  onUpdate: (cb) => ipcRenderer.on('update:status', (_e, st) => cb(st)),
  removeLicense: () => ipcRenderer.invoke('license:remove'),
});
