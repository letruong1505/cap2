const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const load = (rel, ctx) => vm.runInNewContext(fs.readFileSync(path.join(root, rel), 'utf8'), ctx);

test('dữ liệu định hướng của app Phụ huynh trùng với national-data.js của app học', () => {
  const ctx = { window: {} };
  load('renderer/national-data.js', ctx); load('parent/dhqg-data.js', ctx);
  const want = {};
  ctx.window.NATIONAL_DATA.groups.forEach((x) => { want[x.id] = { n: x.n, s: x.s, m: x.m, k: x.k, a: x.a, b: x.b }; });
  assert.deepEqual(JSON.parse(JSON.stringify(ctx.window.PARENT_DHQG)), JSON.parse(JSON.stringify(want)));
  for (const g of Object.values(ctx.window.PARENT_DHQG)) assert.ok(g.n && g.m.length && g.s.length && g.a.length && g.b.length);
});

test('build app Phụ huynh có dữ liệu định hướng và nút xem', () => {
  const { build } = require('../tools/build-parent-www.js');
  const out = fs.mkdtempSync(path.join(require('node:os').tmpdir(), 'pw-'));
  build({ out, version: '1.0.0', api: 'https://x.example/api' });
  assert.ok(fs.existsSync(path.join(out, 'dhqg-data.js')));
  const html = fs.readFileSync(path.join(out, 'index.html'), 'utf8');
  assert.match(html, /id="go-orient"/); assert.match(html, /dhqg-data\.js/);
});

test('app học gửi đúng khóa lưu của mục Định hướng (nl-dhcnqg và nl-dhcnqg-qz) lên máy chủ', () => {
  const sync = fs.readFileSync(path.join(root, 'renderer/progress-sync.js'), 'utf8');
  const nat = fs.readFileSync(path.join(root, 'renderer/national.js'), 'utf8');
  for (const k of ['nl-dhcnqg', 'nl-dhcnqg-qz']) { assert.ok(sync.includes("'" + k + "'")); assert.ok(nat.includes("'" + k + "'")); }
  assert.match(sync, /orientation: ids/);
  for (const f of ['main/orders.js', 'mobile/bridge/api.js']) assert.match(fs.readFileSync(path.join(root, f), 'utf8'), /orientation:/);
  assert.match(fs.readFileSync(path.join(root, 'renderer/index.html'), 'utf8'), /national-quiz\.js[\s\S]*national\.js/);
});

function loadNational() {
  const ctx = { window: {}, localStorage: { getItem: () => null, setItem() {}, removeItem() {} }, document: {}, console };
  ctx.window = ctx; // national.js gắn vào window
  load('renderer/national-data.js', ctx); load('renderer/national-quiz.js', ctx); load('renderer/national.js', ctx);
  return ctx;
}
test('trắc nghiệm chọn hướng: ngân hàng 20 câu (10 cặp), dữ liệu hợp lệ, chấm điểm ra nhóm hợp lý', () => {
  const ctx = loadNational();
  const Q = ctx.NATIONAL_QUIZ; const ids = ctx.NATIONAL_DATA.groups.map((g) => g.id);
  assert.equal(Q.pairs.length, 10);
  const texts = new Set();
  for (const p of Q.pairs) {
    assert.equal(p.length, 2);
    for (const q of p) {
      assert.equal(q.options.length, 4); assert.ok(!texts.has(q.q), 'trùng câu'); texts.add(q.q);
      for (const o of q.options) for (const k of Object.keys(o.w)) assert.ok(ids.includes(k), 'nhóm lạ ' + k);
    }
    // Hai câu trong một cặp cùng chạm tới cùng tập nhóm để lần nào cũng công bằng giữa các nhóm.
    const set = (q) => [...new Set(q.options.flatMap((o) => Object.keys(o.w)))].sort().join();
    assert.equal(set(p[0]), set(p[1]));
  }
  const score = ctx.National.scoreQuiz;
  for (const pick of [0, 1]) {
    const deck = Q.pairs.map((p) => p[pick]);
    const r = score(deck, deck.map(() => 0), ['Toán', 'Tin học', 'Tiếng Anh']);
    assert.equal(r[0].id, 'so'); assert.equal(r[0].p, 100); assert.equal(r.length, 5);
    const bio = score(deck, deck.map((q) => Math.max(0, q.options.findIndex((o) => o.w.sinh))), ['Sinh học', 'Hóa học']);
    assert.equal(bio[0].id, 'sinh');
  }
});
