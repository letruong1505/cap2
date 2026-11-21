const test = require('node:test');
const assert = require('node:assert/strict');
const U = require('../renderer/usage.js');

function setup(extra = {}) {
  const st = { t: new Date(2026, 10, 18, 9, 0, 0).getTime(), vis: true, mode: 'read', mem: {} };
  const storage = { getItem: (k) => st.mem[k] || null, setItem: (k, v) => { st.mem[k] = v; } };
  const tr = U.create({ storage, now: () => st.t, visible: () => st.vis, mode: () => st.mode, ...extra });
  const adv = (sec, tick = true) => { st.t += sec * 1000; if (tick) tr.tick(); };
  return { st, tr, adv, storage };
}
const day = (tr) => tr.list()[0] || { open: 0, active: 0 };

test('đang dùng liên tục: mở app và dùng thực tăng cùng nhau', () => {
  const { tr, adv } = setup();
  tr.tick();
  for (let i = 0; i < 6; i++) { adv(10, false); tr.touch(); } // 60 giây, có thao tác mỗi 10 giây
  assert.equal(day(tr).open, 60); assert.equal(day(tr).active, 60);
});

test('lâu không thao tác khi đang đọc: quá 2 phút thì không tính dùng thực, nhưng vẫn là thời gian mở app', () => {
  const { tr, adv } = setup();
  tr.tick(); tr.touch();
  for (let i = 0; i < 40; i++) adv(5); // 200 giây không thao tác
  const d = day(tr);
  assert.equal(d.open, 200);
  assert.equal(d.active, 120); // chỉ 2 phút đầu
});

test('đang làm câu hỏi: cho phép im lặng tới 5 phút (tính trên giấy)', () => {
  const { tr, adv, st } = setup();
  st.mode = 'question';
  tr.tick(); tr.touch();
  for (let i = 0; i < 80; i++) adv(5); // 400 giây
  const d = day(tr);
  assert.equal(d.open, 400); assert.equal(d.active, 300);
});

test('thu nhỏ hoặc chuyển sang app khác: tính vào ngắt quãng, không tính dùng thực', () => {
  const { tr, adv, st } = setup();
  tr.tick(); tr.touch();
  adv(30, false); tr.touch(); // 30 giây dùng
  st.vis = false; tr.tick(); // thu nhỏ
  adv(600, false); // 10 phút ở nền (bộ hẹn giờ bị ngủ), quay lại
  st.vis = true; tr.tick();
  const d = day(tr);
  assert.equal(d.open, 630); assert.equal(d.active, 30);
});

test('máy ngủ khi đang hiện: khoảng trống dài không bị tính vào thời gian mở app', () => {
  const { tr, adv } = setup();
  tr.tick(); tr.touch();
  adv(3 * 3600); // máy ngủ 3 giờ rồi dậy
  assert.ok(day(tr).open <= 30);
});

test('để nền quá lâu thì tính tối đa 30 phút', () => {
  const { tr, adv, st } = setup();
  tr.tick(); st.vis = false; tr.tick();
  adv(5 * 3600);
  assert.equal(day(tr).open, 1800); assert.equal(day(tr).active, 0);
});

test('lưu và nạp lại giữa các lần mở app; dùng thực không bao giờ vượt thời gian mở', () => {
  const a = setup();
  a.tr.tick(); a.tr.touch(); a.adv(20, false); a.tr.touch();
  const st = a.st;
  const b = U.create({ storage: a.storage, now: () => st.t, visible: () => true, mode: () => 'read' });
  assert.equal(b.list()[0].open, 20);
  b.tick(); st.t += 10000; b.touch();
  assert.equal(b.list()[0].open, 30);
  b.list().forEach((r) => assert.ok(r.active <= r.open));
});

test('tổng hợp theo khoảng ngày và định dạng thời lượng', () => {
  const rows = [{ day: '2026-11-16', open: 3600, active: 1800 }, { day: '2026-11-17', open: 600, active: 900 }, { day: '2026-11-20', open: 100, active: 100 }];
  const s = U.summarize(rows, '2026-11-16', '2026-11-18');
  assert.equal(s.open, 4200); assert.equal(s.active, 2400); assert.equal(s.brk, 1800); // dòng active > open bị chặn bằng open
  assert.deepEqual(s.byDay['2026-11-17'], { open: 600, active: 600, brk: 0 });
  assert.equal(U.fmtDur(0), '0 phút'); assert.equal(U.fmtDur(10), 'dưới 1 phút'); assert.equal(U.fmtDur(1500), '25 phút');
  assert.equal(U.fmtDur(3720), '1 giờ 2 phút'); assert.equal(U.fmtDur(7200), '2 giờ');
});
