/* Cho phụ huynh xem kết quả học trên điện thoại.
   Máy học sinh (khi phụ huynh bật) gửi bản tóm tắt theo ngày × môn × lớp × chương lên máy chủ Nam Linh; không gửi từng câu trả lời.
   Phần logic thuần (aggregate, buildReport, codeFromLicense) dùng được cả trong Node để kiểm thử. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VungProgressSync = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const KEY = 'vungbai.sync.v1';
  const DAY = 86400000;
  const MAX_DAYS = 120; // chỉ gửi 120 ngày gần nhất
  const MAX_ROWS = 1500; // khớp giới hạn của máy chủ

  const isoOf = (t) => { const d = new Date(t); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  const fromIso = (v) => { const [y, m, d] = String(v).split('-').map(Number); return new Date(y, m - 1, d).getTime(); };
  const startOfDay = (t) => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };

  /* Mã đơn (6 ký tự) từ id khóa "NL-3KAHFK" (có thể nhiều id nối bằng dấu phẩy: lấy cái đầu). */
  function codeFromLicense(lic) {
    const m = String(lic && lic.id || '').toUpperCase().match(/NL-([A-Z0-9]{6})/);
    return m ? m[1] : '';
  }

  /* Gom nhật ký làm bài thành các dòng tóm tắt theo ngày (giờ địa phương) × môn × lớp × chương. */
  function aggregate(attempts, now) {
    now = now == null ? Date.now() : now;
    const from = startOfDay(now) - (MAX_DAYS - 1) * DAY;
    const map = new Map();
    (attempts || []).forEach((a) => {
      if (!a || !(a.t >= from) || !a.subject || !(a.grade >= 1)) return;
      const chapter = String(a.chapter || a.lesson || '').slice(0, 120);
      if (!chapter) return;
      const day = isoOf(a.t);
      const k = [day, a.subject, a.grade, chapter].join('|');
      const r = map.get(k) || { day, subject: String(a.subject), grade: Number(a.grade), chapter, correct: 0, total: 0, lessons: 0, seconds: 0 };
      r.correct += Math.max(0, Math.round(a.correct) || 0); r.total += Math.max(0, Math.round(a.total) || 0);
      r.lessons += 1; r.seconds += Math.max(0, Math.round(a.seconds) || 0);
      map.set(k, r);
    });
    const rows = [...map.values()].filter((r) => r.correct <= r.total).sort((a, b) => (a.day < b.day ? 1 : a.day > b.day ? -1 : 0));
    return rows.slice(0, MAX_ROWS);
  }

  /* Báo cáo từ các dòng tóm tắt của máy chủ; cùng hình dạng với VungProgress.report để dùng lại giao diện. */
  function buildReport(rows, opts, goals) {
    opts = opts || {};
    const from = startOfDay(opts.from); const to = startOfDay(opts.to);
    const subject = opts.subject || ''; const grade = opts.grade || 0;
    const pct = (x) => (x.total ? Math.round((100 * x.correct) / x.total) : 0);
    const list = (rows || []).filter((r) => (!grade || r.grade === grade) && (!subject || r.subject === subject));
    const byDay = new Map();
    list.forEach((r) => { const d = byDay.get(r.day) || { correct: 0, total: 0, lessons: 0 }; d.correct += r.correct; d.total += r.total; d.lessons += r.lessons; byDay.set(r.day, d); });
    const g = goals || { daily: 20, weekly: 5 };
    const days = [];
    for (let t = from; t <= to && days.length < 366; t += DAY) {
      const d = new Date(t); d.setHours(0, 0, 0, 0);
      const x = byDay.get(isoOf(d.getTime())) || { correct: 0, total: 0, lessons: 0 };
      const day = { t: d.getTime(), correct: x.correct, total: x.total, lessons: x.lessons };
      day.wrong = day.total - day.correct; day.pct = pct(day); day.reached = !subject && day.total >= g.daily;
      days.push(day);
    }
    const subj = {}, chap = {};
    let correct = 0, total = 0, seconds = 0, attempts = 0;
    list.forEach((r) => {
      correct += r.correct; total += r.total; seconds += r.seconds; attempts += r.lessons;
      const sk = r.subject + '|' + r.grade;
      const s = subj[sk] || (subj[sk] = { subject: r.subject, grade: r.grade, correct: 0, total: 0, lessons: 0 });
      s.correct += r.correct; s.total += r.total; s.lessons += r.lessons;
      const ck = sk + '|' + r.chapter;
      const c = chap[ck] || (chap[ck] = { subject: r.subject, grade: r.grade, name: r.chapter, correct: 0, total: 0 });
      c.correct += r.correct; c.total += r.total;
    });
    const subjects = Object.values(subj).map((x) => Object.assign(x, { wrong: x.total - x.correct, pct: pct(x) })).sort((a, b) => b.total - a.total);
    const weak = Object.values(chap).filter((c) => c.total >= 5).map((c) => Object.assign(c, { pct: pct(c) })).filter((c) => c.pct < 70).sort((a, b) => a.pct - b.pct).slice(0, 5);
    return {
      from, to, days, goals: g, subject, grade, correct, wrong: total - correct, total, pct: pct({ correct, total }),
      minutes: Math.round(seconds / 60), attempts, activeDays: days.filter((d) => d.total > 0).length, subjects, weak,
    };
  }

  const api = { KEY, aggregate, buildReport, codeFromLicense, isoOf, fromIso };
  if (typeof window === 'undefined' || !window.document) return api;

  /* ---------- Phần chạy trên máy (cần giao diện) ---------- */
  const P = window.VungProgress;
  const store = () => { try { return window.localStorage; } catch (e) { return null; } };
  const bridge = () => window.vungBai;
  const readState = () => { try { return JSON.parse(store().getItem(KEY) || '{}') || {}; } catch (e) { return {}; } };
  const writeState = (s) => { try { store().setItem(KEY, JSON.stringify(s)); } catch (e) { /* bỏ qua */ } };
  const supported = () => !!(bridge() && bridge().progressPush && bridge().progressSettings);

  async function currentCode() {
    try { return codeFromLicense(await bridge().loadLicense()); } catch (e) { return ''; }
  }

  let timer = null; let busy = false;
  async function push() {
    const st = readState();
    if (!st.enabled || !supported() || busy) return { ok: false, skipped: true };
    busy = true;
    try {
      const code = await currentCode();
      if (!code) return { ok: false, skipped: true };
      const data = P.load(store());
      if (JSON.stringify(st.goals || null) !== JSON.stringify(data.goals)) {
        const g = await bridge().progressSettings({ code, goals: data.goals });
        if (g.ok) { st.goals = data.goals; writeState(st); }
      }
      const r = await bridge().progressPush({ code, days: aggregate(data.attempts) });
      if (r.ok) { st.lastOk = Date.now(); writeState(st); }
      else if (r.error && /chưa bật/i.test(r.error)) { st.enabled = false; writeState(st); } // phụ huynh đã tắt ở nơi khác
      return r;
    } catch (e) { return { ok: false, offline: true }; } finally { busy = false; }
  }
  /* Gửi sau khi học xong một bài (gộp nhiều lần nộp liên tiếp thành một lần gửi). */
  function schedule() {
    if (!readState().enabled) return;
    clearTimeout(timer); timer = setTimeout(push, 8000);
  }

  async function enable() {
    if (!supported()) return { ok: false, error: 'Phiên bản này chưa hỗ trợ.' };
    const code = await currentCode();
    if (!code) return { ok: false, error: 'Chỉ dùng được với khóa mua trực tuyến trên máy này.' };
    const r = await bridge().progressSettings({ code, enabled: true });
    if (!r.ok) return r;
    writeState({ enabled: true });
    const p = await push();
    return { ok: true, pushed: !!(p && p.ok) };
  }
  async function disable(purge) {
    const code = await currentCode();
    const r = code ? await bridge().progressSettings({ code, enabled: false, purge: purge === true }) : { ok: false, error: 'Không tìm thấy khóa.' };
    if (r.ok || !code) writeState({ enabled: false });
    return r;
  }
  const info = () => readState();

  /* Khóa cấp trực tiếp (USB) chưa có trong hệ thống: khách nhập số điện thoại phụ huynh để đăng ký, rồi bật chia sẻ. */
  function registerForm(box, msg, rerender) {
    const h = (tag, attrs, ...kids) => { const n = document.createElement(tag); Object.entries(attrs || {}).forEach(([k, v]) => { if (v != null && v !== false) n.setAttribute(k, v); }); kids.forEach((k) => n.append(k)); return n; };
    box.querySelectorAll('.reg-form').forEach((n) => n.remove());
    const phone = h('input', { type: 'tel', maxlength: '14', placeholder: 'Số điện thoại phụ huynh', autocomplete: 'off', 'aria-label': 'Số điện thoại phụ huynh' });
    const go = h('button', { type: 'button', class: 'primary' }, 'Đăng ký khóa và bật');
    const form = h('div', { class: 'reg-form' }, h('p', { class: 'meta' }, 'Khóa của máy này được cấp trực tiếp nên chưa có trong hệ thống. Nhập số điện thoại phụ huynh để đăng ký; phụ huynh dùng số này (và mã khóa) để xem kết quả trên điện thoại.'), h('div', { class: 'license-form' }, phone, go));
    go.addEventListener('click', async () => {
      const p = phone.value.replace(/[\s.\-]/g, '');
      if (!/^(0|\+84)\d{9}$/.test(p)) { msg.textContent = 'Kiểm tra lại số điện thoại.'; return; }
      msg.textContent = 'Đang đăng ký...';
      const r = await bridge().registerLegacy({ phone: p });
      if (!r.ok) { msg.textContent = r.offline ? 'Không có mạng. Thử lại khi có mạng.' : (r.error || 'Chưa đăng ký được.'); return; }
      const e = await enable();
      if (e.ok) rerender(); else msg.textContent = e.error || 'Đã đăng ký khóa nhưng chưa bật được. Thử bật lại.';
    });
    msg.before(form);
  }

  /* Hộp bật/tắt trong màn hình báo cáo. guard(title, text, nhãn) trả về Promise<boolean> (hỏi lại mã PIN nếu có). */
  function renderBox(box, rerender) {
    const h = (tag, attrs, ...kids) => { const n = document.createElement(tag); Object.entries(attrs || {}).forEach(([k, v]) => { if (v != null && v !== false) n.setAttribute(k, v); }); kids.forEach((k) => n.append(k)); return n; };
    box.replaceChildren();
    box.append(h('h2', {}, 'Cho phụ huynh xem trên điện thoại'));
    if (!supported()) { box.append(h('p', { class: 'meta' }, 'Phiên bản này chưa hỗ trợ.')); return; }
    const st = readState();
    box.append(h('p', { class: 'meta' }, 'Khi bật, máy này gửi bản tóm tắt theo ngày (số câu đúng/sai theo môn, lớp, chương) lên máy chủ của Nam Linh. Phụ huynh mở ứng dụng trên điện thoại, nhập mã đơn và số điện thoại đã mua để xem. Không gửi từng câu trả lời. Tắt hoặc xóa bất cứ lúc nào.'));
    const msg = h('p', { class: 'meta', role: 'status' });
    const guard = (t, x, l) => (window.VungPinUI && window.VungPinUI.guard ? window.VungPinUI.guard(t, x, l) : Promise.resolve(true));
    const run = async (label, fn) => { msg.textContent = label; const r = await fn(); return r; };
    if (st.enabled) {
      box.append(h('p', {}, st.lastOk ? `Đang bật. Gửi gần nhất lúc ${new Date(st.lastOk).toLocaleString('vi-VN')}.` : 'Đang bật. Chưa gửi lần nào.'));
      const now = h('button', { type: 'button' }, 'Gửi ngay');
      const off = h('button', { type: 'button' }, 'Tắt chia sẻ');
      const del = h('button', { type: 'button' }, 'Tắt và xóa dữ liệu đã gửi');
      now.addEventListener('click', async () => { const r = await run('Đang gửi...', push); if (r.ok) rerender(); else msg.textContent = r.offline ? 'Không có mạng. Sẽ gửi lại sau.' : (r.error || 'Chưa gửi được.'); });
      off.addEventListener('click', async () => {
        if (!await guard('Tắt chia sẻ?', 'Nhập mã PIN hiện tại để tắt. Phụ huynh sẽ không xem được trên điện thoại nữa.', 'Tắt')) return;
        const r = await run('Đang tắt...', () => disable(false)); if (r.ok) rerender(); else msg.textContent = r.offline ? 'Không có mạng, chưa tắt được. Thử lại khi có mạng.' : (r.error || 'Chưa tắt được.');
      });
      del.addEventListener('click', async () => {
        if (!await guard('Tắt và xóa dữ liệu?', 'Nhập mã PIN hiện tại. Dữ liệu đã gửi lên máy chủ sẽ bị xóa; dữ liệu trên máy này vẫn còn.', 'Tắt và xóa')) return;
        const r = await run('Đang xóa...', () => disable(true)); if (r.ok) rerender(); else msg.textContent = r.offline ? 'Không có mạng, chưa xóa được. Thử lại khi có mạng.' : (r.error || 'Chưa xóa được.');
      });
      box.append(h('div', { class: 'license-form' }, now, off, del));
    } else {
      const on = h('button', { type: 'button', class: 'primary' }, 'Bật cho phụ huynh xem trên điện thoại');
      on.addEventListener('click', async () => {
        if (!await guard('Bật cho phụ huynh xem?', 'Nhập mã PIN hiện tại để bật chia sẻ bản tóm tắt học tập.', 'Bật')) return;
        const r = await run('Đang bật...', enable);
        if (r.ok) rerender();
        else if (/không tìm thấy đơn/i.test(r.error || '') && bridge().registerLegacy) registerForm(box, msg, rerender);
        else msg.textContent = r.offline ? 'Không có mạng. Thử lại khi có mạng.' : (r.error || 'Chưa bật được.');
      });
      box.append(on);
    }
    box.append(msg);
  }

  setTimeout(() => { if (readState().enabled) push(); }, 8000);
  return Object.assign(api, { push, schedule, enable, disable, info, renderBox, supported });
});
