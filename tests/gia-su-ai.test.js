'use strict';
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const win = {};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/gia-su-ai-content.js'), 'utf8'), { window: win });
const C = win.GIA_SU_AI;

test('Gia sư AI: đủ 8 bài + tổng quan + phụ lục, có tiêu đề và nội dung', () => {
  for (const k of ['tongquan', 'bai1', 'bai2', 'bai3', 'bai4', 'bai5', 'bai6', 'bai7', 'bai8', 'phuluc']) {
    assert.ok(C[k] && C[k].title && C[k].html.length > 1000, k);
  }
});
test('Gia sư AI: bài học tự học, không còn giọng giáo án lớp học', () => {
  const t = Object.values(C).map((v) => v.html.replace(/<[^>]+>/g, ' ')).join(' ');
  for (const bad of ['Giáo viên', 'giáo viên', 'Cả lớp', 'buổi', 'Chia nhóm', 'trung tâm', 'phiếu giấy']) assert.ok(!t.includes(bad), bad);
  assert.ok(!/<script/i.test(JSON.stringify(C)));
});
test('Gia sư AI: index.html nạp script và có màn hình giasu', () => {
  const idx = fs.readFileSync(path.join(__dirname, '../renderer/index.html'), 'utf8');
  for (const s of ['gia-su-ai-content.js', 'gia-su-ai.js', 'id="giasu-body"', 'id="open-giasu"']) assert.ok(idx.includes(s), s);
  const app = fs.readFileSync(path.join(__dirname, '../renderer/app.js'), 'utf8');
  assert.ok(app.includes("'giasu'") && app.includes('showGiaSu'));
});
