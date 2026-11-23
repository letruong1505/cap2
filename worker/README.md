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

### Tải nội dung khóa học về máy (PACK_MASTER)
Bản exe chỉ giữ mục lục và 2 bài học thử; nội dung từng lớp được mã hóa, nằm trên R2 (`educenter-content/`) và máy khách tải về sau khi kích hoạt. Khoá giải mã của từng lớp sinh từ một bí mật chung `PACK_MASTER`, Worker chỉ cấp cho máy có khoá bản quyền hợp lệ (`POST /api/pack/keys`).

Tạo bí mật (chạy một lần, chép kết quả vào cả hai nơi dưới đây, giữ kín):

```
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
npx wrangler secret put PACK_MASTER        # dán chuỗi vừa tạo, rồi: npm run deploy
```

Trên GitHub: Settings → Secrets and variables → Actions → New repository secret, tên `PACK_MASTER`, dán đúng chuỗi đó. Phải deploy Worker xong rồi mới chạy workflow "Build Windows exe". Chưa đặt secret trên GitHub thì exe vẫn chứa đủ nội dung như trước.

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

## Thu hồi khóa và theo dõi máy đang dùng
- Phần mềm (bản mới) mở lên 8 giây thì gửi tín hiệu `POST /api/ping` về Worker, sau đó mỗi 5 phút, và gửi ngay sau khi kích hoạt. Nội dung chỉ gồm mã máy, mã đơn của các khóa đang dùng và số bản. Không gửi dữ liệu học tập.
- Trang `/admin` có cột "Máy đã dùng": mã máy, số bản, nhãn **Đang online** (có tín hiệu trong 10 phút) hoặc **Offline** kèm lần mở gần nhất. Trang tự tải lại mỗi 30 giây.
- Nút **Thu hồi** (đơn đã thanh toán): gõ lại mã đơn để xác nhận, nhập lý do. Chỉ đánh dấu trong bảng `revocations`, không xóa đơn, không xóa dữ liệu học trên máy khách. Máy khách bị vô hiệu khóa của đúng đơn đó ở tín hiệu kế tiếp (tối đa 5 phút khi có mạng), các khóa khác của khách vẫn dùng.
- Nút **Khôi phục**: gỡ đánh dấu, máy khách dùng lại ở tín hiệu kế tiếp. Lịch sử thu hồi vẫn còn trong bảng.
- **Hoàn tiền một phần:** ở cột Khóa học, mỗi khóa học có nút **Thu hồi** riêng (gõ lại mã đơn để xác nhận, nhập lý do). Chỉ khóa học đó bị tắt trên máy khách, các khóa còn lại trong cùng đơn vẫn dùng, khách không phải nhập lại khóa. Khôi phục theo từng khóa học. Thu hồi hết mọi khóa học của một đơn thì tương đương thu hồi cả đơn. Dữ liệu nằm trong bảng `item_revocations`. Khóa Văn hóa tắt theo lớp (ví dụ chỉ tắt Lớp 9).
- Giới hạn: chỉ áp dụng cho bản phần mềm có tính năng này; khóa cấp tay bằng công cụ cấp khóa (không thuộc đơn nào) không thu hồi được; máy không có mạng vẫn dùng được cho đến khi có mạng.
- Nâng cấp từ bản cũ: chạy lại `npm run db:init` (an toàn, chỉ tạo thêm các bảng `revocations`, `devices` và `item_revocations`) rồi `npm run deploy`.

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

## Cổng đối tác (xem số lượng active để đối soát hoa hồng)

- Trang `/doi-tac` chỉ để xem, không cần mật khẩu quản trị. Mỗi đối tác có một liên kết riêng dạng `/doi-tac#<mã>`; mã tính từ `ADMIN_TOKEN` và tên đối tác nên không cần bảng dữ liệu mới.
- Lấy liên kết ở trang `/admin`, mục "Liên kết cho đối tác" (nút Sao chép), rồi gửi riêng cho từng đối tác.
- Đối tác thấy: số khóa/đơn đang hoạt động (đã thanh toán, chưa hoàn hoặc thu hồi), số máy đã kích hoạt, tiền khách thực trả, theo khóa học và danh sách đơn (số điện thoại chỉ hiện 3 số cuối), lọc theo khoảng ngày đặt đơn. Không thấy tên khách và không thao tác được gì.
- Hoa hồng 25% trên số tiền khách thực trả của từng khóa (làm tròn từng khóa). Tổng hoa hồng trong khoảng ngày đang chọn vượt 5.000.000 đ thì khấu trừ 10% thuế trên toàn bộ số đó; hiện sẵn "thực nhận". Các mức này là hằng số ở đầu `worker/src/partner-portal.js`, trang `/admin` (Đối soát đối tác) dùng cùng cách tính và mặc định 25%.
- Muốn đổi mã của mọi đối tác (lộ liên kết): đặt secret `PARTNER_SALT` bằng một chuỗi mới (`npx wrangler secret put PARTNER_SALT`) rồi deploy; đổi `ADMIN_TOKEN` cũng làm đổi mã.

