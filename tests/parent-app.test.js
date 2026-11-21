const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { build, FROM_RENDERER } = require('../tools/build-parent-www.js');

test('app Phụ huynh: gói www nhẹ, đủ tệp và không chứa bài học', () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'ph-'));
  build({ out, version: '1.0.9', api: 'https://example.workers.dev/api' });
  const html = fs.readFileSync(path.join(out, 'index.html'), 'utf8');
  assert.match(html, /connect-src 'self' https:\/\/example\.workers\.dev/);
  assert.ok(!html.includes('__API_ORIGIN__'));
  for (const m of html.matchAll(/<script src="([^"]+)"/g)) assert.ok(fs.existsSync(path.join(out, m[1])), 'thiếu ' + m[1]);
  for (const f of FROM_RENDERER) assert.ok(fs.existsSync(path.join(out, f)), f);
  assert.ok(!fs.existsSync(path.join(out, 'content')));
  const size = fs.readdirSync(out, { recursive: true }).reduce((a, f) => { const p = path.join(out, f); return a + (fs.statSync(p).isFile() ? fs.statSync(p).size : 0); }, 0);
  assert.ok(size < 3 * 1024 * 1024, 'gói quá nặng: ' + size);
  assert.match(fs.readFileSync(path.join(out, 'mobile-config.js'), 'utf8'), /1\.0\.9/);
});
