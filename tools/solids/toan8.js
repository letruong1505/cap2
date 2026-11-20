// Hình không gian Toán 8: hình chóp tam giác đều, tứ giác đều (đúng tỉ lệ theo số liệu của bài) và hình hộp có đường chéo.
const L = require('./lib');
const { mid, RED, BLUE, lbl, seg, pt, cap, boxFig, model, pyramidFaces } = L;
const out = {};
const NOTE = '#e15759', HC = '#c2410c';

// n = 3 (đáy tam giác đều, M là trung điểm BC, H là tâm đáy) hoặc 4 (đáy hình vuông, M là trung điểm CD, O là tâm đáy).
// a: cạnh đáy, h: chiều cao (cùng đơn vị); show: nhãn nào hiện (h, d).
function pyramid(n, a, h, { showH = false, showD = false, notes = [], centerName = n === 3 ? 'H' : 'O' } = {}) {
  const k = 4.6 / Math.max(a * 1.3, h), A_ = a * k, H_ = h * k;
  const pts = n === 3
    ? { A: [0, A_ / Math.sqrt(3), 0], B: [-A_ / 2, -A_ / (2 * Math.sqrt(3)), 0], C: [A_ / 2, -A_ / (2 * Math.sqrt(3)), 0] }
    : { A: [-A_ / 2, A_ / 2, 0], B: [A_ / 2, A_ / 2, 0], C: [A_ / 2, -A_ / 2, 0], D: [-A_ / 2, -A_ / 2, 0] };
  pts[centerName] = [0, 0, 0];
  pts.S = [0, 0, H_];
  pts.M = n === 3 ? mid(pts.B, pts.C) : mid(pts.C, pts.D);
  const base = n === 3 ? ['A', 'B', 'C'] : ['A', 'B', 'C', 'D'];
  const items = [seg('S', 'M', BLUE, { w: 2 }), seg('S', centerName, '#1d2733', { w: 1.7 }), pt(centerName, '#1d2733'), pt('M', BLUE),
    { t: 'ra', at: centerName, u: [pts.M[0], pts.M[1], 0], v: [0, 0, 1], s: 0.3, c: '#475569' },
    ...lbl([...base, 'S']), ...lbl([{ p: centerName, s: centerName, c: '#1d2733', dx: -9, dy: 11, size: 14 }, { p: 'M', s: 'M', c: BLUE, dx: 10, dy: 10, size: 14 }])];
  if (showH) items.push(...lbl([{ p: mid(pts.S, pts[centerName]), s: 'h', c: HC, dx: -13, dy: 0, size: 15, bold: false }]));
  if (showD) items.push(...lbl([{ p: mid(pts.S, pts.M), s: 'd', c: BLUE, dx: 12, dy: -2, size: 15, bold: false }]));
  const m = model({ view: { az: 26, el: 30 }, fit: 0.84 - 0.05 * notes.length, pts, solids: [{ k: 'poly', faces: pyramidFaces(base, 'S'), fill: '#eef5fb' }], items,
    notes: notes.length ? [{ s: notes.join('\n'), pos: 'tl', c: NOTE, size: 13, bold: true }] : [] });
  if (notes.length) m.dy = 8 * notes.length;
  return m;
}
const triA = (S) => Math.sqrt((4 * S) / Math.sqrt(3));            // cạnh đáy từ diện tích đáy (tam giác đều)
const triR = (a) => a / (2 * Math.sqrt(3));                       // khoảng cách từ tâm đến cạnh
const hOf = (d, r) => Math.sqrt(d * d - r * r);
const T = (name, a, h, show, notes) => { out[name] = pyramid(3, a, h, { ...show, notes }); };
const Q = (name, a, h, show, notes) => { out[name] = pyramid(4, a, h, { ...show, notes }); };
const hd = { showH: true, showD: true }, d = { showD: true }, h = { showH: true }, none = {};

// ---- Bài 38: hình chóp tam giác đều ----
T('bt-toan8-b38-q05', 8, hOf(7, triR(8)), d, ['cạnh đáy a = 8 cm', 'trung đoạn d = 7 cm']);
T('bt-toan8-b38-q06', 8, hOf(5, triR(8)), d, ['cạnh đáy a = ?', 'trung đoạn d = 5 cm', 'Sxq = 60 cm²']);
{ const a = triA(15), dd = 45 / (1.5 * a); T('bt-toan8-b38-q07', a, hOf(dd, triR(a)), none, ['Sxq = 45 cm²', 'S đáy = 15 cm²', 'Stp = ?']); }
T('bt-toan8-b38-q08', triA(12), 9, h, ['chiều cao h = 9 cm', 'S đáy = 12 cm²']);
T('bt-toan8-b38-q09', triA(30), 7, h, ['chiều cao h = 7 cm', 'S đáy = 30 cm²']);
T('bt-toan8-b38-q10', triA(9), 12, h, ['chiều cao h = ?', 'V = 36 cm³', 'S đáy = 9 cm²']);
T('nc-toan8-b38-n01', 10, hOf(6, triR(10)), d, ['trung đoạn d = 6 cm', 'Sxq = 90 cm²', 'chu vi đáy = ?']);
T('nc-toan8-b38-n02', triA(20), 6, h, ['chiều cao h = 6 cm', 'V = 40 cm³', 'S đáy = ?']);
T('vd-toan8-b38-1', 6, hOf(5, triR(6)), d, ['cạnh đáy a = 6 cm', 'trung đoạn d = 5 cm']);
T('vd-toan8-b38-2', triA(15), 6, h, ['chiều cao h = 6 cm', 'S đáy = 15 cm²']);
T('lt-hinh-chop-tam-giac-deu', 6, 5, hd, []);

// ---- Bài 39: hình chóp tứ giác đều ----
Q('bt-toan8-b39-q05', 10, 12, d, ['cạnh đáy a = 10 cm', 'trung đoạn d = 13 cm']);
Q('bt-toan8-b39-q06', 3, 8, h, ['cạnh đáy a = 3 cm', 'chiều cao h = 8 cm']);
Q('bt-toan8-b39-q07', 6, 5, h, ['cạnh đáy a = 6 cm', 'chiều cao h = 5 cm']);
Q('bt-toan8-b39-q08', 4, hOf(5, 2), d, ['cạnh đáy a = 4 cm', 'trung đoạn d = 5 cm', 'Stp = ?']);
Q('bt-toan8-b39-q09', 10, 12, hd, ['cạnh đáy a = 10 cm', 'trung đoạn d = 13 cm', 'chiều cao h = ?']);
Q('bt-toan8-b39-q10', 6, 4, h, ['chiều cao h = 4 cm', 'V = 48 cm³', 'S đáy = ?']);
Q('nc-toan8-b39-n01', 10, hOf(12, 5), d, ['cạnh đáy a = 10 cm', 'trung đoạn d = ?', 'Sxq = 240 cm²']);
Q('nc-toan8-b39-n02', 10, hOf(Math.sqrt(169 - 25), 5), none, ['cạnh đáy a = 10 cm', 'Cạnh bên SA = 13 cm', 'Sxq = ?']);
Q('vd-toan8-b39-1', 6, 4, d, ['cạnh đáy a = 6 cm', 'trung đoạn d = 5 cm']);
Q('vd-toan8-b39-2', 6, 4, h, ['cạnh đáy a = 6 cm', 'chiều cao h = 4 cm']);
Q('lt-hinh-chop-tu-giac-deu', 6, 4, hd, []);

// ---- Hình hộp chữ nhật 12 × 4 × 3 với đường chéo (màu đỏ) ----
out['nc-toan8-b35-n02'] = boxFig({
  dims: [12, 4, 3], labels: ['12 cm', '4 cm', '3 cm'], caption: 'Đường chéo của hình hộp (màu đỏ) = ?', names: true,
  extra: [seg('A', "C'", NOTE, { w: 2.6, dash: 'solid', occ: false })],
});
module.exports = out;
