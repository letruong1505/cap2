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
