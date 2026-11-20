// Hình không gian Toán 9: hình trụ, hình nón, hình cầu (đúng tỉ lệ theo số liệu của bài, xoay được 360°).
const L = require('./lib');
const { add, mul, mid, RED, BLUE, GRAY, lbl, seg, pt, cap, model, unit } = L;
const out = {};
const NOTE = '#e15759';
const DK = '#1d2733';
const FILL = '#eef5fb';
const U = unit([0.5, -0.866, 0]);                  // hướng "về phía người xem" ở góc nhìn mặc định
const dimV = (x, z0, z1) => [seg([x, 0, z0], [x, 0, z1], NOTE, { w: 1.8, occ: false }), seg([x - 0.15, 0, z0], [x + 0.15, 0, z0], NOTE, { w: 1.4, occ: false }), seg([x - 0.15, 0, z1], [x + 0.15, 0, z1], NOTE, { w: 1.4, occ: false })];
const cn = (s, extra = {}) => ({ s, pos: 'bc', c: NOTE, size: 13, bold: true, ...extra });
const lab = (p, s, c = NOTE, extra = {}) => ({ t: 'lbl', p, s, c, size: 14, ...extra });

// Hình trụ: r, h theo số liệu; nhãn bán kính/chiều cao/ghi chú.
function cylinder({ r, h, rLabel, hLabel, caption }) {
  const k = 3.2 / Math.max(r * 1.4, h), R = r * k, H = h * k;
  const top = [0, 0, H], rim = add(top, mul(U, R));
  return model({
    view: { az: 22, el: 24 }, size: [380, 320], pts: { O: [0, 0, 0], T: top },
    solids: [{ k: 'axi', o: 'O', e: [0, 0, 1], prof: [[0, R], [H, R]], fill: FILL }],
    items: [seg('T', rim, NOTE, { w: 2, dash: 'solid', occ: false }), pt('T', DK), ...dimV(R + 0.6, 0, H),
      lab(mid(top, rim), rLabel, NOTE, { dx: 0, dy: -12 }), lab([R + 0.6, 0, H / 2], hLabel, NOTE, { dx: 24, dy: 0 })],
    notes: caption ? [cn(caption)] : [],
  });
}
// Hình nón: r, h (l tính từ đó).
function cone({ r, h, rLabel, hLabel, lLabel, caption }) {
  const k = 3.4 / Math.max(r * 1.4, h), R = r * k, H = h * k;
  const apex = [0, 0, H], rim = mul(U, R);
  return model({
    view: { az: 22, el: 24 }, size: [380, 320], pts: { O: [0, 0, 0], S: apex },
    solids: [{ k: 'axi', o: 'O', e: [0, 0, 1], prof: [[0, R], [H, 0]], fill: FILL }],
    items: [seg('O', 'S', NOTE, { w: 1.8 }), seg('O', rim, NOTE, { w: 1.8 }), pt('O', DK), { t: 'ra', at: 'O', u: [U[0], U[1], 0], v: [0, 0, 1], s: 0.25 * R, c: NOTE },
      ...lbl([{ p: 'S', s: 'S', c: DK, dx: 0, dy: -12 }, { p: 'O', s: 'O', c: DK, dx: -12, dy: 8 }]),
      ...(hLabel ? [lab([0, 0, H / 2], hLabel, NOTE, { dx: -22, dy: 0 })] : []), ...(rLabel ? [lab(mid([0, 0, 0], rim), rLabel, NOTE, { dx: 0, dy: 14 })] : []),
      ...(lLabel ? [lab(mid(apex, rim), lLabel, NOTE, { dx: 24, dy: -2 })] : [])],
    notes: caption ? [cn(caption)] : [],
  });
}
// Hình cầu tâm O, bán kính R. mode: 'radius' (đoạn bán kính) hoặc 'diameter' (đường kính nằm ngang).
function sphere({ rLabel, mode = 'radius', caption, center = true }) {
  const R = 2.3, P = mul(unit([0.62, -0.5, 0.6]), R);
  const items = [{ t: 'circ', o: 'O', n: [0, 0, 1], r: R, c: '#475569', w: 1.5 }];
  if (mode === 'radius') items.push(seg('O', P, NOTE, { w: 2, dash: 'solid', occ: false }), lab(mid([0, 0, 0], P), rLabel, NOTE, { dx: 4, dy: -13 }));
  else items.push(seg([-R, 0, 0], [R, 0, 0], NOTE, { w: 2, dash: 'solid', occ: false }), lab([0, 0, 0], rLabel, NOTE, { dx: 0, dy: -13 }));
  if (center) items.push(pt('O', DK), lab([0, 0, 0], 'O', DK, { dx: -4, dy: 14, size: 15 }));
  return model({ view: { az: 22, el: 22 }, size: [380, 320], pts: { O: [0, 0, 0] }, solids: [{ k: 'sphere', c: 'O', r: R, fill: FILL }], items, notes: caption ? [cn(caption)] : [] });
}

// ---- Bài 31: hình trụ, hình nón ----
out['bt-t9-b31-q03'] = cylinder({ r: 2, h: 7, rLabel: 'r = 2', hLabel: 'h = 7', caption: 'Diện tích xung quanh Sxq = kπ' });
out['bt-t9-b31-q04'] = cylinder({ r: 4, h: 10, rLabel: 'r = 4', hLabel: 'h = 10', caption: 'Thể tích V = kπ' });
out['bt-t9-b31-q08'] = cylinder({ r: 3, h: 12, rLabel: '3 cm', hLabel: '12 cm', caption: 'Lon nước: đường kính 6 cm;  V = kπ' });
out['bt-t9-b31-q09'] = cylinder({ r: 3, h: 8, rLabel: 'r = 3', hLabel: 'h = ?', caption: 'V = 72π;  chiều cao h = ?' });
out['vd-t9-b31-1'] = cylinder({ r: 3, h: 5, rLabel: 'r = 3', hLabel: 'h = 5', caption: 'Thể tích V = kπ;  k = ?' });
out['nc-t9-b31-n03'] = cylinder({ r: 0.5, h: 2, rLabel: 'r = 0,5 m', hLabel: 'h = 2 m', caption: 'Bồn nước hình trụ: V = ?' });
out['bt-t9-b31-q05'] = cone({ r: 6, h: 8, hLabel: 'h = 8', rLabel: 'r = 6', lLabel: 'l = ?', caption: 'Đường sinh l = ?' });
out['bt-t9-b31-q06'] = cone({ r: 6, h: 8, hLabel: 'h = 8', rLabel: 'r = 6', caption: 'Thể tích V = kπ' });
out['bt-t9-b31-q07'] = cone({ r: 5, h: 12, rLabel: 'r = 5', lLabel: 'l = 13', caption: 'Diện tích xung quanh Sxq = kπ' });
out['nc-t9-b31-n02'] = cone({ r: 3, h: 4, hLabel: 'h = ?', rLabel: 'r = 3', caption: 'Hình nón: Sxq = 15π;  h = ?' });
out['vd-t9-b31-2'] = cone({ r: 3, h: 4, hLabel: 'h = 4', rLabel: 'r = 3', lLabel: 'l = ?', caption: 'Hình nón: Sxq = kπ;  k = ?' });

// Hình trụ và hình nón cùng đáy, cùng chiều cao.
out['nc-t9-b31-n01'] = (() => {
  const R = 1.5, H = 3.2, X = 2.4;
  return model({
    view: { az: 18, el: 24 }, size: [420, 300], fit: 1.3, pts: { O1: [-X, 0, 0], O2: [X, 0, 0], T1: [-X, 0, H], S: [X, 0, H] },
    solids: [{ k: 'axi', o: 'O1', e: [0, 0, 1], prof: [[0, R], [H, R]], fill: FILL }, { k: 'axi', o: 'O2', e: [0, 0, 1], prof: [[0, R], [H, 0]], fill: FILL }],
    items: [...dimV(-X - R - 0.7, 0, H), lab([-X - R - 0.7, 0, H / 2], 'h', NOTE, { dx: -14, dy: 0, size: 16 }), ...lbl([{ p: [-X, 0, 0], s: 'Hình trụ', c: DK, dx: 0, dy: 44, bold: false, size: 14 }, { p: [X, 0, 0], s: 'Hình nón', c: DK, dx: 0, dy: 44, bold: false, size: 14 }])],
    notes: [cn('Cùng đáy, cùng chiều cao:  V trụ : V nón = ?')],
  });
})();

// ---- Bài 32: hình cầu ----
out['bt-t9-b32-q03'] = sphere({ rLabel: 'R = 5', caption: 'Mặt cầu: S = kπ' });
out['bt-t9-b32-q04'] = sphere({ rLabel: 'R = 6', caption: 'Hình cầu: V = kπ' });
out['bt-t9-b32-q05'] = sphere({ rLabel: '20 cm', mode: 'diameter', center: false, caption: 'Quả bóng: đường kính 20 cm;  S = kπ' });
out['bt-t9-b32-q06'] = sphere({ rLabel: 'R = ?', caption: 'S = 64π;  bán kính R = ?' });
out['bt-t9-b32-q07'] = sphere({ rLabel: 'R = 3/2', caption: 'Hình cầu: V = kπ' });
out['vd-t9-b32-1'] = sphere({ rLabel: 'R = 3', caption: 'Mặt cầu: S = kπ' });
out['vd-t9-b32-2'] = sphere({ rLabel: 'R = 3', caption: 'Hình cầu: V = kπ' });
out['nc-t9-b32-n02'] = sphere({ rLabel: 'R = ?', caption: 'V = 36π;  S = kπ;  k = ?' });
out['nc-t9-b32-n03'] = sphere({ rLabel: 'R = 2 dm', caption: 'Diện tích mặt cầu = ? dm²' });

// Hình cầu nội tiếp hình lập phương cạnh 6 (cầu chỉ là hình vẽ phụ: không che nét của hình lập phương).
out['nc-t9-b32-n01'] = (() => {
  const a = 3.4, c = a / 2;
  const pts = { A: [0, 0, 0], B: [a, 0, 0], C: [a, a, 0], D: [0, a, 0], "A'": [0, 0, a], "B'": [a, 0, a], "C'": [a, a, a], "D'": [0, a, a], O: [c, c, c] };
  const faces = [['A', 'B', 'C', 'D'], ["A'", "B'", "C'", "D'"], ['A', 'B', "B'", "A'"], ['B', 'C', "C'", "B'"], ['C', 'D', "D'", "C'"], ['D', 'A', "A'", "D'"]];
  return model({
    view: { az: 24, el: 22 }, size: [380, 320], pts,
    solids: [{ k: 'poly', faces }, { k: 'sphere', c: 'O', r: c, fill: '#cfe0f5', ghost: true }],
    items: [{ t: 'circ', o: 'O', n: [0, 0, 1], r: c, c: '#2563eb', w: 1.5, occ: [1] }, pt('O', DK), lab('O', 'O', DK, { dx: 8, dy: 12, size: 14 }),
      lab(mid(pts.A, pts.B), '6', NOTE, { dx: 0, dy: 15, size: 16 })],
    notes: [cn('Hình cầu nội tiếp hình lập phương cạnh 6:  V = kπ')],
  });
})();

// ---- Hình minh họa tổng hợp ----
// Cách tạo ra hình trụ và hình nón: quay hình chữ nhật / tam giác vuông quanh một cạnh.
out['c-t9-b31-tao-hinh'] = (() => {
  const r = 1.2, h = 2.6, x1 = -5.4, x2 = -1.5, x3 = 1.6, x4 = 5.6;
  const rect = [[x1, 0, 0], [x1 + r, 0, 0], [x1 + r, 0, h], [x1, 0, h]];
  const tri = [[x3, 0, 0], [x3 + r, 0, 0], [x3, 0, h]];
  const axis = (x) => seg([x, 0, -0.3], [x, 0, h + 0.4], NOTE, { w: 1.3, dash: 'dash', occ: false });
  return model({
    view: { az: 10, el: 14 }, size: [520, 280], fit: 1.6, dy: -4, pts: { O2: [x2, 0, 0], O4: [x4, 0, 0] },
    solids: [{ k: 'axi', o: 'O2', e: [0, 0, 1], prof: [[0, r], [h, r]], fill: '#dce9f7' }, { k: 'axi', o: 'O4', e: [0, 0, 1], prof: [[0, r], [h, 0]], fill: '#e3efd6' }],
    items: [{ t: 'poly', pts: rect, fill: '#93c5fd', op: 0.55, stroke: DK, w: 1.6, occ: false }, { t: 'poly', pts: tri, fill: '#bbf7d0', op: 0.7, stroke: DK, w: 1.6, occ: false }, axis(x1), axis(x3),
      { t: 'arrow', a: [x1 + 1.9, 0, h / 2], b: [x2 - 1.5, 0, h / 2], c: DK, w: 1.8, occ: false }, { t: 'arrow', a: [x3 + 1.9, 0, h / 2], b: [x4 - 1.6, 0, h / 2], c: DK, w: 1.8, occ: false },
      lab([x1, 0, h / 2], 'h', NOTE, { dx: -12, dy: 0 }), lab([x1 + r / 2, 0, 0], 'r', NOTE, { dx: 0, dy: 12 }), lab([x3, 0, h / 2], 'h', NOTE, { dx: -12, dy: 0 }), lab([x3 + r / 2, 0, 0], 'r', NOTE, { dx: 0, dy: 12 }),
      lab([x3 + r / 2, 0, h / 2], 'l', '#15803d', { dx: 12, dy: -4 })],
    notes: [{ s: 'Cách tạo ra hình trụ và hình nón', pos: 'tc', c: DK, size: 14, bold: true }, { s: 'Quay hình chữ nhật quanh một cạnh  |  Quay tam giác vuông quanh một cạnh góc vuông', pos: 'bc', c: DK, size: 11.5, bold: true }],
  });
})();
// Hình trụ và hình nón kèm công thức.
out['c-t9-b31-tru-non'] = (() => {
  const r = 1.3, h = 2.8, X = 2.6;
  const rimC = add([-X, 0, h], mul(U, r)), rimN = add([X, 0, 0], mul(U, r));
  return model({
    view: { az: 18, el: 22 }, size: [460, 320], fit: 1.2, dy: 0, pts: { O1: [-X, 0, 0], O2: [X, 0, 0], T: [-X, 0, h], S: [X, 0, h] },
    solids: [{ k: 'axi', o: 'O1', e: [0, 0, 1], prof: [[0, r], [h, r]], fill: '#dce9f7' }, { k: 'axi', o: 'O2', e: [0, 0, 1], prof: [[0, r], [h, 0]], fill: '#e3efd6' }],
    items: [seg('T', rimC, NOTE, { w: 1.8, dash: 'solid', occ: false }), pt('T', DK), seg([-X, 0, 0], [-X, 0, h], NOTE, { w: 1.5, dash: 'dash', occ: false }),
      seg('S', [X, 0, 0], NOTE, { w: 1.5 }), seg([X, 0, 0], rimN, NOTE, { w: 1.5 }), seg('S', rimN, '#15803d', { w: 1.6, occ: false }), pt([X, 0, 0], DK),
      lab(mid([-X, 0, h], rimC), 'r', NOTE, { dx: 0, dy: -11 }), lab([-X, 0, h / 2], 'h', NOTE, { dx: -12, dy: 0 }), lab([X, 0, h / 2], 'h', NOTE, { dx: -12, dy: 0 }), lab(mid([X, 0, 0], rimN), 'r', NOTE, { dx: 0, dy: 12 }), lab(mid([X, 0, h], rimN), 'l', '#15803d', { dx: 12, dy: -4 }),
      lab([-X, 0, 0], 'Hình trụ', DK, { dx: 0, dy: 40, size: 14 }), lab([X, 0, 0], 'Hình nón', DK, { dx: 0, dy: 40, size: 14 })],
    notes: [{ s: 'Hình trụ:  Sxq = 2πrh;  V = πr²h', pos: 'tl', c: DK, size: 12, bold: true }, { s: 'Hình nón (l: đường sinh):  Sxq = πrl;  V = ⅓πr²h;  l² = r² + h²', pos: 'bc', c: DK, size: 12, bold: true }],
  });
})();
// Hình cầu và mặt phẳng cắt hình cầu.
out['c-t9-b32-hinh-cau'] = (() => {
  const R = 2.0, X = 2.8, d = 1.1, rr = Math.sqrt(R * R - d * d);
  const O1 = [-X, 0, 0], O2 = [X, 0, 0], Op = [X, 0, d], P = add(Op, mul([1, 0, 0], rr));
  const Pn = add(O1, mul(unit([0.62, -0.5, 0.6]), R));
  return model({
    view: { az: 16, el: 22 }, size: [500, 300], fit: 1.3, dy: 2, pts: { O1, O2, Op, P },
    solids: [{ k: 'sphere', c: 'O1', r: R, fill: '#dce9f7' }, { k: 'sphere', c: 'O2', r: R, fill: '#dce9f7' }],
    items: [{ t: 'circ', o: O1, n: [0, 0, 1], r: R, c: '#475569', w: 1.4 }, seg(O1, Pn, NOTE, { w: 2, dash: 'solid', occ: false }), pt(O1, DK), lab(O1, 'O', DK, { dx: -4, dy: 14 }), lab(mid(O1, Pn), 'R', NOTE, { dx: 6, dy: -12 }),
      { t: 'circ', o: Op, n: [0, 0, 1], r: rr, c: '#f59e0b', w: 2.2, dash: 'solid' }, { t: 'poly', pts: Array.from({ length: 48 }, (_, i) => [X + rr * Math.cos((i / 48) * 2 * Math.PI), rr * Math.sin((i / 48) * 2 * Math.PI), d]), fill: '#fbbf24', op: 0.25, occ: false },
      seg(O2, Op, '#15803d', { w: 1.8, dash: 'solid', occ: false }), seg(Op, P, '#2563eb', { w: 1.8, dash: 'solid', occ: false }), seg(O2, P, NOTE, { w: 1.8, dash: 'solid', occ: false }),
      pt(O2, DK), pt(Op, DK), { t: 'ra', at: Op, u: [0, 0, -1], v: [1, 0, 0], s: 0.22, c: DK },
      lab(O2, 'O', DK, { dx: -4, dy: 14 }), lab(Op, "O′", DK, { dx: -14, dy: -6 }), lab(mid(O2, Op), 'd', '#15803d', { dx: -12, dy: 4 }), lab(mid(Op, P), 'r', '#2563eb', { dx: 0, dy: -11 }), lab(mid(O2, P), 'R', NOTE, { dx: 12, dy: 6 })],
    notes: [{ s: 'Hình cầu tâm O, bán kính R:  S = 4πR²;  V = (4/3)πR³', pos: 'tl', c: DK, size: 12, bold: true }, { s: 'Mặt phẳng cắt hình cầu theo hình tròn:  R² = d² + r²', pos: 'bc', c: DK, size: 12, bold: true }],
  });
})();

module.exports = out;
