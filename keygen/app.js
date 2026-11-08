const $ = (id) => document.getElementById(id);
function setState(s) {
  $('keystate').textContent = s.ready ? 'Đã có khoá riêng: ' + (s.file || '') : 'Chưa chọn khoá riêng. Hãy chọn file private.pem.' + (s.error ? ' ' + s.error : '');
}
window.kg.status().then(setState);
$('choose').addEventListener('click', async () => setState(await window.kg.choose()));
const d = new Date(); d.setFullYear(d.getFullYear() + 1);
$('expires').value = d.toISOString().slice(0, 10);
$('issue').addEventListener('click', async () => {
  const grades = [...document.querySelectorAll('#grades input[type=checkbox][value]:checked')].map((c) => c.value);
  const r = await window.kg.issue({ owner: $('owner').value, grades, allGrades: $('all').checked, machine: $('machine').value, anyMachine: $('any').checked, expires: $('expires').value });
  const msg = $('msg');
  if (r.error) { msg.className = 'err'; msg.textContent = r.error; return; }
  $('out').value = r.key;
  msg.className = 'ok'; msg.textContent = 'Đã tạo khoá ' + r.id + '. Nhấn Sao chép rồi gửi cho khách.';
});
$('copy').addEventListener('click', () => { if ($('out').value) window.kg.copy($('out').value); });
