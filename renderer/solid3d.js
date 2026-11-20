// Hình không gian xoay được 360°: mô hình 3D (đỉnh, mặt, đường phụ, nhãn) -> hình chiếu vuông góc có nét khuất tự cập nhật.
// Dùng chung cho giao diện (mount), bộ sinh hình tĩnh (toSVG) và kiểm thử. Không phụ thuộc thư viện ngoài.
//
// Mô hình (JSON):
//  { v:1, size:[380,300], view:{az,el}, fit:0.84,
//    pts:{A:[x,y,z],...},                       // điểm có tên (trục z hướng lên)
//    solids:[ {k:'poly', faces:[['A','B','C'],...], edges?:[['A','B'],...], fill?} // khối đa diện lồi
//           | {k:'axi', o:[..], e:[..], prof:[[t,r],...]}  // khối tròn xoay lồi quanh trục (trụ, nón, tròn xoay)
//           | {k:'sphere', c:[..], r} ],
//    items:[ {t:'seg',a,b,c,w,dash}, {t:'poly',pts,fill,op,stroke}, {t:'pt',p,c,r}, {t:'lbl',p,s,dx,dy,c,size},
//            {t:'ra',at,u,v,s,c}, {t:'arc',o,u,v,r,c}, {t:'circ',o,n,r,c,w,dash}, {t:'arrow',a,b,c,w},
//            {t:'curve',pts:[...],c,w,dash} ],
//    notes:[ {s,pos:'tl'|'tr'|'bl'|'bc'|'bcc',c,size,bold} ] }
// Tọa độ trong "pts"/"items" có thể là tên điểm (chuỗi) hoặc mảng [x,y,z].
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.NL_SOLID3D = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  const D2R = Math.PI / 180;
  const INK = '#1d2733';
  const MUTED = '#5b6775';
  const FILL = '#eaf2fb';
  const MARK = 'nl-solid3d';

  // ---------- vectơ ----------
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const len = (a) => Math.sqrt(dot(a, a));
  const unit = (a) => { const l = len(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];

  // Hệ tọa độ màn hình: r (sang phải), u (lên), v (hướng về phía người xem). z thế giới hướng lên.
  function basis(az, el) {
    const a = az * D2R, e = el * D2R;
    const r = [Math.cos(a), Math.sin(a), 0];
    const u = [-Math.sin(e) * Math.sin(a), Math.sin(e) * Math.cos(a), Math.cos(e)];
    const v = [Math.sin(a) * Math.cos(e), -Math.cos(a) * Math.cos(e), Math.sin(e)];
    return { r, u, v };
  }

  // Hai vectơ đơn vị vuông góc với e.
  function perp(e) {
    const t = Math.abs(e[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0];
    const p1 = unit(cross(e, t));
    return [p1, cross(e, p1)];
  }

  // ---------- chuẩn bị mô hình ----------
  function prepare(model) {
    const P = {};
    Object.keys(model.pts || {}).forEach((k) => { P[k] = model.pts[k].slice(); });
    const pt = (ref) => {
      if (Array.isArray(ref)) return ref;
      if (!P[ref]) throw new Error('Thiếu điểm ' + ref);
      return P[ref];
    };
    const solids = (model.solids || []).map((s) => makeSolid(s, pt));
    const ext = [];
    Object.keys(P).forEach((k) => ext.push(P[k]));
    solids.forEach((s) => s.extent().forEach((p) => ext.push(p)));
    (model.items || []).forEach((it) => itemExtent(it, pt).forEach((p) => ext.push(p)));
    const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
    ext.forEach((p) => { for (let i = 0; i < 3; i++) { lo[i] = Math.min(lo[i], p[i]); hi[i] = Math.max(hi[i], p[i]); } });
    if (!isFinite(lo[0])) { lo.fill(0); hi.fill(1); }
    const center = mul(add(lo, hi), 0.5);
    let rad = 0;
    ext.forEach((p) => { rad = Math.max(rad, len(sub(p, center))); });
    if (!rad) rad = 1;
    return { model, P, pt, solids, center, rad };
  }

  function itemExtent(it, pt) {
    const out = [];
    if (it.t === 'seg' || it.t === 'arrow') { out.push(pt(it.a), pt(it.b)); }
    else if (it.t === 'poly' || it.t === 'curve') it.pts.forEach((p) => out.push(pt(p)));
    else if (it.t === 'circ') out.push(...circlePoints(pt(it.o), unit(pt(it.n)), it.r, 12));
    else if (it.t === 'pt' || it.t === 'lbl') { if (it.p !== undefined && !it.free) out.push(pt(it.p)); }
    return out;
  }

  function circlePoints(c, n, r, count) {
    const [p1, p2] = perp(n);
    const out = [];
    for (let i = 0; i < count; i++) {
      const th = (2 * Math.PI * i) / count;
      out.push(add(c, add(mul(p1, r * Math.cos(th)), mul(p2, r * Math.sin(th)))));
    }
    return out;
  }

  // ---------- khối chắn (khối lồi, F(p) <= 0 là bên trong) ----------
  function makeSolid(s, pt) {
    if (s.k === 'poly') return makePoly(s, pt);
    if (s.k === 'axi') return makeAxi(s, pt);
    if (s.k === 'sphere') return makeSphere(s, pt);
    throw new Error('Khối không hỗ trợ: ' + s.k);
  }

  function makePoly(s, pt) {
    const faces = s.faces.map((f) => f.map((n) => pt(n)));
    const all = [];
    faces.forEach((f) => f.forEach((p) => all.push(p)));
    const cen = mul(all.reduce((a, p) => add(a, p), [0, 0, 0]), 1 / all.length);
    const planes = [];
    faces.forEach((f) => {
      // Pháp tuyến Newell, hướng ra ngoài.
      let n = [0, 0, 0];
      for (let i = 0; i < f.length; i++) n = add(n, cross(f[i], f[(i + 1) % f.length]));
      n = unit(n);
      if (dot(n, sub(f[0], cen)) < 0) n = mul(n, -1);
      planes.push({ n, h: dot(n, f[0]) });
    });
    // Cạnh: mặc định là cạnh của các mặt (khử trùng).
    let edges = s.edges;
    if (!edges) {
      const seen = new Set(); edges = [];
      s.faces.forEach((f) => f.forEach((n, i) => {
        const m = f[(i + 1) % f.length];
        const key = n < m ? n + '|' + m : m + '|' + n;
        if (!seen.has(key)) { seen.add(key); edges.push([n, m]); }
      }));
    }
    return {
      kind: 'poly', def: s, planes, edges, cen,
      F(p) { let m = -Infinity; for (let i = 0; i < planes.length; i++) { const x = dot(planes[i].n, p) - planes[i].h; if (x > m) m = x; } return m; },
      extent() { return all; },
      hullPoints() { return all; },
    };
  }

  function makeSphere(s, pt) {
    const c = pt(s.c), r = s.r;
    return {
      kind: 'sphere', def: s, c, r,
      F(p) { return len(sub(p, c)) - r; },
      extent() { return [add(c, [r, 0, 0]), add(c, [-r, 0, 0]), add(c, [0, r, 0]), add(c, [0, -r, 0]), add(c, [0, 0, r]), add(c, [0, 0, -r])]; },
      hullPoints() { return []; },
    };
  }

  // Khối tròn xoay: trục qua o hướng e, bán kính tại t là f(t) (hàm lõm theo t, t0 <= t <= t1).
  function makeAxi(s, pt) {
    const o = pt(s.o), e = unit(s.e), prof = s.prof;
    const t0 = prof[0][0], t1 = prof[prof.length - 1][0];
    const [p1, p2] = perp(e);
    function f(t) {
      if (t <= t0) return prof[0][1];
      if (t >= t1) return prof[prof.length - 1][1];
      let lo = 0, hi = prof.length - 1;
      while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (prof[mid][0] <= t) lo = mid; else hi = mid; }
      const a = prof[lo], b = prof[hi];
      const k = (t - a[0]) / (b[0] - a[0] || 1);
      return a[1] + (b[1] - a[1]) * k;
    }
    function df(t) {
      let lo = 0, hi = prof.length - 1;
      if (t <= t0) hi = 1; else if (t >= t1) lo = prof.length - 2; else {
        while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (prof[mid][0] <= t) lo = mid; else hi = mid; }
      }
      const a = prof[lo], b = prof[hi];
      return (b[1] - a[1]) / (b[0] - a[0] || 1);
    }
    const at = (t, th, rho) => add(o, add(mul(e, t), add(mul(p1, rho * Math.cos(th)), mul(p2, rho * Math.sin(th)))));
    function ring(t, count) { const r = f(t); const out = []; for (let i = 0; i < count; i++) out.push(at(t, (2 * Math.PI * i) / count, r)); return out; }
    const slices = s.slices || (prof.length === 2 ? 2 : 48);
    const tt = []; for (let i = 0; i <= slices; i++) tt.push(t0 + ((t1 - t0) * i) / slices);
    prof.forEach((q) => tt.push(q[0]));
    tt.sort((a, b) => a - b);
    return {
      kind: 'axi', def: s, o, e, p1, p2, t0, t1, f, df, at,
      F(p) {
        const w = sub(p, o); const t = dot(w, e);
        const q = sub(w, mul(e, t)); const rho = len(q);
        return Math.max(rho - f(Math.min(t1, Math.max(t0, t))) , t0 - t, t - t1);
      },
      extent() { const out = []; [t0, t1, (t0 + t1) / 2].forEach((t) => out.push(...ring(t, 8))); return out; },
      hullPoints() { const out = []; tt.forEach((t) => out.push(...ring(t, 36))); return out; },
      tt,
    };
  }

  // Điểm p có bị khối che khỏi người xem (hướng v) không: tồn tại s >= 0 để p + s*v nằm trong khối.
  function hiddenBy(solid, p, v, scale) {
    const eps = 2e-4 * scale;
    if (solid.kind === 'sphere') {
      const w = sub(p, solid.c);
      let s = -dot(w, v); if (s < 0) s = 0;
      const q = add(w, mul(v, s));
      return len(q) < solid.r - eps;
    }
    if (solid.kind === 'poly') {
      let lo = 0, hi = Infinity;
      for (let i = 0; i < solid.planes.length; i++) {
        const pl = solid.planes[i];
        const c = dot(pl.n, p) - pl.h + eps, b = dot(pl.n, v);
        if (Math.abs(b) < 1e-12) { if (c > 0) return false; continue; }
        const s = -c / b;
        if (b > 0) { if (s < hi) hi = s; } else if (s > lo) lo = s;
        if (lo > hi) return false;
      }
      return lo <= hi;
    }
    // khối tròn xoay: F lồi theo s, tìm cực tiểu bằng chia ba
    let a = 0, b = 6 * scale;
    for (let i = 0; i < 44; i++) {
      const m1 = a + (b - a) / 3, m2 = b - (b - a) / 3;
      if (solid.F(add(p, mul(v, m1))) < solid.F(add(p, mul(v, m2)))) b = m2; else a = m1;
    }
    return solid.F(add(p, mul(v, (a + b) / 2))) < -eps;
  }

  // ---------- vẽ ----------
  function fmt(x) { return (Math.round(x * 10) / 10).toString(); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function hull(points) {
    const pts = points.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    if (pts.length < 3) return pts;
    const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    const lo = [], up = [];
    pts.forEach((p) => { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); });
    for (let i = pts.length - 1; i >= 0; i--) { const p = pts[i]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
    lo.pop(); up.pop();
    return lo.concat(up);
  }

  // Dựng danh sách đối tượng vẽ (đã chiếu) cho góc nhìn (az, el). Trả về chuỗi các phần tử SVG.
  function draw(prep, view) {
    const model = prep.model;
    const [W, H] = model.size || [380, 300];
    const B = basis(view.az, view.el);
    const fit = model.fit || 0.84;
    const k = (Math.min(W, H) / 2) * fit / prep.rad;
    const cx = W / 2 + (model.dx || 0), cy = H / 2 + (model.dy || 0);
    const scale = prep.rad;
    const proj = (p) => {
      const w = sub(p, prep.center);
      return [cx + k * dot(w, B.r), cy - k * dot(w, B.u)];
    };
    const solidList = prep.solids;
    // Khối "ghost" (vd. mặt cầu nội tiếp) chỉ che những nét chỉ định rõ bằng occ:[chỉ số khối].
    const occl = solidList.filter((g) => !g.def.ghost);
    const hidden = (p, occ) => {
      const list = occ === undefined ? occl : occ;
      for (let i = 0; i < list.length; i++) if (hiddenBy(list[i], p, B.v, scale)) return true;
      return false;
    };
    const out = [];
    const fills = [], hid = [], vis = [], dots = [], texts = [];
    const cenProj = proj(prep.center);

    // Đường cong tham số: tách thành các đoạn thấy / khuất, tinh chỉnh biên bằng chia đôi.
    function strokeCurve(fn, n, o) {
      const color = o.c || INK, w = o.w || 1.7;
      const occ = o.occ === false ? [] : (Array.isArray(o.occ) ? o.occ.map((i) => solidList[i]) : (o.occ || occl));
      const mode = o.dash; // undefined/'auto': khuất thì nét đứt; 'solid': luôn nét liền; 'dash': luôn nét đứt; 'hide': ẩn phần khuất
      const hd = (t) => (occ.length ? hidden(fn(t), occ) : false);
      const ts = []; for (let i = 0; i <= n; i++) ts.push(i / n);
      const st = ts.map(hd);
      const runs = []; // {a,b,h}
      let runStart = 0, cur = st[0];
      for (let i = 1; i <= n; i++) {
        if (st[i] !== cur) {
          let a = ts[i - 1], b = ts[i];
          for (let j = 0; j < 22; j++) { const m = (a + b) / 2; if (hd(m) === cur) a = m; else b = m; }
          const tb = (a + b) / 2;
          runs.push({ a: runStart, b: tb, h: cur });
          runStart = tb; cur = st[i];
        }
      }
      runs.push({ a: runStart, b: 1, h: cur });
      runs.forEach((r) => {
        if (r.b - r.a < 1e-9) return;
        const isHid = r.h;
        if (isHid && mode === 'hide') return;
        const steps = Math.max(1, Math.ceil((r.b - r.a) * n));
        const pts = [];
        for (let i = 0; i <= steps; i++) pts.push(proj(fn(r.a + ((r.b - r.a) * i) / steps)));
        const d = 'M' + pts.map((q) => fmt(q[0]) + ' ' + fmt(q[1])).join('L');
        const dashed = mode === 'dash' || (isHid && mode !== 'solid');
        const el = '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="' + (isHid && mode !== 'dash' && mode !== 'solid' ? Math.max(1, w * 0.78) : w) + '" stroke-linecap="round" stroke-linejoin="round"' + (dashed ? ' stroke-dasharray="5 4"' : '') + '/>';
        (isHid ? hid : vis).push(el);
      });
    }
    const segFn = (a, b) => (t) => lerp(a, b, t);
    function stroke3(a, b, o) {
      const L = len(sub(a, b));
      strokeCurve(segFn(a, b), Math.max(12, Math.min(48, Math.round(L / scale * 40))), o);
    }

    // 1. khối: nền, cạnh, đường bao
    solidList.forEach((s) => {
      if (s.kind === 'poly') {
        const hp = hull(s.hullPoints().map(proj));
        fills.push('<polygon points="' + hp.map((q) => fmt(q[0]) + ',' + fmt(q[1])).join(' ') + '" fill="' + (s.def.fill || FILL) + '" opacity="0.8"/>');
        s.edges.forEach((e) => stroke3(prep.pt(e[0]), prep.pt(e[1]), { c: s.def.c || INK, w: 1.7 }));
      } else if (s.kind === 'sphere') {
        const c = proj(s.c);
        fills.push('<circle cx="' + fmt(c[0]) + '" cy="' + fmt(c[1]) + '" r="' + fmt(s.r * k) + '" fill="' + (s.def.fill || FILL) + '"/>');
        vis.push('<circle cx="' + fmt(c[0]) + '" cy="' + fmt(c[1]) + '" r="' + fmt(s.r * k) + '" fill="none" stroke="' + INK + '" stroke-width="1.8"/>');
      } else {
        const hp = hull(s.hullPoints().map(proj));
        fills.push('<polygon points="' + hp.map((q) => fmt(q[0]) + ',' + fmt(q[1])).join(' ') + '" fill="' + (s.def.fill || FILL) + '" opacity="0.85"/>');
        // đường bao (các đường sinh tại nơi pháp tuyến vuông góc hướng nhìn)
        const sil = [[], []];
        s.tt.forEach((t) => {
          const f = s.f(t), df = s.df(t);
          if (f < 1e-9) { sil[0].push(s.at(t, 0, 0)); sil[1].push(s.at(t, 0, 0)); return; }
          const A = dot(s.p1, B.v), Bv = dot(s.p2, B.v), C = df * dot(s.e, B.v);
          const R = Math.sqrt(A * A + Bv * Bv);
          if (R < 1e-9 || Math.abs(C) > R) return;
          const base = Math.atan2(Bv, A), da = Math.acos(C / R);
          sil[0].push(s.at(t, base + da, f)); sil[1].push(s.at(t, base - da, f));
        });
        sil.forEach((poly) => {
          if (poly.length < 2) return;
          vis.push('<path d="M' + poly.map((q) => { const p2 = proj(q); return fmt(p2[0]) + ' ' + fmt(p2[1]); }).join('L') + '" fill="none" stroke="' + (s.def.c || INK) + '" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>');
        });
        // hai đáy
        [s.t0, s.t1].forEach((t) => {
          const r = s.f(t);
          if (r < 1e-9) return;
          strokeCurve((u) => s.at(t, u * 2 * Math.PI, r), 96, { c: s.def.c || INK, w: 1.8 });
        });
      }
    });

    // 2. các thành phần thêm
    (model.items || []).forEach((it) => {
      const c = it.c || INK;
      if (it.t === 'seg') {
        stroke3(prep.pt(it.a), prep.pt(it.b), { c, w: it.w || 1.7, dash: it.dash, occ: it.occ });
      } else if (it.t === 'curve') {
        const pts = it.pts.map((q) => prep.pt(q));
        const fn = (t) => { const x = t * (pts.length - 1); const i = Math.min(pts.length - 2, Math.floor(x)); return lerp(pts[i], pts[i + 1], x - i); };
        strokeCurve(fn, Math.max(8, (pts.length - 1) * 4), { c, w: it.w || 1.7, dash: it.dash, occ: it.occ });
      } else if (it.t === 'circ') {
        const cc = prep.pt(it.o), nn = unit(prep.pt(it.n)), [p1, p2] = perp(nn);
        strokeCurve((u) => add(cc, add(mul(p1, it.r * Math.cos(u * 2 * Math.PI)), mul(p2, it.r * Math.sin(u * 2 * Math.PI)))), 96, { c, w: it.w || 1.7, dash: it.dash, occ: it.occ });
      } else if (it.t === 'arc') {
        const cc = prep.pt(it.o), u = unit(prep.pt(it.u)), vv = unit(prep.pt(it.v));
        const ang = Math.acos(Math.max(-1, Math.min(1, dot(u, vv))));
        const nrm = unit(cross(u, vv)), w2 = cross(nrm, u);
        strokeCurve((x) => add(cc, mul(add(mul(u, Math.cos(x * ang)), mul(w2, Math.sin(x * ang))), it.r)), 24, { c, w: it.w || 1.5, dash: 'solid' });
      } else if (it.t === 'ra') {
        const at = prep.pt(it.at), u = unit(prep.pt(it.u)), vv = unit(prep.pt(it.v)), s = it.s;
        const a = add(at, mul(u, s)), b = add(add(at, mul(u, s)), mul(vv, s)), cc = add(at, mul(vv, s));
        stroke3(a, b, { c, w: 1.4, occ: false }); stroke3(b, cc, { c, w: 1.4, occ: false });
      } else if (it.t === 'poly') {
        const pts = it.pts.map((q) => prep.pt(q));
        const pp = pts.map(proj);
        fills.push('<polygon points="' + pp.map((q) => fmt(q[0]) + ',' + fmt(q[1])).join(' ') + '" fill="' + (it.fill || '#9ecbf0') + '" opacity="' + (it.op === undefined ? 0.45 : it.op) + '"/>');
        if (it.stroke) for (let i = 0; i < pts.length; i++) stroke3(pts[i], pts[(i + 1) % pts.length], { c: it.stroke, w: it.w || 1.5, dash: it.dash, occ: it.occ });
      } else if (it.t === 'arrow') {
        const a = prep.pt(it.a), b = prep.pt(it.b);
        const pa = proj(a), pb = proj(b);
        const ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]), Lh = 9;
        const l = [pb[0] - Lh * Math.cos(ang - 0.4), pb[1] - Lh * Math.sin(ang - 0.4)];
        const r = [pb[0] - Lh * Math.cos(ang + 0.4), pb[1] - Lh * Math.sin(ang + 0.4)];
        vis.push('<line x1="' + fmt(pa[0]) + '" y1="' + fmt(pa[1]) + '" x2="' + fmt(pb[0]) + '" y2="' + fmt(pb[1]) + '" stroke="' + c + '" stroke-width="' + (it.w || 1.8) + '"/>');
        vis.push('<polygon points="' + fmt(pb[0]) + ',' + fmt(pb[1]) + ' ' + fmt(l[0]) + ',' + fmt(l[1]) + ' ' + fmt(r[0]) + ',' + fmt(r[1]) + '" fill="' + c + '"/>');
      } else if (it.t === 'pt') {
        const q = proj(prep.pt(it.p));
        dots.push('<circle cx="' + fmt(q[0]) + '" cy="' + fmt(q[1]) + '" r="' + (it.r || 3.4) + '" fill="' + c + '"/>');
      } else if (it.t === 'lbl') {
        const q = proj(prep.pt(it.p));
        let dx = it.dx || 0, dy = it.dy || 0;
        if (it.auto !== false && it.dx === undefined && it.dy === undefined) {
          let ox = q[0] - cenProj[0], oy = q[1] - cenProj[1];
          const L = Math.sqrt(ox * ox + oy * oy) || 1;
          const sz = it.size || 15, tw = String(it.s).length * sz * 0.56; // ước lượng bề rộng chữ để nhãn không đè lên nét
          const nx = ox / L, ny = oy / L;
          const dist = 9 + Math.abs(nx) * tw / 2 + Math.abs(ny) * sz * 0.5;
          dx = nx * dist; dy = ny * dist;
        }
        const size = it.size || 15;
        texts.push('<text x="' + fmt(q[0] + dx) + '" y="' + fmt(q[1] + dy) + '" font-size="' + size + '" font-weight="' + (it.bold === false ? 'normal' : 'bold') + '" fill="' + c + '" text-anchor="middle" dominant-baseline="central">' + esc(it.s) + '</text>');
      }
    });

    // 3. chú thích cố định theo màn hình
    (model.notes || []).forEach((n, i) => {
      const size = n.size || 13, c = n.c || '#d64541';
      const lines = String(n.s).split('\n');
      const lh = size + 4;
      lines.forEach((ln, j) => {
        let x = 10, y = 18 + j * lh, anchor = 'start';
        if (n.pos === 'tr') { x = W - 10; anchor = 'end'; }
        else if (n.pos === 'bl') { y = H - 10 - (lines.length - 1 - j) * lh; }
        else if (n.pos === 'bc') { x = W / 2; anchor = 'middle'; y = H - 10 - (lines.length - 1 - j) * lh; }
        else if (n.pos === 'tc') { x = W / 2; anchor = 'middle'; }
        texts.push('<text x="' + x + '" y="' + y + '" font-size="' + size + '" font-weight="' + (n.bold === false ? 'normal' : 'bold') + '" fill="' + c + '" text-anchor="' + anchor + '">' + esc(ln) + '</text>');
      });
    });

    return fills.concat(hid, vis, dots, texts).join('');
  }

  function background(W, H) {
    return '<defs><pattern id="nlg" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#cbd5e1" stroke-width="0.8"/></pattern></defs>' +
      '<rect width="' + W + '" height="' + H + '" fill="#f8fafc"/><rect width="' + W + '" height="' + H + '" fill="url(#nlg)"/>';
  }

  // Tệp SVG tĩnh (góc nhìn mặc định) kèm mô hình để giao diện dựng bản xoay được.
  function toSVG(model, view) {
    const prep = prepare(model);
    const [W, H] = model.size || [380, 300];
    const v = view || model.view || { az: 20, el: 22 };
    const json = JSON.stringify(model).replace(/\]\]>/g, ']]\\u003e');
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" font-family="Segoe UI, Arial, sans-serif">' +
      '<metadata id="' + MARK + '"><![CDATA[' + json + ']]></metadata>' +
      background(W, H) + draw(prep, v) + '</svg>';
  }

  function extractModel(svgText) {
    if (typeof svgText !== 'string' || svgText.indexOf(MARK) < 0) return null;
    const m = /<metadata id="nl-solid3d"><!\[CDATA\[([\s\S]*?)\]\]><\/metadata>/.exec(svgText);
    if (!m) return null;
    try { return JSON.parse(m[1]); } catch (e) { return null; }
  }

  // ---------- giao diện xoay ----------
  function mount(container, model, opts) {
    opts = opts || {};
    const doc = container.ownerDocument || document;
    const prep = prepare(model);
    const [W, H] = model.size || [380, 300];
    const home = model.view || { az: 20, el: 22 };
    const state = { az: home.az, el: home.el };
    const wrap = doc.createElement('div');
    wrap.className = 'solid3d';
    wrap.tabIndex = 0;
    wrap.setAttribute('role', 'img');
    wrap.setAttribute('aria-label', (opts.alt || 'Hình không gian') + ' (kéo để xoay)');
    const NS = 'http://www.w3.org/2000/svg';
    const svg = doc.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('class', 'solid3d-svg');
    svg.setAttribute('font-family', 'Segoe UI, Arial, sans-serif');
    svg.innerHTML = background(W, H);
    const g = doc.createElementNS(NS, 'g');
    svg.appendChild(g);
    const bar = doc.createElement('div');
    bar.className = 'solid3d-bar';
    const hint = doc.createElement('span');
    hint.className = 'solid3d-hint';
    hint.textContent = 'Kéo để xoay hình 360°';
    const reset = doc.createElement('button');
    reset.type = 'button'; reset.className = 'solid3d-reset'; reset.textContent = 'Góc nhìn chuẩn';
    bar.append(hint, reset);
    wrap.append(svg, bar);
    container.append(wrap);

    let queued = false;
    function render() { queued = false; g.innerHTML = draw(prep, state); }
    function schedule() {
      if (queued) return;
      queued = true;
      const raf = (typeof requestAnimationFrame === 'function') ? requestAnimationFrame : (fn) => setTimeout(fn, 16);
      raf(render);
    }
    render();

    let drag = null;
    wrap.addEventListener('pointerdown', (e) => {
      if (e.target === reset) return;
      drag = { x: e.clientX, y: e.clientY, az: state.az, el: state.el };
      try { wrap.setPointerCapture(e.pointerId); } catch (err) { /* bỏ qua */ }
      wrap.classList.add('dragging');
    });
    wrap.addEventListener('pointermove', (e) => {
      if (!drag) return;
      state.az = drag.az + (e.clientX - drag.x) * 0.6;
      state.el = Math.max(-89, Math.min(89, drag.el + (e.clientY - drag.y) * 0.6));
      schedule();
    });
    const end = () => { drag = null; wrap.classList.remove('dragging'); };
    wrap.addEventListener('pointerup', end);
    wrap.addEventListener('pointercancel', end);
    wrap.addEventListener('keydown', (e) => {
      const step = 8;
      if (e.key === 'ArrowLeft') state.az -= step; else if (e.key === 'ArrowRight') state.az += step;
      else if (e.key === 'ArrowUp') state.el = Math.min(89, state.el + step); else if (e.key === 'ArrowDown') state.el = Math.max(-89, state.el - step);
      else return;
      e.preventDefault(); schedule();
    });
    reset.addEventListener('click', () => { state.az = home.az; state.el = home.el; schedule(); });
    return { state, render, reset: () => { state.az = home.az; state.el = home.el; render(); }, element: wrap };
  }

  return { prepare, draw, toSVG, extractModel, mount, basis, hiddenBy, hull, MARK };
});
