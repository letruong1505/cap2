// Hình không gian Toán 12 (mô hình 3D chính xác theo dữ kiện từng bài; tên tệp giữ nguyên).
const L = require('./lib');
const { add, sub, mul, mid, lerp, unit, len, RED, BLUE, GREEN, PURPLE, ORANGE, GRAY, pyramidFaces, prismFaces, tetraFaces, lbl, seg, pt, axes, caption, model } = L;
const out = {};
const OXYZ = { az: 124, el: 22 };
const PR = ["A'", "B'", "C'", "D'"], BASE = ['A', 'B', 'C', 'D'];
const box = (o, du, dv, dw) => { // hình hộp từ gốc o và ba vectơ cạnh
  const A = o, B = add(o, du), D = add(o, dv), C = add(B, dv), w = dw;
  return { A, B, C, D, "A'": add(A, w), "B'": add(B, w), "C'": add(C, w), "D'": add(D, w) };
};
const prismSolid = (n4 = true) => [{ k: 'poly', faces: prismFaces(n4 ? BASE : ['A', 'B', 'C'], n4 ? PR : ["A'", "B'", "C'"]) }];
const P8 = lbl(['A', 'B', 'C', 'D', "A'", "B'", "C'", "D'"]);
const dotsRed = (ns) => ns.map((n) => pt(n, RED));

// ---- Chương 2 bài 6: hình khối quen thuộc ----
out['c2-6-chop-tu-giac'] = model({
  view: { az: 24, el: 24 },
  pts: { A: [0, 0, 0], B: [4, 0, 0], C: [5, 2.6, 0], D: [1, 2.6, 0], S: [2.1, 1.1, 3.6] },
  solids: [{ k: 'poly', faces: pyramidFaces(BASE, 'S') }], items: lbl(['A', 'B', 'C', 'D', 'S']),
  notes: [caption('Hình chóp S.ABCD, đáy là hình bình hành')],
});
out['c2-6-hinh-hop-chu-nhat'] = model({
  view: { az: 24, el: 22 }, pts: box([0, 0, 0], [3.4, 0, 0], [0, 2.2, 0], [0, 0, 3]), solids: prismSolid(), items: P8,
  notes: [caption('Hình hộp chữ nhật ABCD.A\'B\'C\'D\' — minh họa')],
});
out['c2-6-hinh-hop'] = model({
  view: { az: 24, el: 22 }, pts: box([0, 0, 0], [4, 0, 0], [1.2, 2.4, 0], [0.9, 0.7, 3]), solids: prismSolid(), items: P8,
  notes: [caption('Hình hộp ABCD.A\'B\'C\'D\' — minh họa')],
});
out['c2-6-hinh-lap-phuong'] = model({
  view: { az: 24, el: 22 }, pts: box([0, 0, 0], [3, 0, 0], [0, 3, 0], [0, 0, 3]), solids: prismSolid(), items: P8,
  notes: [caption('Hình lập phương ABCD.A\'B\'C\'D\' cạnh 1')],
});
out['c2-6-lang-tru-tu-giac-deu'] = model({
  view: { az: 24, el: 22 }, pts: box([0, 0, 0], [2.4, 0, 0], [0, 2.4, 0], [0, 0, 4.4]), solids: prismSolid(), items: P8,
  notes: [caption('Lăng trụ tứ giác đều (minh họa)')],
});
out['c2-6-lang-tru'] = model({
  view: { az: 22, el: 22 },
  pts: { A: [0, 0, 0], B: [4, 0, 0], C: [1.4, 2.3, 0], "A'": [0, 0, 3.4], "B'": [4, 0, 3.4], "C'": [1.4, 2.3, 3.4] },
  solids: prismSolid(false), items: lbl(['A', 'B', 'C', "A'", "B'", "C'"]),
  notes: [caption('Lăng trụ tam giác ABC.A\'B\'C\' — minh họa')],
});
const TET = { A: [0.1, 0.4, 3.3], B: [-2.4, 0.5, 0], C: [0.2, -1.7, 0], D: [2.4, 0.9, 0] };
const tet = (extraPts = {}, extraItems = [], notes = []) => model({
  view: { az: 14, el: 20 }, pts: { ...TET, ...extraPts }, solids: [{ k: 'poly', faces: tetraFaces('A', 'B', 'C', 'D') }],
  items: [...extraItems, ...lbl(['A', 'B', 'C', 'D'])], notes,
});
out['c2-6-tu-dien'] = model({
  view: { az: 14, el: 20 }, pts: { A: [-2.4, 0.5, 0], B: [2.4, 0.9, 0], C: [0.2, -1.7, 0], D: [0.1, 0.4, 3.3] },
  solids: [{ k: 'poly', faces: tetraFaces('A', 'B', 'C', 'D') }], items: lbl(['A', 'B', 'C', 'D']),
  notes: [caption('Tứ diện ABCD (cạnh AB khuất, vẽ nét đứt)')],
});
// Tứ diện trong phần vectơ.
out['t12-v-tu-dien'] = tet();
{
  const G = mul(add(add(TET.B, TET.C), TET.D), 1 / 3);
  out['t12-v-tu-dien-g'] = tet({ G }, [seg('A', 'G', RED, { w: 2.2 }), seg('B', 'C', GRAY, { w: 0.01, dash: 'hide' }), pt('G', RED), ...lbl([{ p: 'G', s: 'G', c: RED, dx: 4, dy: 14 }])]);
  out['t12-v-tu-dien-q09'] = tet({ G, M: mid(TET.A, G) }, [seg('A', 'G', RED, { w: 2.2 }), pt('G', RED), pt('M', RED),
    ...lbl([{ p: 'G', s: 'G', c: RED, dx: 4, dy: 14 }, { p: 'M', s: 'M', c: RED, dx: 13, dy: 0 }])]);
}
// AC ⊥ AB, BD ⊥ AB; M, N là trung điểm AB, CD.
{
  const A = [-1.8, 0, 0], B = [1.8, 0, 0], C = [-1.8, -2.4, 0.5], D = [1.8, 0.5, 2.4];
  const pts = { A, B, C, D, M: mid(A, B), N: mid(C, D) };
  out['t12-v-tu-dien-mn'] = model({
    view: { az: -28, el: 32 }, pts, solids: [{ k: 'poly', faces: tetraFaces('A', 'B', 'C', 'D') }],
    items: [seg('M', 'N', RED, { w: 2 }), pt('M', RED), pt('N', RED),
      { t: 'ra', at: 'A', u: [1, 0, 0], v: [0, -2.4, 0.5], s: 0.45, c: RED }, { t: 'ra', at: 'B', u: [-1, 0, 0], v: [0, 0.5, 2.4], s: 0.45, c: RED },
      ...lbl(['A', 'B', 'C', 'D']), ...lbl([{ p: 'M', s: 'M', c: RED }, { p: 'N', s: 'N', c: RED }])],
  });
}
// MB + 2MA = 0 và NC = 2DN.
{
  const pts = { ...TET };
  pts.M = lerp(TET.A, TET.B, 1 / 3); pts.N = lerp(TET.D, TET.C, 1 / 3);
  out['t12-v-tu-dien-mn2'] = model({
    view: { az: 14, el: 20 }, pts, solids: [{ k: 'poly', faces: tetraFaces('A', 'B', 'C', 'D') }],
    items: [seg('M', 'N', RED, { w: 2 }), pt('M', RED), pt('N', RED), ...lbl(['A', 'B', 'C', 'D']), ...lbl([{ p: 'M', s: 'M', c: RED }, { p: 'N', s: 'N', c: RED }])],
  });
}

// ---- Hệ toạ độ Oxyz ----
out['c2-7-he-truc-oxyz'] = (() => {
  const M = [2.6, 2.4, 2.2];
  const edge = (a, b) => seg(a, b, '#94a3b8', { w: 1.3, dash: 'dash', occ: false });
  const X = [M[0], 0, 0], Y = [0, M[1], 0], Z = [0, 0, M[2]], XY = [M[0], M[1], 0], XZ = [M[0], 0, M[2]], YZ = [0, M[1], M[2]];
  return model({
    view: OXYZ, size: [380, 320],
    items: [...axes([4, 3.8, 3.6]),
      edge(X, XY), edge(Y, XY), edge(X, XZ), edge(Z, XZ), edge(Y, YZ), edge(Z, YZ), edge(XY, M), edge(XZ, M), edge(YZ, M),
      { t: 'arrow', a: [0, 0, 0], b: M, c: BLUE, w: 2.2, occ: false },
      { t: 'arrow', a: [0, 0, 0], b: [1, 0, 0], c: '#111827', w: 2.4, occ: false }, { t: 'arrow', a: [0, 0, 0], b: [0, 1, 0], c: '#111827', w: 2.4, occ: false }, { t: 'arrow', a: [0, 0, 0], b: [0, 0, 1], c: '#111827', w: 2.4, occ: false },
      ...lbl([{ p: [0.55, 0, -0.32], s: 'i', c: '#111827', dx: 0, dy: 0, bold: false }, { p: [0, 0.55, -0.32], s: 'j', c: '#111827', dx: 0, dy: 0, bold: false }, { p: [-0.28, 0, 0.5], s: 'k', c: '#111827', dx: 0, dy: 0, bold: false },
        { p: [0, 0, 0], s: 'O', c: '#111827', dx: -10, dy: 12 }, { p: M, s: 'M', c: BLUE, dx: 10, dy: -8 }]), pt(M, BLUE)],
    notes: [caption('Hệ toạ độ Oxyz: OM = xi + yj + zk')],
  });
})();

// Đường thẳng Δ đi qua M₀ với vectơ chỉ phương u.
out['c2-7-duong-thang-u'] = (() => {
  const M0 = [1.2, 0.8, 1.6], u = [1.1, 1.0, 0.9];
  const a = sub(M0, mul(u, 0.7)), b = add(M0, mul(u, 1.5));
  return model({
    view: OXYZ,
    items: [...axes([3.6, 3.6, 3.4]), seg(a, b, '#2f5f98', { w: 2.2, occ: false }),
      { t: 'arrow', a: M0, b: add(M0, u), c: '#111827', w: 2.4, occ: false },
      seg(M0, [M0[0], M0[1], 0], '#94a3b8', { w: 1.2, dash: 'dash', occ: false }), pt(M0, '#2f5f98', 4),
      ...lbl([{ p: M0, s: 'M₀', c: '#2f5f98', dx: -14, dy: 8 }, { p: add(M0, mul(u, 0.55)), s: 'u', c: '#111827', dx: 12, dy: 10 }, { p: b, s: 'Δ', c: '#2f5f98', dx: 12, dy: -6 }, { p: [0, 0, 0], s: 'O', c: '#475569', dx: -10, dy: 12, bold: false }])],
    notes: [caption('Δ đi qua M₀, vectơ chỉ phương u')],
  });
})();

// Hai đường thẳng chéo nhau Δ₁, Δ₂.
out['c2-7-hai-duong-cheo'] = (() => {
  const d1a = [0.6, -2.4, 2.4], d1b = [0.6, 2.8, 2.4], d2a = [-1.6, 1.0, 0], d2b = [2.6, 1.0, 0];
  return model({
    view: OXYZ,
    items: [...axes([3.6, 3.6, 3.4]), seg(d1a, d1b, '#2f5f98', { w: 2.3, occ: false }), seg(d2a, d2b, '#111827', { w: 2.3, occ: false }),
      seg([0.6, 1.0, 2.4], [0.6, 1.0, 0], '#94a3b8', { w: 1.2, dash: 'dash', occ: false }),
      ...lbl([{ p: d1b, s: 'Δ₁', c: '#2f5f98', dx: 12, dy: -6 }, { p: d2a, s: 'Δ₂', c: '#111827', dx: -4, dy: 14 }, { p: [0, 0, 0], s: 'O', c: '#475569', dx: -10, dy: 12, bold: false }])],
    notes: [caption('Hai đường thẳng chéo nhau: không song song, không cắt nhau')],
  });
})();

// Hình 2.34: bóng đèn trong góc phòng.
out['c2-7-hinh-2-34'] = (() => {
  const T = [1.5, 1, 2], W = 3.4;
  const wall = (pts, col) => ({ t: 'poly', pts, fill: col, op: 0.35, stroke: '#64748b', w: 1.2, occ: false });
  return model({
    view: OXYZ,
    items: [wall([[0, 0, 0], [W, 0, 0], [W, W, 0], [0, W, 0]], '#e2e8f0'), wall([[0, 0, 0], [W, 0, 0], [W, 0, 3.4], [0, 0, 3.4]], '#bfdbfe'), wall([[0, 0, 0], [0, W, 0], [0, W, 3.4], [0, 0, 3.4]], '#bfdbfe'),
      ...axes([3.9, 3.9, 3.8]),
      seg(T, [0, T[1], T[2]], '#0e90d2', { w: 1.5, dash: 'dash', occ: false }), seg(T, [T[0], 0, T[2]], '#0e90d2', { w: 1.5, dash: 'dash', occ: false }), seg(T, [T[0], T[1], 0], '#0e90d2', { w: 1.5, dash: 'dash', occ: false }),
      pt(T, '#0e90d2', 5),
      ...lbl([{ p: [0.75, T[1], T[2]], s: '1,5 m', c: '#0e90d2', dx: -26, dy: -4, size: 13 }, { p: [T[0], 0.5, T[2]], s: '1 m', c: '#0e90d2', dx: 18, dy: 8, size: 13 }, { p: [T[0], T[1], 1], s: '2 m', c: '#0e90d2', dx: 18, dy: 0, size: 13 },
        { p: [0, 0, 0], s: 'O', c: '#111827', dx: -10, dy: 12 }]),
    ],
    notes: [caption('Hình 2.34 (minh họa): bóng đèn treo cách sàn 2 m')],
  });
})();

// Hình 2.38: ABCM.FODE là hình hộp chữ nhật với O, F∈Ox, D∈Oy, B∈Oz.
out['c2-7-hinh-2-38'] = (() => {
  const pts = { O: [0, 0, 0], F: [3, 0, 0], D: [0, 4, 0], E: [3, 4, 0], B: [0, 0, 3], A: [3, 0, 3], C: [0, 4, 3], M: [3, 4, 3] };
  const faces = [['O', 'F', 'E', 'D'], ['B', 'A', 'M', 'C'], ['O', 'F', 'A', 'B'], ['F', 'E', 'M', 'A'], ['E', 'D', 'C', 'M'], ['D', 'O', 'B', 'C']];
  return model({
    view: OXYZ, size: [380, 320], pts, solids: [{ k: 'poly', faces }],
    items: [...axes([4.6, 5.4, 4.2], [0, 0, 0]), { t: 'arrow', a: 'O', b: 'M', c: '#0e90d2', w: 2, dash: 'dash', occ: false },
      ...lbl(['A', 'B', 'C', 'D', 'E', 'F']), ...lbl([{ p: 'M', s: 'M', c: '#0e90d2' }, { p: 'O', s: 'O', c: '#111827', dx: -10, dy: 12 }])],
    notes: [caption('Hình 2.38 (minh họa): ABCM.FODE là hình hộp chữ nhật')],
  });
})();

// Hình 2.40: A' ≡ O, D' ∈ Ox, B' ∈ Oy, A ∈ Oz, C(2; 3; 5).
out['c2-7-hinh-2-40'] = (() => {
  const pts = { "A'": [0, 0, 0], "D'": [2, 0, 0], "B'": [0, 3, 0], "C'": [2, 3, 0], A: [0, 0, 5], D: [2, 0, 5], B: [0, 3, 5], C: [2, 3, 5] };
  return model({
    view: OXYZ, size: [380, 330], pts, solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }],
    items: [...axes([3.8, 4.8, 6.2]), ...lbl(['A', 'B', 'C', 'D', "A'", "B'", "C'", "D'"], { size: 14 })],
    notes: [caption('Hình 2.40 (minh họa): A\' ≡ O, D\' ∈ Ox, B\' ∈ Oy, A ∈ Oz')],
  });
})();

// Hình 2.42: lăng trụ ABC.A'B'C' với A(1; 0; 2), B(3; 2; 5), C(7; −3; 9), A'(5; 0; 1).
out['c2-7-hinh-2-42'] = (() => {
  const A = [1, 0, 2], B = [3, 2, 5], C = [7, -3, 9], Ap = [5, 0, 1], d = sub(Ap, A);
  return model({
    view: { az: 40, el: 24 }, size: [380, 320],
    pts: { A, B, C, "A'": Ap, "B'": add(B, d), "C'": add(C, d) },
    solids: [{ k: 'poly', faces: prismFaces(['A', 'B', 'C'], ["A'", "B'", "C'"]) }], items: lbl(['A', 'B', 'C', "A'", "B'", "C'"]),
    notes: [caption('Hình 2.42 (minh họa): lăng trụ tam giác ABC.A\'B\'C\'')],
  });
})();

// Hình 2.45: hình hộp chữ nhật, A ≡ O, D(2; 0; 0), B(0; 4; 0), A'(0; 0; 3).
out['c2-7-hinh-2-45'] = (() => {
  const pts = box([0, 0, 0], [2, 0, 0], [0, 4, 0], [0, 0, 3]);
  // đặt tên theo đề: D trên Ox, B trên Oy -> A, D, C, B quanh đáy
  const P = { A: pts.A, D: pts.B, C: pts.C, B: pts.D, "A'": pts["A'"], "D'": pts["B'"], "C'": pts["C'"], "B'": pts["D'"] };
  return model({
    view: OXYZ, size: [380, 320], pts: P, solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }],
    items: [...axes([3.4, 5.2, 4.2]), ...lbl(['A', 'B', 'C', 'D', "A'", "B'", "C'", "D'"], { size: 14 })],
    notes: [caption('Hình 2.45 (minh họa): A trùng O')],
  });
})();

// Bài 2.18: hình hộp OABC.O'A'B'C' với A(1; 1; −1), B(0; 3; 0).
out['c2-7-bai-2-18'] = (() => {
  const O = [0, 0, 0], A = [1, 1, -1], B = [0, 3, 0], C = add(O, sub(B, A)), w = [0.7, -0.6, 1.9];
  const pts = { O, A, B, C, "O'": add(O, w), "A'": add(A, w), "B'": add(B, w), "C'": add(C, w) };
  return model({
    view: OXYZ, size: [380, 320], pts,
    solids: [{ k: 'poly', faces: prismFaces(['O', 'A', 'B', 'C'], ["O'", "A'", "B'", "C'"]) }],
    items: [...axes([3.4, 4.6, 3.6]), ...lbl(['O', 'A', 'B', 'C', "O'", "A'", "B'", "C'"], { size: 14 })],
    notes: [caption('Hình hộp OABC.O\'A\'B\'C\' (minh họa)')],
  });
})();
// Ôn tập 2.39: A(2; 3; 1), C(−1; 2; 3), O'(1; −2; 2).
out['c2-on-tap-2-39'] = (() => {
  const O = [0, 0, 0], A = [2, 3, 1], C = [-1, 2, 3], w = [1, -2, 2], B = add(A, C);
  const pts = { O, A, B, C, "O'": w, "A'": add(A, w), "B'": add(B, w), "C'": add(C, w) };
  return model({
    view: OXYZ, size: [380, 340], pts,
    solids: [{ k: 'poly', faces: prismFaces(['O', 'A', 'B', 'C'], ["O'", "A'", "B'", "C'"]) }],
    items: [...axes([3.4, 6.2, 6.8]), ...lbl(['O', 'A', 'B', 'C', "O'", "A'", "B'", "C'"], { size: 14 })],
    notes: [caption('Hình hộp OABC.O\'A\'B\'C\' (minh họa theo toạ độ đề bài)')],
  });
})();
// Hình 2.51: phòng 8 m × 6 m × 3 m, đèn ở chính giữa trần.
out['c2-8-bai-2-23'] = (() => {
  const pts = { O: [0, 0, 0], P: [8, 0, 0], Q: [8, 6, 0], R: [0, 6, 0], S: [0, 0, 3], T: [8, 0, 3], U: [8, 6, 3], W: [0, 6, 3], D: [4, 3, 3] };
  const faces = [['O', 'P', 'Q', 'R'], ['S', 'T', 'U', 'W'], ['O', 'P', 'T', 'S'], ['P', 'Q', 'U', 'T'], ['Q', 'R', 'W', 'U'], ['R', 'O', 'S', 'W']];
  return model({
    view: OXYZ, size: [400, 320], pts, solids: [{ k: 'poly', faces }],
    items: [...axes([9.4, 7.2, 4.2]), pt('D', '#0e90d2', 5),
      ...lbl(['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W']), ...lbl([{ p: 'D', s: 'Đèn', c: '#0e90d2', dx: 0, dy: -13, size: 13 },
        { p: mid(pts.O, pts.P), s: '8 m', c: '#475569', dx: 0, dy: 13, bold: false, size: 12 }, { p: mid(pts.P, pts.Q), s: '6 m', c: '#475569', dx: 14, dy: 8, bold: false, size: 12 }, { p: mid(pts.O, pts.S), s: '3 m', c: '#475569', dx: -16, dy: 0, bold: false, size: 12 }])],
    notes: [caption('Hình 2.51 (minh họa)')],
  });
})();
// Hình 2.47b: căn nhà gỗ, A'B' = (−120; 0; 300), A'O' = (−240; 0; 0) (đơn vị 100).
out['c2-8-nha-go'] = (() => {
  const pts = { O: [0, 0, 0], A: [2.4, 0, 0], B: [1.2, 0, 3], "O'": [0, 4, 0], "A'": [2.4, 4, 0], "B'": [1.2, 4, 3] };
  const faces = [['O', 'A', 'B'], ["O'", "A'", "B'"], ['O', 'A', "A'", "O'"], ['A', 'B', "B'", "A'"], ['B', 'O', "O'", "B'"]];
  return model({
    view: OXYZ, size: [380, 320], pts, solids: [{ k: 'poly', faces }],
    items: [...axes([3.8, 5.2, 4.2]), { t: 'arc', o: "A'", u: [-1, 0, 0], v: [-1.2, 0, 3], r: 0.8, c: RED },
      ...lbl(['O', 'A', 'B', "O'", "A'", "B'"], { size: 14 }), ...lbl([{ p: add(pts["A'"], [-0.5, 0, 0.3]), s: 'α', c: RED, dx: 0, dy: 0, size: 16 }])],
    notes: [caption('Hình 2.47b (minh họa)')],
  });
})();
// Ôn tập 2.53: đèn trong góc trần, Oz hướng xuống (hệ toạ độ thuận: Ox, Oy, Oz).
out['c2-on-tap-2-42'] = (() => {
  const T = [1.6, -1.2, -0.5]; // x = 1,6; y = 1,2 (trục y hướng −Y thế giới); z = 0,5 hướng xuống
  const wall = (pts, col) => ({ t: 'poly', pts, fill: col, op: 0.4, stroke: '#64748b', w: 1.2, occ: false });
  return model({
    view: { az: 120, el: -18 }, size: [380, 320],
    items: [wall([[0, 0, 0], [3.6, 0, 0], [3.6, -3.6, 0], [0, -3.6, 0]], '#e2e8f0'), wall([[0, 0, 0], [3.6, 0, 0], [3.6, 0, -3], [0, 0, -3]], '#cbd5e1'), wall([[0, 0, 0], [0, -3.6, 0], [0, -3.6, -3], [0, 0, -3]], '#cbd5e1'),
      { t: 'arrow', a: [0, 0, 0], b: [4.2, 0, 0], c: GRAY, w: 1.5, occ: false }, { t: 'arrow', a: [0, 0, 0], b: [0, -4.2, 0], c: GRAY, w: 1.5, occ: false }, { t: 'arrow', a: [0, 0, 0], b: [0, 0, -3.4], c: GRAY, w: 1.5, occ: false },
      seg(T, [0, T[1], T[2]], '#0e90d2', { w: 1.5, dash: 'dash', occ: false }), seg(T, [T[0], 0, T[2]], '#0e90d2', { w: 1.5, dash: 'dash', occ: false }), seg(T, [T[0], T[1], 0], '#0e90d2', { w: 1.5, dash: 'dash', occ: false }),
      pt(T, '#0e90d2', 5),
      ...lbl([{ p: [4.55, 0, 0], s: 'x', c: '#334155', dx: 0, dy: 0, bold: false }, { p: [0, -4.55, 0], s: 'y', c: '#334155', dx: 0, dy: 0, bold: false }, { p: [0, 0, -3.8], s: 'z (hướng xuống)', c: '#334155', dx: 0, dy: 0, bold: false },
        { p: [0, 0, 0], s: 'O', c: '#111827', dx: -11, dy: -8 }, { p: [0.8, T[1], T[2]], s: '1,6 m', c: '#0e90d2', dx: -4, dy: 16, size: 13, bold: false }, { p: [T[0], -0.6, T[2]], s: '1,2 m', c: '#0e90d2', dx: 24, dy: 12, size: 13, bold: false }, { p: [T[0], T[1], -0.25], s: '0,5 m', c: '#0e90d2', dx: 28, dy: -6, size: 13, bold: false }])],
    notes: [caption('Hình 2.53 (minh họa)')],
  });
})();

// ---- Chương 5: phương pháp toạ độ trong không gian ----
out['c5-14-mat-phang-chan'] = (() => {
  const pts = { O: [0, 0, 0], A: [3, 0, 0], B: [0, 3.2, 0], C: [0, 0, 2.8] };
  return model({
    view: OXYZ, size: [380, 320], pts, solids: [{ k: 'poly', faces: tetraFaces('O', 'A', 'B', 'C'), fill: 'none' }],
    items: [{ t: 'poly', pts: ['A', 'B', 'C'], fill: '#60a5fa', op: 0.3, stroke: '#2563eb', w: 1.6, occ: false },
      ...[['A', [4.4, 0, 0]], ['B', [0, 4.6, 0]], ['C', [0, 0, 3.8]]].map(([n, e]) => ({ t: 'arrow', a: n, b: e, c: GRAY, w: 1.5, occ: false })),
      ...lbl([{ p: [4.8, 0, 0], s: 'x', c: '#334155', dx: 0, dy: 0, bold: false }, { p: [0, 5.0, 0], s: 'y', c: '#334155', dx: 0, dy: 0, bold: false }, { p: [0, 0, 4.2], s: 'z', c: '#334155', dx: 0, dy: 0, bold: false }]),
      ...lbl(['A', 'B', 'C']), ...lbl([{ p: 'O', s: 'O', c: '#111827', dx: -10, dy: 12, bold: false }])],
    notes: [caption('Mặt phẳng cắt các trục Ox, Oy, Oz tại A, B, C')],
  });
})();
out['c5-16-goc-duong-mat'] = (() => {
  const I = [0, 0, 0], d = [1.0, 0.7, 1.9], Q = mul(d, 1.2), H = [Q[0], Q[1], 0];
  return model({
    view: { az: 22, el: 24 }, size: [380, 320], pts: { I, H, Q },
    items: [{ t: 'poly', pts: [[-3, -2.2, 0], [3.6, -2.2, 0], [3.6, 2.6, 0], [-3, 2.6, 0]], fill: '#60a5fa', op: 0.28, stroke: '#2563eb', w: 1.4, occ: false },
      seg(add(I, mul(d, -0.5)), add(I, mul(d, 1.8)), '#111827', { w: 2.4, occ: false }), seg('I', 'H', '#334155', { w: 1.7, occ: false }), seg('Q', 'H', '#94a3b8', { w: 1.4, dash: 'dash', occ: false }),
      { t: 'ra', at: 'H', u: [-Q[0], -Q[1], 0], v: [0, 0, 1], s: 0.3, c: RED }, { t: 'arc', o: 'I', u: [Q[0], Q[1], 0], v: Q, r: 0.9, c: RED },
      pt('I', '#111827'), pt('H', '#111827'),
      ...lbl([{ p: 'I', s: 'I', c: '#111827', dx: -12, dy: 10 }, { p: 'H', s: 'H', c: '#111827', dx: 12, dy: 10 }, { p: add(I, mul(d, 1.8)), s: 'Δ', c: '#111827', dx: 12, dy: -6 }, { p: [-2.4, 1.9, 0], s: '(P)', c: '#2563eb', dx: 0, dy: 0 },
        { p: [0.55, 0.38, 0.55], s: 'φ', c: RED, dx: 10, dy: 0, size: 16 }])],
    notes: [caption('Góc φ giữa Δ và (P) là góc giữa Δ và hình chiếu IH')],
  });
})();
out['c5-17-mat-cau'] = (() => {
  const R = 2.4, I = [0, 0, 0], N = [R * 0.62, -R * 0.45, R * 0.64];
  const n = len(N);
  return model({
    view: { az: 28, el: 20 }, size: [380, 320], pts: { I, N: mul(N, R / n) },
    solids: [{ k: 'sphere', c: 'I', r: R, fill: '#e8f0fb' }],
    items: [{ t: 'circ', o: 'I', n: [0, 0, 1], r: R, c: '#94a3b8', w: 1.3 }, seg('I', 'N', '#2f5f98', { w: 2, dash: 'solid', occ: false }), pt('I', '#111827'), pt('N', '#2f5f98'),
      ...lbl([{ p: 'I', s: 'I', c: '#111827', dx: -4, dy: 14 }, { p: 'N', s: 'N', c: '#2f5f98', dx: 12, dy: -8 }, { p: mid([0, 0, 0], mul(N, R / n)), s: 'R', c: '#2f5f98', dx: 6, dy: -12 }, { p: [-R * 0.78, 0, R * 0.78], s: '(S)', c: '#475569', dx: -10, dy: -10, bold: false }])],
    notes: [caption('Mặt cầu (S): tập các điểm cách I một khoảng R')],
  });
})();
// Bể nghiêng 5.24b: lập phương cạnh 1 m, độ cao nước 40, 44, 48 (cm); D = 44.
out['c5-5-24b-be-nghieng'] = (() => {
  const s = 10, h = (cm) => cm / 10; // đơn vị: 10 cm
  const pts = { ...box([0, 0, 0], [s, 0, 0], [0, s, 0], [0, 0, s]) };
  const Wp = { A: [0, 0, h(40)], B: [s, 0, h(44)], C: [s, s, h(48)], D: [0, s, h(44)] };
  const names = { A: [0, 0, 0], B: [s, 0, 0], C: [s, s, 0], D: [0, s, 0] };
  return model({
    view: { az: 24, el: 22 }, size: [380, 320], pts: { ...pts, WA: Wp.A, WB: Wp.B, WC: Wp.C, WD: Wp.D },
    solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }],
    items: [{ t: 'poly', pts: ['WA', 'WB', 'WC', 'WD'], fill: '#38bdf8', op: 0.55, stroke: '#0284c7', w: 1.8, occ: false },
      ...['A', 'B', 'C', 'D'].map((n) => seg(n, 'W' + n, '#94a3b8', { w: 1.2, dash: 'dash', occ: false })),
      ...lbl([{ p: 'WA', s: 'A', c: '#0369a1', dx: -12, dy: 4 }, { p: 'WB', s: 'B', c: '#0369a1', dx: 12, dy: 6 }, { p: 'WC', s: 'C', c: '#0369a1', dx: 12, dy: -6 }, { p: 'WD', s: 'D', c: '#0369a1', dx: -10, dy: -8 }])],
    notes: [caption('Bể lập phương cạnh 1 m; mặt nước ABCD cao 40, 44, 48 cm (A, B, C)')],
  });
})();
// Hình 5.32: cây cột và bóng trên mặt đất.
out['c5-5-32-cay-cot'] = (() => {
  const A = [0, 0, 6], Ap = [3 * Math.cos(Math.PI / 3), 3 * Math.cos(Math.PI / 6), 0];
  return model({
    view: OXYZ, size: [380, 330], pts: { A, "A'": Ap, O: [0, 0, 0] },
    items: [...axes([4, 4.4, 7.4]), seg('O', 'A', '#b4793a', { w: 5, dash: 'solid', occ: false }), seg('A', "A'", '#0e90d2', { w: 1.6, dash: 'dash', occ: false }), seg('O', "A'", '#111827', { w: 2.2, occ: false }),
      { t: 'arc', o: 'O', u: [1, 0, 0], v: Ap, r: 1.3, c: RED }, { t: 'arc', o: 'O', u: [0, 1, 0], v: Ap, r: 0.9, c: RED },
      pt('A', '#0e90d2'), pt("A'", '#0e90d2'),
      ...lbl([{ p: 'A', s: 'A', c: '#111827', dx: 12, dy: -4 }, { p: "A'", s: "A'", c: '#111827', dx: 12, dy: 8 }, { p: 'O', s: 'O', c: '#111827', dx: -12, dy: 10 },
        { p: [2.3 * Math.cos(Math.PI / 6), 2.3 * Math.sin(Math.PI / 6), 0], s: '60°', c: RED, dx: -6, dy: 12, bold: false, size: 12 }, { p: [1.25 * Math.cos(1.3), 1.25 * Math.sin(1.3), 0], s: '30°', c: RED, dx: -16, dy: 2, bold: false, size: 12 }])],
    notes: [caption('Hình 5.32 (minh họa): cây cột và bóng trên mặt đất')],
  });
})();
// Hình 5.33: mái nhà tròn trên ba cột 7 m, 6 m, 5 m tại ba đỉnh tam giác đều cạnh 4 m.
out['c5-5-33-mai-nha'] = (() => {
  const A = [0, 0, 0], B = [4, 0, 0], C = [2, 2 * Math.sqrt(3), 0];
  const T = { "A'": [0, 0, 7], "B'": [4, 0, 6], "C'": [2, 2 * Math.sqrt(3), 5] };
  // đường tròn mái: tâm là trọng tâm tam giác A'B'C' (tam giác đều đáy nên cũng là tâm ngoại tiếp), nằm trong mặt phẳng A'B'C'
  const g = mul(add(add(T["A'"], T["B'"]), T["C'"]), 1 / 3);
  const e1 = unit(sub(T["B'"], T["A'"])), nrm = unit(L.cross(sub(T["B'"], T["A'"]), sub(T["C'"], T["A'"]))), e2 = unit(L.cross(nrm, e1));
  const R = len(sub(T["A'"], g)) * 1.18, ring = [];
  for (let i = 0; i < 64; i++) { const t = (i / 64) * 2 * Math.PI; ring.push(add(g, add(mul(e1, R * Math.cos(t)), mul(e2, R * Math.sin(t))))); }
  const col = (a, b) => seg(a, b, '#b4793a', { w: 5, dash: 'solid', occ: false });
  return model({
    view: { az: 30, el: 30 }, size: [380, 330], pts: { A, B, C, ...T },
    items: [{ t: 'poly', pts: ring, fill: '#f4a3a3', op: 0.45, stroke: '#b91c1c', w: 1.6, occ: false },
      { t: 'poly', pts: [A, B, C], fill: '#e2e8f0', op: 0.5, stroke: '#94a3b8', w: 1.2, occ: false },
      col('A', "A'"), col('B', "B'"), col('C', "C'"), ...["A'", "B'", "C'"].map((n) => pt(n, '#0e90d2')),
      ...lbl(['A', 'B', 'C']), ...lbl([{ p: "A'", s: "A'", c: '#111827', dx: 0, dy: -12 }, { p: "B'", s: "B'", c: '#111827', dx: 12, dy: -6 }, { p: "C'", s: "C'", c: '#111827', dx: 12, dy: -4 },
        { p: [0, 0, 3.5], s: '7 m', c: '#475569', dx: -18, dy: 0, bold: false, size: 12 }, { p: [4, 0, 3], s: '6 m', c: '#475569', dx: 18, dy: 0, bold: false, size: 12 }, { p: [2, 2 * Math.sqrt(3), 2.5], s: '5 m', c: '#475569', dx: 18, dy: 0, bold: false, size: 12 }])],
    notes: [caption('Hình 5.33 (minh họa): mái nhà tròn trên ba cột 7 m, 6 m, 5 m')],
  });
})();
// Bài 5.8: hình chóp đều S.ABCD.
out['c5-5-8-chop-deu'] = (() => {
  const a = 2;
  const pts = { A: [-a, -a, 0], B: [a, -a, 0], C: [a, a, 0], D: [-a, a, 0], O: [0, 0, 0], S: [0, 0, 3.4] };
  return model({
    view: { az: 24, el: 24 }, pts, solids: [{ k: 'poly', faces: pyramidFaces(BASE, 'S') }],
    items: [seg('A', 'C', GRAY, { w: 1.2 }), seg('B', 'D', GRAY, { w: 1.2 }), pt('O', '#111827'), ...lbl(['A', 'B', 'C', 'D', 'S']), ...lbl([{ p: 'O', s: 'O', c: '#111827', dx: 10, dy: 12, bold: false }])],
    notes: [caption('Hình chóp đều S.ABCD: đáy ABCD là hình vuông tâm O'), { s: 'Bốn mặt bên là bốn mái nhà', pos: 'bl', c: '#475569', size: 11, bold: false }].slice(0, 1),
  });
})();

// ---- Các hình của bài vectơ / bài tập ----
out['t12-v-hop-chu-nhat-c'] = (() => {
  const pts = { C: [0, 0, 0], B: [3, 0, 0], D: [0, 2.2, 0], A: [3, 2.2, 0], "C'": [0, 0, 2.2], "B'": [3, 0, 2.2], "D'": [0, 2.2, 2.2], "A'": [3, 2.2, 2.2] };
  return model({
    view: { az: 40, el: 24 }, pts, solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }],
    items: [{ t: 'arrow', a: 'C', b: [1.1, 0, 0], c: RED, w: 2.4, occ: false }, { t: 'arrow', a: 'C', b: [0, 1.1, 0], c: RED, w: 2.4, occ: false }, { t: 'arrow', a: 'C', b: [0, 0, 1.1], c: RED, w: 2.4, occ: false },
      ...lbl(BASE.concat(PR)), ...lbl([{ p: [0.6, 0, 0], s: 'i', c: RED, dx: 0, dy: 13, bold: false, size: 14 }, { p: [0, 0.6, 0], s: 'j', c: RED, dx: -12, dy: 6, bold: false, size: 14 }, { p: [0, 0, 0.6], s: 'k', c: RED, dx: -12, dy: 0, bold: false, size: 14 }])],
  });
})();
// Bài 5.2a: A(1; −1; 3), B(0; 2; 4), D(2; −1; 1) -> C = B + D − A = (1; 2; 2).
out['t12-v-hop-c'] = (() => {
  const A = [1, -1, 3], B = [0, 2, 4], D = [2, -1, 1], w = [-2.1, -0.35, -1.05]; // w ⟂ mặt đáy để hình hộp cân đối
  const C = sub(add(B, D), A);
  return model({
    view: { az: 24, el: 24 }, pts: { A, B, C, D, "A'": add(A, w), "B'": add(B, w), "C'": add(C, w), "D'": add(D, w) },
    solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }], items: [...P8.filter((l) => l.p !== 'C'), ...lbl([{ p: 'C', s: 'C (?)', c: RED }]), pt('C', RED)],
  });
})();
// A(1; 0; 2), B(3; 2; 5), C(7; −3; 9), A'(5; 0; 1) -> D = A + C − B, D' = D + AA'.
out['t12-v-hop-d1'] = (() => {
  const A = [1, 0, 2], B = [3, 2, 5], C = [7, -3, 9], Ap = [5, 0, 1], w = sub(Ap, A), D = sub(add(A, C), B);
  return model({
    view: { az: -35, el: 30 }, pts: { A, B, C, D, "A'": Ap, "B'": add(B, w), "C'": add(C, w), "D'": add(D, w) },
    solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }], items: [...P8.filter((l) => l.p !== "D'"), ...lbl([{ p: "D'", s: "D' (?)", c: RED }]), pt("D'", RED)],
  });
})();
out['t12-v-hop-q10'] = (() => {
  const pts = box([0, 0, 0], [3, 0, 0], [0, 3, 0], [0, 0, 3]);
  const O = mul(add(pts.A, pts["C'"]), 0.5), G = mul(add(add(pts.B, pts.D), pts["A'"]), 1 / 3);
  return model({
    view: { az: 24, el: 22 }, pts: { ...pts, O, G }, solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }],
    items: [seg('B', 'D', RED, { w: 1.5 }), seg("A'", 'B', RED, { w: 1.5 }), seg("A'", 'D', RED, { w: 1.5 }), seg('A', "C'", RED, { w: 1.8 }), pt('O', RED), pt('G', RED), ...P8, ...lbl([{ p: 'O', s: 'O', c: RED, dx: 10, dy: -9 }, { p: 'G', s: 'G', c: RED, dx: -11, dy: 9 }])],
  });
})();
out['t12-v-lap-phuong-q28'] = (() => {
  const pts = box([0, 0, 0], [3, 0, 0], [0, 3, 0], [0, 0, 3]);
  const G = mul(add(add(pts.B, pts["C'"]), pts["D'"]), 1 / 3);
  return model({
    view: { az: 24, el: 22 }, pts: { ...pts, G }, solids: [{ k: 'poly', faces: prismFaces(BASE, PR) }],
    items: [seg('B', "C'", RED, { w: 1.5 }), seg('B', "D'", RED, { w: 1.5 }), seg("C'", "D'", RED, { w: 1.5 }), seg('A', 'G', RED, { w: 2 }), pt('G', RED), ...P8,
      ...lbl([{ p: 'G', s: 'G', c: RED, dx: 4, dy: 14 }, { p: mid(pts.A, pts.B), s: 'a', c: RED, dx: 0, dy: 14, bold: false, size: 14 }])],
  });
})();
out['t12-v-m-hinh-chieu'] = (() => {
  const M = [2, -1, 3], Ax = [2, 0, 0], By = [0, -1, 0], Cz = [0, 0, 3];
  const edge = (a, b) => seg(a, b, '#94a3b8', { w: 1.3, dash: 'dash', occ: false });
  const XY = [2, -1, 0], XZ = [2, 0, 3], YZ = [0, -1, 3];
  return model({
    view: OXYZ, size: [380, 320], pts: { M, A: Ax, B: By, C: Cz },
    items: [...axes([3.4, 2.6, 4.2], [0, 0, 0], GRAY),
      { t: 'poly', pts: [Ax, By, Cz], fill: '#f87171', op: 0.3, stroke: RED, w: 1.8, occ: false },
      edge(Ax, XY), edge(By, XY), edge(Ax, XZ), edge(Cz, XZ), edge(By, YZ), edge(Cz, YZ), edge(XY, M), edge(XZ, M), edge(YZ, M),
      pt('M', RED), ...lbl([{ p: 'M', s: 'M', c: RED, dx: -11, dy: -6 }, { p: 'A', s: 'A', c: RED }, { p: 'B', s: 'B', c: RED }, { p: 'C', s: 'C', c: RED }, { p: [0, 0, 0], s: 'O', c: '#111827', dx: 10, dy: 12, bold: false }])],
    notes: [caption('A, B, C là hình chiếu của M trên Ox, Oy, Oz')],
  });
})();
out['t12-v-mat-cau-ab'] = (() => {
  const R = 2.4, u = unit([0.7, -0.45, -0.55]);
  const A = mul(u, -R), B = mul(u, R);
  return model({
    view: { az: 24, el: 20 }, size: [380, 320], pts: { A, B, I: [0, 0, 0] },
    solids: [{ k: 'sphere', c: 'I', r: R, fill: '#e8f0fb' }],
    items: [{ t: 'circ', o: 'I', n: [0, 0, 1], r: R, c: '#94a3b8', w: 1.3 }, seg('A', 'B', RED, { w: 2.2, dash: 'solid', occ: false }), pt('A', RED), pt('B', RED), pt('I', RED),
      ...lbl([{ p: 'A', s: 'A', c: '#111827', dx: -10, dy: -8 }, { p: 'B', s: 'B', c: '#111827', dx: 10, dy: 8 }, { p: 'I', s: 'I', c: RED, dx: 4, dy: -13 }])],
    notes: [caption('mặt cầu đường kính AB, tâm I là trung điểm AB')],
  });
})();
out['t12-v-chop-oxyz'] = (() => {
  const pts = { A: [0, 0, 0], B: [3, 0, 0], C: [3, 4, 0], D: [0, 4, 0], S: [0, 0, 2] };
  return model({
    view: OXYZ, size: [380, 320], pts, solids: [{ k: 'poly', faces: pyramidFaces(BASE, 'S') }],
    items: [...axes([4.4, 5.4, 3.2], [0, 0, 0], BLUE), { t: 'ra', at: 'A', u: [1, 0, 0], v: [0, 0, 1], s: 0.35, c: RED }, { t: 'ra', at: 'A', u: [0, 1, 0], v: [0, 0, 1], s: 0.35, c: RED },
      ...lbl(['A', 'B', 'C', 'D', 'S']), ...lbl([{ p: [1.5, 0, 0], s: '3', c: RED, dx: 0, dy: 15, size: 14 }, { p: [0, 2, 0], s: '4', c: RED, dx: -14, dy: 6, size: 14 }, { p: [0, 0, 1], s: '2', c: RED, dx: -14, dy: 0, size: 14 }])],
  });
})();
// Bể: dây dọi 4 m, 4,4 m, 4,8 m trên tam giác đều cạnh 2 m.
out['t12-v-be-day-doi'] = (() => {
  const A = [0, 0, 0], B = [2, 0, 0], C = [1, Math.sqrt(3), 0];
  const Ta = [0, 0, 4], Tb = [2, 0, 4.4], Tc = [1, Math.sqrt(3), 4.8];
  return model({
    view: { az: 34, el: 36 }, size: [380, 360], fit: 0.8, pts: { A, B, C, Ta, Tb, Tc },
    items: [{ t: 'poly', pts: [A, B, C], fill: '#e2e8f0', op: 0.6, stroke: '#111827', w: 1.8, occ: false }, { t: 'poly', pts: [Ta, Tb, Tc], fill: '#60a5fa', op: 0.4, stroke: '#2563eb', w: 1.6, occ: false },
      seg('A', 'Ta', RED, { w: 1.8, occ: false }), seg('B', 'Tb', RED, { w: 1.8, occ: false }), seg('C', 'Tc', RED, { w: 1.8, occ: false }), pt('A', '#111827'), pt('B', '#111827'), pt('C', '#111827'),
      ...lbl([{ p: 'A', s: 'A', c: '#111827', dx: -10, dy: 10 }, { p: 'B', s: 'B', c: '#111827', dx: 10, dy: 10 }, { p: 'C', s: 'C', c: '#111827', dx: 4, dy: -12 },
        { p: [0, 0, 2], s: '4 m', c: RED, dx: -20, dy: 0, size: 13 }, { p: [2, 0, 2.2], s: '4,4 m', c: RED, dx: 24, dy: 0, size: 13 }, { p: [1, Math.sqrt(3), 2.4], s: '4,8 m', c: RED, dx: 24, dy: 0, size: 13 },
        { p: mid(A, B), s: '2 m', c: RED, dx: 0, dy: 13, size: 13 }])],
    notes: [caption('mặt nước (phẳng); dây dọi tại A, B, C')],
  });
})();
// Bể 5.24a: A, B, C cách đáy 40, 44, 48 cm; D = A + C − B = 44 cm.
out['t12-v-be-nuoc'] = (() => {
  const W = 10, Dp = 7, Hh = 6.2; // đơn vị 10 cm
  const base = { A0: [0, 0, 0], B0: [W, 0, 0], C0: [W, Dp, 0], D0: [0, Dp, 0], A1: [0, 0, Hh], B1: [W, 0, Hh], C1: [W, Dp, Hh], D1: [0, Dp, Hh] };
  const wa = { WA: [0, 0, 4], WB: [W, 0, 4.4], WC: [W, Dp, 4.8], WD: [0, Dp, 4.4] };
  return model({
    view: { az: 24, el: 22 }, size: [380, 320], pts: { ...base, ...wa },
    solids: [{ k: 'poly', faces: prismFaces(['A0', 'B0', 'C0', 'D0'], ['A1', 'B1', 'C1', 'D1']) }],
    items: [{ t: 'poly', pts: ['WA', 'WB', 'WC', 'WD'], fill: '#38bdf8', op: 0.5, stroke: '#0284c7', w: 1.8, occ: false },
      seg('A0', 'WA', RED, { w: 1.5, occ: false }), seg('B0', 'WB', RED, { w: 1.5, occ: false }), seg('C0', 'WC', RED, { w: 1.5, occ: false }), seg('D0', 'WD', RED, { w: 1.5, dash: 'dash', occ: false }),
      ...lbl([{ p: 'WA', s: 'A', c: '#0369a1', dx: -12, dy: 2 }, { p: 'WB', s: 'B', c: '#0369a1', dx: 12, dy: 6 }, { p: 'WC', s: 'C', c: '#0369a1', dx: 12, dy: -6 }, { p: 'WD', s: 'D', c: '#0369a1', dx: -10, dy: -8 },
        { p: [0, 0, 2], s: '40', c: RED, dx: -14, dy: 0, size: 13 }, { p: [W, 0, 2.2], s: '44', c: RED, dx: 14, dy: 0, size: 13 }, { p: [W, Dp, 2.4], s: '48', c: RED, dx: 14, dy: 0, size: 13 }, { p: [0, Dp, 2.2], s: '?', c: RED, dx: -10, dy: 0, size: 14 }])],
    notes: [caption('mặt nước ABCD; khoảng cách đến đáy (cm)')],
  });
})();

// ---- Thể tích khối đa diện / khối tròn xoay ----
out['t12-c4-chop-deu'] = (() => {
  const L2 = 2.2;
  const pts = { A: [-L2, -L2, 0], B: [L2, -L2, 0], C: [L2, L2, 0], D: [-L2, L2, 0], O: [0, 0, 0], S: [0, 0, 3.6] };
  return model({
    view: { az: 24, el: 24 }, pts, solids: [{ k: 'poly', faces: pyramidFaces(BASE, 'S') }],
    items: [seg('S', 'O', RED, { w: 2.2 }), pt('O', RED), { t: 'ra', at: 'O', u: [1, 0, 0], v: [0, 0, 1], s: 0.35, c: RED }, ...lbl(['A', 'B', 'C', 'D', 'S']),
      ...lbl([{ p: [0, 0, 1.8], s: 'h', c: RED, dx: 12, dy: 0, size: 16 }, { p: mid(pts.A, pts.B), s: 'L', c: RED, dx: 0, dy: 16, size: 16 }, { p: 'O', s: 'O', c: RED, dx: 10, dy: 11 }])],
  });
})();
out['t12-c4-lang-tru'] = (() => {
  const pts = { A: [0, 0, 0], B: [4, 0, 0], C: [1.5, 2.4, 0], "A'": [0, 0, 3.4], "B'": [4, 0, 3.4], "C'": [1.5, 2.4, 3.4] };
  const cen = (a, b, c) => mul(add(add(a, b), c), 1 / 3);
  return model({
    view: { az: 22, el: 22 }, pts, solids: [{ k: 'poly', faces: prismFaces(['A', 'B', 'C'], ["A'", "B'", "C'"]) }],
    items: [...lbl(['A', 'B', 'C', "A'", "B'", "C'"]), seg([5.1, 0, 0], [5.1, 0, 3.4], RED, { w: 1.8, occ: false }), seg([4.9, 0, 0], [5.3, 0, 0], RED, { w: 1.4, occ: false }), seg([4.9, 0, 3.4], [5.3, 0, 3.4], RED, { w: 1.4, occ: false }),
      ...lbl([{ p: [5.1, 0, 1.7], s: 'h', c: RED, dx: 14, dy: 0, size: 16 }, { p: cen(pts.A, pts.B, pts.C), s: 'S', c: RED, dx: 14, dy: 6, size: 16 }, { p: cen(pts["A'"], pts["B'"], pts["C'"]), s: 'S', c: RED, dx: 0, dy: 0, size: 16 }])],
  });
})();
out['t12-b5-hop-tru'] = (() => {
  const r = 1.5, h = 3;
  return model({
    view: { az: 20, el: 24 }, size: [380, 320], pts: { O: [0, 0, 0], T: [0, 0, h] },
    solids: [{ k: 'axi', o: 'O', e: [0, 0, 1], prof: [[0, r], [h, r]], fill: '#eef5fb' }],
    items: [seg('T', [r, 0, h], RED, { w: 2, dash: 'solid', occ: false }), pt('T', RED),
      seg([r + 0.9, 0, 0], [r + 0.9, 0, h], RED, { w: 1.8, occ: false }), seg([r + 0.75, 0, 0], [r + 1.05, 0, 0], RED, { w: 1.4, occ: false }), seg([r + 0.75, 0, h], [r + 1.05, 0, h], RED, { w: 1.4, occ: false }),
      ...lbl([{ p: [r / 2, 0, h], s: 'r', c: RED, dx: 0, dy: -12, size: 16 }, { p: [r + 0.9, 0, h / 2], s: 'h', c: RED, dx: 14, dy: 0, size: 16 }])],
    notes: [{ s: 'V = 1000 cm³', pos: 'bc', c: '#1d2733', size: 14, bold: true }],
  });
})();

module.exports = out;
