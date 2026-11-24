// Sinh parent/dhqg-data.js từ renderer/national-data.js (nguồn dữ liệu duy nhất của mục Định hướng công nghệ quốc gia).
const fs = require('fs'); const path = require('path');
global.window = {}; require('../renderer/national-data.js');
const out = {}; window.NATIONAL_DATA.groups.forEach((x) => { out[x.id] = { n: x.n, s: x.s, m: x.m, k: x.k, a: x.a, b: x.b }; });
fs.writeFileSync(path.join(__dirname, '..', 'parent', 'dhqg-data.js'), '// Dữ liệu Định hướng công nghệ quốc gia cho app Phụ huynh (n: tên nhóm, s: môn nền tảng, m: nhóm ngành, k: kỹ năng, a: việc ở THCS, b: việc ở THPT).\n// Sinh từ renderer/national-data.js; có test đối chiếu, sửa dữ liệu gốc rồi chạy: node tools/build-parent-dhqg.js\nwindow.PARENT_DHQG = ' + JSON.stringify(out) + ';\n');
