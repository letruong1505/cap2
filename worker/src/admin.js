// Trang quản trị đơn: một trang HTML, nhập mật khẩu quản trị (ADMIN_TOKEN) để xem đơn, duyệt tay, hủy, cấp lại key.
const PAGE = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quản trị đơn - Nam Linh Educenter</title>
<style nonce="__N__">
body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#f4f7fb;color:#1c2733}
header{background:#14304f;color:#fff;padding:14px 24px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:18px;margin:0;flex:1}
main{max-width:1400px;margin:0 auto;padding:20px 24px}
input,select,button{font:inherit;padding:8px 12px;border-radius:8px;border:1px solid #c5d0dc;background:#fff}
button{cursor:pointer;font-weight:600}button.p{background:#14304f;color:#fff;border-color:#14304f}
button.d{color:#9b2b1f}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;margin:14px 0}
th,td{padding:9px 12px;border-bottom:1px solid #e3e9f0;text-align:left;vertical-align:top;font-size:14px}
th{background:#eaf0f7}
.st{padding:2px 10px;border-radius:99px;font-size:12.5px;font-weight:700;display:inline-block}
.gone{text-decoration:line-through;color:#8a8f96}button.sm{padding:2px 8px;font-size:12.5px;margin-left:6px}.it{margin:2px 0}.on{background:#d9f2e1}.off{background:#eee}.rv{background:#f6d5d1}.pending{background:#fff4d6}.underpaid{background:#ffe0d6}.paid{background:#d9f2e1}.cancelled{background:#e6e6e6}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
#msg{min-height:22px;color:#9b2b1f}
code{font-size:12.5px;word-break:break-all}
h2{margin:26px 0 0;font-size:17px}
</style></head><body>
<header><h1>Quản trị đơn - Nam Linh Educenter</h1><div class="row"><input id="tok" type="password" placeholder="Mật khẩu quản trị" autocomplete="off"><button class="p" id="go">Vào</button></div></header>
<main><div class="row"><select id="st"><option value="">Tất cả trạng thái</option><option value="pending">Chờ thanh toán</option><option value="underpaid">Chuyển thiếu</option><option value="paid">Đã thanh toán</option><option value="cancelled">Đã hủy</option></select>
<input id="q" placeholder="Tìm tên, SĐT, mã đơn, mã máy"><button id="rf">Tải lại</button></div><div id="msg" role="status"></div>
<div id="orders"></div><h2>Mã đối tác</h2><div class="row"><input id="pc" placeholder="Mã, ví dụ DT-HOAI" maxlength="20"><input id="pp" placeholder="Tên đối tác" maxlength="60"><input id="pn" type="number" value="20" min="1" max="99" style="width:90px" title="Giảm (%)"><input id="pm" type="number" value="5" min="1" max="1000" style="width:90px" title="Số máy tối đa" placeholder="Số máy"><button class="p" id="pcAdd">Tạo mã</button></div><div id="partners"></div><h2>Giao dịch chưa khớp đơn hoặc cần xử lý</h2><div id="tx"></div></main>
<script nonce="__N__">
(function(){
var T=document.getElementById('tok'),msg=document.getElementById('msg'),CAT={};
var LBL={pending:'Chờ thanh toán',underpaid:'Chuyển thiếu',paid:'Đã thanh toán',cancelled:'Đã hủy'};
try{T.value=sessionStorage.getItem('nl-admin')||''}catch(e){}
function money(n){return Number(n||0).toLocaleString('vi-VN')+' đ'}
function api(method,url,data){return fetch(url,{method:method,headers:{'authorization':'Bearer '+T.value,'content-type':'application/json'},body:data?JSON.stringify(data):undefined}).then(function(r){return r.json().then(function(j){if(!r.ok)throw new Error(j.error||'Lỗi');return j})})}
function el(t,a){var e=document.createElement(t);for(var k in (a||{})){if(k==='class')e.className=a[k];else if(k==='onclick')e.onclick=a[k];else e.setAttribute(k,a[k])}for(var i=2;i<arguments.length;i++){var c=arguments[i];if(c==null)continue;e.append(c.nodeType?c:document.createTextNode(String(c)))}return e}
function act(o,what,extra,after){return api('POST','/api/admin/orders/'+o.code+'/'+what,extra).then(after||load).catch(function(e){msg.textContent=e.message})}
function devCell(o){
  var c=el('div',{});
  if(!o.devices.length)c.append(el('div',{},o.status==='paid'?'Chưa thấy máy nào mở phần mềm':'-'));
  o.devices.forEach(function(d){c.append(el('div',{},el('code',{},d.machine),' ',el('span',{class:'st '+(d.online?'on':'off')},d.online?'Đang online':'Offline'),el('div',{},(d.online?'Bản '+(d.version||'?')+', đang mở phần mềm':'Mở gần nhất '+new Date(d.last_seen).toLocaleString('vi-VN')+(d.version?', bản '+d.version:'')))))});
  c.append(el('div',{},'Máy đặt đơn: ',el('code',{},o.machine)));
  return c}
function itemsCell(o,names){
  var c=el('div',{});
  JSON.parse(o.items).forEach(function(id){
    var nm=CAT[id]?CAT[id].name:id,rv=(o.item_revoked||[]).filter(function(r){return r.item===id})[0],row=el('div',{class:'it'});
    if(rv){
      row.append(el('span',{class:'gone'},nm),' ',el('span',{class:'st rv'},'Đã thu hồi'),el('button',{class:'p sm',onclick:function(){if(confirm('Khôi phục khóa học "'+nm+'" của đơn '+o.code+'?'))api('POST','/api/admin/orders/'+o.code+'/restore',{item:id}).then(load).catch(function(e){msg.textContent=e.message})}},'Khôi phục'));
      if(rv.reason)row.append(el('div',{},rv.reason+' ('+new Date(rv.at).toLocaleString('vi-VN')+')'))
    }else{
      row.append(nm,o.prices&&o.prices[id]?el('small',{},' · đã trả '+money(o.prices[id].paid)):null);
      if(o.status==='paid'&&!o.revoked&&refundOpen(o))row.append(el('button',{class:'d sm',onclick:function(){var x=prompt('THU HỒI RIÊNG khóa học "'+nm+'" của '+o.name+' ('+o.phone+'), đơn '+money(o.amount)+'.\\nCác khóa khác trong đơn vẫn dùng bình thường.\\nGõ lại mã đơn '+o.code+' để xác nhận:');if(x===null)return;if(x.trim().toUpperCase().replace(/^NL-/,'')!==o.code){alert('Mã đơn không khớp, chưa thu hồi.');return}var r=prompt('Lý do (hoàn tiền một phần...):','Hoàn tiền một phần');if(r===null)return;api('POST','/api/admin/orders/'+o.code+'/revoke',{item:id,reason:r}).then(load).catch(function(e){msg.textContent=e.message})}},'Thu hồi'))
    }
    c.append(row)});
  return c}
function showKey(k){window.prompt('Khóa kích hoạt (sao chép):',k)}
function refundOpen(o){return !!o.paid_at&&Date.now()-new Date(o.paid_at).getTime()<=7*864e5}
function loadPartners(){
  api('GET','/api/admin/partner-codes').then(function(d){
    var box=document.getElementById('partners');box.replaceChildren();
    var tb=el('table',{},el('tr',{},el('th',{},'Mã'),el('th',{},'Đối tác'),el('th',{},'Giảm'),el('th',{},'Máy đã dùng'),el('th',{},'Trạng thái'),el('th',{},'Số đơn đã dùng'),el('th',{},'')));
    d.partners.forEach(function(p){
      tb.append(el('tr',{},el('td',{},el('code',{},p.code)),el('td',{},p.partner),el('td',{},p.percent+'%'),el('td',{},(p.machines||0)+'/'+(p.max_machines||'∞')+' máy'),el('td',{},el('span',{class:'st '+(p.active?'on':'off')},p.active?'Đang bật':'Đã tắt')),el('td',{},String(p.used||0)),el('td',{},el('button',{onclick:function(){if(!confirm((p.active?'Tắt':'Bật')+' mã '+p.code+'?'))return;api('POST','/api/admin/partner-codes/'+encodeURIComponent(p.code)+'/active',{active:!p.active}).then(loadPartners).catch(function(e){msg.textContent=e.message})}},p.active?'Tắt':'Bật'))));
    });
    box.append(d.partners.length?tb:el('p',{},'Chưa có mã đối tác.'));
  }).catch(function(e){msg.textContent=e.message});
}
document.getElementById('pcAdd').onclick=function(){
  api('POST','/api/admin/partner-codes',{code:document.getElementById('pc').value,partner:document.getElementById('pp').value,percent:Number(document.getElementById('pn').value),maxMachines:Number(document.getElementById('pm').value)})
    .then(function(){document.getElementById('pc').value='';document.getElementById('pp').value='';loadPartners()})
    .catch(function(e){msg.textContent=e.message});
};
function load(){
  msg.textContent='';
  loadPartners();
  try{sessionStorage.setItem('nl-admin',T.value)}catch(e){}
  var u='/api/admin/orders?status='+encodeURIComponent(document.getElementById('st').value)+'&q='+encodeURIComponent(document.getElementById('q').value);
  api('GET',u).then(function(d){
    CAT=d.catalog;var box=document.getElementById('orders');box.replaceChildren();
    var tb=el('table',{},el('tr',{},el('th',{},'Mã đơn'),el('th',{},'Phụ huynh'),el('th',{},'Khóa học'),el('th',{},'Tiền'),el('th',{},'Trạng thái'),el('th',{},'Máy đã dùng'),el('th',{},'Thao tác')));
    d.orders.forEach(function(o){
      var names=JSON.parse(o.items).map(function(i){return CAT[i]?CAT[i].name:i}).join(', ');
      var ops=el('div',{class:'row'});
      if(o.status!=='paid'&&o.status!=='cancelled'){ops.append(el('button',{class:'p',onclick:function(){if(confirm('Xác nhận đã nhận đủ tiền và cấp key cho '+o.code+'?'))act(o,'approve',{note:'Duyệt tay'},function(r){showKey(r.key);load()})}},'Duyệt tay'));ops.append(el('button',{class:'d',onclick:function(){if(confirm('Hủy đơn '+o.code+'?'))act(o,'cancel',{})}},'Hủy'))}
      if(o.status==='paid'&&!o.revoked&&refundOpen(o)){ops.append(el('button',{class:'d',onclick:function(){var c=prompt('THU HỒI khóa của '+o.name+' ('+o.phone+'), '+names+', '+money(o.amount)+'.\\nGõ lại mã đơn '+o.code+' để xác nhận:');if(c===null)return;if(c.trim().toUpperCase().replace(/^NL-/,'')!==o.code){alert('Mã đơn không khớp, chưa thu hồi.');return}var r=prompt('Lý do thu hồi (hoàn tiền, vi phạm...):','Hoàn tiền');if(r===null)return;act(o,'revoke',{reason:r})}},'Thu hồi'))}
      if(o.revoked){ops.append(el('button',{class:'p',onclick:function(){if(confirm('Khôi phục khóa của đơn '+o.code+'? Máy khách dùng lại được ở lần mở phần mềm kế tiếp có mạng.'))act(o,'restore',{})}},'Khôi phục'))}
      if(o.status==='paid'){ops.append(el('button',{onclick:function(){act(o,'reissue',{machine:o.machine},function(r){showKey(r.key)})}},'Xem key'));ops.append(el('button',{onclick:function(){var m=prompt('Mã máy mới (XXXX-XXXX-XXXX):');if(m)act(o,'reissue',{machine:m},function(r){showKey(r.key);load()})}},'Đổi máy'))}
      tb.append(el('tr',{},el('td',{},el('code',{},'NL-'+o.code),el('div',{},new Date(o.created_at).toLocaleString('vi-VN'))),el('td',{},o.name,el('div',{},o.phone)),el('td',{},itemsCell(o,names)),el('td',{},money(o.amount),o.partner?el('div',{},'Mã '+o.partner.code+' · giảm '+o.partner.percent+'%'):null,o.paid_amount&&o.paid_amount!==o.amount?el('div',{},'đã nhận '+money(o.paid_amount)):null),el('td',{},el('span',{class:'st '+o.status},LBL[o.status]||o.status),o.revoked?el('div',{},el('span',{class:'st rv'},'Đã thu hồi'),el('div',{},(o.revoked.reason||'')+' ('+new Date(o.revoked.at).toLocaleString('vi-VN')+')')):null,o.note?el('div',{},o.note):null,o.reissues?el('div',{},'đã đổi máy '+o.reissues+' lần'):null),el('td',{},devCell(o)),el('td',{},ops)));
    });
    box.append(d.orders.length?tb:el('p',{},'Chưa có đơn.'));
    return api('GET','/api/admin/transactions');
  }).then(function(d){
    var box=document.getElementById('tx');box.replaceChildren();if(!d)return;
    var tb=el('table',{},el('tr',{},el('th',{},'Thời gian'),el('th',{},'Số tiền'),el('th',{},'Nội dung chuyển khoản'),el('th',{},'Kết quả'),el('th',{},'')));
    d.transactions.forEach(function(t){tb.append(el('tr',{},el('td',{},new Date(t.created_at).toLocaleString('vi-VN')),el('td',{},money(t.amount)),el('td',{},t.content||''),el('td',{},t.result+(t.order_code?' (NL-'+t.order_code+')':'')),el('td',{},t.order_code?'':el('button',{class:'p',onclick:function(){var c=prompt('Gắn giao dịch '+money(t.amount)+' vào đơn có mã (6 ký tự sau NL):');if(!c)return;api('POST','/api/admin/transactions/'+t.id+'/attach',{code:c.trim()}).then(function(r){if(r&&r.key)showKey(r.key);else if(r)alert('Đã gắn: '+r.status);load()}).catch(function(e){alert(e.message)})}},'Gắn vào đơn'))))});
    box.append(d.transactions.length?tb:el('p',{},'Không có.'));
  }).catch(function(e){msg.textContent=e.message});
}
document.getElementById('go').onclick=load;document.getElementById('rf').onclick=load;document.getElementById('st').onchange=load;
document.getElementById('q').onkeydown=function(e){if(e.key==='Enter')load()};
if(T.value){load();setInterval(function(){if(!document.hidden&&!msg.textContent)load()},30000)}
})();
</script></body></html>`;

export function adminPage() {
  const nonce = btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(16))));
  return new Response(PAGE.replaceAll('__N__', nonce), { headers: {
    'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store',
    'content-security-policy': `default-src 'none'; script-src 'nonce-${nonce}'; style-src 'nonce-${nonce}'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`,
    'x-content-type-options': 'nosniff', 'referrer-policy': 'no-referrer' } });
}
