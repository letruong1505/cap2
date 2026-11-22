// Cầu nối an toàn: giao diện chỉ gọi được các hàm dưới đây.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('NLDesktop', {
  fetch: (url, init) => ipcRenderer.invoke('net:fetch', String(url), { method: init && init.method, body: init && init.body }),
  version: () => ipcRenderer.invoke('app:version'),
  updateStatus: () => ipcRenderer.invoke('update:status'),
  checkUpdate: () => ipcRenderer.invoke('update:check'),
  downloadUpdate: () => ipcRenderer.invoke('update:download'),
  installUpdate: () => ipcRenderer.invoke('update:install'),
  onUpdate: (cb) => ipcRenderer.on('update:status', (_e, st) => cb(st)),
});
