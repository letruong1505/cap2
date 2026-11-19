/* Hộp thoại mã PIN phụ huynh: nhập PIN, đặt/đổi/tắt, quên PIN (mã khôi phục hoặc xác minh đơn hàng online). */
(function () {
  const PIN = window.VungPin;
  const store = () => { try { return window.localStorage; } catch (e) { return null; } };
  const UNLOCK_MS = 5 * 60 * 1000;
  let unlockedUntil = 0;

  function h(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => { if (v !== false && v != null) n.setAttribute(k, v); });
    kids.forEach((k) => n.append(k));
    return n;
  }
  const pinInput = (label) => h('input', { type: 'password', inputmode: 'numeric', maxlength: '6', autocomplete: 'off', placeholder: label, 'aria-label': label });
  const mins = (ms) => Math.max(1, Math.ceil(ms / 60000));

  /* Mở hộp thoại; build(box, close) dựng nội dung, close(value) đóng và trả giá trị. */
  function modal(build) {
    return new Promise((resolve) => {
      const back = h('div', { class: 'pin-back' });
      const box = h('div', { class: 'pin-box', role: 'dialog', 'aria-modal': 'true' });
      const close = (v) => { back.remove(); resolve(v); };
      back.append(box); document.body.append(back);
      build(box, close);
      const first = box.querySelector('input'); if (first) first.focus();
    });
  }
  const msgLine = () => h('p', { class: 'pin-msg', role: 'alert' });
  const actions = (...b) => h('div', { class: 'pin-actions' }, ...b);
  const btn = (text, cls, fn) => { const b = h('button', { type: 'button', class: cls || '' }, text); b.addEventListener('click', fn); return b; };

  /* Hiện mã khôi phục một lần; chỉ đóng khi phụ huynh xác nhận đã chép lại. */
  function showRecovery(code) {
    return modal((box, close) => {
      box.append(h('h2', {}, 'Mã khôi phục'),
        h('p', {}, 'Hãy chép mã này ra giấy và cất cẩn thận. Mã chỉ hiện một lần. Khi quên mã PIN, nhập mã này để đặt PIN mới.'),
        h('p', { class: 'pin-code' }, code));
      const cb = h('input', { type: 'checkbox', id: 'pin-ack' });
      const ok = btn('Đã chép xong', 'primary', () => close(true)); ok.disabled = true;
      cb.addEventListener('change', () => { ok.disabled = !cb.checked; });
      box.append(h('label', {}, cb, ' Tôi đã chép lại mã khôi phục'), actions(ok));
    });
  }

  /* Đặt PIN mới (lần đầu, đổi, hoặc sau khi khôi phục). Trả về PIN hợp lệ hoặc null nếu hủy. */
  function askNewPin(title) {
    return modal((box, close) => {
      const a = pinInput('Mã PIN mới (4–6 chữ số)'); const b = pinInput('Nhập lại mã PIN'); const m = msgLine();
      const ok = btn('Lưu', 'primary', () => {
        if (!PIN.validPin(a.value)) { m.textContent = 'Mã PIN gồm 4 đến 6 chữ số.'; return; }
        if (a.value !== b.value) { m.textContent = 'Hai lần nhập chưa giống nhau.'; return; }
        close(a.value);
      });
      box.append(h('h2', {}, title), a, b, m, actions(btn('Hủy', '', () => close(null)), ok));
    });
  }

  async function setupPin(title) {
    const pin = await askNewPin(title || 'Đặt mã PIN phụ huynh');
    if (!pin) return false;
    const rec = await PIN.setPin(store(), pin);
    unlockedUntil = Date.now() + UNLOCK_MS;
    await showRecovery(rec);
    return true;
  }

  /* Quên PIN: khôi phục bằng mã khôi phục hoặc xác minh đơn hàng qua máy chủ. */
  function forgot() {
    return modal((box, close) => {
      const m = msgLine();
      const newPin = pinInput('Mã PIN mới (4–6 chữ số)');
      const code = h('input', { type: 'text', autocomplete: 'off', placeholder: 'Mã khôi phục XXXX-XXXX-XXXX', 'aria-label': 'Mã khôi phục' });
      const phone = h('input', { type: 'tel', autocomplete: 'off', placeholder: 'Số điện thoại đã mua', 'aria-label': 'Số điện thoại' });
      const order = h('input', { type: 'text', autocomplete: 'off', placeholder: 'Mã đơn 6 ký tự (trong nội dung chuyển khoản NL …)', 'aria-label': 'Mã đơn' });
      const finish = async (res) => {
        if (!res.ok) { m.textContent = res.locked ? `Nhập sai nhiều lần. Thử lại sau ${mins(res.remainMs)} phút.` : (res.error || 'Mã khôi phục chưa đúng.'); return; }
        close(true); unlockedUntil = Date.now() + UNLOCK_MS; await showRecovery(res.recovery);
      };
      const viaCode = btn('Khôi phục bằng mã', 'primary', async () => {
        if (!PIN.validPin(newPin.value)) { m.textContent = 'Mã PIN mới gồm 4 đến 6 chữ số.'; return; }
        finish(await PIN.recover(store(), code.value, newPin.value));
      });
      const viaOrder = btn('Xác minh đơn hàng online', '', async () => {
        if (!PIN.validPin(newPin.value)) { m.textContent = 'Mã PIN mới gồm 4 đến 6 chữ số.'; return; }
        if (!window.vungBai || !window.vungBai.pinReset) { m.textContent = 'Phiên bản này chưa hỗ trợ.'; return; }
        m.textContent = 'Đang xác minh…';
        const r = await window.vungBai.pinReset({ phone: phone.value, code: order.value });
        if (r.offline) { m.textContent = 'Không kết nối được máy chủ. Hãy kiểm tra mạng rồi thử lại.'; return; }
        if (!r.ok) { m.textContent = r.error; return; }
        finish(await PIN.resetVerified(store(), newPin.value));
      });
      box.append(h('h2', {}, 'Quên mã PIN'), newPin,
        h('h3', {}, 'Cách 1: có mã khôi phục'), code, viaCode,
        h('h3', {}, 'Cách 2: xác minh bằng đơn hàng (cần mạng)'), phone, order, viaOrder, m,
        actions(btn('Đóng', '', () => close(false))));
    });
  }

  /* Cổng vào khu vực phụ huynh. Trả về true khi được phép. */
  async function ensureUnlocked() {
    if (!PIN || !PIN.isSet(store())) return true;
    if (Date.now() < unlockedUntil) return true;
    for (;;) {
      const r = await modal((box, close) => {
        const i = pinInput('Mã PIN phụ huynh'); const m = msgLine();
        const go = async () => {
          const v = await PIN.verify(store(), i.value);
          if (v.ok) return close('ok');
          m.textContent = v.locked ? `Nhập sai nhiều lần. Thử lại sau ${mins(v.remainMs)} phút.` : `Mã PIN chưa đúng. Còn ${v.left} lần thử.`;
          i.value = ''; i.focus();
        };
        i.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
        box.append(h('h2', {}, 'Nhập mã PIN phụ huynh'), i, m,
          actions(btn('Hủy', '', () => close('cancel')), btn('Quên mã PIN', '', () => close('forgot')), btn('Mở', 'primary', go)));
      });
      if (r === 'ok') { unlockedUntil = Date.now() + UNLOCK_MS; return true; }
      if (r === 'forgot') { if (await forgot()) return true; continue; }
      return false;
    }
  }

  /* Khối cài đặt PIN trong màn hình báo cáo. */
  function renderSettings(box, rerender) {
    box.replaceChildren();
    const on = PIN.isSet(store());
    box.append(h('h2', {}, 'Mã PIN phụ huynh'),
      h('p', { class: 'meta' }, on ? 'Đang bật: cần nhập PIN để xem báo cáo tuần và đổi mục tiêu.' : 'Chưa bật. Đặt PIN để học sinh không tự xem báo cáo hoặc đổi mục tiêu.'));
    if (!on) box.append(btn('Đặt mã PIN', 'primary', async () => { if (await setupPin()) rerender(); }));
    else {
      box.append(btn('Đổi mã PIN', '', async () => { if (await setupPin('Đổi mã PIN')) rerender(); }),
        btn('Tắt mã PIN', '', async () => {
          const ok = await modal((b, close) => {
            b.append(h('h2', {}, 'Tắt mã PIN?'), h('p', {}, 'Ai dùng máy cũng xem được báo cáo và đổi mục tiêu.'),
              actions(btn('Giữ PIN', '', () => close(false)), btn('Tắt PIN', 'primary', () => close(true))));
          });
          if (ok) { PIN.clear(store()); rerender(); }
        }));
    }
  }

  window.VungPinUI = { ensureUnlocked, renderSettings };
})();
