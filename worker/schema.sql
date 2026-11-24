CREATE TABLE IF NOT EXISTS orders (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  machine TEXT NOT NULL,
  items TEXT NOT NULL,
  amount INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',   -- pending | underpaid | paid | cancelled
  paid_amount INTEGER NOT NULL DEFAULT 0,
  key TEXT,
  terms_version TEXT,
  terms_at TEXT,
  created_at TEXT NOT NULL,
  paid_at TEXT,
  tx_id INTEGER,
  reissues INTEGER NOT NULL DEFAULT 0,
  note TEXT
);
CREATE INDEX IF NOT EXISTS idx_orders_machine ON orders (machine, created_at);
CREATE INDEX IF NOT EXISTS idx_orders_phone ON orders (phone, created_at);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status, created_at);

CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY,                   -- id giao dịch của SePay, chống xử lý trùng
  reference TEXT,
  amount INTEGER NOT NULL,
  content TEXT,
  raw TEXT,
  result TEXT,
  order_code TEXT,
  created_at TEXT NOT NULL
);

-- Lần thử khôi phục mã PIN phụ huynh, dùng để giới hạn tần suất theo mã máy.
CREATE TABLE IF NOT EXISTS pin_attempts (
  machine TEXT NOT NULL,
  at TEXT NOT NULL,
  ok INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_pin_attempts ON pin_attempts (machine, at);

-- Thu hồi khóa theo mã đơn. Còn hiệu lực khi restored_at rỗng. Khôi phục chỉ ghi restored_at, không xóa lịch sử.
CREATE TABLE IF NOT EXISTS revocations (
  code TEXT PRIMARY KEY,
  reason TEXT,
  revoked_at TEXT NOT NULL,
  restored_at TEXT
);

-- Máy đã mở phần mềm với khóa của đơn (phần mềm gửi tín hiệu mỗi 5 phút khi đang mở). Dùng để hiển thị đang online / lần mở gần nhất.
CREATE TABLE IF NOT EXISTS devices (
  code TEXT NOT NULL,
  machine TEXT NOT NULL,
  version TEXT,
  first_seen TEXT NOT NULL,
  last_seen TEXT NOT NULL,
  PRIMARY KEY (code, machine)
);

-- Thu hồi riêng từng khóa học trong một đơn (hoàn tiền một phần). item là mã khóa học trong catalog, ví dụ van-hoa-9 hoặc gia-su-ai.
CREATE TABLE IF NOT EXISTS item_revocations (
  code TEXT NOT NULL,
  item TEXT NOT NULL,
  reason TEXT,
  revoked_at TEXT NOT NULL,
  restored_at TEXT,
  PRIMARY KEY (code, item)
);

-- Mã đối tác: giảm theo tỉ lệ phần trăm trên giá từng khóa. Tắt bằng active = 0, không xóa để giữ lịch sử đơn.
CREATE TABLE IF NOT EXISTS partner_codes (
  code TEXT PRIMARY KEY,
  partner TEXT NOT NULL,
  percent INTEGER NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL
);

-- Số máy tối đa được dùng mỗi mã đối tác (bảng riêng để chạy lại schema an toàn trên DB đã có).
CREATE TABLE IF NOT EXISTS partner_limits (
  code TEXT PRIMARY KEY,
  max_machines INTEGER NOT NULL
);

-- Khóa học mà mã đối tác được áp dụng. Mã không có dòng nào là áp dụng cho mọi khóa.
CREATE TABLE IF NOT EXISTS partner_items (
  code TEXT NOT NULL,
  item TEXT NOT NULL,
  PRIMARY KEY (code, item)
);

-- Giá từng khóa trong đơn: giá niêm yết, giá khách thực trả và mã đối tác đã áp (nếu có). Dùng cho hoàn tiền một phần và phiếu xác nhận.
CREATE TABLE IF NOT EXISTS order_prices (
  code TEXT NOT NULL,
  item TEXT NOT NULL,
  list_price INTEGER NOT NULL,
  paid_price INTEGER NOT NULL,
  partner_code TEXT,
  percent INTEGER,
  PRIMARY KEY (code, item)
);

-- Mỗi đơn có tối đa 2 chỗ thiết bị: 1 máy tính (win) và 1 điện thoại (android), mỗi chỗ một khóa riêng.
-- Đơn cũ chưa có dòng nào được hiểu là đã dùng chỗ máy tính với orders.machine.
CREATE TABLE IF NOT EXISTS order_devices (
  code TEXT NOT NULL,
  platform TEXT NOT NULL,
  machine TEXT NOT NULL,
  key TEXT,
  issued_at TEXT,
  PRIMARY KEY (code, platform)
);
CREATE INDEX IF NOT EXISTS idx_order_devices_machine ON order_devices (machine);

-- Phụ huynh xem kết quả học trên điện thoại: chỉ khi phụ huynh bật trên máy của học sinh. Mỗi dòng là tóm tắt một ngày × môn × lớp × chương
-- từ một thiết bị (src: win hoặc android); không có từng câu trả lời.
CREATE TABLE IF NOT EXISTS progress_sync (
  code TEXT PRIMARY KEY,
  enabled INTEGER NOT NULL DEFAULT 0,
  goal_daily INTEGER,
  goal_weekly INTEGER,
  enabled_at TEXT,
  last_sync TEXT
);
-- Mục tiêu số câu cuối tuần (T7, CN); bảng riêng để chạy lại schema.sql trên cơ sở dữ liệu cũ không lỗi.
CREATE TABLE IF NOT EXISTS progress_goal_ext (
  code TEXT PRIMARY KEY,
  goal_weekend INTEGER
);
CREATE TABLE IF NOT EXISTS progress_daily (
  code TEXT NOT NULL,
  src TEXT NOT NULL,
  day TEXT NOT NULL,
  subject TEXT NOT NULL,
  grade INTEGER NOT NULL,
  chapter TEXT NOT NULL,
  correct INTEGER NOT NULL,
  total INTEGER NOT NULL,
  lessons INTEGER NOT NULL,
  seconds INTEGER NOT NULL,
  PRIMARY KEY (code, src, day, subject, grade, chapter)
);
CREATE INDEX IF NOT EXISTS idx_progress_daily_day ON progress_daily (code, day);

-- Ngưỡng đạt (% câu đúng) mà phụ huynh đặt: pass là ngưỡng chung, pass_by là JSON { mã môn: % }.
CREATE TABLE IF NOT EXISTS progress_pass_ext (
  code TEXT PRIMARY KEY,
  pass INTEGER,
  pass_by TEXT
);

-- Thời gian dùng app theo ngày từ mỗi thiết bị (giây): open = thời gian mở app, active = thời gian dùng thực. Ngắt quãng = open - active.
CREATE TABLE IF NOT EXISTS progress_usage (
  code TEXT NOT NULL,
  src TEXT NOT NULL,
  day TEXT NOT NULL,
  open_s INTEGER NOT NULL,
  active_s INTEGER NOT NULL,
  PRIMARY KEY (code, src, day)
);

-- Phần thưởng chuỗi ngày: máy học sinh gửi trạng thái (đã tính sẵn), điện thoại phụ huynh xem; phần mềm khóa máy sau này đọc "achieved" để cộng giờ.
CREATE TABLE IF NOT EXISTS progress_reward (
  code TEXT PRIMARY KEY,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Thời khóa biểu: máy học sinh gửi (đã làm sạch), điện thoại phụ huynh xem và nhắc học.
CREATE TABLE IF NOT EXISTS progress_timetable (
  code TEXT PRIMARY KEY,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Mua cho con từ app Phụ huynh: mỗi máy phụ huynh có một mã gia đình; đơn mua qua mã đó không gắn máy nào,
-- các máy của con nhập mã gia đình một lần rồi tự nhận khóa (mỗi đơn: 1 máy tính + 1 điện thoại).
CREATE TABLE IF NOT EXISTS families (
  fcode TEXT PRIMARY KEY,
  phone TEXT NOT NULL,
  parent_machine TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_families_parent ON families (parent_machine, phone);
CREATE TABLE IF NOT EXISTS family_orders (
  code TEXT PRIMARY KEY,
  fcode TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_family_orders_f ON family_orders (fcode);
CREATE TABLE IF NOT EXISTS family_links (
  fcode TEXT NOT NULL,
  machine TEXT NOT NULL,
  platform TEXT NOT NULL,
  linked_at TEXT NOT NULL,
  PRIMARY KEY (fcode, machine)
);

-- Hướng con đã chọn trong khóa Định hướng công nghệ quốc gia (tối đa 3 nhóm), phụ huynh xem trên app Phụ huynh.
CREATE TABLE IF NOT EXISTS progress_orientation (
  code TEXT PRIMARY KEY,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
