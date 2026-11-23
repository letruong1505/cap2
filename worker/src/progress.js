// Phụ huynh xem kết quả học trên điện thoại. Chỉ lưu tóm tắt theo ngày (ngày × môn × lớp × chương), chỉ khi phụ huynh bật trên máy của học sinh.
// Ba việc: máy học sinh bật/tắt/xóa (settings), máy học sinh gửi tóm tắt (push), điện thoại phụ huynh xem (view, bằng mã đơn + số điện thoại).
import { HttpError, MACHINE_RE, getOrder, getSlots } from './orders.js';

const PHONE_RE = /^(0|\+84)\d{9}$/;
const DAY_RE = /^\d{4}-\d{2}-\d{2}$/;
const MAX_PUSH_ROWS = 1500;
const MAX_VIEW_ROWS = 8000;
const MAX_USAGE_ROWS = 400;
const MAX_RANGE_DAYS = 366;
const DAY_MS = 86400000;
const nowIso = (now) => now.toISOString();

const cleanCode = (v) => String(v || '').toUpperCase().replace(/[^A-Z0-9]/g, '').replace(/^NL(?=[A-Z0-9]{6}$)/, '');
const cleanMachine = (v) => String(v || '').trim().toUpperCase();

async function revoked(db, code) {
  return !!(await db.prepare('SELECT 1 AS x FROM revocations WHERE code = ?1 AND restored_at IS NULL').bind(code).first());
}

// Máy học sinh gọi: mã đơn + mã máy phải khớp một chỗ thiết bị của đơn đã thanh toán. Trả về đơn và loại thiết bị (win/android).
async function deviceOrder(db, input) {
  const code = cleanCode(input.code); const machine = cleanMachine(input.machineId);
  if (!MACHINE_RE.test(machine) || !/^[A-Z0-9]{6}$/.test(code)) throw new HttpError(404, 'Không tìm thấy đơn trên máy này.');
  const o = await getOrder(db, code);
  if (!o || o.status !== 'paid') throw new HttpError(404, 'Không tìm thấy đơn trên máy này.');
  const slots = await getSlots(db, o);
  const src = ['win', 'android'].find((p) => slots[p] && slots[p].machine === machine);
  if (!src) throw new HttpError(404, 'Không tìm thấy đơn trên máy này.');
  if (await revoked(db, o.code)) throw new HttpError(403, 'Đơn này đã bị thu hồi bản quyền.');
  return { o, src };
}

async function statusOf(db, code) {
  const s = await db.prepare('SELECT enabled, goal_daily, goal_weekly, last_sync FROM progress_sync WHERE code = ?1').bind(code).first();
  const n = await db.prepare('SELECT COUNT(*) AS n FROM progress_daily WHERE code = ?1').bind(code).first();
  const x = await db.prepare('SELECT goal_weekend FROM progress_goal_ext WHERE code = ?1').bind(code).first();
  return { enabled: !!(s && s.enabled), goals: s && s.goal_daily ? { daily: s.goal_daily, weekend: (x && x.goal_weekend) || 80, weekly: s.goal_weekly, ...(await passOf(db, code)) } : null, lastSync: (s && s.last_sync) || null, rows: n.n, reward: await rewardOf(db, code) };
}

// Ngưỡng đạt: pass chung (10–100), passBy riêng từng môn; luôn trả về giá trị đã làm sạch.
function cleanPass(input) {
  const out = { pass: clampInt(input && input.pass, 10, 100, 80), passBy: {} };
  const o = input && input.passBy;
  if (o && typeof o === 'object') Object.keys(o).slice(0, 60).forEach((k) => { const v = Math.round(Number(o[k])); if (/^[a-z0-9_-]{1,30}$/i.test(k) && Number.isFinite(v) && v >= 10 && v <= 100) out.passBy[k] = v; });
  return out;
}
async function passOf(db, code) {
  const r = await db.prepare('SELECT pass, pass_by FROM progress_pass_ext WHERE code = ?1').bind(code).first();
  let by = {};
  try { by = r && r.pass_by ? JSON.parse(r.pass_by) : {}; } catch (e) { by = {}; }
  return cleanPass({ pass: r && r.pass, passBy: by });
}
// Phần thưởng theo tuần: chỉ giữ các trường hợp lệ, văn bản cắt ngắn. achieved = còn tuần thắng chưa trao (phần mềm khóa máy sau này đọc cờ này).
function cleanReward(r) {
  if (!r || typeof r !== 'object') return null;
  const hist = (Array.isArray(r.hist) ? r.hist : []).filter((x) => x && DAY_RE.test(String(x.week))).slice(-12)
    .map((x) => ({ week: String(x.week), ok: x.ok === true, count: clampInt(x.count, 0, 7, 0), done: x.done === true }));
  const on = r.on === true;
  const pending = on ? hist.filter((x) => x.ok && !x.done).length : 0;
  return { on, need: clampInt(r.days, 1, 7, 7), pct: clampInt(r.pct, 10, 100, 70), text: String(r.text || '').replace(/\s+/g, ' ').trim().slice(0, 80), count: clampInt(r.count, 0, 7, 0), pending, achieved: pending > 0, hist };
}
async function rewardOf(db, code) {
  const r = await db.prepare('SELECT data FROM progress_reward WHERE code = ?1').bind(code).first();
  try { return r ? cleanReward({ ...JSON.parse(r.data), days: JSON.parse(r.data).need }) : null; } catch (e) { return null; }
}
// Thời khóa biểu từ máy học sinh: tối đa 12 lớp × 6 ngày × 12 môn, chuỗi ngắn; bỏ mọi trường lạ.
function cleanTimetable(t) {
  if (!t || typeof t !== 'object') return null;
  const grades = {};
  Object.keys(t.grades || {}).slice(0, 12).forEach((g) => {
    const x = t.grades[g];
    if (!/^\d{1,2}$/.test(g) || !x || !DAY_RE.test(String(x.week)) || !x.days || typeof x.days !== 'object') return;
    const days = {}; const pm = {};
    const clean = (a) => (Array.isArray(a) ? a : []).filter((s) => typeof s === 'string' && s).slice(0, 12).map((s) => s.slice(0, 40));
    for (let n = 1; n <= 6; n++) { days[n] = clean(x.days[n]); pm[n] = clean(x.pm && x.pm[n]); }
    grades[g] = { week: String(x.week), days, pm };
  });
  return { v: 1, remindOn: t.remindOn !== false, remindHour: clampInt(t.remindHour, 0, 23, 19), grades };
}
async function timetableOf(db, code) {
  const r = await db.prepare('SELECT data FROM progress_timetable WHERE code = ?1').bind(code).first();
  try { return r ? cleanTimetable(JSON.parse(r.data)) : null; } catch (e) { return null; }
}
const clampInt = (v, lo, hi, d) => { v = Math.round(Number(v)); return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : d; };

// Bật/tắt chia sẻ, đặt mục tiêu, xóa dữ liệu trên máy chủ. Không truyền gì thì chỉ trả trạng thái.
export async function progressSettings(db, input, now = new Date()) {
  const { o } = await deviceOrder(db, input);
  if (input.enabled === true) {
    await db.prepare('INSERT INTO progress_sync (code, enabled, enabled_at) VALUES (?1, 1, ?2) ON CONFLICT(code) DO UPDATE SET enabled = 1, enabled_at = ?2').bind(o.code, nowIso(now)).run();
  } else if (input.enabled === false) {
    await db.prepare('INSERT INTO progress_sync (code, enabled) VALUES (?1, 0) ON CONFLICT(code) DO UPDATE SET enabled = 0').bind(o.code).run();
  }
  if (input.purge === true) {
    await db.prepare('DELETE FROM progress_daily WHERE code = ?1').bind(o.code).run();
    await db.prepare('DELETE FROM progress_usage WHERE code = ?1').bind(o.code).run();
    await db.prepare('DELETE FROM progress_reward WHERE code = ?1').bind(o.code).run();
    await db.prepare('DELETE FROM progress_timetable WHERE code = ?1').bind(o.code).run();
    await db.prepare('UPDATE progress_sync SET last_sync = NULL WHERE code = ?1').bind(o.code).run();
  }
  if (input.goals && typeof input.goals === 'object') {
    await db.prepare('INSERT INTO progress_sync (code, enabled, goal_daily, goal_weekly) VALUES (?1, 0, ?2, ?3) ON CONFLICT(code) DO UPDATE SET goal_daily = ?2, goal_weekly = ?3')
      .bind(o.code, clampInt(input.goals.daily, 5, 200, 50), clampInt(input.goals.weekly, 1, 7, 5)).run();
    await db.prepare('INSERT INTO progress_goal_ext (code, goal_weekend) VALUES (?1, ?2) ON CONFLICT(code) DO UPDATE SET goal_weekend = ?2')
      .bind(o.code, clampInt(input.goals.weekend, 5, 200, 80)).run();
    const ps = cleanPass(input.goals);
    await db.prepare('INSERT INTO progress_pass_ext (code, pass, pass_by) VALUES (?1, ?2, ?3) ON CONFLICT(code) DO UPDATE SET pass = ?2, pass_by = ?3')
      .bind(o.code, ps.pass, JSON.stringify(ps.passBy)).run();
  }
  const rw = cleanReward(input.reward);
  if (rw) {
    await db.prepare('INSERT INTO progress_reward (code, data, updated_at) VALUES (?1, ?2, ?3) ON CONFLICT(code) DO UPDATE SET data = ?2, updated_at = ?3').bind(o.code, JSON.stringify(rw), nowIso(now)).run();
  }
  const tt = cleanTimetable(input.timetable);
  if (tt) {
    await db.prepare('INSERT INTO progress_timetable (code, data, updated_at) VALUES (?1, ?2, ?3) ON CONFLICT(code) DO UPDATE SET data = ?2, updated_at = ?3').bind(o.code, JSON.stringify(tt), nowIso(now)).run();
  }
  return statusOf(db, o.code);
}

function dayOk(day, now) {
  if (!DAY_RE.test(day)) return false;
  const t = Date.parse(day + 'T00:00:00Z');
  if (!Number.isFinite(t)) return false;
  return t <= now.getTime() + 2 * DAY_MS && t >= now.getTime() - (MAX_RANGE_DAYS + 2) * DAY_MS;
}

// Máy học sinh gửi tóm tắt. Mỗi dòng ghi theo kiểu "chỉ tăng": số liệu một ngày không bao giờ giảm (tránh mất dữ liệu khi máy đã xóa bớt nhật ký cũ).
export async function progressPush(db, input, now = new Date()) {
  const { o, src } = await deviceOrder(db, input);
  const st = await db.prepare('SELECT enabled FROM progress_sync WHERE code = ?1').bind(o.code).first();
  if (!st || !st.enabled) throw new HttpError(409, 'Phụ huynh chưa bật cho xem trên điện thoại.');
  const days = Array.isArray(input.days) ? input.days : null;
  if (!days) throw new HttpError(400, 'Dữ liệu gửi lên không hợp lệ.');
  if (days.length > MAX_PUSH_ROWS) throw new HttpError(400, 'Gửi quá nhiều dòng một lần.');
  const stmts = []; let skipped = 0;
  for (const r of days) {
    const day = String(r && r.day || '');
    const subject = String(r && r.subject || '').slice(0, 30);
    const chapter = String(r && r.chapter || '').slice(0, 120);
    const grade = Math.round(Number(r && r.grade));
    const n = (v) => { v = Math.round(Number(v)); return Number.isFinite(v) && v >= 0 && v <= 1_000_000 ? v : NaN; };
    const correct = n(r && r.correct); const total = n(r && r.total); const lessons = n(r && r.lessons); const seconds = n(r && r.seconds);
    if (!dayOk(day, now) || !subject || !chapter || !(grade >= 1 && grade <= 12) || [correct, total, lessons, seconds].some(Number.isNaN) || correct > total) { skipped++; continue; }
    stmts.push(db.prepare(`INSERT INTO progress_daily (code, src, day, subject, grade, chapter, correct, total, lessons, seconds) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10)
      ON CONFLICT(code, src, day, subject, grade, chapter) DO UPDATE SET correct = MAX(correct, ?7), total = MAX(total, ?8), lessons = MAX(lessons, ?9), seconds = MAX(seconds, ?10)`)
      .bind(o.code, src, day, subject, grade, chapter, correct, total, lessons, seconds));
  }
  // Thời gian dùng app: mỗi ngày một dòng cho mỗi thiết bị, ghi kiểu "chỉ tăng" như phần trên.
  const usage = Array.isArray(input.usage) ? input.usage.slice(0, MAX_USAGE_ROWS) : [];
  let usageSaved = 0;
  for (const r of usage) {
    const day = String(r && r.day || '');
    const open = Math.round(Number(r && r.open)); const active = Math.round(Number(r && r.active));
    if (!dayOk(day, now) || !Number.isFinite(open) || !Number.isFinite(active) || open < 0 || active < 0 || open > 86400 || active > open) continue;
    stmts.push(db.prepare(`INSERT INTO progress_usage (code, src, day, open_s, active_s) VALUES (?1,?2,?3,?4,?5)
      ON CONFLICT(code, src, day) DO UPDATE SET open_s = MAX(open_s, ?4), active_s = MAX(active_s, ?5)`).bind(o.code, src, day, open, active));
    usageSaved++;
  }
  for (let i = 0; i < stmts.length; i += 100) await db.batch(stmts.slice(i, i + 100));
  await db.prepare('UPDATE progress_sync SET last_sync = ?1 WHERE code = ?2').bind(nowIso(now), o.code).run();
  return { ok: true, saved: stmts.length - usageSaved, skipped, usage: usageSaved };
}

// Điện thoại phụ huynh xem: mã đơn + số điện thoại đã mua. Giới hạn 5 lần nhập sai mỗi giờ cho mỗi mã máy (dùng chung bảng với nhận khóa).
export async function progressView(db, catalog, input, now = new Date()) {
  const machine = cleanMachine(input.machineId); const phone = String(input.phone || '').replace(/[\s.\-]/g, ''); const code = cleanCode(input.code);
  if (!MACHINE_RE.test(machine)) throw new HttpError(400, 'Không đọc được mã máy.');
  const since = nowIso(new Date(now.getTime() - 3600_000));
  const recent = await db.prepare('SELECT COUNT(*) AS n FROM pin_attempts WHERE machine = ?1 AND ok = 0 AND at > ?2').bind(machine, since).first();
  if (recent.n >= 5) throw new HttpError(429, 'Thử quá nhiều lần. Vui lòng thử lại sau 1 giờ hoặc liên hệ hỗ trợ.');
  const o = /^[A-Z0-9]{6}$/.test(code) && PHONE_RE.test(phone) ? await getOrder(db, code) : null;
  const ok = !!o && o.status === 'paid' && o.phone === phone;
  await db.prepare('INSERT INTO pin_attempts (machine, at, ok) VALUES (?1, ?2, ?3)').bind(machine, nowIso(now), ok ? 1 : 0).run();
  if (!ok) throw new HttpError(404, 'Thông tin không khớp với đơn đã mua.');
  if (await revoked(db, o.code)) throw new HttpError(403, 'Đơn này đã bị thu hồi bản quyền.');

  // Phụ huynh có thể có nhiều đơn (cùng số điện thoại, mỗi đơn một mã khóa): gom tất cả đơn đã thanh toán và chưa bị thu hồi.
  const mine = (await db.prepare("SELECT code, items FROM orders WHERE phone = ?1 AND status = 'paid' ORDER BY created_at").bind(o.phone).all()).results;
  const orders = [];
  for (const r of mine) if (r.code === o.code || !(await revoked(db, r.code))) orders.push(r);
  const codes = orders.map((r) => r.code);
  const byGrade = new Map();
  for (const r of orders) for (const id of JSON.parse(r.items)) {
    const m = /^van-hoa-(\d+)$/.exec(id);
    if (m && !byGrade.has(Number(m[1]))) byGrade.set(Number(m[1]), (catalog.byId[id] && catalog.byId[id].name) || id);
  }
  const courses = [...byGrade].map(([grade, name]) => ({ grade, name })).sort((a, b) => a.grade - b.grade);
  const ph = codes.map((_, i) => `?${i + 1}`).join(',');
  const sts = (await db.prepare(`SELECT code, enabled, goal_daily, goal_weekly, last_sync FROM progress_sync WHERE code IN (${ph})`).bind(...codes).all()).results;
  const enabled = sts.some((x) => x.enabled);
  const gs = sts.find((x) => x.goal_daily);
  const gx = gs ? await db.prepare('SELECT goal_weekend FROM progress_goal_ext WHERE code = ?1').bind(gs.code).first() : null;
  const lastSync = sts.map((x) => x.last_sync).filter(Boolean).sort().pop() || null;
  // Phần thưởng của từng đơn (mỗi bé một khóa, một máy): gắn nhãn khóa/lớp để phụ huynh có nhiều con xem riêng từng bé.
  const rewards = [];
  for (const r of orders) {
    const rw = await rewardOf(db, r.code);
    if (!rw || !rw.on) continue;
    const gs2 = JSON.parse(r.items).map((id) => /^van-hoa-(\d+)$/.exec(id)).filter(Boolean).map((m) => Number(m[1]));
    rewards.push({ code: r.code, grades: gs2, label: gs2.map((g) => (byGrade.get(g) || 'Lớp ' + g)).join(', '), ...rw });
  }
  const timetables = [];
  for (const r of orders) {
    const tt = await timetableOf(db, r.code);
    if (!tt || !Object.keys(tt.grades).length) continue;
    const gs3 = JSON.parse(r.items).map((id) => /^van-hoa-(\d+)$/.exec(id)).filter(Boolean).map((m) => Number(m[1]));
    timetables.push({ code: r.code, grades: gs3, label: gs3.map((g) => (byGrade.get(g) || 'Lớp ' + g)).join(', '), data: tt });
  }
  const base = { timetables, code: o.code, codes, name: o.name, courses, enabled, goals: gs ? { daily: gs.goal_daily, weekend: (gx && gx.goal_weekend) || 80, weekly: gs.goal_weekly, ...(await passOf(db, gs.code)) } : null, lastSync, reward: gs ? await rewardOf(db, gs.code) : null, rewards };
  if (!enabled) return { ...base, rows: [] };

  const today = now.toISOString().slice(0, 10);
  const to = DAY_RE.test(String(input.to || '')) ? String(input.to) : today;
  const defFrom = new Date(Date.parse(to + 'T00:00:00Z') - 6 * DAY_MS).toISOString().slice(0, 10);
  let from = DAY_RE.test(String(input.from || '')) ? String(input.from) : defFrom;
  if (from > to) from = to;
  const minFrom = new Date(Date.parse(to + 'T00:00:00Z') - (MAX_RANGE_DAYS - 1) * DAY_MS).toISOString().slice(0, 10);
  if (from < minFrom) from = minFrom;
  const grade = Math.round(Number(input.grade)) || 0;
  const n = codes.length;
  const sql = `SELECT day, subject, grade, chapter, SUM(correct) AS correct, SUM(total) AS total, SUM(lessons) AS lessons, SUM(seconds) AS seconds FROM progress_daily WHERE code IN (${ph}) AND day >= ?${n + 1} AND day <= ?${n + 2}${grade ? ` AND grade = ?${n + 4}` : ''} GROUP BY day, subject, grade, chapter ORDER BY day LIMIT ?${n + 3}`;
  const rows = (await db.prepare(sql).bind(...codes, from, to, MAX_VIEW_ROWS, ...(grade ? [grade] : [])).all()).results;
  // Thời gian dùng app cộng của mọi thiết bị trong khoảng ngày; không lọc theo lớp hay môn vì app không biết con học môn nào lúc đó.
  const usage = (await db.prepare(`SELECT day, SUM(open_s) AS open, SUM(active_s) AS active FROM progress_usage WHERE code IN (${ph}) AND day >= ?${n + 1} AND day <= ?${n + 2} GROUP BY day ORDER BY day LIMIT ?${n + 3}`).bind(...codes, from, to, MAX_RANGE_DAYS + 2).all()).results;
  return { ...base, from, to, rows, usage };
}
