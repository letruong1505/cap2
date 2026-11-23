// Trang quản trị đơn: một trang HTML, nhập mật khẩu quản trị (ADMIN_TOKEN) để xem đơn, duyệt tay, hủy, cấp lại key.
const PAGE = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quản trị đơn - Nam Linh Educenter</title>
<style nonce="__N__">
:root{--ink:#1c2733;--mut:#64748b;--line:#e2e8f0;--navy:#14304f;--blue:#2563eb;--red:#b42318;--bg:#f1f5f9}
*{box-sizing:border-box}
body{font:14.5px/1.55 "Segoe UI",system-ui,-apple-system,sans-serif;margin:0;background:var(--bg);color:var(--ink)}
header{position:sticky;top:0;z-index:5;background:linear-gradient(135deg,#0f2a47,#1d4a7a);color:#fff;padding:12px 28px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;box-shadow:0 2px 12px rgba(15,42,71,.25)}
header h1{font-size:17px;margin:0;flex:1;font-weight:700;letter-spacing:.2px}
header input{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.3);color:#fff}
header input::placeholder{color:rgba(255,255,255,.65)}
header button.p{background:#fff;color:var(--navy);border-color:#fff}
main{max-width:1400px;margin:0 auto;padding:22px 28px 48px}
input,select,button{font:inherit;padding:8px 12px;border-radius:10px;border:1px solid #cbd5e1;background:#fff;color:var(--ink);transition:border-color .15s,box-shadow .15s,background .15s}
input:focus,select:focus{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(37,99,235,.18)}
button{cursor:pointer;font-weight:600}
button:hover{background:#f1f5f9}
button.p{background:var(--navy);color:#fff;border-color:var(--navy)}button.p:hover{background:#1d4a7a}
button.d{color:var(--red);border-color:#f3c5c0;background:#fff}button.d:hover{background:#fef2f1;border-color:var(--red)}
button.sm{padding:1px 10px;font-size:12.5px;margin-left:8px;border-radius:99px}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:6px}
.bar input[type=text],.bar input:not([type]){min-width:280px}
.bar .inl{display:flex;align-items:center;gap:6px;font-weight:400;margin:0}
#recon .card{margin:8px 0}
table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:14px 0;box-shadow:0 1px 3px rgba(15,23,42,.06)}
th,td{padding:11px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:14px}
th{background:#f8fafc;color:var(--mut);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
tr:last-child td{border-bottom:0}
tbody tr:hover td,table tr:hover td{background:#fafcff}
.st{padding:2px 10px;border-radius:99px;font-size:12px;font-weight:700;display:inline-block;white-space:nowrap}
.on,.paid{background:#dcfce7;color:#166534}.off,.cancelled{background:#f1f5f9;color:#64748b}.rv{background:#fee2e2;color:#991b1b}.pending{background:#fef3c7;color:#92400e}.underpaid{background:#ffedd5;color:#9a3412}
.gone{text-decoration:line-through;color:#94a3b8}.it{margin:3px 0}
small{color:var(--mut)}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:0 1px 3px rgba(15,23,42,.06);margin-top:12px}
.card label{display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:700;color:var(--mut)}
.w90{width:96px}.w180{width:200px}
#msg{min-height:22px;color:var(--red);font-weight:600;margin:6px 0}
code{font:12.5px ui-monospace,Consolas,monospace;background:#f1f5f9;padding:1px 6px;border-radius:6px;word-break:break-all}
h2{margin:34px 0 0;font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px}
h2::before{content:"";width:4px;height:18px;border-radius:2px;background:var(--blue)}
</style></head><body>
<header><h1>Quản trị đơn - Nam Linh Educenter</h1><div class="row"><input id="tok" type="password" placeholder="Mật khẩu quản trị" autocomplete="off"><button class="p" id="go">Vào</button></div></header>
<main><div class="bar"><select id="st"><option value="">Tất cả trạng thái</option><option value="pending">Chờ thanh toán</option><option value="underpaid">Chuyển thiếu</option><option value="paid">Đã thanh toán</option><option value="cancelled">Đã hủy</option></select>
<input id="q" placeholder="Tìm tên, SĐT, mã đơn, mã máy"><select id="fp"><option value="">Tất cả đối tác</option></select><label class="inl">Từ ngày <input id="fd" type="date"></label><label class="inl">Đến ngày <input id="td" type="date"></label><button id="rf">Tải lại</button></div><div id="recon"></div><div id="msg" role="status"></div>
<div id="orders"></div><h2>Mã đối tác</h2><div class="card"><div class="row"><label>Mã<input id="pc" class="w180" placeholder="Ví dụ DT-HOAI" maxlength="20"></label><label>Đối tác<select id="pps" class="w180"><option value="">Chọn đối tác</option><option value="__new">+ Thêm đối tác mới…</option></select></label><label id="ppl" style="display:none">Tên đối tác mới<input id="pp" class="w180" placeholder="Tên đối tác" maxlength="60"></label><label>Giảm (%)<input id="pn" class="w90" type="number" value="20" min="1" max="100"></label><label>Số máy tối đa<input id="pm" class="w90" type="number" value="10" min="1" max="1000"></label><button class="p" id="pcAdd">Tạo mã</button></div><div style="margin-top:10px"><b>Áp dụng cho khóa học</b> <span class="muted">(không tick = áp dụng mọi khóa; mã giảm 100% bắt buộc tick ít nhất một khóa)</span><div id="pi" style="margin-top:6px"></div></div></div><div id="partners"></div><h2>Giao dịch chưa khớp đơn hoặc cần xử lý</h2><div id="tx"></div></main>
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
  o.devices.forEach(function(d){c.append(el('div',{},el('code',{},d.machine),' ',d.platform?el('small',{},d.platform==='android'?'Điện thoại':'Máy tính'):null,' ',d.stranger?el('span',{class:'st rv'},'Máy lạ'):null,' ',el('span',{class:'st '+(d.online?'on':'off')},d.online?'Đang online':'Offline'),el('div',{},(d.online?'Bản '+(d.version||'?')+', đang mở phần mềm':'Mở gần nhất '+new Date(d.last_seen).toLocaleString('vi-VN')+(d.version?', bản '+d.version:'')))))});
  c.append(el('div',{},'Máy tính: ',o.slots&&o.slots.win?el('code',{},o.slots.win.machine):'chưa cấp'));c.append(el('div',{},'Điện thoại: ',o.slots&&o.slots.android?el('code',{},o.slots.android.machine):'chưa cấp'));
  return c}
function itemsCell(o,names){
  var c=el('div',{});
  JSON.parse(o.items).forEach(function(id){
    var nm=CAT[id]?CAT[id].name:id,rv=(o.item_revoked||[]).filter(function(r){return r.item===id})[0],row=el('div',{class:'it'});
    if(rv){
      row.append(el('span',{class:'gone'},nm),' ',el('span',{class:'st rv'},'Đã thu hồi'),el('button',{class:'p sm',onclick:function(){if(confirm('Khôi phục khóa học "'+nm+'" của đơn '+o.code+'?'))api('POST','/api/admin/orders/'+o.code+'/restore',{item:id}).then(load).catch(function(e){msg.textContent=e.message})}},'Khôi phục'));
      if(rv.reason)row.append(el('div',{},rv.reason+' ('+new Date(rv.at).toLocaleString('vi-VN')+')'))
    }else{
      row.append(nm);if(o.prices&&o.prices[id])row.append(el('small',{},' · đã trả '+money(o.prices[id].paid)));
      if(o.status==='paid'&&!o.revoked&&refundOpen(o))row.append(el('button',{class:'d sm',onclick:function(){var x=prompt('THU HỒI RIÊNG khóa học "'+nm+'" của '+o.name+' ('+o.phone+'), đơn '+money(o.amount)+'.\\nCác khóa khác trong đơn vẫn dùng bình thường.\\nGõ lại mã đơn '+o.code+' để xác nhận:');if(x===null)return;if(x.trim().toUpperCase().replace(/^NL-/,'')!==o.code){alert('Mã đơn không khớp, chưa thu hồi.');return}var r=prompt('Lý do (hoàn tiền một phần...):','Hoàn tiền một phần');if(r===null)return;api('POST','/api/admin/orders/'+o.code+'/revoke',{item:id,reason:r}).then(load).catch(function(e){msg.textContent=e.message})}},'Thu hồi'))
    }
    c.append(row)});
  return c}
function showKey(k){window.prompt('Khóa kích hoạt (sao chép):',k)}
function refundOpen(o){return !!o.paid_at&&Date.now()-new Date(o.paid_at).getTime()<=7*864e5}
function fillSel(sel,names,first,extra){var cur=sel.value;sel.replaceChildren(el('option',{value:''},first));names.forEach(function(n){sel.append(el('option',{value:n},n))});extra.forEach(function(x){sel.append(el('option',{value:x[0]},x[1]))});if(Array.prototype.some.call(sel.options,function(o){return o.value===cur}))sel.value=cur}
function syncNew(){document.getElementById('ppl').style.display=document.getElementById('pps').value==='__new'?'':'none'}
function loadPartners(){
  api('GET','/api/admin/partner-codes').then(function(d){
    var box=document.getElementById('partners');box.replaceChildren();
    var tb=el('table',{},el('tr',{},el('th',{},'Mã'),el('th',{},'Đối tác'),el('th',{},'Giảm'),el('th',{},'Áp dụng cho'),el('th',{},'Máy đã dùng'),el('th',{},'Trạng thái'),el('th',{},'Số đơn đã dùng'),el('th',{},'')));
    d.partners.forEach(function(p){
      tb.append(el('tr',{},el('td',{},el('code',{},p.code)),el('td',{},p.partner),el('td',{},p.percent+'%'),el('td',{},p.items?p.items.split(',').map(function(i){return d.catalog&&d.catalog[i]?d.catalog[i].name:i}).join(', '):'Tất cả khóa'),el('td',{},(p.machines||0)+'/'+(p.max_machines||'∞')+' máy'),el('td',{},el('span',{class:'st '+(p.active?'on':'off')},p.active?'Đang bật':'Đã tắt')),el('td',{},String(p.used||0)),el('td',{},el('button',{onclick:function(){if(!confirm((p.active?'Tắt':'Bật')+' mã '+p.code+'?'))return;api('POST','/api/admin/partner-codes/'+encodeURIComponent(p.code)+'/active',{active:!p.active}).then(loadPartners).catch(function(e){msg.textContent=e.message})}},p.active?'Tắt':'Bật'))));
    });
    box.append(d.partners.length?tb:el('p',{},'Chưa có mã đối tác.'));
    api('GET','/api/admin/partner-links').then(function(r){
      if(!r.links.length)return;
      var lt=el('table',{},el('tr',{},el('th',{},'Đối tác'),el('th',{},'Liên kết xem số lượng active (gửi riêng cho đối tác)')));
      r.links.forEach(function(x){var u=location.origin+'/doi-tac#'+x.token;lt.append(el('tr',{},el('td',{},x.partner),el('td',{},el('code',{},u),el('button',{class:'sm',onclick:function(){(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){msg.textContent='Đã sao chép liên kết của '+x.partner}).catch(function(){window.prompt('Sao chép liên kết:',u)})}},'Sao chép'))))});
      box.append(el('h2',{},'Liên kết cho đối tác'),lt)
    }).catch(function(){});
    var names=[];d.partners.forEach(function(p){if(names.indexOf(p.partner)<0)names.push(p.partner)});names.sort(function(a,b){return a.localeCompare(b,'vi')});
    fillSel(document.getElementById('pps'),names,'Chọn đối tác',[['__new','+ Thêm đối tác mới…']]);
    fillSel(document.getElementById('fp'),names,'Tất cả đối tác',[]);
    syncNew();
    var pi=document.getElementById('pi');
    if(!pi.children.length&&d.catalog){Object.keys(d.catalog).forEach(function(id){var c=el('input',{type:'checkbox',value:id,class:'pick'});pi.append(el('label',{style:'display:inline-block;margin:0 14px 6px 0;font-weight:400'},c,' '+d.catalog[id].name+' ('+money(d.catalog[id].price)+')'))})}
  }).catch(function(e){msg.textContent=e.message});
}
document.getElementById('pcAdd').onclick=function(){
  api('POST','/api/admin/partner-codes',{code:document.getElementById('pc').value,partner:(document.getElementById('pps').value==='__new'?document.getElementById('pp').value:document.getElementById('pps').value),percent:Number(document.getElementById('pn').value),maxMachines:Number(document.getElementById('pm').value),items:Array.prototype.map.call(document.querySelectorAll('#pi input:checked'),function(c){return c.value})})
    .then(function(){document.getElementById('pc').value='';document.getElementById('pp').value='';document.getElementById('pps').value='';syncNew();Array.prototype.forEach.call(document.querySelectorAll('#pi input'),function(c){c.checked=false});loadPartners()})
    .catch(function(e){msg.textContent=e.message});
};
function load(){
  msg.textContent='';
  loadPartners();
  try{sessionStorage.setItem('nl-admin',T.value)}catch(e){}
  var u='/api/admin/orders?status='+encodeURIComponent(document.getElementById('st').value)+'&q='+encodeURIComponent(document.getElementById('q').value)+'&partner='+encodeURIComponent(document.getElementById('fp').value)+'&from='+encodeURIComponent(document.getElementById('fd').value)+'&to='+encodeURIComponent(document.getElementById('td').value);
  api('GET',u).then(function(d){
    CAT=d.catalog;var box=document.getElementById('orders');box.replaceChildren();
    var tb=el('table',{},el('tr',{},el('th',{},'Mã đơn'),el('th',{},'Phụ huynh'),el('th',{},'Khóa học'),el('th',{},'Tiền'),el('th',{},'Trạng thái'),el('th',{},'Máy đã dùng'),el('th',{},'Thao tác')));
    d.orders.forEach(function(o){
      var names=JSON.parse(o.items).map(function(i){return CAT[i]?CAT[i].name:i}).join(', ');
      var ops=el('div',{class:'row'});
      if(o.status!=='paid'&&o.status!=='cancelled'){ops.append(el('button',{class:'p',onclick:function(){if(confirm('Xác nhận đã nhận đủ tiền và cấp key cho '+o.code+'?'))act(o,'approve',{note:'Duyệt tay'},function(r){showKey(r.key);load()})}},'Duyệt tay'));ops.append(el('button',{class:'d',onclick:function(){if(confirm('Hủy đơn '+o.code+'?'))act(o,'cancel',{})}},'Hủy'))}
      if(o.status==='paid'&&!o.revoked&&refundOpen(o)){ops.append(el('button',{class:'d',onclick:function(){var c=prompt('THU HỒI khóa của '+o.name+' ('+o.phone+'), '+names+', '+money(o.amount)+'.\\nGõ lại mã đơn '+o.code+' để xác nhận:');if(c===null)return;if(c.trim().toUpperCase().replace(/^NL-/,'')!==o.code){alert('Mã đơn không khớp, chưa thu hồi.');return}var r=prompt('Lý do thu hồi (hoàn tiền, vi phạm...):','Hoàn tiền');if(r===null)return;act(o,'revoke',{reason:r})}},'Thu hồi'))}
      if(o.revoked){ops.append(el('button',{class:'p',onclick:function(){if(confirm('Khôi phục khóa của đơn '+o.code+'? Máy khách dùng lại được ở lần mở phần mềm kế tiếp có mạng.'))act(o,'restore',{})}},'Khôi phục'))}
      if(o.status==='paid'){ops.append(el('button',{onclick:function(){act(o,'reissue',{machine:o.machine},function(r){showKey(r.key)})}},'Xem key'));ops.append(el('button',{onclick:function(){var m=prompt('Mã máy tính mới (XXXX-XXXX-XXXX):');if(m)act(o,'reissue',{machine:m,platform:'win'},function(r){showKey(r.key);load()})}},'Đổi máy tính'));ops.append(el('button',{onclick:function(){var m=prompt('Mã điện thoại (XXXX-XXXX-XXXX):');if(m)act(o,'reissue',{machine:m,platform:'android'},function(r){showKey(r.key);load()})}},'Cấp/đổi điện thoại'))}
      tb.append(el('tr',{},el('td',{},el('code',{},'NL-'+o.code),el('div',{},new Date(o.created_at).toLocaleString('vi-VN'))),el('td',{},o.name,el('div',{},o.phone)),el('td',{},itemsCell(o,names)),el('td',{},money(o.amount),o.partner?el('div',{},'Mã '+o.partner.code+' · giảm '+o.partner.percent+'%'):null,o.paid_amount&&o.paid_amount!==o.amount?el('div',{},'đã nhận '+money(o.paid_amount)):null),el('td',{},el('span',{class:'st '+o.status},LBL[o.status]||o.status),o.revoked?el('div',{},el('span',{class:'st rv'},'Đã thu hồi'),el('div',{},(o.revoked.reason||'')+' ('+new Date(o.revoked.at).toLocaleString('vi-VN')+')')):null,o.note?el('div',{},o.note):null,o.reissues?el('div',{},'đã đổi máy '+o.reissues+' lần'):null),el('td',{},devCell(o)),el('td',{},ops)));
    });
    box.append(d.orders.length?tb:el('p',{},'Chưa có đơn.'));
    renderRecon(d.orders);
    return api('GET','/api/admin/transactions');
  }).then(function(d){
    var box=document.getElementById('tx');box.replaceChildren();if(!d)return;
    var tb=el('table',{},el('tr',{},el('th',{},'Thời gian'),el('th',{},'Số tiền'),el('th',{},'Nội dung chuyển khoản'),el('th',{},'Kết quả'),el('th',{},'')));
    d.transactions.forEach(function(t){tb.append(el('tr',{},el('td',{},new Date(t.created_at).toLocaleString('vi-VN')),el('td',{},money(t.amount)),el('td',{},t.content||''),el('td',{},t.result+(t.order_code?' (NL-'+t.order_code+')':'')),el('td',{},t.order_code?'':el('button',{class:'p',onclick:function(){var c=prompt('Gắn giao dịch '+money(t.amount)+' vào đơn có mã (6 ký tự sau NL):');if(!c)return;api('POST','/api/admin/transactions/'+t.id+'/attach',{code:c.trim()}).then(function(r){if(r&&r.key)showKey(r.key);else if(r)alert('Đã gắn: '+r.status);load()}).catch(function(e){alert(e.message)})}},'Gắn vào đơn'))))});
    box.append(d.transactions.length?tb:el('p',{},'Không có.'));
  }).catch(function(e){msg.textContent=e.message});
}
var RATE={};
function renderRecon(orders){
  var box=document.getElementById('recon');box.replaceChildren();
  var who=document.getElementById('fp').value;if(!who)return;
  var n=0,list=0,paid=0,items=0;
  orders.forEach(function(o){
    if(o.status!=='paid'||o.revoked)return;
    var gone={};(o.item_revoked||[]).forEach(function(r){gone[r.item]=1});var any=false;
    Object.keys(o.prices||{}).forEach(function(id){var p=o.prices[id];if(!p.partner_code||gone[id])return;any=true;items++;list+=p.list;paid+=p.paid});
    if(any)n++;
  });
  var pct=el('input',{type:'number',min:'0',max:'100',value:RATE[who]===undefined?'':RATE[who],placeholder:'%',style:'width:80px'});
  var out=el('b',{});
  function calc(){var r=Number(pct.value);RATE[who]=pct.value;out.textContent=pct.value===''||!(r>=0)?'—':money(Math.round(paid*r/100))}
  pct.oninput=calc;calc();
  box.append(el('div',{class:'card'},el('div',{},el('b',{},'Đối soát đối tác: '+who)),
    el('div',{},n+' đơn đã thanh toán (không tính đơn đã thu hồi hoặc khóa bị thu hồi), '+items+' khóa. Giá niêm yết '+money(list)+', khách thực trả '+money(paid)+'.'),
    el('div',{class:'row',style:'margin-top:8px'},el('span',{},'Hoa hồng (%) trên số thực trả: '),pct,el('span',{},' = '),out),
    el('div',{class:'muted'},'Chọn khoảng ngày để đối soát theo kỳ. Tỉ lệ hoa hồng chỉ để tính tại đây, không lưu trên máy chủ.')));
}
['fp','fd','td'].forEach(function(id){document.getElementById(id).onchange=load});
document.getElementById('pps').onchange=syncNew;
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
