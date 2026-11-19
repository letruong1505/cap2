const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('kg', {
  status: () => ipcRenderer.invoke('key:status'),
  choose: () => ipcRenderer.invoke('key:choose'),
  issue: (f) => ipcRenderer.invoke('key:issue', f),
  copy: (t) => ipcRenderer.invoke('clip:write', t),
});
