# Giáo trình THCS — luyện tập offline cho học sinh cấp 2 (Kết nối tri thức)

Phần mềm luyện tập offline cho học sinh cấp 2. Đây là khung ứng dụng và một bài thử: **Cộng và trừ số hữu tỉ**.

## Chạy thử trên máy phát triển

```
npm install
npm start
```

Yêu cầu: Node.js 18 trở lên, Windows 10/11.

## Cấu trúc

- `main/`: tiến trình chính. `main.js` tạo cửa sổ và đăng ký IPC; `content-loader.js` đọc gói nội dung và chỉ cho phép đọc trong `content/`; `preload.js` là cầu nối an toàn cho giao diện.
- `renderer/`: giao diện. `app.js` hiển thị danh mục theo manifest, bài học, luyện tập và chấm điểm.
- `core/`, `license/`, `exam-lan/`: để trống, sẽ làm ở các mốc sau.
- `content/toan7/manifest.json`: cấu trúc sách theo mục lục Toán 7 tập 1 và tập 2. Bài nào có `file` là bài đã có nội dung.
- `content/toan7/tap1/chuong-1/bai-2/cong-tru.json`: nội dung bài 2 (phần cộng và trừ).
- `tools/validate-content.js`: kiểm tra nội dung trước khi đóng gói (`npm run validate`).

## Chưa có trong bản thử

- Công thức render bằng KaTeX (hiện chỉ hiển thị dạng văn bản).
- Hình minh họa 3D và thao tác trên trục số.
- License theo lớp, đăng nhập học sinh, bài thi thử và thi LAN.
- Đóng gói file cài đặt (exe). Chưa tạo cho đến khi có xác nhận.
