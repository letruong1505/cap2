const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { createStore } = require('../main/persist');

const tmpDir = () => fs.mkdtempSync(path.join(os.tmpdir(), 'persist-'));

test('ghi rồi đọc lại từ file ở lần mở sau', () => {
  const dir = tmpDir();
  const a = createStore(dir);
  assert.equal(a.set('vungbai.pin.v1', '{"pin":"1234"}'), true);
  assert.equal(a.set('vungbai.progress.v1', '{"wrong":[1,2]}'), true);
  const b = createStore(dir);
  assert.deepEqual(b.all(), { 'vungbai.pin.v1': '{"pin":"1234"}', 'vungbai.progress.v1': '{"wrong":[1,2]}' });
});

test('xóa khóa bằng null', () => {
  const dir = tmpDir();
  const a = createStore(dir);
  a.set('k', 'v');
  a.set('k', null);
  assert.deepEqual(createStore(dir).all(), {});
});

test('file chính hỏng thì đọc bản sao lưu', () => {
  const dir = tmpDir();
  const a = createStore(dir);
  a.set('a', '1');
  a.set('b', '2');
  fs.writeFileSync(a.file, '{hỏng', 'utf8');
  assert.deepEqual(createStore(dir).all(), { a: '1' });
});

test('từ chối khóa quá dài hoặc giá trị quá lớn', () => {
  const a = createStore(tmpDir());
  assert.equal(a.set('x'.repeat(201), '1'), false);
  assert.equal(a.set('k', 'y'.repeat(4 * 1024 * 1024 + 1)), false);
});
