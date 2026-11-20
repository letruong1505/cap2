// Tiện ích dựng mô hình 3D cho hình không gian (dùng chung cho mọi môn).
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const mid = (a, b) => mul(add(a, b), 0.5);
const lerp = (a, b, t) => add(a, mul(sub(b, a), t));
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const len = (a) => Math.hypot(a[0], a[1], a[2]);
const unit = (a) => mul(a, 1 / len(a));
const r3 = (a) => a.map((x) => Math.round(x * 1e4) / 1e4);

const RED = '#b91c1c', BLUE = '#1d4ed8', GREEN = '#047857', PURPLE = '#7c3aed', ORANGE = '#c2410c', GRAY = '#64748b';

// Mặt của khối chóp (đáy là danh sách tên đỉnh, apex là tên đỉnh chóp).
function pyramidFaces(base, apex) {
  const f = [base.slice()];
  for (let i = 0; i < base.length; i++) f.push([base[i], base[(i + 1) % base.length], apex]);
  return f;
}
// Mặt của lăng trụ/hình hộp: đáy dưới, đáy trên (cùng thứ tự), các mặt bên.
function prismFaces(bot, top) {
  const f = [bot.slice(), top.slice()];
  for (let i = 0; i < bot.length; i++) { const j = (i + 1) % bot.length; f.push([bot[i], bot[j], top[j], top[i]]); }
  return f;
}
// Đa diện lồi bất kỳ từ các điểm theo tên: tạo mặt tứ diện.
const tetraFaces = (a, b, c, d) => [[a, b, c], [a, b, d], [a, c, d], [b, c, d]];

const lbl = (names, extra = {}) => names.map((n) => (typeof n === 'string' ? { t: 'lbl', p: n, s: n, ...extra } : { t: 'lbl', ...extra, ...n }));
const seg = (a, b, c, extra = {}) => ({ t: 'seg', a, b, c, ...extra });
const pt = (p, c, r) => ({ t: 'pt', p, c, r });
const dots = (names, c) => names.map((n) => ({ t: 'pt', p: n, c }));

// Hệ trục Oxyz: mũi tên + nhãn, không bị khối che.
function axes(L = [4, 4, 4], o = [0, 0, 0], c = GRAY, names = ['x', 'y', 'z']) {
  const dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
  const out = [];
  dirs.forEach((d, i) => {
    const e = add(o, mul(d, L[i]));
    out.push({ t: 'arrow', a: o, b: e, c, w: 1.5, occ: false });
    out.push({ t: 'lbl', p: add(o, mul(d, L[i] + 0.35)), s: names[i], c: '#334155', dx: 0, dy: 0, bold: false, size: 14 });
  });
  return out;
}
const caption = (s) => ({ s, pos: 'bc', c: '#475569', size: 12, bold: false });

function model(o) {
  return { v: 1, size: o.size || [380, 300], view: o.view || { az: 28, el: 22 }, fit: o.fit, pts: o.pts || {}, solids: o.solids || [], items: o.items || [], notes: o.notes || [] };
}
module.exports = { add, sub, mul, mid, lerp, cross, dot, len, unit, r3, RED, BLUE, GREEN, PURPLE, ORANGE, GRAY, pyramidFaces, prismFaces, tetraFaces, lbl, seg, pt, dots, axes, caption, model };

// ---- Hình mẫu dùng chung (hộp, lăng trụ đứng) ----
const DIM = '#e15759';
const cap = (s) => ({ s, pos: 'bc', c: DIM, size: 13, bold: true });
const dimLbl = (p, s, extra = {}) => ({ t: 'lbl', p, s, c: DIM, size: 13, ...extra });

// Hình hộp chữ nhật w × d × h. labels = [chiều rộng, chiều sâu, chiều cao] (chuỗi hoặc null); đỉnh có tên nếu names = true.
function boxFig({ dims, labels = [], caption, names = false, extra = [], notes = [], view, size, S }) {
  const [w, d, h] = dims;
  const k = 4 / Math.max(w, d, h), W = w * k, D = d * k, H = h * k;
  const pts = { A: [0, 0, 0], B: [W, 0, 0], C: [W, D, 0], D: [0, D, 0], "A'": [0, 0, H], "B'": [W, 0, H], "C'": [W, D, H], "D'": [0, D, H] };
  const items = [];
  if (labels[0]) items.push(dimLbl(mid(pts.A, pts.B), labels[0]));
  if (labels[1]) items.push(dimLbl(mid(pts.B, pts.C), labels[1]));
  if (labels[2]) items.push(dimLbl(mid(pts.A, pts["A'"]), labels[2]));
  if (names) items.push(...lbl(['A', 'B', 'C', 'D', "A'", "B'", "C'", "D'"]));
  return model({ view: view || { az: 24, el: 22 }, size, pts, solids: [{ k: 'poly', faces: prismFaces(['A', 'B', 'C', 'D'], ["A'", "B'", "C'", "D'"]) }], items: [...items, ...extra], notes: [...(caption ? [cap(caption)] : []), ...notes] });
}
// Lăng trụ đứng với đáy là đa giác phẳng (mảng [x, y]) và chiều cao h.
function prismFig({ base, h, names, labels = {}, caption, extra = [], view, size, solidNames }) {
  const n = base.length;
  const nm = names || ['A', 'B', 'C', 'D', 'E'].slice(0, n);
  const pts = {}, bot = [], top = [];
  base.forEach((p, i) => { pts[nm[i]] = [p[0], p[1], 0]; pts[nm[i] + "'"] = [p[0], p[1], h]; bot.push(nm[i]); top.push(nm[i] + "'"); });
  const items = [...extra];
  return { pts, bot, top, items, build: (more = []) => model({ view: view || { az: 22, el: 22 }, size, pts, solids: [{ k: 'poly', faces: prismFaces(bot, top) }], items: [...items, ...more], notes: caption ? [cap(caption)] : [] }) };
}
Object.assign(module.exports, { DIM, cap, dimLbl, boxFig, prismFig });
