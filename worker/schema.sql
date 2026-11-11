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
