const test = require('node:test');
const assert = require('node:assert/strict');
const { firstSection } = require('../tools/release-notes');
test('lấy mục đầu tiên của CHANGELOG', () => {
  assert.equal(firstSection('# x\n## Bản 2\n- a\n- b\n## Bản 1\n- c'), '- a\n- b');
  assert.equal(firstSection(''), '');
});
