// Hình không gian Toán 7: hình hộp chữ nhật, hình lập phương, lăng trụ đứng (mô hình 3D theo đúng kích thước đề cho).
const L = require('./lib');
const { mid, dimLbl, boxFig, prismFig, lbl, cap, model, prismFaces } = L;
const out = {};

const box = (name, dims, labels, caption, extra = {}) => { out[name] = boxFig({ dims, labels, caption, ...extra }); };
const NO = [];
box('bt-t7-b36-q01', [4, 3, 3], NO, 'Hình hộp chữ nhật: có bao nhiêu cạnh?');
box('bt-t7-b36-q05', [3, 3, 3], ['3 cm', '3 cm', '3 cm'], 'Hình lập phương cạnh 3 cm: S toàn phần = ?');
box('bt-t7-b36-q08', [3, 3, 3], ['? cm', '? cm', '? cm'], 'Hình lập phương có V = 27 cm³: cạnh = ?');
box('nc-t7-b36-n01', [6, 4, 3], ['6 cm', '4 cm', '3 cm'], 'Hình hộp 6 × 4 × 3 cm: S toàn phần = ?');
box('nc-t7-b36-n02', [3, 3, 3], NO, 'Hình lập phương có Stp = 150 cm²: V = ?');
box('bt-t7-b37-q05', [2, 2, 6], ['2 cm', '2 cm', '6 cm'], 'Đáy hình vuông cạnh 2 cm, cao 6 cm: V = ?');
box('bt-t7-b37-q06', [4, 5, 3], ['4 cm', '5 cm', '3 cm'], 'Đáy chữ nhật 4 cm × 5 cm, cao 3 cm: V = ?');
box('bt-t7-b37-q08', [3, 3, 5], ['3 cm', '3 cm', '5 cm'], 'Đáy hình vuông cạnh 3 cm, cao 5 cm: S xung quanh = ?');
// Đáy 4 × 3 có diện tích 12 cm².
const baseArea = (name, hLabel, caption) => {
  const f = boxFig({ dims: [4, 3, 5], labels: [null, null, hLabel], caption });
  f.items.push({ t: 'lbl', p: [2, 1.5, 0], s: 'S đáy = 12 cm²', c: L.DIM, size: 12, dx: 0, dy: 0 });
  out[name] = f;
};
baseArea('bt-t7-b37-q04', 'h = 5 cm', 'Thể tích = ?');
baseArea('nc-t7-b37-n02', 'h = ?', 'Thể tích 84 cm³: chiều cao = ?');
// Lăng trụ đứng tứ giác tổng quát (đáy là tứ giác bất kỳ).
const quad = (name, caption) => {
  const f = prismFig({ base: [[0, 0], [4.2, 0], [5.2, 2.6], [0.8, 2.4]], h: 3.4 });
  out[name] = f.build();
  out[name].notes = [cap(caption)];
};
quad('bt-t7-b37-q02', 'Lăng trụ đứng tứ giác: có bao nhiêu cạnh bên?');
quad('bt-t7-b37-q03', 'Lăng trụ đứng tứ giác: có bao nhiêu đỉnh?');

// Lăng trụ đứng đáy tam giác: AB, AC, BC (BC là cạnh trước), chiều cao h; scale để hình cân đối.
function triPrism({ ab, ac, bc, h, scale, sideLabels, hLabel, caption, names = true }) {
  const x = (ab * ab - ac * ac + bc * bc) / (2 * bc), y = Math.sqrt(Math.max(ab * ab - x * x, 0.01));
  // đáy theo thứ tự B, C, A để cạnh BC ở phía trước
  const B = [0, 0, 0], C = [bc * scale, 0, 0], A = [x * scale, y * scale, 0], H = h * scale, up = (p) => [p[0], p[1], H];
  const pts = { A, B, C, "A′": up(A), "B′": up(B), "C′": up(C) };
  const items = [];
  if (names) items.push(...lbl(['A', 'B', 'C', 'A′', 'B′', 'C′']));
  if (sideLabels) {
    items.push(dimLbl(mid(pts["A′"], pts["B′"]), sideLabels[0]), dimLbl(mid(pts["A′"], pts["C′"]), sideLabels[1]), dimLbl(mid(pts["B′"], pts["C′"]), sideLabels[2]));
  }
  if (hLabel) items.push(dimLbl(mid(pts.B, pts["B′"]), hLabel));
  return model({ view: { az: 22, el: sideLabels ? 32 : 22 }, pts, solids: [{ k: 'poly', faces: prismFaces(['B', 'C', 'A'], ["B′", "C′", "A′"]) }], items, notes: caption ? [cap(caption)] : [] });
}
out['t2-lang-tru-tam-giac'] = triPrism({ ab: 3.2, ac: 3.6, bc: 4, h: 3.6, scale: 1 });
out['t2-lt-lang-tru'] = triPrism({ ab: 3.2, ac: 3.6, bc: 4, h: 3.6, scale: 1, hLabel: 'h' });
out['t2-lang-tru-6-8-10'] = triPrism({ ab: 6, ac: 8, bc: 10, h: 10, scale: 0.4, sideLabels: ['6', '8', '10'], hLabel: 'h = 10' });
out['t2-vd-lang-tru-3-4-5-h7'] = triPrism({ ab: 3, ac: 4, bc: 5, h: 7, scale: 0.7, sideLabels: ['3', '4', '5'], hLabel: 'h = 7' });
out['t2-vd-lang-tru-3-4'] = triPrism({ ab: 3, ac: 4, bc: 5, h: 10, scale: 0.5, sideLabels: ['3', '4', '5'], hLabel: 'h = 10' });
out['nc-t7-b37-n01'] = triPrism({ ab: 3, ac: 4, bc: 5, h: 10, scale: 0.8, sideLabels: ['3 cm', '4 cm', '5 cm'], hLabel: 'h = 10 cm', caption: 'Đáy 3-4-5 cm, cao 10 cm: Sxq = ?', names: false });

// Hộp / lập phương dùng trong lý thuyết (nhãn chữ đen).
const plain = (name, dims, labels, size) => { const f = boxFig({ dims, labels }); f.items.forEach((it) => { if (it.t === 'lbl') it.c = '#1d2733'; }); out[name] = f; };
plain('t2-be-nuoc', [2, 1.5, 1], ['2 m', '1,5 m', '1 m']);
plain('t2-hop-2-3-4', [2, 3, 4], ['2 cm', '3 cm', '4 cm']);
plain('t2-hop-5-3-4', [5, 3, 4], ['5 cm', '3 cm', '4 cm']);
plain('t2-vd-hop-3-4-5', [3, 4, 5], ['3 cm', '4 cm', '5 cm']);
plain('t2-lap-phuong-5', [5, 5, 5], ['5 cm', '5 cm', '5 cm']);
plain('t2-vd-lap-phuong-2', [2, 2, 2], ['2 cm', '2 cm', '2 cm']);
plain('t2-lap-phuong-a', [1, 1, 1], ['a', 'a', 'a']);
plain('t2-lt-hinh-hop', [3, 2.2, 2.6], ['a', 'b', 'c']);

module.exports = out;
