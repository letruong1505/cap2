// Dựng dữ liệu điểm chuẩn cho khối "Chọn trường" của Ôn thi THPT, chia theo 3 miền (Bắc, Trung, Nam).
// Nguồn: các tệp tools/thpt-data/<trường>.txt (do người biên soạn nhập từ bảng điểm chuẩn đã công bố) + regions.json.
// Mỗi miền sinh ra một tệp riêng renderer/thpt-school-<miền>.js để cập nhật độc lập từng miền.
// Cách chạy: node tools/build-thpt-school.js  (kiểm tra bằng: node --test tests/thpt-school.test.js)
const fs = require('fs');
const path = require('path');
const L = require('../renderer/thpt-school-logic.js');

const SRC = path.join(__dirname, 'thpt-data');
const OUT = path.join(__dirname, '..', 'renderer');

function parseSchool(file) {
  const text = fs.readFileSync(path.join(SRC, file), 'utf8');
  const meta = {}; const rows = []; let defKhoi = null; const dropped = new Set();
  text.split(/\r?\n/).forEach((raw, i) => {
    const line = raw.trim();
    if (!line) return;
    let m = /^#\s*(\w+):\s*(.*)$/.exec(line);
    if (m) { meta[m[1]] = m[2]; return; }
    m = /^@khoi\s+(.+)$/.exec(line);
    if (m) { defKhoi = m[1].split(';').map((s) => s.trim()); return; }
    const parts = line.split('|');
    let name; let khoi; let score;
    if (parts.length === 3) { [name, khoi, score] = [parts[0], parts[1].split(';'), parts[2]]; }
    else if (parts.length === 2 && defKhoi) { [name, khoi, score] = [parts[0], defKhoi, parts[1]]; }
    else throw new Error(`${file}:${i + 1}: dòng sai định dạng`);
    const n = Number(score);
    if (!Number.isFinite(n) || n < 10 || n > 30) throw new Error(`${file}:${i + 1}: điểm "${score}" ngoài khoảng 10–30`);
    const ok = khoi.map((k) => k.trim()).filter((k) => { if (L.KHOI[k]) return true; dropped.add(k); return false; });
    if (!ok.length) return; // mọi tổ hợp của dòng này chưa hỗ trợ (năng khiếu, ngoại ngữ khác…)
    rows.push([name.trim(), ok, n]);
  });
  for (const k of ['id', 'name', 'region', 'year', 'source']) if (!meta[k]) throw new Error(`${file}: thiếu # ${k}`);
  return { meta, rows, dropped: [...dropped].sort() };
}

function build(outDir = OUT) {
  const regions = JSON.parse(fs.readFileSync(path.join(SRC, 'regions.json'), 'utf8'));
  const byRegion = {}; const report = [];
  for (const rg of Object.keys(regions)) byRegion[rg] = [];
  for (const f of fs.readdirSync(SRC).filter((x) => x.endsWith('.txt')).sort()) {
    const { meta, rows, dropped } = parseSchool(f);
    if (!byRegion[meta.region]) throw new Error(`${f}: miền "${meta.region}" không có trong regions.json`);
    byRegion[meta.region].push({
      id: meta.id, name: meta.name, short: meta.short || meta.name, province: meta.province || '', year: Number(meta.year),
      source: meta.source, note: meta.note || '', rows,
    });
    report.push({ file: f, rows: rows.length, dropped });
  }
  const files = [];
  for (const [rg, info] of Object.entries(regions)) {
    const data = { region: rg, name: info.name, updated: info.updated, schools: byRegion[rg] };
    const js = '// Tệp sinh tự động từ tools/thpt-data bằng tools/build-thpt-school.js. Không sửa tay.\n'
      + '(function (root) {\n  var d = ' + JSON.stringify(data) + ';\n'
      + "  if (typeof module === 'object' && module.exports) module.exports = d;\n"
      + '  else { root.THPT_SCHOOL_DATA = root.THPT_SCHOOL_DATA || {}; root.THPT_SCHOOL_DATA[d.region] = d; }\n'
      + "})(typeof self !== 'undefined' ? self : this);\n";
    const p = path.join(outDir, `thpt-school-${rg}.js`);
    fs.writeFileSync(p, js);
    files.push(p);
  }
  return { files, report };
}

module.exports = { build, parseSchool };
if (require.main === module) {
  const { report } = build();
  for (const r of report) console.log(`${r.file}: ${r.rows} dòng${r.dropped.length ? `, bỏ tổ hợp chưa hỗ trợ: ${r.dropped.join(' ')}` : ''}`);
}
