// Cầu nối an toàn giữa giao diện và tiến trình chính.
// Giao diện chỉ gọi được các hàm được liệt kê ở đây.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('vungBai', {
  version: '0.1.0-dev',
  loadManifest: () => ipcRenderer.invoke('manifest:load'),
  loadLesson: (relPath) => ipcRenderer.invoke('lesson:load', relPath),
  appInfo: () => ipcRenderer.invoke('app:info'),
});
