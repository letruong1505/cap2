# Máy chủ đơn hàng Nam Linh (Cloudflare Worker + D1)

Nhận đơn từ phần mềm, nhận thông báo tiền về từ SePay, tự ký khóa `NL1-...` theo mã máy và trả về cho phần mềm tự kích hoạt. Có trang `/admin` để xem đơn, duyệt tay, hủy, đổi máy.

## Luồng
1. Phần mềm gọi `POST /api/orders` (họ tên, SĐT, khóa đã chọn, mã máy, điều khoản đã đồng ý). Máy chủ tự tính tiền theo `renderer/catalog.js`, trả mã đơn và nội dung chuyển khoản `NL <mã>`.
2. Phụ huynh quét mã QR chuyển khoản.
3. SePay gọi `POST /api/sepay`. Máy chủ chống xử lý trùng theo id giao dịch, tìm mã đơn trong nội dung, cộng dồn tiền; đủ tiền thì ký khóa.
4. Phần mềm gọi `GET /api/orders/<mã>/status?machine=<mã máy>` mỗi 5 giây. Chỉ khi đúng mã đơn và đúng mã máy mới nhận được khóa.
5. Trường hợp chuyển thiếu thì chờ chuyển bù; chuyển thừa vẫn cấp khóa và ghi nhận; sai nội dung thì nằm ở mục "Giao dịch chưa khớp" trên trang quản trị để anh xử lý.

## Cài đặt lần đầu (chạy trên máy của anh)
Cần Node 20 trở lên và tài khoản Cloudflare.

```
cd worker
npm install
npx wrangler login
npx wrangler d1 create nam-linh-orders      # chép database_id vào wrangler.toml
npm run db:init                             # tạo bảng
```

Đặt 3 bí mật (không ghi vào mã nguồn):

```
npx wrangler secret put SIGNING_KEY_PEM < private.pem     # khóa riêng đang dùng cho công cụ cấp khóa
npx wrangler secret put SEPAY_API_KEY                      # chuỗi ngẫu nhiên dài, tự đặt; dùng lại ở bước SePay
npx wrangler secret put ADMIN_TOKEN                        # mật khẩu trang /admin, tự đặt, dài ít nhất 20 ký tự
```

Trên Windows PowerShell, lệnh đầu thay bằng: `Get-Content private.pem -Raw | npx wrangler secret put SIGNING_KEY_PEM`.

Triển khai:

```
npm run deploy
```

Wrangler in địa chỉ dạng `https://nam-linh-orders.<tên-tài-khoản>.workers.dev`. Có thể gắn tên miền riêng trong Cloudflare.

## Cấu hình SePay
Trong SePay: Webhooks, Thêm webhook:
- URL: `https://<địa-chỉ-worker>/api/sepay`
- Loại sự kiện: tiền vào
- Tài khoản: tài khoản trong mã QR
- Xác thực: API Key, dùng đúng chuỗi đã đặt ở `SEPAY_API_KEY`. SePay sẽ gửi header `Authorization: Apikey <chuỗi>`.
- Có thể bật "chỉ gửi khi có mã thanh toán" và đặt tiền tố mã thanh toán là `NL`. Không bắt buộc, vì máy chủ tự tìm mã trong nội dung.
- Dùng nút "Gửi thử" của SePay: kết quả hợp lệ trả `{"success":true,...}`.

## Nối vào phần mềm
1. `main/orders-api.json`: điền `"baseUrl": "https://<địa-chỉ-worker>"`.
2. `renderer/payment-config.js`: điền ngân hàng (mã BIN), số tài khoản, tên chủ tài khoản.
3. Build lại phần mềm. Để trống `baseUrl` thì phần mềm quay về cách cũ: sao chép đơn gửi Zalo.

## Kiểm thử trước khi bán
- Chạy thử với giá thấp: tạm sửa giá một khóa trong `renderer/catalog.js` xuống vài nghìn đồng, build, deploy Worker, tạo đơn và chuyển khoản thật. Xong trả giá về như cũ ở **cả** phần mềm và Worker (cùng một file, nên build và deploy lại cả hai).
- Hoặc tạo đơn rồi dùng nút "Duyệt tay" trên `/admin` để thử phần cấp khóa mà không cần chuyển tiền.

## Bảo mật
- Khóa ký riêng nằm trong secret của Worker. Ai vào được tài khoản Cloudflare của anh có thể đọc được nó, nên bật xác thực hai lớp cho tài khoản.
- Nên bảo vệ `/admin` bằng Cloudflare Access (miễn phí đến 50 người dùng) thay vì chỉ dùng mật khẩu.
- Nên thêm quy tắc giới hạn tần suất (Rate limiting rule) cho đường dẫn `/api/orders` trong Cloudflare. Máy chủ đã chặn một máy hoặc một số điện thoại tạo quá 10 đơn mỗi giờ.
- Thông tin khách hàng lưu trong D1: họ tên, SĐT, mã máy. Điều khoản mục 8 đã ghi việc này.

## Kiểm tra mã nguồn
```
cd worker && npm test     # cần Node 22 (dùng sqlite có sẵn của Node để giả lập D1)
```
