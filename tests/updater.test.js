const test = require('node:test');
const assert = require('node:assert/strict');
const { EventEmitter } = require('node:events');
const { createUpdater } = require('../main/updater');

function fake() {
  const au = new EventEmitter();
  au.calls = [];
  au.setFeedURL = (o) => au.calls.push(['feed', o]);
  au.checkForUpdates = async () => { au.calls.push(['check']); au.emit('checking-for-update'); au.emit('update-available', { version: '1.0.60' }); };
  au.downloadUpdate = async () => { au.calls.push(['download']); au.emit('download-progress', { percent: 41.6 }); au.emit('update-downloaded', { version: '1.0.60' }); };
  au.quitAndInstall = (...a) => au.calls.push(['install', a]);
  return au;
}

test('tắt khi không có địa chỉ hoặc không phải https', async () => {
  for (const url of ['', '  ', 'http://x.com', undefined]) {
    const au = fake(); const u = createUpdater({ autoUpdater: au, send() {}, url });
    assert.equal(u.active, false);
    assert.equal(u.status().state, 'off');
    await u.check();
    assert.deepEqual(au.calls, []);
  }
});

test('tắt khi bị vô hiệu (chạy dev hoặc sản phẩm khác)', () => {
  const u = createUpdater({ autoUpdater: fake(), send() {}, url: 'https://u.example.com', enabled: false });
  assert.equal(u.active, false);
});

test('luồng: kiểm tra → có bản mới → hỏi → tải → cài, không tự tải', async () => {
  const au = fake(); const sent = [];
  const u = createUpdater({ autoUpdater: au, send: (s) => sent.push(s.state), url: 'https://u.example.com/educenter/' });
  assert.deepEqual(au.calls[0], ['feed', { provider: 'generic', url: 'https://u.example.com/educenter' }]);
  assert.equal(au.autoDownload, false);
  await u.check();
  assert.equal(u.status().state, 'available');
  assert.ok(!au.calls.some((c) => c[0] === 'download'));
  assert.equal(u.install(), false);
  await u.download();
  assert.equal(u.status().state, 'ready');
  assert.equal(u.status().version, '1.0.60');
  assert.equal(u.install(), true);
  assert.equal(au.calls.at(-1)[0], 'install');
  assert.ok(sent.includes('downloading'));
});

test('lỗi mạng chỉ ghi vào trạng thái', async () => {
  const au = fake(); au.checkForUpdates = async () => { throw new Error('ENOTFOUND'); };
  const u = createUpdater({ autoUpdater: au, send() {}, url: 'https://u.example.com' });
  await u.check();
  assert.equal(u.status().state, 'error');
  assert.match(u.status().error, /ENOTFOUND/);
});
