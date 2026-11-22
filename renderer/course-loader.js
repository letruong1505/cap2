// Nạp nội dung khóa Kỹ năng đã tải về máy vào các biến của giao diện (window.TUDUY, GIA_SU_AI, AI_WORK_*).
// Bản build tách gói chỉ giữ tiêu đề các bài trả phí; nội dung nằm trong gói của khóa, chỉ trả về khi bản quyền có đúng khóa đó.
// Bản build đầy đủ thì cầu nối trả rỗng (giao diện đã có sẵn nội dung), nên các hàm dưới đây không làm gì.
(function () {
  'use strict';
  const merged = {};

  // files: { "TUDUY.k1218": "<json các bài>", "GIA_SU_AI": "<json>" }. Bài nào đã có thì được thay bằng bản đầy đủ.
  function merge(files) {
    for (const [path, json] of Object.entries(files || {})) {
      let lessons; try { lessons = JSON.parse(json); } catch { continue; }
      const parts = path.split('.');
      if (!/^[A-Z_]+$/.test(parts[0])) continue;
      const root = (window[parts[0]] = window[parts[0]] || {});
      const target = parts[1] ? (root[parts[1]] = root[parts[1]] || {}) : root;
      for (const [k, v] of Object.entries(lessons)) target[k] = v;
    }
  }

  // Trả về true nếu nội dung khóa đã sẵn sàng (đã nạp, hoặc không cần nạp); false nếu chưa có quyền hoặc chưa tải về máy.
  async function load(id) {
    if (merged[id]) return true;
    if (!window.vungBai || !window.vungBai.courseContent) return true;
    let r = null;
    try { r = await window.vungBai.courseContent(id); } catch { r = null; }
    if (!r || !r.ok) return false;
    merge(r.files);
    merged[id] = true;
    return true;
  }

  // Có gói mới thì lần mở sau nạp lại.
  if (window.vungBai && window.vungBai.onPacks) window.vungBai.onPacks((st) => { if (st && st.state === 'ready') for (const k of Object.keys(merged)) delete merged[k]; });

  // Khóa có gói nội dung riêng; khớp tools/build-packs.js và worker/src/pack.js.
  const PACKED = ['tu-duy-lap-trinh-scratch', 'tu-duy-lap-trinh-python', 'gia-su-ai', 'ai-nguoi-di-lam-claude', 'ai-nguoi-di-lam-chatgpt', 'ai-nguoi-di-lam-gemini'];
  const MSG_LOADING = 'Đang tải nội dung bài học…';
  const MSG_MISSING = 'Nội dung khóa học này chưa được tải về máy. Hãy giữ kết nối mạng; phần mềm sẽ tự tải, rồi mở lại bài.';

  // Dùng ở màn hình bài học: bài đã mua mà chưa có nội dung (html) thì nạp gói rồi vẽ lại; không được thì báo chưa tải.
  // render(): vẽ lại bài; show(text): hiện thông báo thay cho bài; retried: đã nạp một lần rồi mà vẫn thiếu thì không lặp nữa.
  function ensureLesson(id, lesson, owned, render, show, retried) {
    if (!lesson || lesson.html || !owned) return false;
    if (retried) { show(MSG_MISSING); return true; }
    show(MSG_LOADING);
    load(id).then((ok) => {
      if (ok) { render(); return; }
      if (window.vungBai && window.vungBai.packsSync) window.vungBai.packsSync().catch(() => {});
      show(MSG_MISSING);
    });
    return true;
  }

  window.NLCourse = { load, merge, ensureLesson, PACKED, MSG_MISSING };
})();
