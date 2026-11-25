// Kiểm thử khối "Chọn trường" của Ôn thi THPT: điểm ưu tiên, khối khả dụng, chia nhóm, tính toàn vẹn dữ liệu 3 miền.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const L = require('../renderer/thpt-school-logic.js');
const { build } = require('../tools/build-thpt-school.js');

const root = path.join(__dirname, '..');
const REG = { bac: require('../renderer/thpt-school-bac.js'), trung: require('../renderer/thpt-school-trung.js'), nam: require('../renderer/thpt-school-nam.js') };

test('điểm ưu tiên: dưới 22,5 cộng đủ, từ 22,5 giảm dần theo công thức, liên tục tại 22,5', () => {
  assert.equal(L.priorityBonus(21, 'KV1', 'UT1'), 2.75);
  assert.equal(L.priorityBonus(20, 'KV2', 'UT2'), 1.25);
  assert.equal(L.priorityBonus(20, 'KV3', 'none'), 0);
  assert.equal(L.priorityBonus(22.5, 'KV1', 'none'), 0.75);   // (30-22,5)/7,5 = 1 -> đủ mức
  assert.equal(L.priorityBonus(26.25, 'KV1', 'none'), 0.38);  // (3,75/7,5) x 0,75 = 0,375 làm tròn lên 0,38
  assert.equal(L.priorityBonus(30, 'KV1', 'UT1'), 0);
});

test('khối khả dụng chỉ gồm khối đủ 3 môn trong 4 môn đã thi', () => {
  const a = L.availableKhoi(['PH', 'CH']);
  for (const k of ['A00', 'C01', 'C02']) assert.ok(a.includes(k), k);
  for (const k of ['A01', 'D01', 'B00']) assert.ok(!a.includes(k), k);
  const b = L.availableKhoi(['EN', 'PH']);
  for (const k of ['A01', 'D01', 'C01']) assert.ok(b.includes(k), k);
  assert.ok(L.availableKhoi(['LI', 'DI']).includes('C00'));
  assert.ok(L.availableKhoi(['GDKT', 'EN']).includes('X78'));
});

test('mọi khối gồm đúng 3 môn khác nhau, mã môn khớp bảng môn của khung', () => {
  const E = require('../renderer/thpt-exam-data.js').ELECTIVES.map((e) => e.id);
  for (const [k, ms] of Object.entries(L.KHOI)) {
    assert.equal(ms.length, 3, k);
    assert.equal(new Set(ms).size, 3, k);
    for (const m of ms) assert.ok(m === 'TO' || m === 'VA' || E.includes(m), `${k}: ${m}`);
  }
});

test('khoiScores: bỏ khối thiếu điểm, cộng ưu tiên đúng', () => {
  const ks = L.khoiScores({ TO: '9', VA: '8', PH: '9,5' }, ['PH', 'CH'], 'KV1', 'none');
  assert.deepEqual(Object.keys(ks), ['C01']);               // A00 thiếu điểm Hóa
  assert.equal(ks.C01.total, 26.5);
  assert.equal(ks.C01.bonus, 0.35);                          // (3,5/7,5) x 0,75 = 0,35
  assert.equal(ks.C01.score, 26.85);
});

test('parseScore nhận dấu phẩy, từ chối ngoài 0–10', () => {
  assert.equal(L.parseScore('8,25'), 8.25);
  assert.equal(L.parseScore('11'), null);
  assert.equal(L.parseScore('abc'), null);
  assert.equal(L.parseScore(''), null);
});

test('suggest: chia nhóm theo chênh lệch, lọc miền và từ khóa không dấu', () => {
  const data = {
    bac: { schools: [{ id: 's1', name: 'Trường 1', short: 'T1', rows: [['Ngành A', ['A00'], 24], ['Ngành B', ['A00'], 26.2], ['Ngành C', ['A00'], 28], ['Ngành D', ['D01'], 20]] }] },
    nam: { schools: [{ id: 's2', name: 'Trường 2', short: 'T2', rows: [['Ngành A', ['A00', 'A01'], 25.5]] }] },
  };
  const ks = { A00: { total: 25, bonus: 0, score: 25 } };
  const g = L.suggest(data, ks, {});
  assert.deepEqual(g['an-toan'].map((x) => x.name), ['Ngành A']);            // 25 - 24 = +1
  assert.deepEqual(g['can-nhac'].map((x) => x.name), ['Ngành A']);           // 25 - 25,5 = -0,5 (miền Nam)
  assert.deepEqual(g['thu-suc'].map((x) => x.name), ['Ngành B']);            // 25 - 26,2 = -1,2
  assert.equal([...g['an-toan'], ...g['can-nhac'], ...g['thu-suc']].some((x) => x.name === 'Ngành C'), false); // thấp hơn 3 điểm: không gợi ý
  assert.equal(g['an-toan'].concat(g['can-nhac'], g['thu-suc']).some((x) => x.name === 'Ngành D'), false);       // khối D01 em không có
  assert.equal(L.suggest(data, ks, { regions: ['nam'] })['can-nhac'].length, 1);
  assert.equal(L.suggest(data, ks, { regions: ['nam'] })['an-toan'].length, 0);
  assert.equal(L.suggest(data, ks, { query: 'nganh b' })['thu-suc'].length, 1);
});

test('dữ liệu 3 miền: đủ trường, mã không trùng, điểm trong 10–30, khối đều hỗ trợ', () => {
  const ids = new Set();
  for (const [rg, d] of Object.entries(REG)) {
    assert.equal(d.region, rg);
    assert.match(d.updated, /^\d{4}-\d{2}-\d{2}$/);
    assert.ok(d.schools.length >= 1, `${rg} chưa có trường nào`);
    for (const s of d.schools) {
      assert.ok(!ids.has(s.id), `trùng mã ${s.id}`); ids.add(s.id);
      assert.ok(s.source && s.name && s.year === 2026, s.id);
      assert.ok(s.rows.length >= 40, `${s.id} quá ít dòng`);
      for (const [name, khoi, cut] of s.rows) {
        assert.ok(name && khoi.length >= 1 && cut >= 10 && cut <= 30, `${s.id}: ${name}`);
        for (const k of khoi) assert.ok(L.KHOI[k], `${s.id}: khối ${k}`);
      }
    }
  }
});

test('đối chiếu khoảng điểm với số liệu trường/báo đã công bố', () => {
  const range = (rg, id) => { const s = REG[rg].schools.find((x) => x.id === id); const v = s.rows.map((r) => r[2]); return [Math.min(...v), Math.max(...v)]; };
  assert.deepEqual(range('bac', 'bka'), [20.06, 29.54]);   // ts.hust.edu.vn: từ 20,06 đến 29,54
  assert.deepEqual(range('bac', 'kha'), [23.48, 28.84]);   // cao nhất Kiểm toán 28,84
  assert.equal(range('trung', 'tdv')[1], 26.5);            // Sư phạm Toán học (tài năng) cao nhất 26,5
  assert.deepEqual(range('trung', 'ddk'), [18.25, 27.1]);
  assert.deepEqual(range('nam', 'tct'), [15, 28.12]);
});

test('tệp dữ liệu sinh ra khớp nguồn tools/thpt-data (chạy node tools/build-thpt-school.js nếu lệch)', () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'thptsch-'));
  build(out);
  for (const rg of ['bac', 'trung', 'nam']) {
    assert.equal(fs.readFileSync(path.join(out, `thpt-school-${rg}.js`), 'utf8'), fs.readFileSync(path.join(root, 'renderer', `thpt-school-${rg}.js`), 'utf8'), rg);
  }
});

test('giao diện: tab Chọn trường được nối và các tệp nạp đúng thứ tự', () => {
  const html = fs.readFileSync(path.join(root, 'renderer/index.html'), 'utf8');
  assert.match(html, /thpt-school-logic\.js[\s\S]*thpt-school-bac\.js[\s\S]*thpt-school-trung\.js[\s\S]*thpt-school-nam\.js[\s\S]*thpt-school\.js[\s\S]*thpt-exam\.js/);
  const ex = fs.readFileSync(path.join(root, 'renderer/thpt-exam.js'), 'utf8');
  assert.match(ex, /\['truong', 'Chọn trường'\]/);
  assert.match(ex, /window\.ThptSchool\.panel/);
});
