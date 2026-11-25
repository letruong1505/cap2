// Tính điểm xét tuyển và chia nhóm "an toàn / cân nhắc / thử sức" cho khối Chọn trường của Ôn thi THPT.
// Thuần tính toán, không đụng giao diện. Quy tắc theo Thông tư 06/2026/TT-BGDĐT (điểm ưu tiên) và bảng tổ hợp công bố 2026.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.THPT_SCHOOL_LOGIC = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  // Mã môn khớp renderer/thpt-exam-data.js (ELECTIVES), thêm TO = Toán, VA = Ngữ văn (hai môn bắt buộc).
  // TECH hiểu là Công nghệ công nghiệp (X03, X07, X27); tổ hợp dùng Công nghệ nông nghiệp (X08) chưa hỗ trợ.
  const KHOI = {
    A00: ['TO', 'PH', 'CH'], A01: ['TO', 'PH', 'EN'], A02: ['TO', 'PH', 'BI'],
    B00: ['TO', 'CH', 'BI'], B03: ['TO', 'VA', 'BI'], B08: ['TO', 'BI', 'EN'],
    C00: ['VA', 'LI', 'DI'], C01: ['TO', 'VA', 'PH'], C02: ['TO', 'VA', 'CH'], C03: ['TO', 'VA', 'LI'], C04: ['TO', 'VA', 'DI'],
    D01: ['TO', 'VA', 'EN'], D07: ['TO', 'CH', 'EN'], D08: ['TO', 'BI', 'EN'], D09: ['TO', 'LI', 'EN'], D10: ['TO', 'DI', 'EN'],
    D14: ['VA', 'LI', 'EN'], D15: ['VA', 'DI', 'EN'],
    X01: ['TO', 'VA', 'GDKT'], X02: ['TO', 'VA', 'IT'], X03: ['TO', 'VA', 'TECH'], X05: ['TO', 'PH', 'GDKT'],
    X06: ['TO', 'PH', 'IT'], X07: ['TO', 'PH', 'TECH'], X09: ['TO', 'CH', 'GDKT'],
    X25: ['TO', 'EN', 'GDKT'], X26: ['TO', 'EN', 'IT'], X27: ['TO', 'EN', 'TECH'],
    X70: ['VA', 'LI', 'GDKT'], X74: ['VA', 'DI', 'GDKT'], X78: ['VA', 'GDKT', 'EN'],
  };

  const KV = { KV1: 0.75, 'KV2-NT': 0.5, KV2: 0.25, KV3: 0 };
  const DT = { none: 0, UT1: 2, UT2: 1 };
  const KV_LABEL = { KV1: 'Khu vực 1 (+0,75)', 'KV2-NT': 'Khu vực 2 nông thôn (+0,5)', KV2: 'Khu vực 2 (+0,25)', KV3: 'Khu vực 3 (không cộng)' };
  const DT_LABEL = { none: 'Không thuộc diện ưu tiên', UT1: 'Nhóm ưu tiên 1 (+2,0)', UT2: 'Nhóm ưu tiên 2 (+1,0)' };

  // Nhóm theo chênh lệch giữa điểm của em và điểm chuẩn năm gần nhất.
  const BANDS = [
    { id: 'an-toan', label: 'An toàn', min: 1.0, hint: 'Điểm của em cao hơn điểm chuẩn từ 1 điểm trở lên.' },
    { id: 'can-nhac', label: 'Cân nhắc', min: -0.5, hint: 'Điểm của em sát điểm chuẩn (từ thấp hơn 0,5 đến cao hơn 1 điểm).' },
    { id: 'thu-suc', label: 'Thử sức', min: -2.0, hint: 'Điểm của em thấp hơn điểm chuẩn từ 0,5 đến 2 điểm.' },
  ];

  const r2 = (x) => Math.round(x * 100) / 100;

  // Ghép điểm số: nhận số hoặc chuỗi có dấu phẩy, trả null nếu ngoài 0–10.
  function parseScore(v) {
    if (v === null || v === undefined || v === '') return null;
    const n = typeof v === 'number' ? v : Number(String(v).trim().replace(',', '.'));
    return Number.isFinite(n) && n >= 0 && n <= 10 ? n : null;
  }

  // Các khối em có thể dùng: đủ cả 3 môn trong 4 môn đã thi (Toán, Ngữ văn, 2 môn tự chọn).
  function availableKhoi(picked) {
    const have = new Set(['TO', 'VA', ...(picked || [])]);
    return Object.keys(KHOI).filter((k) => KHOI[k].every((m) => have.has(m)));
  }

  // Điểm ưu tiên: dưới 22,5 điểm được cộng đủ; từ 22,5 trở lên giảm dần theo công thức của Bộ.
  function priorityBonus(total, kv, dt) {
    const base = (KV[kv] || 0) + (DT[dt] || 0);
    if (!base) return 0;
    if (total < 22.5) return r2(base);
    return r2(Math.max(0, ((30 - total) / 7.5) * base));
  }

  // Điểm của em theo từng khối có thể dùng. scores: {TO, VA, EN, ...} thang 10.
  function khoiScores(scores, picked, kv, dt) {
    const out = {};
    for (const k of availableKhoi(picked)) {
      const parts = KHOI[k].map((m) => parseScore(scores[m]));
      if (parts.some((p) => p === null)) continue;
      const total = r2(parts.reduce((a, b) => a + b, 0));
      const bonus = priorityBonus(total, kv, dt);
      out[k] = { total, bonus, score: r2(total + bonus) };
    }
    return out;
  }


  // Môn ôn lớp 12 trong app -> mã môn của khung THPT. Ngữ văn, Tin học, Công nghệ chưa có bài ôn nên không có điểm.
  const SUBJECT_MAP = { toan: 'TO', anh: 'EN', ly: 'PH', hoa: 'CH', sinh: 'BI', gdktpl: 'GDKT', lichsu: 'LI', 'lich-su': 'LI', diali: 'DI', 'dia-li': 'DI' };
  const EST_WINDOW = 60; // lấy các lần làm gần nhất cho tới khi đủ ngần này câu
  const EST_MIN = 20;    // dưới ngần này câu thì chưa đủ dữ liệu để ước điểm

  // Ước điểm từng môn từ các lần làm bài ôn luyện lớp 12: tỉ lệ đúng của ~60 câu gần nhất x 10.
  // attempts: mảng {t, subject, grade, correct, total}. Trả {mã môn: {score, questions, lessons, enough}}.
  function estimateScores(attempts, grade) {
    const g = grade || 12;
    const by = {};
    const list = (attempts || []).filter((a) => a && a.grade === g && a.total > 0 && SUBJECT_MAP[a.subject]).sort((a, b) => b.t - a.t);
    for (const a of list) {
      const m = SUBJECT_MAP[a.subject];
      const x = by[m] || (by[m] = { correct: 0, questions: 0, lessons: 0 });
      if (x.questions >= EST_WINDOW) continue;
      x.correct += a.correct; x.questions += a.total; x.lessons += 1;
    }
    const out = {};
    for (const [m, x] of Object.entries(by)) {
      out[m] = { score: Math.round((x.correct / x.questions) * 100) / 10, questions: x.questions, lessons: x.lessons, enough: x.questions >= EST_MIN };
    }
    return out;
  }

  function bandOf(diff) {
    for (const b of BANDS) if (diff >= b.min) return b.id;
    return null; // thấp hơn điểm chuẩn quá 2 điểm: không gợi ý
  }

  // Duyệt dữ liệu các miền đã chọn và trả danh sách ngành khớp, mỗi (trường, ngành) giữ tổ hợp tốt nhất cho em.
  // data: {bac:{schools}, trung:{...}, nam:{...}}; opts: {regions:[...], query:''}
  function suggest(data, ks, opts) {
    const regions = (opts && opts.regions && opts.regions.length) ? opts.regions : Object.keys(data || {});
    const q = norm((opts && opts.query) || '');
    const best = new Map();
    for (const rg of regions) {
      const reg = data && data[rg];
      if (!reg) continue;
      for (const sc of reg.schools) {
        for (const [name, khoiList, cut] of sc.rows) {
          if (q && !norm(name).includes(q) && !norm(sc.short || sc.name).includes(q)) continue;
          let pick = null;
          for (const k of khoiList) {
            if (!ks[k]) continue;
            if (!pick || ks[k].score > ks[pick].score) pick = k;
          }
          if (!pick) continue;
          const diff = r2(ks[pick].score - cut);
          const key = `${rg}|${sc.id}|${name}`;
          const cur = best.get(key);
          if (!cur || diff > cur.diff) best.set(key, { region: rg, school: sc.short || sc.name, schoolId: sc.id, name, khoi: pick, cut, mine: ks[pick].score, diff, band: bandOf(diff) });
        }
      }
    }
    const list = [...best.values()].filter((x) => x.band);
    const groups = { 'an-toan': [], 'can-nhac': [], 'thu-suc': [] };
    for (const x of list) groups[x.band].push(x);
    groups['an-toan'].sort((a, b) => b.cut - a.cut || a.name.localeCompare(b.name, 'vi'));
    groups['can-nhac'].sort((a, b) => b.cut - a.cut || a.name.localeCompare(b.name, 'vi'));
    groups['thu-suc'].sort((a, b) => a.cut - b.cut || a.name.localeCompare(b.name, 'vi'));
    return groups;
  }

  // Bỏ dấu, hạ chữ thường để tìm ngành không cần gõ đúng dấu.
  function norm(s) {
    return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase().trim();
  }

  return { KHOI, KV, DT, KV_LABEL, DT_LABEL, BANDS, parseScore, availableKhoi, priorityBonus, khoiScores, bandOf, suggest, norm, estimateScores, SUBJECT_MAP };
});
