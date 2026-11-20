const test = require('node:test');
const assert = require('node:assert/strict');
const S = require('../renderer/solid3d.js');

const cube = (view) => ({
  v: 1, view,
  pts: { A: [0, 0, 0], B: [2, 0, 0], C: [2, 2, 0], D: [0, 2, 0], E: [0, 0, 2], F: [2, 0, 2], G: [2, 2, 2], H: [0, 2, 2] },
  solids: [{ k: 'poly', faces: [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['A', 'B', 'F', 'E'], ['B', 'C', 'G', 'F'], ['C', 'D', 'H', 'G'], ['D', 'A', 'E', 'H']] }],
  items: [],
});
const dashed = (svg) => (svg.match(/stroke-dasharray/g) || []).length;

test('khối lập phương: nhìn từ trên xuống thì 3 cạnh khuất, từ dưới lên cũng 3 cạnh khuất', () => {
  for (const view of [{ az: 25, el: 25 }, { az: 140, el: 35 }, { az: -60, el: 20 }, { az: 25, el: -25 }, { az: 200, el: -40 }]) {
    const m = cube(view);
    const svg = S.draw(S.prepare(m), view);
    assert.equal(dashed(svg), 3, 'góc ' + JSON.stringify(view));
  }
});

test('đường chéo không gian nằm trong khối luôn nét đứt; đường chéo mặt trước nét liền', () => {
  const view = { az: 25, el: 25 };
  const m = cube(view);
  m.items = [{ t: 'seg', a: 'A', b: 'G', c: '#d64541' }];
  const inside = S.draw(S.prepare(m), view);
  const redDash = (inside.match(/stroke="#d64541"[^>]*stroke-dasharray/g) || []).length;
  assert.ok(redDash >= 1);
  // Mặt trước (y = 0) có pháp tuyến hướng về người xem khi az nhỏ: chéo A-F phải liền.
  m.items = [{ t: 'seg', a: 'A', b: 'F', c: '#d64541' }];
  const face = S.draw(S.prepare(m), view);
  assert.equal((face.match(/stroke="#d64541"[^>]*stroke-dasharray/g) || []).length, 0);
});

test('hiddenBy: điểm ở tâm khối bị che, điểm trên mặt hướng về người xem thì không', () => {
  const prep = S.prepare(cube({ az: 0, el: 0 }));
  const B = S.basis(0, 0); // camera ở phía y âm
  assert.equal(S.hiddenBy(prep.solids[0], [1, 1, 1], B.v, prep.rad), true);
  assert.equal(S.hiddenBy(prep.solids[0], [1, 0, 1], B.v, prep.rad), false); // mặt y = 0 hướng về camera
  assert.equal(S.hiddenBy(prep.solids[0], [1, 2, 1], B.v, prep.rad), true); // mặt sau
  assert.equal(S.hiddenBy(prep.solids[0], [1, -1, 1], B.v, prep.rad), false); // ngoài khối, phía trước
});

test('mặt cầu, trụ, nón: nửa sau bị che, nửa trước thì không', () => {
  const B = S.basis(0, 0);
  const sph = S.prepare({ pts: { O: [0, 0, 0] }, solids: [{ k: 'sphere', c: 'O', r: 2 }] });
  assert.equal(S.hiddenBy(sph.solids[0], [0, 2 * Math.cos(0.5), 2 * Math.sin(0.5)], B.v, sph.rad), true);
  assert.equal(S.hiddenBy(sph.solids[0], [0, -2 * Math.cos(0.5), 2 * Math.sin(0.5)], B.v, sph.rad), false);
  const cyl = S.prepare({ pts: { O: [0, 0, 0] }, solids: [{ k: 'axi', o: 'O', e: [0, 0, 1], prof: [[0, 1], [3, 1]] }] });
  assert.equal(S.hiddenBy(cyl.solids[0], [0, 1, 1.5], B.v, cyl.rad), true);
  assert.equal(S.hiddenBy(cyl.solids[0], [0, -1, 1.5], B.v, cyl.rad), false);
  assert.equal(S.hiddenBy(cyl.solids[0], [0, 0, 1.5], B.v, cyl.rad), true); // trục nằm trong khối
  const cone = S.prepare({ pts: { O: [0, 0, 0] }, solids: [{ k: 'axi', o: 'O', e: [0, 0, 1], prof: [[0, 2], [3, 0]] }] });
  assert.equal(S.hiddenBy(cone.solids[0], [0, 0, 1], B.v, cone.rad), true);
  assert.equal(S.hiddenBy(cone.solids[0], [0, -2, 0], B.v, cone.rad), false);
});

test('đáy trụ: từ trên nhìn xuống thì nửa sau đáy dưới là nét đứt, đáy trên liền', () => {
  const m = { view: { az: 20, el: 25 }, pts: { O: [0, 0, 0] }, solids: [{ k: 'axi', o: 'O', e: [0, 0, 1], prof: [[0, 1.5], [3, 1.5]] }], items: [] };
  const svg = S.draw(S.prepare(m), m.view);
  assert.ok(dashed(svg) >= 1 && dashed(svg) <= 3);
});

test('toSVG kèm mô hình và extractModel đọc lại đúng', () => {
  const m = cube({ az: 30, el: 20 });
  m.items = [{ t: 'lbl', p: 'A', s: 'A' }];
  const svg = S.toSVG(m);
  assert.match(svg, /^<svg /);
  const back = S.extractModel(svg);
  assert.deepEqual(back, JSON.parse(JSON.stringify(m)));
  assert.equal(S.extractModel('<svg></svg>'), null);
});

test('thiếu điểm trong mô hình thì báo lỗi rõ ràng', () => {
  assert.throws(() => S.prepare({ pts: {}, solids: [{ k: 'poly', faces: [['A', 'B', 'C']] }] }), /Thiếu điểm A/);
});

test('khối ghost (mặt cầu nội tiếp) không che nét hình lập phương, nhưng che nét được chỉ định', () => {
  const m = {
    view: { az: 24, el: 22 },
    pts: { A: [0, 0, 0], B: [2, 0, 0], C: [2, 2, 0], D: [0, 2, 0], E: [0, 0, 2], F: [2, 0, 2], G: [2, 2, 2], H: [0, 2, 2], O: [1, 1, 1] },
    solids: [{ k: 'poly', faces: [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['A', 'B', 'F', 'E'], ['B', 'C', 'G', 'F'], ['C', 'D', 'H', 'G'], ['D', 'A', 'E', 'H']] }, { k: 'sphere', c: 'O', r: 1, ghost: true }],
    items: [],
  };
  assert.equal(dashed(S.draw(S.prepare(m), m.view)), 3); // chỉ 3 cạnh khuất của hình lập phương
  m.items = [{ t: 'circ', o: 'O', n: [0, 0, 1], r: 1, c: '#2563eb', occ: [1] }];
  assert.ok(dashed(S.draw(S.prepare(m), m.view)) >= 4); // nửa sau của đường tròn xích đạo là nét đứt
});

// ---- Các hình trong nội dung ----
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..');
const SOLIDS = ['toan7', 'toan8', 'toan9', 'toan11', 'toan12'];

test('mọi hình 3D trong tools/solids đã được sinh ra đúng và khớp mô hình (không bị trình sinh cũ ghi đè)', () => {
  let n = 0;
  for (const sub of SOLIDS) {
    const models = require(path.join(root, 'tools', 'solids', sub + '.js'));
    for (const [name, model] of Object.entries(models)) {
      const file = path.join(root, 'content', sub, 'figures', name + '.svg');
      assert.ok(fs.existsSync(file), 'thiếu ' + file);
      const text = fs.readFileSync(file, 'utf8');
      const back = S.extractModel(text);
      assert.ok(back, sub + '/' + name + ': thiếu mô hình 3D (chạy: node tools/build-solids.js)');
      assert.deepEqual(back, JSON.parse(JSON.stringify(model)), sub + '/' + name + ': lỗi thời, hãy chạy node tools/build-solids.js');
      n++;
    }
  }
  assert.ok(n > 120);
});

test('mọi hình 3D vẽ được ở nhiều góc nhìn, không có số NaN và có đủ nét', () => {
  for (const sub of SOLIDS) {
    const models = require(path.join(root, 'tools', 'solids', sub + '.js'));
    for (const [name, model] of Object.entries(models)) {
      const prep = S.prepare(model);
      for (const view of [model.view, { az: 0, el: 0 }, { az: 90, el: 60 }, { az: 200, el: -40 }, { az: 310, el: 85 }]) {
        const svg = S.draw(prep, view);
        assert.ok(!/NaN|Infinity/.test(svg), sub + '/' + name + ' ' + JSON.stringify(view));
        assert.ok(svg.length > 200, sub + '/' + name);
      }
    }
  }
});
