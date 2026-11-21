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

test('AI cho người đi làm – ChatGPT: Bài 4–9 có thẻ thực hành với dữ liệu mẫu và đáp án', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/ai-work-chatgpt.js'), 'utf8'), { window: w });
  for (const k of ['bai4', 'bai5', 'bai6', 'bai7', 'bai8', 'bai9']) {
    const h = w.AI_WORK_CHATGPT[k].html;
    assert.ok(h.includes('class="pdata"') && h.includes('class="tans"') && h.includes('class="prompt"'), k);
  }
  // số liệu Bài 7: 1.200.000 + 900.000 + 1.100.000 = 3.200.000
  assert.ok(w.AI_WORK_CHATGPT.bai7.html.includes('3.200.000'));
  const js = fs.readFileSync(path.join(__dirname, '../renderer/ai-work.js'), 'utf8');
  assert.ok(js.includes('addCopyButtons(box)'));
});

test('ChatGPT Bài 11: có bộ dữ liệu mẫu cho Case 1–4 với số liệu đúng', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/ai-work-chatgpt.js'), 'utf8'), { window: w });
  const h = w.AI_WORK_CHATGPT.bai11.html;
  assert.ok(h.includes('bộ dữ liệu mẫu cho các case'));
  assert.strictEqual((h.match(/class="pdata"/g) || []).length, 4);
  // 84/90, 99/108, 10 chiếc: A, B, C
  assert.strictEqual((84 / 90 * 100).toFixed(2), '93.33'); assert.strictEqual((99 / 108 * 100).toFixed(2), '91.67');
  assert.strictEqual(2000000 * 10 + 300000, 20300000); assert.strictEqual(1950000 * 10 + 800000, 20300000); assert.strictEqual(2050000 * 10, 20500000);
  const names = h.match(/<pre class="pdata">Mau_don[^<]*<\/pre>/)[0].replace(/<[^>]+>/g, '').split('\n');
  assert.strictEqual(names.length, 24);
});
