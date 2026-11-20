// Hình không gian Toán 11 (mô hình 3D chính xác; tên tệp giữ nguyên để bài học vẫn tham chiếu được).
const L = require('./lib');
const { add, sub, mul, mid, lerp, RED, BLUE, GREEN, PURPLE, GRAY, pyramidFaces, prismFaces, lbl, seg, pt, caption, model } = L;

const out = {};

// Hình chóp S.ABCD đáy hình bình hành, O là giao điểm hai đường chéo đáy.
out['t11-b10-hinh-chop'] = model({
  view: { az: 24, el: 24 },
  pts: { A: [0, 0, 0], B: [4, 0, 0], C: [5, 2.6, 0], D: [1, 2.6, 0], O: [2.5, 1.3, 0], S: [2.1, 1.1, 3.6] },
  solids: [{ k: 'poly', faces: pyramidFaces(['A', 'B', 'C', 'D'], 'S') }],
  items: [seg('A', 'C', GREEN, { w: 1.4 }), seg('B', 'D', GREEN, { w: 1.4 }), seg('S', 'O', RED, { w: 2 }), pt('O', RED),
    ...lbl(['A', 'B', 'C', 'D', 'S']), ...lbl([{ p: 'O', s: 'O', c: RED, dx: 9, dy: 11 }])],
});

// Lăng trụ đứng tam giác ABC.A'B'C', M thuộc BC, M' thuộc B'C' (M' ứng với M).
{
  const pts = { A: [0, 0, 0], B: [4, 0, 0], C: [1.4, 2.3, 0], "A'": [0, 0, 3.4], "B'": [4, 0, 3.4], "C'": [1.4, 2.3, 3.4] };
  pts.M = mid(pts.B, pts.C); pts["M'"] = mid(pts["B'"], pts["C'"]);
  out['t11-b11-lang-tru'] = model({
    view: { az: 22, el: 22 },
    pts, solids: [{ k: 'poly', faces: prismFaces(['A', 'B', 'C'], ["A'", "B'", "C'"]) }],
    items: [seg('A', 'M', RED, { w: 2 }), seg("A'", "M'", RED, { w: 2 }), pt('M', RED), pt("M'", RED),
      ...lbl(['A', 'B', 'C', "A'", "B'", "C'"]), ...lbl([{ p: 'M', s: 'M', c: RED, dx: 12, dy: 10 }, { p: "M'", s: "M'", c: RED, dx: 12, dy: -8 }])],
  });
}

// Hình chóp S.ABCD, M ∈ SA, N ∈ SB với MN ∥ AB (cắt song song với đáy).
{
  const pts = { A: [0, 0, 0], B: [4, 0, 0], C: [5, 2.6, 0], D: [1, 2.6, 0], S: [2.4, 1.4, 4] };
  pts.M = lerp(pts.A, pts.S, 0.4); pts.N = lerp(pts.B, pts.S, 0.4);
  out['t11-b12-dt-song-song-mp'] = model({
    view: { az: 24, el: 24 },
    pts, solids: [{ k: 'poly', faces: pyramidFaces(['A', 'B', 'C', 'D'], 'S') }],
    items: [seg('M', 'N', RED, { w: 2.4 }), pt('M', RED), pt('N', RED),
      ...lbl(['A', 'B', 'C', 'D', 'S']), ...lbl([{ p: 'M', s: 'M', c: RED }, { p: 'N', s: 'N', c: RED }])],
  });
}

// Hình hộp ABCD.A'B'C'D' (xiên) với các mặt là hình bình hành.
out['t11-b13-hinh-hop'] = (() => {
  const A = [0, 0, 0], B = [4, 0, 0], D = [1.2, 2.4, 0], w = [0.9, 0.7, 3];
  const C = add(B, sub(D, A));
  const pts = { A, B, C, D, "A'": add(A, w), "B'": add(B, w), "C'": add(C, w), "D'": add(D, w) };
  return model({
    view: { az: 24, el: 22 }, pts,
    solids: [{ k: 'poly', faces: prismFaces(['A', 'B', 'C', 'D'], ["A'", "B'", "C'", "D'"]) }],
    items: lbl(['A', 'B', 'C', 'D', "A'", "B'", "C'", "D'"]),
  });
})();

// Định lí Thales trong không gian: ba mặt phẳng song song (P), (Q), (R) cắt hai đường thẳng.
out['t11-b13-thales-khong-gian'] = (() => {
  const z = { P: 6, Q: 3.4, R: 0 };
  const on = (o, d, zz) => [o[0] + d[0] * (6 - zz), o[1] + d[1] * (6 - zz), zz];
  const l1o = [-0.4, 0, 6], l1d = [0.3, 0.05];
  const l2o = [3.4, 0.4, 6], l2d = [0.36, 0.08];
  const pts = {};
  [['A', 'B', 'C', l1o, l1d], ["A'", "B'", "C'", l2o, l2d]].forEach(([a, b, c, o, d]) => { pts[a] = on(o, d, z.P); pts[b] = on(o, d, z.Q); pts[c] = on(o, d, z.R); });
  const plane = (zz, col) => ({ t: 'poly', pts: [[-2.2, -1.4, zz], [6.8, -1.4, zz], [6.8, 1.8, zz], [-2.2, 1.8, zz]], fill: col, op: 0.28, stroke: '#475569', w: 1.3, occ: false });
  const [a1, a2] = [on(l1o, l1d, 6.7), on(l1o, l1d, -0.7)], [b1, b2] = [on(l2o, l2d, 6.7), on(l2o, l2d, -0.7)];
  return model({
    view: { az: 12, el: 14 }, pts, size: [380, 330],
    items: [plane(6, '#60a5fa'), plane(3.4, '#4ade80'), plane(0, '#f87171'),
      seg(a1, a2, BLUE, { w: 2, occ: false }), seg(b1, b2, RED, { w: 2, occ: false }),
      ...['A', 'B', 'C'].map((n) => pt(n, BLUE)), ...["A'", "B'", "C'"].map((n) => pt(n, RED)),
      ...lbl([{ p: 'A', s: 'A', c: BLUE, dx: -11, dy: -9 }, { p: 'B', s: 'B', c: BLUE, dx: -11, dy: -9 }, { p: 'C', s: 'C', c: BLUE, dx: -11, dy: -9 },
        { p: "A'", s: "A'", c: RED, dx: 13, dy: -9 }, { p: "B'", s: "B'", c: RED, dx: 13, dy: -9 }, { p: "C'", s: "C'", c: RED, dx: 13, dy: -9 },
        { p: [-1.8, -1.0, 6], s: '(P)', c: '#334155', dx: 0, dy: 0 }, { p: [-1.8, -1.0, 3.4], s: '(Q)', c: '#334155', dx: 0, dy: 0 }, { p: [-1.8, -1.0, 0], s: '(R)', c: '#334155', dx: 0, dy: 0 }]),
    ],
    notes: [{ s: 'AB/BC = A′B′/B′C′', pos: 'bc', c: '#1d2733', size: 13 }],
  });
})();

// Phép chiếu song song lên mặt phẳng (P) theo phương Δ.
out['t11-b14-phep-chieu'] = (() => {
  const dir = [0.55, -0.35, -1];
  const proj = (p) => { const t = p[2] / -dir[2]; return [p[0] + dir[0] * t, p[1] + dir[1] * t, 0]; };
  const A = [0.8, 0.6, 3.6], B = [4, 1.6, 2.4];
  const pts = { A, B, "A'": proj(A), "B'": proj(B) };
  return model({
    view: { az: 20, el: 26 }, pts,
    items: [{ t: 'poly', pts: [[-1.5, -2, 0], [6.2, -2, 0], [6.2, 3.6, 0], [-1.5, 3.6, 0]], fill: '#60a5fa', op: 0.3, stroke: '#475569', w: 1.4, occ: false },
      seg('A', "A'", PURPLE, { w: 1.6, dash: 'dash', occ: false }), seg('B', "B'", PURPLE, { w: 1.6, dash: 'dash', occ: false }),
      seg('A', 'B', RED, { w: 2.2, occ: false }), seg("A'", "B'", GREEN, { w: 2.2, occ: false }),
      pt('A', RED), pt('B', RED), pt("A'", GREEN), pt("B'", GREEN),
      ...lbl([{ p: 'A', s: 'A', c: RED, dx: -10, dy: -8 }, { p: 'B', s: 'B', c: RED, dx: 10, dy: -8 }, { p: "A'", s: "A'", c: GREEN, dx: -12, dy: 10 }, { p: "B'", s: "B'", c: GREEN, dx: 12, dy: 10 },
        { p: [-1, -1.6, 0], s: '(P)', c: '#475569', dx: 0, dy: 0 }]),
    ],
    notes: [{ s: 'phương chiếu Δ (các đường tím song song)', pos: 'bc', c: PURPLE, size: 12 }],
  });
})();

// Hình lập phương ABCD.A'B'C'D' với góc giữa hai mặt phẳng: AC ∥ A'C', B'D; A'C' và A'B, BC'.
out['t11-b22-goc-hai-duong'] = (() => {
  const pts = { A: [0, 0, 0], B: [3, 0, 0], C: [3, 3, 0], D: [0, 3, 0], "A'": [0, 0, 3], "B'": [3, 0, 3], "C'": [3, 3, 3], "D'": [0, 3, 3] };
  return model({
    view: { az: 24, el: 22 }, pts,
    solids: [{ k: 'poly', faces: prismFaces(['A', 'B', 'C', 'D'], ["A'", "B'", "C'", "D'"]) }],
    items: [seg('A', 'C', RED, { w: 2.2 }), seg("A'", "C'", RED, { w: 2.2 }), seg("A'", 'B', BLUE, { w: 2.2 }), seg("C'", 'B', BLUE, { w: 2.2 }),
      ...lbl(['A', 'B', 'C', 'D', "A'", "B'", "C'", "D'"])],
  });
})();

// Đường thẳng vuông góc với mặt phẳng: S.ABCD với SA ⊥ (ABCD), đáy hình chữ nhật.
function saPerp(extra = {}) {
  const pts = { A: [0, 0, 0], B: [3.6, 0, 0], C: [3.6, 2.4, 0], D: [0, 2.4, 0], S: [0, 0, 3.8] };
  return model({
    view: { az: 32, el: 22 }, pts,
    solids: [{ k: 'poly', faces: pyramidFaces(['A', 'B', 'C', 'D'], 'S') }],
    items: [{ t: 'ra', at: 'A', u: [1, 0, 0], v: [0, 0, 1], s: 0.4, c: RED }, { t: 'ra', at: 'A', u: [0, 1, 0], v: [0, 0, 1], s: 0.4, c: RED },
      ...(extra.items || []), ...lbl(['A', 'B', 'C', 'D', 'S'])],
  });
}
out['t11-b23-duong-vuong-goc-mp'] = saPerp({ items: [seg('S', 'A', RED, { w: 2.4 })] });
// Góc giữa đường thẳng SB và mặt phẳng đáy: góc α = ∠SBA.
out['t11-b24-goc-duong-mp'] = (() => {
  const m = saPerp({ items: [seg('S', 'B', RED, { w: 2.4 }), seg('A', 'B', GREEN, { w: 2.6 })] });
  m.items.push({ t: 'arc', o: 'B', u: [-1, 0, 0], v: [-1, 0, 3.8 / 3.6], r: 0.9, c: RED });
  m.items.push({ t: 'lbl', p: [2.5, 0, 0.45], s: 'α', c: RED, dx: 0, dy: 0, size: 16 });
  return m;
})();

// Hình chóp đều S.ABCD: O là tâm đáy, SO = h là đường cao.
out['t11-b27-hinh-chop-deu'] = (() => {
  const a = 4, h = 3.6;
  const pts = { A: [-a / 2, -a / 2, 0], B: [a / 2, -a / 2, 0], C: [a / 2, a / 2, 0], D: [-a / 2, a / 2, 0], O: [0, 0, 0], S: [0, 0, h] };
  return model({
    view: { az: 24, el: 24 }, pts,
    solids: [{ k: 'poly', faces: pyramidFaces(['A', 'B', 'C', 'D'], 'S') }],
    items: [seg('A', 'C', GREEN, { w: 1.4 }), seg('B', 'D', GREEN, { w: 1.4 }), seg('S', 'O', RED, { w: 2.2 }), pt('O', RED),
      { t: 'ra', at: 'O', u: [1, 1, 0], v: [0, 0, 1], s: 0.4, c: RED },
      ...lbl(['A', 'B', 'C', 'D', 'S']), ...lbl([{ p: 'O', s: 'O', c: RED, dx: 10, dy: 11 }, { p: [0, 0, h / 2], s: 'h', c: RED, dx: 12, dy: 0 }])],
  });
})();

module.exports = out;
