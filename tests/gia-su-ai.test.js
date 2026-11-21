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
  assert.ok(h.toLowerCase().includes('bộ dữ liệu mẫu cho các case'));
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
  assert.ok(w.TUDUY.k811.bai4.html.includes('<b>12</b>'));
  assert.ok(w.TUDUY.k1218.bai4.html.includes('5050'));
  assert.ok(w.TUDUY.k811.bai6.html.includes('<b>9</b>'));
  assert.ok(w.TUDUY.k1218.bai5.html.includes('5.83'));
});
test('Tư duy & lập trình: nối vào app, 2 bài đầu miễn phí', () => {
  const idx = fs.readFileSync(path.join(__dirname, '../renderer/index.html'), 'utf8');
  for (const x of ['tu-duy-content.js', 'tu-duy.js', 'id="tuduy-body"', 'id="open-tuduy"']) assert.ok(idx.includes(x), x);
  const app = fs.readFileSync(path.join(__dirname, '../renderer/app.js'), 'utf8');
  assert.ok(app.includes("'tuduy'") && app.includes('showTuDuy'));
  assert.ok(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy.js'), 'utf8').includes("k811: ['tongquan', 'caidat', 'bai1'], k1218: ['tongquan', 'caidat', 'c1b2']"));
});

test('Tư duy & lập trình: có trong catalog bán hàng, keygen và trang phụ huynh', () => {
  const cat = require('../renderer/catalog.js');
  // Hai khóa bán riêng, mỗi khóa 1.490.000 đ; mã bản cũ vẫn tồn tại để khóa đã bán còn dùng được nhưng không còn nằm trong danh sách bán.
  assert.strictEqual(cat.byId['tu-duy-lap-trinh-scratch'].price, 1490000);
  assert.strictEqual(cat.byId['tu-duy-lap-trinh-python'].price, 1490000);
  assert.ok(cat.byId['tu-duy-lap-trinh'].legacy && !cat.ALL.some((x) => x.id === 'tu-duy-lap-trinh'));
  const kg = fs.readFileSync(path.join(__dirname, '../keygen/index.html'), 'utf8');
  assert.ok(kg.includes('value="tu-duy-lap-trinh-scratch"') && kg.includes('value="tu-duy-lap-trinh-python"'));
  const pc = fs.readFileSync(path.join(__dirname, '../parent/courses.js'), 'utf8');
  assert.ok(pc.includes("'tu-duy-lap-trinh-scratch'") && pc.includes("'tu-duy-lap-trinh-python'"));
});

test('Tư duy & lập trình: bài Cài đặt có hình minh họa và hướng dẫn đúng công cụ', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy-content.js'), 'utf8'), { window: w });
  const sc = w.TUDUY.k811.caidat.html, py = w.TUDUY.k1218.caidat.html;
  assert.ok((sc.match(/<svg/g) || []).length >= 3 && sc.includes('scratch.mit.edu') && sc.includes('.sb3'));
  assert.ok((py.match(/<svg/g) || []).length >= 4 && py.includes('python.org') && py.includes('Add python.exe to PATH') && py.includes('IDLE') && py.includes('F5'));
});

test('Tư duy & lập trình: mỗi bài học có đủ 7 mục kiến thức và 5 bài thực hành tăng dần có lời giải', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy-content.js'), 'utf8'), { window: w });
  const heads = ['Ý nghĩa của bài học', 'Dùng bài học này như thế nào', 'Tư duy bài học mang đến', 'Hình minh họa từng bước', 'Lỗi sai hay gặp', 'Ví dụ minh họa'];
  for (const t of ['k811', 'k1218']) {
    for (const k of ['bai1', 'bai2', 'bai3', 'bai4', 'bai5', 'bai6', 'bai7', 'bai8']) {
      const h = w.TUDUY[t][k].html;
      for (const x of heads) assert.ok(h.includes(x), t + k + ' thiếu ' + x);
      assert.ok(h.includes(t === 'k811' ? 'Ứng dụng vào Scratch' : 'Ứng dụng vào Python'), t + k);
      assert.strictEqual((h.match(/class="tcard tprac"/g) || []).length, 5, t + k);
      assert.strictEqual((h.match(/<details class="tans">/g) || []).length, 5, t + k);
      for (const lv of ['Mức 1', 'Mức 2', 'Mức 3', 'Mức 4', 'Mức 5']) assert.ok(h.includes(lv), t + k + lv);
      assert.ok((h.match(/class="tstep"/g) || []).length >= 3, t + k + ' cần ít nhất 3 bước minh họa');
      assert.ok((h.match(/class="terr"/g) || []).length >= 3, t + k);
    }
  }
});

test('Python 12–18: mục lục 8 chương, Bài 0 và bài tóm tắt cuối mỗi chương; bài mới có giải nghĩa câu lệnh và đủ hình', () => {
  const w = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/tu-duy-content.js'), 'utf8'), { window: w });
  const toc = w.TUDUY_TOC.k1218;
  assert.strictEqual(toc.filter((g) => /^Chương \d/.test(g.t)).length, 8);
  assert.strictEqual(toc[0].items[0].key, 'tongquan');
  for (const g of toc.filter((x) => /^Chương \d/.test(x.t))) assert.ok(/^c\d+t$/.test(g.items[g.items.length - 1].key), g.t + ' phải kết thúc bằng bài tóm tắt');
  const lessons = toc.flatMap((g) => g.items).filter((r) => !/^c\d+t$/.test(r.key) && r.key !== 'tongquan' && r.key !== 'bai6');
  assert.ok(lessons.length >= 26, 'đủ 26 bài học: ' + lessons.length);
  for (const r of toc.flatMap((g) => g.items)) assert.strictEqual(r.ready, !!w.TUDUY.k1218[r.key], r.key);
  // chương 1 đã viết đủ
  for (const k of ['tongquan', 'caidat', 'c1b2', 'c1b3', 'c1t']) assert.ok(w.TUDUY.k1218[k], k);
  for (const k of ['c1b2', 'c1b3']) {
    const h = w.TUDUY.k1218[k].html;
    assert.ok(h.includes('Giải nghĩa từng phần của câu lệnh') && h.includes('Nếu thiếu hoặc viết sai thì sao'), k);
    assert.strictEqual((h.match(/class="tcard tprac"/g) || []).length, 5, k);
    assert.ok((h.match(/<svg/g) || []).length + (h.match(/class="tstep"/g) || []).length >= 10, k + ' cần 10 hình trở lên');
    assert.ok((h.match(/class="terr"/g) || []).length >= 3, k);
  }
  const intro = w.TUDUY.k1218.tongquan.html;
  assert.ok(intro.includes('Vì sao chọn Python') && intro.includes('Lộ trình 8 chương'));
  const t1 = w.TUDUY.k1218.c1t.html;
  assert.ok(t1.includes('Sơ đồ tóm tắt chương') && t1.includes('Dự án') && t1.includes('Tự kiểm tra') && (t1.match(/<svg/g) || []).length >= 4);
  // kết quả lỗi là kết quả chạy thật của Python
  assert.ok(w.TUDUY.k1218.c1b2.html.includes('NameError'));
  assert.ok(w.TUDUY.k1218.c1b3.html.includes('ZeroDivisionError'));
});
test('Tư duy & lập trình: quyền mở theo từng khóa (Scratch, Python) và khóa bản cũ mở cả hai', () => {
  const src = fs.readFileSync(path.join(__dirname, '../renderer/tu-duy.js'), 'utf8');
  assert.ok(src.includes("lic.courses.includes(COURSE[t]) || lic.courses.includes(LEGACY_ID)"));
  assert.ok(src.includes("'tu-duy-lap-trinh-scratch'") && src.includes("'tu-duy-lap-trinh-python'"));
});
