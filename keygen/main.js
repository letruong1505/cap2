// Công cụ cấp khoá của chủ sản phẩm (offline). Không đưa kèm bản bán cho khách.
const { app, BrowserWindow, ipcMain, dialog, clipboard } = require('electron');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const settingsFile = () => path.join(app.getPath('userData'), 'keygen-settings.json');
const readSettings = () => { try { return JSON.parse(fs.readFileSync(settingsFile(), 'utf8')); } catch { return {}; } };
const writeSettings = (s) => { fs.mkdirSync(path.dirname(settingsFile()), { recursive: true }); fs.writeFileSync(settingsFile(), JSON.stringify(s)); };

function loadPrivateKey() {
  const { keyFile } = readSettings();
  if (!keyFile || !fs.existsSync(keyFile)) return null;
  try { return crypto.createPrivateKey(fs.readFileSync(keyFile, 'utf8')); } catch { return null; }
}

ipcMain.handle('key:status', () => ({ ready: !!loadPrivateKey(), file: readSettings().keyFile || '' }));

ipcMain.handle('key:choose', async () => {
  const r = await dialog.showOpenDialog({ title: 'Chọn file khoá riêng (private.pem)', properties: ['openFile'], filters: [{ name: 'PEM', extensions: ['pem'] }] });
  if (r.canceled || !r.filePaths[0]) return { ready: !!loadPrivateKey() };
  try {
    const k = crypto.createPrivateKey(fs.readFileSync(r.filePaths[0], 'utf8'));
    if (k.asymmetricKeyType !== 'ed25519') throw new Error('not ed25519');
  } catch { return { ready: false, error: 'File không phải khoá riêng hợp lệ.' }; }
  writeSettings({ ...readSettings(), keyFile: r.filePaths[0] });
  return { ready: true, file: r.filePaths[0] };
});

ipcMain.handle('key:issue', (_e, f) => {
  const priv = loadPrivateKey();
  if (!priv) return { error: 'Chưa chọn khoá riêng.' };
  const owner = String(f.owner || '').trim();
  if (!owner) return { error: 'Nhập tên khách hàng.' };
  if (!/^\d{4}-\d{2}-\d{2}$/.test(f.expires || '')) return { error: 'Nhập ngày hết hạn.' };
  let grades;
  if (f.allGrades) grades = 'all';
  else {
    grades = (f.grades || []).map(Number).filter(Number.isInteger);
    if (!grades.length) return { error: 'Chọn ít nhất một lớp.' };
  }
  let machine = '*';
  if (!f.anyMachine) {
    machine = String(f.machine || '').trim().toUpperCase();
    if (!/^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$/.test(machine)) return { error: 'Mã máy phải có dạng XXXX-XXXX-XXXX.' };
  }
  const id = 'NL-' + crypto.randomBytes(3).toString('hex').toUpperCase();
  const payload = Buffer.from(JSON.stringify({ v: 1, id, owner, grades, machine, issued: new Date().toISOString().slice(0, 10), expires: f.expires }));
  const sig = crypto.sign(null, payload, priv);
  const key = 'NL1-' + payload.toString('base64url') + '.' + Buffer.from(sig).toString('base64url');
  return { key, id };
});

ipcMain.handle('clip:write', (_e, t) => { clipboard.writeText(String(t)); });

app.whenReady().then(() => {
  const win = new BrowserWindow({ width: 760, height: 720, title: 'Nam Linh - Cấp khoá bản quyền', webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false } });
  win.setMenuBarVisibility(false);
  win.loadFile(path.join(__dirname, 'index.html'));
});
app.on('window-all-closed', () => app.quit());
