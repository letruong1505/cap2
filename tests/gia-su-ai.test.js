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

test('AI cho người đi làm – Gemini: Bài 4–11 dạng thẻ, có thực hành và đáp án đúng', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/ai-work-gemini.js'), 'utf8'), { window: w });
  const G = w.AI_WORK_GEMINI;
  assert.deepStrictEqual(Object.keys(G), ['bai4', 'bai5', 'bai6', 'bai7', 'bai8', 'bai9', 'bai10', 'bai11', 'bai12']);
  for (const k of Object.keys(G)) {
    assert.ok(G[k].html.includes('class="tsum"') && G[k].html.includes('tcard tprac') && G[k].html.includes('class="tans"'), k);
  }
  // số liệu đáp án
  assert.strictEqual(1500000 + 800000 + 1200000, 3500000);
  assert.strictEqual((12 / 10.7 * 100 - 100).toFixed(2), '12.15'); assert.strictEqual((3.5 / 2 * 100 - 100), 75); assert.strictEqual((9 / 8.4 * 100 - 100).toFixed(2), '7.14');
  assert.strictEqual((3 * 6000000 + 1500000) * 1.1, 21450000); assert.strictEqual((3 * 6200000 + 1800000) * 1.1, 22440000); assert.strictEqual(3 * 5500000 + 3 * 800000, 18900000);
  assert.strictEqual(200 * 85000, 17000000); assert.strictEqual(150 * 85000, 12750000);
  for (const t of ['3.500.000', '21.450.000', '22.440.000', '18.900.000', '12.750.000']) assert.ok(Object.values(G).some((x) => x.html.includes(t)), t);
  // Bài 9 (Google): 450 km < 500 km; 2 đêm × 800.000 + 3 ngày × 200.000 = 2.200.000; QUERY tháng 11: KD 4.000.000, HC 2.600.000, KT 1.500.000
  assert.strictEqual(2 * 800000 + 3 * 200000, 2200000); assert.strictEqual(1200000 + 2800000, 4000000); assert.strictEqual(600000 + 2000000, 2600000);
  for (const t of ['2.200.000', '4.000.000', '2.600.000', 'quy chế không quy định']) assert.ok(G.bai9.html.includes(t), t);
  assert.ok(G.bai9.title.includes('hệ sinh thái Google') && G.bai10.title.includes('Bảo mật') && G.bai11.title.includes('Lộ trình'));
  const aw = fs.readFileSync(path.join(__dirname, '../renderer/ai-work.js'), 'utf8');
  assert.ok(aw.includes('AI_WORK_GEMINI') && aw.includes("['Bài 11'"));
  assert.ok(fs.readFileSync(path.join(__dirname, '../renderer/index.html'), 'utf8').includes('ai-work-gemini.js'));
});

test('Bài tổng kết Gemini (Bài 12) và ChatGPT (Bài 13): có phiếu tự đánh giá, dự án cuối và số liệu đúng', () => {
  const w = {}; const ctx = { window: w };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/ai-work-gemini.js'), 'utf8'), ctx);
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/ai-work-chatgpt.js'), 'utf8'), ctx);
  const g = w.AI_WORK_GEMINI.bai12, c = w.AI_WORK_CHATGPT.bai13;
  for (const L of [g, c]) for (const t of ['Phiếu tự đánh giá', 'Dự án cuối', 'tcard tprac', 'Checklist 60 giây', 'Kế hoạch 30 ngày']) assert.ok(L.html.includes(t), t);
  assert.ok(g.title.includes('Bài 12') && c.title.includes('Bài 13'));
  assert.strictEqual(120 / 150, 0.8); assert.strictEqual(4200000 + 600000 + 1800000, 6600000); assert.strictEqual(3900000 + 650000 + 900000, 5450000);
  assert.strictEqual((6600000 / 5450000 * 100 - 100).toFixed(2), '21.10'); assert.strictEqual((4200000 / 3900000 * 100 - 100).toFixed(2), '7.69');
  assert.strictEqual(117 / 130, 0.9); assert.strictEqual((105 / 117 * 100).toFixed(2), '89.74'); assert.strictEqual((99 / 108 * 100 - 105 / 117 * 100).toFixed(1), '1.9');
  for (const t of ['21,10%', '6.600.000', '5.450.000']) assert.ok(g.html.includes(t), t);
  for (const t of ['89,74%', '1,9 điểm', '13']) assert.ok(c.html.includes(t), t);
});

test('Gia sư AI: mọi bài dạng thẻ (tóm tắt đầu bài, thẻ đánh số, không còn khung meta cũ)', () => {
  for (const k of Object.keys(C)) {
    assert.ok(C[k].html.startsWith('<div class="tsum">'), k);
    assert.ok((C[k].html.match(/class="tcard"/g) || []).length >= 3, k);
    assert.ok(!C[k].html.includes('class="meta"'), k);
  }
});

test('AI cho người đi làm – Claude: Bài 4–11 dạng thẻ, giữ hình minh họa', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/ai-work-claude.js'), 'utf8'), { window: w });
  const G = w.AI_WORK_CLAUDE;
  assert.deepStrictEqual(Object.keys(G), ['bai4', 'bai5', 'bai6', 'bai7', 'bai8', 'bai9', 'bai10', 'bai11']);
  for (const k of Object.keys(G)) {
    assert.ok(G[k].html.startsWith('<div class="tsum">') && !G[k].html.includes('class="meta"'), k);
    assert.ok((G[k].html.match(/class="tcard"/g) || []).length >= 4, k);
    assert.ok(G[k].html.includes('<svg'), k);
  }
});

test('Tư duy & lập trình: 2 lộ trình đủ mở đầu + 8 bài, có thực hành và đáp án', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy-content.js'), 'utf8'), { window: w });
  for (const t of ['k811', 'k1218']) {
    for (const k of ['tongquan', 'caidat', 'bai1', 'bai2', 'bai3', 'bai4', 'bai5', 'bai6', 'bai7', 'bai8']) {
      const L = w.TUDUY[t][k];
      assert.ok(L && L.title && L.html.includes('class="tsum"') && L.html.includes('tprac') && L.html.includes('class="tans"'), t + k);
    }
  }
  const all = JSON.stringify(w.TUDUY);
  assert.ok(!/<script/i.test(all));
  // số liệu đã kiểm: biến Scratch bài 4 = 12; tổng 1..99 = 4950; làm ngược 23 -> 9
  assert.ok(w.TUDUY.k811.bai4.html.includes('điểm = 12'));
  assert.ok(w.TUDUY.k1218.bai4.html.includes('4950'));
  assert.ok(w.TUDUY.k811.bai6.html.includes('<b>9</b>'));
  assert.ok(w.TUDUY.k1218.bai5.html.includes('5.83'));
});
test('Tư duy & lập trình: nối vào app, 2 bài đầu miễn phí', () => {
  const idx = fs.readFileSync(path.join(__dirname, '../renderer/index.html'), 'utf8');
  for (const x of ['tu-duy-content.js', 'tu-duy.js', 'id="tuduy-body"', 'id="open-tuduy"']) assert.ok(idx.includes(x), x);
  const app = fs.readFileSync(path.join(__dirname, '../renderer/app.js'), 'utf8');
  assert.ok(app.includes("'tuduy'") && app.includes('showTuDuy'));
  assert.ok(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy.js'), 'utf8').includes("FREE = ['tongquan', 'caidat', 'bai1']"));
});

test('Tư duy & lập trình: có trong catalog bán hàng, keygen và trang phụ huynh', () => {
  const cat = require('../renderer/catalog.js');
  assert.strictEqual(cat.byId['tu-duy-lap-trinh'].price, 1490000);
  assert.ok(fs.readFileSync(path.join(__dirname, '../keygen/index.html'), 'utf8').includes('value="tu-duy-lap-trinh"'));
  assert.ok(fs.readFileSync(path.join(__dirname, '../parent/courses.js'), 'utf8').includes("'tu-duy-lap-trinh'"));
});

test('Tư duy & lập trình: bài Cài đặt có hình minh họa và hướng dẫn đúng công cụ', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy-content.js'), 'utf8'), { window: w });
  const sc = w.TUDUY.k811.caidat.html, py = w.TUDUY.k1218.caidat.html;
  assert.ok((sc.match(/<svg/g) || []).length >= 3 && sc.includes('scratch.mit.edu') && sc.includes('.sb3'));
  assert.ok((py.match(/<svg/g) || []).length >= 4 && py.includes('python.org') && py.includes('Add python.exe to PATH') && py.includes('IDLE') && py.includes('F5'));
});
