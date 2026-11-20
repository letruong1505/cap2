#!/usr/bin/env node
// Sinh lại các hình không gian xoay được 360° (SVG kèm mô hình 3D) từ tools/solids/*.js.
// Dùng: node tools/build-solids.js [môn ...]      ví dụ: node tools/build-solids.js toan11
const fs = require('fs');
const path = require('path');
const S = require('../renderer/solid3d.js');

const root = path.join(__dirname, '..');
const SUBJECTS = ['toan7', 'toan8', 'toan9', 'toan11', 'toan12'];
const wanted = process.argv.slice(2).length ? process.argv.slice(2) : SUBJECTS;
let n = 0;
for (const sub of wanted) {
  const file = path.join(__dirname, 'solids', sub + '.js');
  if (!fs.existsSync(file)) { console.error('Chưa có bộ hình cho', sub); continue; }
  const models = require(file);
  const dir = path.join(root, 'content', sub, 'figures');
  for (const [name, model] of Object.entries(models)) {
    S.prepare(model); // báo lỗi sớm nếu thiếu điểm
    fs.writeFileSync(path.join(dir, name + '.svg'), S.toSVG(model));
    n++;
  }
}
console.log('Đã sinh', n, 'hình 3D.');
