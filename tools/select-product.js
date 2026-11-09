// Chọn sản phẩm sẽ đóng gói: node tools/select-product.js thcs|thpt
// Ghi cấu hình sản phẩm vào main/product.json (tiến trình chính đọc file này khi chạy).
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const id = process.argv[2];
const src = path.join(root, 'product', `${id}.json`);
if (!id || !fs.existsSync(src)) {
  console.error('Sản phẩm không hợp lệ. Dùng: thcs hoặc thpt');
  process.exit(1);
}
const product = JSON.parse(fs.readFileSync(src, 'utf8'));
for (const s of product.subjects) {
  if (!fs.existsSync(path.join(root, 'content', s, 'manifest.json'))) {
    console.error(`Thiếu nội dung môn: ${s}`);
    process.exit(1);
  }
}
fs.writeFileSync(path.join(root, 'main', 'product.json'), JSON.stringify(product, null, 2) + '\n');
console.log(`Sản phẩm: ${product.title} (${product.subjects.length} môn)`);
